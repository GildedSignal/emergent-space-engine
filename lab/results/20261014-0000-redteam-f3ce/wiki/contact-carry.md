topic: contact-carry
status: open
closed-by:
valid-while:
updated: 20261014-0000-redteam-f3ce

# The contact carry: rounding at a mass-contrast contact, "never compounds"

## Current best

**The contact law's error model — representation.md §2's "at most one floor unit per
event, carried forward so that it never compounds" — is measured false on shipped code
for mass-contrast pairs and true for equal masses (20261014-0000-redteam-f3ce).** The
shipped resolver (`crates/lattice/src/relativity.rs::resolve_law`, law
`es-lattice-relativistic-v1`, the law the engine's battle scenes ship) parks each
contact's rounding on the lower-id body's carry and minimises |owed+e|² over the 16
candidate pairs. Measured with `crates/lattice/examples/rt_carry.rs` (Chronon
reference stepper, Q = 2¹⁶):

- **Ledger exactness (control):** ΣE(t) − ΣE(0) = Σ residual, exactly, at every
  checkpoint of every arm and seed (~25 runs). The bookkeeping is perfect; the physics
  it books is not.
- **Equal masses, β ≤ 0.7** (200-body gas, 5 seeds, ~4×10⁴ contacts): bounded —
  running-max exponent α = 0.02, end |Σres|/KE ≤ 4.5×10⁻⁶. **The premise holds for
  peer-to-peer battle.**
- **1000:1 pair, β 0.3–0.7** (10 seeds, 159–209 contacts): the pair-sum carry is an
  unbounded **random walk** (seed 4 swings −1.47×10¹² → +5×10⁸ → −1.04×10¹² in
  fixed-point energy units, E₀ ≈ 1.2×10¹³), per-contact steps 2×10⁻⁵–2.7×10⁻² of KE
  (median 8.4×10⁻⁴), end excursion 16.5% of KE at the median seed, 558% at the worst.
  At β 0.02–0.05 the step is 4.2×10⁻⁵ of KE (median) — the same mechanism, 20× slower:
  not an exotic-speed-only failure. *(Checker: the page's "+2×10¹¹" and "KE ≈
  2.6×10¹²" were misprints — the log's t = 2×10⁴ value is +5×10⁸, and the KE
  denominators are the end Σ m|k|² ≈ 1.9×10¹¹ at seed 4. "100% of KE within
  ~10²–10⁴ contacts" mixes the observed 10² with a linear 1/step extrapolation; a
  diffusive walk needs ~(1/step)².)*
- **Mechanism reading (post hoc, disclosed):** the energy ledger's quantum is
  per-unit-mass (E = m⌊2Q²γ⌋), so the light body's rounding step is a fixed fraction
  of the pair's KE, growing with mass ratio × γ — a representation mismatch in the
  carry. The author's frozen gas kill bars (median α ≥ 0.2 or frac > 1%) did **not**
  fire (mixed-mass gas median: α 0.055, 0.98%; walk exponents on 3/10 seeds
  0.38–0.53): the gas dilutes the pair mechanism. *(Checker: the "Q-independent at
  fixed (β, mass ratio)" claim is refuted — a measured ladder at the same scene
  (3 seeds, q = 2¹⁴→2²⁰) falls ~30–100× over 64× Q, roughly ∝ 1/Q; at the law's
  ceiling Q = 2²⁰ — the engine tests' own Q — the 1000:1 pair still steps
  2×10⁻⁴–4×10⁻³ of KE per contact. The walk survives at every legal Q; its magnitude
  does not.)*
- **Label-invariance (the principle-4 attack) survives:** swapping the ids of the
  1000:1 pair changes no velocity at any contact (10/10 seeds; the carry's *home*
  differs, the outcome does not). A 32-body gas with permuted ids diverges at tick
  16–25 (5/5 seeds) — chaos-amplified quantum noise, the same class as any rounding.

**Domain.** Two-body box pairs and uniform/stirred gases at stress scale (Q = 2¹⁶,
radius Q, box 64Q), β ≤ 0.9, masses 1–1000, ≤ 6×10⁴ chronons; the Chronon CPU
reference (bit-identical to the shipped orders by the crate's own tests). Unmeasured:
the per-contact error distribution (only the cumulative walk), 3-body carry-routing
chains, contact rates at game-second scale (player-visibility horizon), law v0, walls
with energy absorption, and any fix.

## Refuted

- "The contact error budget never compounds" (representation.md §2): an unbounded
  walk at mass contrast, step ∝ light body's energy quantum as a fraction of pair KE
  (20261014-0000-redteam-f3ce).
- "The lower-id carry routing makes contact outcomes label-dependent": 0/10 pair
  seeds diverge under a full id swap (same run) — the routing moves bookkeeping, not
  physics, in the measured domain.

## Open directions

1. **Freeze the missing r5 criterion** (dense order, never frozen; no gate, rung or
   oracle watches contact energy — B12 judges orbit laws, H0173 measured entropy):
   a 1000:1 pair at β 0.6, 200 contacts, |Σres|/KE < 1%, with the equal-mass pair
   as the positive control. *(Checker: the isolated equal-mass pair (1000:1000,
   β 0.3–0.7, 3 seeds) sits at 2–3×10⁻⁵ of KE₀, not 2×10⁻⁶ — that number is the
   gas arm's end fraction. The 1% bar still separates the two by two orders.)*
   Catches the defect in seconds; freeze it at the engine's Q = 2²⁰.
2. **Re-derive the carry at pair scale** (the principle-19 reading of the fix): carry
   in the pair's CM energy where the quantum is the pair's own, or route per pair
   instead of per body; the ledgers stay exact either way. Local to `resolve_law`.
3. **Price the player-visible horizon:** contact rates per ship at game-second scale
   × the measured per-contact step (8.4×10⁻⁴ of pair KE median) → hours-to-visible
   for persistent mass-mixed battles; unmeasured.

## Contradictions

None open. The gas arms (bounded at the median) and the pair arm (walk) are the same
law at different dilution, not a conflict; both are recorded above.

## Runs
- 20261014-0000-redteam-f3ce (awaiting grade): contact carry compounds at mass
  contrast (pair walk, median 8.4×10⁻⁴ KE/contact, 558% worst; equal masses 10⁻⁶);
  label-invariance survives; no rung watches contact energy.
