Grade: silver

**Abstract.** Claim: a 17-line patch to `crates/space/src/orbit.rs` (guarded word division replacing the four u128 hardware divisions per `fast_quad` node, plus a `node()` cos dedup) makes the per-kick orbit recompile cheaper, bit-identically. Reproduced: digests `b3b2412da6e85f12`/`1c32d7508ad8ef47` identical baseline-vs-patched on both corpora; my 675-state adversarial corpus (r=1..2^45, e≤0.97, unbound, 392 refused) digests identical; 50/50 tests green. Timing: patched medians match the author exactly (39.7/43.7 µs), but my quieter baselines (42.3/43.9 µs vs their 47.1/49.8) give −6.6% tuning median (5/5 interleaved pairs), −4.3% heldout mean, −0.5% heldout median — not 12–16%. Real, ~1.05× overall, adoptable at zero risk in minutes; re-measure on the M1.

## Reasons

**Reproduction** (clean tree, `git apply work/patch.diff`, interleaved A/B, `taskset -c 3`, load 1.17):
- Digests match the dossier and each other on `tuning` (72 states) and `heldout` (64), baseline vs patched, 3 rounds each. Bit-identity reproduced.
- `cargo test --release -p emergent-space`: 50 passed, 0 failed. Reproduced.
- Timing: patched 39.6–39.9 µs (tuning), 43.6–43.8 µs (heldout) — equals the author's finals. Baselines: 42.2–43.2 µs (tuning), 43.8–46.0 µs (heldout) — 10–13% faster than the author's. Tuning gain −6.6% in 5/5 alternating pairs with non-overlapping ranges; p90 improves −6.3%/−5.1%. Heldout median gain −0.5% (noise-level); mean −4.3%. The claimed 12–16% did not reproduce in magnitude; direction and patched endpoint did.

**Correctness attack.** Adversarial corpus (my own harness, author's digest function): 15 radii 1..2^45 M × e {0, 0.05, 0.9, 0.95, 0.97} × speed × {0.4, 1.0, 1.5} (1.5 ⇒ unbound passages) × 3 phases = 675 states. Digest `e5da649882517498` identical, ok/err counts identical (283/392). Code-level: `wdiv` is exact whenever divisors are < 2^64 — root ≤ ~2^62.5, x ≤ ONE (Q62), horizon, ONE+root all positive-checked at the call sites; `div_word`'s precondition (`n>>64 < d`) is checked verbatim by the guard; the `n/d` fallback is the original expression. R1's reuse is the identical expression (`x(psi)` is literally `self.k + product(ONE - self.k, cos(psi))`, orbit.rs:238). No correctness surface found.

**Predictions.** `predictions.md` (mtime 20 min) predates `patch.diff` (3 min) and the dossier; ordering consistent with pre-registration. Digests/tests/held-out-within-±30% held (their numbers); cumulative-band miss and H1/H2 misses honestly reported. Not held: the headline magnitude itself is window-fragile (below).

**Novelty.** Nearest prior: 1932f6c "cheaper kicks, exactly" (adopted; kick median 25.75→23.71 µs) — same lane, different mechanism (normalized products, root-gap fit). `wdiv` does not exist in HEAD's orbit.rs (verified pre-patch source). No H entry claims it. New, incremental, composes with the prior commit.

**Goal fit.** Board item 1 (kicks dominate the engine's cost); PRINCIPLES §1 "the cheapest compute is compute not done" and "Floats may explore; only integers decide canonical outcomes" — every quotient identical by construction. Not a 10× move, deletes nothing, kills no premise: not gold, by the author's own assessment too.

**Why silver, not lead.** The artifact is real, regenerable from the shipped patch, bit-identical under adversarial input, free to adopt, and directionally faster in every measurement I took. Why not gold: constant factor, and the 16% headline overstates the reproducible gain ~2.5×.

## The one experiment

Gold from this lane is not a re-measurement — it is the author's own lens note: compile is a pure function and kicks are independent across bodies, so cross-kick parallelism (threads the plane already has) is the ~4–8× on this cost line. If the integrator wants a measurement first: same interleaved A/B on the M1, where u128 division costs differ and the gain must be re-derived, not assumed.

## What the author missed

1. **The baseline is the unstable side.** They disclosed load compressing the gain to −2% and framed the quiet-window −16% as "the number the player sees." My quieter window halves the tuning gain and erases the heldout median gain: their baseline (47.1/49.8 µs) was inflated ~10–13% by window state while the patched endpoint reproduced exactly. The favorable headline is partly the baseline's artifact — the same trap the taste log flags (agreement between runs is not independence when they share a window).
2. **Heldout median as headline.** The heldout gain lives in the tail (p90 −3.5–5%), not the median; the median state barely benefits. Quoting −12.3% median masked the regime mix.
3. **R1's −10.7% is unearned** — `node()` runs on neither corpus; the author says so, keeps the number in the log anyway, and keeps the change on a strictly-less-work argument. Fine to adopt; the log entry misleads.
