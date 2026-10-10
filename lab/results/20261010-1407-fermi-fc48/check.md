Grade: silver

**Abstract.** Claim: stirring a belt is a step, not a rate problem — one Jovian pass scars every body, and the wall is the level. Reproduced bit-identically (seeds 20261010 and 777): f_kicked 0.845 at 1 orbit → 1.000 by 2; 0.85 kicks/body/orbit; scars 126.4 bits/body at 1 orbit; growth 2.95 bits/doubling; `floor.py` 75.5/76.1 bits/body; rate ~33 KB/s at rtf 100. But the 10⁹ headline is wrong: the floor's own −log₂N term gives **61.6–62.2 bits/body = 7.7–7.8 GB at 10⁹ — under** the 8 GB budget, not 9.4–9.5 GB over. Scars (126 bits = 15.8 GB) remain ~2× over, so the requantization/t_p-anchoring conclusion survives; "no exact encoding fits 8 GB" does not.

## Reproduction

- `python3 hlive.py` (82 s): every row matches the shipped `hlive.json` exactly (126.4 / 128.6 / 149.3 fields; σ_e 0.0066→0.0189; 874 kicks/body; slope 2.949). `python3 floor.py` on both the shipped and my regenerated `final_state.npz`: 75.5 birth / 76.1 final, matching the dossier.
- Spec provenance verified: quanta = law.md line 12 (E,L 32-bit, ϖ 32-bit, t_p 64-bit); scars = line 13; belt = `belt.rs` (uniform a, Rayleigh e); B18 bar "≤ 2× floor + 2 bytes, reported at 10⁹" quoted correctly; HANDOFF risk line "H_live … not measured yet" is real; H0190's band is 0.28–32.5 kicks/orbit. Rate arithmetic checks (2.05e-8 kicks/body/s → 20.5/s at 10⁹ → 33 KB/s at rtf 100).
- Predictions: `predictions.md` mtime precedes `hlive.py`/`hlive.json`/`final_state.npz` by 6–7 min. Pre-registered, with a kill criterion. P1/P3/P4/P6 held, P2 marginal-top, P5 faster — the dossier reports the misses honestly.

## Attack

1. **Seed 777, full 1024 orbits:** same table to ~0.1 bits (f_kicked 0.847; slope 2.95; floor 75.5/76.1). At N=65536 these are ensemble statistics, so this is genuine seed-robustness, not a tautology.
2. **N-scaling of the floor (kills the headline).** `floor.py`'s formula is H₁ − log₂N + log₂e; the per-body floor therefore *falls* with N. Measured: 78.98 bits at N=4096, 75.48 at 2¹⁶, 71.53 at 2²⁰ (drop 3.95 ≈ log₂16). At N=10⁹: 61.6 bits birth / ≈62.2 heated = **7.70–7.78 GB, under the 8 GB budget** (margin ~3%). The dossier took the N=65536 number (75.5) and multiplied by 10⁹, contradicting the −log₂N term in its own script. The claim "no exact encoding at the tube's own quanta fits 8 GB at 10⁹" is false as stated; the floor crosses 64 bits/body only after ~2 more σ_e doublings (~10⁴ orbits). Caveat on my side: the sorted floor treats belt-body identity as gauge (law.md: "identity is provenance"; dynamics here are identity-free), which is the reading the author's own "any exact encoding" wording invites; an identity-preserving encoding pays ~H₁ ≈ 90 bits/body (11.3 GB) and is over — but that is the scar representation, not the best possible one.
3. **Model tautology check.** Kick size q ≈ 0.8–1.7×10⁻³ vs quantum ~10⁻¹⁰: every kick is ~7 orders above quantum, so P1 (f_kicked→1 in one pass) could hardly fail in this model; the entropy numbers are the real content. M-at-conjunction is treated as uniform (it advances ~0.77 rad/conjunction), making heating conservative — the dossier concedes this.

## Novelty and fit

No prior measurement of a stirred belt's floor exists: components-98bc (gold, 5 Oct) measured the *smooth* belt (0.126 bits/body); H0190 measured kicks/orbit, not entropy. The rate-side deletion (six orders under bandwidth; the wall is never the rate) and the level-vs-rate decomposition are new and target the named HANDOFF risk. Principle 24 ("the memory floor is information") is served — measured, the floor at 10⁹ is ~7.8 bytes/body once structure is gone.

## The one experiment for gold

Re-issue the floor at the 10⁹ scaling (one line: H₁ − log₂(10⁹) + log₂e, or run `floor.py` on N=2²⁰ states to show the trend) and restate the claim: the wall is the *scar representation* (126 bits/body, 2× over) and a ≤3% margin on the floor — not an information-theoretic impossibility. Optionally show whether an operational encoding (sorted blocks + Elias–Fano, already in shipmem) approaches the corrected floor.

## What the author missed

- The −log₂N term when extrapolating per-body floor to 10⁹ — the central quantitative error.
- Internal inconsistencies: the claim's "raw scars 107 bits/body = 13.4 GB" matches no shipped number (row 1 is 126.4 bits = 15.8 GB; conservative direction); `hlive.json`'s stored floor (65.5) is the capacity-capped B=2¹⁶ estimate that `floor.py` supersedes — the dossier never says the json disagrees with it; "σ_e only doubles" is 2.9×; "converged across 2²⁰–2²⁶" is loose (2²⁰ gives 55.7 vs 58.1).
- The `T_ORBITS = 2` quick path crashes at the slope fit (empty t≥8 set) after printing rows — the "reproduces in ~2 s" command half-works as shipped.
- The identity-is-gauge question (which encoding class the 8 GB verdict applies to) is the actual decision B18's stirred clause needs, and it is unexamined.
