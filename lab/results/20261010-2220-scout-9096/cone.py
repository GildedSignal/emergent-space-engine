#!/usr/bin/env python3
"""Scout falsifier: the player's growing light cone under three representations.

Integer automaton, dyadic-exact (all divisions are shifts). One wildcard source
acts continuously: every cell at distance r (ring r, band k = floor(log2 r))
gains staleness delta_k = (a << F) >> 2k fine units per tick (mass-type news,
d^-2 per cell, dyadic on bands). A cell recompiles when staleness crosses its
quantum. Nothing is ever lost: arrivals + phase0 = apps*q + residue, integers.

L0 naive: every cell inside the cone recompiles every tick (no quantum).
L1 flat: q = 1<<F per cell everywhere.
L2 graded: q = 1<<(F+k) per cell (quantum proportional to distance/cell size).
"""
import json
import numpy as np

F = 32  # fine units per application quantum (dyadic, exact shifts only)

def rings(R):
    r = np.arange(1, R + 1, dtype=np.int64)
    k = np.int64(np.floor(np.log2(r)))
    cells = np.maximum(np.int64(np.round(2 * np.pi * r)), 1)
    return r, k, cells

def q_delta(R, a_coarse, law, two_source=False):
    r, k, cells = rings(R)
    q = np.left_shift(np.int64(1), np.int64(F + (k if law == 'L2' else 0)))
    delta = np.right_shift(np.int64(a_coarse) << np.int64(F), np.int64(2 * k))
    if two_source:
        delta = 2 * delta
    return k, cells, q, delta

def per_band_exact(T, a_coarse, law):
    """Closed form: crossings after T ticks = (T*delta)//q with zero initial phase."""
    k, cells, q, delta = q_delta(T, a_coarse, law)
    K = int(k.max())
    work = ((np.int64(T) * delta) // q) * cells
    tot = int(work.sum())
    band = np.zeros(K + 1, dtype=np.int64)
    np.add.at(band, k, work)
    return [int(x) for x in band], tot

def run_law(T, a_coarse, law, stagger=False, silence_at=None, two_source=False):
    R = T
    k, cells, q, delta = q_delta(R, a_coarse, law, two_source)
    K = int(k.max())
    stal = np.zeros(R, dtype=np.int64)
    phase0 = np.zeros(R, dtype=np.int64)
    if stagger:
        phase0 = (np.arange(1, R + 1, dtype=np.int64) * np.int64(0x9E3779B1)) % q
        stal = phase0.copy()
    apps_band = np.zeros(K + 1, dtype=np.int64)
    work_per_tick = np.zeros(T, dtype=np.int64)
    arrived = np.zeros(R, dtype=np.int64)
    applied_acc = np.zeros(R, dtype=np.int64)
    pending_probe = 0
    for t in range(T):
        d = delta if (silence_at is None or t < silence_at) else np.int64(0)
        arrived += d
        stal += d
        nc = stal // q
        if nc.any():
            work_per_tick[t] = int(np.sum(nc * cells))
            applied_acc += nc * q
            if t % 1024 == 1023:
                apps_band += np.rint(np.bincount(k, weights=(nc * cells).astype(np.float64),
                                                 minlength=K + 1)).astype(np.int64)
            stal -= nc * q
        if t == int(0.9471 * T):
            pending_probe = int(np.sum(stal > 0))
    exact = bool(np.all(arrived + phase0 == applied_acc + stal))
    tail = work_per_tick[int(0.9 * T):]
    half = work_per_tick[: T // 2]
    return {
        'law': law, 'T': T, 'a': a_coarse, 'stagger': stagger,
        'work_per_tick_mean': float(work_per_tick.mean()),
        'work_mean_first_half': float(half.mean()),
        'work_mean_tail': float(tail.mean()),
        'p99_per_tick': float(np.percentile(work_per_tick, 99)),
        'work_total': int(work_per_tick.sum()),
        'pending_rings_end': int(np.sum(stal > 0)),
        'pending_probe_offdyadic': int(pending_probe) if T > 64 else None,
        'exact': exact,
        'apps_band_ckpt': [int(x) for x in apps_band],
        'silence_work_after': (int(work_per_tick[silence_at:].max()) if silence_at else None),
    }

def d_star(a_coarse, law, T=1 << 16):
    k, cells, q, delta = q_delta(T, a_coarse, law)
    rate = delta // q
    hot = rate >= 1
    return int(2 ** int(k[hot][-1])) if hot.any() else 0

def main():
    out = {}
    T, a = 1 << 14, 1 << 12
    for law in ['L1', 'L2']:
        m = run_law(T, a, law)
        out[f'{law}_main'] = m
        res_s = run_law(T, a, law, stagger=True)
        out[f'{law}_stagger'] = {'p99_per_tick': res_s['p99_per_tick'],
                                 'work_per_tick_mean': res_s['work_per_tick_mean'],
                                 'exact': res_s['exact']}
        single = run_law(T >> 3, a, law)
        two = run_law(T >> 3, a, law, two_source=True)
        out[f'{law}_two_source'] = {'single': single['work_per_tick_mean'],
                                    'double_rate': two['work_per_tick_mean'],
                                    'exact': two['exact']}
        out[f'{law}_silence'] = run_law(T >> 3, a, law, silence_at=(T >> 4))
        out[f'{law}_dstar'] = {str(ac): d_star(ac, law)
                               for ac in [1 << 6, 1 << 9, 1 << 12, 1 << 16, 1 << 20, 1 << 24]}
        pb, tot = per_band_exact(T, a, law)
        out[f'{law}_perband_exact'] = pb
        out[f'{law}_selfcheck'] = tot
        out[f'{law}_selfcheck_ok'] = (tot == m['work_total'])
        print(law, 'work/tick: first-half', f"{m['work_mean_first_half']:.4e}",
              'tail', f"{m['work_mean_tail']:.4e}",
              '| pending end/offdyadic', m['pending_rings_end'], m['pending_probe_offdyadic'],
              '| exact', m['exact'],
              '| p99/mean', round(m['p99_per_tick'] / m['work_per_tick_mean'], 2))
        print(law, 'per-band/tick exact:', [round(x / T) for x in pb],
              '| selfcheck', tot, '== sim total', m['work_total'], tot == m['work_total'])
        s = out[f'{law}_stagger']
        print(law, 'stagger p99/mean', round(s['p99_per_tick'] / s['work_per_tick_mean'], 2))
        tw = out[f'{law}_two_source']
        print(law, 'two-source', f"{tw['double_rate']:.4e}", 'vs 2x single', f"{2 * tw['single']:.4e}",
              'ratio', round(tw['double_rate'] / (2 * tw['single']), 4), 'exact', tw['exact'])
        print(law, 'silence: max work/tick after stop', out[f'{law}_silence']['silence_work_after'])
        print(law, 'd* (2^a -> hot radius):', out[f'{law}_dstar'])
    out['L0_naive'] = {
        'work_per_tick_formula': 'sum_{r<=t} round(2*pi*r) ~ pi*t^2',
        't_128': float(np.sum(np.maximum(np.round(2 * np.pi * np.arange(1, 129)), 1))),
        't_1024': float(np.sum(np.maximum(np.round(2 * np.pi * np.arange(1, 1025)), 1))),
    }
    print('L0', out['L0_naive'])
    with open('metrics.json', 'w') as f:
        json.dump(out, f, indent=1)

if __name__ == '__main__':
    main()
