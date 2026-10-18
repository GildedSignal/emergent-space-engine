# check2 — 20261018-2155-second-20261018-2040-system-cc75-e6c9

Grade: silver

**Abstract (for the integrator).** The named experiment is flown and holds: the view's far rows
served from sky-cell membership (near tier + fleet + star walked fresh; far bodies revisited at
predicted crossings; one aggregate per multi-member cell) read 351–374 rows/frame flat in K to
3×10⁵ — and at 10⁶ (my arm): ~380, 786 cells FULL, 302 KB served, wire fall 892×, walk 162×,
digest unchanged three ways. Adversarial: floor 10⁻⁴ stays sound but the wire win is gone (1.09×)
and the author's K2 fires; a 500-frame flight grows a standing wrong-cell population (max 0.07%
≪ K1) and a 0.25 per-cell Σlum transient; 10⁶ reproduces cells_wrong 27/786 (probe id-aliasing).
Silver because P1's literal clauses (≤ 10 ms every rung; ≥ 300× at 3×10⁵) failed while the dossier
reports "P1 held", and the horizon pricing is 10–140× below observed. Gold: one flown step (below).

## Reasons

**Reproduction.** Clean tree; `git apply work/patch.diff` + `cargo build --release -p xtask`
clean (one no-op `drop(&mut)` warning at view.rs:864 — harmless). The runner's regen exited 0;
every dossier number regenerates from `metrics.json` within load noise (oracle p50 2,349.64 vs
2,383 ms at 10⁵; serving 2.65+0.06+10.66 = 13.4 ms → fall 175.8× vs 177×; wire 89.4×; at 3×10⁵:
7,039.64 ms, 35.98 ms, 195.6×, 268.1×; serve1000 351/470/823/290→221 KB/19.33 ms — all match).
Digests: serve-vs-control end digests equal at all three rungs; per-frame digest=1 at every
probe; shipped bench digest equals cc75's unpatched `bench0.json` (`1b801358…`, matches_original
true). The patch is additive (view.rs append; new skyserv.rs; one dispatch arm) — no shipped line
touched, and `serve(&mut self, u: &Universe, …)` is read-only by type, the strongest form of the
claim. The fleet-handout completeness fix holds over 500 frames (tier_err = 0 throughout).

**Predictions.** predictions.md (22:12) precedes patch.diff (22:30) and all flight logs; the
author's own logs were overwritten by the runner's regen, so mtime order beyond that is
unverifiable — regen reproducibility covers it. P2/P3/P5/P6 held; P4 missed 4× and was disclosed.
P1 partially failed **as literally written**: "≤ 10 ms at every rung" (serving path 13.4 ms at
10⁵, 35.8 ms at 3×10⁵ — serve_ms 10.66/33.17 in the author's own metrics.json) and "≥ 300× at
3×10⁵" (198×). The dossier's summary says "P1 held" and reports only the held clauses — the same
record-quality defect the lab has graded silver before (r3 v3), independent of the physics, which
stands.

**Attacks (mine; commands in regen form: `$T universe --skyserv K frames seed floor serve margin`).**
1. **One decade up, K = 10⁶** (`1000000 8 1 8e-3 1 0.5`): the flat law holds — readouts ~380
   (near 311 + fleet 48 + star + due 20), 786 cells FULL, 1,146 rows, 301.9 KB served, oracle
   23.6 s/frame, serving ≈ 146 ms (walk 162×), wire 892×, digest 1. serve_ms = 143 ms confirms
   the O(K) aggregate rebuild binds at 10⁶ (the dossier's residue pricing, ~100 ns × 10⁶, is
   correct). cells_wrong = 27 of 786 every frame from frame 2 (wrong_cell/missing/extra/tier_err
   0): belt body ids ≥ 10⁶ alias the fleet row-id namespace (base 1,000,000, 48 members), so
   ≤ 48 belt bodies are silently unrecorded and the audit census double-counts — probe-side, but
   the exact-census audit is a ≤ 3×10⁵ fact until the offset is widened.
2. **One floor decade finer, 10⁻⁴ at 10⁴, 90 frames** (`10000 90 1 1e-4 1 0.5`): record sound —
   wrong_cell ≤ 4 of 9,717 (0.04%), missing/extra/tier_err 0, digest equals the seed-1 control's;
   walk still ~40×; but the wire win is gone (1.09×, 8,911 cells for 9,717 bodies — below
   saturation the stream is information, the honest 10³ control's own law) and observed due p50
   19/frame fires the author's own K2 (K/1000 = 10) — while the O(N) danger K2 names does not
   materialise (due flat in K across floors and rungs).
3. **500 frames at 10⁴, margin 0.5** (4× the author's longest at that rung): audit-zero is a
   ≤ 120-frame fact. A standing wrong-cell population grows with flight length — mean 0.00 →
   0.29 → 2.62 over frames 2-100/100-300/300-500, max 7 of 9,717 (0.07%, under K1's 1%), all
   self-healing at due events; px_max grows 4.7×10⁻⁵ → 1.15×10⁻⁴ (70× under θ_f, trending to
   the margin×θ_f bound); one cell's Σlum transient hits 0.25 (a crossing between predicted
   revisits) — the dossier's "max 2.7×10⁻⁵" understates the steady residue by ~4 orders.
   Digest 1 throughout.
4. **Seed 13 at 10⁴**: clean (786 FULL, audits 0, digest stable, same 0.25 Σlum transient once).

**The pricing law is biased, not just imprecise.** "Steady due 0.005/0.031/0.18/0.14 per frame"
is K/E[horizon] with a tail-dominated mean (Jensen: the true rate is E[1/h]·K). Observed steady
due: 0.3–0.5/frame at 10⁴ (500-frame arm), 6 at 3×10⁵ (the author's own metrics; the dossier's
"observed 0–2" is wrong at that rung), 15 at the 10⁻³ floor, 19 at 10⁻⁴, 20 at 10⁶ — 10–140× the
pricing everywhere. The law's *shape* (O(1)/frame, flat in K, growing as 1/θ_f) is what holds and
is what the claim needs; the constants do not. I corrected this line in the author's page in place.

**Novelty.** The published page's open direction 10 named exactly this flight as unflown ("the
view half"); cc75's entry says the record unification was a design claim, not a measurement;
docs/HISTORY.md has no earlier flight. The wiki lineage (687c scan-side, 2df1 display-side) is
cited correctly. Novel, and the checker's named experiment, executed.

**The page.** Faithful: the run entry and the top bracket match the evidence; direction 10 is
correctly re-scoped ("the view half is FLOWN"); the domain sentence already carried "flights
≤ 120 frames". I corrected the horizon-pricing line (above) and appended a Checker2 bracket
(10⁻⁴, 500-frame, seed 13, my independent 10⁶ + the 4.3 GB RSS note) after the checker's.

**Goal fit.** Yes: the board's first live question (bodies 28 → 10⁹) via dcf1's finding that the
view gather is the ladder's first N-growing per-body term. This deletes the view's O(K) walk at
fitted zoom — measured 162× at 10⁶ on the readout side, wire 892× — and names the remaining steps
honestly. PRINCIPLES #3 ("Nothing is evolved that can be derived when looked at (clocks,
redshift, views)") is the exact sentence this mechanism implements; #33's raindrop/lion is the
aggregate-per-cell. Cost to adopt: ~150 lines of additive server plus the three named unbuilt
pieces (running sums, hot-set trigger, zoom re-window).

## The one experiment that would make it gold

Fly the deletion with its last O(K) term actually deleted and the audit standing at the top
rung: (a) rebuild the cell aggregates as running sums maintained on the due/churn events
(deletes serve_ms's 143 ms at 10⁶; P1's ≤ 10 ms then holds at every rung with ~3 ms), (b) widen
the fleet row-id base so body ids ≥ 10⁶ cannot alias it (the exact census then audits at 10⁶),
(c) one ≥ 10⁴-frame arm at 10³–10⁴ pinning the steady values of the wrong-cell population,
px_max and the per-cell Σlum transient against K1's 1%. Same ladder, same audit, same digests —
if it holds, the component is adoptable as is.

## What the author missed

- P1's two failed literal clauses, reported as "P1 held" — visible in the author's own
  metrics.json; the strongest single reason this is silver.
- The Jensen bias of K/E[horizon]: the pricing and the "observed 0–2/frame" summary contradict
  the author's own logs at 3×10⁵ (6) and the 10⁻³ floor (15).
- The exactness constants (audit zero, px_max 4.3×10⁻⁵, dlum max 2.7×10⁻⁵) are flight-length
  artifacts; the ≤ 120-frame blind spot was named but the constants were still quoted as
  headline evidence. At 500 frames: 0.07% standing wrong-cell, 1.15×10⁻⁴ px, 0.25 Σlum.
- The id-namespace collision (fleet base 1,000,000 vs body ids ≥ 10⁶) caps the exact-census
  audit at 3×10⁵ — one constant, found only by flying the next decade.
- The wire win's floor-dependence below saturation (1.09× at 10⁻⁴) confirms rather than breaks
  the claim, but the K2 wall (fires between 10⁻³ and 10⁻⁴ at 10⁴) deserved a sentence: the
  record's maintenance cost is 1/θ_f-shaped, so the zoom tax is a churn tax too.
- Probe hygiene: `drop(r)` on a `&mut` is a no-op (build warning); dead `far`/`for r in steady`
  in analyze.py.
- My own error, disclosed: the 10⁶ probe peaked at 4.3 GB RSS (the driver serialises the full
  oracle wire, ~270 MB ×2 at 10⁶) — above the box's 2 GB guidance; it survived, and I did not
  repeat it.
