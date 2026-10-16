#!/usr/bin/env python3
# Parse nladder ES_ROWS dumps + summary lines; report the wave's frame-level peaks and window profile.
# Usage: analyze.py <flights dir>
import sys, re, math
from pathlib import Path

d = Path(sys.argv[1])
for f in sorted(d.glob("*.txt")):
    if not re.match(r"[A-E]_", f.name):
        continue
    rows = []
    summary = {}
    for line in f.read_text().splitlines():
        m = re.match(r"row (\d+) ([\d.]+) ([\d.]+) (\d+) ([\d.-]+)", line)
        if m:
            rows.append((int(m[1]), float(m[2]), float(m[3]), int(m[4]), float(m[5])))
            continue
        m = re.match(r"frames after 1 s: (\d+)\s+engine ms p50 ([\d.]+) p90 ([\d.]+) p99 ([\d.]+) max ([\d.]+); over [\d.]+ ms: (\d+); frames behind: (\d+), worst lag ([\d.]+) s; events/frame p50 (\d+) p99 (\d+) max (\d+)", line)
        if m:
            summary = dict(frames=m.group(1), p50ms=m.group(2), p99ms=m.group(4), maxms=m.group(5),
                           lag=m.group(8), ev_p50=m.group(9), ev_p99=m.group(10), ev_max=m.group(11))
        if line.startswith("game "):
            summary["game_line"] = line
        if line.startswith("memory:"):
            summary["mem_line"] = line
    if not rows:
        print(f"{f.name}: no rows"); continue
    # events and ms in 250 game-s windows (ed3a's instrument), after frame 60 (1 s)
    late = [r for r in rows if r[0] >= 60]
    wins = {}
    for r in late:
        w = int(r[1] // 250)
        a, b = wins.get(w, (0, 0.0))
        wins[w] = (a + r[3], max(b, r[2]))
    wmax_ev = max(wins.values(), key=lambda v: v[0]) if wins else (0, 0)
    wmax_ms = max(wins.values(), key=lambda v: v[1]) if wins else (0, 0)
    # the wave split: frames presented before 13,000 game-s carry no belt first-kicks (the belt's
    # earliest unstaggered first item is 13,051; staggered >= 13,301) -- the pre-wave frames are
    # the plane's own N-independent baseline (the 300 locals + exodus); the post-wave side is
    # baseline + belt stream.
    pre = [r for r in late if r[1] < 13000.0]
    post = [r for r in late if r[1] >= 13000.0]
    if pre and post:
        ppk = max(post, key=lambda r: r[3])
        ppm = max(post, key=lambda r: r[2])
        print(f"  pre-wave (game-s<13k): max {max(r[3] for r in pre)} events, {max(r[2] for r in pre):.2f} ms over {len(pre)} frames; "
              f"post-wave: max {ppk[3]} events ({ppk[2]:.2f} ms) @ {ppk[1]:.0f} game-s, max-ms {ppm[2]:.2f} ms ({ppm[3]} events) @ {ppm[1]:.0f} game-s")
        print(f"  belt-attributable frame peak (post minus pre max): {ppk[3] - max(r[3] for r in pre)} events")
    peak = max(late, key=lambda r: r[3])
    peak_ms = max(late, key=lambda r: r[2])
    # letter check: frames over 12 ms engine, excluding the opening exodus region is NOT done here (raw counts)
    over12 = sum(1 for r in late if r[2] > 12.0)
    tot_ev = sum(r[3] for r in late)
    print(f"{f.name}: frames {len(late)}, total events {tot_ev}, events/frame p50/p99/max {summary.get('ev_p50')}/{summary.get('ev_p99')}/{summary.get('ev_max')}, "
          f"ms p50/p99/max {summary.get('p50ms')}/{summary.get('p99ms')}/{summary.get('maxms')}, over12ms {over12}, worst lag {summary.get('lag')} s")
    print(f"  peak-events frame: f{peak[0]} @ {peak[1]:.0f} game-s = {peak[3]} events, {peak[2]:.2f} ms;  peak-ms frame: f{peak_ms[0]} @ {peak_ms[1]:.0f} game-s = {peak_ms[2]:.2f} ms, {peak_ms[3]} events")
    print(f"  worst 250-s window: {wmax_ev[0]} events (max frame {wmax_ev[1]:.1f} ms);  window with max-frame {wmax_ms[1]:.1f} ms ({wmax_ms[0]} events)")
    # top-5 event frames
    top = sorted(late, key=lambda r: -r[3])[:5]
    print("  top-5 event frames: " + "; ".join(f"f{r[0]}@{r[1]:.0f}s:{r[3]}ev/{r[2]:.1f}ms" for r in top))
    if summary.get("game_line"):
        print("  " + summary["game_line"])
    if summary.get("mem_line"):
        print("  " + summary["mem_line"])
