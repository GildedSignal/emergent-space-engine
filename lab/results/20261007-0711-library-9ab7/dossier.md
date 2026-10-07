# dossier.md — run 20261007-0711-library-9ab7 (library lens)

**Claim.** The plane's hitch risk cannot be sized from bench percentiles or the
bench maximum: under fat-tailed event sizes (α ≈ 1.5) matched-percentile
streams hide an 11.5× spread in the true once-per-hour frame, the bench max
itself varies 26× between benches, and moment extrapolation underestimates by
27× — so the smoothness gate must estimate the event-size tail exponent, and
utilization (slack), not queue ordering, governs the dip duration the player
feels.

**Bottleneck.** Board #4 (smoothness and the allocator) and plane.md's
"Measured on the whole" list; H0161's open limitation ("cost forecasts whose
tail behaviour is unknown until measured") is the seam. Gain: no 10× speedup
claimed; the gain is *deciding correctly where the 10× smoothness lever is*
(slack sizing + bounded admission units + deletion quota, not scheduler
tuning) and deleting one class of work (queue-policy tuning for burst-dominated
classes) from the bottleneck list.

**Evidence** (commands, each ≤ 60 s, run in this folder on the Actions runner,
Linux/x86 — orders of magnitude only):
- `python3 probe_tail.py` (3.3 s) → sizing table: streams with identical bench
  p50=4.0, p95=4.2, p99.9≈12.2–12.8 have truth/h 28.4 : 55.4 : 326.8
  (light : α=3 : α=1.5); Gaussian rule gives 6.5 : 6.8 : 11.9 (27× low on
  α=1.5); Hill-on-frame-totals gives 139 : 207 : 154 (2–5× biased both ways —
  threshold bias). Queue sim (200k frames, budget = bench p99.9, backlog
  carryover = plane §7 overflow): FIFO vs EDF misses — light 2.60e-4 → 1.85e-4
  (−29%), α=1.5 2.54e-3 → 2.79e-3 (+10%, i.e. second-order).
- `python3 probe_rtf.py` (1.8 s) → bench-max noise over 30 benches: light
  24.8±3.3, α=1.5 186±185 (range [32, 844]). RTF dips (budget-capped
  execution): worst dip length α=1.5: 59 / 287 / 1680 frames at ρ = 0.5 / 0.7 /
  0.9 (1 s → 28 s of degraded real-time factor); light-tailed: 6 / 14 / 80.
  RTF instantaneous depth p0.1 ≈ 0.35–0.36 in both (the budget caps depth; the
  tail governs duration).
- Field anchor (not re-measured here — the lab tree has no per-frame trace):
  plane.md's own numbers give worst/p99 = 14.5/2.72 ≈ 5.3 (sonnet-plane2), where
  light-tailed frame times give ≈1.3–1.7 over 36k frames. [INFERENCE]
- Quotes verbatim from the cached Readwise export (`data/highlights.tsv`,
  `data/readwise_books.json`; 770 books, 4,580 highlights, fetched with the
  token, pagination cached).

**Predictions** (`predictions.md`, written before the probes): P1 held (>10×
divergence at matched percentiles: 11.5×). P2 half-held: Gaussian ruin
confirmed (27× under), but Hill was *not* within 2× — naive Hill on mixed
frame totals is threshold-biased; the fix (estimate the exponent on the
event-size stream, where the engine's bursts are identifiable events and
samples are plentiful) is adopted into the recommendation, not the naive
estimator. P3 partially held: par15 does not tolerate ρ=0.9 (dips saturate in
frequency but the worst dip reaches 1,680 frames = 28 s), and the light stream
was not hitch-free at ρ=0.9 as predicted (misses 7.95e-4/frame) — reported as
held-out miss; the utilization knee shifts right but the duration explosion is
real (21× worse than light at ρ=0.9). P4 held (EDF second-order under fat
tails, ±10%; first-order under light tails, 28.8% vs the predicted 30%,
borderline).

**What would make it wrong.** The engine's real event-size stream could be
thin-tailed (α large or bounded sizes by construction — the law's integer
quantization and bounded admission units may already truncate it); then bench
percentiles suffice, ordering regains first-order status, and only lesson 5
survives. The queue model is single-budget preemptive with carryover — no
core/GPU multiplexing, no work stealing; and the dip-length metric assumes
backlog is player-visible as RTF dip, as plane.md §7 states. The
matched-percentile construction uses 0.5% burst frames with Pareto/lognormal
sizes — a different burst rate moves the ratios but not the mechanism
(sample-order statistics do not converge in Extremistan).

**Cost of adoption.** One measurement on existing bench logs (exponent of
kick/encounter event sizes; a Hill plot on the event stream), one line in
plane.md's measured list, and a utilization policy for the frame budget. No
code path changes; gates B15's smoothness report gains a tail line.

**Fit with PRINCIPLES.** "i care about the p95/99 results i want the game to be
smooth" (CL 09-25 14:06) — but plane.md itself warns "a percentile alone can
hide a 200 ms freeze once a minute": this run supplies the missing estimator
(the tail exponent on events, not frames). "Compute only surprises. Cost
follows change and entropy" — the tail *is* the entropy of the surprise
stream; sizing by its exponent is principle 3 made operational for the frame.
"Use idle time to compute ahead" and "the algorithm that allocates the work to
prevent those heavy tails" (OC#36, CL 09-25 14:28): lessons 2–3 show the
allocation's lever is slack sizing and bounded admission units, exactly "the
best part is no part" applied to the queue.

**The lens.** A library lens buys mechanisms with skin in the game but risks
analogy over measurement; I kept only lessons that change a decision and
probed them, but the probe is synthetic (the runner carries no engine trace),
and the two Taleb-dominated lessons share one source's bias: he sells fat
tails everywhere. The honest counter-weight is that the plane's own worst/p99
ratio (5.3) and the allocator's measured pile-ups already point the same way —
the un-run step is measuring α on the shipped engine's event stream, which is
the integrator's to assign (queue candidate: extend the bench, not the queue).

**Artifacts.** `lessons.md` (the ≤40-line deliverable), `predictions.md`,
`probe_tail.py` + `probe_out.json`, `probe_rtf.py` + `probe_out2.json`,
`data/highlights.tsv`, `data/readwise_books.json`.
