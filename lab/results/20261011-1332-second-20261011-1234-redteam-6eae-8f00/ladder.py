#!/usr/bin/env python3
"""The named missing experiment (checker of run 20261011-1234): the visibility ladder.

Per-winding image magnification against observer radius, on the same instrument as
view_images.py (its trace()). Static Schwarzschild M=1, static observer at (r_o, 0), static
emitters on the circle r_e. Images of emitter (r_e, phi_e) = crossings of the exit-azimuth
curve Phi(psi) with the levels phi_e + 2 pi k (same-side family, winding k) and
2 pi - phi_e + 2 pi k (mirror-side family: those are the real images on the mirror sky half,
at sky angle 2 pi - psi). Magnification mu = |dpsi/dphi_e| = 1/|dPhi/dpsi| at the crossing
(secant through the straddling sample pair of the combined curve). rel = mu/mu_brightest.

Grids: probe 32768 uniform over (0.02, pi-0.02) at h=3e-3 (the shipped sweep), a log-spaced
low-psi extension (0.003..0.02, h=1e-4) for the near-radial direct images, and corridor zoom
131072 at h=1.5e-3 on the shipped wrap window +-20%; emitters 360 uniform azimuths plus
geometric refinement toward alignment (phi_e = pi - eps, eps down to 1e-4). Counts are lower
bounds where the corridor outruns the grid; magnitudes do not depend on grid density
(level-crossing topology only). Validation: flat M=0 against the closed-form projection,
the checker's independent aligned-emitter numbers at r_o=10, flanking-ray shots, and the
shipped multiplicity() counter.
"""
import json
import numpy as np
from view_images import trace, multiplicity

KMAX = 3
THRESHOLDS = [("1/50", 1.0 / 50.0), ("1/10", 1.0 / 10.0), ("1/3", 1.0 / 3.0)]
FAMS = [("same", k) for k in range(KMAX + 1)] + [("mirror", k) for k in range(KMAX + 1)]


class Curve:
    """Combined probe+zoom exit-azimuth curve, sorted by psi, with bracket slopes."""

    def __init__(self, psi, phi):
        order = np.argsort(psi)
        self.psi, self.phi = psi[order], phi[order]
        a, b = self.phi[:-1], self.phi[1:]
        self.lo, self.hi = np.minimum(a, b), np.maximum(a, b)
        dpsi = self.psi[1:] - self.psi[:-1]
        self.slope = (b - a) / dpsi
        self.psi0 = self.psi[:-1]

    def crossings(self, level):
        idx = np.where((self.lo < level) & (self.hi > level))[0]
        out = []
        for i in idx:
            t = (level - self.phi[i]) / (self.phi[i + 1] - self.phi[i])
            out.append((float(self.psi0[i] + t * (self.psi[i + 1] - self.psi[i])),
                        float(1.0 / abs(self.slope[i]))))
        return out


def build_curve(r_o, r_e):
    ps = np.linspace(0.02, np.pi - 0.02, 32768)
    res = trace(r_o, r_e, ps)
    phi = res["Phi"]
    fin = np.isfinite(phi)
    psi_all, phi_all = [ps[fin]], [phi[fin]]
    meta = {"n_probe": int(ps.size), "probe_phi_max": round(float(np.nanmax(phi)), 3)}
    # low-psi extension: near-radial outward rays carry the direct images of emitters
    # close to the observer's anti-hole axis; at r_o <= 3.5M GR bending pushes those
    # crossings below the uniform grid's psi floor (0.02), which would fake a winding
    # "visibility band" in the forward cone (instrument v1 artifact, diagnosed on the
    # first run). Log-spaced, tiny h: the sweep is small but du/dphi ~ 1/psi is large.
    plow = np.logspace(np.log10(0.003), np.log10(0.02), 512)
    rlow = trace(r_o, r_e, plow, h=1e-4)
    fl = np.isfinite(rlow["Phi"])
    psi_all.append(plow[fl])
    phi_all.append(rlow["Phi"][fl])
    meta["n_lowpsi"] = int(plow.size)
    wrap = fin & (phi > np.nanmax(phi) - 2 * np.pi)
    psi_w = ps[wrap]
    if psi_w.size > 10:
        lo, hi = float(psi_w.min()), float(psi_w.max())
        pad = 0.2 * (hi - lo)
        psz = np.linspace(lo - pad, hi + pad, 131072)
        rz = trace(r_o, r_e, psz, h=1.5e-3)
        fz = np.isfinite(rz["Phi"])
        psi_all.append(psz[fz])
        phi_all.append(rz["Phi"][fz])
        meta["zoom"] = {"corridor_rad": [round(lo, 5), round(hi, 5)], "n_rays": int(psz.size),
                        "deepest_bend_rad": round(float(np.nanmax(rz["Phi"])), 3)}
    return Curve(np.concatenate(psi_all), np.concatenate(phi_all)), meta, res


def images_of(curve, phi_e):
    """All images of emitter phi_e: {(side,k): [(psi, mu), ...]} over both sky halves."""
    imgs = {}
    for side, k in FAMS:
        base = phi_e if side == "same" else 2 * np.pi - phi_e
        cr = curve.crossings(base + 2 * np.pi * k)
        if cr:
            imgs[(side, k)] = cr
    return imgs


def ladder_row(curve, uni, near):
    phis = np.concatenate([uni, near])
    per = [images_of(curve, p) for p in phis]
    n_uni = uni.size
    brights = [max((mu for cr in imgs.values() for _, mu in cr), default=0.0) for imgs in per]
    fam_stats = {}
    for fam in FAMS:
        rr, mm = [], []
        band_hi, band_lo = 0.0, np.pi
        for j, imgs in enumerate(per):
            if not imgs or fam not in imgs or brights[j] <= 0.0:
                continue
            mu = max(mu for _, mu in imgs[fam])
            rel = mu / brights[j]
            if j < n_uni:
                rr.append(rel)
                mm.append(mu)
            if rel > 1.0 / 50.0:
                band_lo = min(band_lo, phis[j])
                band_hi = max(band_hi, phis[j])
        row = {"frac_exist": round(float(np.mean([1.0 if (imgs and fam in imgs) else 0.0
                                                  for imgs in per[:n_uni]])), 4)}
        if rr:
            row.update({"median_rel": round(float(np.median(rr)), 5),
                        "p90_rel": round(float(np.percentile(rr, 90)), 5),
                        "max_rel": round(float(max(rr)), 5),
                        "median_mu_abs": round(float(np.median(mm)), 6)})
            for name, thr in THRESHOLDS:
                row["frac_gt_" + name] = round(float(np.mean(np.array(rr) > thr)), 4)
            if band_hi > band_lo:
                row["band_gt_1_50_phi_e"] = [round(float(band_lo), 4), round(float(band_hi), 4)]
        fam_stats["%s_k%d" % fam] = row

    vis = {name: [] for name, _ in THRESHOLDS}
    for j in range(n_uni):
        imgs, bright = per[j], brights[j]
        for name, thr in THRESHOLDS:
            vis[name].append(sum(1 for cr in imgs.values() for _, mu in cr
                                 if bright > 0 and mu / bright > thr) if imgs else 0)
    viscount = {name: {"frac_ge2": round(float((np.array(v) >= 2).mean()), 4),
                       "frac_ge3": round(float((np.array(v) >= 3).mean()), 4),
                       "frac_ge4": round(float((np.array(v) >= 4).mean()), 4)}
                for name, v in vis.items()}

    decay = {}
    for side in ("same", "mirror"):
        ratios = {k: [] for k in range(KMAX)}
        for j in range(n_uni):
            imgs = per[j]
            if not imgs:
                continue
            for k in range(KMAX):
                if (side, k) in imgs and (side, k + 1) in imgs:
                    ratios[k].append(max(mu for _, mu in imgs[(side, k + 1)]) /
                                     max(mu for _, mu in imgs[(side, k)]))
        decay[side] = {("k%d_to_k%d" % (k, k + 1)):
                       (round(float(np.median(v)), 5) if v else None) for k, v in ratios.items()}

    near_tab = []
    for j, phi_e in enumerate(near):
        imgs, bright = per[n_uni + j], brights[n_uni + j]
        if not imgs or bright <= 0.0:
            continue
        row = {"eps_to_alignment": round(float(np.pi - phi_e), 5)}
        for fam in FAMS:
            if fam in imgs:
                row["%s_k%d" % fam] = round(max(mu for _, mu in imgs[fam]) / bright, 5)
        near_tab.append(row)
    return {"families": fam_stats, "visible_multiplicity": viscount, "decay": decay,
            "near_alignment": near_tab}


def validate():
    val = {}
    # V1: the checker's independent aligned-emitter numbers at r_o=10, r_e=20
    curve, _, _ = build_curve(10.0, 20.0)
    imgs = images_of(curve, np.pi)
    bright = max(mu for cr in imgs.values() for _, mu in cr)
    v1 = {}
    for (side, k), cr in sorted(imgs.items()):
        for psi, mu in cr:
            v1["%s_k%d" % (side, k)] = {"psi_deg": round(float(np.degrees(psi)), 3),
                                        "mu": round(mu, 5), "rel": round(mu / bright, 6)}
    val["aligned_r10"] = v1
    val["aligned_r10_ref"] = {"checker": "psi 141.11 deg mu~12.13 (k=0), 152.29 deg mu~0.0164 (k=1)",
                              "rel_k1_ref": round(1.0 / 740.0, 6)}

    # V2: flat M=0, same-side k=0 mu vs closed-form projection dpsi/dphi_e
    ps = np.linspace(0.02, np.pi - 0.02, 32768)
    res = trace(10.0, 20.0, ps, M=0.0)
    fin = np.isfinite(res["Phi"])
    c0 = Curve(ps[fin], res["Phi"][fin])
    r_o, r_e = 10.0, 20.0
    worst = 0.0
    for phi_e in np.linspace(0.3, 2.8, 12):
        cr = c0.crossings(phi_e)
        if not cr:
            continue
        psi, mu = cr[0]
        d = (r_e * r_e - r_e * r_o * np.cos(phi_e)) / \
            (r_e * r_e + r_o * r_o - 2 * r_e * r_o * np.cos(phi_e))
        worst = max(worst, abs(mu - d) / d)
    val["flat_M0_mu_vs_projection_max_rel_diff"] = round(float(worst), 6)

    # V3: flanking-ray shots vs curve secants, r_o=10, spread over families. Compared
    # only where mu >= 1e-4: below that the flanking Phi difference (~1e-10 rad) drowns
    # in integration noise (v1 outliers were k=2 windings at mu ~ 1e-5, five orders
    # below any visibility threshold).
    checks = []
    for phi_e in np.linspace(0.3, 3.0, 10):
        for fam, cr in images_of(curve, phi_e).items():
            if cr[0][1] >= 1e-4:
                checks.append((phi_e, fam, cr[0][0], cr[0][1]))
    sel = checks[::max(1, len(checks) // 14)][:14]
    dlt = 5e-6
    flanks = []
    for _, _, psi, _ in sel:
        flanks += [psi - dlt, psi + dlt]
    rf = trace(10.0, 20.0, np.array(flanks), h=1.5e-3)
    diffs = []
    for i, (_, fam, psi, mu_curve) in enumerate(sel):
        dp, dm = rf["Phi"][2 * i], rf["Phi"][2 * i + 1]
        if np.isfinite(dp) and np.isfinite(dm) and dp != dm:
            mu_shot = 2 * dlt / abs(dp - dm)
            diffs.append(abs(mu_shot - mu_curve) / mu_curve)
    val["flanking_vs_curve_mu_max_rel_diff"] = round(float(max(diffs)), 4) if diffs else None
    val["flanking_n_checks"] = len(diffs)
    val["flanking_mu_floor"] = 1e-4

    # V4: crossing counts agree with the shipped multiplicity() counter (probe, r_o=10)
    res = trace(10.0, 20.0, np.linspace(0.02, np.pi - 0.02, 32768))
    fin = np.isfinite(res["Phi"])
    c1 = Curve(res["psi"][fin], res["Phi"][fin])
    worst = 0
    for phi_e in np.linspace(0.2, 2.9, 8):
        mine = sum(len(cr) for cr in images_of(c1, phi_e).values())
        theirs = multiplicity(res["Phi"], phi_e) + multiplicity(res["Phi"], 2 * np.pi - phi_e)
        worst = max(worst, abs(mine - theirs))
    val["count_vs_shipped_counter_max_diff"] = int(worst)
    return val


def main():
    uni = np.linspace(0.02, np.pi - 0.02, 360)
    eps = np.array([0.4, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 5e-4, 2e-4, 1e-4])
    near = np.pi - eps
    val = validate()
    print(json.dumps({"validation": val}, indent=1))
    rep = {"machine": "linux x8664, 8 vCPU", "units": "M=1", "kmax": KMAX,
           "thresholds": dict(THRESHOLDS), "validation": val, "sweeps": []}
    for r_o, r_e in [(10.0, 20.0), (5.0, 20.0), (3.5, 20.0), (3.2, 20.0), (100.0, 200.0)]:
        curve, meta, _ = build_curve(r_o, r_e)
        row = {"r_o": r_o, "r_e": r_e, **meta}
        row.update(ladder_row(curve, uni, near))
        rep["sweeps"].append(row)
        print(json.dumps(row))
    with open("ladder.json", "w") as f:
        json.dump(rep, f, indent=1)
    print("wrote ladder.json")


if __name__ == "__main__":
    main()
