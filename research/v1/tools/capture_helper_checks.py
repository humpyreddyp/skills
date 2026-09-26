#!/usr/bin/env python3
"""Capture helper-only regression results; never runs downstream model experiments."""
import datetime
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def startTest(self, test):
        self.started = time.monotonic()
        super().startTest(test)

    def addSuccess(self, test):
        self.records.append({"id": test.id(), "status": "passed",
                             "duration_seconds": time.monotonic() - self.started})
        super().addSuccess(test)

    def addFailure(self, test, err):
        self.records.append({"id": test.id(), "status": "failed",
                             "detail": self._exc_info_to_string(err, test)})
        super().addFailure(test, err)

    def addError(self, test, err):
        self.records.append({"id": test.id(), "status": "error",
                             "detail": self._exc_info_to_string(err, test)})
        super().addError(test, err)

    def addSkip(self, test, reason):
        self.records.append({"id": test.id(), "status": "skipped", "reason": reason})
        super().addSkip(test, reason)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 capture_helper_checks.py NEW_OUTPUT_DIRECTORY")
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "evals"), pattern="test_*.py")
    with (output / "unittest.txt").open("w") as log:
        result = unittest.TextTestRunner(stream=log, verbosity=2,
                                        resultclass=RecordedResult).run(suite)
    record = {
        "purpose": "Supplemental freeze verification, not a historical console transcript",
        "started_utc": started,
        "completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python_version": platform.python_version(), "python_executable": sys.executable,
        "platform": platform.platform(), "machine": platform.machine(),
        "dependencies": "Python standard library; no model API or network",
        "command": "PYTHONDONTWRITEBYTECODE=1 python3 research/v1/tools/capture_helper_checks.py NEW_OUTPUT_DIRECTORY",
        "equivalent_suite_command": "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s evals -p 'test_*.py' -v",
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ["bootstrap-context/scripts/bootstrap.py", "evals/test_runtime.py"]},
        "tests_run": result.testsRun, "successful": result.wasSuccessful(),
        "failures": len(result.failures), "errors": len(result.errors),
        "skipped": len(result.skipped), "tests": result.records,
    }
    (output / "results.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"tests_run": result.testsRun, "successful": result.wasSuccessful(),
                      "output": str(output)}))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
