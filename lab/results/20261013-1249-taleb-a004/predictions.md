# Predictions (written before the decisive runs)

Question: is the live presented-tick decision log (`xtask/src/universe/session.rs:78-81`,
`input(u.now, keys)`) a bounded bookkeeping offset or a compounding divergence of canonical
history — and does the ungraded a342 fix (a `sched` timeline + `input_frame` on a 0.25 s wall
decision quantum) still close it on the post-merge tree (clock merge f7f6d87, playability merge,
five days of moves since it was built)?

Cases I did NOT tune on: the growth ladder (84M/252M/756M ticks), the 400-member confirmation,
the straddle press at 0.26 s, and everything about how the current tree behaves (I have not run
it yet). Arms are deterministic (`Budget::events(2)` as the load surrogate, fixed fps), so a
checker reruns them bit for bit.

1. **The hole is live on the post-merge tree.** Same seed (11), same wall-keyed script through
   the shipped loop's exact two lines: 60 Hz rich vs 60 Hz starved vs 30 Hz vs 144 Hz produce
   ≥ 3 distinct digests at cut 84M ticks, and the logged decision ticks themselves differ
   (the starved arm logs earlier ticks — the presented time lags). Encounters differ by ≥ 5%
   between rich-60 and starved-60.
2. **The divergence compounds with flight length** (this is the one that decides ruin vs
   bookkeeping). Player separation at the cut between rich-60 and starved-60, over cuts
   84M → 252M → 756M ticks (415 → 1245 → 3734 game-s): the separation grows faster than the
   cut ratio (superlinear; separation(3×t)/separation(t) > 3 at the top of the ladder). If it
   comes out flat or linear, the hole is a bounded offset and I will report it as such — that
   would kill the compounding half of the claim and leave only the canonical-history break.
3. **The fix holds on the current tree**: all four arms (60 rich, 60 starved, 30, 144) produce
   ONE digest and identical logged ticks, at rtf 100; the load-only pair also holds at rtf 1.
   The logged ticks are multiples of the decision quantum (rtf × 0.25 s in ticks).
4. **The fix's price, measured**: every logged decision sits within one quantum (≤ 0.25 s wall,
   ≤ 25 game-s at rtf 100) of the press's scheduled time; typical about half a quantum.
5. **The fix's honest limit reproduces deterministically**: a press at 0.26 s wall (just past a
   quantum boundary) makes 30 Hz and 144 Hz log different ticks → different digests. This is
   declared, not hidden: within ~one frame period of a boundary, the rate pair can disagree.
6. **400 members does not change 1 or 3** (one confirmation pair each).

Kill criteria for my own claim: if (1) fails (all four arms already agree on the post-merge
tree), the hole has been fixed incidentally and the run collapses to a confirmation; if (2)
fails, no compounding claim; if (3) fails, the fix needs rework beyond a port and I report the
breakage mode instead of "holds".
