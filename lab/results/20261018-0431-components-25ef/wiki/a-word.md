topic: a-word
status: open
closed-by:
valid-while:
updated: 20261018-0431-components-25ef

# The acceleration word: one slot per binding, three bottlenecks

## Current best

**The word is wired and the readout half is refuted on the shipped gates: no one-word per-window
stored acceleration, at either write point, can replace `partial`'s per-read mid-field evaluation (20261013-1249-second…, running
549f's checker-named experiment).** Both write points fail the frozen motion-law gates — the free
kick-written `a(B − len/2)` (across-boundary velocity jump 5.07×10⁻²) and the freshest
boundary-written `a(B)` at one extra field eval per step (3.85×10⁻² against the frozen 1×10⁻⁴;
map-ratio 356× against 3×): the gates freeze the readout's continuity across handovers, and a
window-constant word is a first-order quadrature that jumps at every boundary. What stands: the
deletion is worth 1.45× on the gather (25.9→17.1 µs/emitter scratch, 12.7→8.7 memo, interleaved
A/B; 1.69 readouts/body), the write amortizes ~500 reads per window on plain scenes, and digest
identity holds (the word rides kick records, which the digest never hashes). The stale-word
census fell: the free word is hours stale on the plane, err 8.3×10⁻⁵ ≈ 40% of the term. The
strong-field half stays untested, not refuted (the r = 20 M scene never clock-steps the ship;
checker2).

**20261018-0431-components-25ef (checker-corrected): the two-word (a, ȧ) as wired never runs.**
`Kick.word` is `None` on every binding: the backward-difference write in `step.rs` returns
`None` unless the *previous* binding's word is `Some`, and both seed sites (`Kick::NONE`,
`kick_clock`) write `None` — no first `Some` can exist, so every read falls through to the
shipped per-read evaluation. Measured: 0 of 162 binding reads armed (a history scan of the
gates' own scene), and the full readout-gate set plus checker probes at 2⁷→2³ kicks per period
and passes at 1.0–1.5 Hill radii print **digit-identical figures with `A_WORD=2` on and off**.
The run's gate numbers (1.11×, 15.9–18.3×, 5.29e-6) are the shipped path's; nothing about the
two-word was measured. The design (Taylor moments around the kick's own evaluation, slope by
backward difference) remains untested, one seed line away from measurable.

## Refuted

- "One stored acceleration word per binding replaces `observe::partial`'s per-read field
  evaluation" (549f, open direction 1): **refuted for every constant word** (20261013-1249-second…).
- "The two-word (a, ȧ) passes every frozen readout gate at 1.11×" (25ef's dossier and first wiki
  draft): **refuted as evidence** — the arm never engaged (`Kick.word` None on every binding, 0/162
  armed; ON/OFF digit-identical on every gate and probe), so the gates measured the shipped path
  (25ef's checker).
- "The stale error is 2.8×10⁻¹⁰/3×10⁻⁹" (549f's census): that priced `a(B)`, which no event
  writes in-flight on the plane; the free word is `a(B − len/2)` with windows of hours, measured
  err 8.3×10⁻⁵ ≈ 40% of the term (20261013-1249-second…).
- "At r ≲ 20 M the word's refresh cadence approaches one word per read" (549f's worry): not
  answered — the one strong-field scene built never runs a clock at all (`k.clock` false every
  frame, r = 20 and r = 4000 alike; checker2), so no refresh cadence exists to measure; the
  worry stays open (20261013-1249-second…, corrected by checker2).
- "The dive breaks the word at readout windows" (549f's own prediction): Δa/a max 3.0×10⁻²
  there, 0% of reads over 1 (20261013-1145-system-549f).
- "The plane's light-window staleness is negligible (≤ 10⁻⁶)" (549f's P3): measured median
  6.3×10⁻⁴, max 1.9×10⁻³ coast, 4.0×10⁻¹ at the dive's handoff, depth-growing (checker:
  8.0×10⁻¹ at β 0.49, 16 s) (20261013-1145-system-549f).

## Open directions

1. **The two-word (a, ȧ) completion**: untested, not refuted. The write is a wiring only with a
   **seed** (store `(a, 0)` on the first kick of a chain, or pay one field evaluation at the
   first rebind); the build must then instrument word coverage (a census of `Some`-word reads —
   25ef's missing control) before facing the gates, plus the adversarial domain the checker
   flew: steps down to 2³ kicks per period (ratio stays ≤ 1.9× on the shipped path) and passes
   at 1.0–1.5 Hill radii. Named edges that stay: (a) the **strong-field pole** — the r = 20 M
   scene must first be made to run a clock (a scene defect, checker2); (b) **the burn windows** —
   under thrust the clock re-plans at the thrust-limited step, so every window between flushes
   carries a one-kick-stale slope, and no frozen gate reads readout continuity under thrust;
   (c) **the width at 10⁹**: 4×f64 is a probe's width; the slope word wants its own quantum
   (memory-h-live).
2. **The word on the news payload, with thrust** (7ab4's r-news): total acceleration = field +
   the heading's analytic thrust; refresh at rebinds. Unaffected — the scar law
   (|ΔE| ≈ 0.7·β_c²/2·|δv|) judges versions, not readout continuity. Now the natural
   completion: the two-word covers the field half at read time, the heading's analytic thrust
   covers the burn half, and the per-read evaluation dies entirely.
3. **The quantized width at 10⁹** (memory-h-live): unchanged — no working build has carried a
   word at any width.

## Contradictions

None open. 7b86's "the slot buys the view nothing in this regime" and the refuted one-word
agree and sharpen. The strong-field pole is not measured — the r = 20 M scene never clock-steps
the ship, so "unreachable" there is a scene artifact, not a finding (checker2). 25ef's ON=OFF
gate identity was structural (a dead arm), not physical agreement — the same shape as the
5 October lesson that agreement between runs is not independence when they share a harness.

## Runs
- 20261013-1145-system-549f (silver): the three second-order consumers priced as one word — write free (step.rs:669), err/term ≤ 1.5×10⁻⁵ plain, sub-quantum on the dive, 10⁻³-stale across light windows.
- 20261013-1249-second-20261013-1145-system-549f-f2b7 (silver): the word wired: both constant-word write points fail the frozen readout gates (jump 3.85e-2 vs 1e-4); free word hours stale on the plane (err 8.3e-5); deletion worth 1.45× (checker2: the r=20M scene never clock-steps the ship; strong field untested).
- 20261018-0431-components-25ef (lead): the two-word as wired never arms — the write needs a previous `Some` word and no seed exists (checker: 0/162 bindings armed, ON/OFF digit-identical everywhere); the gates measured the shipped path.
