import json, os, resource, subprocess, sys, time
from pathlib import Path
name, *cmd = sys.argv[1:]
root = Path(__file__).resolve().parent
state = {'load': os.getloadavg()}
for key, args in [('swap', ['sysctl','-n','vm.swapusage']), ('power',['pmset','-g','batt']), ('thermal',['pmset','-g','therm'])]:
    r = subprocess.run(args, capture_output=True, text=True)
    state[key] = (r.stdout or r.stderr).strip()
start = time.monotonic()
with (root / (name + '.log')).open('w') as f:
    p = subprocess.Popen(['perl','-e','alarm 60; exec @ARGV',*cmd], stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
    reason = None
    while p.poll() is None:
        if time.monotonic()-start > 60:
            reason = 'timeout'
            os.killpg(p.pid, 9)
            break
        time.sleep(.1)
    rc = p.wait()
record = dict(command=cmd, rc=rc, reason=reason, wall_s=time.monotonic()-start, child_max_rss=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss, before=state, after_load=os.getloadavg())
(root / (name + '.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
sys.exit(0 if rc == 0 else 1)
