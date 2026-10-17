# Dossier — 20261017-2038-second-20261017-1918-fermi-b77d-1fcf (second author on fermi-b77d)

**Claim.** The checker's named gold experiment, done, **refutes the checker's own superlinear
pin and b77d's 475 B/candidate with one closed-form law measured in real bytes at capture:
the held scan's pin is the candidates `Vec` itself — `size_of::<(usize, Binding, Scalar)>()`
= **224 B** (Binding 192) — times the window's candidate count, pooled fit **226 B × C
(r² 0.974)**, flat across a decade of scenes (C = 1,028→8,156), quiet and loaded. Every
larger number in the record (b77d's 475 B/cand, 7bd9's 171 kB→2 MB/scan, the checker's
2.2–2.5 kB/entry at K=2,400) is a window-slope artifact: births and dead-candidate `Entry`
retention are collinear with held growth at the fixed 0.096/game-s arrival, exactly the trap
b8e2 named for 4b8c/7bd9's pins. The count-fence's byte price is therefore 2,048 × 224 B × C
≈ 0.46 GB per 1,000 window candidates — **8 GB at C ≈ 1.7×10⁴ on the capture term alone**
(retained `Entry`s of candidates dying while held add a phase-dependent ~1–5× tail, so the
prudent fence budget is the measured retained growth, ~0.5–0.7 kB × C: bust at ~5–8×10³) —
and the fence must still count bytes at capture, because 224 B is `sizeof(Binding)`'s
accident, not a law. In the paced player loop the crowd K ≤ 4×10³ freezes and pins; at
K = 10⁴ the loop never reaches the FLOW — the warm per-frame view gather alone costs
74 ms p50 (7–11 fps wall) — so the crowd's first wall at 10⁴ is the view, not the queue.

**Bottleneck.** Board memory item: the fence's unit and size. This closes the page's
direction-3 rung (the paced crowd K = 2×10³–10⁴, quiet vs loaded, the real player loop) and
the checker's "one experiment to gold" (the pin counted in real bytes at capture): the
byte-fence budget is now measured, not modeled — one counter (candidates × 224 B at capture,
or the allocation delta itself) plus the page's direction-1 game-s-cadence drop for the
retention tail.

**Evidence** (Linux/x86, 8 vCPU shared, seed 1, threads 1, coast, rtf 100, 12 ms budget,
≤ 50 s per flight; `crates/universe/examples/flowcrowd.rs` via `work/patch.diff` —
print-only, engine untouched: a counting GlobalAlloc (live bytes + live allocations per
frame), 60 fps pacing, one warm `gather_cached` per frame, per-frame probe line; every log
head records its loadavg; arms K ∈ {1000, 1600, 2400, 4000, 10000} × {quiet, 7-spinner
loaded} paced, plus K ∈ {4000, 10000} unpaced/no-gather).

Whole-window pins (live-bytes slope ÷ held slope — the record's estimator) and the
**per-transition estimator** (live-byte delta across the exact frame where held +1 — churn
cannot alias into it):

| arm | loadavg | held_max | cat@trans | window kB/scan | **transition kB/scan** | **B/entry** |
|---|---|---|---|---|---|---|
| K1000l | 2.1→8 | 290 | 1,028 | 477 | **233** (p25 173, p75 277) | **227** |
| K1600q | 2.5 ambient | 356 | 1,586 | 859 | **439** | **277** |
| K1600l | 6.1 | 271 | 1,572 | 984 | **367** | **234** |
| K2400q | 5.6 amb. | 256 | 2,428 | 1,140 | **695** | **286** |
| K2400l | 8.5 | 22 | 2,230 | 11,455 | **498** | **224** |
| K4000q | 8.5 amb. | 11 | 3,461 | 26,787 | **994** | **287** |
| K4000u | 6.0 amb. | 68 | 3,850 | 12,252 | **1,005** | **261** |
| K10000u | 5.3 amb. | 3 | 8,156 | 77,137* | **1,846** | **226** |

*K10000u's window slope is birth-collinear (fleet still birthing, cat 7,959→8,437); its
per-transition deltas are the pin. The same collinearity explains every superlinear window
slope above: higher K → fewer presented game-s in 50 s → the window sits in the birth phase
(K4000q: cat 0→3,761 over its 11 scans ≈ 6.5 MB/scan of births aliased into 26.8).

- **The law:** transition pins 226–287 B/entry on every arm; pooled linear fit
  **226 B × C, r² 0.974** over C = 1,028–8,156; `size_of::<(usize, Binding, Scalar)>()` =
  **224 B** printed by the probe — the pin is the candidates `Vec`, one row per candidate,
  no superlinear term, no load term (quiet 234–286 vs loaded 224–287 at the same K).
- **The artifact:** window slopes grow with K exactly as the checker's RSS slopes did
  (their K=2,400: 5–6 MB/scan ≈ my K2400l 11.5 MB / K2400q early 7.9 MB window slopes;
  7bd9's m1,600 ~2 MB likewise) — and my per-transition estimator shows the true pin there
  is 0.5–0.7 MB. b8e2's refuted-list already named the mechanism ("the raw slope is
  collinear with churn"); this run is the direct demonstration on the crowd family.
- **The retention tail (real, but not the capture's):** mid-flight window slopes exceed the
  transition pin by ~1–2× (K1600q: 828–986 kB vs 439; K2400q: 809–1,179 vs 695) — the
  `Arc<Entry>` of candidates that die while their scan is held [INFERENCE: anatomy;
  bytes measured, ownership inferred] — and the whole-flight K1000l slope 477 vs pin 233.
  The fence's budget must cover this tail: ~0.5–0.7 kB × C measured growth mid-flight.
- **The fence, measured:** 2,048 × 224 B × C = 0.46 GB per 1,000 candidates — ladder near
  set (C≈150): ~69 MB, safe; 8 GB at C ≈ 1.7×10⁴ (capture term) / ~5–8×10³ (retained
  growth). b77d's 8,500 (at 475 B) and the checker's ~2×10³ (at 2.2–2.5 kB) were both the
  artifact's two ends; the measured law sits between them and the fence conclusion
  (bound bytes, not count) is unchanged.
- **The paced loop (direction 3):** K=1,000 quiet drained (held_max 1), loaded froze at 405
  — 470f's bimodality; K ≥ 1,600 froze in every paced arm that presented ≥ 130 game-s
  (quiet, ambient 2.5–5.6); K=4,000 loaded presented 25.8 game-s (gather p50 37.9 ms) and
  never accumulated (crawl starves arrivals, not the drain); **K=10⁴ presented 5–10 game-s:
  the warm gather costs 66.8–74.1 ms p50 (≈ 7 µs/member, linear in K) — the view is the
  crowd's first wall at 10⁴, before any FLOW exists.** Unpaced at 10⁴ the first three scans
  pin 1,846 kB each (226 B/entry at cat 8,156) — the law holds to the top of the range.
- Cross-instruments: arrival 0.092–0.097 held/game-s everywhere it froze (b77d 0.0966,
  7bd9 0.096, b8e2 0.053–0.064 at plane scenes); window-slope K1000l 379 kB against b77d's
  RSS 403–514; RSS slope vs alloc slope in-arm agree within 3–13 % (K2400l 11,444 vs
  11,455 kB/scan).

**Commands** (repo root; ≈ 12 min: build 15 s + 12 flights ≤ 55 s + analysis):
```
lab/results/20261017-2038-second-20261017-1918-fermi-b77d-1fcf/regen.sh
python3 lab/results/20261017-2038-second-20261017-1918-fermi-b77d-1fcf/analyze.py \
    lab/results/20261017-2038-second-20261017-1918-fermi-b77d-1fcf/flights
```
`regen.sh` applies `work/patch.diff`, builds, flies all twelve arms (load arms bring their
own 7 spinners on cores 1–7) and prints every table above. Disclosure: (a) ten of the committed
`flights/*.log` were flown with the identical instrument minus the two-line `sizeof` banner
the final patch adds (verified by a post-hoc 8 s smoke flight; the banner prints before the
build and measures nothing). A four-arm smoke regen through `flights.sh` (fresh flights
K1000q/K1000l/K4000u/K10000u on a busier box) reproduced the transition law at **221 B × C
(r² 0.990)** — the law replicates on fresh flights; the window slopes do not (they are load-
and phase-owned — that is the result); each log head records its loadavg.

**Predictions** (`predictions.md`, pre-registered). P1 held (whole-flight 477 kB at K=1,000, in b77d's 403–514 band). **P2 and P3 refuted by my own cleaner estimator**: the
superlinear per-entry growth I predicted (≥ 15 kB/entry at 10⁴) is the window-slope
artifact; the transition pin is flat 226 B/entry at 10⁴. P4 split: quiet-freeze and
pin-load-independence held; my "gather ≤ 5 ms at K ≤ 4×10³" was refuted (6.7–27.5 ms, 74 at
10⁴ — the rung's second finding). P5: the fence bust measured at ~1.7×10⁴ (capture term)
/ ~5–8×10³ (retained), between both prior readings — the checker's ~2×10³ was the
artifact's high end, b77d's 8,500 its low end.

**What would make it wrong.** (1) The transition estimator samples the frame after capture;
allocations that outlive exactly one frame (the frame's own churn, median ~40–280 allocs)
ride along — the byte medians close onto 224 B × C within 0–30 %, so the law stands, but a
`Held::capture`-scoped probe would nail the last 30 %. (2) The retention tail is measured
as window-minus-transition, not separately instrumented. (3) `candidates ≈ catalogue_live`
is still a proxy (the two agree at crowd scale where the window holds the whole doll;
b77d's A2 windows already showed the proxy swings ~2× on spread scenes). (4) One seed, one
scene family (the dissolving-battle crowd); the law is `sizeof`-driven so it should be
scene-free, but the retention tail is not.

**Cost of adoption.** One counter: at capture, add `candidates.len() × 224` (or the
allocation delta) to a held-bytes budget, answer-or-drop past it — composes with the page's
direction-1 game-s-cadence drop, which is what actually kills the retention tail.

**PRINCIPLES.** "A failed expectation is not automatically a failed method: diagnose which
one broke" (H0183) — my own P2/P3 died to the cleaner estimator and the diagnosis
(collinearity) reconciles three runs' numbers. "Agreement is not independence: several
results from one harness share its bugs" (How to think here) — four runs' window slopes
shared the one aliasing bug. "Measure before claiming, and never strawman" — the fence's
budget is now a measurement. "It's a game … error type over error size" (2): the fence
bounds bytes, the exact quantity at stake, not a count.

**The lens.** The second-author lens starts from the run's own scripts and the checker's
named experiment; what it price-blind spots is the structural cure's cost (dropping scans
at a game-s cadence changes when answers enter the hash chain — direction 1's canonical
schedule) and the view's 7 µs/member gather, which this rung met at 10⁴ but does not fix.
