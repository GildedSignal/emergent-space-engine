"""One picture: transfer path with handoff points (rotating frame), and flyby
dv against impact parameter, law against reference."""
import json
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

WORK = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(WORK)

transfer = json.load(open(f"{WORK}/transfer.json"))
assists = json.load(open(f"{WORK}/assists.json"))

plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white",
                     "savefig.facecolor": "white", "text.color": "black",
                     "axes.labelcolor": "black", "xtick.color": "black",
                     "ytick.color": "black"})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2), facecolor="white")

lp = transfer["law_path_rot"]
rp = transfer["ref_path_rot"]
ax1.plot([p[1] for p in lp], [p[2] for p in lp], lw=0.7, color="#22617a",
         label="law (patched dolls)")
ax1.plot([p[1] for p in rp], [p[2] for p in rp], lw=0.7, color="#b0552a",
         alpha=0.8, label="reference (N-body)")
cx = [c[0] for c in transfer["crossings"]]
# handoff points: evaluate law path nearest each crossing time
hx, hy = [], []
for t in cx:
    best = min(lp, key=lambda p: abs(p[0] - t))
    hx.append(best[1])
    hy.append(best[2])
ax1.scatter(hx, hy, s=9, color="k", zorder=5, label="handoffs (100)")
ax1.scatter([1.0], [0.0], s=60, color="#c9a227", marker="*", zorder=6,
            label="planet")
ax1.scatter([0.0], [0.0], s=80, color="#777", marker="+", zorder=6,
            label="star")
ax1.set_xlabel("rotating-frame x (AU)")
ax1.set_ylabel("rotating-frame y (AU)")
ax1.set_title("Transfer: 2:1 resonant chain, 100 handoffs, 50 planet periods")
ax1.legend(loc="upper left", fontsize=8)
ax1.set_aspect("equal")

bs = [r["b_rplanet"] for r in assists]
dv_l = [math.hypot(*r["dv_law"]) for r in assists]
dv_r = [math.hypot(*r["dv_ref"]) for r in assists]
o = sorted(range(len(bs)), key=lambda i: bs[i])
ax2.loglog([bs[i] for i in o], [dv_r[i] for i in o], lw=1.2, color="#b0552a",
           label="reference")
ax2.scatter(bs, dv_l, s=16, color="#22617a", zorder=5, label="law")
ax2.set_xlabel("impact parameter b (planet radii)")
ax2.set_ylabel("heliocentric |dv| of the flyby")
ax2.set_title("Gravity assists: law vs reference (64 flybys, v_inf = 10 km/s)")
ax2.legend(fontsize=8)
worst = max(r["rel_err"] for r in assists)
ax2.text(0.03, 0.06, f"worst relative error {worst*100:.2f}%",
         transform=ax2.transAxes, fontsize=9)

plt.tight_layout()
plt.savefig(f"{RUN}/picture.png", dpi=110)
print("wrote picture.png")
