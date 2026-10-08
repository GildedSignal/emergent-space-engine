#!/usr/bin/env python3
"""Second author on 20261008-0041-redteam-ecfd: the record corrections named by
the checker, plus the artifact-free rerun that fixes the weak-field floor.

1. Corrections computed from the SHIPPED record (falsifier-out.json, reproduced
   bit-identically by the untouched falsifier.py):
   - oracle-distance ratio |oracle-shipped| / |shipped-GR2PN| per nu, and its range;
   - sign-flipped law (2*shipped - GR2PN(0.25)) vs B11's tolerance: margins;
   - the nudged start's own artifact delta_phi = 1e-9/|u''(up)| per pbar.
2. Artifact-free rerun: start EXACTLY at the periastron turning point (pu = 0),
   integrate to the aphelion event (pu crossing 0 upward), advance = 2*half - 2pi.
   Both integrators, same tolerance. Removes the ~1e-9/|u''| phase offset that
   dominates the original weak-field rows (pbar >= 200).
3. c2 refit under the artifact-free method (control: moves < 0.01).
4. Rust transfer: rel(shipped-rust advance from rust-advance.json vs exact ODE).
5. B11 pass/fail of the sign-flipped law and of the shipped Rust law vs 1PN oracle.
"""
import json
import numpy as np
from scipy.integrate import solve_ivp

RTOL, ATOL = 1e-13, 1e-16
TOL_B11 = lambda p: 0.01 + 16.0 / p  # xtask/src/behave/binary.rs:17-18

orig = json.load(open("falsifier-out.json"))
rust = {r["p"]: r for r in json.load(open("rust-advance.json")) if r["e"] == 0.6}

# ---------- integrators (half-orbit, artifact-free) --------------------------
def half_exact(up, ua):
    invL2 = (up + ua) / 2 - (up * up + up * ua + ua * ua)
    def rhs(phi, y):
        return [y[1], invL2 + 3.0 * y[0] * y[0] - y[0]]
    def apo(phi, y):
        return y[1]
    apo.direction = +1.0
    apo.terminal = True
    sol = solve_ivp(rhs, (0.0, 300.0), [up, 0.0], method="DOP853",
                    rtol=RTOL, atol=ATOL, events=apo)
    u_end = sol.y[0, -1]
    assert abs(u_end - ua) < 1e-9, u_end
    return float(2.0 * sol.t_events[0][0] - 2 * np.pi), float(invL2 + 3 * up * up - up)

def half_eob(nu, up, ua, s=-1):
    A  = lambda u: 1.0 - 2.0 * u + 2.0 * nu * u ** 3
    dA = lambda u: -2.0 + 6.0 * nu * u * u
    D  = lambda u: 1.0 + s * 6.0 * nu * u * u
    dD = lambda u: s * 12.0 * nu * u
    F  = lambda u: A(u) ** 2 * D(u)
    dF = lambda u: 2 * A(u) * dA(u) * D(u) + A(u) ** 2 * dD(u)
    Ap, Aa = A(up), A(ua)
    j2 = (Aa - Ap) / (Ap * up ** 2 - Aa * ua ** 2)
    assert j2 > 0
    j = np.sqrt(j2)
    h = np.sqrt(A(up) * (1 + j2 * up ** 2))
    def rhs(phi, y):
        u, pu = y
        Au = A(u)
        dS_du = (dA(u) * (1.0 + j * j * u * u) + Au * 2.0 * j * j * u
                 + dF(u) * u ** 4 * pu * pu + F(u) * 4.0 * u ** 3 * pu * pu)
        return [F(u) * u ** 2 * pu / (j * Au), -dS_du / (2.0 * Au * j * u * u)]
    def apo(phi, y):
        return y[1]
    apo.direction = +1.0
    apo.terminal = True
    sol = solve_ivp(rhs, (0.0, 100.0), [up, 0.0], method="DOP853",
                    rtol=RTOL, atol=ATOL, events=apo)
    assert sol.y[0, -1] < up - 0.9 * (up - ua), sol.y[0, -1]  # went to aphelion
    u_e, pu_e = sol.y[0, -1], sol.y[1, -1]
    H_end = np.sqrt(A(u_e) * (1 + j * j * u_e * u_e) + F(u_e) * u_e ** 4 * pu_e ** 2)
    return float(2.0 * sol.t_events[0][0] - 2 * np.pi), float(abs(H_end - h) / h)

out = {"corrections_from_shipped": {}, "artifact_free": {}, "c2": {}, "rust": {}, "b11": {}}

# ---------- 1. corrections from the shipped record ---------------------------
C = out["corrections_from_shipped"]
for nu in ("0.01", "0.1", "0.25"):
    rat = [abs(r["rel_oracle_vs_shipped"]) / abs(r[f"rel_shipped_vs_GR2PN_nu{nu}"])
           for r in orig["grid"]]
    C[f"oracle_dist_ratio_nu{nu}"] = {"min": min(rat), "max": max(rat), "ratios": rat}
flip = []
for r in orig["grid"]:
    a_flip = 2 * r["adv_shipped"] - r["adv_GR2PN_nu0.25"]
    dev = abs(a_flip / r["adv_1pn_oracle"] - 1)
    flip.append({"pbar": r["pbar"], "dev_vs_1pn_oracle": dev,
                 "margin": TOL_B11(r["pbar"]) / dev})
C["sign_flip_vs_B11"] = flip
C["sign_flip_min_margin"] = min(f["margin"] for f in flip)

# ---------- 2. artifact-free rerun -------------------------------------------
rows = []
for r in orig["grid"]:
    pbar, E = r["pbar"], r["e"]
    up, ua = (1 + E) / pbar, (1 - E) / pbar
    a_hf, u2p = half_exact(up, ua)
    row = {"pbar": pbar, "e": E,
           "adv_half": a_hf,
           "adv_nudged": r["adv_shipped"],
           "artifact_pred_rad": 1e-9 / abs(u2p),
           "artifact_meas_rad": r["adv_shipped"] - a_hf}
    for nu in (0.01, 0.1, 0.25):
        a_gr, dH = half_eob(nu, up, ua)
        row[f"rel_half_nu{nu:g}"] = (a_hf - a_gr) / a_gr
        row[f"rel_nudged_nu{nu:g}"] = r[f"rel_shipped_vs_GR2PN_nu{nu:g}"]
        if nu == 0.25:
            row["eob_H_drift_half"] = dH
    rows.append(row)
out["artifact_free"]["grid_e0.6"] = rows
# e=0.3 spot check (labeling cross-check against the Rust dump)
e3 = []
for pbar in (20.0, 50.0, 1000.0):
    up, ua = 1.3 / pbar, 0.7 / pbar
    a_hf, _ = half_exact(up, ua)
    a_r = [x for x in json.load(open("rust-advance.json"))
           if x["e"] == 0.3 and x["p"] == pbar][0]["advance"]
    e3.append({"pbar": pbar, "adv_half_e0.3": a_hf, "adv_rust_e0.3": a_r,
               "rel_rust_vs_half": (a_r - a_hf) / a_hf})
out["artifact_free"]["e0.3"] = e3

# ---------- 3. c2 refit (artifact-free) --------------------------------------
def fit_c2(f):
    ps = np.array([30.0, 40.0, 60.0, 80.0])
    g = np.array([f(p) / (6 * np.pi / p) - 1.0 for p in ps])
    X = np.vstack([1 / ps, 1 / ps ** 2]).T
    c, *_ = np.linalg.lstsq(X, g, rcond=None)
    return c[0]
E = 0.6
out["c2"] = {
    "shipped_exact_half": fit_c2(lambda p: half_exact((1 + E) / p, (1 - E) / p)[0]),
    "GR2PN_nu0.25_half": fit_c2(lambda p: half_eob(0.25, (1 + E) / p, (1 - E) / p)[0]),
    "shipped_exact_nudged(orig)": orig["c2"]["shipped_exact"],
    "GR2PN_nu0.25_nudged(orig)": orig["c2"]["GR2PN_nu0.25"],
}

# ---------- 4. rust transfer --------------------------------------------------
tr = []
for r in orig["grid"]:
    p = r["pbar"]
    a_r = rust[p]["advance"]
    tr.append({"pbar": p, "rel_rust_vs_exactODE": (a_r - r["adv_shipped"]) / r["adv_shipped"],
               "rel_rust_vs_GR2PN_nu0.25_nudged":
                   (a_r - r["adv_GR2PN_nu0.25"]) / r["adv_GR2PN_nu0.25"]})
out["rust"]["grid_e0.6"] = tr
out["rust"]["max_abs_rel_vs_exact"] = max(abs(x["rel_rust_vs_exactODE"]) for x in tr)

# ---------- 5. B11 on sign-flipped law and on the shipped Rust law -----------
b11 = []
for r in orig["grid"]:
    p = r["pbar"]
    a_flip = 2 * r["adv_shipped"] - r["adv_GR2PN_nu0.25"]
    a_r = rust[p]["advance"]
    b11.append({"pbar": p,
                "flipped_passes_B11":
                    abs(a_flip / r["adv_1pn_oracle"] - 1) <= TOL_B11(p),
                "rust_rel_vs_1pn_oracle":
                    (a_r - r["adv_1pn_oracle"]) / r["adv_1pn_oracle"],
                "rust_passes_B11":
                    abs(a_r / r["adv_1pn_oracle"] - 1) <= TOL_B11(p)})
out["b11"] = b11

print(json.dumps(out, indent=1))
with open("second-out.json", "w") as f:
    json.dump(out, f, indent=1)
