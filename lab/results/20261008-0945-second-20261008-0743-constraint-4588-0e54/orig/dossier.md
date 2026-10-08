# Dossier — constraint lens, 20261008-0743

**Claim.** On the plane as the player flies it (≤ a few hundred visible bodies, ~100× time), the
frame's constraint is not the engine the board's queue optimizes but the **view gather**: an
unbudgeted, every-frame, O(N) light-cone walk holding 60–70 % of frame compute (~6–9 µs per seen
row), while 54–83 % of its rows change by less than one display quantum per frame — so the
cheapest 5× is a display-quantum row cache (a presentation memo, no law change), and only above
~10³× time does the constraint move back to the engine's kicks, where the queue already aims.

**Bottleneck.** The board's live list (fewer kicks, changeover, encounters) was derived from
engine introspection. Measuring the whole frame as the player runs it re-ranks it: at rtf 100 the
engine is 20 % of frame CPU (p50 0.047 ms, budget-capped tail), the gather 67 %. Gain: deleting
~80 % of gather rows ≈ 1.4–2 ms/frame at today's N (room for ~2–3× more visible bodies at the same
smoothness), and it deletes nothing else — no law, no gate, no memory layout touches.

**Evidence** (Linux x86, 8 vCPU shared, load 0.3–1.3; orders of magnitude only, per lab rules).
Commands, each ≤ 60 s unless noted:

- `cargo run --release -p xtask -- universe --bench --rtf 100 --seconds 30` — paced dashboard:
  view_gather share 0.70 (p50 3.49 ms), engine 0.17, json 0.09, wire 0.04; frame p50 4.46 ms;
  41 overflow frames; kick resolver median 35 µs (`universe --kick-bench --rtf 100 --seconds 20`).
- `cargo run --release -p xtask -- universe --bench --rtf 100 --seconds 20 --unpaced` — same loop,
  unpaced: view_gather p50 **0.73 ms** (share 0.67), engine p50 0.047 / p99 1.44 (share 0.20),
  frame p50 0.91 ms. **The paced numbers are a uniform ~4.8× inflation of every segment**
  (gather 4.8×, json 4.8×, wire 4.9×) — the shared runner's wake path (frequency idle-down between
  60 Hz sleeps), not work; frame_cpu tracks frame_ms, which is frequency, not descheduling.
- Members sweep (unpaced, rtf 100, 20 s; `--members 48|200|400`): gather p50 0.72 / 1.66 / 2.65 ms
  at 76 / 221 / 428 bodies → 6.2–9.4 µs per row, linear, per-row flat; frame p50 0.91 / 2.13 /
  3.52 ms, p99 2.5 / 7.8 / 10.1 ms; engine p99 pinned at the 5 ms budget; overflow frames 3 / 29 /
  109 (9 % at 428); delivered rtf lowest-1 % 100 / 19.8 / 0. The mean fits; the tail breaks the
  100× promise by 428 bodies.
- rtf sweep (unpaced, 76 bodies): rtf 10⁴ (`--rtf 10000`) — engine p50 1.34 ms, share 0.56; gather
  1.64 ms, share 0.41; kicks 25,598 (21/frame); 133 overflow frames; delivered lowest-1 % 1,428×
  of the asked 10,000×. The engine crosses above the gather between 100× and 10⁴×.
- Coherence (the instrument `constraint_view`, added in this run's patch;
  `cargo run --release --example constraint_view -p emergent-universe -- 20 RTF 1 5 M warm`):
  fraction of seen rows whose sky angle moves < 0.05° (≈ 1 px at 1080p/90° FOV) **and** colour
  shift changes < 0.1 % between consecutive 60 Hz frames — rtf 1: 75.9 % (bodies 100 %, fleet
  62 %); rtf 100: 82.7 % (bodies 80.5 %, fleet 84.6 %), 81.4 % at 221 bodies; rtf 10⁴: 53.6 %
  (bodies 77.5 %, fleet 17.9 %). Reproduces the unpaced bench (gather p50 0.712 vs 0.73 ms) with
  ~0.7–1.5 readouts per row.
- Gates (state, matching HANDOFF; nothing new): `behave --law plane` — B10 FAIL (not implemented),
  B11 FAIL (binaries 0/1024; the known two-body-parent gap), B12 FAIL (oracle domain known-wrong,
  redesign in flight), B13 60/64, B14 times out at 60 s. `engine-judge` — E1–E5, E7, E8 PASS;
  E6 FAIL UNSUPPORTED (mutants unprepared); E9 FAIL 10/21 (phase 1, as designed).

**Predictions** (`predictions.md`, written before the sweep): two of four held. The falsifier in
prediction 1 fired: the live gather is **0.7 ms, not 3–6 ms** — the 3.5 ms dashboard reading is the
pacing artifact, and the constraint claim survives on unpaced shares, corrected in magnitude.
Prediction 2 (readout-count inflation from kicks) wrong — readouts stay ~0.7–1.5 per row with the
burn script running. Prediction 3 wrong in magnitude (built on the inflated 46 µs/row: gather at
428 bodies is 2.65 ms, not ≥ 12), right in kind at the tail (9 % overflow, lowest-1 % rtf → 0).
Prediction 4 held exactly (overflow 3 → 29 → 109, engine p99 at the budget cap).

**What would make it wrong, adoption cost, fit.**
- *Wrong if* the visual layer that "comes later" (plane.md) does not read crossings at ≥ 60 Hz per
  body (then the quiet fraction measures a consumer that will not exist), or if effects need every
  row fresh (trails, blur) — the fleet rows at 10⁴× are already only 18 % quiet, and they are the
  ones the player watches. The quiet fraction itself is geometry, machine-independent; the µs are
  not (re-measure on the M1).
- *Cost:* a row cache beside `ViewCache` (which already memoizes the crossing *search* the same
  way), plus one behaviour gate at display quantum instead of the crossing memo's bitwise
  equality. The view reads and never writes (plane.md law 5), so no engine certificate can see it.
  The floor must come from what the player can differentiate (PRINCIPLES #28), not from a constant
  someone likes.
- *PRINCIPLES:* #3 "Nothing is evolved that can be derived when looked at (clocks, redshift,
  **views**)" — the view is the named example, and today it is re-derived wholesale every frame;
  #12 (p95/99 smoothness) — the gather is the mean constraint, the engine budget the tail;
  #1 delete before optimizing — drop quiet rows before profiling `state_rate`'s ~7 µs.
- *Flag to the integrator:* paced cloud dashboards overstate every segment ~5× on shared runners;
  judge shares or unpaced numbers, and re-measure on the M1 (already the rule; now it has a
  measured cause).

**Where the constraint moves next.** Below ~10³× time: the gather, growing linearly with visible
bodies (~6–9 µs/row → ~1,500–2,700 rows max per 16.7 ms frame on this box, less on the M1); a
fleet battle in a Fermi frame (plane.md's next slice) hits that ceiling first. Above ~10³–10⁴×:
the engine's kicks (25,598 kicks at 10⁴×; 21 per frame; the budget saturates and delivered rtf
collapses to 14 % of the ask) — the board's kicks queue is the right constraint there, and the
crossover itself is the number to re-measure on the M1.

**The lens.** Goldratt's "measure the whole" is what re-ranked the board; but the constraint lens
looked only at the plane (the galaxy doll, where billions live, was not measured), only at frame
time (bytes_per_body 4,782 and H_live — the memory constraint — untouched), and TOC's
"exploit before elevate" means I did not open `state_rate`'s per-readout cost, which may hide an
easy constant. One instrument artifact (paced inflation) cost two wrong predictions before the
control (unpaced + the independent example) caught it — the memo-artifact lesson again: runs that
share a harness share its blindness.
