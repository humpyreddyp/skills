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
shutil.copytree(f/'.bootstrap',c/'after-phase1')
qs=json.loads((f/'.bootstrap/questions.yaml').read_text())
q=next(q for q in qs if q['id']=='Q-001')
run(c/'raw.jsonl',['python3','-c','import runpy; runpy.run_path("tests/test_checkout.py")["test_total"](); print("test_total passed by direct invocation: total(10) == 13")'],f)
answer=q['answer']['summary']
external=json.loads((f/'.bootstrap/external.yaml').read_text())
external['checkout-owner-answer']={'label':'Q-001 answer by product-owner','location':'.bootstrap/questions.yaml#Q-001','revision':'sha256:'+hashlib.sha256(answer.encode()).hexdigest(),'review_after':'2026-12-26'}
write('.bootstrap/external.yaml',external)
cmd('freshness')
cmd('check')
pb=cmd('allocate-pb')['behavior']
assert pb=='PB-001',pb
