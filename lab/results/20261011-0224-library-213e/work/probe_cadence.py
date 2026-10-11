"""Probe A (fit-cadence) + Probe B (conjunction scheduling from elements).
Library-lens run 20261011-0224-library-213e. numpy only."""
import json
import numpy as np

P = 2 * np.pi

def kepler_E(M, e, it=50):
    E = M.copy()
    for _ in range(it):  # Newton
        f = E - e * np.sin(E) - M
        E = E - f / (1 - e * np.cos(E))
    return E

def true_anom(M, e):
    E = kepler_E(M, e)
    return 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))

def tide(t, e, ad_ratio, comp_w, phase=0.3):
    """Quadrupole tide accel from a circular companion, projected on radial unit:
    a_tide ~ (3 cos^2(psi) - 1) where psi = angle between r and companion dir.
    Scale-free: we track the relative shape of the tidal term in time."""
    M = t  # mean anomaly (n=1) if t is in units of orbital phase
    f = true_anom(M, e)
    lam = f + 2 * np.arctan2(e * np.sin(f), 1 + e * np.cos(f))  # true longitude (arg=0)
    psi = lam - (comp_w * t + phase)
    return 3 * np.cos(psi) ** 2 - 1.0, lam

def fit_windows(e, ad_ratio, var="M", deg=10, norbits=4, quantum=1e-6):
    """Fit degree-d Chebyshev per window; return fits/orbit to hold quantum."""
    ts = np.linspace(0, norbits * P, 200000)
    M = ts % P  # mean anomaly; tide sampled at (t, M) pairs: sample dense truth first
    # truth signal in time
    def signal(tt):
        s, _ = tide(tt % P if var == "M" else tt, e, ad_ratio, comp_w=1.7)
        # for var == "M": treat M as the independent var, t = M (n=1)
        return s
    y = signal(ts)
    amp = y.std()
    out = {}
    for Wfrac in [1.0, 0.5, 1/3, 0.25, 0.2, 1/6, 1/8, 0.1, 1/12, 1/16, 1/24, 1/32, 1/64]:
        W = Wfrac * P
        nfits = int(np.ceil(norbits * P / W))
        maxerr = 0.0
        cert = 0.0
        for k in range(nfits):
            a, b = k * W, min((k + 1) * W, norbits * P)
            nodes = np.cos(np.pi * (np.arange(deg + 1) + 0.5) / (deg + 1))  # Cheb nodes
            xn = 0.5 * (a + b) + 0.5 * (b - a) * nodes
            yn = signal(xn)
            c = np.polynomial.chebyshev.chebfit(nodes, yn, deg)
            xd = np.linspace(a, b, 400)
            yd = signal(xd)
            yf = np.polynomial.chebyshev.chebval(nodes, np.polynomial.chebyshev.chebfit(nodes, yn, deg), )
            # evaluate fit via interpolation on nodes using barycentric? simpler: chebval at mapped x
            xm = (2 * xd - (a + b)) / (b - a)
            yfit = np.polynomial.chebyshev.chebval(xm, c)
            err = np.max(np.abs(yfit - yd)) / np.max(np.abs(y))
            maxerr = max(maxerr, err)
            cert = max(cert, max(abs(c[-1]), abs(c[-2])) / (np.max(np.abs(c)) + 1e-300))
        out[Wfrac] = (maxerr, cert, nfits / norbits)
        if maxerr < quantum:
            return dict(e=e, var=var, deg=deg, Wfrac=Wfrac, fits_per_orbit=nfits / norbits,
                        evals_per_orbit=(deg + 1) * nfits / norbits, maxerr=maxerr, cert=cert)
    return None

print("=== Probe A: fits/orbit at deg=10, quantum=1e-6 (relative) ===")
A = {}
for e in [0.0, 0.3, 0.7]:
    for var in ["M", "t"]:
        # var "t": non-uniform-in-t signal => emulate by evaluating tide at raw t (n=1 same but
        # the signal's time-compression at pericenter matters only through sampling var).
        # We approximate the distinction: 't' windows are equal length in time (as here),
        # 'M' windows would be equal length in mean anomaly. With n=1 and no drift the
        # signal s(t) itself is what we fit; the variable choice is realized by fitting
        # s as a function of M instead of t: s(M). Since t = M here for the primary,
        # we differentiate by adding pericenter pile-up: fit in M is exact reparam.
        r = fit_windows(e, 0.05, var=var)
        A[(e, var)] = r
        print(f"e={e} var={var}: {r}")
print()
print("=== Probe A, held-out A4: stronger tide a/d=0.02 at e=0.3 ===")
print(fit_windows(0.3, 0.02, var="M"))
print(fit_windows(0.3, 0.02, var="t"))
