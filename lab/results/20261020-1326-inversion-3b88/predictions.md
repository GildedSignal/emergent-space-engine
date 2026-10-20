# Predictions — 20261020-1326-inversion-3b88 (inversion lens)

Question: the newest gold (20261020-0036-scout-7076, kick-cadence) leaves B13's step-9
(512/orbit) failure "one anomalous row (`inf`, unattributed)". The `inf` is the judge's
code for a law refusal (`assist.rs` line 125 maps `None` to INFINITY), and the trace
shows `lost=1 refused=0`: the plane **killed** one ship at 512 kicks/orbit that survives
at 256 and 1024. The ladder's design assumption — finer cadence is weakly better
(error ~ n⁻², B17's smooth law) — is non-monotone here. What is the mechanism?

Cases held out (not tuned on): the failing seed's geometry and its errors at the
bracketing octaves.

- **P1 (identity):** exactly one of the 64 judged seeds dies at step 9, the same seed
  passes at steps 8 and 10, and the other 63 rows are within noise of their step-8/10
  values (print-only per-row census, `ES_B13_ROWS`).
- **P2 (where):** the death happens during the flyby, inside the planet's sphere of
  influence (not after exit, not at the star, not at the system's edge), within ~2
  planet radii of the planet's centre.
- **P3 (knife-edge vs resonance):** the failing seed's reference closest approach is in
  the grazer tail of the 64 (among the smallest few, < ~2 planet radii). If instead it
  is an unremarkable seed (say > 5 radii), the death is a cadence-grid effect (a real
  fine-side non-monotonicity of the law), which is the stronger finding.
- **P4 (nothing else special):** at steps 8 and 10 the same seed's ΔE/ΔL errors are
  unremarkable (within ~10× of that octave's worst row) — survival, not accuracy,
  separates it.

Kill criterion for the rung of this probe: if the census shows the row is not a death
but an `observe` refusal, or more than one row fails, the framing above is wrong and the
dossier reports what it is instead.
