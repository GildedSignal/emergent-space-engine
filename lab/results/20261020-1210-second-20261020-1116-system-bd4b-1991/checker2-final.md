Working...
Check complete. **Grade: gold** — written to `check2.md`, with one confirming note added to the run's wiki page.

**What I did:**

1. **Reproduced bit-for-bit.** Applied `work/patch.diff` at base `caa2a43b` (its `base-patch.diff` is byte-identical to bd4b's committed patch). All four arms regenerate: digests `b42da477…`/`8c242b02…` and replay digests match **bd4b's stored record on its branch** (not just self-consistency), refused 0, mints 23/137, 12,465 B/mint, and every span number in the dossier matches the JSONs. One hygiene find: the shared target dir held the first checker's probe binary; I verified its JSON path equals the patch-only build (span identical, only µs timings drift), so two independent builds confirm.

2. **Predictions.** Pre-registered with a kill criterion; mtime ordering supports written-before-run. P2 held; P1/P3 failed informatively (honestly reported — the failures *are* the result); P4's "never-read ≈ 0" half also failed but is phrased as "held and sharpened" — generous, though the number is disclosed.

3. **Attacked beyond the author's domain.** Held-out seeds 4–5: structure identical. A 50 s arm (3× mints, **147 re-mints**): medians unchanged, and it exercises the plan control the author wrongly said was "never exercised" (30 s seeds 2–3 already have re-mints; estimate error ≤ 18% of the walk, immaterial at 10⁻³ coverage). `--members 1200` is bit-identical to 400 — the bench clamps at 400 (`mod.rs:40`), so the decade-up case is the instrument's limit, not author laziness.

4. **Code-verified the CPU-lever kill:** `step_for` (step.rs:75) reads `period()`/`duration()` (`increments[1]`, a full-arc compile sum, orbit.rs:676) for every interval — a walked-span-only compile cannot answer it.

5. **Novelty:** closes the published page's open directions 1–2; no prior span-coverage measurement in HISTORY. Same shape as gold components-4643: kill one lever, size another, nothing new to build.

Tree restored clean; only `check2.md` and the bracketed wiki note added.
