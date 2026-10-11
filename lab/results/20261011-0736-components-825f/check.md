Grade: silver

**Abstract.** Claim: the plane's frame allocator is at its floor — idiot index 1.01, 99.6% of engine work has zero light-cone slack — so there is nothing to build in the scheduler; at 428 bodies the mandatory demand itself (steady p99 ~6 ms, spinup 20–45 ms) exceeds the 5 ms budget, stalling presented time (rtf lowest-1% = 0.0) without hitches. Reproduced: the digest triple bit-for-bit (`3db02d3d…` traced/untraced/`--engine-ms 10`), idiot index 1.00, deferrable share 0.3–0.4%, slack median 0, and it holds on seed 2. Gain: deletes the "better scheduler" branch at zero adoption cost. But the demand-tail diagnosis is mis-attributed: the player's motion-law step is flat in members; the O(members) term is the PlayerNeighbourhood scan (encounter.rs:53), so the proposed doll-aggregate moment source would change nothing.

## Reproduction (clean tree, `git apply work/patch.diff`)

- Build 35 s; all four dossier commands ran under 60 s each. Digests reproduce **bit for bit**: traced m400, untraced m400 and b10 all `3db02d3d…`; m48 traced `41343a14…` = the author's saved baseline. P6 holds exactly.
- My traced m400: engine wall p50 0.128 / p99 5.31 / max 6.42 ms; mandatory p99 5.28; deferrable p99 0.00, share 0.4%; rekey mean 0.022 ms; **idiot index 1.00**; slack median 0.0 / max 0.1 frames, 0% ≥ 10; player entity 27 = 437.8 ms of item time, battle entity 428 = 195.3 ms (worst item 3.0 ms); kind-B p50 41 µs; demand-by-deadline steady p50 0.04 / p99 5.9 / max 16.6 ms, spinup bins 18–45 ms; causal flattening ratio 1.00×. All matches the dossier within shared-box wall noise.
- Wall-dependent counts differ with load, as expected: overflow frames 117–123 in my runs vs the author's 159 (their untraced run itself says 158); kicks 9079 vs 9007. The dossier correctly leans on the digest, not these.
- Entities 0–26 (the base scene, shipped ships included) resolve **zero** items in both arms; 402 entities with items = 400 members + player + battle. Confirmed.
- b10: overflows 26 (author 30), rtf lowest-1% 19.83 (19.8), engine max 10.69 ms (10.85). Confirmed.

## Predictions

`predictions.md` mtime 07:52:02 precedes every traced artifact (first traced run started 07:52:07 per its own `uptime_before`) and its exploration numbers match the saved baseline JSON. Held: P4 (rekey 22–24 µs), P5 (overflow frames' wall ≈ budget + one item; maxitem p50 1.1–1.6 ms), P6 (all three digests identical — verified bit-for-bit). Failed and reported as failed: P2 (0.4% deferrable, not ≥ 70%), P3 (slack 0, not ≥ 10 frames); P1 half-wrong with an honest correction (player is ~20% of overflow mandatory work, 1 item per frame). This is the discipline the lab wants.

## Adversarial cases

1. **Seed 2, members 400** (unseen by the author): idiot index 1.00, deferrable 0.3%, slack median 0, player 1497 µs/item. The floor finding is not a seed artifact.
2. **The mechanism probe** (scratch instrumentation of `resolve_body`'s player path; probe sums reconcile with the traced player totals to 1–2%): at 48 → 400 members, `step::process` (the motion-law v2 step, which contains `ext.rs:149`) is **flat**, 41.7 → 40.0 µs/item; `encounters_for_player` is the scaler, 238 → 1463 µs/item (85% of the player item at m400).
3. **Members 4000** (clamp raised in a scratch build; 3838 bodies at report): encounter scan 650.8 ms vs step 2.2 ms — still the scan, still ~3–4 µs per body per player item.

## Novelty

The allocator's history (H0158–H0165, `work-allocation-design.md`, `work-allocation-principles.md`, `emergent-allocator`) is all on the lattice engine. No HISTORY entry measures the plane's frame allocator, its mandatory/deferrable split, or an idiot index; the dashboard's `rtf.lowest_1pct`/`overflow_frames` pre-exist (base tree) but were never decomposed this way. The inversion of constraint-986f is a premise check I cannot cross-read (that run's folder is not on this branch), but the measurement here stands on its own. Novel on this tree.

## Goal fit

Board #4, and PRINCIPLES 5 measured against 12: "light cones partition compute" — on the scene the player actually flies, they partition nothing (flattening ratio 1.00×), because every event is at the player. The "no build in the scheduler" conclusion is well earned and the stall-not-hitch distinction (presented time freezes while frame times stay ~10 ms) is the right observable.

## Why silver, not gold

The claim's demand-side half is wrong where it is actionable:

- **The mechanism is mis-attributed.** "The motion-law v2 kick loops over the doll's `sources` (`ext.rs:149`), and every member handed into the doll is pushed there (`universe.rs:427`)" — false. Members are made by `resolve_handout` with `gm = 0` and never enter `sources[d]`; `sources[home_doll]` is `[Moon]` for the whole run (only `make_source`, scenario.rs:186, ever pushes). The kick's cost is flat in members (measured above). The O(members) term is `PlayerNeighbourhood::find` (encounter.rs:53), an O(all bodies) scan per player item — the seam the repo itself already names ("the Binet cone later", encounter.rs:1–4), i.e. the board's existing encounters line, not a new discovery in the kick layer.
- **The proposed redirect aims at the wrong component.** A doll-aggregate moment source (one multipole per doll) touches a list that never held members; it would not move the player's item at all. The correct levers are the encounter seam and the battle slice (the second lever, entity 428 at up to 3.0 ms, is correctly identified).
- **"At 10⁶ members one player step is hours"** is wrong by ~3 orders of magnitude: the author's own slope (3.5 µs/member) and my probe (~3.7 µs/body) both give ~3–4 s per step. Still fatal per frame, but the number matters for what it says about urgency.
- P2 and P3 did not hold (disclosed), so "held-out predictions held" is not met either.

The floor measurement itself is gold-grade; the diagnosis attached to it is not adoptable within one step.

## The one experiment for gold

Decompose the player's item (the probe above, or equivalent) inside the run itself and re-derive the levers from it: encounter scan (encounter.rs:53, the Binet-cone seam) first, battle slice second. Fold that correction into the claim and the redirect, and the result is adoptable as it stands.

## What the author missed

- The `sources` loop was never member-fed: one grep for `make_source` call sites (there is exactly one, the Moon) kills the mechanism claim before any timing is needed.
- The 337/1560 µs pair is from the pre-trace exploration; the traced artifacts regenerate 374/1727 µs (same slope, 3.8 µs/member) — the dossier presents the exploration numbers as the measured ones.
- "At 1 AU a body's deadline is ~198 frames out" — it is ~299 frames at rtf 100 (499 s of light travel / 1.667 s per frame). The qualitative point survives.
- The trace's player item includes work that is not the player's (fleet slices, hand-outs and ship pulls run inside `resolve_body`'s player path, universe.rs:571–582) — the "player's own motion-law step" framing hides that ~9% of the item is pulls and that the encounter check, not the step, owns the tail.
