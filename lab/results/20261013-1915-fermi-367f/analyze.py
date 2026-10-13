#!/usr/bin/env python3
"""The N-ladder probe analysis: reads the bench JSONs, prints the break table."""
import json, re, sys, pathlib

D = pathlib.Path(__file__).parent / "data"
RUNGS = [48, 400, 1500, 4000]

def load(name):
    return json.loads((D / name).read_text())

def stat(st, name):
    m = re.search(name + r": (\d+)", st)
    return int(m.group(1)) if m else 0

def prof_of(r):
    return {p["stage"]: p for p in r["prof"] if p["count"]}

def per(pr, name):
    p = pr.get(name)
    if not p or not p["count"]:
        return (0.0, 0)
    return (p["ns"] / p["count"] / 1e3, p["count"])

rows = []
for pace, tag in [(100, "r100"), (1, "r1")]:
    for m in RUNGS:
        r = load(f"{tag}-m{m}.json")
        st, pr = r["stats"], prof_of(r)
        leb, kicks = stat(st, "leavers"), stat(st, "kicks")
        bodies = r["bodies"]
        ho_us, ho_n = per(pr, "hand-out (a member made a body)")
        hb_us, _ = per(pr, "  hand-out: bind (the member as a tube)")
        f2_us, f2_n = per(pr, "  fit again: the coarser word (bind_surface)")
        ki_us, ki_n = per(pr, "item: kick (Wisdom-Holman)")
        rk_us, rk_n = per(pr, "rekey (all deadlines)")
        fl = [c for c in r["engine_cost_by_kind"] if c["kind"] == "fleet"][0]
        game_s = r["frames"] * pace / 60.0
        leak = leb / m / game_s if m else 0
        rows.append(dict(pace=pace, m=m, rtf=r["rtf"]["median"], eng_p50=r["where_the_time_goes_ms"]["engine"]["p50"],
                         eng_p99=r["where_the_time_goes_ms"]["engine"]["p99"], worst=r["frame_cpu_ms"]["worst"],
                         over=r["rtf"]["overflow_frames"], evs=r["events_per_second"], bodies=bodies, leb=leb,
                         leak=leak, ho_us=ho_us, hb_us=hb_us, f2_pct=100 * f2_n / max(ho_n, 1),
                         ki_us=ki_us, rk_us=rk_us, rk_per_body=rk_us / max(bodies, 1),
                         fleet_us=fl["us_per_item"], bytes=r["bytes_per_body"],
                         rss0=r["rss_kb"]["after_construction"][0], rss=r["rss_kb"]["peak"]))
# seed check
for m in (400, 1500):
    r = load(f"r100-m{m}-s3.json")
    rows.append(dict(pace=100, m=m, seed=3, rtf=r["rtf"]["median"], evs=r["events_per_second"],
                     leb=stat(r["stats"], "leavers")))

hdr = ("pace m     rtf_med eng_p50 eng_p99 worst  over ev/s  bodies leb   leak/m/gs  handout bind fit2% kick  rekey/b fleet_us  B/body rss0MB rssMB")
print(hdr)
for x in rows:
    if x.get("seed"):
        print(f"s3   {x['m']:>5} {x['rtf']:>6.1f} {'-':>22} ev/s {x['evs']:.0f} leb {x['leb']}")
        continue
    print(f"{x['pace']:<4} {x['m']:>5} {x['rtf']:>6.1f} {x['eng_p50']:>6.2f} {x['eng_p99']:>6.2f} {x['worst']:>5.1f} {x['over']:>4} {x['evs']:>5.0f} {x['bodies']:>6} {x['leb']:>5} {x['leak']:>9.2e} {x['ho_us']:>7.0f} {x['hb_us']:>4.0f} {x['f2_pct']:>4.0f} {x['ki_us']:>5.0f} {x['rk_per_body']:>6.3f} {x['fleet_us']:>8.0f} {x['bytes']:>6} {x['rss0']/1024:>5.1f} {x['rss']/1024:>5.1f}")

# The exchange rates and the 10^9 identity
m4000 = [x for x in rows if x["pace"] == 1 and x["m"] == 4000][0]
m400 = [x for x in rows if x["pace"] == 1 and x["m"] == 400][0]
live_marginal_b = (m4000["bytes"] * m4000["bodies"] - m400["bytes"] * m400["bodies"]) / max(m4000["leb"], 1)
print(f"\nlive bytes per promoted body (marginal, m4000 vs m400): {live_marginal_b:.0f} B")
print(f"promotion time {m4000['ho_us']:.0f} us = {m4000['ho_us']/m4000['ki_us']:.1f} kicks; fit2 (coarser re-bind) on {m4000['f2_pct']:.0f}% of handouts")
compact_bits = 22  # fleet member, memory-h-live 17.8-22.3 bits/member
print(f"exchange rate vs compact member ({compact_bits} bits = {compact_bits/8:.1f} B): {live_marginal_b/(compact_bits/8):.0f}x in bytes")
print(f"exchange rate vs packed live floor 56.8 B (42e6): {live_marginal_b/56.8:.0f}x")
# 10^9 identity, belt regime (a9d7 rate) and plane regime (this run)
for name, rate in [("belt (a9d7)", 3.6e-5), ("plane battle (this run)", 0.041)]:
    ev = rate * 1e9
    promo = 0.05 * ev * m4000["ho_us"] * 1e-6
    kicks = 0.95 * ev * m4000["ki_us"] * 1e-6
    growth = 0.05 * ev * live_marginal_b / 1e6
    print(f"10^9 identity, {name}: {ev:.2e} events/game-s -> {kicks:.2f} cores of kicks + {promo:.2f} cores of promotions; sticky growth {growth:.1f} MB/game-s (8 GB in {8192/max(growth,1e-9)/60:.0e} game-min)")
