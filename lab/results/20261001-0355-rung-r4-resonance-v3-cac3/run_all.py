#!/usr/bin/env python3
"""Driver for rung r4 v3.  Subcommands:
  cases            write cases.json (uses the nf2 island half-width)
  truth N          dense truth at N steps/orbit -> truth-N.npz
  laws             nf1, nf2, averaged, arc-g8 on every case -> laws-*.npz
  metrics          metrics.json against truth-2400
  picture          picture.svg (phase portraits, 1 librating + 1 circulating)
  dev              quick 2-case sanity run at N=1200 (development only)
"""
import json
import math
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r4v3 as R

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

def load_cases():
    with open("cases.json") as f:
        return json.load(f)

def series_of_truth(npz, i):
    n = int(npz["counts"][i])
    return dict(t=npz["t"][i, :n], e=npz["e"][i, :n],
                phi=np.mod(npz["phi"][i, :n], 2*np.pi),
                a=npz["a"][i, :n])

def regime_and_amp(phi):
    u = np.unwrap(phi)
    rng = u.max() - u.min()
    if rng < 0.98*2*np.pi:
        return "libration", 0.5*rng
    return "circulation", None

# ------------------------------------------------------------------ cases
def cmd_cases():
    cases = R.make_cases()
    with open("cases.json", "w") as f:
        json.dump(cases, f, indent=1)
    for c in cases:
        print(f"{c['name']:22s} j={c['j']} mu={c['mu']:g} n1={c['n1']:.6f} "
              f"a1={c['a1']:.6f} T={R.run_length(c)/(2*np.pi/c['n1']):.1f} P1")

def cmd_truth(N):
    cases = load_cases()
    R.truth_batch(cases, N, f"truth-{N}.npz")
    print(f"truth-{N}.npz written")

def cmd_laws():
    cases = load_cases()
    ref = np.load("truth-2400.npz")
    names = list(ref["names"])
    out = {cfg: dict(names=[], e=[], phi=[], t=[], epo=[], closed=[],
                     wins=[], orbits=[]) for cfg in ("nf1", "nf2", "averaged", "arc-g8")}
    fits = {}
    for c in cases:
        key = (c["j"], c["mu"])
        if key not in fits:
            fits[key] = R.CoefFit(c["j"], c["mu"])
    for c in cases:
        key = (c["j"], c["mu"])
        i = names.index(c["name"])
        s = series_of_truth(ref, i)
        j, mu = c["j"], c["mu"]
        m0 = 1.0 - mu
        L1 = math.sqrt(m0*c["a1"])
        G0 = L1*(1.0 - math.sqrt(1.0 - R.E0*R.E0))
        Lp = L1 + j*G0
        g0 = -(j+1)*R.LAM20
        for cfg in ("nf1", "nf2"):
            nf = R.NF(j, mu, 1 if cfg == "nf1" else 2, fit=fits[key])
            cyc = nf.compile_cycle(g0, G0, Lp)
            assert cyc is not None, (cfg, c["name"])
            phi, e, _ = nf.state_from_cycle(cyc, s["t"])
            out[cfg]["names"].append(c["name"])
            out[cfg]["e"].append(e); out[cfg]["phi"].append(np.mod(phi, 2*np.pi))
            out[cfg]["t"].append(s["t"])
            out[cfg]["epo"].append(nf.n_evals/(s["t"][-1]*c["n1"]/(2*np.pi)))
            out[cfg]["closed"].append(bool(cyc["closed"]))
            out[cfg]["wins"].append(0); out[cfg]["orbits"].append(s["t"][-1]*c["n1"]/(2*np.pi))
        av = R.run_averaged(c, fits[key])
        out["averaged"]["names"].append(c["name"])
        out["averaged"]["e"].append(av["e"]); out["averaged"]["phi"].append(av["phi"])
        out["averaged"]["t"].append(av["t"])
        out["averaged"]["epo"].append(av["evals"]/av["orbits"])
        out["averaged"]["closed"].append(False)
        out["averaged"]["wins"].append(av["wins"]); out["averaged"]["orbits"].append(av["orbits"])
        g8 = R.run_arc_g8(c)
        out["arc-g8"]["names"].append(c["name"])
        out["arc-g8"]["e"].append(g8["e"]); out["arc-g8"]["phi"].append(g8["phi"])
        out["arc-g8"]["t"].append(g8["t"])
        out["arc-g8"]["epo"].append(g8["evals"]/g8["orbits"])
        out["arc-g8"]["closed"].append(None)
        out["arc-g8"]["wins"].append(g8["wins"]); out["arc-g8"]["orbits"].append(g8["orbits"])
        print(f"{c['name']:22s} done", flush=True)
    for cfg, d in out.items():
        np.savez_compressed(f"laws-{cfg}.npz", names=np.array(d["names"]),
                            e=np.array(d["e"], dtype=object),
                            phi=np.array(d["phi"], dtype=object),
                            t=np.array(d["t"], dtype=object),
                            epo=np.array(d["epo"]), closed=np.array(d["closed"]),
                            wins=np.array(d["wins"]), orbits=np.array(d["orbits"]),
                            allow_pickle=True)

def secular(e, nwin=33):
    """Moving average over ~2 synodic oscillation periods (33 samples at
    16 samples per inner orbit): the secular e1 envelope."""
    if len(e) < nwin:
        return np.asarray(e)
    return np.convolve(e, np.ones(nwin)/nwin, mode="valid")

def config_metrics(law_cases, ref_cases, is_truth=False):
    """law_cases/ref_cases: list of dicts(name, control, e, phi, epo)."""
    pumps, amps, match, ctrl_pass, epos = [], [], [], [], []
    for law, refc in zip(law_cases, ref_cases):
        reg_l, amp_l = regime_and_amp(law["phi"])
        reg_r, amp_r = regime_and_amp(refc["phi"])
        ratio = law["e"].max()/refc["e"].max()
        epos.append(law["epo"])
        if not refc["control"]:
            pumps.append(ratio)
            match.append(reg_l == reg_r)
            if reg_r == "libration":
                r = 0.0 if reg_l != "libration" else amp_l/amp_r
                amps.append(min(r, 1.0/r) if r > 0 else 0.0)
        else:
            sl, sr = secular(law["e"]), secular(refc["e"])
            n = min(len(sl), len(sr))
            scale = max(sr[:n].mean(), 1e-12)
            ok = float(np.max(np.abs(sl[:n] - sr[:n]))) <= 0.2*scale
            ctrl_pass.append(ok)
    m = dict(
        e_pump_ratio_min=float(min(pumps)), e_pump_ratio_max=float(max(pumps)),
        libration_amplitude_ratio=float(min(amps)) if amps else 1.0,
        regime_match_fraction=float(np.mean(match)),
        control_pass_fraction=float(np.mean(ctrl_pass)) if ctrl_pass else 1.0,
        dense_steps=0.0,
        evaluations_per_orbit=float(np.median(epos)) if not is_truth else 0.0,
    )
    return m, pumps, amps

def cmd_metrics():
    cases = load_cases()
    ref = np.load("truth-2400.npz")
    names = list(ref["names"])
    t1200 = np.load("truth-1200.npz")
    metrics = {}
    detail = {}
    ref_cases = []
    for c in cases:
        s = series_of_truth(ref, names.index(c["name"]))
        reg, amp = regime_and_amp(s["phi"])
        ref_cases.append(dict(name=c["name"], control=c["control"], e=s["e"],
                              phi=s["phi"], regime=reg, amp=amp,
                              emax=float(s["e"].max())))
    detail["truth-2400"] = [dict(name=r["name"], regime=r["regime"],
                                 amp=r["amp"], emax=r["emax"]) for r in ref_cases]
    law_cases = []
    for c in cases:
        s = series_of_truth(t1200, names.index(c["name"]))
        law_cases.append(dict(name=c["name"], control=c["control"], e=s["e"],
                              phi=s["phi"], epo=0.0))
    m, pumps, amps = config_metrics(law_cases, ref_cases, is_truth=True)
    metrics["truth-1200"] = m
    detail["truth-1200"] = dict(pumps=pumps, amps=amps)
    for cfg in ("nf1", "nf2", "averaged", "arc-g8"):
        d = np.load(f"laws-{cfg}.npz", allow_pickle=True)
        law_cases = []
        for k, c in enumerate(cases):
            law_cases.append(dict(name=c["name"], control=c["control"],
                                  e=np.asarray(d["e"][k], float),
                                  phi=np.mod(np.asarray(d["phi"][k], float), 2*np.pi),
                                  epo=float(d["epo"][k])))
        m, pumps, amps = config_metrics(law_cases, ref_cases)
        metrics[cfg] = m
        detail[cfg] = dict(pumps=pumps, amps=amps)
    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=1)
    with open("metrics-detail.json", "w") as f:
        json.dump(detail, f, indent=1, default=float)
    print(json.dumps(metrics, indent=1))


def cmd_picture():
    cases = load_cases()
    ref = np.load("truth-2400.npz")
    names = list(ref["names"])
    d1 = np.load("laws-nf2.npz")
    d2 = np.load("laws-nf1.npz")
    # pick one librating and one circulating case from truth-2400
    lib_name = circ_name = None
    for c in cases:
        if c["control"]:
            continue
        s = series_of_truth(ref, names.index(c["name"]))
        reg, _ = regime_and_amp(s["phi"])
        if reg == "libration" and lib_name is None:
            lib_name = c["name"]
        if reg == "circulation" and circ_name is None:
            circ_name = c["name"]
    if lib_name is None:
        lib_name = cases[0]["name"]
    if circ_name is None:
        circ_name = cases[-1]["name"]
    W, H = 900, 460
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">', '<rect width="100%" height="100%" fill="white"/>']
    for k, (nm, ttl) in enumerate(((lib_name, "librating"), (circ_name, "circulating"))):
        c = [x for x in cases if x["name"] == nm][0]
        i = names.index(nm)
        s = series_of_truth(ref, i)
        m0 = 1.0 - c["mu"]
        Gam_t = np.sqrt(m0*s["a"])*(1.0 - np.sqrt(np.maximum(1 - s["e"]**2, 0)))
        ph_t = np.unwrap(s["phi"])
        ph_t = np.mod(ph_t, 2*np.pi)
        x0, y0, w, h = 20 + k*445, 40, 400, 380
        parts.append(f'<text x="{x0+w/2}" y="24" font-size="14" text-anchor="middle" '
                     f'fill="#222">{nm} ({ttl}): (phi, Phi=Gamma1) law vs truth</text>')
        parts.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#999"/>')
        for tick in range(0, 361, 90):
            fx = x0 + w*tick/360
            parts.append(f'<line x1="{fx}" y1="{y0}" x2="{fx}" y2="{y0+h}" stroke="#eee"/>')
            parts.append(f'<text x="{fx}" y="{y0+h+14}" font-size="10" text-anchor="middle" fill="#666">{tick}</text>')
        def px(phi):
            return x0 + w*(np.mod(phi, 2*np.pi)/(2*np.pi))
        def py(G):
            gmax = max(Gam_t.max(), d1["e"][i].max())*1.15
            gmin = 0.0
            return y0 + h - h*(G - gmin)/(gmax - gmin)

        step = max(1, len(ph_t)//1400)
        pts = " ".join(f"{px(ph_t[q]):.1f},{py(Gam_t[q]):.1f}" for q in range(0, len(ph_t), step))
        parts.append(f'<polyline points="{pts}" fill="none" stroke="#d22" stroke-width="1" opacity="0.5"/>')
        # nf2 cycle: recompute Phi from e of law
        j = c["j"]
        Gam_l = None
        # Gamma from the law: use its own Lp: Phi = Lp + j*Gamma -> invert
        # simpler: plot e as Phi proxy is wrong; recompute Gamma from Lambda1
        # of the compiled cycle: not stored; use Gamma = (L1*... from e and a
        # of the law via conservation: Lp = L1 + j*Gm and e -> two unknowns.
        # Instead store enough: recompute the cycle here.
        m0v = 1.0 - c["mu"]
        L1 = math.sqrt(m0v*c["a1"])
        G0 = L1*(1.0 - math.sqrt(1.0 - R.E0*R.E0))
        Lp = L1 + j*G0
        g0 = -(j+1)*R.LAM20
        nf2 = R.NF(j, c["mu"], 2)
        cyc = nf2.compile_cycle(g0, G0, Lp)
        gg = np.unwrap(cyc["g"])
        L1c = cyc["Lp"] + j*cyc["G"]
        phc = np.mod(-gg, 2*np.pi)
        pts = " ".join(f"{px(phc[q]):.1f},{py(cyc['G'][q]):.1f}" for q in range(len(gg)))
        parts.append(f'<polyline points="{pts}" fill="none" stroke="#24c" stroke-width="1.4"/>')
        parts.append(f'<text x="{x0+8}" y="{y0+16}" font-size="11" fill="#24c">nf2 level curve</text>')
        parts.append(f'<text x="{x0+8}" y="{y0+30}" font-size="11" fill="#d22">truth (dense)</text>')
    parts.append('</svg>')
    with open("picture.svg", "w") as f:
        f.write("\n".join(parts))
    print("picture.svg written", lib_name, circ_name)

def cmd_dev():
    """Development sanity: 2:1 mu=3e-4 exact + control 2.55, N=1200."""
    cases = [dict(name="dev-21", j=1, mu=3e-4, n1=2.0, control=False,
                  a1=(1 - 3e-4)**(1/3)*(1/2)**(2/3)),
             dict(name="dev-ctl", j=1, mu=3e-3, n1=2.55**1.5, control=True,
                  a1=((1 - 3e-3)/(2.55**1.5)**2)**(1/3))]
    R.truth_batch(cases, 1200, "dev-truth.npz")
    ref = np.load("dev-truth.npz")
    for i, c in enumerate(cases):
        s = series_of_truth(ref, i)
        reg, amp = regime_and_amp(s["phi"])
        print(f"{c['name']}: truth e max {s['e'].max():.5f} min {s['e'].min():.5f} "
              f"regime {reg} amp {amp}")
    for c in cases:
        i = 0 if c["name"] == "dev-21" else 1
        s = series_of_truth(ref, i)
        j, mu = c["j"], c["mu"]
        m0 = 1.0 - mu
        L1 = math.sqrt(m0*c["a1"])
        G0 = L1*(1.0 - math.sqrt(1.0 - R.E0*R.E0))
        Lp = L1 + j*G0
        g0 = -(j+1)*R.LAM20
        for order in (1, 2):
            nf = R.NF(j, mu, order)
            cyc = nf.compile_cycle(g0, G0, Lp)
            if cyc is None:
                print(f"  nf{order}: no cycle!")
                continue
            phi, e, _ = nf.state_from_cycle(cyc, s["t"])
            reg, amp = regime_and_amp(np.mod(phi, 2*np.pi))
            print(f"  nf{order}: closed={cyc['closed']} period={cyc['period']:.3f} "
                  f"e max {e.max():.5f} regime {reg} amp {amp} "
                  f"evals/orbit {nf.n_evals/(s['t'][-1]*c['n1']/(2*np.pi)):.3f}")

if __name__ == "__main__":
    cmds = dict(cases=cmd_cases, truth=lambda: cmd_truth(int(sys.argv[2])),
                laws=cmd_laws, metrics=cmd_metrics, picture=cmd_picture, dev=cmd_dev)
    cmds[sys.argv[1]]()
