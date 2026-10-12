Grade: gold

**Abstract.** Second blind check of the built co-orbital certificate (`wt/cx-b-coorbital-cert`, adce00d6): everything reproduces bit-identically in a clean patched tree — 0 misses on all six scenes and at 10⁶ snapshots; window k p50 3411 at the gold-e 10⁶ headline (3.41×10⁹ visits, 1379 per contact) vs 48 tight; equation-of-centre 99.5% of reach; scaling exponent 2.04; tree tier exactly C(10⁵,2) in 140 s. Held-out H1/H4/H5 held; H2 missed honestly (order statistic: −3.7%, not 5×). My own cases: headline seed-robust (k p50 3328/3323); true 10⁶ clumps reach k p50 34,310–68,346 — the `reach·n/TAU` formula underestimates 10–20×, only the two-pointer is a safe guard; sound to e ≈ 0.3. The adopted rank-4/O(n·k) premise is wrong at its own headline. Adopt in the merge review: fix the stale board/lens text, add heterogeneous-e and clumped-λ k-gates, budget k in the allocator.

## Reproduction (clean tree, `work/patch.diff` applied by me)

- Patch applies cleanly; `phase.rs`/`tier.rs` byte-identical to `wt/cx-b-coorbital-cert` @ adce00d6 (verified by `git show` diff); the only other lib change drops the branch's unused `pub mod truth;` — no physics touched.
- Build: `CARGO_TARGET_DIR=… cargo build --release -p emergent-encounters --bin redteam --bin checkadv --bin second` ✓.
- `redteam control` (17.7 s): 11 contacts / rank max 2; control-jam-loose-e 314 contacts, 313 ≤ 4, one at 5 — bit-identical. `redteam pileup` (3.2 s): 757 / 14.4% > 4 / max 9; 249 / 0.8%; 705 / 2.3% — bit-identical.
- `checkadv built` (8.4 s): 0 misses on all six scenes, visits 5762/1858/12096/19900/19844/19900 — identical.
- `checkadv builtsnap` (3.9 s, 203 MB): 1e5-tight k p50 4; 1e6-tight 48 (49.1e6 visits); 1e6-gold-e reach 2.142e-2, k p50 3411 (p99 3537, max 3595), visits 3,409,495,373, contacts_t0 2,471,928, window_miss 0 — identical.
- `second decomp|scaling|surgery` (0.5–5.2 s, ≤ 211 MB): EoC share 0.995 / 0.669; k_pred/p50 0.999 / 1.002; clumped scenes 0.006 / 0.045; scaling visits 3.09e7 → 3.41e8 → 3.41e9 (exponent 2.04, and I recomputed log₁₀(110.3) = 2.043); surgery −3.7% / −10% with contacts 100.00% and 0 window misses — identical.
- `second treefall` 1e5: candidate_pairs 4,999,995,000 = C(10⁵,2) exactly, 139.9 s (author: 145.9 s) — matches. (My run's 1e6 continuation was killed by my own timeout, as the author killed theirs.)
- Arithmetic: 3.4095e9/2.472e6 = 1379 visits/contact ✓; 3411/4 = 853× ✓; e_max/median 5.3289/1.1782 = 4.52 ✓.

## Predictions

`predictions.md` predates every run artifact (mtime order: prompts 32m → branch extracts 29–31m → predictions 27m → run-log 20m → evidence/dossier 17m; the malformed JSON in the surgery line is present in both the shipped source and the log, so the log came from this exact source). R1–R3 (record regenerates), H1 (reach 2.142e-2 ∈ [0.018,0.024], k 3411 ∈ [2800,3900], tight EoC 2/3 → 66.9%), H4 (branch gate k=1 on a shared-shape ring), H5 (stale texts) all held. H2 missed (predicted 5× drop from the single-worst-e surgery, measured −3.7%) — honestly reported, and the miss is the finding: at n=10⁶ the Rayleigh tail is dense, k rides the order statistic. One framing slant, flagged: H3 as pre-registered promised ±15% "on every scene I run", failed on the two clumped scenes the author ran (0.006, 0.045); evidence §3 discloses both numbers, but the dossier's Predictions paragraph narrows H3 to "on uniform fleets" post hoc. No number is hidden; the surviving recommendation (two-pointer exact k) is unaffected.

## My adversarial cases

1. **Seed robustness** (new bin `check2adv`, same generators): gold-e 10⁶ seeds 73/74 → k p50 3328/3323, e_max 5.20e-3/5.20e-3, tracking the order statistic — the 3411 headline is not a seed artifact.
2. **True 10⁶ clumps** (σ_λ = 0.2 / 0.1 rad): k p50 34,310 / 68,346 — local λ-density sets k, 10–20× the uniform headline, and `k_pred = reach·n/TAU` underestimates by 10–20× (ratio 0.100/0.050). Confirms the author's caveat quantitatively: only the two-pointer over the sorted λ is a safe pre-visit guard; the formula is not. (The author's `clump`-style scenes at 10⁶ wrap the ring because σ_λ ∝ n·ρ; mine are the genuine article.)
3. **Soundness at extreme e**: e~Rayleigh(5e-2, cap 1e-1), s=1.25ρ, 2 orbits: 56 brute-truth contacts, 0 misses. e~Rayleigh(0.15, cap 0.3): 7 contacts, 0 misses, reach 1.217 < π — note the cert does **not** refuse even here; it silently pays near-C(n,2) visits. The refuse-when-k-large guard is more necessary than the dossier states.
4. **Tree-tier degeneration at n = 10⁴/2×10⁴**: pairs = 49,995,000 / 199,990,000 = exactly C(n,2) — structural, not a 10⁵ fluke.
5. **Gate audit from branch source**: the branch's only scale test `fixed_density_ring_visits_linear_work_to_a_million` builds `Body::new(1.0, 0.02, 0.0, …)` — uniform e and pom, so the shared-shape cancellation fires (measured eoc = 0.0) and it asserts k = 1. No branch test has heterogeneous e or clumped λ. H4 verified from the source, not the run's word.

## Novelty

`docs/HISTORY.md` has no entry on the certificate's reach cost, the equation-of-centre term, or order-statistic cost; the only prior lab run on this cert (`20261006-1931-b-coorbital-cert-152e`, commit 2237a44d) was graded *missing* with empty logs — it never ran. The original author run (evidence-orig.log in `work/`) used the equation of centre to break *sort keys*; using it as the *cost mechanism of the built certificate's reach* is new here, as are the decomposition, the surgery, the scaling exponent, the gate-blindness audit and the fallback measurement. The 3411 headline itself is credited to the first checker; the extension is what this run adds.

## Goal fit

Moves the board's top scaling risk ("candidate work must track real encounters") by showing the adopted premise — "every real encounter lies within partner rank 4 … O(n·k)" (board.md, 6 Oct gold; `lab/lenses/b-coorbital-cert.md`) — is wrong at its own headline fleet: k p50 3411, 853× the implied 4, quadratic in n at fixed e-spread. PRINCIPLES fit: "Certificates need independent, adversarial checks" (this is the second, aimed at the built artifact); "regimes are chosen by dimensionless numbers" — the regime number is k = EoC-reach × local λ-density; #12 smoothness — 3.4×10⁹ visits is a spike, and the free two-pointer makes the cost knowable before it is paid; "Gates are frozen… judge a representation" — the gate-blindness finding is exactly the missing gate. The soundness half of the ledger also stands: the built cert misses zero contacts everywhere tested, including my extreme-e cases.

## What the author missed

- The `k_pred = reach·n/TAU` formula is not a guard on any genuinely concentrated workload (10–20× underestimate at true 10⁶ clumps, measured above); the dossier leads with its uniform-scene accuracy and should lead with the two-pointer only.
- The cert never refuses at extreme eccentricity (reach 1.22 rad at e~0.3 caps): without the k guard it degrades silently toward full pairwise, so the guard is load-bearing for correctness of *cost accounting*, not a nicety.
- The H3 scope in the dossier's Predictions section is narrowed after the fact (details above).
- `group_events` end-to-end at 10⁶ remains untimed (visits stand in) — disclosed; cosmetic: the surgery `top10` line prints malformed JSON.
