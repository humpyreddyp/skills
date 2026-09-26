Scope: checkout
Conclusion: unresolved same-scope contradiction. docs/checkout.md requires current fee 2; src/checkout.py::total adds 3; tests/test_checkout.py::test_total expects 13 for subtotal 10. The test function passes when executed directly with Python 3 -B/runpy at no-git, but a passing implementation test does not settle intended policy. No version/environment distinction or additional context was found across all four source files.
Blocked: PB-001 fee claim; do not publish it. No independent useful scoped behavior is available in this tiny fee-only fixture.
Question: Q-001 preserves explicit FIX/IGNORE options; no decision has been made.
Next: obtain explicit policy/disposition when human context is available, then verify evidence before publication.
