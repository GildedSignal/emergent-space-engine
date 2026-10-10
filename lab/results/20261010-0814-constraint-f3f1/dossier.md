# Dossier — run 20261010-0814-constraint-f3f1 (lens: the constraint)

**Claim.** On the current main, the frame's constraint is the view gather (60–72% of frame time;
at 417 bodies the worst frame is already 15.5 of 16.7 ms), and inside it the per-body retarded
readout, which is bimodal — ~11–15 µs on the tube path and 28–95 µs whenever the read lands
inside kick machinery (partial step / window) — so the cheapest frame-level lever is the queued
readout fix (b-readout-cost), after which the constraint returns to the engine's kick path (the
board's #1).

**Bottleneck.** Board focus "the plane flies, work goes by its measured bottleneck": which one
binds the *frame* (smoothness at 60 Hz) as opposed to the engine's internals. Measured answer:
the gather. This orders the two queued builds (readout before slack skin) and prices them.

**Evidence** (Linux x86 cloud, 8 vCPU shared, load ~0.5–1.2 recorded via uptime; orders of
magnitude only — the integrator re-measures on the M1). All commands from the repo root, binary
built `cargo build --release -p xtask` with this run's measurement patch (work/patch.diff; adds
timers around the gather's phases and a per-frame series to the bench report — verified
bit-neutral: identical digest `6ce636fa…` before and after the patch at seed 1, 20 s, cut
406050894):

1. Whole frame, `xtask universe --bench --rtf 100 --seconds 20` (seed 1, paced 60 Hz):
   - frame p50 4.57 ms / p99 10.4 ms / worst 11.8 ms; 0 hitches > 16.7 ms; RTF median 100.
   - shares: **view_gather 0.68–0.72, engine 0.20 (budget-capped: p99 5.17 ms vs 5.0 ms
     budget, 29–43 overflow frames), view_json 0.09, wire 0.04** (bench-r100-s20.json,
     bench-r100-s20-recheck.json, bench-r100-s55.json).
   - for contrast, the kick resolver alone (`--kick-bench`, pure resolver): median 35 µs,
     leavers 92 µs — the engine's cost is concentrated in rare budget-tail frames, the gather's
     in every frame (kickbench-r100.txt).
2. Gather decomposition (last frame, patch): **bodies phase 94–96%** of gather ns
   (3.37–3.41 ms of 3.56–3.62 ms in expensive frames; 0.68–0.73 ms of 0.72–0.87 ms in cheap
   frames); observer 0.02–0.13 ms; fleets (48 members) 0.004–0.066 ms.
3. Readouts per gather ≈ 1 per body (48–62 for 48–50 crossed bodies): the light-cone memo
   already works; the *eval* is what gets expensive:
   - cheap frames: 10.9–15.1 µs per readout (depth-1 bodies 18.9–19.6 µs/body, deep 10.4–11.3);
   - expensive frames: 57.7 µs per readout (depth-1 95.0 µs/body, deep 54.1) — the partial
     step / kick-window reader path, whose cost also scales with the doll's source count
     (root-doll bodies are the priciest).
4. The expensive mode is canonical in existence, schedule-dependent in share: 95% of frames in
   the 20 s runs, 33% in the 55 s run (gather series in bench-r100-s55.json: 0.8 ms for t=0–31 s,
   3.24 ms for t=32–50 s, 0.73 ms after; the 20 s recheck: 0.73 ms at frame 0 then 3.4–4.6 ms
   throughout). Same seed: the share moves with the wall schedule (engine budget overflows
   shift which presented ticks land inside kick windows), but both modes appear in every run.
5. Gates (this box): `behave --law plane` → B11 FAIL (precession 0/1024, *worst inf*: the float
   reference itself diverges here — an oracle-side blow-up, not a marginal miss; needs
   adjudication on the M1 before anyone blames the law), B12 FAIL (statistic known miscalibrated,
   redesign in flight), B13 FAIL 60/64 (marginal, known), B14 timeout 60.1 s on this slower box.
   `engine-judge`: E1–E8 pass; E9 fails phase 1 as designed (engine-judge.txt; matches the
   handoff).
6. Scale probe, `xtask universe --bench --rtf 100 --seconds 15 --members 400` (417 bodies —
   handed-out members become real bodies): frame p50 8.7 ms / p99 14.1 / **worst 15.5 ms**
   (one bad frame from a 16.7 ms hitch), gather 60% of the frame (p50 6.1 ms, bodies phase
   6.9 ms at 27.8 µs/readout, expensive mode), fleet loop 0.042 ms for 400 members
   (0.1 µs/member: negligible). Engine overflow on 271/900 frames (engine share 0.26).

**Predictions** (predictions.md, written before the decomposition runs): bodies ≥ 60% of gather —
**held** (94–96%); readouts 1.2–2/body — **missed low** (≈1.0/body: the memo is better than I
predicted); implied per-readout cost will exceed the 8 µs single-readout arithmetic and point at
per-eval overhead — **held** (54–95 µs in the expensive mode); members 400 grows fleets phase
~linearly and fleets stays minor — **half-held**: fleets is negligible (0.042 ms for 400
members) but the growth lands in the *bodies* phase, because handed-out members become real
bodies (417 bodies, gather p50 6.1 ms, frame worst 15.5 ms — see item 6); engine not the frame
constraint at rtf 100 — **held** (engine p50 0.26 ms; only the budget tail p99 5.17 ms).

**What would make it wrong.** If the M1's cheap/expensive mode mix differs so much that the
gather never dominates (its share depends on the schedule; the engine budget's overflow count
moves it), or if the partial-step readout is already fixed by the motion law v2's merged work
(my tree is main at the flight-view merge — steps 1–2 only). Cost of adopting: none for this
dossier (measurement only); the readout fix it prices is already a queued lens.

**Fit with PRINCIPLES.** "Compute only surprises … nothing is evolved that can be derived when
looked at (clocks, redshift, **views**)" (#3): the view is listed as derivable, yet it is the
frame's dominant compute; and "The view is an instrument" (#28): the instrument is currently the
most expensive part of the frame. Also #12 (smoothness): the gather's expensive mode is the
frame tail (worst 11.8 ms of a 16.7 ms budget).

**The lens may have made me miss:** the engine-side scale constraint (kicks per orbit at 10⁹
bodies) is invisible at 76 bodies — my run says nothing against the board's #1; it only orders
the frame-level work before it. B11's inf worst also deserves a proper look I did not give it.

**Next:** b-readout-cost first (its measured ceiling from this run: expensive-mode evals
54–95 µs → the tube path's 11–15 µs is a 4–6× gather cut; frame p99 10.4 → ~6.5 ms, where the
engine's 5 ms budget becomes the tail), then the slack skin (b-encounter-skin).
