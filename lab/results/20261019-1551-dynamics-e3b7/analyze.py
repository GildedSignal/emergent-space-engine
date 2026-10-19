#!/usr/bin/env python3
"""Gravity-held belt analysis: season, storm, branches, one-knob walls contrast."""
import sys, json, os

W = os.path.dirname(os.path.abspath(__file__)) + "/work/"

def load(name):
    ts, c, rattle, esc, n_in, walls, ke_in, sr2, ke_all, maxk, ops = [], [], [], [], [], [], [], [], [], [], []
    with open(W + name + ".tsv") as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.split()
            if len(p) != 11:
                continue
            ts.append(int(p[0])); c.append(int(p[1])); rattle.append(int(p[2]))
            esc.append(int(p[3])); n_in.append(int(p[4])); walls.append(int(p[5]))
            ke_in.append(int(p[6])); sr2.append(int(p[7])); ke_all.append(int(p[8]))
            maxk.append(int(p[9])); ops.append(int(p[10]))
    return dict(t=ts, c=c, rattle=rattle, esc=esc, n_in=n_in, walls=walls,
                ke_in=ke_in, sr2=sr2, ke_all=ke_all, maxk=maxk, ops=ops)

def winmeans(d, w=64):
    """mean contacts per w-chronon window, aligned at t=1."""
    out = []
    for i in range(0, len(d["t"]) // w):
        out.append(sum(d["c"][i * w:(i + 1) * w]))
    return out

def blockmeans(d, b):
    return [sum(d["c"][i:i + b]) for i in range(0, len(d["c"]) - b + 1, b)]

res = {}
for name in ["G_s1_h49152", "C_s1_h49152", "GW_s1_h24576", "G_s2_h16384", "C_s2_h16384"]:
    p = W + name + ".tsv"
    if not os.path.exists(p):
        continue
    res[name] = load(name)

out = {}
G = res["G_s1_h49152"]; C = res["C_s1_h49152"]
# P1: cold control
w = winmeans(C)
q1 = sum(w[: len(w) // 4]) / max(1, len(w) // 4)
q4 = sum(w[-(len(w) // 4):]) / max(1, len(w) // 4)
out["P1_cold"] = dict(esc_max=max(C["esc"]), n_in_last=C["n_in"][-1],
                      first_quarter_mean=q1, last_quarter_mean=q4, ratio=q4 / max(q1, 1e-9),
                      holds=(max(C["esc"]) == 0 and C["n_in"][-1] == 800 and q4 <= 3 * max(q1, 1e-9)))
# P2: season vs cold
gw = winmeans(G)
out["P2_season"] = dict(peak_window=max(gw), cold_mean_window=q1,
                        ratio=max(gw) / max(q1, 1e-9))
# storm peak block and late mean (1024-ch blocks)
bm = blockmeans(G, 1024)
peak_i = max(range(len(bm)), key=lambda i: bm[i])
late = bm[-8:]
out["P3"] = dict(esc_frac_at_16384=G["esc"][16383] / 1600.0, esc_last=G["esc"][-1] / 1600.0,
                 n_in_last=G["n_in"][-1],
                 peak_block=bm[peak_i], peak_index=peak_i,
                 late_mean_block=sum(late) / len(late), late_over_peak=(sum(late) / len(late)) / max(bm[peak_i], 1),
                 branch=("quench" if (sum(late) / len(late)) <= bm[peak_i] / 3
                         else ("grinder" if (sum(late) / len(late)) >= 2 * bm[peak_i] / 3 else "middle")),
                 rattle_frac_late=sum(G["rattle"][-8192:]) / max(1, sum(G["c"][-8192:])),
                 contacts_total=sum(G["c"]))
# P5: energy honesty, all arms
p5 = {}
for k, d in res.items():
    ke = d["ke_all"]; peak = max(ke)
    ip = ke.index(peak)
    after = ke[ip:]
    p5[k] = dict(maxk_first=d["maxk"][min(500, len(d["maxk"]) - 1)], maxk_last=d["maxk"][-1],
                 ke_peak=peak, ke_last=ke[-1],
                 rise_after_peak=(max(after) - peak) / max(1, peak))
out["P5"] = p5
# P4: walls flip
if "GW_s1_h24576" in res:
    GW = res["GW_s1_h24576"]
    www = winmeans(GW)
    late_w = sum(www[-len(www) // 4:]) / max(1, len(www) // 4)
    cold_mean = q1
    out["P4_walls"] = dict(esc_max=max(GW["esc"]), esc_last=GW["esc"][-1], n_in_last=GW["n_in"][-1],
                           walls_total=sum(GW["walls"]), late_mean_window=late_w,
                           cold_mean_window=cold_mean, ratio=late_w / max(cold_mean, 1e-9))
# seed 2 robustness
if "G_s2_h16384" in res:
    G2 = res["G_s2_h16384"]
    bm2 = blockmeans(G2, 1024)
    out["G_s2"] = dict(esc_last=G2["esc"][-1] / 1600.0, n_in_last=G2["n_in"][-1],
                       peak_block=max(bm2), last_block=bm2[-1])
# when did esc cross 50%/90%?
def cross(d, frac):
    for i, e in enumerate(d["esc"]):
        if e >= frac * 1600:
            return d["t"][i]
    return None
out["timing"] = dict(esc50=cross(G, 0.5), esc90=cross(G, 0.9),
                     esc50_s2=cross(res["G_s2_h16384"], 0.5) if "G_s2_h16384" in res else None)
print(json.dumps(out, indent=1))
with open(W + "analysis.json", "w") as f:
    json.dump(out, f, indent=1)
