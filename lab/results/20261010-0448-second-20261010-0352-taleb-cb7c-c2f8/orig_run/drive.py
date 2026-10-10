#!/usr/bin/env python3
"""Drive `xtask universe --bench` and sample its /proc memory counters.

Usage: drive.py NAME [extra bench args...]
Writes data/NAME.json (the dashboard) and data/NAME.rss.tsv (t, wall_s, VmRSS_kB, VmHWM_kB, minflt, majflt).
"""
import subprocess, sys, time, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
XT = "/home/glmlab/lab-target-3/release/xtask"

def sample(pid, out, t0):
    fields = {}
    try:
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                if line.startswith(("VmRSS:", "VmHWM:")):
                    k, v = line.split(":", 1)
                    fields[k] = int(v.strip().split()[0])
        with open(f"/proc/{pid}/stat") as f:
            st = f.read().rsplit(")", 1)[1].split()
            fields["minflt"] = int(st[7]); fields["majflt"] = int(st[9])
    except (FileNotFoundError, ProcessLookupError, IndexError):
        return False
    out.write(f"{time.time()-t0:.3f}\t{fields.get('VmRSS',0)}\t{fields.get('VmHWM',0)}\t{fields.get('minflt',0)}\t{fields.get('majflt',0)}\n")
    return True

def main():
    name, extra = sys.argv[1], sys.argv[2:]
    os.makedirs(f"{HERE}/data", exist_ok=True)
    t0 = time.time()
    p = subprocess.Popen([XT, "universe", "--bench"] + extra, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with open(f"{HERE}/data/{name}.rss.tsv", "w") as out:
        out.write("t\tvmrss_kb\tvmhwm_kb\tminflt\tmajflt\n")
        while p.poll() is None:
            sample(p.pid, out, t0)
            time.sleep(0.2)
    o, e = p.communicate()
    with open(f"{HERE}/data/{name}.json", "w") as f:
        f.write(o)
    with open(f"{HERE}/data/{name}.err", "w") as f:
        f.write(e)
    try:
        d = json.loads(o)
        print(f"{name}: exit={p.returncode} wall={time.time()-t0:.1f}s digest={d.get('digest','?')[:16]} "
              f"p50={d['frame_cpu_ms']['p50']:.2f} p99={d['frame_cpu_ms']['p99']:.2f} worst={d['frame_cpu_ms']['worst']:.2f} "
              f"overflow={d['rtf']['overflow_frames']} rtf_med={d['rtf']['median']:.1f}")
    except Exception as ex:
        print(f"{name}: exit={p.returncode} wall={time.time()-t0:.1f}s BAD-OUTPUT {ex}: {o[:200]} {e[:400]}")

if __name__ == "__main__":
    main()
