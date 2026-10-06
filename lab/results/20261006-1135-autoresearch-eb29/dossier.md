# Dossier — 20261006-1135-autoresearch-eb29 (lens: autoresearch)

**Claim.** The plane's kick resolver carries one redundant full decode per rebind — the
universe's `bind_in` discards `from_state`'s `Residual::between(decoded_event())` and
recomputes its own remainder — and deleting that decode cuts the kick's median cost 14%
(made) / 15% (leavers) with bit-identical outputs; the remaining cost is compile-bound
(85% quadrature), with a measured floor that no bit-identical micro-optimization can beat
by more than ~25%, so the next lever must be structural: lazy knot compilation.

**Bottleneck.** Board focus 1 / handoff item 3: "a kick costs 29 µs, 15 of them in
rebinding fit and compile — kicks dominate the engine's cost." Metric: µs per kick on the
plane's own deterministic replay bench (`xtask universe --kick-bench`). Expected gain here:
about 1.2× now, and the anatomy that says where the 10× lives. Cloud timings are orders of
magnitude only.

**Evidence.** See [evidence.md](evidence.md): three seeds, replay and state digests
bit-identical before/after, made median 36.6/36.5/36.7 → 31.5/31.5/31.5 µs, leavers
−15/16/15%; `cargo test -p emergent-space -p emergent-universe` 67/0/1; `behave --law plane`
verdicts numerically identical to the stashed baseline (the failures are main's known
state). Anatomy (per-kick means): rebind 82 µs = compile 60 + fit 4.2 + remainder 5.3 +
decode 4.0; compile = 85% `OrbitShape::append`/`quad`, ~55 EDGE bands (16 per octave), ~130
Gauss panels ≈ 520 `num::cos` (47.7 ns) + 520 `div_word` (18.0 ns) — cos+div alone ≈ 34 µs
of the 60 µs mean compile. Loop in [log.md](log.md): R1 kept, R2 (pre-sizing + hoisting)
measured zero and was reverted, R3 stopped at the measured primitive floor.

**Predictions.** [predictions.md](predictions.md), written before the held-out run.
Bit-identity: held (6/6 digests). Median gain −5–10% predicted, −14% observed (direction
right, magnitude better); leavers −3–6% predicted, −15% observed (the decode mattered more
on compile-heavy leavers); round decay and the <2% third round: held; ceiling: stands.

**What would make it wrong.** A caller of the universe `Binding` that needs the
space-crate `Rebinding.residual` semantics would find it zeroed — none exists today
(`bind_in` consumes only trajectory, periapsis time/angle and sense; verified by grep and
the tests), but the lean/full split must be re-checked if `bind_in` ever reads `fit.residual`.
The timing claims are single-box, shared-machine; medians were stable to ±0.2 µs across
runs, p99 has a ±8% band. M1 numbers will differ.

**Cost of adoption.** Two files, +15/−2 lines: `from_state_lean` beside `from_state`
(`crates/space/src/binding.rs`), one call switched in `crates/universe/src/bind.rs`. No law,
gate, digest or storage change. Fits "the cheapest compute is compute not done" (PRINCIPLES
1) and "no work for no reason" (14).

**The structural lever the lens asks for** (what would beat the best): compile only the psi
window a binding actually reads. A kick's binding lives ~1/64 of a radial period and its
readouts advance monotonically; lazy knot materialization (same `quad` calls, same sums,
same knots — just fewer of them, on demand) would cut the ~130 panels per compile to O(1–2)
per kick, a 10–100× on the compile term, bit-identical by construction. It needs interior
mutability on the `Arc<Entry>` shared across resolver threads and a policy for
`crossings`/`crossing_state` consumers (the encounters seam) — a design step, not a lab
afternoon. Second lever, law-level (not ours to take): the 16-bands-per-octave ladder sets
the node count; its density is a knots/readout contract question, judged by B-gates, not by
ns.

**The lens's blind spot.** A local search over bit-identical edits finds local optima; the
deep alternative (lazy compilation) was designed but not built, so the 10× claim is
argument plus anatomy, not a measurement. I also did not re-run B10 on a quiet machine
(handoff says it flakes under load); its verdict was identical between builds anyway.
