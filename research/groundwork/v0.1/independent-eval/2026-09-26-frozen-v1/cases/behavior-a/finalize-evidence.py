"""Finalize executor metadata without changing fixture behavior or helper code."""
import json
from pathlib import Path
root=Path('/Users/humpyreddypininti/Documents/ChatGPT/skilly/independent-evaluation/2026-09-26-frozen-v1/cases')
for n,source_count in [(1,5),(2,4),(3,3),(4,7),(10,4),(11,6)]:
    case=root/f'case-{n:02}'
    metrics=json.loads((case/'metrics.json').read_text())
    writes=(case/'authored-writes.jsonl').read_text().splitlines()
    metrics['authored_fixture_write_or_delete_steps']=len(writes)
    metrics['recorded_execution_steps']=metrics['command_steps']+len(writes)
    metrics['primary_fixture_content_files_read']=source_count
    metrics['generated_state_content_files_read']=metrics['content_files_read']-source_count
    metrics['step_definition']='Each recorder command plus each authored fixture-file write/deletion. Evidence bookkeeping and snapshot copies are not investigation steps.'
    (case/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    (case/'evidence-manifest.md').write_text('Case prompt: prompt.txt\n\nAppend-only commands and raw outputs: raw.jsonl\n\nFixture writes/deletions: authored-writes.jsonl; exact authored execution scripts in this folder. Shared driver: ../behavior-a/driver.py.\n\nRead list: inspected-files.json. Counts and definition: metrics.json.\n\nIntermediate/final saved state: snapshots/. Actual final baseline is in ../../fixtures/'+f'case-{n:02}'+'/\n\nFinal response and observations: final-response.md; observations.md.\n\nCommon initial skill/reference reads, delegation prompt and execution constraints are retained in ../behavior-a/. This shared-folder location is a deviation from the request to keep evidence under case-NN folders; it does not include other agents’ outcomes. No previous evaluation outcomes, fixture generator, regression suite or other executing agents’ reports were read.\n')
case=root/'case-02'
with (case/'final-response.md').open('a') as f:
    f.write('\n[Groundwork SKILL.md](/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork/SKILL.md) says, “If a contradiction remains, the human chooses **FIX** or **IGNORE**.” This unresolved current-fee disagreement needs that choice.\n')
(root/'behavior-a/setup-notes.md').write_text('Initial setup ran pwd, created the shared evidence folder, saved the exact delegation prompt, then read record_command.py before using the recorder. These bootstrap operations appear in tool history, but not the append-only recorder log because the recorder API was not yet known. A subsequent recorded cat request for requests.json used the wrong root path and failed; the skill text in that same command was successfully read. One rg discovery command failed in zsh before the recorder launched because of an unquoted glob. It was retried with only the requests.json glob and found fixtures/requests.json. No skill/helper failure or repair occurred. The shared driver imports the recorder and reads the request map for exact prompt copies; that map had already been read in the common raw log. Metrics bookkeeping reads evidence records but does not load new fixture content into model context. Case content reads are recorded by cat commands.\n\nAll four agent slots were occupied at the check. No child agent was spawned. Each case used bounded source investigation and saved checkpoints. Cases share this executor context; prior context was not cleared. Token counts are unavailable. Helper scan returns the enclosing Git revision, not an independent fixture commit; pages use working-tree provenance.\n')
print(json.dumps({f'case-{n:02}':json.loads((root/f'case-{n:02}'/'metrics.json').read_text()) for n in [1,2,3,4,10,11]},indent=2))
