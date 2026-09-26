Marked the checkout fee product page (CAP-fee / PB-001) and engineering page (CMP-fee) as needing revalidation. The checkout source fingerprint changed; the engineering page also depends on the affected product behavior.

The receipt product and engineering pages remain current. All four baseline Markdown pages are byte-for-byte unchanged.

The current code uses fee 4, while documentation still says 3 and the test expects total(10) = 13. The saved next step is to investigate that mismatch before reviewing and republishing the fee pages. No human decision was assumed.
