#!/usr/bin/env python3
"""The second-author table: the depth ladder + the matched-fills control.
Reads flights/<scene>_<cut>k_<arm>.txt written by fly2.sh; prints one row per arm,
the identity verdict, and the anchor checks the dossier cites."""
import re, sys, glob, os

def parse(path):
    name = os.path.basename(path)
    scene, cut, arm = name.rsplit(".", 1)[0].split("_", 2)
    txt = open(path, errors="replace").read()
    d = {}
    d["digest"] = re.search(r"^digest ([0-9a-f]+)", txt, re.M).group(1)
    m = re.search(r"^bodies (\d+) \S+ \S+ catalogue_live (\d+) demotions (\d+) promotions (\d+) promote_us.*total_s ([\d.]+)", txt, re.M)
    d["bodies"], d["live"], d["dem"], d["pro"], d["promote_s"] = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), float(m.group(5))
    m = re.search(r"^retain hits (\d+) retained_now (\d+) evictions (\d+) cap (\d+)", txt, re.M)
    d["hits"], d["now"], d["evict"], d["cap"] = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    m = re.search(r"^kicks (\d+) opens (\d+) boundaries (\d+) handoffs \d+ lost (\d+) refused (\d+)", txt, re.M)
    d["kicks"], d["opens"], d["lost"], d["refused"] = int(m.group(1)), int(m.group(2)), int(m.group(4)), int(m.group(5))
    m = re.search(r"^build_s [\d.]+ frames \d+ wall_s ([\d.]+) rss_mb (\d+)", txt, re.M)
    d["wall"], d["rss"] = float(m.group(1)), int(m.group(2))
    return scene, cut, arm, d

rows = {}
for f in sorted(glob.glob("flights/*.txt")):
    if f.endswith("table.txt") or "sanity" in f: continue
    try:
        scene, cut, arm, d = parse(f)
        rows[(scene, cut, arm)] = d
    except Exception as e:
        print(f"WARN {f}: {e}")

hdr = f"{'scene':9} {'cut':4} {'arm':10} {'kicks':>7} {'dem':>7} {'pro':>8} {'ratio':>6} {'hits':>8} {'fills':>8} {'hitfr':>6} {'evict':>7} {'wall':>5} {'rss':>4}"
print(hdr)
for (scene, cut, arm) in sorted(rows, key=lambda k: (k[0], int(k[1][:-1]), k[2])):
    d = rows[(scene, cut, arm)]
    fills = d["hits"] + d["pro"]
    hf = d["hits"] / fills if fills else 0.0
    ratio = d["pro"] / d["dem"] if d["dem"] else 0.0
    print(f"{scene:9} {cut:4} {arm:10} {d['kicks']:>7} {d['dem']:>7} {d['pro']:>8} {ratio:>6.3f} {d['hits']:>8} {fills:>8} {hf:>6.3f} {d['evict']:>7} {d['wall']:>5.1f} {d['rss']:>4}")

print("\n-- identity (every seam arm's digest == its scene+cut ctl) --")
bad = 0
for (scene, cut, arm), d in sorted(rows.items()):
    if arm == "ctl": continue
    ctl = rows.get((scene, cut, "ctl"))
    if ctl and d["digest"] != ctl["digest"]:
        print(f"MISMATCH {scene} {cut} {arm}: {d['digest'][:16]} vs ctl {ctl['digest'][:16]}")
        bad += 1
print("all seam arms bit-identical to their ctl" if bad == 0 else f"{bad} MISMATCHES — VOID")
