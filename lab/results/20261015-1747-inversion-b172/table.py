#!/usr/bin/env python3
"""The falsifier table: belt vs formation, per scene and cap.
Reads flights/*.txt written by fly.sh; prints one row per arm and the verdicts."""
import re, sys, glob, os

def parse(path):
    name = os.path.basename(path)
    txt = open(path, errors="replace").read()
    arm = re.search(r"^arm (.*)$", txt, re.M).group(1)
    d = {}
    d["digest"] = re.search(r"^digest ([0-9a-f]+)", txt, re.M).group(1)
    m = re.search(r"^bodies (\d+) \S+ \S+ catalogue_live (\d+) demotions (\d+) promotions (\d+) promote_us.*total_s ([\d.]+)", txt, re.M)
    d["bodies"], d["live"], d["dem"], d["pro"], d["promote_s"] = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), float(m.group(5))
    m = re.search(r"^retain hits (\d+) retained_now (\d+) evictions (\d+) cap (\d+)", txt, re.M)
    d["hits"], d["now"], d["evict"], d["cap"] = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    m = re.search(r"^kicks (\d+) opens \d+ boundaries \d+ handoffs \d+ lost (\d+) refused (\d+)", txt, re.M)
    d["kicks"], d["lost"], d["refused"] = int(m.group(1)), int(m.group(2)), int(m.group(3))
    m = re.search(r"^build_s [\d.]+ frames \d+ wall_s ([\d.]+) rss_mb (\d+)", txt, re.M)
    d["wall"], d["rss"] = float(m.group(1)), int(m.group(2))
    scene = "belt" if "form" not in name else ("K100" if "form100" in name else ("K10" if "form10" in name else "?"))
    kind = "ctl" if "ctl" in name else ("retain" if "retain" in name else "cap" + re.search(r"_(\d+)_", name).group(1))
    n = re.search(r"_(\d+)_burn", name).group(1)
    return scene, kind, n, d

rows = {}
for f in sorted(glob.glob("flights/*.txt")):
    if f.endswith("table.txt") or "sanity" in f: continue
    try:
        scene, kind, n, d = parse(f)
        rows[(scene, kind, n)] = d
    except Exception as e:
        print(f"WARN {f}: {e}")

print(f"{'scene':5} {'arm':8} {'N':>7} {'dem':>7} {'pro':>8} {'ratio':>6} {'hits':>8} {'hitfr':>6} {'evict':>7} {'now':>7} {'lost':>4} {'ref':>3} {'wall':>5} {'rss':>4}")
for (scene, kind, n) in sorted(rows, key=lambda k: (k[0], k[2], k[1])):
    d = rows[(scene, kind, n)]
    fills = d["hits"] + d["pro"]
    hf = d["hits"] / fills if fills else 0.0
    ratio = d["pro"] / d["dem"] if d["dem"] else 0.0
    print(f"{scene:5} {kind:8} {n:>7} {d['dem']:>7} {d['pro']:>8} {ratio:>6.3f} {d['hits']:>8} {hf:>6.3f} {d['evict']:>7} {d['now']:>7} {d['lost']:>4} {d['refused']:>3} {d['wall']:>5.1f} {d['rss']:>4}")

# Identity: every seam arm's digest must equal its scene ctl digest.
print("\n-- identity (digest == scene ctl) --")
bad = 0
for (scene, kind, n), d in sorted(rows.items()):
    if kind == "ctl": continue
    ctl = rows.get((scene, "ctl", n))
    if ctl and d["digest"] != ctl["digest"]:
        print(f"MISMATCH {scene} {kind} N={n}: {d['digest'][:16]} vs ctl {ctl['digest'][:16]}")
        bad += 1
print("all seam arms bit-identical to their ctl" if bad == 0 else f"{bad} MISMATCHES — VOID")
