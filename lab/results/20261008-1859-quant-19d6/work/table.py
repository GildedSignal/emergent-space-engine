#!/usr/bin/env python3
"""Compact the bench JSONs into one comparison table (capacity knee + burn impact)."""
import json, glob, os

D = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(os.path.join(D, "*.json"))):
    try:
        j = json.load(open(f))
    except Exception as e:
        print(f, "unreadable:", e); continue
    if "frame_ms" not in j: continue
    k = j["engine_cost_by_kind"]
    it = {c["kind"]: c["items"] for c in k}
    us = {c["kind"]: round(c["us_per_item"], 1) for c in k}
    rows.append(dict(
        name=os.path.basename(f)[:-5], rtf=j["rtf_target"], lvl=j["throttle_level"],
        f_p50=j["frame_ms"]["p50"], f_p99=j["frame_ms"]["p99"], f_p999=j["frame_ms"]["p99.9"],
        cpu_p50=j["frame_cpu_ms"]["p50"], cpu_p99=j["frame_cpu_ms"]["p99"],
        cpu_p999=j["frame_cpu_ms"]["p99.9"], cpu_worst=j["frame_cpu_ms"]["worst"],
        hitches=",".join(map(str,j["frame_cpu_ms"]["hitch_counts"])),
        rtf_med=j["rtf"]["median"], rtf_low1=j["rtf"]["lowest_1pct"], ovf=j["rtf"]["overflow_frames"],
        ev_s=j["events_per_second"],
        eng_p99=j["where_the_time_goes_ms"]["engine"]["p99"], eng_share=j["where_the_time_goes_ms"]["engine"]["share"],
        view_share=j["where_the_time_goes_ms"]["view_gather"]["share"],
        json_share=j["where_the_time_goes_ms"]["view_json"]["share"],
        items=it, us_item=us, lost=len(j["lost_bodies"]) if isinstance(j["lost_bodies"], list) else j["lost_bodies"], alive=j["player_alive"],
        digest=j["digest"][:16],
    ))

hdr = ("name            rtf   lvl  cpuP50  cpuP99 cpuP99.9 worst  rtfMed rtfLow1  ovf  ev/s    eng%  view% json%  items(p/m/s/pl/fl)           alive lost digest")
print(hdr)
for r in rows:
    i = r["items"]; u = r["us_item"]
    print(f"{r['name']:<15} {r['rtf']:<5} {r['lvl']:<3}  {r['cpu_p50']:6.2f}  {r['cpu_p99']:6.2f} {r['cpu_p999']:7.2f} {r['cpu_worst']:6.2f} {r['rtf_med']:6.0f} {r['rtf_low1']:7.0f} {r['ovf']:4d} {r['ev_s']:7.0f} {100*r['eng_share']:4.0f}  {100*r['view_share']:4.0f}  {100*r['json_share']:4.0f}  {i.get('planet',0)}/{i.get('moon',0)}/{i.get('ship',0)}/{i.get('player',0)}/{i.get('fleet',0)}  {r['alive']} {r['lost']:4d} {r['digest']}")
print()
for r in rows:
    print(r["name"], "us/item by kind:", r["us_item"])
# wake breadth: level effect on non-player kinds at rtf 100
def find(n):
    return next((r for r in rows if r["name"] == n), None)
b, l5, l15 = find("base-rtf100"), find("burn-rtf100-L5"), find("burn-rtf100-L15")
if b and l15:
    print("\nwake breadth (items, rtf100): base vs L5 vs L15")
    for kind in ["planet", "moon", "ship", "player", "fleet"]:
        print(f"  {kind:<7} {b['items'].get(kind,0):>8} {l5['items'].get(kind,0) if l5 else '-':>8} {l15['items'].get(kind,0):>8}")
