# P1 control: pure two-body drift (no tide), e = 1e-3 injected, 300 orbits, K = 16.
# omega must stay constant. Original vs fixed.
import math
from probe2_common import kepler_core, ecc_vec
a = 0.0173; e_inj = 1e-3
# start at f = 1.2 rad (generic): periapsis speed scaled
p = a*(1-e_inj**2); r = p/(1+e_inj*math.cos(1.2))
v = math.sqrt(2.0/r - 1.0/a); h = math.sqrt(p)
vr = math.sqrt(max(0.0, v*v-h*h/(r*r))); vt = h/r
f = 1.2
x0, y0 = r*math.cos(f), r*math.sin(f)
vx0, vy0 = vr*math.cos(f)-vt*math.sin(f), vr*math.sin(f)+vt*math.cos(f)
dt = a**1.5/16
for fixed in (False, True):
    x, y, vx, vy = x0, y0, vx0, vy0
    ex0, ey0 = ecc_vec(x, y, vx, vy); om0 = math.atan2(ey0, ex0)
    dom_worst = 0.0
    for i in range(300*16):
        x, y, vx, vy = kepler_core(x, y, vx, vy, dt, fixed)
        ex1, ey1 = ecc_vec(x, y, vx, vy)
        d = abs((math.atan2(ey1, ex1)-om0+math.pi) % (2*math.pi)-math.pi)
        dom_worst = max(dom_worst, d)
    print(f"fixed={fixed}: worst |omega drift| over 4800 steps = {dom_worst:.3e} rad")
