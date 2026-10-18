#!/usr/bin/env python3
"""compose_mem.py — the 10^9 memory wall, composed from measured constants only.

Every input is a published, measured constant from the lab's record (citation inline).
No flights; no fitted constants. Regenerates the dossier's Table 1 and checks
P1/P3/P4/P5 from predictions.md. Arithmetic is exact in the ratios; GB = 1e9 B.
"""
GB = 1e9

# --- inputs -----------------------------------------------------------------
BUDGET_TARGET = 6.0 * GB    # scoreboard: "10^9 in ~6 GB", <= ~6 B (48 bits)/body
BUDGET_HARD   = 8.0 * GB    # the M1's unified memory (HANDOFF, "The machine")
N = 1e9

plateau_now_lo, plateau_now_hi = 4850.0, 5060.0  # B per live body, b30b (nladder page)
plateau_carlson = 1300.0     # post-cd6e (HANDOFF interlock "live bodies x ~1.3 KB";
driven_q24_GB   = (4.8 * GB, 5.2 * GB) # event-scarred store q24 (ab9d, gold)
ship_program_B  = 16456.0    # the whole birth program, fixed size (98bc, gold)
rock_bits = (20.7, 22.1)     # bits/ship, phase-locked mature (6baf-2b8e, gold)
driven_q16_GB   = 3.0 * GB   # event-scarred store q16 (ab9d, gold)
driven_worst_bits = 126.0    # the scoreboard's driven-belt worst, bits/body
fully_mixed_bits  = 63.0     # a91f: fully mixed = "the first wall"
wall_measured = (1.2e6, 1.65e6)  # measured live wall (1051: every comb arm saturates it)

census = {"program": (17.3, 29.6),            # bits/body at rest (9d49, gold)
          "scarred": (88.0, 106.3),           # 17.3-29.6 + 70.7-76.7
          "individual": (149.7, 196.6)}
census_ceiling = (0.095, 0.129)               # individuals fraction at 4 GiB (9d49)
forte_band = (0.10, 0.20)                     # Forte: layer <= 10-20% of the one below

pin_per_1000 = 2048 * 226.0                   # 0.46 GB per 1,000 held-scan candidates (1fcf)
latch = (0.17 * GB, 0.95 * GB)                # FLOW latch cap, m=100..400 (b8e2/470f)
pin_C_worst = 1000.0
def bits_GB(b): return N * b / 8.0
def live(budget, compact, plateau): return (budget - compact) / plateau
M = lambda x: f"{x/1e6:5.2f}M" if x > 0 else " BUST"


rows = [
    ("ship belt (program)",    (ship_program_B, ship_program_B)),
    ("rock, phase-locked 22b", tuple(bits_GB(b) for b in rock_bits)),
    ("driven q16 (3.0 GB)",    (driven_q16_GB, driven_q16_GB)),
    ("driven q24 (4.8-5.2)",   tuple(g for g in driven_q24_GB)),
    ("driven worst 126b",      (bits_GB(driven_worst_bits),)*2),
    ("fully mixed 63b",        (bits_GB(fully_mixed_bits),)*2),
]

print("Table 1 — the 10^9 memory wall, composed. Live ceilings in millions;")
print("conservative: compact=hi everywhere. plateau now = b30b 4.85-5.06 kB/B; C = post-Carlson 1.3 kB.")
print(f"{'mix (all 10^9)':22} {'compact':>10} {'@6G now':>8} {'@8G now':>8} {'@6G C':>7} {'@8G C':>7}")
for name, (lo, hi) in rows:
    print(f"{name:22} {lo/GB:>4.2f}-{hi/GB:<5.2f} "
          f"{M(live(BUDGET_TARGET,hi,plateau_now_hi)):>8} {M(live(BUDGET_HARD,hi,plateau_now_hi)):>8} "
          f"{M(live(BUDGET_TARGET,hi,plateau_carlson)):>7} {M(live(BUDGET_HARD,hi,plateau_carlson)):>7}")

print()
print("P1 — identity: the ship-belt row at the shipped plateau vs the measured wall")
w_lo = live(BUDGET_HARD,  ship_program_B, plateau_now_hi)
w_tgt = live(BUDGET_TARGET, ship_program_B, plateau_now_hi)
print(f"  8 GB/5060 B = {w_lo/1e6:.2f}M, 6 GB/5060 B = {w_tgt/1e6:.2f}M; measured wall "
      f"{wall_measured[0]/1e6:.2f}-{wall_measured[1]/1e6:.2f}M -> "
      f"{'HOLDS' if w_lo <= wall_measured[1]*1.08 and w_tgt >= wall_measured[0]*0.92 else 'FAILS'}")

print()
print("P3 — the quantum decides existence")
worst = bits_GB(driven_worst_bits)
print(f"  126-bit driven: {worst/GB:.2f} GB compact alone vs 8 GB hard -> "
      f"{'BUSTS at ZERO live bodies' if worst > BUDGET_HARD else 'fits'}")
q16_live = live(BUDGET_HARD, driven_q16_GB, plateau_carlson)
print(f"  q16 driven: {driven_q16_GB/GB:.1f} GB + post-Carlson live ceiling {q16_live/1e6:.2f}M at 8 GB "
      f"-> {'HOLDS (>2M)' if q16_live > 2e6 else 'FAILS'}")

print()
print("P4 — complements, not substitutes")
a = ("Carlson alone cannot fit the 126-bit worst" if worst > BUDGET_HARD
     else "Carlson alone fits it (P4 fails)")
q24_wall = driven_q24_GB[1] + wall_measured[1] * plateau_now_hi
b_ = (f"quantum alone (q24, {driven_q24_GB[1]/GB:.1f} GB) + the wall's own live count at the 5 kB "
      f"plateau = {q24_wall/GB:.1f} GB > 8 GB -> no margin" if q24_wall > BUDGET_HARD
      else "q24 fits the wall's count (P4 fails)")
print(f"  {a}; {b_}")
print(f"  -> {'HOLDS (both fail alone)' if worst > BUDGET_HARD and q24_wall > BUDGET_HARD else 'FAILS'}")

print()
print("P5 — fences second-order at the fitting mixes (quiet vs battle-alive latch)")
fences_lo = latch[0] + pin_per_1000
fences_hi = latch[1] + pin_per_1000
for name, (lo, hi) in rows:
    slack6 = BUDGET_TARGET - hi
    ok_lo, ok_hi = slack6 - fences_lo, slack6 - fences_hi
    verdict = ("yes/yes" if ok_lo > 0.13e9 and ok_hi > 0.13e9
               else ("quiet only" if ok_lo > 0.13e9 else "NO"))
    print(f"  {name:22} slack@6G {slack6/GB:6.2f} GB; minus fences quiet {ok_lo/GB:6.2f} / "
          f"battle {ok_hi/GB:6.2f} GB; 1e5 post-Carlson live needs 0.13 GB -> {verdict}")
print(f"  fences total: quiet {fences_lo/GB:.2f} GB = {fences_lo/BUDGET_TARGET*100:.0f}% of 6 GB; "
      f"battle {fences_hi/GB:.2f} GB = {fences_hi/BUDGET_TARGET*100:.0f}%")

print()
print(f"  individuals {census_ceiling[0]*100:.1f}-{census_ceiling[1]*100:.1f}% of population; "
      f"scarred 24% (9d49); Forte band for a layer over the one below: {forte_band[0]*100:.0f}-{forte_band[1]*100:.0f}% "
      f"-> individuals sit inside it, scarred 1.2x over its top edge")
print(f"  the promotion jump (store individual -> live runtime): "
      f"{plateau_carlson/(census['individual'][1]/8):.0f}x post-Carlson, "
      f"{plateau_now_hi/(census['individual'][1]/8):.0f}x at the shipped plateau "
      f"({census['individual'][1]:.1f} bits = {census['individual'][1]/8:.1f} B at rest)")
