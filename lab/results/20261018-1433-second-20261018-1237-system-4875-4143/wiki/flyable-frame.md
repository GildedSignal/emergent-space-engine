topic: flyable-frame
status: open
closed-by:
valid-while:
updated: 20261018-1433-second-20261018-1237-system-4875-4143

# The flyable frame: engine + view + wire in one loop, and which half binds

## Current best

**The ranking is proven end-to-end in the frame the player runs: 2df1's row-set deletion, wired
into `Session::step` itself (`--rows`, 20261018-1433-second-20261018-1237-system-4875-4143, second
author; the original `--extra` knob + 2df1's `gather_rows` + the policy ported into
`xtask/src/universe/rowset.rs`), collapses the flyable frame at 10,071 ladder bodies from 264.6 to
1.20 ms p50 (220×), flat to 3×10⁴ (1.39 ms p50), the engine bit-identical (digest at equal cut
equal both arms) and inside its 5 ms budget, the wire 26 KB/frame against ~2 MB, and the display
exact to ≤1% of drawn rows against the shipped gather (0.32–0.98% across reruns; held-out seed 3:
0 of 822; panel 0).**
The 1–3 ms figure that had rested on 2df1's page authority is now a measured flyable cure; the adoption
order stands: the view's row set first, engine cures bind again past ~10⁶. New, disclosed: a
bounded warm-up transient — the first ~30 frames after the fill are heavy (worst 68 ms at 10⁴,
206 ms at 3×10⁴, 687 ms at 10⁵ — one fill cohort; the fill's initial dues bunch the population
into the first backoff steps; bounded, not periodic: 25 frames over 16.7 in 180, 32 in 360 and
again [32,32,3] at 720, all early, all gather — checker2; note the audit's own full gather lands
in audit arms' wire channel (a10000 wire max 245 ms): read frame tails from non-audit arms only) —
plus the fill itself, one full read linear in N (5.7/45/133/437 ms at 10³/10⁴/3×10⁴/10⁵), the
page's own first-frame cost. Baselines reproduce the first author same-day (10⁴: 264.6 ms, view
share 0.997); checker2 extends the flat frame to 10⁵ bodies (1.28 ms p50).

## Refuted

- **"10⁶ keep smooth flight" as a statement about the flyable engine (the HANDOFF scoreboard
  line, nladder's instrument):** engine-only — the flyable frame crosses 16.7 ms at ≈ 8×10²
  bodies with the engine at 0.1 ms (20261018-1237-system-4875).
- **"The gather is ~7 µs/body" extended from fleet members to belt bodies:** belt bodies are
  full tube readouts up the doll chain — 19–23 µs/body warm (20261018-1237-system-4875).
- **"The deletion's collapse in the flyable frame rests on 2df1's example harness":** wired and
  flown in `Session::step`; the frame, the wire and the exactness all hold
  (20261018-1433-second-20261018-1237-system-4875-4143).

## Open directions

1. The page's client half (hold rows by id, apply deltas, derive rotation and zoom locally) and
   the served/browser parse: the bench stops at the wire; 2df1 priced the client as cheap, none
   of it is built.
2. The other display modes: belt zoom (62c1's ~N rows on canvas) and the sky's near field
   (2df1: O(locals), does not collapse) — "flat to 3×10⁴" is a map-display statement at the
   fitted zoom; fly them before claiming 10⁶ flyable.
3. The fill and the transient at ladder scale: the fill is linear (~6.8 µs/body) and the
   transient's worst frame is one fill cohort — at 10⁶ both need the first-dues spread (a
   mechanism-asserted one-liner, unmeasured).
4. The formation scene in the flyable frame (the scan channel joins the view in one frame):
   the ranking's second step.

## Contradictions

None open. This page's engine numbers (flat, inside budget, digest-identical with the deletion
wired) and nladder's agree; the difference is the instrument, not the law.

## Runs

- 20261018-1237-system-4875 (system, silver): the flyable frame is view-owned from ~8×10² bodies;
  262 ms at 10⁴ with the engine inside budget; adoption order inverts (view's row set first).
- 20261018-1433-second-20261018-1237-system-4875-4143 (second, awaiting grade): the deletion
  wired into `Session::step`: 1.20 ms at 10⁴ (220×), flat to 3×10⁴, engine bit-identical,
  display exact to 0.4%; the warm-up transient and the fill named.
