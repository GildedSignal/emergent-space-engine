#!/usr/bin/env python3
"""Run built tests serially, each individual test under the probe's 59 s cap."""
import json, pathlib, re, subprocess
root = pathlib.Path(__file__).resolve().parents[3]
log = (root / 'artifacts/runs/memory/build-tests.txt').read_text()
binaries = re.findall(r'Executable (.+?) \((target/release/deps/[^)]+)\)', log)
results = []
for label, binary in binaries:
    listed = subprocess.run([str(root / binary), '--list', '--format=terse'], capture_output=True, text=True, timeout=10, check=True).stdout
    tests = [line[:-6] for line in listed.splitlines() if line.endswith(': test')]
    for test in tests:
        name = re.sub(r'[^\w.-]', '_', pathlib.Path(binary).name + '--' + test)
        status = subprocess.run(['python3', 'artifacts/runs/memory/run.py', 'tests', name,
                                 binary, '--exact', test, '--test-threads=1'], cwd=root).returncode
        output = (root / 'artifacts/runs/memory/tests' / (name + '.txt')).read_text()
        passed = re.search(r'(\d+) passed;', output)
        ignored = re.search(r'(\d+) ignored;', output)
        results.append({'binary': binary, 'label': label, 'test': test, 'exit': status,
                        'passed': int(passed[1]) if passed else 0,
                        'ignored': int(ignored[1]) if ignored else 0})
        (root / 'artifacts/runs/memory/test-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(label, len(tests), 'tests attempted', flush=True)
raise SystemExit(any(r['exit'] for r in results))
