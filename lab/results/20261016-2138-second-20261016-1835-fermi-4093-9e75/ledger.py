#!/usr/bin/env python3
"""Parse flights.log (freeze: / game: / ladder: lines per arm) into the freeze ledger:
the directly-measured spell, the freeze law with same-run constants, N-scaling, and the
10^6/10^9 arithmetic. Pure arithmetic on printed integer counts and exact per-frame sums."""
import re
import sys

arms = []
cur = None
pat_arm = re.compile(r"^=== (\d+) (coast|burn) (\d+) (\d+)$")
pat_freeze = re.compile(r"^freeze: lag_frames=(\d+) deficit_s=([\d.]+) spell_at=(\d+) "
                        r"spell_frames=(\d+) spell_wall_s=([\d.]+) spell_events=(\d+) "
                        r"spell_presented_s=([\d.]+) spell_ms=([\d.]+) spell_us_per_ev=([\d.]+)")
pat_game = re.compile(r"^game ([\d.]+) s after the first second: kicks (\d+) .*? events (\d+) .*?boundaries (\d+)")
pat_ladder = re.compile(r"^ladder: n=(\d+).*?rtf=(\d+).*?frames=(\d+).*?foot_end_mb=([\d.]+).*?"
                        r"p50_ms=([\d.]+) p99_ms=([\d.]+) max_ms=([\d.]+) over=(\d+) lag_s=([\d.]+).*?"
                        r"held_max=(\d+).*?truncated=(\w+)")
pat_frames = re.compile(r"^frames after 1 s: (\d+)\s+engine ms p50 ([\d.]+) p90 [\d.]+ p99 ([\d.]+) max ([\d.]+)")

for line in open(sys.argv[1] if len(sys.argv) > 1 else "flights.log"):
    m = pat_arm.match(line)
    if m:
        cur = dict(n=int(m.group(1)), flight=m.group(2), secs=int(m.group(3)), rtf=int(m.group(4)))
        arms.append(cur)
    m = pat_freeze.match(line)
    if m:
        cur.update(lag_frames=int(m.group(1)), deficit=float(m.group(2)), spell_at=int(m.group(3)),
                   spell_frames=int(m.group(4)), spell_wall=float(m.group(5)), E=int(m.group(6)),
                   presented=float(m.group(7)), ms=float(m.group(8)), c=float(m.group(9)))
    m = pat_game.match(line)
    if m:
        cur.update(game_s=float(m.group(1)), kicks=int(m.group(2)), events=int(m.group(3)),
                   boundaries=int(m.group(4)))
    m = pat_frames.match(line)
    if m:
        cur.update(late_frames=int(m.group(1)), p50=float(m.group(2)), p99=float(m.group(3)), fmax=float(m.group(4)))
    m = pat_ladder.match(line)
    if m:
        cur.update(ran=int(m.group(3)), foot_end=int(m.group(4)), p99=float(m.group(6)), fmax=float(m.group(7)),
                   over=int(m.group(8)), lag_s=float(m.group(9)), held_max=int(m.group(10)), trunc=m.group(11))
f1 = next((a for a in arms if a["n"] == 100000 and a["flight"] == "coast" and a["rtf"] == 1800), None)
f2 = next((a for a in arms if a["n"] == 300000 and a["flight"] == "coast" and a["rtf"] == 1800), None)
f3 = next((a for a in arms if a["n"] == 300000 and a["flight"] == "burn"), None)
f4 = next((a for a in arms if a["n"] == 300000 and a["rtf"] == 3600), None)

print("== The freeze, measured directly (spell = longest run of frames with target-presented > 0; "
      "wall at the game's real 60-fps pacing = frames/60) ==")
print(f"{'arm':<20}{'ran':>5}{'spell@':>7}{'spellF':>7}{'wall s':>7}{'E_spell':>8}"
      f"{'present':>8}{u'Ĉ µs/ev':>8}{'E·Ĉ/0.72':>9}{'ratio':>6}{'deficit s':>10}{'lag(°)':>7}")
for name, a in (("F1 1e5 coast 1800", f1), ("F2 3e5 coast 1800", f2), ("F4 3e5 coast 3600", f4)):
    if not a or "E" not in a:
        print(f"{name}: MISSING")
        continue
    pred = a["E"] * a["c"] * 1e-6 / 0.72
    print(f"{name:<20}{a['ran']:>5}{a['spell_at']:>7}{a['spell_frames']:>7}{a['spell_wall']:>7.1f}{a['E']:>8}"
          f"{a['presented']:>8.0f}{a['c']:>8.1f}{pred:>9.1f}{a['spell_wall'] / pred:>6.2f}"
          f"{a['deficit']:>10.0f}{a['lag_s']:>7.2f}")
    print(f"    window: game {a['game_s']:.0f} s, kicks {a['kicks']}, boundaries {a['boundaries']}, events {a['events']};"
          f" deficit frames {a['lag_frames']} in total (the spell is {100 * a['spell_frames'] / max(a['lag_frames'], 1):.0f}% of them;"
          f" delivered at real pacing {a['E'] / a['spell_wall']:.0f} ev/s)")

if f2 and f1 and "E" in f2 and "E" in f1:
    r = f2["E"] / f1["E"]
    print(f"\n== N-scaling: E_spell(3e5)/E_spell(1e5) = {r:.2f} (belt bodies x3.00) — one crest event per body, linear ==")
    e6, c = f2["E"] * 1e6 / 3e5, f2["c"]
    w6 = e6 * c * 1e-6 / 0.72
    print(f"10^6 (cannot fly: build alone 2,340 B/B = 2.34 GB > the 2-GB process cap) = 3.33x F2:"
          f" E ~= {e6:.0f}, spell {w6:.0f} s per 28,141.5-game-s interval")
    e9 = f2["E"] * 1e9 / 3e5
    cpu = e9 * c * 1e-6
    print(f"10^9: E ~= {e9:.2e}, CPU {cpu:.0f} s per crest -> freeze {cpu / 0.72 / 3600:.1f} h of clamped"
          f" presented time per interval, or {cpu / 28141.5:.1f} cores sustained at rtf 1"
          f" ({cpu * 10 / 28141.5:.0f} at rtf 10, {cpu * 100 / 28141.5:.0f} at rtf 100)")
if f4 and f2 and "E" in f4 and "E" in f2:
    print(f"\n== The metric replaces the lag: at rtf 3600 the lag prints its ceiling {f4['lag_s']:.3f} (= rtf/60)"
          f" while E(3600)/E(1800) = {f4['E'] / f2['E']:.3f}, spell {f4['spell_wall']:.1f} s vs {f2['spell_wall']:.1f} s"
          f" (rtf-independent), deficit ratio {f4['deficit'] / f2['deficit']:.2f} (= rtf ratio 2.00) ==")
if f3:
    print(f"\n== F3 burn arm: the freeze is ABSENT — the crest breaks the budget instead ==")
    print(f"    spell {f3.get('spell_frames', 0)} frames = {f3.get('spell_wall', 0):.1f} s, E_spell {f3.get('E', 0)},"
          f" deficit {f3.get('deficit', 0):.0f} game-s (coast: 22.1 s, 299,138, 42,364)")
    print(f"    frames over 12 ms: {f3.get('over', 0)}, p99 {f3.get('p99', 0):.0f} ms, max {f3.get('fmax', 0):.0f} ms;"
          f" truncated={f3.get('trunc', '?')} at {f3.get('ran', 0)}/2400 frames; memory 705 -> {f3.get('foot_end', 0)} MB"
          f" ({f3.get('foot_end', 0) * 1e6 / 300028:.0f} B/B); held_max {f3.get('held_max', 0)}")
    print(f"    worst frame: {f3.get('fmax', 0):.0f} ms carrying the crest's events at the usual cost — one started"
          f" item resolved a whole wave; the budget's per-item stop (first item always runs, margin = recent item"
          f" cost, shipped worst case 1.4 ms) cannot see inside it")
