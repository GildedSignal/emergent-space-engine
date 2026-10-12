Grade: silver

**Abstract (for the integrator).** Claim: the plane's frame is readout-bound below ~500 bodies (68–89% of measured frame time) and budget-bound above (26% overflow at 480 members, ~100% at 4,000); its memory is orders off the 16-byte tube; and the dashboard's `bytes_per_body` under-reports by charging Passage tubes a flat 4 kB. Reproduced: readout shares and **exact digests** at 4 and 48 members; peak RSS 845.9 MB at 4,000 members (author 845.4); per-handout RSS 15–23 kB early rising to ~400 kB at handout #3,600; the flat-4096 in `body.rs:174` and the 400-member clamp verified in code. Adopt in one step: fix `bytes_of`, lift the clamp. The memory-scaling headline is contradicted in part by the author's own unreported 40,000-member run.

## What reproduced (clean tree, `git apply work/patch.diff`, release build, seed 1)

- **Digests exact:** m4 S=8 `6af71966…` and m48 S=8 `29f440d6…` match the saved JSONs byte for byte; all engine counts identical (kicks 633, opens 75, items 915/79/2200). (An earlier one-nibble "mismatch" at m48 was my own transcription typo — the file is clean.)
- **Shares:** m48 engine 0.250 / readout 0.750 (author 0.252/0.747); m4 0.107/0.893 (author 0.11/0.89); m4000 readout 0.886, overflow 478/480 (author 479).
- **Memory headline run:** m4000 S=8 peak RSS **845,944 kB** (author 845,392); `PROBE handout` deltas ~15–23 kB/handout at #0–450, **19–22 MB per 50 handouts (~400 kB/handout) at #3,550–3,700** — the author's numbers, regenerated.
- **Code claims verified:** `xtask/src/universe/mod.rs:32` clamps `--members` at 400 (stock cannot be asked the question); `body.rs:170–177` counts Cycle knots exactly but charges `Passage(_) => 4096` flat; `orbit.rs:910–978` — Passage really is an `Arc<OrbitShape>` knot table plus a 15/16-shrinking `(Scalar, Integral)` tail. The instrument-lie finding is real and the fix is one afternoon.

## What did not hold

1. **"N=40,000 was not run … the plane cannot be constructed at 4×10⁴ members on this box" is false.** `data/bench-m40000.json` is a *completed* run in the author's own folder (digest, machine_after 10:37:40, 47.7 s, 12,420 bodies, 12,392 leavers) — an undisclosed run contradicting the dossier text. My reproduction constructs it too: flat **11–60 kB/handout through handout #12,350, RSS ~241 MB at 12.4k live bodies** (~19 kB/body).
2. **"Per-handout cost rising with body count" is the wrong attribution.** At 40,000 members with 3.4× more handouts and 5× more bodies than m4000's blow-up point, the probe stayed flat — because the author's m40000 run did zero kicks (presented tick 136: construction only). The acceleration tracks **battle churn** (m4000: 2,139 kicks, 2,109 encounters), not N. My own m40000 continued past #39,200 and *there* the deltas explode (0.2–5 MB/handout, RSS 5 GB) once game work starts. So "~330 kB/body, growing with body count" is regime-dependent, not a law: ~19 kB/body construction-dominated, ~10⁵–10⁶ B battle-dominated.
3. **Digest reproducibility under overload:** m480 digests differ across machines/loads (presented tick 127.19M author vs 122.99M mine) — the "independent of schedule and budget" note holds only when the engine is not saturated. The dossier leans on "digest reproducibility is the harness's own" without this caveat.
4. Prediction 2 failed as written ("~0 overflow at 480": actual 125/480). Disclosed honestly, and the falsifier they pre-registered (engine share ≥60%) was not the right one.

## Novelty

The readout's dominance is known (H: "the view gather is 83% of a light frame", kicks 29 µs; board focus item 5 names the 10⁹-in-8-GB question). New here: the members-ladder quantification (shares and overflow bracket), the flat-4096 instrument lie, the clamp, and the per-handout probe. No prior entry measures `bytes_of` or per-handout memory.

## Goal fit

Real and on-focus: it arms the B18b/shipmem memory design with an honest instrument and shows the *frame* (readout), not the kick law, is the wall below ~500 bodies — "The cheapest compute is compute not done" (1), "deeply aware of von-neumann bottleneck and memory" (17). Nothing here weakens a gate. The lens caveat (readout is a debug view; kick builds are physics) is fair and the integrator may still order the queue by physics.

## The one experiment for gold

An attribution run that separates the two regimes: the members ladder crossed with a no-battle (construction-only) variant, plus one heap profile of a battle-churned m4000 frame — deciding whether the ~400 kB–5 MB per-handout cost is allocator transients or retained state, and so fixing the true steady-state marginal (17–60 kB vs ~330 kB) that the 20,000× idiot index is computed from. The author's own m40000 file is half of this experiment and should have been reported.

## What the author missed

- The completed m40000 run sitting in `data/`, contradicting "was not run"/"cannot be constructed" and softening their own headline; leaving it undisclosed is exactly "a headline the log contradicts".
- The regime confound: handout count, live bodies and battle work co-vary in their ladder; the probe cannot separate them as run.
- The digest's load-dependence under overload (m480/m4000 numbers are single-load snapshots; overflow and bodies move with machine speed).
- `run.log` is empty: the PROBE evidence existed only in a lost stderr (I regenerated it; it does reproduce).
