# Dossier — 20261017-1018-redteam-13c6 (lens: premise red-team)

## Claim

The view rung r6 now exists, frozen and executed on shipped code with a mechanical verdict — **PASS: the shipped memo-carrying gather holds every bar (rows 38400/38400, median 2.0 readouts/emitter, p99 2.92), while the no-memo `cold` path is killed (median 3.66, p99 6.0, and it silently drops 12/38400 emitters) and the doc's "any cache, however stale or foreign" is killed as a cost claim (poisoned caches: same rows, p99 5.13)** — closing the representation-premises census's named hole that r6 was assigned to GLM (law.md L90) and never created.

## Bottleneck

The census's #2 premise ("the view gathered at the past light cone") was letter-dead but *unguarded*: no gate or rung judged the gather. The board's scoreboard does not yet carry the view as a gap (the gather is 90%+ of the flyable frame at 10⁵ per view.md), so the lever here is guarding what the doc promises: ~1 readout per emitter, and a memo that "adds speed, never error". The rung converts both promises into mechanical bars with a planted-law negative — the cheapest falsifier the §7 ladder was missing. Gain: not a speedup; a certificate (and one killed configuration: the cold fallback).

## Evidence

All numbers from `regen.sh` (Linux/x86 shared runner, deterministic, `threads = 1`; orders of magnitude only — the integrator re-measures on the M1). Scene: `scenario::stream` (bare tubes — the view measured alone), 64 emitters, 5 frozen cases spanning closing/passing/receding streams at β 0.5–0.9999 and observers at β 0–0.9, 120 frames per case at 60 Hz rtf 100. Frozen bars (`r6-view.md`, sha256 `88b4dfaa…`, recorded in `predictions.md` before the decisive run): `rows_found ≥ 0.999`, `readouts_median ≤ 2.2`, `readouts_p99 ≤ 3.2`.

| config | rows_found | readouts_median | readouts_p99 | verdict |
|---|---|---|---|---|
| `warm` (candidate) | **1.000000** | **2.000** | **2.922** | pass |
| `poisoned` (candidate) | 0.999948 | 2.000 | **5.125** | killed (tail) |
| `cold` (candidate) | 0.999688 | **3.656** | **6.000** | killed (med, tail) |
| `amnesiac` (negative) | 1.000000 | 2.500 | 4.000 | fails as required |

`verdict.txt`: **PASS; warm passed every criterion; killed: poisoned, cold.**

Three measured findings beyond the verdict:

1. **The cold path silently drops emitters.** 12/38400 (case, frame, emitter) rows missing, all in the Toward cases (per-case `R6_DIAG` in the regen log: 4 rows per Toward case), deterministic across rebuilds. The 64-iteration search budget is exhausted for the racing crossings (a 0.999c closing emitter's retarded time advances ~3.4×10⁸ ticks per frame; the from-the-present Newton walk does not converge inside the budget). Player-visible as an emitter blinking out of the sky for a frame — on a no-memo fallback path the plane does not currently fly (the plane carries the cache), but the doc's own fallback ("every crossing found from scratch") is not row-complete at these speeds.
2. **"Any cache, however stale or foreign, gives the same view" holds for the view and dies for the cost.** Poisoned (2-frame-stale alternation + a foreign twin-observer cache every 8th frame) returns the same rows (0.99995 — 2 dropped) at 1.76× the warm p99 (5.125 vs 2.922). The memo is not a pure accelerator for arbitrary caches; it is one for a *kept* cache.
3. **A tick-level light-cone bracket oracle is float-noise-limited at game scale — an instrument lesson.** At positions ~10⁸ root units, f64 puts ±1–2 ticks of noise on g(t) = t + |x(t)−xo| − t_now, while the engine's own acceptance window (rate − 10⁻⁴, with rate down to 10⁻³ for closing emitters) is 1000× below that floor. I built that oracle first, watched it fail 40% of *identically-correct* rows in every config, and withdrew it (recorded in the rung's Truth section). Consequence: at this scale the gather's tick answer is decided in floats whose noise exceeds its own window; the rung freezes presence + cost, and exactness needs either a smaller-scale scene (prediction 8) or an integer oracle. This is also mild evidence that the crossing *itself* is only tick-exact to ±1–2 at far separations — player-invisible (≤ 2 light-ticks of retarded time), but worth one line in view's physics holes.

The negative needed one redesign, disclosed: the historical 1.5 slope clamp (lab run 20261003-2306-redteam-4570) does **not** separate on this scene — at 60 Hz × rtf 100 a 0.999c closing stream races through its entire approach inside one or two frames (dt_e/dT = 10³), so medians are dominated by the receding phase where all configs agree. Physics kills that negative, not tuning. The amnesiac memo (frozen-root guess, no arrival-rate extrapolation) separates robustly (2.5/4.0 vs 2.0/2.92) and is the honest naive alternative.

## Predictions

`predictions.md` was written after the freeze hash, before the decisive run. What happened: 1–4 all held exactly as reasoned (warm passes; cold killed on cost not rows; poisoned fails the tail; amnesiac fails both cost bars). Held-out cases 5–8 are for the checker and are reasoned, not measured: rtf 10 (verdict unchanged), rtf 1000 (the p99 bar is cadence-dependent and would not hold — flagged), mixed β 0.6 (no separation), bracket oracle at 10⁶ scale (becomes freezable).

## What would make it wrong

- The rows oracle is presence-only: a config that returns *wrong* crossings (right id, wrong tick) passes `rows_found`. The bracket oracle that would catch it is float-limited here (finding 3); until an integer or small-scale oracle exists, r6 does not guard tick exactness. A planted wrong-tick law would pass this rung — that is the named hole in the rung, not in the law.
- The cost bars are calibrated on this scene and cadence (prediction 6): at rtf 1000 warm's p99 likely exceeds 3.2. The bars are cadence-relative, which the freeze states.
- The dropped-row mechanism (64-iteration exhaustion) is inferred from the racing-frame geometry plus the deterministic drop pattern, not from a counter inside `crossing` (adding one is a 3-line follow-up).

Cost of adopting: the integrator commits `r6-view.md` to `lab/rungs/` (the file is final here, hash recorded) and, if wanted, the probe (`r6_view.rs`, shipped-quality, self-contained) and the `gather_counted`/`ViewCache::amnesiac` additions (flag-off bit-identical; `cargo test -p emergent-universe --release --lib` 10/10 green; the crate's full `--release` test build does not link on Linux for an unrelated pre-existing reason — example `nladder` calls macOS's `proc_pid_rusage`). Nothing on main changes otherwise.

## Fit with PRINCIPLES

- "Compute only surprises" (§1.3) and "The view ≤ 1 sample per pixel per frame" (§6): the rung puts numbers on both promises — the memo is what makes the gather ~2 readouts; without it 1.8×.
- "A test that cannot fail is a control": r6 has a planted-law negative that fails, and it killed two real configurations (the cold fallback, the any-cache cost claim). "Errors never compound" is not implicated — the dropped rows are per-frame, not cumulative.
- Julien: "i care about the p95/99 results i want the game to be smooth" (CL 09-25): the tail bar (`readouts_p99 ≤ 3.2`) is the frozen form of that for the view.

## The lens (what the premise red-team lens may have made me miss)

Red-teams overweight exotic cases — I spent the pilot on 0.9999c Toward streams, where the physics itself makes both the letter and its falsifiers fragile (the racing-frame lesson above). The player's common case (Across/Away at moderate β) is where warm is most comfortably inside the bars, and I did not probe the *plane's own* scene (planets, moons, the fleet) where 7b86 measured 2.5–3.8 readouts/body — above my median bar; the rung's cases are stream scenes by design, and a checker running it on the plane's scene would see different medians. Also missed by construction: r5 (dense ≡ sparse), the other never-created rung — it cannot be executed in this lab at all, because `lattice-metal`'s dense order is `#[cfg(target_os = "macos")]` and compiles to a stub on Linux. That hole stays open for an M1-side run.
