"""Analysis for run 20261005-2231-q-secular-008e.

Frozen estimators (predictions.md): amp = e_free (construction); g_hat = linear fit of
unwrapped arg(z - zf_LL) over samples with |z - zf| > amp/3; rate_err relative to truth;
evec_err = max_t |zbar_truth - z_law| / amp; PASS = rate_err <= 0.05 AND evec_err <= 0.10;
Fraction(L) = |admitted AND PASS| / 1024. KILL if Fraction(rings) < 0.5 or any admitted
body inside a resonance width measured from the run-averaged <a>.
"""
import json
import math

import numpy as np

import selector as SEL

NSTOR = 384

def ghat(zs, ts, zf, amp):
    """Frozen rate estimator on a (masked, unwrapped) angle fit. zf may be static (NB,)
    or time-dependent (nst, NB)."""
    d = zs - (zf if zf.ndim == 2 else zf[None, :])
    mask = np.abs(d) > (amp / 3.0)[None, :]
    g = np.full(zs.shape[1], np.nan)
    for i in range(zs.shape[1]):
        m = mask[:, i]
        if m.sum() < 10:
            continue
        ang = np.unwrap(np.angle(d[m, i]))
        g[i] = np.polyfit(ts[m], ang, 1)[0]
    return g

def main():
    meta = json.load(open("truth_meta.json"))
    a = np.array(meta["a"]); e_free = np.array(meta["e_free"])
    zf = np.array(meta["zf_re"]) + 1j * np.array(meta["zf_im"])
    A = np.array(meta["A"])
    amp = e_free
    zt = np.load("truth_zbar.npz"); ts = zt["t"]; zbar_t = zt["z"]
    zbar_c = np.load("conv_zbar.npz")["z"]
    zbar_k = np.load("kick_zbar.npz")["z"]
    z_ll = np.load("ll_z.npz")["z"].astype(np.complex128)
    z_ri = np.load("rings_z.npz")["z"].astype(np.complex128)
    a_stor = np.load("truth_a.npz")["a"]
    a_mean = a_stor.mean(axis=0)
    # time-dependent LL forced term (the modes rotate; static zf(0) would corrupt the fits)
    from wh_run import modes, laplace_b, MU_J, A_J, MU_S, A_S, E_J, E_S, VARPI_J, VARPI_S
    gm, VV, VVi = modes()
    zpl0 = np.array([E_J * np.exp(1j * VARPI_J), E_S * np.exp(1j * VARPI_S)])
    cc = VVi @ zpl0
    n_b = a ** -1.5
    BPk = np.zeros((2, len(a)))
    for P, (mup, ap) in enumerate([(MU_J, A_J), (MU_S, A_S)]):
        alpha = a / ap
        b2 = np.array([laplace_b(1.5, 2, al) for al in alpha])
        for k in range(2):
            BPk[k] += -n_b * mup / 4 * alpha * alpha * b2 * VV[P, k]
    zf_t = np.zeros((NSTOR, len(a)), complex)
    for k in range(2):
        zf_t += np.outer(np.exp(1j * gm[k] * ts), BPk[k] * cc[k] / (A - gm[k]))

    # selector admission (frozen rules)
    g5g6, V, Vinv = SEL.planet_modes()
    res = SEL.resonances()
    adm = np.zeros(len(a), bool)
    why_not = {}
    for i in range(len(a)):
        ok, why = SEL.select(a[i], e_free[i], g5g6, V, Vinv, res)
        adm[i] = ok
        if not ok:
            why_not[why] = why_not.get(why, 0) + 1

    # rates (subtract the rotating forced term; identical treatment for all laws)
    g_true = ghat(zbar_t, ts, zf_t, amp)
    g_ll = ghat(z_ll, ts, zf_t, amp)
    g_ri = ghat(z_ri, ts, zf_t, amp)

    # e-vector errors
    def evec(zlaw):
        return (np.abs(zbar_t - zlaw) / amp[None, :]).max(axis=0)
    ev_ll, ev_ri = evec(z_ll), evec(z_ri)
    ev_kick = evec(zbar_k)

    rate_err_ll = np.abs(g_ll - g_true) / np.abs(g_true)
    rate_err_ri = np.abs(g_ri - g_true) / np.abs(g_true)

    pass_ll = (rate_err_ll <= 0.05) & (ev_ll <= 0.10)
    pass_ri = (rate_err_ri <= 0.05) & (ev_ri <= 0.10)
    frac_ll = (adm & pass_ll).sum() / len(a)
    frac_ri = (adm & pass_ri).sum() / len(a)

    # a-posteriori: inside a resonance width measured from <a>?
    inside = np.zeros(len(a), bool)
    min_dw = np.full(len(a), np.inf)
    for i in range(len(a)):
        n = a_mean[i] ** -1.5
        e_eff = max(e_free[i], abs(zf[i]), SEL.E_FLOOR)
        for r in res:
            ratio = n / (r["P"]["a"] ** -1.5)
            d = abs(ratio / r["ratio"] - 1)
            w = SEL.mmr_halfwidth(r, e_eff) / 1.0  # already includes KAPPA_M
            min_dw[i] = min(min_dw[i], d / w * SEL.KAPPA_M)  # in units of the raw half-width
            if d < w:
                inside[i] = True
    leaked = adm & inside
    # pumping signature for admitted bodies
    z0mag = np.abs(zf + e_free * np.exp(1j * np.array(meta["beta"])))
    pumped = np.abs(zbar_t).max(axis=0) > (np.abs(zf) + amp + 0.05)

    # convergence (median/p90 over bodies of the max over time; the max is one chaotic
    # 2:1-zone body where h-sensitivity is genuine chaos)
    conv_by_body = np.abs(zbar_c - zbar_t).max(axis=0)
    conv_err = float(np.median(conv_by_body))
    conv_p90 = float(np.percentile(conv_by_body, 90))
    conv_max = float(conv_by_body.max())

    # depletion zones (3:1 and 5:2 with Jupiter): inside raw width
    zones = {"3:1J": None, "5:2J": None}
    zone_stats = {}
    for r in res:
        key = f"{r['p']}:{r['q']}{r['P']['name']}"
        if key not in zones:
            continue
        n = a ** -1.5
        ratio = n / (r["P"]["a"] ** -1.5)
        d = np.abs(ratio / r["ratio"] - 1)
        w = SEL.mmr_halfwidth(r, np.maximum(e_free, SEL.E_FLOOR))
        inzone = d < w
        if inzone.sum() == 0:
            continue
        tz = np.abs(zbar_t[:, inzone]).max(axis=0)
        kz = np.abs(zbar_k[:, inzone]).max(axis=0)
        zone_stats[key] = dict(
            n=int(inzone.sum()),
            truth_pumped_frac=float((tz > 2 * z0mag[inzone]).mean()),
            kick_pumped_frac=float((kz > 2 * z0mag[inzone]).mean()),
            truth_maxe_med=float(np.median(tz)),
            kick_maxe_med=float(np.median(kz)),
            traj_err_med=float(np.median(np.abs(zbar_k[:, inzone] - zbar_t[:, inzone]))),
            traj_err_p90=float(np.percentile(np.abs(zbar_k[:, inzone] - zbar_t[:, inzone]), 90)),
        )

    # kick-law accuracy on admitted (the cost of NOT being a phasor)
    kick_adm_med = float(np.median(ev_kick[adm]))

    metrics = dict(
        n_bodies=len(a),
        admitted=int(adm.sum()),
        admitted_frac=float(adm.mean()),
        rejection_reasons=why_not,
        frac_ll=float(frac_ll), frac_rings=float(frac_ri),
        pass_ll_admitted=float(pass_ll[adm].mean()),
        pass_rings_admitted=float(pass_ri[adm].mean()),
        kill_fraction=frac_ri < 0.5,
        leaked_inside_resonance_width=int(leaked.sum()),
        leaked_pumped=int((adm & pumped).sum()),
        convergence_med_dz=conv_err, convergence_p90_dz=conv_p90, convergence_max_dz=conv_max,
        rate_err_rings_med_adm=float(np.nanmedian(rate_err_ri[adm])),
        rate_err_rings_p90_adm=float(np.nanpercentile(rate_err_ri[adm], 90)),
        rate_err_ll_med_adm=float(np.nanmedian(rate_err_ll[adm])),
        evec_rings_med_adm=float(np.median(ev_ri[adm])),
        evec_rings_p90_adm=float(np.percentile(ev_ri[adm], 90)),
        evec_ll_med_adm=float(np.median(ev_ll[adm])),
        evec_kick_med_adm=kick_adm_med,
        zone_stats=zone_stats,
    )
    # a-binned summary for the dossier
    bins = [(2.0, 2.5), (2.5, 2.9), (2.9, 3.3)]
    table = []
    for lo, hi in bins:
        m = adm & (a >= lo) & (a < hi)
        if m.sum() == 0:
            continue
        table.append(dict(
            a_range=f"[{lo},{hi})", n=int(m.sum()),
            rate_ll_med=float(np.nanmedian(rate_err_ll[m])),
            rate_rings_med=float(np.nanmedian(rate_err_ri[m])),
            evec_ll_med=float(np.median(ev_ll[m])),
            evec_rings_med=float(np.median(ev_ri[m])),
            pass_rings=float(pass_ri[m].mean()),
            pass_ll=float(pass_ll[m].mean()),
        ))
    metrics["a_bins"] = table
    # where rings fails, why
    fail = adm & ~pass_ri
    metrics["rings_failures"] = int(fail.sum())
    if fail.sum():
        fi = np.where(fail)[0]
        metrics["rings_fail_examples"] = [
            dict(a=float(a[i]), e_free=float(e_free[i]),
                 rate_err=float(rate_err_ri[i]), evec=float(ev_ri[i]),
                 dist_over_W=float(min_dw[i]), pumped=bool(pumped[i]))
            for i in fi[:12]
        ]
    def default(o):
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        raise TypeError(repr(o))

    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=1, default=default)
    print(json.dumps(metrics, indent=1, default=default))

if __name__ == "__main__":
    main()
