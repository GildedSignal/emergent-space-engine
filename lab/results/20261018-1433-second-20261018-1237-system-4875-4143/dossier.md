# Dossier — 20261018-1433-second-20261018-1237-system-4875-4143 (second author on 20261018-1237-system-4875)

**Claim.** The experiment the checker named for gold is done — 2df1's row-set deletion wired into
`Session::step` itself (`--rows`, this run's patch: the original `--extra` knob + 2df1's
`gather_rows` + a ~470-line port of the flyframe2 policy into `xtask/src/universe/rowset.rs`) — and
the first author's ranking holds end-to-end in the flyable frame: at 10,071 bodies the frame
collapses **264.6 → 1.20 ms p50 (220×)** with the engine bit-identical (digest at equal cut:
`03abdbc9…` both arms) and still inside its 5 ms budget (p99 4.45 ms), flat in N to 3×10⁴
(1.39 ms p50 at 30,071), the wire at 26 KB/frame against ~2 MB, and the display exact to
0.32–0.39% of drawn rows against the shipped gather — so the view's row-set deletion is now a
measured flyable cure, not a page-authority figure, and the adoption order (view first, engine
cures bind again only past ~10⁶) is proven on the frame the player runs.

**Bottleneck.** The board's #1 (bodies in the flyable engine, 28 → 10⁹). The first author measured
the gap (flyable frame view-owned from ~794 bodies; 99.7% of the frame in the view's Θ(N)
channels); the silver's open half was whether the built-but-unwired deletion actually collapses
the frame loop it was never flown in. This run wires it and re-flies the exact matrix: it does.

**Evidence** (Linux/x86, 8 vCPU, load recorded in the JSONs, orders of magnitude; `regen.sh`
regenerates every number below in ~4 min from shipped code + `work/patch.diff`; the same-day
baselines reproduce the first author's arms: 10⁴ 264.6 ms against its 261.8, view share 0.997,
engine 0.10/4.68):

| arm | bodies | frame p50/p99 ms | over 16.7 | engine p50/p99 | gather p50 | wire KB | served rows | readouts/frame |
|---|---|---|---|---|---|---|---|---|
| b0 baseline (shipped plane) | 71 | 1.02 / 3.19 | 0 | 0.06 / 2.10 | 0.78 | — | all | — |
| b10000 baseline | 10,071 | 264.6 / 280.7 | 360 | 0.10 / 4.68 | 234.9 | ~2,000 | 10,071 | — |
| r0 rows | 71 | 0.95 / 3.00 | 0 | 0.05 / 2.02 | 0.76 | 13.9 | 46 | 69 |
| r1000 rows | 1,071 | 1.16 / 6.47 | 0 | 0.07 / 4.39 | 0.85 | 25.9 | 88 | 108 |
| **r10000 rows** | **10,071** | **1.20 / 37.8** | **32** | **0.06 / 4.45** | **0.89** | **26.3** | **88** | 368 |
| r30000 rows (held-out decade) | 30,071 | 1.39 / 205 | 25 | 0.06 / 4.60 | 0.95 | 26.9 | 91 | 1,422 |
| r10000s2 rows (held-out seed) | 10,070 | 0.97 / 67.6 | 25 | 0.06 / 4.50 | 0.66 | 23.3 | 78 | 511 |

- **The collapse:** 20× at 10³, 220× at 10⁴, and at 3×10⁴ (outside the first author's range) the
  p50 is still 1.39 ms — the steady frame is flat in N; what scales with N is gone from it.
- **The engine is untouched:** digest at the same cut bit-identical with and without `--rows`
  (checked at 10³ pre-predictions and at 10⁴ in the matrix); engine p99 4.4–4.6 ms in every arm,
  overflow 0 — the ladder's own record holds on the same flights.
- **Exactness (the audit, the control):** the shipped `gather_cached` compared every 30 frames
  against what the client would draw from its held rows (the page's own draw conditions): 0.32%
  of drawn rows at 10⁴ (3 violations in 947 rows), 0.39% at 10³, panel violations 0 — inside
  2df1's own residue band (its fit-zoom 1.2/frame ≈ 0.4%), same cause (hand-off births between
  event-feed scans). The audit runs after the frame is timed and is charged to no channel
  (audit arms' p50 = 1.19/1.21 ms, same as the r-arms).
- **The warm-up transient (new, unpredicted):** the first ~30 frames after the fill are heavy —
  worst 68 ms at 10⁴, 206 ms at 3×10⁴ — because the fill's initial dues bunch the whole
  population into the first backoff steps (2df1 untimed 30 warm-up frames for exactly this; this
  wiring times frame 1, honestly). It is bounded, not periodic: 25 frames over 16.7 ms in a
  180-frame run, 32 in a 360-frame run, all in the gather channel, all early (worst at frame 6–7);
  the run-averaged readouts/frame (368 at 10⁴, 1,422 at 3×10⁴) are transient-dominated — the
  steady gather p50 (0.89–0.95 ms) is the frame's own number. A first-cohort spread in the fill's
  dues is the one-line cure if the page's loading second does not absorb it.
- **The wire:** median 23–27 KB/frame at 10³–3×10⁴ (against the baseline's ~2 MB at 10⁴, a ~75×
  wire cut), served 78–91 rows/frame against 10⁴–3×10⁴ bodies.

Commands: `xtask universe --bench --unpaced --seconds S --rtf 100 --extra N [--rows
[--rows-audit K]] [--seed 2]` (S = 10/10/6/10/10/6/3/3/6/6 per arm, in `regen.sh`); the 3×10⁴
boundedness probe (`--seconds 6`, hitch counts 25→32 at 2× the frames) is `work/r30000_6s_probe.json`.

**Predictions** (`predictions.md`, written before the matrix). Held: the 10⁴ collapse (≤ 3 ms →
1.20), the held-out decade (≤ 5 ms → 1.39 p50), wire ≤ 40 KB (26.3), served ≤ 150 rows (88–91),
the audit ≤ 2% (0.32–0.39), panel 0, the control plane ≤ 1.2 ms (0.95 — no regression), seed 2
within 20% (0.97 vs 1.20), engine digest identity, fill linear (5.7/45/133 ms across 10³/10⁴/3×10⁴).
Missed, both disclosed: the readout counter's run-average constant (predicted ≤ 250/frame, measured
368 at 10⁴ — transient-contaminated, see above), and the warm-up transient itself, which I did not
predict (the p99 story is the transient, not the steady frame).

**What would make it wrong.** The bench stops at the wire: the page's client half (hold rows by id,
apply deltas, derive rotation and zoom locally) is still 2df1's stated adoption cost, not built —
the served page and the browser's parse remain unmeasured, as in the first author's run. The audit
is the map display at the fitted zoom; belt zoom (62c1's ~N rows on canvas) and the sky's near
field (2df1: O(locals), does not collapse) are not flown here, so "flat to 3×10⁴" is a
map-display statement at the fitted zoom. The transient's worst frame grows with N (one fill
cohort ≈ 6.8 µs/body); at 10⁶ it would be ~seconds unless the fill spreads its first dues —
named, not fixed here. The row-set policy is 2df1's, not mine: its pixel-quantum choices (20 px
margin, half-pixel serve, one-pixel violation) are inherited design decisions I did not re-derive.

**Cost of adopting.** `gather_rows` + the factoring are 2df1's ~300-line view.rs change
(byte-identity to `gather_cached` proven there by rolling digest); the policy port is ~470 lines
in xtask (`rowset.rs`); the session wiring is ~60 lines. No law change: the engine digest is
identical, and the view is pure derivation (PRINCIPLES #3 "clocks, redshift, views are derived,
never evolved"). The remaining adoption work is the page's client half.

**Fit with PRINCIPLES.** #1 "the cheapest compute is compute not done": 98.9% of the 10⁴ gather's
readouts are deleted in the steady frame (368 average, transient-dominated; steady ~40/frame by
gather cost) because the display's own quantum says they cannot change a pixel. #28 "the view is
an instrument": the quantum is the pixel, held in the client's frame, not the server's tick.
#27 "The goal, never a proxy": the first author's silver said the flyable frame's ranking rested
on a figure taken on page authority; it now rests on the frame loop itself. #12 (smoothness):
the steady frame is 14× under budget at 10⁴ with zero hitches after the transient; the transient
and the fill are the named residuals.


**Instrument notes.** the universe crate's tests pass on the patched tree (10 lib + 16
 integration); the `nladder` example fails to link on Linux at **pristine HEAD** already
 (`proc_pid_rusage`, a macOS-only symbol, verified on an unpatched archive) — pre-existing,
 untouched by this run's patches, which touch no example.
**The lens (what the second-author lens may have missed).** I inherited the first author's
instrument boundary (bench-to-wire) and 2df1's policy constants rather than re-deriving either;
the p99 finding is mine but its cure (spreading the fill's first dues) is asserted by mechanism,
not measured; and I fly one display mode (map, fitted zoom) — the sky and belt zoom, where 2df1
and 62c1 both found Θ(N) residues, are the honest next probes before "10⁶ flyable" is claimed.
