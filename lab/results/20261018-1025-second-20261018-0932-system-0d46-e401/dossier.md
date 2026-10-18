# Run 20261018-1025-second-20261018-0932-system-0d46-e401 — second author on 0d46 (system lens)

## Claim

**0d46's ~300× phase-word deletion of the gather's crowd term is refuted as stated, and bounded:**
the wiring (b083/5f36's phase word in `view.rs`'s emitter loop, one shared compiled key + one
per-member phase word, degrading on scarred members) was built, audited and priced, and it holds
**exactly where it applies but deletes one order, not two, and covers ~0% of a live crowd**: on a
4,000-member formation (one shared key by construction) the tier prices **0.56 µs/member (solve
0.13, row 0.27) against the shipped 7.3 µs/body — the walk term falls ~13× end-to-end (~50×
crossing-to-crossing)**, the audit is display-exact (**48,000 rows: 0 pixel violations, t_e exact 48,000/48,000, max
Δlight_seconds 1.3×10⁻¹¹ of tolerance**) — but the shipped bench crowd has **no
shared keys at all** (the battle disperses them: exact keys ≈ all distinct; even 2⁻³-relative
quantized grouping peaks at 37), and on the flown formation **every member's emission-tick read
lands inside its current step's partial/ramp window (kick_inel = 4,000/4,000 per steady window)**,
so the pure-tube tier degrades everything to the individual read in flight: the deletion needs the
step's shared kick inside the word. The checker's decomposition (asked first) confirms the target:
**the crossing walk is 0.70–0.97 of the gather's body loop on every scene flown** (0.95 on the
formation; row math 3–5%).

## Bottleneck

Board focus 1 (bodies: 10⁶ → 10⁹) via the view page's open direction 2 (the phase word in the
gather). What this settles: the lever is real but formation-class only, its magnitude is ~13×
(row math is not a compare), and its blocker is the motion law v2's partial step, not the
representation. What it deletes at adoption: nothing yet — one named experiment away (the kick in
the word).

## Evidence (all from the patched probe, print-only; regen: `regen.sh`, ~4 min)

- **The decomposition (D, asked first).** Timers inside the shipped body loop split the crossing
  call (Newton + `state_rate` readouts) from the row math. Cross share of the loop: **0.70–0.97**
  (bench crowd across windows, 0.96–0.97 steady at 12.6 µs/body; control 0.96 at 32 bodies, 58
  µs/body — the fixed per-frame cost amortises, the walk never leaves; formation 4,071 bodies
  **0.95**, cross 28.1–29.4 ms, row 1.08–1.16 ms, 7.2 µs/body). 51bf's 95% on the 28-body plane
  holds on crowds: **if the phase word deletes the crossing it deletes the gather** — row math is
  3–5%.
- **Arm A (the shipped bench crowd, 0d46's own scene).** The census (one `binding_at` per body,
  0.43 µs/body — the scan's own capture walk) finds **exact compiled keys ≈ one per body**
  (215 distinct keys for the crowd's ~213 live from-members at the last window, and every window
  groups 0 at 2⁻¹⁴; the formation's 4,000 stand at 2 in the same instrument).
  Quantized grouping at 2⁻¹⁴ relative: groups=0. Coarser (the domain probe): 2⁻⁸ → gmax 3, 2⁻⁵ →
  11, 2⁻³ → 37. **The bench crowd is battle-dispersed; efd4's 2-key formation census does not
  transfer to it.** On this scene the phase word deletes nothing (0d46's "what would make it
  wrong" named exactly this lever class, and the checker's out-of-range 2.3k crowd was the same
  battle).
- **Arm B (the formation, `examples/phasegather.rs`: K=4,000 ring, one `OrbitSpec` but the phase,
  e=2⁻⁴⁸, Home's doll, beside the shipped plane).** One group of 4,000 (gmax=4,000; the locals
  stay singletons and degrade by construction). Flown through the shipped `gather_cached`:
  - **Price (steady windows):** tier **2.23–2.33 ms/frame = 0.56 µs/member** (solve 0.53 ms =
    0.13 µs; row build 1.09–1.18 ms = 0.27 µs — the same `push` math as shipped), against the
    shipped loop **29.5–30.9 ms = 7.3 µs/body** (crossing 6.9). **Walk term ~13× end-to-end,
    ~50× crossing-to-crossing.** Census 0.45 µs/body. The 10⁶-crowd extrapolation: this term
    6.9 s/frame → ~0.56 s/frame (not ~0.02 s).
  - **Audit (2df1's standard: sky-polar pixel at 432 px over log₁₀ ls ∈ [−5, 3.6]; panel
    |Δ| > 10⁻⁴·|x| + 10⁻¹²):** the pure regime (the first window, before the members' first steps
    fire: 800 of 4,000 tiered per gather) audits **48,000 rows: px_viol=0, panel_viol=0, t_e
    exact 48,000/48,000, max deltas 1.3×10⁻¹¹ / 1.1×10⁻¹² / 10⁻⁴ of tolerance** (K=1,000 the
    same: 12,000 rows, 0 violations). The representation is exact: one compiled key + one phase
    word reproduces the shipped row to float noise on a rigid ring.
  - **Coverage (the wall):** windows 2–4: **tiered = 0, kick_inel = 4,000/4,000 per gather** —
    the emission tick (~10⁴ root ticks back) falls inside the current binding's partial/ramp
    window, so the shipped readout is the partial step (a per-member field eval) and the pure-tube
    tier must degrade (0d46's own lens risk, now measured as 100% of steady reads, not a tail;
    the 200/gather average is window 1 alone). Rebindings (rebound 1,970 in window 2, 0 after)
    are second-order beside it.
- **Control (`--members 4`, 32 bodies):** cross share 0.70–0.79, tier groups all singletons —
  the individual read is the default everywhere outside a formation.

## Predictions (`predictions.md`, written before the decisive flights)

- **D1 held** (cross ≥ 60%: 0.70–0.97, formation 0.95).
- **C1 half-held then refuted on the named scene:** the ≥300-in-groups prediction was withdrawn by
  measurement twice — exact keys are all distinct on the bench crowd (arm A), and the formation's
  group of 4,000 exists only by construction. **C2 failed:** ≥30% eligible in flight — actual
  100% in the pre-step window, **0% after the first kicks** (kick_inel 4,000/4,000); the risk I
  pre-registered ("I do not know the live-kick fraction") resolved to ~100% live.
- **A1/A2 held** (≥99% display-exact, max |Δt_e| ≤ 1: 48,000/48,000 exact, 0 violations).
- **P1 held on its letter** (tier ≤ 0.3 µs predicted for the solve+row: solve 0.13 µs; the full
  row path 0.56 µs — 1.9× my letter, and 2.8× the kill line of 1 µs is not approached) — but the
  **projected ~300× was the wrong number to test**: 13× end-to-end is what the row math leaves.
  **P2 held** (census 0.45 µs/body).
- Kill criteria: none fired (cross 0.95 ≥ 0.5; audit 100% ≥ 95%; tier 0.56 < 1 µs) — but the gold
  claim as 0d46 stated it (≈300×, "the same lever" on the shipped crowd) is dead on the domain
  and magnitude evidence, not on the kill lines I wrote for my own tier.

## What would make it wrong

The tier's price excludes the audit by construction (double-read) — an adopted tier would not pay
it; it also excludes the incremental word-store maintenance (rebinds refresh words; the census
walk here is per-frame, 0.45 µs/body, and is the same walk the scan's capture pays — one store
serves both). The formation arm is one (K, e=2⁻⁴⁸, seed) point: an eccentric formation (the
circular fit degrades as e grows) and a kicked-but-coherent formation (the scar index's cost) are
unflown; the battle-crowd verdict is measured at three quantizations, not proven at all. The
partial-step blocker is measured on this scene's step cadence (step_log2 = 7); a sparser cadence
would raise coverage without changing the mechanism.

## Cost of adopting, and fit

Nothing to adopt yet: the wiring exists (in `work/patch.diff`, print-only) and is one experiment
away from a law change — put the step's kick in the word: the partial step's field eval is the
shared sources' field at the member's mid-tick; on a ring those mid-points sit within a Taylor
sheet of one shared eval (the sources are the doll's secondaries, shared per frame; PRINCIPLES 33:
"a body resolves only the influences that are significant at its own scale"). If that lands, the
crowd's gather term is the formation's 13× at live coverage. PRINCIPLES 32 ("under the right
representation many symmetries can appear") is affirmed by the audit — the symmetry is real and
exact; 3 ("compute only surprises") is what the 0.56 µs floor teaches: a row is not a surprise
per member, but it is also not a compare — 0d46 borrowed the scan's 19.2 ns figure for a path
that must still build a row.

## The lens (what the second-author lens may have missed)

I measured the crowd's CPU win and priced the scan's byte win by identity of the walk (the
census), not by wiring the scan side again — 5f36 already flew it; a checker may want the 224 B
pin counted against the word's own bytes (the word is ~16 B: angle + time). The formation scene is
my own construction (as 5f36's was); the bench crowd is the shipped one. I did not run the
eccentric formation (time); the circular-fit error there is the obvious next probe, and the
quantization sweep (2⁻³…2⁻¹⁴) is a coarse instrument for it.
