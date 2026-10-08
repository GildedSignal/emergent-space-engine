# v2 harness: author's toy with three corrections (vr branch, om:=0 at e<thresh,
# true 2*pi cadence/orbits). Vectorized over phases.
import math, numpy as np
MU_S = 1.0e-3; R = 1.0; R_HILL = R*(MU_S/3.0)**(1.0/3.0)

def ecc_vec(X, Y, VX, VY):
    r = np.hypot(X, Y); v2 = VX*VX+VY*VY; rv = X*VX+Y*VY
    return (v2-1.0/r)*X - rv*VX, (v2-1.0/r)*Y - rv*VY

def kepler_v2(X, Y, VX, VY, dt, broken=False):
    EX, EY = ecc_vec(X, Y, VX, VY)
    E = np.hypot(EX, EY)
    A = 1.0/(2.0/np.hypot(X, Y)-(VX*VX+VY*VY))
    if np.any(A <= 0): raise ValueError("unbound")
    n = A**-1.5
    r = np.hypot(X, Y)
    cosf = np.where(E > 1e-14, (EX*X+EY*Y)/np.maximum(E*r, 1e-300), X/r)
    cosf = np.clip(cosf, -1.0, 1.0)
    f0 = np.arccos(cosf)
    f0 = np.where(X*VX+Y*VY < 0, 2*np.pi-f0, f0)
    E0 = 2*np.arctan2(np.sqrt(1-E)*np.sin(f0/2), np.sqrt(1+E)*np.cos(f0/2))
    M0 = E0 - E*np.sin(E0)
    M1 = (M0 + n*dt + np.pi) % (2*np.pi) - np.pi
    Ei = np.where(E < 0.8, M1, np.pi).copy()
    for _ in range(60):
        d = (Ei - E*np.sin(Ei) - M1)/(1 - E*np.cos(Ei)); Ei -= d
        if np.max(np.abs(d)) < 1e-15: break
    f1 = 2*np.arctan2(np.sqrt(1+E)*np.sin(Ei/2), np.sqrt(1-E)*np.cos(Ei/2))
    p = A*(1-E*E); r1 = p/(1+E*np.cos(f1))
    v2 = 2.0/r1 - 1.0/A; hdot = np.sqrt(p)
    vr = np.sqrt(np.maximum(0.0, v2 - hdot*hdot/(r1*r1)))
    if broken: vr = np.where(f1 > np.pi, -vr, vr)
    else:      vr = np.where((f1 < 0) | (f1 > np.pi), -vr, vr)
    vt = hdot/r1
    om = np.where(E > 1e-14, np.arctan2(EY, EX), 0.0)   # v2: no noise rotation
    px, py = r1*np.cos(f1), r1*np.sin(f1)
    x1 = px*np.cos(om)-py*np.sin(om); y1 = px*np.sin(om)+py*np.cos(om)
    vpx, vpy = vr*np.cos(f1)-vt*np.sin(f1), vr*np.sin(f1)+vt*np.cos(f1)
    return x1, y1, vpx*np.cos(om)-vpy*np.sin(om), vpx*np.sin(om)+vpy*np.cos(om)

def tide_v(X, Y, t, PHI):
    th = t + PHI
    sx, sy = R*np.cos(th), R*np.sin(th)
    dx, dy = sx-X, sy-Y; d3 = (dx*dx+dy*dy)**1.5
    return MU_S*(dx/d3 - sx/R**3), MU_S*(dy/d3 - sy/R**3)

def accel_v(X, Y, t, PHI):
    r3 = (X*X+Y*Y)**1.5; tx, ty = tide_v(X, Y, t, PHI)
    return -X/r3+tx, -Y/r3+ty

def kicked_v2(a_moon, K, n_orb, PHI, broken=False):
    PHI = np.asarray(PHI, dtype=float)
    X = np.full(PHI.shape, a_moon); Y = np.zeros_like(PHI)
    VX = np.zeros_like(PHI); VY = np.full(PHI.shape, 1.0/math.sqrt(a_moon))
    dt = 2*math.pi*a_moon**1.5/K; t = 0.0
    ex0, ey0 = ecc_vec(X, Y, VX, VY); om0 = np.arctan2(ey0, ex0)
    for _ in range(n_orb*K):
        X, Y, VX, VY = kepler_v2(X, Y, VX, VY, dt, broken)
        ax, ay = tide_v(X, Y, t+dt, PHI)
        VX += ax*dt; VY += ay*dt; t += dt
    ex1, ey1 = ecc_vec(X, Y, VX, VY)
    return (np.arctan2(ey1, ex1)-om0) % (2*np.pi)/n_orb

def truth_v2(a_moon, n_orb, PHI, steps_per_orb=4000):
    PHI = np.asarray(PHI, dtype=float)
    T = n_orb*2*math.pi*a_moon**1.5
    X = np.full(PHI.shape, a_moon); Y = np.zeros_like(PHI)
    VX = np.zeros_like(PHI); VY = np.full(PHI.shape, 1.0/math.sqrt(a_moon))
    ex0, ey0 = ecc_vec(X, Y, VX, VY); om0 = np.arctan2(ey0, ex0)
    h = T/(n_orb*steps_per_orb); t = 0.0
    for _ in range(n_orb*steps_per_orb):
        ax1, ay1 = accel_v(X, Y, t, PHI)
        x2, y2, vx2, vy2 = X+VX*h/2, Y+VY*h/2, VX+ax1*h/2, VY+ay1*h/2
        ax2, ay2 = accel_v(x2, y2, t+h/2, PHI)
        x3, y3, vx3, vy3 = X+vx2*h/2, Y+vy2*h/2, VX+ax2*h/2, VY+ay2*h/2
        ax3, ay3 = accel_v(x3, y3, t+h/2, PHI)
        x4, y4, vx4, vy4 = X+vx3*h, Y+vy3*h, VX+ax3*h, VY+ay3*h
        ax4, ay4 = accel_v(x4, y4, t+h, PHI)
        X = X + h*(VX+2*vx2+2*vx3+vx4)/6.0; Y = Y + h*(VY+2*vy2+2*vy3+vy4)/6.0
        VX = VX + h*(ax1+2*ax2+2*ax3+ax4)/6.0; VY = VY + h*(ay1+2*ay2+2*ay3+ay4)/6.0
        t += h
    ex1, ey1 = ecc_vec(X, Y, VX, VY)
    return (np.arctan2(ey1, ex1)-om0) % (2*np.pi)/n_orb
