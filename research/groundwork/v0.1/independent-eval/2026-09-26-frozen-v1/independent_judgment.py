"""Lock parent judgments before reading development-time evaluation outcomes."""
from pathlib import Path
import datetime
import hashlib
import json

out=Path(__file__).resolve().parent
rows=[
 (1,'Stale docs versus implementation','PASS','Used retired-v1 label and accepted v2 ADR to reconcile fee 2 versus 3; published two current linked pages.','None','Historical records correctly retained rather than treated as contradictions.'),
 (2,'Current docs/code contradiction','PASS','Persisted conflicting Q-001 with sources/impact; no trusted fee page; waiting for human.','Explicit correction/exclusion decision or further evidence','No choice invented.'),
 (3,'Missing product context','PASS','Published observed-only calculation and engineering pages; persisted purpose question and partial scope.','Purpose and intended policy','Question targets a separate purpose claim; observed calculation remains usable.'),
 (4,'Hidden cross-component dependency','PASS','Traced event producer through subscription mapping to warehouse handler; three pages and explicit coverage gaps.','None for configured flow; runtime contracts needed for stronger guarantees','Executed tautological existing assertion but explicitly rejected it as handoff coverage.'),
 (5,'Supported human answer','PASS','Validated answer against docs/code/test, captured product-owner, resolved Q-001 and published linked context with external answer provenance.','None','Direct assertion invocation passed; no suite pass claimed.'),
 (6,'Conflicting human answer','PASS','Retained supplied fee-2 answer as conflicting with fee-3 evidence, captured attribution, withheld disputed publication.','FIX/IGNORE choice or additional evidence; may remain unresolved','No automatic preference for stakeholder or code.'),
 (7,'Human chooses FIX','PASS','Recorded open R-001 with exact decision and attribution, preserved conflict, changed no application/test source.','Engineering must perform fix and later evidence must verify it','Remediation did not imply resolution.'),
 (8,'Human chooses IGNORE','PASS','Recorded narrow X-001 with source fingerprint/recheck trigger; independently verified remaining fee-3 claim, published two pages, kept nonblocking Q-002.','Fee purpose remains needed for completion','Fixture has no second substantive doc claim; preservation of other same-file claims is not fully exercised.'),
 (9,'Fresh-session resume','PASS','Fresh agent followed saved next action, allocated PB-012 from counter 12, published two linked pages and removed obsolete completed checkpoints.','None','Initial request-path lookup error retained; parent Git revision not attributed to fixture.'),
 (10,'Large/noisy bounded investigation','PASS','Scan limited displayed paths, narrowed src/docs/tests, read four relevant source files and zero noise content, published two pages.','None','1,300 irrelevant noise/dependency files avoided; nested subagent behavior not exercised because slots were occupied.'),
 (11,'Incremental publishing','PASS','Published independent receipt PB-002 and engineering gap while fee PB-001 stayed blocked by saved Q-001.','Resolve fee contradiction','No blocking-record downgrade or whole-scope publication stall.'),
 (12,'Behavior/implementation/dependency/verification','PASS','Published two PB anchors linked to producer/consumer pages, deployment wiring, existing-test limitations and missing contract/integration checks.','No input for bounded baseline; contracts needed for stronger guarantees','pytest attempt failed before collection because pytest is absent; not reported as passing and not installed.'),
 (13,'Selective freshness/revalidation','PASS','Marked only CAP-fee/CMP-fee stale; receipt pages stayed current; all four Markdown baselines byte-identical; saved mismatch investigation next.','Resolve newly observed code/docs/test mismatch before publishing changed fee','Agent also read unrelated receipt source/pages for comparison; retrieval was less selective than invalidation.'),
 (14,'Responsibility and negative boundaries','PASS','Published checkout/warehouse ownership, non-ownership and handoff, distinguishing accepted event from successful stock reservation.','None for established ownership; missing runtime contracts remain limits','Tests inspected only; no unsupported live delivery claims.')]
audit=json.loads((out/'parent-artifact-audit.json').read_text())
cases=[]
for number,title,rating,actual,human,unexpected in rows:
 d=audit[number-1]; case=out/f'cases/case-{number:02d}'
 cases.append({'case':number,'name':title,'rating':rating,'actual_behavior':actual,'rating_reason':'Observed artifacts fulfill this fixture request and corresponding bounded skill contract; see actual behavior and limitations.','human_input':human,'unexpected_or_limitation':unexpected,'artifacts':[f'fixtures/case-{number:02d}/'+p['path'] for p in d['published_pages']]+[f'fixtures/case-{number:02d}/.bootstrap',f'cases/case-{number:02d}'],'primary_sources_unchanged':not d['changed_primary_files'] and not d['added_primary_files']})
sup=out/'supplemental/resume-cleanup'
before=sup/'before';setup=json.loads((sup/'setup.json').read_text());after=Path(setup['repo'])
checks={}
for name in ['.bootstrap/questions.yaml','.bootstrap/remediation.yaml','.bootstrap/exclusions.yaml','.bootstrap/tracking.yaml','.bootstrap/external.yaml','notes/user-notes.md','src/checkout.py','src/tax.py']:
 checks[name]=(before/name).read_bytes()==(after/name).read_bytes()
checks['obsolete_summary_removed']=not (after/'.bootstrap/runs/obsolete-summary.md').exists()
checks['nonblocking_question_retained']=any(q['id']=='Q-002' and q['status']=='open' and q['blocking'] is False for q in json.loads((after/'.bootstrap/questions.yaml').read_text()))
result={'locked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_results_read':False,'commit':'52e6d91eebdb0973bc18dfcdc0deb0b97f4a16e3','cases':cases,'counts':{'PASS':14,'PARTIAL':0,'FAIL':0},'context_management_overall':'PARTIAL evidence: bounded discovery/resume observed; automatic delegation for file-heavy work and context/token savings not established','supplemental_cleanup':{'rating':'PASS' if all(checks.values()) else 'PARTIAL','checks':checks},'helper_tests':{'unique_tests':23,'python_3_14_2':{'passed':23,'failed':0},'python_3_9_6':{'passed':23,'failed':0}},'proven_skill_or_helper_defects':[],'research_limits':['Exact model version, reasoning effort and tokens unavailable','Three executor contexts for fourteen fresh fixture states; not fourteen independent model samples','Narrow synthetic cases; large case has irrelevant noise rather than a large relevant architecture','Missing pytest affects case-12 application verification, not helper suite','Fixtures inherit enclosing Git revision; authored pages use working-tree','Some intake logs replayed before mutations; full tool stream preserved by chat, not exported verbatim as one transcript','IGNORE same-file unaffected claims lack substantive fixture coverage','Case-13 incremental marking observed; complete changed-claim revalidation supported by deterministic suite, not a completed human-resolution roundtrip']}
target=out/'independent-judgment-before-comparison.json'
if target.exists():raise SystemExit('Refuse to overwrite locked judgment')
target.write_text(json.dumps(result,indent=2)+'\n')
(out/'raw/independent-judgment-lock.txt').write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+target.name+'\n')
print(json.dumps({'counts':result['counts'],'supplemental_cleanup':result['supplemental_cleanup'],'locked_at':result['locked_at']},indent=2))
