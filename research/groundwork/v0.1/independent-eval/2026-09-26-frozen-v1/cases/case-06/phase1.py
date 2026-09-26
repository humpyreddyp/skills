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
qs=json.loads((f/'.bootstrap/questions.yaml').read_text())
q=next(q for q in qs if q['id']=='Q-001')
q['answer']={'summary':'The current fee is definitely 2; please make the baseline reflect that.','github_id':'product-owner','sources':['docs/checkout.md'] if 6==5 else []}
q['validation']='The supplied answer asserts fee 2, while docs/checkout.md and src/checkout.py use 3 and test_total expects 13 for subtotal 10. The answer is not supported as current observed behavior; desired intent and implementation remain in conflict. An explicit FIX or narrowly targeted IGNORE decision is needed before publishing the disputed claim.'
q['status']='conflicting'
write('.bootstrap/questions.yaml',qs)
cmd('freshness')
cmd('check')
