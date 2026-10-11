# Dossier — second author on inversion-b292: the named experiment done; the claim holds, two sub-claims corrected, the fleet-scale arithmetic worsens

## Claim (one sentence)

The checker's named experiment (modular λ̄-rank) is done and shipped, and the inversion-b292 thesis **holds on the corrected, regenerating record**: the gold taleb-09b5's "partner rank ≤ 4" is an artifact of a metric bounded by construction (distance-rank ≤ 3 in every nc=200 scene, even where the λ̄-rank a phase watch needs is 28–98), that λ̄-rank is **28 max / 61.1% > 4 in the gold's own formation scene** (seed-robust: 44 / 76.2% at seed 40) and **90–100% > 4 under any spread** — with two of the original run's sub-claims corrected by the modular re-run (**ϖ-spread alone reaches 59–74 of the 99 cap, not the cap; the cap needs e-spread; the worst w1 pair is 59 λ̄-neighbours out, not diametrically opposite**), and the watch's degree is **k̂ ≈ 51 in the control with k̂/n_c ≈ 0.25–0.29 scale-free (nc 200→1000)** — so at the gold's formation density a 10⁶-ship fleet's λ̄-watch admits ≈1.4×10¹¹ pairs ≈ 11 TB, the ruin regime itself (the original run's "3.6 GB" held k̂ fixed at its nc=200 value; k̂ grows ∝ n_c at fixed density) — while at 5× density **the gold's own distance/true-longitude metrics break too (max 10/11)**, and the exact-amplitude window family stays sound out to e = 0.5.

## Bottleneck

The board's top scaling risk (candidate work at scale) and the in-flight `b-coorbital-cert` build, which the silver verdict found implementing the clump-wide ϖ-free window family with the degree never measured. The corrected record re-aims it before it lands: the rank-4 / O(n·4) cost model is dead on every metric (λ̄, distance and true-longitude); the degree budget k/n_c ≈ 2L̄/W must be computed from real amplitudes *before* the tier is chosen, and the ζ trigger then declines exactly the formation-density clumps (k̂/n_c → 0.29) and debris clumps (→ 1.0) it cannot afford. Nothing on `main` to delete; the certificate is unmerged.

## Evidence

All runs Linux x86, 8 vCPU, one process per scene ≤ 15 s at nc=200; `n1k` (nc=1000) is the largest at 152 s, peak RSS **7.4 MB**. Binary `crates/encounters/src/bin/invert.rs` (the b292 instrument + this run's fix: every line carries `ranks.lbar` (raw, byte-compatible with the b292 record) **and** `ranks.lbar_mod` (`(m + pom).rem_euclid(TAU)` before `circ_rank`), plus the checker's four attack scenes shipped); `taleb.rs` is the gold's verbatim, byte-identity preserved.

**The record regenerates.** All 13 scene lines + `taleb adj` reproduce byte-identically (only `sweep_s`/`meth_s` differ). The b292 bookkeeping gap is closed: the missing `invert-c0.jsonl` regenerates exactly as its dossier row (enc 234, dist max 3, λ̄ max 28 / p90 16 / 61.1%, k̂ 50.6, fracQ 0.254, method missed 5/234), and the b292 stored lines regenerate against the b292 instrument (w1, d30 re-verified here; all eight by the checker). `taleb adj` byte-level reproduces the gold's own numbers: disputed 197, **missed_true_sub_rho 4**, extra_true 193, extra_false 0, rank_max 4 — and the gold's λ̄-binned brute saw only 40 encounters (rank_probe), the blind axis.

**Corrected table** (raw λ̄ max → **mod λ̄ max (p90)**, % > 4; cap = 99):

| scene (knob) | enc | dist max | λ̄ raw→mod max | mod p90 | % > 4 mod | k̂ | k̂/n_c | meth miss |
|---|---|---|---|---|---|---|---|---|
| **c0 = gold's adj** (s27) | 234 | 3 | 28→**28** | 16 | **61.1%** | 50.6 | 0.25 | 5/234 |
| c0b (control, s40) | 235 | 2 | 73→**44** | 26 | **76.2%** | 59.9 | 0.30 | 17/235 |
| w1 (ϖ π, s27) | 219 | 1 | 99→**59** | 32 | **90.4%** | 50.6 | 0.25 | 1/219 |
| w1b / w1c (s40/s41) | 218/230 | 1 | 99→**73 / 74** | 48/46 | **93.6 / 94.3%** | 59.9 | 0.30 | not run |
| e3 (σ_e 3e-3) | 186 | 0 | 99→**98** | 82 | **100%** | 127.5 | 0.64 | 0/186 |
| e10 (σ_e 1e-2, s27/s40) | 40/44 | 0 | 99→**98**, 98→**98** | 94/93 | **100 / 97.7%** | 195 | 0.98 | 0/40 |
| s5 (σ_λ 0.05) | 42 | 0 | 99→**39** | 27 | **90.5%** | 36.0 | 0.18 | 0/42 |
| d30 (debris) | 12 | 0 | 94→**98** | 92 | **100%** | 198.7 | 0.99 | 0/12 |
| aspread (a_hw 1e-3, ϖ π) | 195 | 1 | 98→**64** | 30 | **88.7%** | 76.2 | 0.38 | 5/195 |
| e5 (σ_e 5e-2, e ≤ 0.5) | 2 | 0 | 77→**96** | 96 | **100%** | 199.0 | 1.00 | 0/2 |
| **n1k (nc 1000, control)** | 6081 | **10** | 497→**218** | 99 | **94.1%** | 286.0 | **0.29** | 46/6081 |

1. **The control refutation is untouched by the bug** (raw = mod exactly, 28/16/61.1%) and seed-robust (44/26/76.2% at seed 40). The gold's metric (distance-rank ≤ 3) and true-longitude rank (≤ 4) stay flat in every nc=200 scene while the needed λ̄-rank is 28–98.
2. **The two contaminated narratives, restated.** ϖ-spread alone: λ̄-mod max 59 (w1), 73/74 (seeds 40/41) — 60–75% of the cap, not "the circular maximum (99 of 200)"; the cap is reached under e-spread (98 at σ_e ≥ 3e-3, all seeds) and at debris dispersion (98). The worst w1 pair is [9,11]: λ̄-mod rank **59** (raw said 82; the b292 dossier's "rank 99, diametrically opposite" pair was a wrap artifact), |Δλ̄| = 8.1e-3 = 81 spacings, e_sum 4.2e-3, contact at 0.41ρ — no ±4 phase window catches it, for the same reason as before.
3. **Density kills the gold's own metric** (n1k): distance-rank max 10, true-longitude max 11 at 5× density — rank ∝ density × reach, so k=4 was never scale-free on *any* order metric; this closes the "watch k nearest by distance" door the original only asserted. k̂/n_c = 0.286 vs 0.253 at nc=200 (scale-free), λ̄-mod max 218, 94.1% > 4. The pairwise tier's low-e miss persists at scale (46/6081 = 0.76% at σ_e = 1e-3; 17/235 = 7.2% at seed 40 — the near-tangential fix is owed independently).
4. **a-spread is costlier, not kinder** (the b292 "what would make it wrong" guessed the opposite): k̂/n_c = 0.381 vs 0.253 control, λ̄-mod max 64, 88.7% > 4.
5. **Windows stay sound to e = 0.5** (e5): exact-amplitude viol −0.24, 2-term −0.25 (worst pair e_sum 0.16); every scene's viol < 0 (tightest: w1 s41, −2.8e-6). The soundness claim now covers e ∈ [0, 0.5].
6. **Fleet-scale arithmetic, corrected again.** k̂/n_c is the scale-free quantity (0.253 at nc=200, 0.286 at nc=1000, same geometry). The b292 dossier's "k≈50 → 5×10⁷ sections ≈ 3.6 GB" held k̂ fixed from the nc=200 scene; at the gold's formation density a 10⁶-ship fleet gives k̂ ≈ 0.29×10⁶ → watch ≈ 1.4×10¹¹ pairs ≈ **11 TB at 80 B** ≈ 29% of the quadratic tier — the watch *is* the ruin regime it was meant to replace. Spread over the whole orbit instead (W = 2π): k̂ ≈ 1.6e-3·n_c ≈ 1600 → ≈64 GB, still 200× the gold's O(n·4) claim. Either way the gold's 300 MB cost model is dead at 10⁶; the ζ trigger declining such clumps is a necessity, not an optimization.

**Reproduce** (CARGO_TARGET_DIR=/home/glmlab/lab-target-1, T=$CARGO_TARGET_DIR; each scene ≤ 15 s except n1k at ~152 s):
```
cargo build --release -p emergent-encounters --bin invert --bin taleb
$T/release/invert c0    # and w1 w1b w1c e3 e10 e10b s5 d30 c0b aspread e5 (≤15 s each); n1k (152 s)
python3 lab/results/20261011-0736-second-20261011-0614-inversion-b292-5033/work/summarize.py   # the table above
$T/release/taleb adj    # gold byte-level reproduction (~20 s; its line 1 is the gold's malformed JSON — parse leniently)
```
Raw lines: `work/invert-*.jsonl` (this run, fixed instrument, raw+mod side by side), `work/orig-invert-*.jsonl` (the b292 record + regenerated c0), `work/orig-taleb-adj-repro.jsonl`, `work/second-author.patch` (the exact delta on the b292 instrument).

## Predictions

`predictions.md` was written before the fixed-instrument runs. **All nine held.** The checker-derived corrected values (w1 59/32/90.4%, e3 98/82/100%, e10 98/94/100%, s5 39/27/90.5%, d30 98/92/100%, c0b 44/26/76.2%, aspread 64/88.7%/0.38, e5 96/100%/sound, n1k 218/94.1%/0.286/10/11) reproduced **exactly** from the shipped fix. My own novel predictions held: w1b/w1c λ̄-mod max in 50–75 with 85–95% > 4 (measured 73/93.6%, 74/94.3%); c0 raw = mod (clean control); every stored line regenerates. The kill criterion (mod rank ≤ 4 in c0) did not trigger: the control refutation is real from shipped code.

## What would make it wrong

- **The agreement with the checker's corrected values is same-harness agreement** (same `fleet2` RNG, same sweep truth, same `circ_rank`): the 5 October register lesson. The mod fix stands on its definition — values in [0, TAU), one cut, modular gap — which closes the wrap bug class by construction; the agreement adds convenience, not independence.
- e5 has 2 encounters: the rank statement there is thin; the soundness statement is about the closed-form bound and holds with margin −0.24.
- The 10⁶ extrapolation carries the density law over 3 decades on 2 measured points (200, 1000). The law is analytic for the window family (k̂/n_c ≈ 2L̄/W), but the fleet's σ_λ at 10⁶ is a design choice; both bounding cases are given above.
- Scene family as in b292: one a-scale (±1e-5, plus the single 1e-3 aspread probe), one ρ, Gaussian bunches, 1 orbit, four seeds, nc ≤ 1000.
- k̂ remains the degree of the ϖ-free epicycle-amplitude family, not a lower bound over all sound predicates (unchanged from b292); but the n1k result now kills fixed-k on *every* order metric.

## Cost of adoption, fit with PRINCIPLES

Adoption is the same re-aim b292 proposed, now on a clean record: (1) drop the rank-4 / O(n·4) cost model from `b-coorbital-cert`; (2) compute the degree budget k/n_c ≈ 2L̄/W from real amplitudes *before* choosing the tier — the ζ trigger, fed L̄, declines formation-density and debris clumps by itself; (3) declined clumps fall back to the pairwise tier, whose low-e near-tangential miss (5/234, 17/235, 46/6081) is owed independently; (4) nothing is merged, so migration cost is zero. PRINCIPLES #10: "Measure before claiming, and never strawman" — the gold's premise is now refuted by measurement on every metric it could have used; #19: "a fix signals the wrong representation" — a fixed-k watch was the wrong representation, the degree budget is the one the dynamics admit. The 5 October register lesson cut both ways here and is quoted in the dossier's wrongness section.

## The lens (second author)

I inherited b292's scenes, RNG and truth sweep deliberately (byte-compatibility is the point of a second-author run), so artifacts surviving in *those* are invisible to me: the truth's 1.9ρ true-longitude bins with adjacent-bin-only checks rest on b292's chord argument, which I did not re-derive; n1k's sweep (152 s) exceeds the 60 s guidance and shares that binning. A dynamics lens would derive k̂/n_c = 2L̄/W analytically instead of trusting two points; a fresh-instrument lens would re-implement the truth independently (different binning axis, e.g. eccentric-anomaly) rather than trust the same-harness agreement; neither heterogeneous fleets (mixed dispersions in one clump) nor resonance-crossing formations were touched, and e > 0.5 is untested (the gold's cap-10σ Rayleigh makes 0.5 the natural ceiling of this generator).
