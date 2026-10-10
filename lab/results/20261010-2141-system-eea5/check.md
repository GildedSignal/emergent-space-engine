Grade: silver

## Check — run 20261010-2141-system-eea5

**Abstract.** Claim: the rebind-per-kick full trajectory compile is one mechanism behind three bottlenecks (kick cost/tail, per-body memory, encounters re-pay), and the already-adopted jet's honest ceiling is ~1.6× on the median kick, ~10× on the p99 — not 5–10×. Reproduced bit-for-bit on every deterministic field (digests, counts): compiles/kick 1.0 (37 kicks), exact memo sharing 0.0 (31/31 distinct shapes), compile share median 0.365/p99 0.908 (my rerun 0.376/0.9086); bytes_per_body 1203 against a verified 16-byte Tube (75×), stats.kicks 0 at 10 s, engine 3.8% vs gather 73%. Adversarial seed 7: sharing still 0.0, share median 0.70, p99 0.91. It kills the 5–10× hope and re-ranks the slice's bottleneck to the view; the jet itself is not wired.

## Reproduction

Applied `work/patch.diff`, built (`cargo build --release -p xtask`, 35.5 s), ran both dossier commands.

- `--kick-bench --seconds 55`: **bit-identical** on `digest`, `replay_digest`, `compile_calls=37`, `compiles_per_kick=1.0`, `refused=0`, `frames`, memo block (`exact_hit_rate 0.0`, 31 exact / 26 quantized of 31 cycles, quantized 16.1%). Timing: compile share median 0.376 (author 0.365), p99 0.9086 (author 0.9078); kick µs ~1.4× the author's (shared box, load 2.46 at author time) — same structure.
- `--bench --seconds 10 --unpaced`: digest identical; `bytes_per_body 1203`, `catalogue_live 28 = bodies`, `stats` identical (`kicks: 0, opens: 34, decisions: 6`); shares engine 3.7% / gather 68% / view JSON 20% (author 3.8/73/17).

Code claims verified by reading: `kick` (step.rs:354) → `rebind` (:381) → `bind` → `bind_in` → `Rebinding::from_state` (bind.rs:226) is the only `from_state` in `crates/universe`; `Tube` = u32+u32+`Words([u32;2])` = **16 bytes**; `bytes_of` (body.rs:170–176) matches the dossier's memory breakdown. law.md's jet citation is verbatim ("about 0.05 compiles per kick", line 35).

## Predictions

`predictions.md` (mtime …8857) precedes every result JSON (…9030, …9055, …9143) and the dossier. P1 hit exactly; P2 missed at the median (0.37 vs ≥ 0.5) and is reported as missed; P3 badly missed — and that miss is the run's most valuable finding (the slice's bottleneck is the view gather, not kicks); P4 half-held and reported as such. Gold's "the held-out predictions held" fails by the letter.

## Adversarial cases

1. **Seed 7 kick-bench (55 s):** `compiles_per_kick = 0.988` (82 compiles / 83 kicks, `refused=0`) — one kick resolved as a Kick with **zero** compiles: `kick_clock` rebinds only when fired (step.rs:617–618). So "every kick pays exactly one full trajectory compile" is scene-true, not law-true. Conclusions unchanged: `exact_hit_rate` still 0.0, compile share median **0.70**, p99 0.91 — the compile is even more dominant off the tuned scene, and the p99 ≈ 0.91 tail claim is robust across seeds.
2. **55 s horizon bench (seed 1):** `stats.kicks = 16` (not 0), engine 3.6%, gather 74.8% — kicks are rare but the 10 s zero is a window artifact; claim 4's substance (view dominates, kick lever is a scale lever) holds. `bytes_per_body = 2351` with the fleet's leavers (Passage = flat 4096 B): the 75× gap is a floor, strengthening the memory hat.
3. **Structural:** no `from_state` callsite in `crates/universe` outside `bind_in` (checked); the instrumentation brackets exactly that call; the bench replays pending kicks out-of-band (update digested, never applied), which reconciles 23 replayed kicks with `stats.kicks = 0` in the same window.

## Novelty

HISTORY.md has no measurement of kick compile share, of the live bytes-per-body gap, or of the slice's engine/view split. The 0% exact sharing and ~99%-recompile were known (board, 5 Oct; cited honestly in predictions.md); what is new: the 37%/91% split, the 1203 B/body vs 16 B accounting, the ceiling (kills the 5–10× hope), and the re-ranking of the current slice's bottleneck. The encounters hat is cited from components-4643, not re-measured (admitted in the lens section).

## Goal fit

Focus #1 (kicks), #5/`shipmem` (10⁹ in 8 GB) and the re-pay risk, all named on the board. Principles 3 and 6 are quoted and apt: the post-kick trajectory is derivable from the pre-kick one plus an offset; the offset is the compressed generator. The correction "the kick lever is a scale lever, not this slice's bottleneck" is decision-grade for the integrator's ranking.

## Why silver, not gold, not lead

Real and exactly reproduced, but: no 10× is delivered (a ceiling is measured; the lever is not wired), two of four held-out predictions missed (honestly), and the unification's third leg is cited rather than measured. Not lead: it is reproduced bit-for-bit, it kills a hoped-for 5–10× (principle 9: a failed configuration), and it re-ranks a board assumption with numbers the shipped code regenerates.

**The one experiment for gold:** wire the jet for one doll's ships (integer offset from entry, the memo's ∂/∂E, ∂/∂L multiply-add, re-anchor when the offset reaches √(floor/C)), re-run `--kick-bench` and the existing gates: expect ~0.05 compiles/kick, kick p99 −~80%, B5 exponent ≤ 0.2, B12's Jacobi holding. Budget: one directed build — exactly what the dossier names.

## What the author missed

- `compiles_per_kick` is not structurally 1.0: `kick_clock` compiles only when fired (seed 7: 82/83). The claim should read "one compile per kick that rebinds".
- The compile share is scene-dependent (median 0.37 on seed 1, 0.70 on seed 7): the jet's median ceiling is a range 1.6–3.3×, not a number. The dossier generalizes from one scene; its "not 5–10×" conclusion survives, but by a narrower margin than written.
- The third cited run (median 0.359) has no JSON in the folder — two of three runs are on the record; my reruns (0.365 saved, 0.376 mine) support ~0.37, but the taste log's trap ("numbers the shipped code cannot regenerate") applies to that one figure.
- The p99 tail rests on 12 leaver samples (p99 = second-largest of 37); the 10 s run gave p99 0.62. Tail statistics are thin; direction consistent.
- Machine state is half-recorded on Linux (therm/batt/loadavg "unavailable" — macOS `sysctl` paths); the bench JSON carries loadavg via `uptime`, the kick-bench JSON nothing. The tool should grow Linux probes.
