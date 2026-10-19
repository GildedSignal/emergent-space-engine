# 20261019-1452-spacex-396d — the player-seam flight: what crossing a population's radial hull costs

## Claim

The player-seam (the unflown arm two pages name) is flown at K = 10⁴ and 3×10⁴: crossing the belt turns **every** player scan inside the belt's *registered radial hull* (1.6–5.2 AU — the e-smeared `[rmin, rmax]` registration, ~2.5× wider than the 2–3 AU density band) into a full-universe walk (`cands` = N − locals, capture 0.9–2.0 ms at 10⁴ / 4.3–9.1 ms at 3×10⁴, ∝N at 167→214 ns a body), yet **no frame goes over from the seam at these rungs** — the over-budget frames of both flights are the root doll's boundary wave, and the worst frame (42.36 ms) is 4447's known burn tail (42.5) — while the walk zone's held scans and the memory ratchet walk together to the guard (1,400/1,300 MB) with a **K-independent** late slope of ~2.1–2.2 MB per held scan, which excludes the walks' own candidate pins (3× more candidates at 3×10⁴, same slope) as the ratchet's bytes.

## Bottleneck

Board item 1 ("bodies in the flyable engine: which term breaks first as the plane grows … measured on shipped code at 10³–10⁶"), in the one regime every census had avoided: the player inside a population's radial band (c439's domain note; promotion od 1: "the player-seam flight … stays unflown"). Expected gain: not a speedup — a measured law where there was an unflown gap: the seam's per-scan cost is N-proportional with the walk as the shipped fallback, so it is one of the ~10³-idiot-index terms at 10⁹ (N reads to find ~O(1) real neighbours), and its frame/memory verdict decides whether it is *the* term that breaks first in flight, or nothing.

## Evidence

All numbers from the two flights below (shipped code; the instrument is print-only and env-gated, `ES_SEAM_CENSUS` off = the shipped path unchanged; each flight ≤ 90 s wall here, on the shared 8-vCPU box).

- **The walks (the census, `logs/long-k1e4-burn.err`, `logs/long-k3e4-burn.err`):** 118 walks of 3,256 scans (10⁴) / 118 of 3,082 (3×10⁴), all in doll 0, none in Home's doll (2,095 scans, walk = 0 — the negative control holds). Walk zone: r = 1.62 → 5.17 AU over gs 45,247 → 103,580 (~59k game-s ≈ 1.7 octaves — the belt's registered hull: periapsis ≥ 1.2 AU, apoapsis ≤ 3/(1−0.4) = 5.0 AU). In the zone every scan bails (`candidates` = `None`) and the capture reads the whole universe: `cands` = 9,715 (10⁴, N = 10,028) and 29,715 (3×10⁴, N = 30,028) — every doll-0 body. Capture cost: 0.86–2.05 ms (10⁴) and 4.3–9.1 ms (3×10⁴) ⇒ **167 → 214 ns per walked body** (c439's binding_at law, on the walk).
- **Why the bail:** not the window's width (the player's own step keeps it ~0.02–0.09 AU) — the *registration's* width: every belt body registers the hull of its eccentric range (~10–20 bins each), so any window touching the hull's bins sums ~N bin-entries against the global `bodies/4 + 64` threshold. A 1-D radial index cannot cut a population at its own band once e > 0 smears the registration — the same wall b083/5f36 hit from the answer side.
- **The frames stay in budget at these rungs:** over-budget frames 74 (10⁴) / 80 (3×10⁴) of 297,840 / 160,380 late frames; their frame ids cluster at gs ≈ 140–150k in **both** arms (root-doll boundary wave; the belt's step-end events), outside the walk zone (gs 45–104k); the walk zone itself contains **zero** over-budget frames — p50 frame 0.024 ms leaves idle room, and the deferred answers (9,715 candidates each) drain there. Worst frame 42.36 ms at gs ≈ 18.5k, before any walk: 4447's known burn-mode worst (42.5 ms at the same K) — the instrument's control match.
- **Memory and held:** held_max 693 (10⁴) / 539 (3×10⁴); resident memory climbs monotonically to the guards (1,400 MB at gs 496k / 1,300 MB at gs 267k). Late-flight slope: (1398−202)/(692−156) = 2.23 MB per held scan (10⁴) and (1294−305)/(539−61) = 2.07 MB (3×10⁴) — **the same slope at 3× the candidates**, so the ratchet's bytes are not the walk candidates (which would scale 3×); this run's census thus *excludes the scan-answer channel as the owner of 4447's ratchet bytes* (their open attribution stands, now narrower), while confirming their held↔RSS coupling (their late "0.9→2.2 MB/held" compounding, here flat at its top).

Reproduce (≤ 5 min + two flights ≈ 3 min):

```
cargo build --release -p emergent-universe --example seam   # encounter.rs census + examples/seam.rs (work/patch.diff)
ES_SEAM_CENSUS=1 ES_SEAM_CAP_S=1500 ES_SEAM_RSS_MB=1400 $CARGO_TARGET_DIR/release/examples/seam 10000 burn 700000 100 12 \
  > logs/long-k1e4-burn.out 2> logs/long-k1e4-burn.err
ES_SEAM_CENSUS=1 ES_SEAM_CAP_S=1400 ES_SEAM_RSS_MB=1300 $CARGO_TARGET_DIR/release/examples/seam 30000 burn 40000 100 12 \
  > logs/long-k3e4-burn.out 2> logs/long-k3e4-burn.err
python3 analyze.py long-k1e4-burn && python3 analyze.py long-k3e4-burn
```

(`regen.sh` runs exactly this.)

## Predictions

`predictions.md` was written after the smoke arm's build, before these flights (never having read any long-flight output). Verdicts: **P1 held and extended** (the bail fires through the whole registered hull 1.6–5.2 AU, not just the 2–3 AU band — the e-smear, which I had not derived); **P2 held** (capture ∝N measured: 167/214 ns a body; the 12 ms frame line is crossed at ~6×10⁴ bodies *per capture* — but the capture is per player item, and the item interval h grows relativistically, thinning the tax); **P3 wrong on frames, half right on memory** (no seam-owned over frames at 10⁴/3×10⁴ — the answers drained into idle room; the held pins are real but their bytes are K-independent, so they are not the candidates); **P4 wrong** (neither frame nor memory broke *from the seam* at these rungs within 496k gs — the guard stops are the 4447 ratchet, which the census now excludes from the scan-answer channel); **P5 half-held** (the walks end at the hull's top ≈ 5.2 AU and the filter cuts again, near = 3–5, cands p50 3 — the seam is the hull's width, not a permanent tax; but it begins *before* the band and lasts ~2.5× the band's crossing time). The run's own kill criterion (walk = 0 through the crossing at every K) did not fire.

## What would make it wrong

- The two flights share the box with each other; load-elastic digits (ns_cap p50 under contention) could shift ±2×, but the walk counts, `cands` = N − locals, and the zone's span are census facts, not timings.
- The frame verdict is a *these-rungs* verdict: the answer cost per candidate (~4.4 µs, 604c's class) was not re-measured here; if it holds, one in-band answer at 10⁶ is ~4 s — the seam becomes frame ruin two rungs up, and my "no over frames" must not be quoted past 3×10⁴.
- The K-independent MB/held slope could be an artefact of both arms dying at the same guard; a longer-leash flight (or the per-reader `oldest` fix, 1b3f) could change the slope's late value, not the exclusion logic (candidates 3×, slope equal).
- The belt here is the ladder's own (a ∈ [2,3) AU, e Rayleigh 0.07); a cold population (e ≈ 0) registers ~1 bin and the seam collapses to it — the hull's width is the law, so a different belt geometry moves the zone's span exactly as its `[rmin, rmax]` does.

## Cost of adoption, and fit

Nothing to adopt: this is a measurement that closes a named gap (promotion od 1's unflown arm) and prices the shipped fallback. Design consequence for the record: the 1-D radial index is already defeated by e-smear at the population's own band — the cheap fix direction is not a better radial threshold (0552's local bail) but the second axis the record keeps arriving at (the phase/along-orbit axis of b083/5f36's 2D capability curve, one compare on a stored phase word), which cuts the *candidates*, not the bins. PRINCIPLES 32 ("symmetry is found, not given … change the representation before paying to simulate") and 33 ("a body resolves only the influences that are significant at its own scale") are the fit: the walk reads N bindings to resolve ~O(1) significant neighbours.

## The lens

SpaceX's order (question, delete, measure at the edges) chose the flight; the blind spot it left: I nearly priced only the bail-vs-cut verdict (the filter's letter) and would have missed that the *registration's* width, not the window's, sets the zone — that came from reading the census's r_au column against `ladder_ship`'s geometry. The lens also under-weighted the answer channel (deferred, idle-drained), which is why P3/P4 missed.
