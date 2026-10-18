#!/usr/bin/env python3
"""The 10^9 CPU rail recomposed from regenerable anchors, at BOTH pace conventions.

The Fermi control: re-derive the standing 10^9 CPU row (10.3 M1 cores, split S*~20,
'kick <=23us required') independently. It fails: the row's implied belt rate is
9.9 events/body/interval where the page's own thrice-measured census says 2.00.

Sources (page-cited):
- belt interval 28,141.5 game-s: belt_first p50 first-kick 14,071.5 = interval/2.
- fired-kick census 3.55e-5/body/game-s, N- and seed-invariant (a9d7, gold) == 1/28,141.5.
- two combs, 1.00 kicks + 1.00 boundaries per body per interval (8ffc; 3294 fire-rate 1.000;
  checker2 at N=10^4: 1.008 + 1.007).
- 9e75's own "the average fits: 1.75 cores at rtf 1" == one comb at 50 us x86.
- kick cost bracket: 29.3 us (e7ef M1 event), 50 us (x86), 72 us (f5bd fired kick hi).
- survival: 0.615 belt (274/712 deleted, 1a46's own belt count); RES 0.
- encounters 0.95 cores at F=10^3 (b509); view 1e-4 (ee30); reabsorb 0.011 (d205);
  re-kick add-back 1/213 of deleted stream at 0.57x (f5bd k*=213).
- player pace: rtf 100 is the shipped flying pace (HANDOFF: Julien flies --rtf 100);
  rtf 1 is the literal "compared to real time" reading.
- memory (6793): 5,060 B live plateau; q16 store 3.0 GB; 126-bit bust 15.75 GB.
"""
import numpy as np

rng = np.random.default_rng(20261018)
AU = 101_300_000.0
PLANETS = {"Cinder": (-21, 35_600_000.0, 0.1), "Home": (-18, 99_300_000.0, 0.02), "Giant": (-10, 500_000_000.0, 0.05)}
planet_a = {n: p / (1 - e) / AU for n, (_, p, e) in PLANETS.items()}
planet_mu = {n: 2.0 ** m for n, (m, _, _) in PLANETS.items()}
INTERVAL = 28141.5
NB = 1e9
OTHER = 0.95 + 1e-4 + 0.011
REKICK = 0.0028 * 0.57
SURV = {"no delete (S=1)": 1.0, "flown belt delete (S=0.615)": 0.615, "RES (S=0)": 0.0}

def rail(S, cost_us, rtf):
    base = 2 / INTERVAL * NB * cost_us * 1e-6 * S
    if S == 0.0:
        base = REKICK * 2 / INTERVAL * NB * cost_us * 1e-6 + OTHER
    return base * rtf

print("=" * 100)
print("A. THE CONTROL: can the standing row regenerate? (Fermi lens attack 3)")
print(f"  identity: 1/interval = {1/INTERVAL:.3e} ev/B/game-s   vs a9d7 census 3.55e-5 (gold, N-invariant)")
one = {c: 1 / INTERVAL * NB * c * 1e-6 for c in (29.3, 50.0, 72.0)}
print(f"  one-comb rail at rtf 1: 29.3us={one[29.3]:.2f}, 50us={one[50.0]:.2f}, 72us={one[72.0]:.2f} cores")
print(f"  control C+ (9e75's own 'the average fits: 1.75 cores at rtf 1'): one comb @50us = {one[50.0]:.2f}  [PASS]")
standing = 10.3
print(f"  control C- (the standing row 4e2d/de7b/f790): {standing} M1 cores = "
      f"{standing/one[29.3]:.1f}x one-comb@29.3us, {standing/(2*one[29.3]):.1f}x two-comb@29.3us (at rtf 1)")
print(f"  its implied belt rate: {standing/(NB*29.3e-6)*INTERVAL:.1f} ev/B/interval vs the page's own measured"
      " census 2.00  [FAIL: not regenerable]")
print(f"  the artifact's mechanism, from the row's own anchors: at 10^4 the scene flies kicks ~73.8k + boundaries"
      " ~71.6k per comb window with the locals' N-INDEPENDENT 86-88k/interval stream (4e2d's own text): a"
      " per-body division of a locals-dominated scene count. At 10^9 the belt is everything and its rate is 2.00.")
print(f"  the rtf-100 anchors: two combs @29.3us x100 = {2*one[29.3]*100:.0f} cores ~ 9e75's '185-187 at rtf 100';"
      f" one comb @50us x100 = {one[50.0]*100:.0f} ~ e7ef's '104-178'.")

print("=" * 100)
print("B. THE RECOMPOSED RAIL at both pace conventions (cores = core-seconds per wall-second)")
print(f"{'':32s}{'rtf 1 (literal real time)':>28s}{'rtf 100 (shipped player pace)':>34s}")
for sl, S in SURV.items():
    lo = rail(S, 29.3, 1)
    hi = rail(S, 72.0, 1)
    print(f"{sl:32s}{lo:12.2f}-{hi:8.2f} cores{rail(S,29.3,100):16.0f}-{rail(S,72.0,100):8.0f} cores")
print("  (two combs; cost bracket 29.3-72us; S=0 rows add re-kick 0.28%@0.57x + encounters 0.95 + view + reabsorb)")
print(f"  budget 4.0 P-eq (5.12 with E-cores at 0.28P). rtf 1: fits everywhere except the 72us/no-delete corner"
      f" ({rail(1.0,72.0,1):.2f} = 1.28x over 4.0).")
print(f"  rtf 100: {rail(1.0,29.3,100):.0f}-{rail(1.0,72.0,100):.0f} no-delete, {rail(0.615,29.3,100):.0f}-"
      f"{rail(0.615,72.0,100):.0f} at the flown delete (26-79x over) -- ONLY the RES end closes "
      f"({rail(0.0,29.3,100):.1f}-{rail(0.0,72.0,100):.1f} cores).")
print(f"  the S dial's price at rtf 100: each 0.1 of survival = {0.1*2/INTERVAL*NB*29.3e-6*100:.0f}-"
      f"{0.1*2/INTERVAL*NB*72e-6*100:.0f} cores. No measured cadence lever closes rtf-100 CPU at S>=0.615:")
print(f"  split 8 (f790, measured) gives {rail(1.0,29.3,100)/8:.0f}-{rail(1.0,72.0,100)/8:.0f}; split+delete "
      f"{rail(0.615,29.3,100)/8:.0f}-{rail(0.615,72.0,100)/8:.0f}; the ~50ns event floor gives "
      f"{2/INTERVAL*NB*50e-9*100:.2f}-{2/INTERVAL*NB*50e-9*100:.2f}.")

print("=" * 100)
print("C. THE CREST AT rtf 1 IS THE GENESIS WAVE, NOT A STEADY RATE")
print(f"  steady rtf-1 demand: {2/INTERVAL*NB:.3e} ev/wall-s = {2/INTERVAL*NB*29.3e-6:.1f}-{2/INTERVAL*NB*72e-6:.1f}"
      " cores; 9e75's 19-20-h freeze is the rtf-100 budget clamp, not a rate.")
print(f"  at belt birth the genesis train (C50 40-58x, calendar d520) peaks ~20x for ~1.4e3 game-s: "
      f"{20*2/INTERVAL*NB*29.3e-6:.0f}-{20*2/INTERVAL*NB*72e-6:.0f} cores rtf 1 -- one-time, stagger-cured (f82a).")

print("=" * 100)
print("D. THE S DIAL (what the delete still owes), from shipped scenario.rs")
N = 200_000
a = 2.0 + rng.random(N)
e = np.minimum(rng.rayleigh(0.07, N), 0.4)
a = a[a * (1 - e) > 1.2]
def ratios(m):
    return sorted({j / k for j in range(1, m + 1) for k in range(1, m + 1) if np.gcd(j, k) == 1})
spared = np.zeros(a.size, bool)
per = {}
P = a ** 1.5
for n, pa in planet_a.items():
    r = P / pa ** 1.5
    near = np.zeros(a.size, bool)
    for ratio in ratios(8):
        near |= np.abs(r / ratio - 1.0) <= 0.02
    per[n] = near.mean()
    spared |= near
print(f"  frozen exclusion replica (j,k<=8, 2% on period): spared {spared.mean():.3f} "
      f"(anchor 434/712 = 0.615, ratio {spared.mean()/0.615:.2f})")
print("  per planet: " + ", ".join(f"{n}={v:.3f}" for n, v in per.items())
      + "  (Cinder zero: its period ratio to the belt exceeds 8)")
first = [(n, f"{j+1}:{j}", round(pa * ((j + 1) / j) ** (2 / 3), 3)) for n, pa in planet_a.items()
         for j in range(1, 64) if 2.0 <= pa * ((j + 1) / j) ** (2 / 3) < 3.0]
print(f"  first-order (j+1):j resonances inside [2,3) AU: {len(first)} -> {first if first else 'NONE'}")
for n in planet_a:
    print(f"    {n}: mu={planet_mu[n]:.2e}, shipped first-order W=2.5*mu^(2/3)={2.5*planet_mu[n]**(2/3):.2e}"
          f" (frozen 2% = this W x {0.02/(2.5*planet_mu[n]**(2/3)):.1f})")
print("  => no first-order member exists in the belt; the frozen 2% applies Giant-width protection to")
print("     >=2nd-order resonances: a dial with 33x (Home) headroom, not a tide fact (nladder's own note).")

print("=" * 100)
print("E. MEMORY ROW (cited 6793, reproduced as controls)")
print(f"  live wall: 8 GB / 5,060 B = {8e9/5060:.3e} live bodies (6793's 1.58-1.65e6) [PASS]")
print("  q16 store 3.0 GB + live: at 1.3 kB post-Carlson ~3.85M live -> total ~8.0 GB [AT the ceiling]")
print(f"  negative control: 126-bit store = {126e9/8/1e9:.2f} GB > 8 GB busts [PASS]")
print()
print("VERDICT: the standing 10.3-core 10^9 row is not regenerable at any pace (implied belt rate 9.9")
print("ev/B/interval vs the page's own census 2.00; a locals-dominated scene-rate artifact). Recomposed:")
print("rail = 2.08-5.12 cores x rtf/100 x S for the stream, plus the game-rate terms (encounters 0.95 at")
print("F=10^3, view, reabsorb, re-kick) which scale with the pace too. rtf 1: everything fits (<=5.2 worst,")
print("<=3.15 with the delete). rtf 100: the stream alone is 208-512 no-delete / 128-315 flown delete -- the")
print("row UNDERSTATES 20-50x -- and even RES carries the terms (encounters ~95 at F=10^3 on b509's own")
print("basis): rtf-100 closure needs the RES-legal delete AND b509's fleet contract AND/OR ns-class events.")
print("Two unpinned conventions decide 10^9 CPU: the pace (rtf) and the exclusion width (S): >100x together.")
print("Memory (6793) binds once pace and S let CPU close.")
