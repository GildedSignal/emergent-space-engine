# check2.md — run 20261007-0800-second-20261007-0711-library-9ab7-480e

Grade: silver

**Abstract.** Second blind check. The deterministic core reproduces exactly: byte-identical reruns (digests and all 12 integer fields, seeds 1/3/5, twice for seed 5; flat-vs-item digest control extended to seed 3), `analysis.py`/`addendum.py` regenerate their JSONs, demand max/p99.9 = 3.69 (A) and 4.25 (hour), median-bench-misses-hour 4.5×/6.8×, bench-window lottery 44×, Gaussian miss 11.1×/25.8×, rtf-16 thinning (2.61) and m-400 burst (p99.9 = 100, max 328) — all timing-free. The cost plateau α̂(1%) ≈ 1.0–1.4 held on 7/7 quiet-box runs. Not reproduced: seed 1's tail tip (6 650 → 2 248 µs, p99.9 3 064 → 328), the 8× seed-max spread (→ 2.1×), the ≥ 3 ms fleet census (→ 0). Adoption stands on the demand stream alone; the "no construction bound" leg does not survive a quiet box.

## Reproduction (clean tree, `work/patch.diff` is empty — no repo edits, as claimed)

- `cd probe && cargo build --release` — builds. `bash sweep.sh` not re-run whole; components rerun below.
- Reruns (binary `/home/glmlab/lab-target-0/release/plane_events`): seeds 1, 3, 5 (item mode), seed 5 twice, seed 3 flat, fresh held-out seeds 21–23. Load during my runs 0.25–1.8 (quieter than the author's 1.8).
- **Determinism holds fully.** Seed 5 twice: digest `86260d22…` (= sweep.log), all 12 integer fields byte-for-byte equal to `data/A_s5.0` and to each other; kind annotation differs in exactly 1/60 000 frames, as the dossier discloses. Seed 1 digest `2f5383af…` ✓. Flat-vs-item digest control reproduced on a second seed (3): identical digest `06114353…` (and again flat's slice counter +1, digest unaffected).
- `python3 analysis.py`, `python3 addendum.py` on the author's `data/`: **both JSONs regenerate exactly** (diff of pretty-printed = empty).
- Every decision number I could pin to the deterministic stream is as stated: A demand p50/p99/p99.9/max = 1/1/13/48, per-seed maxima 26–48, pooled max/p99.9 = 3.69; H p99.9 = 8, max 34, ratio 4.25; bench-vs-hour 4.49× (A) / 6.8× (H), worst window captures the hour at 1.08–1.22×; window p99.9 min/median/max = 1/11/44.4 (lottery 44×); Gaussian 11.05× (demand) and 25.78× (frame work, truth 5 019 µs); B demand ratio 2.61 with max 47 (rtf-16 *thinner*, P4 inversion confirmed on deterministic data); C p99.9 = 100, max 328, per-seed item maxima 2.3–2.75 ms; heavy frames mean 9.4 slices + 7.8 boundaries + 5.6 kicks.
- **Held-out seeds (21–23, config A):** demand max/p99.9 = 4.33, 3.36, 2.21 — the P1 kill (> 3) holds pooled and on 2 of 3 fresh seeds; digests unique, item counts 15 311/61 921/61 749 (seed 21 is another early-ending battle, like seed 8).

## Attack results (where the run is weaker than its claim sentence)

1. **The tail tip is runner noise, not engine work.** Seed 1 resolves an identical item sequence in every run (identical digest and counters), yet its top-1 stream gives max 6 650 µs / p99.9 3 064 µs (author, load 1.8) vs max 2 248 µs / p99.9 328 µs (my rerun): a 3×/9× swing on the *same work*. The claimed "no construction bound (per-seed worst item 0.84–6.65 ms, an 8× spread)" collapses to 1 065–2 248 µs (~2.1×) across my 6 runs — below the 3× that P2's registered kill required. So the P2 kill fires only under load; on a quiet box the tip sits near ~1–2.3 ms, which is *consistent with* a compile-class ceiling. "No construction bound" is unproven, not measured.
2. **The ≥ 3 ms census vanishes on a quiet box.** Author: 174 items ≥ 3 ms, 158 fleet. My 360 000 frames: none ≥ 2.25 ms; at ≥ 500 µs the census is player-dominated (12–15 per run) and ≥ 1 ms is unattributed (`?`). The "tail is made of fleet contact epochs" mechanism is load-dependent; only the player-kick-recompile part (0.4–1 ms) reproduces.
3. **What does reproduce on the cost stream** is the body: α̂(1%) = 0.985–1.37 on 5 fresh/rerun runs here plus the author's pooled 1.267 and jackknife 1.24–1.40, and p50/p99 ≈ 21–22/31–42 µs. The plateau is real; only its extreme tip and the seed-max spread are environmental. The dossier concedes ratios-not-absolutes, but the claim sentence and P2's kill lean on the unstable leg.
4. The author's own data contains an unremarked **construction bound on the demand stream**: A's max = 48 = members, C's max = 328 at m = 400 — the per-frame demand ceiling scales with the fleet. Relevant to "no bound" and to the fleet-scale risk the run itself flags.

## Novelty

`docs/HISTORY.md` has no event-tail/Hill entry (searched); the silver probe it checks (20261007-0711-library) is unjournaled in this checkout. The measured-on-engine numbers, the P4 inversion (hazard at 1:1, not fast-forward) and the m-400 demand-burst are new. `dash.rs` already reports worst-ms and hitches/hour (extrapolated from ≤ 55 s) — the dossier's "the gate currently reports percentiles" slightly undersells the dashboard, but its point stands: nothing in a 55-s window sizes the hour's tail, and the bench-window p99.9 varies 44×.

## Goal fit and PRINCIPLES

Board #4 (smoothness/allocator): decides what the gate measures, points at the known cadence/compile lever; no engine change; adoptable in one step (one line in plane.md's measured list + per-item logging in the bench, this harness as template). "i care about the p95/99 results i want the game to be smooth" — the run shows those percentiles of a 55-s bench do not size the player's worst moment (4.5–6.8×, Gaussian 11–26×). "Compute only surprises. Cost follows change and entropy" — the tail measured as the surprise stream's entropy. Honest self-kills (P1/P3) and a reported inversion of the author's own P4; predictions.md timestamps precede the sweep data (08:11 vs 08:12+).

## The one experiment to gold

Re-measure the per-item tail with a noise-robust cost unit — thread-CPU time per item (the shipped bench already separates `frame_cpu_ms` from stalls) or a deterministic work counter per item — at controlled load, ≥ 15 seeds × 2 repeats, plus demand max vs members ∈ {48, 100, 200, 400}. That either pins a construction ceiling (P2's original shape) or shows the spread is engine-real, and settles the mechanism (player recompile vs fleet epoch vs scheduler). Everything adoptable already reproduces; only this leg is open.

## What the author missed

- Timing stability was never tested on a repeat (the regeneration check compares demand fields byte-for-byte but dismisses all timing as "must differ"); one seed-1 rerun would have shown the 6.65 ms item and the 8× spread are load artifacts — the same class of lesson as the 5 October memo artifact (shared-harness agreement ≠ independence).
- The demand-stream bound ≈ members is sitting in the results (48→48, 400→328) and unremarked.
- `addendum.py`'s Gaussian quantile is dead code (scipy `erfcinv` computed, then overwritten by a 10 M-sample MC quantile; deterministic only via the fixed rng seed) — works, but undocumented and fragile.
- `probe/src/main.rs`'s header claims the digest control ran "once per configuration"; the sweep ran it once, seed 1, config A (pilots aside). It held on my second seed.
- The dossier's framing "the gate currently reports percentiles of a ≤ 55-s bench" ignores that the dashboard already keeps the worst hitch and hitches/hour — the true gap is the 55-s window and single-shot extrapolation, which the tail line and multi-bench max fix.
