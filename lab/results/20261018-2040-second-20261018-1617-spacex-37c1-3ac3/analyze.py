#!/usr/bin/env python3
"""Analyse the censuses of run 20261018-2040-second-20261018-1617-spacex-37c1-3ac3.

Reads cens/*.cens (CENSUS/FIRE/PAIR lines from the patched resolver; see sweep.sh and
probe.txt) and writes analysis.txt: per arm — contacts, ghosts (d·w ≥ 0 at the gate),
fires, the contaminated split (τ* < −1), and the fix-vs-oracle bit-identity of every
fired pair's outgoing velocities; plus the cross-run checks (digest identity of the
no-ghost arm with the fix on, dense/sparse identity with the fix on, and 37c1's sd2
census reproduction up to the first fire).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def arm(path: Path):
    census = ghosts = fires = 0
    tau = []
    pair_total = pair_same = 0
    max_dev = 0.0
    for line in path.read_text().splitlines():
        f = line.split()
        if f[0] == "CENSUS":
            census += 1
            if int(f[2]) >= 0:
                ghosts += 1
        elif f[0] == "FIRE":
            fires += 1
            tau.append(float(f[4]))
        elif f[0] == "PAIR":
            pair_total += 1
            import re
            nums = [int(x) for x in re.findall(r"-?\d+", line)][2:]  # skip the two body ids
            fix, orc = nums[:4], nums[4:]
            if fix == orc:
                pair_same += 1
            else:
                dev = sum(abs(a - b) for a, b in zip(fix, orc))
                mag = max(1, max(abs(v) for v in fix))
                max_dev = max(max_dev, dev / mag)
    cont = sum(1 for t in tau if t < -1.0)
    return dict(census=census, ghosts=ghosts, fires=fires, tau_min=min(tau) if tau else None,
                contaminated=cont, pair_total=pair_total, pair_same=pair_same, max_dev=max_dev)


def digest(p: Path):
    try:
        return json.loads(p.read_text())["digest"]
    except Exception:
        return None


def main():
    out = []
    for name in ["ship400off", "ship400on", "sd2off", "sd2on", "sd2denseon", "sd2m400off", "sd2m400on", "sd4on"]:
        p = HERE / "cens" / f"{name}.cens"
        if not p.exists():
            continue
        a = arm(p)
        out.append(
            f"{name:12} contacts {a['census']:5} ghosts {a['ghosts']:4} fires {a['fires']:4} "
            f"tau_min {a['tau_min']} contaminated(tau*<-1) {a['contaminated']:3} "
            f"| PAIR {a['pair_total']:4} bit-identical {a['pair_same']:4} max rel dev {a['max_dev']:.3e}"
        )
    # Cross-run checks.
    d_off, d_on = digest(HERE / "cens" / "ship400off.json"), digest(HERE / "cens" / "ship400on.json")
    out.append(f"\nship400 digest fix-off {d_off}")
    out.append(f"ship400 digest fix-on  {d_on}")
    out.append(f"ship400 bit-identity with the fix on: {d_off == d_on and d_off is not None}")
    pa, pb = HERE / "cens" / "sd2on.cens", HERE / "cens" / "sd2denseon.cens"
    if pa.exists() and pb.exists():
        out.append(f"sd2on vs sd2denseon census cmp-identical (the fix preserves stepper identity): {pa.read_bytes() == pb.read_bytes()}")
    # 37c1's record reproduced: the fix-OFF censuses must match the original run exactly.
    for ref_name, mine_name in [("sd2", "sd2off"), ("sd2m400", "sd2m400off"), ("ship400", "ship400off")]:
        ref = HERE / "cens" / "ref" / f"{ref_name}.cens"
        mine = HERE / "cens" / f"{mine_name}.cens"
        if ref.exists() and mine.exists():
            r = [l for l in ref.read_text().splitlines() if l.startswith("CENSUS")]
            m = [l for l in mine.read_text().splitlines() if l.startswith("CENSUS")]
            out.append(f"{mine_name} vs 37c1 {ref_name} census: {len(r)} vs {len(m)} lines, identical: {r == m}")
    (HERE / "analysis.txt").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
