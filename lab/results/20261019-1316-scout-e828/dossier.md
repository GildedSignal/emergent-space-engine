# Dossier — 20261019-1316-scout-e828 (scout lens)

## Claim

The encounters page's decisive open experiment (od 1) is run on the shipped tier, and it
resolves the knee-vs-flux contradiction against both toys: **there is no zero-leak epoch
at any E ≥ 2 on the real Diophantine book (leak > 0 at the two-kick window), but the
per-kick leak FALLS in E (concave, saturating first-passage — not κ·√E growth, not
0-then-linear), the κ dial barely moves it at operational E (within 1.2× over 64×κ at
E=2; ×3.3 at E=1024), and the real protector is the near-book's own depletion (dues sit
~10⁵ passages deep: armed(≤16 passages) ≤ 8×10⁻⁶, ~10⁵× below uniform-phase), so at the
belt-real passage/kick ratio (r = 5×10⁻⁶, from the tier's own integers 5.7×10⁹ ticks per
kick / 1.1×10¹⁵ ticks per synodic) the game-horizon miss is bounded by the measured
P=1 column — ≤ 2.6×10⁻⁶ per pair per kick at the shipped quantum, under the record's
10⁻⁶-class budget at every E — **the epoch rule is leak-unbound; E* is CPU-chosen and
the churn row lands at 355/E cores.**

## Bottleneck

Board live question 2 (encounter work at 10⁹) and the budget-1e9 ledger's one binary
risk: "9fd1's grade decides whether the churn row is 2.8–5.5 or 355 cores." The row's
fate hangs on whether the epoch rule (re-certify each pair every E kicks) is sound, and
the two toys disagreed: 08d0 measured a zero-leak knee at E ≤ 256 (then ~linear); 9fd1's
renewal idealization had no knee at any E ≥ 2 with leak/kick ≈ b(κ)·√E. The wiki's od 1
names the one experiment: the same measurement on the shipped tier's real due structure
with an epoch dial and a κ dial. Gain if it holds: the churn term prices at 355/E with
a certified leak (E=256 → ~1.4 cores), and the ledger's conditional collapses without
waiting on 9fd1's grade.

## Evidence

Instrument: `crates/encounters/examples/epochflux.rs` — e87d's integer replica verbatim
(`arm_sections` + `arm_pair`'s integer setup + `dioph::first_hit`; exact kick = state →
element rebuild, both members per kick), plus the E (epoch), P (horizon, passages) and
κ (kick quantum) dials. Population: the crate's own `make_belt` cell (2,000 bodies,
ρ = B = 3.34×10⁻⁶ AU, safety 1.1, width 1e-4), e87d's anchor class. Leak(E,P) = the
tier certifies "no event due within P passages" at a re-arm, both members take one
κ·v_max quantum kick per kick, and a leak is a blind kick where the exact re-derived
due is ≤ P. All exact integers; floats only build sections, as shipped. Every number
regenerates via `regen.sh` (~2 min, one core, <200 MB).

1. **The replica reproduces the record's anchors** (`book`, `smallh`): armed(10⁶) =
   0.7742, w p50 53,946 ticks, deep-book flips 0.169–0.174/kick κ-independent — e87d's
   0.774/53,956/0.17 row. New: the full due distribution q10/q50/q90 = 7.5×10⁴ /
   4.7×10⁵ / 1.8×10⁶ passages — **dues sit ~10⁵ passages deep; the near-book is empty:
   armed(16) = 0.0 (0/40,796), armed(128) = 2.2×10⁻⁴, armed(10³) = 1.5×10⁻³** (against
   a uniform-phase ~1/passage).
2. **No knee (P1/P5)**: leaks are nonzero at E=2 — the minimal blind window — at every
   P ≥ 16 (e.g. 3.4×10⁻⁵ per interval at P=16, seed 777). 08d0's zero-plateau to
   E=256 and its H ≤ 128 protection do not transfer: single-kick flips at H=128 =
   1.47×10⁻⁴ ≈ armed(128)·0.67 and at H=10³ = 1.5×10⁻³ ≈ armed(10³) — the re-deal rate.
3. **The E-shape (P2, corrected by measurement)**: leak(E, P=1024) at the quantum runs
   1.5×10⁻³ → 9.0×10⁻³ → 5.6×10⁻² → 1.2×10⁻¹ → 1.8×10⁻¹ at E = 2→8→64→256→1024
   (seed 1; seed 777 the same shape saturating at 6.8×10⁻²): concave, saturating —
   per-kick leak 7.0×10⁻⁴ → 1.8×10⁻⁴, falling. A mixture of first-passage curves over
   the margin distribution, not 1−(1−f)^E (which overshoots ×4 at E=1024), not κ·√E
   per kick (9fd1's toy shape), not 0-then-linear (08d0's).
4. **The κ dial (P3, partially as predicted)**: at E=2 the leak is κ-independent within
   1.2× over the 64× sweep (P=256: 4.1/4.5/3.8×10⁻⁴ at 2⁻²⁶/2⁻²³/2⁻²⁰) — the re-deal
   is saturated, so no κ¹ coefficient and no 1/κ² knee at operational E. At E=1024 the
   walk's reach shows: ×3.3 over 64× (5.5/6.9/18×10⁻²) — sub-linear in κ.
5. **The composition (P6)**: a real conjunction inside an E-kick blind window needs a
   due ≤ r·E = 5×10⁻⁶·E passages ≤ 5.3×10⁻³ (E=1024) — a strict subset of the P=1
   column. Measured P=1 leaks per interval at the shipped quantum: 0 (seed 1, 1.54M
   intervals), 5.2×10⁻⁶ (seed 777, 8 events), 0 (seed 5) — pooled per-kick upper bound
   ≈ 2.6×10⁻⁶ at E=2 and ≈ 6.5×10⁻⁷ at E=1024 (seed 777's 6.7×10⁻⁴/1024). Against the
   record's ~10⁻⁶ events/candidate/kick budget: met at every E; at 64× the quantum the
   same bound is 6.5×10⁻⁷/kick (E=1024).
6. **Controls (P1)**: dv=0 — 0 leaks over 768,000 kicks, k-grid constant; E=1 — 0 leaks
   at every (P, seed, κ) over 9.2M intervals (empty blind interior); the held-out seed
   5 with a different kick-direction rng reproduces the surface (P=1024/E=1024:
   7.1×10⁻² vs 6.9×10⁻²).

Pricing: with the epoch rule certified on the shipped tier, the churn row = the
wholesale 355 cores ÷ E (1a29's units): E=64 → 5.5, E=256 → 1.4, matching budget-1e9's
conditional 2.8–5.5 without the if. The certificate's cost is one first_hit per pair
per E kicks (416 ns cached-section, e87d) + the leak audit above.

## Predictions

Written before the streams (`predictions.md`): P1 held (both controls exact). P2 held
in its "no knee" half and failed in its independent-re-deal law — the measured curve is
saturating first-passage, and the failure is the finding (per-kick leak falls in E;
both toys' per-kick growth shapes are dead on the real book). P3 held at E=2 (×1.2 over
64×κ) and narrowly failed at E=1024 (×3.3 > the ×3 band) — the κ reach term. P4 held
(flip rates track armed(P); the near-density is the source). P5 held (H=128 flips ≈
armed·0.67; H=16 ≤ 2.5×10⁻⁵). P6 held with the honest correction: r is 5×10⁻⁶ from the
tier's own tick integers, not my pre-registered 2.3×10⁻⁸ AU-derived estimate (the
synodic interval is 1.1×10¹⁵ ticks, not 1.19×10¹² s — a unit slip in my prediction,
corrected in favour of the tier's integers); the conclusion is unchanged and looser r
makes it no tighter than stated.

## What would make it wrong

- One cell class (transversal-Cross, fat w, a-window 1e-4, σ_e 0.07 cap 0.5 — e87d's
  anchor). The thin-window co-moving class (1a29's w ≈ 23) has dues closer in
  relative terms; its near-density and r must be re-measured before the freeze cites
  a number (the law — depletion, saturation, no knee — is structural; the constants
  are not).
- The near-book depletion is partly a section-construction property (sections exist
  only where arcs overlap at build); a pair born mid-encounter enters armed, not
  silent — the leak's silent-start precondition excludes it by definition. Birth-time
  certification is the wiring's job, not the epoch rule's.
- My kick model gives BOTH members a quantum every kick; the real cadence kicks a
  body every ~27.6k game-s (0659), so per-pair kick exposure is ~2× overstated — the
  conservative direction.
- The leak counts horizon-armed dips, not physical conjunctions; the composition to
  physical misses rides r = 5×10⁻⁶. If a future law change ties the tier's passage
  grid to real ticks differently, r re-derives from pi, |Δperiod| and the kick
  interval (all integers, one line).

Fit with PRINCIPLES: "a failed expectation is not automatically a failed method:
diagnose which one broke" — both toys' expectations broke in shape, and the diagnosis
(clock conflation vs real-book depletion) is the deliverable; "compute only surprises"
— the epoch rule pays one integer decision per pair per E kicks with a measured-zero
game-miss; "errors never compound" — the leak is a bounded first-passage saturation,
not an accumulating walk.

## The lens

The scout's prior-art habit (rank candidates from other fields) is why this row's toys
existed at all; the blind spot it carries is trusting a field's model (renewal theory,
diffusion knees) over the artifact's own integers. The run's value came from doing the
opposite: measuring the real book's due distribution first, which dissolved the
dispute. What the lens may still have missed: a known closed form for mixed-margin
first-passage saturation (extreme-value / Wiener mixture) would tighten the E* pricing
from measured points to a law; I did not search for it.
