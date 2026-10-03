Grade: silver

Abstract for the integrator: the claim reproduces bit for bit (`python3 kicks.py`, 61 s shared container): at the same behaviour band (1% apsidal precession, |Δe|≤1e-4, 200 orbits), plain symmetric leapfrog needs the fewest kicks per orbit in a free-drift engine — y4 3.0× more, y6 2.3× (my corrected minima; the author's 2.25×/1.75× came from sparse grids). The ordering holds at every band down to the probe's ~6.5e-5 floor and at e=0.6/J2=1e-2, and nothing passes at e=0.9. This kills the "higher-order splits" candidate under focus item 1 before a builder window is spent, and redirects `q-correctors` to zero-kick correctors. Not gold: the held-out prediction P2 failed in direction, and the "directly adoptable" integer table (8, 32) is wrong — true minima are 6 and 29.

## Reasons

1. **Reproduced.** `python3 kicks.py` in a clean tree (patch.diff is empty, no tree edits): all 81 grid rows identical to `kicks-out.txt`, positive control 0.0001, negative control 0.1254. Runtime 61 s vs claimed 44 s (order only, shared 2-vCPU container). Oracle independently re-derived: ϖ̇ = Ω̇ + ω̇ = (3/2)·n·J2·(R/p)² at i = 0, so 3π·J2·(R/p)² per orbit — the author's 3π form is right and Vallado's 6π is the node-referenced singular limit, as claimed.

2. **Pre-registration.** mtimes: predictions.md 18:47:28 < kicks.py 18:50:25 < kicks-out.txt 18:52:12. Predictions written first; no undisclosed redefinitions; falsifications reported honestly. P3/P4/P5 held; P1 falsified; P2 (held-out) falsified in direction. Gold requires the held-out predictions to hold.

3. **Attacks (my own, five):**
   - **Sub-grid gap (decisive defect).** The author's grids start at the first candidate (8 at e=0.1, 24→32 at e=0.6) with only k=4 as negative control. Contiguous sweep: lf2 passes at **6** kicks/orbit at e=0.1 (rel 3.9e-3; k=5 fails at 2.3e-2) and at **29** at e=0.6 (rel 7.75e-3; k=28 fails at 1.09e-2), stable at 100/200/400 orbits. y4@6 kicks and y6@7 kicks fail. So the ordering is safe — indeed stronger (3.0×/2.3×) — but the shipped integers are wrong, and the dossier sells them as "directly adoptable as compiled per-class kick counts". Adopting 8 where 6 passes wastes a third of the low-e kick budget.
   - **Band sweep.** Min kicks at rel ≤ 1e-2/1e-3/1e-4, e=0.1: lf2 6/7/10, y4 18/24/24, y6 14/42/56. The ordering never flips; the gap widens as the band tightens. The probe's error floor is ~6.5e-5 (y6 dense control saturates there), which bounds what this probe can discriminate.
   - **Extreme e=0.9.** Nothing passes at ≤ 192 kicks/orbit (best rel 3.6e-2), energy error ~1e-3 for all methods. Uniform stepping — composed or not — is dead there; the probe's regime is e ≲ 0.7. Not an inversion, but a regime bound the dossier's "what would make it wrong" does not name.
   - **Combined held-out e=0.6, J2=1e-2.** Same ordering and ratios (first passes 32/72/56 on that grid) — P3's ε-independence extends to the combined case.
   - **Horizon stability** of the corrected minima (above). One caveat worth noting: y4's rel is non-monotonic in k near the band edge (0.068 → 0.093 between k=8 and k=12 at e=0.6); if the integer table is adopted, boundary cases deserve a median over windows, per the rung-writing lessons.

4. **Novelty.** No H entry measures composition order against the plain split at equal kick counts: H0190 measured kick counts for tides/J2 (K1 32.5, K3 3.3·10⁵) but not compositions; law.md already fixes the symmetric split without measuring the alternative; the reference file's Forest–Ruth steal (Children of a Dead Earth) is exactly the transfer this probe tests. New in-repo, and it deletes a live candidate on the board's focus list.

5. **Goal fit.** Focus item 1 ("fewer kicks per orbit at the same behaviour (correctors, higher-order splits)"); HANDOFF's "the bigger lever is fewer kicks (GLM `q-correctors`)". Respects "measure before claiming" (10), "a failed experiment kills that configuration, never the method" (9), "floats may explore; only integers decide". Cost to adopt: negative for the kill (a queued branch dies before it is built); the corrected table (6/29) is adoptable as compiled per-class counts in one step.

## The one experiment that would make it gold

Rerun `kicks.py` with contiguous k grids (k = 1..40 per method) to fix the integer table — my 6/29 already confirm it — plus the dossier's own named case: the same probe with r9's averaged tide as the kick, so the ordering is shown on the engine's actual kick layer, not an impulse stylization. Pre-register the minima this time.

## What the author missed

- The grids have untested gaps below their first pass, so the "measured smallest integers" (8, 32) were never the smallest (6, 29) — the exact defect the Simon/satisficing lesson warns about, committed while stating it.
- The "H0190's 32 drops to 8 at e≤0.1, a 4× cut" redirect conflates experiments: H0190's 32.5 was Moon/Sun tides on a low orbit (K1), not this J2 probe at e=0.6. The cross-experiment mapping is a hypothesis, not a measured gain; with the corrected integer it would read 5.4× anyway.
- The ~6.5e-5 measurement floor is visible in the author's own dense control (1e-4) and bounds every tight-band statement.
- e=0.9 kills all uniform-grid methods in this probe; the stated falsification regime ("error not pericenter-dominated") omits that the probe itself stops answering there.
- Lesson 5's "a kick costs 29 µs, 15 in rebinding" is unsourced in the run folder.
- The correctors that the dossier redirects to were argued, not measured — by the author's own admission; that next probe, not this one, is the gold candidate.
