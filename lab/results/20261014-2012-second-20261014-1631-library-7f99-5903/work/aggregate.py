#!/usr/bin/env python3
"""Aggregate run 5903's arms into the dossier's table. Every number read from the raw/ logs."""
import re
import sys
from pathlib import Path

RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "raw"


def census(path: Path):
    line = next((l for l in path.read_text().splitlines() if l.startswith("scan census")), None)
    if not line:
        return None
    return {k: float(v) for k, v in re.findall(r"(\w+)=([0-9.]+)", line.split("candidates ", 1)[1])}


def digest_and_ladder(path: Path):
    text = path.read_text().splitlines()
    d = next((l for l in text if l.startswith("digest")), "?")
    lad = next((l for l in text if l.startswith("ladder:")), "")
    build = float(re.search(r"build_s=([0-9.]+)", lad).group(1)) if "build_s=" in lad else float("nan")
    bpb = float(re.search(r"b_per_body=([0-9.]+)", lad).group(1)) if "b_per_body=" in lad else float("nan")
    m = re.match(r"digest ([0-9a-f]+) at (\d+) \(contacts (\d+), logged (\d+)\)", d)
    return (m.groups() if m else (d, "?", "?", "?"), build, bpb)


rows = []
for name in ["base-n1000-coast", "patched-n1000-coast", "h0-n1000-coast", "base-n100000-coast",
             "patched-n100000-coast", "base-n10000-burn", "patched-n10000-burn"]:
    c = census(RAW / f"{name}.census")
    (dg, cut, contacts, logged), build, bpb = digest_and_ladder(RAW / f"{name}.txt")
    if c is None:
        rows.append((name, "no scans (flight never ran)", f"build {build:.1f}s", dg[:16], cut))
        continue
    calls = c["calls"]
    rows.append((name, f"walked/call {c['walked']/calls:.1f}, kept/call {c['kept']/calls:.1f}",
                 f"some {c['some']:.0f} density-era {c.get('density', 0):.0f} horizon {c.get('horizon', 0):.0f} of {calls:.0f}",
                 f"{dg[:16]}… at {cut} (logged {logged})", f"build {build:.1f} s, {bpb:.0f} B/body"))

w = max(len(r[0]) for r in rows)
for r in rows:
    print(f"{r[0]:<{w}}  {r[1]:<38}  {r[2]:<34}  {r[3]}  {r[4] if len(r) > 4 else ''}")

print()
base10 = census(RAW / "base-n1000-coast.census")
patched10 = census(RAW / "patched-n1000-coast.census")
print(f"10^3 coast: walked {base10['walked']/base10['calls']:.1f} -> {patched10['walked']/patched10['calls']:.1f} per call "
      f"({base10['walked']/patched10['walked']:.1f}x cut); kept {base10['kept']/base10['calls']:.1f} -> {patched10['kept']/patched10['calls']:.1f}")
for arm in ["n1000-coast", "n10000-burn", "n100000-coast"]:
    b, p = digest_and_ladder(RAW / f"base-{arm}.txt")[0], digest_and_ladder(RAW / f"patched-{arm}.txt")[0]
    same = "IDENTICAL" if b[0] == p[0] else "DIFFERS"
    print(f"{arm}: digest {same} ({b[0][:16]}… vs {p[0][:16]}…; logged {b[3]} vs {p[3]})")
