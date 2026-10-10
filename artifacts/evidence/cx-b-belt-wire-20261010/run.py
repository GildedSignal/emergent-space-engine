#!/usr/bin/env python3
"""Watch validation's process tree: 60 s and 2 GB per process; longer build timeout via RUN_TIMEOUT."""
import os, signal, subprocess, sys, time
from pathlib import Path
label, *cmd = sys.argv[1:]
out = Path(__file__).parent / (label + '.txt')
timeout = int(os.environ.get('RUN_TIMEOUT', '60'))
start = time.monotonic()
peak = 0
with out.open('w') as f:
    f.write('command: ' + ' '.join(cmd) + f'\ntimeout={timeout}s; process RSS ceiling=2000000000 bytes\n')
    f.flush()
    proc = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
    code = None
    while code is None:
        snapshot = subprocess.run(['ps','-axo','pid=,ppid=,rss='],capture_output=True,text=True)
        if snapshot.returncode:
            os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            f.write('RSS guard unavailable; refusing unbounded run\n');code=125;break
        rows = [tuple(map(int,line.split())) for line in snapshot.stdout.splitlines() if line.strip()]
        descendants = {proc.pid}
        while True:
            more = {pid for pid,parent,_ in rows if parent in descendants} - descendants
            if not more: break
            descendants.update(more)
        sizes = [rss*1024 for pid,_,rss in rows if pid in descendants]
        peak = max(peak,max(sizes,default=0))
        if peak >= 2_000_000_000 or time.monotonic()-start > timeout:
            os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            f.write('RSS LIMIT\n' if peak >= 2_000_000_000 else f'TIMEOUT {timeout}s\n');code=124;break
        try: code=proc.wait(timeout=0.1)
        except subprocess.TimeoutExpired: pass
    f.write(f'\npeak_observed_process_rss_bytes={peak}\nexit={code}; wall_s={time.monotonic()-start:.3f}\n')
print(out.read_text())
sys.exit(code)
