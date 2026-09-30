#!/usr/bin/env python3
"""Picture for rung r4 v2: e1(t) law vs truth per case + resonant-angle histogram."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, "samples")

def load(tag, case):
    z = np.load(os.path.join(S, f"{tag}-{case}.npz"))
    return z["t"], z["e"], z["phi"]

CASES = ["r2-base", "r2-shift", "c-5.00", "c-2.55", "c-2.15"]
TITLES = {
    "r2-base": "2:1 resonant (base)",
    "r2-shift": "2:1 resonant (phase-shifted, $w_2$=4)",
    "c-5.00": "control, period ratio 5.00",
    "c-2.55": "control, period ratio 2.55",
    "c-2.15": "control, period ratio 2.15",
}
LAWS = [("arc-g8", "#d62728", "-"), ("arc-g16", "#9467bd", "-"),
        ("arc-g8-half", "#ff7f0e", "-")]
SYN = {"r2-base": 4*np.pi, "r2-shift": 4*np.pi, "c-5.00": 2*np.pi/0.8,
       "c-2.55": 2*np.pi/(1-1/2.55), "c-2.15": 2*np.pi/(1-1/2.15)}

fig, axes = plt.subplots(2, 3, figsize=(16, 8))
for i, c in enumerate(CASES):
    ax = axes[i // 3][i % 3]
    tt, te, _ = load("truth2400", c)
    ax.plot(tt / SYN[c], te, color="k", lw=1.4, label="truth (2400/orbit)")
    for name, col, ls in LAWS:
        tl, el, _ = load(name, c)
        ax.plot(tl / SYN[c], el, color=col, lw=0.9, ls=ls, alpha=0.85, label=name)
    ta, ea, _ = load("averaged", c)
    ax.plot(ta / SYN[c], ea, color="#8c564b", lw=0.7, ls=":", label="averaged")
    ax.set_title(TITLES[c])
    ax.set_xlabel("synodic periods")
    ax.set_ylabel("$e_1$")
    ax.set_ylim(0, None)
    if i == 0:
        ax.legend(fontsize=8, loc="upper left")

# histogram panel: resonant angle, base case
ax = axes[1][2]
bins = np.linspace(0, 2*np.pi, 49)
tt, te, tph = load("truth2400", "r2-base")
ax.hist(np.asarray(tph) % (2*np.pi), bins=bins, density=True, color="k",
        alpha=0.45, label="truth")
for name, col, ls in LAWS[:2]:
    _, _, ph = load(name, "r2-base")
    ax.hist(np.asarray(ph) % (2*np.pi), bins=bins, density=True, histtype="step",
            color=col, lw=1.2, label=name)
_, _, pha = load("averaged", "r2-base")
ax.hist(np.asarray(pha) % (2*np.pi), bins=bins, density=True, histtype="step",
        color="#8c564b", lw=1.0, ls=":", label="averaged")
ax.set_title("resonant angle $\\phi=2\\lambda_2-\\lambda_1-\\varpi_1$, 2:1 base")
ax.set_xlabel("$\\phi$ [rad]")
ax.set_ylabel("density")
ax.legend(fontsize=8)

# metrics panel
ax = axes[0][2]
ax.axis("off")
m = json.load(open(os.path.join(HERE, "metrics.json")))
rows = [("config", "pump\nmin", "pump\nmax", "lib", "ctrl", "kicks")]
for k, v in m.items():
    rows.append((k, f"{v['e_pump_ratio_min']:.2f}", f"{v['e_pump_ratio_max']:.2f}",
                 f"{v['libration_ratio_min']:.2f}", f"{v['control_pass_fraction']:.2f}",
                 f"{v['kicks_per_orbit']:.2f}"))
tab = ax.table(cellText=rows[1:], colLabels=rows[0], loc="center",
               cellLoc="center")
tab.scale(1, 1.7)
tab.auto_set_font_size(False)
tab.set_fontsize(9)
ax.set_title("metrics (criteria: pump_min$\\geq$0.8, pump_max$\\leq$1.25, "
             "lib$\\geq$0.8, ctrl$\\geq$1.0, kicks$\\leq$8)")

fig.suptitle("Rung r4 v2: arc-integrated (Gauss-Picard) conjunction kicks vs 2:1 resonance — "
             "m2/M = 3e-3, e1_0 = 0.05, 200 synodic periods", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(HERE, "picture.svg"))
fig.savefig(os.path.join(HERE, "picture.png"), dpi=110)
print("wrote picture.svg / picture.png")
