#!/usr/bin/env python3
"""Galactic program probe: do multipole cells PRODUCE the galaxy doll's smooth Phi?

The handoff page's unmeasured half: 'Galaxy: a given smooth Phi(r) -- how the
multipole cells produce that program, and bar/arm lumps as kicks, is the
unmeasured half.'  This probe builds the program (a polar log-grid of the
disc's own density, truncated in the azimuthal Fourier order m and in radial
cell count) from N sampled bodies and measures, at test points spread over the
disc:

  - err(m_max, n_r)  : |F_program - F_bodies| / |F_bodies|, same softened kernel
                       on both sides, so the error isolates the program's own
                       truncation (the smooth half), not a force-law mismatch;
  - lumps(N)         : |F_bodies - F_program(full grid)| / |F_bodies| -- the
                       granularity residual the kick layer owns (shot noise),
                       measured at N = 1e5 and 1e6;
  - the churn bar    : 0.008 relative (2da8's measured disc-churn switch-on,
                       eps_eff ~ 0.008-0.025).

Scenes: S1 = smooth two-arm exponential disc (arm contrast 0.3);
        S2 = the lab's galaxy scene shape (bodies in Zipf clusters on the arms).

Truth control: the axisymmetric program (m_max = 0) must FAIL the bar on both
scenes (a control that would pass voids the m-sweep).  The full-resolution
program must track the bodies' field at the softening scale.
Units: R_disc = 1, G = 1, masses sum to 1.  Floats explore; integers decide.
"""
import sys
import numpy as np

RNG_SEED = 20261017
R_MAX = 5.0          # disc radius sampled
EPS_S = 0.05         # Plummer softening (the aggregate's one-quantum scale)
NR_DEFAULT = 64
NPHI = 256
TEST_N = 400
BAR = 0.008          # 2da8's churn switch-on, low end
PITCH = np.deg2rad(15.0)
CHUNK = 32768


def sample_smooth(n, seed):
    rng = np.random.default_rng(seed)
    need = int(n * 1.8)
    r = -np.log(1 - rng.random(need) * (1 - np.exp(-R_MAX)))  # Sigma ~ e^-R
    r = r[r < R_MAX]
    phi = rng.random(len(r)) * 2 * np.pi
    arm = -np.log(np.maximum(r, 1e-3)) / np.tan(PITCH)
    w = 1.0 + 0.3 * np.cos(2 * (phi - arm))
    keep = rng.random(len(r)) < w / 1.3
    pts = np.stack([r[keep], phi[keep]], 1)
    while len(pts) < n:
        r2 = -np.log(1 - rng.random(need) * (1 - np.exp(-R_MAX)))
        r2 = r2[r2 < R_MAX]
        p2 = rng.random(len(r2)) * 2 * np.pi
        a2 = -np.log(np.maximum(r2, 1e-3)) / np.tan(PITCH)
        w2 = 1.0 + 0.3 * np.cos(2 * (p2 - a2))
        k2 = rng.random(len(r2)) < w2 / 1.3
        pts = np.concatenate([pts, np.stack([r2[k2], p2[k2]], 1)])
    pts = pts[:n]
    return np.stack([pts[:, 0] * np.cos(pts[:, 1]), pts[:, 0] * np.sin(pts[:, 1])], 1)


def sample_clusters(n, seed):
    rng = np.random.default_rng(seed)
    weights = 1.0 / np.arange(1, 129)
    weights = weights / weights.sum()
    counts = rng.multinomial(n, weights)
    rcl = -np.log(1 - rng.random(len(counts)) * (1 - np.exp(-R_MAX)))
    pcl = rng.random(len(counts)) * 2 * np.pi
    spread = 0.02 + 0.04 * rng.random(len(counts))
    out = []
    for c, rc, pc, sp in zip(counts, rcl, pcl, spread):
        if c == 0:
            continue
        dr = rng.normal(0, sp, c)
        dp = rng.normal(0, sp / max(rc, 0.1), c)
        out.append(np.stack([np.clip(rc + dr, 0.02, R_MAX), pc + dp], 1))
    pts = np.concatenate(out)
    arm = -np.log(np.maximum(pts[:, 0], 1e-3)) / np.tan(PITCH)
    onarm = np.abs(np.angle(np.exp(1j * (pts[:, 1] - arm)))) < 0.5
    sel = np.where(onarm | (rng.random(len(pts)) < 0.15))[0]
    pts = pts[sel[:n]]
    if len(pts) < n:
        pts = np.concatenate([pts, sample_smooth(n, seed + 7)[: n - len(pts)]])
    return np.stack([pts[:, 0] * np.cos(pts[:, 1]), pts[:, 0] * np.sin(pts[:, 1])], 1)


def kernel(dx, dy):
    d2 = dx * dx + dy * dy + EPS_S * EPS_S
    inv = d2 ** -1.5
    return np.stack([dx * inv, dy * inv], -1)


def sum_force(points, cents, weights):
    f = np.zeros_like(points)
    for i in range(0, len(cents), CHUNK):
        ch = cents[i:i + CHUNK]
        w = weights[i:i + CHUNK]
        dx = points[:, 0:1] - ch[None, :, 0]
        dy = points[:, 1:2] - ch[None, :, 1]
        k = kernel(dx, dy)
        f += (k * w[None, :, None]).sum(1)
    return f


def force_at(points, sources, mass):
    return sum_force(points, sources, np.full(len(sources), mass))


def grid_density(xy, mass, n_r, n_phi):
    """log-radial x azimuthal grid of the surface density (mass per cell)."""
    r = np.hypot(xy[:, 0], xy[:, 1])
    lr = np.log(np.clip(r, 1e-6, None))
    lo, hi = np.log(0.02), np.log(R_MAX)
    ir = ((lr - lo) / (hi - lo) * n_r).astype(int)
    ip = ((np.arctan2(xy[:, 1], xy[:, 0]) % (2 * np.pi)) / (2 * np.pi) * n_phi).astype(int)
    ok = ir < n_r          # inner bodies clip into cell 0: no mass is dropped
    irc = np.maximum(ir, 0)
    grid = np.zeros((n_r, n_phi))
    np.add.at(grid, (irc[ok], ip[ok]), mass)
    return grid, (lo, hi)


def grid_centers(n_r, n_phi, extent):
    lo, hi = extent
    rr = np.exp(lo + (np.arange(n_r) + 0.5) / n_r * (hi - lo))
    pp = (np.arange(n_phi) + 0.5) / n_phi * 2 * np.pi
    P, R = np.meshgrid(pp, rr)
    return np.stack([R * np.cos(P), R * np.sin(P)], -1).reshape(-1, 2)


def program_force(points, cents, flat, n_phi, m_max):
    """force of the density grid truncated at azimuthal order |m| <= m_max."""
    n_r = len(flat) // n_phi
    dens = flat.reshape(n_r, n_phi)
    fh = np.fft.rfft(dens, axis=1)
    if m_max is not None:
        fh[:, m_max + 1:] = 0.0
    dens = np.fft.irfft(fh, n=n_phi, axis=1)
    return sum_force(points, cents, dens.reshape(-1))


def rel_err(f, ft):
    return np.linalg.norm(f - ft, axis=1) / np.linalg.norm(ft, axis=1)


def m_star_scan(scene, N, tests, ft, xy, mass):
    """smallest m_max passing the bar per n_r, and the spectrum crossover."""
    out = {}
    for n_r in [8, 16, 32, 64]:
        grid, ext = grid_density(xy, mass, n_r, NPHI)
        cents = grid_centers(n_r, NPHI, ext)
        flat = grid.reshape(-1)
        for m_max in [0, 2, 4, 8, 16, 32, None]:
            mm = NPHI // 2 if m_max is None else m_max
            fp = program_force(tests, cents, flat, NPHI, m_max)
            e = rel_err(fp, ft)
            out[(n_r, mm)] = (float(np.median(e)), float(np.percentile(e, 90)))
    return out


def run():
    rng = np.random.default_rng(RNG_SEED)
    tp_r = np.sqrt(0.2 ** 2 + rng.random(TEST_N) * (4.8 ** 2 - 0.2 ** 2))
    tp_p = rng.random(TEST_N) * 2 * np.pi
    tests = np.stack([tp_r * np.cos(tp_p), tp_r * np.sin(tp_p)], 1)
    summary = {}
    for scene, sampler in [("smooth", sample_smooth), ("clusters", sample_clusters)]:
        for N in [100_000, 1_000_000]:
            xy = sampler(N, RNG_SEED + N)
            mass = 1.0 / N
            ft = force_at(tests, xy, mass)
            table = m_star_scan(scene, N, tests, ft, xy, mass)
            print(f"\n=== scene={scene} N={N}  (bar = {BAR}) ===")
            print("n_r  m_max  med_err  p90_err  bar   program_numbers")
            best = {}
            for (n_r, mm), (med, p90) in sorted(table.items()):
                tag = "PASS" if med < BAR else "fail"
                print(f"{n_r:<4d} {mm:<6d} {med:.5f}  {p90:.5f}  {tag}  {n_r * (2 * mm + 1)}")
                if med < BAR:
                    best.setdefault(n_r, (mm, med, p90))
            summary[(scene, N)] = best
            # lumps: bodies vs full-resolution program
            grid, ext = grid_density(xy, mass, NR_DEFAULT, NPHI)
            cents = grid_centers(NR_DEFAULT, NPHI, ext)
            fp = program_force(tests, cents, grid.reshape(-1), NPHI, None)
            lump = rel_err(fp, ft)
            frac = float(grid.sum())  # mass-conservation control: must be 1.0
            print(f"mass-control {scene} N={N}: grid carries {frac:.6f} of the mass")
            summary[("lumps", scene, N)] = (float(np.median(lump)), float(np.percentile(lump, 90)))
            # spectrum crossover (signal vs redraw noise), n_r = NR_DEFAULT
            xy2 = sampler(N, RNG_SEED + N + 1)
            g1, _ = grid_density(xy, mass, NR_DEFAULT, NPHI)
            g2, _ = grid_density(xy2, mass, NR_DEFAULT, NPHI)
            p1 = (np.abs(np.fft.rfft(g1, axis=1)) ** 2).sum(0)
            p2 = (np.abs(np.fft.rfft(g2, axis=1)) ** 2).sum(0)
            noise = np.abs(p1 - p2).mean()
            sig = np.minimum(p1, p2)
            above = np.where(sig > 10 * noise)[0]
            m_star = int(above.max()) if len(above) else 0
            summary[("spectrum", scene, N)] = (m_star, float(noise), float(p1[2] / max(noise, 1e-300)))
    print("\n=== SUMMARY ===")
    for scene in ["smooth", "clusters"]:
        for N in [100_000, 1_000_000]:
            best = summary[(scene, N)]
            lump = summary[("lumps", scene, N)]
            spec = summary[("spectrum", scene, N)]
            beacons = {nr: v for nr, v in best.items()}
            print(f"{scene:9s} N={N}: smallest passing m_max per n_r {beacons}")
            print(f"{scene:9s} N={N}: lumps med={lump[0]:.5f} p90={lump[1]:.5f} "
                  f"(-> at 1e9: ~{lump[0] * (N / 1e9) ** 0.5:.6f} med)")
            print(f"{scene:9s} N={N}: spectrum crossover m*~{spec[0]} (noise {spec[1]:.2e}, m=2 power/noise {spec[2]:.1f}x)")


if __name__ == "__main__":
    run()
