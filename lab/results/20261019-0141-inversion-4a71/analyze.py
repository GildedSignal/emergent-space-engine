#!/usr/bin/env python3
"""4a71: fold the flight logs into the dossier's numbers. Stdout = the evidence table."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGS = HERE / "logs"


def parse(path: Path) -> dict:
    probes = []
    ladder = {}
    prune = None
    game = None
    for line in path.read_text().splitlines():
        if line.startswith("probe: "):
            d = {}
            for kv in line[len("probe: "):].split():
                k, _, v = kv.partition("=")
                d[k] = float(v) if "." in v else int(v)
            probes.append(d)
        elif line.startswith("ladder: "):
            for kv in line[len("ladder: "):].split():
                k, _, v = kv.partition("=")
                try:
                    ladder[k] = float(v) if ("." in v or "e" in v) else int(v)
                except ValueError:
                    ladder[k] = v
        elif line.startswith("prune: "):
            prune = line
        elif line.startswith("game "):
            game = line
    return {"probes": probes, "ladder": ladder, "prune": prune, "game": game}


def main() -> None:
    rows = []
    for name in ["ctrl-70k", "pin6e9", "pin12e9", "ctrl-5ms", "ctrl-burn"]:
        p = LOGS / f"{name}.log"
        if not p.exists():
            print(f"!! missing {p}")
            continue
        d = parse(p)
        pr = d["probes"]
        hmax = max((x.get("hist_max", 0) for x in pr), default=0)
        htot_max = max((x.get("hist_total", 0) for x in pr), default=0)
        rss0 = pr[0]["rss_mb"] if pr else 0
        rss_end = pr[-1]["rss_mb"] if pr else 0
        bpb0 = pr[0]["bpb"] if pr else 0
        bpb_end = pr[-1]["bpb"] if pr else 0
        gs_end = pr[-1]["gs"] if pr else 0
        gap = d["ladder"].get("max_gap_s", -1)
        held = d["ladder"].get("held_max", -1)
        over = d["ladder"].get("over", -1)
        print(f"== {name}: {gs_end:.0f} gs flown; max_gap now-oldest {gap} s; held_max {held}; over {over}")
        print(f"   hist: max generations on one body {hmax}; peak total retired {htot_max} "
              f"({htot_max / 30028:.2f}/body); rss {rss0:.0f} -> {rss_end:.0f} MB; bpb {bpb0} -> {bpb_end}")
        # the staircase witness: (gs, hist_total) at each wave neighbourhood
        waves = [x for x in pr if x["gs"] >= 10000]
        if waves:
            series = " ".join(f"{x['gs']:.0f}:{x['hist_total']}" for x in waves)
            print(f"   hist_total series (gs:total): {series}")
        if d["game"]:
            print(f"   {d['game'][:150]}")
        print()


if __name__ == "__main__":
    main()
