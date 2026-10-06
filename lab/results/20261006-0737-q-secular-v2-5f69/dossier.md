# Dossier — 20261006-0737-q-secular-v2-5f69 (second author: fix the reference, then decide)

**Claim.** With the Wisdom–Holman truth repaired and independently verified (Saturn's
eccentricity history matches two exact integrations to 1.9e-5; Saturn really swings
|z_S| 0.054 → 0.0040 → 0.0403 over the run), R2 — stable belt bodies as zero-kick
secular phasors — is KILLED at two-planet belt scale by its own pre-registered rule:
only 14.5% of 1,024 belt bodies pass rate-within-5% AND e-vector-within-10% under the
strongest phasor (exact Gauss-ring double averaging; 0% under first-order
Laplace–Lagrange), AND 24 admitted bodies ended inside a resonance width — both kill
clauses fire, and the kill is HARDER than run 008e's broken-reference 20.5%.

**Bottleneck.** Unchanged target (board focus "fewer kicks per orbit"): R2 promised to
delete all 64 kicks/orbit and the ~82 B scars for stable bodies, keeping the 0.126-bit
belt program. This run kills that promise for a belt as a whole, against a reference
that is now the declared scene.

**Evidence** (all files in this folder; scene, estimators and kill arithmetic frozen
in predictions.md BEFORE the decisive belt runs):

*Truth verification chain (the run's first deliverable).*
- Drift self-test (Gauss f/g vs DOP853, two-body): 1.8e-15.
- Tolerance ladder, planets only: barycentric 1e-11 vs 1e-14 agree to 5.9e-8; the
  ladder CAUGHT a real bug in my own first heliocentric RHS (missing −m_i r_i/|r_i|³
  self-indirect term: 8.4e-3 gap, both families internally converged — controls on
  both sides, per the README's r2 lesson). Fixed: helio(1e-12) vs bary(1e-14) = 2.1e-9.
- Hand-coded planets-only WH (independent file, same equations as the shipped fix):
  max|Δz_S| vs exact = 1.7e-5 (h=0.125), 2.6e-5 (h=0.1875) — error shrinks with h.
- **Shipped truth's planet history vs exact: max|Δz_S| = 1.93e-5** (truth, h=0.125),
  2.9e-5 (conv, h=0.1875), 4.7e-5 (kick, h=0.278): monotone in h, far under the 5e-3
  bar. Belt convergence pair: median |Δz̄| = 1.29e-4, p90 2.55e-4.
- Exact Saturn: |z_S| min 0.0040 at t = 83.0 kyr, end 0.0403; Jupiter max 0.0599,
  end 0.0528. Run 008e's stored truth had |z_S| frozen at 0.0537 ± 0.0003 — the bug.

*Fixes vs 008e* (all pre-registered in predictions.md before any belt run):
1. `accel()`: pass j contributes to every row except row j (was: wiped row j).
2. Planet LL matrix: outer planet's row single α (quadrupole limit; inner row α²
   unchanged). g = (3.49, 22.17) "/yr vs old (2.92, 14.44); against exact Saturn the
   corrected matrix errs max|Δz_S| = 0.021 vs old 0.054 (2.5×), |z_S|(T) 0.0297 vs
   exact 0.0403 (old: 0.0102). Still first-order-incomplete — the residual 0.011 is
   the size of belt free amplitudes.
3. μ-consistent planet init velocities (checker's note).

*Decisive comparison* (metrics.json; frozen estimators; 2,000 J-orbits, 1,024 bodies,
a ∈ [2.0, 3.3], e ≤ 0.25):
- Selector admits 822/1024 = 80.3% (identical rejection census to 008e: 2:1J 76,
  3:1J 38, 5:2J 32, 4:1J 22, 7:3J 15 … — MMR-driven, same (a, e_free) draws).
- rings: Fraction = 0.1445; rate err median 6.7% (p90 36%); evec/amp median 0.46
  (p90 2.4). By a-bin: [2.0,2.5) 43% pass, rate 1.4%, evec 0.11; [2.5,2.9) 0%;
  [2.9,3.3) 0%. **Kill rule fires** (0.1445 < 0.50).
- LL: Fraction = 0.0 (rate err 15–26% by bin, evec/amp 1.3–2.5).
- Leak clause: 24 admitted bodies inside an MMR width from run-averaged ⟨a⟩ (008e:
  20 — the chaotic a-diffusion is real, not a driver artifact). **Fires.**
- Kick law (the plane's 64/orbit): 3:1J and 5:2J depletion reproduced EXACTLY (pumped
  fractions 0.342/0.342 and 0.281/0.281, truth vs kick; the same bodies), trajectory
  error medians 5.7e-5 / 8.9e-5; admitted-body evec median 1.9e-3. Same-integrator
  caveat as 008e applies (not an independent code family).
- Truth-driven rings (`rings_tc`, the driver/averaging decomposition): NOT completed
  in the window. The author's original monkey-patch patched a second module copy and
  silently re-ran the LL driver (output identical to `rings` to 4 digits — caught and
  deleted); my repair then hit an interpolation-range error (t = 0 outside the stored
  grid) and a return-shape error, each fatal at step 0. The decomposition stays open;
  the kill does not rest on it.

**Predictions** (predictions.md, written before the belt runs): admission 0.77–0.84 ✓
(0.803); truth/convergence bars ✓ (1.93e-5, 1.29e-4); kick-law zones ✓✓ (identical
pumping, evec 1.9e-3 in [3e-4, 3e-3]); leak 5–40 ✓ (24) and verdict KILL ✓ (both
clauses); LL ∈ [0, 0.15] ✓ (0.0). **One held-out prediction FAILED, the decisive
one: rings ∈ [0.40, 0.75] — actual 0.1445.** I expected the corrected driver to help
rings; it hurt (inner-belt pass fell 61% → 43% vs 008e's broken pairing): the true
Saturn exchange (dip to 0.004) swings the belt's forced term far more than the broken
driver did, and neither phasor law follows it. The kill's direction survives my error;
its margin does not.

**What would make it wrong.** The 10%-of-free-amplitude yardstick still assumes a
stable free amplitude; where truth modulates it, a rate-only judgement would flatter
the phasors — but the kicked tube must track the true z-trajectory for encounters and
views, so the e-vector bar is the game-relevant one. The kick-law check shares the
truth's integrator family. The `pumped` flag (299 admitted bodies) is miscalibrated
as a chaos indicator here: it tests max|z̄| against the STATIC initial forced term,
which the planets' real secular exchange moves by more than 0.05 — it measures the
driver, not the belt. None of these rescue Fraction = 0.1445 against 0.50.

**Cost of adopting: none — it is a kill** (principle 9: the configuration dies, not
the method). What survives as leads: the frozen selector (80.3% admission, planet
parameters only), the kick-law cadence result (the plane's law is the accurate one at
1.9e-3 evec), the α-power convention fix for any future LL use, and this run's
verification protocol (ladder + two exacts + h-monotonicity: 40 min of the window,
and it caught one real bug in the instrument itself).

**Fit with PRINCIPLES.** #3 "compute only surprises": the surprise budget of a real
belt is dominated by the planets' own secular exchange — a zero-kick phasor computes
no surprises and therefore misses them. #2 "behaviours, not continuum fidelity": the
e-vector swing IS the behaviour the law must reproduce. #9: the kill is of first-order
phasors with linear drivers at two-planet coupling; the selector and the memory
coupling survive. #10 "measure before claiming": 008e's 5× Saturn culprit was a bug —
this run measures before concluding, and its own first instrument failed a control.

**The lens.** A fix-the-reference lens trusts repair to soften verdicts; here the
repaired reference hardened it. It also initially under-weighted that the estimator
suite (static-zf `pumped` flag) embeds the broken-driver assumption one level below
the metrics — frozen estimators inherit the assumptions of the scene they were
frozen against.

**Reproduce** (this folder; wall times on the shared 8-vCPU runner):
`python3 ladder.py 1e-14_bary` (25 s) and `1e-12_helio` (63 s), `python3 ladder.py
cmp`; `python3 exact_check.py` (11 min: self-test, exacts, hand-WH, LL drivers);
`python3 verify.py` then `python3 verify.py ce` (verification chain incl. truth zp);
`python3 selector.py` (1 s); `python3 wh_run.py truth|conv|kick` (18/13/9 min);
`python3 laws.py ll|rings|rings_tc` (5 s / 6 min / 6 min); `python3 analyze.py` (2 s)
→ `metrics.json`. Files: `metrics.json`, `predictions.md`, `exact_*.npz`,
`verify.log`, `exact_check.log`, `*_zbar.npz`/`*_zp.npz`, scripts as named.
