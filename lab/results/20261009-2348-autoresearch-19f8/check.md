# check.md — independent check of 20261009-2348-autoresearch-19f8

Grade: silver

**Abstract.** Claim: the plane's per-kick rebind (`Rebinding::from_state`, ~14 µs p50 here) is at its bit-identical local floor; the next 10× must come from fewer rebinds or warm-started quadrature. Reproduced: digests exact (tune `fd33f759b10e569f`, held-out `c45b567dfc5b395c`, plus an extreme corpus of my own, `57a2c0d885335b22`); KEPT gain 0.8–2% vs claimed ~0.7%; phase split 46.5/26.3/8.5/18.6 vs quoted 47/25/9/19; my independent E4 re-implementation changed the tune digest and failed `witnessed_fit_keeps_the_full_search_key…`, confirming the kill. Tests green (space 50/50; universe 0 failures). Gain: none measurable — a confirmed ~1% ceiling, i.e. the board's cadence conclusion with numbers; the patch is free hygiene. Gap: quoted op counts do not regenerate (below).

## Reproduction (clean tree, both patches applied by me)

- BASE digests: tune `fd33f759b10e569f`, held-out `c45b567dfc5b395c` — exact match. KEPT (`work/patch.diff`): identical digests on both. Timings same order under shared load (load 1.4–2.6): BASE p50 14327 ns, KEPT 14207 ns (0.8%); p99 noise (64358 vs 64074). Held-out/tune p50 ratio 1.11 (dossier 1.11; prediction ≤1.2 held).
- Attribution build (`instrumented-attribution.diff`, `--features profile`): phases fit/compile/orient/residual = 6941/12273/2251/4910 ns → 26.3/46.5/8.5/18.6% (quoted 25/47/9/19 ✓); counts iter 84.0, skip 29.7, mul 354, div 61, add 450, isqrt 34.9, divw 104.5.
- Suites: `emergent-space` 50/50 ✓; `emergent-universe` 0 failures (I count 54 passed + 1 ignored across targets, not 37 — count label off, everything green).
- Machine: shared Linux x86, 8 vCPU, load 2.1–2.6, 1.8 GB/15 GB used.

## Predictions

All four held. `predictions.md` (00:10:37) predates the final run (log 00:14:13): digests unchanged ✓; 1–3% p50, p99 noise ✓ (0.8%); held-out within ×1.2 ✓ (1.11); E4 not bit-identical ✓ (reproduced below). Caveat: `bench/src/main.rs` mtime 00:11:22, 45 s after predictions — the corpus freeze before predictions is asserted, not provable from mtimes; mitigated because the predicted digests then reproduced exactly, which a post-hoc corpus retune would be unlikely to preserve.

## Adversarial cases (mine)

1. **E4 re-implemented from scratch** (witness-tightened bracket `lo,hi = a,b`): tune digest changed to `cd362cc1024c16fc` and `witnessed_fit_keeps_the_full_search_key_at_kicks_and_boundaries` fails — the kill is real and its control works. Two nuances the author did not state: the held-out digest is *unchanged* under E4 (the kill's bite is corpus-dependent — it lives on the tune set), and E4 buys only ~6% at p50 (the witness already skips the poly cost; tightening saves mostly cheap midpoint steps), so killing it cost nothing measurable.
2. **Extreme corpus** (radius exps {2,7,33,90,150}, e ∈ {(1<<48)−1, 0, ⅓·2^48, 1}, kick quantum 8192, fresh seed; 1920 states, all Ok): BASE and KEPT digests identical (`57a2c0d885335b22`); interleaved on a quiet machine KEPT is ~1.6% faster at p50. Bit-identity and the gain's direction hold beyond both corpora. (A first contaminated run showed a 30% swing while another test suite churned — shared-machine numbers are orders of magnitude only, as the cloud rule says.)
3. **Op-count regeneration:** the shipped instrumented build does **not** regenerate the quoted counts on either shipped corpus — measured 61 div / 34.9 isqrt / 354 mul / 450 add / 84 iter per call on tune (61/20.9/349/440/84 on held-out) vs quoted 54/31/317/404/76. Same order, no conclusion changes, but this is exactly the "numbers the shipped code cannot regenerate" defect the taste log flags (5 October), likely quoted from a pre-final `main.rs` revision.

## Novelty

No HISTORY entry measures or optimizes `Rebinding::from_state`. H0210 notes "kicks cost 29 µs" (whole path) and queued "kick cost (Sol)"; `components-4643` (6 Oct) measured the window tier, a different artifact. The phase/op floor map and the E4 sequence-semantics finding are new. But the run's conclusion — cadence is the lever, cheaper events are not — *confirms* the board's standing conclusion (focus list; components-4643's "ceiling 1.1–1.2×") rather than overturning a live premise.

## Goal fit

Real bottleneck (board #1/#3: kicks dominate). Honest negative with a map; the patch is two bit-identical dedupes, adoptable at nil cost. PRINCIPLES fit is genuine: E4's kill is P2's "error type over error size" made concrete — the root's low bits are *defined* by the midpoint sequence, so "same math" was not the same integer; the digest and the witnessed test both failed when they should have ("a test that cannot fail is a control" honored in both directions).

## Why silver, not gold

Reproduced and honest, but it moves no bottleneck 10×, deletes no component, and kills no live premise: the board already ranks cadence above cheaper per-kick work, and the measured ~1% ceiling matches what components-4643 already found on the sibling artifact. Add the op-count regeneration gap (adversarial case 3) and this sits one experiment short.

**The experiment that would make it gold:** the floor map points at the compile phase (47%) and the taste log says the plane recompiles on ~99% of kicks — so test a *bit-identical warm start* of `OrbitShape`'s quadrature across consecutive kicks of the same body (prove refinement-invariance or show none exists). Either branch upgrades: reuse that keeps the digest deletes the recompile (a component, ~2× per call, and the certificate for the 99% number), or a proof that sequence semantics forbid it converts this run's floor claim into a demonstrated premise kill.

## What the author missed

- The quoted op counts are not regenerable by the shipped code (case 3); regenerate-ability is the lab's explicit bar.
- E4's digest change is corpus-dependent (tune only, not held-out); the prediction should have said where the kill bites.
- "Universe 37/37" does not match what `cargo test -p emergent-universe` runs here (54+1 ignored, all green).
- "~half the call is the division chain" is an inference from op counts plus E1's null result, never isolated by a measurement (e.g. timing a division-free variant); defensible as an order of magnitude, and E1 itself I did not re-verify (reverted, not part of the deliverable).
- The M1 caveat is correctly flagged but the run's headline ("at its floor") is this x86 machine's floor; the integrator should not quote it before the ARM64 re-measure.
