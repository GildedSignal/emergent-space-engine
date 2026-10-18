#!/usr/bin/env python3
"""Confirmation: what binds the program's floor -- cell scale h, softening eps,
or the monopole-at-centre approximation?  Tests (a) grid refinement at fixed
N, (b) mass at the cell's centre of MASS (the dipole term) vs the geometric
centre, at N = 1e6 (smooth two-arm scene, the decisive scene of the sweep)."""
import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location("gal", "galprogram.py")
gal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gal)

RNG = gal.RNG_SEED
N = 1_000_000


def com_program(points, xy, mass, n_r, n_phi):
    """mass at each cell's centre of mass (monopole + dipole), no m truncation"""
    r = np.hypot(xy[:, 0], xy[:, 1])
    lr = np.log(np.clip(r, 1e-6, None))
    lo, hi = np.log(0.02), gal.R_MAX
    ir = ((lr - lo) / (hi - lo) * n_r).astype(int)
    ip = ((np.arctan2(xy[:, 1], xy[:, 0]) % (2 * np.pi)) / (2 * np.pi) * n_phi).astype(int)
    ok = ir < n_r          # clip inner bodies into ring 0: no mass dropped
    idx = np.maximum(ir, 0)[ok] * n_phi + ip[ok]
    M = np.zeros(n_r * n_phi)
    np.add.at(M, idx, mass)
    X = np.zeros(n_r * n_phi)
    Y = np.zeros(n_r * n_phi)
    np.add.at(X, idx, mass * xy[ok, 0])
    np.add.at(Y, idx, mass * xy[ok, 1])
    nz = M > 0
    cents = np.stack([np.zeros(n_r * n_phi), np.zeros(n_r * n_phi)], 1)
    cents[nz, 0] = X[nz] / M[nz]
    cents[nz, 1] = Y[nz] / M[nz]
    return gal.sum_force(points, cents[nz], M[nz]), nz.sum()


def main():
    rng = np.random.default_rng(RNG)
    tp_r = np.sqrt(0.2 ** 2 + rng.random(gal.TEST_N) * (4.8 ** 2 - 0.2 ** 2))
    tp_p = rng.random(gal.TEST_N) * 2 * np.pi
    tests = np.stack([tp_r * np.cos(tp_p), tp_r * np.sin(tp_p)], 1)
    xy = gal.sample_smooth(N, RNG + N)
    mass = 1.0 / N
    ft = gal.force_at(tests, xy, mass)
    print(f"N={N} smooth; bar={gal.BAR}; eps={gal.EPS_S}")
    print("grid          centre   med_err  p90_err  bar   cells_used")
    for n_r, n_phi in [(64, 256), (128, 512), (256, 1024)]:
        grid, ext = gal.grid_density(xy, mass, n_r, n_phi)
        cents = gal.grid_centers(n_r, n_phi, ext)
        fp = gal.program_force(tests, cents, grid.reshape(-1), n_phi, None)
        e = gal.rel_err(fp, ft)
        tag = "PASS" if np.median(e) < gal.BAR else "fail"
        print(f"{n_r}x{n_phi:<6d} geom     {np.median(e):.5f}  {np.percentile(e, 90):.5f}  {tag}  {(grid > 0).sum()}")
        fpc, used = com_program(tests, xy, mass, n_r, n_phi)
        ec = gal.rel_err(fpc, ft)
        tagc = "PASS" if np.median(ec) < gal.BAR else "fail"
        print(f"{n_r}x{n_phi:<6d} COM      {np.median(ec):.5f}  {np.percentile(ec, 90):.5f}  {tagc}  {used}")
    # softening scan at the finest grid, COM centring: does eps bind?
    for eps in [0.05, 0.02, 0.01]:
        gal.EPS_S = eps
        ftc = gal.force_at(tests, xy, mass)
        fpc, used = com_program(tests, xy, mass, 256, 1024)
        ec = gal.rel_err(fpc, ftc)
        tagc = "PASS" if np.median(ec) < gal.BAR else "fail"
        print(f"256x1024 COM eps={eps:<5g} {np.median(ec):.5f}  {np.percentile(ec, 90):.5f}  {tagc}  {used}")
    gal.EPS_S = 0.05


if __name__ == "__main__":
    main()
