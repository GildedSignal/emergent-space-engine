Grade: silver

**Abstract.** Claim: the sign-fixed, window→0 Fermi-frame Schwarzschild tide confirms the q-fermi2-tide closed form at 6/4/3.1M, eccentric and unbound scenes, and the epoch rule is N/orbit = 512π√2·3f√g/√((2−3x)²+g²): 3047 at 1000M → 421 at 3.1M (weak-field-set), while the prior run's axis columns (3214/4017/16081) are unwrap artifacts. Everything reproduced **bit-identically** (kernel.py 51 s, leakage.py 4 s, sanity.py 1 s). My attacks confirm every load-bearing claim: the prior line-118 unwrap gives 1.998 turns where the honest doubled-angle unwrap gives exactly 1.0000 per prior window at 6/4/3.1M; the exact epoch formula matches independent quadrature at 7 new radii to ≤3×10⁻⁵; E-independence is exact; the mirror rotation sign is rejected at O(1.8). Gain: E9's phase-2 controls plus a premise fix (16081→289). Cost: none (one rational comparison). Silver because P6's unbound half failed (6898/5320 vs <1500) and several summary headlines overstate the run's own printed numbers.

## Reproduction

- `python3 sanity.py` (0.7 s), `python3 kernel.py` (50.7 s), `python3 leakage.py` (3.7 s): `decisive.log` and `kernel-table.json` reproduce **bit-identically**; `leakage.log` identical. All ≤ 60 s. `work/patch.diff` is empty (no tree edits), as stated.
- Ordering: `predictions.md` (mtime 30 m) precedes `kernel.py` (18 m), `decisive.log` (17 m), `kernel-table.json` (15 m). Predictions contain genuinely held-out numbers (P5 predicted 3055 at 1000M, measured 3047).
- Prior-run anchors verified from `origin/claude/lab-20261002-0539-redteam-fermi2-21db`: the prior checker's 2877 (6M) and 2395 (3.1M) tensor counts, normalized per true orbit (÷1.4142, ÷5.5678), give 2034 and 430 vs this run's 2035 and 421 — the quoted cross-check is real.

## Adversarial cases (5)

1. **The artifact mechanism (K4), directly.** Applying the prior run's own formula (`probe-orig.py` line 118: unwrap on the *half* angle) to the einsum kernel over the prior window 2πr^1.5: sweep = 12.555/12.551/12.555 rad = **1.998 turns** at r = 6/3.1/4, where the honest doubled-angle unwrap gives **1.0000 turns** and the identity ω·2πr^1.5 = 2π predicts exactly 1. The prior columns (2.0–2.5 turns) are unwrap noise, not physics. Confirmed stronger than claimed.
2. **Epoch formula at 7 radii not in their table** (200, 30, 7, 5, 3.5, 3.05, 3.01M): independent quadrature of the closed form vs N = 512π√2·3f√g/√((2−3x)²+g²) agree to ≤2.6×10⁻⁵ everywhere; monotone 3026→131. I also re-derived the rule algebraically (√2|a−b|ωTp/(ε√(a²+b²)) with ε = 2⁻⁸, λ = x/g, 2g+3x = 2−3x): the formula is right.
3. **E-independence** at L = 6.5, r = 20, E ∈ {1.05, 1.2, 1.5, 3, 10}: in-plane eigenvalues {−(2+3λ)m, +m} identical to 9 decimals (out-of-plane m(1+3λ) also E-independent; only C23 mixes). Holds far beyond the tested pair.
4. **Deeper than 3.1M:** at r = 3.05M the geodesic pair-difference measurement fails at every window size down to 8 steps (members plunge) — the geodesic-validated table genuinely ends at 3.1M; below it only the einsum+closed-form paths remain (both share the transport). The run's boundary is honest but should be stated as such in any E9 freeze.
5. **Rotation sign (P3) falsifiability:** Φ = −∫ω matches the einsum to 3.3×10⁻¹³ over the 6M window; the mirror Φ = +∫ω disagrees at 1.79 — the sign is pinned, not fitted.
6. (Cross-check) Prior "eccentric" scene `ecc_y0(6.5, 3.5)`: E² = 0.893 gives r_a = 7.5, e = 0.071 — the relabeling to rosette is correct; the prior dossier's "eccentric" naming was wrong (note: no prior file ever wrote "e ≈ 0.88"; that number was this author's own P6 label).

## Novelty

No HISTORY entry or doc contains the window→0 kernel table, the closed-form epoch rule, or the artifact finding. The kernel's closed form itself is the prior checker's (−w(3γ²−1); their check.md) and q-fermi2-tide's — this run is exactly the one re-derivation that check named (h→0, all scenes, cross-checked), plus two things genuinely new: the exact epoch formula and the demonstration that the prior epoch columns were unwrap artifacts. The E9 freeze in `docs/engine-judge.md` cites the prior runs' records; no frozen gate depends on the artifact columns, so nothing frozen is weakened.

## Goal fit

Direct hit on board focus item 4 (Schwarzschild tide in the Fermi frame, phase 2 after E9). "Compute only surprises"/"the best part is no part" (principles 3/17): the epoch rule is one rational comparison and deletes the strong-field epoch fear. "The simulation tells us what's next, not us" (principle 22): validation against geodesic pair differences, never the formula — K2 of the prior run, now with the h→0 discipline the prior lacked.

## Why silver, not gold

- **P6's unbound half failed** (predicted <1500/passage, measured 6898 and 5320) — honestly reported, but by this lab's precedent (the law's red-team, the prior fermi2 run) a failed held-out prediction caps the grade below gold.
- **Headlines the log contradicts** (the lab's named grade-loser): the dossier says "Held: P1 … geodesic within 1e-3: worst 9e-4 at rosette peri", but its own table shows parab outbound −1.41708 vs closed −1.42205 = **3.5×10⁻³**; "the transverse eigenvalue is +w at every scene to ≤2×10⁻⁴" is false at rosette peri (2.3×10⁻³), ecc peri (1.1×10⁻³) and parab outbound (1.6×10⁻³); "quadrature … and einsum agree to 4+ digits" is false at 3.1M (430 vs 421, 2%). The data is all printed honestly; the summary sentences overstate it. Also "its 23.6 (a 5.57-orbit window…)": the prior 23.58 was measured on eeff's 1.64M window (0.27 orbits; `eeff-orig.py` line 19) — the inflation and the non-reproducibility-with-consistent-member-data claims both stand, but the window provenance is misstated.
- Small record gaps: `leakage6.log` is cited but absent (leakage.py fully regenerates leakage.log); `sanity.py`'s own axis() double-unwraps (printing 2× sweeps) and its "closed" print carries a spurious r₀ factor — cosmetic, since kernel.py's versions are correct.

## The one experiment that would make it gold

Close the unbound half analytically: derive the amplitude-drift epoch law (∫‖ṁ‖/m dτ ≈ 6 ln(r_max/r_p) per passage) from the closed form, pre-register counts for 2–3 new unbound scenes (different E, L, r_max), and confirm them — turning the failed P6 half into a held prediction. With the three summary sentences corrected to the printed tables, the record is clean and the whole kernel+epoch package is freeze-ready.

## What the author missed

- The per-*proper-time* kick rate rises ~4500× from 1000M to 3.01M (N/T_p: 0.015 → 69 per M); only per-orbit and per-battle counts fall. "Cadence is set by the weak field" is true per battle (τ₁₀ shrinks faster than N), but the headline should say which normalization — the same trap the prior run's "×21.9" fell into.
- The out-of-plane eigenvalue m(1+3λ) is quoted, never geodesic-measured (disclosed; the game is 2D).
- Kicks-per-battle was computed from the prior run's τ₁₀ table, not re-measured (disclosed).
- sanity.py, the convention-pinning file, misprints the two conventions it exists to pin.
