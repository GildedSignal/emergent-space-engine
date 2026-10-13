topic: a-word
status: open
closed-by:
valid-while:
updated: 20261013-1249-second-20261013-1145-system-549f-f2b7

# The acceleration word: one slot per binding, three bottlenecks

## Current best

**The word is wired and the readout half is refuted on the shipped gates: no one-word per-window
stored acceleration, at either write point, can replace `partial`'s per-read mid-field evaluation (20261013-1249-second…, running
549f's checker-named experiment).** Both write points fail the frozen motion-law gates — the free
kick-written `a(B − len/2)` (across-boundary velocity jump 5.07×10⁻²) and the freshest
boundary-written `a(B)` at one extra field eval per step (3.85×10⁻² against the frozen 1×10⁻⁴;
map-ratio 356× against 3×): the gates freeze the readout's continuity across handovers, and a
window-constant word is a first-order quadrature that jumps at every boundary — the mid evaluation
is load-bearing, not re-derivation. The census's magnitude model also falls: on the plane the
windows are 7.7 h and no boundary event fires in an 8-s flight, so the only free word is hours
stale — measured error 8.3×10⁻⁵ doll units ≈ 40% of the term it replaces (10⁴× the census's
3×10⁻⁹, which priced an unwritable word); the probe's control build on the pristine tree reads
exactly 0. What stands: the deletion is worth 1.45× on the gather (25.9→17.1 µs/emitter scratch,
12.7→8.7 memo, interleaved A/B; 1.69 readouts/body), the write amortizes ~500 reads per window on
plain scenes, and digest identity holds bit for bit on every scene — the word rides kick records,
which the digest never hashes (checker2 extended the control to the strong-field scene: both
digests identical on the pristine tree). The strong-field half does not stand as written: the
r = 20 M scene (a 2⁻⁴-solar doll with a 1-M surface, β_circ 0.224, 4.35 M events in 1.42 orbits)
never clock-steps the ship at any radius — checker2's diagnostic reads `k.clock` false at every
frame, at r = 4000 M as well — so the 0 gated reads never reach the read gate and neither word
nor per-read term is shown anything there: the strong-field readout stays untested, not refuted
(checker2).

## Refuted

- "One stored acceleration word per binding replaces `observe::partial`'s per-read field
  evaluation" (549f, open direction 1): both the free word and the freshest boundary word fail the
  three frozen readout gates of `tests/motion.rs` (20261013-1249-second…).
- "The stale error is 2.8×10⁻¹⁰/3×10⁻⁹" (549f's census): that priced `a(B)`, which no event
  writes in-flight on the plane; the free word is `a(B − len/2)` with windows of hours, measured
  err 8.3×10⁻⁵ ≈ 40% of the term (20261013-1249-second…).
- "At r ≲ 20 M the word's refresh cadence approaches one word per read" (549f's worry): not
  answered — the one strong-field scene built never runs a clock at all (`k.clock` false every
  frame, r = 20 and r = 4000 alike; checker2's diagnostic), so no refresh cadence exists to
  measure; the worry stays open (20261013-1249-second…, corrected by checker2).
- "The dive breaks the word at readout windows" (549f's own prediction): Δa/a
  max 3.0×10⁻² there, 0% of reads over 1 (20261013-1145-system-549f).
- "The plane's light-window staleness is negligible (≤ 10⁻⁶)" (549f's P3):
  measured median 6.3×10⁻⁴, max 1.9×10⁻³ coast, 4.0×10⁻¹ at the dive's handoff,
  depth-growing (checker: 8.0×10⁻¹ at β 0.49, 16 s) (20261013-1145-system-549f).

## Open directions

1. **The two-word (a, ȧ) completion**: the only stored form second order at the handover by
   construction (≈2 multiply-adds more at the read; the write needs the field's derivative, which
   the kick does not compute — a real law change, not a wiring). The measured 1.45× deletion price
   and ~500 reads/window amortization transfer to it.
2. **The word on the news payload, with thrust** (7ab4's r-news): total acceleration = field +
   the heading's analytic thrust; refresh at rebinds. Unaffected by this refutation — the scar law
   (|ΔE| ≈ 0.7·β_c²/2·|δv|) judges versions, not readout continuity.
3. **The quantized width at 10⁹** (memory-h-live): unchanged — this run wired 2×i64 + i16 per
   kick record and the gates never saw it.

## Contradictions

None open. 7b86's "the slot buys the view nothing in this regime" and this run agree and sharpen:
the slot buys the view nothing where the term is invisible (plain scenes); the strong-field pole is
not measured — the r = 20 M scene never clock-steps the ship, so "unreachable" there is a scene
artifact, not a finding (checker2). The middle (gated reads with a visible term) is unmeasured.
The 1.45× is the per-read evaluation's price, collectible only by a passing variant.

## Runs
- 20261013-1145-system-549f (pending grade): the three second-order consumers priced as one word — write free (step.rs:669), err/term ≤ 1.5×10⁻⁵ plain, sub-quantum on the dive, 10⁻³-stale across light windows.
- 20261013-1145-system-549f (silver): the three second-order consumers priced as one word — write free (step.rs:669), err/term ≤ 1.5×10⁻⁵ plain, sub-quantum on the dive, 10⁻³-stale across light windows.
- 20261013-1249-second-20261013-1145-system-549f-f2b7 (pending grade): the word wired: both write points fail the frozen readout gates (jump 3.85e-2 vs 1e-4); free word hours stale on the plane (err 8.3e-5); deletion worth 1.45× (checker2: the r=20M scene never clock-steps the ship; strong field untested).
