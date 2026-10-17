# Dossier — 20261017-1240-spacex-9c67

**Claim.** 5ade's third "exact duplicate" — `apply`'s post-event `root_state_raw` position
walk — is built and measured: the deletion is real, small and **digest-identical on both
seeds** (game and replay), but it is **not an exact duplicate**: on 17,643 of 35,275 handed
events (49.97%) the walk's position differs from the resolver's own state **at the bit
level**, and the digest's indifference to that is the load-bearing result — the position
cache and its sub-quantum divergence are provably outside the outcome channel.

**Bottleneck.** The kick/event cycle (board #3: the kick at 75–160 µs against a ~50 ns
floor). 5ade (kick-jet, silver) decomposed the fired belt kick and priced this walk at
5.0 µs × 2.06/kick, "another −13% of the cycle, not built". This run builds it. Expected
gain here: order 10⁻⁰·⁰⁵ of the event cycle on the plane scene (measured −5.1…−6.0%),
i.e. a deletion worth taking but not a bottleneck mover; the exactness finding is the
value.

**Evidence** (Linux/x86 shared runner, orders of magnitude; all numbers regenerate by
`regen.sh`, ~4 min):

- The patch (work/patch.diff, +83/−7 over `step.rs`/`universe.rs`/`cost_split.rs`): every
  resolver arm notes the integer state it last read or built at the item tick
  (`Update::own`); `apply` converts it to the root frame with `root_state_raw`'s exact
  arithmetic (doll chain still walked); handoffs (capture/release) and first plans fall
  back to the walk.
- **Coverage 99.89%:** `ES_POS_VERIFY=1 bin-patched/cost_split` → pos probe
  `(handed, walked, mismatch) = (35275, 39, 17643)` over 49,617 events.
- **Digest identity:** `xtask universe --kick-bench --seconds 5`, seeds 1 and 7 (held
  out), pristine vs patched binaries: `digest` and `replay_digest` identical on all four
  runs (`work/kick-*.json`); refused 0. The pure-resolver kick medians are a control:
  58.5→58.1 µs (seed 1, unchanged within noise; the deletion is outside its timed scope).
- **Timing, interleaved A/B/A on one box** (the b583 lesson): cost_split's whole-universe
  arm, 3 pairs: 56.6/56.7/56.3 → 53.7/53.0/54.0 µs per kick/open/boundary = **−5.1…−6.0%**
  of the event cycle (5ade's −13% was priced on the N=10⁵ belt wave, whose walk is deeper;
  this scene is the 32-body plane).
- **The mismatch half:** the walk re-derives the position from the **fresh binding**
  (`binding_at(i,t).cartesian(t)` = decode + residual); the hand-off uses the **fit's
  input state**. They disagree in bits on ~½ of events — by construction these are the
  rebinding events (kicks) where a new binding exists; opens/boundaries/crashes read the
  standing binding and match. The fit's residual does not always close the anchor
  round-trip bit-exactly (a-word/knot-quantum territory: the disagreement is a
  representation fact, not yet diagnosed to the quantum; the leading suspect is the
  residual word's width in `Binding::between`). The two readings differ by sub-quantum
  position bits — and **nothing in the game's digest can see them** (positions feed only
  `light_distance` → queue deadlines; observe.rs:8 "deadlines and positions … are never
  an outcome" — now measured, not just documented).

**Predictions** (predictions.md, written before the decisive runs): coverage ≥95% ✓
(99.89%); timing −8…−15% ✗ (−5…−6%, fallback clause fired: 5ade's −13% was the belt's
deeper walk); digest identical ✓ (both seeds); **bit identity ✗ — the kill criterion for
the "exact duplicate" letter fired**: POS_MISMATCH = 17,643 ≠ 0. The deletion survives on
the digest evidence, not the exactness premise.

**What would make it wrong.** A scene where the position cache's sub-quantum divergence
changes resolution order in a way a digest records (flown here: two seeds, burns via the
bench script, 300 frames; not flown: the belt at 10⁵, long horizons, the M1). If the
residual's anchor round-trip is ever made bit-exact (a one-word fix in `between`), the
mismatch count must drop to 0 with this patch unchanged — that is the falsifier.

**Cost of adopting.** +83/−7 lines; no law change (digests identical); removes ~1 walk
per event on the apply path; the counters and `pos_probe()` are permanent instrumentation.
Fit with PRINCIPLES: "The cheapest compute is compute not done. Delete before
optimizing" (§1); "positions … are never an outcome" (§28, the view is an instrument) —
now with a measurement behind it.

**The lens (SpaceX).** Delete-first was the right order, and the falsifier was cheap; but
the lens's blind spot bit exactly where warned — a deleted "duplicate" carried a
certificate-grade fact (the anchor round-trip is lossy) that only a bit-level verify
mode could see. Averaging the two readings (handed vs walked) would have hidden it.
