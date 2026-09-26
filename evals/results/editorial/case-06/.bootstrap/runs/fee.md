Scope: checkout fee.
Conclusion: The requested current fee 2 conflicts with FEE=3, test expectation total(10)=13, and current docs stating fee 3 for packing. No version or environment distinction is present. A request to reflect 2 does not explicitly choose FIX or IGNORE.
Sources: src/checkout.py::FEE,total; tests/test_checkout.py::test_total; docs/checkout.md.
Unresolved: Q-001.
Next: Obtain explicit FIX/IGNORE decision or reconciling evidence.
