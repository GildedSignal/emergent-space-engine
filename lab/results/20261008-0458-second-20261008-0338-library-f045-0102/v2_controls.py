# Controls for v2: (a) omega conserved in pure drift, generic + circular starts;
# (b) K=1 full-orbit roundtrip from circular start; (c) vec vs scalar domega agreement.
import numpy as np, math
from v2 import kepler_v2, ecc_vec, kicked_v2, truth_v2, R_HILL
# (a) generic e=1e-3 start
a = 0.0173; e_inj = 1e-3; f = 1.2
p = a*(1-e_inj**2); r = p/(1+e_inj*math.cos(f))
v = math.sqrt(2.0/r - 1.0/a); h = math.sqrt(p)
vr = math.sqrt(max(0.0, v*v-h*h/(r*r))); vt = h/r
X = np.array([r*math.cos(f)]); Y = np.array([r*math.sin(f)])
VX = np.array([vr*math.cos(f)-vt*math.sin(f)]); VY = np.array([vr*math.sin(f)+vt*math.cos(f)])
ex0, ey0 = ecc_vec(X, Y, VX, VY); om0 = math.atan2(ey0[0], ex0[0]); worst = 0.0
dt = 2*math.pi*a**1.5/16
for i in range(300*16):
    X, Y, VX, VY = kepler_v2(X, Y, VX, VY, dt)
    ex1, ey1 = ecc_vec(X, Y, VX, VY)
    worst = max(worst, abs((math.atan2(ey1[0], ex1[0])-om0+math.pi) % (2*math.pi)-math.pi))
print(f"(a) v2 pure drift, e=1e-3: worst |dw| over 4800 steps = {worst:.3e} rad")
# (b) circular start, K=1 (dt = full period): must return to start
X = np.array([a]); Y = np.array([0.0]); VX = np.array([0.0]); VY = np.array([1.0/math.sqrt(a)])
X1, Y1, VX1, VY1 = kepler_v2(X, Y, VX, VY, 2*math.pi*a**1.5)
err = math.hypot(X1[0]-a, Y1[0]-0.0)/a + math.hypot(VX1[0]-0.0, VY1[0]-1/math.sqrt(a))*math.sqrt(a)
print(f"(b) v2 full-orbit roundtrip from circular start: rel err = {err:.3e}")
# (c) vec-vs-scalar domega agreement (scalar via broken=False single-element calls = same code path)
for phi in (0.0, math.pi/2, math.pi):
    P = np.array([phi]); am = 0.25*R_HILL
    w16 = kicked_v2(am, 16, 300, P)[0]; w1 = kicked_v2(am, 1, 300, P)[0]
    print(f"(c) phi={phi/math.pi:.2f}pi v2 domega K=16: {w16:.9e}  K=1: {w1:.9e}")
