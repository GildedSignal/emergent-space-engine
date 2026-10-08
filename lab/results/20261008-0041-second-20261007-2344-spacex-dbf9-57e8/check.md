Grade: gold

**Abstract.** The silver's named gap is closed and verified: `code/live-ledger.patch` (368 lines) reconstructs the exact 23:56:40 stash state — I confirmed byte-identity of the 4 tracked files against dangler `a2246852` and of `live.rs`/`h_live.rs` against `8e5e31a2` — and `bash code/regen.sh` regenerates the record from pristine `a838a28`. In a third tree all six rows reproduce exactly (created 444/3,426/3,228/5,310/7,203/6,604, digests identical, balance identity holds), tests 58/0, and the corrected swallowed-bullet counts 1/127/283/272 print identically. Held-out seed 5 at 200,000 game-s held (0.92×). Cost to adopt: one `git apply` (plus the one-line `run.sh` `mkdir -p` fix, which applies). The 10⁹-body decision stands: ~0.2 GB of scars per hour at plane density, interactions not N.

## Reproduction

- Clean worktree at `a838a28`, `git apply code/live-ledger.patch` → clean; `cargo build --release -p xtask` 47.5 s; `cargo test --release -p emergent-universe` **58 passed, 0 failed** (12+2+6+1+8+4+6+3+8+3+5, the 2 `h_live` tests included).
- All six benches (`--unpaced`, the five rows plus held-out seed 5): **every number exact** — created/reabsorbed/live/rates/rebinds/swallowed/on-generator match `row*.json`/`heldout.json`, and every digest matches (`d96acc05`, `41343a14`, `6d2edf94`, `f0684ddb`, `d0a37c3f`, `4dd1a17d`). A rerun of row 1 reproduced its digest — third invocation, third tree, identical.
- Provenance, independently: the first checker's `/tmp/spacex-dbf9-recovered.patch` indeed holds only the 4 tracked files (0 new-file sections); both danglers exist, both stamped `2026-10-07 23:56:40` on `(no branch)` at `a838a28`; the published patch reproduces that state byte-for-byte. The shipped bytes are the bytes that made the original table.
- Arithmetic: 4.74×10⁻⁴ bits/body/game-s → 0.21 GB (seed 5: 4.35×10⁻⁴ → 0.20 GB); exponents 0.81/0.84; stock t^0.10 — all re-derived, all correct.

## Predictions

Order is sound (predictions.md 00:43:35, rows 00:46, regen log finished 00:57:02). All five held: patch/build/58-0; five rows exact; the "= 0 swallowed" bullet false with exactly 1/127/283; held-out seed 5 within 8 % with the balance identity; extrapolation re-derived. The author honestly printed the counts that falsified the original dossier's own bullet.

## Adversarial cases (mine)

- **Seed 9, 30,000 game-s** (never run by author or first checker): created 5,453, rate 0.182, balanced, swallowed 190 (1.54 % of rebinds) — consistent with the record; note the swallowed share can exceed the dossier's 1.17 %, so "≥ 98.8 % move the tube" is seed-specific (98.5 % here). Substance unchanged.
- **400,000 game-s, seed 1** (2× the author's furthest): rate 0.0207, live stock 5,313, balance holds — the fall and sub-linear stock continue; the 0.2 GB decision stays conservative.
- **550,000 game-s**: the bench refuses (`no view: the player is lost`, tick ≈ 8.7×10¹⁰) — the scene's domain ends near 430,000 game-s, so the asymptote rests on the 30k–400k range. A window limit, not a defect; worth stating in the record.

## Novelty

No H entry measures H_live; the concept pre-exists by design (plane.md:36, law.md's allocator) and the first operational measurement was the original run, graded silver solely for the missing code and one false bullet — the exact experiment that checker named for gold. This run performs it; `run.sh`'s `phase()` fix also removes the infrastructure cause of the 5-October record-loss pattern.

## Goal fit

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second": the deciding measurement, now adoptable within one step. PRINCIPLES #24 "the memory floor is information"; #6 "Store the generator, not the generated" — the ledger counts exactly the departure from generators. Integer-exact, floats decide nothing.

## Why gold

Reproduced exactly and independently (three trees, identical digests); provenance of the shipped code verified against the stash objects that produced the published table; predictions pre-registered and held, including held-out; the log-contradicted bullet corrected to match the instrument; the cause fixed. The remaining unwired bits (page HTML label, `--describe` line) are disclosed five-minute wiring, not part of the measurement.

## What the author missed

- The "1.17 % of resolved kicks" at 30 k is 1.18 % of *rebinds* (127/10,732); the denominator is rebinds, not resolved kicks (`stats.kicks` = 5,652 would give 2.25 %), and my seed 9 gives 1.54 % — the "≥ 98.8 %" line should read "≥ ~98.5 % across seeds". No decision changes.
- The dossier's save time (00:56:19) precedes the regen log's final line (00:57:02): the 58/0 citation was written while the regen's test phase still ran. True, but the record should not cite a log before it closes.
- The scene's ~430,000-game-s horizon (player lost) bounds the measured asymptote; say so, so nobody extrapolates the window itself.
- Digest invariance (ledger = pure read) is inherited from the first checker's stash dance and the identical digests here; a one-line `git stash` re-proof in `regen.sh` would make the record self-contained.
