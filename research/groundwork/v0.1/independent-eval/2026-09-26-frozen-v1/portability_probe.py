from pathlib import Path
import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from record_command import run

OUT = Path(__file__).resolve().parent
WT = Path('/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly')
LOG = OUT/'raw/portability.jsonl'
scratch = Path(tempfile.mkdtemp(prefix='groundwork-portability-', dir='/private/tmp'))
skill = WT/'groundwork'
summary = {'scratch': str(scratch), 'checks': {}, 'notes': []}
links = []
for p in skill.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
        if '://' not in target and not target.startswith('#'):
            dest = (p.parent/target.split('#')[0]).resolve()
            links.append({'file': str(p.relative_to(skill)), 'target': target, 'exists': dest.exists()})
summary['relative_links'] = links
summary['checks']['all_relative_links_resolve'] = all(x['exists'] for x in links)
summary['checks']['name'] = skill.joinpath('SKILL.md').read_text().splitlines()[1] == 'name: groundwork'
summary['checks']['no_old_folder_runtime_references'] = not any('bootstrap-context' in p.read_text() for p in skill.rglob('*') if p.is_file())
with zipfile.ZipFile(WT/'groundwork.zip') as z:
    summary['checks']['zip_matches_committed_skill'] = all(z.read(str(p.relative_to(WT))) == p.read_bytes() for p in skill.rglob('*') if p.is_file())
    z.extractall(scratch/'package')
with zipfile.ZipFile(WT/'bootstrap-context.zip') as z:
    z.extractall(scratch/'old-package')
old = scratch/'old-package/bootstrap-context/scripts/bootstrap.py'
new = scratch/'package/groundwork/scripts/bootstrap.py'
relocated = scratch/'arbitrary-installed-folder'
shutil.copytree(skill, relocated)
repo = scratch/'saved-run'
repo.mkdir()
(repo/'src').mkdir(); (repo/'src/app.py').write_text('VALUE = 3\n')
def cli(script,*args):
    return run(LOG,[sys.executable,'-B',str(script),'--repo',str(repo),*args])
cli(old,'init','--scope','checkout')
first=cli(old,'allocate-pb')
(repo/'.bootstrap/runs/unfinished.md').write_text('Investigated src/app.py; next publish observed VALUE.\n')
cli(old,'checkpoint','--scope','checkout','--status','partial','--next','Publish observed value','--finding','.bootstrap/runs/unfinished.md')
before=(repo/'.bootstrap/state.yaml').read_bytes()
cli(new,'status'); cli(new,'init','--scope','checkout')
summary['checks']['old_saved_state_preserved_by_new_init'] = before == (repo/'.bootstrap/state.yaml').read_bytes()
second=cli(new,'allocate-pb')
summary['checks']['old_saved_ids_resume'] = json.loads(first.stdout)['behavior']=='PB-001' and json.loads(second.stdout)['behavior']=='PB-002'
summary['checks']['arbitrary_folder_scan'] = cli(relocated/'scripts/bootstrap.py','scan','--limit','10').returncode == 0
summary['checks']['old_and_new_helper_identical'] = old.read_bytes()==new.read_bytes()
summary['metadata']=(skill/'agents/openai.yaml').read_text()
summary['notes'].append('Archived old-name package used only as compatibility fixture; no historical evaluation results read.')
shutil.copytree(repo,OUT/'portability-saved-run')
(OUT/'portability-report.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
