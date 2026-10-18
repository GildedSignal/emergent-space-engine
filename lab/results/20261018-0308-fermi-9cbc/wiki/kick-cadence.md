topic: kick-cadence
status: open
closed-by:
valid-while:
updated: 20261018-0308-fermi-9cbc

# Kick cadence: how often a body is kicked, and by what rule

## Current best

**[20261018-0308-fermi-9cbc, fermi] The standing 10⁹ CPU row (4e2d/de7b/f790's "10.3 M1
cores, 2.6× over, split S* ≈ 20, kick ≤ 23 µs REQUIRED") is not regenerable from any
anchor on this page at any pace: it implies a belt rate of 9.9 events/body/interval where
the page's own thrice-measured census says 2.00 (a9d7's gold N-invariant 3.55e-5 = 1/28,141.5
exactly; 3294's fire-rate 1.000; 8ffc's two combs + two checkers) — a 4.9× locals-dominated
scene-rate artifact (the row's own anchors fly 73.8k + 71.6k events per comb window at
N = 10⁴ with the locals' N-independent 86–88k/interval stream, divided per-body).**
Recomposed from the census: **rail = 2.08–5.12 cores × (rtf/100) × S** (two combs; cost
bracket 29.3 µs M1 event / 50 µs x86 / 72 µs fired kick; S = belt survival under the
secular delete, 1 / 0.615 / 0; the re-kick add-back at S = 0 is 0.28% × 0.57). Controls:
9e75's own "the average fits: 1.75 cores at rtf 1" regenerates exactly (1.78); the
rtf-100 siblings regenerate as pace costs (208 ≈ "185–187 at rtf 100", 178 ≈ e7ef's
"104–178"); the 126-bit memory bust fails as it must. **At rtf 1 everything fits (≤ 5.12
worst corner, ≤ 3.15 with the flown delete, ~0.97 at RES incl. encounters 0.95 + view +
reabsorb); at the shipped player pace rtf 100 (Julien flies `--rtf 100`, HANDOFF) the
stream alone is 208–512 cores no-delete and 128–315 at the flown delete — the row
UNDERSTATES 20–50× — no measured cadence lever closes it at S ≥ 0.615 (split 8 → 26–64;
split+delete → 16–39; the ~50 ns event floor → 0.36), and even RES carries the ×100
game-rate terms (encounters ~95 at F = 10³ on b509's basis).** The crest at rtf 1 is the
genesis wave, not a steady rate (steady demand 7.1×10⁴ ev/wall-s = 2.1–5.1 cores; the wave
peaks ~20× for ~1.4×10³ game-s at birth, one-time, stagger-cured — f82a); 9e75's 19–20-h
freeze is the rtf-100 budget clamp. **Consequence: two never-pinned conventions — the
player's pace (rtf) and the resonance-exclusion width (S) — are together a >100× dial and
are THE 10⁹ CPU decisions; the "split ≥ 21×" and "≤ 23 µs kick, no measured lever"
requirements are artifacts of their product.** The S dial, from shipped `scenario.rs`:
the frozen exclusion replica (j,k ≤ 8, 2% on period) spares 0.530 against the flown
anchor 0.615 (ratio 0.86); **no first-order (j+1):j resonance of any planet falls in
[2,3) AU** (all the belt's commensurabilities are ≥ 2nd order; Cinder's ratio to the belt
exceeds 8 — it spares exactly zero), and the frozen 2% flat width is the Giant's shipped
first-order width (2.5·μ^(2/3) = 2.46%, resonance.rs:59) × 0.8 but 33× Home's and 131×
Cinder's — Giant-width protection for resonances with no first-order member: the width is
a dial, not a tide fact. Memory (6793) binds once pace and S let CPU close (1.58×10⁶ live
at the 5,060 B plateau; q16 3.0 GB + 1.3 kB live ≈ 8.0 GB at ~3.85M).**

*[Prior best retained below: the boundary comb's information price (3570/16ec), the welded
two-comb structure (de7b/f790), the crest/freeze record (4093/9e75/8ffc/98cb), e7ef's
closure product, and the regime-aware rule sections — the 10⁹ ledger rows of 4e2d/de7b and
the "104–178 falls to 5.1–8.65" row of e7ef are superseded by the census-rate
recomposition above; their cadence-lever measurements (split 8, welding, freeze cure)
stand unchanged.]*

## Refuted

- **The standing 10⁹ CPU row's belt rate (implicit 9.9 ev/B/interval; 98cb's composed
  4.44e-6 ev/B/frame = 7.5, already listed below): a locals-dominated scene-rate
  artifact** — the per-body division of a scene count that includes the locals'
  N-independent 86–88k/interval stream; the belt's own census is 2.00 everywhere
  measured, and 10⁹ is all belt (20261018-0308-fermi-9cbc).
- **"10.3 M1 cores (2.6× over the 4-core budget)" and "split S* ≈ 20 closes CPU" as
  pace-free statements: dead at both paces** — at rtf 1 the recomposed rail fits without
  any split (≤ 5.12 worst, ≤ 3.15 with the delete); at rtf 100 it is 128–512 cores and
  split 8 buys only 16–64: the row is 5× high or 20–50× low depending on the unstated
  pace, and neither reading regenerates (20261018-0308-fermi-9cbc).
- *[prior refutations retained: the one-crest reading; the boundary-floor branch; e7ef's
  composed row as stated; the kick-floor-as-10⁹-requirement reading — now with the
  sharper form: at rtf 1 the floor is unnecessary, at rtf 100 it is the only single-lever
  closure (0.36 cores).]*

## Open directions

1. **Pin the pace (the integrator's one sentence):** every "×-over-budget" 10⁹ statement
   on this page multiplies an event rate by a cost by a pace; the pace was never pinned
   (rtf 1 literal vs the shipped `--rtf 100` flying config). Until it is, CPU ledgers
   should be printed as `cores × rtf/100 × S` (20261018-0308-fermi-9cbc).
2. **Price the exclusion width (the S dial, 21–51 cores per 0.1 at rtf 100):** the frozen
   2% is Giant-first-order-width applied to ≥ 2nd-order resonances (no first-order member
   exists in [2,3) AU); the legality experiment is B17's width law flown at the belt's own
   commensurabilities vs the Giant and Home. RES legality (S = 0) is the only single-digit
   closure at rtf 100 short of ns-class events.
3. *[prior directions retained: the key-range test's burn-arm harness (16ec); the fleet
   population contract (b509's od 2, now load-bearing at rtf 100); the belt-anchor
   dispute; the kick-cost bracket 29.3 vs 51–72 µs reconciliation on the M1.]*

## Contradictions

- New: e7ef/4e2d's "the player's rtf 100" vs 9e75's "the average fits at rtf 1" — never
  reconciled; the recomposition carries both (the table's two columns) until the
  integrator pins the pace. Recorded so no run reads one column as the other.

## Runs
- 20261018-0308-fermi-9cbc (fermi, this run): the 10⁹ CPU row re-derived independently —
  the standing 10.3-core row implies 9.9 ev/B/interval vs the census 2.00 (a 4.9×
  locals-dominated artifact); rail = 2.08–5.12 × rtf/100 × S; pace and exclusion width are
  the unpinned >100× dial; no first-order resonance exists in the belt.
