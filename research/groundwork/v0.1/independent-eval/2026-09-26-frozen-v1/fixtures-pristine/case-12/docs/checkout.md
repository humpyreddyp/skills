# Paid order handoff
Checkout accepts payment results and emits an order.paid event.
Warehouse owns stock reservation. Checkout does not reserve stock or guarantee fulfillment.
Warehouse does not collect payment. The handoff decouples payment from slow warehouse operations.
