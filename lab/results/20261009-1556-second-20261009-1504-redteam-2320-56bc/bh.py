#!/usr/bin/env python3
"""BH-lens transit (opaque r* = 3M) on the SHIPPED falsifier.py instrument.

Parts:
  A   cold start (doll entry): seed = the single no-lens crossing; BH on from
      the first frame (eta=400). Miss fraction + missed-image brightness.
  A2  generous seed (author's convention): seed = ALL truth roots at frame 0.
  C   n=0 census over eta 1600->400: impact parameters b = r0*|theta-theta_lens|
      (r0 = |O-L|; the capture hole's half-width is b_c/r0, NOT b_c/D_OL).
      wrap: lens side, b < 2*b_c ; strong: lens side, b >= 2*b_c ; direct: else.
 Ctl  held branches match truth, converged, <= 6 iterations.

Brightness = 1/|ds/dtheta| with the absolute slope (downward crossings count);
slope falls back to the bracket difference when the 3-point stencil touches a
blocked ray. Writes bh-out.json.
"""
import numpy as np, json, time
import falsifier as F

THETA_C = 3*np.sqrt(3)*F.M / F.D_OL

def roots_on_grid(thetas, L, Srel, rS, dphi=0.005, max_steps=None):
    s, ok, _ = F.trace_grid(thetas, L, Srel, rS, dphi, max_steps)
    sv = np.where(ok, s, np.nan)
    roots = []
    for i in range(thetas.size - 1):
        a, b = sv[i], sv[i+1]
        if np.isnan(a) or np.isnan(b): continue
        if a == 0.0: roots.append((float(thetas[i]), 1.0)); continue
        if a*b < 0.0:
            t = thetas[i] + (thetas[i+1]-thetas[i])*a/(a-b)
            iu = min(i+2, thetas.size-1); il = max(i-1, 0)
            slope = (sv[iu]-sv[il])/(thetas[iu]-thetas[il])
            if not np.isfinite(slope):            # stencil touched a blocked ray
                slope = (b - a)/(thetas[i+1]-thetas[i])
            roots.append((float(t), float(abs(slope))))
    out = []
    for t, sl in sorted(roots):
        if out and abs(t - out[-1][0]) < 3e-4:
            out[-1] = (out[-1][0], min(out[-1][1], sl)); continue
        out.append((t, sl))
    return out

def classify(roots, eta):
    B_C = 3*np.sqrt(3)*F.M
    tl = np.arctan2(eta, F.D_OL)
    r0 = float(np.hypot(F.D_OL, eta))
    lab = []
    for t, _ in roots:
        d = t - tl
        b = r0*abs(d)
        if b < 2*B_C:
            lab.append('wrap')                    # near-capture, either side
        elif np.sign(d) == np.sign(tl):
            lab.append('strong')                  # beyond the lens
        else:
            lab.append('direct')
    return lab

def transit(seed_mode):
    etas = np.concatenate([np.linspace(400, 20, 30), np.linspace(20, 400, 30)[1:]])
    thetas = np.linspace(-0.25, 0.25, 2001)
    frames, tracked = [], None
    for k, eta in enumerate(etas):
        L, Srel, rS = F.geom(eta)
        roots = roots_on_grid(thetas, L, Srel, rS)
        if tracked is None:
            if seed_mode == 'generous':
                tracked = []
                for t, _ in roots:
                    s0, _ = F.trace1(t, L, Srel, rS)
                    tracked.append((t, s0, 0))
            else:
                tracked = [(0.0, 0.0, 0)]
        cont = F.continuation_frame(tracked, L, Srel, rS)
        ct = [c['theta'] for c in cont]
        tt = [t for t, _ in roots]
        sl = [sl for _, sl in roots]
        held_ok = all(any(abs(t - c) < 6e-4 for t in tt) for c in ct) if ct else True
        frames.append(dict(
            k=int(k), eta=float(eta), n_truth=len(tt),
            thetas_true=tt, slopes=sl, labels=classify(roots, eta),
            n_cont=len(cont), thetas_cont=ct, iters=[c['iters'] for c in cont],
            missed=[t for t in tt if not any(abs(t - c) < 6e-4 for c in ct)],
            held_branch_on_truth=bool(held_ok)))
        tracked = [(c['theta'], c['s'], c['iters']) for c in cont]
    return frames

def missed_relmags(frames):
    """For every missed truth root: its brightness relative to the brightest
    held image in that frame. Returns (frame, label, ratio)."""
    out = []
    for f in frames:
        if not f['missed'] or not f['thetas_cont']: continue
        held_sl = [sl for t, sl in zip(f['thetas_true'], f['slopes'])
                   if any(abs(t - c) < 6e-4 for c in f['thetas_cont'])]
        if not held_sl: continue
        best_held = min(held_sl)
        for j, t in enumerate(f['thetas_true']):
            if any(abs(t - c) < 6e-4 for c in f['thetas_cont']): continue
            out.append((f['k'], f['labels'][j], best_held/f['slopes'][j]))
    return out

def census():
    rows = []
    for eta in [1600, 1400, 1300, 1260, 1240, 1220, 1200, 1100, 1000, 800, 600, 400]:
        tl = np.arctan2(eta, F.D_OL)
        r0 = float(np.hypot(F.D_OL, eta))
        lo = min(-0.05, tl - 0.05); hi = tl + 0.06
        thetas = np.linspace(lo, hi, 2001)
        L, Srel, rS = F.geom(eta)
        roots = roots_on_grid(thetas, L, Srel, rS)
        lab = classify(roots, eta)
        B_C = 3*np.sqrt(3)*F.M
        bs = [round(r0*abs(t - tl), 3) for t, _ in roots]
        p1 = min((sl for _, sl in roots), default=np.inf)
        rows.append(dict(eta=eta, theta_lens=round(float(tl), 5),
                         hole_halfwidth=round(B_C/r0, 6),
                         n_truth=len(roots), labels=lab,
                         thetas=[round(t, 6) for t, _ in roots],
                         b_roots=bs,
                         relmag_vs_brightest=[round(p1/sl, 6) if sl > 0 else None
                                              for _, sl in roots]))
    return rows

def main():
    t0 = time.time()
    F.R_STAR = 3.0
    cold, generous = transit('cold'), transit('generous')
    cens = census()
    cm, gm = missed_relmags(cold), missed_relmags(generous)
    strong_cm = [x for _, l, x in cm if l == 'strong']
    wrap_cm = [x for _, l, x in cm if l == 'wrap']
    def rng(v): return [round(min(v), 4), round(max(v), 4)] if v else None
    multi = [f for f in cold if f['n_truth'] >= 2]
    gen_strong_held = [any(abs(t - c) < 6e-4 for c in f['thetas_cont'])
                       for f in generous
                       for t, l in zip(f['thetas_true'], f['labels']) if l == 'strong']
    out = dict(
        wall_s=round(time.time()-t0, 1), R_STAR_BH=3.0, theta_c=THETA_C,
        cold=dict(
            frames=len(cold), frames_truth_ge2=len(multi),
            miss_fraction=round(len([f for f in multi if f['missed']]) / max(len(multi), 1), 3),
            n_cont_always_1=all(f['n_cont'] == 1 for f in cold),
            images_at_entry_frame0=dict(n_truth=cold[0]['n_truth'], labels=cold[0]['labels'],
                                        n_cont=cold[0]['n_cont']),
            missed_relmag_strong_range=rng(strong_cm),
            missed_relmag_wrap_range=rng(wrap_cm),
            missed_strong_ge_2pct_all_frames=all(
                any(x >= 0.02 for k, l, x in cm if k == f['k'] and l == 'strong')
                for f in multi),
            max_iters=max(max(f['iters']) for f in cold if f['iters']),
            held_branch_on_truth_all=all(f['held_branch_on_truth'] for f in cold)),
        generous=dict(
            n_seeds=generous[0]['n_truth'],
            seeds_labels=cold[0]['labels'],
            frames=len(generous),
            miss_fraction=round(len([f for f in generous if f['missed']]) / len(generous), 3),
            strong_held_frac=round(sum(gen_strong_held) / max(len(gen_strong_held), 1), 3),
            first_frame_strong_lost=next((f['k'] for f in generous
                                          for t, l in zip(f['thetas_true'], f['labels'])
                                          if l == 'strong'
                                          and not any(abs(t - c) < 6e-4 for c in f['thetas_cont'])), None),
            n_cont_after_frame1=generous[1]['n_cont'],
            missed_relmag_strong_range=rng([x for _, l, x in gm if l == 'strong']),
            max_iters=max(max(f['iters']) for f in generous if f['iters'])),
        census=cens)
    print(json.dumps(out, indent=1))
    with open('bh-out.json', 'w') as fh:
        json.dump(dict(summary=out, cold=cold, generous=generous, census=cens), fh, default=float)

if __name__ == '__main__':
    main()
