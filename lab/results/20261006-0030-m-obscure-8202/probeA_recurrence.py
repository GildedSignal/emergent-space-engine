#!/usr/bin/env python3
"""Probe A — is every boring readout stream a low-order linear recurrence?

Scene: light-cone gather. Emitter and observer on two incommensurate Kepler
orbits (mu=1, a_e=1, a_o=1.7, c=10 scene units). 64 frames per emitter period,
8192 frames. Stream = apparent angle of the emitter at the observer (unwrapped)
and the emission eccentric anomaly E.

Identification is forward-backward least squares (Lang & McClellan 1980): the
backward rows force the fitted roots onto the unit circle, which is the exact
structure of a quasi-periodic stream. The fixed-point test runs on the
INCREMENT stream (bounded), as the engine stores increments, not absolutes.

Parts:
  A1  minimal recurrence order k for one-step rel err < tol
  A2  Q24 fixed-point coefficient/sample quantization, feed-forward: drift?
  A3  cost: Newton iterations per frame, cold starter vs predicted starter
  A4  held out: kick of 1e-4 relative dv at frame 3000 -> detection latency,
      re-identification window
  A5  order vs eccentricity scaling

Run: python3 probeA_recurrence.py [--seed 3]   (< 60 s, < 200 MB)
"""
import json, sys
import numpy as np

SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 3
C_LIGHT = 10.0
NF = 8192
FPS = 64.0
TWOPI = 2.0 * np.pi


def kepler_E(M, e, it=8):
    """E - e sin E = M, vectorized Newton from E=M."""
    E = np.array(M, dtype=float)
    for _ in range(it):
        f = E - e * np.sin(E) - M
        fp = 1.0 - e * np.cos(E)
        E = E - f / fp
    return E


def position(t, a, e, w, tp=0.0):
    n = (a ** -1.5)
    M = n * (t - tp)
    E = kepler_E(np.mod(M, TWOPI), e) + np.floor(M / TWOPI) * TWOPI  # unwrapped E
    x = a * (np.cos(E) - e)
    y = a * np.sqrt(1 - e * e) * np.sin(E)
    return np.cos(w) * x - np.sin(w) * y, np.sin(w) * x + np.cos(w) * y, E


def gather_stream(a_e, e_e, w_e, a_o, e_o, w_o):
    dt = TWOPI / FPS
    tf = np.arange(NF) * dt
    xof, yof, _ = position(tf, a_o, e_o, w_o)
    lo, hi = tf - 1.0, tf.copy()          # light lag < 0.55 < 1 in these units
    for _ in range(52):                    # vectorized bisection, 2^-52
        mid = 0.5 * (lo + hi)
        xe, ye, _ = position(mid, a_e, e_e, w_e)
        G = tf - mid - np.hypot(xof - xe, yof - ye) / C_LIGHT
        lo = np.where(G > 0, mid, lo)
        hi = np.where(G > 0, hi, mid)
    t_e = 0.5 * (lo + hi)
    xe, ye, Ee = position(t_e, a_e, e_e, w_e)
    theta = np.unwrap(np.arctan2(ye - yof, xe - xof))
    return theta, Ee, t_e, tf, (xof, yof)


def apply_kick_stream(base, kick_frame, rel_dv):
    """Stream with the emitter's orbit changed at kick_frame: n -> n(1+rel_dv)^-3,
    e -> e(1-rel_dv/2), phase-continuous at the kick (an along-track burn)."""
    a_e, e_e, w_e, a_o, e_o, w_o = base
    dt = TWOPI / FPS
    tf = np.arange(NF) * dt
    tk = kick_frame * dt
    n0 = a_e ** -1.5
    a1 = a_e * (1 + rel_dv) ** 2
    n1 = a1 ** -1.5
    e1 = e_e * (1 - 0.5 * rel_dv)

    def emit_pos(t):
        pre = t <= tk
        M0 = n0 * tk
        t_eff = np.where(pre, t, tk + (t - tk) * (n1 / n0))
        Marr = np.where(pre, n0 * t, M0 + n1 * (t - tk))
        Earr = np.where(pre, e_e, e1)
        aarr = np.where(pre, a_e, a1)
        E = kepler_E(np.mod(Marr, TWOPI), Earr) + np.floor(Marr / TWOPI) * TWOPI
        x = aarr * (np.cos(E) - Earr)
        y = aarr * np.sqrt(1 - Earr ** 2) * np.sin(E)
        return np.cos(w_e) * x - np.sin(w_e) * y, np.sin(w_e) * x + np.cos(w_e) * y

    xof, yof, _ = position(tf, a_o, e_o, w_o)
    lo, hi = tf - 1.0, tf.copy()
    for _ in range(52):
        mid = 0.5 * (lo + hi)
        xe, ye = emit_pos(mid)
        G = tf - mid - np.hypot(xof - xe, yof - ye) / C_LIGHT
        lo = np.where(G > 0, mid, lo)
        hi = np.where(G > 0, hi, mid)
    t_e = 0.5 * (lo + hi)
    xe, ye = emit_pos(t_e)
    theta = np.unwrap(np.arctan2(ye - yof, xe - xof))
    pre = t_e <= tk
    M0 = n0 * tk
    Marr = np.where(pre, n0 * t_e, M0 + n1 * (t_e - tk))
    Earr = np.where(pre, e_e, e1)
    Ee = kepler_E(np.mod(Marr, TWOPI), Earr) + np.floor(Marr / TWOPI) * TWOPI
    return theta, Ee, t_e, tf


def identify(s, k, fit_len):
    """Forward-backward LS predictor: s[n] = sum_j c_j s[n-j].
    Backward rows (time-reversed) pin the roots to the unit circle."""
    fl = max(fit_len, 4 * k, 256)
    F = np.array([[s[n + k - 1 - j] for j in range(k)] for n in range(fl)])
    b = np.array([s[n + k] for n in range(fl)])
    r = s[::-1]
    B = np.array([[r[n + k - 1 - j] for j in range(k)] for n in range(fl)])
    rb = np.array([r[n + k] for n in range(fl)])
    A = np.vstack([F, B])                 # time-reversed stream, same recurrence
    y = np.concatenate([b, rb])
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    return c


def onestep_err(s, c, n0, horizon):
    """Teacher-forced one-step prediction error over [n0, n0+horizon)."""
    k = len(c)
    seg = s[n0:n0 + horizon]
    errs = np.empty(horizon - k)
    for i in range(horizon - k):
        val = sum(c[j] * seg[i + k - 1 - j] for j in range(k))
        errs[i] = abs(val - seg[i + k])
    return errs


def fixed_point_run(dq_true, c, Q=24):
    """dq_true: increment stream quantized to Q bits (integer quanta).
    Runs the recurrence on its OWN predictions; returns |err| in quanta."""
    k = len(c)
    C = [int(round(cj * (1 << Q))) for cj in c]
    q = [int(v) for v in dq_true[:k]]
    n_max = min(len(dq_true) - k, 4096)
    errs = []
    for i in range(n_max):
        acc = sum(C[j] * q[-1 - j] for j in range(k))
        pred = (acc + (1 << (Q - 1))) >> Q
        err = abs(pred - int(dq_true[k + i]))
        errs.append(min(err, 1 << 40))
        q.append(pred)                    # compounding test
        if err >= (1 << 40):
            break
    return np.array(errs, dtype=float)


def newton_iters(t_true, tf, xof, yof, a_e, e_e, w_e, starter, tol=1e-13):
    """Newton iterations on G(te)= tf - te - dist/c, counted per frame."""
    iters = np.zeros(len(tf), dtype=int)
    te = np.array(starter, dtype=float)
    for _ in range(30):
        E = kepler_E(np.mod(te * (a_e ** -1.5), TWOPI), e_e)
        x = a_e * (np.cos(E) - e_e)
        y = a_e * np.sqrt(1 - e_e ** 2) * np.sin(E)
        xe = np.cos(w_e) * x - np.sin(w_e) * y
        ye = np.sin(w_e) * x + np.cos(w_e) * y
        G = tf - te - np.hypot(xof - xe, yof - ye) / C_LIGHT
        done = np.abs(G) < tol
        h = 1e-7
        E2 = kepler_E(np.mod((te + h) * (a_e ** -1.5), TWOPI), e_e)
        x2 = a_e * (np.cos(E2) - e_e)
        y2 = a_e * np.sqrt(1 - e_e ** 2) * np.sin(E2)
        xe2 = np.cos(w_e) * x2 - np.sin(w_e) * y2
        ye2 = np.sin(w_e) * x2 + np.cos(w_e) * y2
        G2 = tf - (te + h) - np.hypot(xof - xe2, yof - ye2) / C_LIGHT
        dG = (G2 - G) / h
        te = te - np.where(done, 0.0, G / dG)
        iters += (~done).astype(int)
        if done.all():
            break
    return iters


def predict_stream(s, c, n0, count):
    k = len(c)
    hist = list(s[n0 - k:n0])
    preds = []
    for i in range(count):
        preds.append(sum(c[j] * hist[-1 - j] for j in range(k)))
        hist.append(s[n0 + i])
    return np.array(preds)


def main():
    out = {"seed": SEED, "scenes": {}}
    scenes = [
        ("e005_o01", 0.05, 0.1), ("e03_o01", 0.3, 0.1), ("e07_o01", 0.7, 0.1),
        ("e005_o03", 0.05, 0.3), ("e03_o03", 0.3, 0.3), ("e07_o03", 0.7, 0.3),
    ]
    k_grid = [4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96]
    for name, e_e, e_o in scenes:
        a_e, a_o, w_e, w_o = 1.0, 1.7, 0.4, 2.1
        theta, Ee, t_e, tf, (xof, yof) = gather_stream(a_e, e_e, w_e, a_o, e_o, w_o)
        res = {}
        n0 = 1024
        for tol in (1e-6, 1e-9):
            kmin = None
            for k in k_grid:
                c = identify(theta[n0:], k, 4 * k)
                errs = onestep_err(theta, c, n0, 512)
                if errs.max() < tol * TWOPI:
                    kmin = k
                    break
            res[f"kmin_{tol:g}"] = kmin
        k2 = min(res["kmin_1e-06"] or 32, 64)
        # A2: fixed point on the increment stream (bounded), feed-forward
        dth = np.diff(theta)
        dq = np.round(dth / TWOPI * (1 << 24)).astype(np.int64)
        c_inc = identify(dth[n0:], k2, 4 * k2)
        fp = fixed_point_run(dq[n0:], c_inc)
        res["fp_order"] = k2
        res["fp_frames_to_1e-6"] = int(np.argmax(fp * (TWOPI / 2**24) > 1e-6)) if (fp * (TWOPI / 2**24) > 1e-6).any() else len(fp)
        res["fp_frames_to_1e-9"] = int(np.argmax(fp * (TWOPI / 2**24) > 1e-9)) if (fp * (TWOPI / 2**24) > 1e-9).any() else len(fp)
        res["fp_max_err_rad"] = float(fp.max() * TWOPI / 2**24)
        res["fp_max_err_quanta"] = float(fp.max())
        # A3: Newton iterations, cold vs predicted starter
        cE = identify(Ee[n0:], k2, 4 * k2)
        predE = predict_stream(Ee, cE, 512, 1024)
        starter_pred = (predE - e_e * np.sin(predE)) / (a_e ** -1.5)
        seg = np.arange(512, 1536)
        it_cold = newton_iters(t_e[seg], tf[seg], xof[seg], yof[seg], a_e, e_e, w_e, t_e[seg - 1])
        it_pred = newton_iters(t_e[seg], tf[seg], xof[seg], yof[seg], a_e, e_e, w_e, starter_pred)
        res["newton_mean_cold"] = float(it_cold.mean())
        res["newton_mean_pred"] = float(it_pred.mean())
        res["newton_pred_frac0"] = float((it_pred == 0).mean())
        out["scenes"][name] = res

    # A4: kick detection + re-identification (e=0.3, e_o=0.1)

    # ---- Part 2: the forms that survive --------------------------------
    # P2a: single-orbit stream = exact finite recurrence (aliasing makes the
    # digital spectrum finite; order <= samples/orbit is a theorem).
    out["P2a_single_orbit"] = {}
    t = np.arange(NF) * (TWOPI / FPS)
    for e_e in (0.05, 0.3, 0.7, 0.9):
        x, y, _ = position(t, 1.0, e_e, 0.0)
        row = {}
        for k in (8, 16, 32, 64):
            c = identify(x, k, 2048)
            errs = onestep_err(x, c, 2100, 512)
            row[f"k{k}"] = float(errs.max())
        out["P2a_single_orbit"][f"e{e_e}"] = row
    # P2b: fixed-point Q24 self-feeding drift on the single-orbit x stream
    # (bounded samples, FB-stabilized coefficients; k=8/16 at e=0.3).
    x, y, _ = position(t, 1.0, 0.3, 0.0)
    dx = np.diff(x)
    dq = np.round(dx / 4.0 * (1 << 24)).astype(np.int64)   # range +-2 -> quanta
    fp_out = {}
    for k in (8, 16):
        c = identify(dx, k, 2048)
        fp = fixed_point_run(dq, c)
        fp_out[f"k{k}"] = {
            "frames_run": int(len(fp)),
            "max_err_quanta": float(fp.max()),
            "max_err_units": float(fp.max() / (1 << 24) * 4.0),
            "frames_to_1e-6_units": int(np.argmax(fp / (1 << 24) * 4.0 > 1e-6)) if (fp / (1 << 24) * 4.0 > 1e-6).any() else int(len(fp)),
        }
    out["P2b_fixed_point"] = fp_out
    # P2c: kick flag on a single-orbit E stream (phase form). Fit k=16 at
    # e=0.3, kick rel_dv=1e-4 at frame 3000, count frames until |resid| > 5x
    # the pre-kick residual scale, then refit and count frames to recover.
    E0 = position(t, 1.0, 0.3, 0.0)[2]
    k = 16
    c0 = identify(E0, k, 2048)
    n1 = 1.0 * (1 + 1e-4) ** -1.5
    t_eff = np.where(t <= 3000 * TWOPI / FPS, t, 3000 * TWOPI / FPS + (t - 3000 * TWOPI / FPS) * n1)
    Ek = position(t_eff, 1.0, 0.3, 0.0)[2]
    preds = predict_stream(Ek, c0, 2900, 220)
    resid = np.abs(preds - Ek[2900:3120])
    scale = np.median(resid[:99]) + 1e-15
    flag = int(np.argmax(resid > 5 * scale))
    reid = None
    for start in range(3001, 3001 + 200):
        c2 = identify(Ek[start:], k, 4 * k)
        errs = onestep_err(Ek, c2, start + 4 * k, 128)
        if len(errs) and errs.max() < 1e-6 * TWOPI * 0 + 5e-6:
            reid = (start + 4 * k) - 3000
            break
    out["P2c_kick"] = {"k": k, "pre_scale": float(scale),
                       "flag_frames_after_kick": flag,
                       "resid_at_flag": float(resid[flag]),
                       "reident_frames": reid}
    base = (1.0, 0.3, 0.4, 1.7, 0.1, 2.1)
    theta, Ee, t_e, tf = apply_kick_stream(base, kick_frame=3000, rel_dv=1e-4)
    k = out["scenes"]["e03_o01"]["kmin_1e-06"] or 16
    c = identify(theta[1024:], k, 4 * k)
    preds = predict_stream(theta, c, 2900, 300)
    resid = np.abs(preds - theta[2900:3200])
    sigma = 1.4826 * np.median(resid[:99])
    sigma = max(sigma, 1e-12)
    flag = int(np.argmax(resid > 3 * sigma))
    reid = None
    for start in range(3000, 3000 + 6 * k + 48):
        c2 = identify(theta[start:], k, 4 * k)
        errs = onestep_err(theta, c2, start + 4 * k, 128)
        if len(errs) and errs.max() < 1e-6 * TWOPI:
            reid = (start + 4 * k) - 3000
            break
    out["A4"] = {"k": k, "sigma_pre": float(sigma), "flag_frame_offset": flag,
                 "kick_frame": 3000, "resid_at_flag": float(resid[flag]),
                 "reident_frames": reid}
    ks = [out["scenes"][nm]["kmin_1e-06"] for nm in ("e005_o01", "e03_o01", "e07_o01")]
    out["A5"] = {"k_by_e": ks}
    json.dump(out, open("probeA_out.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
