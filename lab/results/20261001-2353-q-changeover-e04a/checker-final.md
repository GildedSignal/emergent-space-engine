Working...
Check complete. `check.md` written to the run folder; nothing else touched (the `force.rs` patch was applied, verified void, and restored).

## Verdict: silver

**Reproduced bit-for-bit** in a clean tree: truth, symba, mercurius, wh-fixed, wh-dense, soi-switch (every metrics digit identical, e.g. symba median `0.4115731539552824`, mercurius `0.468136196260884`), and janus.json identical. The B12 judge port matches `fit.rs`/`handoff.rs` exactly. Predictions were written before the decisive run (file times verified).

**What held:** the headline — no float changeover at 64 kicks/orbit reaches B12's 0.2 in this replica; mercurius's 1.7 switch events/pass with bounded 2.3e-5 max error; TRACE-roundtrip vacuity (my independent reimplementation ≈ wh-fixed, errors O(0.1) pass at any eps); the JANUS reversibility result (position-only mid-state switch bit-reversible, velocity-dependent not, 30× invariant drift).

**What held it to silver:**
- Two headline held-out predictions failed (symba ≤0.1 → 0.41; trace ≤0.2 → 0.74), plus wh-dense and the truth noise level; the moon case never ran.
- The stored trace row is **not regenerable** — both stored trace files are the roundtrip variant, but the shipped `Trace` class is the Jacobi variant (the r4-v3 build smell, smaller and disclosed).
- Truth-control claim overstated: max 6.7e-8, not ≤2e-11.
- Kill #2 tested a **cumulative**-error ratchet (check vs initial C0 → permanent floor-stepping). My per-step variant stays cheap (28.6 retries/pass) yet still fails at 0.59 — TRACE dies on accuracy, but not by the dossier's mechanism.
- The 600×-fewer-events claim is queue accounting; total force-evals per pass are 2053 vs symba's 1681 — equal work, not a deletion.

**My adversarials strengthened the kill:** all checked symba exclusions are error-driven (truth stays at r≈1–5); at 0.08 R_H (below the deepest shell — the lens's named regime) the symba replica corrupts outright (err 77); at μ=3e-6 symba ≈ no changeover (expo ~5) while mercurius holds 2.7e-8.

**To gold:** run the shipped plane's phase-stepped cascade and the per-step-Jacobi TRACE on these same frozen 32 seeds.
