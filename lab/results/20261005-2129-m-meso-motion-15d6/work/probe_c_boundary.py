"""Decisive probe: the conjunction event's domain boundary.

Shared initial states: at t=0 the ship sits d0 from the planet (Hill-zone
entrance) with synodic velocity V0 (|V0| = U, direction randomized in the
synodic plane).  Truth: DOP853 restricted problem.  Law: Sun-only drift +
ONE exact event (Strang: drift w, pair 2w, drift w) + first-order tail
moments outside the window.  Negative control: straight-line impulse.

Sweep: d0 in {0.5, 1, 2, 4} r_H  x  U in {0.5, 1, 3, 10} v_H(d_edge),
v_H(b) = sqrt(mu_p / b) (the speed of a circular orbit at b: the impulsive
criterion is U >> v_H).  Metrics per case: |dv|/U and |dC_J|/|C_J| at +L.
"""
import numpy as np, json, time, warnings
warnings.filterwarnings("ignore")
from scipy.integrate import solve_ivp
import conjlaws as C

MU_SUN = 4.0 * np.pi ** 2
MU_P = 9.5459e-4 * MU_SUN
A_P = 5.2
N_P = np.sqrt(MU_SUN / A_P ** 3)
R_H = A_P * (MU_P / (3.0 * MU_SUN)) ** (1.0 / 3.0)
KAP = 0.5


def planet_state(t):
    th = N_P * t
    return A_P * np.exp(1j * th), 1j * N_P * th


def jacobi(r, v, rp):
    vrot = v - 1j * N_P * r
    return (N_P * abs(r)) ** 2 + 2.0 * (MU_SUN / abs(r) + MU_P / abs(r - rp)) \
        - abs(vrot) ** 2


def run_case(d0, U, ang, seed, kap=KAP):
    rng = np.random.default_rng(seed)
    rp0, vp0 = planet_state(0.0)
    # ship entrance: d0 from the planet, synodic velocity U in a random
    # in-plane direction (mostly inbound: ang offsets from -rhat)
    rhat = (rp0 / abs(rp0))
    dvec = d0 * np.exp(1j * ang) * rhat
    vdir = np.exp(1j * rng.uniform(0, 2 * np.pi))
    V0 = U * vdir
    r0, v0 = rp0 + dvec, vp0 + V0
    # window: edge at kappa*r_H, duration from the closing speed
    w = kap * R_H / max(U, 1e-6)
    L = (5.0 + 1.0) * w
    # ---- truth
    def rhs(t, y):
        rr = y[0] + 1j * y[1]
        vv = y[2] + 1j * y[3]
        rp, _ = planet_state(t)
        acc = -MU_SUN * rr / abs(rr) ** 3 - MU_P * (rr - rp) / abs(rr - rp) ** 3
        return [vv.real, vv.imag, acc.real, acc.imag]
    sol = solve_ivp(rhs, [0, L], [r0.real, r0.imag, v0.real, v0.imag],
                    rtol=1e-11, atol=1e-13, method="DOP853", dense_output=True)
    ts = np.linspace(0, L, 3001)
    yy = sol.sol(ts)
    rr = yy[0] + 1j * yy[1]
    rpf = A_P * np.exp(1j * N_P * ts)
    dd = np.abs(rr - rpf)
    i = int(np.argmin(dd))
    t_star, b_real = ts[i], dd[i]
    rbT = sol.y[0, -1] + 1j * sol.y[1, -1]
    vbT = sol.y[2, -1] + 1j * sol.y[3, -1]
    # ---- law
    tw0 = max(t_star - w, 1e-9)
    rbw, vbw = law_drift(r0, v0, MU_SUN, tw0)
    dr_pre, dv_pre = C.tail_moments_circ(rbw, vbw, tw0, 0.0, MU_P, MU_SUN, A_P, N_P, tw0)
    rbw, vbw = rbw + dr_pre, vbw + dv_pre
    rpw, vpw = planet_state(tw0)
    rbE, vbE = C.encounter_event(rbw, vbw, rpw, vpw, MU_P, MU_SUN, w, use_pair_flow=True)
    te = t_star + w
    rbE, vbE = law_drift(rbE, vbE, MU_SUN, L - te)
    dr_po, dv_po = C.tail_moments_circ(rbw, vbw, te, L, MU_P, MU_SUN, A_P, N_P, L)
    rbE, vbE = rbE + dr_po, vbE + dv_po
    # ---- negative control
    rpw2, vpw2 = planet_state(t_star)
    rbw2, vbw2 = law_drift(r0, v0, MU_SUN, t_star)
    rbN, vbN = C.impulse_event(rbw2, vbw2, rpw2, vpw2, MU_P)
    rbN, vbN = law_drift(rbN, vbN, MU_SUN, L - t_star)
    CJ0 = jacobi(r0, v0, rp0)
    CJt = jacobi(rbT, vbT, planet_state(L)[0])
    CJe = jacobi(rbE, vbE, planet_state(L)[0])
    vH = np.sqrt(MU_P / max(b_real, 1e-9))
    return dict(b_rH=b_real / R_H, U_vH=abs(V0) / vH, t_star=t_star,
                dv_U=abs(vbE - vbT) / abs(V0), dCJ=abs(CJe - CJ0) / abs(CJ0),
                dCJ_truth=abs(CJt - CJ0) / abs(CJ0),
                dvN_U=abs(vbN - vbT) / abs(V0))



def law_drift(r, v, mu, dt):
    """Exact drift leg for this probe: tight DOP853 two-body (the law's own
    drift is the compiled tube, exact by construction; this isolates the
    event's error from my quick element route's near-parabolic corners)."""
    from scipy.integrate import solve_ivp
    if abs(dt) < 1e-12:
        return r, v
    def rhs(t, y):
        rr = y[0] + 1j * y[1]
        vv = y[2] + 1j * y[3]
        acc = -mu * rr / abs(rr) ** 3
        return [vv.real, vv.imag, acc.real, acc.imag]
    sol = solve_ivp(rhs, [0, dt], [r.real, r.imag, v.real, v.imag],
                    rtol=1e-13, atol=1e-15, method="DOP853")
    return sol.y[0, -1] + 1j * sol.y[1, -1], sol.y[2, -1] + 1j * sol.y[3, -1]

import conjlaws as _C
_C._law_drift = law_drift
_orig_ef = _C.encounter_event
def _ef(r_b, v_b, r_p, v_p, mu_p, mu_sun, w, planet_arc=None, use_pair_flow=True):
    r1, v1 = law_drift(r_b, v_b, mu_sun, w)
    rp1, vp1 = law_drift(r_p, v_p, mu_sun, w)
    d2, V2 = _C.pair_flow(r1 - rp1, v1 - vp1, mu_p, 2.0 * w)
    r2, v2 = rp1 + d2, vp1 + V2
    return law_drift(r2, v2, mu_sun, w)
_C.encounter_event = _ef

if __name__ == "__main__":
    rows = []
    t00 = time.time()
    vH_rH = np.sqrt(MU_P / R_H)
    for d0r in [0.5, 1.0, 2.0, 4.0]:
        for Uv in [0.5, 1.0, 3.0, 10.0]:
            for rep in range(3):
                seed = 100 * int(d0r * 10) + int(Uv * 10) + rep
                rng = np.random.default_rng(seed)
                ang = rng.uniform(0, 2 * np.pi)
                U = Uv * np.sqrt(MU_P / (d0r * R_H))
                try:
                    r = run_case(d0r * R_H, U, ang, seed)
                except Exception as ex:
                    r = dict(b_rH=np.nan, U_vH=np.nan, dv_U=np.nan, dCJ=np.nan,
                             dCJ_truth=np.nan, dvN_U=np.nan, err=str(ex))
                r.update(d0r=d0r, Uv=Uv, rep=rep)
                rows.append(r)
                print(f"d0={d0r:3.1f}rH U/vH(target)={Uv:4.1f} -> b={r['b_rH']:5.2f}rH "
                      f"U/vH={r['U_vH']:6.2f}  dv/U={r['dv_U']:8.2e}  dCJ={r['dCJ']:8.2e} "
                      f"(truth {r['dCJ_truth']:.1e})  impulse dv/U={r['dvN_U']:8.2e}")
    print(f"wall {time.time()-t00:.0f} s")
    json.dump(rows, open("probe_boundary.json", "w"), indent=1, default=float)
