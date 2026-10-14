# Rung r5: the contact carry at mass contrast (the dense order's missing gate)

Frozen 14 October 2026 by the second author of 20261014-0000-redteam-f3ce, per its
checker's named gold experiment, **before any run at Q = 2²⁰**. Design:
[docs/representation.md](../../../../docs/representation.md) §2 ("at most one floor unit
per event, carried forward so that it never compounds"). No rung, gate or oracle watched
contact energy before this (B12 judges orbit laws; H0173 measured entropy).

**Question.** Does the shipped contact law's rounding carry stay bounded at mass
contrast, at the engine's own Q = 2²⁰ (the law's ceiling; the engine's tests run there),
and does a pair-scaled (sigma-delta) carry repair it locally?

**Scene.** Two bodies in a 64Q box, radius 4Q, both at exactly β = 0.6 (k = ±0.6Q on x),
head-on with a per-seed y-offset `(1 + 3·f)·Q/2` from the run's LCG high-entropy draw
`f` (revision before the decisive run: the low-bit `range(2,5)` draw is constant across
consecutive seeds — an LCG small-period artifact found at 2¹⁶; the original run's pair
arm had the same constant y-offset, its seed diversity came entirely from its β draw). Masses 1000:1 (judged scene) and 1000:1000
(positive-control scene). Chronon reference stepper; run to exactly **200 contacts**;
metric is the end |Σ residual| / Σ m|k|², **median over 5 seeds** (0–4; held-out 11–15
run after grading starts). Ledger exactness (ΣE − ΣE₀ = Σ residual at every contact) is
asserted throughout and any break voids the rung.

**Mechanism (measured at Q = 2¹⁶ before freezing, diagnostics only).** The first
contact ejects the light body at γ ≈ 3.9; Fermi pumping against the shuttling heavy
body drives it to γ ~ 30–100 within ~15 contacts, where its energy quantum
dE/dk = 2mγ³|k| is a fixed fraction of the pair's KE. The carry's per-contact step is
that quantum; it walks. Equal masses stay at γ ≈ 1.3 with quanta ~10⁻⁵ KE.

**Configurations.**
- `shipped`: `es-lattice-relativistic-v1` exactly as in `crates/lattice` (negative: it
  must fail `frac1000` — if it passes, the 1%-at-200-contacts severity bar is wrong at
  the engine's Q and the rung reports that as its finding).
- `pair-carry`: `resolve_law` with the pair-scaled carry (the patch in
  `work/patch.diff`, selected by `RUNG_PAIR_CARRY=1`; final form after three
  iterations at 2¹⁶, all before the decisive runs): the coarse-energy body (larger
  exact radial energy step ΔE) rounds to its exact target; for each of its corners the
  fine body's target is shifted radially so its energy lands on
  old_E − E(coarse corner) − owed_E, repaying both the standing carry and the fresh
  corner error in-contact, in the fine body's own units. Shifts are zero while
  everything sits inside one quantum, so low-carry contacts are bit-identical to
  shipped. Ledgers unchanged by construction (e is recomputed from actual
  four-momenta).

**Metrics** (`metrics.json`, one row per configuration; medians over seeds 0–4):
- `frac_1000_1_median`: end |Σres|/KE on the 1000:1 scene (β 0.6, 200 contacts).
- `frac_equal_median`: same on the 1000:1000 scene (the positive control: the shipped
  law must pass it — the instrument can pass where physics is right).

```configs
shipped negative
pair-carry candidate
```

```criteria
frac1000 type frac_1000_1_median <= 0.01
fracequal type frac_equal_median <= 0.001
```
