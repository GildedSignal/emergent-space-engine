Grade: gold

**Abstract.** Second-author flight of cc75's named experiment: the view's far rows served from a
window-membership record over the sky circle. Reproduced on a clean tree (runner regen exit 0 + my
own fresh arms): readouts 351–374/frame flat in K to 3×10⁵; serving path 13.4/35.8 ms against the
oracle gather's 2,350/7,040 ms (177×/198×); wire 89×/268× (27 MB → 302 KB/frame at 10⁵); audits
zero, fresh rows bit-identical, engine digest unchanged three ways. My extensions: the margin cliff
is benign, seed 7 at 10⁵ clean, a 1200-frame flight shows a bounded standing wrong-cell population
(≤ 0.8% of far rows), and at K = 10⁶ the flat law itself holds (162× walk) with the O(K) aggregate
rebuild at 142 ms (running sums now mandatory) and a probe-side census artifact (27/786 cells).
Adoption: additive, digest-neutral server; needs running sums, the hot-set trigger, zoom re-window.

## Reasons

**Reproduction.** Applied `work/patch.diff` myself to the clean tree at base `e4f3b7ed`
(reverse-check clean, builds, purely additive to view.rs + a driver; one benign `drop(&mut)`
warning). The runner's regen (exit 0) and my own re-derived metrics agree with every dossier
number: oracle gather p50 19.3/230.7/2,349.6/7,039.6 ms; serving path (near+due+serve)
2.7/3.7/13.4/36.0 ms; wire falls 1.31/9.05/89.4/268.1×; served rows 823/1,143/1,145/1,145
(470/786/786/786 cells); ratchet floor 6,284 cells, 6,643 rows, 15.65×; px_max ≤ 4.3×10⁻⁵;
Σlum p50 ≤ 1.1×10⁻⁵; wrong_cell/missing/extra/tier_err zero at 10³–10⁵ (the one ratchet frame of
wrong_cell = 1 reproduced, plus cells_wrong max 2 there, which the dossier omits); serve-arm end
digests equal control arms at all three rungs; no `digest=0` in any serve log; the patched-tree
bench digest equals cc75's unpatched `1b801358…`. The churn law is confirmed K-independent
(horizon p50 71,392/69,041/68,962/68,867).

**Predictions.** `predictions.md` predates the dossier and final logs (folder mtimes; the runner's
regen overwrote the author's work logs, so the author's own flight-log times are not independently
checkable — noted, not counted against). P2, P3, P5, P6 held (wire 9.0/89/268 vs predicted
~9/~90/~270; ratchet ~15.7 vs ~15; seed 7 clean). P4 missed on a constant (px_max 4.3×10⁻⁵ vs
≤ 10⁻⁵) and was reported as a miss — good. **P1 did not fully hold and the dossier says it did**:
its literal clauses "server's own per-frame cost ≤ 10 ms at every rung" and "≥ 300× at 3×10⁵"
measured 36 ms and 198× (the serve-loop aggregate rebuild is O(K), not the O(cells) P1 assumed).
The numbers are in the dossier's own table and the residue is its named honest residue #1, so
nothing was hidden — but the predictions summary reports only the held clauses. I corrected the
page. No kill criterion fired (K1: wrong_cell max 0/1; K2: due ≪ K/1000; K3: 13 ms ≪ 120 ms;
K4: 0; K5: 0).

**Adversarial (mine; one outside the author's range).**
1. *Margin cliff, 10⁴, 90 frames:* margin 1.0 (no slack) breaks exactness gracefully — wrong_cell
   p50 2/max 3 of 9,717 far rows, self-healing at due events, digest unchanged; margin 0.25 clean.
   The 0.5 margin is load-bearing, and the failure mode is bounded, not a blow-up.
2. *10× flight length (10³, 1,200 frames):* audit-zero is a ≤ 120-frame fact. A standing
   wrong-cell population appears (464 of 1,195 frames, mean ~1, max 6 of 717 far rows = 0.8%,
   under K1's 1%); px_max grows to 4.2×10⁻⁴ rad (19× under θ_f); 20 due events ≈ the priced law;
   digest never moves. The record self-heals; the errors do not compound.
3. *Seed 7 at 10⁵ (author flew it only at 10⁴):* clean — 786 FULL, audits zero, 13 ms vs 2,350 ms.
4. *Next decade, K = 10⁶, 10 frames (outside the author's range):* the flat law itself holds —
   786 cells FULL, 1,146 rows, ~302 KB served, readouts ~370, horizon p50 68,810 (K-independence
   extends a decade), digest 1 at every probe, walk fall 162×. Two new facts: serve_ms 142 ms
   (the O(K) rebuild at ~142 ns/member — the running-sums deletion is *required*, not optional,
   at 10⁶, exactly as the author's lens predicted at 100 ns × 10⁶); and a persistent bounded
   census artifact — cells_wrong 27 of 786 cells every frame, worst-cell Σlum 1.5×10⁻³, one
   transient missing at a handout frame (missing/extra/wrong_cell/tier_err otherwise 0). Candidate
   mechanisms: the probe's id convention (body ids ≥ 10⁶ collide with the fleet's row-id range
   1,000,000–1,000,047) or the audit census counting fresh far fleet rows that are never recorded.
   Probe-side either way, but the exact-census audit is a ≤ 3×10⁵ fact until the id offset is
   widened.

**Novelty.** The published view page bracketed cc75's record as "this run's design claim, not a
measurement" and open direction 10 asked for exactly this flight; the prior rung was held at
silver for not flying it. 2df1's deletion is the canvas/display side (panel audit 0.1–2%); 687c's
window-membership record is the scan side; this is the seen-stream/gather side with an exact
per-row audit against the oracle's own rows. Not a repetition; the composition claim (one record
class, two windows) is now half-measured, as the page says.

**The page.** Faithful fold-in (new top bracket, direction 10 moved from "to fly" to "flown", run
line appended; prior bests retained). I corrected three overstatements in place: observed due p50
is 0/0/2/6 across the rungs (not "0–2"; 6 at 3×10⁵), the ratchet arm's observed due p50 is
15/frame in the 40-frame transient (the stated 1.9 is the priced steady rate), and I added a
checker bracket carrying the extensions, the 10⁶ artifact, and the P1 clause misses.

**Goal fit.** The board's first live question (bodies 28 → 10⁹): dcf1 named the view gather as the
ladder's first N-growing per-body term, and this run deletes its walk (177×/198× at 10⁵/3×10⁵)
and its wire (89×/268×), with digest neutrality proven three ways. PRINCIPLES #3 — "Nothing is
evolved that can be derived when looked at (clocks, redshift, views)": the far row is derived at
the tick from membership + the cell aggregate, and membership itself moves only at crossing
events; #1 — the cheapest compute is the row not walked; #24 — the floor is what the player can
differentiate, and the record's cost is 2π/θ_f; #33 — the belt below one sky pixel is the
raindrop, entering as an aggregate; #13 — the audit shows the record self-heals at due events and
(my 1200-frame flight) the error does not compound.

**Why gold and not silver.** Reproduced end-to-end; the scoped claim (flat readouts/wire at
fitted zoom on the shipped scene class, audit exact, digest untouched, the rebuild as the one
measured O(K) residue) is exactly what was flown and every number regenerates; it deletes the
component the previous checker held the rung for, by two orders of magnitude; it is adoptable
within one step (additive, digest-neutral, composes with 2df1's wire side and 687c's scan side).
The reporting defects (P1's dropped clauses, the due-rate wordings) are corrected on the page and
named here; the underlying numbers were never hidden — they are in the dossier's own table. My
attacks bound the domain (margin is load-bearing but fails gracefully; audit-zero decays with
flight length to a bounded population; 10⁶ needs running sums and an id-offset fix) without
killing any claim the run actually makes.

## What the author missed

- P1's literal thresholds (≤ 10 ms every rung; ≥ 300× at 3×10⁵) failed and the predictions summary
  reports P1 as held — the one reporting defect in the run.
- The observed due rates vs priced: 6/frame at 3×10⁵ (stated "0–2"), and the ratchet arm's
  40-frame transient runs 15/frame against the priced 1.9 (stated as "due rate 1.9/frame").
- Audit-zero is flight-length-dependent: over 10× the horizon a bounded standing wrong-cell
  population (≤ 0.8%) appears, self-healing — the domain line says crossings were "priced, not
  observed", but not that the exact-zero audit itself decays.
- The 10⁶ decade: the flat law holds, but serve_ms hits 142 ms (running sums become mandatory,
  not "deletable"), and the id convention (body ids ≥ 10⁶ vs fleet ids 1,000,000–1,000,047) or the
  census definition produces a 27/786-cell artifact — the exact-census claim needs the id offset
  widened before it extends past 3×10⁵.
- The aggregate's displayed direction is the cell centre by construction (never audited against
  the member-weighted mean); covered by the θ_f floor argument but unstated.

For the next run on this topic (not gold-blocking): the formation ruin class, the hot-set trigger
on the kick stream (cd3b), the zoom re-window against ee30's drain, and running cell sums —
which together would close open direction 10's remaining half.
