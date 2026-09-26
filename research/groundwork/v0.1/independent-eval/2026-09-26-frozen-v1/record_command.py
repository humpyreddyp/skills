"""Append-only command recorder for this independent evaluation; not skill code."""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

def run(log, command, cwd=None):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    begin = time.monotonic()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    proc = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    record = {'started': started, 'duration_seconds': time.monotonic()-begin,
              'command': command, 'cwd': str(cwd) if cwd else os.getcwd(),
              'returncode': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}
    dest=Path(log); dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open('a') as f: f.write(json.dumps(record)+'\n')
    print(proc.stdout, end=''); print(proc.stderr, end='', file=sys.stderr)
    return proc

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--log',required=True)
    parser.add_argument('--cwd')
    parser.add_argument('command',nargs=argparse.REMAINDER)
    a=parser.parse_args(); cmd=a.command[1:] if a.command[:1]==['--'] else a.command
    sys.exit(run(a.log,cmd,a.cwd).returncode)
