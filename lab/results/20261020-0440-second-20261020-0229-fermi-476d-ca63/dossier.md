# Dossier — 20261020-0440-second-20261020-0229-fermi-476d-ca63 (second author on 476d)

## Claim

The checker's named gold experiment is flown whole, and it splits 476d's finding: the crest law
**is** adoptable re-anchored on game-time — the burst's onset_gs is locked to 13,107–13,270 gs
across rungs, replicates and a 4× cost regime (idle vs load-16: medians differ by **1 gs at 1e5
and 9 gs at 2e5**, while its frame index drifts 449→1,393), width 712–842 gs, arrivals
**0.977–1.038 events/body K-flat and load-flat**, per-event over-budget cost mild within a regime
(+6.5%/doubling idle, +3.8% load; load multiplier 3.97–4.07×, K-uniform) — but the tail's identity
**dies by deletion**: the TTL fence does NOT delete it (fence 1e5 tail 3,050 ms vs no-fence 2,226,
1.37×; the 2e5 fence arm still shows 8,244 ms of tail), because the tail is **more arrivals** —
1.50/body extra events in gs [onset+1.5k, onset+20k), incl. 6–12 big wave-2 frames — not the
held-scan channel (which the fence does delete: held_max 274 vs 1,867, end RSS 547 vs 1,494 MB at
1e5; 1,050 vs 2,758 MB at 2e5). The crest exponent is regime-stable but not a settled power law:
α(1e5→2e5) idle 1.110 [0.810..1.179] vs load 1.029 [0.915..1.308] (bands overlap) while
α(2e5→3e5) idle 1.527 [1.427..1.632] — disjoint: the super-linearity carrier is the per-event
cost, which steepens (+6.5% → +26% per doubling), so no single exponent composes to 1e9.

## Bottleneck

Board item 1 (bodies: 28 against 1e9) and smoothness. 2d26's coverage table decides the wave
exits and prices the stagger; 476d (silver) killed its ×2.37 unit but left every substitute
constant single-regime. This run measures the load dimension (the checker's "what the author
missed") and re-anchors the wave on game-time with per-frame event counts, so the exit ranking
now stands on quantities that do not move with the schedule. What it deletes: any tail-anchored
exit reasoning (the tail is arrivals — only the stagger touches it), and any single-α 1e9
composition (the crest floor at 1e9 is 13 h of arrival work at flat cost, open above).

## Evidence (all: shipped `nladder` burn scene, seed 1, rtf 2000, 12 ms, this box; instrument =
print-only per-frame CSV with a presented-game-time column + an env-gated TTL fence, both in
`work/patch.diff`; engine behaviour identical when the env is unset; 14 matrix flights + 2
disclosed calibrations + 7 shipped-binary anchor flights, `work/flights/`)

Per-flight and per-regime tables print from `python3 work/gs_analysis.py` after `regen.sh`
(build + flights are idempotent; full re-flight ≈ 13 min, cached ≈ 1 min):

- **Game-time lock (P1 held).** onset_gs (events-argmax over 1,500-gs windows; the ms-based
  onset is unusable under load — it fires on contention noise at gs 137): idle 1e5
  13,136–13,170 (n=3), idle 2e5 13,133–13,170 (n=3), idle 3e5 13,133 (n=1), load 1e5
  13,127–13,270 (n=3), load 2e5 13,107–13,203 (n=3). Regime shift of medians: 1 gs (1e5),
  9 gs (2e5). Frames-to-onset: 449–501 idle vs 1,150–1,523 load. Width (central 90% of window
  events): 712–842 gs everywhere. 2d26's premise resolves: onset IS game-time-locked; the frame
  index is set by load through the lag, exactly as its falsifier demanded.
- **Flat arrivals (P2 held).** Crest-window events/body: 0.977–0.980 (idle 1e5), 0.992–0.994
  (idle 2e5), 1.009 (idle 3e5), 1.034–1.038 (load 1e5), 1.017–1.021 (load 2e5). Regime shift
  ≤ 0.055. (476d's "arrivals fall 1.26→1.02" was indeed the window artifact; the checker's
  crest-window numbers are confirmed on two regimes.)
- **Crest ms and exponent (P3 held at 1e5→2e5; not a settled power law).** Crest excess:
  idle 4,617–5,486 / 9,621–10,455 / 18,647 ms at 1e5/2e5/3e5; load 17,476–20,206 /
  38,096–43,271 ms. α(1e5→2e5): idle 1.110 [0.810..1.179], load 1.029 [0.915..1.308] — bands
  overlap (|Δα|=0.08). α(2e5→3e5) idle 1.527 [1.427..1.632]: disjoint from 1e5→2e5 — the
  exponent is band-stable across regimes at a fixed rung pair, not across rungs. The mechanism
  (per-frame counts): µs/event 47.5→50.5→61.6 idle (+6.5%, then +26% per doubling; same-rung
  spread ±9%) and 193.2→200.6 load (+3.8%); the load multiplier is 4.07×/3.97× (K-uniform,
  which is why α carries across regimes). Arrivals carry no super-linearity; cost carries all
  of it and steepens with rung.
- **The tail is arrivals, not the scan channel (P4 failed on its letter; K4 fired — and killed
  the attribution, not the crest law).** Fence arm (idle, TTL=16 gs): 1e5 tail 3,050 ms vs
  no-fence idle median 2,226 (1.37×, kill bar >0.25×) with the memory channel verifiably gone
  (held_max 274 vs 1,867; RSS 547 vs 1,494 MB); 2e5 fence s17 (1,050 MB, the no-fence twin is
  unflightable at 2 GB — 476d's 2,758 MB) still shows 8,244 ms of tail. Identity of the tail:
  the tail window [onset+1.5k, onset+20k gs) carries 1.515–1.530 events/body at 1e5 and
  1.264–1.280 at 2e5, in 6–12 big frames (60–200k events) plus 81–214 over-frames — arrival
  waves 2+, on the same game-time anchor (same count with the fence on: 1.495/body). 476d's
  era/shape match to 7b6f's scan channel was coincidence — its own hedge ("the era/shape match,
  not the deletion") is now resolved by deletion.
- **The fence is not measurement-neutral.** Crest with fence: 6,466 vs 4,651 ms at 1e5 (+39%;
  per-event 65.4 vs 47.5 µs), 10,462 vs 10,039 at 2e5 (+4%). Likely re-mint churn (an expired
  scan is re-minted on the body's next capture, defeating the held-reuse; one probe away — not
  flown here). Any future fence measurement must price this.
- **Coverage, honest bars (the demoted table).** Full-ish-window coverage(1e5) idle
  0.235–0.307 (n=3); load windows are partial (0.201–0.441, biased high, disclosed).
  Coverage(2e5): load full-window 0.079–0.109, fence 0.136, idle partial 0.188–0.214 (tail
  missing — biased high): span **0.08–0.21**. 3e5: crest-only 0.048. The ebb is schedule-bound
  exactly as the checker said: 1,852–2,080 ms idle (K-flat, 2d26's ~2,046) vs 5,227–8,564 ms
  at load. Composition: crest(1e9) = 1e9 arrivals × cost; at flat 47.5 µs that is **13.2 h per
  wave minimum** (matches 476d's 32 h at α≈1.11), open above because the cost steepens — no
  single-α number is adoptable. Every exit conclusion survives: prepay and amortize are deader
  than 2d26 priced (coverage → 0), and both the crest and the tail need the stagger (they are
  the same phenomenon: arrivals).
- **Reproduction anchors.** Shipped-binary flights (work/shipanchor/, the accident disclosed
  below): 1e5 max 817.4/p99 160.9/over 108 vs 2d26's 812.6/160.5/108. My patched idle 1e5:
  crest 4,617–5,486 vs 476d's 4,568–4,633; tail 1,975–2,379 vs 1,940–2,019; ebb 1,852–2,080
  vs 2,050–2,098; 3e5 max 2,854 (476d) — crest-window 3e5 µs/ev 61.6 consistent with cc9d's
  49.8–52.7 at 2e5.

Commands: `regen.sh` (≈1 min cached, ≈13 min full re-flight) → `work/gs_analysis.py` prints
every number above; predictions are scored in its "prediction verdicts" block.

## Predictions

`predictions.md` written after two disclosed calibrations (1e5 idle + 1e5 load-16, which also
forced the events-channel onset before any decisive flight) and before the 15-flight matrix.
Scored: **P1, P2, P3 (incl. held-out 3e5 α(1e5→3e5)=1.264 ∈ [1.05,1.40]), P5 held.**
**P4 failed on its letter and fired its kill bar K4** (fence tail 1.37× > 0.25×; held_max 274 >
50) — which kills the tail=scan-channel attribution, not the crest law; the fence's crest
inflation (+39% at 1e5) also breached P4's "crest within [0.7,1.4]×" upper edge exactly. K1–K3,
K5 did not fire. One registered hazard materialised: load-2e5 flights peaked at 3.2–3.8 GB RSS
(the memory cap was not enforced on this box; one replicate died to it mid-run but completed on
the rerun; the fence twin at 2e5 flew at 1,050 MB — the fence's memory value is itself
confirmed).

## What would make it wrong

- The events-argmax onset is a window choice (1,500 gs, grid 100): a wider wave-2 could drag
  the argmax if waves merged; they do not here (wave 2 sits ≥1.5 k-gs past onset at both rungs
  and regimes), but a scene with closer waves would need the window re-registered.
- The tail identity is measured at 1e5/2e5 on this scene only; a rung where the scan channel
  outgrows arrivals (7b6f's guard at 2e5 was memory, 20.6k gs) could re-add a scan-cost tail on
  top — my load-2e5 tails (28–36 s over-budget) are load-inflated arrivals, but I cannot
  exclude a scan contribution there from ms alone (the fence arm pins it at idle only).
- α to 1e9: the cost steepening (+6.5%→+26%/doubling) is 3 rungs, one flight at 3e5, and the
  1e5 replicate spread on µs/ev is ±9% — the crest floor (13 h) is safe, the ceiling is not
  claimed. The +39% fence-crest mechanism is named, not measured.

## Cost of adoption

None in code (print-only instrument + env-gated fence, off = shipped). What it reprices: (a) the
wave's exit table is re-anchored on gs — crest and tail are ONE arrival phenomenon (≈2.3–2.5
events/body over 20 k-gs), so the stagger targets the whole wave, and nothing else will;
(b) no single-α 1e9 crest number may be quoted — floor 13 h/wave at flat cost, open above;
(c) fence-based measurement must carry the +4–39% schedule caveat; (d) coverage keeps its
demotion, now with measured bars (0.08–0.21 at 2e5) and a schedule-bound ebb.

## Fit with PRINCIPLES

"Measure before claiming, and never strawman": the load dimension is now measured on both
sides of every constant. "A failed expectation is not automatically a failed method" (H0183):
P4's failure is the result — it deletes an attribution, not the law. "Fat tails … the wave IS
the tail": 3 flights per rung per regime is now the floor, and the same-rung spread it buys
(±9% on cost, 34 gs on onset) is what separates law from draw. "Error type over error size":
the correction is which channel carries the exponent (arrivals flat, cost steepening), not the
third decimal.

## The lens

The second-author lens (make the record regenerate, run the named experiment) forced the
events-channel onset: the gold experiment as literally specified (gs-anchored windows) is not
flyable under load with an ms-anchored detector — contention noise fires it at gs 137. What
the lens may have missed: the fence's crest inflation is a schedule effect I report but do not
decompose (the re-mint churn hypothesis needs a mints counter, one probe); and my load-2e5 arms
exceeded the 2 GB cap (3.2–3.8 GB) because the cap was not enforced — the numbers stand (timing
is not memory-dependent below the guard), but a stricter box would have voided those replicates.

## Process note (disclosed)

Three matrix launches wrote their outputs to a stray `lab/lab/` path (the session's async cwd
differs from the repo root) and one flew a stale unpatched binary from the session's ambient
`CARGO_TARGET_DIR` (those 7 flights are kept as shipped-binary anchors in `work/shipanchor/`;
their max/p99/over reproduce 2d26). All matrix numbers in this dossier come from the patched
binary, verified by the CSV columns' presence; `fly_matrix.sh` now pins the absolute root and
the target dir.
