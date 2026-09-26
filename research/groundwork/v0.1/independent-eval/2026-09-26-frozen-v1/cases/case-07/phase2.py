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
import shutil
shutil.copytree(f/'.bootstrap',c/'after-phase1')
qs=json.loads((f/'.bootstrap/questions.yaml').read_text())
q=next(q for q in qs if q['id']=='Q-001')
q['validation']='FIX authorizes future engineering work only. Reinspection shows src/checkout.py still uses FEE=3 and tests/test_checkout.py still expects 13 for subtotal 10, while docs specify 2. R-001 remains open and Q-001 remains conflicting; no completed fix has been verified.'
q['status']='conflicting'
write('.bootstrap/questions.yaml',qs)
finding="""# Checkout remediation checkpoint
Scope: checkout. Human chose FIX; R-001 records engineering changing implementation to fee 2 and updating tests.
Current code/test still use fee 3; docs specify 2. No code or tests changed. The fee claim remains unpublished and Q-001 blocks completion.
Next action: when engineering supplies the fix, inspect code and tests and verify behavior before closing R-001/Q-001 or publishing.
"""
(f/'.bootstrap/runs').mkdir(exist_ok=True)
(f/'.bootstrap/runs/remediation.md').write_text(finding)
print(finding)
cmd('freshness')
cmd('check')
cmd('checkpoint','--scope','checkout','--status','partial','--next','Await engineering remediation R-001, then inspect and verify the completed fee-2 change before resolving Q-001','--finding','.bootstrap/runs/remediation.md')
