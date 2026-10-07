Working...
Check complete. `check2.md` written; nothing else in the run folder touched.

**Grade: silver.**

What I did and found:

- **Reproduced** every dossier command in a clean tree (patch.diff empty — standalone bench). Core rows match bit-for-bit: corr ε=1e-6 → 0.0075 compiles/kick @ 9.18e-7 (e=0.5), 0.077 @ 6.12e-7 (e=0.9); rand 0.002 @ 8.14e-7; Peters 5.02 @ 1.11e-4. Cost split reproduces within shared-runner noise (compile 5.3 µs = 36% of the 14.8 µs rebind tail). Three quoted rows mix the pre-safety-factor code's runs (≤1.25× off, same verdicts).
- **Verified in source:** `ShapeKey = {k, compactness}` — no p, so p-only kicks genuinely hit the shape memo; the C correction is real (scan ⇒ C≈147 at e=0.9 vs ≈0.33 at p=20; global C breaks the floor 89×), correcting law.md line 35's adopted single-C rule.
- **Two adversarial failures of the delivered rule:** (1) the *both-axes* kick — the realistic (ΔE, ΔL) shape, in the bench as `plane` but never run by the author — breaks the 10⁻⁶ floor 1.6× at e=0.5 at every ε from 1e-7 to 1e-5 (mixed partial missing from c_est); (2) a 10⁵-kick e-walk into the separatrix breaks it 57× (the tested n=10⁴ stays bounded; e=0.99 can't even arm — the crate refuses).
- **Timing honest:** predictions.md (06:31:26) precedes scan (06:32:38) and streams (06:33:27); P7's misread disclosed.

Gold leg was "premise wrong" (constant C) — that stands — but the replacement as delivered doesn't hold the floor on the game's actual kick shape, so it's exactly one named experiment (mixed second difference + separatrix guard, rerun plane and 10⁵-walk) away from gold.
