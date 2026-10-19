#!/usr/bin/env python3
"""1b3f: fold the flight logs into the dossier's table. Deterministic counts and census from
probe lines; timings indicative (shared box)."""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
BODIES = 30028

ARMS = [
    ("ctrl-70k", "control (no pin, shipped rule)"),
    ("pin6e9", "global arm: pin D=6e9 ticks"),
    ("pin12e9", "global arm: pin D=1.2e10"),
    ("reader-pin6e9", "per-reader + pin D=6e9"),
    ("reader-pin12e9", "per-reader + pin D=1.2e10"),
    ("reader-nopin", "per-reader, no pin"),
    ("reader-pin67M", "negative: per-reader + D=2^26"),
    ("ctrl-burn", "control burn (SOI switch)"),
    ("reader-burn", "burn + per-reader + pin D=1.2e10"),
    ("reader-5ms", "5 ms corner + per-reader + pin"),
]

def num(pat, s, cast=float):
    m = re.search(pat, s)
    return cast(m.group(1)) if m else None

rows = []
for name, desc in ARMS:
    p = HERE / "logs" / f"{name}.log"
    if not p.exists():
        continue
    s = p.read_text()
    probes = re.findall(r"^probe: gs=(\d+) rss_mb=(\d+) bpb=(\d+) hist_gt1=(\d+) hist_total=(\d+) hist_max=(\d+) gap_s=([-\d.]+)", s, re.M)
    if not probes:
        rows.append((name, desc, "NO PROBE LINES — FOREIGN BINARY", ""))
        continue
    last = probes[-1]
    gs_last, rss, bpb, gt1, total, hmax, gap = int(last[0]), int(last[1]), int(last[2]), int(last[3]), int(last[4]), int(last[5]), float(last[6])
    ladder = re.search(r"^ladder: (.*)$", s, re.M)
    if not ladder:
        rows.append((name, desc, "TRUNCATED (no ladder line)", ""))
        continue
    L = ladder.group(1)
    game = num(r"game ([\d.]+) s", s)
    stats = re.search(r"stats \{opens (\d+), boundaries (\d+), handoffs (\d+), lost (\d+), refused (\d+), slices (\d+)\}", s)
    dolls = re.search(r"the player's doll \(frame, doll\): (\[[^\]]*\])", s)
    rows.append((name, desc, {
        "gs_probe": gs_last, "game_s": game,
        "retained_per_body": round(total / BODIES, 3), "hist_total": total, "hist_max": hmax,
        "gt1": gt1, "bpb_end": bpb, "rss_end": rss,
        "gap_s": gap,
        "over": num(r"over=(\d+)", L, int),
        "p99_ms": num(r"p99_ms=([\d.]+)", L), "p50_ms": num(r"p50_ms=([\d.]+)", L),
        "kicks_rate": num(r"kicks_per_body_gs=([\d.e-]+)", L), "events_rate": num(r"events_per_body_gs=([\d.e-]+)", L),
        "kicks": num(r"kicks (\d+) ", s, int), "events": num(r"events (\d+) ", s, int),
        "refused": int(stats.group(5)) if stats else None, "handoffs": int(stats.group(3)) if stats else None,
        "lost": int(stats.group(4)) if stats else None,
        "held_refusals": num(r"refusals held (\d+)", s, int), "dead": num(r"dead (\d+)", s, int),
        "alive": "alive(player) true" in s,
        "seen": num(r"\((\d+) seen\)", s, int),
        "doll_seq": dolls.group(1) if dolls else "?",
    }, ""))

hdr = ["arm", "desc", "retained/body", "hist_max", "bpb", "RSS MB", "gap s", "over", "p99 ms", "game s", "kicks/body/gs", "refused", "handoffs", "doll seq"]
print("\t".join(hdr))
for name, desc, d, _ in rows:
    if isinstance(d, str):
        print("\t".join([name, desc, d]))
        continue
    print("\t".join([
        name, desc, str(d["retained_per_body"]), str(d["hist_max"]), str(d["bpb_end"]), str(d["rss_end"]),
        f"{d['gap_s']:.0f}", str(d["over"]), str(d["p99_ms"]), f"{d['game_s']:.0f}",
        f"{d['kicks_rate']:.3e}", str(d["refused"]), str(d["handoffs"]), d["doll_seq"],
    ]))

print()
for name, desc, d, _ in rows:
    if isinstance(d, dict):
        print(f"{name}: kicks {d['kicks']} events {d['events']} lost {d['lost']} held_ref {d['held_refusals']} dead {d['dead']} alive {d['alive']} seen {d['seen']} gt1 {d['gt1']}")
