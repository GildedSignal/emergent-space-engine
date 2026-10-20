#!/usr/bin/env python3
"""Analyze the coretail flights: hazard windows, droplet law, clamp re-arm, channels."""
import json, math, sys
from pathlib import Path

FL = Path(__file__).parent / "flights"
STRIDE = 128
Q = 1 << 20


def load(name):
    core = []
    for ln in open(FL / f"{name}.core.tsv"):
        p = ln.split()
        core.append(dict(t=int(p[0]), n_live=int(p[1]), esc=int(p[2]), n_near=int(p[3]),
                         n_zone=int(p[4]), n_q1=int(p[5]), n_sub=int(p[6]), ct_tot=int(p[7]),
                         ct_near=int(p[8]), ct_zone=int(p[9]), ct_sub=int(p[10]),
                         cl_zone=int(p[11]), cl_sub=int(p[12]), ke_near=int(p[13]),
                         sr2_near=int(p[14]), ke_all=int(p[15]), maxk=int(p[16])))
    ev = [ln.split() for ln in open(FL / f"{name}.events.tsv")]
    body = []
    hdr = open(FL / f"{name}.body.tsv").readline()
    for ln in open(FL / f"{name}.body.tsv"):
        p = ln.split()
        if p[0] == "#":
            continue
        body.append(dict(id=int(p[0]), ring=int(p[1]), dead_t=int(p[2]), unbound_t=int(p[3]),
                         fclamp=int(p[4]), cl=int(p[5]), ct=int(p[6]), min_r=int(p[7]),
                         sub_s=int(p[8]), first_sub=int(p[9]), last_sub=int(p[10]),
                         zone_s=int(p[11])))
    head = (FL / f"{name}.head").read_text()
    return core, ev, body, head


def window_hazard(core, ev, w=8192):
    """deaths per live body per ch, windowed."""
    out = []
    tmax = core[-1]["t"]
    for t0 in range(w, tmax + 1, w):
        d = sum(1 for e in ev if e[0] == "D" and t0 - w < int(e[1]) <= t0)
        lives = [c["n_live"] for c in core if t0 - w < c["t"] <= t0]
        nbar = sum(lives) / len(lives) if lives else 0
        out.append((t0, d, nbar, d / (nbar * w) if nbar else 0.0))
    return out


def droplet_law(core, epoch=4096):
    """f = ct_tot / (stride * C(n_sub,2)) per epoch window; zone share."""
    out = []
    tmax = core[-1]["t"]
    for t0 in range(epoch, tmax + 1, epoch):
        rows = [c for c in core if t0 - epoch < c["t"] <= t0]
        if not rows:
            continue
        ct = sum(r["ct_tot"] for r in rows)
        czt = sum(r["ct_zone"] for r in rows)
        cst = sum(r["ct_sub"] for r in rows)
        clz = sum(r["cl_zone"] for r in rows)
        # pair-capacity-weighted f: sum over strides of ct/(stride*C(n_sub,2))
        fs, pairs = [], []
        for r in rows:
            nn = r["n_sub"]
            if nn >= 2:
                fs.append(r["ct_tot"] / (STRIDE * nn * (nn - 1) / 2))
                pairs.append(nn * (nn - 1) / 2)
            else:
                fs.append(float(r["ct_tot"]) / STRIDE)  # no capacity
                pairs.append(0.0)
        fpair = sum(r["ct_tot"] for r in rows) / (STRIDE * sum(pairs)) if sum(pairs) else 0.0
        nsub_med = sorted(r["n_sub"] for r in rows)[len(rows) // 2]
        out.append(dict(t=t0, ct_per_ch=ct / epoch, zone_share=czt / ct if ct else 0,
                        sub_share=cst / ct if ct else 0, f_pair=fpair, f_med=sorted(fs)[len(fs)//2],
                        n_sub_med=nsub_med, cl_zone=clz,
                        rms_near=math.sqrt(sum(r["sr2_near"] for r in rows) /
                                           max(1, sum(r["n_near"] for r in rows))) / Q))
    return out


def analyze(name):
    core, ev, body, head = load(name)
    res = {"head": head.splitlines()[1]}
    for ln in head.splitlines():
        if ln.startswith("# ck"):
            k, v = ln.split(" = ") if " = " in ln else (ln, "")
            res[ln.split()[1]] = ln
    deaths = sorted((int(e[1]), int(e[2])) for e in ev if e[0] == "D")
    res["n_dead"] = len(deaths)
    res["final_live"] = core[-1]["n_live"]
    res["final_n_sub"] = core[-1]["n_sub"]
    res["final_n_zone"] = core[-1]["n_zone"]
    # hazard windows
    hz = window_hazard(core, ev)
    res["hazard"] = [f"{t} {d} {n:.0f} {lam:.2e}" for t, d, n, lam in hz]
    res["hazard_late"] = [x for x in hz if x[0] > 98304]
    lam_late = [lam for _, _, _, lam in res["hazard_late"]]
    if lam_late:
        res["lam_late_max"] = max(lam_late)
        res["lam_late_med"] = sorted(lam_late)[len(lam_late) // 2]
    lam_mid = [lam for t, _, _, lam in hz if 49152 < t <= 98304]
    if lam_mid:
        res["lam_mid_med"] = sorted(lam_mid)[len(lam_mid) // 2]
    # droplet law
    dl = droplet_law(core)
    res["droplet"] = dl
    tail = [d for d in dl if d["t"] > 98304]
    if tail:
        res["f_pair_tail_med"] = sorted(x["f_pair"] for x in tail)[len(tail) // 2]
        res["zone_share_tail_min"] = min(x["zone_share"] for x in tail)
        res["n_sub_tail_min"] = min(x["n_sub_med"] for x in tail)
        res["n_sub_tail_max"] = max(x["n_sub_med"] for x in tail)
        xs = [x["t"] for x in tail]; ys = [x["n_sub_med"] for x in tail]
        nx = len(xs); mx = sum(xs) / nx; my = sum(ys) / nx
        res["n_sub_tail_slope_per_49k"] = (sum((x - mx) * (y - my) for x, y in zip(xs, ys)) /
                                           sum((x - mx) ** 2 for x in xs)) * 49152
    # tail deaths channels
    td = [b for b in body if b["dead_t"] >= 98304]
    if td:
        res["tail_deaths"] = len(td)
        res["tail_deaths_never_clamped"] = sum(1 for b in td if b["fclamp"] == 0)
        res["tail_deaths_subrecent"] = sum(1 for b in td
                                           if b["sub_s"] > 0 and b["dead_t"] - b["last_sub"] <= 512)
    # all dead: ever clamped
    res["dead_ever_clamped"] = sum(1 for b in body if b["dead_t"] > 0 and b["fclamp"] > 0)
    # survivors of the droplet
    live = [b for b in body if b["dead_t"] == 0]
    res["live_n"] = len(live)
    res["live_subres"] = sum(1 for b in live if b["sub_s"] >= len(core) // 2)
    res["live_ever_sub"] = sum(1 for b in live if b["sub_s"] > 0)
    res["live_ever_clamped"] = sum(1 for b in live if b["fclamp"] > 0)
    res["live_zone_res"] = sum(1 for b in live if b["zone_s"] >= len(core) // 2)
    res["min_r_min"] = min(b["min_r"] for b in body) / Q
    return res


out = {}
for name in sys.argv[1:]:
    out[name] = analyze(name)
json.dump(out, open(Path(__file__).parent / "analysis.json", "w"), indent=1)
for name, r in out.items():
    print(f"== {name}: {r['head']}")
    print(f"  dead={r['n_dead']} final_live={r['final_live']} n_sub={r['final_n_sub']} n_zone={r['final_n_zone']}")
    print(f"  lam_mid_med={r.get('lam_mid_med', float('nan')):.2e} lam_late_med={r.get('lam_late_med', float('nan')):.2e} lam_late_max={r.get('lam_late_max', float('nan')):.2e}")
    if "f_pair_tail_med" in r:
        print(f"  TAIL f_pair_med={r['f_pair_tail_med']:.3f} zone_share_min={r['zone_share_tail_min']:.3f} "
              f"n_sub[{r['n_sub_tail_min']},{r['n_sub_tail_max']}] slope49k={r['n_sub_tail_slope_per_49k']:.1f}")
    if "tail_deaths" in r:
        print(f"  tail_deaths={r['tail_deaths']} never_clamped={r['tail_deaths_never_clamped']} subrecent={r['tail_deaths_subrecent']}")
    print(f"  live: n={r['live_n']} ever_sub={r['live_ever_sub']} subres(half)={r['live_subres']} zone_res={r['live_zone_res']} ever_clamped={r['live_ever_clamped']} min_r_min={r['min_r_min']:.3f}q")
