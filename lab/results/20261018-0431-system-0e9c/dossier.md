# Dossier — 20261018-0431-system-0e9c (system lens)

## Claim

The player-scan's fallback walk reads the whole universe and throws away every cross-doll body one line after the read — 80.6% of a bail's walk at the belt seam — while the per-doll radial index already holds the doll-local answer; one index-served bail path (`ES_LOCAL_BAIL`) makes every capture O(doll) with the candidate set identical to the body at every scene and the frozen 13-case digest record bit for bit, which deletes the bail's cost class at 10⁹ and makes the bail's nonlocal threshold knob cost-neutral.

## Bottleneck

Board live question 1's read path ("which term breaks first as the plane grows … memory per live body / the queue"): the scan. The pages price it three ways — promotion (604c: the filter bails on 100% of plane-scale scans; a 200-ship formation beside a 10⁴ belt switches scans to full walks, 9,549 `binding_at` a scan; "a nonlocal coupling against PRINCIPLES 15"), scan-queue (cdf0's N-relative rule; 3999: in the belt band the fallback is an every-N disease; f102: the fallback regime's capture ~44 µs), memory-h-live (the held-scan pin, candidates × 224 B). All three circle one walk whose domain is wrong. Expected gain: the bail's walk term drops from O(universe) to O(doll) — at the goal's N (belt in another doll) a bail goes from ~10⁹ reads ≈ 100 s to ~333; at the flown seam, walked bodies −75.1%. What it deletes: the "when does the filter bail" cost question (cdf0's threshold rule, 3999's every-N disease, promotion's priced threshold fix — all become moot for cost), i.e. a whole tuning axis rather than a constant.

## Evidence

All numbers from `regen.sh` (shipped code + `work/patch.diff`; `SCAN_CENSUS` print-only counters; `ES_LOCAL_BAIL` env-gated; off-arm is the pristine path). `nladder` ported to Linux `/proc` (the macOS `proc_pid_rusage` extern does not link there — the known lab issue).

The waste, measured on the shipped path (off-arm census, cumulative):

| Scene | captures | bails | walked/bail | discarded/bail (after the read) | share | candidates kept/bail |
|---|---|---|---|---|---|---|
| N=0 coast (plane scale) | 384 | 383 (99.7%) | 72.7 | 18.0 | 24.8% | 32.5 |
| N=10³ burn (f102's fallback regime) | 2,112 | 416 | 1,070 | 718 | 67.1% | 344 |
| N=3000 belt-crossing L10 (the seam) | 9,280 | 2,920 | 1,841 | 1,484 | 80.6% | 333 |
| N=10⁴ coast (filter on) | 384 | 0 | — (201 walked/scan, filtered) | 0 | — | 179 |

The mechanism is in the shipped code: `encounter.rs::capture` walks `0..ctx.bodies.len()` when `radial.rs::candidates` returns None, pays `binding_at(j, t)` for every j, and discards at `if other.doll != me.doll { continue }` — the doll test runs one read too late. The index (`radial.rs`) already holds exactly the doll's registered population (`note` widens per binding, `rebuild` hulls the retained history per doll), so the bail can be answered locally.

The fix (`ES_LOCAL_BAIL`, `radial.rs::all_of`): a bail returns unbounded + every bin of the doll, deduped. Measured, on-arm vs off-arm, same scenes:

- **Candidates identical to the body**: seam 1,201,472 = 1,201,472; N=10³ burn 261,373 = 261,373; kept-per-bail unchanged (333, 344). doll-discards 0 everywhere on the on-arm.
- **Walked bodies**: seam 5,773,664 → 1,437,104 (−75.1%); N=10³ burn 570,958 → 272,270 (−52.3%). Seam capture wall 500.9 → 329.8 ms over the same window (−34%); N=10³ capture_ms 54.2 → 55.7 (noise — the discarded reads are ~0.1 µs each; f102's ~44 µs is the kept candidates and the tube solve, 7343's 85–90%, not the walk).
- **Digests**: `ladder_digest` full 13-case × 4-schedule record, off vs on: identical after stripping per-case wall times (the seam case `4995f38448103cc20232d292eb40a84b`, kicks 40,106, encounters 789, contacts 0, in both arms; `regen.sh` diffs and fails on any move). Off-arm vs the shipped frozen record `artifacts/runs/nladder/ladder_digests_newpop.txt`: all 12 shared cases identical to the digit (my run adds the two wave cases the record lacks) — the patched build with flags off is pristine.
- Exactness is by construction, checked empirically: the caller's cheap tests already discard other dolls' bodies (so the fix cannot drop a candidate the old path kept), and the index is a superset of every retained binding per doll (so it cannot miss one); the digest record exercises handoffs and 789 encounters at the seam.

Reproduce: `sh lab/results/20261018-0431-system-0e9c/regen.sh` (~9 min: build 30 s, census arms ~15 s, two full digest runs ~2:40 each). Each individual command ≤ 60 s except the two digest runs (2:41 each, one process, self-bounded by the frozen case set).

## Predictions

`predictions.md` was written before the decisive runs. P1 held in mechanism, missed in one number: cross-doll reads dominate the bail walk beside the belt (80.6% at the seam — I had said ≥ 90% at N=10⁴ coast; at 10⁴ *coast* the filter stays on and there are no bails at all, so the ≥90% claim had no domain there; the seam is the belt-arm truth). P2 held (99.7% bails at plane scale vs 604c's 100%; the filter on at 10⁴ coast; the seam ~all-bail regime). P3 held (13/13 cases bit-identical, both arms one digest on every schedule). P4 held (walk −75.1% seam; capture −34% seam; frame p50/p99 unchanged — the scan is not the frame's owner on these scenes, promotion's finding stands); the pin is untouched as predicted. P5 stands as an inference priced by the arm comparison: both sides of the threshold now cost O(doll).

## What would make it wrong

A body whose binding at the scan's tick lives in the player's doll but is absent from that doll's index (a registration gap outside the flown scenes — e.g. a capture edge the case set does not cross) would be silently dropped from candidates under the fix. The construction argument (note/rebuild cover every retained binding) plus 13 digest cases with handoffs and encounters bound this, but a dedicated capture-stress case (rapid doll handouts at the edge) would close it. Second: the census measures seed 1 and the frozen scripts; other seeds' seam crossings share the law but not the letter.

## Cost of adoption, and fit

One env flag to flip after review (or delete the flag and keep the local path — the off-path then dies); ~40 lines including the census (which stays print-only). No law change: the candidate set is provably and measurably unchanged, so no B-gate re-freeze (unlike the cadence arms). The integrator still re-measures on the M1 (Linux x86 here; the walk is reads, so the ratio carries, the constants do not). Fit — PRINCIPLES 15: "local laws are great because parallelizable and simple and efficient"; PRINCIPLES 1 (the cheapest compute is compute not done: 80.6% of the seam walk never needed doing) and 17 ("the best part is no part": the threshold tuning axis deletes). It also answers the lens's hunt: a component (the bail's threshold rule and its priced fix) existed only to repair another (a fallback whose domain was the universe).

## The lens

The whole-system lens found a cross-page mechanism (three pages pricing one walk) and its representation fix, but it may have missed the crowd case: a formation (K-sized doll population) beside a belt — 604c's bailing population pair — is unflown here; there the doll-local walk is O(K), the pin K × 224 B, and both should be confirmed unchanged (wiki direction 5). It also did not touch the kept-candidate term (the seam's 333 reads per capture — the pages' angular certificate and phase-rank levers remain the real seam work), so this run must not be read as "the scan is cheap now": only its walk term died.
