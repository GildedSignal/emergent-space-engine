#!/usr/bin/env python3
"""Pilot: does check A's mpmath error fall like nsteps^-4 (RK4 truncation)?
Runs the two hardest families at nsteps in (1500, 3000, 6000). Not part of the
reference; used only to set verify v2's A tolerance from a measured instrument
floor, before the decisive run."""
import sys, time
sys.path.insert(0, "..")
import numpy as np
from mpmath import mp, mpf
mp.dps = 40
src = open("../verify.py").read().split("# ---------------------------------------------------------------- run")[0]
exec(compile(src, "verify-pre.py", "exec"))  # defines mp_transport, mp_angle, FAMILIES
st = __import__("schwarztide")

M = 1.0

cases = list(FAMILIES)

for (name, E, L, r0, s, tag) in cases:
    tau = 2*np.pi*r0**1.5/8.0
    row = []
    for ns in (1500, 3000):
        t0 = time.time()
        r1, ph1, s1, fr = mp_transport(E, L, r0, s, tau, nsteps=ns)
        Phi = float(mp_angle(E, L, r1, s1, fr))
        u = st.u_of(E, L, r1, M, s1)
        frn = [np.array([float(x) for x in v]) for v in fr]
        Cd = st.C_from_frame(M, r1, u, frn)
        Cp = st.tide_parallel(M, E, L, r1, Phi, s1)
        errA = np.max(np.abs(Cd - Cp))/max(np.max(np.abs(Cp)), 1e-30)
        # omega: central difference with window transport scaled too
        h = 1e-3
        rA, _, sA, frA = mp_transport(E, L, r0, s, -h, nsteps=ns//10)
        rB, _, sB, frB = mp_transport(E, L, r0, s, +h, nsteps=ns//10)
        wnum = float((mp_angle(E, L, rB, sB, frB) - mp_angle(E, L, rA, sA, frA))/(2*h))
        wcl = -st.omega(M, E, L, r0)
        errW = abs(wnum - wcl)/max(abs(wcl), 1e-30)
        row.append((ns, float(errA), float(errW), time.time()-t0))
    print("%-22s" % (name+"/"+tag), end="")
    for (ns, eA, eW, dt) in row:
        print("  n=%5d errA=%.2e errW=%.2e (%.0fs)" % (ns, eA, eW, dt), end="")
    if len(row) > 1 and row[1][1] > 0:
        print("   ratio A: %.3f" % (row[1][1]/row[0][1]), end="")
    print()
