#!/usr/bin/env python3
"""One child at a time, hard 60 s wall cap, machine state beside every result."""
import os, pathlib, signal, subprocess, sys, time
root = pathlib.Path(__file__).resolve().parents[3]
phase, name, *command = sys.argv[1:]
out = root / 'artifacts/runs/memory' / phase
out.mkdir(exist_ok=True)
env = dict(os.environ, CARGO_BUILD_JOBS='2', ES_MEMORY_PROBE='1')
start = time.monotonic()
with (out / (name + '.txt')).open('x') as log:
    subprocess.run(['sh', 'artifacts/runs/frame/state.sh'], cwd=root, stdout=log, stderr=log, env=env, timeout=5)
    log.write('command: ' + repr(command) + '\n'); log.flush()
    child = subprocess.Popen(command, cwd=root, stdout=log, stderr=log, env=env, start_new_session=True)
    try:
        code = child.wait(timeout=max(0.01, 59 - (time.monotonic() - start)))
    except subprocess.TimeoutExpired:
        os.killpg(child.pid, signal.SIGKILL)
        child.wait()
        code = 124
    log.write(f'runner: exit={code} wall_s={time.monotonic()-start:.3f}\n')
print(out / (name + '.txt'), 'exit', code)
sys.exit(code)
