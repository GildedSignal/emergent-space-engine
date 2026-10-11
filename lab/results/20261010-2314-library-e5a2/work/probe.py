"""Pay-on-crossing cadence probe (library lens, 20261010-2314).

CR3BP toy: star(1) + Jupiter(1e-3, a=5.2, circular) + massless belt, heliocentric
with indirect term, leapfrog dt=P_p/300, T=200 P_p. Per body, orbit-averaged
osculating a at each of its own orbits; residue vs linear fit; S=cumsum.
Growth class gamma; deferral D(Q) = orbits until |S|>Q*a0.
"""
import numpy as np, json

rng = np.random.default_rng(42)
M_P, A_P = 1e-3, 5.2
P_P = 2*np.pi*A_P**1.5                      # Jupiter period (time units)
DT, T = P_P/300.0, 200.0*P_P
NSTORE = 3                                   # store every 3rd step
N = 240
a0 = rng.uniform(2.0, 3.6, N)
e0 = np.where(np.arange(N) % 2 == 0, 0.05, 0.20)   # half mild, half adversarial
w0, M0 = rng.uniform(0, 2*np.pi, N), rng.uniform(0, 2*np.pi, N)

# start at random mean anomaly: position on ellipse
def elements_to_state(a, e, w, M):
    E = M.copy()
    for _ in range(60):
        E -= (E - e*np.sin(E) - M)/(1 - e*np.cos(E))
    c, s = np.cos(E), np.sin(E)
    n = a**-1.5
    den = 1 - e*c
    x0, y0 = a*(c - e), a*(1-e**2)**0.5*s
    vx0, vy0 = -a*n*s/den, a*(1-e**2)**0.5*n*c/den
    cw, sw = np.cos(w), np.sin(w)
    return (x0*cw - y0*sw, x0*sw + y0*cw, vx0*cw - vy0*sw, vx0*sw + vy0*cw)

X, Y, VX, VY = elements_to_state(a0, e0, w0, M0)
nsteps = int(T/DT)
store_idx = np.arange(0, nsteps, NSTORE)
a_store = np.empty((len(store_idx), N))
t_store = store_idx*DT

def accel(x, y, t):
    om = 1.0/A_P**1.5
    xp, yp = A_P*np.cos(t*om), A_P*np.sin(t*om)
    dx, dy = x - xp, y - yp
    r3 = (x*x + y*y)**-1.5
    d3 = (dx*dx + dy*dy)**-1.5
    pr3 = (xp*xp + yp*yp)**-1.5
    ax = -r3*x - M_P*(d3*dx - pr3*xp)   # direct + indirect
    ay = -r3*y - M_P*(d3*dy - pr3*yp)
    return ax, ay

si = 0
for i in range(nsteps):
    t = (i + 0.5)*DT
    ax, ay = accel(X, Y, t)
    VX += ax*DT; VY += ay*DT
    X += VX*DT; Y += VY*DT
    if i % NSTORE == 0:
        r = np.hypot(X, Y); v2 = VX*VX + VY*VY
        a_store[si] = 1.0/(2.0/r - v2); si += 1

# per body: orbit-window means, residue vs linear fit, S, gamma, D(Q)
P_body = 2*np.pi*a0**1.5
rows = []
res_lattice = {f"{p}:{q}": A_P*(q/p)**(2/3) for p, q in [(2,1),(3,1),(5,2),(7,3),(8,3),(5,3),(3,2),(4,3)] if 2.0 < A_P*(q/p)**(2/3) < 3.6}
Qs = [1e-5, 1e-4]
for j in range(N):
    per = P_body[j]
    m_max = int((t_store[-1] - 0.6*per)//per)
    means = []
    for m in range(1, m_max+1):
        i0 = np.searchsorted(t_store, (m-1)*per + 0.3*per)
        i1 = np.searchsorted(t_store, m*per + 0.3*per)
        means.append(a_store[i0:i1, j].mean())
    mm = np.array(means); t_orb = np.arange(1, len(mm)+1)*per
    # drop first 5 orbits (relaxation of initial conditions)
    keep = slice(5, None)
    mm2, t2 = mm[keep], t_orb[keep]
    A_ = np.polyfit(t2, mm2, 1)
    r = mm2 - np.polyval(A_, t2)
    S = np.cumsum(r)/per                    # accumulated residue, in AU-equivalent per orbit time
    # gamma: dyadic window max of |S|
    M_ = len(S); gammas = []
    k = 4
    while 2*k <= M_:
        w1 = np.abs(S[k:2*k]).max(); w0_ = np.abs(S[:k]).max()
        gammas.append(np.log2(max(w1,1e-15)/max(w0_,1e-15)))
        k *= 2
    gamma = float(np.mean(gammas[-3:])) if gammas else np.nan
    dres = min(abs(a0[j]-v) for v in res_lattice.values())
    near = dres < 0.04
    D = {}
    for Q in Qs:
        hit = np.nonzero(np.abs(S) > Q*a0[j])[0]
        D[Q] = int(hit[0])+1 if len(hit) else -1   # -1 = never crossed (censored)
    rows.append(dict(a=a0[j], e=e0[j], near=bool(near), dres=float(dres),
                     n_orbits=M_, gamma=gamma, amp=float(np.abs(r).max()),
                     D={str(q): d for q, d in D.items()}))

far = [r_ for r_ in rows if not r_["near"]]
near_ = [r_ for r_ in rows if r_["near"]]
def med(x): return float(np.median(x)) if x else float("nan")
summary = dict(
    n_far=len(far), n_near=len(near_),
    frac_near=round(len(near_)/N, 3),
    gamma_far_med=med([r_["gamma"] for r_ in far]),
    gamma_near_med=med([r_["gamma"] for r_ in near_]),
    D_far_med={q: med([r_["D"][q] if r_["D"][q]>0 else r_["n_orbits"] for r_ in far]) for q in map(str,Qs)},
    D_far_cens_frac={q: round(sum(1 for r_ in far if r_["D"][q]<0)/max(len(far),1),3) for q in map(str,Qs)},
    D_near_med={q: med([r_["D"][q] if r_["D"][q]>0 else r_["n_orbits"] for r_ in near_]) for q in map(str,Qs)},
    D_far_e05={q: med([r_["D"][q] if r_["D"][q]>0 else r_["n_orbits"] for r_ in far if r_["e"]<0.1]) for q in map(str,Qs)},
    D_far_e20={q: med([r_["D"][q] if r_["D"][q]>0 else r_["n_orbits"] for r_ in far if r_["e"]>0.1]) for q in map(str,Qs)},
    gamma_far_e20_med=med([r_["gamma"] for r_ in far if r_["e"]>0.1]),
    orbits_median_far=med([r_["n_orbits"] for r_ in far]),
)
json.dump(dict(summary=summary, rows=rows), open("probe_out.json","w"), indent=1)
print(json.dumps(summary, indent=1))
