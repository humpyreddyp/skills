import sys,json
sys.path.insert(0,'/Users/humpyreddypininti/Documents/ChatGPT/skilly/independent-evaluation/2026-09-26-frozen-v1/cases/behavior-a')
sys.argv=['driver','4','noop']
from driver import *
a=json.loads(helper('allocate-pb').stdout)['behavior']; b=json.loads(helper('allocate-pb').stdout)['behavior']
command(['python3','-c',"import runpy; runpy.run_path('tests/test_checkout.py')['test_event_name'](); print('test_event_name PASS (literal equality only; no application exercised)')"])
write('.bootstrap/runs/handoff.md','# Paid-order routing finding\nThe non-import connection is explicit: checkout publishes order.paid with id; deploy/subscriptions.json maps that event to warehouse/worker.py:reserve, which calls inventory.reserve(message["id"]). docs/checkout.md explains decoupling payment from slow warehouse operations and separates ownership. CI invokes python -m pytest, but the only discovered test compares a literal to itself. No bus implementation, inventory implementation, delivery guarantee, or payment validation is established. Next: publish the supported configured handoff and its verification gaps.\n')
helper('checkpoint','--scope','paid-order','--status','partial','--next','Publish the configured checkout-to-warehouse handoff and verification gaps','--finding','.bootstrap/runs/handoff.md'); snapshot('handoff-discovered')
sources=['docs/checkout.md','src/checkout.py','deploy/subscriptions.json','warehouse/worker.py','tests/test_checkout.py','.github/workflows/check.yml']
watches=['src/*checkout*.py','warehouse/*.py','deploy/*subscriptions*.json','tests/test*checkout*.py','tests/test*warehouse*.py','tests/test*order*.py','.github/workflows/*.yml','docs/*checkout*.md']
page('.bootstrap/runs/product.md',id='CAP-paid-order',kind='product',scope='paid-order',title='Paid-order handoff',sources=sources,watches=watches,behaviors=[a,b],body=f'''# Paid-order handoff

## Purpose and boundaries
Intended, per docs/checkout.md: checkout accepts payment results and the event handoff decouples payment from slow warehouse operations. Checkout does not reserve stock or guarantee fulfillment; warehouse owns reservation and does not collect payment. The code establishes the configured handoff below, not payment validation, successful fulfillment, or runtime delivery guarantees.

<a id="{a.lower()}"></a>
## {a} — Publish an order identifier
Observed: checkout calls its supplied bus with event `order.paid` and payload `{{"id": order.id}}`, then returns `{{"status": "accepted"}}` if publishing returns. Its input is an order; the implementation does not establish that payment has been validated.

<a id="{b.lower()}"></a>
## {b} — Hand the identifier to inventory reservation
Configured and observed in the consumer: `deploy/subscriptions.json` routes `order.paid` to `warehouse/worker.py:reserve`. That handler passes `message["id"]` to its supplied inventory object's `reserve` method. This establishes the reservation request, not that inventory allocation succeeds.

## Ownership and handoffs
Checkout owns event production; deployment configuration owns the event-to-handler mapping; the warehouse handler owns translating the incoming identifier to the inventory call. The supplied bus and inventory services form the remaining runtime boundary. Their internals and operational delivery/retry guarantees are unavailable in this fixture.

[Checkout implementation](../engineering/checkout.md) · [Warehouse implementation](../engineering/warehouse.md)
''')
helper('publish','--draft','.bootstrap/runs/product.md','--to','context/product/paid-order.md')
page('.bootstrap/runs/warehouse.md',id='CMP-warehouse',kind='engineering',scope='paid-order',title='Warehouse reservation consumer',sources=sources,watches=watches,implements=[b],depends_on=['CAP-paid-order'],verification=[{'behavior':b,'kind':'gap','reference':'Contract check routing order.paid payload id through warehouse.reserve to a fake inventory reserve call; reservation failure/idempotency expectations require the external inventory contract.'}],body=f'''# Warehouse reservation consumer

`warehouse/worker.py::reserve(message, inventory)` implements [{b}](../product/paid-order.md#{b.lower()}). It owns extracting `message["id"]` and forwarding it to `inventory.reserve`. Warehouse does not collect payment; inventory implementation is a supplied dependency outside the available code.

The incoming connection is established by `deploy/subscriptions.json`: event `order.paid` selects `warehouse/worker.py:reserve`. Checkout produces the required `id` field in `src/checkout.py`; imports are not the connection. Changes to event name or payload require review of producer, deployment mapping, and consumer together.

## Verification
No discovered check exercises the consumer or configured mapping. A contract/integration check should connect checkout's published event and payload through the mapping to the worker and assert the same id reaches inventory.reserve. Add isolated handler checks for the agreed payload contract. Delivery, retries, idempotency, and successful allocation cannot be verified without bus/inventory implementations and contracts; do not infer those guarantees.
''')
helper('publish','--draft','.bootstrap/runs/warehouse.md','--to','context/engineering/warehouse.md')
page('.bootstrap/runs/checkout.md',id='CMP-checkout',kind='engineering',scope='paid-order',title='Checkout paid-order producer',sources=sources,watches=watches,implements=[a],depends_on=['CAP-paid-order','CMP-warehouse'],verification=[{'behavior':a,'kind':'existing','reference':'tests/test_checkout.py::test_event_name (literal equality only)'},{'behavior':a,'kind':'gap','reference':'Exercise checkout with a fake bus; assert event name, id payload and accepted return; validate subscription and warehouse consumer contract.'}],body=f'''# Checkout paid-order producer

`src/checkout.py::checkout(order, bus)` implements [{a}](../product/paid-order.md#{a.lower()}). It publishes `order.paid` with `id` then returns accepted. It owns event creation, not stock reservation, fulfillment, or payment validation. Both order and bus come from its caller; the caller and bus implementation are absent from the available fixture.

## Handoff and change impact
`deploy/subscriptions.json` names the [warehouse consumer](warehouse.md) for `order.paid`; `warehouse/worker.py::reserve` requires the payload id. Changing event names, payload fields, or timing requires coordinated mapping/consumer review despite no direct import. The documentation states that this split isolates slow warehouse operations.

## Verification
CI in `.github/workflows/check.yml` declares `python -m pytest`. No install or CI run was performed. The discovered `test_event_name` was executed directly through Python runpy in the working-tree fixture: PASS, but it compares the same string literal to itself and does not exercise checkout. It provides no evidence that event production or routing works.

Verification gaps: test checkout using a fake bus and assert its event, payload and return value; add a producer-to-subscription-to-consumer contract check; test failures only against an established bus/inventory contract. No new test infrastructure was created and no live bus or warehouse action was invoked.
''')
helper('publish','--draft','.bootstrap/runs/checkout.md','--to','context/engineering/checkout.md')
helper('publish','--draft','context/product/paid-order.md','--to','context/product/paid-order.md')
helper('freshness'); helper('check'); snapshot('published-before-cleanup')
helper('checkpoint','--scope','paid-order','--status','complete','--next','Revalidate the event mapping and producer/consumer contract together when this flow changes; obtain external contracts before changing delivery guarantees')
cleanup('.bootstrap/runs/producer.md','.bootstrap/runs/handoff.md','.bootstrap/runs/product.md','.bootstrap/runs/warehouse.md','.bootstrap/runs/checkout.md')
finish('Published the paid-order baseline with two behavior IDs and linked checkout/warehouse pages. The connection is explicit in deploy/subscriptions.json: order.paid routes to warehouse.reserve, which forwards the order id to inventory.reserve. Ownership and change-impact checks are documented. The existing test passed but only compares identical literals; meaningful handoff verification is a recorded gap. Runtime bus/inventory guarantees remain outside the available evidence.', 'Seven primary source files read in two bounded investigations with a preserved intermediate checkpoint. Found the non-import event dependency through deployment configuration. Scope marked complete for the supported configured handoff, with explicit limits on live delivery, payment validation and inventory success. No helper failure.', 'None needed for the documented configured handoff. External bus/inventory contracts are needed before asserting or changing operational delivery/retry guarantees.')
