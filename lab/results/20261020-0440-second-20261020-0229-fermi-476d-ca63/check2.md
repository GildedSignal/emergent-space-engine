Grade: gold

**Abstract.** Second blind check of ca63 (476d's named gold experiment, flown whole). Every dossier
number regenerates: fresh `gs_analysis.py` identical to regen.log; 17/17 matrix CSVs carry the gs
instrument, 7/7 shipanchor CSVs are unpatched and reproduce 2d26 (max 811.6–817.4 / over 108–109);
patch applies clean at base 5f7ce7a1; predictions (04:52:51) precede all 15 flights (04:59–05:17).
My four arms: fence-2e5 full-window still shows a 7,084 ms tail at 1.280 events/body with the memory
channel verifiably deleted (held 386, RSS 1,089 MB) — the tail-is-arrivals correction stands, hole
closed; onset_gs locks at 13,102 (rtf 400) and 13,129 (seed 2), two axes beyond the author's grid;
my own 3e5 draw (14,467 ms, 0.998/body, 48.3 µs/ev) confirms the "+26% steepening" was one draw
(α(2e5→3e5) draws {1.53, 0.92, 0.90}). Adoption cost: none in code. Page corrected: wave total
2.49–2.51 (not 2.56–2.57); crest-window constant flagged seed-bound.

## Reasons

**Reproduction.** The runner's regen exited 0; re-running `work/gs_analysis.py` reproduces every
regen.log line identically (all per-flight rows, medians, exponents, prediction verdicts). I
re-derived the tail identity independently of the author's script (own loader, same registered
windows): tail window carries 1.515–1.530 ev/body at 1e5 idle (fence-on 1.495 — same count), 1.264–1.280
at 2e5 (load arms fully covered; fence 1.264), in 6–7 big frames (9–36k events each) plus 87–224
over-frames. The dossier's "60–200k events" per big frame is wrong (it is the collective load:
top-7 sums 62.5k at 1e5, 155–173k at 2e5 — the page already corrects this, and the correction
regenerates). Provenance verified: all 17 patched-flight CSVs carry `gs`; all 7 shipanchor CSVs are
empty and their ladder lines match the dossier's anchors. `work/patch.diff` applies clean at the base
commit and rebuilds in 21 s; with the env unset the diff is print-only plus a default-55 s dial, so
"off = shipped" holds by code read.

**Predictions.** mtime order verified: calibrations 04:48–04:49 (disclosed in predictions.md),
predictions.md 04:52:51, decisive matrix 04:59:11–05:17:38, dossier 05:20:52. P1/P2/P3a/P5 hold as
scored; P3b (held-out 3e5) held on the author's draw and on mine (α(1e5→3e5)=1.135 with my 3e5).
P4 failed its letter and fired K4 — reported as the result, which is the honest reading: K4 kills
476d's tail-attribution (the checker-476d bracket itself hedged "the era/shape match, not the
deletion"), not the crest law. This is "a failed expectation is not automatically a failed method"
done right.

**Attack (four arms of my own; three outside the author's grid).**
1. *Fence-2e5, full tail window* (the author's s17 fence arm ended at gs 32,096, short of
   onset+20k — `covered: False`): with TTL=16 and the window fully covered (end_gs 48,248), the
   tail is still 7,084 ms carrying 1.280 ev/body in big frames at gs 27.7–28.9k, while the memory
   channel is verifiably deleted (held_max 386 vs 1,800–1,901; peak RSS 1,089 MB, under the 2 GB
   cap). The central claim survives its strongest form at the second rung.
2. *rtf 400 (play cadence — a regime axis the author never varied; they varied load only)*: onset_gs
   13,102, wave-1 totals unchanged (1.12/body across gs 12–16k, matching rtf 2000). The game-time
   lock holds on a third axis; the over-budget share amortizes, as the record already knows.
3. *Seed 2 (the author flew seed 1 only)*: onset_gs 13,129, wave eras identical (12–16k, 26–30k gs),
   wave totals similar (1.27/body in wave-1 bins) — but the fixed 1,500-gs crest window captures only
   0.49/body. So "crest 0.977–1.038 ev/body" is registration×seed-bound, not a law constant; the
   seed-stable objects are the eras and the per-wave totals. The claim's stated domain (seed 1,
   rtf 2000) is honest, and the page now carries the caveat.
4. *3e5 idle, fresh draw*: 14,467 ms, 0.998 ev/body, 48.3 µs/ev, onset_gs 13,170. Combined with the
   author's 18,647/61.6 and checker 1's 14,571/48.7, α(2e5→3e5) draws are {1.53, 0.92, 0.90}: the
   author's "disjoint band" and "+26%/doubling steepening" were single-draw artifacts, exactly as
   the author's own "≥3 flights per rung" floor predicts. The corrected reading — crest ≈ K-linear
   at flat ~48–50 µs/ev with ±22% draw noise, cost mildly rising at most — is what stands, and it
   strengthens "no single-α 1e9 composition" (the 13.2 h/wave floor at flat 47.5 µs arithmetic
   checks: 1e9 × 47.5 µs = 13.2 h).

**Novelty.** The wiki page and record held the opposite on the tail: 476d's entry says "the tail
does not need the stagger (the fence deletes it)". This run refutes that by deletion and re-prices
the stagger's target as the whole wave (crest + tail are one arrival phenomenon, ≈2.3–2.5/body over
20 k-gs). f80a/b911's channel work is the memory ratchet — a different question; no prior entry
claims the ms tail is wave-2 arrivals. The load dimension and the gs-anchored instrument are new.
The second-author pattern (flying the named gold experiment) is the designed workflow, and this one
changed the record's conclusion, not just its constants.

**Goal fit.** Board item 1 (bodies 28 vs 1e9) and smoothness. The exit table is re-anchored on
game-time (quantities that do not move with the schedule — PRINCIPLES: "Measure before claiming"),
a standing premise is shown wrong ("A failed expectation is not automatically a failed method",
H0183), and the correction is error-type, not decimal-polish ("types of errors and not just
errors"). Adoption cost: none in code (print-only instrument, env-gated fence, off = shipped).

**Page.** Faithful after checker 1's corrections; I verified those corrections regenerate
(independently for the 3e5 draw and the top-7 sums) and fixed one number that did not (wave total
2.56–2.57 → 2.49–2.51) plus added the seed-2 caveat in a checker2 bracket. Topic stays open: one
gold run agrees with... nothing else yet on this exact sentence — three gold runs are not present,
so no closure.

## What the author missed

- The crest-window arrivals constant (≈1.0/body) is seed-sensitive: at seed 2 the same registered
  window captures 0.49/body while the wave totals and eras stay put. The invariant object is the
  per-wave total, not the fixed-window integral — the page now says so.
- The 3e5 single flight carried two claims (α disjointness, cost steepening) that two further draws
  kill; the author's own ≥3-flight floor was not applied at the rung it was invoked on.
- The fence-2e5 tail window was left partially covered (their own analysis printed
  `covered: False`); one more second of flight would have closed it. I closed it: the claim holds.
- The dossier's "6–12 big frames (60–200k events)" overstated per-frame counts ~10× (collective,
  not per-frame); the dossier text still carries it, the page corrects it.
- Minor: tail over-frame range is 87–224, not 81–214 as stated; the wiki's "1e5 idle measures
  2.56–2.57" did not regenerate (2.49–2.51; corrected in place).
