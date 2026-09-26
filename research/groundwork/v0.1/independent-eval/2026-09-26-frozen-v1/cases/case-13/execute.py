from pathlib import Path
import sys,json,shutil,hashlib
ROOT=Path('/Users/humpyreddypininti/Documents/ChatGPT/skilly/independent-evaluation/2026-09-26-frozen-v1'); sys.path.insert(0,str(ROOT)); from record_command import run
CASE=ROOT/'cases/case-13'; REPO=ROOT/'fixtures/case-13'; HELPER='/Users/humpyreddypininti/.codex/worktrees/groundwork-independent-eval/skilly/groundwork/scripts/bootstrap.py'
def cmd(*a): return run(CASE/'raw.jsonl',list(a),REPO)
def h(*a): return cmd('python3',HELPER,'--repo',str(REPO),*a)
for d in ['.bootstrap','context']: shutil.copytree(REPO/d,CASE/'before-freshness'/d,dirs_exist_ok=True)
h('freshness')
cmd('cat','context/index.yaml','.bootstrap/exclusions.yaml','.bootstrap/questions.yaml','.bootstrap/tracking.yaml','context/product/fee.md','context/engineering/fee.md','context/product/receipt.md','context/engineering/receipt.md','src/checkout.py','src/receipt.py','docs/checkout.md','tests/test_checkout.py')
h('check')
