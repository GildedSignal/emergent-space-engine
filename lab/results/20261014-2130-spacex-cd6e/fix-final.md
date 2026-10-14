Working...
regen.sh exits 0 in ~4m51s and regenerates every dossier number from shipped code + the patch: closed-forms vs quadrature (I2 3.6e-16, t 2.2e-30, τ 2.3e-17, adv 4.9e-31), shipped read wall 2496–4632 ns p50 4040 flat in e, compile wall 5.0–262 µs, and the full-grid walk-vs-closed-form check that was crashing.

**Fix:** 3 lines in `verify.py` (159–161) — the exact `None` guard the author's working subsample `verify_fast.py` already had: `invert_t` returns `None` when the target time sits marginally outside the `[t(1e-12), t(π−1e-12)]` bracket (the u = 0.5 rows, where the walk's float half-period and the closed `t(π)` straddle the bracket edge at high e); such rows now count once in the denominator and skip, instead of crashing on `None - mpf`. regen.sh itself, the patch, and all other steps were already sound (verified: `git apply --check` clean, guard prevents double-apply).

**The full-grid result, now on the record:** 825/828 agree; worst rel errors ψ 1.06e-8, r 4.3e-9, τ 4.7e-11, adv 4.5e-6 (the known weak-field corner) — the dossier's point (a) under "what would make it wrong" is answered: the subsample's agreement holds on the full grid.

Claim: regen.sh is fixed by mirroring the author's own None-guard into the full-grid verify.py, and it now regenerates every dossier number end-to-end (exit 0, ~5 min), with the full-grid check confirming the subsample — 825/828 rows agree, worst ψ/r/τ errors at 1e-8/4e-9/5e-11.
