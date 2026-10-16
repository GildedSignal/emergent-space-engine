#!/usr/bin/env python3
"""The composed ledger: parse the flight matrix, measure the composed stream's rate and
per-event cost, and recompute e7ef's 10^9 closure with the MEASURED composed constants.

Reads flights/*.txt (written by flights.sh). Pure arithmetic after parsing.
"""
import json, re, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))

def parse(path):
    t = open(path).read()
    a = {"tag": os.path.basename(path).replace(".txt", "")}
    m = re.search(r"rung N=(\d+) \((\d+) bodies\).*?rtf (\d+)", t)
    a["n"], a["bodies"], a["rtf"] = int(m.group(1)), int(m.group(2)), float(m.group(3))
    m = re.search(r"game ([\d.]+) s after the first second: kicks (\d+) \(([\de.+-]+)/body/game-s\), events (\d+) \(([\de.+-]+)/body/game-s\)", t)
    a["game_s"], a["kicks"], a["kick_rate"] = float(m.group(1)), int(m.group(2)), float(m.group(3))
    a["events"], a["ev_rate"] = int(m.group(4)), float(m.group(5))
    m = re.search(r"refusals held (\d+), dead (\d+), alive\(player\) (\w+)", t)
    a["refused"], a["dead"], a["alive"] = int(m.group(1)), int(m.group(2)), m.group(3) == "true"
    m = re.search(r"frames after 1 s: (\d+)\s+engine ms p50 ([\d.]+) p90 ([\d.]+) p99 ([\d.]+) max ([\d.]+); over [\d.]+ ms: (\d+); frames behind: (\d+), worst lag ([\d.]+) s; events/frame p50 (\d+)", t)
    a["frames"], a["p50"], a["p99"], a["max_ms"], a["over"], a["behind"], a["lag_s"], a["ev_p50"] = (
        int(m.group(1)), float(m.group(2)), float(m.group(4)), float(m.group(5)), int(m.group(6)), int(m.group(7)), float(m.group(8)), int(m.group(9)))
    m = re.search(r"freeze: lag_frames=(\d+) deficit_s=([\d.]+) spell_at=(\d+) spell_frames=(\d+) spell_wall_s=([\d.]+) spell_events=(\d+) spell_presented_s=([\d.]+) spell_ms=([\d.]+) spell_us_per_ev=([\d.]+) lag_events=(\d+) lag_ms=([\d.]+)", t)
    if m:
        a.update(deficit_s=float(m.group(2)), spell_frames=int(m.group(4)), spell_s=float(m.group(5)),
                 spell_events=int(m.group(6)), spell_us=float(m.group(9)), lag_events=int(m.group(10)), lag_ms=float(m.group(11)))
    m = re.search(r"impact_guess: fires=(\d+) fallbacks=(\d+) window_readouts=(\d+)", t)
    a["fires"], a["fallbacks"] = int(m.group(1)), int(m.group(2))
    m = re.search(r"memory: peak footprint (\d+) MB", t)
    a["peak_mb"] = int(m.group(1)) if m else 0
    # total engine ms over late frames: not printed as a sum; approximate by p50*frames (low) and
    # use lag_ms/lag_events (the clamped frames only) as the per-event cost during overload.
    a["chat_us_lag"] = a["lag_ms"] * 1e3 / a["lag_events"] if a.get("lag_events") else None
    return a

arms = {parse(p)["tag"]: parse(p) for p in sorted(glob.glob(os.path.join(HERE, "flights/*.txt"))) if not os.path.basename(p).startswith("belt_first")}
rows = []
def note(s):
    rows.append(s); print(s)

note("# The flight matrix (parsed from flights/)")
for t, a in arms.items():
    note(f"  {t:22s} N={a['n']:>6} rtf={a['rtf']:>6} game_s={a['game_s']:>8.0f} kicks={a['kicks']:>7} ev/frame p50={a['ev_p50']:>4} "
         f"p50_ms={a['p50']:.2f} p99={a['p99']:.2f} over={a['over']:>3} spell={a.get('spell_s',0):>4.1f}s deficit={a.get('deficit_s',0):>6.0f} "
         f"us/ev(lag)={a['chat_us_lag'] or 0:.1f} fires={a['fires']} refusals={a['refused']} dead={a['dead']} alive={a['alive']} peakMB={a['peak_mb']}")

# ---- the split's interval (direct, from belt_first: first-kick p50 = interval/2) -------------
note("")
note("# The split's cadence, measured directly (belt_first, same scene, BELT_SPLIT off/on)")
def belt_p50(path):
    t = open(os.path.join(HERE, path)).read()
    return int(re.search(r"belt: (\d+) bodies, first item \(game s\) min (\d+) p01 (\d+) p50 (\d+)", t).group(4))
p0, p1 = belt_p50("flights/belt_first-shipped.txt"), belt_p65 if False else belt_p50("flights/belt_first-split.txt")
note(f"  belt first-kick p50: shipped {p0} game-s, split {p1} game-s -> interval ratio {p1/p0:.3f}x")
note(f"  (all 2,700 belt bodies qualify as bulk at the 4-Hill rule; the locals' line is identical in both)")
note("  in-window flight rates (context, window-shaped): S3 crest window {s3:.2e}/B/game-s vs C5 {c5:.2e} (the".format(
    s3=arms["S3-ship-3e5-1800"]["kick_rate"], c5=arms["C5-comp-3e5-1800"]["kick_rate"]))
note("  composed windows end inside the staggered first interval, so they see only its leading ~17%)")
RATE0, SPLIT = 3.55e-5, p1 / p0
RATE1 = RATE0 / SPLIT

# ---- per-event cost ----------------------------------------------------------------------------
note("")
note("# Per-event cost C (us): clamped frames (lag_ms/lag_events, 9e75's estimator)")
for t in ("S3-ship-3e5-1800", "C5-comp-3e5-1800", "C6-comp-3e5-3600", "C7-comp-3e5-7200", "S1-ship-1e5-1800", "C1-comp-1e5-1800", "C4-comp-1e5-14400", "AB0-guess-off-1e5-3600", "AB1-guess-on-1e5-3600"):
    if t in arms and arms[t].get("chat_us_lag"):
        note(f"  {t:22s} {arms[t]['chat_us_lag']:.1f} us/ev over {arms[t]['lag_events']} clamped events")
ab0, ab1 = arms.get("AB0-guess-off-1e5-3600"), arms.get("AB1-guess-on-1e5-3600")
if ab0 and ab1:
    d = abs(ab1["chat_us_lag"] - ab0["chat_us_lag"]) / max(ab0["chat_us_lag"], ab1["chat_us_lag"]) * 100
    note(f"  IMPACT_GUESS on/off: {ab0['chat_us_lag']:.1f} vs {ab1['chat_us_lag']:.1f} us/ev ({d:.0f}% apart; P4 said <10%) and fires {ab0['fires']} vs {ab1['fires']}")

# ---- the composed 10^9 ledger ------------------------------------------------------------------
note("")
note("# The 10^9 ledger on the composed measured constants (rtf 100, budget 4 cores)")
N, RTF, DEL, M1R = 1e9, 100.0, 0.61, 29.3 / 50.0
c_x86 = arms["S3-ship-3e5-1800"]["chat_us_lag"]
note(f"  anchors: belt rate 3.55e-5/{SPLIT:.2f} = {RATE1:.3e}/B/game-s (interval-measured); C x86 {c_x86:.1f} us (S3, this box);")
note(f"  the composed arms' C stays the same order ({min(arms[t]['chat_us_lag'] for t in ('C5-comp-3e5-1800','C6-comp-3e5-3600','C7-comp-3e5-7200')):.0f}-{max(arms[t]['chat_us_lag'] for t in ('C5-comp-3e5-1800','C6-comp-3e5-3600','C7-comp-3e5-7200')):.0f} us): the split cuts count, not cost")
def cores(rate, c_us, dele=0.0):
    return N * rate * (c_us * 1e-6) * RTF * (1 - dele)
for name, rate, c, dele in [
    ("shipped cadence, shipped C (x86)", RATE0, c_x86, 0.0),
    ("8x split, shipped C (x86)", RATE1, c_x86, 0.0),
    ("8x split + 61% delete (x86)", RATE1, c_x86, DEL),
    ("8x split, M1 C (x0.586)", RATE1, c_x86 * M1R, 0.0),
    ("8x split + delete, M1 C", RATE1, c_x86 * M1R, DEL),
]:
    note(f"    {name:34s} {cores(rate, c, dele):7.2f} cores  -> fits 4? {cores(rate, c, dele) <= 4.0}")
need = 4.0 / (N * RATE1 * RTF * (1 - DEL)) / 1e-6
note(f"  the kick cost REQUIRED to close with split+delete: {need:.1f} us (today's x86 {c_x86:.0f}, M1 {c_x86*M1R:.1f})")
note(f"  b583's halving acts on the crash search; the belt arms' fires are N-independent (1179 at 1e4/1e5/3e5,")
note(f"  identical shipped vs composed): the belt kick holds no search, so the halving is absent from the 10^9 population.")

# ---- the crest ----------------------------------------------------------------------------------
note("")
note("# The crest (first-interval concentration), matched N and pace")
s3, c5, c6, s1, c1 = arms["S3-ship-3e5-1800"], arms["C5-comp-3e5-1800"], arms["C6-comp-3e5-3600"], arms["S1-ship-1e5-1800"], arms["C1-comp-1e5-1800"]
note(f"  3e5 rtf 1800: shipped spell {s3['spell_s']:.1f}s deficit {s3['deficit_s']:.0f} (delivered {s3['game_s']/ (31*1800)*100:.0f}% of due);")
note(f"                 composed spell {c5['spell_s']:.1f}s deficit {c5['deficit_s']:.0f} (delivered {c5['game_s']/(74*1800)*100:.0f}% of due)")
note(f"  3e5 rtf 3600 composed (36x pace): spell {c6['spell_s']:.1f}s, delivered {c6['game_s']/(39*3600)*100:.0f}% of due")
note(f"  3e5 rtf 7200 composed (control, must fail): spell {arms['C7-comp-3e5-7200']['spell_s']:.1f}s CLAMPED")
note(f"  1e5: shipped spell {s1['spell_s']:.1f}s; composed rtf 1800 {c1['spell_s']:.1f}s; rtf 14400 (control) {arms['C4-comp-1e5-14400']['spell_s']:.1f}s CLAMPED")

json.dump({t: {k: v for k, v in a.items()} for t, a in arms.items()}, open(os.path.join(HERE, "ledger2.json"), "w"), indent=1, default=str)
print("\nwrote ledger2.json")
