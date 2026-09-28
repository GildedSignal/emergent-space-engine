#!/usr/bin/env python3
# Premise probe K5 (GLM, 28 Sep 2026): planet at 1 AU around the dominant star of a
# near-equal binary (mass ratio m2/m1 = 0.8, total 1 solar mass, separation 3 AU).
# Formula: Kepler circle about star 1. Unknown: star 2 tide (exact, star-1 frame).
# The impulse amplitude is ~1e7 dv, so the quantum is scaled up by a factor s and the
# crossing count is multiplied back by s (crossings scale ~ 1/dv when amplitude >> dv).
# Validated at two scales.
import math, time, os

G = 6.6743e-11; MTOT = 1.989e30
m1 = MTOT/1.8; m2 = 0.8*m1
GM1 = G*m1; GM2 = G*m2
AB = 3.0*1.495978707e11; RP = 1.495978707e11
n1 = math.sqrt(GM1/RP**3); P = 2.0*math.pi/n1
nb = math.sqrt((GM1+GM2)/AB**3)
DV = 2.7e-4
PB = 2.0*math.pi/nb

def tide2(x, y, t):
    c = math.cos(nb*t); s = math.sin(nb*t)
    mx = AB*c-x; my = AB*s-y
    d2 = mx*mx+my*my; dd = d2*math.sqrt(d2)
    return GM2*(mx/dd - c/(AB*AB)), GM2*(my/dd - s/(AB*AB))

def run(scale, orb=3, spb=8192):
    dve = DV*scale; dt = P/spb
    Ix = Iy = 0.0; lx = ly = 0; kicks = 0
    for step in range(orb*spb):
        tm = (step+0.5)*dt
        th = n1*tm
        x = RP*math.cos(th); y = RP*math.sin(th)
        ax, ay = tide2(x, y, tm)
        Ix += ax*dt; Iy += ay*dt
        nx = math.floor(Ix/dve+0.5); ny = math.floor(Iy/dve+0.5)
        kicks += abs(nx-lx) + abs(ny-ly); lx, ly = nx, ny
    return kicks/orb

print(f"K5: m1={m1:.3e} kg m2={m2:.3e} kg (ratio {m2/m1:.2f}), a_bin=3 AU, r_planet=1 AU")
print(f"K5: P_planet={P/86400.0:.0f} d, P_binary={PB/86400.0:.0f} d, dv={DV:.1e} m/s")
t0 = time.time()
r3 = run(3.0e4); r1 = run(1.0e5)
wall = time.time() - t0
print(f"K5: scale 3.0e4 -> {r3:.1f} crosses/orbit -> {r3*3.0e4:.2e} kicks/orbit")
print(f"K5: scale 1.0e5 -> {r1:.1f} crosses/orbit -> {r1*1.0e5:.2e} kicks/orbit")
print(f"K5: kicks/orbit ~ 1e{0.5*(math.log10(r3*3.0e4)+math.log10(r1*1.0e5)):.1f} (threshold 1e3 = binaries need a two-body parent)")
print(f"K5: kick rate = {r1*1.0e5/P:.2e} /s/body; wall={wall:.1f}s load={os.getloadavg()[0]:.2f}")
