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
cmd('decision','--question','Q-001','--choice','IGNORE','--statement','For Q-001 I choose IGNORE the claim in docs/checkout.md that checkout fee is 2. That claim is outdated; the current fee of 3 is supported by the code and test. Keep other claims in that document usable. Recheck this exclusion if the fee documentation changes. My GitHub ID is product-owner.','--source','docs/checkout.md','--claim','The fee is 2.','--rationale','The human identifies this fee claim as outdated; current code and test support fee 3. Other claims in the document remain usable.','--recheck-when','The fee documentation changes','--github-id','product-owner')
run(c/'raw.jsonl',['cat','.bootstrap/questions.yaml','.bootstrap/exclusions.yaml'],f)
cmd('freshness')
cmd('check')
