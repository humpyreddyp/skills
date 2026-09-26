"""Additional fixture for fresh-session cleanup with all durable record types."""
from pathlib import Path
import datetime
import json
import shutil
import tempfile

out=Path(__file__).resolve().parent
evidence=out/'supplemental/resume-cleanup'
evidence.mkdir(parents=True,exist_ok=True)
repo=Path(tempfile.mkdtemp(prefix='groundwork-resume-cleanup-',dir='/private/tmp'))/'repo'
shutil.copytree(out/'fixtures/case-08',repo)
def write(name,value):
 p=repo/name;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(value if isinstance(value,str) else json.dumps(value,indent=2)+'\n')
write('src/tax.py','TAX_RATE = 0.05\n')
write('docs/tax.md','# Current tax intent\nThe agreed tax rate is 0.06.\n')
write('notes/user-notes.md','User-owned note: retain this file.\n')
st=json.loads((repo/'.bootstrap/state.yaml').read_text())
st['scopes']['tax']={'status':'waiting for human','next_action':'Verify R-001 after engineering completes the tax rate correction'}
st['scopes']['checkout']['next_action']='Review checkout progress, retain unanswered purpose question, and remove obsolete Groundwork drafts after confirming their content is durable'
st['next_question']=4
write('.bootstrap/state.yaml',st)
qs=json.loads((repo/'.bootstrap/questions.yaml').read_text())
qs.append({'id':'Q-003','scope':'tax','found':'docs/tax.md requests 0.06; src/tax.py currently uses 0.05','sources':['docs/tax.md','src/tax.py'],'why':'Tax changes affect charged totals','affects':['CAP-tax','CMP-tax'],'question':'Which rate should apply?','blocking':True,'status':'conflicting','decision':'R-001','answer':{'summary':'FIX: engineering should align implementation to 0.06, record work only.','github_id':'fixture-owner','sources':['docs/tax.md']},'validation':'Intent remains different from current implementation; no completed fix verified.'})
write('.bootstrap/questions.yaml',qs)
write('.bootstrap/remediation.yaml',[{'id':'R-001','question_id':'Q-003','scope':'tax','affects':['CAP-tax','CMP-tax'],'sources':['docs/tax.md','src/tax.py'],'action':'Align tax implementation and tests to agreed 0.06 rate','status':'open','decision':{'choice':'FIX','human_statement':'Engineering should align tax implementation to 0.06; record remediation only.','github_id':'fixture-owner'}}])
write('.bootstrap/runs/obsolete-summary.md','Obsolete completed finding: observed checkout fee is 3. This is already published in context/product/fee.md and context/engineering/fee.md.\n')
prompt='Continue Groundwork for checkout from saved state in this new session. I have no prior conversation to provide and no answer to the saved purpose question. Review the current checkout baseline and next action, and remove obsolete Groundwork-owned drafts whose useful content is already durable. Leave a clear next step. Do not implement application changes.'
(evidence/'prompt.txt').write_text(prompt+'\n')
(evidence/'setup.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repo':str(repo),'source_case':'case-08 completed state','additional_fixture_records':'Synthetic unrelated tax contradiction/remediation, user note, obsolete owned draft; not historical evaluation outputs'},indent=2)+'\n')
shutil.copytree(repo,evidence/'before')
print(repo)
