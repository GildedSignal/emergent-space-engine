#!/usr/bin/env python3
"""One child at a time, hard 60 s wall cap, machine state beside every result."""
import os, pathlib, re, signal, subprocess, sys, time
root = pathlib.Path(__file__).resolve().parents[3]
phase, name, *command = sys.argv[1:]
out = root / 'artifacts/runs/kickcost' / phase
out.mkdir(exist_ok=True)
saved = out / (name + '.txt')
if saved.exists():
    completed = re.search(r'runner: exit=(\d+)', saved.read_text())
    if completed:
        print(saved, 'retained exit', completed[1])
        sys.exit(int(completed[1]))
    raise SystemExit('Incomplete prior evidence; retain it and use a new probe name: ' + str(saved))
env = dict(os.environ, CARGO_BUILD_JOBS='2', ES_MEMORY_PROBE='1')
start = time.monotonic()
with (out / (name + '.txt')).open('x') as log:
    subprocess.run(['sh', 'artifacts/runs/frame/state.sh'], cwd=root, stdout=log, stderr=log, env=env, timeout=5)
    log.write('command: ' + repr(command) + '\n'); log.flush()
    child = subprocess.Popen(command, cwd=root, stdout=log, stderr=log, env=env, start_new_session=True)
    remaining = max(0.01, 59 - (time.monotonic() - start))
    # The cap survives a host/session interruption that terminates this runner.
    watchdog_code = "import os,signal,sys,time\ntime.sleep(float(sys.argv[2]))\ntry:\n os.killpg(int(sys.argv[1]), signal.SIGKILL)\nexcept ProcessLookupError:\n pass\n"
    watchdog = subprocess.Popen([sys.executable, '-c', watchdog_code,
        str(child.pid), str(remaining)], start_new_session=True)
    try:
        code = child.wait(timeout=remaining)
    except subprocess.TimeoutExpired:
        try: os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError: pass
        child.wait()
        code = 124
    if code == -signal.SIGKILL and time.monotonic() - start >= 58: code = 124
    watchdog.terminate(); watchdog.wait()
    log.write(f'runner: exit={code} wall_s={time.monotonic()-start:.3f}\n')
print(out / (name + '.txt'), 'exit', code)
sys.exit(code)
