#!/usr/bin/env python3
"""Analysis of the decisive grid: rate attractor, burstiness, scalings."""
import json, glob
import numpy as np

def load(tag):
    r = json.load(open(f"res_{tag}.json"))
    return r

def stats(tag, n=None, quiet=False):
    r = load(tag)
    n = n or r["cfg"]["n"]
    rate = np.array(r["rate_per_orbit"], dtype=float) / n      # per body per orbit
    T = len(rate)
    snaps = np.array(r["e_snap"])
    a_std = snaps[:, 4]; emean = snaps[:, 5]
    # windows
    w = lambda lo, hi: rate[lo:hi].mean() if hi <= T else rate[lo:].mean()
    early, mid, late = w(5, 50), w(175, 225), w(350, 400)
    peak_orbit = int(np.argmax(rate[10:])) + 10
    # Fano on orbits 200..400: var/mean of counts (counts = per-orbit totals)
    counts = np.array(r["rate_per_orbit"][200:400], dtype=float)
    fano = counts.var() / counts.mean() if counts.mean() > 0 else float("nan")
    # cluster factor: encounters within +-1 orbit of another encounter, vs baseline
    raw = np.load(f"raw_{tag}.npy")
    ts = raw[:, 0] / (2 * np.pi)     # in orbits
    if len(ts) > 50:
        dt = np.diff(np.sort(ts))
        # conditional: for each encounter, expected neighbors within 1 orbit = rate*N
        base = counts.mean()
        within1 = np.mean([(np.abs(ts - t) <= 1.0).sum() - 1 for t in ts[::max(1, len(ts)//300)]])
        phi = within1 / base if base > 0 else float("nan")
    else:
        phi = float("nan")
    out = dict(tag=tag, enc=len(raw), ejected=r["ejected"],
               early=round(early, 4), mid=round(mid, 4), late=round(late, 4),
               peak=round(rate.max(), 4), peak_orbit=peak_orbit,
               fano=round(float(fano), 2), phi=round(float(phi), 2),
               a_std0=round(snaps[0, 4], 4), a_stdF=round(snaps[-1, 4], 4),
               e_mean0=round(snaps[0, 5], 4), e_meanF=round(snaps[-1, 5], 4))
    if not quiet:
        print(json.dumps(out))
    return out

if __name__ == "__main__":
    import sys
    rows = []
    for tag in (sys.argv[1:] or ["g1","g2","g3","g4","g5","g6","g7","g8","g9","g10","g11","g12","g13","g14"]):
        try:
            rows.append(stats(tag))
        except Exception as ex:
            print(tag, "ERR", ex)
    # scalings on gentle regime
    try:
        r3, r8, r9 = stats("g3", quiet=True), stats("g8", quiet=True), stats("g9", quiet=True)
        print("R_cap exponent:", round(np.log(r3["mid"]/r8["mid"]) / np.log(3e-3/1e-3), 2),
              round(np.log(r9["mid"]/r3["mid"]) / np.log(1e-2/3e-3), 2))
        r10, r11 = stats("g10", quiet=True), stats("g11", quiet=True)
        print("N exponent:", round(np.log(r11["mid"]/r10["mid"]) / np.log(600/150), 2))
    except Exception as ex:
        print("scaling ERR", ex)
    with open("summary.json", "w") as f:
        json.dump(rows, f, indent=1)
