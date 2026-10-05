"""Probe A: B13-like flybys — the encounter as ONE exact event.

Scene: Sun (mu=1) + Jupiter-mass planet on a circular orbit at 5.2 AU.
Ship on a planetocentric hyperbola with given v_inf and periapsis q_p.
Truth: DOP853 on the restricted problem (Sun + moving planet), rtol 1e-12.
Event: pair two-body flow over the window [t*-w, t*+w], Sun-only counterfactual.

TUNED HERE (and only here): the window edge kappa = d_edge / r_H, on the
in-range grid q_p in {2,5,10,30} r_p, v_inf in {5,10,15} km/s.
Held out (predictions.md): (1.2 r_p, 20 km/s), (50 r_p, 5 km/s), trailing
side, inbound/outbound senses.
"""
import numpy as np, json, time, warnings
warnings.filterwarnings("ignore")
from scipy.integrate import solve_ivp
import conjlaws as C

MU_SUN = 4.0 * np.pi ** 2   # AU^3/yr^2 (GM of 1 M_sun)
MU_P = 9.5459e-4 * MU_SUN  # GM_Jupiter in AU^3/yr^2
A_P = 5.2
N_P = np.sqrt(MU_SUN / A_P ** 3)  # rad/yr
R_P = 71492.0 / 1.496e8          # AU
R_H = A_P * (MU_P / (3.0 * MU_SUN)) ** (1.0 / 3.0)  # a*(m_p/3M_sun)^(1/3)
KMS = 4.74057                    # 1 AU/yr in km/s


def planet_state(t):
    th = N_P * t
    r = A_P * np.exp(1j * th)
    v = 1j * N_P * r
    return r, v


def make_case(q_p, v_inf, phase, sense=+1):
    """Heliocentric state at t = -T of a ship entering a hyperbola about the
    planet with periapsis q_p and asymptotic speed v_inf.  `phase` sets the
    encounter's orientation; sense=-1 mirrors the incoming side."""
    U = v_inf / KMS
    v_peri = np.sqrt(U ** 2 + 2 * MU_P / q_p)
    psi = phase
    d_peri = q_p * np.exp(1j * psi)
    V_peri = sense * 1j * v_peri * np.exp(1j * psi)
    return d_peri, V_peri, U

def run_case(q_p, v_inf, phase, sense, kappa, negative=False, lead=5.0):
    """Honest law emulation.  The encounter state is defined at t*=0
    (periapsis q_p, planetocentric speed from v_inf); the ship is then
    propagated Sun-only backward/forward by the LAW's own drift, so the
    drift leg is exact by construction and every reported error comes from
    the event channel alone.  Truth: restricted 3-body over the same span.
    """
    U = v_inf / KMS
    v_peri = np.sqrt(U ** 2 + 2 * MU_P / q_p)
    d_peri = q_p * np.exp(1j * phase)
    V_peri = sense * 1j * v_peri * np.exp(1j * phase)
    d_edge = kappa * R_H
    w = max(d_edge / U, 4.0 * q_p / v_peri)
    L = (lead + 1.0) * w
    # encounter state at t=0, then the law's own Sun-only drift to -L
    rp0, vp0 = planet_state(0.0)
    r_enc, v_enc = rp0 + d_peri, vp0 + V_peri
    rb0, vb0 = C.propagate(r_enc, v_enc, MU_SUN, -L)
    # ---- truth: restricted 3-body over [-L, +L]
    def rhs(t, y):
        rr = y[0] + 1j * y[1]
        vv = y[2] + 1j * y[3]
        rp, _ = planet_state(t)
        acc = -MU_SUN * rr / abs(rr) ** 3 - MU_P * (rr - rp) / abs(rr - rp) ** 3
        return [vv.real, vv.imag, acc.real, acc.imag]
    sol = solve_ivp(rhs, [-L, L], [rb0.real, rb0.imag, vb0.real, vb0.imag],
                    rtol=1e-12, atol=1e-14, method="DOP853", dense_output=True)
    ts_fine = np.linspace(-L, L, 4001)
    yy = sol.sol(ts_fine)
    rr = yy[0] + 1j * yy[1]
    rpf = A_P * np.exp(1j * N_P * ts_fine)
    i_star = np.argmin(np.abs(rr - rpf))
    t_star, b_real = ts_fine[i_star], np.abs(rr[i_star] - rpf[i_star])
    rbT = sol.y[0, -1] + 1j * sol.y[1, -1]
    vbT = sol.y[2, -1] + 1j * sol.y[3, -1]
    # ---- law: Sun-only drift to the window edge, first-order tail on the
    # way in, one exact event, first-order tail + drift on the way out
    tw0 = t_star - w
    rbw, vbw = C.propagate(rb0, vb0, MU_SUN, tw0 - (-L))
    if not negative:
        dr_pre, dv_pre = C.tail_moments_circ(rbw, vbw, tw0, -L, MU_P, MU_SUN, A_P, N_P, tw0)
        rbw, vbw = rbw + dr_pre, vbw + dv_pre
    rpw, vpw = planet_state(tw0)
    if negative:
        rbE, vbE = C.impulse_event(rbw, vbw, rpw, vpw, MU_P)
        rbE, vbE = C.propagate(rbE, vbE, MU_SUN, L - (t_star - w))
    else:
        rbE, vbE = C.encounter_event(rbw, vbw, rpw, vpw, MU_P, MU_SUN, w)
        te = t_star + w
        rbE, vbE = C.propagate(rbE, vbE, MU_SUN, L - te)
        dr_post, dv_post = C.tail_moments_circ(rbw, vbw, te, L, MU_P, MU_SUN, A_P, N_P, L)
        rbE, vbE = rbE + dr_post, vbE + dv_post
    E0, L0 = C.helio_energy_L(rb0, vb0, MU_SUN)
    Et, Lt = C.helio_energy_L(rbT, vbT, MU_SUN)
    Ee, Le = C.helio_energy_L(rbE, vbE, MU_SUN)
    dE_t, dL_t = Et - E0, Lt - L0
    dE_e, dL_e = Ee - E0, Le - L0
    scale_E = max(abs(dE_t), 1e-12)
    scale_L = max(abs(dL_t), 1e-10)
    return (abs(dE_e - dE_t) / scale_E, abs(dL_e - dL_t) / scale_L,
            abs(vbE - vbT) / abs(vbT), b_real / q_p)


# ---------------------------------------------------------------- tuning
rng = np.random.default_rng(11)
tune = []
for q in [2.0, 5.0, 10.0, 30.0]:
    for vinf in [5.0, 10.0, 15.0]:
        ph = rng.uniform(0, 2 * np.pi)
        tune.append((q * R_P, vinf, ph, +1))
kappas = [0.05, 0.1, 0.25, 0.5, 1.0]
print("=== tuning on in-range grid (12 cases per kappa) ===")
best = None
for kap in kappas:
    errs = [run_case(q, v, ph, s, kap) for q, v, ph, s in tune]
    med = np.median([e[0] for e in errs])
    worst = np.max([e[0] for e in errs])
    print(f"kappa={kap:4.2f}  median dE err {med:.2e}  worst {worst:.2e}")
    if best is None or med < best[1]:
        best = (kap, med)
kap = best[0]
print(f"chosen kappa = {kap}")

# ---------------------------------------------------------------- held out
held = [
    ("fast+deep 1.2rp 20km/s", 1.2 * R_P, 20.0),
    ("slow+far 50rp 5km/s", 50.0 * R_P, 5.0),
    ("mid 10rp 12km/s", 10.0 * R_P, 12.0),
    ("deep 1.5rp 8km/s", 1.5 * R_P, 8.0),
]
print("\n=== held-out cases (event law) ===")
res = []
for name, q, v in held:
    for sense, ph in [(+1, 0.7), (-1, 2.4)]:
        eE, eL, ev, br = run_case(q, v, ph, sense, kap)
        res.append((name, sense, eE, eL, ev, br))
        print(f"{name:26s} sense={sense:+d}  dE err {eE:.2e}  dL err {eL:.2e}  dv err {ev:.2e}  b_real/q={br:.3f}")

print("\n=== negative control (straight-line impulse), same held-out cases ===")
for name, q, v in held:
    eE, eL, ev, br = run_case(q, v, 0.7, +1, kap, negative=True)
    print(f"{name:26s}  dE err {eE:.2e}  dL err {eL:.2e}  dv err {ev:.2e}  b_real/q={br:.3f}")

# ---------------------------------------------------------------- in-range final at chosen kappa + timing
t0 = time.time()
errs = [run_case(q, v, ph, s, kap) for q, v, ph, s in tune]
dt = time.time() - t0
print(f"\nin-range at kappa={kap}: median dE {np.median([e[0] for e in errs]):.2e}, "
      f"worst {np.max([e[0] for e in errs]):.2e}, 12 cases in {dt:.1f} s incl. truth")
json.dump({"kappa": kap, "tune": errs, "held": res}, open("probe_a.json", "w"), indent=1)
