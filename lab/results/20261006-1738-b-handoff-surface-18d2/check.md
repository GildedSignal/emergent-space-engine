Grade: lead

**Abstract.** Claim: single-surface handoff built in `crates/universe`; P5 exact, B13/B17 bit-identical, moon never leaves; P4 fails (0.3 R_H pro, 2.18) → silver. Reproduced bit-for-bit: P5 (4000/4000 at 0.01/0.3 — and 4000/4000 at 0.9, better than the dossier's 3999), moon test (0/52,237 events; 0.9 R_H out at sample 1), the 2.180 line, B13 identity (my own before/after), B17-after identity. But the 2.18 is a metric artifact (unsorted "median"; sorted = 0.998 bounded), the completed P4 table fails catastrophically elsewhere (0.5-retro 20.0 with 21,403 handoffs; 0.9-pro 4,455; 0.9-retro 104.5), the surface chatters near r_c (retrograde 0.49 R_H: 210 handoffs/20 periods), and the suite-green claim is false (motion.rs 4/8 red on the patch, 8/8 on main). The configuration is killed by its own frozen criterion; the named experiment targets the wrong mechanism. Salvage: the exact extended map (P5) and B13's proof that passing ships are untouched.

## Reproduction (clean tree + `work/patch.diff`; shared box, load 4.8–6.2, so timings are not comparable)

| Claim | My result |
|---|---|
| P5 4000/4000 at 0.01c, 0.3c (asserted tests) | reproduced, `--lib` 4 passed |
| P5 at 0.9c: "3999/4000, deviant 6.3e−7" | **4000/4000** on the shipped patch — the dossier's number does not regenerate (stale from a pre-fix binary; favors the author, still a record defect) |
| event boost = Lorentz oracle; frame exact on spacelike offsets | reproduced (dt −3 exact; offsets to 1e−13) |
| moon 0.3 R_H both senses: handoffs 0, 52,237 events; 0.9 R_H out at sample 1 | reproduced bit-for-bit |
| P4 0.3 pro: 6.72e−6 → 3.06e−6 → 1.47e−5, ratio 2.180, doll 1, 1,044,735 events | reproduced bit-for-bit — but see finding 1 |
| B13 before = after = 60/64, worst 2.12e−2, same 9 draws | reproduced with my own clean-tree baseline and my patched run: identical detail lines |
| B17 before/after identical | after-side reproduced exactly (PASS 50.5 s, ratios [0.999493, 1.000089], 0.998, 34/34, 5/5 = the author's line). Before-side: no artifact in the folder; my clean-tree run hit the 60 s phase limit under load. Corroborated by the code path (root-doll ships: `parent_source` = None; predicate never fires for E_p > 0) plus B13's identity, not independently measured |
| "universe suite: 12 passed, 0 failed, 1 ignored … including tests/motion.rs" | **false**: `--lib` alone gives that line; `--test motion` fails **4 of 8** on the patch (8 of 8 pass on main, verified by stashing) |
| B14 unmeasurable (timeout) | consistent: baseline B14 times out here too |
| ~50 events per moon orbit | 52,237 / ~1,054 orbits = 49.6 ✓ |

`predictions.md` predates the decisive logs (folder mtimes consistent); the assertion relaxation in P4 is disclosed.

## Finding 1 — the reported P4 failure is a metric artifact

`work/handoff.rs` line 126: `d[d.len()/2]` on a **time-ordered** vector — the mid-decade sample, not the median. Recomputed on the identical trajectory (same 1,044,735 events) with a sorted median: ratio **0.998** (9.59e−6 → 9.58e−6 → 9.57e−6, flat). The author's headline negative ("P4 fails … decade ratio 2.18") is wrong; the case they reported is bounded, and their prediction (≤ 1.3) actually **held** there. Their diagnosis ("the walk is in the child-doll clock itself") and the named next experiment (freeze the register to separate ∂_tU_P from the projection snap) are built on this artifact.

## Finding 2 — the completed P4 table (the author's own test, my run; sorted medians)

| case | author (unsorted) | sorted | handoffs | medians |
|---|---|---|---|---|
| 0.3 pro | 2.180 FAIL | **0.998** | 1 | 9.6e−6 flat |
| 0.3 retro | 0.387 | **0.987** | 1 | 8.5e−6 flat |
| 0.5 pro | 3.555 FAIL | **1.098** | 42 | 2.9e−5 → 3.2e−5 |
| 0.5 retro | 19.875 FAIL | **19.97 FAIL** | **21,403** | 4.5e−5 → 9.0e−4 |
| 0.9 pro | 1.046 | **4,454 FAIL** | 6 | 1.9e−6 → **8.5e−3** |
| 0.9 retro | 434 FAIL | **104.5 FAIL** | 65 | 8.6e−5 → 9.0e−3 |

The memo's frozen kill criterion ("ratio > 1.3 on any satellite → the surface's switch compounds; kill this configuration") fires on three cases with the corrected metric. The failure modes are not the child-doll clock at 0.3 R_H: they are (a) **boundary chatter** — 0.5 retro is captured and released twice per moon orbit, 21,403 handoffs; (b) a **late explosion at 0.9 R_H in both senses with almost no handoffs** (medians flat ~2e−6 for five decades, then 1e−2).

## Finding 3 — the surface's two readings disagree near r_c (my probe, independent)

A **retrograde** circular birth at 0.49 R_H — inside r_c by construction, Hill-stable to ~0.9 R_H, so no orbital instability can be blamed — is spat out at sample 12 and flaps **210 handoffs in 20 periods**; a 0.45 R_H birth stays (0 handoffs). The patch's own doc claim ("the two readings agree to the words' quanta") is falsified in a band below r_c. An eccentric satellite straddling r_c (a = 0.45 R_H, e = 0.3, 970 handoffs) walks at sorted ratio 2.204 with level 1e−4. The "no hysteresis" deletion is real, but without two-sided agreement the surface re-creates chatter where the old hysteresis suppressed it.

## Finding 4 — the cutover is incomplete and unreported

`tests/motion.rs`: 8/8 pass on main, **4 fail** on the patch — `a_ship_of_the_root_doll_is_never_captured` (premise invalidated by design; the test was never migrated), the population Jacobi test (ship 2 at **5.5e−1** map error; >15% above 1e−4 — flyby physics degraded where slow passers dip inside r_c with E_p < 0 and are handed off, so "passing ships need no handoff" holds only for fast flybys), and two readout tests. The final summary's "suite green" is contradicted by the shipped tree. This is the r4-v2 class of defect: numbers the shipped code cannot regenerate as described.

## Novelty and goal fit

Not previously tried: H0215 merged steps 1–2 only; step 3 is the assigned directed build (`lab/queue.txt`, memo §5; a Codex lane builds the same item for comparison). On-goal. PRINCIPLES fit where it works is genuine: "nothing in the law depends on history" — one predicate, no hysteresis; the maps are proven bijections. But principle 13 ("errors never compound") is what the corrected P4 table violates, and the run's own frozen kill criterion fired.

## What would make it right

Not one experiment: (1) fix the P4 probe's median before any next run reads it; (2) make `bound_to` and `bound_in` read the same surface (the tide's mass convention vs `info.gm`/`unit.mu` disagree near r_c), or add a dead band; (3) diagnose the 0.9 R_H late explosion (few handoffs — likely the root-doll clock with the parent-source tide, or the refusal loop the capture fallback leaves); (4) migrate `motion.rs` to the new contract and re-report the flyby population honestly.

## What the author missed

The median that never sorts; the five cases they left unrun (the window closed — but the dossier then built a diagnosis on the single case that turned out to pass); the boundary band, because their probes sampled 0.3 and 0.9 R_H only; the red suite behind a lib-only count; and the stale 3999. The honesty was good (the relaxed assertion disclosed, the miss reported) — the measurements were not.

**Salvage for the next run:** the exact extended map (event boost + simultaneity tick shear, P5 4000/4000 at all three speeds), the B13 bit-identity method, and my completed sorted P4 table as the starting map of what actually fails.
