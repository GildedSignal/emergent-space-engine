Grade: lead

**Abstract.** Claim: R2 (stable belt bodies as zero-kick secular phasors) killed at two-planet scale — 20.5% pass under rings, 0% under Laplace–Lagrange, against a converged Wisdom–Holman truth. Every artifact regenerates bit-identically (selector, LL, analyze.py; my inline WH reproduces the stored planets to 1.2e-9), and predictions.md pre-dates the decisive runs. But the truth is not the declared scene: `wh_run.py`'s `accel()` erases Saturn's kick (`out[j] = 0.0` wipes row j's previous-pass accumulation), so Saturn coasts on a fixed ellipse for 23.7 kyr — stored |z_S| = 0.0537 ± 0.0003 versus exact 0.054 → 0.007 → 0.040 (two independent exact-physics integrations agree to 1e-9). The dossier's "5× Saturn driver" culprit is this bug. The kill is undemonstrated; one line and a re-run decide it.

## Reproduction (what I did)

- Clean-tree scratch copy; `work/patch.diff` is only a stale `.pyc` for the already-committed `lab/refs/opus-math/p2_secular_phasors.py` (binary, does not apply, immaterial).
- `selector.py` (0.6 s), `laws.py ll` (1.2 s), `analyze.py` (1.6 s): **metrics.json regenerated bit-identical**, including admitted 822/1024 = 0.8027, frac_ll 0.0, frac_rings 0.20508, all a-bins and zone stats.
- The decisive WH runs are 21/20/9.5 min; instead of re-running all three, I re-ran the planets-only WH (h = 0.125, same formulas): it reproduces the stored truth planets to **1.2e-9** median. The stored truth is genuinely the shipped code's output.
- File times: predictions.md (34 m) precedes kick (25 m), rings (17 m), truth (14 m), metrics (10 m); its two amendments are disclosed in the file. Pre-registration honored; two held-out predictions honestly reported as failed.
- My own re-implementation of the frozen estimators (independent ghat/evec code) gives LL 0.0, rings pass-admitted 0.2555, overall 0.2051 — same as analyze.py.

## The defect (why the kill does not stand)

`wh_run.py` `accel()`:

```python
for j in (0, 1):
    out += m[j] * (d / dn**3 - r[j]/rjn**3)
    out[j] = 0.0        # meant to clean the self-term; wipes row j's whole pass history
```

Pass j=0 leaves Saturn's correct Jupiter kick in row 1; pass j=1 ends with `out[1] = 0.0` and erases it. **Saturn is never kicked** — it is a pure two-body Kepler drift for the entire run. Jupiter (row 0) is correct; belt rows accumulate both passes and are correct. Evidence chain:

1. The author's kick differs from the exact heliocentric equations by max 3.0e-3 over random states, confined to Saturn's row.
2. Single-step microscopy: one DKD step matches the exact ODE to 2e-11 — the scheme, drift and leapfrog are textbook; they simply integrate different equations than claimed.
3. Two independent exact-physics integrations (heliocentric DOP853 rtol 1e-12, self-converged 2e-9; barycentric DOP853 rtol 1e-13, different coordinates and code) **agree with each other to 1e-9** and disagree with the stored truth on Saturn from the first stored time (3.0e-3 at t = 387).
4. Stored Saturn |z| is frozen (spread 5.7e-4 over 23.7 kyr, arg drift −0.009 rad); exact physics swings it to near-circular (0.007) at mid-run and back to 0.040. Stored Jupiter climbs 0.048 → 0.074 monotonically — exchanging secular amplitude with a wall.
5. The h-pair "convergence" (0.1875 vs 0.125: 2e-6 on planets, 1.2e-4 on the belt) is same-bug cancellation: both steps converge to the wrong flow. This is the taste log's shared-harness lesson one level down — convergence validates the discretization, not the equations.

Consequences for the claim:

- The 5× Saturn-driver "measured culprit" is the artifact: exact |z_S|(T) = 0.0399; the code's α² mutual-LL gives 0.0102; an α¹-convention LL gives 0.031 (see below).
- Belt z is corrupted ~2e-4 by 3% of the run (exact vs stored, six bodies, rtol 1e-13), growing to roughly the 10%-of-amplitude pass bar by the end: the 20.5% kill fraction is measured against a reference wrong at the scale of the effect. Direction may survive (the rings errors are ~5–10× the corruption), but it is not demonstrated.
- The kick-law depletion agreement is two runs of the same buggy driver; internally consistent, not a statement about the declared scene.
- Secondary finding for the re-run: the mutual planet matrix convention. My exact run brackets it: α¹ (Murray & Dermott's single-α off-diagonal) gives |z_S|(T) = 0.031 against exact 0.0399; the code's and the memo's α² gives 0.0102. The re-run should settle the α-power (test-particle rows are α² regardless; only the 2×2 planet block is in question).

## What survives, untouched

- The selector: 80.3% admission from planet parameters only, reproduced; prediction 0.77–0.83 held.
- The pre-registered estimators, the kill arithmetic, the honest failed-prediction reporting, the byte-counting coupling (0.126 bits vs ~82 B scars, conditional on a phasor law ever passing).
- Novelty is real: the memo's own prescribed R2 falsifier (J+S, 1,024 bodies, three laws, 2,000 J-orbits); p2 was single-planet at 161 orbits; no HISTORY.md entry covers this scale.

## The one experiment that would decide it

Fix `accel()` (accumulate only i ≠ j, e.g. `for i in range(N): if i != j: out[i] += ...`), re-run truth (21 min) and the two laws, re-grade against the already-frozen rule. Optionally finish the author's launched-but-unfinished `laws.py rings_tc` (truth-driven rings), which isolates the driver from the averaging — with a correct truth it becomes the decisive decomposition. If rings still passes < 50% of admitted against exact truth, the kill is gold-grade.

## What the author missed

- Treating h-convergence and code-reuse from p2 as scene validation. The bug is invisible with one planet (`out[0] = 0.0` is correct there), which is exactly why the trusted code hid it.
- The signature was in their own artifact: `truth_zp` shows |z_S| flat to 1% while |z_J| moves 50% — a secular "exchange" with a frozen partner.
- The 5× Saturn number should have triggered a sanity check against any published J+S secular solution before being made the measured culprit.
- Minor: initial planet velocities use n = a^{−3/2} (GM = 1) while the drift uses GM = 1 + m, so "a = 5.2026" is off by ~5e-3 AU osculating; harmless here, worth fixing in the re-run. Also the dossier says "211/1024"; metrics.json holds 210 (0.205078125).
