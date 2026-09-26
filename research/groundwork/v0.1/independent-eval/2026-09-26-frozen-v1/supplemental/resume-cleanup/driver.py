import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from record_command import run
E=Path(__file__).resolve().parent
R=Path('/private/tmp/groundwork-resume-cleanup-xirc58xq/repo')
S=Path('/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork')
def cmd(*args): return run(E/'commands.jsonl',list(args),R)
if sys.argv[1]=='intake':
    # Replay initial read-only intake to preserve complete output before any mutations.
    cmd('cat',str(E/'prompt.txt'),str(S/'SKILL.md'),str(R/'.bootstrap/state.yaml'),str(R/'context/index.yaml'),*[str(S/'references'/x) for x in ['commands.md','state-format.md','evidence.md','questions.md']],str(E.parents[1]/'record_command.py'))
    cmd('python3',str(S/'scripts/bootstrap.py'),'--repo',str(R),'freshness')
    cmd('python3',str(S/'scripts/bootstrap.py'),'--repo',str(R),'status')
    cmd('rg','--files','--hidden','-g','!.git/**')
elif sys.argv[1]=='cmd': cmd(*sys.argv[2:])
