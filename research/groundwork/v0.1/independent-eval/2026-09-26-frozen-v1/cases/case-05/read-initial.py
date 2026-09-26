from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record_command import run
r=Path(__file__).resolve().parents[2]
for n in (5,6,7,8):
 c=r/'cases'/f'case-{n:02d}'; f=r/'fixtures'/f'case-{n:02d}'
 run(c/'raw.jsonl',['sh','-c','for p in .bootstrap/state.yaml context/index.yaml; do if test -f "$p"; then echo "$p"; cat "$p"; fi; done'],f)
