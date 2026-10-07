# Predictions (written before the decisive run of twin.py)

Run: second author on 20261007-1032-taleb-ab03. Decisive experiment = the checker's named one
(the secular-shadow twin: same birth states under the Giant's exact double-averaged ring field,
same integrator/windows/floors, residual bits vs the full run at 5 and 20 yr), plus three
companions needed to read it: (B) synodic-window re-analysis of the full run, (C) clone
sensitivity at the tube's u32 birth quantum, (N) twin-noise controls (dt/2, 128-node table).

Pre-registered domain: double-averaging is valid only for non-crossing orbits, so the twin
claims cover belt bodies with birth apocentre Q0 < 4.64 AU (Giant pericentre 4.69 minus 0.05).
Crossing bodies are counted separately as the encounter regime. Smoke tests done before this
file: harness runs; full/orbit regenerates the shipped 1-yr row exactly; a coarse table showed
the twin's own E column can be polluted by table numerics (hence control N).

1. **Regeneration.** `frozen` rows (belt, orbit window, hyper→144) match shipped hlive2.json at
   1/5/20 yr to <0.01 bits; belt hyper count on this seed = 0 (the shipped 94 hyper are
   crossers). If any belt body is hyper, regeneration still holds via the 144 forcing.
2. **Twin noise (N).** dt/2 and 128-node controls at 20 yr read ≤ ~18 (E), ~10 (L), ~8 (w), ~8
   (M) bits mean. Any column whose residual is not ≥3× above these is unreadable below the
   twin's own numerics — I will not claim absorption on it.
3. **(A) residual full−twin, secular belt at 20 yr.** E: ≈ the full column (~36 bits; variance
   explained < 0.3 — the twin cannot see synodic leftover). L: ≈ full (~24; var expl < 0.5).
   w and M: ≤ ~12 bits mean, within 3× of control N, variance explained > 0.9 (the secular
   precession is exactly the averaged-field flow). Same shape at 5 yr with smaller w/M.
4. **(B) synodic window.** For the secular belt at 20 yr, E+L bits collapse ≥ 5× vs the
   one-orbit window (E from ~36 to ≤ 20; median |ΔE| from 4.3e-3 to ≤ 8e-4): the E/L columns
   are leftover synodic oscillation — deterministic machinery of (birth, shared ephemeris, t),
   not secular drift. Coverage ≥ 0.7.
5. **(C) clones.** dλ0 = 2π/2³² at 20 yr: total divergence ≤ ~12 bits mean, p99 ≤ 20, growth
   with t roughly linear (regular belt, no exponential divergence). d a0 = 1e-9 AU: same
   magnitude. Amplification ≤ ~10³ over 20 yr.
6. **Resonant minority** (secular domain, |a−res| < 0.05, n ≈ 17,000): w/M residual ≥ 2× the
   proper belt's (resonant terms survive double-averaging; variance explained on w < 0.8);
   clone p99 ≥ 2× proper.
7. **Crossing minority.** ~150–350 belt bodies (0.2–0.5%) have Q0 ≥ 4.64; they carry the
   encounter scars (discrete steps, 144-bit individuals) — the original dossier's tail.
8. **Verdict shape.** Irreducible belt H_live at 20 yr ≈ the clone level (≲ 12 bits mean, and
   reducible to ~0 by evaluating the birth program with ~10 extra bits of precision): the store
   keeps the birth program + shared ephemeris + secular machinery; the ~100-bit frozen figure
   decomposes into ~60 bits synodic machinery + ~49 bits secular program + small residual.

**Kill criteria for the absorption claim.** If (A)'s w/M residual for the proper belt exceeds
3× control N with variance explained < 0.9, the secular program does not absorb even the
regular belt and the ~100 bits stand as per-body cost — I report a clean refutation. If (B)
does not collapse, the E/L bits are real secular drift (resonant diffusion) — same conclusion.
If the clone divergence grows super-linearly in t (chaos), the birth→now map is not smooth and
recompute-from-birth dies at these horizons regardless of the twin.
