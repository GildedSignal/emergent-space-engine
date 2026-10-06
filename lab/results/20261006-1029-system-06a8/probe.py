"""Cadence probe: fixed-phase kicks (law's shape) vs conjunction-scheduled pair events.

System-lens question: are the kick cadence and the encounter finder one schedule?
Float replica, heliocentric 2D restricted 3-body (Sun + circular Jupiter + test ships).
Truth: vectorised RK4 tiny step. Every disturbing-acceleration evaluation counts.
"""
import numpy as np, json, sys

GM = 4 * np.pi**2
MU = 1e-3
AP = 5.2
NP_ = np.sqrt(GM / AP**3)

def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(50):
        d = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        E -= d
        if abs(d) < 1e-15:
            break
    return E

def elems_to_state(a, e, w, M):
    E = kepler_E(np.mod(M, 2 * np.pi), e)
    c, s = np.cos(w), np.sin(w)
    sa, ca = np.sin(E), np.cos(E)
    q = np.sqrt(1 - e * e)
    x, y = a * (ca - e), a * q * sa
    n = np.sqrt(GM / a**3)
    den = 1 - e * ca
    vx, vy = -a * n * sa / den, a * n * q * ca / den
    return c * x - s * y, s * x + c * y, c * vx - s * vy, s * vx + c * vy

def state_to_elems(rx, ry, vx, vy):
    r = np.hypot(rx, ry); v2 = vx * vx + vy * vy; rv = rx * vx + ry * vy
    a = 1.0 / (2.0 / r - v2 / GM)
    ex = (v2 / GM - 1 / r) * rx - rv / GM * vx
    ey = (v2 / GM - 1 / r) * ry - rv / GM * vy
    e = np.hypot(ex, ey) + 1e-18
    w = np.arctan2(ey, ex)
    if e >= 0.999:
        return a, e, w, 0.0
    cosf = np.clip((ex * rx + ey * ry) / (e * r), -1, 1)
    sinf = np.clip((ex * ry - ey * rx) / (e * r), -1, 1)
    f = np.arctan2(sinf, cosf)
    E = np.arctan2(np.sqrt(1 - e * e) * np.sin(f), e + np.cos(f))
    M = E - e * np.sin(E)
    return a, e, w, np.mod(M, 2 * np.pi)

def accel(rx, ry, t):
    jx, jy = AP * np.cos(NP_ * t), AP * np.sin(NP_ * t)
    dx, dy = jx - rx, jy - ry
    d3 = (dx * dx + dy * dy) ** 1.5
    return MU * GM * (dx / d3 - jx / AP**3), MU * GM * (dy / d3 - jy / AP**3)

def truth_vec(state, T, h=2.5e-4):
    """state: array (N,4) of rx,ry,vx,vy at t=0. Vectorised RK4."""
    rx, ry, vx, vy = state[:, 0].copy(), state[:, 1].copy(), state[:, 2].copy(), state[:, 3].copy()
    n_steps = int(round(T / h))
    for k in range(n_steps):
        t = k * h
        k1x, k1y = accel_full(rx, ry, t)
        ax, ay = vx + 0.5 * h * k1x, vy + 0.5 * h * k1y
        r2x, r2y = rx + 0.5 * h * vx, ry + 0.5 * h * vy
        k2x, k2y = accel_full(r2x, r2y, t + 0.5 * h)
        v3x, v3y = vx + 0.5 * h * k2x, vy + 0.5 * h * k2y
        r3x, r3y = rx + 0.5 * h * ax, ry + 0.5 * h * ay
        k3x, k3y = accel_full(r3x, r3y, t + 0.5 * h)
        v4x, v4y = vx + h * k3x, vy + h * k3y
        r4x, r4y = rx + h * v3x, ry + h * v3y
        k4x, k4y = accel_full(r4x, r4y, t + h)
        rx += h / 6 * (vx + 2 * ax + 2 * v3x + v4x)
        ry += h / 6 * (vy + 2 * ay + 2 * v3y + v4y)
        vx += h / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        vy += h / 6 * (k1y + 2 * k2y + 2 * k3y + k4y)
    return np.stack([rx, ry, vx, vy], axis=1)


def accel_full(rx, ry, t):
    """Total heliocentric acceleration: Sun (Kepler) + Jupiter perturbation."""
    r3 = (rx * rx + ry * ry) ** 1.5
    px, py = accel(rx, ry, t)
    return px - GM * rx / r3, py - GM * ry / r3
def drift(state, dt):
    rx, ry, vx, vy = state
    a, e, w, M = state_to_elems(rx, ry, vx, vy)
    M = M + np.sqrt(GM / a**3) * dt
    return np.array(elems_to_state(a, e, w, M))

def candA(s0, T, n_per_orbit):
    st = np.array(elems_to_state(*s0)); a0 = s0[0]
    n = np.sqrt(GM / a0**3); dt = (2 * np.pi / n) / n_per_orbit
    steps = int(round(T / dt))
    evals = 1
    rx, ry, vx, vy = st
    ax, ay = accel(rx, ry, 0.0)
    vx += 0.5 * dt * ax; vy += 0.5 * dt * ay
    for k in range(1, steps + 1):
        st = drift((rx, ry, vx, vy), dt)
        rx, ry, vx, vy = st
        ax, ay = accel(rx, ry, k * dt); evals += 1
        if k < steps:
            vx += dt * ax; vy += dt * ay
        else:
            vx += 0.5 * dt * ax; vy += 0.5 * dt * ay
    return state_to_elems(rx, ry, vx, vy), evals

_B = {}
def b32(al):
    key = round(al, 4)
    if key not in _B:
        psi = np.linspace(0, 2 * np.pi, 8192, endpoint=False)
        _B[key] = 2 * float(np.sum(np.cos(psi) / (1 - 2 * al * np.cos(psi) + al**2) ** 1.5)) / 8192
    return _B[key]

def gsec(a, e):
    al = a / AP
    return 0.75 * np.sqrt(GM / a**3) * MU * al * b32(al) / np.sqrt(1 - e * e)

def candB(s0, T, m_sub, Wdeg=30.0, events=True):
    a, e, w, M = s0
    evals = 1  # kernel compile charged once
    t = 0.0
    W = np.radians(Wdeg)
    guard = 0
    while t < T and guard < 400:
        guard += 1
        n_ = np.sqrt(GM / a**3)
        psid = n_ - NP_
        if not events or abs(psid) < 1e-9:
            dt = T - t
            w += gsec(a, e) * dt; M += n_ * dt; t = T
            break
        psi0 = np.mod(w + M - NP_ * t, 2 * np.pi)
        to_c = np.mod(-psi0, 2 * np.pi) / psid if psid > 0 else np.mod(psi0, 2 * np.pi) / (-psid)
        if to_c <= 0:
            to_c += abs(2 * np.pi / psid)
        t_c = t + to_c
        if t_c >= T:
            dt = T - t
            w += gsec(a, e) * dt; M += n_ * dt; t = T
            break
        t_ws = max(t_c - W / abs(psid), t)
        dt = t_ws - t
        if dt > 0:
            w += gsec(a, e) * dt; M += n_ * dt
            evals += 1
        t = t_ws
        t_we = min(t_c + W / abs(psid), T)
        rx, ry, vx, vy = elems_to_state(a, e, w, M)
        hstep = (t_we - t_ws) / m_sub if m_sub > 0 else (t_we - t_ws)
        if m_sub > 0:
            ax, ay = accel(rx, ry, t_ws); evals += 1
            vx += 0.5 * hstep * ax; vy += 0.5 * hstep * ay
            for k in range(1, m_sub + 1):
                rx, ry, vx, vy = drift((rx, ry, vx, vy), hstep)
                ax, ay = accel(rx, ry, t_ws + k * hstep); evals += 1
                f = 1.0 if k < m_sub else 0.5
                vx += f * hstep * ax; vy += f * hstep * ay
        a, e, w, M = state_to_elems(rx, ry, vx, vy)
        t = t_we
    if guard >= 400:
        return (a, e, w, M), -1  # pathology marker
    return (a, e, w, M), evals

def dangle(x):
    return np.mod(x + np.pi, 2 * np.pi) - np.pi

rng = np.random.default_rng(6)
seeds = []
while len(seeds) < 48:
    a = rng.uniform(2.3, 4.4)
    if abs(a - 3.276) < 0.25 or abs(a - 3.97) < 0.2:
        continue
    seeds.append((a, rng.uniform(0.02, 0.3), rng.uniform(0, 2 * np.pi), rng.uniform(0, 2 * np.pi), "nonres"))
for da in (0.0, 0.02, -0.02, 0.04, -0.04, 0.06, -0.06, 0.08):
    for ph in (0.0, np.pi):
        seeds.append((3.276 + da, 0.02, ph, ph * 0.5, "res"))
for i in range(8):
    seeds.append((4.45 + 0.02 * i, rng.uniform(0.02, 0.2), rng.uniform(0, 2 * np.pi), rng.uniform(0, 2 * np.pi), "edge"))

T = 40.0

def run(sub):
    st0 = np.array([elems_to_state(*s[:4]) for s in sub])
    fin = truth_vec(st0, T)
    tr = [state_to_elems(*f) for f in fin]
    res = {"A": {}, "B": {}, "B0": []}
    for n in (4, 8, 16, 32):
        res["A"][n] = [candA(s[:4], T, n) for s in sub]
    for m in (4, 8):
        res["B"][m] = [candB(s[:4], T, m) for s in sub]
    res["B0"] = [candB(s[:4], T, 0, events=False) for s in sub]
    res["Bn"] = [candB(s[:4], T, 2, Wdeg=3.0) for s in sub]
    return tr, res

if __name__ == "__main__":
    quick = "--quick" in sys.argv
    sub = (seeds[:8] + seeds[48:64]) if quick else seeds
    tr, res = run(sub)
    orbits = np.array([T / (2 * np.pi * np.sqrt(s[0]**3 / GM)) for s in sub])
    def band(i):
        return sub[i][4]

    def check(i, els):
        a0, e0, w0, _, _ = sub[i]
        a, e, w = els[0], els[1], els[2]
        ta, te, tw, _ = tr[i]
        if te >= 0.999 or e >= 0.999 or ta <= 0 or a <= 0:
            return (te >= 0.999 or ta <= 0) == (e >= 0.999 or a <= 0)
        dw_tr = dangle(tw - w0)
        okA = abs(a - ta) / ta <= 0.005
        okE = abs(e - te) <= 0.05
        okW = abs(dangle(w - w0) - dw_tr) <= max(0.1, 0.1 * abs(dw_tr))
        return okA and okE and okW
    for key, get in [("A4", lambda i: res["A"][4][i]), ("A8", lambda i: res["A"][8][i]),
                     ("A16", lambda i: res["A"][16][i]), ("A32", lambda i: res["A"][32][i]),
                     ("B4", lambda i: res["B"][4][i]), ("B8", lambda i: res["B"][8][i]),
                     ("Bn", lambda i: res["Bn"][i]), ("B0", lambda i: res["B0"][i])]:
        for b in ("nonres", "res", "edge"):
            idx = [i for i in range(len(sub)) if band(i) == b]
            if not idx:
                continue
            ps = [check(i, get(i)[0]) for i in idx]
            ev = [get(i)[1] / orbits[i] for i in idx]
            print(f"{key},{b},{np.mean(ps):.3f},{np.mean(ev):.2f},{np.median(ev):.2f}")
    print("pump ratios (res band), e_model/e_truth:")
    for key, get in [("A4", lambda i: res["A"][4][i]), ("A8", lambda i: res["A"][8][i]),
                     ("A16", lambda i: res["A"][16][i]), ("B4", lambda i: res["B"][4][i]),
                     ("B8", lambda i: res["B"][8][i]), ("B0", lambda i: res["B0"][i])]:
        rr = [get(i)[0][1] / tr[i][1] for i in range(len(sub)) if band(i) == "res"]
        ok = np.mean([(0.8 <= x <= 1.25) for x in rr])
        print(f"  {key}: median {np.median(rr):.3f}  in-band {ok:.2f}")
    with open(__file__.replace("probe.py", "raw.json"), "w") as f:
        json.dump({"seeds": [list(s) for s in sub],
                   "truth": [[t[0], t[1], t[2]] for t in tr],
                   "res": {k: ({n: [[list(e[0]), e[1]] for e in v] for n, v in val.items()} if isinstance(val, dict) else
                          [[list(e[0]), e[1]] for e in val]) for k, val in res.items()},
                   "orbits": list(orbits)}, f)
    print("wrote raw.json")
