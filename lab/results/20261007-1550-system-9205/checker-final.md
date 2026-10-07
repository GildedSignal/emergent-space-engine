Working...
Check written. Summary of what I found as checker for run `20261007-1550-system-9205`:

**Grade: lead** — the measurement question is good, but the instrument is broken, so the numbers don't back the claim.

**Reproduction**
- `belt_cadence.py hard` regenerates `belt_cadence_hard.json` **bit-for-bit** (29.6 s).
- The belt command **cannot** regenerate `belt_cadence.json` — the shipped `main()` runs one scene with no `winsec` variants; the stored 27-row JSON came from an earlier driver (script mtime sits between the two JSONs, undisclosed). Overlapping rows and all six `winsec` rows reproduce exactly when I reconstruct the driver, so the numbers are faithful to the shipped physics code.

**The decisive finding** — the replica's Kepler layer is wrong:
- `init`/`drift` build tangential speed `(1+e·cosν)·h/r²` where Kepler needs `h/r` — factor `(h/r)²≈0.44`, exactly the measured 0.29 vs 0.66.
- The intended "a=2.35, e=0.05 belt body" actually sits at a≈1.27, e≈0.80; the hard scene at e≈0.82–0.96 with perihelia 0.08–0.29 (its claimed d_min≈0.6 planet conjunctions never occur — min distance ≈1.5; the "fixed-cadence divergences" are under-resolved unintended plunges).
- `drift(0)` changes v by 0.28 — the "exact Kepler drift" isn't exact; after 10 orbits the map vs RK4-on-the-same-state differ by 10.6.
- Killer control: with R_win=1.5 (window never opens, **zero kicks**) the Δϖ error is 0.76% and per-seed ϖ rotations match the truth's to ~1% — the "secular exchange" the whole ladder judges is a drift artifact, not the planet.
- Because `init` and `drift` share the wrong map, the ladder converges internally — the trap that made it look valid, and the unexplained "Jacobi broken" symptom the author disclosed but didn't chase.

**Also found**: "winsec diverges at every scene" contradicted by its own reproduced 2.44 row (6/6 pass); hard-scene truth noise understated 10× in the dossier (7.1×10⁻³, not 10⁻⁴ — that ladder sits at its noise floor); dossier R_w=1.2 vs code's hard-coded 1.9. Predictions were genuinely written pre-run and honestly reported wrong — good process, wrong instrument.

Only `check.md` was written in the run folder; everything else ran in `/tmp/chk-9205`.
