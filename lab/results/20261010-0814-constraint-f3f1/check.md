# Check — run 20261010-0814-constraint-f3f1 (checker: fresh session, 10 October)

Grade: silver

**Abstract (for the integrator).** Claim: on main (741d05e-era tree, digest-anchored) the frame's constraint is the view gather — 0.62–0.72 of frame time, 94–96% of it in per-body retarded readouts, bimodal ~11–15 µs (tube path) vs 28–95 µs (read lands in kick machinery), worst frame 13.4–15.5 of 16.7 ms at 417 bodies. Reproduced: digest `6ce636fa…` exact (patch bit-neutral), gather 0.66 vs author 0.67–0.72, per-readout 11.6 µs cheap / 57.7 µs expensive, kick-bench digest and 35 µs median exact, gates identical verdicts. Survived my attacks: seed 7, rtf 400, unpaced, m1000. Gain: orders the queued work (readout before slack skin, priced 4–6× gather cut). Cost: none (measurement only). Headline dominance was already known (H0210: "the view gather is 83% of a light frame"); the decomposition, bimodality and scale point are new.

## Reproduction (clean tree, patch applied by me)

- `cargo build --release -p xtask` (CARGO_TARGET_DIR is `~/lab-target-1`); `xtask universe --bench --rtf 100 --seconds 20`: **digest `6ce636fa…` identical** to both the author's pre-patch run and their post-patch recheck — tree identity and bit-neutrality both confirmed in one shot. Gather share 0.661 (author 0.674–0.720), engine 0.210 p99 5.19 ms, 0 hitches, worst 15.6 ms (schedule tail; author 11.8 — same box, shared load). Last frame cheap mode in my run: 59 readouts, 11.6 µs/readout, depth-1 18.9 µs vs deep 11.1 µs — matches the author's cheap-mode rows exactly.
- Bimodality: my `gather_ms_series` shows both modes in one run (0.72–1.2 ms cheap, 3.4–4.7 ms expensive), like the author's s55 three-regime series and their recheck. The mode mix moves with the wall schedule, as claimed; both modes appear in every run.
- `--members 400` (15 s): 417 bodies, gather p50 6.08 ms share 0.604, engine overflow 259/900, worst hitch 14.4 ms — author: 6.14 ms, 0.596, 271/900, 15.5 ms. Reproduced.
- `--kick-bench` **needs `--rtf 100`** (the dossier's command omits it; without it: 33 samples, wrong digest). With it: digest `eccc7f5a…`, 365/1158 samples, kick median 35.0 µs, leavers 92.1 µs — exact match. Memo exact-hit 0.0 / quantized 0.95, consistent with the taste log's 5 October correction.
- Gates reproduce identically: `behave --law plane` 13 FAILs with the same numbers (B13 60/64 worst 2.12e-2; B14 timeout 60.1 s); `engine-judge` E1–E5, E7, E8 PASS, **E6 FAIL UNSUPPORTED** (missing `prepared-mutants.json`), E9 FAIL phase 1 as designed.

## Predictions

`predictions.md` (08:21:39) precedes the first decomposition run (08:22:05); only the pre-patch whole-frame bench came before, disclosed in the preamble. The author's own grading is honest and matches the files: bodies ≥ 60% held (94–96%), readouts missed low (1.0–1.2 vs 1.2–2.0 — the memo is better than predicted), per-readout overhead held (54–95 µs expensive mode), members half-held (fleets negligible but handed-out members become real bodies), engine-not-the-frame-constraint held (p50 0.26 ms; only the budget tail). Pre-registration is real, not decorative.

## Attacks (mine)

1. **Seed 7, 20 s**: gather 0.62, bodies phase 93% of gather, 16.6 µs/readout, worst 6.5 ms — claim holds off-seed.
2. **rtf 400, 10 s**: engine share rises to 0.28 (p99 3.7 ms, 3 overflow frames) but the gather still leads at 0.62 — the "engine is not the frame constraint" claim extends past rtf 100.
3. **--members 1000**: **saturates at 417 bodies** (m1000 == m400 == 417) — the CLI's scaling axis is capped there; at the cap gather 0.53–0.56 vs engine 0.29, worst 13.4–13.8 ms. Claim survives, but see misses.
4. **--unpaced**: gather share 0.61 — the split is not a pacing artifact (shares are of busy frame time).

## Novelty

H0210 already recorded "the view gather is 83% of a light frame; kicks cost 29 µs" as a limitation, and `b-readout-cost` is already a queued lens (HANDOFF). What is new here: the phase decomposition (bodies 94–96%, observer/fleets negligible), the bimodal readout cost and its schedule dependence, readouts ≈ 1/body (the frame-level memo works), the 417-body worst-frame scale point, and the measured ordering/pricing of the two queued builds. That is a real refinement of where the frame's cost lives, not a new mechanism and not a 10× move — it prices the lever without pulling it.

## Goal fit

Board focus "the plane flies, work goes by its measured bottleneck" and bottleneck 4 (smoothness/allocator): the run measures which constraint binds the *frame* and cleanly separates it from the engine's kick constraint. PRINCIPLES #3 lists "views" among what should be derived, not evolved — the finding that the view is the frame's dominant compute sharpens that tension usefully. #12 (p95/99 smoothness) is directly served. The lens lens-caveat (nothing said against the board's #1 at scale) is correct and honest.

## The one experiment that would make it gold

Implement the priced fix: make the partial-step/kick-window readout take the tube path (the queued `b-readout-cost` build), then re-run this same harness and show the measured 4–6× gather cut (frame p99 10.4 → ~6.5 ms) with the digest-neutral protocol — that moves bottleneck 4 by the measured margin and hands the constraint back to the kick path on evidence.

## What the author missed

- **"E1–E8 pass" is contradicted by the author's own `engine-judge.txt`** (and by my rerun): E6 FAIL UNSUPPORTED, missing `prepared-mutants.json` — infrastructure, not physics, but the dossier line is wrong as written.
- The gate block under-reports: G1–G6, B7, B9 and B10 also fail with `worst inf`/NaN on this box (wholesale, 0/256-style). That *strengthens* the author's oracle-blow-up reading of B11, but listing only B11–B14 invites the misreading that the rest passed.
- **The `--members` axis saturates at 417 bodies** — m1000 gives the same 417. The dossier's "417 bodies" scale point sits at the axis ceiling and cannot be pushed further from this CLI; the per-body gather cost (10–28 µs) is the only extrapolation base toward game scale, and the engine share is climbing with body count (0.20 → 0.26 → 0.29) while the gather share falls (0.66 → 0.60 → 0.53) — the two constraints are converging, invisible at the cap.
- The kick-bench reproducing command omits `--rtf 100` (33 vs 1158 samples without it).
- Minor: the per-body timer includes the doll-depth walk (left-to-right tuple evaluation, `depth(...)` after `Instant::now()`); < 1% of the measured µs, not a distortion.
