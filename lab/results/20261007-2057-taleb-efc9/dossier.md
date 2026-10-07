# Dossier — 20261007-2057-taleb-efc9 (lens: Taleb)

**Claim.** The phase-neighbour certificate now being built (`b-coorbital-cert`) certifies only *strict formations* — co-orbital groups sharing (e, ω): encounter partner rank in mean anomaly equals (n/2π)·(the pair's co-location lag), so any dispersion breaks it silently (13.5% of encounters missed at rank 4 for σ_e = 0.02 alone; a collision-debris ring degenerates to k\* = n/2, 98.5% missed) while the miss-free pairwise tier costs exactly all n(n−1)/2 pairs at *every* same-a group — the two certified tiers leave the game's swarm workloads uncertified, and the certificate's k must be sized by the group's lag **tail** (it is O(n²·lag) beyond strict formations), not fixed at 4 or gated by concentration.

**Bottleneck.** Encounters at N — the board's top scaling risk, and the co-orbital certificate is in flight on both the GLM and Codex lanes right now. Gain: prevents shipping a certificate with *silent* misses — a ruin state, since a lost encounter corrupts the canonical history irreversibly and is undetectable downstream (PRINCIPLES #13, errors that compound; here they compound by absence). What it deletes: the fixed rank 4 and the concentration trigger from the build; what it adds: one measurable (the lag bound) and a named hole (swarms) that needs a third tier.

## Evidence

Exact Kepler two-body truth, all bodies at a = 1 (co-orbital; σ_a = 0 ⇒ M-rank is frozen in time and one period of dense sampling is a complete truth; T = 8192/orbit gives ≥ 3 samples per crossing at e ≤ 0.6 — verified: encounter counts identical at T = 8192/16384/32768). n = 384, R_enc = 0.005 a (battery 2 varies). k\* = max circular M-rank over real encounter pairs; miss@4 = fraction of encounter pairs with rank > 4 (the gold's rank). Events are distinct by construction (one min-distance per unordered pair per period).

| scene (n=384) | n_enc | k\* | miss@4 | shell setup |
|---|---|---|---|---|
| ctl-ring, circular, aligned | 124 | 2 | 0.0% | 73,536 (100%) |
| ctl-arc (convoy, 30° phase arc, aligned) | 1341 | 9 | **11.9%** | 73,536 (100%) |
| ctl-ring e=0.3, aligned | 139 | 3 | 0.0% | 73,536 (100%) |
| σ_e=0.02, aligned | 237 | 9 | **13.5%** | 73,536 (100%) |
| σ_e=0.05, aligned | 229 | 20 | **45.0%** | 73,536 (100%) |
| σ_e=0.10, aligned | 220 | 34 | 66.4% | 73,536 (100%) |
| σ_e=0.30, aligned | 258 | 107 | 84.1% | 73,536 (100%) |
| e=0.3, σ_ω=15° | 229 | 95 | 81.2% | 73,536 (100%) |
| e=0.3, σ_ω=45° | 249 | 191 | 93.6% | 73,536 (100%) |
| e=0.3, ω uniform, e∈{0.1,0.3,0.6} | 231–255 | 191–192 = n/2 | 97–98% | 73,536 (100%) |
| two counter-aligned sub-fleets | 179 | 140 | 60.3% | 73,536 (100%) |
| **debris ring** (e∈[.05,.6], ω,Ω uniform, σ_i=10°) — n=768, R=0.02 | 396 | **384 = n/2** | **98.5%** | 294,528 (100%) |

Controls pass on the certificate's home turf (rings: k\* = 2–3, zero miss), so the instrument works; the convoy control already breaks a *fixed* rank 4 (k\* = 9–11 over 3 seeds, miss 12–18%) because k\* scales with phase density × R, and every dispersion scene breaks it catastrophically. Seed robustness: k\* = 189–192 and miss@4 = 97–98% across 4 seeds (sw180-e03); 20–25 / 36–52% (σ_e=0.05); 10–11 / 12–18% (convoy). The R-scan (0.005 → 0.02 → 0.05) leaves k\* pinned at n/2 — the failure is geometric, not a resolution artifact. Node dispersion only (i=15°, Ω uniform, aligned apsides) stays phase-local: k\* = 6, miss@4 = 27.8% — apsidal/shape dispersion, not inclination, is the killer.

**Mechanism (measured and derived).** At the encounter instant, misaligned pairs meet with true-anomaly separation Δν\* = Δω (measured 84.3° vs Δω 84.2°, median; debris 80.8° vs 89.2°), aligned pairs meet at Δν\* ≈ 0 (0.1–0.5°) with the lag coming from 2Δe·|sin ν\*|. The M-separation of co-located bodies is then lag·dM/dν, dM/dν = (1−e²)^{3/2}/(1+e cos ν)² — this reproduces the sw015 max-rank pair analytically (predicted 98.7° vs measured 95.8°) and M(ν+π)−M(ν) = π + 4e sin ν reproduces the bimodal k\* = 140 ≈ (n/2π)(π+4e). So **partner rank = (n/2π)·lag**: zero only for shared (e, ω); the pairwise shell tier cannot retreat below n(n−1)/2 because same-a shells always overlap.

**Scaling corollary (analytic, from the same formula).** At fixed dispersion, k\* ∝ n (rank = lag × density), so the certificate is O(n²·lag) — quadratic — for *any* dispersion, however small; it tracks the real encounter rate only in the strict-formation limit (lag → 0, k\* = density·R·margin). At n = 10⁶, σ_e = 0.05 gives k\* ≈ 3×10⁴: 3×10¹⁰ pair-touches per orbit, only ~16× under the raw 5×10¹¹. The trigger must therefore gate on the group's lag tail (max circular Δω + 2·max Δe, times n/2π, against the work budget), and it must be a *tail* statistic — k\* is set by the extreme pair (sw015: σ_ω = 15° but one 2.6σ pair drove k\* = 95), not by the dispersion moment.

**Commands** (work/ folder; deterministic seeds; peak memory ≈ 0.6 GB; Linux x86 shared runner — counts, not timings):
- `python3 coorb_probe.py 384 8192 grid_results.json` — the grid above, ~20 s per scene.
- `python3 battery2.py` — debris/R-scan/mechanism/seeds, ~7 min total (the n=768 debris scene ~90 s).
- `python3 summarize.py` — the table.

## Predictions

See `predictions.md` (written before the decisive grid; controls and sampling convergence checked first). Outcome: 3, 4, 6, 7, 8 held (swarm degeneration to n/2, e-scaling, bimodal ≈ n/2, debris ≥ 98% missed, shell tier = 100% of pairs everywhere). Two of mine failed, both in the *dangerous* direction: the convoy control beats rank 4 (11.9% missed; I had predicted all controls pass at k ≤ 4), and σ_e = 0.02 already misses (I had predicted clean up to σ_e = 0.05) — the lag mechanism is stronger than I guessed. Node-dispersion prediction held on k\* (6 ≤ 16) but not on miss@4 (27.8% > 10%). Kill criteria pre-registered: the fragility claim would have died if k\* ≤ 4 everywhere — it did not; the no-man's-land (k\* ≥ 16 **and** setup/encounter ≥ 100) is confirmed on sw015, sw045–sw180, se03, bimodal and debris (setup/encounter = 300–744 on those scenes).

## What would make it wrong

- The build ranks dynamically (re-ranked per epoch or by true anomaly) rather than by frozen M-rank. Ranking by ν absorbs only the σ_e term (aligned pairs meet at Δν ≈ 0); misaligned pairs meet at Δν\* = Δω, so the swarm failure stands in any phase-like coordinate. Only a locus/spatial ranking fixes it. Dynamic re-ranking cost under σ_a > 0 is unmeasured here.
- Game fleets stay strict formations forever. Implausible: collisions are certain content (debris), and two convoys sharing one orbit with counter-aligned apsides is natural tactics — both are in the measured set.
- Shared-harness artifact: one Kepler implementation underlies truth and certificate. Mitigated by passing controls, by the analytic reproduction of three independent scenes' k\* from the closed-form lag, and by 3–4 seeds per headline scene; an independent checker should re-derive the truth with its own sampler.
- Not covered: 3D-inclination-dominated dispersion (one mild scene only), σ_a > 0 rank churn, perturbed (non-Kepler) swarms, and n beyond 768 (the n-scaling is analytic, not measured).

**Cost of adopting:** small and timely — `b-coorbital-cert` is mid-build. Replace the fixed rank with the lag-tail bound (O(n) group moments: circular max-gap of ω, max Δe, phase density·R); accept that beyond the budget the phase tier is void and the encounters design needs a third structure for swarms. Lead for that tier, from the same measurements: same-a encounters happen only at orbit-pair **crossing loci** (fixed points, revisited once per orbit) — a locus-keyed bucketing is the natural certificate where phase order degenerates. No gate, crate or frozen evidence is touched.

**Fit with PRINCIPLES.** #13 "basically we don't want errors that can compound" — a silent miss is the worst error type, invisible by construction; #4 "no categories: regimes are chosen by dimensionless numbers" — "formation" vs "swarm" is exactly the category naming to avoid, and the lag (in rank units) is the dimensionless number that chooses the regime; #9 "A failed experiment kills that configuration, never the method" — this kills the fixed-rank configuration, not phase ordering; #34 "the oracles are guards" — the certificate must reject what it cannot certify, not miss quietly.

**The lens.** Taleb looked for the cliff and found it tail-driven (k\* is an extreme-value statistic of the group's dispersion tail — a σ-based trigger would pass sw015 and lose 81% of its encounters). What the lens may have missed: it prizes the failure and offers only a sketch for the third tier; the constructive question — what the swarm certificate *is* — is one experiment away (crossing-loci bucketing, measurable with this same harness). It also did not measure the allocator side (p99 of per-frame work under tier switching), which is where a cliff in cost would bite the player.
