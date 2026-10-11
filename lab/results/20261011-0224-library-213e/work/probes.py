"""Probe A (fit-cadence) + Probe B (conjunction scheduling from elements).
Run 20261011-0224-library-213e. numpy only. Truth = dense evaluation.

A: JPL practice — degree-10 Chebyshev fit of the tidal perturbation per window,
   windows uniform in t vs uniform in true anomaly f (Sundman stretch).
B: conjunction times & miss distances for two eccentric orbits from elements only.
"""
import numpy as np

P = 2 * np.pi
rng = np.random.default_rng(7)

def kepler_E(M, e):
    E = M.copy()
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def f_of_M(M, e):
    E = kepler_E(M, e)
    return 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))

def M_of_f(f, e):
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(f / 2), np.sqrt(1 + e) * np.cos(f / 2))
    return E - e * np.sin(E)

# ---------- Probe A ----------
def tide_t(t, e, cw=1.7, ph=0.3):
    """tidal term 3cos^2(lam - cw*t - ph) at time t (n=1)."""
    lam = f_of_M(np.mod(t, P), e)
    return 3 * np.cos(lam - cw * t - ph) ** 2 - 1.0

def tide_f(f, e, cw=1.7, ph=0.3):
    """same signal parametrized by true anomaly f (unwrapped across orbits)."""
    j = np.floor(f / P)
    fr = f - j * P
    t = M_of_f(fr, e) + j * P
    return 3 * np.cos(fr - cw * t - ph) ** 2 - 1.0

def probe_A(e, var, deg=10, norbits=4, quantum=1e-6):
    sig = tide_t if var == "t" else tide_f
    span = norbits * P
    xspan = span  # in either variable one orbit covers 2*pi
    xd = np.linspace(0, xspan, 300000)
    yd = sig(xd, e)
    ymax = np.max(np.abs(yd))
    for Wfrac in [1.0, 0.5, 1/3, 0.25, 0.2, 1/6, 0.125, 0.1, 1/12, 1/16, 1/24, 1/32, 1/64]:
        W = Wfrac * P
        nfits = int(np.ceil(span / W))
        maxerr, cert = 0.0, 0.0
        for k in range(nfits):
            a, b = k * W, min((k + 1) * W, span)
            nodes = np.cos(np.pi * (np.arange(deg + 1) + 0.5) / (deg + 1))
            xn = 0.5 * (a + b) + 0.5 * (b - a) * nodes
            yn = sig(xn, e)
            c = np.polynomial.chebyshev.chebfit(nodes, yn, deg)
            xs = np.linspace(a, b, 500)
            ys = sig(xs, e)
            xm = (2 * xs - (a + b)) / (b - a)
            err = np.max(np.abs(np.polynomial.chebyshev.chebval(xm, c) - ys))
            maxerr = max(maxerr, err / ymax)
            cert = max(cert, max(abs(c[-1]), abs(c[-2])) / (np.max(np.abs(c)) + 1e-300))
        if maxerr < quantum:
            return dict(e=e, var=var, W=Wfrac, fits_per_orbit=nfits / norbits,
                        evals_per_orbit=(deg + 1) * nfits / norbits,
                        maxerr=maxerr, cert=cert)
    return None

print("=== A: deg=10 Chebyshev, quantum=1e-6 relative, windows in t vs in f ===")
for e in [0.0, 0.3, 0.7]:
    for var in ["t", "f"]:
        print(f"e={e} var={var}:", probe_A(e, var))
print("=== A4 held-out: extra harmonics via cw=3.4 (faster companion) ===")
tide_t_h = lambda t, e: tide_t(t, e, cw=3.4)
tide_f_h = lambda f, e: tide_f(f, e, cw=3.4)
globals()['tide_t'], globals()['tide_f'] = tide_t, tide_f
for var in ["t", "f"]:
    r = None
    # temporarily swap signal
    import types
    def run(var):
        sigmap = {"t": (lambda x, e: tide_t_h(x, e)), "f": (lambda x, e: tide_f_h(x, e))}
        sig = sigmap[var]
        span = 4 * P
        yd = sig(np.linspace(0, span, 300000), 0.3)
        ymax = np.max(np.abs(yd)); deg = 10
        for Wfrac in [1.0, 0.5, 1/3, 0.25, 0.2, 1/6, 0.125, 0.1, 1/12, 1/16, 1/24]:
            W = Wfrac * P; nfits = int(np.ceil(span / W)); maxerr = 0.0
            for k in range(nfits):
                a, b = k * W, min((k + 1) * W, span)
                nodes = np.cos(np.pi * (np.arange(deg + 1) + 0.5) / (deg + 1))
                xn = 0.5 * (a + b) + 0.5 * (b - a) * nodes
                c = np.polynomial.chebyshev.chebfit(nodes, sig(xn, 0.3), deg)
                xs = np.linspace(a, b, 500)
                xm = (2 * xs - (a + b)) / (b - a)
                err = np.max(np.abs(np.polynomial.chebyshev.chebval(xm, c) - sig(xs, 0.3)))
                maxerr = max(maxerr, err / ymax)
            if maxerr < 1e-6:
                return dict(var=var, W=Wfrac, fits_per_orbit=nfits/4, evals_per_orbit=(deg+1)*nfits/4, maxerr=maxerr)
        return None
    print("cw=3.4 e=0.3", var, run(var))

# ---------- Probe B ----------
def orbit(t, a, e, n, wbar):
    M = n * t
    f = f_of_M(np.mod(M, P), e)
    lam = f + wbar
    r = a * (1 - e ** 2) / (1 + e * np.cos(f))
    return lam, r

def conjunctions(a1, e1, n1, w1, a2, e2, n2, w2, T):
    t = np.linspace(0, T, 400000)
    l1, r1 = orbit(t, a1, e1, n1, w1)
    l2, r2 = orbit(t, a2, e2, n2, w2)
    d = np.unwrap(l1 - l2)
    ks = np.where(np.diff(np.floor(d / P)) != 0)[0]
    # refine by linear interp
    out = []
    for i in ks:
        d0, d1 = d[i], d[i + 1]
        # crossing of next multiple of 2pi between i and i+1
        m = np.ceil(d0 / P)
        tc = t[i] + (m * P - d0) / (d1 - d0) * (t[i + 1] - t[i])
        lam1, rr1 = orbit(np.array([tc]), a1, e1, n1, w1)
        lam2, rr2 = orbit(np.array([tc]), a2, e2, n2, w2)
        out.append((float(tc), abs(rr1[0] - rr2[0])))
    return np.array(out)

print("\n=== B: conjunction scheduling from elements ===")
def two_freq_predict(delta, half=None):
    K = len(delta)
    if half is None:
        half = K // 2
    k = np.arange(half)
    F = np.fft.rfft(delta[:half] - delta[:half].mean())
    freqs = np.fft.rfftfreq(half)
    idx = np.argsort(np.abs(F))[::-1][:2]
    freqs_sel = freqs[idx]
    # least squares on sin/cos of selected freqs + const
    def design(kk):
        cols = [np.ones_like(kk)]
        for fr in freqs_sel:
            cols += [np.cos(2 * np.pi * fr * kk), np.sin(2 * np.pi * fr * kk)]
        return np.stack(cols, 1)
    A = design(k)
    coef, *_ = np.linalg.lstsq(A, delta[:half], rcond=None)
    kk = np.arange(K)
    return design(kk) @ coef

cases = [
    ("e=0.1 ratio=0.83", dict(a1=1.0, e1=0.1, n1=1.0, w1=0.0, a2=1.6, e2=0.1, n2=0.83, w2=1.0)),
    ("e=0.3 ratio=0.83", dict(a1=1.0, e1=0.3, n1=1.0, w1=0.0, a2=1.8, e2=0.2, n2=0.83, w2=1.0)),
    ("e=0.7 ratio=0.83", dict(a1=1.0, e1=0.7, n1=1.0, w1=0.0, a2=2.6, e2=0.2, n2=0.83, w2=1.0)),
    ("near 7:6 detuned 1e-3", dict(a1=1.0, e1=0.1, n1=1.0, w1=0.0, a2=1.3, e2=0.1, n2=6/7 + 1e-3, w2=1.0)),
]
for name, kw in cases:
    cj = conjunctions(T=400 * P, **kw)
    t_k, d_k = cj[:, 0], cj[:, 1]
    Tb = P / abs(kw["n1"] - kw["n2"])
    kk = np.round(t_k / Tb).astype(int)
    terr = np.abs(t_k - kk * Tb) / Tb
    n1c = len(t_k) // 2
    pred = two_freq_predict(d_k)
    derr = np.max(np.abs(pred[n1c:] - d_k[n1c:])) / (np.std(d_k) + 1e-300)
    print(f"{name}: K={len(t_k)} beats/conj ratio max|t_k-kTb|/Tb={terr.max():.2e} "
          f"half2 missdist 2-freq max err/std={derr:.3f} delta_amp={d_k.std():.3f}")

# exact commensurability control
cj = conjunctions(1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, T=100 * P)
print("exact commensurate (n1=n2, e=0): conjunctions found =", len(cj), "(degenerate as expected)")
