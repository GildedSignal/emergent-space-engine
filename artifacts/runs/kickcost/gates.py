#!/usr/bin/env python3
"""Serial frozen gate and census runner; run.py caps each child at 59 seconds."""
import subprocess, sys, pathlib, re
phase = sys.argv[1]
def run(name, args):
    saved = pathlib.Path(f'artifacts/runs/kickcost/{phase}/{name}.txt')
    if saved.exists():
        result = re.search(r'runner: exit=(\d+)', saved.read_text())
        if result:
            print(saved, 'retained exit', result[1], flush=True)
            return int(result[1])
    return subprocess.run(['python3', 'artifacts/runs/kickcost/run.py', phase, name, *args]).returncode
run('space', ['cargo','run','--release','-j','2','-p','xtask','--','behave','--law','space','--gates','G1,G2,G3,G4,G5,G6,B19'])
run('plane', ['cargo','run','--release','-j','2','-p','xtask','--','behave','--law','plane','--gates','B13,B17'])
subprocess.run(['python3','artifacts/runs/kickcost/tests.py',phase])
run('replay', ['target/release/xtask','universe','--replay-all'])
run('digests', ['sh','artifacts/runs/frame/digests.sh','artifacts/runs/nladder/digests_before.txt'])
for n in [0, 100000, 1000000]:
    for flight in ['coast','burn']:
        run(f'n{n}_{flight}', ['target/release/examples/nladder',str(n),flight,'20'])
    run(f'rebind{n}', ['target/release/examples/kickcost',str(n)])

raise SystemExit(subprocess.run([sys.executable, "artifacts/runs/kickcost/evaluate.py", phase]).returncode)
