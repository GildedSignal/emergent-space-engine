import sys, json
sys.path.insert(0, '.')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hillkit import *

rows = [json.loads(l) for l in open('grid.jsonl')]
main = [r for r in rows if r['tag'] == 'main']
held = [r for r in rows if r['tag'] == 'heldout']
kf = [r for r in rows if r['tag'] == 'kickfloor']

print('=== MAIN GRID: relative apsidal-precession error ===')
print(f"{'a/RH':>6} {'e0':>4} {'s':>2} {'apse':>5} {'rel2Q':>9} {'rel1Q':>9} "
      f"{'truth wd/n_p':>12} {'emax tr':>7} {'emax 1Q':>7}")
for r in sorted(main, key=lambda r: (r['e0'], r['s'], r['aR'])):
    print(f"{r['aR']:>6.2f} {r['e0']:>4.1f} {r['s']:>2d} {str(r['apse']):>5} "
          f"{r.get('rel2Q', float('nan')):>9.4f} {r.get('rel1Q', float('nan')):>9.4f} "
          f"{r['truth_wdot']/NP:>12.4f} {r['e_max']:>7.4f} "
          f"{r.get('avg1Q_emax', float('nan')):>7.4f}")

print('\n=== HELD-OUT ===')
for r in held:
    print(f"a={r['aR']:.2f} e0={r['e0']:.2f} s={r['s']:+d} apse={r['apse']} "
          f"esc={r['escaped']} rel2Q={r.get('rel2Q')} rel1Q={r.get('rel1Q')} "
          f"emax_tr={r['e_max']:.4f} emax_1Q={r.get('avg1Q_emax', float('nan')):.4f}")

print('\n=== KICK FLOOR (rel error vs N) ===')
Ns = [2, 4, 8, 16, 32, 64]
for r in kf:
    errs = [r.get(f'rel_kick{N}') for N in Ns]
    print(f"a={r['aR']:.2f} e0={r['e0']:.2f} s={r['s']:+d} rel2Q={r.get('rel2Q'):.3f} "
          f"rel1Q={r.get('rel1Q'):.3f} kick_errs={['%.3f' % e if e else 'NA' for e in errs]}")
    good = [(N, e) for N, e in zip(Ns, errs) if e is not None]
    if len(good) >= 3:
        x = np.log([N for N, _ in good]); y = np.log([e for _, e in good])
        sl = np.polyfit(x, y, 1)[0]
        print(f'   fitted exponent {sl:.2f}')

# single-average truncation: exact tide single-avg minus closed quadrupole form
def single_avg_exact(a, e, w, lam, nE=2048):
    Es = np.linspace(0, TWO_PI, nE, endpoint=False)
    rs = a * (1 - e * np.cos(Es))
    wgt = (1 - e * np.cos(Es)); wgt /= wgt.sum()
    f_t = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(Es / 2),
                         np.sqrt(1 - e) * np.cos(Es / 2))
    th = w + f_t
    xs, ys = rs * np.cos(th), rs * np.sin(th)
    ddx, ddy = np.cos(lam) - xs, np.sin(lam) - ys
    dist = np.hypot(ddx, ddy)
    full = np.sum(MU_S * (1 / dist - 1.0 - (xs * np.cos(lam) + ys * np.sin(lam))) * wgt)
    proj2 = (xs * np.cos(lam) + ys * np.sin(lam))**2
    q = np.sum(MU_S * (3 * proj2 - rs**2) / 2 * wgt)
    return full, q

print('\n=== SINGLE-AVG truncation vs evection term ===')
for aR, e0 in [(0.18, 0.3), (0.30, 0.3), (0.30, 0.6)]:
    a = aR * RH
    C = MU_S * a**2 / 4
    ev = 7.5 * C * e0**2
    res = []
    for lam in np.linspace(0, TWO_PI, 24, endpoint=False):
        full, q = single_avg_exact(a, e0, 0.7, lam)
        res.append(full - q)
    print(f"a={aR:.2f} e={e0}: evection_amp={ev:.3e} "
          f"resid_amp={max(abs(np.array(res))):.3e} "
          f"ratio={max(abs(np.array(res)))/ev:.3f}")

# events per moon orbit and idiot index
print('\n=== FLOOR / IDIOT INDEX ===')
# measured accepted steps of the avg1Q slow flow (DOP853): 21-31 per planet
# orbit at rtol 1e-10 (0.39/1.17/2.92 events per moon orbit at 0.10/0.18/0.30
# R_H); at behaviour tolerance rtol 1e-4 it is ~5x fewer (wdot unchanged to
# 1.4e-4 relative). Events per moon orbit = steps / moon orbits.
measured = {0.10: (0.387, 1643), 0.18: (1.174, 680), 0.30: (2.922, 316)}
for aR, (ev, mo) in measured.items():
    print(f"a={aR:.2f} R_H: avg1Q events/moon-orbit = {ev:.2f} (rtol 1e-10), "
          f"~{ev/5:.2f} at behaviour tol; vs 32 kicks: {32/ev:.0f}x "
          f"(resp. {32/(ev/5):.0f}x)")

# figures
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
for ax, s in zip(axes, [+1, -1]):
    for e0, mk in [(0.3, 'o')]:
        xs2 = [r['aR'] for r in main if r['e0'] == e0 and r['s'] == s and r.get('rel2Q')]
        ys2 = [r['rel2Q'] for r in main if r['e0'] == e0 and r['s'] == s and r.get('rel2Q')]
        xs1 = [r['aR'] for r in main if r['e0'] == e0 and r['s'] == s and r.get('rel1Q')]
        ys1 = [r['rel1Q'] for r in main if r['e0'] == e0 and r['s'] == s and r.get('rel1Q')]
        ax.plot(xs2, ys2, '^-', label='avg2Q (double-avg, r9 kick-avg law)')
        ax.plot(xs1, ys1, 's-', label='avg1Q (evection kept, 0 kicks)')
    for r in kf:
        if r['s'] == s:
            for N, c in [(8, 'lightgray'), (32, 'dimgray')]:
                e = r.get(f'rel_kick{N}')
                if e:
                    ax.plot([r['aR']], [e], 'x', color=c,
                            label=f'kick{N}/orbit' if r is kf[0] else None)
    ax.axhline(0.10, color='r', ls='--', lw=1)
    ax.text(0.105, 0.11, '10% gate (B14/r9)', color='r', fontsize=8)
    ax.set_yscale('log'); ax.set_xlabel('a / R_H')
    ax.set_title('prograde' if s == 1 else 'retrograde', fontsize=10)
    ax.grid(alpha=0.3)
axes[0].set_ylabel('rel. apsidal-precession error')
axes[0].legend(fontsize=8)
sec = axes[1].secondary_xaxis('top', functions=(lambda x: (2/3)*x**3, lambda t: (3*t/2)**(1/3)))
sec.set_xlabel(r'tidal ratio $\tau=(2/3)(a/R_H)^3$')
fig.suptitle('Parent-tide representation error, e0=0.3, 30 planet orbits (mu_p=1e-3)', fontsize=10)
fig.tight_layout()
fig.savefig('fig-error.png', dpi=130)

fig2, ax = plt.subplots(figsize=(5.5, 4))
for r in kf:
    good = [(N, r[f'rel_kick{N}']) for N in Ns if r.get(f'rel_kick{N}')]
    if good:
        ax.plot([g[0] for g in good], [g[1] for g in good], 'o-',
                label=f"a={r['aR']:.2f}, e0={r['e0']:.1f}, s={r['s']:+d}")
ref=[max(r.get(f'rel_kick{N}',1e9) for r in kf) for N in Ns];
ax.plot(Ns, [ref[0]*(Ns[0]/n)**2 for n in Ns], 'k:', label=r'$N^{-2}$')
ax.axhline(0.10, color='r', ls='--', lw=1)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel('kicks per moon orbit N')
ax.set_ylabel('rel. precession error')
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig2.tight_layout(); fig2.savefig('fig-kickfloor.png', dpi=130)
print('\nfigures written')
