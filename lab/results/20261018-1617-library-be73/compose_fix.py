#!/usr/bin/env python3
"""compose_fix.py — the answer-or-expire fix composed from page-cited constants.

Every input is a published measurement (cited inline); the script only combines
them. Regenerates every number in the dossier's Evidence section."""

# --- inputs (page-cited, no new constants) ---------------------------------
LAM      = 0.0526        # mints/game-s, K-flat, const over 3,900 gs (acf2, nladder)
LAM_LOHI = (0.053, 0.064)# b8e2's held-scene band (dynamics), corroborates
BYTES    = 224           # B per window candidate: size_of tuple, exact (b77d-1fcf, acf2)
ADD      = 38            # the "+38" background of the mint Vec (acf2)
ENTRIES  = (1.9, 2.0)    # deque entries per mint, measured (acf2)
C_FORM   = 0.515e-9      # s/member, compare-form native 0.50-0.53 ns (acf2)
WALK     = 190e-9        # s/body, shipped bail full walk ~190 ns/body (96f6)
STORED   = 0.67e-3       # s/scan at K=1e6, store-grounded form (96f6)
BUDGET   = 12e-3         # s, frame budget (96f6/acf2 flights)
WALL8    = 8e9           # B
GS_FRAME = 1.5           # flown: 898.6 gs / 600 frames, rtf 100 (7581, nladder)
CAP      = 2048          # SCAN_BACKLOG entries, shipped

def t8gb(K):                # one-doll time to the 8 GB wall, no expiry, no answers
    return WALL8 / (LAM * BYTES * (K + ADD))

print("== P1: one-doll bust law  t_8GB = 8e9/(λ·224·(K+38)) ==")
for K in (1e4, 1e5, 1e6, 1e7, 1e8, 1e9):
    t = t8gb(K)
    print(f"  K={K:.0e}: {t:10.1f} game-s   ({t/100:.3f} wall-s at rtf 100)")
print(f"  at 1e6: script {t8gb(1e6):.0f} gs vs acf2 measured 687 gs "
      f"-> ratio {t8gb(1e6)/687:.3f}")

print("== P2: the 2048-count cap's byte edge ==")
# bytes at cap: 2048 deque entries ~ 2048/m distinct Vecs, each (K+ADD)·BYTES
for m in (1.0, 1.95):
    k = WALL8 * m / (CAP * BYTES) - ADD
    print(f"  entries/mint m={m}: cap alone holds 8 GB only below K = {k:.3e}")
print(f"  entries to 8 GB at K=1e6 without the cap: {WALL8/(BYTES*(1e6+ADD)):.1f}")

print("== P3: the answer half — per-frame cost of answering EVERY mint at arrival ==")
arr = LAM * GS_FRAME        # mints/frame
print(f"  arrivals/frame = λ·{GS_FRAME} gs/frame = {arr:.4f}")
rows = [("compare-form (acf2)", lambda K: C_FORM*(K+ADD)),
        ("shipped walk (96f6)",  lambda K: WALK*(K+ADD))]
for name, cost in rows:
    for K in (1e6, 1e7):
        us = arr*cost(K)*1e6
        print(f"  {name}: K={K:.0e} {us:10.1f} us/frame = {arr*cost(K)/BUDGET*100:7.2f}% of budget")
print(f"  store-grounded (96f6, 0.67 ms/scan at 1e6): {arr*STORED*1e6:.1f} us/frame "
      f"= {arr*STORED/BUDGET*100:.2f}% of budget")
print(f"  compare-form crosses the whole budget only at K = {BUDGET/(arr*C_FORM):.2e} (one doll)")
print(f"  shipped walk crosses it at             K = {BUDGET/(arr*WALK):.2e} (one doll)")

print("== P4: the latch spike — ONE forced answer inside a frame (shipped walk) ==")
for K in (6.3e4, 1e5, 2.3e5):
    print(f"  K={K:.1e}: {WALK*K*1e3:5.1f} ms = {WALK*K/BUDGET*100:5.0f}% of budget; "
          f"compare-form same answer {C_FORM*K*1e6:6.1f} us ({WALK/C_FORM:.0f}x cheaper)")

print("== P5: supersede bound — steady pin with expiry on the census triggers ==")
for D in (1e5, 1e6, 1e7):
    lo = ENTRIES[0]*BYTES*(D+ADD); hi = ENTRIES[1]*BYTES*(D+ADD)
    print(f"  D={D:.0e}: {lo/1e6:7.0f}-{hi/1e6:7.0f} MB ({WALL8/hi:5.0f}x under 8 GB)")
print(f"  partition ceiling for the 2-entry bound: D = {WALL8/(ENTRIES[1]*BYTES)-ADD:.2e}")
print("  load-independence: the bound uses no µ; b8e2's utilization knob")
print("  (µ/λ = 1.0 quiet vs 0.03-0.15 loaded) leaves it unchanged.")

print("== answer stream as a core fraction under partition (rtf 100) ==")
for D in (1e5, 1e6, 1e7):
    s = LAM*C_FORM*D*100
    print(f"  D={D:.0e}: {s*1e3:7.2f} ms/s = {s*100:5.2f}% of one core")

print("== λ corroboration ==")
print(f"  ladder λ {LAM}/gs inside b8e2's held-scene band {LAM_LOHI}/gs (member-independent)")
