# Dossier — 20261016-1740-spacex-3999 (spacex lens)

## Claim

The player's scan latches inside the belt at every N the plane already flies (measured: fallback +
answer-latch at N = 10³, the ladder's own rung; 0.994·N reads at 4.2 µs, zero encounters, nearest
miss ~2×10⁶–6×10⁷ reach), the fallback is **belt-band occupancy** (eccentricity tails put ≥ bodies/4
in every core bin — not a small-N disease), and the priced angular cure cannot reach its "tens of
µs" soundly: a mean-longitude certificate must carry the ±2e anomaly margin (0.14 rad at the belt's
σ_e = 0.07), ~50× fatter than the 3×10⁻³ rad sweep term, keeping ~4.5% ≈ 23 ms of reads at 10⁵.

## Bottleneck

The board's first focus ("the queue" term of the N ladder) and scan-queue's named unmeasured regime:
cdf0 — "the belt-bin regime (the player inside the belt) stays unmeasured"; "re-measure per doll
before pricing a cure there". The scan is the player's only encounter/HUD seam (plane.md: impacts
warned minutes ahead). Measured: it dies exactly there, at the plane's own flown N. The gain at
stake is the whole seam (unbounded: without a cure no exact answer is ever served in a belt), and
what it lets us delete: the `bodies/4 + 64` fallback rule's O(N) walk (0.10 µs/body) and, at 10⁵,
10.6 ms of frame-path capture per scan mint.

## Evidence

Shipped code only, plus one print-only example (`belt_scan_probe.rs`, in this folder; the patch adds
nothing else). It builds the plane with the ladder's population (`plane_with_extra`, seed 1; seed 2
held out), then asks the shipped `Radial::candidates` for real bodies' windows and times the shipped
capture walk (`PlayerNeighbourhood::capture`'s loop) and answer (`Scan::compute`'s loop: one
cartesian readout + the exact `law::hit` per candidate). The belt window is a real belt body's own
window (its r, v, step h, radius), doll 0, r = 2.5 AU. Reproduce: `bash
lab/results/20261016-1740-spacex-3999/regen.sh` (~1 min warm).

| N (extra) | fallback in-belt | pass (doll-0 candidates) | capture | answer S | latch (bar 2.5 ms) | encounters |
|---|---|---|---|---|---|---|
| 10³ | **yes** | 714 | 47–75 µs | **2,905–3,088 µs** | **answer latches** | 0 |
| 10⁴ | **yes** | 9,714 | 1.11 ms | 41.2 ms | answer latches | 0 |
| 10⁵ | **yes** | 99,714 | **10.0–11.3 ms** | **415–435 ms** | **both latch** | 0 |
| 10⁵ seed 2 | **yes** | 99,714 | 10.0 ms | 418.7 ms | both latch | 0 |

- Per-read 4.07–4.85 µs (one contended 10⁴ run at 5.68), flat in N (cdf0's 4.5–8.5 µs band, independently reproduced); capture
  0.046–0.152 µs/walked (the machine is shared; the deterministic cells are bit-identical), flat. Latch arithmetic: the answer reads N − 314 doll-0 bodies (the
  non-root-doll constant at every measured N — 714/1,028 at 10³, 99,714/100,028 at 10⁵), so it
  latches from (N − 314) × 4.2 µs ≥ 2.5 ms ⇒ **N ≈ 9×10²** (measured: latched at 10³);
  capture latches from N ≈ 2.5×10⁴ (0.10 µs·N = 2.5 ms), and the capture runs **inside the player's
  item on the frame path** (`universe.rs:772`, the code already anticipates the player in the root
  doll at :769) — at 10⁵ the belt costs 10 ms of frame per scan mint, before any answer.
- **Why the fallback trips — occupancy, not window width.** The radius sweep (stand-in's v, h): the
  fallback fires for r ∈ [1.75, 3.0) AU and nowhere else (kept = 3–7 bodies outside, 11,184 at 3.0,
  10,881 at 1.67, fallback at 1.75–2.75). The window itself is narrow (reach = near + (v+cap)·h ≈
  0.04 AU ≈ 0.36 bins); what trips `hit + unbounded > bodies/4 + 64` is that the belt's
  eccentricity tails (Rayleigh σ_e = 0.07, redrawn ≤ 0.4) put a body's whole [peri, apo] range into
  the index, so every core bin holds ≥ bodies/4 once N ≳ 700. cdf0's "small-N disease of the plane's
  own regime" is the same rule read at the Home doll; in the belt band it is an every-N disease.
- **The slack is real but not cheaply reachable.** Zero encounters at every N and seed; nearest
  candidate's miss 2.1×10⁶–5.7×10⁷ × reach; its angular separation 4.2×10⁴–1.1×10⁵ × reach. A sound
  pre-read cut in **true** longitude needs threshold ≈ (reach + |w|h)/r: |w|h with each body's own
  rate ≈ 2.9×10⁻³ rad ⇒ keeps ~0.1% (~95 bodies at 10⁵, 0.4 ms — enough) — but true longitude at
  scan t **is** the 4.2 µs readout. The cheap axis is mean longitude (key + periapsis_angle + a
  linear rate), and it must carry the anomaly margin: max|ν−M| = 2e (verified: 0.1401 rad at
  e = 0.07, 0.816 at 0.4), so the sound mean-longitude window is ±0.15–0.28 rad ≈ 4.5–9% of the
  circle ≈ **4.5–9 × 10³ reads ≈ 19–38 ms at 10⁵ — 8–15× over the bar**. The sweep term and the
  anomaly term are the two halves of the price, and the anomaly term dominates by ~50×.
- **Controls.** Player's own Home-doll window at 10⁵: no fallback, kept 8, pass 7 (cdf0's
  "6 of 100,071" class — the instrument agrees with the shipped record). Empty belt (extra = 0):
  kept 1, no fallback. Huge-h window: falls back (the rule fires when it should). `hit` verdicts
  exact in i128 (`law::hit`), digests untouched: no engine file is modified; the probe only reads.

## Predictions

Written before the probe ran (`predictions.md`). **Held:** P2 (answer latches in-belt, per-read
4–9 µs flat, capture never the latch term below 10⁴), P3 (hits ≤ 2 — measured 0; reads/hit ∞),
P4 (all controls), P5 (costs flat in N). **Refuted, and the refutation is the result:** P1 — the
`bodies/4+64` fallback DOES trip in-belt at 10⁴/10⁵ (I modelled one bin ≈ N/16 under the threshold;
the eccentricity tails' range-hull registration puts ≥ bodies/4 into every core bin instead). The
latch threshold also moved the other way: predicted from ~5×10³, measured at 10³ (the anomaly:
occupancy, not kept-count, drives pass to 0.99·N).

## What would make it wrong

A flown 20-s session with the player actually resident in the belt doll (the scenario pins the
player to Home's doll; the probe substitutes a real belt body's own window — every parameter is the
engine's, but the end-to-end frame trace is not flown; the capture's 10.6 ms at 10⁵ could interleave
with the queue's pull burst, making the frame worse, not better). The Home-doll and hauler controls
tie the instrument to cdf0's shipped-flight census, and seed 2 holds every number. The anomaly-term
price assumes the certificate registers nothing at events; a true-longitude registration refreshed
at each binding event goes stale on the orbit timescale (a quiet belt body's last event is its
birth), which is why the cheap axis is mean longitude — that assumption is the design fact to
attack.

## Cost of adopting / fit

Nothing to adopt as code: this closes the page's open measurement and reprices its cure. The design
consequence for the integrator (one sentence, three measured legs): the seam inside a dense belt
cannot be a per-pair exact scan at any flown N — either reads get ~50× cheaper (closed-form kernel,
`closed-form-kernel`: 4.2 → ~0.5 µs, and the fat-but-sound mean-longitude cut then lands at
~2.4 ms, marginal at 10⁵), or the candidate axis becomes phase-neighbour rank (the encounters gold
`20261006-0346-taleb-09b5`: every real encounter within partner rank 4 along the orbit), or the
belt doll is answered at population level, never per body. PRINCIPLES #5: "Priority is slack, not
proximity" — the belt's slack is measured at 10⁶× reach and the seam still latches; the
representation, not the schedule, is what spends it.

## The lens

SpaceX's question→delete→idiot-index asked "what does the scan cost per real encounter?" — answer:
in-belt, 0.99·N × 4.2 µs per **zero** encounters; the idiot index is infinite, and the delete target
is the fallback's O(N) walk. What the lens may have missed: the machine frame — these are shared-x86
timings, orders of magnitude only (the M1 re-measures); and the red-team's angle (could the
fallback's conservatism be a *soundness* bug in the other direction?) is untested — `range_of`'s
widenings were assumed correct, not audited.
