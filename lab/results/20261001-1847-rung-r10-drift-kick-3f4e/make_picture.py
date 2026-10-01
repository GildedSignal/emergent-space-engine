#!/usr/bin/env python3
"""The rung's one picture: |dC_J/C_J| against time (planet periods) for each configuration,
on three ships (the three with the most SOI crossings)."""

import json
import math
import os

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

sel = json.load(open("b12_sel.json"))
order = sorted(range(len(sel["kept"])), key=lambda i: -sel["kept"][i]["crossings"])
ships = order[:3]
N = 200 * 8 + 1
t = np.array([j / 8 for j in range(N)])

cj = np.array([sel["kept"][i]["cj"] for i in ships])
cj0 = cj[:, 0]
truth_err = np.abs(cj - cj0[:, None]) / np.abs(cj0)[:, None]

colors = {"truth": "#4059ad", "symba": "#1b998b", "wh-fixed": "#c1666b", "soi-switch": "#8d6a9f"}
labels = {"truth": "truth (DOP853 1e-12)", "symba": "symba (smooth changeover)",
          "wh-fixed": "wh-fixed (no changeover)", "soi-switch": "soi-switch (hard, events3)"}

fig, ax = plt.subplots(figsize=(8.6, 5.4), dpi=140)
ax.plot(t, truth_err.T if truth_err.ndim > 1 else truth_err[None].T,
        color=colors["truth"], lw=1.0, alpha=0.8, label=labels["truth"])
for cfg in ["symba", "wh-fixed", "soi-switch"]:
    e = np.load(f"cand_{cfg}_b12err.npy")[ships]
    for row in e:
        row = np.clip(row, 1e-18, None)
        ax.plot(t, row, color=colors[cfg], lw=1.0, alpha=0.8)
    ax.plot([], [], color=colors[cfg], lw=1.2, label=labels[cfg])

ax.set_yscale("log")
ax.set_xlabel("planet periods")
ax.set_ylabel(r"$|\Delta C_J / C_J|$")
ax.axhline(1e-12, color="k", lw=0.6, ls=":", alpha=0.7)
ax.axhline(1e-4, color="k", lw=0.6, ls="--", alpha=0.7)
ax.text(0.4, 1.3e-12, "float floor 1e-12", fontsize=7)
ax.text(0.4, 1.4e-4, "B12 max 1e-4", fontsize=7)
ax.set_title("r10: Jacobi error on three ships (most SOI crossings: "
             f"{[sel['kept'][i]['crossings'] for i in ships]} crossings / 200 periods)")
ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
ax.grid(alpha=0.25, which="both", lw=0.4)
fig.tight_layout()
fig.savefig("picture.png")
print("picture.png written")
