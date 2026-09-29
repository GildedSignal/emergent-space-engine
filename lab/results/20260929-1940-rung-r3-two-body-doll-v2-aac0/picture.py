#!/usr/bin/env python3
"""Stage 5: the picture. Transfer path with handoff points; dv vs impact parameter."""
import sys, json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

# ---- panel 1: 6 years of the transfer in the co-rotating frame
try:
    path = np.array(json.load(open('handoff_path6yr.json')))
    data = json.load(open('handoff_data.json'))
    om = 2 * math.pi
    # rotate each point back by planet phase so the planet sits at (1, 0)
    ts = np.arange(len(path)) * 2e-3
    c, s = np.cos(om * ts), np.sin(om * ts)
    xr = path[:, 0] * c + path[:, 1] * s
    yr = -path[:, 0] * s + path[:, 1] * c
    ax1.plot(xr, yr, '-', lw=0.8, color='#7a6a55')
    # reference crossing points (first 12 crossings within 6 yr)
    ct = np.array(data['cross_t'])
    rxy = np.array(data['ref_xy'])
    m = ct < 6.0
    cr, sr = np.cos(om * ct[m]), np.sin(om * ct[m])
    cx = rxy[m, 0] * cr + rxy[m, 1] * sr
    cy = -rxy[m, 0] * sr + rxy[m, 1] * cr
    ax1.plot(cx, cy, 'o', ms=5, mfc='none', mec='#b3541e', mew=1.4,
             label='SOI handoffs (ref)')
    th = np.linspace(0, 2 * np.pi, 200)
    from r3lib import SOI
    ax1.plot(1 + SOI * np.cos(th), SOI * np.sin(th), ':', color='#b3541e', lw=1,
             label='planet SOI')
    ax1.plot(0, 0, '*', color='#c9a227', ms=14, label='star')
    ax1.plot(1, 0, 'o', color='#4a6b8a', ms=7, label='planet')
    ax1.set_xlabel('x [AU], co-rotating')
    ax1.set_ylabel('y [AU], co-rotating')
    ax1.set_title(f'transfer, 6 yr co-rotating; {len(ct)} crossings in 50 yr')
    ax1.legend(fontsize=8, loc='upper right')
    ax1.set_aspect('equal')
except Exception as ex:
    ax1.set_title(f'handoff data unavailable: {ex}')

# ---- panel 2: assist dv error vs impact parameter
res = json.load(open('assists.json'))
b = np.array([r['b'] for r in res]) * 1 / 6.371e3 * 1.495978707e8 / 1.495978707e8
bRE = np.array([r['b'] for r in res]) / (6371e3 / 1.495978707e11)
err = np.array([r['err'] for r in res])
o = np.argsort(bRE)
ax2.loglog(bRE[o], err[o], 'o-', ms=4, lw=0.9, color='#7a6a55', label='doll vs N-body')
ax2.axhline(0.01, color='#b3541e', ls='--', lw=1, label='1% tolerance')
ax2.set_xlabel('impact parameter [planet radii]')
ax2.set_ylabel('|ΔΔv| / |Δv_ref|')
ax2.set_title(f'gravity assists: pass fraction {(err <= 0.01).mean():.3f}')
ax2.legend(fontsize=8)
ax2.grid(alpha=0.25, which='both')

plt.tight_layout()
plt.savefig('picture.png', dpi=140)
print("picture.png written")
