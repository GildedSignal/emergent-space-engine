# Dossier — 20261013-2005-quant-7055 (Quant lens)

**Claim.** On the shipped plane the fleet's hand-outs already share compiled trajectories exactly —
one third of them (33.0% at 4,000 members, rtf 1) are the *second member of a consecutive pair*
handed out on the very same escape passage — so an exact compile-key memo (or sharing by
construction, which the pair structure makes possible with no lookup at all) cuts the hand-out's
bind 39% and the whole hand-out 31%, bit-identically, while the "shared-shape" promotion at flying
pace (rtf 100) is worth nothing (0.6% hits): sharing is a battle-regime edge, not a scale edge.

**Bottleneck.** The furthest-gap one: bodies in the flyable engine (28 vs 10⁹). The fermi run
(20261013-1915) measured the plane's first N-wall as the fleet frame's leak into sticky promotions
(486–585 µs, 8.3 kB each) and named the fix's halves: ephemeral, shared-shape, census-gated. Nobody
had measured whether shapes are actually shared. This run prices the shared-shape half: **1.45× on
the hand-out, no more** — a constant factor, not the 10× the board wants, so the ephemeral half
stays the real lever; but the pair structure it found (below) changes what the smallest promotion
*is*: for the second member of a pair the compile is not needed at all, only placement.

**Evidence** (shipped code + the probe patch in `work/` — env-gated `ES_ORBIT_KEYS`/`ES_ORBIT_MEMO`,
inert unless set; Linux/x86 runner, i7-4790-class, orders of magnitude only; all runs
`--unpaced --seconds 8 --seed 1` unless said; digests at the canonical cut):

| scene | hand-outs | hand-out compiles | exact hits | hit % | bind µs A→C | hand-out µs A→C | digest A=C |
|---|---|---|---|---|---|---|---|
| m48, m400 (rtf 1) | 0, 0 | — | — | — | no hand-outs in 8 game-s | | yes |
| m1500 | 232 | 352 | 118 | 33.5% | 494 → 336 | (bind-dominated) | yes |
| m4000 | 2,157 | 3,303 | 1,090 | 33.0% | 407–419 → 250–252 | 508–525 → 351–354 | yes (×2) |
| m4000 seed 3 | 2,041 | 3,104 | 1,009 | 32.5% | 402 → 246 | 506 → 349 | yes |
| m400 rtf 100 | 378 | 617 | 4 | 0.6% | 349 → 377 | 479 → 513 | yes |

- The hit is exact: `Orbit::compile`/`Passage::compile` are pure functions of (key, edge), the memo
  keys on them, so a hit returns bit-identical bits (this is *not* the killed 12+12-bit quantized
  memo, which changed orbits). Digests are bit-identical memo-off vs memo-on at every scene, twice
  at m4000, and the shipped universe suite passes with the memo forced on (26 passed, 1 ignored
  clock flight, 0 failed, including `the_digest_is_the_same_through_a_frames_whole_life`).
- The no-hit regime neither helps nor hurts measurably: m400 rtf 100 bind 349–359 → 361–377 µs
  (+0.6% on regen, +8% on the first matrix pass — shared-box noise, 4 hits). A production version
  should key on the pair structure (below) and pay nothing when there is no pair.
- **The sharing is pairwise and consecutive.** Every one of the 1,090 duplicate keys at m4000 is
  held by exactly two members (top-5 keys: 2, 2, 2, 2, 2), and the two hand-outs are *adjacent in
  the hand-out stream* (gap 1 in 1,090 of 1,090 cases). All repeats are passages (unbound); no
  periodic key ever repeats. [INFERENCE] The cause is the birth pair: scene members are generated
  in mirrored pairs (`engine_judge/scene.rs`), an untouched pair conserves (E, L) exactly in
  integer arithmetic, and the pair leaves the frame together at one anchor; not measured directly.
- Per-hit saving ≈ 476 µs (157 µs average over a 33% hit rate), larger than the compile's share of
  bind alone (60–66%, ≈ 250–270 µs): the second member's read of the shared `OrbitShape` is also
  cache-hot (the shape is `Arc`-shared by the clone). Mechanism attribution partial; the total is
  what is measured.

**Predictions** (`predictions.md`, written before the decisive runs): global hit rate ≥ 25% at
m4000 **held** (25.0% of all compiles); digest identity **held** everywhere; cost ≈ −30% at a 50%
hit rate — measured −31% at 33% (better per hit than predicted, cache warmth); seed 3 within 2%
(held). **Failed:** the rung-by-rung hand-out hit rates (≥ 50% at 48, 20–60% at 400) were
untestable — no hand-outs occur at ≤ 400 members in 8 game-seconds; and rtf 100 (predicted within
2×) failed at 50×: the sharing exists only where the battle is resolved (rtf 1), 0.6% at flying
pace. My kill signal for the shared-shape half ("≤ 5% at every rung ≥ 400") did *not* fire at rtf 1
— the initial 0% reading was a probe artifact (the hit column only records under the memo), caught
because the key strings showed 1,090 repeats the hit counter denied.

**What would make it wrong.** The pair structure is measured on one scene (the plane's fleet, one
formation geometry) at 8 game-seconds; a sparser battle geometry or a longer run could change the
pair fraction (touched members scatter onto singleton orbits, so the hit rate should *fall* as the
battle ages — not measured). The 476 µs/hit decomposition is [INFERENCE] beyond the compile skip.

**Cost of adopting.** The memo is ~40 lines (probe patch, `work/`), a per-doll key→entry map on the
compile path, plus release of entries when their tube count falls to zero; the cheaper adoption is
no memo at all: the frame hands the pair out consecutively, so `resolve_handout` can hold the last
hand-out's entry and let the next hand-out test equality against it (one comparison, no map, no
misses ever paid). Memory side: the second member's `Entry` Arc-shares the compiled shape instead
of duplicating it, so standing bytes per promotion fall too (not measured numerically here).
Fit with PRINCIPLES: "The cheapest compute is compute not done" and "Store the generator, not the
generated" — the pair *is* the generator of the second member's tube; also "Compute only surprises"
(the second member of a pair is not a surprise).

**The lens.** Quant may have under-priced the exactness argument: it measured the edge before the
bet, but it nearly reported the probe artifact (0% hits) as a refutation — the key-string
duplicates saved it. What it may still miss: whether 33% is stable as the battle ages (touched
members leave singleton orbits), and whether the *first* member's compile can be deferred (the
ephemeral half) so that neither member of a quiet pair is ever promoted at all.

## Reproduce

`work/probe.sh` (matrix: 6 scenes × 3 arms, ~2 min), `work/analyze.py` (the table), the interleaved
A/C/C/A runs at m4000 (~1 min), the memo-on test suite (`cargo test --release -p emergent-universe`,
~6 min), all through `regen.sh` (≤ 15 min total including the build).
