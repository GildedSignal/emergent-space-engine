Grade: gold

**Abstract.** Reproduced; two premises of the shipped plane fall. Its presented frame pays an
O(N) rekey tax with zero events resolved — 43–85 ns/body, linear to 10⁶ bodies (my probe:
84.7 ms/frame, 5× the 16.7 ms budget; the author's extrapolation is conservative), and no body
class escapes it (inert and 3–6 AU controls pay the same). The kick is 70.7 % rebind, 2.7 %
force arithmetic, 11× p99.9 tail — so the levers are rebind slimming and lazy deadline
re-keying (one local change; digest-identity control demonstrated), not cheaper force math or
more splits. Controls: bit-identical digest pristine vs instrumented, 11/11 suites both, belt
arithmetic (≈39 µs/event budget vs ≈35 µs ship item). Predictions 1,2,5,6,8 held; 3,7 failed,
disclosed, and sharpen the claims.

**Reasons.**

*Reproduction (clean tree, patch applied by me).* `kick_budget` twice (load 1.96 and 1.20) and
`digest_control` on pristine sources: items 49,619 (kicks 24,827, opens 198, boundaries 24,594,
lost 4, refused 0) and digest `e317b268…a5be` identical in all three, author's numbers included.
Stage shares bit-stable across every run: readout 8.5 %, inputs 17.5 %, force 2.5 %, quantize
0.2 %, rebind 70.7 %; kick total ≈41.3 µs; Kick(0) p99.9/p50 = 11.2×; Kick(1)/(2) ≈413 µs
(n=216); apply 7.5 µs/item with root_state 97.0 %; classes planet 21.7 / moon 34.1 / ship 35.5 /
player 150.0 / fleet 66.6 µs. Phase B at load 1.20 matches the author's row almost exactly
(256k: 15.32 ms vs 15.39 ms, 59.8 vs 60.4 ns/body); events resolved 0 in every row. `cargo
test --release -p emergent-universe`: 11 suites, all pass, pristine and instrumented. The
pilot the predictions quote regenerates on the pre-existing `cost_split` (49.9 / 34.8 / 3.32 /
3.32 / 3.28 / 6.82 µs vs predicted ~50 / ~35 / 3.3 / 3.3 / 3.3 / 6.8).

*Adversarial cases (mine, wall-clock only, pristine sources).*
1. **10⁶ planned bodies** (the headline extrapolation, unmeasured by the author): frame p50
   84.7 ms = 84.7 ns/body; 512k = 85.3, 256k = 85.0 — linear, no cache bend; 5× over the 16.7 ms
   budget with zero events. Peak RSS 1.93 GB, inside the limit.
2. **Far belt (3–6 AU, not near-Home)**: 76.4 ns/body at 64k, 84.6 at 256k — the tax is
   position-independent; "no body class escapes" holds where the author never probed.
3. **Load swing** (same binary, load 1.20 → 1.92): 59.8 → 85.0 ns/body at 256k. The slope moves
   ±40 % with machine state; the O(N) shape and the over-budget verdict are invariant (even 43
   ns/body gives 43 ms at 10⁶). Structural check: `advance` calls `rekey` unconditionally
   (universe.rs:818–821); `rekey` loops all bodies and requeues each through the calendar's
   heap sift (`Calendar::set` → up/down), so the mechanism is as claimed.

*Predictions.* Pre-registration is credible: mtime order (predictions 19 min before the
session-end artifacts), pilot quotes match `cost_split` exactly, ranges bracket outcomes
rather than fit them, and two misses are disclosed as misses. 1, 2, 5, 6, 8 held; 3 failed
(tail 11× vs ≤5×) and 7 failed (inert bodies pay full price: root-doll ships are planned
because the planets are root-doll sources — the "inert" control was not inert, which the
dossier diagnoses correctly). Both failures strengthen the claims (the tail is worse; the tax
is broader). Neither pre-stated kill criterion triggered. Past silvers lost the grade on
honesty failures (missing predictions.md, undisclosed redefinitions); this run has none.

*Novelty.* No prior measurement of the per-frame rekey tax or of the kick's stage-level
distribution exists in HISTORY, docs or examples. The plane freeze (H3102) measured frame p99
2.45 ms at the default ~28 bodies; `cost_split.rs` is mean-level on one body's record; the
taste log knew the recompile's *frequency* (~99 % of kicks), not its *price* or tail. plane.md
foundation 7's "Nothing takes an unbounded synchronous claim on the frame" is quoted verbatim
and verified.

*Goal fit and premise breaks.* Two premises fall, both on the shipped path: (a) the presented
frame is not bounded at scale — the scheduler itself is an O(N) synchronous claim, 4–5× over
budget at 10⁶ bodies with zero work done (board #4, foundation 7); (b) the kick's price is
bookkeeping, not physics — force 2.7 % kills "cheaper force math / more splits" as the lever
and redirects board #1 to rebind slimming, quantifying the existing memo direction. Belt
arithmetic verified: 10⁹ × 32 kicks / 3.16e7 s / rtf 100 / 60 Hz = 1.7e3 events/frame, 4 cores
→ 39 µs/event against a 35.5 µs ship item. PRINCIPLES #14 ("no work for no reason") and #3
("Nothing is evolved that can be derived when looked at"): N heuristic deadlines recomputed
per frame is exactly that; #12 names the allocator as the most important algorithm, and the
tax is its overhead. Adoption is one local change (amortized rekey, drift ≤ 2c·Δt), with this
run's digest-identity control as its test.

**What the author missed.**
- Mixed provenance in Phase A: the dossier's Kick(0) percentiles (34.0 / 379 / 544 µs) and
  rebind (26.8 µs) come from a lighter-load run whose full output was not saved; the saved
  artifact and my runs give 37.7 / 421–424 / 580 and 29.2–29.4 µs. Shares, counts and ratios
  are identical, so no claim moves, but the quoted absolutes are not the saved artifact's.
- The ≥10³× deletion (60 ms → sub-µs) is extrapolated, not built: no lazy-rekey measurement
  exists, and the deadline-density spike case (fleet arrival, all deadlines near the heap min)
  is untested — the author names both.
- The 11× tail's internal stage is unresolved (sum accumulators only); a per-event stage trace
  is the named next probe, and the level-1/2 kicks' flat ~413 µs (the SyMBA changeover path)
  deserves its own decomposition.
- The slope's load sensitivity is understated: the dossier says 43–60 ns/body; the same binary
  swings to 85 under load on this shared runner. Immaterial to the verdict, but the M1
  re-measurement should record load, per PRINCIPLES.
- "Physics inputs 28 %" is 26.0 % in the artifact (readout 8.5 + inputs 17.5); trivial, noted
  for exactness.

**For the integrator:** adopt the diagnosis (levers = rebind + lazy rekey; force math and
splits are dead ends at 2.7 %), and queue the one-step build this run specifies — amortized
rekey with digest identity as the gate, plus a deadline-spike capacity case. That build is
what converts the 10³× from arithmetic to measurement.
