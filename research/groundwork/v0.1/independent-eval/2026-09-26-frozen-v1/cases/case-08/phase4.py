from pathlib import Path
import sys,json,hashlib
r=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(r))
from record_command import run
c=Path(__file__).resolve().parent
f=r/'fixtures'/'case-08'
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
(f/'.bootstrap/runs/purpose.md').write_text('Scope: checkout. Fee-3 behavior is independently supported and published; Q-001 resolved and X-001 remains narrow. Q-002 asks what purpose the fee serves and which requirement supports it. Do not invent a rationale. Next: validate supplied purpose evidence, update provenance, and reassess completion.\n')
cmd('checkpoint','--scope','checkout','--status','partial','--next','Obtain and validate Q-002 fee purpose evidence before completing the scope','--finding','.bootstrap/runs/purpose.md')
for name in ('product.md','engineering.md','review.md'):
 (f/'.bootstrap/runs'/name).unlink()
 print('Removed obsolete Groundwork-owned draft',name,'after preserving evidence snapshot')
cmd('freshness')
cmd('check')
cmd('status')
