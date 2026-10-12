Grade: silver

**Abstract for the integrator.** Claim: at 10⁹ bodies, live distinctions come from SOI rebinds (plus contacts and the player), not mutual encounters — inert at ship mass for ~10²⁶ yr, m_crit ≈ 3×10¹⁸ kg — so the 8 GB budget is birth programs plus repopulation. All code reproduces bit-for-bit (139 s and 75 s, < 2 GB). P2, P4, P5 and the dense-scan control hold. But the headline is 460× high: "36.5 rebinds/s" should read 0.0365/s (a 10³ arithmetic slip), and that rate is itself 2.2× low — crosscheck's planet Newton is sign-flipped; my brute force gives 1.30×10⁻² transits/body/orbit (stable to 200 orbits), inside the pre-registered range. True H_live ≈ 20 bits/s, with the player co-dominant. The decomposition is adoptable; the numbers are not.

## Reproduction

Clean copy of both scripts to `/tmp` (the stored JSONs untouched); `patch.diff` is 0 B — the scripts are the whole work.

- `h_live_fermi.py` (139 s): every stored number regenerated exactly — P1 median 5.00×10⁻⁶, P2 1.020/2.58, first-version P3 54.4 (the superseded bug), P4 and P5 tables identical.
- `crosscheck.py` (75 s): `diff` against the stored `crosscheck_results.json` is **identical** — dense 81 hits (2.03×10⁻²/body/orbit), Newton machinery 0, epicyclic analytic 4.80×10⁻², SOI 1197 (5.985×10⁻³), P2 1.020/2.577.

## Adversarial cases (my own, `/tmp/check-fermi/adversarial.py`, 6 s)

1. **The headline arithmetic fails by 10³.** The dossier's own adjudicated inputs give 5.985×10⁻³/body/orbit × 10⁹ ÷ 1.64×10⁸ s = **0.0365 rebinds/s**, not 36.5/s. H_live(rebinds) = 4.7 bits/s, 0.59 B/s, 2.1 kB per hour — not 4.7×10³ bits/s, 590 B/s, 2.1 MB/h. Worse, the stored `h_live_results.json` was never regenerated after the P3 fix and still carries the *first* bug's downstream table (331.7 rebinds/s, 42,462 bits/s, 19.1 MB/h). Three mutually inconsistent headline values coexist; none is right.
2. **The "corrected" P3 is itself from broken code.** In `crosscheck.py` §2, `dn = npp − nb` but the residual is `dth = λ_body − λ_planet`, whose derivative is `−dn`; the update `t −= dth/dn` is sign-flipped and diverges from the conjunction root. Brute-force dense-time truth (dt = 0.3, episodes counted at rising edges): **2600 transits = 1.30×10⁻²/body/orbit**. As-shipped Newton reproduces 1197 exactly; flipping the sign gives 2380 (the residual 8% is the single-time-evaluation defect, negligible at R_SOI scale). The rate is window-stable: 1.26×10⁻² at 60 orbits, 1.29×10⁻² at 200 orbits — no synodic-truncation artifact. The true value sits **inside** the pre-registered P3 range 0.01–0.05: the prediction held; the instrument did not. The author's "held within a factor 1.7 of the lower edge" honesty flagged a real anomaly but stopped one diagnosis short.
3. **Corrected term structure.** At the true rate: rebinds 0.079/s × 128 bits ≈ **10 bits/s ≈ the player's ~10 bits/s** — "player nil" flips to co-dominant. Contacts 0.29 bits/s. Total H_live ≈ 20 bits/s, 460× below the headline. Singleton saturation ≈ **77 orbits** (~400 game-years), not 167. Every structural conclusion survives and is *strengthened*: the encounter-certification O(N²) risk is informationally dead at ship mass by ~12 orders (P4 reproduced: 2.4×10²⁶ yr; robust to factor-few errors in lnΛ and Σ), and the only 8 GB-scale term is the mixed-population entropy after repopulation.
4. **Minor unflagged slips** (both immaterial): the 10 m contact radius is converted with 1 doll = 9 AU instead of 3 AU (contacts 3× low; nil either way against the < 10² bound); μ_crit uses σ_e where v_rel = √2·σ_e (√2). P2 as coded is the analytic identity √(x²+1)/x — a formula-choice check, acceptable. The r8-v2 belt-0 anchor (427 encounters → 2.135×10⁻³) matches the board's taste log.

## Predictions

File times order correctly (predictions.md predates both results JSONs). P2, P4, P5 held. P1's Monte-Carlo half failed to zero and was withdrawn with the pre-registered failure branch fired — honest and correct; the analytic half is validated only at one hot point (2.4×), unvalidated at r8-cold parameters (author admits ~10× possible; immaterial to the 12-order margin). P3's prediction in fact held against the truth.

## Novelty

HANDOFF names H_live as "not measured yet"; plane.md lists it as a plane metric. No H-entry measures it or claims rebind dominance or mutual-encounter inertness. components-98bc's 0.126 bits/body birth floor is properly cited. Novel and on a named board bottleneck ("fitting 10⁹ in 8 GB … decided by distinctions created per game-second"). Fits PRINCIPLES #24 ("the memory floor is information") and #6 ("influences below one quantum accumulate" — confirmed quantitatively: the accumulation lives in the field, not per-ship scars).

## Why silver, not gold

The run's single deliverable to `b-h-live` — the headline rate — is wrong by 460× (10³ text slip on top of a 2.2× instrument bug), the stored JSON was never regenerated after the author's own fix, and one term verdict ("player nil") flips at the corrected rate. By the lab's own standard (a headline the log contradicts), the run loses the gold grade even though every qualitative conclusion survives correction.

**The one experiment for gold:** fix the Newton sign (or replace §2 with the brute force), regenerate the 10⁹ table and dossier numbers from rate = 1.30×10⁻²/body/orbit, and reconcile JSON, dossier and abstract — under an hour.

## What the author missed

- The control asymmetry: a dense-scan control existed for P1 but none for the corrected P3, so the number that decided the headline had exactly one instrument — the one fixed in a hurry after two prior bugs. The lens note says it ("numbers agreeing because they share assumptions") and then repeats the failure class it names.
- No code path regenerates the headline table, so the 10³ slip had nowhere to be caught.
- "Player nil" is rate-dependent; at the true rate the player's input is co-dominant with rebinds, which matters for how `b-h-live` bounds H_live (player input is a floor, not a rounding error).
