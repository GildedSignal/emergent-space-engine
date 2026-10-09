# Predictions (written before the decisive run)

Question: at 10⁹ bodies at fixed belt density on one 8 GB M1, which term breaks first (memory via H_live, kick compute, candidate re-setup), and is H_live bounded in steady play?

Model constants taken from the repo (not tuned by me): tube = 16 bytes/body (law.md §State); belt program ≈ 0.126 bits/body (gold 20261005? components-98bc); kicks 0.3/orbit averaged, 32/orbit unaveraged (H0190); candidate-pair setup 2.5–24 µs per pair per element change (law.md, encounters); encounter radii ρ/a ∈ [10⁻⁴, 10⁻³] (r8 v4 cases); kick sizes in the design's own tests δa/a ≈ 10⁻³ (r8 v4 case d); the law's error floor ~10⁻⁶ per cycle (jet discussion).

Held-out predictions (the decisive instrument is an Öpik–Arnold Monte Carlo belt, written fresh, independent of the r8 harness):

1. **Encounter rate per body per orbit** at σ_e = 10⁻², ρ = 10⁻⁴ (relative), fixed surface density: between 10⁻⁴ and 10⁻² per orbit. And per-body rate within 3× when N grows 10× at fixed density (i.e., total rate ∝ N).
2. **Bits per encounter outcome** (spread of element deltas over a 10⁻⁶ relative quantum): between 30 and 300 bits.
3. **H_live stock per body** after a 3-hour session at RTF 100 with 1-year orbits (≈ 1 orbit/session): ≤ 1 bit/body, i.e. 10⁹ bodies gain ≤ 0.2 GB of live distinctions per such session — memory not the wall.
4. **The first-breaking term at 10⁹** is not memory and not the kicks themselves but per-kick candidate-pair re-setup: it exceeds a whole M1 (≈ 10¹⁰ simple ops/s) somewhere between RTF 10 and RTF 10⁴ depending on orbit scale (1 AU vs 1 day). I predict the crossover RTF at 1-AU-year orbits is ≈ 10²–10³.
5. Claim-check (lens item 3): the board's "10⁹ orbiting bodies ≈ 190 cores" re-derives to within 10× from steps/orbit × time-compression alone (no exotic term).

What would make me wrong: encounter rates above 10⁻²/orbit (belt too dense), bits/outcome above 10³ (quantum far below 10⁻⁶), or per-body rate growing with N (dilution claim wrong for this regime).

Machine state at run: shared Linux x86 runner, 8 vCPU, load recorded in dossier.
