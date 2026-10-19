# Dossier — 20261018-2312-second-20261018-2155-spacex-9292-e3a4 (second author, spacex lens)

## Claim

The checker's named experiment is done and the claim holds through the broken window: the root churn
that breaks "0 past half a cell" at (L15 × ≥4× flight length) and (L15 × 10× zoom) is the observer's
own displacement parallax — one shared vector per frame — so the record's designed serve (stored
root offsets, `stored − (o_now − o_at_repair)`, displayed through the shipped `aberration`) needs
**0 staleness repairs at the stock floor in 1.18×10⁷ burned row-frames** (β to 0.64, K-flat 1e3→1e4)
and 1.4×10⁻⁵ per row-frame at the 10× floor; the checker's K-scaling tier (~0.4 %·K) is real only
for the naive angle-store (measured 6.6–12 % of far rows per frame at stock, 13–26 % at 10× zoom,
60–91 % at 100× — the walk in disguise). The record's per-frame far work through the broken window
stays O(occupied cells ≤ 786) + O(near) + O(0 repairs), ~0.1 ms-class against the gather walk's
375 ms/frame at 1e4 on this box: in budget at every scale flown, and at 10⁹ in budget at the 100-ns
due-event repair form (row-priced boundary K\* ≈ 2.4×10⁸ at the 10× floor, ≈ 2.4×10⁹ at stock).

## Bottleneck

The board's first focus term (which per-frame walk breaks first as the plane grows): dcf1 named the
view gather; e6c9 flew the record's coast half; 9292 measured the wildcard's churn and its checker
broke the window, pricing an unbounded staleness tier. This run flies the record's own cost law
through that window — the experiment the checker named for gold — and converts "safe under the
wildcard as flown" into "safe under the wildcard, with the boundary and its price on the page."
Gain: the deletion license (2df1's row-set deletion, e6c9's server) now covers the burn axis at all
flight lengths and zooms flown, deleting the O(K) walk (~500-3700× at the worst measured point)
instead of licensing it only inside a 500-game-s window.

## Evidence

All numbers from `crates/universe/examples/skyserve.rs` (print-only probe beside the shipped
`gather_cached`, the same call the page flies; the record simulated as accounting: per far row the
stored root offset at last repair, served through the exact displacement+aberration composition,
repaired only when the serve error crosses θ/2 — eight policies at once: naive/warp × root/disp
trigger × θ_f/θ_f/10, plus a never-repair drift observer), plane ladder scene seed 1, rtf 100,
12-ms engine budget, near = light-seconds < 100. Reproduce with `regen.sh` (~11 min; logs in
`work/`). The probe's one-step anchors reproduce the checker's broken windows first (the
instrument-check):

- **Arm A (1e3, L15, 1500 frames = 2500 game-s, β → 0.644, rate 0.765, alive throughout):**
  one-step past θ_f/2 per frame — displayed 2.8915 %, root 0.3477 % (checker: 2.9227 / 0.3569).
  Policies: naive-root repairs **6.897 % of far rows per frame (last quarter 12.03 %)**, 39.92 %
  (LQ 54.97 %) at θ_f/10; **warp-root 0 repairs in 1439 intervals at stock**, 38 total at θ_f/10
  (2.8×10⁻⁵ per row-frame, LQ 0.06/frame); warp-disp 0 at stock, 22 at θ_f/10.
- **Arm A2 (1e4, L15, 1115 frames, β → 0.52, wall-truncated):** naive-root **6.592 %/frame (LQ
  11.65 % = 1153 repairs/frame)** — K-flat against arm A; θ_f/10: 44.80 % (LQ 69.28 %). **Warp:
  0 at stock over 1.0436×10⁷ far row-pairs; 149 total at θ_f/10 (1.4×10⁻⁵, LQ 0.51/frame); warp-disp
  θ_f/10 54 total (1.8×10⁻⁶ LQ).** β trajectory K-independent (0.4488 vs 0.4483 at f900).
- **Arm C (1e3, L15, 360 frames at θ_f = 8e-4, the 10×-zoom window):** anchors displayed 42.26 %,
  root 0.4509 % past θ/2 (checker: 46.5 / 0.676 — same window, within probe/stepping variance);
  naive-root **12.97 %/frame (LQ 26.16 %)**, 59.99 % (LQ 91.41 %) at 8e-5; **warp 0 repairs at
  8e-4 and at 8e-5, root- and disp-triggered.**
- **Mechanism (why the warp wins):** the warp's one-step residual is the emitters' own retarded
  orbital drift — p50 7.0×10⁻⁸ rad/frame (≈ v_em·Δt/d̄), p99 4.8×10⁻⁷, max 2.0×10⁻⁶ — coherent,
  accumulating to p99 2.7×10⁻⁴ / max 1.3×10⁻³ rad over the whole 2500 game-s flight (0.31 × θ_f/2:
  no stock-floor row ever crosses). Machine-zero before the belt's first tube steps (jump census:
  0.23 % of row-frames in arm C's first 600 game-s, 56.8 % after at 1e3 — 649c's bit-reproducibility
  era structure). The naive record instead re-pays the observer's parallax β·Δt/d every frame:
  that is the checker's tier, and it grows with β (LQ 12 % at β 0.6).
- **The other tiers, priced:** displayed-cells changed per frame p99 372 of 463 occupied (1e3), 651
  of ≤ 786 (1e4) — the re-map is O(occupied cells), never O(K); occupied cells fall 463 → 364 as
  aberration compresses the forward sky at β 0.64. The zoom re-window (one cold membership pass)
  measures **27-81 ns/row** (0.26-0.60 ms at 1e4; ≈ 30-80 s at 10⁹ — ee30's drain class, one pass
  per zoom event, amortized by the dwell). The near tier empties on an interstellar burn (355 → 0
  by f600; the far tier absorbs the locals: 718 → 1057 far rows, one insert wave of 341; drops
  20-25 = fleet handouts) and re-enters at 1-2 rows inside the belt annulus at 1e3, ~15 at 1e4
  approaching it — near ∝ K × local density, ~10⁴ rows at 10⁹, unmeasured above 1e4 (kept open).
- **Controls:** coast 1e3 (299 intervals): 0/0 anchors, 0 repairs under both policies (the
  pass-side control); L8 interior 1e4 seed 1 (111 intervals, 1.08×10⁶ pairs) and seed 7 (156
  intervals, 1.52×10⁶ pairs): 0/0 anchors, 0 repairs — 9292's interior window and the checker's
  arm D reproduced; the broken-window arms fail the naive policy massively (the fail-side control).
- **Budget at the worst measured point (A2 last quarter):** near 14 rows re-served + 0.5 repairs
  (θ_f/10) + ≤ 786 cell remaps ≈ 0.1 ms-class at ~100 ns/op, against the walk's 375 ms/frame
  (37.9 µs × 9901 far rows on this box; the M1's 5-7 µs/row ⇒ 50-70 ms — already 3-4× over the
  16.7 ms budget at 1e4). **Boundary:** warp repair rate ≤ 2.5×10⁻⁷ per row-frame at stock
  in-flight (0 events in 1.18×10⁷, Poisson 95 %), 1.4×10⁻⁵ measured at the 10× floor (rate ∝ 1/θ
  ⇒ steady-state stock ≈ 1.4×10⁻⁶): at 10⁹ far rows the tier is ≤ 250 repairs/frame at stock to
  1.4×10⁴ at 10× floor — **1.4 ms at the 100-ns due-event price (e6c9's running sums, already
  required at 10⁶), 70 s at the 5-µs row price: K\* ≈ 2.4×10⁸ (10× floor) / 2.4×10⁹ (stock) at
  the row price.** The naive store at 10⁹: 7×10⁷-1.2×10⁸ repairs/frame — dead at any price.

## Predictions

`predictions.md` was written before the arms; P1-P6 all held as written (P2's KILL did not fire:
warp-root last-quarter 0.0000 % against the 0.1 % kill bar; P3's residual p99 4.8×10⁻⁷ ≤ 1e-5,
never-repair 2.7×10⁻⁴ ≤ 2e-3; P5's rebin 27-81 ns ≤ 150; P6 β 0.644 ≥ 0.4, alive). One honest
half-miss: P4's second clause (the 1e4 near-set growth *inside* the annulus) was not reached — the
420-s wall truncated arm A2 at β 0.52, r 788 ls, near 15 and rising; the ∝K law is supported by
the approach (15 at 1e4 vs 1-2 at 1e3) but the in-annulus 1e4 point is unmeasured and stays open.

## What would make it wrong

- The steady-state repair rate at stock (≈1.4×10⁻⁶/frame) is an estimate scaled from the measured
  10×-floor rate by 1/θ, not itself measured (no stock-floor crossing occurred in 2500 game-s); a
  multi-hour flight could concentrate crossings (a dense formation at one bearing — taleb-09b5's
  ruin class — where per-row drifts correlate and cross together).
- The record's aggregate half (Σlum, colour per cell) rides the same θ law but was not simulated;
  so was the shift/patina serve under warp (9292 measured the raw |d ln shift| p99 = dβ,
  shared-side; the warp-residual shift drift is second-order but unmeasured).
- The hot-set trigger (kicked bodies re-entering the resolvable tier) remains unflown; a kick wave
  through the far belt would add an insert class this census never sees.
- At 10⁹ bodies with sustained 10× zoom the row-priced repair tier exceeds the frame budget
  (K\* ≈ 2.4×10⁸): the due-event/running-sums form is load-bearing there, not an optimization.
- All cloud timings are Linux/x86 shared-box: orders of magnitude only; the integrator re-measures
  on the M1 (the 27-81 ns/row re-bin and the ~100 ns/cell remap are the constants that matter).

## Cost of adoption

None as code (print-only probe; the tree is restored). The design consequence: 2df1/e6c9's record
is licensed on the burn axis at all flight lengths and zooms flown — store far rows' root offsets
(not angles), compose the shared displacement and aberration warps per frame at O(cells), repair on
the emitter-drift law (≈ never at stock floor), re-bin cold once per zoom event. Fit with
PRINCIPLES: "Nothing is evolved that can be derived when looked at (clocks, redshift, views)" (3) —
the parallax and aberration of every far row are derivable from one shared vector pair per frame;
"the best part is no part" (17) — the K-walk and the naive tier are the parts deleted.

## The lens

The SpaceX eye flew the failure boundary first (the checker's two arms) and then attacked the
record where it was designed but unmeasured — the displacement warp — with the record's own
accounting, not a proxy. Its blind spot is the same one-way-door underweighting 9292 named: this
census says the *angles* serve exactly under warp, but the patina (shift/colour aggregates), the
formation ruin class and the hot-set seam are unflown, and a stale aggregate is a player-visible
wrong sky, not a lost test.
