Grade: gold

**Abstract.** Claim: the adopted phase-neighbour certificate (gold 20261006-0346) silently drops 95–100% of encounters on equally a-concentrated lawful states with scattered apsides, and 100% of inter-formation battle encounters; rebuilds cannot fix it. All dossier commands reproduced bit-exactly (e=0.6: miss@4 96.3%, ranks p50 147; battle rank ≈ N/2; mechanism rank = N·|Δλ*|/π, correlation 0.994–0.998). My attacks strengthened it: e=0.1 scattered already misses 94%; N=512 doubles ranks (p50 300); aligned-apsides e=0.6 stays clean (0%), isolating Δϖ as the trigger variable. Adoption: one closed-form Δλ*(e,Δϖ) gate, synodic-drift expiry, per-phase-cluster certificates — before crates/encounters builds. It blocks the B13 silent-loss ruin class inside the tier replacing the quadratic one.

## Reproduction

Ran the dossier's four commands in a scratch copy (`/tmp/check1`, originals untouched; `work/patch.diff` is empty so nothing to apply). Every headline number matches the stored JSONs exactly:

- `A_gold_T4_s1`: miss@4 35.12% → 0.0% with P/4 rebuilds, max rank 13→4; controls PASS both ways.
- `B_e06_s1`: miss@4 96.3%, p50 147, max 202, rebuild identical to the digit.
- `D_battle_s1`: inter-cluster miss@4 100%, max rank 129 ≈ N/2; intra-cluster remainder at rank ≤ 4.
- `geo.py`: correlations 0.9941 / 0.9977 / 0.9978; Δλ* p50 1.784 / 2.594 / 1.556.

Truth instrument: v_cap = 2·v_max(a,e) makes the KD-tree dilation `ρ + v_cap·dt` a genuine bound on missed minima; every trough refined by ternary search. My own resolution control (B_e06_s1 at 16384 vs 32768 slices/period): identical 27-pair sets, empty symmetric difference, dmin agree to 2.2×10⁻¹⁵. Positive/negative controls pass. The truth is converged; this is not an instrument artifact.

Mechanism verified independently of the code: at a crossing longitude the mean-longitude offset is Δλ* ≈ |Δ(M−f)| + |Δϖ|; for the two-ϖ-cluster battle at e=0.4 that gives 4e ≈ 1.6 rad (measured p50 1.556), rank = N·Δλ*/π = 256·1.556/π ≈ 127 (measured 121–129). The dossier's formula is exact, not fitted.

## Predictions

`predictions.md` mtime precedes every decisive result file (smoke.json, a calibration run, is the only older artifact — allowed). P1 held (0.4% / 35.1–36.2% / 49.8% against predicted ≈0 / 5–40% / ≥50%; rebuild residue 0.33%), P2 held (95–100%, rank halving 202→99, rebuild identical), P3 held (100% inter-cluster, all seeds), P4 held by construction. The author's own kill criteria did not trigger. One flag: `probe.py`'s mtime postdates `results_A.json` — an edit after some results — but the current code regenerates every stored number exactly, which I verified, so the record is regenerable (the usual silver failure is the opposite).

## Attacks (my own cases)

1. **e=0.1, ϖ uniform, N=256**: miss@4 = 93.9%, p50 rank 18, rebuild no help. The failure domain is *wider* than tested — asteroid-typical eccentricities already break rank-4. (miss@16 = 60.6%, so even k=16 is not safe there.)
2. **e=0.6, ϖ aligned, N=256**: miss@4 = 0%, max rank 3, 25 encounters. Eccentricity alone is harmless with aligned apsides — the domain boundary is apsidal spread, not e. This slightly narrows the claim ("aligned-apsides, near-circular" → apsidal alignment suffices) and confirms the proposed Δλ*(e, Δϖ) gate reads exactly the right variables.
3. **e=0.6, N=512**: miss@4 98.9%, p50 rank 300 vs 147 at N=256 (2.04×), 89 encounters. Linear-in-N confirmed with a thick sample, where the author's N=128 cases were thin (3–4 encounters). Fixed k is quadratic in disguise, as claimed.

## Novelty

No HISTORY entry bounds the certificate's domain: the gold lives in the board's 6 October taste log as regime-free ("every real encounter lies within partner rank 4… triggered by a dimensionless number"), and H0214 records only the symptom class (B13, 7 of 64 flybys lost). The conjunction-displacement trigger, the synodic-drift expiry, and the refutation of "paid once per element change" are new.

## Goal fit

Board's top scaling risk: candidate work must track real encounters. This shows the adopted O(n·k) certificate silently loses encounters exactly where its trigger fires hardest (P4), i.e. a premise of an adopted gold is wrong, and the correction is a gate, not a component. PRINCIPLES: "a failed expectation is not automatically a failed method" — the run kills no method, it sizes the trigger; findings are rank counts and miss fractions ("Floats may explore; only integers decide"); cheapest falsifying test first. The miss class is the ruin class the board already paid for at B13: silent, not slow.

## Weaknesses (none gold-blocking)

- `ranks_of_pairs` counts the body itself (separation 0), so every quoted rank is +1: "rank 4" tests true rank ≥ 4. Boundary statistics slightly overstate misses; p50 ranks 18–300 and miss@16 90–96% are untouched, and in the aligned cases rebuilds zero everything anyway.
- `geo.py`'s `pred_rank = N·Δλ*/(2π)` is half the dossier's (correct) `N·Δλ*/π` — visible as pred 72.7 vs measured 149; only scale-invariant correlations are quoted from it, and the dossier's own formula checks out against measurement exactly.
- Truth is pure Kepler: no librating co-orbitals (Trojans/horseshoes), which need an integrator; mutual gravity only adds scatter, so this weakens, not strengthens, the certificate.
- The Δλ* gate's per-certificate cost is unmeasured (author discloses; it is one closed-form Kepler evaluation per certificate).

## What the author missed

- Failure begins near e ≈ 0.1, not 0.3: real belts sit mostly in the broken regime, so the Binet-cone fallback will carry most belt work — the certificate's true domain is the aligned-formation niche only.
- Aligned-apsides eccentric formations are safe (0% miss at e=0.6): the domain is set by Δϖ spread, not eccentricity — good news for the proposed trigger, since Δλ*(e, Δϖ) already encodes it.
- The +1 rank inflation and the geo.py half-scale prediction noted above.
