# Dossier — run 20261012-0358-second-20261012-0311-scout-6759-0ae6
(lens: second author on 20261012-0311-scout-6759; the checker's named
gold experiment, run and answered)

**Claim (one sentence).** Steady-state reabsorption does not save the
belt store at the law's quanta: with the population program recompiled
every orbit — at any cadence k, in every program class tested,
including the checker's per-kick oracle accounting (their 61.2 bits,
reproduced at 61.16) — a Jupiter-kicked belt's residual scar stock
stays at 45–76 bits/body against the 34.4 bits/body live budget (best
regenerable program: a two-block generator-deformation ∪ λ−λ_J
Fourier, 54.3 bits with flat steady-state peaks 55.3–57.2), so exact
scars for 10⁹-body belt populations in 4 GiB are dead at every cadence
(and the scout's "1 km" quantum was in fact 10 km — Q_A = 6.6846×10⁻⁸
AU — so its headline was 10× optimistic), and the budget is restored
only by per-population quanta coarsened 256× (2,560 km, 2π·2⁻¹⁶ rad →
33.2 bits steady state), with reabsorption every orbit and 76% of the
residual in the angle elements.

**Bottleneck.** Board item "fitting 10⁹ in 8 GB … decided by
distinctions created per game-second"; HANDOFF H_live. The scout run
measured the raw scar stock (66.6→77.3 bits, 8 orbits); the checker
named the missing experiment: the steady state under reabsorption, the
largest k, and the quantum valve. Gain: a premise-level kill plus two
design constants (cadence k = 1; per-population quantum scale 256×) —
10⁰–10¹ on constants, but it deletes the "exact belt scars in 4 GiB"
premise outright.

## Evidence (all numbers from JSONs in this folder; every command
regenerates them deterministically, seed 6759)

```
python3 reabs.py smoke     # <1 s:  synthetic fit recovery 6e-15; shuffle
                            #        absorbs 3.3% = chance (153/4096)
python3 reabs.py control   # 4 s:   perturber off ⇒ payload ≡ 0 bit-exact
python3 reabs.py evolve    # 29 s:  16-orbit trajectory → /tmp (257 MB),
                            #        reproduces the scout run bit-exact
python3 reabs.py analyze   # 17 min: P1/P1B/P2/P3 × k-scan × c-scan
python3 reabs_ss.py        # 4 min: steady-state valve, exact per-cycle
python3 reabs_B.py         # 4 min: predictive per-kick program
python3 reabs_pk.py        # 2 min: per-kick oracle (checker's probe)
```

Reproduction (bit-exact): scar_word_bits orbits 1–8 = [66.630018,
70.235699, 72.167732, 73.649662, 74.804615, 75.785142, 76.606401,
77.330067] = the scout's published values; raw per-kick entropy over
their 256-kick window 51.440877076 vs published 51.440877075679346.
**Unit correction inherited from the scout run:** its code comment and
dossier call Q_A = 6.6846×10⁻⁸ AU "1 km"; 1 km is 6.6846×10⁻⁹ AU, so
every number in the scout run, the checker's verdict, and this run is
measured at a 10 km a-quantum (angle quantum 2π/2²⁴, correctly
labeled). The checker's probe instrument also reproduced: per-kick
energy absorption [0.872, 0.729, 0.571, 0.571] (orbit 1) vs their
[0.87, 0.70, 0.50, 0.50]; oracle residual stock after orbit 1 = 61.16
vs their quoted 61.2 (their probe was a one-orbit per-kick accounting;
the 77.3 they compared it against is the 8-orbit raw stock — different
horizons). Shuffle control absorbs 0.008–0.012 = chance level
(153/16384).

**The named experiment — steady state with reabsorption** (payload =
quantized residual vs the frozen program, refit on the total deviation
each k orbits; W = Σ log₂(1+2·median|S|), the scout's own instrument;
budget 34.4; cold belt, 16 orbits, N = 16384):

| Program (refit each orbit, k=1) | W post-refit orb 1 → 16 | sup W | bits/doubling |
|---|---|---|---|
| raw (no program; scout's headline) | 66.63 → 81.03 | 81.0 | ~2 |
| P1 checker's λ−λ_J basis, true anchor | 63.41 → 74.03 | 74.85 | 2.55 |
| P1B same, base anchor (non-circular) | 63.66 → 75.81 | 76.70 | 2.96 |
| P2 generator deformation (initial λ,a,e,ω) | 61.74 → 74.77 | 75.30 | 3.05 |
| **P3 = P2 ∪ P1 (two-block, best regenerable)** | **44.87 → 54.26** | **66.47** | **2.18** |
| B predictive per-kick subtraction | 66.64 → 76.01 | 76.31 | 2.27 |
| per-kick oracle (not regenerable) | 61.16 → 80.42 | 80.4 | — |

- **P3's steady state is real:** cycle peaks (orbits 2–16) are flat at
  55.3–57.2; the post-refit value creeps +2.18 bits/doubling
  (increments +3.4, +3.1, +2.9, +1.2 — diffusive-log, decelerating).
- **k-scan at belt quanta:** k = 1 is optimal everywhere; sup_W for P3
  at k = 1/2/4/8 = 66.5/70.2/73.6/77.3; for P1 = 74.8/74.9/75.7/77.5.
  **No (program, k) reaches 34.4: the largest k is none.** Even the
  oracle (a different program per kick — 32 refits/orbit, and its
  predictions presuppose the true phases it is fitted on) leaves 61.16
  bits after one orbit.
- **Why B fails:** the program's state drifts from the truth by the
  accumulated payload itself; its rolling-window field fit collapses to
  0.26/0.36/0.06/0.06 absorption (vs 0.87/0.72/0.37/0.37 for true-phase
  single-kick fits) — per-kick prediction is self-defeating at these
  quanta. The checker's 61.2 is an oracle bound no regenerable program
  achieves: the honest carry is 63–76 bits (P1) or 45–57 (P3).
- **Per-element (P3, orbit 16):** δa 12.98, **δe 0.00 — the generator
  deformation absorbs δe exactly (median residual zero)**, δω 20.64,
  δM 20.64: the angle elements carry 76% of the residual at the 2⁻²⁴
  angle quantum (the checker's B18 note, now measured).

**The quantum valve (P3, k = 1, per-population scar quanta ×c):**

| c | steady-state sup W (orbit ≥ 2) | sup W incl. cold-start orbit |
|---|---|---|
| 1 | 57.17 | 66.47 |
| 64 | 39.18 | 42.48 |
| **256** | **33.19 ✓** | 34.50 (misses by 0.10) |
| 1024 | 27.18 | **27.18 ✓** |

So: **c\* = 256 for the steady state** (a-quantum 2,560 km, e
2.56×10⁻⁵, angles 2π/2¹⁶ ≈ 9.6×10⁻⁵ rad), **c\* = 1024 if the
cold-start orbit must also fit** (the first orbit carries raw before
the first recompile; the alternative is refitting sooner during orbit
1, not measured here). The checker's basis alone never fits: P1 at
c = 1024 still carries 34.90. k must stay 1 even at the valve:
sup_W(P3, k=2, c=1) = 70.18 measured; at c = 256 ≈ 38 ± 1 (derived)
> 34.4. Reactivation noise at c = 256 (the cost the memo-artifact
citation never quantified): a half-quantum state error per
reactivation = 1,280 km in a (1.1% of one orbit's natural δa drift,
1.12×10⁵ km) and 4.8×10⁻⁵ rad in angles (0.07% of the 0.065 rad/orbit
natural wobble); the per-orbit phase drift it injects is ~3×10⁻⁵ rad.
Bounded per reactivation, not compounding (the payload is recomputed
from the true state each epoch). At the measured belt quanta the
steady state instead costs 57.2 bits/body = 6.7 GiB per 10⁹ bodies
(1.7× the live budget).

**Predictions** (predictions.md, written before the decisive runs):
Q0 reproduction **held** (bit-exact, every anchor). Q1 **falsified**:
P1 post-refit at orbit 8 is 71.87, not 61 ± 4 — the 61.2 was the
per-kick oracle at orbit 1 (now reconciled at 61.16); the predicted
sawtooth (peak/post ≥ 1.2) is absent (1.04) — the phase-anchored
program absorbs so little of the total that mid-cycle shear costs only
~3 bits; peak ≥ 50 held (74.85). Q2 **held**: no k works, k = 1
optimal. Q3 **falsified high**: P2's plateau starts at 61.7, not
28–55 (the short-period leftover is larger than my Fermi estimate);
no-sawtooth held (1.08). Q4 **held at the top edge**: P3 = 44.87, in
[18, 45] (point estimate 33 ± 8 was 12 bits optimistic). Q5
**held**: c\* = 256 is the top of [1, 256] (point 8 was 5× low);
angles ≥ 50% held (76%). Q6 **held**: shuffle at chance, per-kick
absorption reproduced within 0.07.

## What would make it wrong

- A program class I did not test that absorbs the angle-wobble
  residual: e.g. the true-phase-evaluated predictive program (its
  regeneration is a fixed point I did not attempt), or a basis that
  includes Jupiter's true anomaly (the kick field is only approximately
  synodic-frame invariant — the window-fit collapse in B shows the
  modulation is real). Any such class must beat 54.3 → 34.4, a further
  ~2⁵ cut in residual magnitude at the belt's quanta.
- Horizon and regime: 16 orbits, cold belt, one perturber; the growth
  is decelerating but not zero, and resonant belts over 10²–10³ orbits
  (the scout's P4) are untested here.
- The entropy instrument saturates at 4·log₂N = 56 bits for N = 16384
  (sup_H = 55.5 even for P3 residuals); W is the verdict instrument.
  At 10⁹ bodies ideal entropy coding could sit below W, but both breach
  at the belt's quanta by ≥ 10 bits, so the kill does not hinge on it.

**Cost of adoption, fit with PRINCIPLES.** Informational, feeds
b-h-live / redteam-b18-belt: (i) B18's belt gate must judge residual
word cost at per-population quanta, never the marginal entropy of
deltas (saturated twice over now); (ii) shipmem's belt store needs the
two-block program (generator deformation ∪ phase-locked Fourier) with
reabsorption every orbit at ≈256× quanta — or 6.7 GiB per 10⁹ bodies
at the law's quanta; (iii) the angle quantum is the lever (41 of 54
bits). P24 "the memory floor is information" — the floor is now
measured at both quanta; P6 "store the generator" — δe absorbed
exactly is direct evidence the generator is the right store; P33 "each
scale resolves only what matters" — the 2⁻²⁴ angle quantum is four
orders below the belt's own wobble; the 256× per-population quantum is
that rule applied; P1 — the two-block program deletes 23 of 77 bits
before any optimization.

**The lens.** The second-author lens strengthened the program toward
survival (union basis, predictive variant, oracle reconciliation)
rather than attacking the physics: no second perturber, no resonant
belt at long horizons, no e-distribution tails, no N-scaling check of
the entropy instrument. The oracle-vs-61.2 reconciliation matches
every anchor to ≤ 0.07 bits but the checker's probe code was not
preserved (checker-patch.diff is empty), so a horizon difference in
their probe cannot be fully excluded — it does not affect the verdict,
which holds under every semantics measured. The 10 km quantum mislabel
was found by unit-checking at dossier time; all scout-run numbers
stand as measured, only their label changes.
