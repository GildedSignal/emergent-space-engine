Grade: gold

The shipped loop logs player key changes at the frame's presented tick, so load and frame rate rewrite canonical history; this run measures that the divergence compounds (0.31→2.3→18 AU rich-vs-starved on identical inputs, ×7.5–7.8 per 3× game-time, contacts 6 vs 54) and ports the a342 `sched`+decision-quantum fix to the current tree, wired into `session.rs` and `kick_bench.rs`: one digest across 30/60/144 Hz, load, rtf 100 and 1, 48 and 400 members, at 0.05–0.15 s measured input lag. Suite 69/0/2. Adoption is one patch (+34 lines, regression tests included); it should land before the in-flight flight recorder freezes logs and turns machine load into merge-gate verdicts.

## Reproduced

Clean tree, `git apply work/patch.diff`, `bash regen.sh`: exit 0, 6/6 HELD, every digest, logged tick, encounter and contact count bit-identical to the author's stored matrix (only `wall_ms` differs — machine noise, as the lab rules expect). `cargo test --release -p emergent-universe`: 69 passed, 0 failed, 2 ignored (run twice); the `decision_tick` regression tests pass; `xtask` builds, so the wiring claim is real. Predictions were pre-registered (file times: predictions.md 12:57, decisive runs from 13:05) and the held-out items (ladder, straddle, 400 members, current-tree behavior) were genuinely untested when written.

## Adversarial (mine, beyond the author's domain)

1. **Next decade of the ladder** (cut 2.268G ticks = 11,202 game-s, 3× the author's top): separation 22.9 AU — ×1.27, not ×7.5. Growth **saturates at system scale**; the dossier's "the effect grows without bound" is wrong as a literal claim (the histories stay divergent: 339 vs 405 encounters, 58 vs 142 contacts). Page corrected in place.
2. **Seed 7** (author ran only seed 11): raw four arms → four digests (enc 43/28/43/43, same starvation pattern); fix four arms → one digest. Hole and fix both reproduce off the author's seed.
3. **144 Hz starved** (combination the author never ran): fix → the same 711b3acf digest.
4. **Two presses inside one quantum** (0.30 and 0.31 s, both in [0.25, 0.5) — a path the author's scripts never exercise, and the natural worry for `schedule`'s write-order rule): both decisions logged, in order, at the same quantum tick 10,151,272; `input_err=0`; one digest across 30/60/144 Hz and load. No silent drop, no refusal (t == last_decision is legal; refusal is unreachable since a second press in the same quantum cannot snap below `now`). Sub-quantum intent collapses exactly as declared — and raw mode collapses at frame resolution the same way, so the fix introduces no new mechanism, only a coarser one.

## Novelty

The hole is 40c0's (gold, docs/HISTORY.md:380); the fix is a342's (ungraded, unmerged, pre-clock-merge). This run adds: the compounding measurement (refutes the "bounded offset" reading and makes the recorder-gate argument concrete), the port through five days of merges into the shipped loop with regression tests, and closure across rtf, members and rates. The wiki page and dossier attribute all of this correctly. Not a repetition: a342's fix was going nowhere without a port someone checked.

## The page

Faithful after my corrections: saturation added (my run 1), the unverifiable "a342 had measured it, same ticks" replaced with what the record here shows, and 40c0's grade fixed to gold per docs/HISTORY.md (the page said silver). Topic page `decision-log` is a justified split from frame-cost (its "one live contract hole" paragraph names this exact leak and says the fix is not on main).

## Goal fit

AGENTS.md Truth: "Canonical outcomes are exact and independent of cache, partition, observation, schedule and hardware" — the shipped interactive loop broke this, measurably worse than known (compounding, contacts 6 vs 54 on identical inputs); the patch restores it at one integer add per frame. PRINCIPLES #13: "divergence is not a joke and it compounds" — here, measured, then deleted. It unblocks the in-flight recorder (HANDOFF, `wt/recorder`) whose `--replay-all` gate would otherwise flag load, not regressions. The mechanism is not new, but the premise it kills ("bounded offset") and the one-step adoption are.

## What the author missed

- "Grows without bound" is false at the next decade: saturation at ~23 AU by 11,202 game-s (system scale). The compounding claim only lives in 415–3,734 game-s.
- The dossier carries two contradictory "No regression" paragraphs (69/0/2 and 58/58); the true count on this tree is 69/0/2. A leftover, not a fabrication (58/58 is an older tree's count), but sloppy in a dossier whose currency is exactness.
- The double-press-within-quantum path was never exercised (I ran it: clean, but it needed running to say so).
- The playability price (up to 0.25 s input lag) is measured but never flown; the author flags this honestly — the integrator owns the judgment, and the follow-up (snap to the input event's own wall timestamp) is already named.
