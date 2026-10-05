# Independent engine judge

`xtask engine-judge` judges Claude's frame and hooks through their public APIs. It changes no engine, lattice or space source. The initial judge source/tolerance freeze is `078ab968`; the numerical oracle was subsequently refined without changing cases, denominators or tolerance bands.

Run from the specialist worktree:

```sh
cargo build --offline --release -p xtask
./target/release/xtask engine-judge --prepare-mutants
```

Compilation prepares the scratch controls before the tests. Every gate has a hard 55 s watchdog. Exit 0 requires every selected gate to pass. Use `--gates E3` (or comma-separated IDs) for a reproducer; E6 requires the prepared mutant binary. Mutable outputs are in `artifacts/runs/engine-judge/`; sealed review evidence is under `artifacts/evidence/engine-judge-20260930/`.

| Gate | Frozen requirement |
|---|---|
| E1 | All 6,480 checkpoint digests equal on macOS (4,320 elsewhere): 24 scenes, four seeds, Chronon/EventCore/MetalChronon on macOS, three insertion permutations, 1/4/8 kick threads; contacts and kicks must occur. Flat reduction also equals the bare lattice |
| E2 | Every member/sample in five independent release groups, both orders, one period: position within 3% of the nonlinear inverse-square oracle |
| E3 | Nine groups, both orders, ten periods: position and group shape within 1%; 3% at initial dr/R = 0.003 |
| E4 | Across 48 manual anchors, common-frame total momentum exactly equal; kinetic energy changes by at most one m*k² quantum |
| E5 | Handoff IDs unique, mass partition exact, active mask agrees with ledger, snapshots compose to the parent positions; two outliers leave in both orders |
| E6 | Scratch unmutated E1/E2/E8 controls pass; each of four isolated planted defects fails a gate. A timeout, panic or build failure is not a kill |
| E7 | Future state digests distinguish different frame clocks; an empty anchored scene remains legal |
| E8 | Independently accumulated sub-velocity-quantum drift settles exactly into per-body positions at seven arbitrary manual anchors, both orders |

The oracle is a symmetric composition of three velocity-Verlet maps, not RK4. Coefficients solve `2a+b=1`, `2a³+b³=0`; this cancels the cubic splitting error. Each case is computed at 1,024 and 2,048 substeps/sample. Their positions must differ by less than 1e-5 of each member's initial offset, and their centred group shapes by less than 1e-5 of the group radius. Failure of this check invalidates the behaviour verdict. Circular convergence and forward/backward reversibility controls are unit tests.

The E2/E3 position denominator is the larger of the oracle's current offset and the initial offset, with a one-unit floor. Shape compares deviations from independently mass-weighted group centres, divided by the oracle group's largest offset. Every case is retained in `behaviour-short.jsonl` or `behaviour-anchored.jsonl`. No 99% success threshold hides a failed case.

E4 reconstructs velocities in the pre-anchor axes, using the tube and the complete parent position. Angular-frame terms are exact in 2^-92 units; momentum uses those exact rational values. Energy rounds the reconstructed velocities once to 2^-48 and compares squared mass-weighted speeds in m*k² units. This is the free-fall model's kinetic invariant, not a claim of GR energy conservation. The check does not use `AnchorReport.dp` as its oracle.

The public World API requires strictly increasing IDs. Input permutations are inserted into an independent BTreeMap and normalized before construction; there is no engine insertion API to test. Different seeds are separate physical scenes: equality is required within each scene, not between different universes. The steppers are single-threaded; the thread gate exercises the frame's real kick threads.

Scratch mutations are prepared by `xtask/src/engine_judge/prepare_mutants.py`. Only the copied frame/tube/anchor/sparse-hook sources are changed. The epoch setter is delayed only for EventCore; the first tidal row is corrupted; per-body drift flush is dropped; only the sparse kick hook's revision bump is removed. Child gate output is saved per mutant. Scratch controls run the same binary with the mutant environment removed.

Machine lines include uptime, power, thermal status and swap. The supplied sandbox denies sysctl swap/load/hardware access and thermal queries; the output preserves those denials. No thermal or target-device performance qualification follows from these runs.

The supplied sandbox makes the worktree administrative index read-only. Commits use the permitted common object/ref store and `GIT_INDEX_FILE=artifacts/runs/engine-judge/index`. The integrator should refresh the normal worktree index with `git reset --mixed HEAD` before working here; the branch commits hold the complete changes.

## judge2 adjudication and E9 freeze

E1 and E3 retain every existing parameter and tolerance as **Newtonian behaviour tests**. E1's nominal 16c reference and E3's 0.244c reference are mathematical stress fixtures, not relativistic universes. The engine reads their tubes at compactness near 2^-40. Equality qualifies evaluation orders; E3 qualifies the Newtonian tidal approximation. Neither qualifies a Schwarzschild tide. No original scene or band is weakened or removed. A missing Metal device on macOS makes E1 UNSUPPORTED, never a CPU-only PASS. CPU comparisons still run and report their actual denominator; unavailable-device failures never count as mutant kills.

E9's requirements below are admitted after the cloud GLM red-team and independent checker (`20261001-1847-redteam-e9-f0b3`), plus the phase-2 kernel/checker records (`20261002-0539-redteam-fermi2-21db`, `20261002-0539-q-fermi2-tide-0dee`). The oracle-only falsifying probe precedes admission; no engine execution precedes the freeze. The immutable source freeze is recorded below; the sandbox denied the commit.

| E9 frozen requirement | Fixed value |
|---|---|
| Reference grid | Periapsis r_p/M = 10, 30, 100, 1,000, 10,000, 100,000, 1,000,000; e = 0, 0.3, 0.6. All 21 retained |
| Duration and samples | Ten proper radial periods (azimuthal proper periods for circles), 40 samples per period plus genesis |
| Members | Three independent 2D offset directions and their negatives; six bodies, pair masses 1, 2, 3, initial extent 10^-5 r_p; quantized positions and velocities initialize both implementations |
| Physics units | c = Q = 2^20, r_p = 2^40 lattice units, n = round(2^60 Q/(r_p sqrt(r_p/M)))/2^60, GM = n² r_p³. Actual compactness is recorded |
| Engine order | EventCore; on_orbit with inertial axes; anchors every eight epochs plus every observation to settle position debt. Symmetric members keep the origin fixed. Refused anchors, recentring or handed-out bodies fail the case; runtime errors invalidate the physics verdict |
| Position and shape | E3's 1% bands (the 3% exception remains exclusive to E3's initial dr/R=0.003). Same denominators, mass-weighted centre and worst member/sample; every case must pass |
| Oracle validity | Step halving 256→512 RK4 substeps/sample and finite-separation scale 1/16→1/32 must each change position and shape by <10^-5. Timelike normalization, axis orthonormality and orthogonality to reference velocity also <10^-5; invalid oracle means no physics verdict |
| Planted defects | Scratch sign/static tide defects must fail r_p/M=10^6 after its positive control passes (wiring only). Independent circular Jacobi GR tide must pass at r_p/M=100 and 10; replacing only its radial stretching by Newtonian 2w or the wrong-Riemann-sign w(γ²+1) must fail each radius. All use the same 1% band, samples, denominators and oracle checks. Timeout, panic, nonfinite result or invalid oracle is not a kill |
| Output | One JSONL row per case; full passed/failed radii separately for each e. The pass frontier is bracketed by tested radii, never interpolated. E9 stays FAIL if any near-field case fails |

The admitted source sets `E9_FROZEN`; its immutable source record must precede any engine execution (the commit is deferred only if the sandbox denies the index). E9 runs its full spectrum, the independent GR tide controls, then scratch positive/negative controls. `--gates E9 --e9-weak-control` runs only the three large-radius controls with identical bands and oracle checks; this subset never qualifies GR or the full E9. The GR controls compare a separate circular Jacobi integrator against geodesic-pair differences; they qualify discrimination, not an integrated engine. In proper-time units the parallel-frame radial axis turns at λ-rate 1, tangential acceleration is −w, and radial acceleration is +w(3γ²−1), γ²=(1−2M/r)/(1−3M/r). Only the tide eigenvalue changes in its mutants, so origin/clock/axes cannot cause their kill.

The float64 oracle derives its own Schwarzschild geodesic ODEs from the diagonal metric and Killing constants. Nearby geodesics begin at the spacelike exponential map of each local offset, with parallel-transported 4-velocities. Two opposite geodesics form a centred finite difference; the reference axes are parallel transported by the metric connection, not by engine tide code. Projection onto those axes removes a first-order shift along the reference velocity. Finite-separation halving checks the remaining nonlinear coordinate/simultaneity error. Factored inverse-power differences prevent cancellation of two galactic positions. The circular radial epicycle and geodetic rotation have independent analytic controls ([geodesic deviation paper](https://arxiv.org/abs/1508.06457)).

**Phase-1 limitation:** the public Frame API still builds its origin at Newtonian compactness, independently of c. E9 therefore judges the public frame's full local evolution against the physically scaled Schwarzschild reference; a near-field discrepancy can include reference motion, clock convention, transported axes and tide. It cannot isolate a GR tidal coefficient until the engine exposes true parent (M,c) units. This is evidence for phase 2, not permission to rescale the Schwarzschild oracle to the engine's hidden 2^-40 compactness.

## Red-team disposition (before freeze)

| Finding / invariant | Disposition |
|---|---|
| Independent oracle / mirror vs dump | Reject oracle-unsound implication: checker's mirror agrees at 6.3e-12. Reject dossier's ~1e-9 absolute-construction claim: its final error is 1.02e-5 at r/M=10, e=0.6; not an oracle error |
| Weak-control GR discrimination | Fix: retain sign/static wiring controls at 10^6 and require GR-positive / Newtonian and wrong-sign tide negatives at 100 and 10 |
| Strong-end oracle validity margin | Accept: separation error 1.614e-6 at r/M=10,e=0.6, 6.2× below 1e-5. Keep strict refinement/extent/invariant checks; invalid oracle denies a physics verdict |
| Engine-extent vs odd-pair linearization | Accept bounded gap: 4.88e-7, inside 1% band; retain paired initialization and extent checks |
| “5/5 tests” / reproducible evidence | Reject unverified count as evidence: checker ran out of build time. Capture six current release unit tests individually with hard 55 s limits and wall times |
| Killing constants, units, sample grid, quantized velocity | Accept checker confirmation; keep actual compactness and quantized shared genesis. Weak rungs are drop clouds, never claimed moving-member GR tests |
| Runtime / inferred epoch cost | Replace inference with recorded engine gate wall times and machine-state queries. Compilation is preparation; timeouts never count as mutant kills |
| Fail closed / validity and determinism | Retain strict admission, oracle-validity and engine-validity checks; retain all 21 cases. Byte-identical dump reproduction supports oracle determinism, not engine qualification |
| Phase-2 kernel / projected Riemann sign | Reject author's γ²·7/6 fit and inflated 1.56/23.6 values; accept independently checked −w(3γ²−1) curvature eigenvalue. Wrong-sign and Newtonian tide must fail geodesic-pair comparisons |
| Phase-2 reference provenance / claimed machine precision | Accept checked closed forms, reject unregenerable check-B numbers and derive6 as evidence. Local positive tide comparison supplies reproducible circular evidence; no eccentric/turning-point implementation claim |

Freeze: uncommitted source blob `64c2dfea131e85b0f2e61c08d9f065a146cd6913`; SHA-256 `11ca9ede42fb0163be49f52d217711a78ecee7d986a345e1f08eaa0317cd9451`; base `55d76a669e4ca923eeabe6aff7fce7c7ab6cf9cf`. `git add` was denied at the administrative `index.lock`; the integrator commits these unchanged gate requirements. Immutable pre-engine source/spec snapshots and the freeze manifest are in `artifacts/runs/sol-judge2-freeze/`. Run evidence: `artifacts/runs/sol-judge2-freeze/`; per-case and mutant evidence: `artifacts/runs/engine-judge/`.

This job leaves the normal index untouched after its denial; it does not use the earlier alternative-index method.
