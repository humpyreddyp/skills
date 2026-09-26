from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record_command import run
r=Path(__file__).resolve().parents[2]
requests=json.loads((r/'fixtures/requests.json').read_text())
for n in (5,6,7,8):
 c=r/'cases'/f'case-{n:02d}'; f=r/'fixtures'/f'case-{n:02d}'
 (c/'request.txt').write_text(requests[str(n)]['request']+'\n')
 print('CASE',n)
 run(c/'raw.jsonl',['cat','.bootstrap/questions.yaml','.bootstrap/remediation.yaml','.bootstrap/exclusions.yaml','.bootstrap/external.yaml','.bootstrap/tracking.yaml','src/checkout.py','tests/test_checkout.py','docs/checkout.md','pyproject.toml'],f)
