"""S*: the recurrence ratio conditioned on state distance instead of cells.

Pairs of far-field samples (planet > 3 R_H), classified by time gap (near 2-8 P, far 64-200 P)
and by normalized state distance D in (a/sep, e, r2/R_H, theta_rel, v_r) with fixed per-coordinate
scales. Ratio = p90(|d err| over far pairs with D <= d0) / p90(|d err| over near pairs with
D <= d0), d0 = the 10th percentile of near-pair distances (frozen, applied to both), p90 floored
at the gate's 1e-12. A state-only error is the same at the same state, however far apart in
time: ratio 1. An error with memory is not.
"""
import numpy as np
from stats import HILL, PERIOD, NS, FLOOR, load, plants, growth_exponent, median_inf, recurrence, TP

# robust per-coordinate spreads of the frozen ships' far-field samples
SCALES = np.array([0.01, 0.005, 0.05, 0.05, 1e-5])  # a/sep, e, r2/R_H, theta_rel, v_r


def coords(d):
    """(16, NS, 5): a/sep, e, r2/R_H, theta_rel (rad, wrapped), v_r (radial speed about barycentre)."""
    out = np.empty((16, NS, 5))
    omega = 2 * np.pi / PERIOD
    for s in range(16):
        x, y, vx, vy = d[s, :, 1], d[s, :, 2], d[s, :, 3], d[s, :, 4]
        out[s, :, 0] = d[s, :, 6]
        out[s, :, 1] = d[s, :, 7]
        out[s, :, 2] = d[s, :, 5] / HILL
        out[s, :, 3] = np.angle(np.exp(1j * (np.arctan2(y, x) - omega * d[s, :, 0])))
        out[s, :, 4] = (x * vx + y * vy) / np.hypot(x, y)
    return out


def pairs(es, C5, r2, out_near, out_far):
    for s in range(16):
        idx = np.where((r2[s] > 3 * HILL) & np.isfinite(es[s]))[0]
        T, E, X = TP[idx], es[s][idx], C5[s][idx]
        n = len(idx)
        for a0 in range(0, n, 256):
            b = slice(a0, min(a0 + 256, n))
            i = np.arange(a0, a0 + 256 if a0 + 256 <= n else n)
            dt = np.abs(T[b, None] - T[None, :])
            derr = np.abs(E[b, None] - E[None, :])
            D = np.sqrt((((X[b, None, :] - X[None, :, :]) / SCALES) ** 2).sum(-1))
            keep = i[:, None] > np.arange(n)[None, :]
            for lo, hi, acc in ((2.0, 8.0, out_near), (64.0, 200.1, out_far)):
                sel = keep & (dt >= lo) & (dt <= hi)
                if sel.any():
                    acc.append((D[sel], derr[sel]))


def s_ratio(es, C5, r2, qmatch=0.1, q=0.9):
    near, far = [], []
    pairs(es, C5, r2, near, far)
    if not near or not far:
        return np.nan, 0, 0
    Dn = np.concatenate([x[0] for x in near]); En = np.concatenate([x[1] for x in near])
    Df = np.concatenate([x[0] for x in far]); Ef = np.concatenate([x[1] for x in far])
    d0 = np.quantile(Dn, qmatch)
    nf, ff = Dn <= d0, Df <= d0
    p90 = lambda v: max(np.quantile(v, q), FLOOR) if len(v) else np.nan
    return p90(Ef[ff]) / p90(En[nf]), int(nf.sum()), int(ff.sum())


def main():
    r13 = load("r13")
    a, e, r2 = r13[:, :, 6], r13[:, :, 7], r13[:, :, 5]
    C5 = coords(r13)
    P = plants(r13)
    refs = {}
    for nm, kk in [("ref-r13", "r13"), ("ref-r12", "r12"), ("ref-r11", "r11")]:
        d = load(kk)
        refs[nm] = (d[:, :, 8] - d[:, 0:1, 8]) / np.abs(d[:, 0:1, 8])
    print(f"{'plant':14s} {'exponent':>8s} {'cells':>7s} {'S*':>8s}  matched pairs n/f")
    for nm, es in list(P.items()) + list(refs.items()):
        ex = median_inf([growth_exponent(np.abs(es[s])) for s in range(16)])
        rc = recurrence(es, a, e, r2)[0]
        rs = s_ratio(es, C5, r2)
        print(f"{nm:14s} {ex:8.3f} {rc:7.2f} {rs[0]:8.2f}  ({rs[1]}/{rs[2]})")


if __name__ == "__main__":
    main()
