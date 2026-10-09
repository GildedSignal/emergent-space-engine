#!/usr/bin/env python3
"""Distinctions per encounter on the law's integer grid, and the 10^9 ledger.

Units (the repo's own, crates/encounters/src/kepler.rs + law.md): G = M_sun = 1,
length AU, time yr/2pi, so v_circ(a=1) = 1 = 29.78 km/s, 1 time unit = yr/2pi,
2^32 ticks per time unit. The law's element quantum: period in ticks, so
Delta-a/a per tick = (2/3) * (1 tick)/(P ticks) = (2/3)/(2*pi*2^32*a^1.5).
"""
import json, math

TAU = 2 * math.pi
TICK = 2.0 ** 32          # ticks per time unit

def rock_mass_sun(radius_m, rho_gcc=2.5):
    MSUN_KG = 1.989e30
    return 4/3 * math.pi * radius_m**3 * (rho_gcc * 1e3) / MSUN_KG

print("== measured: encounter rate per body per orbit (repo belts, toy density) ==")
runs = [  # (name, n, orbits, truth_enc, rho, sigma_e) from `encounters verify a/b/d`
    ("s1e-3-r1e-4", 1000, 200, 35, 1e-4, 1e-3),
    ("s3e-3-r1e-4", 1000, 100, 68, 1e-4, 3e-3),
    ("s1e-2-r1e-4", 1000, 100, 189, 1e-4, 1e-2),
    ("s3e-2-r1e-4", 1000, 50, 248, 1e-4, 3e-2),
    ("s1e-3-r1e-3", 1000, 100, 236, 1e-3, 1e-3),
    ("s1e-2-r1e-3", 1000, 50, 921, 1e-3, 1e-2),
    ("dense-n3000", 3000, 20, 1042, 3e-4, 1e-2),
    ("hot-s0.1", 500, 50, 1744, 1e-3, 1e-1),
]
for name, n, orb, enc, rho, se in runs:
    print(f"  {name:14s} r_enc={enc/(n*orb):.2e} /body/orbit")

print("\n== the law's quantum ==")
for a in (1.0, 2.7):
    P_ticks = TAU * a**1.5 * TICK
    da_tick = (2/3) * a / P_ticks
    print(f"  a={a}: P={P_ticks:.3e} ticks, one period tick = Delta-a = {da_tick:.3e} AU = {da_tick*1.496e8:.4f} km")

print("\n== deflection per encounter vs the tick quantum ==")
print("  hyperbolic: theta = 2*atan(mu/(q*v^2)), Delta-a/a = (2/3)*theta")
a, sigma_e = 2.7, 0.1                      # main-belt-like
vc = 1/math.sqrt(a)
vrel = sigma_e * vc
q = 1e-4                                   # encounter distance (rho)
masses = {
    "ship 1e6 t": 1e9/1.989e30,
    "rock r=50 m": rock_mass_sun(50),
    "rock r=500 m": rock_mass_sun(500),
    "rock r=5 km": rock_mass_sun(5000),
    "Ceres": 9.4e-10,
}
P_ticks = TAU * a**1.5 * TICK
da_tick = (2/3) * a / P_ticks
for name, m in masses.items():
    mu = 2 * m
    theta = 2 * math.atan(mu / (q * vrel**2))
    da = (2/3) * theta * a
    ticks = da / da_tick
    print(f"  {name:12s} m={m:.2e} Msun  theta={theta:.2e} rad  Delta-a={da:.2e} AU"
          f"  = {ticks:10.1f} period ticks  ({'CROSSES GRID' if ticks >= 1 else 'below grid'})")
m_crit = da_tick * (q * vrel**2) * 3 / (8 * a)   # mu=2m; ticks=1
print(f"  m_crit (1 tick, q=1e-4 AU, sigma=0.1, a=2.7) = {m_crit:.2e} Msun ~ rock r~500 m")

print("\n== game-density belt (3D): encounter rate per body per orbit ==")
N = 1e9
for label, width_au, sigma_i in (("thick (i~0.14rad)", 1.5, 0.14), ("thin (i~0.005)", 1.5, 0.005)):
    vol = TAU * a * width_au * 2 * sigma_i * a
    nvol = N / vol
    per_orbit = nvol * math.pi * q**2 * vrel * TAU * a**1.5
    print(f"  {label}: V={vol:.1f} AU^3, rate = {per_orbit:.2f} encounters/body/orbit (rho=1e-4 AU)")

print("\n== individualization at the tick quantum (only for m > m_crit participants) ==")
for label, per_orbit in (("conservative", 0.05), ("thick-belt rate", 2.77)):
    tau_ind = 1.0 / (2 * per_orbit)   # each encounter touches 2 bodies
    print(f"  {label}: a body individualizes within ~{tau_ind:.1f} orbits of crossing-grid encounters")

print("\n== but at consumer resolution the program belt IS an attractor ==")
da_over_a_rock = (2/3) * 2 * math.atan(2*rock_mass_sun(50)/(q*vrel**2))
for per_orbit in (0.3, 2.0):
    k = (1e-3 / ((3/2)*da_over_a_rock*TAU*math.sqrt(per_orbit)))**2
    print(f"  rock encounters at {per_orbit}/orbit: one pixel (1e-3 rad) of phase noise needs"
          f" k={k:.1e} orbits ~ {k*a**1.5:.1e} yr of game time (never)")

print("\n== the 10^9 ledger on one 8 GB M1 ==")
tube_gib = 16 * 1e9 / 2**30
prog_mib = 0.126 * 1e9 / 8 / 2**20
yr_s = 3.156e7
orbit_s = a**1.5 * yr_s
enc_s = N * 2.77 / orbit_s
rec_s = N * 0.3 / orbit_s          # secular distinct kicks -> recompiles (H0190)
print(f"  storage: tubes 16B x 1e9         = {tube_gib:.1f} GiB  (binding: {tube_gib/8:.1f}x over 8 GiB)")
print(f"  storage: program belt 0.126 bit  = {prog_mib:.0f} MiB   ({8*2**30*8/(0.126*1e9):.0f}x under)")
print(f"  storage: hybrid, 1e8 tubes + rest program = {(1e8*16)/2**30:.1f} GiB + {prog_mib:.0f} MiB (fits, ~5x headroom)")
print(f"  events : all encounters ~ {enc_s:.0f} exact pair events/s at 1x; x100 RTF at 10 us/event"
      f" = {100*enc_s*1e-5*100:.1f}% of one core")
print(f"           secular recompiles ~ {rec_s:.0f}/s at 1x; x100 RTF at 10 us = {100*rec_s*1e-5*100:.1f}% of one core")
print(f"  bandwidth: full 16 GiB sweep at 60 GB/s = {16/60:.2f} s (16x over one 16.7 ms frame;"
      f" event-driven touches ~{100*enc_s:.0f} bodies/s ~ {100*enc_s*32/1e3:.0f} KB/s)")
json.dump({n: e/(nn*o) for n, nn, o, e, _, _ in runs}, open("rate.json", "w"), indent=1)
