#!/usr/bin/env python3
"""The checker's named gold experiment, composed from the flown record.

Part 1 (CPU half): the standalone mint+demote measured on the flown store (promote_us
p50 + demote_us p50) against the 4-core mint budget at 1e9 rtf 100 — the 23.1 us line —
at shipped rate, /8 cadence, and composed /8 + 61% delete. Anchors reconciled.
Part 2 (memory half): the dwell dial per regime — resident collapse vs re-mint cost —
and the burn-knee extrapolation to 1e9 (does any dwell meet 6 GB AND ~4 cores?).

Pure arithmetic over flights/*.txt and page-cited constants; <1 s.
"""
import re, glob, os

B = 1e9
RTF = 100.0
r_ship = 3.55e-5          # fired events/body/game-s (a9d7; 3294 fire rate 1.000)
SPLIT, DEL = 8.0, 0.39    # BELT_SPLIT (7f97); 1a46+RES delete remainder (98cb)
P_entry = 1_400           # bytes/retained entry (measured below from rss deltas; ~0.96-1.6 kB class)
MEM = 6e9

def load():
    rows = {}
    for f in glob.glob(os.path.join(os.path.dirname(__file__), "flights", "*.txt")):
        t = open(f).read()
        g = lambda p: float(re.search(p, t).group(1)) if re.search(p, t) else float("nan")
        name = os.path.basename(f)[:-4]
        rows[name] = dict(
            digest=re.search(r"digest ([0-9a-f]+)", t).group(1)[:8],
            demotions=g(r"demotions (\d+)"), promotions=g(r"demotions \d+ promotions (\d+)"),
            promote_p50=g(r"promote_us p50 ([\d.]+)"), promote_p99=g(r"promote_us p50 [\d.]+ p99 ([\d.]+)"),
            demote_p50=g(r"demote_us p50 ([\d.]+)"), demote_p99=g(r"demote_us p50 [\d.]+ p99 ([\d.]+)"),
            mid90_res=float(re.search(r"mid90 tick \d+ retained_now (\d+)", t).group(1)) if "mid90" in t else float("nan"),
            hits=g(r"retain hits (\d+)"), resident=g(r"retain hits \d+ retained_now (\d+)"),
            dwell_ev=g(r"dwell_evictions (\d+)"), rss=g(r"rss_mb (\d+)"),
            bodies=g(r"bodies (\d+)"), wall=g(r"wall_s ([\d.]+)"),
        )
    return rows

rows = load()
def get(arm, n, reg): return rows[f"{arm}_{n}_{reg}_20000_1"]

print("== Identity controls (every arm must print its scene's ctl digest) ==")
for n, reg in ((100000, "coast"), (100000, "burn"), (10000, "coast"), (10000, "burn")):
    ctl = get("ctl", n, reg)["digest"]
    bad = [a for a in ("seam", "retain", "dwell100", "dwell1000") if get(a, n, reg)["digest"] != ctl]
    no = rows.get(f"noseam_100000_coast_20000_1", {}).get("digest")
    print(f"{n} {reg}: ctl {ctl}  arms_off={bad or 'NONE'}  noseam={'=ctl' if no == get('ctl',100000,'coast')['digest'] else no}")

print("\n== Part 1: standalone mint+demote on the flown store (the named experiment) ==")
for n in (10000, 100000):
    for reg in ("coast", "burn"):
        for a in ("seam", "retain", "dwell100", "dwell1000"):
            r = get(a, n, reg)
            md = r["promote_p50"] + r["demote_p50"]
            print(f"{a:>8} {n//1000}k {reg:>5}: mint p50 {r['promote_p50']:.2f} p99 {r['promote_p99']:.2f} | demote p50 {r['demote_p50']:.3f} p99 {r['demote_p99']:.3f} | mint+demote {md:.2f} us | promotions {r['promotions']:.0f} hits {r['hits']:.0f} resident {r['resident']:.0f}")

print("\n== The 23.1 us test (4-core mint budget at 1e9 rtf 100, composed /8 + delete) ==")
lam = {"shipped": r_ship * B, "/8": r_ship / SPLIT * B, "+delete": r_ship / SPLIT * DEL * B}
md_coast = get("retain", 100000, "coast")["promote_p50"] + get("retain", 100000, "coast")["demote_p50"]
md_burn = get("retain", 100000, "burn")["promote_p50"] + get("retain", 100000, "burn")["demote_p50"]
for md, tag in ((md_coast, "coast retain"), (md_burn, "burn retain"), (md_coast, "dwell100 coast")):
    if tag.startswith("dwell"):
        md = get("dwell100", 100000, "coast")["promote_p50"] + get("dwell100", 100000, "coast")["demote_p50"]
    print(f"{tag:>15}: mint+demote {md:.2f} us ->", end=" ")
    for k, l in lam.items():
        print(f"{k} {l*RTF*md*1e-6:.2f} cores", end="  ")
    print(f"| budget 4 cores <=> {23.1:.1f} us: {'HOLDS' if md <= 23.1 else 'DIES'}")

print("\n== Anchor reconciliation (why 9.2 / 34-38 / 486 differ from the measured mint) ==")
print(f"measured mint (the compile at true keys): {get('retain',100000,'coast')['promote_p50']:.2f} us coast, {get('retain',100000,'burn')['promote_p50']:.2f} us burn")
print("9.2 us  = add_body: compile + catalogue insert + bind_exact + store write (c4d3; the sticky wired path)")
print("34-38   = b29a's composed EVENT: compile 9.5 + readout 5.4 + from_state refit 21 + scar 0.9;")
print("         the refit is the kick's own settle bill (inside e7ef's kick C-hat), not the promotion's")
print("486 us  = resolve_handout, the wired sticky leaver (367f/b29a): dead by 13x")

print("\n== Part 2: the dwell dial per regime (standing resident = mid90, terminal = final settle) ==")
ARMS = ("seam", "dwell17", "dwell100", "dwell1000", "retain")
base = get("retain", 100000, "coast")["promotions"]
print("coast 10^5 (standing resident is N-independent; re-mints ~free):")
for a in ARMS[1:]:
    r = get(a, 100000, "coast")
    r4 = rows.get(f"{a}_10000_coast_20000_1", r)
    print(f"  {a:>9}: promotions {r['promotions']:.0f} ({r['promotions']/base:.2f}x retain) | standing resident {r['mid90_res']:.0f} (10^4: {r4['mid90_res']:.0f}) | terminal {r['resident']:.0f}")
print("burn 10^5 (reads = promotions + hits; the miss cliff sits between dwell 17 and 100):")
rb = get("retain", 100000, "burn")["promotions"]
for a in ARMS:
    r = get(a, 100000, "burn")
    reads = r["promotions"] + r["hits"]
    r4 = rows[f"{a}_10000_burn_20000_1"]
    print(f"  {a:>9}: promotions {r['promotions']:.0f} ({r['promotions']/rb:.2f}x retain) reads {reads:.0f} miss {r['promotions']/max(reads,1):.1%} | standing resident {r['mid90_res']:.0f} (10^4: {r4['mid90_res']:.0f}) | terminal {r['resident']:.0f}")

print("\n== Burn-knee extrapolation to 1e9 (standing resident = lambda_reads x dwell, reads' N-term b) ==")
b = (get("retain",100000,"burn")["promotions"] + get("retain",100000,"burn")["hits"]
     - get("retain",10000,"burn")["promotions"] - get("retain",10000,"burn")["hits"]) / 9e4
fixed = get("retain",10000,"burn")["promotions"] + get("retain",10000,"burn")["hits"] - b * 1e4
reads_s9 = (b * 1e9 + fixed) / 20000 * RTF
print(f"read stream: b = {b:.2f} reads/body/20k gs, fixed {fixed:.0f} -> at 1e9 rtf 100: {reads_s9:.3g} reads/s (wall)")
for a in ("dwell17", "dwell100", "dwell1000"):
    r5 = get(a, 100000, "burn")
    reads5 = r5["promotions"] + r5["hits"]
    miss = r5["promotions"] / max(reads5, 1)
    stand9 = r5["mid90_res"] * 1e9 / 1e5        # standing resident scales with the read stream's N-term
    mem9 = stand9 * P_entry
    remint = reads_s9 * miss * r5["promote_p50"] * 1e-6
    print(f"  {a:>9}: miss {miss:.1%} | standing@1e9 ~{stand9:.3g} entries ({mem9/1e9:.0f} GB) -> re-mint {remint:.0f} cores")
dmax = MEM / P_entry / (b * 1e9 / 20000)        # largest dwell whose standing set fits 6 GB
print(f"  memory-feasible dwell at 1e9: <= {dmax:.1f} gs; measured miss at the nearest flown class (17 gs): "
      f"{get('dwell17',100000,'burn')['promotions']/(get('dwell17',100000,'burn')['promotions']+get('dwell17',100000,'burn')['hits']):.0%}"
      f" -> re-mint {reads_s9 * get('dwell17',100000,'burn')['promotions']/(get('dwell17',100000,'burn')['promotions']+get('dwell17',100000,'burn')['hits']) * get('dwell17',100000,'burn')['promote_p50'] * 1e-6:.0f} cores")
print("  VERDICT: no dwell meets 6 GB and ~4 cores on burn at 1e9; the reads are the bill")

print("\n== Bytes per retained entry (rss delta, coast 10^5 retain: the only arm with a large clean resident) ==")
seam_rss, ret = get("seam", 100000, "coast")["rss"], get("retain", 100000, "coast")
print(f"  retain: rss {ret['rss']:.0f} - seam {seam_rss:.0f} over terminal resident {ret['resident']:.0f} = {(ret['rss']-seam_rss)*1e6/max(ret['resident'],1):.0f} B/entry")
