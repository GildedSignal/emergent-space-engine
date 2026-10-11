Grade: silver

**Abstract.** Claim: the view's light-cone gather (law.md §Observation, representation.md §2) omits gravitational arrival-time delay, so bodies within ~60 M of a hole render 1–97 px wrong; no gate or rung covers it; the fix is one arrival(b) column in the doll's memo. I reproduced all four modes exactly, cross-checked the oracle against an independent r-space quadrature (shape 1e-7, time 1e-4 on the columns the scenes use), and varied phi0: the claim and the r_e ≥ 20 rows survive; the delay-memo fix collapses error 40–150× at r_e ≥ 60, below floor. But the oracle's arrival time is under-converged for nearly-radial photons (up to +24 M), making the ISCO row's err_fix (9.9e-3, "14×") an artifact — refined: 9.6e-2. Adoption (one memo column + a correctness r6) is one step; the strong-field quantification needs one rerun.

## Reproduction

`attack.py calibrate/sweep/converge/newton` reproduce `results-*.json` and the dossier table exactly (err_phase medians 1.40e-1/4.85e-2/7.44e-3/1.53e-3/2.35e-4/2.37e-5 at r_e = 6…1000; controls 7.4e-7 pass, nodefl 3.4e-5, noretard 5.9e-3; Newton fails 0/0 at β ≤ 0.99, 3–8/399 at 0.999, wrong-derivative 399/399, frozen seed 9/399). Timeline consistent with pre-registration: predictions.md 19:44:10 → attack.py 19:47:21 → results 19:50; patch.diff empty (no tree edits). Design quotes verified verbatim: law.md:53, representation.md:56-57; B3/B16 gate deflection angle only; B7 clock rates; B19 Kerr geodesics/clocks; r5/r6 named in representation.md §7 with no file in lab/rungs/, and r6 as sketched gates cost, not truth. Pixel conversion 1.45e-3 = 90°/1080 ✓.

## Held-out predictions

P1–P7, P9, P11 held (pixel floor crossed between 20 and 60 M: 5.1 px → 1.05 px). P8 and P10 partially failed, disclosed honestly as failures — no spin. P10's failure at β = 0.999 (1–2% of frames, all at closest approach, degeneracy not staleness) is the bottleneck-5 worst case and the bracket fix is sound (G strictly decreasing ⇒ unique bracketed root; I checked G′ = −1 − û·v is correct).

## My attacks

1. **Independent oracle** (r-parameterized Simpson quadrature of dt/dr, dφ/dr — different parameterization and integrator): A_phi agrees to ~1e-7 for mid-b columns; delta_inf matches 4M/b + 15π/4b² to 2e-5 at b = 1000. Trajectory shape validated.
2. **Found: A_t under-converged for nearly-radial photons.** The arrival-time linear interpolation over the last giant step inflates t for out-family columns with α ≲ 0.13 (b ≲ 0.15 r_e): +14 M at (r_e=60, b=1.22), +22 to +24 M at (r_e=1000, b=20–77), +1.1 M at (r_e=6, b=0.15), confirmed against both a fine φ-RK4 (dφ=2e-4) and the corrected quadrature. Consequence per scene (coarse → converged table, dφ=7.5e-4, 4000 α): r_e=6: err_phase 0.140→0.166, err_design 0.085→0.116, **err_fix 9.9e-3→9.6e-2 (10×)**, delay 30.9→38.6; r_e=8: err_design 0.090→0.061, err_fix −9%; r_e=20: err_design −21%, err_fix 0.40; r_e=60 and 1000: stable (<1%, 6%). The dossier's convergence guard ("median refinement convergence 3.4e-6") was measured only at r_e = 8/60 and only on err_phase/err_design — converge mode never diffs err_fix, and r_e=6 was never refined. So the ISCO row's "collapses the error 14×" is not regenerable at convergence; direction unchanged (the per-family memo fails at r_e ≤ 20 even harder than reported), and P8's "held at r_e = 6" is also an artifact — under a converged oracle P8 fails at r_e = 6 as well.
3. **phi0 robustness** (0.3/1.0/2.2/4.1 at r_e = 6/20/60): err_phase medians stable (6: 0.135–0.198; 20: 0.0073–0.0082; 60: 0.00141–0.00154); image medians unchanged. Not a phase artifact.
4. **The design-text reading.** The strongest counter-reading is that "the observer's past light cone" means the curved cone compiled into cell geometry (representation.md's min-plus shift-and-OR cone is flat; but docs/reference/original-research-report.md:53 says "Fine arrival through gravity is delegated to a certified metric/propagator query"). The author addressed implementation-ahead-of-text but not this reference text. Even so, the design's own Observation section names no delay mechanism and no gate judges it, so the hole stands as a spec hole; the ambiguity is worth one sentence in law.md either way.

## Novelty

Not previously found. H0183 gave the GR oracle a Shapiro quantity (two methods) but nothing ever applied it to the view's gather; the 1 October red-team (B16) covered only the deflection angle of a static-memo. The "Shapiro appears nowhere in docs/" parenthetical is literally false — docs/HISTORY.md H0033–H0036 mention it (old codex law-lab lineage, GEO-N tick binning, "no Shapiro magnitude is frozen", a different subsystem) — a wording error that if anything confirms the author's substantive point: no text decides the view's delay. Attack 2 (B8 unpassable by construction on formation scenes) correctly chains the measured gold 20261006-0346 to the B8 scene set; not re-measured, disclosed.

## Goal fit

Principle 30 ("what really matters is navigation, knowledge and dynamics those need to be perfect") — the sky is the navigation instrument and the AI's perception is the same gather; both are wrong by degrees exactly where the player is meant to feel GR. Not a speed bottleneck (truth, not gain) — legitimate for the red-team lens, ranked by player likelihood as the lens orders. The proposed adoption (one memo column compiled from the light tubes the doll already compiles; r6 frozen as a correctness rung with the author's criterion and both planted negatives) is one step and violates no principle.

## The one experiment for gold

Rerun the sweep with a converged arrival time (finer dφ plus quadratic or step-limited final-step interpolation; verify dt against the independent r-space quadrature at all sampled b), report the r_e ≤ 20 rows from it, and re-derive P8 — then prototype the image-resolved delay memo at r_e = 8 to show it reaches the floor where the per-family memo provably cannot. The central claim and the r_e ≥ 60 fix already stand; this closes the record.

## What the author missed

- The arrival-time interpolation bug and its 10× corruption of the ISCO err_fix row (the record's only non-regenerable number).
- converge mode never diffs err_fix, and never refines r_e = 6 — the convergence claim was over-generalized from two friendly scenes.
- "Shapiro appears nowhere in docs/" is false as stated; the H0033–H0036 mentions are a different subsystem and should have been cited as supporting evidence instead.
- The reference-level counter-reading (original-research-report.md:53, fine arrival delegated to a metric query) — the integrator's likeliest reply; pre-empting it would have made the design-text hole airtight.
- Pixel floor assumes vertical 90°/1080; horizontal would halve rad/px (strengthening the claim) — worth stating the convention.
