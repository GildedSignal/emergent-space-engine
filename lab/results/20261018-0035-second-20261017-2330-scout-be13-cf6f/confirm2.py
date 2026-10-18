#!/usr/bin/env python3
"""Second author (cf6f) on 20261017-2330-scout-be13: the checker's named
experiment to gold.  be13's confirm.py shipped a third instrument bug:
com_program binned radial mass with extent hi = gal.R_MAX (5.0) instead of
np.log(gal.R_MAX) (1.609), i.e. a 1.61x coarser log grid filling ~62% of the
rings -- visible in the shipped confirm.out as the cells_used mismatch
(148599 vs geom 221937).  Every 'COM is worse' number sat on that mismatched
grid.  This script is be13's dial set rerun on the corrected instrument, with
the controls that would have caught all three bugs shipped IN the instrument:

  C1 mass control   : each grid carries exactly 1.000000 of the mass
                      (would have caught be13 bug 1, the r<0.02 mask);
  C2 cell-count     : COM and geom grids must use the SAME cells
                      (would have caught be13 bug 3, the extent bug);
  C3 COM-in-ring    : each cell's COM lies inside its own ring's radial bin;
  C4 m=0 control    : the axisymmetric program FAILS the bar on both scenes
                      (a control that passes voids the sweep);
  C5 positive       : chunk step == slice width in every sum (be13 bug 2)
                      -- inherited unchanged from the fixed galprogram.sum_force.

Dials, all N=1e6, same Plummer kernel both sides, bar=0.008 (2da8 low end):
  D1 grid ladder x {geom, COM} x {smooth, clusters} incl. 512x2048 on smooth
     (the COM convergence ORDER was never measured);
  D2 m-truncation at the passing grid 256x1024 (be13's m*~2-4 clause was
     extrapolated from 64x256; the checker measured geom only, m<=4);
  D3 fresh seeds (never tuned on);
  D4 test annuli inside and outside be13's [0.2, 4.8] window;
  D5 softening scan at the passing grid.
Floats explore; the pass/fail at the bar decides.  ~10 min on the shared box.
"""
import time
import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location("gal", "galprogram.py")
gal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gal)

N = 1_000_000
GRIDS = [(64, 256), (128, 512), (256, 1024)]
FINE = (512, 2048)
PASSING = (256, 1024)


def log_bins(n_r):
    lo, hi = np.log(0.02), np.log(gal.R_MAX)      # <- the one-line fix (be13 bug 3)
    return lo, hi


def com_cells(xy, mass, n_r, n_phi):
    """Cell masses at each cell's centre of mass on bins MATCHED to grid_density.
    Empty cells keep their geometric centre (zero mass: position is inert)."""
    lo, hi = log_bins(n_r)
    r = np.hypot(xy[:, 0], xy[:, 1])
    lr = np.log(np.clip(r, 1e-6, None))
    ir = ((lr - lo) / (hi - lo) * n_r).astype(int)
    ip = ((np.arctan2(xy[:, 1], xy[:, 0]) % (2 * np.pi)) / (2 * np.pi) * n_phi).astype(int)
    ok = ir < n_r                                   # clip inner bodies into ring 0
    idx = np.maximum(ir, 0)[ok] * n_phi + ip[ok]
    M = np.zeros(n_r * n_phi)
    X = np.zeros(n_r * n_phi)
    Y = np.zeros(n_r * n_phi)
    np.add.at(M, idx, mass)
    np.add.at(X, idx, mass * xy[ok, 0])
    np.add.at(Y, idx, mass * xy[ok, 1])
    cents = gal.grid_centers(n_r, n_phi, (lo, hi))  # geometric fallback
    nz = M > 0
    cents[nz, 0] = X[nz] / M[nz]
    cents[nz, 1] = Y[nz] / M[nz]
    # C3: a cell's COM cannot leave its own ring (all members share the bin;
    # the mean of positions has radius below the members' max radius)
    rc = np.hypot(cents[nz, 0], cents[nz, 1])
    ring = nz.nonzero()[0] // n_phi
    assert np.all(rc < np.exp(lo + (ring + 1) * (hi - lo) / n_r)), "C3: COM left its ring"
    assert abs(M.sum() - 1.0) < 1e-9, "C1: mass lost in COM binning"
    return M, cents, nz.sum()


def geom_cells(xy, mass, n_r, n_phi):
    grid, ext = gal.grid_density(xy, mass, n_r, n_phi)
    cents = gal.grid_centers(n_r, n_phi, ext)
    assert abs(grid.sum() - 1.0) < 1e-9, "C1: mass lost in geom binning"
    return grid.reshape(-1), cents, int((grid > 0).sum())


def program(points, flat, cents, n_phi, m_max):
    """force of the cell program, azimuthally truncated at |m| <= m_max."""
    n_r = len(flat) // n_phi
    dens = flat.reshape(n_r, n_phi)
    if m_max is not None:
        fh = np.fft.rfft(dens, axis=1)
        fh[:, m_max + 1:] = 0.0
        dens = np.fft.irfft(fh, n=n_phi, axis=1)
    return gal.sum_force(points, cents, dens.reshape(-1))


def mid_tests(rng):
    """be13's exact mid-annulus test set (R in [0.2, 4.8], area-uniform)."""
    tp_r = np.sqrt(0.2 ** 2 + rng.random(gal.TEST_N) * (4.8 ** 2 - 0.2 ** 2))
    tp_p = rng.random(gal.TEST_N) * 2 * np.pi
    return np.stack([tp_r * np.cos(tp_p), tp_r * np.sin(tp_p)], 1)


def annulus_tests(rng, r0, r1, n):
    tp_r = np.sqrt(r0 ** 2 + rng.random(n) * (r1 ** 2 - r0 ** 2))
    tp_p = rng.random(n) * 2 * np.pi
    return np.stack([tp_r * np.cos(tp_p), tp_r * np.sin(tp_p)], 1)


def err_stats(fp, ft):
    e = gal.rel_err(fp, ft)
    return float(np.median(e)), float(np.percentile(e, 90))


def report(tag, med, p90, extra=""):
    v = "PASS" if (med < gal.BAR and p90 < gal.BAR) else ("med-pass" if med < gal.BAR else "fail")
    print(f"{tag:<34s} {med:.5f}  {p90:.5f}  {v}  {extra}")
    return med, p90


def main():
    t0 = time.time()
    rng = np.random.default_rng(gal.RNG_SEED)
    tests = mid_tests(rng)                    # stream continues below for annuli
    inner = annulus_tests(rng, 0.02, 0.2, gal.TEST_N)
    outer = annulus_tests(rng, 4.8, gal.R_MAX, gal.TEST_N)
    print(f"N={N} bar={gal.BAR} eps={gal.EPS_S}; PASS needs med AND p90 < bar")
    print(f"{'case':<34s} {'med':>7s}  {'p90':>7s}  verdict")

    for scene, sampler in [("smooth", gal.sample_smooth), ("clusters", gal.sample_clusters)]:
        xy = sampler(N, gal.RNG_SEED + N)
        mass = 1.0 / N
        ft = gal.force_at(tests, xy, mass)
        grids = GRIDS + ([FINE] if scene == "smooth" else [])
        for n_r, n_phi in grids:
            g_flat, g_cents, g_used = geom_cells(xy, mass, n_r, n_phi)
            c_flat, c_cents, c_used = com_cells(xy, mass, n_r, n_phi)
            assert g_used == c_used, f"C2 cell-count mismatch {g_used} vs {c_used}"
            mg, pg = err_stats(program(tests, g_flat, g_cents, n_phi, None), ft)
            mc, pc = err_stats(program(tests, c_flat, c_cents, n_phi, None), ft)
            report(f"{scene} {n_r}x{n_phi} geom", mg, pg, f"cells={g_used}")
            report(f"{scene} {n_r}x{n_phi} COM ", mc, pc, f"cells={c_used} ratio={mg/max(mc,1e-12):.2f}x")
            if (n_r, n_phi) == PASSING:
                for m in [0, 4, 8]:
                    mgt = err_stats(program(tests, g_flat, g_cents, n_phi, m), ft)
                    mct = err_stats(program(tests, c_flat, c_cents, n_phi, m), ft)
                    report(f"{scene} 256x1024 geom m<={m:<2d}", *mgt, "C4:fail" if m == 0 else "")
                    report(f"{scene} 256x1024 COM  m<={m:<2d}", *mct)
        print(f"[{scene} elapsed {time.time()-t0:.0f}s]")

    # D3 fresh seeds (never tuned on): the shipped program + COM, smooth
    for seed in [gal.RNG_SEED + N + 101, gal.RNG_SEED + N + 202]:
        xy = gal.sample_smooth(N, seed)
        mass = 1.0 / N
        ft = gal.force_at(tests, xy, mass)
        g_flat, g_cents, gu = geom_cells(xy, mass, *PASSING)
        c_flat, c_cents, cu = com_cells(xy, mass, *PASSING)
        assert gu == cu
        report(f"smooth seed={seed % 1000} geom", *err_stats(program(tests, g_flat, g_cents, PASSING[1], None), ft), f"cells={gu}")
        report(f"smooth seed={seed % 1000} COM ", *err_stats(program(tests, c_flat, c_cents, PASSING[1], None), ft))
    print(f"[seeds elapsed {time.time()-t0:.0f}s]")

    # D4 annuli (smooth, at the passing grid)
    xy = gal.sample_smooth(N, gal.RNG_SEED + N)
    mass = 1.0 / N
    g_flat, g_cents, _ = geom_cells(xy, mass, *PASSING)
    c_flat, c_cents, _ = com_cells(xy, mass, *PASSING)
    for name, pts in [("inner 0.02-0.2", inner), ("outer 4.8-5.0", outer)]:
        ft = gal.force_at(pts, xy, mass)
        report(f"smooth {name} geom", *err_stats(program(pts, g_flat, g_cents, PASSING[1], None), ft))
        report(f"smooth {name} COM ", *err_stats(program(pts, c_flat, c_cents, PASSING[1], None), ft))
    print(f"[annuli elapsed {time.time()-t0:.0f}s]")

    # D5 softening scan (smooth, 256x1024): a finer aggregate quantum demands
    # finer cells -- does the coupling survive the corrected instrument?
    for eps in [0.02, 0.01]:
        gal.EPS_S = eps
        ft = gal.force_at(tests, xy, mass)
        report(f"smooth 256x1024 geom eps={eps}", *err_stats(program(tests, g_flat, g_cents, PASSING[1], None), ft))
        report(f"smooth 256x1024 COM  eps={eps}", *err_stats(program(tests, c_flat, c_cents, PASSING[1], None), ft))
    gal.EPS_S = 0.05
    print(f"[done elapsed {time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
