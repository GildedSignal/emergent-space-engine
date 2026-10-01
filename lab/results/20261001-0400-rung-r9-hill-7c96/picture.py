"""One picture for Julien: (a) precession error vs tau with tau0 marked,
(b) truth's bound fraction vs a/R_H (the Hill stability edges) and kick-avg's
running class-match fraction, (c) a Poincare section in Hill units (rotating
frame, y=0, ydot>0) from the truth, tori and chaotic sea coloured.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import RH
from cands import TS, DT, T_EVAL

with open("table.json") as f:
    rows = json.load(f)
with open("metrics.json") as f:
    M = json.load(f)
tau0 = M["kick-avg"]["tau0"]
shards = [np.load(f"truth_shard{k}.npz") for k in range(4)]

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4))

# (a) precession error vs tau
ax = axes[0]
for key, lab, mkr in (("nu_kick", "kick-avg", "o"), ("nu_hill", "hill-torus (declared)", "^")):
    t_ = [r["tau"] for r in rows if not r["escaped"] and r[key] is not None and r["nu_truth"]]
    e_ = [abs(r[key] - r["nu_truth"]) / abs(r["nu_truth"]) for r in rows
          if not r["escaped"] and r[key] is not None and r["nu_truth"]]
    ax.loglog(t_, np.clip(e_, 3e-3, 1e3), mkr, ms=3, alpha=0.55, label=lab)
ax.axhline(0.1, color="k", lw=0.8, ls="--")
ax.axvline(tau0, color="crimson", lw=1.2)
ax.text(tau0 * 1.15, 3e-3, f"$\\tau_0$={tau0:.3f}", color="crimson", fontsize=9)
ax.set_xlabel(r"tidal ratio $\tau$")
ax.set_ylabel("precession error vs truth")
ax.set_title("(a) where orbit-averaged kicks stop")
ax.legend(fontsize=8, loc="upper left")

# (b) truth bound fraction vs a/R_H + kick-avg running class match
ax = axes[1]
grid = np.linspace(0.1, 0.95, 18)
for retro, lab, col in ((False, "prograde", "tab:blue"), (True, "retrograde", "tab:green")):
    sub = [r for r in rows if r["retro"] == retro]
    fb = [np.mean([not r["escaped"] for r in sub if abs(r["aRH"] - g) < 0.075]) for g in grid]
    ax.plot(grid, fb, color=col, label=f"truth bound ({lab})")
taus = sorted(r["tau"] for r in rows)
cm = []
for tstar in taus:
    sub = [r for r in rows if r["tau"] <= tstar and not r["chaotic"]]
    cm.append((tstar, np.mean([not r["escaped"] for r in sub])))
ax.plot([c[0] for c in cm], [c[1] for c in cm], "k-", lw=1, label="kick-avg class match")
ax.axhline(0.99, color="k", lw=0.8, ls="--")
ax.axvline(tau0, color="crimson", lw=1.2)
ax.set_xlabel(r"$\tau$   (prograde edge $\tau\approx0.085$ is $a/R_H\approx0.5$)")
ax.set_ylabel("fraction")
ax.set_title("(b) Hill stability edges")
ax.legend(fontsize=8, loc="center left")

# (c) Poincare section in Hill units
ax = axes[2]
for r in rows[:]:
    u = shards[r["i"] // 64][f"u{r['i']}"].astype(np.complex128)
    v = np.gradient(u, T_EVAL)
    y, yp = u.imag, v.imag
    idx = np.where((y[:-1] * y[1:] < 0) & (yp[:-1] > 0))[0]
    fr = y[idx] / (y[idx] - y[idx + 1])
    x = u.real[idx] + fr * (u.real[idx + 1] - u.real[idx])
    vx = v.real[idx] + fr * (v.real[idx + 1] - v.real[idx])
    col = ("#d62728" if r["escaped"] else ("#ff7f0e" if r["chaotic"] else "#1f77b4"))
    ax.scatter(x / RH, vx / RH, s=1.5, c=col, alpha=0.45, linewidths=0)
ax.set_xlim(-3, 3)
ax.set_ylim(-4, 6)
ax.set_xlabel("x / R_H")
ax.set_ylabel(r"$\dot{x}$ / (R_H n_p)")
ax.set_title("(c) Poincare section (Hill units)")
import matplotlib.lines as mlines
ax.legend(handles=[mlines.Line2D([], [], color=c, marker="o", ls="", ms=4, label=l)
                   for c, l in (("#1f77b4", "bound regular"), ("#ff7f0e", "bound chaotic"),
                                ("#d62728", "escaped"))], fontsize=8, loc="upper left")

fig.suptitle("rung r9: the Hill regime - class and precession vs tau, tori and chaotic sea", fontsize=11)
fig.tight_layout()
fig.savefig("picture.svg", dpi=110)
fig.savefig("picture.png", dpi=110)
print("wrote picture.svg / picture.png")
