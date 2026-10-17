# Dossier — 20261017-1829-second-20261017-1447-dynamics-fd35-e517 (second author on fd35)

## Claim

The checker's named experiment is done and fd35's claim holds on the positive side:
**the finality assert's firing is decided exactly by state at certify time** — on
01e7's selfchurn harness with fd35's print-only instrument (plus one new field), 9
reproduced fires were each preceded by PRE `D = 16 = fin_hi − s0` (exact assert
inputs, 9/9) and by HAZ `A > 0` from scene start (fd35's P5), while all 2,286
non-fatal realized clashes sat at D = 0 and rollback's union-find closure never once
left PRE's descendants closure (`out=` empty on 2,295/2,295 RB events, fires
included) — the sibling-closure hole the checker named is now a measured-shut,
live-checkable invariant rather than an asserted direction.

## Bottleneck

`lab/wiki/allocator-ratchet.md` direction 7 and fd35's "what would make it wrong":
the negative certificate was validated only on draws that never fire; the positive
direction (crash ⇒ armed > 0 first) was one reproduction away, and PRE's
"over-arm, never miss" was asserted, not shown. Both gaps closed here. No compute
claim: this finishes the *test* of the confirmed-necessary engine-side fix (its gate
is "armed ≤ 0 ∧ D ≤ 0 maintained", now sound in both directions on realized draws)
and deletes the window Monte Carlo the fix would otherwise need.

## Evidence (numbers from the saved logs in `work/`, which `regen.sh` rebuilds from
shipped tree + `work/patch.diff` under the same protocol in ~1.5 min; fires are
raced, so a regen may catch fewer — every invariant below held identically in the
regen run: 4/7 fires, P2/P3/P4/P5 zero fails, `out=` 0/906)

Patch = fd35's print-only instrument (HAZ/PRE/RB/FIRE in `crates/allocator/src/alloc.rs`
+ `examples/race.rs`), verbatim, **plus one print-only field** in RB: `out=` =
affected ids outside the descendants of the clash lineages (the union-find
sibling-closure gap), `mo=` = the restore margin they alone would carry; plus
`examples/finpol.rs` (01e7's selfchurn harness, fetched from its branch, byte-equal
use). No engine line touched; the assert is unmodified.

**The firing sweep** (`finpol selfchurn frames 120 6 128 600 2 <seed>`, seeds 11–19 ×
2 replicates, serial, one process per draw; `work/sweep/`):

| quantity | value |
|---|---|
| fires | **9/18** (s11, s13, s15, s16 2-of-2; s14 1-of-2; s12/17/18/19 0-of-2 — bc0f's seed skew, richer than 01e7's 3/9 under this window's load) |
| every fire's violation | exactly one window: `fin_hi − s0 = 16` (s0 = 32 scene start ×7; s13 twice at s0 = 80, bc0f's late reclash phase) |
| P5 / armed precedes | **0 fails**: first armed at publish 8–12, presented t = 0.41 (scene start); armed lead = 51–449 publishes ≈ the whole scene start (~32 chronons) |
| PRE decides | fatal PRE `D = 16` before every FIRE (9/9; 7/9 on the immediately preceding line; s13's gap = 9 is the same certify's benign pairs). 18 D = 16 lines total = 2 armed truths per fatal clash list, both D = 16 |
| equality law | 950 PRE at D = 0, 2,286/2,295 RB pairs at m = 0 (the 9 exceptions are the fires), **D < 0 never, D > 0-without-fire never** |
| closure gap | `out=` non-empty **0 of 2,295** RB events, fires included; mo = 0 always |
| armed ≠ incidence | all 9 survivors armed too (139–376 armed publishes, 89–99% of theirs) — armed is the possibility state; realization stays the wall-clock race |

**State-side arms regenerate from shipped code** (`work/racearms/`, fixing both of
fd35's regen bugs): the armed-episode probe with sabotage genuinely off
(`race 400 11 1 900 2 16 8 128 60 x 0.3` — `x` parses to `None`, where fd35's
`sab 0` meant `Some(1)`): 14–15 armed publishes to A = 128, rb = 0, every episode
resolved by disarm (the checker's rescue, now the regen line); two churn arms
(`3000 11/15 1 2400 4 16 8 64 40 3 1.0`): 1,123 further clashes, all D = 0, all
m = 0, never armed, `out=` never opens — fd35's equality law unchanged under the
e517 patch. Rollback counts are schedule-moved (565/558 in regen vs 579/541 in the
window run vs fd35's 1,305/1,326): incidence is wall-clock raced, exactly as the
page says; the invariants are schedule-independent and held in every run.

Reproduce: `bash lab/results/20261017-1829-second-20261017-1447-dynamics-fd35-e517/regen.sh`
(clean tree, applies the patch, builds, sweeps; fires are raced — each firing seed
gets 3 attempts, panic values per seed stable).

## Predictions

`predictions.md` written after one disclosed pilot (s11 fired), before the sweep.
P1 (≥ 2/9 seeds fire) **held** (5/9 r1). P2 (armed > 0 before every fire, ≥ 8
publishes) **held** (0 fails, lead 51–449). P3 (fatal D = violation, exact; no fire
with D ≤ 0) **held** (9/9, D = 16 = viol). P4 (`out=` never opens) **held** (0/2,295).
P5 (equality law on non-fatal clashes) **held** (2,286 at m = 0, D < 0 never).
P6 (armed survivors exist) **held** (9/9 survivors armed).

## What would make it wrong

- The D ⟺ fire equivalence is proven on 9 fires + 2,286 benign clashes of one family
  (plus fd35's 8,213 across 45 arm-processes and the checker's 2,393). A fire with
  `out=` non-empty and mo > D would break PRE's exactness — the instrument now
  prints it, so the gate fails loudly rather than silently.
- The closure coincidence is *measured*, not derived: `out=` shuts the hole on every
  realized clash flown, but a scene where snapshot-sharing siblings outside both
  lineages carry a higher fin_hi is not excluded by argument — the derivation of why
  `alone_at` and `certify` pin the same tick (fd35's lens note) remains the missing
  proof the fix should be written against.
- The A ≤ 0 (publish-side) half of the certificate misses strides dispatched between
  publishes; their clashes are still caught by D at certify. The certificate's
  soundness rests on D, which is exact because it mirrors `certify`'s own scan.
- Incidence stays a raced draw (s14 fired 1-of-2 here, 0-of-1 in regen); nothing in
  this run predicts *whether* an armed pair clashes — that was never the claim.

## Cost of adopting, fit with PRINCIPLES

Patch is print-only (~180 lines, test harness only). The fix's gate is now:
"armed ≤ 0 at every publish ∧ D ≤ 0 at every certify, `out=` empty" — decidable per
draw from state. Measured cost of the hold-publication fix on this family: armed
publishes are 89–99% of *every* draw (survivors included) at scene start, so
refusal alone starves publication — the fix must pair with the disarm channel
(truth pruning/aging, the h_nosab episode's resolver). PRINCIPLES 13 ("errors never
compound" — the assert aborts the engine; the certificate reads it before it
fires) and 34 ("the oracles are guards, not shepherds" — D judges the boundary, it
does not move it).

## The lens

Second-author lens: I did exactly the checker's named experiment and nothing else;
what it may have missed is everything outside that experiment — no new scenes, no
load axis, and the `finpol` harness is 01e7's, so the two-family independence of
the equality law rests on fd35's race arms, not on anything new here.
