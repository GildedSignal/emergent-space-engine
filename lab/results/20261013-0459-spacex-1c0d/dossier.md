# Dossier — the far-field `Range` wall deleted by an invariants fallback

- **Claim.** The shipped fit's far hyperbolic `Range` wall (a fast flight far from the star is lost) is deleted — 11 of 14 refused grid points now fit, bit-identically everywhere the shipped path already succeeded — by a 20-line fallback that re-derives the key from the state's own invariants (`E² = lapse²/den`, no cancellation; `L` a state word product) through the already-shipped exact big-int cubic; what remains is one honest wall (the stiff single-real-root hyperbola, both paths refuse) plus two disclosed anomalies the checker must adjudicate (root selection at stiff far corners; a gap-column disagreement at high E that predates the patch).

## Bottleneck

`high-gamma-clock`, open limit in HANDOFF item 1: "a hyperbolic key is refused (`Range`) when its periapsis is above ~2.7×10⁸ M even at E = 3: a fast flight far from the star is lost". Wiki open direction 2 names the fix: "build the key from invariants … where the state→key cancellation bites". This run builds it. Gain: a whole refusal class deleted (not a speedup); cost: ~20 lines in `fit_key`, zero on the success path (fires only where shipped returned `Err`).

## Evidence

All from `regen.sh` (Linux/x86 shared runner; grid = 88 exact periapsis states, E ∈ {1.001…10⁶} × periapsis ∈ {10²…1.6×10¹⁰ M}, velocity words at 2⁻⁶⁰; the state's own Scalar E is the oracle, per the code's identity `E² = lapse²/den`).

- **Base arm** (`ES_INVDOMAIN=0` on the patched tree = shipped bits): 56 ok, 14 `Range`, 18 `NoBoundOrbit`. Every `Range` point has a working `from_invariants` control key ("inv-ok"); every `NoBoundOrbit` point has none — the stiff hyperbola is a representation limit (single-real-root cubic), not arithmetic.
- **Fallback arm** (default on): 67 ok, 0 `Range`, 21 `NoBoundOrbit`. The 56 originally-accepted rows are **bit-identical** (diff of matched arms touches exactly the 14 refused rows; construction guarantee — the fallback only enters at the former `Err(Error::Range)` returns — confirmed by measurement). 11 formerly-`Range` points fit; 3 (E ≥ 10³ at periapsis ≥ 10⁹ M) convert to `NoBoundOrbit` at the **compile** stage: `Passage::compile` of the very invariants key refuses (`far_diag` isolates the stage) — the wiki's "it compiles" was measured on a different grid; at these corners it does not.
- **Key agreement**: at sampled new points the fitted k equals the control `from_invariants` k exactly (kdiff = 0 at (1.5, 10⁹), (2, 4×10⁸)); periapsis differs by ≤ 5×10⁻⁹ relative (the fallback and the probe's control form `L` through one differently-rounded product).
- **Physics of the new fits**: at periapsis ≤ 2.7×10⁸ M, peri_relerr = 0 (the fit recovers the state's own turning radius exactly, as the shipped path does at its accepted points) and residuals ≤ 10⁻⁹ relative. **At the far corners** (E ≳ 1.1 with periapsis ≳ 4×10⁸ M), the fitted periapsis disagrees with the state's vr = 0 turning radius by 0.39–1.00 — and the control key does the **same** (`far_diag`: fit and control both put (100, 4×10⁸) at periapsis ≈ 4×10⁴ ≈ r/(E²−1)): the two shipped root-selection predicates agree on a far root there. Not introduced by the patch (shipped refused those points outright); unresolved here; needs an exact-GR turning-radius oracle before adoption is signed.
- **Gap column anomaly (predates the patch)**: the clock-oracle column (`E² = tn/d`) disagrees with the state's `E² = lapse²/den` by up to 1.01×10⁻² at E = 100–1000, far periapsis — **identical values in both arms**, so not a fallback effect; my probe cannot decide whether it is probe-oracle imprecision at high E or a shipped gap defect (the flight record — γ 2,056 at 1.3×10⁻⁵ — suggests flight keys avoid this corner). Handed to the checker with the anomaly named.
- **Digest identity**: space suite 63/63 and universe plane digests 6/6 pass in **both** arms (the fallback never fires on shipped scenes — they never fitted a wall point, which is why the flights were "lost").
- **Cost**: the fallback is the cold big-int cubic, firing only where shipped refused; whole grid (88 points, both arms) runs in < 5 s.

## Predictions

`predictions.md` was written before the patched run. Held: #2 (bit-identity — exactly the 14 refused rows changed), #3 (the 18 `NoBoundOrbit` stand), #5 (suites pass both arms), #6 (cost). Partially held: #1 — 11 of 14, not 14 of 14; the three misses fail at `Passage::compile`, which prediction 1 did not model (it modeled the fit stage only). Not settleable this run: #4's far-corner physics (the root-selection anomaly above dominates peri_relerr there; at peri ≤ 2.7×10⁸ it held with residuals ≤ 10⁻⁹).

## What would make it wrong

The far-corner root selection: if the exact-GR turning radius at (E ≥ 1.1, peri ≥ 4×10⁸ M) is the state's r (my reading of vr = 0), then the invariants path's exterior-interval predicate picks a wrong root there and the fallback would fit wrong orbits at exactly the corner it was built for — a checker must adjudicate with an independent oracle before merge. The gap-column anomaly, if a shipped defect, is a clock bug independent of this patch.

## Cost of adoption, fit with PRINCIPLES

~20 lines in `fit_key` + the probe examples; no law change (the fallback calls the already-frozen `OrbitKey::from_invariants`); env gate `ES_INVDOMAIN=0` restores shipped bits for bisection (delete the gate on merge). "A fix signals the wrong representation" (P19) cuts the other way here: the representation was right (the key compiles), the scratch arithmetic was the wall — "the cheapest compute is compute not done" (P1): refusing to lose a flight is not compute. Domain: one grid, one scene family, x86; not tested: a live settle flight through the wall (needs a plane scene aimed past 2.7×10⁸ M — the sweep's "fast flight far from the star" is exactly that, next run's probe), the M1.

## The lens

SpaceX's delete-first found the wall is already deleted in the codebase's own exact path; the run's value is the measurement that the fallback is free and bit-safe, and the two honest edges it surfaced (root selection, gap column). The lens may have under-weighted a red-team of my own probe oracle — the far-corner anomaly could be my construction, not the engine's; the checker's independent oracle must decide.
