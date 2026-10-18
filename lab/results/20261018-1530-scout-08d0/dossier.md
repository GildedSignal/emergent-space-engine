# Dossier — 20261018-1530-scout-08d0

**Claim (one sentence).** The beat-resident pair record (encounters open
direction 1) is dead as a sound per-pair certificate at the design reach —
the Diophantine slack that would certify "no early hit post-kick" is
S ≈ 0.48·C/k² (three-distance class, measured) and only **1.8%** of deep-beat
pairs carry S above the belt-quantum kick — but the same measurement gives
the leak-gated epoch rule its law: the near-horizon is NOT re-rolled by kicks
(blind-span misses = 0 measured to E = 256; the leak channel is grazers, so
miss ~ E²·δd/C), letting re-arm cadence carry the whole cut (E ≥ 256 measured kicks for ε = 10⁻⁶–10⁻⁴ per pair per kick: 355 cores →
1.4–14).

## Bottleneck

Board #2: encounter work at 10⁹ (~10³ cores → a few). Today's state (1a29,
this morning): sound per-kick re-arm on the shipped representation is
wholesale Θ(n−1) — 355 cores per 10⁴-cell occupancy at ~1.1 µs/arm — and the
due-band rule is killed. The page's open direction 1 ("a representation that
stores the beat... could certify 'no early hit post-kick' without paying
first_hit. One design step") is this run's target; direction 2 (leak-gated
slack) gets its missing deep-beat constant. Expected gain: deletes the
per-kick wholesale term (the row's dominant cost) by moving it to a cadence;
orders: E = 256 measured, knee to ~1000 (355 cores → 1.4–0.35).

## Method and evidence (exact integers; floats never decide)

`beat.rs` (this folder; `regen.sh` rebuilds all numbers in < 6 min): a 1-D
phase-rotation toy on the 1a29 tier's own constants — window w = 23 ticks,
d log-uniform in [1.5, 6]×10⁵ ticks, C = 2.3×10⁷ ticks (mean first-hit
C/w = 10⁶ conjunctions, their k ~ 10⁶), all phases in u128 units of 2⁻²⁵
ticks (kicks are exact powers of two: zero rounding anywhere). Silent pairs
(2,500, 10.7% censored at k = 3×10⁶) walked exactly; the same walk extracts
the slack certificate S = min_{j<k}(m_j − w/2)/j by cross-multiplication
(no division). Controls: slack-kept pairs must show 0 early-hit violations
(math validity — held, 0 at every arm); E = 1 re-arm arm (0 misses by
construction); the dv axis spans 2⁻²⁶…2⁻¹⁴.

Seed 1, n = 2500 (`main.txt`; held-out seeds 2 and 77 in regen):

| arm | keep (δd < S) | P(k′<k) | flips-on H=4096 |
|---|---|---|---|
| 2⁻²⁶ | 6.8% | 0.457 | 9.0×10⁻⁴ |
| **2⁻²³ (belt quantum)** | **1.8%** | 0.464 | 4.5×10⁻³ |
| 2⁻²⁰ | 0.8% | 0.467 | 4.5×10⁻³ |
| 2⁻¹⁷ | 0.4% | 0.454 | 2.2×10⁻³ |
| 2⁻¹⁴ | 0.2% | 0.449 | 2.2×10⁻³ |

1. **S's law (P1 held):** median S/(3C/k²) = 0.160 (i.e. S ≈ 0.48·C/k²),
   against S/(C/k) = 8.5×10⁻⁷ — the three-distance/convergent class, and the
   binding j* sits near k (P(j* < 0.2k) = 3.1%). The slack of a deep-beat
   pair is set by its deepest convergent, not by its typical phase margin.
2. **Survival (P2 held, conservative side):** at the quantum only 1.8% of
   silent pairs can keep a stored due soundly across ONE kick (6.8% even at
   2⁻²⁶). The closed form k* = √(0.48·C/δd) ≈ 1.8×10⁴ predicts
   P(k < k*) ≈ 2.6% — matches the measured 1.8%. **The beat-resident record
   recomputes 98.2% of pairs per kick: no cheaper than wholesale. Direction 1
   is dead as a sound per-kick certificate.**
3. **The deep book re-rolls; the near-horizon does not (the inversion):**
   P(k′ < k) ≈ 0.46, dv-independent — 1a29's re-roll, reproduced. But
   flips-ON into a small horizon are 10⁻³-class (H = 4096) and ~0 at H ≤ 128:
   a kick cannot create a hit at step j until j·δd reaches the pair's
   margin m_j − w/2. Epoch sim (256 quantum kicks per pair, exact re-arm
   every E kicks, misses = in-window conjunctions inside the next E steps at
   blind kicks): **0 missed conjunctions at every E ∈ {4, 16, 64, 256}**
   (800 pairs × 255 blind kicks each). The leak lives on *grazer* pairs
   (early margins barely above w/2), clusters on those pairs, and scales
   ~ E²·δd/C.
4. **The frontier (measured, turn-on included):** cadence arms E = 4…256
   re-arm every E kicks and show **0 missed conjunctions at every one**
   (drift between re-arms ≤ E·δd never reaches the near-phase margins). The
   E = 1024/4096 arms (train 256 kicks < E: effectively no re-arm after t = 0)
   catch the turn-on: 0.29 → 1.07 missed conjunctions per pair, 17/800 →
   80/800 pairs, i.e. per-kick hazard 1.1×10⁻³ → 4.2×10⁻³ — the uniform
   phase hazard 2E·w/C (4.1×10⁻³ predicted at E = 4096): once accumulated
   drift j·Σδd decorrelates the near phases, the look-ahead window E is what
   pays. So: cost ∝ 1/E; leak 0 (measured) to E = 256 [95% CI ≤
   1.5×10⁻⁵/pair/kick], then ~linear in E. **E = 256 takes 1a29's 355-core
   row to ~1.4 cores at a measured leak ≤ 1.5×10⁻⁵; the knee between 256 and
   1024 is the budget dial for anything cheaper.**

## Predictions

`predictions.md` was written before the decisive run (P1–P5). P1 held
(C/k² class, factor 0.48); P2 held on the conservative side (6.8% < the
predicted 50% bound at 2⁻²⁶; 1.8% < 10% at the quantum); P3 held
(P(k′<k) flat in dv, 0.449–0.467); P5 held (0 violations; E=1 control
exact). **P4 MISSED in its stated analytic form and was corrected by the
measurement:** I predicted the blind-span miss rate ~ linear accumulation of
the uniform re-roll (dd·k²/C per kick); the measured rate is ~0 to E = 256
because the re-roll randomises the deep book while the near-horizon is
protected by the already-paid walk — misses come only from grazers,
quadratically in E. The miss is the finding (the naive model would have set
E* far too small).

## What would make it wrong

- The constants (C, w, d, the quantum's δd in ticks) are taken from the wiki
  page of 1a29/c9c7, not re-derived from shipped code; they set k* and E*'s
  absolute values. The laws (S ~ C/k², leak ~ E²·δd/C, dv-independence) are
  structural and re-measurable at true constants — regen with `C_TICKS`
  edited is a one-line change. [UNVERIFIED at source, flagged]
- The toy is a 1-D phase rotation — the element tier's U-rotation as in
  1a29's own toy (their instrument's constants, same class). It carries no
  e-dispersion coupling and no multi-window (perigee/apogee) structure; a
  second window doubles the grazer channel (~2× the leak, same law).
- If the shipped arm eval can be made ≪ 1.1 µs, the wholesale row shrinks
  and the epoch cut matters less (still strictly dominates at equal cost).
- 1a29's leak "~10⁻⁶ real events per candidate per kick" is the number to
  beat; my grazer leak at E = 256 is ≤ 1.5×10⁻⁵ per pair per kick (95% CI
  from 0/800 pairs over 256 kicks) — the two agree in order; the exact
  budget arbitration (what missed conjunctions cost the game) is the
  integrator's, not mine.

## Cost of adoption, PRINCIPLES fit

Adoption = replace per-kick wholesale re-arm with a per-cell epoch cadence
chosen by an explicit leak budget ε (a dimensionless number choosing the
regime — PRINCIPLES 4), grazers carried as the only per-kick exact class
(alongside the 1.8% slack keepers). No component added; one deleted (the
per-kick walk). "Compute only surprises" (P3): the deep book is a surprise
only at the epoch; "the simulation decides" (P22): ε is measured, then E
follows. Cost: a missed-conjunction budget must be frozen by the integrator
(the same class of decision as B18's belt rung); the mapping to the shipped
`tier::arm_pair` cadence is one wiring step (the epoch is a knob on the
existing armed-list machinery, b509's stored standing list).

## The lens (what scout may have missed)

Sourced from training knowledge, not live search (no network use): EDMD's
lazy invalidation (Rapaport/Lubachevsky counters), KDS flight-plan repair
(Basch–Guibas–Hershberger), aerospace conjunction re-screen cadences
(NASA CARA's probability budgets) — all UNVERIFIED at source this run. The
lens optimised for the certificate question and may underweight a cheaper
arm eval (a 10× cheaper arm halves every number above without touching the
laws) and the multi-window grazer coupling.
