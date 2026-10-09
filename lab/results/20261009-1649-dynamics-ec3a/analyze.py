#!/usr/bin/env python3
"""Summarize the decisive runs against predictions.md."""
import json, glob, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base = os.path.dirname(os.path.abspath(__file__))
labels = [("C0_main", "C0 main (m'=0.03, e'=0.05)"),
          ("C1_nomass", "C1 negative (m'=0)"),
          ("C2_edge", "C2 positive (edge, e'=0.15)"),
          ("H1_mass2x", "H1 held-out (m'=0.06)"),
          ("H2_ee03", "H2 held-out (e'=0.3)"),
          ("H3_j2", "H3 held-out (J2=0.01)")]

rows = []
data = {}
for key, lab in labels:
    p = os.path.join(base, "runs", key + ".json")
    if not os.path.exists(p):
        continue
    d = json.load(open(p))
    data[key] = d
    m1 = d["mults"][0]
    rows.append((lab, d["live_frac"], d["ejected_frac"], m1["r_key"]["mean"],
                 m1["r_key"]["median"], m1["r_key"]["p99"], m1["S_key_p99_over_mean"],
                 m1["waste_uniform_key"], m1["frac"]["frozen"], m1["frac"]["librarian"],
                 m1["frac"]["walker"], d["burst_bin_over_mean"], m1["hot_frac_10x_median"]))

print("=" * 130)
print("%-34s %5s %6s | %9s %9s %9s | %5s %5s | %5s %5s %5s | %5s %5s" % (
    "config", "live", "eject", "mean r", "med r", "p99 r", "S", "waste",
    "froz", "lib", "walk", "burst", "hot10"))
for r in rows:
    print("%-34s %5.2f %6.3f | %9.3g %9.3g %9.3g | %5.1f %5.2f | %5.2f %5.2f %5.2f | %5.1f %5.2f" % r)

print("\nquantum scaling (mean a-rate, median e-rate, frac_zero key):")
for key, lab in labels:
    if key not in data:
        continue
    d = data[key]
    s = ["%-30s" % lab]
    for m in d["mults"]:
        s.append("m%-4g a:%9.3g e:%8.3g 0:%.2f" % (m["mult"], m["r_a"]["mean"],
                 m["r_e"]["median"], m["r_key"]["median"] == 0))
    print("  ".join(s))

# per-a scatter for C0 and C2
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=False)
for ax, key, title in zip(axes, ["C0_main", "C2_edge"],
                          ["C0 main belt [0.28,0.40]", "C2 edge belt [0.36,0.46], e'=0.15"]):
    if key not in data:
        continue
    z = np.load(os.path.join(base, "runs", key + ".npz"))
    a0, r_a, r_e, alive = z["a0"], z["r_a"], z["r_e"], z["alive"]
    ax.scatter(a0[alive], r_a[alive] + 1e-3, s=4, alpha=0.5, label="a-key rate")
    ax.scatter(a0[alive], r_e[alive] + 1e-3, s=4, alpha=0.5, label="e-key rate")
    ax.set_yscale("log")
    ax.set_xlabel("initial a (a' = 1)")
    ax.set_ylabel("quantum crossings per belt orbit")
    ax.set_title(title)
    for q, p, nm in [(1, 7, "7:1"), (1, 6, "6:1"), (1, 5, "5:1"), (1, 4, "4:1"),
                     (2, 9, "9:2"), (3, 11, "11:3")]:
        ar = (q / p) ** (2 / 3)
        if a0.min() < ar < a0.max():
            ax.axvline(ar, color="k", lw=0.5, ls=":")
            ax.text(ar, ax.get_ylim()[0] * 2, nm, fontsize=7, rotation=90)
    ax.legend(fontsize=7, loc="upper right")
plt.tight_layout()
plt.savefig(os.path.join(base, "rates_vs_a.png"), dpi=110)
print("\nwrote rates_vs_a.png")

# traces: frozen vs walker examples from C0
if "C0_main" in data:
    z = np.load(os.path.join(base, "runs", "C0_main.npz"))
    tr_a = z["tr_a"]  # (nsamp_tr, ntr)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.4))
    rng_a = z["a0"][:tr_a.shape[1]]
    med = np.median(z["r_a"] + z["r_e"])
    hot = np.argsort((z["r_a"] + z["r_e"]))[-8:][:8]
    cold = np.where((z["r_a"] + z["r_e"]) < med * 0.5)[0][:8]
    for i in hot:
        if i < tr_a.shape[1]:
            axes[0].plot(tr_a[:, i] - tr_a[0, i], lw=0.7)
    axes[0].set_title("C0 hottest 8 bodies: key index k_a(t) drift")
    axes[0].set_xlabel("time (a' orbits / 1)")
    for i in cold:
        if i < tr_a.shape[1]:
            axes[1].plot(tr_a[:, i] - tr_a[0, i], lw=0.7)
    axes[1].set_title("C0 coldest 8 bodies: k_a(t) bounded")
    plt.tight_layout()
    plt.savefig(os.path.join(base, "traces.png"), dpi=110)
    print("wrote traces.png")
