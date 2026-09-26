from pathlib import Path
import sys,json,hashlib
r=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(r))
from record_command import run
c=Path(__file__).resolve().parent
f=r/'fixtures'/'case-07'
helper='/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork/scripts/bootstrap.py'
def cmd(*args):
 p=run(c/'raw.jsonl',['python3',helper,'--repo',str(f),*args],f)
 if p.returncode: raise RuntimeError(p.stderr)
 return json.loads(p.stdout)
def write(path,value):
 (f/path).write_text(json.dumps(value,indent=2)+'\n')
 print('WROTE',path,json.dumps(value))
cmd('decision','--question','Q-001','--choice','FIX','--statement','For Q-001 I choose FIX: engineering should change the implementation to fee 2 and update its tests. Record that as remediation only. My GitHub ID is product-owner.','--action','Engineering should change the implementation to fee 2 and update its tests. Record remediation only; do not implement it during Groundwork.','--github-id','product-owner')
run(c/'raw.jsonl',['cat','.bootstrap/questions.yaml','.bootstrap/remediation.yaml'],f)
cmd('freshness')
cmd('check')
