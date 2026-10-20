#!/usr/bin/env python3
"""analyze.py <dir> — per-arm allocation constants from alloc_scope logs.
Player/ship per-item constants use the checker-corrected denominator (items[3]=player,
items[2]=ship — asserted by the seed-1 anchor reproducing 8994's 193.4/3.7 KB)."""
import re, sys, glob, os

d = sys.argv[1]
for log in sorted(glob.glob(os.path.join(d, "*.log"))):
    txt = open(log).read()
    name = os.path.basename(log)[:-4]
    m = re.search(r"kicks=(\d+).*?items=\[([\d, ]+)\]", txt)
    if not m:
        print(f"{name}: NO HEADER"); continue
    kicks = int(m.group(1)); items = [int(x) for x in m.group(2).split(",")]
    per_kick = re.search(r"per fired kick: item-scope ([\d.]+) KB alloc'd, base ([\d.]+) KB/game-s; per fired item \(any class\): item-scope ([\d.]+) KB", txt)
    scopes = {}
    for cls, sid, al, by, fr, re_ in re.findall(
        r"scope\s+(\S+)\s+\((\d+)\): allocs (\d+), bytes (\d+) \([\d.]+ KB\), frees (\d+), freed [\d.]+ KB, reallocs (\d+)", txt):
        rb = re.search(rf"scope\s+{cls}\s+\({sid}\): realloc bytes (\d+)", txt)
        scopes[int(sid)] = dict(cls=cls, allocs=int(al), bytes=int(by), reallocs=int(re_),
                                rbytes=int(rb.group(1)) if rb else 0)
    print(f"== {name}: kicks={kicks} items={items} item={per_kick.group(1)} KB/kick base={per_kick.group(2)} KB/gs")
    ship, player = scopes.get(3), scopes.get(4)
    if ship and items[2]:
        t = ship["bytes"] + ship["rbytes"]
        print(f"   ship:    {t/1e3:.1f} KB total, /ship-item(items[2]={items[2]}) = {t/items[2]/1e3:.1f} KB, /kick = {t/kicks/1e3:.2f} KB, calls/item={(ship["allocs"]+ship["reallocs"])/max(items[2],1):.1f}")
    if player and items[3]:
        t = player["bytes"] + player["rbytes"]
        print(f"   player:  {t/1e3:.1f} KB total, /player-item(items[3]={items[3]}) = {t/items[3]/1e3:.1f} KB, realloc-share={(player['rbytes']/t*100):.0f}%, calls/item={(player['allocs']+player['reallocs'])/items[3]:.1f}")
        print(f"            (author-denominator items[4]={items[4]}: {t/items[4]/1e3:.0f} KB — the 8994 author error)")
        # ladder decomposition from the >2KiB census
        rows = re.findall(r"\s+(\d+) B\s+player:\s+(\d+) calls,\s+(\d+) bytes, mean\s+(\d+) B", txt)
        tot = sum(int(b) for _, _, b, _ in rows)
        print(f"   player >2KiB census: {tot/1e3:.1f} KB = {tot/t*100:.0f}% of player term; rungs:")
        for bucket, calls, by, mean in sorted(rows, key=lambda r: int(r[0])):
            print(f"      bucket {bucket:>7}: {calls:>6} calls x mean {mean:>6} = {int(by)/1e3:8.1f} KB  (mean/352={int(mean)/352:.2f}, /384={int(mean)/384:.2f})")
    if ship:
        rows = re.findall(r"\s+(\d+) B\s+ship:\s+(\d+) calls,\s+(\d+) bytes, mean\s+(\d+) B", txt)
        tot = sum(int(b) for _, _, b, _ in rows)
        if tot: print(f"   ship >2KiB census: {tot/1e3:.1f} KB = {tot/(ship['bytes']+ship['rbytes'])*100:.0f}% of ship term")
