#!/usr/bin/env python3
"""Bounded discovery and baseline bookkeeping. Python standard library only."""
import argparse
from contextlib import contextmanager
from datetime import date
import fnmatch
from functools import lru_cache
import hashlib
import itertools
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

STATUSES = ('not started', 'partial', 'waiting for human', 'needs revalidation', 'complete')
SKIP = {'.git', '.hg', '.svn', 'node_modules', 'vendor',
        '.venv', 'venv', '__pycache__', 'dist', 'build', 'target', '.next', '.cache'}
PB = re.compile(r'PB-[0-9]{3,}$')
SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*$')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def safe(root, name):
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '\\' in name:
        raise ValueError('Expected a repository-relative POSIX path: ' + name)
    out = root
    for part in p.parts:
        out = out / part
        if out.is_symlink():
            raise ValueError('Symlink paths are not supported: ' + name)
    return out


def read(root, name, default=None):
    path = safe(root, name)
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as error:
        raise ValueError(f'{name}: expected JSON-form YAML 1.2: {error}') from error


def write(root, name, value, raw=False):
    path = safe(root, name)
    if not (name.startswith('.bootstrap/') or name.startswith('context/')):
        raise ValueError('Writes are restricted to .bootstrap/ and context/')
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value if raw else json.dumps(value, indent=2, ensure_ascii=False) + '\n'
    fd, tmp = tempfile.mkstemp(prefix='.bootstrap-write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def lock(root):
    base = safe(root, '.bootstrap')
    base.mkdir(exist_ok=True)
    path = safe(root, '.bootstrap/.lock')
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise ValueError('Another writer or interrupted run holds .bootstrap/.lock; '
                         'verify its PID before removing the lock.') from error
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(str(os.getpid()))
        yield
    finally:
        path.unlink()


def state(root):
    value = read(root, '.bootstrap/state.yaml')
    if not isinstance(value, dict) or value.get('schema_version') != 1:
        raise ValueError('Missing or unsupported state; initialize or explicitly migrate, do not reset.')
    return value


def records(root, name):
    value = read(root, '.bootstrap/' + name + '.yaml', [])
    if not isinstance(value, list):
        raise ValueError(name + ' must be a list')
    return value


def file_hash(root, name):
    path = safe(root, name)
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def source_key(source):
    if not isinstance(source, dict) or (('path' in source) == ('external' in source)):
        raise ValueError('A source needs exactly one of path or external')
    field = 'path' if 'path' in source else 'external'
    if not isinstance(source[field], str) or not source[field]:
        raise ValueError('Empty source')
    return field + ':' + source[field]


def source_snapshot(root, source):
    key = source_key(source)
    if 'path' in source:
        if PurePosixPath(source['path']).parts[0] in ('.bootstrap', 'context'):
            raise ValueError('Generated state/context is not primary evidence; use an external record for human answers')
        return key, file_hash(root, source['path']), []
    evidence = read(root, '.bootstrap/external.yaml', {}).get(source['external'])
    errors = []
    if not isinstance(evidence, dict) or not all(evidence.get(k) for k in ('label', 'location', 'revision', 'review_after')):
        errors.append('external evidence missing or incomplete: ' + source['external'])
    else:
        try:
            if date.fromisoformat(evidence['review_after']) <= date.today():
                errors.append('external evidence review due: ' + source['external'])
        except (ValueError, TypeError):
            errors.append('invalid external review date: ' + source['external'])
        if evidence['revision'].lower() in ('latest', 'unknown'):
            errors.append('external evidence needs a concrete revision: ' + source['external'])
    return key, digest(evidence) if evidence else None, errors


def walk(root, within='.', budget=10000, skip_generated=True):
    start = root if within == '.' else safe(root, within)
    if not start.is_dir():
        raise ValueError('Scan directory not found: ' + within)
    files, pending, visited, incomplete = [], [start], 0, False
    while pending:
        directory = pending.pop()
        remaining = budget - visited
        if remaining <= 0:
            incomplete = True
            break
        with os.scandir(directory) as stream:
            entries = list(itertools.islice(stream, remaining + 1))
        if len(entries) > remaining:
            entries = entries[:remaining]
            incomplete = True
        for entry in sorted(entries, key=lambda e: e.name):
            visited += 1
            if entry.is_symlink():
                continue
            if entry.is_dir(follow_symlinks=False):
                generated_root = directory == root and entry.name in ('.bootstrap', 'context')
                if not skip_generated or (entry.name not in SKIP and not generated_root):
                    pending.append(Path(entry.path))
            elif entry.is_file(follow_symlinks=False):
                files.append(Path(entry.path).relative_to(root).as_posix())
        if incomplete:
            break
    return sorted(files), incomplete, visited


def watch_snapshot(root, pattern):
    safe(root, pattern)
    if PurePosixPath(pattern).parts[0] in ('.bootstrap', 'context', '.git'):
        raise ValueError('Watch evidence locations, not generated state or VCS metadata')
    # Enumerate only the literal directory prefix, then match paths. Bounded even
    # when the caller accidentally supplies a very broad wildcard.
    parts = pattern.split('/')
    prefix = []
    for part in parts[:-1]:
        if any(c in part for c in '*?['):
            break
        prefix.append(part)
    within = '/'.join(prefix) or '.'
    if not safe(root, within).exists():
        return digest([])
    paths, incomplete, _ = walk(root, within, 20000)
    if incomplete:
        raise ValueError('Watch exceeds 20000 entries; narrow it: ' + pattern)
    matches = [p for p in paths if glob_match(p, pattern)]
    return digest([(p, file_hash(root, p)) for p in matches])


def glob_match(path, pattern):
    """Anchored portable glob: * is one segment; ** spans zero or more."""
    names, patterns = path.split('/'), pattern.split('/')

    @lru_cache(maxsize=None)
    def match(i, j):
        if j == len(patterns):
            return i == len(names)
        if patterns[j] == '**':
            return match(i, j + 1) or (i < len(names) and match(i + 1, j))
        return i < len(names) and fnmatch.fnmatchcase(names[i], patterns[j]) and match(i + 1, j + 1)

    return match(0, 0)


def parse_page(text, label):
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError(label + ': missing front matter')
    front, body = text[4:].split('\n---\n', 1)
    try:
        meta = json.loads(front)
    except json.JSONDecodeError as error:
        raise ValueError(label + ': front matter must use JSON-form YAML') from error
    if not isinstance(meta, dict):
        raise ValueError(label + ': metadata must be an object')
    required = ('id', 'kind', 'scope', 'title', 'revision')
    if meta.get('schema_version') != 1 or not all(isinstance(meta.get(k), str) and meta[k] for k in required):
        raise ValueError(label + ': missing metadata or unsupported schema')
    if meta['kind'] not in ('product', 'engineering') or not SLUG.fullmatch(meta['scope']):
        raise ValueError(label + ': invalid kind/scope')
    for field in ('sources', 'watches', 'behaviors', 'implements', 'depends_on', 'verification'):
        if not isinstance(meta.get(field), list):
            raise ValueError(label + ': ' + field + ' must be a list')
    if not meta['sources'] or not body.strip():
        raise ValueError(label + ': source evidence and body required')
    for source in meta['sources']:
        source_key(source)
    for field in ('watches', 'behaviors', 'implements', 'depends_on'):
        if any(not isinstance(x, str) or not x for x in meta[field]):
            raise ValueError(label + ': invalid ' + field)
        if len(set(meta[field])) != len(meta[field]):
            raise ValueError(label + ': duplicate ' + field)
    for behavior in meta['behaviors'] + meta['implements']:
        if not PB.fullmatch(behavior):
            raise ValueError(label + ': invalid PB ID ' + behavior)
    if meta['kind'] == 'product' and meta['implements']:
        raise ValueError(label + ': product owns behaviors, engineering implements them')
    if meta['kind'] == 'engineering' and meta['behaviors']:
        raise ValueError(label + ': engineering cannot own PB IDs')
    for behavior in meta['behaviors']:
        if f'<a id="{behavior.lower()}"></a>' not in body:
            raise ValueError(label + ': missing anchor for ' + behavior)
    covered = set()
    for check in meta['verification']:
        if not isinstance(check, dict) or check.get('kind') not in ('existing', 'gap') or not check.get('reference'):
            raise ValueError(label + ': malformed verification entry')
        if check.get('behavior') not in meta['implements']:
            raise ValueError(label + ': verification must refer to an implemented PB')
        covered.add(check['behavior'])
    if set(meta['implements']) - covered:
        raise ValueError(label + ': every implemented behavior needs verification or an explicit gap')
    return meta, body


def pages(root):
    result = {}
    context = safe(root, 'context')
    if context.exists():
        for path in sorted(context.rglob('*.md')):
            name = path.relative_to(root).as_posix()
            safe(root, name)
            result[name] = parse_page(path.read_text(encoding='utf-8'), name)
    return result


def links(root, docs, allow_missing_dependencies=False):
    ids, owners, errors = {}, {}, []
    for path, (meta, body) in docs.items():
        if meta['id'] in ids:
            errors.append('duplicate document ID: ' + meta['id'])
        ids[meta['id']] = path
        for pb in meta['behaviors']:
            if pb in owners:
                errors.append('duplicate behavior ID: ' + pb)
            owners[pb] = path
    for path, (meta, body) in docs.items():
        if not allow_missing_dependencies:
            for dep in meta['depends_on']:
                if dep not in ids:
                    errors.append(meta['id'] + ': missing dependency ' + dep)
        for pb in meta['implements']:
            if pb not in owners:
                errors.append(meta['id'] + ': missing product owner for ' + pb)
                continue
            target = os.path.relpath(root / owners[pb], (root / path).parent).replace(os.sep, '/')
            if '](' + target + '#' + pb.lower() + ')' not in body:
                errors.append(meta['id'] + ': missing Markdown link to ' + target + '#' + pb.lower())
    return errors


def issues(root):
    questions = records(root, 'questions')
    seen = set()
    for q in questions:
        needed = ('id', 'scope', 'found', 'sources', 'why', 'affects', 'question', 'blocking', 'status')
        if not isinstance(q, dict) or any(k not in q for k in needed):
            raise ValueError('Question missing required fields')
        if q['id'] in seen or not re.fullmatch(r'Q-[0-9]{3,}', q['id']):
            raise ValueError('Invalid or duplicate question ID')
        seen.add(q['id'])
        if not isinstance(q['affects'], list) or not isinstance(q['blocking'], bool):
            raise ValueError('Question affects/blocking malformed')
        if q['status'] not in ('open', 'answered', 'conflicting', 'needs evidence', 'resolved'):
            raise ValueError('Invalid question status')
        if q['status'] == 'resolved' and not q.get('validation'):
            raise ValueError('Resolved question needs evidence validation')
    return questions


def blockers(root, meta):
    own = {meta['id'], *meta['behaviors'], *meta['implements']}
    return [q['id'] for q in issues(root) if q['blocking'] and q['status'] != 'resolved'
            and q['scope'] == meta['scope'] and (not q['affects'] or own.intersection(q['affects']))]


def exclusion_digest(root, meta):
    relevant = []
    own = {meta['id'], *meta['behaviors'], *meta['implements']}
    keys = {source_key(s) for s in meta['sources']}
    for ex in records(root, 'exclusions'):
        if ex['status'] == 'retired':
            continue
        if (ex['scope'] == meta['scope'] and (not ex['affects'] or own.intersection(ex['affects']))) or source_key(ex['source']) in keys:
            relevant.append(ex)
    return digest(relevant)


def snapshot(root, meta):
    sources, errors = {}, []
    for src in meta['sources']:
        key, value, problems = source_snapshot(root, src)
        sources[key] = value
        errors.extend(problems)
        if value is None:
            errors.append('source missing: ' + key)
    watches = {pattern: watch_snapshot(root, pattern) for pattern in meta['watches']}
    docs = pages(root)
    ids = {m['id']: p for p, (m, _) in docs.items()}
    owners = {pb: m['id'] for m, _ in docs.values() for pb in m['behaviors']}
    deps = set(meta['depends_on']) | {owners.get(pb, 'missing:' + pb) for pb in meta['implements']}
    dependencies = {d: file_hash(root, ids[d]) if d in ids else None for d in deps}
    return {'sources': sources, 'watches': watches, 'dependencies': dependencies,
            'exclusions': exclusion_digest(root, meta)}, errors


def refresh(root, docs, tracking):
    updated = json.loads(json.dumps(tracking))
    for path, (meta, body) in docs.items():
        old = updated.get(path, {})
        reasons = {r for r in old.get('reasons', []) if not r.startswith('dependency needs revalidation: ')}
        if not old:
            reasons.add('no reviewed baseline')
        current, errors = snapshot(root, meta)
        reasons.update(errors)
        for field in ('sources', 'watches', 'dependencies', 'exclusions'):
            if old.get(field) != current[field]:
                reasons.add(field + ' changed')
        if old.get('document_hash') != file_hash(root, path):
            reasons.add('published document changed')
        reasons.update('blocking question: ' + q for q in blockers(root, meta))
        old['status'] = 'needs revalidation' if reasons else 'current'
        old['reasons'] = sorted(reasons)
        updated[path] = old
    ids = {meta['id']: path for path, (meta, _) in docs.items()}
    owners = {pb: meta['id'] for meta, _ in docs.values() for pb in meta['behaviors']}
    changed = True
    while changed:
        changed = False
        for path, (meta, _) in docs.items():
            deps = set(meta['depends_on']) | {owners.get(pb, 'missing:' + pb) for pb in meta['implements']}
            for dep in deps:
                if dep not in ids or updated[ids[dep]]['status'] != 'current':
                    reason = 'dependency needs revalidation: ' + dep
                    if reason not in updated[path]['reasons']:
                        updated[path]['reasons'].append(reason)
                        updated[path]['status'] = 'needs revalidation'
                        changed = True
    return updated


def save_index(root, docs, tracking):
    entries = []
    fields = ('id', 'kind', 'scope', 'title', 'behaviors', 'implements', 'depends_on')
    for path, (meta, _) in sorted(docs.items()):
        item = {k: meta[k] for k in fields}
        item.update(path=path, freshness=tracking.get(path, {}).get('status', 'needs revalidation'),
                    reasons=tracking.get(path, {}).get('reasons', ['no reviewed baseline']))
        entries.append(item)
    write(root, 'context/index.yaml', {'schema_version': 1, 'documents': entries,
          'exclusions': '.bootstrap/exclusions.yaml', 'questions': '.bootstrap/questions.yaml',
          'read_contract': 'Run freshness; use current pages only; respect active and needs-review exclusions.'})


def save_refresh(root, docs, tracking):
    updated = refresh(root, docs, tracking)
    st = state(root)
    stale_scopes = {meta['scope'] for path, (meta, _) in docs.items()
                    if updated[path]['status'] != 'current'}
    for scope, item in st['scopes'].items():
        if item['status'] == 'needs revalidation' and scope not in stale_scopes:
            item['status'] = 'partial'
    for path, (meta, _) in docs.items():
        if updated[path]['status'] != 'current' and meta['scope'] in st['scopes']:
            st['scopes'][meta['scope']]['status'] = 'needs revalidation'
    write(root, '.bootstrap/tracking.yaml', updated)
    write(root, '.bootstrap/state.yaml', st)
    save_index(root, docs, updated)
    return updated


def revise_exclusions(root):
    exclusions = records(root, 'exclusions')
    modified = False
    for ex in exclusions:
        if ex['status'] == 'active':
            _, value, errors = source_snapshot(root, ex['source'])
            if errors or value != ex['source_snapshot']:
                ex['status'] = 'needs review'
                modified = True
    if modified:
        write(root, '.bootstrap/exclusions.yaml', exclusions)


def initialize(root, scope):
    if not SLUG.fullmatch(scope):
        raise ValueError('Scope must be a lowercase hyphenated slug')
    st = read(root, '.bootstrap/state.yaml')
    if st is None:
        st = {'schema_version': 1, 'scopes': {}, 'next_pb': 1, 'next_question': 1}
    elif st.get('schema_version') != 1:
        raise ValueError('Unsupported state version; explicit migration required')
    st['scopes'].setdefault(scope, {'status': 'not started', 'next_action': 'Select one bounded investigation'})
    write(root, '.bootstrap/state.yaml', st)
    for name, initial in [('questions', []), ('remediation', []), ('exclusions', []), ('external', {}), ('tracking', {})]:
        if not safe(root, '.bootstrap/' + name + '.yaml').exists():
            write(root, '.bootstrap/' + name + '.yaml', initial)
    safe(root, '.bootstrap/runs').mkdir(exist_ok=True)
    return st


def publish(root, args):
    st = state(root)
    target = safe(root, args.to)
    if not re.fullmatch(r'context/(product|engineering)/[a-z0-9][a-z0-9-]*\.md', args.to):
        raise ValueError('Target must be a capability/component Markdown page in context/product or context/engineering')
    text = safe(root, args.draft).read_text(encoding='utf-8')
    meta, body = parse_page(text, args.draft)
    if meta['scope'] not in st['scopes']:
        raise ValueError('Initialize this scope first')
    if '/' + meta['kind'] + '/' not in args.to:
        raise ValueError('Kind must match target directory')
    blocked = blockers(root, meta)
    if blocked:
        raise ValueError('Publication blocked by ' + ', '.join(blocked))
    docs = pages(root)
    if args.to in docs and docs[args.to][0]['id'] != meta['id']:
        raise ValueError('Preserve existing document identity')
    docs[args.to] = (meta, body)
    errors = links(root, docs, allow_missing_dependencies=True)
    if errors:
        raise ValueError('; '.join(errors))
    snap, errors = snapshot(root, meta)
    if errors:
        raise ValueError('; '.join(errors))
    tracking = read(root, '.bootstrap/tracking.yaml', {})
    write(root, args.to, text, raw=True)
    snap.update(document_hash=file_hash(root, args.to), status='current', reasons=[])
    tracking[args.to] = snap
    # Existing stale dependency reasons remain until explicit review. Candidate
    # freshness still checks its current dependencies, including product owners.
    updated = save_refresh(root, docs, tracking)
    # Successful publication starts work even if no prior checkpoint was saved.
    st = state(root)
    if st['scopes'][meta['scope']]['status'] == 'not started':
        st['scopes'][meta['scope']]['status'] = 'partial'
        write(root, '.bootstrap/state.yaml', st)
    return {'published': args.to, 'freshness': updated[args.to]['status']}


def decision(root, args):
    qs = issues(root)
    q = next((x for x in qs if x['id'] == args.question), None)
    if not q:
        raise ValueError('Question not found')
    if q.get('decision'):
        raise ValueError('Decision already recorded; review it in place instead of duplicating')
    dec = {'choice': args.choice, 'human_statement': args.statement, 'github_id': args.github_id}
    item = {'question_id': q['id'], 'scope': q['scope'], 'affects': q['affects'], 'decision': dec}
    if args.choice == 'FIX':
        if not args.action:
            raise ValueError('FIX requires --action')
        name, prefix = 'remediation', 'R'
        item.update(status='open', action=args.action, sources=q['sources'])
    else:
        if bool(args.source) == bool(args.external) or not all((args.claim, args.rationale, args.recheck_when)):
            raise ValueError('IGNORE needs one source/external, claim, rationale, and recheck trigger')
        source = {'path': args.source} if args.source else {'external': args.external}
        _, value, errors = source_snapshot(root, source)
        if errors or value is None:
            raise ValueError('Cannot scope exclusion to missing/unregistered evidence')
        name, prefix = 'exclusions', 'X'
        item.update(status='active', source=source, claim=args.claim, rationale=args.rationale,
                    recheck_when=args.recheck_when, source_snapshot=value)
    items = records(root, name)
    # Recover an interruption after record write but before question linkage.
    existing = next((x for x in items if x['question_id'] == q['id']), None)
    if existing:
        if existing['decision'] != dec:
            raise ValueError('A different decision already exists for this question')
        item = existing
    else:
        number = max([int(x['id'].split('-')[-1]) for x in items] + [0]) + 1
        item['id'] = f'{prefix}-{number:03d}'
        items.append(item)
        write(root, '.bootstrap/' + name + '.yaml', items)
    q['decision'] = item['id']
    write(root, '.bootstrap/questions.yaml', qs)
    save_refresh(root, pages(root), read(root, '.bootstrap/tracking.yaml', {}))
    return item


def scan(root, args):
    if not 1 <= args.limit <= 1000:
        raise ValueError('Scan limit must be 1..1000')
    paths, incomplete, visited = walk(root, args.within)
    visible = [p for p in paths if not (Path(p).name.startswith('.env') or
               Path(p).suffix.lower() in ('.pem', '.key', '.p12', '.png', '.jpg', '.zip', '.pdf'))]
    categories = {'manifests': [], 'ci': [], 'tests': [], 'docs': [], 'config': []}
    for p in visible:
        low = p.lower()
        if Path(p).name in ('package.json', 'pyproject.toml', 'Cargo.toml', 'go.mod', 'pom.xml', 'Makefile', 'Gemfile'):
            categories['manifests'].append(p)
        if low.startswith('.github/workflows/') or Path(p).name in ('.gitlab-ci.yml', 'Jenkinsfile'):
            categories['ci'].append(p)
        if 'test' in low or 'spec' in low:
            categories['tests'].append(p)
        if low.endswith(('.md', '.rst', '.adoc')):
            categories['docs'].append(p)
        if low.endswith(('.yaml', '.yml', '.toml', '.json')) or 'docker' in low:
            categories['config'].append(p)
    try:
        proc = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True, timeout=5)
        revision = proc.stdout.strip() if proc.returncode == 0 else 'no-git'
    except (FileNotFoundError, subprocess.TimeoutExpired):
        revision = 'no-git'
    return {'revision': revision, 'within': args.within, 'entries_visited': visited,
            'coverage_incomplete': incomplete, 'paths_truncated': len(visible) > args.limit,
            'paths_seen': len(visible), 'paths': visible[:args.limit],
            'categories': {k: {'count_seen': len(v), 'sample': v[:min(10, args.limit)]} for k, v in categories.items()}}


def run(root, args):
    command = args.command
    if command == 'scan':
        return scan(root, args)
    if command == 'init':
        return initialize(root, args.scope)
    if command == 'status':
        st = read(root, '.bootstrap/state.yaml', {'status': 'not started'})
        tracking = read(root, '.bootstrap/tracking.yaml', {})
        return {'state': st, 'open_questions': [q['id'] for q in issues(root) if q['status'] != 'resolved'],
                'open_remediation': [x['id'] for x in records(root, 'remediation') if x['status'] == 'open'],
                'exclusions': [{'id': x['id'], 'status': x['status']} for x in records(root, 'exclusions') if x['status'] != 'retired'],
                'recorded_stale_pages': [p for p, t in tracking.items() if t.get('status') != 'current'],
                'note': 'Read-only recorded status; run freshness to detect source changes.'}
    st = state(root)
    if command == 'allocate-pb':
        used = [int(pb.split('-')[1]) for meta, _ in pages(root).values() for pb in meta['behaviors']]
        number = max([st['next_pb']] + [x + 1 for x in used])
        st['next_pb'] = number + 1
        write(root, '.bootstrap/state.yaml', st)
        return {'behavior': f'PB-{number:03d}'}
    if command == 'publish':
        return publish(root, args)
    if command == 'decision':
        return decision(root, args)
    docs = pages(root)
    tracking = read(root, '.bootstrap/tracking.yaml', {})
    if command == 'check':
        issues(root)
        errors = links(root, docs)
        for path, (meta, _) in docs.items():
            if meta['scope'] not in st['scopes']:
                errors.append(path + ': unknown scope')
        if errors:
            raise ValueError('; '.join(errors))
        return {'valid': True, 'pages': len(docs), 'note': 'Structure only; evidence truth requires model review.'}
    if command == 'invalidate':
        ids = {meta['id']: path for path, (meta, _) in docs.items()}
        if set(args.ids) - set(ids):
            raise ValueError('Unknown document IDs: ' + ', '.join(set(args.ids) - set(ids)))
        for identity in args.ids:
            entry = tracking.setdefault(ids[identity], {})
            entry.setdefault('reasons', []).append(args.reason)
            entry['status'] = 'needs revalidation'
    if command in ('freshness', 'index', 'invalidate'):
        revise_exclusions(root)
        updated = save_refresh(root, docs, tracking)
        return {'pages': {p: {'status': t['status'], 'reasons': t['reasons']} for p, t in updated.items() if p in docs}}
    if command == 'checkpoint':
        if args.scope not in st['scopes']:
            raise ValueError('Unknown scope')
        if args.status == 'complete':
            refreshed = refresh(root, docs, tracking)
            selected = {p: v for p, v in docs.items() if v[0]['scope'] == args.scope}
            errors = links(root, docs)
            kinds = {m['kind'] for m, _ in selected.values()}
            owned = {pb for m, _ in selected.values() for pb in m['behaviors']}
            implemented = {pb for m, _ in selected.values() for pb in m['implements']}
            if kinds != {'product', 'engineering'} or not owned or owned - implemented:
                errors.append('scope needs linked product and engineering behaviors')
            if any(refreshed[p]['status'] != 'current' for p in selected):
                errors.append('scope contains stale/unreviewed pages')
            if any(q['scope'] == args.scope and q['blocking'] and q['status'] != 'resolved' for q in issues(root)):
                errors.append('scope has blocking questions')
            if errors:
                raise ValueError('; '.join(errors))
        item = st['scopes'][args.scope]
        item.update(status=args.status, next_action=args.next)
        if args.finding:
            if not args.finding.startswith('.bootstrap/runs/') or not safe(root, args.finding).is_file():
                raise ValueError('Finding must exist in .bootstrap/runs/')
            item['checkpoint'] = args.finding
        else:
            item.pop('checkpoint', None)
        write(root, '.bootstrap/state.yaml', st)
        return item
    raise ValueError('Unknown command')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('scan'); p.add_argument('--within', default='.'); p.add_argument('--limit', type=int, default=200)
    p = sub.add_parser('init'); p.add_argument('--scope', required=True)
    for name in ('status', 'allocate-pb', 'freshness', 'index', 'check'):
        sub.add_parser(name)
    p = sub.add_parser('publish'); p.add_argument('--draft', required=True); p.add_argument('--to', required=True)
    p = sub.add_parser('invalidate'); p.add_argument('--ids', nargs='+', required=True); p.add_argument('--reason', required=True)
    p = sub.add_parser('checkpoint'); p.add_argument('--scope', required=True); p.add_argument('--status', choices=STATUSES, required=True)
    p.add_argument('--next', required=True); p.add_argument('--finding')
    p = sub.add_parser('decision'); p.add_argument('--question', required=True); p.add_argument('--choice', choices=('FIX', 'IGNORE'), required=True)
    p.add_argument('--statement', required=True)
    for name in ('github-id', 'action', 'source', 'external', 'claim', 'rationale', 'recheck-when'):
        p.add_argument('--' + name)
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    try:
        if not root.is_dir():
            raise ValueError('Repository directory not found')
        if args.command in ('scan', 'status', 'check'):
            result = run(root, args)
        else:
            with lock(root):
                result = run(root, args)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError) as error:
        print('bootstrap: ' + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
