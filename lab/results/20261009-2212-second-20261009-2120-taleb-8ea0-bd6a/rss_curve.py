#!/usr/bin/env python3
"""RSS curve for one cell: (t, VmRSS) every 50 ms, phase-tagged by process milestones."""
import subprocess, sys, time, os
XT = os.environ.get("XT", "./target/release/xtask")
tag, args = sys.argv[1], sys.argv[2:]
p = subprocess.Popen([XT, "universe", "--bench", *args], stdout=subprocess.PIPE, text=True)
t0 = time.time(); curve = []
while p.poll() is None:
    try:
        with open(f"/proc/{p.pid}/status") as f:
            for ln in f:
                if ln.startswith("VmRSS:"):
                    curve.append((round(time.time()-t0,2), int(ln.split()[1]))); break
    except FileNotFoundError:
        break
    time.sleep(0.05)
out = p.stdout.read()
d = eval(out[out.find('"wall_seconds"'):].split(",")[0].split(":")[1]) if '"wall_seconds"' in out else None
os.makedirs("rss", exist_ok=True)
with open(f"rss/{tag}.csv", "w") as f:
    f.write(f"# bench_wall_s={d}\n")
    for t, kb in curve: f.write(f"{t} {kb/1024:.1f}\n")
print(f"{tag}: {len(curve)} samples, peak {max(kb for _,kb in curve)/1024:.0f} MB, bench_wall {d}")
