Grade: silver

**Abstract.** H_live (live distinguishing bits) is now measured: an exact integer ledger in `xtask universe --bench` whose creation rate falls from 14.8 bits/game-second (30 game-s) to 0.036 (200,000 game-s), stock 5,240 bits for 76 bodies, reabsorption 27% — extrapolating to ~0.2 GB of scars for 10⁹ bodies over an hour at plane density (≥ 40× under 8 GB), so the fit is decided by interactions per body per second, not N. I reproduced every table number, the bit-identical digest across patched/pristine trees (6ee2bcb8…, cut 101,512,723) and 58/0 tests — from the author's edits recovered out of dangling git objects, because `work/patch.diff` was never saved. Not gold: the published record carries no code, and one bullet is contradicted by the log.

## Reproduction

- **`work/patch.diff` does not exist** (run.log: "line 24: …work/patch.diff: No such file or directory"); the tree was restored clean. I recovered the author's exact bytes from this runner's dangling stash objects — tracked hooks in `a22468523b443c7c7c5cb3f37c854e8c3fb5ee62`, untracked `crates/universe/src/live.rs` + `tests/h_live.rs` in `8e5e31a292aa033fad34f9ccaeb1676c7714f31a` (both stamped 23:56:40, mid-run) — and applied them to a clean tree at a838a28. Saved at `/tmp/spacex-dbf9-recovered.patch`.
- All five evidence rows reproduce **exactly**: 444 (221/128/95), 3,426 (3,298/128/0), 3,228, 5,310, 7,203 created; reabsorbed 0/25/48/317/1,963; live 444/3,401/3,180/4,993/5,240; rates 14.8/1.14/1.08/0.177/0.036; rebinds 24/2,551/3,570/10,732/51,976; on-generator 34/39, 19/76, 23/76, 5/76, 4/76.
- **Digest invariance**: I re-did the stash → rebuild → bench → pop myself; both trees give `6ee2bcb8b6f05aea83d15e91beb32884e6d8d35f2db17fb81e027db7d7b0b216` at cut 101,512,723 (`--rtf 100 --seconds 5`). The ledger is a pure read.
- **Tests**: 58 passed, 0 failed (`cargo test --release -p emergent-universe`), ledger-balance and budget-independence tests included.
- **Arithmetic checks**: 4.7×10⁻⁴ bits/body/game-second, 0.2 GB and 6.5 GB extrapolations, 27% reabsorption, 1.3/0.13 bits per rebind — all correct.

## Predictions

Genuinely pre-registered: predictions.md sat in the stash at 23:56:40 byte-identical to its final form, before the session's last 10 minutes (the decisive benches and dossier). Honest split: 1 and 2 failed and are reported as failed; 3 and 5 held; 4 held at the transient and was beaten at the asymptote.

## Adversarial cases (mine)

- **Held-out seed 3** (never run by the author), 3,000 game-s: created 3,001, rate 1.0003 — consistent with seeds 1/5 (3,426/3,228; 1.14/1.08). Tubes dominate on every seed.
- **Window beyond the author's furthest** (300,000 game-s, seeds 1 and 3): rates 0.0261 and 0.0307 — the fall continues, so the 0.2 GB extrapolation is conservative in its own direction. Balance identity created − reabsorbed = live_now holds in every run.
- **"~1/t" is generous**: measured exponent ≈ 0.8 in the tail (0.56 over the transient). The conclusion (sub-linear stock, falling rate) is unaffected; say "~t⁻⁰·⁸" next time.
- **"Swallowed-at-tube-resolution = 0 in every run" is false**: the author's own commands print 1 (seed 5, 3,000 game-s), 127 (30,000) and 283 (200,000) — and 396 at seed 3/300,000. The share stays ≤ 0.5% of rebinds, so prediction 1's substance (nearly every resolved kick moves the tube) survives, but the categorical bullet contradicts the log — exactly the failure mode the lab README names.

## Novelty

The concept pre-exists by design (docs/plane.md line 36, the 5 October review; law.md's allocator "reads H_live"; queue item `b-h-live` asked for exactly this), and components-98bc's 0.126 bits/body is the static program side. This run supplies the first operational definition, implementation and measurement — the live scar side. No H entry measures it. Not a redo.

## Goal fit

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" and the queue's own `b-h-live`: filled, except the page's HTML label and the `--describe` line. PRINCIPLES #24 ("the memory floor is information") and #6 ("Store the generator, not the generated"): the ledger counts exactly the departure from generators. The density caveat (one 76-body system; a billion-body universe has more close pairs, the board's top scaling risk) is scoped honestly in the dossier.

## Why silver, and the one experiment to gold

The measurement is real, decision-grade and fully reproduced here — but gold requires adoption within one step, and the record cannot be adopted: `work/patch.diff` was never saved (run.sh's `phase()` redirects into `work/` without creating it; something removed the empty directory mid-run), so the published branch carries a dossier and predictions with no code. The edits survive only as dangling objects on this runner, which any `git gc` erases — the 5 October silver pattern, "results that the shipped code cannot regenerate", now with an infrastructure cause. **The experiment to gold:** re-attach the code to the record — publish the recovered patch inside the run folder (it is at `/tmp/spacex-dbf9-recovered.patch`, reconstructible from the two dangling commits until a gc) — and correct the swallowed bullet; nothing else stands between this and adoption.

## What the author missed

- The swallowed-kick bullet was written against the instrument's own nonzero output; reading the JSON once more would have caught it.
- The 1/t framing hides a two-regime exponent (0.56 transient, ~0.8 tail); the stock's t^0.2 growth is the more decision-relevant number.
- run.sh's fragile `work/` redirect deserves a one-line fix (`mkdir -p "$out/work"` in `phase()`); report it to the integrator rather than losing the patch silently — the same accident will eat future runs.
