# dossier.md — autoresearch: the per-kick compile is at its bit-identical floor

**Claim.** The plane's per-kick rebind (`Rebinding::from_state` in `crates/space`) cannot be made materially cheaper by local, bit-identical change: five measured rounds bottom out at ~0.7% (noise); ~half the call is an exact wide-division chain that integer semantics forbid shortcutting, and the fit's 76-iteration bisection is definitional (its midpoint sequence *is* the rounded root), so the next 10× must come from fewer rebinds or warm-started quadrature, not faster ones.

**Bottleneck.** Board #1/#3: "kicks dominate the engine's cost"; the taste log: the plane recompiles an orbit on ~99% of kicks. Expected gain from cheaper events at 10⁹ bodies: any 10× here is a 10× off the 190-core estimate. Measured instead: the ceiling for *local* wins is ≈1%, which deletes nothing — so the lever stays cadence, confirming the board's standing conclusion with numbers.

**Evidence.** Baseline on a fixed deterministic corpus of 4608 kicked states (tune) + 1440 held-out, Linux x86-64 (shared, load 1.4–2.1; orders of magnitude only):
- ns per rebind: p50 ≈ 13 µs, p99 ≈ 58 µs (tune); held-out p50 ≈ 14–15 µs. Phase split (feature-gated timers): compile ≈ 47%, fit ≈ 25%, orient ≈ 9%, residual ≈ 19%. Per call: ≈54 `Scalar::div` + 31 `isqrt` ≈ 94 wide divisions, 317 `mul`, 404 `add`, bisection ≈ 76 iterations.
- Rounds (hypothesis → verdict): isqrt division via `div_word` → exact but 1.00× (reverted); `Scalar::add` fast path → noise (reverted); `poly`'s duplicate `z·z` → kept; **witness-tightened bisection start → KILLED by its own control** (digest changed; `witnessed_fit_keeps_the_full_search_key_at_kicks_and_boundaries` failed — the rounded cubic is non-monotone at fine scale, so tightening the bracket lands on a different dyadic root); duplicate `cos ψ` in `node()` → kept.
- Final interleaved A/B under identical load: BASE p50 13071 ns vs KEPT 12982 ns (≈0.7%). Digests identical to baseline on both sets (`fd33f759b10e569f`, `c45b567dfc5b395c`); `emergent-space` 50/50 and `emergent-universe` 37/37 green.

Reproduce (each ≤ 60 s once built; build ≈ 10 s):
```
cd lab/results/20261009-2348-autoresearch-19f8/bench
cargo build --release && ./target/release/rebind-bench tune 3   # KEPT (tree as left)
./target/release/rebind-bench heldout 3
# BASE (pristine HEAD), interleaved with KEPT under the same load — see work/README.md:
cd ../../.. && git checkout HEAD -- crates/space
cd lab/results/20261009-2348-autoresearch-19f8/bench && cargo build --release && ./target/release/rebind-bench tune 3
cd ../../.. && git apply lab/results/20261009-2348-autoresearch-19f8/work/patch.diff   # restore KEPT
# attribution (from HEAD): git apply .../work/instrumented-attribution.diff,
# then in bench/: cargo run --release --features profile -- tune 3
```

**Predictions.** `predictions.md` was written before the final run: digest unchanged on both sets ✓; gain 1–3% at p50, noise at p99 ✓ (0.7% measured); held-out within ×1.2 of tune ✓ (p50 14140 vs 12741 = ×1.11); E4 not bit-identical if re-applied ✓ (that is what killed it). All four held.

**What would make it wrong.** On the M1 (ARM64, no 128/64 divide) the division floor may sit elsewhere: `div_word` vs `__udivti3` could differ by more there, and the i128 multiply/add costs differ — the ~1% ceiling is this machine's, so the integrator should re-measure before quoting it. A proof that the *rounded* poly's sign pattern admits a certified tighter bracket (making E4 bit-identical) would also reopen the fit phase. Cost of adopting the patch: nil (two expression dedupes, bit-identical, tests green); it is offered as hygiene, not as a gain.

**Fit with PRINCIPLES.** "The cheapest compute is compute not done" (P1) — the two kept changes delete duplicate exact expressions; the killed E4 is exactly P2's "error type over error size": the answer's low bits are *defined* by the search sequence, so "the same math" was not the same integer. "A test that cannot fail is a control" — the bit-digest and the existing witnessed-fit test both failed when they should have.

**Lens (autoresearch) blind spot.** A local search over one artifact finds local optima; the loop's real output is the floor map (divisions ≈ 50%, sequence-semantic bisection, fixed quadrature), which points the next run at structure: cadence of rebinds per orbit (board's queue), or a bit-identical warm start for `OrbitShape` across kicks of the same body — neither reachable from inside this loop.
