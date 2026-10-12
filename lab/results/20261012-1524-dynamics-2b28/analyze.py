#!/usr/bin/env python3
"""Analyze the decisive ensemble of run 20261012-1524-dynamics-2b28."""
import json, glob, math
import numpy as np

def load(pat):
    out = []
    for f in sorted(glob.glob(pat)):
        with open(f) as fh:
            out.append(json.load(fh))
    return out

L = []
def p(s=""):
    print(s)
    L.append(s)

p("# Ensemble analysis (dynamics lens)\n")

# ---------- A: feedback ----------
ctl = load("A_ctl_s*.json")
T = ctl[0]["cfg"]["T"]; N = ctl[0]["cfg"]["N"]
W = 150  # rate window (orbits)
nw = int(T // W)
ctl_rate = np.zeros(nw)
for c in ctl:
    eh = np.array(c["enc_hist"][: nw * W]).reshape(nw, W).sum(1)
    ctl_rate += eh / (N * W)
ctl_rate /= len(ctl)
p(f"Control encounter rate per body per orbit: {ctl_rate.mean():.3e} "
  f"(window spread {ctl_rate.min():.2e}..{ctl_rate.max():.2e})")

p("\n## A. Feedback scan (belt, N=512, T=1500, mean of 3 seeds)\n")
p("| mu | R_med | A_early | A_mid | A_end | e2 xgrowth | deaths | repay/enc | repay share |")
p("|---|---|---|---|---|---|---|---|---|")
for mu in [m for m in ["1e-9", "3e-8", "3e-7", "2e-6"] if load(f"A_mu{m}_s*.json")]:
    runs = load(f"A_mu{mu}_s*.json")
    As = np.zeros((len(runs), nw)); e2g = []; dth = []; rp = []; rsh = []
    Rall = []
    for r, d in enumerate(runs):
        eh = np.array(d["enc_hist"][: nw * W]).reshape(nw, W).sum(1) / (N * W)
        As[r] = eh / ctl_rate
        e2g.append(d["e2_curve_v"][-1] / d["e2_curve_v"][0])
        dth.append(d["deaths"]); rp.append(d["repay_ops"] / max(d["kicks"], 1))
        rsh.append(d["repay_ops"] / (d["repay_ops"] + d["conjunctions"]))
        Rall += d["enc_R"]
    A = As.mean(0)
    p(f"| {mu} | {np.median(Rall):.1f} | {A[0]:.2f} | {A[nw//2]:.2f} | "
      f"{A[-1]:.2f} | {np.mean(e2g):.2f} | {int(np.mean(dth)*100/N):.1f}% | "
      f"{np.mean(rp):.0f} | {np.mean(rsh):.2f} |")

p("\nA(t) window means per mu (cascade check: any window >1.1 * first window?):")
for mu in [m for m in ["1e-9", "3e-8", "3e-7", "2e-6"] if load(f"A_mu{m}_s*.json")]:
    runs = load(f"A_mu{mu}_s*.json")
    As = []
    for d in runs:
        eh = np.array(d["enc_hist"][: nw * W]).reshape(nw, W).sum(1) / (N * W)
        As.append(eh / ctl_rate)
    A = np.mean(As, 0)
    p(f"  mu={mu}: " + " ".join(f"{x:.2f}" for x in A))

# e-growth decomposition: d<e2>/dt vs Gamma*<de^2>
p("\nStirring check (mu=3e-7, seed 1): measured d<e2>/dt vs Gamma*<de^2> per body:")
d = load("A_mu3e-7_s1.json")[0]
t = np.array(d["e2_curve_t"]); v = np.array(d["e2_curve_v"])
slope = np.polyfit(t[1:], v[1:], 1)[0]
de = np.array(d["enc_de"]); Gamma = d["encounters"] / (N * d["cfg"]["T"])
p(f"  d<e2>/dt = {slope:.3e}/orbit ; Gamma*mean(de^2) = {Gamma*np.mean(de**2):.3e} "
  f"(coherent pumping would give ~2e*de: {Gamma*np.mean(2*np.sqrt(v[0])*de):.3e})")

# ---------- B: N scaling ----------
p("\n## B. N scaling at fixed linear density (mu=1e-9, T=300, mean of 2 seeds)\n")
p("| N | conj/body/orb | enc/body/orb | repay/enc | repay share | work tot (Mops) |")
p("|---|---|---|---|---|---|")
rows = []
for Nn in [Nn for Nn in [512, 1024, 2048] if load(f"B_N{Nn}_s*.json")]:
    runs = load(f"B_N{Nn}_s*.json")
    cj = np.mean([d["conjunctions"] / (Nn * d["cfg"]["T"]) for d in runs])
    en = np.mean([d["encounters"] / (Nn * d["cfg"]["T"]) for d in runs])
    rp = np.mean([d["repay_ops"] / max(d["kicks"], 1) for d in runs])
    rsh = np.mean([d["repay_ops"] / (d["repay_ops"] + d["conjunctions"]) for d in runs])
    wk = np.mean([(d["repay_ops"] + d["conjunctions"]) / 1e6 for d in runs])
    rows.append((Nn, cj, en, rp, rsh, wk))
    p(f"| {Nn} | {cj:.3f} | {en:.2e} | {rp:.0f} | {rsh:.2f} | {wk:.1f} |")
for k, name in [(1, "conj/body"), (2, "enc/body")]:
    x = np.log([r[0] for r in rows]); y = np.log([r[k] for r in rows])
    p(f"exponent {name} vs N: {np.polyfit(x, y, 1)[0]:+.3f}")

# ---------- C: formations ----------
p("\n## C. Formation bursts (N=32, T=3000)\n")
p("| cfg | enc tot | R_med | peak/mean (50-orb) | Fano (1-orb) | first3/last3 peak/mean |")
p("|---|---|---|---|---|---|")
for mu in ["1e-11", "1e-8"]:
    for form in ["aligned", "random"]:
        runs = load(f"C_{form}_mu{mu}_s*.json")
        pm = []; fano = []; dec = []; ens = []; Rs = []
        for d in runs:
            et = np.array(d["enc_times"])
            h, _ = np.histogram(et, bins=np.arange(0, 3001, 50))
            pm.append(h.max() / max(h.mean(), 1e-9))
            h1, _ = np.histogram(et, bins=np.arange(0, 3001, 1))
            fano.append(h1.var() / max(h1.mean(), 1e-9))
            f3 = h[:60].max(); l3 = h[-60:].max()
            dec.append((f3, l3))
            ens.append(d["encounters"]); Rs += d["enc_R"]
        p(f"| {form} mu={mu} | {np.mean(ens):.0f} | {np.median(Rs):.1f} | "
          f"{np.mean(pm):.1f} | {np.mean(fano):.1f} | "
          f"{np.mean([a for a,_ in dec]):.0f}->{np.mean([b for _,b in dec]):.0f} |")

# belt Fano for contrast
fan = []
for d in load("B_N512_s*.json"):
    h1 = np.array(d["enc_hist"])
    fan.append(h1.var() / max(h1.mean(), 1e-9))
if fan:
    p(f"\nBelt Fano (per-orbit counts, mu=1e-9, mixed): {np.mean(fan):.2f}")

with open("summary.md", "w") as f:
    f.write("\n".join(L) + "\n")
print("\nwrote summary.md")

# mu=1e-9 datapoint from B runs (T=300) vs control first 300 orbits
bs = load("B_N512_s*.json")
if bs:
    r = np.mean([d["encounters"]/(512*300) for d in bs])
    c300 = np.array([np.array(x["enc_hist"][:300]).sum()/(512*300) for x in ctl]).mean()
    p(f"\nmu=1e-9 (T=300, B runs): enc rate {r:.3e}/body/orb vs control {c300:.3e} -> A = {r/c300:.2f}")
    for d in bs[:2]:
        h1 = np.array(d["enc_hist"]); p(f"  B mu=1e-9 Fano: {h1.var()/max(h1.mean(),1e-9):.1f}")
