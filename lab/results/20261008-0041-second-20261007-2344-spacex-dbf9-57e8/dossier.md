# The H_live record now regenerates: code shipped, rows exact, false bullet corrected

## Claim

The silver's single named gap is closed: the H_live ledger's code is reconstructed byte-for-byte from the runner's dangling stash objects and published **inside the record** (`code/live-ledger.patch`, 368 lines: the 4 tracked hook files + `live.rs` + `tests/h_live.rs`), one command (`code/regen.sh`) regenerates every evidence row from a pristine `a838a28` worktree — all five rows exact, digests identical across two invocations, 58/0 tests — and the dossier's one log-contradicted bullet ("swallowed-at-tube-resolution = 0 in every run") is corrected: it is 0.03–1.17 % of resolved kicks, so the underlying claim and its decision (≈ 0.2 GB of scars for 10⁹ bodies over an hour at plane density) stand.

## Bottleneck

The record-regeneration bottleneck the checker named (the 5 October silver pattern, now with an infrastructure cause: `run.sh`'s `phase()` redirects into `work/` without creating it). Gain: the measurement becomes adoptable within one step — the integrator applies one patch or runs one script. Also fixes the cause itself: `lab/run.sh:24` now does `mkdir -p "$out/work"` before redirecting (one-line tree edit in this run), so no future run loses its patch silently.

## Evidence

Provenance of the reconstruction (this runner still held the danglers; any `git gc` would have erased them):

- `a2246852` (stash, tracked): 4 files, 27+/1− — hooks in `lib.rs`, `universe.rs`, `xtask/universe/mod.rs`, `session.rs`.
- `8e5e31a2` (stash, untracked): `crates/universe/src/live.rs` (196 lines), `crates/universe/tests/h_live.rs` (67 lines), both `live.rs`/`h_live.rs` verified byte-identical after extraction. The checker's `/tmp/spacex-dbf9-recovered.patch` held **only** the 4 tracked files (0 references to the new files); the complete patch is in this folder.
- Both stamped 23:56:40, the state the checker reproduced the record from — so the shipped bytes are exactly the bytes that produced the published table.

One command regenerates everything (each step ≤ 60 s after the build; full log in `regen-run.log`):

```
bash lab/results/20261008-0041-second-20261007-2344-spacex-dbf9-57e8/code/regen.sh
# worktree at a838a28 → git apply live-ledger.patch → build -p xtask → 6 benches → tests
```

All five published rows reproduce **exactly**, plus one held-out seed (mine, `heldout.json`):

| run | game-s | created (kick/dec/other) | reabsorbed | live now | rate /game-s | rebinds | on generator | swallowed |
|---|---|---|---|---|---|---|---|---|
| rtf 1, 30 s, seed 1 | 30 | 444 (221/128/95) | 0 | 444 | 14.8 | 24 | 34/39 | 0 |
| rtf 100, 30 s, seed 1 | 3,000 | 3,426 (3,298/128/0) | 25 | 3,401 | 1.14 | 2,551 | 19/76 | 0 |
| rtf 100, 30 s, seed 5 | 3,000 | 3,228 (3,100/128/0) | 48 | 3,180 | 1.08 | 3,570 | 23/76 | 1 |
| rtf 1000, 30 s, seed 1 | 30,000 | 5,310 (5,178/128/4) | 317 | 4,993 | 0.177 | 10,732 | 5/76 | 127 |
| rtf 10000, 20 s, seed 1 | 200,000 | 7,203 (7,091/88/6) | 1,963 | 5,240 | 0.036 | 51,976 | 4/76 | 283 |
| **held-out** rtf 10000, 20 s, seed 5 | 200,000 | 6,604 (6,500/88/6) | 1,359 | 5,245 | 0.033 | 78,568 | 6/76 | 272 |

- Balance identity `created − reabsorbed = live_now` holds in all six runs (integer-exact).
- Digests at the canonical cut are identical between the manual run and the pristine-worktree regen run for all six rows (e.g. seed-1 rows `d96acc05…`, `41343a14…`, `f0684ddb…`, `d0a37c3f…`): deterministic across invocations and paths.
- Tests: `cargo test --release -p emergent-universe` → **58 passed, 0 failed** (12+2+6+1+8+4+6+3+8+3+5; the 2 `h_live` ledger tests included).
- **Corrected bullet.** Swallowed-at-tube-resolution is not 0: 1 (3 k, seed 5), 127 (30 k), 283 (200 k, seed 1), 272 (200 k, seed 5) — 0.03 %, 1.17 %, 0.54 %, 0.35 % of resolved kicks. The author's prediction-1 substance survives: ≥ 98.8 % of resolved kicks move the tube. (The checker's "≤ 0.5 % of rebinds" bound is itself slightly off at 30 k: 1.17 %.)
- **Held-out seed 5 at 200,000 game-s:** created 6,604 (0.92× seed 1), rate 0.033 (0.92×) → 4.35×10⁻⁴ bits/body/game-s → **0.20 GB** for 10⁹ bodies/hour (seed 1: 4.74×10⁻⁴ → 0.21 GB). The asymptote is not seed-specific; the decision holds on both seeds.
- Rate fall: transient exponent ≈ 0.81 (3 k→30 k), tail ≈ 0.84 (30 k→200 k) — "~1/t" was generous, as the checker said; the live stock grows only ~t^0.10 past the transient (3,401 → 5,240 over 3,000 → 200,000 game-s).

## Predictions

All five in `predictions.md` held, written before the decisive runs: (1) patch applies, builds, 58/0 tests; (2) all five rows exact; (3) the "= 0 swallowed" bullet false with the expected counts 1/127/283; (4) held-out 200 k seed 5 within 2× of seed 1 (it was within 8 %) with the balance identity holding; (5) the 0.2 GB extrapolation re-derived from the 7,203-bit row.

## What would make it wrong

- The patch reconstructs the stash state at 23:56:40. If the author made further edits in the session's last 10 minutes that were never stashed, they are lost with the danglers' reflog window — but the checker reproduced the published table from exactly these bytes, so the record and the code agree.
- The substance caveats are unchanged from the original dossier: one 76-body scene (density fixed by the plane), correlated kicks share structure the delta code overcounts, fleet-frame members and cross-doll re-encoding are outside the ledger.
- Digest invariance (ledger = pure read) is the checker's reproduction, not re-run here; the row digests above regenerating identically across two trees is consistent with it.

## Cost of adoption

One `git apply` of `code/live-ledger.patch` onto `a838a28` (or `bash code/regen.sh` for the full record). ~200 additive lines, zero outcome change (checker's stash-dance proof), per-event cost one field compare. Still unwired, as the author noted: the page's HTML label and the `--describe` line. The `run.sh` `mkdir -p` fix is a one-line tree edit in this run.

Fit with PRINCIPLES: #24 "the memory floor is information" — the measurement the decision needs; #11/text-has-a-cost via the lab's own rule the checker quoted — a record the shipped code cannot regenerate is not a record.

## The lens (second author)

What this lens may have missed: I verified the record, not the instrument's semantics — the ledger's delta-encoding definition (1+32 key bits, bitlen deltas) is taken from the author's dossier as published; auditing whether that definition is the *right* floor (the SpaceX lens's own "lower bound next" note) is a different run. I also did not re-run the digest-invariance stash dance (checker's proof stands) and left the page wiring untouched.
