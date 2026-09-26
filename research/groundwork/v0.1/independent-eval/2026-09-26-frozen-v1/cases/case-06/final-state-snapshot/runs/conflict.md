# Checkout conflict
Scope: checkout. Q-001 remains conflicting and blocks CAP-fee/PB-001.
Observed: src/checkout.py adds FEE=3; tests/test_checkout.py expects total(10)=13; docs/checkout.md states fee 3 for packing. The human asserts fee 2. No source resolves the mismatch. No fee claim is published as trusted context.
Supported independent detail: docs describe packing costs and exclusion of inventory availability; these can be investigated/published separately if desired.
Next action: ask whether to FIX implementation/tests/docs for fee 2 or IGNORE a specific source/claim with rationale, or leave unresolved. No choice inferred.
