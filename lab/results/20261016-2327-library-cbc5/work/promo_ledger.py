#!/usr/bin/env python3
"""Promotion ledger at 10^9: the compact<->live boundary priced from measured constants.

Every constant is page-cited (lab/wiki pages, run ids); nothing is fitted.
Prints: controls (must reproduce e7ef), the working-set identity, the dwell wall,
and the promotion==kick identity. Pure arithmetic; runs in <1 s.
"""
B = 1_000_000_000
GB = 1e9

# --- constants (citations in dossier.md) ---
r_ship = 3.55e-5          # fired events /body/game-s, shipped doll grid (a9d7 gold; 3294 fire rate 1.000)
SPLIT = 8.0               # BELT_SPLIT, measured interval ratio 8.000x (7f97; 98cb)
DEL = 0.39                # remaining fraction after 1a46+RES 61% delete (98cb)
T = 28_141.5              # belt kick interval, game-s, doll grid (3294; belt_first anchor 28,144)
CH_X86 = 52.8e-6          # kick cost x86 upper (c01c: 43-52.8 us; composed 39-54 us, 98cb)
CH_M1 = 29.3e-6           # kick cost M1 (e7ef)
BIND = 0.84               # bind/refit share of kick cost, lower bound (b063: 84-89%)
P_ship = 5_062            # live bytes/body plateau, upper (b30b: 4,854-5,062)
P_diet = 56.5 + 29.6 / 8  # packed live state 56.0-56.8 B (42e6) + widest member bits (9d49) ~ 80 B
N_hot = (1.3e4, 2.7e4)    # measured hot set, rtf 100 (ba64)
CORES, MEM, RTF = 4.0, 6 * GB, 100.0

r8 = r_ship / SPLIT                       # composed cadence
lam_ship, lam_8, lam_del = r_ship * B, r8 * B, r8 * DEL * B   # promotions /game-s at 1e9

print("== Controls (instrument check against e7ef) ==")
cost4 = CORES / (lam_del * RTF)
print(f"required kick cost, composed(/8)+61% delete, 4 cores: {cost4*1e6:.1f} us  [e7ef: 23 us]")
print(f"cores at 52.8 us x86: {lam_del*RTF*CH_X86:.1f}  [98cb: 8.8 x86]")
print(f"cores at 29.3 us M1:  {lam_del*RTF*CH_M1:.1f}  [98cb: 5.1 M1]")
for gb in (6, 8):
    lo, hi = gb*GB/5062/1e6, gb*GB/4854/1e6
    print(f"ladder wall {gb} GB / plateau 4,854-5,062 B: {lo:.2f}-{hi:.2f} x1e6 bodies  [e7ef: 1.19-1.65e6]")

print("\n== Working-set identity (no fitted parameter) ==")
for name, lam in (("shipped rate", lam_ship), ("composed /8", lam_8), ("composed+delete", lam_del)):
    print(f"{name:>16}: resident at dwell=1 game-s = {lam:,.0f}  vs measured N_hot {N_hot[0]:,.0f}-{N_hot[1]:,.0f} (ba64)")

print("\n== Dwell wall: dwell* where resident x P busts 6 GB ==")
for name, lam in (("shipped rate", lam_ship), ("composed /8", lam_8), ("composed+delete", lam_del)):
    for pname, P in (("P_ship ~5 kB", P_ship), ("diet ~80 B", P_diet)):
        d = MEM / (lam * P)
        print(f"{name:>16} | {pname:>9}: dwell* = {d:,.0f} game-s = {100*d/T:,.1f}% of interval T=28,141.5")

print("\n== Promotion == kick identity (if every fired event mints a live body) ==")
print(f"promotion stream at 1e9 rtf 100: shipped {lam_ship*RTF:,.0f}/s, composed /8 {lam_8*RTF:,.0f}/s, +delete {lam_del*RTF:,.0f}/s")
mint = BIND * CH_X86
print(f"mint+demote priced at the bind/refit share (84% of 52.8 us = {mint*1e6:.0f} us):")
for name, lam in (("shipped rate", lam_ship), ("composed /8", lam_8), ("composed+delete", lam_del)):
    print(f"{name:>16}: {lam*RTF*mint:,.1f} cores  (kick ledger same: promotions ARE the kicks, 3294 fire=1.000)")
print(f"mint+demote budget for 4 cores at composed+delete: {CORES/(lam_del*RTF)*1e6:.1f} us  [= e7ef's kick requirement, identical]")

print("\n== Delete coverage = promotion-skip coverage (1a46, measured) ==")
print(f"in-situ locals: 200/233 = {200/233:.1%} skippable; belt frozen exclusion 274/712 = {274/712:.1%}; RES 708/712 = {708/712:.1%} (ledger effect -0.7%)")
