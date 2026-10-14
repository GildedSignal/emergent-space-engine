#!/usr/bin/env python3
"""The 10^9 game-second ledger, composed from shipped-code constants and the lab's
measured constants (each cited). CPU in cores = CPU-seconds per game-second at rtf 1;
the M1 budget is 4 performance cores. Every input is printed with its source.

Code constants (this tree, commit 33c83f1a):
  step_log2 = 7            crates/universe/src/ctx.rs:44  -> kappa = 2^7 = 128 kicks per radial period
  step rounding            crates/universe/src/step.rs:75-97 (power-of-two, so kappa in [128,256])
  MIN_STEP 128, MAX_STEP 2^50   step.rs:49-50 (checked: neither binds in the plane)
  plane orbits             crates/universe/src/scenario.rs:115-256 (PLANETS, moon, haulers,
                           orbiters, skimmers, fleet/player altitudes)
  root unit = 1.477 km (the sun's M); AU = 101_300_000 root units (scenario.rs:10); c = 1.

Measured constants (lab wiki pages, gold unless noted):
  a9d7  fired kicks 3.55-3.64e-5 /body/game-s, invariant in seed and N   (memory-h-live)
  3071 natives' compiled rates 0.0484 -> 3e-5 /s, 1613:1                 (nladder)
  7497  Orbiters 202-223 kicks/orbit                                     (nladder)
  367f  shipped kick 182-231 us; battle density 0.041 events/member/s    (frame-cost)
  790b  stacked ceiling ~2.8e4 battle members; D-slope 10.6 us/member/s  (frame-cost)
  90fb  encounter cascade: 0.077 cores (skin on) / 0.966 (no skin) per 10^4-cell (encounters)
  0820  driven-belt memory 126 bits/body; quiet 21-40 bits/body          (memory-h-live)
  ba64  hot: 6.9 KB/live body, N_hot 1.3-2.7e4 at rtf 100                (memory-h-live)
  ad26  Carlson-priced event 30 us; floor 42-55 ns (scoreboard)          (frame-cost)
"""
import math

G = 6.674e-11
MSUN = 1.989e30
ROOT_M = 1477.0            # metres in one root unit
AU_M = 101_300_000 * ROOT_M
YR = 3.156e7

def kep(r_m, m_kg):
    """Circular-orbit period, seconds."""
    return 2 * math.pi * math.sqrt(r_m ** 3 / (G * m_kg))

KAPPA_LO, KAPPA_HI = 128.0, 256.0   # step = 2^floor(log2(P/128)) -> kappa in [128,256]
def rate(P):
    return KAPPA_LO / P, KAPPA_HI / P

print("=" * 78)
print("1. THE CADENCE LAW AGAINST THE MEASURED ROSTER (prediction 1 and 2)")
print("=" * 78)
m_home = MSUN * 2 ** -18
m_giant = MSUN * 2 ** -10
r_home = 4313 * ROOT_M
r_giant = 47400 * ROOT_M

# Fastest Orbiter: alt = 1.15 Home radii (scenario.rs:210, k=0, e<=0.02)
P_orb0 = kep(1.15 * r_home, m_home)
# Player / fleet: 7,000 km altitude (scenario.rs:246-251)
P_player = kep(r_home + 7000e3, m_home)
# Moon: 60 Earth radii in Home's doll (scenario.rs:176-181), mass 2^-6 of Home
P_moon = kep(60 * r_home, m_home + m_home * 2 ** -6)
# Fastest hauler: a = 0.5 AU, e<=0.25 (scenario.rs:190-191)
P_haul0 = kep(0.5 * AU_M, MSUN)
# Slowest hauler: a = 8 AU
P_haul1 = kep(8.0 * AU_M, MSUN)
# Planets (periapsis -> a = p/(1-e))
for name, per_root, e in (("Cinder", 35.6e6, 0.1), ("Home", 99.3e6, 0.02), ("Giant", 500e6, 0.05)):
    a = per_root * ROOT_M / (1 - e)
    print(f"  {name:7s} a={a/AU_M:5.2f} AU  P={kep(a, MSUN)/YR:6.2f} yr   rate {rate(kep(a,MSUN))[0]:.1e}-{rate(kep(a,MSUN))[1]:.1e}/s")
print(f"  Orbiter0 (1.15 R_Home)  P={P_orb0:7.0f} s ({P_orb0/60:.0f} min)  rate {rate(P_orb0)[0]:.4f}-{rate(P_orb0)[1]:.4f}/s   [3071 top: 0.0484]")
print(f"  Player (7000 km alt)    P={P_player:7.0f} s ({P_player/3600:.1f} h)    rate {rate(P_player)[0]:.4f}-{rate(P_player)[1]:.4f}/s")
print(f"  Moon (60 R_Home)        P={P_moon:7.0f} s ({P_moon/86400:.1f} d)     rate {rate(P_moon)[0]:.2e}-{rate(P_moon)[1]:.2e}/s")
print(f"  Hauler a=0.5 AU         P={P_haul0:7.0f} s ({P_haul0/YR:.3f} yr)  rate {rate(P_haul0)[0]:.2e}-{rate(P_haul0)[1]:.2e}/s   [3071 floor: 3e-5]")
print(f"  Hauler a=8 AU           P={P_haul1:7.0f} s ({P_haul1/YR:.1f} yr)   rate {rate(P_haul1)[0]:.2e}-{rate(P_haul1)[1]:.2e}/s")
top = rate(P_orb0)[1] / 0.0484
floor_ = rate(P_haul0)[1] / 3e-5
print(f"  -> roster TOP  predicted {rate(P_orb0)[1]:.4f} vs measured 0.0484 : ratio {top:.2f} (within 2x: {top<2})")
print(f"  -> roster FLOOR predicted {rate(P_haul0)[1]:.2e} vs measured 3e-5  : ratio {floor_:.2f} (within 2x: {floor_<2})")
print(f"  -> 7497 Orbiters 202-223/orbit inside [128,256]: {128 <= 202 and 223 <= 256}")

# mean native rate (roster model): 3 planets, moon, 12 haulers (a~U[0.5,8]), 8 orbiters
# (alt=1.15+0.35k+0.2u), 3 skimmers (1.6+1.1k+0.3u Giant radii), player
import random
random.seed(3)
tot = 0.0
for per, e in ((35.6e6, .1), (99.3e6, .02), (500e6, .05)):
    tot += 128 / kep(per * ROOT_M / (1 - e), MSUN)
tot += 128 / P_moon + 128 / P_player
for _ in range(2000):  # monte-carlo the seeded draws
    s = 0.0
    for _ in range(12):
        a = (0.5 + 7.5 * random.random()) * AU_M
        s += 128 / kep(a, MSUN)
    for k in range(8):
        s += 128 / kep((1.15 + 0.35 * k + 0.2 * random.random()) * r_home, m_home)
    for k in range(3):
        s += 128 / kep((1.6 + 1.1 * k + 0.3 * random.random()) * r_giant, m_giant)
    tot += s / 2000
print(f"  -> roster MEAN rate (kappa=128) ~ {tot/28:.2e}/s per native  [a9d7's instrument: 3.55e-5/body/s]")

print()
print("=" * 78)
print("2. THE 10^9 LEDGER (quiet belt, one game-second, rtf 1; budget 4 cores)")
print("=" * 78)
N = 1e9
costs = (("shipped kick 231 us", 231e-6), ("Carlson-priced 30 us", 30e-6), ("floor 50 ns", 50e-9))
rates = (("code-derived, belt at 1-2 AU (kappa=128-256/P)", 128 / kep(AU_M, MSUN), 256 / kep(2 * AU_M, MSUN)),
         ("a9d7 plane instrument 3.55e-5", 3.55e-5, 3.64e-5))
print(f"  {'event-rate bracket':44s} {'231us':>10s} {'30us':>10s} {'50ns':>10s}   (cores)")
for name, lo, hi in rates:
    row = f"  {name:44s}"
    for _, c in costs:
        row += f" {N*lo*c:10.3f}"
    print(row + "   (upper edge of bracket)")
enc_skin, enc_noskin = 0.077 * (N / 1e4), 0.966 * (N / 1e4)
print(f"  ENCOUNTERS  skin on  : {enc_skin:.3e} cores   ({enc_skin/4:.0f}x the 4-core budget)")
print(f"  ENCOUNTERS  no skin  : {enc_noskin:.3e} cores   ({enc_noskin/4:.0f}x)")
kick_lo = N * (128 / kep(2 * AU_M, MSUN)) * 30e-6
kick_hi = N * 3.64e-5 * 30e-6
print(f"  -> encounters / kicks (Carlson, worst-rate bracket) = {enc_skin/kick_hi:.0f}x")
print(f"  MEMORY quiet 21-40 bits/body: {21*N/8/1e9:.2f}-{40*N/8/1e9:.2f} GB of 8;  driven 126 bits: {126*N/8/1e9:.2f} GB")
print(f"  HOT   6.9 KB x N_hot 1.3-2.7e4: {6.9e3*1.3e4/1e6:.0f}-{6.9e3*2.7e4/1e6:.0f} MB;  H_live 21 bits/s: ~0")
print(f"  FRAME tier: deleted by the lazy tier (8b43; 1.35 us flat) - ~0 (gate regression open)")

print()
print("=" * 78)
print("3. THE TWO RAILS (where each scoreboard gap actually lands)")
print("=" * 78)
dens = 0.041            # events/member/game-s in the battle regime (367f)
for nm, c in costs:
    n_max = 1e6 / (dens * c * 1e6)   # 1000 ms/game-s = 25% of 4 cores (790b's convention)
    print(f"  HOT ceiling at {c*1e6:6.1f} us/event: {n_max:.1e} battle members  [790b measured ~2.8e4 at the stack]")
print(f"  COLD encounter wall: N = 4 cores / 7.7e-6 cores/body/s = {4/7.7e-6:.1e} bodies (skin on);"
      f" {4/9.66e-5:.1e} (no skin)")
print(f"  bodies gap decomposition: 10^9 needs the COLD encounter term cut {enc_skin/4:.0f}x more (skin on),")
print(f"  and the HOT rail's kick cost decides only the hot ceiling (2.8e4 -> {1e6/(dens*50e-9*1e6):.0e} at the floor).")

print()
print("=" * 78)
print("4. CHECK-A-CLAIM: 367f/ad26's quiet-belt arithmetic, independently")
print("=" * 78)
print(f"  367f: 1e9 x 3.6e-5 x 231 us = {1e9*3.6e-5*231e-6:.2f} cores  (published ~8.3)  -> agrees")
print(f"  ad26: 1e9 x 3.55e-5 x 30 us = {1e9*3.55e-5*30e-6:.3f} cores  (published 1.08)  -> agrees")
print(f"  Both inherit the a9d7 rate (the plane's mix); at code-derived 2-AU belt rates the same")
print(f"  arithmetic gives {1e9*(128/kep(2*AU_M,MSUN))*231e-6:.2f}-{1e9*(256/kep(2*AU_M,MSUN))*231e-6:.2f} cores (231 us) / {1e9*(256/kep(2*AU_M,MSUN))*30e-6:.3f} cores (30 us).")
