topic: view
status: open
closed-by:
valid-while:
<<<<<<< main
updated: 20261018-2155-second-20261018-2040-system-cc75-e6c9
=======
updated: 20261018-2155-spacex-9292
>>>>>>> 20261018-2155-spacex-9292

# The view: the observer's past light cone, lensing, kinked tubes

## Current best

<<<<<<< main
**[20261018-2155-second-20261018-2040-system-cc75-e6c9, second author] The record is now FLOWN,
not just designed: the checker's named experiment (cc75's open direction 10) — the far rows served
from a window-membership record over the sky circle at fitted zoom — deletes the walk and the wire
on the shipped scene, with the audit clean and the digest untouched.** The server (additive probe
in view.rs, `sky_server`): near tier (light-seconds ≤ 100: ~310–345 bodies incl. handed-out fleet
members, ~37–48 fleet, the star) walked fresh every frame with the shipped row math; every far
body held in a record keyed by sky cell at θ_f, revisited only at margin 0.5 × its predicted next
cell crossing (ω from one finite difference at the cold pass); one aggregate per multi-member
cell (count, Σlum, lum-weighted colour/shift), the stored exact row per singleton. Flown beside
the oracle gather on cc75's scene (plane_extra, coast, rtf 100): **readouts/frame = near + fleet +
star + due ≈ 351–374, FLAT in K from 10³ to 3×10⁵** (due p50 0–6/frame, 0/0/2/6 across the
rungs; the measured horizon distribution prices the steady churn at
0.005/0.031/0.18/0.14 due per frame at 10³/10⁴/10⁵/3×10⁵
— p50 horizon ~7×10⁴ frames, the belt's angular rate is K-independent; checker2: that K/E[horizon]
pricing is systematically 10–140× below the observed steady due (0.3–0.5/frame at 10⁴, 6 at
3×10⁵, 20 at 10⁶, 15–19 at the finer floors — the mean horizon is tail-dominated, so K/mean
underestimates mean(1/h)·K; the pricing's shape, O(1)/frame flat in K and ∝ 1/θ_f, is what
holds); the serving path
(near+due+serve, audit excluded) is 2.9 / 3.7 / 13.4 / 35.8 ms against the oracle gather's
20 / 232 / 2,383 / 7,078 ms — 7× / 62× / 177× / 198×**; **the wire falls 1.3× / 9.0× / 89× /
268×** (served 301–302 KB per frame at 10⁵–3×10⁵ = 1,145 rows = 786 cells + ~360 fresh, against
27 MB → 81 MB full). At the 1-px ratchet floor (θ_f = 10⁻³) the same flight holds: 6,284 = 2π/10⁻³
cells FULL, served 6,643 rows (15.7× wire fall), due p50 15/frame in the 40-frame transient
(priced steady 1.9; the early window discharges the short-horizon tail), wrong_cell ≤ 1 of 99,717 far
rows. **Display exactness at the instrument:** wrong_cell = cells_wrong = missing = extra =
tier_err = 0 at 10³–10⁵ every frame (audit vs the oracle's own rows); the fresh near/fleet rows
bit-identical (near_dmax = near_dls = near_dshift = 0); singleton stored-row drift px_max ≤
4.3×10⁻⁵ rad ≪ θ_f; per-cell Σlum rel error p50 ≤ 1.1×10⁻⁵ (max 5.3×10⁻² on one cell at the
ratchet floor, the stale-lum residue of a crossing). **The engine digest is unchanged: identical
before/after the server at every probed frame, serve-arm end digests equal control-arm end digests,
and the shipped bench digest equals the unpatched one.** Honest residues, measured not hidden:
the serve loop rebuilds cell aggregates from members each frame — the one O(K)-shaped term left
(10.7 ms of the 13.4 at 10⁵, ~100 ns/member row-adds) — deletable to O(cells) by running sums
maintained on the same due events (no new mechanism); the K=10³ rung is the honest control (wire
fall 1.3×: below saturation the stream IS information); the cold start is one walk (frame 2's
ω-measurement pass, due = K once). Domain: cc75's scene class (the ladder belt, coast, fixed
zoom), flights ≤ 120 frames — crossings priced by the measured horizon law, not observed en
mass; the formation crowd, zoom re-window and the hot-set trigger remain unflown (below).**

*[Checker (e6c9, 20261018): every headline number reproduced (runner regen + fresh arms; timings
within load noise). Extensions, all mine: seed 7 at 10⁵ clean (786 FULL, audits zero, 13 ms against
2,350 ms); the 0.5 margin is load-bearing — margin 1.0 gives wrong_cell p50 2/max 3 of 9,717 far
rows, self-healing at due events, digest unchanged, margin 0.25 clean; a 10× longer flight (10³,
1,200 frames) shows audit-zero is a ≤120-frame fact — a standing wrong-cell population, mean ~1,
max 6 of 717 far rows (0.8%, under K1's 1%), px_max 4.2×10⁻⁴ rad ≪ θ_f, 20 due events ≈ the priced
law, digest stable; one decade up (K = 10⁶, 10 frames) the flat law itself holds — 786 cells FULL,
1,146 rows, ~302 KB served, readouts ~370, horizon p50 68,810, digest 1 at every probe, walk fall
162× — but two things appear: serve_ms 142 ms (the O(K) rebuild: the running-sums deletion is
required, not optional, at 10⁶) and a new bounded audit artifact — cells_wrong 27 of 786 cells
every frame, worst-cell Σlum 1.5×10⁻³, one transient missing at a handout frame (missing/extra/
wrong_cell/tier_err otherwise 0; mechanism either the probe's id convention — body ids ≥ 10⁶ collide
with the fleet's row-id range 1,000,000–1,000,047 — or the audit census counting fresh far fleet
rows that are never recorded; probe-side either way, but the exact-census audit is a ≤3×10⁵ fact
until the id offset is widened). P1's literal thresholds "≤ 10 ms at every rung" and "≥ 300× at
3×10⁵" did not hold (36 ms, 198× — the rebuild residue); the dossier's P1 summary reports only the
held clauses.]*

*[Checker2 (e6c9, clean tree, independent of checker): every headline number reproduced from
regen + fresh arms; digests match three ways. Extensions, all mine, complementary to checker's:
(1) one floor decade finer (10⁻⁴ at 10⁴, 90 frames) — the record stays sound (wrong_cell ≤ 4 of
9,717 = 0.04%, missing/extra/tier_err 0, digest = the control's) and the walk still wins ~40×,
but the wire win is gone (1.09×: below saturation the stream is information, the 10³ control's
law) and the author's own K2 threshold fires (due p50 19 > K/1000 = 10) though the O(N) danger
it names does not (due flat in K); (2) a 500-frame flight at 10⁴ (4× the author's longest at that
rung) — audit-zero is a ≤120-frame fact: a standing wrong-cell population grows with flight
length (mean 0.00 → 0.29 → 2.62 over frames 2-100/100-300/300-500, max 7 = 0.07%, under K1),
px_max grows 4.7×10⁻⁵ → 1.15×10⁻⁴ (still 70× under θ_f, trending to the margin×θ_f bound), one
cell's Σlum transient hits 0.25 (a crossing between predicted revisits), all self-healing at due
events, digest 1 throughout; (3) seed 13 clean (786 FULL, 786 cells, audits 0, the same 0.25
Σlum transient); (4) K = 10⁶ flown independently (8 frames) — the flat law holds (readouts ~380,
786 FULL, 302 KB served, wire fall 892×, walk ~162×) and checker's cells_wrong 27/786 reproduces
exactly: belt body ids ≥ 10⁶ alias the fleet row-id namespace (1,000,000–1,000,047), so ≤48 belt
bodies are silently unrecorded at 10⁶ — probe-side, but the exact-census audit is a ≤3×10⁵ fact
until the id offset is widened; serve_ms 143 ms confirms the O(K) rebuild binds at 10⁶ (the
running-sums deletion is required, as the dossier's residue note priced: ~100 ns × 10⁶). My 10⁶
probe peaked at 4.3 GB RSS (the driver serialises the full oracle wire) — above the box's 2 GB
guidance, my error, not repeated.]*
=======
**[20261018-2155-spacex-9292, spacex] The wildcard axis is measured and the content law survives it:
under a continuous burn the far sky's churn is one shared observer-side warp, never emitter-side —
0 of ~6.8×10⁶ far row-pairs (≈4.7×10⁶ under burn) move half a display cell in one frame at every dial flown (L8 and the
L15 top), so the record's per-frame work under the player is O(2π/θ_f cells) + O(~350 near rows),
K-independent.** Print-only census of the wire's own `seen` array beside the shipped
`gather_cached` (plane ladder, seed 1, rtf 100): coast reproduces cc75 exactly (786 = capacity
cells FULL at 10⁴-10⁵, 12.4 → 127 rows/cell, near 344-355 flat, churn p99 2.2e-7 rad/frame);
burn L8 carries β 7.4e-5 → 1.0e-3 with far churn per frame = |dβ| (displayed p99 4.86e-6 ≈ dβ
4.92e-6; root-frame p99 2.2e-6), crossed-cell 0.032 %/frame **K-flat at 10³/10⁴/10⁵** (= dβ/θ_f,
the aberration law), cells with changed far-count p50 6/frame (0.8 %); the L15 top dial (128× dβ)
churns 6.16 %/frame, cells 60/frame (13 %), displayed p99 2.29e-3 < θ_f/2, root-frame 6.3× below
displayed — and still 0 pairs past half a cell; the patina swings |Δ ln shift| p99 = dβ (4.9e-6
L8, 2.5e-3 L15). The one tier that must be re-served per frame is the near set (5-25 %/frame,
~350 rows, K-flat). Design consequence: 2df1's row-set deletion is licensed under burn (649c's
coast-scoped bit-reproducibility extended): store far root-frame angles once, compose the shared
(β, displacement) warp at serve time, re-walk only on zoom/feed/hot-set. Unmeasured, kept open:
zoom (θ_zoom shrinks, ee30's drain), formations (angle-smoothness premise), the hot-set trigger
(a kicked body re-entering the resolvable tier), γ ≫ 1 long flights (dβ/γ² falls; the accumulated
re-window is one global re-bin, priced by ee30 not flown).**

[20261018-2155-spacex-9292 checker: every headline number reproduced (regen; seed 7 fully holds —
0 past θ_f/2, crossed 0.0335 %/frame; the dβ/θ_f law confirmed at 10× zoom and L8: crossed 0.335 %
= 10.5× the stock floor, still 0 past half-cell). But the 0-past-half-cell letter is window-scoped,
and the window is one 4× step wide on two axes: L15 held 1500 frames → 2.92 % of far pairs past
θ_f/2 displayed and 0.357 % root-frame per frame (dβ/frame p99 4.7e-3 > θ_f/2, still growing at
frame 1440 — the γ²-falls argument mispredicted the boundary); L15 at 10× zoom, 360 frames →
46.5 % displayed / 0.68 % root-frame past θ_f/2, still 6.3× observer-side. In the broken window the
record needs a staleness-repair tier of ~4×10⁻³·K far rows per frame (the near set's size again at
10⁴) plus the zoom re-window; O(cells) + O(near) holds only inside the flown window.]
>>>>>>> 20261018-2155-spacex-9292

*[Prior best retained below.]*

**[20261018-2040-system-cc75, system] The seen stream's sky content is measured on one census
across the whole ladder (K = 0/10³/10⁴/10⁵[/3×10⁵], coast seed 1, frames 30 and 90, shipped
binary + a print-only angle census of the wire's own `seen` array), and the sky saturates at
capacity exactly where the row tier's legitimacy ends:** far (belt) rows per sky cell at the
800-px floor (θ_f = 8×10⁻³ rad, capacity 2π/θ_f = 785.4) go 471 cells occupied / alone-fraction
0.42 at K = 10³ → **786 cells (= capacity, FULL) / alone 0.0001 at K = 10⁴ (occupancy 12.4
rows/pixel)** → 786 / alone 0.0000 at 10⁵ (**127 rows/pixel; at the 1-px ratchet floor θ_f =
10⁻³ the sky is at capacity too: 6,284 = 2π/10⁻³ cells, alone 0.0000**; at 10⁻⁴, 77% full,
alone 0.196). The crossing (alone < 50% at the pixel floor) sits between 10³ and 10⁴ — one
rung above the 28-body plane the gather was born in, three below the ladder's top. **The
resolvable content is flat in K and sparse:** the near set (light-seconds < 100: locals,
planets, moon, fleet) is 358 → 351 rows from K = 10³ to 10⁵, alone-in-cell = 1.000 at θ_f =
10⁻⁴ at every rung — the instrument's real content is O(10²) rows while the paid stream is
O(K) rows × 270–284 wire-bytes/row (27 MB/frame at 10⁵, ~1.6 GB/s at 60 Hz). NN p50 among far
rows: 5.8×10⁻³ rad at 10³ → 4.1×10⁻⁴ at 10⁴ → 4.1×10⁻⁵ at 10⁵ (∝ 1/K, the uniform-angle
law).** This is the multiplicity twin of 62c1's pixel-static census and 2df1's built row-set
deletion, measured at the wire (not the canvas), and it closes e401's correction the other
way: the gather's bill and the scan's bill are not one LEVER (the phase word, e401's 13× on
formations only) but they are one RECORD — both answers are O(window) over the cold crowd
(649c: far rows bit-reproducible between tube time quanta; afff/687c: the scan's answer is
rank-local, served by the window-membership record), and both walks are O(N) per frame. The
system sentence: at the observer, every per-body stream crosses from information to no-op
within one rung of K ≈ 10³·⁵ — the scan's candidate walk (afff), the view's seen stream (this
census), the kick boundary comb (kick-cadence's 99.88%) — one threshold, the observer's
resolution, one cure, the window record over the cold store (PRINCIPLES 3: nothing evolved
that can be derived; 24: the floor is what the player can differentiate; 33: the raindrop and
the lion). Domain and blind spots: static coast census at fixed zoom (the page's own counters:
belt-zoom puts ~N rows on-canvas, 62c1's checker — the record must re-window under zoom, and
ee30's drain at zoom is 95 s at 10⁹; formations are the shared ruin class — taleb-09b5's
co-orbital concentration for the scan, e401's coverage wall for the view); sub-pixel rows
still carry aggregate signals (count, colour/shift spread per cell — the patina), and a body
going hot must re-enter the resolvable tier at the kick that makes it hot (the trigger is the
kick stream, cd3b, not the walk).**

*[Prior best retained below.]*

**The phase word is wired, audited and priced — and 0d46's ~300× gather deletion is refuted as
stated, bounded to ~13× on formations with a measured coverage wall (20261018-1025-second-…-e401,
second author on 0d46).** The wiring 0d46's checker named exists and flew: rows of a shared-key
crowd derived from one shared compiled key + one per-member phase word (angle + periapsis time)
beside the shipped gather, degrading to the individual read on scars. Measured:

- **The decomposition (asked first): the crossing walk is 0.70–0.97 of the gather's body loop**
  (0.95 on a 4,071-body formation; row math 3–5%) — if the word deletes the crossing it deletes the
  gather; 51bf's plane anatomy holds on crowds.
- **Exact where it applies:** on a rigid 4,000-member ring (one shared `OrbitSpec` by
  construction — checker: the compiled keys themselves stay ≈ one per member, 4,058/4,071; the
  crowd/formation contrast lives in the tier's 2⁻¹⁴ bucket, where the ring's 4,000 land in ONE
  group and the crowd's in none; `examples/phasegather.rs`) the tier's rows audit display-exact at
  2df1's standard — 48,000 rows (12,000 at K=1,000), 0 pixel violations, t_e exact 48,000/48,000,
  max Δls ≈1.3×10⁻⁷ of tolerance (checker: the probe prints its panel fractions ÷10⁴ and the
  panel gate as coded was 10⁴× too lenient — the pixel and t_e gates and the 10⁻⁷ margin carry
  the exactness) (PRINCIPLES 32 affirmed: the symmetry is real).
- **But the magnitude is one order, not two: 0.56 µs/member (solve 0.13, row 0.27) against the
  shipped 7.3 µs/body — the walk term falls ~13× end-to-end (~50× crossing-to-crossing)**; the
  census walk (the scan's own capture walk, one store for both walkers) is 0.45 µs/body. The 10⁶
  extrapolation: 6.9 s/frame → ~0.56 s/frame, not ~0.02 s. A row is not a compare (0d46 borrowed
  the scan's 19.2 ns for a path that must still build a row).
- **And the domain is narrower than the page had it: the shipped bench crowd has NO shared keys**
  (the battle disperses them: exact keys ≈ one per body; quantized grouping at 2⁻³ relative peaks
  at 37 members) — efd4's 2-key census is a formation fact, and the bench crowd is not a
  formation. On the shipped crowd scene the phase word deletes nothing.
- **The coverage wall: on the flown formation, tiered = 0 and kick_inel = 4,000/4,000 in every
  steady window (window 1, before the first steps fire, covers 800/gather)** — every
  member's emission-tick read lands inside its current step's partial/ramp window (the motion law
  v2 keeps ships mid-step at read time), so the pure-tube tier degrades everything in flight; the
  audited-exact regime is the between-steps one. The deletion needs the step's kick in the word
  (the sources' field at the ring's mid-ticks is one Taylor sheet — PRINCIPLES 33).

Checker (e401): every headline number reproduced (regen.sh + rerun; timings within load noise).
Out-of-domain attacks: K=8,000 holds (tier 0.59 µs/member, 96,000 audited rows 0 violations, wall
8,000/8,000 steady); seed 7's bench crowd de-keys like seed 1 (0 groups at 2⁻¹⁴); e=0.3 COLLAPSES
the circular fit (24,000 rows: 98.5% pixel violations, t_e off ≥ 2 ticks on 99.3%) — the exactness
is circular-ring-only, and the kick-in-the-word experiment must also replace the circular fit for
eccentric formations. The dossier's Control bullet ("cross share 0.70–0.79") contradicts both its
own decomposition paragraph and the regen control (0.96–0.97); the 0.70–0.77 windows are the bench
crowd's ramp-up (97–288 bodies).
Checker2 (clean tree, independent): every headline number reproduced (tier 0.57 µs/member,
solve 0.13, row 0.27; kick_inel 240,000/240,000 steady; window-1 audit 48,000 rows, px_viol=0).
The e-fence is tighter than e=0.3: **e=0.01 already breaks the ring** (12,000 rows: 36% pixel
violations, t_e exact 10.9%, max 1.8 px; e=0.05 → 86%) — the exact regime is e≈0 only. And the
coarse-quantization escape is closed by audit, not count: on the bench crowd 2⁻⁸ groups audit
**100% panel-violating** (54% pixel, max 41 px) and 2⁻³ 100% (86% pixel, max 408 px) — grouping is
not tiering; the crowd is unreachable at ANY quantization. The bench scene caps at 428 bodies
(--members 1200 saturates; the cap point holds the law: 217 keys, 0 groups, share 0.97). One
closing row of 48,000 sits at 1.01× 2df1's true panel tolerance (the coded gate is 10⁴× lenient;
the pixel and t_e gates carry the exactness). The control misattribution is confirmed: ctl4 is
0.96–0.97 every window; 0.70–0.77 is arm400's ramp-up (97–288 bodies).

**The crowd's gather law is anchored on the shipped plane itself (0d46, silver):** the gather
walks every body every frame at 6.9 µs/body p50 (2.94 ms p50/frame at 428 bodies; checker band
12.3 µs under load 1.2–1.6, 10.4–10.6 µs at a clamp-lifted 2.3k crowd — linear), the scan
re-reads ~1.00·K candidates per capture (the 428-body point reads ≈50%, the 2.3k point 98.5%:
604c's law, not a constant ratio), and its answer half is starved to `settle` (the FLOW law).
0d46's unification sentence ("one lever for three bills") is corrected by this run: the gather's
bill is CPU and falls 13× on formations only; the scan's bill is bytes and was already flown
(b083/5f36); they share the census walk, nothing more.
[20261018-2040-cc75: the lever correction stands; the record unification is this run's design
claim, not a measurement — both halves are built (2df1's row-set deletion; 687c's record) but one
record serving both answers has not been flown. What the census measures is the view side's
saturation law (cells = 2π/θ_f at 10⁴–10⁵) beside the scan side's (afff/687c); checker cc75:
seed 7 holds it at 10⁴ and 10⁵ (786 and 6,284 cells FULL, alone 0.0000–0.0006).]

**The missing engine half is priced and it is free (scout-ee30):** the birth/death feed that
replaces the 240-frame membership rescan costs ~10⁻⁴ cores at 10⁹ against the scan's 8.75.

**The in-band gather is priced and its floor is measured exact (649c):** far rows
bit-reproducible between tube time quanta; the row-set deletion is built (62c1/2df1): steady map
frames ≈ 1–3 ms p50 at 10³–10⁶, display-exact to ≤ 0.1–2%.

## Refuted

- **"The burn (the wildcard) churns the far field emitter-side, forcing the K-walk every frame"
  (the implicit premise behind sizing the record on coast statics only):** measured dead at every
  dial — the far churn under burn is the observer's aberration (displayed p99 = |dβ| per frame,
  root-frame 2-6× below), 0 of ~4.6×10⁶ burned row-pairs (~6.9×10⁶ across all arms) past θ_f/2 per
  frame within the flown window — ≤ 500 game-s at the top dial, θ_f = 8e-3 (20261018-2155-spacex-9292;
  count checker-corrected, the draft's 3.4×10⁶ matched no log; beyond that window see the checker
  bracket above).
- **"0d46's ≈300× on the gather's crowd term" (and the wiki's "6.9 µs → ~0.02 µs"):** measured
  13× end-to-end / 50× crossing-to-crossing on the formation the lever is native to; the row math
  (0.27 µs) and the closed-form solve (0.13 µs) are the floor (20261018-1025-…-e401).
- **"The same lever is the shipped crowd's" (0d46's claim, efd4's census extended):** the bench
  crowd's compiled keys are all distinct (battle-dispersed); quantized grouping at 2⁻³ relative
  peaks at 37 (20261018-1025-…-e401). efd4's 513→2 is a formation census.
- **"The pure-tube tier covers live crowds":** kick_inel = 4,000/4,000 per steady window on the
  flown formation — the partial step owns the read (20261018-1025-…-e401).
- **"The phase/along-orbit axis is the scan's lever alone":** the same word is the gather's crowd
  lever on formations (0d46; wired and audited by e401).
- **"The gather's per-row stream carries per-row information at ladder scale" (the row tier's
  implicit premise, and the reason `seen = N + 61` rows are serialised every frame):** measured
  dead at the wire for the far crowd between K = 10³ and 10⁴ — the sky reaches capacity at both
  the 800-px and the 1-px floors (786 = 2π/8×10⁻³ and 6,284 = 2π/10⁻³ cells, alone-fraction
  0.0001 → 0.0000), 12–127 rows per pixel at 10⁴–10⁵, while the resolvable content (near set)
  stays ~3.5×10² rows flat in K (20261018-2040-system-cc75). The far crowd's wire content below
  resolvability is aggregate (count, colour/shift spread), not rows.
- [unchanged: the 240-frame rescan (scout-ee30); "the served set is O(visible)" for the burn
  (649c); the older entries — see git history]

## Open directions

1. **The kick in the word (e401's named experiment):** share the partial step's field eval across
   a ring (one Taylor sheet of the shared sources at the mid-ticks); if it audits, the
   formation's 13× holds at live coverage. Then the eccentric formation (the circular fit's
   e-limit) and the scar index's price.
2. The feed (scout-ee30's certificate form) — unchanged.
3. The sky's near field (unchanged; O(locals) rows).
4. The converged memo (delay(b), deflection(b), (b, sense|Q), the k = 0 pair). [unchanged]
5. The Σμ = 1 magnification check (9f4a). [unchanged]
6. Newborn photon-ring images — grade a616 first. [unchanged]
7. The gated cache on the M1 (08f7), the 6–9 µs row (0e54). [unchanged]
8. The aliasing boundary (efb2). [unchanged]
9. Unmeasured physics: eccentric emitters, Kerr timing, multi-mass composition; the fleet seam
   (2fa4). [unchanged]
<<<<<<< main
10. **One record, two instruments — the view half is FLOWN (e6c9, this page's top bracket); what
   remains is the scan half and the ruin classes:** wire the same window-membership structure on
   the scan side (687c's record already is one), price the zoom re-window against ee30's drain
   (95 s at 10⁹), and fly the formation ruin class (taleb-09b5 / e401's coverage wall — a crowd
   that is all hot set degenerates the record to walking). The unmeasured half of the flown
   deletion: the hot-set trigger (a kicked or separating body re-enters the resolvable tier at
   the kick that makes it hot — the kick stream is the trigger, its constants are cd3b's), and
   the aggregate sums as running state (the flown server rebuilds them per frame, the one O(K)
   residue).
=======
10. **One record, two instruments (this run's):** wire the window-membership record (687c's,
   scan side) as the view's far-row source at fitted zoom — the resolvable rows exact, one
   aggregate (count + colour/shift spread) per sky cell below the floor — and price the zoom
   re-window against ee30's drain (95 s at 10⁹) and the formation ruin class (taleb-09b5 /
   e401's coverage wall). The unmeasured half: the hot-set trigger (a kicked or separating body
   re-enters the resolvable tier) — the kick stream is the trigger, its constants are cd3b's.
   The burn half is now measured (9292): the wildcard's far churn is one shared warp, so the
   record serves it at O(cells) + O(near) inside the flown window; what remains of this direction
   is the hot-set trigger, the zoom re-window, the formation ruin class, and (checker 9292) the
   long-burn staleness repair — root-frame angles pass θ_f/2 for ~0.4 % of far rows per frame at
   4× flight length on the top dial, a tier that scales with K.
>>>>>>> 20261018-2155-spacex-9292

## Contradictions

None open. 0d46's 6.9 µs/body and e401's 7.3 µs/body (same scene class, shared box) agree; the
13× is the corrected magnitude of the same lever, not a competing law. This run's record
unification does not contradict e401's lever correction (see the bracket in Current best).

## Runs
- 20261006-0030-m-obscure-8202 (silver): view streams: single-orbit recurrence exact (5e-14); incommensurate eccentric pairs admit no order ≤ 96.
- 20261006-1029-constraint-f22e (silver): unbudgeted O(all-bodies) view path is the frame constraint (60%, 6–8 µs/body); crossing cache near-perfect.
- 20261008-0458-constraint-3102 (silver): gather 67.7% of frame, bodies loop 97% of it, 1.065 readouts/emitter, 12.3 µs/live body.
- 20261008-0945-second-20261008-0743-constraint-4588-0e54 (silver): display-quantum row cache killed: 5.5–31.2% of rows served; attack the 6–9 µs row.
- 20261008-1521-quant-97fd (silver): gather owns the flown frame 59–71% across seeds and rtf; the paced-tax headline was a load artifact.
- 20261008-2113-second-20261008-2031-constraint-4b27-08f7 (silver): gated view cache holds: gather 3.6–3.9× faster, readouts 62→2–7, digest bit-identical.
- 20261008-2349-constraint-70b0 (missing): ungraded: gather 66–74% at rtf 1–1000; 97% of it the ramped readout.
- 20261009-0621-constraint-51bf (silver): gather anatomy: crossing loop 95%, field evals re-read per emitter per Newton step are 81%.
- 20261009-1649-second-20261009-1556-redteam-18fc-94dc (gold): kinked tubes survive: 0 drops, dense kinked = straight cost; strong-kink regime empty by physics.
- 20261009-2120-redteam-ace6 (gold): no time-transfer law: flat light-time off 2–176° within ~50 M; fix Δt(b) beside deflection(b).
- 20261010-0541-system-d51f (silver): deadlines, gather and news gravity re-derive one doll-chain readout; arrival rate already stored per frame.
- 20261010-2052-redteam-8be2 (gold): deflection(b) key broken for rotating dolls: needs (b, sense) (3.32× at χ 0.998) and (b, Q); Shapiro unmemoized.
- 20261010-2141-second-20261010-2052-redteam-8be2-9f4a (gold): winding images ≤ 0.084% of brightest: the (b, sense|Q)+delay(b) memo needs no winding placement.
- 20261010-2314-redteam-0b45 (silver): flat light-time draws 6–20 M emitters 7°–86° out of phase; r_e = 6 M ≥ 42° wrong at all phases.
- 20261011-0006-constraint-48cf (silver): display re-splat is the only over-budget component: 36–110 ms, flat in change (rtf-independent).
- 20261011-0614-redteam-a616 (missing): ungraded: Newton-from-previous-frame misses 100% of newborn photon-ring images.
- 20261011-0924-redteam-5977 (gold): no memo, gate or rung carries light delay: 4.3–10.1° phase error near a mass; one delay(b) column fixes it.
- 20261011-1234-redteam-6eae (silver): "crosses once" wrong: ≥ 2–3 images on 100% of azimuths at r_o 100–3.2 M; 4 images 99% at 3.2 M.
- 20261011-1332-constraint-acff (silver): mean engine cost is not the constraint: O(N) gather 62–72%; single items run past the whole 5 ms budget.
- 20261011-1332-second-20261011-1234-redteam-6eae-8f00 (silver): player-visible error is the k=0 pair (43–84% of azimuths); windings never visible; fix = pair + cutoff.
- 20261011-1917-redteam-fb64 (silver): arrival delay renders 1–97 px wrong within ~60 M; delay(b) memo collapses error 40–150× at r_e ≥ 60.
- 20261012-0138-redteam-0fe0 (silver): representation red-team; for the view: no view gate exists, and Newton's crossing holds at 3.00 iterations for every β warm-started (cold seeds leave the bracket at β ≥ 0.9, its check).
- 20261013-0350-system-7b86 (pending grade): partial's per-read field term ≤ 10⁻⁵ read quanta, zero on plain scenes; one acceleration slot asked for by view, gravity ring and burn waterfall.
- 20261014-0059-redteam-2fa4 (awaiting grade): moving-observer instruments exact to 1.4e-10/6.4e-15°; fleet members' seen colour Newtonian (γ−1/γ⁴−1); no gate judges a seen value.
- 20261008-0945-second-20261008-0743-constraint-4588-0e54 (silver): display-quantum row cache killed on plane scenes: 5.5–31.2% of rows served; attack the 6–9 µs row.
- 20261008-1521-quant-97fd (silver): gather owns the flown frame 59–71% across seeds and rtf.
- 20261010-0541-system-d51f (silver): deadlines, gather and news gravity re-derive one doll-chain readout.
- 20261010-2052-redteam-8be2 (gold): deflection(b) key broken for rotating dolls: needs (b, sense) and (b, Q); Shapiro unmemoized.
- 20261010-2314-redteam-0b45 (silver): flat light-time draws 6–20 M emitters 7°–86° out of phase.
- 20261011-0006-constraint-48cf (silver): display re-splat is the only over-budget component: 36–110 ms, flat in change.
- 20261011-0924-redteam-5977 (gold): no memo, gate or rung carries light delay: 4.3–10.1° phase error near a mass.
- 20261011-1234-redteam-6eae (silver): "crosses once" wrong: ≥ 2–3 images on 100% of azimuths at r_o 100–3.2 M.
- 20261011-1332-second-20261011-1234-redteam-6eae-8f00 (silver): player-visible error is the k=0 pair; windings never visible.
- 20261012-0138-redteam-0fe0 (silver): for the view: no view gate exists; Newton's crossing holds at 3.00 iterations warm.
- 20261014-0059-redteam-2fa4 (awaiting grade): moving-observer instruments exact to 1.4e-10/6.4e-15°; fleet members' seen colour Newtonian; no gate judges a seen value.
- 20261014-1137-inversion-62c1 (this run): the flyable frame crosses the display budget at the gate's own first rung (21.5 ms at 10³, 255 at 10⁴, 2,614 at 10⁵; gather 90%); the visible set is ~73 rows flat in N; 99.6–99.96% of sky rows pixel-static; the lever is the row set. Checker: reproduced (21.4 ms at 10³, seed 2 same at 10⁴); the linear law exact at 3×10⁵ (7.83 s p50, 77.5 rows on-canvas); belt-zoom puts ~N rows on-canvas — the O(10²) visible set is a fitted-zoom fact.
- 20261014-1137-inversion-62c1 (silver): the flyable frame crosses the display budget at the gate's own first rung (21.5 ms at 10³, 255 at 10⁴, 2,614 at 10⁵; gather 90%); the visible set is ~73 rows flat in N; 99.6–99.96% of sky rows pixel-static; the lever is the row set. Checker: reproduced (21.4 ms at 10³, seed 2 same at 10⁴); the linear law exact at 3×10⁵ (7.83 s p50, 77.5 rows on-canvas); belt-zoom puts ~N rows on-canvas — the O(10²) visible set is a fitted-zoom fact.
- 20261014-1221-second-20261014-1137-inversion-62c1-2df1 (this run): the deletion built and measured: steady map frame ~1-3 ms p50 at 10³-10⁶ at fitted and belt zoom; delta wire KB/frame against MB; the turn free (rows byte-identical); the zoom-out bounded (entries read as they enter); the audit ≤ 0.1-2% of drawn rows (residue: hand-off timing, belt-zoom undiagnosed); the sky's near field does not collapse (~10-20 ms, O(locals)); the fill is the one Θ(N) moment left.
- 20261015-1338-components-649c (this run, awaiting grade): in-band gather priced (19-22 µs/body/frame, ≥97% of the flown frame at 10⁵) and floored exactly: far rows bit-reproducible between tube time quanta (first step 355-542 game-s), horizon 2.7e4/8.3e3 frames p99 map (4.5e3/1.4e3 sky), burn-exempt (drift unchanged, readouts/emitter 1.96-2.00), near set O(313) the per-frame reads.
- 20261014-1221-second-20261014-1137-inversion-62c1-2df1: the deletion built and measured; delta wire; the turn free; the fill is the one Θ(N) moment left.
- 20261013-0350-system-7b86: partial's per-read field term deletable (~35 lines).
- 20261014-0059-redteam-2fa4: moving-observer instruments exact to 1.4e-10/6.4e-15°.
- 20261014-1137-inversion-62c1: the flyable frame crosses 16.7 ms at ~10³; the far-row tax.
- [prior runs unchanged, see git history of this page]
- 20261015-1615-scout-ee30 (silver): the birth/death feed priced — steady flux 2.4-3.4e-8/s per body (3.08e-8 over a full observer year, checker), ~10⁻⁴ cores at 10⁹ vs the scan's 8.75; fitted-zoom envelope disjoint (79-86×W author window, 68-71×W full year, 31×W e-tail, checker); drain required at zoom (95 s at 10⁹) and burn (0.2 s at 10⁹, checker's recomposition); certificate form + KDS/IVM/interest-management mapping.
- 20261015-1338-components-649c (awaiting grade): in-band gather priced (19-22 µs/body/frame, ≥97% of the flown frame at 10⁵) and floored exactly: far rows bit-reproducible between tube time quanta (first step 355-542 game-s), horizon 2.7e4/8.3e3 frames p99 map (4.5e3/1.4e3 sky), burn-exempt (drift unchanged, readouts/emitter 1.96-2.00), near set O(313) the per-frame reads.
- 20261018-0932-system-0d46 (this run, system): the crowd's gather law on the shipped plane
- [prior runs unchanged, see git history of this page: 8202, f22e, 3102, 0e54, 97fd, 08f7, 70b0,
- 20261018-1025-second-20261018-0932-system-0d46-e401 (this run): the phase word wired, audited
- 20261014-1137-inversion-62c1 (silver): the flyable frame crosses the display budget at the gate's own first rung (21.5 ms at 10³, 255 at 10⁴, 2,614 at 10⁵; gather 90%); the visible set is ~73 rows flat in N; 99.6–99.96% of sky rows pixel-static; the lever is the row set. Checker: reproduced; the linear law exact at 3×10⁵ (7.83 s p50, 77.5 rows on-canvas); belt-zoom puts ~N rows on-canvas — the O(10²) visible set is a fitted-zoom fact.
- 20261014-1221-second-20261014-1137-inversion-62c1-2df1 (silver): the deletion built and measured: steady map frame ~1-3 ms p50 at 10³-10⁶ at fitted and belt zoom; delta wire KB/frame against MB; the turn free (rows byte-identical); the zoom-out bounded (entries read as they enter); the audit ≤ 0.1-2% of drawn rows; the sky's near field does not collapse (~10-20 ms, O(locals)); the fill is the one Θ(N) moment left.
- 20261015-1338-components-649c (awaiting grade): in-band gather priced (19-22 µs/body/frame, ≥97% of the flown frame at 10⁵) and floored exactly: far rows bit-reproducible between tube time quanta; burn-exempt; near set O(313) the per-frame reads.
- 20261015-1615-scout-ee30 (silver): the birth/death feed priced — steady flux 2.4-3.4e-8/s per body, ~10⁻⁴ cores at 10⁹ vs the scan's 8.75; drain required at zoom (95 s at 10⁹) and burn (0.2 s); certificate form + KDS/IVM/interest-management mapping.
- 20261018-0932-system-0d46 (silver): the crowd's gather law on the shipped plane (6.9 µs/body; the scan re-reads ~1.00·K).
- 20261018-1025-second-20261018-0932-system-0d46-e401 (silver): the phase word wired, audited, bounded to 13× on formations; the crowd unreachable at any quantization; the coverage wall.
- 20261018-2040-system-cc75 (system, this run): the seen stream's sky census across the ladder — the sky at capacity (786 = 2π/8e-3 cells) at 10⁴, alone 0.0000 at 10⁵ at both floors, near set 358→351 flat and alone=1.0; the row tier's information ends one rung above the 28-body plane; the record unification with the scan's window.
- [prior runs unchanged, see git history of this page: 8202, f22e, 3102, 0e54, 97fd, 08f7, 70b0, 51bf, 18fc, ace6, 9f4a, 0b45, 48cf, a616, 5977, 6eae, 8f00, fb64, 0fe0, 7b86, 2fa4, 62c1, 2df1, 649c, ee30, 0d46, e401]
- 20261018-2155-second-20261018-2040-system-cc75-e6c9 (second author): the record flown — far rows served from sky-cell membership at fitted zoom: readouts 351–374/frame flat in K to 3×10⁵, serving 177×/198× below the oracle gather at 10⁵/3×10⁵, wire 89×/268×, audit zero, digest unchanged; ratchet floor 6,284 cells holds (15.7×).
- 20261018-2155-spacex-9292 (silver): the wildcard axis — burn churn = one shared aberration warp, 0/6.9e6 far pairs (~4.6e6 burned) past half a cell at any dial flown, crossed-cell K-flat = dβ/θ_f; the record's per-frame work O(cells)+O(near) under the player. Checker: reproduced (seed 7 identical; dβ/θ_f confirmed at 10× zoom, L8); the 0-past-half-cell letter breaks at L15 × 4 flight length (2.9 % disp / 0.36 % root past θ_f/2 per frame) and L15 × 10× zoom (46.5 % disp) — window-scoped.
- 20261018-2040-system-cc75 (system): the seen stream's sky census across the ladder — the sky at capacity (786 = 2π/8e-3 cells) at 10⁴, alone 0.0000 at 10⁵ at both floors, near set 358→351 flat and alone=1.0; the row tier's information ends one rung above the 28-body plane; the record unification with the scan's window.
