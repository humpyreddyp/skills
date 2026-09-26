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
qs=json.loads((f/'.bootstrap/questions.yaml').read_text())
q=next(q for q in qs if q['id']=='Q-001')
q['answer']={'summary':'The current fee is 3, for packing costs, as documented in docs/checkout.md.','github_id':'product-owner','sources':['docs/checkout.md'] if 5==5 else []}
q['validation']='The answer agrees with docs/checkout.md, FEE = 3 and total(subtotal) in src/checkout.py, and test_total expecting total(10) == 13. Packing purpose is documented. Q-001 is resolved.'
q['status']='resolved'
write('.bootstrap/questions.yaml',qs)
cmd('freshness')
cmd('check')
