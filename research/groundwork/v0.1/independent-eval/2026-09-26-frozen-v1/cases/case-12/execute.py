from pathlib import Path
import sys,json,shutil
ROOT=Path('/Users/humpyreddypininti/Documents/ChatGPT/skilly/independent-evaluation/2026-09-26-frozen-v1'); sys.path.insert(0,str(ROOT)); from record_command import run
CASE=ROOT/'cases/case-12'; REPO=ROOT/'fixtures/case-12'; HELPER='/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork/scripts/bootstrap.py'
def cmd(*a): return run(CASE/'raw.jsonl',list(a),REPO)
def h(*a): return cmd('python3',HELPER,'--repo',str(REPO),*a)
def write(p,t): return cmd('python3','-c','from pathlib import Path; import sys; p=Path(sys.argv[1]); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(sys.argv[2]); print("Wrote",p)',str(p),t)
def snap(n):
    for d in ['.bootstrap','context']:
        if (REPO/d).exists(): shutil.copytree(REPO/d,CASE/n/d,dirs_exist_ok=True)
h('init','--scope','paid-order')
pb1=json.loads(h('allocate-pb').stdout)['behavior']; pb2=json.loads(h('allocate-pb').stdout)['behavior']; assert (pb1,pb2)==('PB-001','PB-002')
write(REPO/'.bootstrap/runs/current.md','Scope: paid-order. Checkout publishes order.paid with id, subscriptions route it to warehouse reserve, which calls inventory.reserve. Docs establish decoupling purpose and ownership boundaries. Existing test is tautological and does not call implementation. CI declares python -m pytest; safe local attempt failed because pytest is unavailable. No infrastructure installed. Seven relevant source files read; all agent slots occupied, so investigation remains bounded. Next: publish traceability and explicit verification gaps.\n')
h('checkpoint','--scope','paid-order','--status','partial','--next','Publish paid-order traceability and verification gaps','--finding','.bootstrap/runs/current.md')
sources=[{'path':p} for p in ['docs/checkout.md','src/checkout.py','deploy/subscriptions.json','warehouse/worker.py','tests/test_checkout.py','.github/workflows/check.yml']]
base={'schema_version':1,'scope':'paid-order','revision':'working-tree','sources':sources,'watches':['src/checkout*.py','deploy/*subscriptions*.json','warehouse/*.py','tests/test_checkout*.py','tests/test_warehouse*.py','tests/test_*order*.py','docs/checkout*.md','.github/workflows/*.yml'],'behaviors':[],'implements':[],'verification':[],'depends_on':[]}
def draft(file,m,b): write(REPO/'.bootstrap/runs'/file,'---\n'+json.dumps(base|m,indent=2)+'\n---\n\n'+b)
draft('paid-order.md',{'id':'CAP-paid-order','kind':'product','title':'Paid-order handoff','behaviors':[pb1,pb2],'depends_on':['CMP-checkout','CMP-warehouse']},'''# Paid-order handoff

## Purpose
Documented intent: separate payment results from slow warehouse operations. Checkout accepts payment results; warehouse owns stock reservation. Source: docs/checkout.md. The implementation demonstrates event publication and reservation delegation, not payment processing or successful fulfillment.

<a id="pb-001"></a>
## PB-001 — Publish an accepted order handoff
Observed: when checkout(order, bus) is called, it publishes order.paid with a payload containing id=order.id, then returns status=accepted. The function contains no payment validation or receipt of a warehouse result. The caller is responsible for the precondition described in the documentation; the fixture does not establish that caller. [Checkout implementation and checks](../engineering/checkout.md).

<a id="pb-002"></a>
## PB-002 — Delegate stock reservation
Observed configuration: deploy/subscriptions.json maps order.paid to warehouse/worker.py:reserve. That handler passes message["id"] to inventory.reserve. This establishes the intended routing and consumer contract; no running broker or real inventory outcome was verified. [Warehouse implementation and checks](../engineering/warehouse.md).

## Ownership and handoffs
Checkout owns emitting the paid-order event, not stock reservation or guaranteed fulfillment. It hands the order ID to the configured warehouse consumer through the bus. Warehouse owns reservation delegation, not collecting payment. Inventory implementation and bus delivery semantics are outside the supplied evidence. No guarantee about retries, duplicate delivery, atomicity, or eventual reservation is established by this baseline.
''')
draft('checkout.md',{'id':'CMP-checkout','kind':'engineering','title':'Checkout event producer','implements':[pb1],'depends_on':['CAP-paid-order'],'verification':[{'behavior':pb1,'kind':'existing','reference':'tests/test_checkout.py::test_event_name (tautological; no implementation coverage)'},{'behavior':pb1,'kind':'gap','reference':'Unit-check checkout publishes order.paid with order.id and returns accepted; contract-check payload against subscription and reserve consumer'}]},'''# Checkout event producer

## Responsibilities
src/checkout.py::checkout implements [PB-001](../product/paid-order.md#pb-001). It emits an event and returns acceptance. Per docs/checkout.md it does not reserve stock or guarantee fulfillment. It does not itself validate or collect payment; the documented payment-result precondition belongs to a caller absent from this fixture.

## Implementation and dependencies
Input: order with an id attribute and a supplied bus. Output: bus.publish("order.paid", {"id": order.id}), then an accepted status. deploy/subscriptions.json maps that exact event to warehouse/worker.py:reserve, which consumes the id key; see [warehouse](warehouse.md). This config is the evidence for the connection despite no import. The bus and inventory adapters are injected and their implementation is unavailable. Exceptions before the return are not caught here; no end-to-end delivery guarantee is established.

## Verification
Existing tests/test_checkout.py::test_event_name asserts one constant string equals itself. It neither invokes checkout nor verifies the event, payload, routing, or return value. CI declares python -m pytest in .github/workflows/check.yml. A local working-tree attempt, python3 -m pytest -p no:cacheprovider, failed before collection: No module named pytest. No tests passed and no dependency was installed. The enclosing repository SHA is not a dedicated fixture revision.

Needed checks: call checkout with a stub bus and order to assert the exact event, id payload, and accepted return; contract-check the emitted event against deploy/subscriptions.json and warehouse.reserve; check behavior when publish fails if future changes need an error guarantee. A producer schema/event-name change must include the consumer and subscription, even if their files would otherwise stay unchanged.
''')
draft('warehouse.md',{'id':'CMP-warehouse','kind':'engineering','title':'Warehouse reservation consumer','implements':[pb2],'depends_on':['CAP-paid-order'],'verification':[{'behavior':pb2,'kind':'gap','reference':'Unit-check reserve forwards message id; integration/contract-check order.paid subscription and producer-to-consumer handoff'}]},'''# Warehouse reservation consumer

## Responsibilities
warehouse/worker.py::reserve implements [PB-002](../product/paid-order.md#pb-002). Warehouse owns stock reservation, delegating it to supplied inventory.reserve. It does not collect payment, according to docs/checkout.md. It does not establish payment validity or guarantee fulfillment in the supplied implementation.

## Implementation and dependencies
The handler reads message["id"] and calls inventory.reserve with that value. deploy/subscriptions.json routes order.paid to this handler; src/checkout.py::checkout supplies that event and key. See [producer](checkout.md). An event name or payload change therefore crosses both components and deployment wiring. The inventory adapter and running bus are not provided, so actual reservation completion, persistence, duplicate handling, and delivery semantics remain outside this baseline.

## Verification
There is no warehouse test in the complete seven-file inventory. tests/test_checkout.py::test_event_name provides no consumer or handoff coverage. CI's pytest command could not run locally because pytest is unavailable; no runtime result is claimed.

Needed checks: unit-check that reserve forwards the exact order ID to a fake inventory; contract-check producer payload and subscription target; integration-check delivery through the configured bus to inventory when that infrastructure is available. Changes to the message shape should also verify checkout, not just this handler. Retry/idempotency and failure handling require additional specification and checks if they become part of a future change.
''')
snap('before-publication')
h('publish','--draft','.bootstrap/runs/paid-order.md','--to','context/product/paid-order.md')
h('publish','--draft','.bootstrap/runs/checkout.md','--to','context/engineering/checkout.md')
h('publish','--draft','.bootstrap/runs/warehouse.md','--to','context/engineering/warehouse.md')
h('publish','--draft','context/product/paid-order.md','--to','context/product/paid-order.md')
h('freshness'); h('check')
h('checkpoint','--scope','paid-order','--status','complete','--next','Revalidate paid-order sources and cross-component contracts before changes')
snap('before-cleanup')
cmd('python3','-c','from pathlib import Path; import json; p=Path(".bootstrap/state.yaml"); d=json.loads(p.read_text()); d["scopes"]["paid-order"].pop("checkpoint",None); p.write_text(json.dumps(d,indent=2)+"\\n"); [p.unlink() for p in Path(".bootstrap/runs").glob("*.md")]; print("Removed obsolete Groundwork drafts and checkpoint pointer")')
h('status'); h('check'); snap('final-snapshot')
