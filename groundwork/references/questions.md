# Questions and human decisions

Ask when a missing answer could change the baseline or make a future change unsafe. First check whether the repo and supplied context can answer it. People should not have to repeat what the evidence already says.

## Ask a question someone can answer

State what you found, where you found it, why the difference matters, what it affects, and the decision you need. Save the question before asking so another session can continue from it.

For example: “The current refund policy allows 14 days, but the handler rejects requests after 7. Both appear to cover web orders. Which rule should apply, and which source needs correction?”

Use the question fields in [state-format.md](state-format.md). Mark whether the question blocks publication or completion. Batch non-blocking questions at a checkpoint, keep working on unaffected claims, and reuse an existing question instead of asking it again every session.

## Check the answer

Save a concise, faithful answer summary and any supplied source or revision. Record the answerer's GitHub ID when provided or available from authenticated authorship. Otherwise use null; local Git configuration does not establish who answered.

Compare the answer with the available evidence. Record a short comparison and mark the question resolved, conflicting, or needing evidence as appropriate. A human answer may establish intent while the implementation still differs. Preserve that distinction.

If the answer conflicts with evidence, show the mismatch and its consequence respectfully. Do not silently replace the baseline with the answer, or assume the implementation must be right.

## Let the human choose FIX or IGNORE

When a contradiction still matters, explain the options and ask for an explicit choice. They may also leave it unresolved. Never infer a choice from silence or choose on their behalf.

### FIX: record the work

Save an open remediation item with the requested correction, scope, affected claims, sources, and human decision. Groundwork does not perform the fix.

A recorded fix is still future work. Keep the blocked claim unpublished until the completed fix is verified or other evidence independently resolves the question. Recording a decision does not close remediation or publish a claim.

### IGNORE: record exactly what to exclude

Save the source and claim being excluded, its scope, rationale, affected IDs, decision maker, and when to review it again. Keep the exclusion as narrow as the human's choice. Excluding one outdated sentence does not discard every other claim in the document.

The remaining claim still needs support. If a published page relied on the excluded evidence, mark it for revalidation immediately. When the source changes, review the exclusion before applying it to the new revision. Do not silently broaden or retire it.

A source can support several claims while being excluded for one. The helper conservatively marks affected pages and pages citing that source for review; the agent decides which conclusions need attention.

## Record the decision, then reassess

Use the `decision` examples in [commands.md](commands.md) only after the human has made the choice. The command records their statement; it cannot establish that authorization happened.

After recording FIX or IGNORE, check the evidence again before resolving the question or publishing. Keep useful supported context moving while the disputed part remains open.
