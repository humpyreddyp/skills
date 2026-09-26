"""Read-only parent audit of completed behavioral fixtures."""
from pathlib import Path
import hashlib
import json
import sys
from record_command import run

OUT=Path(__file__).resolve().parent
WT=Path('/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly')
report=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for number in range(1,15):
 name=f'case-{number:02d}';root=OUT/'fixtures'/name;before=OUT/'fixtures-pristine'/name
 originals={str(p.relative_to(before)):sha(p) for p in before.rglob('*') if p.is_file() and p.relative_to(before).parts[0] not in ('.bootstrap','context')}
 changes=[p for p,h in originals.items() if not (root/p).exists() or sha(root/p)!=h]
 additions=[str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.relative_to(root).parts[0] not in ('.bootstrap','context') and str(p.relative_to(root)) not in originals]
 check=run(OUT/'raw/parent-structural-audit.jsonl',[sys.executable,'-B',str(WT/'groundwork/scripts/bootstrap.py'),'--repo',str(root),'check'])
 pages=[]
 for p in sorted((root/'context').rglob('*.md')):
  front,body=p.read_text()[4:].split('\n---\n',1);meta=json.loads(front)
  pages.append({'path':str(p.relative_to(root)),'id':meta['id'],'behaviors':meta['behaviors'],'implements':meta['implements'],'depends_on':meta['depends_on'],'verification':meta['verification'],'body_words':len(body.split()),'front_matter_bytes':len(front.encode()),'body_bytes':len(body.encode())})
 index=json.loads((root/'context/index.yaml').read_text()) if (root/'context/index.yaml').exists() else {}
 qs=json.loads((root/'.bootstrap/questions.yaml').read_text())
 report.append({'case':number,'state':json.loads((root/'.bootstrap/state.yaml').read_text()),'source_file_count':len(originals),'changed_primary_files':changes,'added_primary_files':additions,'structural_check_returncode':check.returncode,'published_pages':pages,'freshness':{d['id']:d['freshness'] for d in index.get('documents',[])},'questions':[{k:q.get(k) for k in ('id','status','blocking','affects','decision')} for q in qs],'index_bytes':(root/'context/index.yaml').stat().st_size if index else 0})
(OUT/'parent-artifact-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'cases':len(report),'all_primary_files_unchanged':all(not r['changed_primary_files'] and not r['added_primary_files'] for r in report),'all_structural_checks_pass':all(r['structural_check_returncode']==0 for r in report),'total_published_pages':sum(len(r['published_pages']) for r in report)},indent=2))
