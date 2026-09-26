from pathlib import Path
import sys,json,hashlib
r=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(r))
from record_command import run
c=Path(__file__).resolve().parent
f=r/'fixtures'/'case-05'
helper='/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork/scripts/bootstrap.py'
def cmd(*args):
 p=run(c/'raw.jsonl',['python3',helper,'--repo',str(f),*args],f)
 if p.returncode: raise RuntimeError(p.stderr)
 return json.loads(p.stdout)
def write(path,value):
 (f/path).write_text(json.dumps(value,indent=2)+'\n')
 print('WROTE',path,json.dumps(value))
import shutil
shutil.copytree(f/'.bootstrap/runs',c/'final-draft-snapshot')
cmd('checkpoint','--scope','checkout','--status','complete','--next','Run freshness before relying on the fee baseline; revalidate any changed fee sources or checked owner intent')
state=json.loads((f/'.bootstrap/state.yaml').read_text());state['scopes']['checkout'].pop('checkpoint',None);write('.bootstrap/state.yaml',state)
for name in ('product.md','engineering.md','review.md'):
 (f/'.bootstrap/runs'/name).unlink()
 print('Removed obsolete Groundwork-owned draft',name,'after preserving evidence snapshot')
cmd('freshness')
cmd('check')
cmd('status')
