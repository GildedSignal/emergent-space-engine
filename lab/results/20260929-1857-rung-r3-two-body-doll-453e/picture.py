"""Picture: transfer path with handoff points + flyby dv vs impact parameter."""
import json
import math
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SOI = 0.006178008505674118
G = 39.478417604357434


def ref_path(t_end, n=1200):
    r = 1.0 + 3e-3
    v = math.sqrt(G/r)
    inp0 = f"{r:.17g} 0.0 0.0 {-v:.17g}\n"
    out = subprocess.run(["./rung3_ships", "ref3", str(t_end)], input=inp0,
                         capture_output=True, text=True, timeout=600)
    cross = []
    for line in out.stdout.split("\n"):
        f = line.split()
        if f and f[0] == "CROSS":
            cross.append((float(f[2]), int(f[3]), [float(x) for x in f[4:6]]))
    # sample the path via ref3state
    ts = [i*t_end/n for i in range(n+1)]
    pts = []
    for t in ts:
        o = subprocess.run(["./rung3_ships", "ref3state", repr(t)], input="0.0 "+inp0,
                           capture_output=True, text=True).stdout.split()
        v_ = [float(x) for x in o[1:]]
        pts.append((v_[1], v_[2]))
    return cross, pts


cross, pts = ref_path(6.0)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))

px, py = zip(*pts)
ax1.plot(px, py, '-', color="#7a6a55", lw=0.8, label="ship (N-body reference), 6 yr")
th = [2*math.pi*i/720 for i in range(721)]
ax1.plot([math.cos(t) for t in th], [math.sin(t) for t in th], ':', color="#b0a89a", lw=0.8, label="planet orbit")
ax1.plot(0, 0, '*', color="#c9a227", ms=14, label="star")
c6 = [c for c in cross if c[0] <= 6.0][:26]
ent = [(c[2][0], c[2][1]) for c in c6 if c[1] == -1]
exi = [(c[2][0], c[2][1]) for c in c6 if c[1] == 1]
ax1.plot(*zip(*ent) if ent else [(), ], 'o', color="#3d7ea6", ms=5, label="SOI entry handoffs")
ax1.plot(*zip(*exi) if exi else [(), ], 's', color="#a63d3d", ms=5, label="SOI exit handoffs")
ax1.set_aspect("equal")
ax1.set_xlabel("AU"); ax1.set_ylabel("AU")
ax1.set_title("Counter-rotating co-orbital transfer: 2 SOI handoffs/yr\n(ship r = 1.003 AU retrograde; 100 handoffs over 25 yr)")
ax1.legend(loc="upper right", fontsize=8)

rows = json.load(open("fly_rows.json"))
for cfg, col, mk in (("schw", "#3d7ea6", "o"), ("kepler", "#a63d3d", "x")):
    rr = sorted(rows[cfg], key=lambda r: r["b"])
    ax2.plot([r["b"] for r in rr], [r["magr"] for r in rr], '-', color=col, lw=1.2, label=f"|Δv| reference")
    ax2.plot([r["b"] for r in rr], [r["mag"] for r in rr], mk, color=col, ms=4.5,
             mfc='none' if mk == "o" else None, label=f"|Δv| {cfg} doll")
ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlabel("impact (pericentre) parameter  [planet radii]")
ax2.set_ylabel("|heliocentric Δv|  [AU/yr]")
ax2.set_title("Gravity assists from the moving planet (v∞ = 6 km/s):\ndoll vs N-body, worst vector error 0.57% (gate 1%)")
ax2.legend(fontsize=8)

fig.suptitle("Rung r3 — handoffs and assists behave; the 1PN EOB doll does not (see metrics.json)", fontsize=11)
fig.tight_layout()
fig.savefig("picture.png", dpi=140)
print("saved picture.png")
