Case prompt: prompt.txt

Append-only commands and raw outputs: raw.jsonl

Fixture writes/deletions: authored-writes.jsonl; exact authored execution scripts in this folder. Shared driver: ../behavior-a/driver.py.

Read list: inspected-files.json. Counts and definition: metrics.json.

Intermediate/final saved state: snapshots/. Actual final baseline is in ../../fixtures/case-01/

Final response and observations: final-response.md; observations.md.

Common initial skill/reference reads, delegation prompt and execution constraints are retained in ../behavior-a/. This shared-folder location is a deviation from the request to keep evidence under case-NN folders; it does not include other agents’ outcomes. No previous evaluation outcomes, fixture generator, regression suite or other executing agents’ reports were read.
