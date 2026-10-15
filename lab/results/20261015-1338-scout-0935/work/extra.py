#!/usr/bin/env python3
"""Beta scan (burn vs free fall), jerk family, RX completeness, burn scaling."""
import numpy as np, json, news_strong as ns

def rho(v0, aburn, jerk, t, r, phase=0.7):
    src = ns.Source(np.array([v0,0.0,0.0]), a_burn=aburn, jerk=jerk)
    x = r*np.array([np.cos(phase), np.sin(phase), 0.0])
    G = ns.gamma_fd(src, t, x); a_ex = -G[1:4,0,0]; A = ns.arms(src, t, x)
    Ga = ns.gamma_analytic(src, t, x)
    rx = -Ga[1:4,0,0]
    return (float(np.linalg.norm(A['R2b']-a_ex)/np.linalg.norm(a_ex)),
            float(np.linalg.norm(rx-a_ex)/np.linalg.norm(a_ex)),
            float(np.linalg.norm(A['R0']-a_ex)/np.linalg.norm(a_ex)))

gentle20 = 0.10*np.sqrt(1/20)/(0.25*2*np.pi*20**1.5)
out={"beta_scan":[], "burn_scaling":[], "jerk_scaling":[], "rx":[]}
for beta in (0.003,0.03,0.1,0.2,0.3,0.4,0.5):
    ff = [rho(beta,0,0,300.0,20.0,phase=p) for p in (0.0,1.0)]
    bu = [rho(beta,gentle20,0,300.0,20.0,phase=p) for p in (0.0,1.0)]
    out["beta_scan"].append(dict(beta=beta, ff=np.median([q[0] for q in ff]), burn=np.median([q[0] for q in bu])))
    print(f"beta={beta:5.3f} ff={out['beta_scan'][-1]['ff']:.3e} burn={out['beta_scan'][-1]['burn']:.3e} law1.4b2={1.4*beta**2:.3e}")
for r in (50.0, 20.0, 12.0):
    for k in (0.25, 1.0, 4.0):
        a = k*0.10*np.sqrt(1/r)/(0.25*2*np.pi*r**1.5)
        r2b, rx, r0 = rho(0.003, a, 0, min(300, 0.2/a), r)
        out["burn_scaling"].append(dict(r=r, k=k, a=a, r2b=r2b, r0=r0, rx=rx))
        print(f"r={r:5.1f} a={a:.2e}: rho(R2b)={r2b:.3e} rho(RX)={rx:.1e}")
for jk in (gentle20/160, gentle20/40, gentle20/10):
    r2b, rx, r0 = rho(0.1, gentle20, jk, min(120, np.sqrt(2*0.1/jk)), 20.0)
    out["jerk_scaling"].append(dict(j=jk, r2b=r2b, rx=rx))
    print(f"j={jk:.2e}: rho(R2b)={r2b:.3e} rho(RX)={rx:.1e}")
for (v0,ab,r,t) in ((0.3,0,200.0,300.),(0.3,gentle20,20.0,300.),(0.1,gentle20*4,12.0,300.),(0.5,0,50.0,300.)):
    _, rx, _ = rho(v0,ab,0,t,r)
    out["rx"].append(dict(v0=v0,a=ab,r=r,rx=rx))
    print(f"RX beta={v0} r={r}: {rx:.2e}")
json.dump(out, open("scaling.json","w"), indent=1)
