from pathlib import Path
import json,sys,shutil,hashlib
r=Path(__file__).resolve().parents[2];sys.path.insert(0,str(r))
from record_command import run
skill=Path('/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork')
for n in (5,6,7,8):
 c=r/'cases'/f'case-{n:02d}';f=r/'fixtures'/f'case-{n:02d}'
 run(c/'raw.jsonl',['python3',str(skill/'scripts/bootstrap.py'),'--repo',str(f),'status'],f)
 run(c/'raw.jsonl',['cat','.bootstrap/state.yaml','.bootstrap/questions.yaml','.bootstrap/remediation.yaml','.bootstrap/exclusions.yaml','.bootstrap/external.yaml','context/index.yaml'],f)
 shutil.copytree(f/'.bootstrap',c/'final-state-snapshot')
 if (f/'context').exists():shutil.copytree(f/'context',c/'final-context-snapshot')
 files=['.bootstrap/state.yaml','.bootstrap/questions.yaml','.bootstrap/remediation.yaml','.bootstrap/exclusions.yaml','.bootstrap/external.yaml','.bootstrap/tracking.yaml','src/checkout.py','tests/test_checkout.py','docs/checkout.md','pyproject.toml','context/index.yaml']
 shared=[str(skill/'SKILL.md')]+[str(skill/'references'/x) for x in ['commands.md','state-format.md','evidence.md','questions.md']]+[str(skill/'assets'/x) for x in ['product.md','engineering.md']]
 (c/'inspected-files.json').write_text(json.dumps({'fixture_files':[str(f/p) for p in files],'shared_skill_reads_logged_in':'../case-05/raw.jsonl','skill_files':shared,'note':'State first; index initially absent. Shared skill read once before applying it to cases 5–8. Requests read from fixtures/requests.json; authored drivers are preserved.'},indent=2)+'\n')
 hashes={str(p.relative_to(f)):hashlib.sha256(p.read_bytes()).hexdigest() for p in f.rglob('*') if p.is_file()}
 (c/'final-file-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 print('FINAL EVIDENCE SNAPSHOT',n)
