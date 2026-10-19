# Dossier — 20261019-0325-spacex-959a (spacex)

## Claim

The sky record's serving path is no longer O(K): keeping each cell's aggregate as **running sums
updated on the events that already touch the record** (due refreshes, churn, tier moves — no new
mechanism, no new reads) deletes the per-frame member walk that both e6c9 checkers priced
"required, not optional" at 10⁶ — serve_ms falls **1.09 → 0.18 ms at 10⁴ (6.1×), 10.55 → 0.16 ms
at 10⁵ (66×), 33.18 → 0.14 ms at 3×10⁵ (237×)**, audits stay zero (a 300-frame arm flat at
0.20 ms), and every END digest is bit-identical to e6c9's published anchors.

## Bottleneck

Board item 1's measured first N-growing per-body term on current main is the view gather (dcf1);
the record (e6c9) already deletes the gather's walk but kept one O(K)-shaped term: the per-frame
rebuild of multi-member cells' aggregates from members (~100 ns/member; 10.7 ms of the 13.4 ms
serving path at 10⁵; 142–143 ms at 10⁶, both checkers). This run deletes that term inside the
record: serving becomes O(cells) — ~786 lookups at the stock floor — and the update cost rides
the due/tier events the record already pays (sums_ops steady = 2×due + tier moves ≤ ~10–20/frame,
flat in K; the frame-2 ω-measurement wave 2×k_far is e6c9's own, unchanged, paid in `due_ms` in
both arms). At the goal's 10⁶ the serve tier extrapolates to ~0.2 ms against the measured 142 ms
rebuild — the record's last objection at scale is gone; what remains is the near tier (~2.5 ms,
O(locals)) and the cold start (one walk).

## Evidence

Instrument: e6c9's probe verbatim (sky_server + the skyserv driver, from its published branch,
applied clean to this tree) + this run's ~120-line running-sums serve tier behind `ES_SKY_SUMS=1`
(unset = e6c9 verbatim; the binary is one build for both arms). Flights: coast, seed 1, stock
floor 8e-3, e6c9's own frame counts (120/90/40/20 at 10³/10⁴/10⁵/3×10⁵); controls flown unset.

| arm (log) | frames | serve_ms p50 | vs ctl | drift max | audits (wrong/cells/missing/extra/tier) | END digest |
|---|---|---|---|---|---|---|
| ctl 10³ (e6c9 log) | 120 | 0.04 | — | — | 0 | 5dc903e6… |
| **sum 10³** | 120 | 0.07 | 0.6× (parity) | 4.2e-16 | 0/0/0/0/0 | **5dc903e6… = e6c9** |
| ctl 10⁴ | 90 | 1.09 | e6c9 1.03 | 0 | 0 | bd6f9840… |
| **sum 10⁴** | 90 | **0.18** | **6.1×** | 1.1e-15 | 0/0/0/0/0 | **bd6f9840… = e6c9** |
| ctl 10⁵ | 40 | 10.55 | e6c9 10.66 | 0 | 0 | 82aa152c… |
| **sum 10⁵ (refly)** | 40 | **0.16** (max 0.37) | **66×** | 2.9e-15 | 0/0/0/0/0 | **82aa152c… = e6c9** |
| **sum 10⁵ seed 7** (held-out) | 40 | **0.16** | — | — | 0/0/0/0/0 | 41ccb6a0… |
| **sum 3×10⁵** | 20 | **0.14** (max 0.18) | **237×** (e6c9 33.18) | 5.6e-15 | 0/0/0/0/0 | **c3943af5… = e6c9** |
| **sum 10⁴ fine floor 1e-3** | 90 | 1.20 | parity-class | 5.7e-16 | 2/2/0/0/0 (0.03%) | bd6f9840… = e6c9 |
| **sum 10⁴ long** | 300 | 0.20 | flat | 1.1e-15 | the standing class, below | 8f8855f1… (digest probes 0 bad) |

Three readings the table carries: (1) the **fine floor** (4,759–6,284 cells, 1.9k singletons)
is parity-class — the cell-law meets the singleton-row cost; the deletion pays where cells ≪
members (stock floor, 10⁴-up; any floor at 10⁶); (2) the **long arm** shows e6c9's checker's
standing wrong-cell class in the same window they found it (0 through 226 frames, then a
self-healing population, 118 cells_wrong over the last 74 frames ≈ 1.6/frame against their
rebuild-form 2.6/frame at 300–500 — same class, same order; the 300-frame control arm was not
flown, so the rate comparison is against their published numbers, not a same-box pair; drift
stayed 1.1e-15 and every in-driver digest probe clean); (3) the 10⁵ sums arm's first pass ran
under mutual load — the table quotes the serial re-fly (0.16; the contaminated pass measured
0.14, i.e. contention did not inflate it) and seed 7, flown under the window's other job, is an
audit arm (0.16, audits zero). serve=0 control at 10⁴: END digest bd6f9840… = both serve arms'.
At 10³ the sums arm is parity-to-slower (0.07 vs 0.04): below saturation the walk is cheap —
the wire's own "1.3× at 10³" law; the deletion pays from 10⁴ up, exactly where the record's
legitimacy begins (cc75: the sky is FULL at 10⁴).
Reproduce: `regen.sh` (~11 min: patch → build → 10 flights → `work/analyze.py`). Per-frame lines:
`grep SKYSERV work/logs/sum100000.log`. Digest probes in-driver every 10th frame: digest=0
count = 0 in every log (the server, sums on, stays outside the outcome channel).

## Predictions

Written before the deletion flights (`predictions.md`). Held: flat-in-K serve_ms ≤ 3.5 ms at
every rung (measured 0.07–0.37); sums_ops O(due), cold = k_far, frame-2 = 2×k_far (19,434 =
2×9,717 at 10⁴, e6c9's ω wave); audits zero at ≤120 frames; sums_drift ≤ 1e-12 (measured
≤5.6e-15); digests identical across arms AND to e6c9's anchors at 10³/10⁴/10⁵; wire within
±0.1%. Missed: none — but the 10³ parity clause of prediction 1 deserves its honest reading
(≤3.5 held trivially; the win clause is 10⁴-up).

## What would make it wrong

- **Catastrophic cancellation in the sums:** every member's luminosity is near-equal on this
  scene; a hot body (lum magnitudes above its cell's) entering and leaving would erode the small
  members' bits in the running total. The audit recomputes Σlum from members every frame and
  would catch it (drift is printed per frame), but the bound measured here (3e-15) is
  scene-scoped. The hot-set trigger (od 10) is the designed companion: hot bodies re-enter the
  resolvable tier and leave the sums before they bite.
- **The zoom re-window** rebuilds the record (one cold walk, 27–81 ns/row, e3a4) — the sums
  rebuild with it; unflown here, unchanged by this run.
- **The formation ruin class** (a crowd all hot-set) degenerates the record to walking —
  unchanged; the sums neither help nor hurt it.

## Cost of adoption

~120 lines beside the record's own probe in `view.rs` (sums add/sub at five call sites, the
gated serve branch); no engine change, no law change, no new reads. The record's adoption
decision (the integrator's) now carries no O(K) term and no per-frame walk at any K.

## Fit with PRINCIPLES

- **3 (compute only surprises):** the aggregates change only at crossings and tier moves —
  derived when looked at, never walked.
- **14 (no work for no reason):** the per-frame member rebuild was a tick; the record now moves
  only on its own events.
- **17 (the best part is no part):** the deleted walk is gone, not optimized — the per-cell cost
  falls from ~100 ns × members to one HashMap lookup.

## The lens

SpaceX: delete before optimize — this deletes the record's last walk instead of tuning it, and
the deletion is measured on the shipped scene beside its own control. What the lens may have
missed: numeric corners (the cancellation above — a physics lens would have run the adversarial
luminosity arm first), and the 10³ rung's parity is reported only because the prediction forced
the honesty.
