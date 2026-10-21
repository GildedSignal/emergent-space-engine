#!/usr/bin/env python3
"""Pull the dossier's numbers out of the three arm logs (20261021-0429-spacex-9d3a)."""
import re, sys, pathlib

args = []
for p in sys.argv[1:]:
    q = pathlib.Path(p)
    args.extend(sorted(q.glob("arm_*.txt")) if q.is_dir() else [q])

rows = {}
for p in args:
    for line in pathlib.Path(p).read_text().splitlines():
        if "rcensus reads:" in line or "rcensus gens:" in line or "rcensus live" in line or "rcensus rebuilds" in line or line.startswith("rcensus: gens") or line.startswith("rcensus: n=") or "frames after 1 s" in line or line.startswith("memory:"):
            key = pathlib.Path(p).name
            rows.setdefault(key, []).append(line)

def num(s):
    return float(s.replace("_", ""))

print(f"{'arm':<28}{'bodies':>9}{'gens':>10}{'0post%':>8}{'live@1f/@1s/@5s':>18}{'rebl@60f':>10}{'eng rd/fr':>10}{'kick%':>7}")
for key, lines in rows.items():
    blob = "\n".join(lines)
    bodies = re.search(r"bodies=(\d+)", blob)
    gens = re.search(r"gens=(\d+)", blob)
    zp = re.search(r"pct_zero_post=([\d.]+)", blob)
    live = re.search(r"frames \[1, 60, 300, 1200\]\): ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)", blob)
    rb = re.search(r"build_born=(\d+)_(\d+)_(\d+)_(\d+)", blob)
    tot = re.search(r"readout_engine=(\d+)", blob)
    fr = re.search(r"frames=(\d+)", blob)
    kk = re.search(r"kicks (\d+) \(([\de.-]+)/body/game-s\)", blob)
    n = re.search(r"n=(\d+)", blob)
    b = int(bodies.group(1)) if bodies else 0
    g = int(gens.group(1)) if gens else 0
    z = float(zp.group(1)) if zp else -1
    lv = f"{float(live.group(1)):.2f}/{float(live.group(2)):.2f}/{float(live.group(3)):.2f}" if live else "-"
    r60 = int(rb.group(2)) if rb else -1
    eng = int(tot.group(1)) / int(fr.group(1)) if tot and fr else -1
    kp = kk.group(2) if kk else "-"
    print(f"{key:<28}{b:>9}{g:>10}{z:>8.2f}{lv:>18}{r60:>10}{eng:>10.0f}{kp:>7}")

# the dossier's derived line: timeout-demotion's bill at 1e9 (per-body return rate from rebuilds@slack60)
blob = "\n".join(rows.get("arm_1000000_20_sparse.txt", []))
m = re.search(r"rcensus rebuilds.*build_born=(\d+)_(\d+)", blob)
g = re.search(r"build_born=(\d+)", blob)
f = re.search(r"frames=(\d+)", blob)
if m and f:
    returns_per_body = int(m.group(2)) / 1_000_032
    per_s = returns_per_body / (int(f.group(1)) / 60.0)
    for tag, cost in [("compile 4.4 us", 4.4e-6), ("served 0.64 us", 0.64e-6)]:
        print(f"1e9 timeout-demotion rebuild bill ({tag}): {per_s:.4f} returns/body/wall-s -> {per_s*1e9*cost:.0f} cores")
