#!/usr/bin/env python3
"""Probe: why is O3 (exact for a cubic) not at the floor? Run oracle-vs-oracle
(identical arms, only float paths differ in no way) and O3 with reconstruction
error tracked."""
import math

def make(beta, a0, jerk):
    r0 = 1.0/beta**2; v0 = beta; P = 2.0*math.pi/beta**3
    def src(t):
        return ((0.5*a0*t*t + jerk*t*t*t/6.0, 0.0),
                (a0*t + 0.5*jerk*t*t, 0.0), (a0 + jerk*t, 0.0))
    return r0, v0, P, src

def probe(beta, a0, jerk, T_frac=1/64.0, order=3, twin=False):
    r0, v0, P, src = make(beta, a0, jerk)
    T = T_frac*P; h = P/1024.0; n = 1024
    def retarded_t(t, xc):
        tr = t - math.hypot(xc[0], xc[1])
        for _ in range(6):
            xs, _, _ = src(tr)
            tr = t - math.hypot(xc[0]-xs[0], xc[1]-xs[1])
        return tr
    maxerr_x = 0.0; maxerr_v = 0.0
    def field(t, xc, mode):
        nonlocal maxerr_x, maxerr_v
        tr = retarded_t(t, xc)
        if mode == "oracle":
            xr, vr, _ = src(tr)
        else:
            tv = T*math.floor(tr/T); d = tr - tv
            xv, vv, av = src(tv)
            xr = (xv[0]+vv[0]*d+0.5*av[0]*d*d + jerk*d*d*d/6.0, xv[1]+vv[1]*d)
            vr = (vv[0]+av[0]*d+0.5*jerk*d*d, vv[1])
            xt, vt, _ = src(tr)
            maxerr_x = max(maxerr_x, abs(xr[0]-xt[0]))
            maxerr_v = max(maxerr_v, abs(vr[0]-vt[0]))
        R = math.hypot(xc[0]-xr[0], xc[1]-xr[1])
        nx, ny = (xc[0]-xr[0])/R, (xc[1]-xr[1])/R
        v2 = vr[0]*vr[0]+vr[1]*vr[1]
        g = 1.0/math.sqrt(1.0-v2); ndv = nx*vr[0]+ny*vr[1]
        rinv = g*R*(1.0-ndv); c = g/(rinv*rinv); k = (1.0-v2)/(1.0-ndv)
        return (c*(vr[0]-k*nx), c*(vr[1]-k*ny))
    def deriv(t, s, m):
        f = field(t, (s[0], s[1]), m); return (s[2], s[3], f[0], f[1])
    def rk4(s, t, m):
        k1 = deriv(t, s, m)
        s2 = [s[i]+0.5*h*k1[i] for i in range(4)]; k2 = deriv(t+0.5*h, s2, m)
        s3 = [s[i]+0.5*h*k2[i] for i in range(4)]; k3 = deriv(t+0.5*h, s3, m)
        s4 = [s[i]+h*k3[i] for i in range(4)];     k4 = deriv(t+h, s4, m)
        return [s[i]+h/6.0*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(4)]
    def energy(t, s):
        xs, _, _ = src(t)
        return 0.5*(s[2]**2+s[3]**2) - 1.0/math.hypot(s[0]-xs[0], s[1]-xs[1])
    s1 = [r0, 0.0, 0.0, v0]; s2 = [r0, 0.0, 0.0, v0]
    marks = []
    for i in range(n):
        t = i*h
        s1 = rk4(s1, t, "oracle")
        s2 = rk4(s2, t, "oracle" if twin else "pay")
        if (i+1) % 16 == 0:
            marks.append(energy(t+h, s2)-energy(t+h, s1))
    half = marks[len(marks)//2:]
    growth = [abs(half[i+1]-half[i]) for i in range(len(half)-1)]
    pr = sum(growth)/len(growth) if growth else 0.0
    return pr, maxerr_x, maxerr_v, max(abs(m) for m in marks)

beta = 0.03; P = 2.0*math.pi/beta**3; v0 = beta
A0 = 0.01*v0/P; J0 = A0*4.0/P
print("twin (oracle vs oracle), case C jerk: ", probe(beta, 0.0, J0, twin=True))
print("O3 vs oracle,       case C jerk:      ", probe(beta, 0.0, J0, order=3))
print("O3 vs oracle,       case A no jerk:   ", probe(beta, A0, 0.0, order=3))
print("O2 vs oracle,       case C jerk:      ", probe(beta, 0.0, J0, order=2))
