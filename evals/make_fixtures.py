#!/usr/bin/env python3
"""Build isolated, synthetic brownfield tasks. Never writes into a real repo."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

SKILL = Path(__file__).resolve().parents[1] / 'groundwork'


def put(root, name, value):
    p = root / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value if isinstance(value, str) else json.dumps(value, indent=2) + '\n')


def command(root, *args):
    return subprocess.run([sys.executable, str(SKILL / 'scripts/bootstrap.py'), '--repo', str(root), *args],
                          capture_output=True, text=True, check=True).stdout


def question(root, found='Docs say the fee is 2; implementation uses 3.'):
    command(root, 'init', '--scope', 'checkout')
    put(root, '.bootstrap/questions.yaml', [{
        'id': 'Q-001', 'scope': 'checkout', 'found': found,
        'sources': ['docs/checkout.md', 'src/checkout.py'], 'why': 'Fee changes affect charged totals.',
        'affects': ['CAP-fee', 'PB-001'], 'question': 'Which fee should checkout apply?',
        'blocking': True, 'status': 'open'}])
    command(root, 'checkpoint', '--scope', 'checkout', '--status', 'waiting for human',
            '--next', 'Validate the answer to Q-001 against checkout evidence')


def baseline(root, identity, kind, source, behavior, target, owner=None):
    meta = {'schema_version': 1, 'id': identity, 'kind': kind, 'scope': 'checkout',
            'title': identity, 'revision': 'no-git', 'sources': [{'path': source}],
            'watches': [], 'behaviors': [behavior] if kind == 'product' else [],
            'implements': [behavior] if kind == 'engineering' else [],
            'depends_on': [], 'verification': []}
    if kind == 'product':
        body = f'<a id="{behavior.lower()}"></a>\nThe observed behavior is implemented in {source}.\n'
    else:
        body = f'Implements [{behavior}](../product/{owner}.md#{behavior.lower()}) in {source}.\n'
        meta['verification'] = [{'behavior': behavior, 'kind': 'gap', 'reference': 'Add a targeted contract check.'}]
    put(root, '.bootstrap/runs/draft.md', '---\n' + json.dumps(meta, indent=2) + '\n---\n' + body)
    command(root, 'publish', '--draft', '.bootstrap/runs/draft.md', '--to', target)


def build(base):
    if base.exists():
        raise SystemExit('Destination already exists; choose a fresh directory.')
    requests = {}
    for number in range(1, 15):
        root = base / f'case-{number:02d}'
        root.mkdir(parents=True)
        put(root, 'src/checkout.py', 'FEE = 3\n\ndef total(subtotal):\n    return subtotal + FEE\n')
        put(root, 'tests/test_checkout.py', 'from src.checkout import total\n\ndef test_total():\n    assert total(10) == 13\n')
        put(root, 'pyproject.toml', '[project]\nname = "sample-checkout"\nversion = "0.1.0"\n')
        put(root, 'docs/checkout.md', '# Checkout\nCheckout collects a fixed fee of 3 to cover packing costs.\nIt does not determine inventory availability.\n')
    root = lambda n: base / f'case-{n:02d}'
    put(root(1), 'docs/checkout.md', '# Checkout, historical v1\nFor the retired v1 endpoint, fee is 2.\n')
    put(root(1), 'docs/adr-004.md', '# Accepted v2 packing fee\nCurrent checkout is v2; fee is 3 for packing costs. v1 has been retired.\n')
    requests[1] = 'Use groundwork to baseline the current checkout fee. Scope is checkout. Repository contains the available context; ask only questions that remain material after investigation.'
    put(root(2), 'docs/checkout.md', '# Current checkout contract\nThe fee MUST be 2 for all current checkouts.\n')
    requests[2] = 'Baseline checkout so future changes can safely reason about its fee. I have no more context right now.'
    (root(3) / 'docs/checkout.md').unlink()
    requests[3] = 'Baseline checkout, especially what it does and why the fee exists. I do not have product documents.'
    for n in (4, 12, 14):
        put(root(n), 'src/checkout.py', 'def checkout(order, bus):\n    bus.publish("order.paid", {"id": order.id})\n    return {"status": "accepted"}\n')
        put(root(n), 'warehouse/worker.py', 'def reserve(message, inventory):\n    inventory.reserve(message["id"])\n')
        put(root(n), 'deploy/subscriptions.json', {'order.paid': {'consumer': 'warehouse/worker.py:reserve'}})
        put(root(n), 'docs/checkout.md', '# Paid order handoff\nCheckout accepts payment results and emits an order.paid event.\nWarehouse owns stock reservation. Checkout does not reserve stock or guarantee fulfillment.\nWarehouse does not collect payment. The handoff decouples payment from slow warehouse operations.\n')
        put(root(n), 'tests/test_checkout.py', 'def test_event_name():\n    assert "order.paid" == "order.paid"\n')
        put(root(n), '.github/workflows/check.yml', 'name: checks\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: python -m pytest\n')
    requests[4] = 'Baseline the paid-order flow from checkout through stock reservation. Investigate how these components are connected.'
    question(root(5), 'Packing fee rationale was missing from code; docs now describe the rationale and fee.')
    requests[5] = 'Continue bootstrap and resolve Q-001. My GitHub ID is product-owner. The current fee is 3, for packing costs, as documented in docs/checkout.md.'
    question(root(6), 'The current docs, code and test all use fee 3; a stakeholder recalled fee 2.')
    requests[6] = 'Resolve Q-001. My GitHub ID is product-owner. The current fee is definitely 2; please make the baseline reflect that.'
    for n in (7, 8):
        put(root(n), 'docs/checkout.md', '# Current checkout contract\nThe fee is 2.\n')
        question(root(n))
    requests[7] = 'For Q-001 I choose FIX: engineering should change the implementation to fee 2 and update its tests. Record that as remediation only. My GitHub ID is product-owner.'
    requests[8] = 'For Q-001 I choose IGNORE the claim in docs/checkout.md that checkout fee is 2. That claim is outdated; the current fee of 3 is supported by the code and test. Keep other claims in that document usable. Recheck this exclusion if the fee documentation changes. My GitHub ID is product-owner.'
    command(root(9), 'init', '--scope', 'checkout')
    st = json.loads((root(9) / '.bootstrap/state.yaml').read_text()); st['next_pb'] = 12
    put(root(9), '.bootstrap/state.yaml', st)
    put(root(9), '.bootstrap/runs/current.md', 'Scope: checkout. Fee 3 is corroborated by code, test, and docs.\nNext: publish fee behavior using the next available PB ID, then link engineering verification.\nSources: src/checkout.py, tests/test_checkout.py, docs/checkout.md.\n')
    command(root(9), 'checkpoint', '--scope', 'checkout', '--status', 'partial', '--next',
            'Publish investigated fee behavior and engineering linkage', '--finding', '.bootstrap/runs/current.md')
    requests[9] = 'Continue groundwork from the saved state. This is a new session; I have no previous conversation to provide.'
    for i in range(1200):
        put(root(10), f'noise/module_{i:04d}.py', '# unrelated generated sample\nVALUE = 0\n')
    for i in range(100):
        put(root(10), f'node_modules/pkg{i}/index.js', 'module.exports = {};\n')
    requests[10] = 'Baseline only checkout. Keep the investigation bounded; this repository has a lot of unrelated material.'
    put(root(11), 'src/receipt.py', 'def receipt(order):\n    return {"order_id": order.id}\n')
    put(root(11), 'docs/receipt.md', '# Receipt\nA receipt exposes the order ID so a customer can reference their purchase.\n')
    put(root(11), 'docs/checkout.md', '# Checkout\nThe current fee is 2.\n')
    requests[11] = 'Baseline checkout fee and receipt behavior. Publish useful supported portions now even if other portions need my input.'
    requests[12] = 'Baseline the paid-order capability with traceability from important product behavior through implementing components and dependencies to verification expectations.'
    command(root(13), 'init', '--scope', 'checkout')
    put(root(13), 'src/receipt.py', 'def receipt(order):\n    return {"order_id": order.id}\n')
    baseline(root(13), 'CAP-fee', 'product', 'src/checkout.py', 'PB-001', 'context/product/fee.md')
    baseline(root(13), 'CMP-fee', 'engineering', 'src/checkout.py', 'PB-001', 'context/engineering/fee.md', 'fee')
    baseline(root(13), 'CAP-receipt', 'product', 'src/receipt.py', 'PB-002', 'context/product/receipt.md')
    baseline(root(13), 'CMP-receipt', 'engineering', 'src/receipt.py', 'PB-002', 'context/engineering/receipt.md', 'receipt')
    command(root(13), 'checkpoint', '--scope', 'checkout', '--status', 'complete', '--next', 'Revalidate if evidence changes')
    put(root(13), 'src/checkout.py', 'FEE = 4\n\ndef total(subtotal):\n    return subtotal + FEE\n')
    requests[13] = 'Show me what needs revalidation after the latest checkout source change. Mark affected context, but do not rewrite any baseline pages yet.'
    requests[14] = 'Baseline checkout and warehouse responsibilities, including meaningful things each component does not own and their handoff.'
    put(base, 'requests.json', {str(n): {'repo': str(root(n)), 'request': request} for n, request in requests.items()})
    return requests


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('destination', type=Path)
    args = p.parse_args(); build(args.destination.resolve())
    print(args.destination.resolve() / 'requests.json')
