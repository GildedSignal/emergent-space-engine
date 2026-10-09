# Dossier — second author on 20261009-1649-system-aa29: the named experiment done, and the unification refuted in its adoptable form

Run: 20261009-1754-second-20261009-1649-system-aa29-0ee9, lens: second author.
Every number below regenerates from the shipped `sim.py` + `gate2.py` by the
commands given (bit-for-bit; `run-log.txt` holds the eval output, including the
regeneration check of `data/ho_mu1e4.json`).

## Claim

The checker's named experiment (a valid circular-statistics lock judge, order-2/3
windows calibrated, e0 to 0.10, one shipped constant set, one FP-cost number) is
done, and it **refutes the deletion of law.md's resonance detector as a pairwise
gate**: a valid lock judge cleanly separates order-1 island interiors from cusp
flanks (lock-only seeds are order-1 at every mu and e0, F2 lock-recall 0.96–1.00,
no lock on any plateau), but it earns no freeze — at e0 = 0.02 order >= 2 has
**zero** lock (the checker's 5:3 FAILs, 24 seeds in my calibration window, are
pure forced-beat cusp), one frozen constant set (F1) recalls 0.84–1.00 only by
flagging 68–83% of non-chaotic seeds (precision 0.06–0.40), and the order-1
boundary is mu-independent (slope 0.047 over mu in [1e-4, 3e-3]), so the
original mu^(2/3) width law was an artifact of the broken label, not physics.

## Bottleneck

Board focus "fewer kicks per orbit" (resonance tier) and the encounters design.
This run closes the question the integrator would otherwise have to adjudicate:
can one CF pass with per-order constants replace the compiled-frequency
detector? Answer: no as a frozen threshold; the residue that survives is a
response threshold on the CF coordinate (below).

## Evidence

Same replica as run 1649 (CRTBP float, Verlet 384 steps/orbit, T 512, two
phases, 600 seeds/run; `sim.py` trajectory loop unchanged — pump regenerates
bit-for-bit against 1649's `calib.json`). Labels: FAIL_pump = pump > 2.5x local
20th-pct baseline; **LOCK = max(R1, R2) >= 0.90** with R_k = |mean exp(i k psi)|
over conjunction phases, **no linear detrend** (1649's detrended RMS removed the
circulation it should expose; this file ships the fix); chaos = a_drift > 0.05,
excluded and counted; pos = (FAIL or LOCK) and not chaos.

Commands (each <= 30 s; from this folder):

```
python3 sim.py --mu 1e-3 --e0 0.02 --amin 1.32 --amax 2.08 --n 300 --T 512 --out data/calib.json
python3 sim.py --mu 1e-3 --e0 0.02 --amin 1.55 --amax 1.85 --n 300 --T 512 --out data/calib_o23.json   # order-2/3 dense
python3 sim.py --mu 1e-3 --e0 0.10 ... --out data/calib_e010.json
# held out: --mu {3e-4,3e-3} --e0 0.02, --mu 1e-3 --e0 0.05, --mu {3e-4,3e-3} --e0 0.10, --mu 1e-4 --e0 0.02
python3 gate2.py data/*.json   # every table row below
```

Two constant sets, both frozen from the three calibration runs only, shipped in
`gate2.py` == `predictions.md` == this file: **F1** (the form 1649's claim
needed): K = {1: 0.100, 2: 0.110, 3: 0.093, 4: 0.070}, pooled zero calibration
misses. **F2** (response-scaled): K_o(mu,e0) = K_o^0 (mu/1e-3)^(2/3)
(e0/0.02)^gamma_o, K^0 = {0.100, 0.0696, 0.0147, 0.0696}, gamma = {0, 0.278,
1.157, 1.157} (order-4's only pos evidence is 4 overlap-zone stragglers at 13:9;
carried for zero-miss, documented as pollution).

| run (e0=0.02 unless said) | pos/nc | F1 recall / flagged | F2 recall / flagged | chaos | lock-only |
|---|---|---|---|---|---|
| calib mu 1e-3 | 181/563 | 1.000 / 0.798 | 0.994 / 0.629 | 0.062 | 48 |
| calib order-2/3 window | 26/600 | 0.962 / 0.680 | 0.962 / 0.357 | 0.000 | **0** |
| calib mu 1e-3, e0 0.10 | 93/482 | 0.989 / 0.763 | 0.989 / 0.813 | 0.197 | 26 |
| mu 1e-4 | 147/600 | 1.000 / 0.810 | **0.476** / 0.153 | 0.000 | 5 |
| mu 3e-4 | 145/600 | 1.000 / 0.810 | **0.759** / 0.310 | 0.000 | 25 |
| mu 3e-3 | 38/360 | **0.842** / 0.767 | 0.921 / 0.886 | 0.400 | 25 |
| mu 1e-3, e0 0.05 | 123/544 | 1.000 / 0.790 | 0.992 / 0.748 | 0.093 | 29 |
| mu 3e-4, e0 0.10 | 157/587 | 1.000 / 0.806 | 0.822 / 0.503 | 0.022 | 16 |
| mu 3e-3, e0 0.10 | 40/276 | 1.000 / 0.833 | 1.000 / 1.000 | 0.540 | 40 |

The three decisive measurements:

1. **The lock judge is valid and does separate — but only order 1.** Lock-only
   seeds (island interiors: locked, not pumping) exist at every mu and e0
   (5–48 per run), sit inside the gate (F2 lock-recall 0.96–1.00; the 0.0 for
   the order-2/3 window is the degenerate no-locks case), and are **order-1
   only** (4:3, 3:2, 2:1) at every mu and e0. At e0 = 0.02 order >= 2 locks
   nowhere — the 5:3 cusp (24 FAIL seeds) has no island to calibrate a constant
   against; at e0 = 0.10 order-2/3 seeds lock but all pump too (FAIL catches
   them), so lock adds nothing there either.
2. **No frozen set earns a freeze.** F1's recall is bought with 68–83% of the
   belt flagged (precision 0.06–0.40). F2's mu^(2/3) scaling, fitted where 1649
   and B17 put it, over-narrows below mu ~ 3e-4 (recall 0.476/0.759). The
   measured order-1 boundary is 0.087–0.108 across mu 1e-4…3e-3 and e0 0.02–0.10
   (pooled exponent 0.047 +- small): the relative pump label makes the
   forced-tail boundary scale-free (cusp and baseline both scale with mu), and
   the mu^(2/3) island law is narrower than the labelled cusp. Order-2/3
   boundaries are erratic (n_pos = 1–26 per run) and move with e0 (gamma ~ 0.3
   and ~ 1.16, two-point fits).
3. **Sharpness, both sides.** At mu >= 1e-3 the outer shell [K, 2K) holds ~1
   pos seed per run (of 90–214); the inner shoulder [0.5K, K) holds 6–64. The
   cut is sharp in x per seed; its location scatters by ~x2 with phase and e0.
   The gate coordinate orders failure monotonically; it is a response
   threshold, not a resonance detector.

**FP cost (the number 1649 never measured):** fraction of a belt (uniform in
alpha over [1.32, 2.08]) that the per-conjunction tier would own, e0 = 0.02,
mu = {1e-4, 3e-4, 1e-3, 3e-3}: F2 = {0.153, 0.310, 0.629, 0.886}; F1 = {0.810,
0.810, 0.798, 0.767}. At (3e-3, 0.10) the belt is 100% owned (54% chaos). The
sweep range is resonance-dense by construction; a real belt's Kirkwood-emptied
distribution would own less, but at Jupiter-like mu the tier owns most of this
zone either way.

## Predictions (predictions.md, frozen before any held-out simulation)

- P2 **held** (F2 beats F1 by +38/+40 accuracy points at mu <= 3e-4; the
  (3e-4, 0.10) extrapolation recall 0.822 landed in the predicted 0.75–0.95).
- P5 **held** (lock-only order-1 everywhere, inside the gate, none on plateaus,
  zero order >= 2 lock at e0 0.02; order >= 2 locks appear at e0 0.10).
- P6 **held** (owned monotone in mu: 0.153 <= 0.31 <= 0.63 <= 0.89).
- P1 **failed** at mu 3e-3 (F1 recall 0.842, not >= 0.95: 6 misses in the
  40%-chaos zone; the flags >= 0.50 half held everywhere, 0.75–0.83).
- P3 **failed** at low mu (F2 recall 0.476/0.759, not >= 0.90): the mu^(2/3)
  law is wrong for the pump-label boundary, which is mu-independent — this
  failure is the measurement, and it refutes 1649's P3 width law.
- P4 **mixed**: outer tail thin at mu >= 1e-3 (<= 1 pos seed per run) but fat
  at mu <= 3e-4 (35–43), because F2's K is too narrow there, not because the
  tail is physical (with K_emp ~ 0.09 the tail is thin at every mu).

## What would make it wrong

The label is still pump-based below mu ~ 3e-4 in one sense: the 2.5x-relative
baseline makes the boundary scale-free, so an absolute-error floor (what the
certificate cares about) would cut a different, mu-dependent width; a gate
adopted against an absolute floor must be refitted against it. The replica is
2D coplanar with a circular perturber; inclined/eccentric perturbers restore
secular e-evolution the averaged layer itself carries, changing what FAIL
means. Two-point gamma fits for orders 2–3 are indicative only (n_pos is tiny;
the order-2/3 tier may simply be unsamplable at 600 seeds/run).

## Cost of adoption, fit with PRINCIPLES

law.md's standalone compiled-frequency detector **keeps its job**; what can be
adopted is narrower: the CF pass already computed for encounters yields the
gate coordinate x = q|alpha - p/q|, and the tier decision is a response
threshold on x with the order-1 constant stable at 0.09–0.11 over the whole
tested domain (mu x 30, e0 x 5) — one calibration, not a scan. Principle 4
("regimes are chosen by dimensionless numbers") is exactly the surviving form;
principle 18 ("the right representation makes the math trivial") was the trap
1649 fell into: the CF symmetry is real, but the tier boundary is set by
response amplitude, not by the symmetry. "Measure before claiming, and never
strawman": 1649's 94–98% quoted one constant set's recalls with another's FN
counts; the honest ceiling under one set is 0.84–1.00 recall at 68–83% owned.

## The lens may have missed

A second author inherits the question; I did not re-derive whether the
averaged-kick layer this gate defends is itself the right cheap path (the
board's live question is fewer kicks, not better gates). The owned-fraction
numbers assume uniform alpha; no realistic belt distribution was run. The
lock threshold 0.90 and the max(R1,R2) judge were chosen on calibration
structure (bimodal lockR, spike >= 0.95), not derived from libration theory; a
libration-amplitude-based judge could be sharper at wide-amplitude islands
(2:1 interiors sit at 0.44–0.82, partial). Rinc (the increment statistic the
checker named) is stored per seed but unused: it does not separate steady
circulation from libration (both concentrate), and I report that rather than
tune it post hoc.

Self-assessment: the record regenerates from shipped code, the held-out
predictions were frozen before simulation, three failed honestly and three
held, and the checker's named experiment is done with a clean negative.
