#!/usr/bin/env python3
"""metrics.py — headline numbers of run 20261011-2132-spacex-91a0, computed from the raw rows.

Corrects the record defect the checker named: the shipped metrics.json said "zero kicks in
2000 game-seconds" and "ships peak 275", contradicting the rows. This script regenerates
every headline number from `hlive-*.json` (one JSON per invocation of
`xtask universe --hlive ...`; rows = one snapshot per game-second).

Usage: python3 metrics.py file1.json [file2.json ...]   (each file printed on its own line)
"""
import json
import math
import sys


def fit(xs, ys):
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    d = n * sxx - sx * sx
    return (n * sxy - sx * sy) / d if d else float("nan")


def log2_fit(t_pairs, y_pairs):
    """Bits gained per doubling of game time: fit y against log2(t)."""
    pts = [(math.log2(t), y) for t, y in zip(t_pairs, y_pairs) if t > 0 and y > 0]
    return fit([p[0] for p in pts], [p[1] for p in pts]) if len(pts) > 2 else float("nan")


def metrics(path):
    d = json.load(open(path))
    rows = d["rows"]
    t = [r["game_s"] for r in rows]
    half = t[len(t) // 2]

    kv = [(r["game_s"], r["fleet"]["floor_bits_per_member_velocity"]) for r in rows if r["fleet"]["members"] > 0]
    st = [(r["game_s"], r["fleet"]["floor_bits_per_member_state"]) for r in rows if r["fleet"]["members"] > 0]
    sh = [(r["game_s"], r["ships"]["floor_bits_per_ship"]) for r in rows if r["ships"]["n"] > 0]

    kicks = [r["ships"]["kicks_this_s"] for r in rows]
    contacts = [r["fleet"]["contacts_this_s"] for r in rows]
    last_kick_s = max((r["game_s"] for r, k in zip(rows, kicks) if k > 0), default=0)
    last_contact_s = max((r["game_s"] for r, c in zip(rows, contacts) if c > 0), default=0)

    prev_n = 0
    spawn_events = 0
    ship_deaths = 0
    cat = [r["catalogue_live"] for r in rows]
    for r in rows:
        n = r["ships"]["n"]
        if n > prev_n:
            spawn_events += n - prev_n
        elif n < prev_n:
            ship_deaths += prev_n - n
        prev_n = n

    bpb = [r["bytes_per_body"] for r in rows if r["bytes_per_body"] > 0]
    kv2 = [(g, y) for g, y in kv if g >= half]
    sh2 = [(g, y) for g, y in sh if g >= half]
    return {
        "file": path,
        "seed": d["seed"],
        "game_s_end": t[-1],
        "wall_s": round(d["wall_seconds"], 1),
        "kicks_total": sum(kicks),
        "kicks_per_game_s": round(sum(kicks) / t[-1], 2),
        "kicks_secs_nonzero": sum(1 for k in kicks if k > 0),
        "last_kick_game_s": last_kick_s,
        "contacts_total": rows[-1]["fleet"]["contacts_total"],
        "last_contact_game_s": last_contact_s,
        "contacts_last_100s": sum(c for r, c in zip(rows, contacts) if r["game_s"] > t[-1] - 100),
        "ships_peak": max(r["ships"]["n"] for r in rows),
        "ships_end": rows[-1]["ships"]["n"],
        "ship_bits_t1": round(sh[0][1], 1) if sh else None,
        "ship_bits_second_half_mean": round(sum(y for _, y in sh2) / len(sh2), 1) if sh2 else None,
        "ship_bits_slope_second_half": round(fit([g for g, _ in sh2], [y for _, y in sh2]), 5) if sh2 else None,
        "ship_keys_all_distinct": all(r["ships"]["n"] == r["ships"]["distinct_tubes"] for r in rows),
        "vel_bits_t1": round(kv[0][1], 1),
        "vel_bits_second_half_mean": round(sum(y for _, y in kv2) / len(kv2), 1) if kv2 else None,
        "vel_bits_slope_second_half": round(fit([g for g, _ in kv2], [y for _, y in kv2]), 5) if kv2 else None,
        "state_bits_t1": round(st[0][1], 1),
        "state_bits_end_members_nonzero": round(st[-1][1], 1),
        "state_bits_per_doubling": round(log2_fit([g for g, _ in st], [y for _, y in st]), 2),
        "members_end": rows[-1]["fleet"]["members"],
        "distinct_velocities_first_last": [rows[0]["fleet"]["distinct_velocities"], kv[-1][1] and next(r["fleet"]["distinct_velocities"] for r in reversed(rows) if r["fleet"]["members"] > 0)],
        "catalogue_first_last": [cat[0], cat[-1]],
        "catalogue_monotone_nondecreasing": all(b >= a for a, b in zip(cat, cat[1:])),
        "catalogue_flat_from_game_s": next(r["game_s"] for r in rows if r["catalogue_live"] == cat[-1]),
        "ship_spawn_events": spawn_events,
        "ship_deaths": ship_deaths,
        "bytes_per_body_first_max_last": [bpb[0], max(bpb), bpb[-1]],
    }


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(metrics(p)))
