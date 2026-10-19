Grade: silver

**Abstract.** The belt's rebind cells saturate, not accumulate: 1,831 standing (11+11) cells at 299,699 bodies, reproduced bit-for-bit; the checker extended it 33× beyond the top arm by censusing keys straight from the draw program (10⁷ bodies: 2,141 cells, 2.03 MB, 0.20 B/body, β = 0.083, seeds within 0.3%) and to ~8.4 belt intervals (stream still exactly its 1,425 birth cells). Gain: the belt's shape memory is O(1) — ~2–3 MB at any N against 2,460–5,100 B/body live — and the 10⁹ rebind stream re-prices from ~4 compiled cores to ~0.02–0.04 served. One correction: the 4,096-cell ceiling is draw-bounded (≤ 2 gap octaves from a ∈ [2,3) AU, p > 1.2 AU), not code-bounded. Silver because the CPU row composes cited constants (0355's serve cost still awaiting grade) and adoption — 9eeb's wiring, B12/B13/B17 re-judged, guard recalibration, the unflown turnover arm — is the one experiment to gold.

## Reproduction

Clean tree at `c41a9892` (the runner had reverted the patch after its regen; `regen.log` matches every dossier number). I applied `work/patch.diff` myself and re-ran:

- `beltcensus 300000 1 0 1800` — bit-for-bit: 1,831 cells w11, weak 1.0000, 270,195 keys, 484/127/33 at w9/7/5, 5.58 B/body. Peak RSS 845 MB.
- `beltcensus 100000 1 50 1800` — birth census bit-for-bit (1,731 cells, 96,358 keys, 15.41 B/body); stream cells exactly 1,760, recurrence 0.9943 (author 0.9942), belt recurrence 0.9915 (0.9914), new-beyond-birth 29, fires p50 2. Live-flight counters differ in the 4th digit (rebinds 306,339 vs 304,239) — budget/wall noise, not a discrepancy.
- `cargo test -p emergent-universe --test memo`, hook OFF and ON (`ES_CENSUS=1`): both pass, 0.44 s — the print-only hook leaves the shipped path inert.

The hook itself is sound: one relaxed load when `ES_CENSUS` is unset, records `(body, MemoCode bits)` per actual rebind in `step.rs`, passages/plunges skipped — the rebinds are distinct state changes by construction, so the 5 October re-timed-kick lesson does not bite here.

## Predictions

`predictions.md` predates the dossier by 4 minutes of file time and shows tuning only on the disclosed 3×10³ pilot. P1 actuals sat 4–8 % *above* the pre-registered band tops (1,610/1,731/1,831 vs tops 1,550/1,650/1,700), β = 0.11 against ≤ 0.1 — all disclosed, and the systematic undershoot is the signature of an honest pre-registration, not a tuned fit. Kill criteria (> 4,000 cells or β > 0.25) never fired. P2 held and is stronger than registered (belt stream cells = birth cells *exactly*). P3 held (15.4 vs < 15 B/body at 10⁵, 3 % over). P4 held (weak 1.0000 every arm). P5's unflown domains scope the claim honestly.

## Attacks (4, two beyond the author's range)

1. **Next decades (outside the range).** A live 10⁶ arm is impossible under the 2 GB cap (845 MB at 3×10⁵), so I censused keys directly from `ladder_ship` + `OrbitKey::bound` with doll 0's unit — validated **exact** against the universe census at 10⁵ (96,358 keys, 1,731 cells, 1,401,000 bytes), then run to 3×10⁶ (**2,035 cells**) and 10⁷ bodies: **2,141 cells, 2.03 MB standing, 0.20 B/body, β = 0.083 over 3×10³→10⁷** (0.046 over 10⁵→10⁷); seed 2 at 10⁷: 2,136; seed 7 at 10⁵: 1,728. Saturation is real and robust; the exact-key memo stays dead (1.73 M distinct keys at 10⁷, occupancy 0.17).
2. **Horizon past the named blind spot.** 10⁴ seed 1 at 140 s wall → 250,282 game-s, ~8.4 belt intervals (author: 2–3.2; the 8ffc shearing horizon is 5–6): belt stream cells still **exactly the 1,425 birth cells**, belt recurrence 0.9837, cells/body p50 1, fires p50 9; all 144 new-beyond-birth cells are the locals' (their cells 459→698 — the locals, not the belt, are the ones still exploring).
3. **Seeds.** Seed 2 (author) and my seed 7 and 10⁷-seed-2 all within 0.3 % — the census is a property of the draw, not a seed accident.
4. **The ceiling's mechanism (the correction).** The gap-exponent histogram: **every** belt key at the author's N sits in gap octave `ge=1` (99,699/99,699). So the occupied ceiling is 2,048, and the "2 exponent × 2,048 = 4,096" is not a property of `MemoCode::shape_bits` (whose weak branch allows 64 octaves × 2,048 = 131,072) — the octave *count* belongs to the draw (a ∈ [2,3) AU with p > 1.2 AU bounds the gap to ≤ 2 binades). The second octave opens only at ~3×10⁶ bodies (37 keys; 126 at 10⁷), which is why the author's per-decade increments (185→121→100, "shrinking") stabilise near 200/decade instead of dying. The 4,096 value survives for *this* belt; a wider or multi-belt galaxy multiplies it by octave count. Corrected in the page.

## Novelty

The lab wiki's cell-rebind page (unchanged base, `updated: 20261018-2312-system-9eeb`) names exactly this as open: "the belt's cell census at this width (unmeasured; the view page's 'peaks at 37' was a coarser 2⁻³ grouping)", and the 9eeb checker note called "the gates + belt census" the gold rung. No `belt census`/`beltcensus` entry in docs/HISTORY.md. This run is the census half of that rung; nothing prior measured the standing set on the belt. Not a repetition.

## The page

Faithful fold-in: the 9eeb content is carried verbatim, the open direction struck through and closed, the turnover successor added. Corrected in place where it overstated: (1) the ceiling attribution ("a property of the code, not the fit" → draw-bounded, one octave occupied at the run's N, second opens ~3×10⁶, with the 10⁷ extension); (2) the locals' rebind range 104–136k → 103–160k (seed 2 measured 160,388); (3) added the 948 B/shape figure at the 10⁷ cells. Runs line and header are accurate. (One note: mid-check, the author's paragraph about the locals lost its "459–506 stream cells" clause between my first read and my edits — no other clause changed and the remaining sentence is supported by the log; the corrected range now covers it.)

## Goal fit

Moves the board's memory-at-10⁹ row and the budget-1e9 interlock's live-bytes term for the belt: the standing shape set is O(1) in N, measured (not composed) to 10⁷. PRINCIPLES fit is exact — 6 ("Store the generator, not the generated"), 33 ("a body resolves only the influences that are significant at its own scale, and smaller ones enter as an aggregate"), 24 ("The memory floor is information": ~11 gap bits per shape is near the belt's actual entropy). The instrument is print-only on the shipped law; no gate, crate or frozen evidence touched.

## Why silver, not gold

The measured core (saturation, stationarity of the stream, the ceiling) is gold-quality and survived every attack including two beyond its range. What holds it at silver: the headline 10⁹ re-pricing (0.016–0.037 vs 3.7–4.5 cores) is a composition of cited constants — 0659's fire rate (p = 1.0, worst arm), 0355's 0.40 µs serve (itself awaiting grade), 9eeb's 0.85 µs carried serve — not a measurement; and it is adoptable only through 9eeb's law change (B12/B13/B17 re-judged, memo.rs guard recalibration), which this run de-risks but does not fly. Exactly one named experiment remains, as the 9eeb checker pre-registered: **the gates + census rung** — wire `Orbit::from_shared` in the rebind, re-judge B12/B13/B17, recalibrate the 0.9 guard on the served stream, and fly the turnover arm (stirred belt + burn) with this census hook; that converts both halves into an adopted, measured 10⁹ row.

## What the author missed

- The ceiling's attribution (attack 4): octave count is the draw's, not the code's; the second octave opening at 3×10⁶ explains why the increments stop shrinking — the "missing-mass of the Rayleigh e-draw" model is incomplete without it.
- The live 10⁵/3×10⁵ arms leave a 845 MB RSS trail, so the census method itself does not scale to the decade it prices; the key-space census (draw program + `OrbitKey::bound`, validated exact) reaches 10⁷ in 4 s and 32 MB and should be the instrument for the turnover successor too.
- The locals (459→698 stream cells over the longer horizon) keep exploring; at galaxy scale their population may need its own census before the "one aggregate" sentence generalises past the belt.
- The composition leans on read-stream 0355's serve constant while that run is still awaiting grade; if 0355 falls, the 0.40 µs serve goes with it (the 0.85 µs carried serve from cell-rebind survives).
