# Predictions (written before the patched run; base arm already measured)

Base arm (shipped, `/tmp/base_arm.txt`): 88 exact periapsis states, E ∈ {1.001…1e6} ×
periapsis ∈ {1e2…1.6e10 M}. 56 fit, 17 refused `Range` (every one `inv-ok`: the big-int
invariants key exists), 15 refused `NoBoundOrbit` (every one `inv-err`: the invariants path
refuses too — the single-real-root stiff hyperbola, a representation limit, not arithmetic).
The fast path and `from_invariants` disagree on (periapsis, k) bits at 53/56 accepted
points (different scratch roundings; the fallback must therefore fire only on refusal).

The patch adds an invariants fallback at the two `Range` returns of `fit_key`
(env-gated: `ES_INVDOMAIN=0` restores shipped bits; default on).

## Held-out predictions (not tuned on)

1. **The 17 `Range` refusals all fit**, and every fitted key equals the `from_invariants`
   key bit for bit at the same point (the fallback calls it; predicts agreement, i.e. the
   control column flips to `same` exactly where the fallback fired).
2. **The 56 originally-accepted points are bit-identical** across arms: same keys, same
   residuals, same rows (the fallback never fires on the success path — by construction,
   but the prediction is the table diff is empty on those rows).
3. **The 15 `NoBoundOrbit` points still refuse with `NoBoundOrbit`** (the fallback does
   not touch non-`Range` errors; predicts the representation limit stands).
4. **Physics of the newly-fitted keys**: periapsis relerr ~1 quantum (≤ 2⁻⁴⁸-ish relative);
   clock gap E² readout vs the state's own E² agrees within the state's word floor
   (velocity word ve = −60 bounds expressible 1−vt² ≈ 1/E²: floor ≈ 2⁻⁶⁰·2E² — meaningful
   to E ≤ 1e4, gross check only at 1e5, meaningless at 1e6); residuals comparable to
   neighboring accepted points (≤ 1e-6 relative).
5. **Digest identity**: the space and universe suites pass unchanged in both arms
   (no scene on main reaches the `Range` wall — HANDOFF says the flights that hit it are
   lost today, so shipped scenes never fitted one).
6. **Cost**: the fallback is a cold big-int path firing only where shipped refuses; per
   fitted point ≤ ~1 ms (no throughput claim).
