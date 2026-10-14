# Predictions (written before the mutant panel)

Instrument: `cargo run --release -q -p xtask -- universe --replay-all [--flights DIR]`, the
merge gate. Two corpora:

- **Stale arm (main as it is):** `artifacts/flights/` recorded at 73c98a46 under law hash
  `be41b063…`; the tree is at 33c83f1ab483, law hash `41f180a0…`; the baseline gate prints
  `3 changed, 0 regression(s)`, exit 0 (measured before this file was written).
- **Refreshed arm:** the same three flights with `digest`/`law_hash`/`commit` rewritten to
  the current tree's replay values (what decision-log's open direction 1 says to do after a
  law change). Baseline there must be `3 same, 0 regression(s)`, exit 0 — if it is not, the
  refresh is wrong and the arm is void.

Panel: six one-line mutants in the law's crates (inside the `law_hash` closure: universe,
space, engine, lattice, lattice-event), each a plausible refactor slip, plus one historical
control (the i128 contact wrap that the 13-October merge actually fixed):

| id | file, edit | class |
|---|---|---|
| M-wrap | `lattice/src/law.rs` `hit`: drop the 512-bit `Wide` fallback, call `hit_in` narrow | the real shipped bug, reverted |
| M-sign | `universe/src/force.rs` `pull`: negate the returned acceleration | absurd control (must be visible) |
| M-thrust | `universe/src/ctx.rs` `thrust_log2: -44` → `-45` | plausible constant slip |
| M-kick | `universe/src/step.rs:440` kick `len` shift `>> (2*level)` → `>> (2*level+1)` | plausible cadence slip |
| M-bind | `universe/src/bind.rs:233` retry trigger `len <= cur_len && vel <= cur_vel` → `+1` on both | off-by-one at the word |
| M-prune | `universe/src/universe.rs:1105` history margin `(1 << 26)` → `(1 << 20)` | plausible optimization |

## Predictions

P1 (stale arm, the today condition). Every mutant that does not create a new loss or
refusal leaves the gate's printed verdict bit-identical to baseline (`3 changed, 0
regression(s)`, exit 0): digest drift is already saturated, so a mutant's digest change has
nowhere to show. I predict **all six exit 0 on the stale arm**, and at most M-sign changes
a loss note (flight 2 lost by "hit Home"; a flipped field changes the loss tick/reason,
which prints as `changed` with a note, still not a regression).

P2 (refreshed arm, the mesh). Visible = any departure from `3 same`: digest moves to
`changed`, or a loss/refusal note. I predict:
- **M-sign: visible** (changed, all three flights; possibly a loss-note change).
- **M-thrust: visible** (changed on the flights with burns — at least the two with thrust
  keys).
- **M-kick: visible** (changed, all three; kicks are universal).
- **M-wrap: invisible** (`same`) — the corpus's contacts never reach i128-wrapping scale.
- **M-bind: invisible** (`same`) — no fit-again retries at 48 members (frame-cost measured
  retries only in hand-outs, which need ≥ the leak regime).
- **M-prune: invisible** (`same`) — the digest does not cover pruned history, and the
  margin cut does not touch a live item.

So the predicted mesh on a *fresh* corpus is 3 of 6 fully invisible, all three invisible
ones in subsystems the corpus cannot fly at 48 members / seed 1.

P3 (exit code). No mutant reaches exit 1 on either arm unless it mints a *new* loss or
refusal; I predict zero exit-1 outcomes across all twelve runs (the gate's exit code only
bites on loss/refusal deltas and replay failures, not on law changes).

P4 (held-out, not tuned on). The refreshed arm's `same` classification for M-wrap depends
on contact coordinates staying inside i128 products; if flight 3 (rtf 800, 445 M ticks)
flies far enough out, M-wrap may instead show `changed` — I would count that as a miss of
this prediction, not evidence of mesh.
