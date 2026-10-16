#!/usr/bin/env python3
"""Wave census for the stagger rung (20261016-0346-scout-7da3).

Reads the stagger example's CSVs (frame, game_s, ms, events, lag_s), finds the
event-mass waves, and reports per-wave peak events/frame, peak ms, the train's
flatness wave over wave, and us/event on the heaviest frames. Pure arithmetic
on the recorded rows; no re-flight.
"""
import csv, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    rows = []
    with open(os.path.join(HERE, name)) as f:
        for r in csv.DictReader(f):
            rows.append((int(r["frame"]), float(r["game_s"]), float(r["ms"]), int(r["events"])))
    return rows

def census(name):
    rows = load(name)
    tot = sum(r[3] for r in rows)
    # Wave windows: 1000 game-s buckets by event mass; a wave is a run of buckets above
    # 5% of the max bucket. Report peaks inside each wave.
    B = 1000.0
    buckets = {}
    for r in rows:
        buckets.setdefault(int(r[1] // B), [0, 0])
        buckets[int(r[1] // B)][0] += r[3]
        buckets[int(r[1] // B)][1] += 1
    if not buckets:
        return None
    mx = max(v[0] for v in buckets.values())
    hot = sorted(k for k, v in buckets.items() if v[0] > 0.05 * mx)
    waves, cur = [], [hot[0], hot[0]]
    for k in hot[1:]:
        if k == cur[1] + 1:
            cur[1] = k
        else:
            waves.append(tuple(cur)); cur = [k, k]
    waves.append(tuple(cur))
    # per-frame peaks inside each wave window, plus us/event on the peak frame
    out = {"file": name, "frames": len(rows), "game_s_span": (rows[0][1], rows[-1][1]),
           "events_total": tot, "waves": []}
    for (a, b) in waves:
        w = [r for r in rows if a * B <= r[1] < (b + 1) * B]
        pk = max(w, key=lambda r: r[3])
        pkm = max(w, key=lambda r: r[2])
        us_per_ev = pkm[2] * 1e3 / pkm[3] if pkm[3] else 0.0
        out["waves"].append({"win_game_s": (a * B, (b + 1) * B), "events": sum(r[3] for r in w),
                             "peak_ev_frame": pk[3], "peak_ev_at_game_s": round(pk[1]),
                             "peak_ms": pkm[2], "peak_ms_events": pkm[3],
                             "us_per_event_at_peak_ms": round(us_per_ev, 1)})
    return out

if __name__ == "__main__":
    for name in sys.argv[1:]:
        c = census(name)
        if not c:
            continue
        print(f"\n== {c['file']}: {c['frames']} frames, game-s {c['game_s_span'][0]:.0f}..{c['game_s_span'][1]:.0f}, events {c['events_total']}")
        for i, w in enumerate(c["waves"]):
            print(f"  wave {i}: game-s {w['win_game_s'][0]:.0f}-{w['win_game_s'][1]:.0f} events {w['events']}"
                  f" peak {w['peak_ev_frame']}/frame @ {w['peak_ev_at_game_s']} | peak ms {w['peak_ms']:.2f} ({w['peak_ms_events']} ev, {w['us_per_event_at_peak_ms']} us/ev)")
