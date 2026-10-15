**Grade: leCheck complete. **Grade: lead** — `check.md` written, the author's wiki page corrected in place, tree restored clean.

**The run's two halves split:**

1. **The probe's "unnamed wall" is an instrument artifact.** The port's `settle(i64::MAX)` (nladder_lin.rs:79) simulates to game-time infinity — `settle(horizon)` means "resolve every item up to `horizon`" (universe.rs:1049–58), and every other call site in the tree passes a finite cut (`settle(cut)`, `settle(p.u.now)`, `settle(30_000_000)`). Proven three ways with a minimal shipped-loop probe:
   - rtf 100, N=10⁴, 12 ms budget, no settle/gather: **flat 54 MB through 59,880 frames (12 waves)**, 0 frames over budget, digest prints, exits;
   - rtf 6000, 1,200 frames: **bounded 159 MB in 13.7 s** — the "pre-wave arm fails to complete in 100 s" was settle, never the frames;
   - the identical flat loop + `settle(i64::MAX)`: **~17 MB/s monotone growth, never terminates** — reproducing the author's curve exactly. Growth is rtf-*independent* (same slope at 100 and 6000), which independently kills the "chronic budget deficit at high rtf" mechanism. The no-gather control shared the bug; the tell was in the author's own artifacts — every `out/*.txt` is a single line, no flight ever printed its census or digest.

2. **The five library lessons are genuine** (all quotes verified against the 4,580-highlight cache) but measure nothing: every anchor is scout-760f/b30b/0e37's own result, and the lead lesson (lazy-Entry) is scout-760f's checker's already-named gold condition.

**Adversarial beyond the author's range:** rtf 100 and rtf 600 (a decade down), both with the view off — the growth is identical, so the claimed regime boundary doesn't exist. b30b's flatness is mechanically consistent (its arms used `until: 30 s`/frame, ~2,300 frames flat — the "~1,100-frame cut" framing was wrong, corrected on the page). Also restored the c481 runs line the author's page dropped.

Page corrections: the "unnamed wall" paragraph now carries the refutation, and the run line reads lead. Evidence for the second checker: `out-chk/` (probe source + traces).
