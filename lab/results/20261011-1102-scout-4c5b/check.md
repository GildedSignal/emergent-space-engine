Grade: silver

**Abstract.** Claim: Peters' flux balance drifting the exact Schwarzschild tube's (E, L) is adoptable, with measured constants (handoff = separatrix, re-key wall, 1PN flux contract). Everything reproduces bit-identically (`python3 inspiral.py`, 43 s, 35 MB); I independently verified the Peters–Mathews flux (time-domain method, 5e-7 at e=0.3), the angular-momentum flux (exact algebra), the wall closed form, and the 1PN+tail coefficient. But one of three headline claims is an artifact: `circ_L` is wrong by √a (coded √(a/(a−3)), true a/√(a−3)), so the P9 "spurious e = 0.81" was born on a plunging orbit; corrected, e < 1e-4 — the author's own prediction held and the harness was broken. Also: an in-domain high-e birth meets the author's own pre-registered kill criterion (wall 15× out, never applied), and "690"/"0.005/orbit" aren't regenerable. One line + rerun from gold.

## Reproduction

- Clean tree, `work/patch.diff` empty (no repo edits). `python3 inspiral.py`: log identical, `inspiral-out.json` **bit-identical**, 43 s, 35 MB RSS. The author's 40 s / < 100 MB claims hold.
- File-time order: `predictions.md` 11:19 < `inspiral.py` 11:38 < log 11:38:52 < `dossier.md` 11:42; the JSON's 11:43 mtime is the author's post-dossier regeneration check (bit-identical, as claimed in author-final.md). Pre-registration genuine.

## What I verified independently (supports the run)

- **R(u) cubic, Vieta, circular family:** re-derived; `circ_r` inversion exact (round-trip ≤ 1.2e-13 at r = 6.001; 6.000 at ISCO); `EL_from_ae(a, e→0)` → E matches `circ_E` to 1e-14 — the eccentric machinery is exact algebra.
- **Fluxes:** my time-domain Kepler + finite-difference quadrupole average agrees with Peters–Mathews to 5.1e-7 at e = 0.3 (my method's own limit at e = 0.9 is 2.7e-4; not a contradiction); `flux_G` I derived algebraically from Peters' da/dt and de/dt — exact match.
- **1PN+tail coefficient** (−1247/336 − 35ν/12, +4πx^{3/2}): matches the standard Blanchet circular flux; "from memory" but correct.
- **Wall closed form** a_wall^{5/2} = (192π/5)νF̃(e)/ε̄ (my derivation): 24.7/61.9M predicted vs 25.4/62.6M measured (ν=0.25 circ); 17.1 vs 18.0 (ν=0.01, 0.1%). The wall-as-closed-form claim stands.
- **P4** (circularize-before-plunge): confirmed at ν=0.05 (a* = 6.83, e* = 0.000) and from a₀=1000M (e_end = 0.010).
- **Novelty:** nothing in HISTORY.md, docs or lab/results measures radiation reaction; law.md:35 names "Peters' a(t) is its generator" with no numbers; HANDOFF "Headed next" #4. First numbers behind an adopted-on-paper law.

## Attacks that landed

1. **`circ_L` bug; the P9 headline is an artifact.** Coded `√(a/(a−3))`; the tube's circular family needs `a/√(a−3)` (double root: L² = 1/(u₀(1−3u₀)) = a²/(a−3); R(u₀) = −1.1e-16 with correct L, +0.010 with coded L; the author's own `EL_from_ae` e→0 limit gives 10.153 at a=100, the code gives 1.0153). The P9 two-flux experiment therefore started off-family on a plunging orbit (one positive root), drifted L through zero. **Corrected initial L: spurious max_e = 0.0000, final L = 3.492 vs family 3.464 (+0.8%).** The two-flux wiring is consistent at Newtonian order, exactly as P9 predicted ([1e-4, 1e-2]); the dossier's "measured 0.81 → the wiring is inconsistent, hence the projection rule" (claim 3, second half) is a law extracted from a bug, and P9 should have been reported as *prediction held, harness broken* — the lab's own H0183 lesson. Projection remains a fine *simplification*, but its stated evidence is false.
2. **The author's own pre-registered kill criterion, met and not applied.** ν=0.25, e₀=0.9, a₀=110M (p = 20.9M, inside B11's domain): 1% wall at ~110M vs separatrix 7.5M — ≥15× (kill line: ≥5× at ν ≥ 0.01), 23 orbits, non-adiabatic for its whole life. All the author's e₀=0.9 runs start at p < 20M. The claim "inside B11's domain eccentric binaries circularize before plunge" needs the high-e comparable-mass corner excluded; the table shows "wall at start" but the kill decision is never drawn.
3. **Handoff-band edges are soft.** Shipped code ends the a₀=1000M, e₀=0.3 run at a* = 11.57 (outside [6.1, 9.1]M); my line-identical replication ends at 6.78; step-tightening moves a* 6.76→6.23 and e_end 0↔0.03 (A5). The band is real (~6–12M, near-circular) but not a 0.1M-precision constant.
4. **Non-regenerable dossier numbers.** "690 re-keys from 1000M" (circular): not in the JSON; analytic telescoping gives 551, measured eccentric gives 642, 345+415 gives 760. "0.005 re-keys/orbit": measured 1.34e-3/orbit (478,997 orbits, 642 re-keys — the generator is *cheaper* than claimed). The "re-keys from 1000M" table column is the analytic telescoping (script line 368), presented beside measured columns.
5. Minor: born-plunging pericenter (r_p = 1.5M) crashes with IndexError (out of domain; the plunge tube owns it — robustness note). W2 scaling is ~4–6× per 4× step change (O(h) endpoint), not the "2×" stated — same conclusion, imprecise number. The e*(ν) trend skips its non-monotone point (e₀=0.9: 0.277 at ν=0.25 > 0.000 at ν=0.01).

## Predictions

Held: P1, P3, P7, P5-circular-half, P8 at 100M and the flux-only crossover. Failed and honestly disclosed: P2 (partially; my A9 confirms endpoint O(h)), P4, P5-e₀=0.9, P6, P8@20M. P9 was reported as a failed prediction when it had actually held (see attack 1).

## Goal fit

Real and on-target: the unowned headed-next item; deletes inspiral-as-kicks (df81) by supplying the replacement's constants; PRINCIPLES #3 ("Nothing is evolved that can be derived": 1.3e-3 events/orbit), #6 (store the generator), #13 (staleness resets at each re-key) all genuinely served by the measured design.

## The one experiment for gold

Fix `circ_L` (one line), rerun P9 (expected: e < 1e-4, prediction held), apply the pre-registered kill criterion to in-domain high-e births and restrict the adoptability claim to e₀ ≲ 0.6 at ν ≥ 0.01 (plus the adiabatic EMRI corner), and regenerate 690 / 0.005-per-orbit from the shipped code with the a₀=1000M re-key column measured, not telescoped.

## What the author missed

- The artifact (wrong circular L) was checkable in one line against the author's own `EL_from_ae` limit — the run contained its own control and it wasn't consulted; instead a correct pre-registered prediction was overruled by a broken harness.
- The kill criterion written before the run was not evaluated against the runs that meet it.
- Endpoint precision (a*, e* to 0.1M/0.001) reported without step-convergence evidence.
