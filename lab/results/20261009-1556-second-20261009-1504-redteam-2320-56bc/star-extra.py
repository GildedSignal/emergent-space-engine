#!/usr/bin/env python3
"""Checker's star symptoms, reproduced on the SHIPPED falsifier.py.

P5  r* = 100 >= b_E ("normal star"): transit eta 400->5->400. Truth goes
    1 -> 0 (occulted) -> 1; the gather, which HELD the branch before
    occultation, holds 0 for every post-occultation frame (absorbing
    emptiness).
P7  r* = 50: tracker seeded with BOTH truth images at eta=40, swept outward;
    the held secondary dies well inside truth's eta_crit = 81.6.
Writes star-extra-out.json.
"""
import numpy as np, json, time
import falsifier as F
from bh import roots_on_grid

def transit(R_STAR, etas, seed_at_first=True, seed_with_truth=True):
    F.R_STAR = R_STAR
    thetas = np.linspace(-0.25, 0.25, 2001)
    frames, tracked = [], None
    for k, eta in enumerate(etas):
        L, Srel, rS = F.geom(eta)
        roots = roots_on_grid(thetas, L, Srel, rS)
        if tracked is None:
            tracked = []
            if seed_with_truth:
                for t, _ in roots:
                    s0, _ = F.trace1(t, L, Srel, rS)
                    tracked.append((t, s0, 0))
        cont = F.continuation_frame(tracked, L, Srel, rS)
        ct = [c['theta'] for c in cont]
        tt = [t for t, _ in roots]
        frames.append(dict(k=int(k), eta=float(eta), n_truth=len(tt),
                           thetas_true=tt, n_cont=len(cont),
                           thetas_cont=ct,
                           missed=[t for t in tt if not any(abs(t - c) < 6e-4 for c in ct)]))
        tracked = [(c['theta'], c['s'], c['iters']) for c in cont]
    return frames

def main():
    t0 = time.time()
    # P5: occultation recovery, r* = 100
    etas5 = np.concatenate([np.linspace(400, 5, 40), np.linspace(5, 400, 40)[1:]])
    occ = transit(100.0, etas5)
    seen_before = [f['k'] for f in occ if f['n_truth'] >= 1 and f['n_cont'] >= 1]
    occulted = [f['k'] for f in occ if f['n_truth'] == 0]
    post = [f for f in occ if occulted and f['k'] > max(occulted)]
    p5 = dict(frames=len(occ),
              held_before_occultation=bool(seen_before),
              occulted_frames=len(occulted),
              post_occultation_frames=len(post),
              post_truth1_cont0=sum(1 for f in post if f['n_truth'] == 1 and f['n_cont'] == 0),
              post_any_image_held=sum(1 for f in post if f['n_cont'] >= 1),
              counts_by_eta=[(round(f['eta'], 1), f['n_truth'], f['n_cont']) for f in occ[::4]])
    # P7: held secondary near the fold, r* = 50
    etas7 = np.arange(40.0, 400.0, 5.0)
    fold = transit(50.0, etas7)
    drop = next((f['eta'] for f in fold
                 if f['n_truth'] == 2 and f['n_cont'] == 1), None)
    p7 = dict(frames=len(fold), seed_eta=40.0,
              secondary_dropped_at_eta=drop,
              truth_eta_crit=81.6,
              counts_by_eta=[(round(f['eta'], 1), f['n_truth'], f['n_cont']) for f in fold[:14]])
    out = dict(wall_s=round(time.time()-t0, 1), occultation_r100=p5, fold_r50=p7)
    print(json.dumps(out, indent=1))
    with open('star-extra-out.json', 'w') as fh:
        json.dump(dict(summary=out, occultation=occ, fold=fold), fh, default=float)

if __name__ == '__main__':
    main()
