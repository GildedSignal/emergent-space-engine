Working...
Check complete. `check.md` written; the author's patch reverted (tree clean except the untracked run folder).

**Grade: gold.**

- **Reproduced** from the dossier's commands in a clean tree: empty frame 0.002/0.25/5.3/96 ms at N=12/1.2k/12k/120k (author: 0.004/0.245/2.9/133.6 — same shape, differences are load only; RSS 484 MB at 120k matched exactly). All commands ≤60 s here.
- **Mechanism verified in code**, not just timed: `advance` rekeys unconditionally (universe.rs:792), the drain defers every not-due entity and requeues it after (805–831), the heap is deadline-keyed while the drain tests tick-due-ness, and `Budget::events(0)` never gates deferral. With no player in this scenario, rekey provably recomputes identical deadlines every frame.
- **Adversarial:** my N=250k extension (158 ms empty frame, 9.5× the 16.7 ms budget, no superlinear cliff), threads=8 + rtf=100 (fixed tier serial, 0 events), and an independent check that events-rare holds (~4 expected kicks over the whole frame loop).
- **Predictions:** P1/P2/P4/P5 held; P3 borderline and disclosed by the author against its own claim. Pre-registration timing is unverifiable (run.log is 0 B, mtimes re-stamped) — flagged in the check.
- **Novelty/goal fit:** no prior HISTORY entry measures the frame's fixed tier in N; it corrects plane.md foundation 7's premise ("nothing takes an unbounded synchronous claim on the frame") — the scheduler itself is that claim, with the budget unspent while the frame is 5–8× over. Lands directly on board #4 and the top scaling risk, before `b-belt-wire` can ship ships into the wall.

Missed by the author (recorded): no-player probe leaves the rekey player path and `root_state_raw` unexercised; "BodyRecs three times" overcounts (drain pops heap slots, not records); "five orders" is 4.2–4.8; the p50-vs-empty-frame gap is load noise, not stable; and the fixes are priced from code reading, not A/B-measured.
