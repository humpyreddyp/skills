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
shutil.copytree(f/'.bootstrap',c/'before-publication')
(f/'.bootstrap/runs').mkdir(exist_ok=True)
(f/'.bootstrap/runs/review.md').write_text('Scope: checkout. Q-001 evidence review completed; existing test directly invoked and passed. Sources: src/checkout.py::total, tests/test_checkout.py::test_total, docs/checkout.md, Q-001. Next: publish reviewed fee behavior and implementing function; preserve any remaining purpose gap.\n')
cmd('checkpoint','--scope','checkout','--status','partial','--next','Publish reviewed product and engineering context for PB-001','--finding','.bootstrap/runs/review.md')
common={'schema_version':1,'scope':'checkout','revision':'working-tree','watches':['src/checkout.py','tests/test_checkout.py','docs/checkout.md'],'sources':[{'path':'src/checkout.py','section':'FEE and total'},{'path':'tests/test_checkout.py','section':'test_total'}]}
product=dict(common,id='CAP-fee',kind='product',title='Checkout fee',behaviors=['PB-001'],implements=[],depends_on=['CMP-checkout'],verification=[])
product['sources']=product['sources']+[{'external':'checkout-owner-answer','section':'Q-001 checked answer'}]+([{'path':'docs/checkout.md'}] if 5==5 else [])
engineering=dict(common,id='CMP-checkout',kind='engineering',title='Checkout calculation',behaviors=[],implements=['PB-001'],depends_on=['CAP-fee'],verification=[{'behavior':'PB-001','kind':'existing','reference':'tests/test_checkout.py::test_total'},{'behavior':'PB-001','kind':'gap','reference':'Caller integration and numeric/input contract coverage require caller and contract evidence'}])
for name,meta,body in [('product',product,'# Checkout fee\n\n## Purpose and evidence\n\nIntended and observed: checkout adds a fixed fee of 3. docs/checkout.md and the checked product-owner answer identify its purpose as covering packing costs.\n\n<a id="pb-001"></a>\n### PB-001 — Add the checkout fee\n\nFor a supplied subtotal, `total(subtotal)` returns `subtotal + 3`; the existing check uses subtotal 10 and expects 13. The sources do not define currency or an input-validation contract. See [implementation and checks](../engineering/checkout.md).\n\n## Ownership and handoff\n\nCheckout owns the fee addition to a supplied subtotal. It does not determine inventory availability, as stated in docs/checkout.md. src/checkout.py::total returns the computed total to its caller; caller identity, payment collection, and inventory ownership are not established by this fixture.\n'),('engineering',engineering,'# Checkout calculation\n\n## Responsibilities\n\n`src/checkout.py::total` implements [PB-001](../product/checkout.md#pb-001): it accepts a subtotal, adds the module constant `FEE = 3`, and returns the result to the caller. No payment, inventory, persistence, or remote I/O occurs in the inspected function. The fixture does not establish its callers or their contracts.\n\n## Dependencies and verification\n\nThe function depends on its supplied subtotal and the local `FEE` constant. `tests/test_checkout.py::test_total` imports this function and asserts `total(10) == 13`. That existing assertion passed by direct Python invocation on the inspected working-tree snapshot; a test runner suite was not run. `pyproject.toml` declares the sample project but no test command.\n\nA fee change must review the product intent, constant, and existing expectation together. Verification gap: the available test does not establish input validation, currency/precision rules, or callers’ expectations. Caller integration checks require caller evidence, which is unavailable here. No missing test infrastructure was created.\n')]:
 content='---\n'+json.dumps(meta,indent=2)+'\n---\n\n'+body
 (f/'.bootstrap/runs'/f'{name}.md').write_text(content)
 print('DRAFT',name,content)
cmd('publish','--draft','.bootstrap/runs/product.md','--to','context/product/checkout.md')
shutil.copytree(f/'context',c/'after-product-publication')
cmd('publish','--draft','.bootstrap/runs/engineering.md','--to','context/engineering/checkout.md')
cmd('publish','--draft','context/product/checkout.md','--to','context/product/checkout.md')
cmd('freshness')
cmd('check')
