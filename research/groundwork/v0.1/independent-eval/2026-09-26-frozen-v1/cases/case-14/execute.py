from pathlib import Path
import sys,json,shutil
ROOT=Path('/Users/humpyreddypininti/Documents/ChatGPT/skilly/independent-evaluation/2026-09-26-frozen-v1'); sys.path.insert(0,str(ROOT)); from record_command import run
CASE=ROOT/'cases/case-14'; REPO=ROOT/'fixtures/case-14'; HELPER='/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork/scripts/bootstrap.py'
def cmd(*a): return run(CASE/'raw.jsonl',list(a),REPO)
def h(*a): return cmd('python3',HELPER,'--repo',str(REPO),*a)
def write(p,t): return cmd('python3','-c','from pathlib import Path; import sys; p=Path(sys.argv[1]); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(sys.argv[2]); print("Wrote",p)',str(p),t)
def snap(n):
    for d in ['.bootstrap','context']:
        if (REPO/d).exists(): shutil.copytree(REPO/d,CASE/n/d,dirs_exist_ok=True)
h('init','--scope','checkout-warehouse')
pb1=json.loads(h('allocate-pb').stdout)['behavior']; pb2=json.loads(h('allocate-pb').stdout)['behavior']; assert (pb1,pb2)==('PB-001','PB-002')
write(REPO/'.bootstrap/runs/current.md','Scope: checkout-warehouse responsibilities. Documentation establishes checkout payment-result acceptance and event emission, warehouse reservation ownership, exclusions for reservation/fulfillment and collecting payment, and decoupling purpose. Implementation and subscriptions establish payload id and actual handler target. No conflicting evidence in seven-file bounded scan. Existing test checks only constant equality and does not establish handoff. Next: publish ownership and verification coverage. Isolated-agent slots unavailable; no large investigation needed.\n')
h('checkpoint','--scope','checkout-warehouse','--status','partial','--next','Publish supported responsibilities, non-ownership, and event contract','--finding','.bootstrap/runs/current.md')
base={'schema_version':1,'scope':'checkout-warehouse','revision':'working-tree','sources':[{'path':p} for p in ['docs/checkout.md','src/checkout.py','deploy/subscriptions.json','warehouse/worker.py','tests/test_checkout.py','.github/workflows/check.yml']],'watches':['src/checkout*.py','warehouse/*.py','deploy/*subscriptions*.json','docs/checkout*.md','tests/test_checkout*.py','tests/test_warehouse*.py','tests/test_*order*.py','.github/workflows/*.yml'],'behaviors':[],'implements':[],'depends_on':[],'verification':[]}
def draft(f,m,b): write(REPO/'.bootstrap/runs'/f,'---\n'+json.dumps(base|m,indent=2)+'\n---\n\n'+b)
draft('handoff.md',{'id':'CAP-order-handoff','kind':'product','title':'Checkout and warehouse responsibility boundary','behaviors':[pb1,pb2],'depends_on':['CMP-checkout','CMP-warehouse']},'''# Checkout and warehouse responsibility boundary

## Purpose
The documented handoff decouples payment from slow warehouse operations (docs/checkout.md). Checkout accepts payment results and emits an order.paid event; warehouse owns stock reservation. This states intended ownership. The observed functions corroborate event emission and reservation delegation, but do not themselves demonstrate payment collection or a deployed delivery guarantee.

<a id="pb-001"></a>
## PB-001 — Checkout accepts and emits the handoff
When invoked with an order and bus, checkout publishes order.paid carrying {"id": order.id}, then returns {"status": "accepted"}. Checkout owns creating this event. It does not reserve stock or guarantee fulfillment. An accepted return is not proof of warehouse completion. [Implementation and checks](../engineering/checkout.md).

<a id="pb-002"></a>
## PB-002 — Warehouse owns reservation
Configuration routes order.paid to warehouse/worker.py:reserve. The handler reads message["id"] and delegates to inventory.reserve. Warehouse owns this reservation step and does not collect payment. [Implementation and checks](../engineering/warehouse.md).

## Handoff and limits
The responsibility passes from checkout's bus publication to the configured warehouse handler carrying the order ID. The subscription mapping is direct evidence of that connection; matching names alone are not the basis. The runtime bus, payment-result caller, and inventory implementation are unavailable. Retry, delivery, duplicate-message handling, and actual fulfillment guarantees are not established. Those are coverage limits rather than invented responsibilities for either component.
''')
draft('checkout.md',{'id':'CMP-checkout','kind':'engineering','title':'Checkout responsibilities','implements':[pb1],'depends_on':['CAP-order-handoff'],'verification':[{'behavior':pb1,'kind':'existing','reference':'tests/test_checkout.py::test_event_name; constant equality only'},{'behavior':pb1,'kind':'gap','reference':'Exercise checkout with a fake bus to verify event, id, and return; contract-check subscription and warehouse handler'}]},'''# Checkout responsibilities

## Owns
src/checkout.py::checkout implements [PB-001](../product/handoff.md#pb-001): it reads order.id, calls the supplied bus.publish with order.paid and an id payload, then returns accepted. Documentation supplies the reason for this boundary: isolate payment from slow warehouse work.

## Does not own
Per docs/checkout.md, checkout neither reserves stock nor guarantees fulfillment. The function contains no inventory call, warehouse completion wait, or payment-validation logic. The payment-result caller and bus adapter are not present, so this baseline does not assert how they establish payment validity or event delivery.

## Handoff
Input is the order and bus; output is an event plus the accepted return. deploy/subscriptions.json routes that event to [warehouse.reserve](warehouse.md). The shared contract is event name order.paid and payload key id. Renaming either requires checking producer, deployment mapping, and consumer together. Checkout returning accepted does not establish that reserve has run.

## Verification
Existing tests/test_checkout.py::test_event_name checks only literal equality and never calls checkout. It is not implementation or handoff coverage. CI declares python -m pytest; tests were inspected, not executed for this fixture. Revision is the supplied working tree; the enclosing repository SHA does not identify a dedicated fixture commit.

Missing checks: unit-check exact publication and accepted return using a fake bus; contract-check event and payload against subscription/consumer; integration-check actual delivery where bus and inventory infrastructure are available. A failure or retry requirement needs explicit policy evidence before claiming guarantees.
''')
draft('warehouse.md',{'id':'CMP-warehouse','kind':'engineering','title':'Warehouse responsibilities','implements':[pb2],'depends_on':['CAP-order-handoff'],'verification':[{'behavior':pb2,'kind':'gap','reference':'Check reserve passes message id to inventory; contract/integration-check configured order.paid handoff'}]},'''# Warehouse responsibilities

## Owns
warehouse/worker.py::reserve implements [PB-002](../product/handoff.md#pb-002). It reads message["id"] and passes the value to inventory.reserve. docs/checkout.md assigns stock reservation to warehouse; the injected inventory adapter owns details unavailable in this fixture.

## Does not own
The documentation explicitly states warehouse does not collect payment. This handler receives an already named paid-order event and does not process a payment result, charge a customer, or set checkout's accepted return. The supplied implementation also does not establish end-to-end fulfillment or durable reservation success; do not infer those guarantees from the method name.

## Handoff
Upstream [checkout](checkout.md) publishes order.paid with id; deploy/subscriptions.json selects warehouse/worker.py:reserve. This is the proven configuration connection. Warehouse's downstream call is inventory.reserve(message["id"]); the adapter implementation and transport runtime are outside the evidence. Changes to consumed payload keys must be coordinated with the producer and subscription contract.

## Verification
The complete seven-file source inventory contains no warehouse test. The checkout test only compares constants, and no tests were run for this fixture. Needed checks: fake-inventory unit check for forwarded id, producer/consumer payload contract check, and configured-bus integration check. Duplicate delivery, malformed messages, and failures would need agreed semantics and corresponding checks if future work changes those cases.
''')
snap('before-publication')
h('publish','--draft','.bootstrap/runs/handoff.md','--to','context/product/handoff.md')
h('publish','--draft','.bootstrap/runs/checkout.md','--to','context/engineering/checkout.md')
h('publish','--draft','.bootstrap/runs/warehouse.md','--to','context/engineering/warehouse.md')
h('publish','--draft','context/product/handoff.md','--to','context/product/handoff.md')
h('freshness'); h('check')
h('checkpoint','--scope','checkout-warehouse','--status','complete','--next','Revalidate checkout, subscription, and warehouse evidence before changing the handoff')
snap('before-cleanup')
cmd('python3','-c','from pathlib import Path; import json; p=Path(".bootstrap/state.yaml"); d=json.loads(p.read_text()); d["scopes"]["checkout-warehouse"].pop("checkpoint",None); p.write_text(json.dumps(d,indent=2)+"\\n"); [p.unlink() for p in Path(".bootstrap/runs").glob("*.md")]; print("Removed obsolete Groundwork drafts and checkpoint pointer")')
h('status'); h('check'); snap('final-snapshot')
