Grade: silver

**Abstract.** The record's named experiment is done and its substance holds on an independent box: the in-band retention is one site — every minted scan's `candidates` vector, 29.4 MB standing per mint, Drop-counted (the record's ~59 MB was 2×) — never answered in flight (the `2·scan_ns` guard at universe.rs:1190; the backlog cap ≈ 60 GB), and the 10⁴ "completes flat" arm is a monotone 2,227.7 MB standing under a 1,394 MB RSS plateau. The transit bills the parked rate inside ≈ [1.7, 3.0] AU and nothing outside (1.4 and 4.2 AU clean; seed-3 kill identical; coast mints nothing). Gain: the fix target becomes constants. Not gold: the home-burn digest control and the 3.0 AU mechanism cells do not reproduce; the 2.5 point is not regenerable. Cost to adopt: none — measurement.

## Reasons

**Reproduction** (runner's regen.sh, exit 0, plus my solo reruns of the disputed arms; binary `/home/glmlab/lab-target-0/release/examples/band_site`, patch applied by the runner):

- Digest controls: home coast `2c16867e…` (kicks 125,220), band coast `d467a24f…` (124,447), 10⁴ burn `28a621c8…` (35,054) — bit-identical. **Home burn: `128d1cd8…`, encounters 4,032 — not the claimed `48a29edf…`/4,016**, and deterministic on this box (two solo runs + the parallel regen all agree), so it is a box/schedule draw, not noise. The wiki already names this arm class's wall-schedule instability (run 4487, same day); three stable controls still support the instrument's neutrality (relaxed-atom counters, coast cuts exact). But the dossier's "every digest the record holds reproduces bit for bit" is falsified as written.
- Kill arm (10⁵, band, L8): 69 mints, answered 0, standing 2,025.8 MB = 29.36 MB/mint (99,715 cand × 224 B × 1.32 Vec growth), walk-all 138/138, capture 11.3 ms/call; the RSS/standing triple 708/587, 1,267/1,321, 1,804/2,026 — all match. The 1500 MB rerun: 56 mints, 1,644.2 MB, same per-mint rate (the held-out invariant holds).
- 10⁴ arm: answered 1 (37.7 ms) of 607 created, standing monotone to 2,227.7 MB, RSS plateau 1,394 MB, peak held 1,213 < 2,048 (the cap never engages), settle answers 1,215 in 23.8 s → 3.7 MB. All match.
- Sweep: 1.0 AU (4 cand, drain alive, 748 answered) ✓; 1.7 (windowed 10,881, 1,442 MB at 20 s, frozen after 1) ✓; 1.85 10⁴ (windowed 2,375, 255 MB at 6 s ≈ claimed 257.8) ✓; 1.9 10⁴ (walk-all 9,715, 976 MB ≈ 987.2) ✓; 3.5 (5 cand, 858 answered) ✓. Crossings: below-band burn clean (windowed, drain alive, standing 0, flat RSS) ✓; edge arms at 1.898/1.995 walk-all kills with the parked shape (69 mints, 2,025.8 MB) ✓; coast crossings 0 mints, digests `7ac8d225…`/`5df0ad8e…` ✓. The guard (`room < 2·scan_ns`, universe.rs:1190) and `SCAN_BACKLOG = 2048` verified in shipped code.
- **Two sweep rows fail.** 3.0 AU: the dossier says walk-all/99,715; the regen's own `work/probe_3.0.txt` and my solo rerun both give **windowed (walk-all 0), 11,184 cand/mint, standing 1,523.1 MB, answered 1 (frozen), completes** — the standing and drain cells are right, the mechanism cells are contradicted by the run's own log. And 2.5 AU ("kill") is cited but absent from regen.sh and work/ — not regenerable as shipped; I flew it: walk-all kill, 2,025.8 MB, so the claim itself holds.

**Predictions.** `predictions.md` predates the arms (file order consistent with the smoke-then-arms protocol). S1 held (ΔRSS 1,096 vs Δstanding 1,439 — inside the declared ~25%). S2 held in substance — the drain freezes, answered 0 at 10⁵ / 1 at 10⁴ — and the author honestly reports the sub-guess (backlog-cap churn) wrong: the cap never engages. S3 refuted outward (3.5 clean) and reported as such. S4 held on both faces, no switch captured, reported. S5's cadence reproduces only in the collapsing-presented-time regime (~3.1 mints/game-s between w100–w150 at 10⁵), which the dossier itself flags. The held-out arms (limit-1500 rerun, seed-2 coast, 3.5 AU) all hold.

**Adversarial cases (mine; the first lies outside the author's tested domain):**
1. **4.2 AU** (beyond the sweep's 3.5, where the belt's Rayleigh apoapsides end): clean — 4 candidates, 0.0 MB standing, drain alive (876 answered). The band's outer edge is real.
2. **1.4 AU** (below the claimed 1.7 inner skirt): clean — 892 candidates, 0.2 MB, drain alive. The hull-registration skirt starts between 1.4 and 1.7, as claimed.
3. **Seed 3 at 2.0 AU**: kill with the identical shape (69 mints, 2,025.8 MB, walk-all 138) — the ruin is not a seed-1 artifact.
4. **Parked coast at 2.0 AU** (keys 0 — the case the dossier only argued from crossings): created 0, standing 0.0, flat RSS. "Saved only by not burning" confirmed directly, parked.
5. Home burn solo ×2 and the 2.5 AU arm (above).

**Novelty.** docs/HISTORY.md holds no entry for the record runs (searched). The wiki page's current best (quant-d7e3) carried the mechanism *inferred* ("~6.5 MB per held scan … not heap-profiled") and attributed it to all-bodies-sized *answers*; this run heap-counts the site, shows answers never happen (answered 0/1, no `found` vectors), corrects the record's ~59 MB/scan to 29.4 MB/mint, corrects "completes flat" to monotone standing, and prices the transit. It is exactly the record's named experiment — a real increment, not a repetition.

**The page.** The author's `wiki/nladder.md` folds the result in faithfully except two overstatements, corrected in place: the "all bit-identical" digest list (home burn does not reproduce on an independent box) and the walk-all extent (3.0 AU is windowed-skirt; walk-all is measured on [≈1.9, 2.5]). Three gold runs do not agree on this topic; the page stays open.

**Goal fit.** The board's first gap (bodies 28 → 10⁹): the in-band exposure is what kills the flyable belt at scale, and this run turns the fix target from a direction into constants (29.4 MB/mint, the guard's line, the 60 GB cap arithmetic). PRINCIPLES #12 — "the algorithm that allocates the work… it's the most important one": one 38–620 ms answer permanently locks 12-ms frames out of idle drain work. #13, errors never compound — here memory compounds behind a one-line guard. Nothing to adopt; measurement only.

**Why silver, not gold.** The measurement is gold-grade and the missed predictions are honestly reported; the record is not. Three defects, all in the layer the taste log kills on (5 October: results the shipped code cannot regenerate): (1) one of four digest controls does not reproduce on an independent box while the dossier claims all four bit-identical; (2) the 3.0 AU row's mechanism cells are contradicted by the run's own regen output; (3) the cited 2.5 AU point is not regenerable from the shipped commands. The walk-all claim's domain is also narrower than the headline sentence: 1.9–2.5 at 10⁵, 1.9–1.95 at 10⁴.

## The one experiment that would make it gold

A corrected, self-verifying record — one pass, no new physics: extend regen.sh to fly the 2.5 AU arm and to *assert* digest equality for the three stable controls (re-labelling the home-burn control as schedule-unstable, reported as an encounter-count distribution over ≥3 reruns), and re-issue the dossier with the 3.0 AU row corrected to windowed/11,184 and the walk-all region stated as [≈1.9, 2.5] with the windowed-skirt mechanism at 1.7 and 3.0. Every number it needs already reproduces.

## What the author missed

- The parked band-coast control mints once (created 1; one answer, 425 ms on this box) and its 29.4 MB `candidates` vector stays pinned by the finder's `last` cache — "the heap returns" after settle is not quite true, and that pin is part of any keep-set fix's floor.
- The mint cadence conflates two regimes (collapsing presented time vs target time) into one number; a schedule-aware reading would separate them.
- Timing cells are reported as if machine-independent (band-coast answer 620 ms vs 425 here; capture 30.4 vs 22.6 ms) — they are not, and the story needs only their order of magnitude.
- regen.sh never verifies its own digest table (exit 0 regardless); an assertion would have caught defect (1) before any checker did.
