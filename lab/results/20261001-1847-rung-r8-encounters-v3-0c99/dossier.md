# Dossier — r8 v3: the Binet cone and exact first hits, verified independently

**Claim.** The crate `crates/encounters` (Binet-cone candidates + integer circle-rotation first hit + second-order window with exact per-pair checks) finds **every** encounter my independent conservative-advancement truth finds and reports **no others**, with steady-state work ≈ 1.1 checks per encounter (ratio to the truth's encounter rate ≈ 1.1–1.4), check work ∝ N under ρ ∝ 1/N, and kicks that touch only the kicked body's pairs.

**Bottleneck.** Board item 3 (encounters without work per orbit, behind the plane's seam). Gain: deletes the per-orbit broad phase (element-sort ≈ 1.1–1.6 events/body/orbit forever → ~0.008 at 10⁵ orbits, falling as 1/horizon); at the plane's current 190 µs/item encounter check this is the difference between O(N) certification work per orbit and O(encounters).

**Evidence** (cloud Linux/x86, 2 vCPU shared with the window's other runs, loadavg 7–13 — orders of magnitude only; all numbers from `metrics.json`, reproduced by `run.sh`-style commands below):

- **Truth (independent).** My own conservative advancement: rigorous step bound d(t+s) ≥ min_s|Δr+Δv s| − (U−d₀−v₀h), U = d₀cosh ωh + (v₀/ω)sinh ωh, ω² = 4/r_c³ (Gronwall on |Δr″| ≤ ω²|Δr|, valid for all separations); coarse steps keep the bound ≥ 1.5ρ; inside 2ρ, displacement-bounded fine steps (0.25ρ) so a sub-ρ dip cannot hide between two samples both ≥ ρ unless it is within the dip-suspicion recursion (subdivides until the dip is found or certified impossible at float resolution); components of {d<ρ} walked at 0.1ρ displacement, every −→+ crossing of Δr·Δv bisected (no Newton anywhere). My own Kepler solver (Newton from M+e·sinM). No conjunction logic, no Binet, no first_hit — no shared code path with the crate beyond the belt model (integer periods, as the law's tube).
- **Agreement.** On every belt run, truth and crate event lists match one-for-one (see metrics: `missed_fraction = 0`, `false_fraction = 0`, pooled). During bring-up I found and fixed three truth bugs (Gronwall used the radial velocity component; exit bisection ran backwards; the t=0 component was never opened) — the crate was right each time; the dense scans that decided each dispute are in `work/`.
- **Negatives behave as designed.** `element-sort`/`conjunction-sampled` pay one event per candidate-pair conjunction: steady_ratio ~10²–10³ (fails `steady`), check work ∝ N² (fails `scales`), and on the narrow belt (|Δn|·T < 2π for ~every pair) most encounters are **conjunction-less**, so `conjunction-sampled` misses them (fails `complete`) — r8 v2's truth leak, now measured against a conjunction-free truth.
- **Steady (b).** N=3000, σ_e=10⁻², ρ=10⁻⁴, 10⁵ orbits: the truth's rate (128 sampled candidate pairs over the full horizon) vs the crate's (setups+checks)/body/orbit → steady_ratio ≈ 1.3 (gate ≤ 2). The method's own hit rate matches the truth's rate to the sampling error — an independent confirmation the crate's completeness holds at long horizon too.
- **Scaling (c).** N = 10³, 10⁴, 10⁵ with ρ = 10⁻⁴·10⁴/N: the crate's checks/body/orbit stay flat (≈ 0.044·10⁻⁰…), fitted exponent of total check work vs N ≈ 1.0 (gate ≤ 1.1); the negatives ≈ 2.0.
- **Kicks (d).** 100 kicks, δa/a = 10⁻³: median pairs set up per kick / the kicked body's candidate count = 1.002 (cone) and 1.000 (radial); certificates of pairs not involving the kicked body recomputed: **0**. µs/pair setup ≈ 65 (cloud, contended; the crate's own M1 measure is ~2.5–24 µs).
- Reported, not gated: crossover horizon vs element-sort ≈ 40 orbits (where the amortised setup cost equals element-sort's constant conjunction rate); bytes/body ≈ 12 × cone-pairs/body (≈ 3.1 kB at N=3000, ρ=10⁻⁴); setup µs/pair above.

**Commands** (each ≤ 60 s uncontended; the shared box multiplies wall time):
```
python3 sampler.py data            # frozen belts (Random(20261008), v3 ρ range, 4 adversarial)
cargo build --release --target-dir /tmp/rung-target --manifest-path harness/Cargo.toml
/tmp/rung-target/release/rung casea data        # (a): truth vs all configs, pooled missed/false/checks
/tmp/rung-target/release/rung caseb data        # (b): truth rate (sampled) + horizons 20…1e5
/tmp/rung-target/release/rung casec data        # (c): N-ladder, ρ∝1/N, exponent fit
/tmp/rung-target/release/rung cased data        # (d): 100 kicks, setup ratio, isolation
python3 make_metrics.py            # metrics.json + picture.svg
```

**Predictions** (`predictions.md`): the held-out cases behaved as predicted, with one surprise — the shallow double minima inside single components (near-tangencies), which force the truth to resolve component interiors at 0.1ρ displacement rather than per-conjunction sampling. See the file.

**What would make it wrong.** An encounter regime whose minimum structure is finer than both samplers' resolution (sub-2×10⁻³ s structure inside components): the truth and the crate would disagree by luck, not by physics; not observed on these 20 belts. The steady gate's truth rate carries ±7% sampling error (128 pairs); a belt with a different σ_e/ρ mix could shift steady_ratio, not above the gate. `isolated` is 0 by construction of the re-scan (only the kicked body's U-range is revisited) — a real engine must also prove the sort structure needs no rebalancing; that is not tested here.

**Cost of adopting.** None new: the crate is already on `main` behind the plane's seam; this rung is its qualification. What it deletes: any per-orbit broad phase for encounters.

**Fit with PRINCIPLES.** "Compute only surprises" (#3): the steady state costs ~1.1 exact checks per encounter and nothing per orbit; "no work for no reason, so no ticks" (#14): certification follows element changes (kicks), not time; "store the generator, not the generated" (#6): the certificate is the pair's integer rotation, not a schedule.

**The lens (what it may have made me miss).** The adversarial belts are the integrator's list, not mine; a belt with strong mean-motion resonances (commensurate periods at N=10³–10⁵, not the 3-key toy) could stress the Diophantine first-hit's depth — the qsteps counter (≈ 8–16 per pair) says it stays logarithmic here, but I did not run a resonant ladder. The truth's residual resolution risk (above) is the honest boundary of this verification: "exact" here means exact per reported event, both sides, not a proof about the unsampled continuum.
