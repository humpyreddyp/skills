from pathlib import Path
import sys,json,shutil
ROOT=Path('/Users/humpyreddypininti/Documents/ChatGPT/skilly/independent-evaluation/2026-09-26-frozen-v1')
sys.path.insert(0,str(ROOT)); from record_command import run
CASE=ROOT/'cases/case-09'; REPO=ROOT/'fixtures/case-09'
HELPER='/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork/scripts/bootstrap.py'
def cmd(*args): return run(CASE/'raw.jsonl',list(args),REPO)
def h(*args): return cmd('python3',HELPER,'--repo',str(REPO),*args)
def write(path,text): return cmd('python3','-c','from pathlib import Path; import sys; p=Path(sys.argv[1]); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(sys.argv[2]); print("Wrote",p)',str(path),text)
def snap(name):
    for folder in ['.bootstrap','context']:
        p=REPO/folder
        if p.exists(): shutil.copytree(p,CASE/name/folder,dirs_exist_ok=True)
requests=json.loads(cmd('cat',str(ROOT/'fixtures/requests.json')).stdout)
write(CASE/'exact-prompt.txt',requests['9']['request']+'\n')
snap('before-resume')
h('freshness')
h('status')
pb=json.loads(h('allocate-pb').stdout)['behavior']
assert pb=='PB-012', pb
write(REPO/'.bootstrap/runs/resume-finding.md','Scope: checkout. Saved next action resumed; primary code, test, docs agree on fee 3 for packing. Scope excludes inventory availability per docs. PB-012 allocated after preserved next_pb=12. Source checks: src/checkout.py::total, tests/test_checkout.py::test_total, docs/checkout.md. Existing test read but not run; no test execution command declared in pyproject.toml. Next: publish reviewed product and engineering pages.\n')
h('checkpoint','--scope','checkout','--status','partial','--next','Publish reviewed PB-012 product and engineering pages','--finding','.bootstrap/runs/resume-finding.md')
base={'schema_version':1,'scope':'checkout','revision':'working-tree','sources':[{'path':'src/checkout.py','section':'total'},{'path':'tests/test_checkout.py','section':'test_total'},{'path':'docs/checkout.md'}],'watches':['src/checkout*.py','tests/test_checkout*.py','docs/checkout*.md'],'verification':[],'implements':[],'behaviors':[],'depends_on':[]}
def draft(name,meta,body): write(REPO/'.bootstrap/runs'/name,'---\n'+json.dumps(base|meta,indent=2)+'\n---\n\n'+body)
draft('checkout-product.md',{'id':'CAP-checkout','kind':'product','title':'Checkout fee','behaviors':[pb],'depends_on':['CMP-checkout']},'''# Checkout fee

## Purpose
The checkout documentation states that the fixed fee covers packing costs. This is documented intent; the implementation and test corroborate the fee amount.

<a id="pb-012"></a>
## PB-012 — Add the packing fee
Observed and intended behavior agree: checkout adds 3 to the supplied subtotal. For example, subtotal 10 produces 13. No currency is specified by the supplied evidence. [Implementation and verification](../engineering/checkout.md).

## Ownership and handoffs
Checkout owns this fee calculation. It does not determine inventory availability, per docs/checkout.md. The inspected function accepts a subtotal and returns a total to its caller. No caller or inventory integration is established by this bounded fixture; this baseline makes no claim about payment collection or inventory orchestration.
''')
draft('checkout-engineering.md',{'id':'CMP-checkout','kind':'engineering','title':'Checkout total calculation','implements':[pb],'depends_on':['CAP-checkout'],'verification':[{'behavior':pb,'kind':'existing','reference':'tests/test_checkout.py::test_total'}]},'''# Checkout total calculation

## Responsibilities
src/checkout.py::total implements [PB-012](../product/checkout.md#pb-012). It owns adding the module-level FEE (3) to its input subtotal and returning the result. Inventory availability belongs outside checkout, according to docs/checkout.md; this function performs no inventory lookup or payment operation.

## Implementation and dependencies
The input subtotal is provided by a caller whose identity is not supplied. The function depends on the module constant and numeric addition. The test imports total directly. There are no external calls or other component handoffs in this function; repository evidence does not establish a broader checkout architecture.

## Verification
Existing: tests/test_checkout.py::test_total asserts total(10) == 13. The test was inspected, not executed, against the supplied working-tree fixture. pyproject.toml contains project metadata but no declared verification command. A fee change requires checking both total and its expected test value against packing-fee intent. Input-domain and boundary checks are not present in the supplied test; supported domains are not established. No new infrastructure was added. The enclosing Git revision is not a dedicated fixture revision.
''')
snap('before-publication')
h('publish','--draft','.bootstrap/runs/checkout-product.md','--to','context/product/checkout.md')
h('publish','--draft','.bootstrap/runs/checkout-engineering.md','--to','context/engineering/checkout.md')
h('publish','--draft','context/product/checkout.md','--to','context/product/checkout.md')
h('freshness'); h('check')
h('checkpoint','--scope','checkout','--status','complete','--next','Revalidate checkout sources before future changes')
snap('before-cleanup')
# Only known Groundwork-owned obsolete drafts/checkpoints; copies retained as evaluation evidence.
cmd('python3','-c','from pathlib import Path; import json; root=Path("."); state=root/".bootstrap/state.yaml"; data=json.loads(state.read_text()); data["scopes"]["checkout"].pop("checkpoint",None); state.write_text(json.dumps(data,indent=2)+"\\n"); paths=["current.md","resume-finding.md","checkout-product.md","checkout-engineering.md"]; [(root/".bootstrap/runs"/p).unlink() for p in paths if (root/".bootstrap/runs"/p).exists()]; print("Removed obsolete Groundwork drafts and checkpoint pointer")')
h('status'); h('check'); snap('final-snapshot')
