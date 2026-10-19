# Dossier — 20261019-1817-fermi-d4ff (Fermi lens)

## Claim

The 10⁹ ledger's dominant row (the kick/event stream, 91–97% of the composed CPU budget) is now **closed against the belt's own physics**: its only missing belt-belt term is *contacts* (encounters fire no items — ships are massless test bodies on exact orbits, so a 100-km pass changes nothing), and it is priced at **+0.054 cores at today's full fired cost** (5.6 contacts/game-s at 10⁹, both bodies itemized at 82.5 µs x86 → 48.3 µs M1, rtf 100) — the closure sentence (cadence cut + ≤4.9 µs/event) survives. The same derivation yields the discovery tier's true-positive bar and the stream's fat tail: **the belt's conjunction rate at 10⁹ is 84 pair-events per game-second per root unit of screening reach** (5.7×10³/game-s at the shipped 2¹⁰ instrument reach of 100.4 km, linear in reach), contacts wake up at **N ≈ 7×10⁶** (rate ∝ N²), and a concentrated population's contact stream equals its own clock stream at concentration **C = 3.2×10³** (a 10⁶-ship fleet in a ~510-km box).

## Bottleneck

Board focus rows 1–2 and the budget-1e9 ledger (3aec): the stream row was composed from the **clock cadence λ = 3.55×10⁻⁵/body/game-s (0659) on an inert belt**, with the belt's own interaction stream unpriced — mandatory once every body is real at 10⁹. This run prices it (order-of-magnitude lens: derivation on shipped constants, anchored to the record's own published digits), deleting the premise's open risk without moving any number that matters: no component grows, none is deleted, but the ledger's headline now carries a bound instead of a hole.

## Evidence

All numbers regenerate by `./regen.sh` (~2 s; `work/belt_stream.py`, constants cited to shipped code in its header):

- **Constants (shipped, cited):** 1 root unit = 1.477 km = GM☉/c², root time = 4.927 µs (`scenario.rs`: "The sun's M is 1.477 km: one root length unit"; AU = 101,300,000); belt a uniform [2,3) AU at 2⁻⁸-root quanta, e Rayleigh σ=0.07 capped 0.4, uniform angle/phase; ship radius `Scalar::raw(34, -10)` = **49.0 m**; encounter reach 2¹⁰·(rᵢ+rⱼ) = **100.4 km**, contact reach 98 m (`encounter.rs`, ENCOUNTER_LOG2 = 10). The genesis integer lanes (splitmix64 `draw`, `rayleigh_q48`) are ported verbatim; port validated by mean e = 0.0873 vs Rayleigh prediction 0.0877 and a ∈ [2.00001, 2.99989] AU.
- **⟨|Δv|⟩ = 22.9 km/s** between random belt members (20k exact-genesis samples × 8 phase realizations, shell-resolved). Independent closed form (circular orbits, uniform a, random phases, no shells): **24.2 km/s** — the model, not the number, is what my wrong prior underestimated: the a-spread [2,3) AU dominates, not e-dispersion.
- **Conjunction law (10⁹, shipped annulus, occupied r ∈ [1.53, 3.74] AU):** 84.1 pair-events/game-s per root unit of reach → **5,718/game-s at 100 km** (= 5.7×10⁵ answers/wall-s at rtf 100, the encounters tier's TP bar, against 5×10¹⁷ pairs: selectivity 10⁻¹⁴); **contacts 5.58/game-s** (filling factor 9×10⁻¹²: ships 49 m with ~29,000 km mean spacing — the emptiness is real, N² wins anyway). Systematic: global-mean rate 2,811 vs shell-integrated 5,718 (factor 2.0 from radial correlation — inner shells denser and hotter); every conclusion below survives a 2× swing either way.
- **Stream fold:** contacts → items (both bodies): 2×5.58×100×48.3 µs = **0.054 cores** today-cost; 0.0067 at the 6 µs arithmetic floor. Against the composed totals (193 shipped / 39.3 split8+survival / 22.5–25.3 checker belt-cost): ≤ 0.25%.
- **Thresholds:** contacts ≥ 1/game-hour at N = 7.05×10⁶ (∝ N²: unmeasurable at every flown rung — at 10⁶, one contact per ~week); C_contact = λ/Γ_c = **3,179** (a 10⁶ fleet doubles its own event budget inside a 507-km box; side ∝ √F at fixed C); a belt-temperature mixing zone (battle) hits encounter-criticality at C = 3.1.
- **Census reconciliation (closes the page's flagged caveat, its clock half):** the "inert belt" census reading is a window artifact — f80a measured the belt's first clock wave at gs 11k–16k, so the census windows (10 s wall, rtf 100 ≈ 10³ game-s) see zero belt kicks by construction, while the long arms read 8.03 bindings/body at 174k gs = **1.30×λ** (P2 band [1.1, 1.5]: held). λ is the belt's own steady rate, not a player-stream fact.

## Predictions

`predictions.md`, written before any computation. Held: **P2** (1.300 ∈ [1.1, 1.5]), **P4** (wake-up 7.05×10⁶ ∈ [3×10⁶, 5×10⁷]), **P6** (co-lane pair fraction 3.9×10⁻¹¹ < 10⁻⁶; same-lane pairs never drift — equal periods), **P7** in substance (+0.054 < 0.5 cores). Failed, and the failures are the run's content: **P1** (⟨|Δv|⟩ 22.9 vs band 1.5–4: my prior ignored the a-spread; the closed form convicts the prior, not the model), **P3** (encounter events 32% of the clock stream as raw events vs band 1–10%; contact items 3.1×10⁻⁴ vs band ≤ 2×10⁻⁴), **P5** (the concentration threshold is two-armed, C = 3.1 for belt-temperature mixing and C = 3,179 for contacts, not one number in [20, 80]).

## What would make it wrong

- The law gives ships **no mutual gravity** (massless test bodies; "ships' aggregate mass can become a source" is future work). If aggregate ship mass is ever wired as a source, sub-quantum tides accumulate (principle 6) and the encounter term stops being discovery-only — the +0.054-core bound dies with it. Named, not hidden.
- The rate rests on the kinetic (straight-relative-motion) assumption over the encounter scale — the same assumption as the seam's own `hit` predicate; and on phase uniformity, broken only by formations (which is the C-threshold arm, priced separately).
- No live flight measures belt-belt conjunctions (the seam scans only the player's neighbourhood today); the anchors are the record's own published digits (f80a's census/bindings, 0659's λ, 3aec's costs) plus the closed-form cross-check. A stirred-belt flight (the page's od 3) with a conjunction counter would promote this from anchored bound to measured.
- Cost of adopting: none (a bound); the ledger gains a row priced at ≤ 0.25% of total. Fit with PRINCIPLES: "Compute only surprises" (3 — contacts are the only surprise the belt's own physics contains at 10⁹); "The memory floor is information" (24 — the conjunction law is the belt's surprise rate, 84/s per root of reach, the number any certificate scheme must budget); "the simulation tells us what's next not us" (22).

## The lens

Fermi runs estimate before building; mine did, and the estimate's first duty — kill my own priors — fired three times (P1, P3, P5). What the lens may have made me miss: everything here is steady-state and shipped-geometry; transient waves (a burn crossing the belt, 90b7's combs, c749's battles) ride on top of the 84/s baseline and are priced elsewhere in the record; and I did not re-derive the clock cadence's *cause* (28.1k gs ≈ T_orbit/4,432 — why the certificate horizon lands there belongs to kick-cadence, not here).
