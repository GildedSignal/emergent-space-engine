# Dossier — inversion-b292: the co-orbital certificate's "rank 4" is an artifact of the metric; the specified watch's degree is 12× the claim and 100% at debris dispersion

## Claim (one sentence)

The gold `20261006-0346-taleb-09b5` premise "every real encounter lies within partner rank 4 along the orbit" was measured with **distance-rank at closest approach — a metric bounded by construction** (the partner is then within ρ, so the rank counts only bodies within ~ρ), while the mean-longitude (λ̄) rank that a phase-sorted watch actually needs is **28 max, 61% of encounters above 4, in the gold's own formation scene** and hits the circular maximum (99 of 200) once apsides are spread — excluding a ±k phase-neighbour watch at k≈4 under any window formula — and the ϖ-free epicycle window family the design specifies gives the λ̄-walk degree **k ≈ 51, not 4** (25% of the quadratic tier's pairs) even in the control, degenerating to **k ≈ 199/200 (the full quadratic tier)** for concentrated-but-e-dispersed clumps (debris), so the sound escape is crossing-anchored windows — the pairwise tier's own structure, whose *cost*, not soundness, is the real problem — and the `b-coorbital-cert` build now in flight (GLM queue + Codex lane) must be re-aimed before it lands.

## Bottleneck

The board's top scaling risk (candidate work at scale) and HANDOFF's "Risks to attack first". The gold replaced the quadratic tier inside co-orbital clumps with a phase-neighbour watch at O(n·k), k≈4, triggered by a dimensionless number; that cost model is what `b-coorbital-cert` is being built to. Measured correction: k/n_c ≈ 0.25 in the gold's own scene (12× the claim), → 1.0 at debris dispersion. Corrected arithmetic for the gold's 10⁶-ship fleet: k≈50 → 5×10⁷ sections ≈ **3.6 GB** (not ~300 MB), and for concentrated debris the 40 TB ruin arithmetic **stands** (the watch equals the quadratic tier it was meant to replace). Nothing on main to delete — the certificate is unmerged; this run re-aims the build before it lands.

## Evidence

All runs Linux x86, 8 vCPU, < 100 MB, one process per scene (≤ 15 s each). Binary `crates/encounters/src/bin/invert.rs` (new; the gold's `taleb.rs` applied unmodified beside it for comparison). Scenes are the gold's own generator (`fleet2`, RNG call order preserved — `c0` *is* the gold's `adj` scene, seed 27), one knob at a time: nc=200, a=1±1e-5, ρ=1e-4, 1 orbit.

**Truth is unbiased** (the gold's own instrument lesson, applied to their instrument): a true-longitude-binned sweep at dt=2e-5 (relative motion ≤ 0.46ρ/step at max relative speed 2.3), bins 1.9ρ; sub-ρ pairs cannot exceed one bin of true-longitude separation (chord ≥ 2·rmin·sin(Δθ/2)), and every same/adjacent-bin pair is distance-checked at every step. The gold's λ̄-binned brute cannot see equation-of-center offsets (their e=1e-3 gives 2e ≈ 20ρ ≫ their bin); mine bins by true longitude, so it can.

| scene (σ_λ, σ_e, ϖ span, seed) | enc | dist-rank max | **λ̄-rank max (p90)** | **% λ̄-rank > 4** | λ̄ window max | sound k̂ | k̂/n_c | method miss |
|---|---|---|---|---|---|---|---|---|
| **c0 = gold's adj** (.01, 1e-3, 0.1, 27) | 234 | 3 | **28 (16)** | **61%** | 5.2e-3 | **50.6** | 0.25 | 5/234 |
| w1 (.01, 1e-3, π, 27) | 219 | 1 | 99 (92) | 88% | 8.5e-3 | 50.6 | 0.25 | 1/219 |
| w1 s40 / s41 (same, new seeds) | 218/230 | 1 | 99 (86/83) | 91% | 1.1e-2 | 59.9 | 0.30 | — |
| e3 (.01, 3e-3, π) | 186 | 0 | 99 (83) | 98% | 3.0e-2 | 127.5 | 0.64 | 0/186 |
| e10 (.01, 1e-2, π, s27/s40) | 40/44 | 0 | 99/98 | 100/96% | 4.2e-2 | 195 | 0.98 | 0/40 |
| s5 (.05, 3e-3, π) | 42 | 0 | 99 (86) | 88% | 2.3e-2 | 36.0 | 0.18 | 0/42 |
| d30 debris (.02, 3e-2, π) | 12 | 0 | 94 (80) | 100% | 5.4e-2 | 198.7 | 0.99 | 0/12 |

1. **The gold's metric cannot fail.** Distance-rank at closest approach ≤ 3 in *every* scene, including those where the partner is 99 members away in λ̄ order. True-longitude rank also stays ≤ 4 (proximity again). A rank metric evaluated at the moment of contact measures local ρ-density, not watch structure. The gold's 234/234 "rank ≤ 4" is this tautology; so is its "traffic-jam" case.
2. **The watch-relevant rank fails in the gold's own scene.** With apsides aligned (±0.1 rad) and e~Rayleigh(1e-3) — the gold's station-keeping formation — 143/234 encounters have λ̄-rank > 4 (max 28). Mechanism: differential eccentricity still gives differential epicycles (Δ(e sin ν) ~ Δe ≈ 1e-3 = 10ρ vs mean λ̄ spacing ≈ 1.2ρ), so contacts are equation-of-center events, not lane conjunctions. Spreading apsides (w1) or e (e3→d30) takes the max to the circular cap and the fraction > 4 to 88–100%, on all three seeds. Worst measured pair (w1): partners diametrically opposite in λ̄ order (rank 99), |Δλ̄| = 3.2e-3 = 32 spacings, e_sum = 2.5e-3, contact at d = 0.63 ρ — no overtake ever brings them into a ±4 window (Δa ≈ 0 ⇒ drift ≈ 2 gaps/orbit).
3. **The specified watch's degree, and its scaling.** The ϖ-free window family the design specifies (per-pair L̄_ij = arcsin(ρ/min rmin) + amp_i + amp_j, amp = max|ν−M| exactly by golden section on ν∈(0,π); admission iff min over the horizon of |Δλ̄| ≤ L̄_ij under linear drift) never misses an encounter (window violation ≤ −2.9e-6 across all scenes, e up to 0.3; the 2-term epicycle bound also held everywhere), but its degree is k̂ ≈ 51 in the control (12× the claimed k=4; 25% of the 19,900 quadratic pairs), 128 at σ_e=3e-3, 195 at 1e-2, **199/200 at debris dispersion** — the in-flight build's clump-wide `walk_bound` is wider still, so costlier. k̂/n_c tracks 2L̄/W (control: 0.25 measured, ~0.25 predicted from n_c·2L̄/(σ_λ·√(2π)·√2) ≈ 56); bunching is the *worst* case (s5 vs e3: 5× the λ̄ spread cuts k̂ 3.5×), exactly the regime the certificate is for. A cheaper sound λ̄-watch would have to anchor windows to the orbit-crossing longitudes the Binet cone already computes (at a crossing, |Δλ̄| at contact is the equation-of-center difference *there*, not the global amplitude) — which is the pairwise sections tier's structure, not a phase-order train.
4. **The pairwise tier's misses concentrate at low e** (5/234 in c0 — the gold reported 4/233 with their partially-blind truth; 1/219 in w1; **0** at σ_e ≥ 3e-3): the near-tangential regime, consistent with the gold's diagnosis. The Binet **cone found 100% of candidate pairs in every scene** (19,900/19,900 in each phalanx; every true encounter inside the candidate set) — the quadratic ruin lives in the sections setup and memory, not in the cone.

**Reproduce** (each ≤ 60 s; CARGO_TARGET_DIR=/home/glmlab/lab-target-1, T=$CARGO_TARGET_DIR):
```
cargo build --release -p emergent-encounters --bin invert --bin taleb
$T/release/invert c0    # 14 s; also w1, w1b, w1c, e3, e10, e10b, s5, d30 — one JSON line each
python3 lab/results/20261011-0614-inversion-b292/work/summarize.py     # the table above
$T/release/taleb adj    # the gold's own instrument, byte-level reproduction (~20 s)
```
Raw JSON lines: `work/invert-*.jsonl`, `work/taleb-adj-repro.jsonl`. `taleb adj` on this tree reproduces the gold's numbers exactly: disputed 197, **missed_true_sub_rho 4**, extra_true 193, extra_false 0, rank_max 4 — and shows their λ̄-binned brute found only 40 of the 233 truth encounters (the blind axis their own instrument lesson names).

## Predictions

`predictions.md` was written before any run. **P1 failed in the informative direction**: I predicted all three rank metrics ≤ 4 in the control; distance and true-longitude held (3, 4) but λ̄-rank was 28/61% — the failure is present *without* any knob change, in the gold's own scene (my proposed mechanism, ϖ-spread, only removes the last common-mode cancellation; differential e is enough). Predicted k ≈ 4–8 → measured 50.6. **P2–P6 held**: ϖ-spread → λ̄-rank ≥ 10 (99) and ≥ 20% > 4 (88–91%) while distance-rank stays ≤ 4; linear growth with σ_e (k̂ 51→128→195, rank → cap); k ∝ σ_e/σ_λ (bunching worst case); the exact equation-of-center window sound at every e (viol < 0); debris: k̂ ≈ n_c (0.999), λ̄-rank ≥ 30 (94), quadratic ruin stands.

## What would make it wrong

- λ̄-rank is measured at the sampled closest approach (dt=2e-5 ⇒ timing error ≤ 1 step ⇒ rank error ±0–1); it cannot explain 28 vs 4 or 99 vs 4.
- A watch rebuilt on overtakes could catch drifting pairs earlier — but the worst pairs have Δa ≈ 0 (no overtake signal), and the closed-form watch admission (min |Δλ̄| over the horizon, drift included) is how k̂ was computed, so rebuilds cannot reduce it.
- k̂ is the degree of the epicycle-amplitude window family (the one the gold's adoption note and the in-flight build specify), not a lower bound over all sound predicates: a family anchored to crossing longitudes, or an admission exploiting drift-through-conjunction, could be cheaper — untested here. The rank-4 refutation does not depend on this: it is measured directly at contact. No *phase-order* family escapes it, and true-longitude order has no persistent validity window (the equation of center moves members by ~2e per orbit ≫ ρ).
- Scene family: one a-scale, one ρ, Gaussian bunches, nc=200, 1 orbit, three seeds. The mechanism (equation-of-center amplitude vs λ̄ spacing) is dimensionless, but the *numbers* are these scenes'; a larger a-spread (drift-dominated lanes) may be kinder to a λ̄-watch — untested.
- My c0 differs from the gold's adj only in the truth's binning (true vs mean longitude), finding 234 vs 233 encounters and 5 vs 4 window-tier misses; their instrument's adjudication sampler (150k samples/pair) is what assembled their truth despite the blind brute.

## Cost of adoption, fit with PRINCIPLES

Adoption is a re-aim of the in-flight `b-coorbital-cert` build (nothing merged, nothing to migrate): (1) drop the rank-4/O(n·4) cost model — a ±4 phase-neighbour watch is excluded by measurement; (2) if the λ̄-walk is kept, its windows come from the exact equation-of-center amplitude (measured sound to e = 0.3) and carry a **degree budget** k/n_c ≈ 2L̄/W computed *before* the tier is chosen — the gold's ζ trigger, fed L̄ from real amplitudes, declines exactly the debris clumps where k̂ → n_c; (3) those declined clumps fall back to the pairwise tier, whose window tier still misses ~2% at low e (5/234) — that fix (near-tangential contacts) is owed independently; (4) the deeper direction the evidence points to: anchor the watch to crossing longitudes (the cone's output — sound and already computed) and attack the sections *setup cost* in tight clumps, rather than replacing the tier's structure with a phase-order train; (5) memory arithmetic for a 10⁶ fleet: 3.6 GB at k≈50. Fit: "a fix signals the wrong representation" (#19) — rank-at-contact was the wrong representation of watch structure; "regimes are chosen by dimensionless numbers" (#4) — the degree budget is that number; "compute only surprises" (#3) — the watch degree is predictable from (āmp, spread) before anything is built; "behaviours over many seeds" (#20) — one seed family produced "rank 4"; three seeds put the max at the circular cap.

## The lens (what inversion made me miss)

Inversion found the artifact by asking what the gold's metric could not fail at — but it nearly shipped two of its own: the "100% method miss" on seeds 40/41 was my harness not running the method on those scenes (caught by checking `meth_pairs=0` in 0.00 s), and my first summarizer read those as misses. A dynamics lens would have derived the k/n_c law analytically instead of measuring it on six scenes; a speed lens would have pushed to nc=2000 to see whether k̂/n_c stays put (it should — the ratio is scale-free) and to a-spread scenes, where drift may restore the lane picture; neither the resonance-crossing formation (the gold's other named hole) nor heterogeneous fleets (mixed dispersions inside one clump) were touched.
