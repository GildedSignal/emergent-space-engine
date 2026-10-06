#!/usr/bin/env python3
"""Fermi budget: does 1e9 bodies fit one 8 GB M1, and what binds first?

Reads the frozen encounter evidence directly (P6 check), then computes the
memory/compute decision table from measured anchors. Pure arithmetic, no sim.
Run: python3 budget.py  (cwd = repo root or lab/results/20261006-1354-fermi-c9fa)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SCALE = os.path.join(ROOT, "artifacts/evidence/opus-encounters-20260930/scale.jsonl")
STEADY = os.path.join(ROOT, "artifacts/evidence/opus-encounters-20260930/steady.jsonl")

# ---------------- anchors (provenance in anchors.json) ----------------
N = 1e9                 # bodies (the goal)
CORES = 8.0             # M1: 4P+4E cores (docs/HANDOFF.md "The machine")
STATE_CAP_B = 4 * 2**30 # frozen ladder peak-RSS cap (scenarios/scale-ladder-v7.json)
BW = 60e9               # B/s unified memory (board bottleneck 5)
T_LEO = 5400.0          # s per orbit, 90-min low orbit (HANDOFF risk list)
KICK_US = 29e-6         # s, plane's kick today, M1 (H0210 limitations)
KICK_US_PROBE = 100e-6  # s, implied by H0190's 0.6 core per 1e6 at 32.5/orbit
CAD_RAW = 32.5          # kicks/orbit (H0190 K1)
CAD_AVG = 32.5 / 114.0  # averaged (H0190 K2)
SCAR_BITS = 64.0        # Elias-Fano ordinal ~22-24 bits at n=2^23 + packed delta row
TUBE_B = 16.0           # bytes, the law's 16-byte tube (docs/plane.md)
PROG_BITS_BELT = 0.126  # bits/body, gold components-98bc (board taste log)
PROG_B_CONV = 488.0 / 1e6  # bytes/body convoy program (H0208)

# ---------------- P6: hits rate vs rho, straight from frozen evidence -------
def p6():
    rows = [json.loads(l) for l in open(SCALE) if '"scale"' in l]
    out = []
    for r in rows:
        if r.get("sigma_e") != 0.01:
            continue
        hits_pb = r["hits_per_pair_orbit"] * r["cone_per_body"] / 2.0
        out.append((r["n"], r["rho"], hits_pb))
    st = [json.loads(l) for l in open(STEADY) if '"steady"' in l]
    st = max(st, key=lambda r: r["orbits"])  # converged row
    hits_steady, rho_steady = st["hits_per_body_orbit"], st["rho"]
    print("P6: hits/body/orbit vs rho (sigma_e=0.01 sweep, from scale.jsonl)")
    for n, rho, h in out:
        ratio = (h / rho) / (hits_steady / rho_steady)
        print(f"  n={n:>7}  rho={rho:.1e}  hits={h:.4f}  hits/rho vs steady = {ratio:7.3f}")
    print(f"  steady (converged 1e5 orbits): hits={hits_steady:.4f} at rho={rho_steady:.1e}")
    # the sweep keeps rho*N fixed, so hits there is the fixed-neighbourhood rate
    inv = [h for _, _, h in out]
    print(f"  sweep hits N-invariant within +/-{(max(inv)-min(inv))/min(inv)*100:.0f}% "
          f"(mean {sum(inv)/len(inv):.4f}), = fixed rho*N; steady belt at same n=3000 "
          f"but rho/3.33 gives hits/3.34 -> hits ~ rho at fixed n. P6 as written FAILS; "
          f"carry both rates: {hits_steady:.4f} and {sum(inv)/len(inv):.4f}\n")
    return hits_steady

HITS = p6()
HITS_SWEEP = 0.020

# ---------------- memory: scar production vs the 4 GiB cap ------------------
def memory_table():
    print("MEMORY: steady scar bits from encounters (the only per-body producer)")
    print(f"  state cap {STATE_CAP_B/2**30:.0f} GiB = {STATE_CAP_B*8:.2e} bit")
    for name, T_orb in [("90-min orbit", T_LEO), ("24-h orbit", 86400.0), ("1-AU orbit (~1 yr)", 3.156e7)]:
        for lbl, h in (("steady 5.9e-3", HITS), ("sweep 2.0e-2", HITS_SWEEP)):
            for bits in (40, 64, 96):
                rate = N * h / T_orb
                fill = STATE_CAP_B * 8 / (rate * bits)
                print(f"  {name:>20} hits={lbl} scar={bits:2d}b: fills cap in {fill/86400:9.2f} days (no reabsorption)")
    gen = N * PROG_BITS_BELT / 8
    print(f"  belt programs: {N:.0e} x {PROG_BITS_BELT} bit = {gen/2**20:7.1f} MiB; convoy form: {N*PROG_B_CONV/2**20:.1f} MiB")
    for f in (0.01, 0.05):
        print(f"  active fleet f={f:.0%}: {N*f*TUBE_B/2**30:.2f} GiB in 16-B tubes")
    s_mem = STATE_CAP_B * 8 / SCAR_BITS
    print(f"  S_live cap from MEMORY (scars only): {s_mem:.2e} bodies ({s_mem/N:.0%} of population)\n")
    return s_mem

# ---------------- compute: kick cadence x cost ------------------------------
def cores(rtf, cad, tkick, n_orbit=N, t_orb=T_LEO):
    return n_orbit * cad / t_orb * rtf * tkick

def compute_table():
    print("COMPUTE: cores for tide kicks at 1e9 bodies (90-min orbits)")
    print(f"{'RTF':>5} {'cadence':>9} {'kick':>10} {'cores':>9}  verdict vs 8-core M1")
    for rtf in (1, 10, 100):
        for cname, cad in (("raw 32.5", CAD_RAW), ("avg 0.285", CAD_AVG)):
            for kname, tk in (("29us plane", KICK_US), ("100us probe", KICK_US_PROBE)):
                c = cores(rtf, cad, tk)
                v = "fits" if c <= CORES else f"{c/CORES:.0f}x over"
                print(f"{rtf:>5} {cname:>9} {kname:>10} {c:9.0f}  {v}")
    p7 = cores(1, CAD_RAW, KICK_US)
    print(f"\nP7: 29us x 32.5/orbit at RTF 1 = {p7:.0f} cores (board ~190; predicted 140-220) "
          f"-> {'AGREES' if 140 <= p7 <= 220 else 'DISAGREES'}")
    print(f"  H0190's own averaged rate: {0.01*1000:.0f} cores/1e9 at RTF 1 vs mine {cores(1, CAD_AVG, KICK_US):.1f} "
          f"(same order; probe kick heavier)\n")

# ---------------- the unified number: allowed live set ----------------------
def live_set():
    print("UNIFIED: the live set S_live (bodies off program form) decides both budgets")
    for rtf in (1, 10, 100):
        s = CORES / (CAD_AVG / T_LEO * rtf * KICK_US)
        print(f"  RTF {rtf:>3}, 29us kicks: compute allows S_live <= {s:.2e} ({s/N:.0%})")
    s_fast = CORES / (CAD_AVG / T_LEO * 100 * 1.4e-6)
    print(f"  RTF 100, 1.4us kicks (20x cut): compute allows S_live <= {s_fast:.2e} ({s_fast/N:.0%})")
    s_cap = 5.23e7  # compute cap at RTF100/29us (row above)
    for T_orb, lbl in ((T_LEO, "90-min"), (86400.0, "24-h"), (3.156e7, "1-AU")):
        for h, hl in ((HITS, "5.9e-3"), (HITS_SWEEP, "2.0e-2")):
            feed = N * h / T_orb
            print(f"  {lbl} orbits, hits={hl}: feed {feed:7.1f} scars/s -> reabsorb within {s_cap/feed/3600:9.2f} h to hold S_live <= {s_cap:.1e}")
    ev = N * CAD_AVG / T_LEO * 100
    for touch in (32, 256, 4096):
        print(f"  bandwidth RTF100: {ev:.2e} kick-events/s x {touch} B touched = {ev*touch/BW*100:5.1f}% of 60 GB/s")
    print()

# ---------------- P5: resident candidate stores -----------------------------
def candidate_stores():
    print("P5: resident per-body candidate stores vs the 4 GiB cap (1e9 bodies)")
    rows = [json.loads(l) for l in open(SCALE) if '"scale"' in l and '"n"' in l]
    for r in rows:
        if r["n"] in (1000, 100000):
            print(f"  measured pair-store, n={r['n']:>6}: {r['per_pair_bytes_per_body']:>8.1f} B/body -> {r['per_pair_bytes_per_body']*N/2**30:7.0f} GiB at 1e9")
    for b in (16, 25, 64):
        print(f"  hypothetical {b} B/body resident certificate store: {b*N/2**30:5.0f} GiB ({b*N/STATE_CAP_B:.1f}x cap)")
    print("  -> certificates must be program-derived (ordinal neighbours ~0 B) + per-scar only\n")

s_mem = memory_table()
compute_table()
live_set()
candidate_stores()

print("BOTTOM LINE")
print(f"  S_live: memory cap {s_mem:.1e} vs compute cap (RTF100, 29us) 5.2e7 -> compute binds {s_mem/5.2e7:.0f}x before memory")
print(f"  at RTF 1 the order flips: compute cap 5.2e9 > population -> memory (5.4e8 scars) binds")
print(f"  RTF 10: both ~5e8 — the budgets bind together")
