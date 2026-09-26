Scope: checkout fee.
Conclusion: The human establishes intended fee 2 and chooses future engineering remediation. Current code remains FEE=3 and the test expects 13 for subtotal 10. The fix has not occurred, so the fee claim remains blocked.
Sources: src/checkout.py::FEE,total; tests/test_checkout.py::test_total; docs/checkout.md.
Unresolved: Q-001.
Next: Await engineering remediation R-001, then inspect and verify completed implementation and tests.
