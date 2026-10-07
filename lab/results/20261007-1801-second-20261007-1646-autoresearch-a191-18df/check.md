Grade: silver

**Abstract.** The claim: the silver deletion rebuilt scope-free regenerates its record from the patch alone, and the cadence lever is priced (work exponent ≈ 1 at flat per-kick cost; ≈ 4× B13 error per halving). Reproduced exactly: my own interleaved A/B on the author's four scenes plus my m4/rtf1000 gives made −18…−21 %, leavers −5.5…−8.5 %, digests bit-identical everywhere, 18 suites 104/0/1; cadence kicks 949→507→287→173, work ×0.54/×0.30/×0.16, exponent 0.98–1.04; B13 60/64→41/64→15/64, worst 2.12e-2→8.47e-2→3.39e-1; Jacobi ×3.5 with kicks exactly halved. Gain stays 1.1–1.2× per kick; cadence prices the integrator's door without opening it. Cost to adopt: apply `work/scope-free.patch` (clean on HEAD, zero prof refs).

## Reproduction (clean tree at a838a28; every number mine unless stated)

- **Patch hygiene:** `scope-free.patch` applies clean; zero `prof` references; the `universe.rs` deletion is byte-identical to the silver run's; `bind.rs`/`step.rs` differ only by prof-scope removal and one brace reshuffle (same semantics). The run's snapshot `patch.diff` equals scope-free + cadence-flag applied together.
- **A/B (my binaries, my interleave, quieter box):** made −18.3/−19.4/−19.0 % (tuned/m24/m96), −19.2 % m4, −19.3 % rtf1000, −21.0 % rtf10; leavers −5.5…−8.5 %. `replay_digest` and canonical `digest` bit-identical on all six scenes (tuned = `eaef383e…`/`c8ab26da…`), `refused` 0. The author's `data/*.json` regenerate the dossier text verbatim (made −17.8…−19.6 %, leavers −5.9…−9.7 %).
- **Digest gate has teeth:** digests differ across scenes and cadences, so equality is not vacuous; `--step-log2 7` ≡ default confirmed bit-identically.
- **Tests:** 18 suites, 104 passed, 0 failed, 1 ignored — exact.
- **Cadence cost:** kicks 949→507→287→173 (m48, exact); per-kick made 28.5→29.6 µs flat (theirs 28.6→29.9); work ×0.534/×0.301/×0.154 (theirs ×0.54/×0.30/×0.16); work-vs-rebind exponent 1.04/0.98 (theirs 1.05/1.03).
- **Cadence price:** B13 60/64→41/64→15/64 within 1e-2, worst 2.12e-2→8.47e-2→3.39e-1 (×4.00 per halving), runtime 2.25→1.13→0.64 s. Jacobi (valid range) worst 5.1e-6→1.8e-5 (×3.5), kicks exactly halved 82930→40650.
- **Predictions:** `predictions.md` (18:03:36) precedes all decisive data (18:06:39+). Ranges, digest identity, suites, linearity, Jacobi ≈4×/doubling: held. Honest corrections disclosed (samples fall 1.9× not 2× — floors).

## Adversarial (mine)

1. **m4 and rtf1000** (edges the author never ran): gains and digest identity hold; rtf1000 gives 2312 kicks, still −19.3 %.
2. **Beyond the ladder:** l2=8 → work ×1.94 (finer side also linear); l2=3 → ×0.083 but per-kick made rises +11–18 % — the flat-per-kick claim is range-bound to 7–4, which the dossier respects.
3. **The panic:** jacobi at step 7 panics `Space(Range)` — I stash-verified it at unpatched HEAD; pre-existing, correctly reported, not caused.
4. **Load contamination check:** the author's m24 pair reads −34.3 %/−24.3 %, but their base median (43.3 µs) is inflated against their own other scenes (35.1–35.5); my clean interleaved m24 is −19.4 %/−8.5 %, in family. The m24 "super-gain" is a contaminated pair, disclosed but misread.

## Novelty

The deletion is the parent silver's (`20261007-1646-autoresearch-a191`); this run's contributions — the adoptable scope-free artifact and the engine-side cadence pricing — have no H entry. `q-cadence-7d0d` (5 Oct, silver) measured the *behaviour* frontier offline (moon model, N* = 4–16 kicks/orbit at Hill positions, mixed scene unvalidated); this run measures the *cost* side and the frozen-gate price on the shipped plane. Complementary, not duplicate — but see misses.

## Goal fit

Board focus line 1 ("cheaper events"; "fewer kicks per orbit at the same behaviour"). PRINCIPLES §1 "The cheapest compute is compute not done. Delete before optimizing" — a pure deletion, bit-identical; §19 — pricing the door instead of patching `compile` is the right representation question. The lens honestly marks the 1.1–1.2× ceiling.

## Why silver, not gold

Everything reproduced, predictions held, record quality is the best I have checked here. But the gold bar is magnitude: the deletion moves the kick path 1.1–1.2× (the parent already judged this below 10×, and no component dies — redundant compute dies); the cadence table *prices* the integrator's one-way door without opening it — at l2=4 work falls 6.3× while B13 collapses to 15/64, so no 10× exists at held behaviour, and no premise is killed (the compile wall is confirmed, not overturned).

## The one experiment for gold

Harvest the lever at held gates: a per-body, Hill-gated cadence (coarse away from secondaries, fine through flybys — exactly `q-cadence-7d0d`'s offline frontier, whose mixed-scene validation is its own named gap), measured on the plane holding B13 and the redesigned B12. If ~10× fewer kicks per orbit at held behaviour, that is gold; this run's table is its cost model.

## What the author missed

1. `q-cadence-7d0d` is never cited: its N* = 4–16 near the secondary against the plane's global 2⁷ = 128 per radial period is the design tension the B13 ladder exposes — global coarsening fails precisely where flybys need finesse; per-body gating is the harvest, and the two runs together already specify it.
2. The m24 contaminated pair (above) — a load artifact read as a super-gain instead of a flagged pair.
3. l2=3 breaks flat per-kick cost (+11–18 %): worth stating, since any q-cadence design that averages coarser than 2⁴ will pay it.
4. B12's finite-vs-inf exponent flip across cadences (0.982 at step 6, inf at 7) is visible in their own runs and unremarked — noise in a broken gate, but B12's redesign should know the reading is cadence-sensitive.
