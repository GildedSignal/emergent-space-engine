"""Belt H_live probe: restricted Sun+Jupiter belt, test-particle WH map.

State: (x, y, vx, vy) float64, units AU, yr, G=1, M_sun=1.
Drift: exact Kepler advance under the Sun (universal variables, Newton, 5 iters).
Kick: Jupiter impulse at kick times (Jupiter on exact analytic Kepler orbit).
DKD split: half kick - drift - half kick. Symplectic to O(dt^2) in the interaction.
"""
import sys, time
import numpy as np

MJ = 9.5479438e-4      # Jupiter mass / Sun
AJ, EJ = 5.2, 0.048    # Jupiter a, e
NJ = AJ ** -1.5        # Jupiter mean motion (G=1)

def init_belt(n, seed):
    rng = np.random.default_rng(seed)
    a = rng.uniform(2.2, 3.4, n)
    e = rng.rayleigh(0.05, n)
    w = rng.uniform(0, 2 * np.pi, n)   # periapsis angle
    M = rng.uniform(0, 2 * np.pi, n)   # mean anomaly
    return a, e, w, M
def elements_to_state(a, e, w, M):
    # Kepler -> cartesian (mu=1)
    E = M.copy()
    for _ in range(8):  # Newton on Kepler's eq (e<=0.45)
        E -= (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    r = a * (1 - e * cE)
    xf = a * (cE - e); yf = a * np.sqrt(1 - e * e) * sE      # in orbital frame
    n = a ** -1.5
    vxf = -n * a * a * sE / r
    vyf = n * a * a * np.sqrt(1 - e * e) * cE / r
    cw, sw = np.cos(w), np.sin(w)
    x = xf * cw - yf * sw; y = xf * sw + yf * cw
    vx = vxf * cw - vyf * sw; vy = vxf * sw + vyf * cw
    return x, y, vx, vy

def jupiter_pos(t):
    M = NJ * t
    E = M
    for _ in range(6):
        E -= (E - EJ * np.sin(E) - M) / (1 - EJ * np.cos(E))
    cE, sE = np.cos(E), np.sin(E)
    r = AJ * (1 - EJ * cE)
    x = AJ * (cE - EJ); y = AJ * np.sqrt(1 - EJ ** 2) * sE
    n = NJ
    vx = -n * AJ * AJ * sE / r; vy = n * AJ * AJ * np.sqrt(1 - EJ ** 2) * cE / r
    return x, y, vx, vy

def drift(x, y, vx, vy, dt):
    """Exact Kepler advance (mu=1) by dt via universal variables."""
    r0 = np.sqrt(x * x + y * y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    alpha = 2.0 / r0 - v2          # 1/a
    sqmu = 1.0
    # initial guess (elliptic): chi ~ sqrt(mu)*|alpha|*dt
    chi = np.abs(alpha) * dt
    for _ in range(5):
        z = alpha * chi * chi
        zs = np.sqrt(np.maximum(z, 1e-12))
        C = (1 - np.cos(zs)) / np.maximum(z, 1e-14)
        S = (zs - np.sin(zs)) / np.maximum(z * zs, 1e-14)
        chi2 = chi * chi
        chi3 = chi2 * chi
        F = rv * chi2 * C + (1 - alpha * r0) * chi3 * S + r0 * chi - dt
        dF = rv * chi * (1 - z * S) + (1 - alpha * r0) * chi2 * C + r0
        chi -= F / dF
    z = alpha * chi * chi
    zs = np.sqrt(np.maximum(z, 1e-12))
    C = (1 - np.cos(zs)) / np.maximum(z, 1e-14)
    S = (zs - np.sin(zs)) / np.maximum(z * zs, 1e-14)
    chi2 = chi * chi; chi3 = chi2 * chi
    f = 1 - chi2 / r0 * C
    g = dt - chi3 * S
    xn = f * x + g * vx; yn = f * y + g * vy
    rn = np.sqrt(xn * xn + yn * yn)
    fd = chi * (z * S - 1) / (r0 * rn)
    gd = 1 - chi2 / rn * C
    return xn, yn, fd * x + gd * vx, fd * y + gd * vy

def kick(x, y, vx, vy, xj, yj, half):
    dx = xj - x; dy = yj - y
    d3 = (dx * dx + dy * dy) ** 1.5
    ax = -MJ * dx / d3; ay = -MJ * dy / d3   # attraction toward Jupiter
    return vx + ax * half, vy + ay * half

def run(prefix, n=2000, seed=1, jup=True, t0=0.0, steps=1000, dt=0.185, snap_every=8192,
        state=None):
    if state is None:
        a, e, w, M = init_belt(n, seed)
        x, y, vx, vy = elements_to_state(a, e, w, M)
        t0 = 0.0
    else:
        x, y, vx, vy, t0 = state
    h = dt if jup else dt * 0  # no-Jupiter control: pure drift
    out = {k: [] for k in ("a", "e", "ex", "ey", "M")}
    meta = []
    t = t0
    t_start = time.time()
    for i in range(steps):
        if jup:
            xj, yj, _, _ = jupiter_pos(t + 0.5 * dt)
            vx, vy = kick(x, y, vx, vy, xj, yj, 0.5 * dt)
        x, y, vx, vy = drift(x, y, vx, vy, dt if jup else dt)
        if jup:
            xj, yj, _, _ = jupiter_pos(t + dt)
            vx, vy = kick(x, y, vx, vy, xj, yj, 0.5 * dt)
        t += dt
        if (i + 1) % snap_every == 0 or i == steps - 1:
            r = np.sqrt(x * x + y * y); v2 = vx * vx + vy * vy
            a_ = 1.0 / (2.0 / r - v2)
            rv = x * vx + y * vy
            exv = (v2 - 1.0 / r) * x - rv * vx
            eyv = (v2 - 1.0 / r) * y - rv * vy
            ev = np.hypot(exv, eyv)
            out["a"].append(a_.astype(np.float32)); out["e"].append(ev.astype(np.float32))
            out["ex"].append(exv.astype(np.float32)); out["ey"].append(eyv.astype(np.float32))
            meta.append(t)
    np.savez(prefix + "-snap.npz", meta=np.array(meta, dtype=np.float32),
             **{k: np.array(v) for k, v in out.items()})
    np.savez(prefix + "-state.npz", x=x, y=y, vx=vx, vy=vy, t=t)
    return t, time.time() - t_start

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("prefix"); p.add_argument("--steps", type=int, required=True)
    p.add_argument("--seed", type=int, default=1); p.add_argument("--nojup", action="store_true")
    p.add_argument("--resume", default=""); p.add_argument("--dt", type=float, default=0.185)
    p.add_argument("--n", type=int, default=2000)
    A = p.parse_args()
    state = None
    if A.resume:
        s = np.load(A.resume)
        state = (s["x"], s["y"], s["vx"], s["vy"], float(s["t"]))
    t, w = run(A.prefix, n=A.n, seed=A.seed, jup=not A.nojup, steps=A.steps,
               dt=A.dt, state=state)
    print(f"{A.prefix}: t={t:.1f} yr steps={A.steps} wall={w:.1f}s")
