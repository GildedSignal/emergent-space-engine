# dossier.md — 20261017-1447-components-5eb2 (lens: first principles, one component at a time)

**Claim.** The belt kick's 46-52 µs is priced from the inside on shipped main for the first
time: the fit is 45-59% of it but the quadrature (`Orbit::compile`) is only ~a quarter of the
fit — the fit's own mass is decode-class work — and the per-event `Ctx::secondaries` rebuild,
which read-stream's open direction 1 wants to delete, is measured **2.66×-7.81× redundant at
its `(doll, tick)` key** (64-89% of all calls share a tick), so the shared field read is real
but buys only ~8-10% off the kick, not the 23 µs the 10⁹ ledger requires.

**Bottleneck.** The board's kick row (75-160 µs vs ~50 ns floor on the M1; 46-52 µs on this
x86). The page's own pointer ("the belt kick's cost lever is the bind/refit (84-89%, b063)")
had never been decomposed in wall time; read-stream's lever (delete the per-event sources
rebuild) had never been sized. This run decomposes both and prices the one lever it can
measure end to end.

**Evidence** (Linux/x86, shared 8-vCPU box, orders of magnitude; instrument = print-only
nested prof stages `READOUT`/`SECONDARIES` + a `(doll, tick)` census in `Ctx::secondaries`,
`ladder_digest` N=3000 all five cases **bit-identical** with the patch, prof off; regen.sh
reproduces everything in ~6 min):

- Main arm `refit_probe 30000 30 600` (17,989 game-s, 89,923 events, 3 sources in doll 0):
  kick clock item **46.3 µs/call**; `bind_surface` (FIT) **20.9 µs/call** at 1.00 calls per
  kick; `secondaries` **6.25 µs/call** (48.4 calls/frame ≈ 0.97/event); `readout`
  **3.77 µs/call** (372 calls/frame). Held-out arm `10000 20 1800`: kick **51.6-52.9 µs**,
  FIT **30.4 µs**, secondaries 5.35 µs, readout 4.84 µs (743 calls/frame). Re-runs move the
  stage timings ≤ 5% and the main arm's census to the digit (84,254/31,652 again).
- The census (the number read-stream's direction 1 was missing): main arm **84,254 calls at
  31,652 distinct (doll, tick) keys = 2.66× redundancy, 63.9% of calls at multiplicity ≥ 2,
  62.6% at ≥ 8, 42% at ≥ 64**; held-out arm (deeper into the first crest) **101-108k calls at
  12.9-13.1k keys = 7.8-8.2×, 89-90% at ≥ 2, 87.8-88.6% at ≥ 8** (two runs; the window's
  crest mass moves a few % with delivery). The budget-sliced drain does NOT batch
  events at shared ticks — the ticks are already shared and every event re-reads them.
- The fit at its true inputs: `Rebinding::from_state` on 512 real flown belt states =
  **17.3 µs/call** (main arm) / **28.0 µs** (held-out arm), against `Orbit::compile` on
  synthetic belt-class keys (q = 2⁻²⁰⁻³⁰, e ≤ 0.33) = **4.4 µs median** (3.2-6.6, 6-10
  knots). So the quadrature is ~26% of the fit; the other ~13 µs sits in `at_radius`,
  `decoded_event`/residual and `word_for` [INFERENCE by subtraction, not separately timed —
  the named next probe]. `fit_key` itself is ~30-50 Scalar ops (~0.5 µs by inspection).
- The kick's arithmetic floor ladder: one wide `u128 / u128` division = **22.4 ns** vs the
  law's own exact `div_word` (num.rs, unit-tested "any faster implementation must return the
  same bits") = **2.8 ns — 8×**. The belt's compile path is `weak_quad`, which already uses
  `div_word`; the strong-field `fast_quad` still pays **four wide divisions per node**
  (`orbit.rs:429-433`) where `div_word`'s precondition holds — a found, measured, unadopted
  bit-identical lever for strong-field compiles (worth ~4×14 ns/node there; the belt is
  unaffected).

**Predictions** (predictions.md, written before the flights): P2 held and overshot (the ≥ 8
multiplicity tail is 62.6-87.8%, not ≥ 5%; the "steady flight is mostly alone at its tick"
half was wrong — the belt's two-comb train concentrates the stream even pre-crest at rtf
600). P1 half-wrong: secondaries is 13.5% of the kick, not ≥ 35%; the fit is the largest
term (45-59%) but not b063's 84-89%. P3 wrong low: real-state bind is 17.3-28.0 µs, above
my 8-15 µs. Held-out arm (N=10⁴, rtf 1800) confirms every direction.

**What would make it wrong.** The decomposition is only as good as the nesting: FIT nests in
the kick item, READOUT nests in both, so shares are read against the parent (prof.rs's rule);
a stage attributed elsewhere (the view's scans, the walk) would move the kick's "remainder"
(~29%, force algebra + ext + quantize + inserts), not its ranking. The census counts calls,
not µs: sharing deletes (calls − keys)/calls of the secondaries term only if the cache
invalidation (a source rebinding between two events at the same tick) is rare — plausible
(sources rebind on their own slow combs) but unmeasured. Cloud timing caveat: x86 numbers,
orders of magnitude; the M1 re-measures.

**Cost of adopting.** The `(doll, tick)` field cache is a pure compute memo on a pure
function — bit-identical by construction, invalidated when a source of `d` rebinds; it is
~30 lines in `Ctx` and deletes 62-89% of secondaries calls (≈ 8-10% of the belt kick, more
of the frame's read stream: readout is 372-743 calls/frame). The `div_word` swap in
`fast_quad` is 4 lines guarded by the precondition (fall back to the wide division), exact
by the primitive's own contract. Neither touches the law's outcomes; both are one step.

**Fit with PRINCIPLES.** "the cheapest compute is compute not done" (#1): the same field
read done 2.66-7.81× per tick is compute not done; "Compute only surprises" (#3) — a
redundant re-read of an unchanged source state is not a surprise. The deeper finding is
representation-shaped: the kick's floor is not paid in quadrature (the compiled generator is
cheap) but in *decodes* — `at_radius`/`readout` at 3.8-4.8 µs each against a ~0.1-0.3 µs
arithmetic floor — which is the same term the read-stream census found by call count; here
it is priced in time.

**The lens.** A component lens prices one thing and can mis-attribute its neighbours by
subtraction (the fit's 13 µs "decode-class" remainder is inferred, not directly timed; the
kick's 29% remainder is unnamed). The next run should time `at_radius` and `decoded_event`
directly and try the one-line version: `Trajectory::at_radius` is a binary search over the
same knots `state()` walks — if its repeated `state()` calls dominate the fit, the refit's
lever is a smarter search, not a cheaper quadrature.

## Commands
- `cargo run --release -p emergent-universe --features prof --example refit_probe -- 30000 30 600`
- `cargo run --release -p emergent-universe --features prof --example refit_probe -- 10000 20 1800`
- `cargo run --release -p emergent-space --example kickfloor`
- Parity: `cargo run --release -p emergent-universe --example ladder_digest -- "N=3000"` before/after `git apply work/patch.diff`.
