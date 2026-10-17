#!/usr/bin/env python3
"""The 10^9 encounters ledger on the MEASURED live word (run 20261017-0839-fermi-2b89).

Every constant below is either measured by enc_quantum.rs on shipped code (marked M)
or standard SI. Floats price orders of magnitude; the anchor itself (ev = -73, the
word's exponent) is an integer read off the shipped binding.
"""
import math

C = 299_792_458.0
AU_M = 149_597_870_700.0
RHO = 3000.0            # kg/m^3 rock density
G = 6.674e-11
AREA = math.pi * (9 - 4) * AU_M**2     # the [2,3) AU annulus: 3.52e23 m^2

# ---- measured anchors (enc_quantum.rs, shipped path, seed 1, N=3000) ----
EV = -73                # (M) belt binding velocity exponent: quantum = 2^-73 c
EL = -32                # (M) belt binding length exponent
KICK_QUANTA = 2**35.0   # (M) the belt's own metronome kick (2^-23 of speed) in quanta
Q_SI = 2.0**EV * C      # (M) the live velocity quantum, m/s

def mu(d_m):            # G m of a rock of diameter d_m
    return G * (math.pi / 6.0) * RHO * d_m**3

def dstar(b_m, vrel, ev=EV):
    """Partner diameter whose conjunction impulse is exactly 1 quantum at (b, v_rel)."""
    q = 2.0**ev * C
    m_min = (q * b_m * vrel / 2.0) / G
    return (6.0 * m_min / (math.pi * RHO)) ** (1 / 3.0)

def bflip(d_m, vrel, ev=EV):
    q = 2.0**ev * C
    return 2.0 * mu(d_m) / (q * vrel)

print(f"live quantum 2^{EV} c = {Q_SI:.3e} m/s (measured); belt kick = 2^{math.log2(KICK_QUANTA):.0f} quanta")
print(f"legacy E-key anchor equivalent (f0a2: 319.3 m^2/s^2 at v~1.9e4 m/s): "
      f"{319.3/ (2*1.9e4):.2e} m/s = 2^{math.log2(319.3/(2*1.9e4)/C):.1f} c "
      f"= 2^{math.log2(319.3/(2*1.9e4)/Q_SI):.1f} live quanta")

print("\nD* (partner that flips 1 quantum) at the live word:")
for b, vr in [(1e5, 1e3), (1e6, 1e3), (1e5, 30.0)]:
    print(f"  b={b:8.0e} v_rel={vr:5.0f}: D* = {dstar(b, vr):7.2f} m")

print("\nThe two-threshold ladder (measured): word fires at 1 quantum; the compiled KEY mints from 2^12 quanta (dv/v ~ 2^-47):")
for b, vr in [(1e5, 1e3), (1e6, 1e3), (1e5, 30.0), (1e7, 1e3)]:
    q_key = 2.0**-61 * C
    m_key = (q_key * b * vr / 2.0) / G
    d_key = (6.0 * m_key / (math.pi * RHO)) ** (1 / 3.0)
    print(f"  b={b:8.0e} v_rel={vr:5.0f}: D*_word={dstar(b, vr):6.2f} m, D*_key(mint)={d_key:8.1f} m")

print("\nThe word-width dial (what coarsening the velocity word does; kick stays >= 2^7 quanta until ev = -45):")
for ev in [-73, -68, -64, -58, -45]:
    dq = 2.0**(ev - EV)  # quanta still in one belt kick
    print(f"  ev={ev}: D*(1e5,1e3) = {dstar(1e5,1e3,ev):9.1f} m; belt kick = 2^{math.log2(KICK_QUANTA)- (EV-ev):.0f} quanta")

print("\nFlip reach at the live word (every crossing pair inside this b fires):")
for d, vr in [(49.0, 30.0), (70.0, 1e3), (470e3, 1e3)]:
    bf = bflip(d, vr)
    print(f"  D={d:8.0f} m v_rel={vr:5.0f}: b_flip = {bf:.2e} m = {min(bf/AU_M, 1e9):.4f} AU")

print("\nConjunction + rebind price at 10^9 on the live word (per-pair handling, the dead branch):")
SIGMA = 1e9 / AREA
for b, vr in [(1e5, 1e3), (bflip(70.0, 1e3), 1e3)]:
    rate = SIGMA * 2 * b * vr          # per body /s
    events = rate * 1e9 / 2
    print(f"  b<{b:.1e} m v_rel={vr:.0f}: {rate:.3g}/s/body -> {events:.3g} pair-events/s"
          f" -> {events*4e-6:.3g} cores at 4us find, {events*50e-6:.3g} cores if each rebinds (50us)")

print("\nThe aggregate flux (what MUST be delivered somehow), Dohnanyi [70 m, 470 km], N=1e9:")
# dN/dD = C0 D^-3.5, mass integral dominated by the top
C0 = 1e9 * 2.5 * 70.0**2.5       # dN/dD = C0 D^-3.5 normalized by N_total = (C0/2.5)*D_min^-2.5
mass = (math.pi/6)*RHO * C0 * 2 * (math.sqrt(470e3) - math.sqrt(70.0))
mu_tot = G * mass
sigma_mu = mu_tot / AREA
flux = 4 * sigma_mu                     # m/s per s per body (2-D gas, weak deflection, b-independent)
print(f"  belt mass {mass:.2e} kg, mu_tot {mu_tot:.2e} m^3/s^2, flux {flux:.2e} m/s per s per body")
for ev in [-73, -64, -45]:
    q = 2.0**ev * C
    per_interval = flux * 28141.5
    print(f"  ev={ev}: {per_interval:.2e} m/s per 28141.5-s interval = {per_interval/q:.3g} quanta/body/interval"
          f" -> {'rides the kick stream (2 events/body/interval)' if per_interval/q >= 1 else 'sub-quantum: fires every ' + format((q/per_interval), '.0f') + ' intervals'}")

print("\nFlown-plane cross-check (N=2700 belt ships of 49 m): mutual conjunction rate per body at v_rel=30:")
for n in [2700, 1e6, 1e9]:
    s = n / AREA
    bf = bflip(49.0, 30.0)
    rate = s * 2 * bf * 30.0
    print(f"  N={n:9.0f}: {rate:.2e}/s/body -> one per {1/rate/3.15e7 if rate>0 else float('inf'):.1e} yr/body; fleet {rate*n/2:.2e}/s")
