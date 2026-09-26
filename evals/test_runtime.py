"""Observable invariants for the portable helper; runtime skill has no eval code."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'groundwork/scripts/bootstrap.py'
spec = importlib.util.spec_from_file_location('bootstrap', SCRIPT)
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='bootstrap-eval-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.cli('init', '--scope', 'checkout')
        self.put('src/fee.py', 'FEE = 3\n')
        self.put('src/receipt.py', 'RECEIPT = True\n')

    def put(self, path, value):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(value if isinstance(value, str) else json.dumps(value))

    def get(self, path):
        return json.loads((self.root / path).read_text())

    def cli(self, *args, ok=True):
        p = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(self.root), *args], capture_output=True, text=True)
        if ok:
            self.assertEqual(p.returncode, 0, p.stderr)
            return json.loads(p.stdout)
        self.assertNotEqual(p.returncode, 0, p.stdout)
        return p.stderr

    def publish(self, name='fee', number=1, kind='product', source=None, deps=None, watches=None, mutate=None, ok=True):
        pb = f'PB-{number:03d}'
        meta = {'schema_version': 1, 'id': ('CAP-' if kind == 'product' else 'CMP-') + name,
                'kind': kind, 'scope': 'checkout', 'title': name, 'revision': 'working-tree',
                'sources': [{'path': source or 'src/' + name + '.py'}], 'watches': watches or [],
                'behaviors': [pb] if kind == 'product' else [],
                'implements': [pb] if kind == 'engineering' else [], 'depends_on': deps or [],
                'verification': [] if kind == 'product' else [{'behavior': pb, 'kind': 'gap', 'reference': 'contract check needed'}]}
        body = f'<a id="{pb.lower()}"></a>\nObserved behavior in source.\n' if kind == 'product' else f'Implements [{pb}](../product/{name}.md#{pb.lower()}).\n'
        if mutate:
            meta, body = mutate(meta, body)
        self.put('.bootstrap/runs/draft.md', '---\n' + json.dumps(meta) + '\n---\n' + body)
        return self.cli('publish', '--draft', '.bootstrap/runs/draft.md', '--to', f'context/{kind}/{name}.md', ok=ok)

    def questions(self, affects=None):
        self.put('.bootstrap/questions.yaml', [{
            'id': 'Q-001', 'scope': 'checkout', 'found': 'Code and docs disagree', 'sources': ['src/fee.py'],
            'why': 'Wrong amount charged', 'affects': affects or ['PB-001'],
            'question': 'Which rule is intended?', 'blocking': True, 'status': 'conflicting'}])

    def test_resume_preserves_ids_and_checkpoint(self):
        self.cli('allocate-pb')
        self.put('.bootstrap/runs/finding.md', 'Compact finding')
        self.cli('checkpoint', '--scope', 'checkout', '--status', 'partial', '--next', 'Trace event', '--finding', '.bootstrap/runs/finding.md')
        before = self.get('.bootstrap/state.yaml')
        self.cli('init', '--scope', 'checkout')
        self.assertEqual(before, self.get('.bootstrap/state.yaml'))
        self.assertEqual(self.cli('allocate-pb')['behavior'], 'PB-002')

    def test_scope_expansion_preserves_old_scope(self):
        before = self.get('.bootstrap/state.yaml')['scopes']['checkout']
        self.cli('init', '--scope', 'inventory')
        self.assertEqual(before, self.get('.bootstrap/state.yaml')['scopes']['checkout'])

    def test_changed_source_invalidates_only_related_pages(self):
        self.publish(); self.publish(kind='engineering'); self.publish('receipt', 2)
        before = (self.root / 'context/product/receipt.md').read_bytes()
        self.put('src/fee.py', 'FEE = 4\n')
        out = self.cli('freshness')['pages']
        self.assertEqual(out['context/product/fee.md']['status'], 'needs revalidation')
        self.assertEqual(out['context/engineering/fee.md']['status'], 'needs revalidation')
        self.assertEqual(out['context/product/receipt.md']['status'], 'current')
        self.assertEqual(before, (self.root / 'context/product/receipt.md').read_bytes())

    def test_removed_source_does_not_refresh_trust(self):
        self.publish(); (self.root / 'src/fee.py').unlink()
        self.assertEqual(self.cli('freshness')['pages']['context/product/fee.md']['status'], 'needs revalidation')
        self.publish(ok=False)

    def test_watch_detects_new_hidden_consumer(self):
        self.put('services/existing/subscriptions.json', '{}')
        self.publish(watches=['services/**/subscriptions.json'])
        self.put('services/new/deep/worker/subscriptions.json', '{"order.paid": "consumer"}')
        self.assertEqual(self.cli('freshness')['pages']['context/product/fee.md']['status'], 'needs revalidation')

    def test_watch_zero_directory_glob(self):
        self.publish(watches=['src/**/*.py'])
        self.put('src/new.py', '# new consumer')
        self.assertEqual(self.cli('freshness')['pages']['context/product/fee.md']['status'], 'needs revalidation')

    def test_nested_context_package_is_real_evidence(self):
        self.put('src/context/route.py', 'ROUTE = 1')
        self.publish(watches=['src/**/*.py'])
        self.put('src/context/route.py', 'ROUTE = 2')
        self.assertEqual(self.cli('freshness')['pages']['context/product/fee.md']['status'], 'needs revalidation')

    def test_revalidated_scope_returns_to_partial_not_stale(self):
        self.publish()
        self.cli('invalidate', '--ids', 'CAP-fee', '--reason', 'New evidence')
        self.assertEqual(self.get('.bootstrap/state.yaml')['scopes']['checkout']['status'], 'needs revalidation')
        self.publish()
        self.assertEqual(self.get('.bootstrap/state.yaml')['scopes']['checkout']['status'], 'partial')

    def test_material_question_blocks_only_affected_publication(self):
        self.questions(); self.publish(ok=False); self.publish('receipt', 2)
        self.assertFalse((self.root / 'context/product/fee.md').exists())

    def test_manual_page_edit_is_untrusted(self):
        self.publish()
        p = self.root / 'context/product/fee.md'; p.write_text(p.read_text() + 'Unreviewed assertion.\n')
        self.assertEqual(self.cli('index')['pages']['context/product/fee.md']['status'], 'needs revalidation')

    def test_fix_never_changes_application_or_resolves_question(self):
        self.questions(); before = (self.root / 'src/fee.py').read_bytes()
        self.cli('decision', '--question', 'Q-001', '--choice', 'FIX', '--statement', 'Please fix fee', '--action', 'Correct fee', '--github-id', 'owner')
        self.assertEqual(before, (self.root / 'src/fee.py').read_bytes())
        self.assertEqual(self.get('.bootstrap/remediation.yaml')[0]['status'], 'open')
        self.assertEqual(self.get('.bootstrap/questions.yaml')[0]['status'], 'conflicting')
        self.publish(ok=False)

    def test_ignore_is_scoped_and_source_changes_require_review(self):
        self.publish(); self.questions()
        self.cli('decision', '--question', 'Q-001', '--choice', 'IGNORE', '--statement', 'Ignore fee claim',
                 '--source', 'src/fee.py', '--claim', 'Fee is intended to be 3', '--rationale', 'Old rule', '--recheck-when', 'Source changes')
        self.assertEqual(self.get('.bootstrap/exclusions.yaml')[0]['claim'], 'Fee is intended to be 3')
        self.assertEqual(self.get('context/index.yaml')['documents'][0]['freshness'], 'needs revalidation')
        self.put('src/fee.py', 'FEE = 4')
        self.cli('freshness')
        self.assertEqual(self.get('.bootstrap/exclusions.yaml')[0]['status'], 'needs review')

    def test_external_revision_expiry_and_selectivity(self):
        self.put('.bootstrap/external.yaml', {'intent': {'label': 'Requirement', 'location': 'doc:1', 'revision': 'v1', 'review_after': '2999-01-01'}})
        def external(meta, body):
            meta['sources'] = [{'external': 'intent'}]
            return meta, body
        self.publish(mutate=external); self.publish('receipt', 2)
        ext = self.get('.bootstrap/external.yaml'); ext['intent']['review_after'] = '2000-01-01'
        self.put('.bootstrap/external.yaml', ext)
        out = self.cli('freshness')['pages']
        self.assertEqual(out['context/product/fee.md']['status'], 'needs revalidation')
        self.assertEqual(out['context/product/receipt.md']['status'], 'current')
        self.publish(mutate=external, ok=False)

    def test_traceability_requires_product_anchor_and_verification(self):
        self.publish(kind='engineering', ok=False)
        self.publish()
        self.publish(kind='engineering', mutate=lambda m, b: (dict(m, verification=[]), b), ok=False)
        self.publish(kind='engineering', mutate=lambda m, b: (m, 'No product link'), ok=False)
        self.publish(kind='engineering'); self.cli('check')

    def test_complete_requires_linked_fresh_scope(self):
        self.publish()
        self.cli('checkpoint', '--scope', 'checkout', '--status', 'complete', '--next', 'Done', ok=False)
        self.publish(kind='engineering')
        self.cli('checkpoint', '--scope', 'checkout', '--status', 'complete', '--next', 'Check if sources change')
        self.put('src/fee.py', 'FEE = 5')
        self.cli('checkpoint', '--scope', 'checkout', '--status', 'complete', '--next', 'Done', ok=False)

    def test_missing_tracking_fails_closed(self):
        self.publish(); self.put('.bootstrap/tracking.yaml', {})
        self.assertEqual(self.cli('freshness')['pages']['context/product/fee.md']['status'], 'needs revalidation')

    def test_dependency_propagation_and_revalidation(self):
        self.publish(); self.publish('receipt', 2, deps=['CAP-fee'])
        self.cli('invalidate', '--ids', 'CAP-fee', '--reason', 'New evidence')
        self.assertEqual(self.get('context/index.yaml')['documents'][1]['freshness'], 'needs revalidation')
        self.publish()
        # Unchanged upstream conclusion means the dependent page can remain valid.
        self.assertEqual(self.cli('freshness')['pages']['context/product/receipt.md']['status'], 'current')

    def test_changed_dependency_doc_invalidates_even_when_republished(self):
        self.publish(); self.publish('receipt', 2, deps=['CAP-fee'])
        self.publish(mutate=lambda m, b: (m, b + 'New supported interpretation.\n'))
        self.assertEqual(self.cli('freshness')['pages']['context/product/receipt.md']['status'], 'needs revalidation')

    def test_cyclic_dependencies_can_recover(self):
        self.publish(deps=['CAP-receipt']); self.publish('receipt', 2, deps=['CAP-fee'])
        self.publish(deps=['CAP-receipt'])
        out = self.cli('freshness')['pages']
        self.assertTrue(all(p['status'] == 'current' for p in out.values()), out)

    def test_bounded_scan_skips_dependencies_and_marks_truncation(self):
        for n in range(80):
            self.put(f'noise/file{n}.py', '# unrelated')
        self.put('node_modules/huge/pkg.js', 'secret payload')
        out = self.cli('scan', '--limit', '5')
        self.assertTrue(out['paths_truncated'])
        self.assertEqual(len(out['paths']), 5)
        self.assertFalse(any('node_modules' in p for p in out['paths']))
        self.assertNotIn('secret payload', json.dumps(out))
        files, incomplete, visited = bootstrap.walk(self.root, budget=10)
        self.assertTrue(incomplete); self.assertLessEqual(visited, 10)

    def test_path_escape_and_symlink_writes_rejected(self):
        self.cli('scan', '--within', '../outside', ok=False)
        (self.root / 'context').symlink_to(self.tmp.name)
        self.publish(ok=False)

    def test_lock_and_unknown_schema_preserve_state(self):
        self.put('.bootstrap/.lock', '123')
        before = (self.root / '.bootstrap/state.yaml').read_bytes()
        self.cli('allocate-pb', ok=False)
        self.assertEqual(before, (self.root / '.bootstrap/state.yaml').read_bytes())
        (self.root / '.bootstrap/.lock').unlink()
        self.put('.bootstrap/state.yaml', {'schema_version': 99, 'keep': True})
        self.cli('init', '--scope', 'checkout', ok=False)
        self.assertEqual(self.get('.bootstrap/state.yaml'), {'schema_version': 99, 'keep': True})

    def test_decision_interruption_recovers_without_duplicate(self):
        self.questions()
        args = ('decision', '--question', 'Q-001', '--choice', 'FIX', '--statement', 'Fix it', '--action', 'Fix fee')
        self.cli(*args)
        qs = self.get('.bootstrap/questions.yaml'); qs[0].pop('decision')
        self.put('.bootstrap/questions.yaml', qs)
        self.cli(*args)
        self.assertEqual(len(self.get('.bootstrap/remediation.yaml')), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
