import json
from pathlib import Path
R=Path('/private/tmp/groundwork-resume-cleanup-xirc58xq/repo')
p=R/'.bootstrap/state.yaml'
s=json.loads(p.read_text())
s['scopes']['checkout']['status']='partial'
s['scopes']['checkout']['next_action']='When purpose evidence becomes available, validate it against Q-002 and current checkout sources; register supported intent provenance, update affected baseline pages, and reassess scope completion. Until then retain the observed fee-3 baseline and do not infer fee rationale.'
s['scopes']['checkout'].pop('checkpoint',None)
p.write_text(json.dumps(s,indent=2)+'\n')
for rel in ['.bootstrap/runs/obsolete-summary.md','.bootstrap/runs/purpose.md']:
    (R/rel).unlink()
    print('Removed obsolete Groundwork-owned draft:',rel)
print('Checkout remains partial; Q-002, tax scope, remediation, exclusions, external evidence and fingerprints retained.')
