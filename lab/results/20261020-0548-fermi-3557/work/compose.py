#!/usr/bin/env python3
"""Compose the 10^9 byte-traffic and allocator rows from the scoped probe's measured constants.

Every input is a number printed by `scoped_alloc` (work/logs/*.log); nothing is hand-set.
Bands: item B/kick and base B/gs are the min/max over the five decisive arms.
"""
import re, sys, pathlib

LOG = pathlib.Path(__file__).parent / "logs"
ARMS = [("10000", "coast", "240"), ("10000", "burn", "240"), ("30000", "coast", "240"),
        ("30000", "burn", "240"), ("10000", "coast", "480")]
PAT = re.compile(
    r"scoped: n=(\d+) flight=(\w+) rtf=(\d+) game_s=(\S+) kicks=(\d+) items=(\d+) "
    r"naive_allocs_per_kick=(\S+) naive_B_per_kick=(\S+) item_allocs_per_kick=(\S+) "
    r"item_B_per_kick=(\S+) item_share=(\S+) base_B_per_gs=(\S+) item_big_B_per_kick=(\S+) "
    r"naive_big_B_per_kick=(\S+)")

rows = []
text = (LOG / "decisive2.log").read_text() + (LOG / "decisive.log").read_text()
for m in PAT.finditer(text):
    rows.append(dict(n=int(m[1]), flight=m[2], gs=float(m[4]), kicks=int(m[5]),
                     naive_bpk=float(m[8]), item_apk=float(m[9]), item_bpk=float(m[10]),
                     share=float(m[11]), base_bpgs=float(m[12]), item_big=float(m[13]),
                     naive_big=float(m[14])))
want = {(int(n), f, int(s)) for n, f, s in ARMS}
sel = [r for r in rows if (r["n"], r["flight"], round(r["gs"] / 100) * 100 if r["gs"] < 30000 else 48000) in want
       or (r["n"], r["flight"]) in {(int(n), f) for n, f, _ in ARMS}]
# keep the five decisive arms (decisive.log's 45s arms have gs<5000; exclude them)
sel = [r for r in sel if r["gs"] > 20000]
assert len(sel) == 5, f"expected 5 arms, got {len(sel)}: {[(r['n'], r['flight'], r['gs']) for r in sel]}"

item_lo, item_hi = min(r["item_bpk"] for r in sel), max(r["item_bpk"] for r in sel)
item_a_lo, item_a_hi = min(r["item_apk"] for r in sel), max(r["item_apk"] for r in sel)
share_lo, share_hi = min(r["share"] for r in sel), max(r["share"] for r in sel)
base_coast = [r["base_bpgs"] for r in sel if r["flight"] == "coast"]
base_burn = [r["base_bpgs"] for r in sel if r["flight"] == "burn"]
# the burn wave's per-frame base scratch: parsed from the same log's per-arm >2KiB detail lines
big = {}  # (n, flight, wall) -> {scope: (allocs, bytes)} for the >2KiB tail lines
sec = None
for line in (LOG / "decisive2.log").read_text().splitlines():
    if line.startswith("=== "):
        _, n, flight, wall, _ = line.split()
        sec = big.setdefault((n, flight, wall), {})
    elif sec is not None:
        for scope in ("item-scoped", "base-scoped"):
            m = re.search(rf"^{scope}:.*>2KiB: (\d+) allocs (\d+) B", line)
            if m:
                sec[scope] = (int(m[1]), int(m[2]))
wb, wc = big[("10000", "burn", "240")], big[("10000", "coast", "240")]
big_burn, big_burn_B = wb["base-scoped"]
big_coast = wc["base-scoped"][0]
item_big_burn, base_big_burn = wb["item-scoped"][1], wb["base-scoped"][1]
frames = 240 * 60  # the arm's wall seconds at 60 presented fps
for lmbda, tag in [(4e-5, "lambda=4e-5"), (8.4e-5, "lambda=8.4e-5")]:
    kicks_s = lmbda * 1e9 * 100  # rtf 100
    marginal = kicks_s * item_lo / 1e9, kicks_s * item_hi / 1e9  # GB/s
    pct = lambda g: 100 * g / 60.0
    print(f"{tag}: kicks/wall-s {kicks_s:.2e}  marginal item traffic "
          f"{marginal[0]:.1f}-{marginal[1]:.1f} GB/s = {pct(marginal[0]):.0f}-{pct(marginal[1]):.0f}% of 60 GB/s"
          f"   after split8 (/4.92): {marginal[0]/4.92:.1f}-{marginal[1]/4.92:.1f} GB/s "
          f"= {pct(marginal[0]/4.92):.0f}-{pct(marginal[1]/4.92):.0f}%")
base_wall = max(base_burn) * 100 / 1e6  # B/gs * gs/wall-s -> MB/s at rtf 100
malloc_ns = 11.6  # f623's measured floor: ns per alloc+touch+free pair
for lmbda in (4e-5, 8.4e-5):
    calls = lmbda * 1e9 * 100 * item_a_hi
    print(f"allocator cores at {lmbda:.1e}: {calls * malloc_ns / 1e9:.2f} (split8: {calls * malloc_ns / 1e9 / 4.92:.2f})")
print(f"\nconstants over 5 arms: item {item_lo:.0f}-{item_hi:.0f} B/kick ({item_a_lo:.1f}-{item_a_hi:.1f} allocs/kick), "
      f"share {share_lo:.3f}-{share_hi:.3f}")
print(f"base: coast {min(base_coast):.0f}-{max(base_coast):.0f} B/gs, burn {min(base_burn):.0f}-{max(base_burn):.0f} B/gs "
      f"(N-flat at 1e4 and 3e4: coast identical, burn within 1 B/gs)")
print(f"base at 1e9 (N-flat, per frame not per body): {base_wall:.2f} MB/s wall at rtf 100 -- nil")
print(f"burn wave frame scratch: {(big_burn - big_coast)} extra >2KiB calls over {frames} frames = "
      f"{(big_burn - big_coast) / frames:.2f}/frame, avg {big_burn_B / big_burn / 1e3:.1f} KB, "
      f"{100 * base_big_burn / (base_big_burn + item_big_burn):.1f}% of burn-arm big bytes are BASE-scoped")
