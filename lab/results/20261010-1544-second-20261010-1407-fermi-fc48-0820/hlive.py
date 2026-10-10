#!/usr/bin/env python3
"""H_live of a belt under conjunction kicks, measured at the tube's own quanta. v2

v2 fixes: entropies measured by coarse-graining (factor B) then adding log2(B)
back, so they are not capacity-capped at log2(N); hist_bits no longer
double-counts log2(nbins); t_p mod-cycle capped at the 64-bit field;
sorted-floor uses (a, e_vec) only (periapsis angle is derived from e_vec).

Belt: the repo's own spec (crates/encounters/src/belt.rs): a ~ U[1, 1.5] AU,
Rayleigh e, sigma_e = 0.01. Perturber: Jupiter, a_J = 5.2 AU, m_J = 9.55e-4.
Kick at each synodic conjunction: dv_r = 2 G m_J/(v_rel d), radial.
Quanta from the tube spec (docs/law.md line 12): E, L 32-bit over the belt's
ranges; periapsis angle 32-bit; periapsis time 64-bit per radial cycle.
"""
import json
import numpy as np

rng = np.random.default_rng(20261010)

N = 65536
A_LO, A_HI = 1.0, 1.5
SIGMA_E = 0.01
A_J = 5.2
GMJ = 4 * np.pi**2 * 9.55e-4
DT = 0.05
P_REF = 1.2**1.5
T_ORBITS = 1024

a0 = rng.uniform(A_LO, A_HI, N)
ex0 = rng.normal(0, SIGMA_E, N)
ey0 = rng.normal(0, SIGMA_E, N)
a, ex, ey = a0.copy(), ex0.copy(), ey0.copy()
M = rng.uniform(0, 2 * np.pi, N)
psi = rng.uniform(0, 2 * np.pi, N)
n0 = 2 * np.pi * a0**-1.5
nJ = 2 * np.pi * A_J**-1.5
Phi = np.zeros(N)
kicks = np.zeros(N, dtype=np.int64)

Q_A = 2 * 1.2**2 / (6 * 2**32)                  # E-quantum in a-units
Q_L = (np.sqrt(1.5) - np.sqrt(0.75)) / 2**32    # L-quantum
Q_W = 2 * np.pi / 2**32                          # periapsis-angle quantum
BA, BL = 1 << 18, 1 << 24                        # coarse-grain factors

def ent_cg(x, q, B):
    """Entropy of x at quantum q, measured at q*B then +log2(B)."""
    _, c = np.unique(np.round(x / (q * B)).astype(np.int64), return_counts=True)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum() + np.log2(B))

def ent2_cg(x, y, qx, qy, B):
    kx = np.round(x / (qx * B)).astype(np.int64)
    ky = np.round(y / (qy * B)).astype(np.int64)
    _, c = np.unique(kx * (1 << 26) + ky, return_counts=True)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum() + 2 * np.log2(B))

rows = []
t, next_meas = 0.0, 1.0
while t < T_ORBITS * P_REF:
    n = 2 * np.pi * a**-1.5
    psi += (n - nJ) * DT
    hit = psi >= 2 * np.pi
    Phi += (n - n0) * DT
    if hit.any():
        idx = np.nonzero(hit)[0]
        e_idx = np.hypot(ex[idx], ey[idx])
        Mc = M[idx]
        f = Mc + 2 * e_idx * np.sin(Mc)
        d = A_J - a[idx] * (1 - e_idx * np.cos(Mc))
        vr = 2 * np.pi * (a[idx]**-0.5 - A_J**-0.5)
        q = (2 * GMJ / (vr * d)) / (2 * np.pi / np.sqrt(a[idx]))
        sinf, cosf = np.sin(f), np.cos(f)
        ex[idx] += q * sinf
        ey[idx] += -q * cosf
        a[idx] *= 1 + 2 * e_idx * sinf * q
        kicks[idx] += 1
        psi[hit] -= 2 * np.pi
    M = (M + n * DT) % (2 * np.pi)
    t += DT
    if t / P_REF >= next_meas - 1e-9:
        torb = t / P_REF
        e_cur = np.hypot(ex, ey)
        da = a - a0
        dex, dey = ex - ex0, ey - ey0
        dL = np.sqrt(a) * (ex * dex + ey * dey) / np.maximum(e_cur, 1e-300) \
             / np.sqrt(np.maximum(1 - e_cur**2, 1e-9))
        dw = (np.arctan2(ey, ex) - np.arctan2(ey0, ex0)) % (2 * np.pi)
        above = (np.abs(da) > Q_A) | (np.abs(dL) > Q_L) | (dw > Q_W)
        H_a = ent_cg(da, Q_A, BA)
        H_L = ent_cg(dL, Q_L, BL)
        H_w = ent_cg(np.where(dw > np.pi, dw - 2 * np.pi, dw), Q_W, BL)
        H_Lw = ent2_cg(dL, np.where(dw > np.pi, dw - 2 * np.pi, dw), Q_L, Q_W, BL)
        abin = np.clip((a0 * 64).astype(int) - 64, 0, 63)
        keys = np.round(dL / (Q_L * BL)).astype(np.int64) * (1 << 26) + \
               np.round(np.where(dw > np.pi, dw - 2 * np.pi, dw) / (Q_W * BL)).astype(np.int64)
        H_cond = 0.0
        for b in range(64):
            m = abin == b
            if m.sum() > 8:
                _, c = np.unique(keys[m], return_counts=True)
                p = c / c.sum()
                H_cond += (m.sum() / N) * float(-(p * np.log2(p)).sum() + 2 * np.log2(BL))
        # t_p: mean-anomaly divergence; mod-cycle at 64-bit field (cap 64)
        h, _ = np.histogram(Phi % (2 * np.pi), bins=1 << 12, range=(0, 2 * np.pi))
        p = h.astype(float); p = p[p > 0] / p.sum()
        H_tp_mod = min(float(-(p * np.log2(p)).sum() + np.log2(2**64 / (1 << 12))), 64.0)
        hr, _ = np.histogram(Phi, bins=1 << 12, range=(0, max(Phi.max(), 1e-3)))
        pr = hr.astype(float); pr = pr[pr > 0] / pr.sum()
        H_tp_raw = float(-(pr * np.log2(pr)).sum() + np.log2(2**64 / (1 << 12)))
        rows.append(dict(orbits=round(torb, 3), frac_kicked=float(above.mean()),
                         kicks_per_body_orbit=float(kicks.sum() / N / torb),
                         sigma_e=float(np.std(e_cur)),
                         H_a=H_a, H_L=H_L, H_w=H_w, H_Lw=H_Lw, H_cond_Lw=H_cond,
                         H_tp_mod=H_tp_mod, H_tp_raw=H_tp_raw,
                         fields=H_a + H_Lw + H_tp_mod))
        next_meas *= 2
        if next_meas > T_ORBITS:
            break

fit = [r for r in rows if r["orbits"] >= 8]
if len(fit) >= 2:  # quick path (T_ORBITS < 8) has no t>=8 rows: no slope fit
    x = np.log2([r["orbits"] for r in fit])
    y = [r["fields"] for r in fit]
    slope = float(np.polyfit(x, y, 1)[0])
else:
    slope = None

# sorted-microstate floor (any exact encoding of a generic microstate), bits/body:
# iid on the (a, e_vec) grid at tube quanta: H@q summed - log2(N) + log2(e)
def floor_bits(av, exv, eyv):
    h, _ = np.histogram(av, bins=1 << 10, range=(A_LO, A_HI))
    p = h.astype(float); p = p[p > 0] / p.sum()
    H_a_at_q = float(-(p * np.log2(p)).sum() + np.log2((A_HI - A_LO) / (1 << 10) / Q_A))
    qe = Q_L / np.sqrt(1.2)
    H_e2d = ent2_cg(exv, eyv, qe, qe, 1 << 16)
    return H_a_at_q + H_e2d - np.log2(N) + np.log2(np.e)

floor_birth = floor_bits(a0, ex0, ey0)
floor_final = floor_bits(a, ex, ey)
np.savez("final_state.npz", a=a, ex=ex, ey=ey, a0=a0, ex0=ex0, ey0=ey0,
         Phi=Phi, kicks=kicks)

out = dict(N=N, rows=rows, slope_bits_per_doubling=slope, Q_A=Q_A, Q_L=Q_L,
           floor_birth=floor_birth, floor_final=floor_final,
           final_sigma_e=float(np.std(np.hypot(ex, ey))),
           final_kicks_per_body=float(kicks.mean()))
with open("hlive.json", "w") as f:
    json.dump(out, f, indent=1)

print(f"{'orbits':>7} {'f_kick':>6} {'k/orb':>5} {'sig_e':>7} {'H_a':>5} {'H_L':>5} "
      f"{'H_w':>5} {'H_Lw':>5} {'Hcond':>5} {'Htpm':>5} {'Htpr':>6} {'fields':>6}")
for r in rows:
    print(f"{r['orbits']:7.1f} {r['frac_kicked']:6.3f} {r['kicks_per_body_orbit']:5.2f} "
          f"{r['sigma_e']:7.4f} {r['H_a']:5.1f} {r['H_L']:5.1f} {r['H_w']:5.1f} {r['H_Lw']:5.1f} "
          f"{r['H_cond_Lw']:5.1f} {r['H_tp_mod']:5.1f} {r['H_tp_raw']:6.1f} {r['fields']:6.1f}")
print(f"slope (field bits per doubling of t, t>=8): "
      f"{'n/a (T_ORBITS < 8)' if slope is None else f'{slope:.2f}'}")
print(f"sorted floor: birth {floor_birth:.1f}, final {floor_final:.1f} bits/body "
      f"(sigma_e {out['final_sigma_e']:.4f}, kicks/body {out['final_kicks_per_body']:.0f})")
