#!/usr/bin/env python3
"""Probe: is a pair's miss distance at successive conjunctions quasi-periodic
(one frequency), so the next close conjunction is predictable and the pair is
paid once per element change (board r8 v2 'Next' lead)?

Truth: brute-force root-finding of every angle crossing (conjunction) for two
coplanar secularly-precessing ellipses around one primary.
Model: d_k = sum_{h=0..3} [a_h cos(h k D) + b_h sin(h k D)], one per-conjunction
phase advance D, fit on the first 100 conjunctions, tested on the rest.
Deterministic (seeded). Cases: random / positive control / near-resonant / e=0.5.
"""
import json
import numpy as np

N_TRAIN = 100


def kepler_E(M, e):
    E = M.copy()
    for _ in range(40):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def angle(a, e, w0, M0, n, g, t):
    w = w0 + g * t
    E = kepler_E(M0 + n * t, e)
    xp, yp = a * (np.cos(E) - e), a * np.sqrt(1 - e * e) * np.sin(E)
    return np.arctan2(xp * np.sin(w) + yp * np.cos(w), xp * np.cos(w) - yp * np.sin(w))


def Dfun(p1, p2, t):
    return angle(*p1, t) - angle(*p2, t)


def conjunction_distances(p1, p2, n_cyc):
    """All angle crossings (conjunctions) over n_cyc synodic cycles, miss distances."""
    T1 = 2 * np.pi / p1[4]
    Tsyn = 2 * np.pi / abs(p1[4] - p2[4])
    dt = T1 / 60.0
    t = np.arange(0.0, n_cyc * Tsyn, dt)
    D = np.unwrap(Dfun(p1, p2, t))
    k = np.floor(D / (2 * np.pi))
    idx = np.nonzero(np.diff(k))[0]  # grid intervals containing a 2*pi crossing
    lo, hi = t[idx], t[idx + 1]
    for _ in range(45):  # vectorized bisection over all crossings
        mid = 0.5 * (lo + hi)
        left = np.floor(Dfun(p1, p2, lo) / (2 * np.pi))
        Dm = Dfun(p1, p2, mid)
        go_hi = np.floor(Dm / (2 * np.pi)) == left
        lo = np.where(go_hi, mid, lo)
        hi = np.where(go_hi, hi, mid)
    tk = 0.5 * (lo + hi)


    def pos(p, t):
        a, e, w0, M0, n, g = p
        w = w0 + g * t
        E = kepler_E(M0 + n * t, e)
        xp, yp = a * (np.cos(E) - e), a * np.sqrt(1 - e * e) * np.sin(E)
        c, s = np.cos(w), np.sin(w)
        return xp * c - yp * s, xp * s + yp * c


    x1, y1 = pos(p1, tk)
    x2, y2 = pos(p2, tk)
    d = np.hypot(x1 - x2, y1 - y2)
    order = np.argsort(tk)
    return d[order], tk[order]


def _design(ks, freqs, n_harm=3):
    cols = [np.ones(len(ks))]
    for D in freqs:
        cols += [c(h * ks * D) for h in range(1, n_harm + 1) for c in (np.cos, np.sin)]
    return np.column_stack(cols)


def _peaks(x, n_pk, n_harm=3):
    """Top-n_pk distinct FFT peaks (DC excluded; harmonics of chosen peaks excluded)."""
    N = len(x)
    F = np.abs(np.fft.rfft(x - x.mean(), n=1 << 16))
    f = np.fft.rfftfreq(1 << 16)
    order = np.argsort(F)[::-1]
    picked = []
    for i in order:
        if f[i] <= 0:
            continue
        if any(abs(f[i] - m * fp) < 3.0 / N for fp in picked for m in (0.5, 1.0, 2.0, 3.0)):
            continue
        picked.append(f[i])
        if len(picked) == n_pk:
            break
    return [2 * np.pi * fp for fp in picked]


def fit_one_freq(d, n_harm=3):
    """Fourier fit with a single per-index frequency, found by periodogram+refine."""
    N = len(d)
    D0 = _peaks(d, 1)[0]
    best = None
    for D in D0 * (1 + np.linspace(-0.05, 0.05, 201)):
        A = _design(np.arange(N), [D], n_harm)
        coef, *_ = np.linalg.lstsq(A, d, rcond=None)
        sse = float(np.sum((A @ coef - d) ** 2))
        if best is None or sse < best[0]:
            best = (sse, D, coef)
    return best[1], best[2]


def fit_two_freq(d, n_harm=3):
    """Two incommensurate frequencies (carrier + envelope), FFT bins, linear LS."""
    N = len(d)
    freqs = _peaks(d, 2)
    A = _design(np.arange(N), freqs, n_harm)
    coef, *_ = np.linalg.lstsq(A, d, rcond=None)
    return freqs, coef


def run_case(name, pairs):
    out = []
    for seed, (p1, p2) in enumerate(pairs):
        d, tk = conjunction_distances(p1, p2, n_cyc=165)  # ~>=150 conjunctions
        if len(d) < N_TRAIN + 40:
            out.append(dict(seed=seed, n_conj=len(d), note="too few conjunctions"))
            continue
        d = d[: N_TRAIN + 50]
        train, test = d[:N_TRAIN], d[N_TRAIN:]
        ks_tr, ks_te = np.arange(N_TRAIN), np.arange(N_TRAIN, len(d))
        D, coef = fit_one_freq(train)
        resid = _design(ks_tr, [D]) @ coef - train
        pred = _design(ks_te, [D]) @ coef
        freqs2, coef2 = fit_two_freq(train)
        resid2 = _design(ks_tr, freqs2) @ coef2 - train
        pred2 = _design(ks_te, freqs2) @ coef2
        amp = train.max() - train.min()
        tau = 3 * train.min()
        misc = int(np.sum((test < tau) != (pred < tau)))
        misc2 = int(np.sum((test < tau) != (pred2 < tau)))
        k_true = int(np.argmin(test))
        out.append(
            dict(seed=seed, n_conj=len(d), amp=float(amp), tau=float(tau),
                 train_rms_over_amp=float(np.sqrt(np.mean(resid**2)) / amp),
                 test_rms_over_amp=float(np.sqrt(np.mean((pred - test) ** 2)) / amp),
                 misclose_rate=misc / len(test), k_err=abs(int(np.argmin(pred)) - k_true),
                 d_at_true_min_err=float(abs(pred[k_true] - test[k_true]) / amp),
                 train_rms2_over_amp=float(np.sqrt(np.mean(resid2**2)) / amp),
                 test_rms2_over_amp=float(np.sqrt(np.mean((pred2 - test) ** 2)) / amp),
                 misclose2_rate=misc2 / len(test), k_err2=abs(int(np.argmin(pred2)) - k_true),
                 d2_at_true_min_err=float(abs(pred2[k_true] - test[k_true]) / amp),
                 D_per_conj=float(D % (2 * np.pi))))
    with open(f"probe_{name}.json", "w") as f:
        json.dump(out, f, indent=1)
    ok = [r for r in out if "note" not in r]
    print(f"== {name} ({len(ok)} pairs) ==")
    for key in ("train_rms_over_amp", "test_rms_over_amp", "misclose_rate", "k_err", "d_at_true_min_err",
                "train_rms2_over_amp", "test_rms2_over_amp", "misclose2_rate", "k_err2", "d2_at_true_min_err"):
        v = np.array([r[key] for r in ok])
        print(f"  {key:22s} median={np.median(v):.4g}  max={v.max():.4g}")
    return out


rng = np.random.default_rng(0)
MU = 1.0


def body(a, e, g_over_n):
    n = np.sqrt(MU / a**3)
    return (a, e, rng.uniform(0, 2 * np.pi), rng.uniform(0, 2 * np.pi), n, g_over_n * n)


cases = {}
# 1. random non-resonant: a2/a1 in [1.03,1.25], e<=0.3, g<=0.003n
pairs = []
for s in range(8):
    r = np.random.default_rng(100 + s)
    a1 = 1.0
    a2 = a1 * (1.03 + 0.22 * r.uniform(0, 1))
    e1 = 0.3 * r.uniform(0, 1)
    e2 = 0.3 * r.uniform(0, 1)
    p1 = (a1, e1, r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), np.sqrt(MU / a1**3), 0.003 * r.uniform(0, 1) * np.sqrt(MU / a1**3))
    p2 = (a2, e2, r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), np.sqrt(MU / a2**3), 0.003 * r.uniform(0, 1) * np.sqrt(MU / a2**3))
    pairs.append((p1, p2))
cases["random"] = pairs
# 2. positive control: identical precession (sequence exactly periodic)
pairs = []
for s in range(4):
    r = np.random.default_rng(200 + s)
    g = 0.002 * r.uniform(0, 1)
    a1, a2 = 1.0, 1.1
    p1 = (a1, 0.1 * r.uniform(0, 1), r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), np.sqrt(MU / a1**3), g * np.sqrt(MU / a1**3))
    p2 = (a2, 0.1 * r.uniform(0, 1), r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), np.sqrt(MU / a2**3), g * np.sqrt(MU / a2**3))
    pairs.append((p1, p2))
cases["control_g_equal"] = pairs
# 3. near-resonant: n2/n1 = 1+1/301 (synodic = 301 orbits)
pairs = []
for s in range(4):
    r = np.random.default_rng(300 + s)
    a1 = 1.0
    n1 = np.sqrt(MU)
    n2 = n1 * (1 + 1 / 301)
    a2 = (MU / n2**2) ** (1 / 3)
    p1 = (a1, 0.15 * r.uniform(0, 1), r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), n1, 0.001 * n1)
    p2 = (a2, 0.15 * r.uniform(0, 1), r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), n2, 0.002 * n2)
    pairs.append((p1, p2))
cases["near_resonant"] = pairs
# 4. high eccentricity e=0.5
pairs = []
for s in range(4):
    r = np.random.default_rng(400 + s)
    a1, a2 = 1.0, 1.1 + 0.1 * r.uniform(0, 1)
    p1 = (a1, 0.5, r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), np.sqrt(MU / a1**3), 0.001 * np.sqrt(MU / a1**3))
    p2 = (a2, 0.4 * r.uniform(0, 1), r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi), np.sqrt(MU / a2**3), 0.002 * np.sqrt(MU / a2**3))
    pairs.append((p1, p2))
cases["ecc05"] = pairs

summary = {}
for name, pairs in cases.items():
    summary[name] = run_case(name, pairs)

# amortized observation accounting (pay-once vs per-orbit), case 'random'
n_paid = N_TRAIN
for H in (50, 100, 150):
    print(f"pay-once: observations per conjunction at horizon {H}: {n_paid / H:.3f}")
with open("probe_summary.json", "w") as f:
    json.dump({k: [r for r in v] for k, v in summary.items()}, f, indent=1)
print("done")
