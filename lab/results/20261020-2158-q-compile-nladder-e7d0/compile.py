#!/usr/bin/env python3
"""Compile lab/wiki/nladder.md back under its budget (lens: q-compile-nladder).

Reads the shipped page (never writes it), deduplicates `## Runs` to one line per
run id (preferring each id's graded, complete line; grades refreshed from the run
branches by wiki.py's own rule), completes the five run lines the old page leaves
mid-sentence (from those runs' own dossiers/entries), and emits the compiled page
to results/<run>/wiki/nladder.md with:

  - `## Current best`: <= 15 lines, the standing numbers with domain and run ids;
  - `## Refuted`: one line per superseded or killed claim, with its run;
  - `## Open directions`: <= 8, ranked by board row and multiplier;
  - `## Contradictions`: only the unresolved ones;
  - `## Runs`: every run, one line each.

Then audits: the budget by lab/wiki.py's own counting, run coverage, and a fixed
30-number preservation sample. Exits non-zero if any audit fails.
"""
import collections, json, os, re, subprocess, sys

ROOT = os.getcwd()
OLD_PAGE = os.path.join(ROOT, "lab/wiki/nladder.md")
OUT_DIR = os.path.join(ROOT, "lab/results/20261020-2158-q-compile-nladder-e7d0")
OUT_PAGE = os.path.join(OUT_DIR, "wiki", "nladder.md")
RUN_ID = "20261020-2158-q-compile-nladder-e7d0"

# ---------------------------------------------------------------- current best
CURRENT_BEST = """**The belt's clock stream (the ladder's own event law):** each belt ship's clock ticks every ~27.9k game-s and emits a KICK comb and a BOUNDARY comb exactly half a period apart (step.rs:717-718) — ~1.1 events/body per 13.9-14k gs, flat ±1.3% through eras (8 eras / 120k gs flown, decay -26% by era 8), burn and coast identical; total kick rate 4.889e-5 kicks/body/gs at 1e5-3e5 (0a46; 8365; 9ed1); the belt's cadence is the doll's — P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law, shipped step_log2 148x over at flying pace (cf45).
**The combs' cost is PAYLOAD, not path:** 45.3-45.9 µs/kick vs 5.9-8.6 µs/boundary (honest 4-era split 7.7x); coast alternates era walls 5.6/1.6/5.2/1.6 s with the player flat (max frame 12.0 ms, player-class cost flat 0.46-0.47 s) — the budget-latch and the gulp-vs-drain attributions are dead; at 1e9 each 27.9k-gs era costs ~12.8 h (kick comb) then ~2.4 h (boundary comb), alternating forever; "make era 1 serve like era 2" is dead as a scheduling lever (8365 + checker2).
**The stagger kills the kick-comb freeze at every rung flown:** a birth phase-spread of one comb width (ES_STAGGER_GS, 8365's gate: 49%→16% in the 4 hottest bins at 14k spread) takes the worst frame 718-1231 → 40.6 ms at an IDENTICAL kick stream (4.889e-5 vs 4.899e-5); era-1 max = the 12 ms budget at 1e5/2e5/3e5 (unstaggered 714.9/1,568.6/2,430.4 ms), seed 2, load-16 (no batch over 1,852 events; worst 351.5 ms is drain), 8 eras with no re-concentration (21.6→14.9%); walls only BAND under a 14k spread (1.72-1.98x) — the 28k payload interleave (half the clocks offset half a period) flattens them (8365; 9ed1).
**The standing freeze after the stagger is ONE held-scan answer:** the answer walks the doll at 4.2-4.4 µs/BODY — O(N) in the belt, measured at every rung (442.9/1e5, 847.8/2e5, 1,273.5/3e5 ms; ms/encounter 6.2-7.15 vs 0.1-1 normal) — TTL-proof (TTL=8: 1,272.4 ms), 3/3 draws at 3e5 (the en=178 object, ~1 ms class-attributed, 6.9 ms/encounter, kill bar 1,225 >= 800), ~4 ks in ONE frame at 1e9: a walk prop. to doll population is the allocator's true ruin (9ed1 + checker).
**The two O(N) walks, typed per body:** capture (building the scan, ON the player's item — the frame's critical path) walks EVERY body of the doll when the radial apsidal filter bails (the in-belt burn regime; coast has zero ALL captures): 0.25-0.30 µs/body across rungs (74-91 ms per walk of 300,076 at 3e5), fence-independent, ~1.1 ms of average frame at 1e5; the same bail walk measured 190-205 ns/body linear to 1e5 on the crowd scene; answer = 4.2-4.4 µs/body, 97% the cartesian read; the drain guard locks the channel at every belt rung >= 3e3 (one answer > 6 ms ≈ 1.4k candidates), so belt-wide scans (cand = 299,715 at 3e5) exit only via the 2048 cap or the TTL fence (a0a1 + checker; 96f6).
**The dropped carry bound is exact and ~100x on the warm walk:** ce694696's per-body remembered-position map (dropped by 72b71c56), re-anchored on the shipped `same` behind ES_CARRY_BOUND, is digest-IDENTICAL to the shipped finder at canonical cuts (OFF 8eecf1fa twice byte-identical; 4.1e6 bound decisions at mean 97.55% skip) at 1e5/3e5/3e3; warm belt-wide answers 0.041 µs/body (best 0.030) against the 4.17-4.5 law ≈ 100x, one cold lump 3.86 µs/body per flight, settle 18.4→1.1 s at 1e5, 1.6→0.2 at 3e5 — and it does NOT touch the capture walk (0.267/0.247 ON/OFF at 1e5, 0.292 at 3e5) nor reopen the channel (belt-wide scans still never answered in-window) (23a6; a0a1's two sentences die).
**The memo's invalidation law:** delta_eff = miss/(λ·gap) is NOT a constant — 0.053-0.399, drifting (28/40 inside a2c0's fitted [0.065,0.266]; the <0.5 letter and the delta=1 exclusion are WINDOW facts of gs 19.9k-29.9k, not scene laws); the mechanism is slack-margin crossing (at constant 165-gs gaps the miss grows 7.5x, 0.044→0.333%, as the burn approaches the belt; kick-Poisson dead outright), c_check 27.4 ns/cand (20f2 + checker; a2c0).
**The single-doll 1e9 ledger (why the representation is the exit):** kick comb 12.75 h/era = 658x the 69.75 s era budget (50 s = 0.72x at the scoreboard's ~50 ns kick-item floor — the deletion of the boundary comb, -50% of stream events, buys only 1.2x and halves the alternation) + capture ALL-walks 2.15-6.02 h/era + answers 1.19 h = 16.1-20.0 h/era = 830-1,030x budget; era-cadence answers alone read 24-57x budget, the 330-gs warm cadence pays 44x in checks alone — no cadence reaches the quoted 41 s (20f2; a2c0; a31c).
**The standing exit is the Binet cone TIER, not incremental answering:** the seam is wired (universe.rs:469), ask cost O(k) with the width DERIVED — never k <= 4, this wiki's own refuted constant (coorbital-cert: k ≈ 16-17 at 10^6 line density; the built tier sizes windows by occupancy, 74a1/4ec3); incremental answering is dead twice (f102: no maintenance signal below the candidate set exists — no epoch/version/dirty bit in encounter.rs or radial.rs; its maintenance rides the 658x comb); the walk's kill is form, not policy: walked spans 4,127x across flown scenes while kept spans 10.6x (32.5→333, en=178), >= 3x10^6 reads per answer of O(10^2) content, 4.2-4.4 ks = 60.2-63.1x budget at 1e9 (b57f).
**Memory channel 1 — the held scans:** bytes_touched = 0.0526 mints/game-s · (K+38) · 224 B, exact (identity 0.997-0.999 over 7 flights), and the burning player mints 13.5x coast (16.8x same-convention, stream bit-identical 10^5→7x10^5: 145/2,069 entries, census equal); the TTL fence (ES_SCAN_TTL_S=16) deletes the channel — 120k gs flat at 635 MB at 1e5, <= 0.3% encounters — a law change owing the digest re-freeze; channel 1 saturates at 444 MB by 46k gs at 3x10^4; at 1e5 the rung's wall is 82-100% this channel, residual machinery <= 0.15 KB/kick — no per-kick memory law at 1e5 (acf2; 2403; 99da; e181; b911; 7b6f).
**Memory channel 2 — history retention behind the receding observer:** the binder is the 2·light_distance term in BOTH the visit key and the keep — freezing both switches the ratchet off totally and permanently (census flat ±50 bindings for 180k+ gs; post-onset freeze still works), either half alone still ratchets; 1,295 B deep / 1,760 B RSS per extra binding (RSS = 64.6 + 1.063·scan + 1.359·hist, rmse 15.8 MB); retained-extra ≈ 1.4·λ·(2·ld+330 s), unbounded in play time (the visit key re-keys with the live distance: onset 1.5 rising to 2.3 late); the TTL fence alone staircases to 1,457 MB at 419k gs — ~15% horizon at 3x10^4, both arms guard at O(0.3-0.5x10^6) (b911; f80a + two gold checkers).
**The burn-mode ratchet (the plane's memory wall):** unbounded in play time and past every prior horizon — 10^4 flies 560,764 game-s (93 wall-min) to a 1,601 MB guard still climbing 3.4 MB/1k gs; 3x10^4 guards at 332,604 gs; mid-flight slopes ~K-proportional (5.7/16.3/42.8 MB/1k gs at 10^4/3x10^4/10^5); 4 GiB at ~95k gs ≈ 16 wall-min at 10^5; one wall-hour of held L8 burn = 989 MB-2.2 GB; coast is flat (61 MB, 0.02 MB/1k, held 0) — the ratchet needs the player interstellar, and the reader-oldest door is NOT its channel (ON ≡ OFF to the digit, gap_s <= 1.7 s) (4447 + two blind checkers; 527a).
**The oldest door (prune's horizon):** closed at one star BY CONSTRUCTION — now − oldest <= the widest pending light gap (max 2,302.5 s over 77,399 gs at 3x10^4; 0-0.1 s in the quiet scenes); a pin deeper than the gap staircases +1 generation/body per 27.6k gs (law 1 + ⌊min(D,elapsed)/27.6k⌋ + ~1, unbounded in play time) at ~2 KB/retained binding (1.9-2.35 KB, N-independent; RSS 155→279→384 MB at D = 6e9/1.2e10 ticks) and eats the frame (over 6→383/683; at 10^5 23% over, p99 61 ms); at 4 ly ONE pending item is ~+9.2 MB/body ≈ 9.2 TB at the 10^6 rung — the first interstellar doll is ruin while its light is in flight; the fix is the term's SCOPE, and per-reader oldest is flown bit-neutral with the pin live (1.016 vs 5.14/body; digest suite byte-identical; per-doll calendars stale on handoffs — found and fixed) (4a71 + two checkers; 1b3f).
**The root-doll player item (the burn freeze's mechanism) and its gate:** the worst frame of every rung 10^4-3x10^5 is ONE top-level item — the player's — holding >= 99.5% of the frame's wall as NESTED ship kicks the budget never checks (max_ms ≈ 8.1-9.5 µs x K; 1,643.5 ms / 32,958 kicks at 2x10^5 at 49.8-57 µs/kick; the budget-bypass is causal: a 2 ms budget still gulps 938.7 ms; 2,840.8 ms ≈ 9.5 µs x K at 3x10^5); ES_ROOT_STREAM (19 lines, ee4d) collapses it to 13.9-18.1 ms with mega-frames 0 and the canonical cut BIT-IDENTICAL (1d47's gate: 58-111x, 14/14 shipped digests), price 0.62-0.71x rtf in the wave era; under the canonical-tick cut_digest both gate forms hold ONE digest a rung over 34 runs (stale reads answer 3-6 encounters a run, verdict-preserving) — the invariance is empirical (0 flips), not structural (cc9d + checker; ee4d; 1d47; 4063).
**The locals' comb is CLOSED, and the ladder's steady state:** the composed law (ES_SECULAR + ES_CHAIN + ES_LOCAL_STAGGER) is strictly dominant (max 41 vs 52/131; ledger 6,298 vs 22,219 = -72%; envelope decays 41→3; N-flat 0-10^5; 13/13 schedule-determinism; patch-off = the frozen record) and legality-dominant (doll-born |ΔE/E0| median 5.5e-11 at 11,000 gs = 424x under OFF, flat in horizon; the spared tail bit-identical to chain+stagger's); the delete ALONE transfers to the crowd scene (1,013→28 max events at 10^3; the de-phase converts the standing 8-frame beat into uniform O(K) load, 6.2x sim-time starvation — never ship a de-phase without it); the comb is 0.006% of the 10^9 stream, so no comb decision moves the 10^9 CPU ledger; coast per-body memory is a CONSTANT through waves (4.85-5.06 kB/body steady, +0.2-0.7%/wave, build 2,338-2,459 B/body, catalogue constant; the view gather at 5.0 µs/seen-body, seen = N+61, is the ladder's first N-growing per-body term); the 10^6 gate rung reproduces on the Linux lab at 2,346 MB peak / 86.8 s through a 6-line instrument port, and the wave the rung's 20-s window cannot see costs 704.7/2,395.3 ms single frames at 1e5/3e5 — but F1's zero-lag clause does NOT reproduce there (worst lag 1.448 s; the M1 rows read 0.000) (f134; 7fcf; 7581; 1051; b30b; d839; 99da; dcf1; 03f4)."""

# ------------------------------------------------------------------- refuted
REFUTED = [
'"The wave is an event" (the premise under 2d26\'s coverage, 476d\'s crest law and ca63\'s 13.2 h/wave, all built on <= 2-era windows): the comb stands — 1.09-1.12 ev/body/era, flat ±1.3% through 4-8 eras at two seeds and two rungs, coast-identical; every per-wave 1e9 number is a per-14k-gs recurring floor (0a46).',
'"The freeze follows the arrivals" (cc9d\'s K-law read as an every-era law): across four identical-arrival eras the worst frame alternates 718/42/339/12 ms (same at 1.5e5 and seed 2) — a separate, schedule-state channel; clean eras serve the same arrivals 3x cheaper (12-17 vs 47-50 µs/event) (0a46).',
'e181\'s "expiring held scans past 16 game-s deletes the burn-mode ratchet" as an unscoped claim: with prune() restored and the arm flown past every prior horizon, the fence deletes the scan channel only — the history channel alone staircases unbounded (+1 binding/body/wave from the FIRST wave, 1,457 MB at 419k gs, ~15% horizon at 3x10^4) (f80a).',
'"1b3f\'s per-reader `oldest` is the fix for 4447\'s burn-mode ratchet": identical to the digit at 60k gs and at the guard (gs 332,277/332,604, held 588 both, census 620,831 both); gap_s never opens (<= 1.7 s) — two channels, two fixes (527a).',
'"Memory per body might grow with every cadence wave" (d839\'s own pre-registered P2): flat through the second full kick wave and the boundary wave at 3x10^4 and 10^5 (+0.2-0.7%/wave); the steady state is one retired + one current binding per body (d839).',
'"The prune horizon is safe as shipped, at any scale": the door is closed at one star only because the widest pending light gap there is ~2,300 s; the horizon rule makes now − oldest equal that gap BY CONSTRUCTION — the certificate is scale-coupled and inverts at the first far doll (4a71).',
'dcf1\'s "VmHWM grows K-flat ... 8 GB ~300,000 game-s out" under burn: the flight ended at the SOI switch (frame 948), the phase boundary where the ratchet begins — past it the slope is K-growing (5.7/16.3/42.8 MB/1k gs at 10^4/3x10^4/10^5), 4 GiB at ~95k gs at 10^5; the "~300 locals cap the candidates" mechanism does not hold interstellar (4447; 10^5 arm checker2).',
'0a46\'s "3x served-path lever" (gulped vs budgeted paths): the carrier is the ships\' own sequential items — 45.9 µs/kick vs 8.6 µs/boundary PAYLOAD — and coast pays the same split with no gulp at all; the alternation is per-ship structure (8365).',
'8365\'s "with the stagger the freeze — max 718-1231 → 40.6 ms" as the final word: the scan-answer channel regrows it — 0.4-0.8 s at 1e5/2e5 (one draw in three), reliably ~1.2 s at 3e5 (2.4 s off / 1.2 s on), TTL-proof (9ed1).',
'2d26\'s excess x2.37 per x2 K law and its coverage table: the full-window excess has ±46% same-scene flight spread and is load-elastic (load 24 reads 74 ms where idle reads 9,814); coverage(1e9) demotes to an order-of-magnitude span, 1e-5...1e-4 (476d + checker).',
'ca63\'s alpha(2e5→3e5) "disjoint band" [1.427..1.632] and the +26% cost steepening: single draws — three 3e5 flights give alpha {1.53, 0.92, 0.90}; crest ≈ K-linear at ~48-50 µs/event with the record\'s ±22% floor; the 0.977-1.038 crest constant is registration x seed-bound (ca63 checkers).',
'476d\'s crest alpha 1.08-1.15 and tail alpha 1.92 as adopted constants: window artifacts or single-regime draws; crest-vs-amortized is schedule-chosen (476d checker).',
'476d\'s "the tail does not need the stagger (the fence deletes it)": TTL=16 does NOT delete the tail (3,050 vs 2,226 ms at 1e5) while it does delete the scan channel — the whole wave is ONE arrival phenomenon (≈2.3-2.5/body over 20k gs; 1e5 idle 2.49-2.51), so the stagger targets all of it (ca63 + checkers).',
'3eb3\'s "the named 10^5 rung\'s wall is kick machinery (5.3-9.9 KB/kick)": collinear regressors on the same bytes — 82-100% of the wall is the scan channel, residual machinery <= 0.15 KB/kick; no per-kick memory law at 1e5 (7b6f + checker).',
'3eb3\'s "scene-fixed locals / nil seed spread on the primitive": seed 3 at 5x10^4 fails both registered ratio bands (stream 1.447 vs [1.73,2.11]) — quiet-region locals wander 1,466-1,486 → 1,813-1,832 across seeds (3eb3 checker).',
'88e9\'s naive "ratchet slope ÷ S" split reading: killed by its own pre-registered falsifier (1.76-1.86 measured vs the [4,16] band); the ratio is the BULK\'S SHARE of the kick stream (1.76-1.92x at 3x10^4-5x10^4, 8.00x only at 10^9) (88e9; 3eb3).',
'96f6\'s pin ranking (compare-form at 6.25x10^5, pin "co-located ~6-7x10^5") and its x-held model: the direct Drop count is 40-51 distinct and the pin stands ALONE (8 GB at 687 game-s ≈ 7 wall-s at the 10^6 target; native compare 0.50-0.53 ns/member, 40x under the 19.2 numpy replica); x-held refuted by its own hwm (acf2; 96f6 checker).',
'acf2\'s "alive == mints in every flight" (the freeze\'s universality): at K = 10^3 over 25,899 gs the quiet frame margin answers every scan in-frame (mints 1,260, held_max 0) — domain K >~ 10^4 on this scene; both branches ruin only above the drain\'s crossover (acf2 checker).',
'2403\'s "all six predictions held" headline: P1 and P6 were NOT held as written (coast-phase λ 0.0027/0.431 against the 0.05-0.15 band; +21 MB against >= +100 MB) — corrected on the record by the second author (99da).',
'0c0f\'s "the burst\'s simplest cause is shared kick-grid phase at birth": the burst is BURN-gated (coast at the same rung and cadence has no wave, onset window covered) — the shared phase is the burn\'s kick-grid re-mint; the stagger dial must target the burn response, not birth (0c0f checker).',
'1d47\'s "bookkeeping, not a law — nothing to re-freeze": at canonical cuts (settle(cut), the shipped contract) the gate makes the digest SCHEDULE-DEPENDENT at 1e5 and 2e5 (ON bistable: ad732607/1770 vs 75543d72/1775; kicks moved -11 in one) — a stale read does change what the scans find (1d47 checker).',
'1d47 checker\'s ON bistability as a property of the gate: not reproduced under the canonical-tick cut_digest (34 cut runs, one digest a rung, ON\'s 1,838-entry encounter log byte-identical across reruns; stale answers verdict-preserving) — the invariance is empirical (0 flips), not structural; the structural fix is canonical bindings in capture (4063).',
'527a\'s "the drop threshold is not the binder — the body is simply never visited again": both terms (the visit key AND the keep) carry the ratchet — freezing either half alone leaves it alive; the level law and the 1.4·λ·(2·ld+330 s) retained-extra hold (b911).',
'4c22\'s per-frame attribution (the "unattributed pull-lane residue"): the ES_ATTRIB instrument pushed two takes a frame, misaligned 2:1 — with the deduplicated instrument every headline regenerates and the storm is ONE population, 97.2% doll d2+d3 (dd75).',
'7da3\'s "the staggered letter break at 1.7-2.2x10^6": REFUTED at rtf 100 (crest 342/366, N-flat, a 660-s beat) — corrected break ≈ 6x10^5 (7da3).',
'917c\'s stagger configuration as the locals\' cure: B13 armed 0/64 vs off 60/64 and all 13 armed digests change — killed; the cure goes to the birth program (c840).',
'1051\'s dossier arithmetic ("≈123" storm; "100% in-situ legal"): the flown hybrid delete gives 131 max (the Moon-corrected ≈134 candidate wins; the script\'s proportional 83.5 refuted) and in-situ legal = 200/233 = 85.8% with the quarter spared 75/75 by the tide bound (1a46 + checkers).',
'The SCAN_BACKLOG count cap as a fence ("about 10 KB each"): measured 1.94 MB/scan at 3x10^4, 7.36 at 10^5, 11.3 MB marginal (51b7) and 12.7 MB pinned (e181) — a 2,048-count cap licenses 5.6-26 GB and never engages before the ruin; the fence must count pinned BYTES at capture and answer-or-expire (51b7; e181; 527a; b911).',
'd839\'s "the per-body memory wall is a constant" as a burn-mode headline: coast-and-history-terms only — burn resident memory ratchets unbounded in the mint channel past the SOI switch (d839\'s own checker; 4447).',
]

# ------------------------------------------------------------ open directions
OPEN_DIRECTIONS = [
"(Macro, kicks per body ~10^3) Land the Binet cone tier behind the wired seam (universe.rs:469): it deletes BOTH O(N) walks — capture 2.15-6.02 h/era and the 4.2-4.4 µs/BODY answers — from the 830-1,030x ledger; the ask is O(k) with the width derived. The named first flight is the rank census (9ed1's en=178 encounters' partner ranks along the orbit; k ≈ 16-17 at 10^6 per coorbital-cert) (b57f).",
"(Macro, kicks per body ~10^3) The kick comb at 45.3-45.9 µs/kick against the scoreboard's ~50 ns floor: the remaining ~918x is REPRESENTATION (the walk → kernels port), not more per-kick polishing of the banked class; the boundary comb deletion (-50% of stream events, 49.7/50.7%) is the cheapest first cut and buys 1.2x on the era wall plus halved alternation (a31c).",
"(Macro, live set ~10^2-10^3) Channel 2's view-side answer: scope WHAT is kept (bodies the view reads), not the margin — cone-wide keep at 10^6 bodies is ruin by arithmetic on 1,760 B/binding and 1.4·λ·(2·ld+330 s) unbounded in play time; the TTL fence alone leaves 1,457 MB at 419k gs; belongs to the retention design (b911; f80a).",
"(Micro, the freeze ~10-10^2) Two named arms on the answer channel: which path fires the bite (the 2048 cap vs a settle — 9ed1's en=178 object and a0a1's 45-s draws disagree), and the structural fix for the root pull (canonical bindings in capture — the reach pull buys nothing measurable, offenders 10^7 ticks out) (a0a1; 4063).",
"(Plane smoothness, the p99) The adoption freeze: ES_STAGGER_GS and the TTL fence are both LAW CHANGES owing one digest re-freeze — together they delete the kick-comb freeze (30x) and the scan channel; unfreezing them is one rung on the merged corpus (8365; 9ed1; e181).",
"(Macro, live set) The split's seed ensemble at 5x10^4 with L measured per flight (the ON quiet-region cut separates L(seed) from B/8 for free) before any 10^9 adoption arithmetic — the share law underpredicts ~23% at the second rung and seed 3 fails the bands (3eb3 checker; 88e9 checker).",
"(Prune horizons — parked by the board below 2x until E9) The per-reader oldest at the first REAL far doll: E9's far-system wiring, then re-fly 1b3f's rule — the pin (+9.2 MB/body at 4 ly) is the honest simulation until then, and the first binding soundness test needs exactly that far doll (4a71; 1b3f).",
"(Evidence) The 10^6 gate rung re-measured on the M1 with the 6-line Linux instrument port folded in (cfg-gated VmHWM — the ladder's only instrument is macOS-only on main): F1's zero-lag clause reads 0.000 on the M1 rows and 1.448 s worst lag on the lab, 2,346 MB / 86.8 s; the integrator re-measures (03f4).",
]

# ------------------------------------------------------------- contradictions
CONTRADICTIONS = [
"F1's zero-lag clause at the 10^6 gate rung: the M1 rows read 0.000 lag, the Linux lab reads worst lag 1.448 s (one frame behind) on the same shipped bits + the disclosed instrument port — a machine discrepancy, unresolved until the M1 re-measure (03f4).",
"88e9's share law vs 3eb3's seed-3 arm at 5x10^4 (stream ratio 1.447 against the [1.73,2.11] band; locals seed-wandering 1,466→1,832): unresolved — the per-flight L measurement is the named closure (88e9; 3eb3 checker).",
]

# --------------------------------------------------- completions for Runs lines
# (the run-line completions live inside build_runs, below)
MY_RUN_LINE = ("- 20261020-2158-q-compile-nladder-e7d0 (awaiting grade): the page compiled back under budget — "
               "current best 15 lines, every run one line (100 kept of 186 duplicate lines), grades refreshed from the branches, "
               "15 mid-sentence run lines completed from their own dossiers/entries; no supported number lost (30/30 sample).")


def grade_of(rid):
    r = subprocess.run(["git", "log", "-1", "--format=%s", f"origin/claude/lab-{rid}"],
                       capture_output=True, text=True)
    m = re.search(r"Grade: (\w+)", r.stdout)
    return m.group(1) if m else None


def refresh_grade(line, rid):
    """Refresh any 'awaiting grade'/'this run' token from the run's branch."""
    g = grade_of(rid)
    if g not in ("gold", "silver"):
        return line
    if re.search(r"\((gold|silver)", line):
        return line  # already graded on the page
    out = line.replace("awaiting grade", g, 1)
    out = out.replace("(this run)", f"({g})", 1)
    if out == line:  # no grade token at all: "- <id>: claim"
        out = re.sub(r"^(- \S+):", rf"\1 ({g}):", line, count=1)
    # normalize the old page's append artifacts: "(this run, silver)" reads
    # wrong on a compiled page; the id itself says when it was a second author
    if "-second-" in rid:
        out = out.replace("(this run, ", "(second author, ", 1)
    else:
        out = re.sub(r"\(this run, ", "(", out, count=1)
    return out


def build_runs(old_text):
    # The old page leaves these run lines mid-sentence (re-appends kept only
    # their truncated first fragment); each completion is grounded in that
    # run's own branch dossier (git show origin/claude/lab-<id>) or its own
    # entry text on the old page. No other line is reworded.
    COMPLETIONS = {
        "20261016-1319-system-4fa8": "- 20261016-1319-system-4fa8 (silver [checker]): the comb is the anchor's artifact — ES_CHAIN+birth spread retires it (334→52, p99 136→24, -11% engine ms, zero steady-state rate); chaining alone inert; ES_LOCAL_PHASE equal-trade, beaten on parsimony and CPU.",
        "20261016-0213-fermi-1a1c": "- 20261016-0213-fermi-1a1c (silver): the assembled 10^9 budget on merged main — first engine-side breaker ≈ 8x10^4 bodies (the unstaggered first-kick wave's true peak 487 events violates F1's 12-ms letter at 10^5; \"the wave holds at 3x10^5\" was the budget cap hiding it); throughput break ≈ 1.0x10^6, memory 1.3-1.6x10^6.",
        "20261016-0346-spacex-917c": "- 20261016-0346-spacex-917c (silver): staggered wave flown budget-free at 10^5 and 3x10^5 — the belt's frame peak collapses 28x (994→35 events) and sinks below the locals' 334-452 storms; the staggered-break ~1.4x10^6 is not findable and the wave stops binding at 3x10^5.",
        "20261018-0543-spacex-7fcf": "- 20261018-0543-spacex-7fcf (gold): the composed law's doll-born drift debt flown and empty — median 5.5e-11 at 11,000 gs (424x under OFF's 2.31e-5, flat in horizon), the spared tail bit-identical to chain+stagger's, kicks -89% at the worst horizon.",
        "20261018-1126-inversion-7581": "- 20261018-1126-inversion-7581 (gold): the composed law on the crowd — cures the formation's frame ruin (max 1,013→28 at 10^3, over 68→0), but the transfer is the delete's alone: the de-phase converts the standing 8-frame beat into uniform O(K) load (6.2x sim-time starvation at 10^4); never ship a de-phase without the delete at crowd scale.",
        "20261016-0023-quant-404b": "- 20261016-0023-quant-404b (silver): the birth rail split — plan pass 32.5-33.5 µs/body (76-78% of the 42-44 µs rail; draw+add_body 9.3-9.7), flat in N from 10^4 to 3x10^5, seed-stable.",
        "20261016-0117-library-cfe5": "- 20261016-0117-library-cfe5 (silver): the plan pass attributed — secondaries 30% of birth (the planets' exact states re-derived once per body), deleted digest-identically by a birth-only hoist (33→23 µs/body); the bulk of the rest is the per-body clock derivation.",
        "20261016-1319-fermi-1051": "- 20261016-1319-fermi-1051 (silver): one lever, not two — the comb and the stream are both 2^step_log2 events per P_D per body (2^7/P_Cinder = 3.32e-5 from shipped constants vs measured 3.55-4.62e-5; the Home doll 4.016 vs 4.02 measured); every arm past the post-wave memory wall 1.2-1.65x10^6, all buying the same 1.9-2.6x flyable N; the comb is 0.006% of the 10^9 stream.",
        "20261016-1637-dynamics-87fd": "- 20261016-1637-dynamics-87fd (silver): the cure judged on doll-born locals — ensembles innocent to 3e-5 of the seed band, but the median per-body drift triples-quadruples (|dE/E0| 2.0→7.4e-6 per 4,500 gs) and it is horizon-local: the arms cross at 6,700 gs and OFF is worse at 9,000 (checker); the frozen gates are structurally blind to this law (every gate body root-doll).",
        "20261018-1717-inversion-d839": "- 20261018-1717-inversion-d839 (silver): memory through cadence waves is flat — the longest coast flight (45.5k gs at 3x10^4/10^5) crosses three belt-wide waves at +0.2-0.7%/wave, catalogue constant (30,076/100,076), the boundary wave costs 0 MB; the 20-s rung under-reads the steady rate ~11x; [checker] the burn at this horizon ratchets resident memory in the mint channel.",
        "20261019-1551-inversion-f80a": "- 20261019-1551-inversion-f80a (gold, two checkers): the fence inverted — channel 1 deleted, the ratchet survives on channel 2 to 1,457 MB at 419k gs (+3.32/+4.19 MB/1k); onset is the first kick wave (gt1 saturates 30,065 of 30,076 bodies), not 527a's ~95-130k slope-dominance; the fence buys ~15% horizon at 3x10^4.",
        "20261019-2339-inversion-1d47": "- 20261019-2339-inversion-1d47 (silver): the root burst is an over-strict read order; gating the root pull off is bits-clean (14/14 digests) and cuts max_ms 58-111x (867.9→15.0 ms at 10^5, 1,851.9→16.7 at 2x10^5) — but at the rungs where the deferral fires the canonical-cut digest is schedule-dependent (the checker bracket on the page).",
        "20261020-1503-taleb-a0a1": "- 20261020-1503-taleb-a0a1 (silver): capture 0.25-0.3 us/body ON the critical path (126 belt-wide walks, radial=ALL); answer 4.3 us/body 97% read, skip ceiling 99.8%; the guard is structurally closed (belt-wide scans exit via the 2048 cap or the TTL fence); the uncarried bound attacks both walks — later corrected by 23a6: the capture walk stands.",
        "20261020-1621-second-20261020-1503-taleb-a0a1-23a6": "- 20261020-1621-second-20261020-1503-taleb-a0a1-23a6 (second author on a0a1, gold): the dropped bound carried: exact (digest identity 1e5/3e5/3e3 + verify control), warm answer walk 0.041 us/body (~100x), one cold lump 3.86, settle 17x/8x cheaper; the capture walk and the lock stand.",
        "20261020-2102-inversion-03f4": "- 20261020-2102-inversion-03f4 (inversion, awaiting grade): the evidence frontier on shipped bits — the 10^6 gate rung reproduces on Linux (2,346 MB, 86.8 s build+flight, through a 6-line instrument port the tree lacks; F1's zero-lag clause does NOT reproduce there: worst lag 1.448 s); the wave the 20-s rung window cannot see costs 704.7/2,395.3 ms at 1e5/3e5.",
    }
    m = re.search(r"^## Runs\s*$", old_text, re.M)
    rest = old_text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    section = rest[:end.start()] if end else rest
    lines = [l for l in section.splitlines() if l.startswith("- ")]
    by_id = collections.OrderedDict()
    for l in lines:
        rid = re.match(r"^- (\d{8}-\d{4}-\S+?)([(:]|\s)", l).group(1)
        by_id.setdefault(rid, []).append(l)

    def clean_end(l):
        return l.rstrip().endswith((".", ")", "]", "*", "%"))

    chosen, n_graded_refreshed = [], 0
    for rid, ls in by_id.items():
        if rid in COMPLETIONS:
            chosen.append((rid, COMPLETIONS[rid]))
            continue
        graded = [l for l in ls if re.search(r"\((gold|silver)", l)]
        pool = graded if graded else ls
        clean = [l for l in pool if clean_end(l)] or pool
        pick = max(clean, key=len)
        new = refresh_grade(pick, rid)
        if new != pick:
            n_graded_refreshed += 1
        chosen.append((rid, new))
    return chosen, len(lines), n_graded_refreshed

def assemble(runs):
    head = [
        "topic: nladder",
        "status: open",
        "closed-by:",
        "valid-while:",
        f"updated: {RUN_ID}",
        "",
        "",
        "# The N ladder: 28 live bodies toward 10⁹",
        "",
        "## Current best",
        "",
    ]
    cb = CURRENT_BEST.split("\n")
    body = head + cb + [""] + ["## Refuted", ""]
    body += [f"- {r}" for r in REFUTED] + [""] + ["## Open directions", ""]
    body += [f"{i+1}. {d}" for i, d in enumerate(OPEN_DIRECTIONS)] + [""] + ["## Contradictions", ""]
    body += [f"- {c}" for c in CONTRADICTIONS] + [""] + ["## Runs", ""]
    body += [l for _, l in runs] + [MY_RUN_LINE]
    return "\n".join(body) + "\n"


# --------------------------------------------------------------------- audits
SAMPLE = ["27.9k", "4.889e-5", "77.24", "45.3-45.9", "8.6 µs/boundary", "40.6 ms",
          "1,273.5", "4.2-4.4 µs", "299,715", "8eecf1fa", "0.041", "97.55%",
          "0.053-0.399", "27.4 ns", "12.75 h", "69.75 s", "830-1,030x", "0.0526",
          "(K+38)", "16.8x", "635 MB", "0.15 KB/kick", "1,295 B", "1,760 B",
          "1,457 MB", "560,764", "42.8", "2,302.5", "9.2 MB/body", "1.448"]


def budget_by_wiki_py(text):
    """lab/wiki.py index's own counting: (total lines, current-best non-blank)."""
    total = len(text.splitlines())
    m = re.search(r"^## Runs\s*$", text, re.M)
    no_runs = text[:m.start()] + (text[m.end():] if False else "")
    # replicate split_runs: page without Runs section
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    no_runs = text[:m.start()] + (rest[end.start():] if end else "")
    best = no_runs.split("## Current best", 1)[-1].split("\n## ", 1)[0]
    best_lines = len([l for l in best.splitlines() if l.strip()])
    return total, best_lines


def main():
    old = open(OLD_PAGE, encoding="utf-8").read()
    runs, old_run_lines, refreshed = build_runs(old)
    page = assemble(runs)

    os.makedirs(os.path.dirname(OUT_PAGE), exist_ok=True)
    open(OUT_PAGE, "w", encoding="utf-8").write(page)

    report, fail = [], 1
    total, best = budget_by_wiki_py(page)
    report.append(f"budget: {total} total lines (cap 300), current best {best} non-blank (cap 15)")
    if total > 300 or best > 15:
        fail = 2
    if not (len(OPEN_DIRECTIONS) <= 8):
        fail = 2

    old_ids = {re.match(r"^- (\d{8}-\d{4}-\S+?)([(:]|\s)", l).group(1)
               for l in old.split("## Runs", 1)[1].splitlines() if l.startswith("- ")}
    new_ids = {rid for rid, _ in runs}
    report.append(f"runs: {old_run_lines} old lines over {len(old_ids)} distinct ids -> "
                  f"{len(new_ids)} kept one-per-id (+ this run's own line); "
                  f"{refreshed} grade tokens refreshed from branches")
    if old_ids - new_ids:
        report.append(f"LOST RUN IDS: {sorted(old_ids - new_ids)}")
        fail = 2

    missing = [t for t in SAMPLE if t not in page]
    report.append(f"number sample: {len(SAMPLE) - len(missing)}/{len(SAMPLE)} present in the new page"
                  + (f"; MISSING {missing}" if missing else ""))
    if missing:
        fail = 2

    n_ref = len(REFUTED)
    report.append(f"sections: {len(CURRENT_BEST.splitlines())} best lines, {n_ref} refuted, "
                  f"{len(OPEN_DIRECTIONS)} open directions, {len(CONTRADICTIONS)} contradictions")
    print("\n".join(report))
    json.dump({"total_lines": total, "best_lines": best, "old_run_lines": old_run_lines,
               "distinct_ids": len(old_ids), "kept": len(new_ids), "refreshed": refreshed,
               "sample_ok": len(SAMPLE) - len(missing), "sample_n": len(SAMPLE),
               "refuted": n_ref, "bytes": len(page.encode())},
              open(os.path.join(OUT_DIR, "compile-report.json"), "w"), indent=1)
    sys.exit(0 if fail == 1 else 2)


if __name__ == "__main__":
    main()
