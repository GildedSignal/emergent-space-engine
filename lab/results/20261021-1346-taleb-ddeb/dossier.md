# Dossier — 20261021-1346-taleb-ddeb

**Claim.** The fine-class census of the plane's belt (kick-cadence's open direction 1, the deletion's missing half): the desynchronised grid's belt headroom is **78×**, not the ~10³ of the board's sentence — 17.8% of the bodies (the resonance tail, Giant 3:1 dominant) pay 75% of the composed event bill, 41.0% sit in an unflown Hill bridge below the certificate's floor, and a belt born 0.15 AU higher dies outright (53.8% first-order, uncertifiable at any cadence).

**Bottleneck.** Board macro row 1 (kicks per body, ~10³ at stake): "the star's doll kicks every body on one grid, ~9,000 kicks per belt orbit; ... which bodies must stay fine (resonances, encounters) and what fraction they are". cbe6 (gold) named the census as the deletion's missing half: "the census sizes the rescue". This run sizes it: the rescue survives on the plane's own belt (first-order fraction exactly 0) but at ~10¹·⁹, an order below the hoped ~10³, and it sits on a placement cliff (the 2:1 zone starts 0.148 AU above the belt's edge).

**Evidence.** All numbers from `crates/universe/examples/beltcensus.rs` (new, this run's patch): calls the shipped `ladder_ship` belt arm verbatim (a uniform [2,3) AU at 2⁻⁸ root units, Rayleigh e σ=0.07 redrawn above 0.4, periapsis = a(1−e)) and the shipped `PLANETS` (Cinder 2⁻²¹ @ 0.390 AU, Home 2⁻¹⁸ @ 1.000, Giant 2⁻¹⁰ @ 5.194, e 0.05, periapsis 4.936). Classification per body, against cbe6/7076's measured floors: crossing → 256/own-orbit; first-order resonance zone (67be: uncertifiable at any cadence, no floor); q≥2 zone or e>0.23 (outside the certified e-draw) → 256; conjunction gap < 6.3 Hill (below cbe6's certified interior draws 6.3–8.8) → 64/Giant-period (conservative) or 16 (optimistic); else 16/Giant-period. Zone widths are the oracle side (pendulum model, Murray & Dermott ch. 8: δa/a = (j/k)√(16μe^q/3), order q via d'Alembert); floats explore, the counts decide. Both combs ×2 (the boundary rides every step lever, de7b); the anchor 9,000/belt-orbit is the board's own (≈ 2 combs × 4,479 doll-grid intervals at the median belt orbit).

Shipped belt, 999,702 bodies, seeds 1/2/3 (f_fine 0.1784/0.1793/0.1784 — ±0.1%):

| class | fraction | floor | share of the composed bill |
|---|---|---|---|
| certified belt (gap ≥ 6.3 Hill) | 41.1% | 16/Giant-period | **4%** |
| Hill bridge 4.1–6.3 Hill | 40.7% | 64 (unflown; 16 if the arm passes) | 21% |
| strong tide < 4.1 Hill | 0.26% | 64 | (in the 21%) |
| resonance zones (q ≥ 2) + e > 0.23 | 17.8% | 256/own-orbit | **75%** |
| first-order (uncertifiable) | **exactly 0** | none exists | — |

Zones by body count: Giant 3:1 = 9.4% of the belt (a_res 2.521 AU), 4:1 = 3.4% (2.064), 5:2 = 2.9% (2.764), 7:3 = 1.0% (2.917), 7:2/8:3/10:3/11:4 ≈ 0.8%. Home/Cinder/Moon zones are negligible (μ 2⁻¹⁸, 2⁻²¹, 2⁻²⁴ → widths ≤ 6% of the Giant's). The plane's exact belt (extra = 3,000, seeds 1/2: the 2,700 bodies c857 flew) gives 17.6%/19.3% — same census at sampling noise.

- **Composed desync rate 115 events/body/belt-orbit (both combs) → headroom 9,000/115 = 78×** (90× if the bridge certifies at 16; **170× if zone bodies hold at 64** — 5022's near-2:1 study, first order, needed 64; the q≥2 floor is unmeasured).
- **Width-robust**: wmult 0.5 → f 9.2%, 122×; 2 → 34.7%, 46×; 4 → 60.1%, 28×. The verdict "an order below 10³" survives any plausible width error.
- **Placement cliff (design arms, the same shipped e-draw remapped)**: belt [3.0,3.5) → **53.8% inside the Giant's 2:1** (zone [3.148, 3.398] at e 0.07) → uncertifiable at any cadence, headroom 0; belt [1.4,2.4) → 6.2% fine, 231×. The plane's belt [2,3) clears the 2:1's lower edge (3.148 AU) by **0.148 AU** — a margin, not an engineering (the window predates the census).
- **Worst cell (the allocator's number)**: bins on a zone run 90–98% fine (bin at the 3:1: 28,420/31,063 = 91%); 5 of 32 bins > 50% fine. Per-cell cadence is bimodal; the population mean (115) is nobody's rate: clean bodies pay ~11, zone bodies 512.
- **Frozenness (derivation, no flight)**: synodic periods with the Giant are 3.75–9.6 yr (1.2–3.0×10⁸ game-s); a 10⁶ game-s session gives < 0.009 conjunctions/body — the census is birth-frozen on any playable horizon (and 45c0/c857 measured the belt's own clock frozen likewise).

Commands (each ≤ 60 s, Linux/x86):

```
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1,2,3 1.0 shipped   # the census table
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1 0.5 shipped      # width sweep (also 2, 4)
cargo run --release -p emergent-universe --example beltcensus -- 1000002 1,2 1.0 3.0:3.5    # the death arm (also 1.4:2.4)
cargo run --release -p emergent-universe --example beltcensus -- 3000 1,2 1.0 shipped       # the plane's own 2,700
```

**Predictions** (`predictions.md`, written before the run): held — f_enc exactly 0 (1), D1 exactly 0 (3's half), the [3.0,3.5) cliff > 25% (5's half). Missed, reported: f_res 17.8% vs [8,16] (3); headroom 78× vs [400,900] (4) — the prediction itself repeated the board's error, pricing the mean cadence and not the tail; strong-tide 0.26% vs ≤ 0.2% (2, marginal); [1.4,2.4) 6.2% vs > 15% (5's half). The two headline misses are the finding.

**What would make it wrong.** (a) The zone floor: 256/own-orbit for q≥2 zones is B13's encounter floor borrowed; if 16/Giant-period holds at the 3:1 (nothing measured says it does — 67be killed only first order), the headroom returns to ~700×. One cbe6-style arm at a 3:1-drawn belt closes it. (b) The width model is oracle-side literature, not shipped code; the ×0.5–×4 sweep brackets it, and even ×4 keeps ≥ 28×. (c) The 9,000 anchor and the 2-comb identity are the board's/cbe6's, not re-derived here. (d) Belt–belt encounters (the encounters row) and the crest/wave tail (4093/9e75) are other tails not composed into this bill. Cost of adoption: none — a design input; the desync grid's belt constants and any birth-belt placement rule now have their tail priced.

**Fit with PRINCIPLES.** "i care about the p95/99 results i want the game to be smooth" (12): the mean cadence is nobody's cadence — 17.8% of the bodies pay 75% of the bill, and the worst cell runs 100% fine-class. "A raindrop is an event for an ant and nothing for a lion" (33): each body resolves only the influences significant at its scale — the census is that rule's price list for the belt. Heuristic kept: "Never trust an average where tails decide."

**The lens.** Taleb: what breaks. The desync rescue's ~10³ sentence was fragile to a tail nobody had counted; the census is the via-negativa check (no new mechanism, one deleted assumption). Missed by this lens: nothing here flew the engine (birth-frozenness is a derivation, and the zone floor needs a flight); the census says nothing about where the 10⁹ tail goes *wrong* endogenously (stirring into zones over horizons ≫ playable) — the horizon bound is the game's, not the universe's.

**Grade suggested:** silver — reproduced (seeds stable to ±0.1%, width-robust, the plane's own N matches), one named experiment from gold: the zone floor at the 3:1 on cbe6's instrument (and the 5–6.3 Hill interior arm), which pins the 78–170× interval to a number.
