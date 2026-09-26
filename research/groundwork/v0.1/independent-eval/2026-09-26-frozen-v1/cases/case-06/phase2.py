from pathlib import Path
import sys,json,hashlib
r=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(r))
from record_command import run
c=Path(__file__).resolve().parent
f=r/'fixtures'/'case-06'
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
finding="""# Checkout conflict
Scope: checkout. Q-001 remains conflicting and blocks CAP-fee/PB-001.
Observed: src/checkout.py adds FEE=3; tests/test_checkout.py expects total(10)=13; docs/checkout.md states fee 3 for packing. The human asserts fee 2. No source resolves the mismatch. No fee claim is published as trusted context.
Supported independent detail: docs describe packing costs and exclusion of inventory availability; these can be investigated/published separately if desired.
Next action: ask whether to FIX implementation/tests/docs for fee 2 or IGNORE a specific source/claim with rationale, or leave unresolved. No choice inferred.
"""
(f/'.bootstrap/runs').mkdir(exist_ok=True)
(f/'.bootstrap/runs/conflict.md').write_text(finding)
print(finding)
cmd('checkpoint','--scope','checkout','--status','waiting for human','--next','Obtain explicit FIX or narrowly scoped IGNORE choice for Q-001; compare any new evidence before publication','--finding','.bootstrap/runs/conflict.md')
cmd('freshness')
cmd('check')
