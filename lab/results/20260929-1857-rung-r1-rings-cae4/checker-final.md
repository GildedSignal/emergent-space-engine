Working...
Check complete. Summary of what I found and delivered:

**The author's run never happened.** `metrics.json`, `dossier.md`, `predictions.md`, the picture and `run.log` are all absent; `author-final.md` says "Deadline exceeded". The delivered script crashes at startup on every configuration — `oracle.bound_constants` calls `math.sqrt` on numpy arrays, and the author's own cached `.pyc` (from its session) contains the identical code, so the author hit the same wall. A second crash (`NameError` on dead code) blocks `square`.

**Reproduction** (in `/tmp/r1check`, author folder untouched, fixes documented in `check.md`): all seven configs run. `lab/verdict.py` on my `metrics-check.json` gives:

```
Verdict: PASS; binet-m16, binet-m32 passed every criterion; killed: binet-m8, river-m16, river-m32
square, tiltonly (negatives) fail 8 of 9 criteria — the rung discriminates.
```

**Spec deviations found and corrected** (all loud, none silent): photon-capture cases were run as massive particles (`lightc` built, never used) — under the rung's light model all five ring configs classify capture **0/10 wrong**, not 2; the precession gate used 1% of the full 2π angle instead of 1% of the advance, which alone flips binet-m8 from pass to **fail** (0.984); `river_run` never counts crossings (0.0 printed, true value 1.0 — itself diagnostic); the ISCO lanes stop after ~2 cycles instead of 100/50 orbits (re-run at full length: binet still correct, river still fails); square/tiltonly never terminate without iteration caps.

**Oracle verified** line-by-line against the Rust sources and numerically (author's RK4 at 1e-11, my independent RKF45 converging onto the port, series agreeing to the known 2PN term, exact closed-form spot checks). Sampler reproduced identically from the rung text.

**The physics result for the integrator:** Binet rings at m=16 hold every behaviour gate — precession 0.996, period 0.996, deflection 1.0, capture perfect, ISCO correct, exact cycle repeat at 1e-12 over 10⁴ cycles — at **38 events per radial cycle, ~10–20× fewer than the 350–700 fixed steps** the board cites. River rings die structurally: at the first edge past periapsis the continuum A² is +5.8e-5 but frozen-β gives −6.9e-4, so the rung's own reflection rule cages the orbit at r≈59 against a true apoapsis of 151 — a configuration kill, not a method kill (per principle 9).
