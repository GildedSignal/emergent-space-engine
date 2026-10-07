Grade: silver

**Abstract.** Claim: frame cost is member-flat to 4×10⁵ at rtf 100 (frame p99 ≈ 11 ms, no hitch) while the 5 ms budget converts a ~30 ms true tail into a 27–30% silent deferral that rtf_median (pinned at 100.0) cannot see; knee in rtf, not members; player's doll 30× a ship. Reproduced on clean main + patch: 49,152 row (fp99 10.13, engine p99 5.62 ms, overflow 96/360, ev/s 2.26e3, digest bit-identical `4ec59efc…`), 393,216 row, capped ≡ uncapped digest at one cut, player 1,881 µs vs ship 64 µs, burn/coast 0.90, rtf floor 310 seed-stable. Adversarial: on a 20 s paced run the deferral amortizes to 8.4% (coverage 91.6%) — the 27–30% headline is short-run; maxrss 50 MB, not 120; "p99.9 ≤ 13 everywhere" contradicted by the author's own m3072x runs (18.5 ms). Adopt: ~20-line resolution-rate line in dash.rs.

**Reasons.**

*Reproduction (clean tree at origin/main `70f27a9`, `git apply work/patch.diff`, rebuilt, load 0.95).*
- 49,152 members, rtf 100, 6 s, seed 1: frame p99 10.13 (author 10.17), engine p99 5.62 (5.60), worst 10.8 (12.7), overflow 96/360 = 26.7% (97), ev/s 2.26e3 (2.26e3), slices 6,322 (6,315), digest bit-identical `4ec59efc352fe240…`.
- 393,216 members: fp99 10.59 (11.04), overflow 98/360 (111), digest identical. Member-flatness and outcome-flatness hold: 768 → 393,216 all give the same digest at the same cut; uncapped 6 s at 768 and 49,152 give byte-identical stats (slices 7,651, kicks 4,075).
- Player eval 1,880.8 µs vs ship 63.9 µs (29.4×), fleet slice 40.4 µs; burn/coast engine p99 0.90 (author 0.91). Burn windows in `analyze.py` match `script()` in `xtask` (`n % 240 < 20`).
- rtf floor: 49,152 members at rtf 1,000, seed 2 → rtf_median 309.7, matching seed 1's 309.8 — the floor is seed-stable at that point (the author had flagged it untested).
- `predictions.md` predates all `run-*.json` in file order; P2/P4 held, P1/P3/P5 honestly scored as wrong-informative. Exemplary prediction hygiene.

*Adversarial findings (mine).*
1. **Deferral is front-loaded, not steady-state.** Paced 20 s at 49k: coverage (presented/cut) 91.6%, overflow 126/1200 = 10.5%, vs 84.8%/111 at 10 s. The absolute deficit is roughly constant (~150–170 game-s): warm-up debt that amortizes. The dossier's "27–30% silent deferral / 68–73% resolution" is a 6–10 s window measured mostly during warm-up; steady state is ~8–15%. The qualitative finding stands; the headline number overstates steady-state ~3×.
2. **Deferral never touches outcomes.** Capped and uncapped runs at the same cut give the same digest (`4ec59efc…`), and code reading closes the author's open question: `frame_to` sets `now = horizon` where the horizon is the smallest unresolved deadline − 1, so the view can never read unresolved state. Deferral is exactly game-clock lag, never wrong light. The author left this to "a view-side check I did not run"; it is answerable from the code plus the digest.
3. **rtf_median is pinned by construction.** `want = rtf × wall_dt`: an unpaced frame faster than 16.7 ms presents exactly rtf × wall, so per-frame rtf can only fall below target on horizon-clamped (overflow) frames — hence median 100.0 at 27% overflow. The dossier presents the pinning as an empirical observation without the mechanism.

*Record defects (small, but the checker's job).*
- "p99.9 ≤ 13 ms everywhere" is contradicted by the author's own runs: m3072x1000 p99.9 = 18.45, m3072x10000 = 18.17; "zero 16.7/33/50 ms frames in 15 runs" silently excludes exactly those two grid runs (3–4 frames above 16.7 ms each).
- The deferral metric "1,052 slices/game-s vs 1,435 required" is mislabeled: it is slices per nominal run-second (60 Hz frames), not per game-second; per presented game-second the uncapped number is *lower* than the capped one (27 vs 41). The ratio is real on the chosen metric, but the clean metric — `presented_tick_at_end / cut_tick`, already in every JSON — goes unreported.
- "393k bodies ≈ 120 MB here": measured maxrss 50.4 MB (and 48.5 MB at 768 members — memory is member-flat on x86 too, since members ride the fleet's lattice world generator).
- "true engine demand p99 ≈ 30 ms" is specific to the 3 s uncapped shape; at 6 s uncapped I measure p99 18.1 / max 45.

*Novelty.* No H entry measures members scaling, rtf floors, deferral, or cost-by-kind on the plane. Nearest: H0210 (frame p99 2.45 ms at one configuration) and docs/plane.md §7, which *predicts* overflow "becomes a brief, smooth dip of the real-time factor" — this run shows the dip is neither visible in the median nor brief at 6 s, a real correction to the doc's expectation.

*Goal fit.* Board #4 verbatim: smoothness and the allocator, p95/99. Deletes work: no members-based capacity scaling, no player-decision debouncing, no members-driven view culling — and it points at the lever the board already holds (player eval 1.9 ms ≈ kick-window setup, consistent with gold components-4643). PRINCIPLES: "no work for no reason, so no ticks" (14) measured as the plane's cost law; "your dials are made up and hold no informations" (28) — rtf_median is exactly such a dial. It respects every lab rule (crates untouched, patch is a 20-line instrument, ≤ 60 s runs, load recorded).

**The one experiment to gold.** A steady-state service-level run: long paced runs (≥ 60 s) at 49k members reporting `presented_tick_at_end / cut_tick` (and its p99) as the capacity number, with the pinning mechanism and horizon-clamp correctness stated, the resolution-rate line landed in `dash.rs`, and the three defective numbers above corrected. Everything else is already gold-grade: bit-identical reproduction, pre-registered predictions, a premise shown wrong (members price nothing at 64×), a deleted workstream, and a one-step adoption.

**What the author missed.**
- The long paced run: their deferral headline is warm-up, and they had the coverage metric in every JSON they saved.
- The mechanism (want = rtf × wall_dt) behind the median's pin, and the horizon clamp as the proof that deferral can never corrupt the view — both one code-read away, and together they convert "silent deferral" from an interpretation into a theorem with a number.
- maxrss (memory is member-flat too — the M1 caveat is weaker than claimed, in the claim's favour).
- The marginal contradictions with their own m3072x JSONs, and the units on the slices metric.
- Single-seed floors elsewhere in the rtf sweep (only the 310 point is now seed-checked, by me).
