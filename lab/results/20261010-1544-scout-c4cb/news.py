#!/usr/bin/env python3
"""Falsifier for the hierarchical gravity-news channel.

Question: does a system's gravity reach a distant observer through a
quantized multipole news stream whose required rate/bits track the mass
distribution's bandwidth (NOT the body count), with bounded error at the
absorber?

Scene: star (M=100) + 4 heavy planets (8.0 total, a in [0.30,0.60]L) +
n_light light bodies (2.0 total, a in [0.20,0.50]L), all exact Kepler
generators about the star. Observer: one body on its own orbit at D >> L
about the whole system. Truth field = direct sum over all masses (analytic
positions, zero integration error). News field = quantized spherical-
harmonic multipole moments q_lm(t_k) about the fixed star-origin, linearly
interpolated, evaluated as the truncated expansion
  Phi_l = -G/L * 4pi/(2l+1) * [q_l0 Y_l0 + 2 Re sum_{m>0} q_lm Y_lm] / u^{l+1}.

Channel accounting: per l, m=0 is real, m=1..l complex -> (1+2l) reals.
l=0 is static (emitted once); live channels are l>=1.
"""
import json
import sys
import time

import numpy as np
from scipy.special import sph_harm

G = 1.0
L = 1.0  # cell radius; all orbiting mass fits inside


# ---------------------------------------------------------------- scene ----
def make_scene(seed, n_light, m_planets=8.0, m_disk=2.0, M_star=100.0,
               intruder=None):
    rng = np.random.default_rng(seed)
    n_p = 4
    a_p = np.array([0.30, 0.40, 0.50, 0.60])
    e_p = rng.uniform(0.0, 0.2, n_p)
    inc_p = rng.uniform(0.0, np.pi, n_p)
    node_p = rng.uniform(0.0, 2 * np.pi, n_p)
    om_p = rng.uniform(0.0, 2 * np.pi, n_p)
    M_p = rng.uniform(0.0, 2 * np.pi, n_p)
    m_p = np.full(n_p, m_planets / n_p)

    a_d = rng.uniform(0.20, 0.50, 1024)
    e_d = rng.uniform(0.0, 0.15, 1024)
    inc_d = rng.uniform(0.0, np.pi, 1024)
    node_d = rng.uniform(0.0, 2 * np.pi, 1024)
    om_d = rng.uniform(0.0, 2 * np.pi, 1024)
    M_d = rng.uniform(0.0, 2 * np.pi, 1024)
    m_d = np.full(n_light, m_disk / n_light)

    a = np.concatenate([a_p, a_d[:n_light]])
    e = np.concatenate([e_p, e_d[:n_light]])
    inc = np.concatenate([inc_p, inc_d[:n_light]])
    node = np.concatenate([node_p, node_d[:n_light]])
    om = np.concatenate([om_p, om_d[:n_light]])
    M0 = np.concatenate([M_p, M_d[:n_light]])
    m = np.concatenate([m_p, m_d])
    if intruder is not None:
        a = np.append(a, intruder["a"])
        e = np.append(e, intruder["e"])
        inc = np.append(inc, rng.uniform(0, np.pi))
        node = np.append(node, rng.uniform(0, 2 * np.pi))
        om = np.append(om, rng.uniform(0, 2 * np.pi))
        M0 = np.append(M0, rng.uniform(0, 2 * np.pi))
        m = np.append(m, intruder["m"])

    n = np.sqrt(G * M_star / a ** 3)
    return dict(M_star=M_star, a=a, e=e, inc=inc, node=node, om=om,
                M0=M0, m=m, n=n, m_orb=float(m.sum()))


def kepler_pos(sc, t):
    """Exact Kepler positions of all orbiters at times t (T,) -> (T,nb,3)."""
    t = np.atleast_1d(t)
    Ma = sc["M0"][None, :] + sc["n"][None, :] * t[:, None]
    E = Ma.copy()
    for _ in range(12):
        f = E - sc["e"][None, :] * np.sin(E) - Ma
        fp = 1.0 - sc["e"][None, :] * np.cos(E)
        E = E - f / fp
    a, e = sc["a"][None, :], sc["e"][None, :]
    xp = a * (np.cos(E) - e)
    yp = a * np.sqrt(1 - e ** 2) * np.sin(E)
    inc, node, om = sc["inc"][None, :], sc["node"][None, :], sc["om"][None, :]
    cO, sO = np.cos(node), np.sin(node)
    ci, si = np.cos(inc), np.sin(inc)
    cw, sw = np.cos(om), np.sin(om)
    x = xp * (cO * cw - sO * sw * ci) - yp * (cO * sw + sO * cw * ci)
    y = xp * (sO * cw + cO * sw * ci) - yp * (sO * sw - cO * cw * ci)
    z = xp * (sw * si) + yp * (cw * si)
    return np.stack([x, y, z], axis=-1)


def scene_sources(sc, ts):
    """Sources (star at origin appended) at times ts: (T, nb+1, 3), masses."""
    pos = kepler_pos(sc, ts)
    pos = np.concatenate([pos, np.zeros((len(ts), 1, 3))], axis=1)
    mm = np.concatenate([sc["m"], [sc["M_star"]]])
    return pos, mm


# ------------------------------------------------------------- news feed ----
def chan_offsets(lmax):
    off, k = {}, 0
    for l in range(lmax + 1):
        off[l] = (k, k + l + 1)  # complex slots m=0..l
        k += l + 1
    return off, k


def live_reals(lmax):
    return sum(1 + 2 * l for l in range(1, lmax + 1))  # live reals, l>=1


def multipole_stream(sc, times, lmax, chunk=1500):
    """q_lm(times) about the star-origin, star included: complex m=0..l,
    laid out l-major. Per-l quantization scales from scene kinematic bounds
    only (no signal peeking)."""
    Tn = len(times)
    off, chan = chan_offsets(lmax)
    out = np.zeros((chan, Tn), dtype=complex)
    m_orb, M_star = sc["m_orb"], sc["M_star"]
    u_star = m_orb / (M_star + m_orb) * 0.75  # star-wobble bound
    scales = [M_star * u_star ** l + m_orb for l in range(lmax + 1)]
    for i0 in range(0, Tn, chunk):
        t = times[i0:i0 + chunk]
        pos, mm = scene_sources(sc, t)            # (c, nb+1, 3)
        r = np.linalg.norm(pos, axis=-1)
        u = r / L
        theta = np.arccos(np.clip(pos[..., 2] / np.maximum(r, 1e-300), -1, 1))
        phi = np.arctan2(pos[..., 1], pos[..., 0])
        for l in range(lmax + 1):
            k0, k1 = off[l]
            ms = np.arange(0, l + 1)
            Y = sph_harm(ms[:, None, None], l, phi[None, :, :],
                         theta[None, :, :])            # (m, c, nb+1)
            w = mm[None, None, :] * u[None, :, :] ** l  # (1, c, nb+1)
            out[k0:k1, i0:i0 + len(t)] = (np.conj(Y) * w).sum(-1)
    return out, scales


def quantize(q, scale, bits):
    s = scale / 2 ** (bits - 1)
    return np.round(q / s) * s


class NewsField:
    """Field from quantized news: linear readout of q_lm, truncated sum."""

    def __init__(self, tk, qk, lmax):
        self.tk, self.qk, self.lmax = tk, qk, lmax
        off, _ = chan_offsets(lmax)
        self.plan = [(l, off[l][0], np.arange(0, l + 1),
                      4 * np.pi / (2 * l + 1)) for l in range(lmax + 1)]

    def channels_at(self, t):
        qc = np.empty(self.qk.shape[0], dtype=complex)
        for j in range(self.qk.shape[0]):
            qc[j] = complex(np.interp(t, self.tk, self.qk[j].real),
                            np.interp(t, self.tk, self.qk[j].imag))
        return qc

    def phi_from(self, qc, x):
        r = np.linalg.norm(x)
        u = max(r / L, 1e-9)
        th = np.arccos(np.clip(x[2] / max(r, 1e-300), -1, 1))
        ph = np.arctan2(x[1], x[0])
        total = 0.0
        for l, k0, ms, fac in self.plan:
            Y = sph_harm(ms, l, ph, th)          # (l+1,)
            qv = qc[k0:k0 + l + 1]
            val = qv[0] * Y[0]
            for m in range(1, l + 1):
                val = val + 2.0 * (qv[m] * Y[m]).real
            total += fac * val / u ** (l + 1)
        return (-G / L * total).real

    def acc(self, qc_cache, x, t, h):
        qc = qc_cache.get(t)
        if qc is None:
            qc = self.channels_at(t)
            qc_cache[t] = qc
        g = np.empty(3)
        for i in range(3):
            dx = np.zeros(3)
            dx[i] = h
            g[i] = (self.phi_from(qc, x + dx) - self.phi_from(qc, x - dx)) / (2 * h)
        return -g


# ------------------------------------------------------------- observer ----
def run_truth(sc, D, e_obs, n_steps, dt):
    """Truth run: direct-sum field; batched source computation."""
    M_tot = sc["M_star"] + sc["m_orb"]
    v0 = np.sqrt(G * M_tot * (1 - e_obs) / (D * (1 + e_obs)))
    x = np.array([D, 0.0, 0.0])
    vh = np.array([0.0, v0, 0.0])
    xs = np.empty((n_steps + 1, 3))
    Es = np.empty(n_steps + 1)
    ts = np.arange(n_steps + 1) * dt
    src = np.empty((n_steps + 1, len(sc["m"]) + 1, 3))
    for i0 in range(0, n_steps + 1, 800):
        p, _ = scene_sources(sc, ts[i0:i0 + 800])
        src[i0:i0 + len(p)] = p
    mm = np.concatenate([sc["m"], [sc["M_star"]]])

    def fields(i, xq):
        d = xq[None, :] - src[i]                     # (nb+1,3)
        rn = np.linalg.norm(d, axis=1)
        a = G * (mm[:, None] * (-d) / rn[:, None] ** 3).sum(0)
        phi = -G * (mm / rn).sum()
        return a, phi

    a0, p0 = fields(0, x)
    Es[0] = 0.5 * vh @ vh + p0
    xs[0] = x
    vh = vh + 0.5 * dt * a0
    for i in range(n_steps):
        x = x + dt * vh
        a, phi = fields(i + 1, x)
        vh = vh + dt * a
        v = vh - 0.5 * dt * a
        xs[i + 1] = x
        Es[i + 1] = 0.5 * v @ v + phi
    return xs, Es


def run_news(sc, news, xs_t, D, e_obs, n_steps, dt, h):
    M_tot = sc["M_star"] + sc["m_orb"]
    v0 = np.sqrt(G * M_tot * (1 - e_obs) / (D * (1 + e_obs)))
    x = np.array([D, 0.0, 0.0])
    vh = np.array([0.0, v0, 0.0])
    xs = np.empty((n_steps + 1, 3))
    cache = {}
    chk = set(np.linspace(0, n_steps, 9).astype(int).tolist())
    dist = {}
    xs[0] = x
    a0 = news.acc(cache, x, 0.0, h)
    vh = vh + 0.5 * dt * a0
    v_fin = vh - 0.5 * dt * a0
    for i in range(n_steps):
        t = (i + 1) * dt
        x = x + dt * vh
        a = news.acc(cache, x, t, h)
        vh = vh + dt * a
        xs[i + 1] = x
        v_fin = vh - 0.5 * dt * a
        if (i + 1) in chk:
            dist[i + 1] = float(np.linalg.norm(x - xs_t[i + 1]) / D)
    return xs, v_fin, dist


# ------------------------------------------------------------------ run ----
def run_config(scene, D, e_obs, n_orb, lmax, rate, bits, base_rate=16,
               steps_per_orb=600, P_ref=None, quiet=False):
    sc = scene
    M_tot = sc["M_star"] + sc["m_orb"]
    P_obs = 2 * np.pi * np.sqrt(D ** 3 / (G * M_tot))
    dt = P_obs / steps_per_orb
    n_steps = int(n_orb * steps_per_orb)
    T = n_steps * dt
    if P_ref is None:
        P_ref = 2 * np.pi * np.sqrt(0.30 ** 3 / (G * sc["M_star"]))
    h = 1e-3 * D

    t0 = time.time()
    dn = P_ref / base_rate
    times = np.arange(-dn, T + 2 * dn, dn)
    q, scales = multipole_stream(sc, times, lmax)
    t_stream = time.time() - t0

    step = max(1, base_rate // rate)
    tk = times[::step]
    qk = q[:, ::step].copy()
    for l in range(lmax + 1):
        k0, k1 = chan_offsets(lmax)[0][l]
        qk[k0:k1] = quantize(qk[k0:k1], scales[l], bits)
    news = NewsField(tk, qk, lmax)

    t0 = time.time()
    xs_t, Es_t = run_truth(sc, D, e_obs, n_steps, dt)
    t_truth = time.time() - t0
    t0 = time.time()
    xs_n, v_n, dist = run_news(sc, news, xs_t, D, e_obs, n_steps, dt, h)
    t_news = time.time() - t0

    # news-run final energy with the TRUE field (isolates trajectory error)
    pos, mm_all = scene_sources(sc, np.array([T]))
    d_n = xs_n[-1] - pos[0]
    phi_n = -G * (mm_all / np.linalg.norm(d_n, axis=1)).sum()
    dE = float(0.5 * v_n @ v_n + phi_n - Es_t[-1])

    # field error along truth trajectory (200 samples)
    ts = np.linspace(0, T, 200)
    ferr = []
    for tt in ts:
        xq = xs_t[min(int(tt / dt), n_steps)]
        ps, mma = scene_sources(sc, np.array([tt]))
        d = xq[None, :] - ps[0]
        rn = np.linalg.norm(d, axis=1)
        at = G * (mma[:, None] * (-d) / rn[:, None] ** 3).sum(0)
        an = news.acc({}, xq, tt, h)
        ferr.append(np.linalg.norm(an - at) / np.linalg.norm(at))
    ferr = float(np.sqrt(np.mean(np.square(ferr))))

    E0 = Es_t[0]
    work_true = float(Es_t[-1] - Es_t[0])
    keys = sorted(dist)
    pos_err = dist[keys[-1]]
    bps = live_reals(lmax) * bits * rate / P_ref
    vacuous = abs(work_true) < 10e-6 * abs(E0)
    res = dict(lmax=lmax, rate_per_Pref=rate, bits=bits, D=D, e_obs=e_obs,
               n_orb=n_orb, nbodies=len(sc["m"]), steps=n_steps,
               P_ref=P_ref, P_obs=P_obs,
               pos_err_final=pos_err,
               dist_traj=[dist[k] for k in keys],
               dE_final=dE, work_true=work_true, E0=float(E0),
               field_rms_rel=ferr, vacuous=bool(vacuous),
               live_reals=live_reals(lmax), news_bits_per_time=bps,
               t_stream_s=round(t_stream, 2), t_truth_s=round(t_truth, 2),
               t_news_s=round(t_news, 2))
    res["pass"] = bool(pos_err <= 1e-3 and abs(dE) <= max(0.01 * abs(work_true),
                                                         1e-6 * abs(E0))
                       and not vacuous)
    if not quiet:
        print(json.dumps(res))
    return res


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "calib"
    if mode == "calib":
        sc = make_scene(1, 256)
        grid = []
        for lmax in [0, 1, 2, 3, 4]:
            for rate in [2, 4, 8, 16]:
                grid.append(run_config(sc, 12.0, 0.1, 8.37, lmax, rate, 16))
        for bits in [8, 32]:
            grid.append(run_config(sc, 12.0, 0.1, 8.37, 2, 8, bits))
        with open("grid_calib.json", "w") as f:
            json.dump(grid, f, indent=1)
    elif mode == "single":
        seed, n_light, D, e_obs, n_orb, lmax, rate, bits = \
            [float(x) for x in sys.argv[2:10]]
        base = int(sys.argv[10]) if len(sys.argv) > 10 else 16
        sc = make_scene(int(seed), int(n_light))
        run_config(sc, D, e_obs, n_orb, int(lmax), int(rate), int(bits),
                   base_rate=base)
