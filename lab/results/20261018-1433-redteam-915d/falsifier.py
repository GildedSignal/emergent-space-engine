#!/usr/bin/env python3
"""Premise red-team 20261018-1433: boosts do not commute; the additive heading cannot carry it.

Exact law (physics): body frame B in SO(2,1), dB/dtau = B.(alpha.(m0*Kx + m1*Ky) + omega*J),
thrust along the nose marker m0 (body coords, fixed under held keys), keyed turn omega in J.
Shipped law (docs/representation.md L50; crates/universe/src/thrust.rs `owed`/`burn`): a
doll-frame heading accumulator h <- h + omega*dtau, the burn composed exactly along it
(burn() is exact proper-velocity boost composition, replicated verbatim, flat limit).
One difference only: where the thrust direction comes from.

Reported angles:
- theta_sky: rotation of Bp^-1 B (Bp = pure boost of B's velocity). It fixes e0 exactly, so it
  is a spatial rotation in body coords: the angle by which the entire seen field rotates.
- nose_err: doll-frame angle between the true nose B(0,m0) and the accumulator heading.
Pure float, c = 1, flat local orthonormal frame. Writes results.json.
"""
import json
import math
import time

def mmul(A, B):
    (a00, a01, a02), (a10, a11, a12), (a20, a21, a22) = A
    (b00, b01, b02), (b10, b11, b12), (b20, b21, b22) = B
    return [
        [a00 * b00 + a01 * b10 + a02 * b20, a00 * b01 + a01 * b11 + a02 * b21, a00 * b02 + a01 * b12 + a02 * b22],
        [a10 * b00 + a11 * b10 + a12 * b20, a10 * b01 + a11 * b11 + a12 * b21, a10 * b02 + a11 * b12 + a12 * b22],
        [a20 * b00 + a21 * b10 + a22 * b20, a20 * b01 + a21 * b11 + a22 * b21, a20 * b02 + a21 * b12 + a22 * b22],
    ]

def mvec(A, v):
    return (
        A[0][0] * v[0] + A[0][1] * v[1] + A[0][2] * v[2],
        A[1][0] * v[0] + A[1][1] * v[1] + A[1][2] * v[2],
        A[2][0] * v[0] + A[2][1] * v[1] + A[2][2] * v[2],
    )

def minv(A):
    T = [[A[j][i] for j in range(3)] for i in range(3)]
    return [[(1.0 if i == 0 else -1.0) * T[i][j] * (1.0 if j == 0 else -1.0) for j in range(3)] for i in range(3)]

def eye():
    return [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

def expm_small(A, order=6):
    R = eye()
    P = eye()
    fact = 1.0
    for k in range(1, order + 1):
        P = mmul(P, A)
        fact *= k
        f = 1.0 / fact
        R = [[R[i][j] + P[i][j] * f for j in range(3)] for i in range(3)]
    return R

def gen(a, w, m):
    ax, ay = a * m[0], a * m[1]
    return [[0.0, ax, ay], [ax, 0.0, -w], [ay, w, 0.0]]

def beta_of(B):
    g = B[0][0]
    return (B[1][0] / g, B[2][0] / g, g)

def rot2(v, a):
    c, s = math.cos(a), math.sin(a)
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)

def angle_between(a, b):
    return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])

def boost_pure(beta):
    sp = math.hypot(*beta)
    th = math.atan2(beta[1], beta[0])
    ph = math.atanh(min(sp, 1.0 - 1e-15))
    ch, sh = math.cosh(ph), math.sinh(ph)
    c, s = math.cos(th), math.sin(th)
    return [
        [ch, sh * c, sh * s],
        [sh * c, ch * c * c + s * s, c * s * (ch - 1.0)],
        [sh * s, c * s * (ch - 1.0), ch * s * s + c * c],
    ]

def nose_doll(B, m):
    return (B[1][1] * m[0] + B[1][2] * m[1], B[2][1] * m[0] + B[2][2] * m[1])

def sky_angle(B):
    """Angle of Bp^-1 B (a spatial rotation in body coords): the seen field's rotation."""
    bx, by, _ = beta_of(B)
    R = mmul(minv(boost_pure((bx, by))), B)
    return math.atan2(R[2][1], R[1][1]), max(abs(R[0][1]), abs(R[1][0]), abs(R[0][2]), abs(R[2][0]), abs(R[0][0] - 1.0))

def wrap(a):
    while a > math.pi:
        a -= 2 * math.pi
    while a < -math.pi:
        a += 2 * math.pi
    return a

def shipped_step(u, h, alpha, dtau, w, fwd):
    h_mid = h + w * dtau / 2.0
    h = h + w * dtau
    if fwd != 0:
        eta = fwd * alpha * dtau
        cn, sn = math.cos(h_mid), math.sin(h_mid)
        g = math.sqrt(1.0 + u[0] * u[0] + u[1] * u[1])
        un = u[0] * cn + u[1] * sn
        f = un / (g + 1.0)
        ch, sh = math.cosh(eta), math.sinh(eta)
        u = (u[0] * ch + (cn + u[0] * f) * sh, u[1] * ch + (sn + u[1] * f) * sh)
    return u, h
def exact_flight(B0, m0, alpha, w, fwd, T, N, every=None):
    """Held keys: A constant in body coords -> one exact exponential per step, plus the
    cumulative sky rotation (per-step increments, keyed spin excluded: both models apply it)
    and (optionally) a coarse trajectory."""
    A = gen(fwd * alpha, w, m0)
    dtau = T / N
    M = expm_small([[A[i][j] * dtau for j in range(3)] for i in range(3)], order=8)
    B = B0
    x = [0.0, 0.0]
    path = 0.0
    sky = 0.0
    prev = 0.0
    th0 = None
    traj = []
    for k in range(N):
        u1, u2 = B[1][0], B[2][0]
        x[0] += dtau * u1
        x[1] += dtau * u2
        path += dtau * math.hypot(u1, u2)
        B = mmul(B, M)
        s, _ = sky_angle(B)
        sky += wrap(s - prev)
        prev = s
        if every is not None and k % every == 0:
            bx, by, _ = beta_of(B)
            thv = math.atan2(by, bx)
            if th0 is None:
                th0 = thv
            traj.append({"tau": (k + 1) * dtau, "sky_deg": math.degrees(sky - w * (k + 1) * dtau),
                         "vel_turned_deg": math.degrees(thv - th0)})
    m_fw = rot2(m0, -w * T)
    return B, m_fw, x, path, sky - w * T, traj

def shipped_flight(u0, h0, alpha, w, fwd, T, N):
    u, h = u0, h0
    x = [0.0, 0.0]
    path = 0.0
    for _ in range(N):
        u, h = shipped_step(u, h, alpha, T / N, w, fwd)
        x[0] += (T / N) * u[0]
        x[1] += (T / N) * u[1]
        path += (T / N) * math.hypot(*u)
    return u, h, x, path

def prescribed_turn(beta, psi_total, T, N):
    """Velocity turns by psi_total at constant gamma: comoving burn kept doll-perpendicular
    (aimed at the midpoint of the step). Returns B and the cumulative sky rotation."""
    g = 1.0 / math.sqrt(1.0 - beta * beta)
    B = boost_pure((beta, 0.0))
    x = [0.0, 0.0]
    dtau = T / N
    psid = psi_total / T
    a = g * beta * psid
    m = (0.0, 1.0)
    sky = 0.0
    prev = 0.0
    for _ in range(N):
        u1, u2 = B[1][0], B[2][0]
        x[0] += dtau * u1
        x[1] += dtau * u2
        # aim the thrust at the velocity direction half a step ahead (midpoint)
        half = psid * dtau / 2.0
        ch, sh = math.cos(half), math.sin(half)
        v1, v2 = u1 * ch - u2 * sh, u1 * sh + u2 * ch
        n = math.hypot(v1, v2)
        nd = (-v2 / n, v1 / n)
        sb = mvec(minv(B), (0.0, nd[0], nd[1]))
        ln = math.hypot(sb[1], sb[2])
        m = (sb[1] / ln, sb[2] / ln)
        A = gen(a, 0.0, m)
        B = mmul(B, expm_small([[A[i][j] * dtau for j in range(3)] for i in range(3)], order=3))
        s, _ = sky_angle(B)
        sky += wrap(s - prev)
        prev = s
    return B, x, sky

results = {"flights": {}, "closed_form": {}, "sweeps": {}, "controls": {}}
t0 = time.time()
N_OPEN = 40_000
N_PRE = 16_000

# ---------- Closed form: two perpendicular boosts, both orders ----------
ph = math.atanh(0.9)
Bx = [[math.cosh(ph), math.sinh(ph), 0.0], [math.sinh(ph), math.cosh(ph), 0.0], [0.0, 0.0, 1.0]]
By = [[math.cosh(ph), 0.0, math.sinh(ph)], [0.0, 1.0, 0.0], [math.sinh(ph), 0.0, math.cosh(ph)]]
w_yx, cont_yx = sky_angle(mmul(By, Bx))
w_xy, cont_xy = sky_angle(mmul(Bx, By))
results["closed_form"] = {
    "rapidity_each": ph, "gamma_each": math.cosh(ph),
    "sky_ByBx_deg": math.degrees(w_yx), "sky_BxBy_deg": math.degrees(w_xy),
    "block_contamination": max(cont_yx, cont_xy),
    "cand_2atan_t2t2_deg": math.degrees(2.0 * math.atan(math.tanh(ph / 2) ** 2)),
    "cand_atan2_shsh_deg": math.degrees(math.atan2(math.sinh(ph) ** 2, 2.0 * math.cosh(ph))),
}

# ---------- Controls ----------
B0 = boost_pure((0.8660254, 0.0))
u0 = (B0[0][0] * 0.8660254, 0.0)
B, m_fw, x, path, sky, _ = exact_flight(B0, (1.0, 0.0), 1.0, 0.0, +1, 1.0, N_OPEN)
bx, by, g = beta_of(B)
us, hs, xs, ps = shipped_flight(u0, 0.0, 1.0, 0.0, +1, 1.0, N_OPEN)
bex = math.hypot(bx, by)
bsh = math.hypot(*us) / math.sqrt(1 + us[0] ** 2 + us[1] ** 2)
results["controls"]["collinear"] = {
    "sky_deg": math.degrees(sky), "beta_err": abs(bex - bsh),
    "pos_err_over_path": math.hypot(x[0] - xs[0], x[1] - xs[1]) / path,
    "col0_norm_err": abs(B[0][0] ** 2 - B[1][0] ** 2 - B[2][0] ** 2 - 1.0),
}
B, m_fw, x, path, sky, _ = exact_flight(B0, (1.0, 0.0), 0.0, math.pi, 0, 1.0, N_OPEN)
results["controls"]["pure_turn"] = {"sky_deg": math.degrees(sky)}

# ---------- Prescribed constant-gamma turns ----------
sweep = {}
for beta in [0.05, 0.1, 0.3, 0.5, 0.6, 0.75, 0.8660254, 0.95, 0.99]:
    row = {}
    for deg in [90.0, 180.0, 360.0]:
        B, x, sky = prescribed_turn(beta, math.radians(deg), 1.0, N_PRE)
        bx, by, g = beta_of(B)
        row[str(deg)] = {
            "sky_deg": math.degrees(sky),
            "beta": math.hypot(bx, by), "gamma": g,
            "cf_gm1_deg": (math.degrees((g - 1.0) * math.radians(deg))),
            "cf_1m1g_deg": (math.degrees((1.0 - 1.0 / g) * math.radians(deg))),
        }
    sweep[str(beta)] = row
results["sweeps"]["prescribed_turn"] = sweep

# ---------- Open-loop flights: same keys, exact vs accumulator ----------
def run_open(m0, alpha, w, T, delta_label, N=N_OPEN):
    n0 = nose_doll(B0, m0)
    h0 = math.atan2(n0[1], n0[0])
    B, m_fw, x, path, sky, traj = exact_flight(B0, m0, alpha, w, +1, T, N, every=200)
    us, hs, xs, ps = shipped_flight(u0, h0, alpha, w, +1, T, N)
    bx, by, g = beta_of(B)
    bs = math.hypot(*us) / math.sqrt(1 + us[0] ** 2 + us[1] ** 2)
    ne = nose_doll(B, m0)
    return {
        "theta_sky_final_deg": math.degrees(sky),
        "gamma_final": g, "beta_err": abs(math.hypot(bx, by) - bs),
        "vel_dir_err_deg": math.degrees(abs(angle_between((bx, by), us))),
        "nose_err_deg": math.degrees(abs(angle_between(ne, (math.cos(hs), math.sin(hs))))),
        "pos_err_over_path": math.hypot(x[0] - xs[0], x[1] - xs[1]) / path,
        "trajectory": traj,
    }

# off45: nose 45 deg off velocity, thrust on (the record's off45 held burn)
m0_45 = rot2((1.0, 0.0), math.pi / 4)
results["flights"]["off45_burn_gamma2"] = run_open(m0_45, 1.0, 0.0, 1.0, "off45")

# off135 brake: the record's held brake family (nose 135 deg off, mostly retro)
m0_135 = rot2((1.0, 0.0), 3 * math.pi / 4)
results["flights"]["off135_brake_gamma2"] = run_open(m0_135, 1.0, 0.0, 1.0, "off135")

# reversal: keys (turn + thrust, nose initially 90 deg off) tuned once on the exact model
m0_90 = rot2((1.0, 0.0), math.pi / 2)
best = None
for w_try in [0.2, 0.35, 0.5, 0.7, 1.0, 1.4, 1.8]:
    for T_try in [2.0, 3.0, 4.0, 6.0, 8.0, 10.0]:
        B, m_fw, x, path, sky, _ = exact_flight(B0, m0_90, 1.0, w_try, +1, T_try, 4_000)
        bx, by, g = beta_of(B)
        turned = abs(math.degrees(math.atan2(by, bx)))
        if best is None or abs(turned - 180.0) < best[0]:
            best = (abs(turned - 180.0), w_try, T_try, turned)
w_star, T_star = best[1], best[2]
n0 = nose_doll(B0, m0_90)
h0_90 = math.atan2(n0[1], n0[0])
B, m_fw, x, path, sky, traj = exact_flight(B0, m0_90, 1.0, w_star, +1, T_star, N_OPEN, every=200)
us, hs, xs, ps = shipped_flight(u0, h0_90, 1.0, w_star, +1, T_star, N_OPEN)
bx, by, g = beta_of(B)
bs = math.hypot(*us) / math.sqrt(1 + us[0] ** 2 + us[1] ** 2)
ne = nose_doll(B, m0_90)
results["flights"]["reversal_gamma2"] = {
    "omega": w_star, "T": T_star, "vel_turned_deg": abs(math.degrees(math.atan2(by, bx))),
    "theta_sky_deg": math.degrees(sky), "gamma_final": g,
    "beta_err": abs(math.hypot(bx, by) - bs),
    "vel_dir_err_deg": math.degrees(abs(angle_between((bx, by), us))),
    "nose_err_deg": math.degrees(abs(angle_between(ne, (math.cos(hs), math.sin(hs))))),
    "pos_err_over_path": math.hypot(x[0] - xs[0], x[1] - xs[1]) / path,
}

# step-halving convergence (instrument check)
Bh, _, xh, pathh, skyh, _ = exact_flight(B0, m0_45, 1.0, 0.0, +1, 1.0, N_OPEN // 2)
ush, hsh, xsh, psh = shipped_flight(u0, math.atan2(*reversed(nose_doll(B0, m0_45))), 1.0, 0.0, +1, 1.0, N_OPEN // 2)
results["controls"]["step_halving_sky_deg"] = abs(math.degrees(skyh) - results["flights"]["off45_burn_gamma2"]["theta_sky_final_deg"])
results["controls"]["step_halving_pos"] = abs(math.hypot(xh[0] - xsh[0], xh[1] - xsh[1]) / pathh - results["flights"]["off45_burn_gamma2"]["pos_err_over_path"])
results["timing_s"] = time.time() - t0

with open(__file__.replace("falsifier.py", "results.json"), "w") as f:
    json.dump(results, f, indent=1)

print("closed_form:", json.dumps(results["closed_form"], indent=1))
print("controls:", json.dumps(results["controls"], indent=1))
for b, row in sweep.items():
    print(f"beta {b}: " + " | ".join(
        f"{d}deg: sky={row[d]['sky_deg']:+8.2f} (cf(g-1)psi={row[d]['cf_gm1_deg']:+7.2f}, cf(1-1/g)psi={row[d]['cf_1m1g_deg']:+7.2f}) gamma={row[d]['gamma']:.4f}" for d in row))
for k in ["off45_burn_gamma2", "off135_brake_gamma2", "reversal_gamma2"]:
    print(k, ":", {kk: vv for kk, vv in results["flights"][k].items() if kk != "trajectory"})
print(f"timing {results['timing_s']:.1f}s")
