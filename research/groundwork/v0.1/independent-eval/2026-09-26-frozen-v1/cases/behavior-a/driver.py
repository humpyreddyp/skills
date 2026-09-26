"""Exact evaluator-authored execution driver. Cases use independent fixture repositories."""
import sys, json, shutil
from pathlib import Path
ROOT=Path('/Users/humpyreddypininti/Documents/ChatGPT/skilly/independent-evaluation/2026-09-26-frozen-v1')
sys.path.insert(0,str(ROOT))
from record_command import run
SKILL=Path('/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork')
N=int(sys.argv[1]); ACTION=sys.argv[2]
CASE=ROOT/'cases'/f'case-{N:02}'; CASE.mkdir(parents=True,exist_ok=True)
REPO=ROOT/'fixtures'/f'case-{N:02}'
def command(cmd):
    return run(CASE/'raw.jsonl',cmd,REPO)
def helper(*args):
    return command(['python3',str(SKILL/'scripts/bootstrap.py'),'--repo',str(REPO),*args])
def read(*paths):
    catalog=CASE/'inspected-files.json'
    seen=json.loads(catalog.read_text()) if catalog.exists() else []
    for p in paths:
        path=str(p)
        if path not in seen: seen.append(path)
    catalog.write_text(json.dumps(seen,indent=2)+'\n')
    return command(['cat',*[str(p) for p in paths]])
def write(path,data):
    p=REPO/path; p.parent.mkdir(parents=True,exist_ok=True)
    value=data if isinstance(data,str) else json.dumps(data,indent=2)+'\n'
    p.write_text(value)
    with (CASE/'authored-writes.jsonl').open('a') as f: f.write(json.dumps({'path':path,'content':value})+'\n')
def snapshot(name):
    dest=CASE/'snapshots'/name; dest.mkdir(parents=True,exist_ok=True)
    for item in ['.bootstrap','context']:
        src=REPO/item
        if src.exists(): shutil.copytree(src,dest/item,dirs_exist_ok=True)
if ACTION=='start':
    requests=json.loads((ROOT/'fixtures/requests.json').read_text())
    (CASE/'prompt.txt').write_text(requests[str(N)]['request']+'\n')
    (CASE/'execution-constraints.md').write_text('All four agent slots are occupied (root and three executing agents). No isolated investigator is available. Each investigation is bounded to one uncertainty and checkpointed. This shared executor does not clear earlier case context. No token count is exposed. Common skill and reference reads are recorded in cases/behavior-a/raw.jsonl.\n')
    for path in ['.bootstrap/state.yaml','context/index.yaml']:
        if (REPO/path).exists(): read(path)
    helper('scan','--limit','40')
    command(['git','status','--short'])
elif ACTION=='read': read(*sys.argv[3:])
elif ACTION=='helper': helper(*sys.argv[3:])
elif ACTION=='snapshot': snapshot(sys.argv[3])
elif ACTION=='run': command(sys.argv[3:])
def page(path, *, id, kind, scope, title, sources, watches, behaviors=None, implements=None, depends_on=None, verification=None, body):
    meta={'schema_version':1,'id':id,'kind':kind,'scope':scope,'title':title,'revision':'working-tree','sources':[{'path':p} for p in sources], 'watches':watches,'behaviors':behaviors or [],'implements':implements or [],'depends_on':depends_on or [],'verification':verification or []}
    write(path,'---\n'+json.dumps(meta,indent=2)+'\n---\n\n'+body+'\n')
def cleanup(*paths):
    for path in paths:
        (REPO/path).unlink()
        with (CASE/'authored-writes.jsonl').open('a') as f: f.write(json.dumps({'deleted':path})+'\n')
def finish(final,observations,needs):
    (CASE/'final-response.md').write_text(final+'\n')
    (CASE/'observations.md').write_text(observations+'\n\nHuman input needs: '+needs+'\n\nRevision limit: fixtures have no independent Git commit; helper reports the enclosing repository revision. Published provenance uses working-tree and source fingerprints.\n')
    raws=(CASE/'raw.jsonl').read_text().splitlines()
    inspected=json.loads((CASE/'inspected-files.json').read_text())
    (CASE/'metrics.json').write_text(json.dumps({'command_steps':len(raws),'content_files_read':len(inspected),'inspected_files':inspected,'token_count':None,'common_skill_content_files_read':7,'isolation':'All agent slots occupied; bounded checkpoints used. Prior case context remains in executor.'},indent=2)+'\n')
    snapshot('final')
