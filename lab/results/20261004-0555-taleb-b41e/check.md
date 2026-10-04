Grade: silver

**Abstract.** Claim: the plane's keyless `Catalogue` recompiles a fresh trajectory on 98.6% of rebinds; keying it by the law's 12-bit memo quantum would hit 95.25% of them, bit-identically (300/300, residual ≤ 52 bits vs the documented 65), capping memory at distinct keys (~848 B/entry ⇒ ~850 GB unshared at 10⁹ bodies). Reproduced exactly: every integer metric identical (29402/28997/1398/0.9525/300/52/848 B); tests pass, patches change no behaviour; compile work drops 21×. Adversarial: hit rate 0.9485–0.9584 across seeds 1/3/7, members 96/1024, 3600 frames (keys grow sublinearly); memo-key period shift median 1.0e-4, max 5.0e-4 — inside B2's 0.1% band, little margin. Adoption cost: one crate change plus re-freezing B1/B2/B9. Not gold: behaviour gates unrun on memo keys, and the kick-path saving is ~9% on this box (fit dominates).

## Reproduction

Clean tree, `git apply work/patch.diff`, then the dossier's commands:

- `memo_probe 1024 1800` → identical on every integer/count metric: rebinds=29402, distinct_exact=28997 (98.6%), distinct_memo12=1398, quantize errors 0, hitrate 0.9525, top multiplicities [152,146,…], bit-identical 300/300, max residual 52 bits, catalogue_live 1052, entry 184+664=848 B, kicks_sampled 365, refused 0. Timings within noise (kick median 26.16 vs 26.21 µs; load 2.02 vs the author's 0.53).
- `memo_probe 256 60` smoke → 782/767/243, hitrate 0.6893, 30/30 — matches predictions.md's bracketed smoke values.
- `cargo test --release -p emergent-universe` → all suites ok (18 passed, 1 ignored), rc=0. The observer (`REBIND_KEYS`) is write-only; no engine branch reads it.
- Predictions pre-registration: predictions.md mtime 06:07:41, decisive-run.txt 06:07:49 (run wall 4.4 s) — written first. Smoke values disclosed as tuned-on.

Arithmetic in the claim checks: 28997/29402 = 0.9863; hits/representable = 0.9525; 29402/1398 = 21.0×; 848 B × 10⁹ ≈ 850 GB ≈ 106× of 8 GB; residual 52 ≤ 65 bits documented at `crates/space/src/binding.rs` ("Each component can require 65 bits"). The 12-bit quantum is real and vetted (`MEMO_SHAPE_BITS = 12`, orbit.rs, "one fewer shape bit passes G1/G2 but is not sufficient for the full weak envelope"). `docs/law.md` line 14 does specify the shared memo; the universe `Catalogue` (bind.rs) is keyless slots — the fence exists in prose and in `crates/space` (`Catalogue.ids`, `CyclePool::intern`), not on the plane. All confirmed by reading the code.

## Held-out and adversarial cases (mine)

1. **Memo-key behaviour proxy (the author's named gold experiment, cheap half):** exact- vs memo-compiled period on the 300 sampled ship states: median 1.045e-4, p90 1.7e-4, **max 4.98e-4** — inside B2's 0.1% band with little margin, exactly the risk the dossier states. B9 precession remains unmeasured.
2. **Seed/scale robustness:** seed 7 members 1024 → hitrate 0.9502; seed 3 members 96 → 0.9485 (distinct-exact falls to 87%, memo sharing holds). Prediction 2 held out of sample.
3. **Long-run growth:** 3600 frames → hitrate 0.9584, distinct keys 1398→1662 (rebinds 29402→39992): sublinear, no memory blow-up on this horizon.
4. **Zero-kick control (accidental, decisive for attribution):** a probe bug skipped all kick processing — the universe still produced 39283 rebinds (10.9/frame vs 11.1 with kicks replayed). **~98% of the rebind stream is non-kick (frame/settle) rebinds.** The 21× compile-work reduction is real but accrues mostly off the kick path; on the kick path proper the saving is the honest paired-timing arithmetic (0.95 × 2.36 µs of 26 µs ≈ 9% here). The Bottleneck section's "per kick … on 95% of rebinds" conflates the two streams.
5. **Dense order:** unmeasurable within the checker budget (>40× costlier per frame; times out at members=256/300 frames). The hit rate under dense fleets remains unmeasured — same shape as the author's one-scene caveat.
6. **Eviction caveat:** the stream hit rate assumes an unbounded, never-evicted memo; with sublinear key growth this is immaterial on these horizons but the 10⁹ distinct-live-keys estimate rests on one 28-body scene.

## Novelty

No H entry covers plane-catalogue keying. The G3-era `field_at` memo (H ~784–819 region) is a different engine and a different memo (field query, `es-inertial-causal-v1`), not cycle-compile sharing. The shared-memo *idea* is in law.md (design prose) and the interning *pattern* ships in `crates/space`; what is new is the measurement on the plane's real rebind stream (95.25%, exactness, 848 B/entry, 21×) that turns that prose into adoptable evidence.

## Goal fit

Board #3/#5 via handoff item 3. Quotes hold: "Compute only surprises" (§3 — a recompile inside one (E, L) quantum is work for no reason), "Store the generator, not the generated" (§6), "The memory floor is information" (§24 — distinct live keys are the information). The fat-tail 850 GB reading sizes the allocator's worst case, the right Taleb instinct.

## Why silver, not gold

Real, reproduced exactly, predictions held (1, 2, 3, 5; 4 partial and disclosed). But it cannot be adopted within one step: memo keys change the law each cycle by the quantum (periods shift up to 5e-4, measured), and frozen gates B1/B2/B9 have never run on memo keys — adopting without re-freezing would weaken the gate regime the repo forbids weakening. The measured 21× is compile work, not the kick's 10–100× (kick gets ~9% here; the 2× M1 figure is inference), and ~98% of the benefiting rebinds are not kick rebinds.

**The one experiment to gold:** re-freeze B1/B2/B9 on memo keys (positive control: exact keys) plus the B15 Zipf-fleet and a dense-order hit-rate measurement.

## What the author missed

- The attribution gap is larger than flagged: a zero-kick control shows kicks contribute ~2% of rebinds in this scene, so the memo's measured benefit sits mostly on frame/settle rebinds, not the cited kick bottleneck.
- The plane *today* already spends 31,860 B/body on the catalogue at members=1024 (the probe prints it; the dossier buries it) — a stronger statement of the requirement than the 10⁹ extrapolation.
- The stream hit rate is an unbounded-memo upper bound; no eviction policy was measured.
- The period-shift distribution (my case 1) was measurable within the run's own budget and directly de-risks the named gold experiment; leaving it unmeasured kept the dossier one experiment short.
