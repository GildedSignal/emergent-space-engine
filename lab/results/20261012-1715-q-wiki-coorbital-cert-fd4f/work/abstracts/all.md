### 20261006-0030-rung-r8-encounters-v3-3501
Grade: silver

**Abstract.** Claim: the diophantine method finds every encounter of an independent truth (0/18708 missed) at 1.16 checks each, steady 1.29×, exponent 0.98, kick-isolated — but reports one false encounter, so KILL on `sound`. I reproduce every number (verify, steady, xcheck, kicks, scale, scale-dio, false1 byte- or count-identical; belts and the (a)/(b) truths regenerate byte-identically). I then refute the run's diagnosis: at 50 significant digits the disputed report IS a true local minimum (g crosses up at 220.39551645, dip ~5e-10 below its chord), the run's own truth with a 0.002 step cap records it (t=220.395582), and the method matches that finer truth 2023/2023, 0 false. The KILL's cause is the truth's 0.02 resolution, not the method. Adopt: the method stands; the law needs a dip-depth quantum for terrace minima.

**Reasons.**

1. **Reproduction (clean tree, no patch needed — work/patch.diff is empty).** `verify`: pools identical (diophantine truth 18708, missed 0, false 1, checks 21772; negatives miss 12391; oracle clean). `steady`: all counts identical (rate 7.526043e-3 at 1e5 orbits, ratio 1.2902; matchup-1000 1750/1750), only wall-times differ. `xcheck` (6 belts): byte-identical. `kicks`, `scale`, `scale-dio`, `false1 coorbital`: identical. `gen_belts.py` regenerates the belts bit-for-bit (proven post-hoc: false1 re-run after regeneration is byte-identical, and truth-a00 re-runs byte-identical). One numeric nit: my steady_ratio from raw events is 1.29018 vs the author's printed 1.2902 (rounding of the same number). My metrics-check.json gives the same verdict: KILL, diophantine fails only `sound`; oracle passes all seven criteria; both negatives fail their named gates. No disputed outcomes.

2. **The one false report is not false — the run's central diagnosis is refuted.** The dossier claims "d decreases monotonically through the report: there is no local minimum at 220.40" and "g touches −3.2×10⁻¹⁸ without crossing". Three independent checks say otherwise:
   - **50-digit arithmetic (my own solver, no shared code):** g = Δr·Δv crosses zero upward at t = 220.3955164525 and back down at 220.4061097742, so the exact distance has a strict local minimum at the reported time (report 220.395521856, Δ = 5.4e-9), d = 4.418732e-4 < ρ, dip ~5.4e-10 below its ±0.01 chord. The crossing scale (g ~ 1e-11) is 8 orders above any evaluation noise floor.
   - **The run's own truth, finer:** with the fine-step cap 0.02 → 0.002 (one constant, same code), the coorbital truth gains exactly one event — pair (155,218), t = 220.395582 — and nothing else changes (2024 vs 2023).
   - **Method vs finer truth:** 2023/2023 matched, missed 0, false 0, dup 0 on the coorbital belt.
   The author's instruments could not see it: a 0.02-spaced g-grid straddles the 0.0106-wide excursion; the 2e-4 dense scan's argmin is dominated by the 5.5e-9 terrace trend over a 5.4e-10 dip; golden section over ±0.05 converges to the window edge. The dossier's "What would make it wrong" named exactly this hypothesis and rejected it on under-resolved evidence. Note the xcheck's event-for-event agreement between the two truths is shared blindness at sub-resolution scale, not independence ("agreement is not independence" — this run is now an example of it).

3. **Adversarial cases of my own** (my sampler, my seeds; method vs both truths):
   - `tangency` (200 bodies, one exact semi-major axis, Δn = 0 for every pair): 950/950 matched, 0 missed, 0 false; conjunction-sampled finds nothing at all (0 checks).
   - `highe` (σ_e = 0.3 crossers): 1442/1442, 0/0 — but checks per encounter 1.55, above the rung's 1.5 gate, outside the rung's sampled σ_e range (≤ 0.029 regular, 0.1 hot). Worth a look before adoption at high e.
   - `bigrho` (ρ = 0.01 on a 0.02-wide belt): 14946/14946 vs the frozen truth, 0 false; against a finer truth 1 missed, 0 false — fixed-resolution scanners (the method's k-step grids included) can miss terraces; symmetric with the truth's limit, no false positives anywhere.

4. **Reproducibility defect.** `run_truth.sh` cannot regenerate the (c) evidence: its `sample 8 12345` argument is not an integer (the truth binary would panic), its n=10⁴ line is unsampled, and the stored truths are 1-in-32 (187341 pairs) and 1-in-512 (1178022 pairs) samples with the phase unrecorded. My 1-in-32 phase-0 rerun gives 619 encounters vs the stored 643 (×32 → 19808 vs 20576; oracle exponent 1.0014 vs 1.0049 — immaterial to any criterion). The dossier text states the sampling; the shipped script contradicts it. By the lab's own standard (numbers the shipped code cannot regenerate), this alone bars gold.

5. **Novelty.** r8 v2 (taste log, 30 September) killed element-sort, shear-grid and hier-bounds on cost and exposed the conjunction leak; the Binet-cone/first-hit crate is the Opus research proposal on `main` (c7b225d). This rung is its first independent, adversarial verification — genuine and needed. The terrace finding is new (no H entry): near-tangential co-orbital passages produce micro-minima below any fixed step resolution, so the frozen "local minimum of distance below ρ" needs a dip-depth quantum, or truths need sub-terrace refinement; "A failed expectation is not automatically a failed method: diagnose which one broke (H0183)" — here the diagnosis itself was what broke.

6. **Goal fit.** Moves the board's "finding encounters without work per orbit" and answers the top scaling risk (check exponent 0.98 at ρ ∝ 1/N; steady 1.29× the encounter rate at 1e5 orbits). PRINCIPLES: "Certificates need independent, adversarial checks" — this check is that, working; it caught what the author's instruments missed.

**Why silver, not gold.** Every number reproduces, the controls behave, predictions were pre-registered (00:49, before all truth runs) and 7/8 held — but the run's headline mechanism ("bracket fires on noise tangency; not a local minimum") is refuted by a discrimination experiment the author should have run before claiming it, and the committed truth script does not regenerate the (c) truths. Not lead: the verification itself is real, independent and nearly all of it stands.

**The one experiment that would make it gold.** Re-derive (a)'s truth with the finer cap (16 s for the coorbital belt; spot-check disputed events at high precision) and rewrite the dossier accordingly: false 0, the method complete and sound against a strictly finer truth, and the KILL reframed as a finding about the encounter definition (the law needs a dip-depth quantum; the method's k-grids and any step truth share the limit — see my bigrho result). That run would be adoptable as-is within one step.

**What the author missed.** The high-precision/fine-truth discriminator before asserting "not a local minimum"; the shared-blindness reading of the xcheck; the (c) commands in run_truth.sh not matching the stored truths; the checks-per-encounter edge at high σ_e; that a 5.4e-10 dip under a 5.5e-9 trend needs bracket-local differencing (compare d(t±ε) at ε ≈ 1e-3), not window-wide scans, to be seen.

### 20261006-0916-inversion-f0be
Grade: gold

**Abstract (for the integrator).** Attack on the adopted gold `taleb-09b5`'s phase-neighbour train. Reproduced bit-for-bit (S1, S3b, S4, plus an independent ring reimplementation): overtakes/orbit = 16 449 / 263 795 / 1 052 179 at n = 128/512/1024 — exponent 2.000, coefficient ≈ 1.0, 26×–257× the n·k watch, robust under a new seed, the trimmed n = 256 point, and 16× finer sampling (+0.5%, so the report is conservative). The gold's O(n·k) cost premise is wrong: rebuild-on-overtakes is Θ(n_c²) events/orbit, 26× the watch in the gold's own control scene. The rank claim survived even my extra attacks (2D-compressed blob, 668 dense contacts, max λ-rank 1). Adoption: re-derive maintenance before freezing, add wiggle/spacing to the trigger; a design note, no code.

## Reasons

**1. Reproduction (clean copy, author's folder untouched).** `python3 probe.py s1`, `python3 probe.py s4`, `python3 s3b.py` in a scratch copy: S1, all three S4 points and S3b match `results-all.json` field-for-field, including float fields. `work/patch.diff` is content-free (one line: a failed `python3 probe.py s4` from the wrong cwd); nothing to apply. A file-time anomaly (probe.py mtime after results-s4.json) is resolved: the shipped code regenerates every number exactly.

**2. Predictions.** `predictions.md` predates the decisive runs (S2a–S3b results are all younger; S1, the self-declared instrument control, legitimately ran first). S1 and S4 held (exponent [1.7,2.3] → 2.000; >10× watch at n=1024 → 257×; correctness intact). S2/S3 prongs failed and were reported as failed exactly as the pre-registered kill criteria required. One gap: pre-registered prediction #5 (quadrature clustering) is never reported. I tested it: refuted, and inverted — quadrature fraction 0.222 against 0.509 chance on S4's 9 contacts (my pipeline independently reproduces those 9). A dropped prediction is a reporting fault, not a load-bearing one.

**3. My attacks (beyond the author's).**
- **2D-compressed swarm** (the attack the lens missed: the author only compressed phase, never radius): n = 64, radial extent ~6ρ and phase extent ~10ρ, 668 contacts verified by a 65 536-node dense all-pairs scan — max λ-rank at contact still 1, k = 4 misses 0. The rank-survival conclusion is *stronger* than the author claimed.
- **Overtake-count artifact hunt:** mean 221 swaps/body at S2b (max 477 of 511) — broadly distributed, not a near-tie flip-flop; S4 at 16 368 samples gives 1 057 696 (+0.5%), so the Θ(n²) count is sampling-robust. S2b at 4× density gives +19% — the 4 096-sample Kendall *under*counts there, i.e. the maintenance number is conservative.
- **Ladder:** added n = 256 (66 003) and seed 99 (exponent 1.998); my independent ring code reproduces the author's three points exactly.
- **LB-gate sensitivity at e = 0.9:** densifying the gate T = 256→4096 adds 464 candidate pairs of which exactly 1 hides a contact (d = 5.7×10⁻⁵): S3 contact counts are ~0.4% low. Immaterial to the dwell refutation.

**4. Novelty.** No overtakes/maintenance measurement exists in docs/HISTORY.md or the board (searched; the gold appears only in the 6 October taste-log entry, whose text claims "a phase-neighbour certificate at O(n·k) replaces the quadratic tier"). The gold's own folder is absent from this tree, so the board entry is the record; this run supplies the term that claim omitted.

**5. Goal fit.** Direct hit on the encounters design (focus list). The premise shown wrong is the adopted gold's cost claim, with the mechanism (λ-wiggle ≫ local spacing ⇒ every pair within one wiggle swaps twice per orbit) measured at exponent 2.000 with coefficient ≈ 1. PRINCIPLES #1: "The cheapest compute is compute not done" — ~10¹² rebuild events/orbit at 10⁶ ships is the opposite; #4: "regimes are chosen by dimensionless numbers" — the trigger lacks the wiggle/spacing number this run exposes. Cost to adopt: one design-note change to the encounters spec plus a trigger invariant; no code.

## What the author missed

- Prediction #5 was registered and then silently dropped; it is false (contacts avoid quadrature, 0.222 vs 0.509).
- Radial compression was never attacked; I ran it and the rank claim survives it — the "watch is stronger than its proof" conclusion could have been stated more strongly.
- The ~19% Kendall undercount at 4 096 samples in the low-e jam scenes (conservative, but the dossier asserts sampling adequacy without the finer run I did).
- The 10¹²-events extrapolation to 10⁶ ships borrows the e = 0.3 scene's coefficient ≈ 1; the gold's own control scene measures 0.53 (21 052/200²), giving ~5×10¹¹ — same order, but the dossier should say which coefficient it extrapolates.
- The kill binds the *flat* rebuild-on-overtakes design as specified. A hierarchical maintenance (a tree over the λ-ring, rebuilds amortized by level) is neither measured nor discussed; the frozen-ring pad alternative is argued, not measured — the author discloses this honestly. If the integrator wants the alternative closed, that is the one experiment to queue: measure the pad width k needed for a frozen mean-longitude ring in the gold's control scene (predicted Θ(n_c) in wiggle/spacing).

### 20261006-0916-library-80a8
Grade: silver

**Abstract.** Claim: five verbatim Readwise lessons map to engine decisions, and the load-bearing probe shows phase-neighbour certificates (the 6 Oct gold tier) cannot be maintained by element-change or quantum-slack payments at belt density: zero-kick static certificates miss 19/19 close conjunctions, per-kick 16/37, quantum-slack 35/37, all structural (partner churn by shear). Reproduced bit-for-bit; stable across seeds (52–59%, 89–97%, ~100%); per-kick needs λ≈16/orbit to close; quotes and cited plane costs verified. Gain: a corrected maintenance premise (budget must scale with shear rate × window), not a measured 10× — a zero-miss trigger costs 3.5–7× per-kick. Cost to adopt: a sizing rule for the encounters skin, one rung from proof.

**Reasons.**

1. **Reproduction: exact.** `python3 run_one.py B,1,16` + `nokick` in a clean copy (11.4 s) regenerate `probe_slack.json` bit for bit. Dossier arithmetic checks: 254.1 candidates/body (measured), |Δn| mean 0.355, max 0.75 rad/yr ("up to ~0.6" ✓); churn timescale w_k/|Δn| ≈ 0.1–0.2 yr ✓; 15.06× rebuild ratio ✓. All five quotes single-hit verbatim in the cached export (770 docs) with correct attribution; the four cited plane costs (83 % gather, 29/15 µs kick, 190 µs/item, step_for 0.795→0.245) are in HANDOFF. `predictions.md` predates the decisive JSON by 30 min (folder re-copied at publication, so not fully auditable; `run.log` is 0 bytes — "bit-for-bit identical to the run log" points at an empty file; I verified identity against the JSON instead).
2. **Predictions, honestly reported with two omissions.** 3 killed (disclosed), 5 confirmed, 1 (the A control) failed and the VOID is scoped honestly in the dossier tail. But prediction 2's "0 misses" also failed (its failure became the headline) and is not counted in the outcome list; predictions 4 and 6 were never run — because of a bug, not the host (next item).
3. **The "host suspended" attribution is wrong.** The author's C/D policies push K=4 heap entries per fire with no dedup: multiplicative growth, measured 52 fires/yr → 123,141/yr by year 15, 400 k rebuilds by year 16.7 of 60 (heap 1.2 M). A one-entry-per-body version-stamped heap terminates in ~30 s. The dossier's missing row is a bug report, not a host report.
4. **Attacks (beyond the author's), all in a faithful re-implementation of the same model.** Seeds 12/13/21: A 52–59 %, B16 89–97 %, static ~100 %, all structural, 0 stale — stable. λ sweep: per-kick closes only near λ=16/orbit (1/37), matching the churn timescale. k sweep: static k=16 and k=64 still miss 19/19; only k→full candidate set catches (my k=252 cap still dropped 1 pair — misses are membership churn, and the instrument can pass). Density: N=100 (~60 cand/body) per-kick **0/3 misses** — the kill is density-scoped, beginning between ~60 and ~254 cand/body; N=1600 (~1031 cand): static 155/155, per-kick 83 %, shear-sized trigger 6.5 % at 25.6 rebuilds/orbit.
5. **The positive claim was never run, and my completion corrects it.** Shear-sized per-body deadlines (η = the k-window, 0.099 rad) give 2/37 misses at 7.5 rebuilds/body/orbit; η = w/2 gives **0/37 at 14.3**. But cadence at matched budget (R = 0.134 yr, 6.7/orbit) also gives 2/37 — indistinguishable, because per-body max|Δn| ≈ 0.75 is nearly uniform across the ±0.08 AU band, so displacement deadlines degenerate to cadence. Prediction 4's premise (cadence starves the tail) is unsupported at belt density; the defensible law is a **size rule** (budget = shear rate × window), not a trigger rule. The two differ only under heterogeneous shear — exactly taleb-09b5's co-orbital concentrations.
6. **Novelty.** The phase tier is taleb-09b5's gold (cited by the author); the churn-rate measurement and the element-currency kill appear in no HISTORY/board entry. Same-day siblings overlap: q-skin ("a slack skin is exact in its regime… the literal skin is killed") and taleb-3ec1 — not citable if they finished after 09:16; the integrator should reconcile. Lesson 1 (fit-key memo on the kick) collides with the 5 Oct kill (taste log; law.md "Not adopted: a quantized (E, L) memo… random walk") — uncited.
7. **Goal fit.** On the board's #1 live question and the top scaling risk; P9 honored (kills configurations, keeps the method). No 10× realized: the 15× cheapness carries 35/37 misses; the working trigger costs 3.5–7× per-kick; nothing is deleted yet.

**The one experiment to gold.** The author's own follow-up, with the corrected claim: on `crates/encounters`' real certificates, a shear-sized maintenance (rebuild when accumulated |Δn|·Δt crosses η ≈ 0.5–1 × the neighbour window) reaches zero misses across seeds and densities, cost measured against the a-compatible pair tier, with displacement vs cadence discriminated in a heterogeneous-shear (co-orbital formation) scene where the two differ. My lab version already shows the zero-miss side feasible (0/37 at 14.3/orbit; 6.5 % at N=1600) — the real-certificate transfer and the discrimination remain.

**What the author missed.** The C/D hang was their own heap flood, two minutes from fixed, and the fixed version contradicts prediction 4's premise; their only D data point used a mis-sized η = π/2 (16× the window, equivalent to static), so the proposed trigger was never shown to work at all; the kill is density-scoped (per-kick already achieves zero misses at ~60 candidates/body) and the boundary was never measured; prediction 2's failure is uncounted; lesson 1 re-proposes a 5 Oct kill; `run.log` is empty, so the run-log identity claim points at nothing.

### 20261006-1249-inversion-fd48
Grade: gold

**Abstract.** Claim: the k=4 phase-neighbour train adopted from gold taleb-09b5 is unsound inside its own firing domain — partner rank is the contact-band multiplicity m̂ (bodies within ρ), unbounded under concentration and not bounded by the Binet-diameter trigger — and that trigger reads ~47 on the motivating fleet (e ~ 1e-3), so as specified it never fires there. Reproduced bit-for-bit: jam misses 35.3/37.1/36.0% over seeds (trigger 0.44–0.60 in every kill scene), m̂ = 11.1 scaling ∝ n/σ_λ (controls 4.44, 5.64), the gold's own scene dilute at m̂ 0.21 / max rank 4, the 6-ship echelon dropping a rank-5/5 encounter. My independent re-implementation confirms 21–45% misses depending on metric and convention. Cost to adopt: a design edit (k_i = m_i + 1 at rebuild, m-triggered rebuild, m as the trigger's second number), no new structure.

**Reasons.**

1. **Reproduction: exact.** Clean tree + `git apply work/patch.diff`, `cargo build --release -p emergent-encounters --bin invert` (CARGO_TARGET_DIR=/home/glmlab/lab-target-inversion). Every dossier command rerun: `echelon`, `table` (7 rows), `jam 0.004 800 27|1|2`, `jam 0.01 800 27`, `jam 0.01 800 27 1e-5 1e-3`, `jam 0.004 400 27`, `xcheck 0.004 400 27`. Every number matches the recorded JSONL bit-for-bit; the only differing field is `truth_s` (0.32→0.40 s — timing on a shared runner). Memory well under 2 GB; each run < 7 s.
2. **Predictions: pre-registered and held.** File times: `predictions.md` predates all four `experiments-*.jsonl`. The pre-registered kill criterion ("any scene with trigger ≤ 1 yields ≥ 1 true encounter with rank > 4 on both directions") is met by the echelon (rd 5/5) and every jam. Magnitude misses are disclosed, not hidden: the trigger table read 47 against their predicted 9–13 (same direction), and the echelon's sort-position rank measured 1 against a predicted 5 (tidal shear; the jam carries that metric — and kills it: miss_long 728–823, rl_max 15–17).
3. **Adversarial (my own instrument).** I re-implemented the jam scene from scratch in Python (xorshift64*, integer-period Kepler propagation per `kepler.rs`, dense 641-sample brute force over all pairs, my own rank code — no shared path with `invert.rs`): n=800, σ_λ=0.004, seed 27 gives 5927 contacts below ρ (3041 with interior argmin, consistent with truth's 3481 interior minima), k=4 sort-rank miss 27.2% (21.2% interior-only), distance-rank miss 44.7%, max_rl 16. The author's 35.3% (union metric over truth's list) sits inside my bracket; nothing about the interior-minimum convention manufactures the miss. Rank distribution (p50 3–4, p90 11–12, max 24–28) rules out a knife-edge at rank 5; the miss is not tie-fragile. Concentration tightens it: contacts grow 3481→11916 at σ_λ=0.002, and m̂ scales ∝ n/σ_λ across their three controls (11.06, 4.44, 5.64) — a density number, exactly as claimed.
4. **Novelty.** The adoption is live: board taste log (6 October, gold taleb-09b5: "every real encounter lies within partner rank 4 along the orbit") and `lab/refs/opus-motion/memo.md` §6 line 275 ("a fleet in formation is a Fermi frame (dense order), so the phase-neighbour certificate (rank ≤ 4) belongs there"). The memo's own list of known holes (line 277: e > 0.7 tightening, horizon-edge misses) does not include rank multiplicity; no HISTORY entry measures rank under concentration. This is the measurement of the hole the gold flagged as untested, and it inverts the constant the integrator adopted yesterday — in the very regime (dense formation) the memo assigns the certificate to.
5. **Goal fit.** Board's top scaling risk: candidate work must track real encounters. The premise "rank ≤ 4 in-domain" is now measured false; a constant k was a bandaid over a density number (PRINCIPLES #19). The fix respects "regimes are chosen by dimensionless numbers" (#4 — m̂ is the missing number) and "a failed experiment kills that configuration, never the method" (#9 — the train survives, k=4 dies). Cost honestly tracks real contacts: O(n·m̂), quadratic exactly when contacts are.
6. **Residual (does not affect the grade).** The gold's own dossier branch (`claude/lab-20261006-0346-taleb-09b5`) is not in this checkout's refs and the remote needs credentials, so the trigger formula "max pairwise Binet distance / eps_u ≤ 1" rests on the author's quotation of the gold abstract. I checked robustness: the in-domain kill (findings 1–2) does not depend on it, and the author's own table shows e = 1e-4 already reads 4.8, so any reasonable variant of the diameter test leaves the motivating fleet (e ~ 1e-3) far outside the domain. Findings 1–2 alone carry gold.

**What the author missed.**
- The proposed fix k_i = m_i + 1 is a tautology only at rebuild time; m breathes between rebuilds, and the breathing rate over a horizon was measurable with the machinery they already built. That measurement, not the kill, is the natural next run.
- A decaying-jam control (free shear dispersing the bunch) would bound the exposure window they only argue for ("~ρ/Δv"); station-keeping realism is asserted from the game's intent, not measured.
- The two metrics disagree in opposite directions across scenes (distance carries the echelon, phase carries the jam; phase even misses 7.5% in the gold's dilute scene): neither is the certificate's invariant — the sound width is max-over-horizon m, which points at the same missing measurement as the first item.
- The dossier quotes the gold's trigger formula without a file-and-line pin; checkers on fresh checkouts cannot reach the gold's branch, so finding 4 arrives unverifiable (I treated it as secondary for that reason).
- Minor: the "predictions held" section counts the trigger-domain prediction (47 vs 9–13) as held "by more than predicted"; a 4× magnitude miss in a computed quantity suggests the ΔV ~ e/p estimate was mis-derived, worth one line of diagnosis.

### 20261006-1249-taleb-e013
Grade: gold

**Abstract.** The claim reproduces exactly and survives adversarial attack: the phase-neighbour train adopted this morning (taleb-09b5) has k ∝ true-longitude line density, not k = 4. Full ladder regenerated bit-for-bit (`python3 probe.py` in a clean copy): μ̂ linear in n (μ̂/n = 7.0–7.5×10⁻⁶ over n = 12.8k→256k), k=4 silently misses 3.4% of real encounters at 128k and 17.7% at 256k; at the gold's own n=800 an ϖ-aligned formation puts 29% of encounters beyond distance-rank 4 (max 23). My fresh seeds (256k: 17.0–18.9%; 128k: 3.3%), a random rank subsample (no bias: 17.0% vs 18.9%), S=256 resolution, and a 3D inclination variant all confirm. Gain: it reopens this morning's adoption before the certificate ships — the premise "rank 4, O(n·k)" is wrong at the 10⁶ scale it was adopted for. Cost of adoption: zero build; the integrator drops k-as-constant and takes the ρ-wide radial-phase strata as the design hypothesis to test.

## Reproduction

- `work/patch.diff` is empty; `probe.py` is self-contained. Copied to /tmp and run whole (`python3 probe.py`, 288 s, < 1 GB): **every statistic in every case identical to `all.log` and to the dossier table** (checked field by field, C0 through X1 and the nest check 44/44). Only wall times differ (shared machine: X1 181 s vs the author's 182–194 s).
- Extrapolation arithmetic verified: μ̂(10⁶) = 7.2 from the measured μ̂/n; raw Poisson(7.2) tail gives 84% miss at k=4 (the dossier's 94% sits between this and the capped empirical calibration — the measured points sit 4.6–48× above raw Poisson, so "misses most" is robust; 94% itself is not a number); Poisson p99.9 → k ≈ 17 (dossier: 16); store 10⁶·16·72 B = 1.15 GB (dossier: ~1.1 GB; gold's k=4 → 0.29 GB ≈ its "~300 MB").

## Held-out predictions

- The anchor (C0) reproduced the gold's own observation first — no strawman: ranks ≤ 4, zero misses on the gold's workloads at n ≤ 800, then the break is demonstrated elsewhere.
- Load-bearing predictions held: linear μ̂ ∝ n (4 points, factor 20 in n); miss emergence (0 → 0.24% → 3.4% → 17.7%, X1 just above the registered 8–16% band, disclosed); distance-rank resilient under ϖ-random workloads; the ruin arithmetic's direction (store ~4× low, setup ×4).
- Failed honestly and disclosed: the pre-registered bunching mechanism was wrong (σ_λ-axis flat at μ̂ 0.17–0.18 — itself a clean negative: the gold's phalanx adversarial cases probed an axis the physics decouples), re-registered before D/X1 (file mtimes consistent with this; not independently verifiable from the restored tree); the amended D magnitudes over-predicted ~2.5× (trend held).

## My adversarial cases (four, all pass)

1. Fresh seeds: X1 seed 15 → miss(k=4) λ = 18.9%, μ̂ 1.96; C3c seed 71 → 3.3%, μ̂ 0.98. Not seed artifacts.
2. Sampling bias in the rank cap: the author ranks the first 2500 encounters by earliest argmin step (0.12% of X1's 2.1M). Random 2500 subsample measured in the same pass: X1 17.0% vs 18.9%, C3c 3.2% vs 3.3% — unbiased, though the author neither flagged nor tested it.
3. Resolution: C3c at S=256 (halved step) → miss 3.8% vs 3.4% at S=128. Sampled dips are not manufacturing the misses.
4. Inclination (the author's declared blind spot, asserted not run): i ~ Rayleigh(1e-3), 3D detection. Encounter rate falls 33× (2.06 → 0.063/body/orbit) exactly as claimed ("z can only thin crowding"), and the surviving encounters still carry μ̂ 0.79 with miss(k=4) λ = 2% at 128k while dist-rank collapses (max 2) — confirming the mechanism: interlopers are λ-close, 3D-far.

## Novelty

No HISTORY entry (latest is H0214, 5 October) covers the train's k-scaling; the target gold was adopted this morning per the board's taste log. Nearest records: H0212 (the off-time lab's 39 results, q-candidate-degree's fixed-density O(N²) risk) and the board's top scaling risk. This run answers it for the train specifically: at fixed distribution the train's O(n_c·k) is O(n_c²·ρ/W_λ) — the same ruin it deleted. Differs from r8 v2 (30 September, other algorithms' exponents) in mechanism and target.

## Goal fit

Direct hit on the board's top scaling risk, and a premise kill of an adopted certificate at the exact scale it was adopted for (the 10⁶ formation fleet that motivated the gold). PRINCIPLES #19 "a fix signals the wrong representation" — a 1D longitude sort is the wrong water for a 2D contact; #4 "regimes are chosen by dimensionless numbers" — the operative number is ρ·d_λ, not σ_λ; #13 "errors never compound" — the misses are silent (the train replaced the tier that would have found them) and enter the canonical history. The one honest caveat, disclosed by the author: the gold's binary is not in this checkout, so the attack reads the board's quote of its claim; the anchor reproduction makes a strawman unlikely.

## What the author missed

- The rank-cap sampling (first-by-step 2500) was unflagged and untested; it happens to be unbiased (my check 2). Luck, not design.
- The 94% headline is calibration-dependent (84% raw Poisson); "most encounters missed" survives, the specific number does not. The 10⁶ claim rests on a measured line plus tail argument, not a direct run — disclosed, and n=256k at 17.7% direct makes it hard to doubt the direction.
- The radial-phase strata repair is stated, not tested — that is the next run: show k collapses to O(1) within ρ-wide strata on the same ladder (including the D-series formations), which converts this premise kill into the replacement certificate.

### 20261006-1354-system-d9fb
Grade: silver

**Abstract (for the integrator).** Claim: the encounters tier's three adopted parts do not
collapse into one storeless watch; the per-body equation-of-center band (2N certificates,
zero setup) is a sound necessary filter but misses tangency-dip encounters, firing the
pre-registered kill. Reproduced bit-for-bit from the dossier's commands (all four scenes;
27 s + 48 s). I re-adjudicated 5 of the claimed REAL misses with my own 4M-point sampler:
all real; the (13,134) dip verified root-for-root (roots 0.1254 apart, d≈1.4e-3 each, true
min 8.1e-5 between). My adversarial scenes strengthen the kill: highe 54% missed, resonant
80%. Gain: the tier's O(N²) store is measured deletable (cone pairs 0.14–0.69·N²/2 vs 2N
certs) and its windows are exonerated as second-order structure. Cost to adopt: the hybrid
fragment is proposed, not built. Not gold: two table cells the shipped code contradicts
(epochs/body "5.3" vs actual 13.17; cl_caught "1" vs 0) and a silently dropped prediction.

**Reasons.**

1. **Reproduction (exact).** `python3 watch.py uniform:250:1 uniform:500:1` and
   `phalanx:250:4 clumped:250:3` in a clean copy regenerate every stored cell (wall times
   differ ≤0.1 s). Encounters, misses, evals/enc, cone pairs, pp_evals max all match.
   patch.diff is empty (all work inside the run folder; nothing to apply).

2. **The kill is real and honestly earned.** predictions.md (14:08) predates watch.py
   (14:22) and metrics.json (14:24). P1 was pre-registered as the kill and fired. I
   independently re-adjudicated 5 misses across three scenes with my own sampler: min
   distances 8.10e-5, 6.64e-5, 5.87e-6, 6.17e-5, 1.44e-5 — all < ρ, matching the author's
   adjudication. The diagnosed mechanism is verified: two alignment roots 0.1254 apart with
   d≈1.34e-3/1.45e-3 at each, the true minimum 8.1e-5 between them with |ΔΛ| = 7.7e-5 rad
   and no crossing — a tangency, exactly as reported. P2 and P6 held (conjunction-less
   6.9% belt / 37% phalanx, band catches 13/16 phalanx; cone fraction 0.14–0.69 of N²/2).

3. **Adversarial cases (mine) strengthen the kill.** highe:250:2 (e 0.7–0.9): 7 of 13 truth
   encounters missed (54%); resonant:250:5: 4 of 5 missed (recall 20%). The failure is
   structural across regimes, not a σ_e = 0.01–0.05 artifact. The shared Newton-Kepler
   solver is not the culprit: residual ≤ 2e-7 rad at e = 0.95, far below ρ. The watch's
   precision is perfect by construction (every hit is a direct distance evaluation); the
   harness's two "FALSE ALARM" labels at highe are adjudicator-anchor artifacts — golden-path
   hits register no roots, so adjudication anchors at T/2 and searches the wrong window.

4. **Novelty.** No HISTORY or board entry tests a storeless band watch or the
   equation-of-center unification; this is new work, connected to (not redoing) r8 v2's
   conjunction-less leak and taleb-09b5's phase train.

5. **Goal fit.** Board focus item 3 and the top scaling risk: the measured cone fractions
   re-derive the materialized tier's O(N²) memory exposure at fixed geometry, and the
   negative result narrows q-skin's successor to "setup → per-body constants, windows
   stay". Respects PRINCIPLES #9: the failed experiment kills the configuration
   (unification), never the method (the tier's windows are exonerated as the second-order
   structure). Honest self-diagnosis; the author's own pre-registered kill makes the report
   trustworthy.

6. **Why not gold.** The record, not the physics: (a) the uniform:500 "epochs/body 5.3"
   cell is contradicted by the shipped code (6,587 epochs → 13.17), and the "flat and
   small / the O(N²) never materializes as work" narrative built on it is false —
   epochs/body grows ∝ N at fixed geometry (1,262 → 6,587 total for ×2 N) and reaches
   270/body at highe; epochs per **pair** is the bounded quantity. (b) cl_caught "1" vs
   actual 0. (c) P7 was silently dropped — my run answers it: evals hold (6.3e4/enc, within
   the predicted 3×) but recall collapses to 20%, a material omission for a soundness
   claim. (d) P3 is called "not decidable" though its own two points give slope
   log(7.80/5.95)/log 2 = 0.39, above the pre-registered 0.3 kill. (e) The adoptable
   fragment (per-body C_e band epochs as the candidate filter, tier's windows and walk
   inside epochs) is proposed but neither built nor measured — gold's "adopted within one
   step" is not met.

**The one experiment that would make it gold.** Build the hybrid in `crates/encounters`'
own harness: per-body C_e constants + closed-form band epochs as the candidate filter
(deleting the store), the tier's per-pair second-order windows and Diophantine walk inside
epochs. Belt scale (N ≥ 1e5, ρ = 1e-4): zero adjudicated misses including tangency and
resonant scenes, setup cost per-body not per-pair, work per real encounter ≤ the tier's.

**What the author missed.**
- P7's answer existed one run away and was dropped without a word: resonant recall 20%.
- The false "flat epochs" narrative — the honest invariant is epochs per pair, not per
  body; per body it grows with N and with e² (270/body at highe, evals/enc 8.95e6).
- The FALSE-ALARM adjudicator-anchor bug (roots unregistered for golden-path hits);
  harmless here but it would corrupt any precision claim at high e.
- The stored metrics.json omits the two uniform scenes the dossier table cites; they
  regenerate exactly, but the frozen record does not contain them.
- P3's own two-point slope already exceeded the pre-registered kill threshold.

### 20261007-0800-inversion-7532
Grade: silver

**Abstract.** Claim: the co-orbital gold's rank-4 certificate is a snapshot property of tight formations only; with σ_e = 0.02–0.05 a k=4 certificate misses 60–88% and needs element coherence, shear-scaled refresh, per-pair routing. Everything reproduces bit-identically (events.csv md5 equal; D cross-ranks re-derived from raw rows). But the headline is a definition artifact: the gold pre-registered rank "by current distance," and on the author's own scenes the distance- and true-longitude-rank at closest approach is med 0 with 0.000% > 4 at every σ_e; the 60–88% exists only in mean-longitude order — the axis the gold rejected. Surviving, definition-robust: one-orbit-stale watch misses 1.2% (tight) / 44.7% (loose); the 87.3% fleet×belt routing hole. Adopt routing + refresh cost, not "element coherence gates misses."

## Reasons

1. **Reproduction: exact.** Clean tree, empty `work/patch.diff`, built with `CARGO_TARGET_DIR` outside the folder (`cargo build --release --offline`, ~1.5 s), full rerun 119 s, < 200 MB, 4 threads. `fleet-out.jsonl` identical to the author's except the `secs` field; `events.csv` md5 `bd310ef82a43dadc2345c466bfc5576b` identical. Every dossier number matches the jsonl: A 0/0.0% dyn, 1/1.9% lag-1, 57/93.4% static; B 1/6/14 medians with 4.9/60.4/88.0% >4; C 3/29.3%, 5/57.3%, 170/96.9%; D fleet-fleet 1/0.5%, fleet-belt 8/73.7% (re-derived from the first-4,000 raw rows), 87.3% = 9427/10796. The 4σ_e·n/2π = 1.9/7.6/19.1 law tracks the measured medians within ×0.8. No number differs.

2. **Predictions: pre-registered, but they cannot cover the flaw.** `predictions.md` 08:06:15 vs outputs 08:14:40 — before the decisive run. P1, P3, P4 held; P2 held *under the author's own definition*, which is the problem: the prediction is phrased in mean-longitude rank, so pre-registration certifies the quantity, not its fit to the gold. Minor: P3's δa shifts between full width (~9, predictions) and half width (4.5, dossier); both inside the factor-2 tolerance, measured 5.

3. **Attack: the headline breaks against the gold's actual definition.** The gold's folder is one `git show origin/claude/lab-20261006-0346-taleb-09b5:...` away in this repo — the author's declared "main risk" was checkable. Its `predictions.md` pre-registers "partner rank (**by current distance, min of both directions**) <= 4"; its dossier says "watches k nearest by distance"; its blind second checker already re-tested with a true-longitude instrument and held r_max ≤ 4 at e-spread 1000×ρ. I rebuilt the author's scenes exactly (same seeds 21/22/23/31, same `truth_pair`, same ρ) and re-ranked at t_m:
   - B σ_e=0.02 (5,760 events): mean-λ med 6 / 60.4% >4; **true-longitude med 0 / 0.0%; distance med 0 / 0.000%**.
   - B σ_e=0.05 (6,000): mean-λ 14 / 88.0%; **true-longitude 0 / 0.0%; distance 0 / 0.000%**.
   - C (927): mean-λ 3 / 29.3%; **true-longitude 0 / 0.0%; distance 0 / 0.000%**.
   At closest approach the partner is within ρ, hence within ρ/r in true longitude — the equation-of-centre gap is a property of mean-longitude ordering only. The gold's own lesson 6 says exactly this ("co-orbital proximity aligns *true* longitude"; its first λ-binned brute missed 193/233 for this same reason). The A-control cannot expose the mismatch because at e≈0 all three orderings coincide — the control reproduced the gold's number while silently swapping its definition.
   **What survives the definition change:** the shear break and the routing break. Lag-1-orbit *distance* rank: med 1 / 1.2% >4 (A, tight), med 4 / 44.7% (C, loose) — the ordering churn ≈ (3/2)(δa/a)·n ranks/orbit is real in any ordering and is the rebuild rate the gold's O(n·k) cost statement omitted (its own check2 called it "the actual cost driver — unmeasured"). The composition hole is rank-independent: 87.3% of fleet-body encounters are fleet×belt, invisible to any ordering of the fleet alone; per-pair routing is a genuine new condition on the trigger.

4. **Novelty: first attack on the adopted gold.** The builder follow-up `20261006-1931-b-coorbital-cert-152e` died on a 429 with no dossier. Nothing in docs/HISTORY.md or the docs bounds the certificate's scope, measures its refresh cost, or addresses composition routing; q-candidate-degree and r8 covered fixed-density cost, not this.

5. **Goal fit.** Board's top scaling risk (encounters at N). Two of the three claimed conditions are real corrections the encounters design (v2) must absorb: per-pair routing for baths, and a churn-scaled rebuild term (shear (3/2)(δa/a)·n, and 4σ_e·n/2π under e-spread — in any along-orbit ordering). The third condition (element coherence gates *misses*) is refuted by my re-measure. PRINCIPLES: "A failed expectation is not automatically a failed method: diagnose which one broke (H0183)" — this run's own headline needed that diagnosis; and the how-to's "never strawman" — the control reproduced the number, but the definition was the strawman.

## The one experiment to gold

Implement the gold's actual watch — k=4 nearest by distance (or true-longitude train), rebuilt on overtake/set-change — and measure misses plus rebuilds across σ_e ∈ {0.005, 0.02, 0.05}, the C shear scene and the D bath. My adversarial numbers predict zero misses at t_m everywhere (distance rank 0.000% >4 on all 19,140 B + C events) with rebuilds following the churn law; the correction then lands on the right object: routing + churn-scaled rebuild, and the "element coherence" gate dies.

## What the author missed

- The gold's run folder was reachable from this repo's remotes with one `git show`; its pre-registered distance-rank definition and its check2's true-longitude validation were available before writing the dossier. The "what would make it wrong" branch fired, and its impact estimate ("halves, 2e not 4e — does not vanish") is wrong: at contact the coupling vanishes entirely.
- A control whose regime makes all candidate definitions coincide cannot falsify a definition choice; the only scenes that separate them (B, C) were scored with the author's own definition.
- The run undersells its best surviving result: the 4σ_e·n/2π law is a rebuild-rate law for any along-orbit ordering (the gold's unmeasured cost driver), not a miss law.
- `truth_pair`'s local-minimum criterion inherits the standing-proximity leak the gold itself exposed (1–2%; r8's conjunction-less 0.5–6%): the truth undercounts, undisclosed here. Direction is conservative for the surviving breaks; it cannot rescue the headline.
- Bookkeeping: D ran 63.8 s (just over the 60 s guidance, disclosed); B's medians weight events over 115 frozen pairs (disclosed); single seed per scene, planar only (disclosed).

### 20261007-0842-inversion-0a7a
# Check — 20261007-0842-inversion-0a7a

Grade: gold

**Abstract.** The claim: the train certificate adopted from gold taleb-09b5 is not O(n·k) — its watch churns ∝ e·n_c/σ_λ, re-importing quadratic work per orbit, and the gold's contact-rank statistic cannot see it. Reproduced bit-for-bit: s0-control (churn 46/86 per body per orbit, ev 601, ratio 69.15×), s1-e005 (199/302.5, 50 encounters), cone-s0/s1 (19900/19900 pairs, 0 missed). I measured the author's missing n_c point: churn/nc ≈ 0.20 flat over nc = 200→1600 (46/79/158/344), and the gold's λ-uniform corner goes 0→4→16 over nc = 200→800→3200. Cost: the b-coorbital-cert trigger gains one dimensionless number (2e·n_c/σ_λ) and per-orbit budgets, before that build lands. The dossier's tier-2 "blindness" side-claim is refuted (see below).

## Reproduction (clean tree, `git apply work/patch.diff`, same build command)

- `invert s0-control`: every field matches the stored JSON (encounters 64, churn p50/p90 46/86, ev 601/807, work ratio 69.15, ranks ≤ 1, leads capped, window_churn 132, 14/64). Only `brute_us` (wall time) differs, as expected.
- `invert s1-e005`: exact (churn 199/302.5, 50 encounters, ev 0, ratio NaN — the disclosed ∞-regime).
- `invert cone-s0`, `cone-s1`: exact (64 and 50 encounters, cone saturated at 19900/19900, 0 missed — the O(n²) control validates the binned brute force).

## Predictions

`predictions.md` mtime 08:51:17; all scenario JSONs 09:03–09:04; dossier 09:09. Pre-registered before the decisive runs. P2 (the kill), P3 (non-vacuity at σ_e = 0.02), P4 (statistic blindness) held. P1 under-predicted churn 2.3× (46 vs ≲20 — in the kill's favour, reported); P5 failed (reported; its charitable branch was pre-registered as "the cost is then the kill").

## My adversarial cases

1. **The n_c slope the author could not run** (nc=800 died with the author's shell timeout; slope was [INFERENCE]). Churn at σ_e=0.001, σ_λ=0.05, 1 orbit, exact author metric: nc 200/400/800/1600 → p50 46/79/158/344. churn/nc = 0.230/0.198/0.198/0.215 — flat: linear in n_c confirmed. Per-orbit watch events = n_c·churn ∝ n_c² while encounters ∝ n_c: the board's "candidate work must track real encounters" is violated by the adoption at scale, as claimed.
2. **The gold's own safe corner.** λ-uniform, σ_e=0.001, ϖ clustered: churn p50 0 (p90 4) at nc=200 — confirming the author's scoping honesty (the gold's measured corner was genuinely safe) — rising to 4 at nc=800 and 16 at nc=3200. The mechanism enters the gold's corner well before 10⁶ (spacing TAU/n_c vs wobble 4e-3), so "any 10⁶ fleet is deep in the violating regime" holds on both λ distributions.
3. **The author's named next experiment, adjudicated.** For all 50 real encountering pairs at σ_e=0.005, the shipped tier 2 emits windows (84 Cross + 16 Wide, zero pairs with no window) and `pair_events` finds 50/50, 0 missed. The dossier's "sections() emits zero windows for e-spread pairs" misread the instrument: `ev` counts numeric-window state evaluations; analytic Cross sections cost 0 evals and are full windows. Tier 2 is **not** blind to e-spread encounters. This removes the dossier's side-anomaly and simplifies adoption (the cone tier saturates and misses nothing here; tier 2 stays sound).

## Novelty

No HISTORY entry or board note measures watch maintenance/overtake churn; the gold's adoption (board taste log, 6 October; taleb-09b5: "rebuild on overtakes", "~4×10⁶ sections (~300 MB), setup falls 10⁵×" at 10⁶) asserted the cost model the run falsifies. components-4643 killed deferred *setup* on the old tier — a different tier and question. The nearest prior instrument lesson (agreement ≠ independence, 5 October) is cited by the author and obeyed (the O(n²) control caught the author's own velocity-angle binning bug, disclosed).

## Goal fit

Top board risk (5 October): candidate work must track real encounters. Measured: the adopted remedy's work ∝ n_c² per orbit at fixed spread, with events outnumbering real encounters by ~10⁵× at 10⁶. It shows a premise of an adoption is wrong before the queued b-coorbital-cert build encodes it, and names the missing dimensionless number — PRINCIPLES #4 ("regimes are chosen by dimensionless numbers") and #19 ("a fix signals the wrong representation"); #13's ruin shape. Adoptable within one step: amend the trigger and state the certificate's budget per orbit, not per setup.

## Reservations (do not change the grade)

- The 69× headline uses churn p90 × k=4 (full-watch rebuild). The charitable reading (p50, incremental, one sections per change) gives 9–17× — still ≥ 3× (P2's own threshold). The formula is printed, so the choice is auditable; the kill survives every reading.
- The 0.9 TB pool constant (1.3e10 pairs) does not reconstruct cleanly from the stated parameters (I get 0.9–3 TB depending on the wobble reading); the conclusion (≫ 8 GB, well under the quadratic's ~36–40 TB) holds under all of them; "55×" is ~43×.
- "Even in the gold's own near-circular control" conflates the gold's λ-uniform fleet (safe; churn 0) with the gold's bunched σ_λ=0.05 rank scenario (where the gold also claimed the certificate and where churn is 46). The dossier's evidence section keeps the two corners straight; the claim sentence is the loosest sentence in it.
- At σ_e ≥ 0.005, per-rebuild sections are analytic Cross windows (0 evals), so churn there is event-count, not evals, cost — the dossier prints those ratios as NaN and says so.

## What the author missed

- `ev` is not a window counter: the "zero windows / wholesale blind" reading was an instrument artifact, and the adjudication (my case 3) refutes it. It was honestly parked as unadjudicated, but printed as measured fact in evidence point 5.
- The n_c slope was one 12-second run away (my ladder ran 200→1600 in ~11 s single-threaded, no brute force needed); the killed nc=800 point did not require the full probe with its 300 s parent timeout.
- The churn law follows in one line from the equation of center (wobble ≈ 2(e_i+e_j), swaps ≈ 2 per orbit per pair within wobble, pairs within wobble = 4e·n_c/σ_λ); the author's own lens section says a dynamics lens would have derived it — correct, and the measured ladder agrees with that line (predicted 0.2·n_c, measured 0.198–0.230).

### 20261007-0842-second-20261007-0800-inversion-7532-c1bf
Grade: silver

**Abstract.** Claim: the gold's watch (k=4 nearest by current distance, either direction, rebuilt on set-change) misses zero encounters on the inversion's six scenes — its 60–88% headline is a mean-longitude artifact — and the true cost is churn 0.95–20 entries/body/orbit (crossover σ_e ≈ k/n), 87% bath-driven, with lazy 1-orbit refresh missing 0.16–67% (leads 0.12–2.8 orbits). Reproduced bit-exact: `events.csv` md5 equals the inversion's branch blob; `watch-out.jsonl`/`lead.csv` identical to the author's; 152 s, < 300 MB; predictions pre-registered, P2 held on all six scenes. My attacks: zero-miss breaks at 5.7% in a dense convoy (ρ ≳ k·spacing — needs a density gate); churn scales √n, not n (12.4→18.2→24.1 at n=600/1200/2400); σ_e=0.3 still safe. Design conditions, certificate unbuilt.

## Reasons

1. **Reproduction: exact.** Clean out-of-place rerun (`CARGO_TARGET_DIR=/tmp/fleet2-target-check cargo build --release --offline`, then the binary from /tmp so the author's record was never overwritten): `events.csv` md5 `bd310ef82a43dadc2345c466bfc5576b` — verified equal to the inversion's own blob on `origin/claude/lab-20261007-0800-inversion-7532` (both its `work/events.csv` and `work/fleet/events.csv`), not just self-consistent; `watch-out.jsonl` (`05db7fe3…`) and `lead.csv` (`0891d73e…`) identical to the author's files; 152.5 s wall, 4 threads, well under memory. Every dossier table number re-derived from the jsonl: D's fleet 13.46 = 269,158/(200·100) and belt 18.94 = 1,515,073/(800·100) from `entries_split` (these are population *means*; the column header says "(med)" — `pop_med` is 13.33/18.06 — trivial); 87.0% belt-driven fleet entries = 234,207/269,158; 87.3% fleet×belt encounters = 9,427/10,796; entries-per-encounter 7.07 (A) to 521.7 (C). The lead-time model `miss ≈ 1 − E[min(2·lead, T)]` recomputed from `lead.csv`: A 0.0016/0.0016, C 0.363/0.377, D 0.632/0.674 (pred/meas), B deviating exactly as disclosed (0.49/0.35 at σ_e=0.02). Definition premise ve

2. **Predictions: genuinely pre-registered.** `predictions.md` (mtime 17 min before the outputs) contains quantitative bands with honest failures on the far side (P3: B(0.05) 19 vs band ≥ 24; P5: D 67% vs 0–40% band; P6 magnitudes), the signature of real pre-registration. P0 held (bit-identical, twice). P2 — the decisive kill-the-gold criterion (> 0.5% anywhere) — never fired on the six scenes. P1, P4 held.

3. **Attack: four adversarial cases (instrument = the author's `fleet2.rs` copied to /tmp with a λ-window population knob and tunable sampling cadence; scenes below).**
   - **E1 dense convoy** (n=300 in a 0.02-rad λ-window, σ_e=0.003, varpi uniform, ρ=1e-3; ~12 neighbours within ρ vs k=4, the regime the dossier itself flagged "untested"): **exact-policy misses 5.71%** (7,650/133,908; 5.73% on the first 100k rows), distance rank > 4 at t_m for 2.49% (max ≥ 6, the instrument cap), missed contacts are grazing (d median 9.1e-4 = 0.9ρ) with ≥5 nearer bodies, and only 23/2,506 rank>4 events are rescued by the either-direction rule. The author's own kill threshold (0.5%) fires 11× over. Lead collapses to 0.032 orbits; 1-orbit refresh misses 86%; churn 45/body/orbit vs the law's 1.44 (31×). **The zero-miss property needs a validity gate — expected neighbours within ρ ≲ k (πρ²·local density) — which no scene in the run or the gold measures.** Co-orbital concentration is the gold's own subject; a player convoy is a game-realistic workload.
   - **E2 high eccentricity** (σ_e=0.3, cap 0.5, n=600, ρ=1e-3 — 6–15× beyond the sweep): **zero exact misses**, dist rank max 0: the continuity/cadence argument holds even at pericentre closure; the certificate is more robust than tested. Refresh failure worsens (92%, lead 0.03); churn 59 measured vs 288 by the law (saturation deepens to 4.9×).
   - **E3 n-scaling** (B σ_e=0.02, seed 22, nested populations, 30 orbits): entries/body/orbit **12.4 (n=600) → 18.2 (n=1200) → 24.1 (n=2400)**: √n (predicted 17.5/24.8 from the n=600 anchor), not the linear 1.6·σ_e·n (24.8/49.6). The dossier's cost extrapolation O(n·(k+churn)) with churn ∝ σ_e·n is wrong in its n-dependence in the churn-dominated regime — the true total is ~O(n^1.5) at fixed σ_e (overestimate, i.e. conservative for adoption, but the law as printed mis-extrapolates). Zero misses held at n=2400 (dist rank max 1).
   - **E4 cadence control** (B σ_e=0.05 at 1024 samples/orbit): churn 20.0/20.45 (med/mean) vs 19.0/20.1 at 256 — the saturation below the linear law is real physics (overlapping swaps), not coalescing undercount (+1–2%, inside the disclosed <8%); miss_exact still 0; miss_ref1 57.0% identical.

4. **Novelty.** The deciding experiment for a live dispute; nothing prior implements it. The builder follow-up `20261006-1931-b-coorbital-cert-152e` died on a 429 with no dossier (grade "missing", branch checked); docs/HISTORY.md (through H0215) has no watch/churn/rebuild measurement; the inversion (today, silver) is the only prior and this run supersedes its headline on the primary record.

5. **Goal fit.** Board's top scaling risk (encounters at N / the co-orbital certificate). The run converts the gold's bare O(n·k) into a measured cost structure (churn term, crossover, bath inheritance, refresh-at-churn) and kills the inversion's miss headline — exactly "A failed expectation is not automatically a failed method: diagnose which one broke (H0183)", and "Compute only surprises" — churn *is* the ordering's surprise rate. But the adoption unit is a set of conditions, not a component: the O(1)-per-entry incremental rebuild is asserted, not built (admitted), and the certificate's validity domain now has an unmeasured boundary (E1). Not adoptable within one step as a working tier; the design v2 can adopt the numbers.

## The one experiment to gold

Build the watch in the encounters crate as a real incremental structure — event-driven rebuild on set-change (the asserted O(1)-per-entry sorted-structure update), refresh paced by churn, with the density gate πρ²·n_local ≲ k wired into the regime trigger — and measure end-to-end evals per real encounter against the quadratic window tier on the six scenes plus a convoy scene and an n-sweep, checking churn against the √n law. Zero misses at ≤ the tier's cost, including E1's convoy, is gold.

## What the author missed

- The validity condition of the zero-miss claim. "Zero misses, everywhere" is true only while ρ ≪ k·neighbour-spacing; a 30-second convoy scene breaks it at 5.7% — the author's own P2 kill threshold. The gap is disclosed ("untested here") but not measured, and the dossier's headline and abstract do not carry the condition. The gold's trigger (Binet diameter vs ε_u) does not gate on contact density either — this is a *new* condition, not a restatement.
- The churn law's n-dependence was inferred, not measured, and is wrong (√n, E3); the lens section says so, but the dossier's cost model and the crossover arithmetic are stated as if linear in n.
- Population means are presented under a "(med)" column header for D (pop_med is 13.33/18.06; the quoted 13.46/18.94 are entries-split means) — cosmetic.
- The instrument itself recomputes kNN every sample (O(n log n) per sample = 256·n·log n per orbit); the papered-over gap between that and the claimed O(n·(k+churn)) is exactly the unbuilt incremental structure, and in 2-D decorrelated fields (varpi spread, E2) the "sorted along-track adjacent swaps" maintenance assumption is weakest.
- The lead-time floor under adversarial closure (E1/E2 leads ~0.03 orbits) means churn-paced refresh must run ~30×/orbit in dense regimes — a stronger statement than "refresh must track churn", visible in the author's own C and D numbers but not drawn out.

### 20261007-1106-inversion-e618
Grade: gold

**Abstract.** Claim: the adopted phase-neighbour train certificate's k=4 (gold taleb-09b5) is an artifact of nc ≤ 800 evidence — the watch width is the ρ-arc occupancy, linear in nc. Reproduced bit-for-bit (8/9 sweep rows + smoke; lon-rank>4 = 0 → 0.086 → 0.661 → 0.910 at nc = 200 → 12800, occupancy 2.3 → 79.7, dist-rank>4 = 0.550 at 12800); the gold's distance-rank metric recovers to 0.000 exactly where the certificate fails (σ_e = 0.01). My attacks confirm: seed 8, σ_λ = 0.005 (occupancy doubles), isotropic ϖ, and the mean-longitude order (p50 rank 223, 99.1% > 4). At 10⁶ bunched: ~450 GB or ~90% misses (gold: 300 MB). Gain: a premise correction landing before the pending b-coorbital-cert build. Cost: amend that spec — derive k from occupancy or order 2D.

## Reproduction (clean tree, `git apply work/patch.diff`, CARGO_TARGET_DIR=/home/glmlab/lab-target-1, Linux x86)

- `invert smoke`: identical — enc 232, dist-rank max 2, lon-rank max 3, occ 2.3/9, validation `val_miss: 0` (grid vs full O(nc²) pair scan).
- `invert sweep`, rows 1–4 + 6–8: **every counted field identical** to sweep2.log (enc 305/4777/59030/935820; lon gt4 0.000/0.086/0.661/0.910 with p50/p99/max 0/3/3, 1/7/12, 8/26/33, 34/97/114; dist max 2/7/20/73 with gt4 0.000/0.005/0.211/0.550; occ 2.3/6.0/20.9/79.7, occ_max 9/18/50/156). Only timings differ. Row 9 (σ_λ=0.02) not re-run; I ran the stronger untested direction instead (below). The dossier's table matches sweep2.log cell for cell.
- Arithmetic re-derived: k*(10⁶, uniform λ) = 10⁶·2.2ρ/TAU = 35.0; k*(10⁶, σ_λ=0.01) = 79.7×78 = 6.2×10³ → sections 10⁶·k*·72 B ≈ 448 GB; the gold's k=4 store = 288 MB ("≈300 MB"); shortfall ≈1.5×10³×.
- `predictions.md` mtime 11:16:51 < sweep.log 11:18:42 < sweep2.log 11:51:33 < dossier 11:56: written before both decisive sweeps, and the predictions contain a claim the data then broke (dist-rank ≤ 4 everywhere; max reached 73) — the signature of genuine pre-registration.

## Attack (own binary `invert_x`, same fleet/instrument code, arbitrary configs; tree restored after)

1. **Seed 8, headline config** (3200/0.001/σ_λ=0.01): gt4 = 0.674, occ 21.2 (seed 7: 0.661/20.9) — prediction 5's ±0.15 band holds.
2. **σ_λ = 0.005** — the direction the author ran out of time for: occ 40.3 ≈ 2× 20.9, lon p50 16 ≈ 2× 8, gt4 = 0.829. The 1/σ_λ law holds in both directions (author measured only the widening one).
3. **Isotropic ϖ** (pom_half = π): gt4 = 0.696, occ 20.6 — indistinguishable from ±0.1. The mechanism is angular, apsidal-independent, exactly as predicted; the author's disclosed unmeasured control now measured.
4. **The sort key the gold never pinned down.** The train "sorts by longitude": the author ranked the *true*-longitude order — the favorable reading. In the *mean*-longitude order (where Kepler overtakes and rebuilds actually happen; the gold's own brute binned mean longitude), partner rank at contact is p50 **223**, p99 955, max 1359, gt4 = **0.991** at nc=3200 — the equation of center ~2(e_i+e_j) ≈ 40ρ dwarfs the ρ-arc (the gold's own instrument lesson, its point 6). No reading of the certificate saves k=4; the inversion is conservative.
5. **Instrument robustness**: the scan uses `state()`, the rank pass `state_halley()`; max position delta 1.1e-15 over all sampled contacts (11 orders below ρ), 0 rank disagreements. The two-solver split cannot explain the ranks. The `d0 > 1.2ρ` refine skip is sound (true d_min ≥ d0 − ρ/8 > ρ).
6. **Contact-rate corroboration**: per-body contacts per orbit grow 0.76 → 3.0 → 18.4 → 73.1 with nc (and double at σ_λ=0.005: 36.2) — ∝ occupancy, as the "bunched fleets are contact plasmas" reading requires.

## Predictions

Held, including the honest miss (dist-rank max 73 at nc=12800, predicted ≤ 4, reported as strengthening the inversion). The kill criterion (lon-rank max ≤ 4 at 12800) did not fire: max is 114.

## Novelty

docs/HISTORY.md (through H0215), the board, HANDOFF and the gold's own check contain no measurement past nc=800 and no occupancy mechanism. The gold's `ranks` mode evidence was n_c ∈ {200, 800} — and its nc=800 case was *uniform-λ* (a_hw=1e-3, σ_λ=0, seed 22, 0.5 orbits); the bunched family (σ_λ ∈ {0.05, 0.02, 0.01}) was measured only at nc=200. The gold's checker attacked at nc ≤ 800 too (σ_λ=0.005, n_c=400, e×10 — all max rank ≤ 4 by *distance*). This is the first run past the evidence base and the first to name the certificate's true watch width. Nothing to cite as prior art.

## Goal fit

The board's top scaling risk ("candidate work must track real encounters") and HANDOFF's live item "co-orbital concentration … work must track real encounters" cite this exact certificate. The pending directed build `lab/lenses/b-coorbital-cert.md` (queued for both the GLM and Codex lanes) instructs a builder to implement O(n·k) on the premise "every encounter lies within partner rank 4" — this run falsifies that premise at the 10⁶-fleet scale the certificate was adopted for, before the build runs. That is "shows that a premise is wrong", adoptable within one step (amend the spec: k derived from occupancy, or a 2D order; no crate implements the train — verified). PRINCIPLES: "A fix signals the wrong representation" (#19 — constant k over a 1D order is the wrong water for a 2D contact problem); "regimes are chosen by dimensionless numbers" (#4 — the occupancy nc·ρ/λ-spread is that number, mistaken for a constant); ruin arithmetic before ruin (#25). Evidence rules respected: predictions pre-registered, controls on both sides (grid vs brute; dist-rank vs lon-rank decoupling), the gold's numbers never strawmanned (reproduced 232 vs 233–238 family).

## What the author missed

- **The gold's evidence base was weaker than stated.** "The gold's sweep stopped at nc=800, where k* ≈ 4–6 sits just under its k=4" — the gold's nc=800 case was uniform-λ; its bunched evidence was nc=200 only. At the author's own nc=800 bunched config, 8.6% of contacts already exceed k=4 (0.5% even by distance, max 7). The k=4 claim was already failing at the gold's scale in the tight case it never ran.
- **The sort key is unspecified, and the worse reading is the natural one.** Rebuild "on overtakes" lives in mean-longitude order, where ranks are ~30× larger (my attack 4). The build spec must pin the order; neither the gold nor this run did. The inversion survives either reading — but the 2D-order conclusion follows a fortiori.
- **Undisclosed instrument iteration:** sweep.log (first sweep) reports occ 3.0/5.1/12.8 at configs where sweep2 (and my reproduction) give 2.3/6.0/20.9, with identical encounter/rank fields — the occupancy window changed between runs without a word in the dossier. The shipped code regenerates sweep2 exactly, so nothing is unreproducible, but the taste log's rule (numbers the shipped code cannot regenerate) applies to sweep.log as it lies in the folder.
- **"Smoke reproduces the gold (232 vs 233)"** is a different seed (7 vs the gold's 27): family agreement, not a seed-exact reproduction. Substance unaffected.
- **The 10⁶ uniform-λ claim stays arithmetic** (disclosed): occ ≈ 35 there, so k=4 fails at the gold's fleet scenario too by the same mechanism, but ranks at uniform λ were measured at no nc. A ~10⁵ uniform run would close it; at nc ≤ 1.28×10⁴ uniform occupancy is < 1 and the test cannot bite.

### 20261007-1420-inversion-384f
Grade: silver

**Abstract.** Claim: the gold's phase-neighbour certificate silently drops all encounters under two other concentration topologies (crossing lanes 247/247, pericentre funnel 413/413 cross-recall 0.000 — structural, reproduced exactly), while the window tier it replaces is forced quadratic by orbit-path intersection alone (candidates exactly C(N,2), ×4.01 per fleet doubling at fixed linear density, bit-for-bit); the repair ranks bodies by arrival time at the orbit-intersection locus (funnel k8 1.000, fresh crossing seeds k8 0.995–1.000). But the gold's own dossier scopes its train to the Binet-clump regime via a regime switch — S2/S3 route to the pairwise tier there (quadratic, not silent drops), so the kill lands on the board's routing summary, as the author concedes. Evidence defects: stored s3.json is empty, the "1.000 fine-seeded" and "0.993 at k=4" numbers do not regenerate (shipped code: 0.8866/0.983), and `invert.py s3` takes 458 s, not "~10 s". One experiment short.

## Reproduction (clean tree, no patch to apply; shared runner, load 0.9–1.8, each process ≪ 2 GB)

- `python3 invert.py s1`: 393 encounters, phase-rank 0.964 (k8 1.000), window 28,680 = 73/enc, conc 48.7× — matches the dossier row exactly (no stored artifact existed).
- `s2`: identical to s2.json on every recall (cross 0.000, internal 0.9855, 79,800 cand = 121/enc, coarse locus cross 0.1012); checks 2257 vs stored 2258 (one pair; recalls identical at 4 decimals).
- `s2scale`: **all 72 counted fields identical** — 270/601/1204 encounters, candidates 19,900/79,800/319,600 (×4.010, ×4.005), 74→133→265 cand/enc, cross recall 0.000 at all n. Only wall-times differ.
- `s2fine`: identical to s2fine.json — cross 0.8866 (k4), total 0.9667 (k8), union 0.9485, 3,009 checks. Note: this contradicts the dossier's table ("1.000 (fine-seeded run)") and claim line; the 1.000/6,391-checks figure came from an earlier script version preserved nowhere (patch.diff is 0 B, folder untracked).
- `s3`: stored s3.json is **empty**. The shipped command does regenerate the row — 413 truth, 55 checks / cross recall 0.000, 12,720 = C(160,2), locus 2,886 checks, k4 **0.983** (dossier says 0.993), k8 1.000, conc 125.7×, mgf 0.019 — but in **458 s**, not the claimed ~10 s (862 locus clusters × per-body golden-section refinement); the author's own final rerun evidently never finished either.
- Truth instrument validated: an independent dense O(N²) brute force (fixed upper-triangle extraction) returns the **set-identical** 413 on S3.

## Predictions

`predictions.md` mtime precedes every decisive artifact (46 min before s2scale, ~40 before s2/s2fine/s3); content shows genuine pre-registration (P1 cand/enc > 300 vs measured 121; P3 > 200 vs 31 — both honestly reported as misses). P1/P2/P3/P5 held; P4 partially held and is honestly qualified — but the table and claim line still cite the unregenerable 1.000. Kill criteria for the attack: not triggered (0.000 cross recall stands).

## My attacks

1. **Seed robustness (S2 seeds 12, 23, correct 2-group element grouping):** phase-rank cross recall 0.000 both (structural); fine-gate locus cross recall k8 0.995 / 1.000 — the repair is real and seed-robust at k8, but k4 sits at 0.846–0.878, so the P4 "≥ 0.95 at k=4" target does not generalize beyond seed 11.
2. **Congestion extreme on the funnel** (tspan 0.03 → 2,735 encounters, phase-rank still 55 checks / 0.000): my independent exact-arrival rank at the one true locus gives **k4 0.22 / k8 0.40** — the fixed-k certificate collapses under jams; k must scale with flux density. Diffuse (tspan 3.0): 1.000 at k4. n=320: 0.63/0.92. "The same O(n·k) trick with k=4 covers all three topologies" overreaches.
3. **No grouping rescues phase rank on the funnel:** forcing all 160 bodies into one orbit group gives recall ≤ 0.24 even at k8 — the miss is not an artifact of the element tolerances.
4. **Truth adjudication** (above): the recall denominators are exact; my first sweep claiming 986 was my own bug (self-pairs from a zeroed triangle), retracted after ultra-fine arbitration.

## Novelty

docs/HISTORY.md, git log, the gold (8d339c5) and q-candidate-degree (eaac72b) contain no locus/arrival-time work. The gold's own dossier already scopes its train to "when a cell's clump number (max pairwise Binet distance / eps_u) ≤ 1" — i.e. shared-orbit concentration — and keeps the pairwise tier elsewhere; the board's taste log ("replaces the quadratic tier, triggered by a dimensionless number") is the summary this run breaks. The new content that survives: two measured topologies outside q-candidate-degree's belt domain where the geometric candidate tier is exactly C(N,2) at fixed density (its "answered for fixed density" was dilution-only), and the arrival-time-at-locus rank as the general certificate form (formation = degenerate locus) — same trick as the Binet-cone Diophantine work's regime question, different mechanism.

## Goal fit

Board risk #1 (candidate work must track real encounters) and a correction to an adopted gold's routing rule; PRINCIPLES #13 "errors never compound — a dropped encounter is not an error, it is a lost event" and #32. The author honestly flags that the frequency of lanes/funnels in the actual game is unmeasured (argued from the goal, not from scenes).

## The experiment that would make it gold

The author's own named one, done certificate-grade: replace the sampling-tolerant locus gate with exact orbit-pair curve intersections (the funnel's locus is exactly the shared pericentre; the lanes' are the two nodes), ship it in `invert.py` regenerable ≤ 60 s (my exact single-locus arrival rank already runs in milliseconds and gives k8 0.998–1.000 across seeds and the default funnel), and measure k against flux density (the jam case needs k ≫ 4) — pre-registered, with `s3.json` actually stored.

## What the author missed

- The decisive S3 artifact was never stored and the S3 command runs 45× over its stated time; a checker following the dossier's commands verbatim (60 s budget) would grade the run's second headline unreproduced.
- The table's "1.000 (fine-seeded run)" is contradicted by the run's own s2fine.json (0.8866/0.9667); P4's prose is honest, the headline is not.
- The k=4 form of the repair fails congestion extremes (0.22 under a jam) — "O(n·k) at the gold's rank" was tested only at one congestion level.
- The attack's framing ("silently drops every encounter") targets the board's summary; under the gold's actual Binet-clump switch those scenes route to the pairwise tier (quadratic, no drops) — the run's value is the routing correction plus the new topologies, not a kill of the gold's certificate in its own regime (S1 control confirms it works there: 0.964/1.000).
- `invert.py` was edited after all stored runs (mtime 4 min before the end, same instant as the empty s3 rerun) with no history to audit what changed; "see run history in git patch" points at an empty patch.diff.

### 20261007-2002-taleb-9fa1
Grade: lead

**Abstract.** The headline — "a λ sort drops 33–60% of encounters; safe only under θ" — is an instrument artifact. The λ key is `pom + mean_anomaly(0)` with no `mod τ`: keys span [0, 2τ), so half the swarm sorts a full circle away; every ϖ-spread scene has the wrap active, the only aligned scene cannot wrap — bug confounded with "mechanism". Reproduction is bit-for-bit; adding `.rem_euclid(TAU)` makes λ equal or better than θ everywhere (gold corner: λ miss4 0.000, p95 3, identical to θ). The pre-registered void rule (gold-corner λ miss4 > 0) fired and was overridden. Survives (θ/M columns, reproduced): M-key invalid, k_p95 ≈ 1.6·C, shear drift, ρ-negligible — a trigger refinement, not a 10× move.

## Reasons

1. **Reproduction: exact.** `git apply work/patch.diff`, then `cargo run --release -p emergent-encounters --example phase_probe -- main` and `-- scale`: every stored field of `main.jsonl`/`scale.jsonl` regenerates identically (0 differing fields; only `truth_s` excluded). The dossier's tables faithfully quote the JSONL. Reproduction of the numbers is not in question — the interpretation is.

2. **The λ column is a wrap artifact.** `phase_probe.rs`, key construction: `lam0 = x.pom + x.mean_anomaly(0.0)` — both terms ∈ [0, τ), no `rem_euclid`, so lam0 ∈ [0, 2τ). The θ key *does* wrap (`atan2(...).rem_euclid(TAU)`); `mean_anomaly` is intrinsically wrapped. Debug dump (same seed, same 1146 encounters): pair (46,82) carries keys 5.824 vs 12.103 (> τ = 6.283). Geometry proves this is fatal, not physical: encounter pairs at the gold corner have |Δλ(t_enc)| ≤ 2.4e-3 (the probe's own `dlam_p95`) and |Δn·t_end| ≤ 1.5·da·60π ≈ 2.8e-2 rad, so |Δλ(0)| ≤ 3.1e-2 rad — measured max 2.35e-2 — i.e. true λ-rank ≈ 1–3. The stored p95 = 106 is impossible for a wrapped key. Adding the one-character wrap and rerunning all 12 scenes: λ miss4 = 0.000 / 0.000 / 0.018 / 0.080 / 0.574 (gold corner → s3e-2) vs θ 0.000 / 0.000 / 0.032 / 0.145 / 0.455; λ p95 ≤ θ p95 in every fat scene (17 vs 24 at n=1200). λ(0) and θ(0) are interchangeable certificate keys; neither dominates.

3. **The author's pre-registered void criterion fired and was overridden.** `predictions.md`: "The positive control failing (gold-corner λ miss4 > 0) would void the instrument instead." It failed (0.332); the dossier instead promoted the failure to the finding ("λ is not a valid certificate key at all"). H0183: "A failed expectation is not automatically a failed method: diagnose which one broke." The author's prediction 1 (λ miss4 = 0 at the gold corner) was in fact *correct physics* — their own derivation in `predictions.md` ("needed rank in λ ≈ n·(2(e_i+e_j)+ρ/a)/τ") predicts it, and their own measured Δλ(t_enc) ≈ O(e) confirms it. The number contradicted the derivation and they trusted the number.

4. **The "mechanism" control is confounded.** `pom_window = 0` forces pom = 0, so `lam0 = M(0)` can never exceed τ: the aligned control is the only scene whose λ column is unbuggy. "The ϖ spread is the mechanism" reads the bug's on/off switch as physics. Real spread effect on a wrapped λ key: 0.184 → 0.574 at k = 4, but 0 at k = 16 in both — the dominant budget is C either way (aligned-s3e-2 at C = 11 misses at k = 4 with *zero* spread).

5. **The predictions bookkeeping is wrong in both directions.** The dossier says "two failed". Against the stored numbers, prediction 3 also failed (λ miss4 0.595 < 0.8) and prediction 7's "≳90%" (0.691). Against the fixed instrument, prediction 1 *held* while 2, 3, 4 and 6 failed (fixed shear λ miss4 = 0.416, not "small"). The predictions section is not a reliable record of what the instrument said.

6. **What genuinely survives** (θ/M columns reproduce exactly, and none of it depends on the λ bug): the mean-anomaly key is invalid under ϖ spread (miss4 ≈ 0.97 everywhere — though M is not a longitude, so the warning is thin); the rank-budget law k_p95 ≈ 1.6·C, k_max ≈ 2.7·C (measured 6/13/24 and 10/23/41 at C = 3.7/7.4/14.7), so "rank 4" is a C ≲ 1.5 statement and the phase tier is O(n²·σ_e) at fixed internal e; the shear horizon drift (θ miss16 0.009 at 30 orbits vs early-5-orbits 0.049 miss4 — a t=0 sort decays without rebuild); ρ's negligible share (0.145 → 0.114). This refines the adopted gold's "triggered by a dimensionless number" into a measured trigger. It does not change the gold's design, and the run's stated contribution — stopping `b-coorbital-cert` from shipping the wrong key — evaporates: among longitude-type keys there is no wrong choice, θ ≈ λ.

7. **Novelty.** No HISTORY entry addresses the key choice or the budget law; the gold (20261006-0346) recorded neither. The budget law is new and measured. But its size is one trigger constant, not a component deleted or a premise killed.

8. **Goal fit.** The red-team intent was right (a dropped encounter compounds, principle 13; "before any freeze, one GLM red-team"), the probe cheap (~35 s), the scenes well-designed (the controls were exactly the right controls — which is how the bug was findable). But the deliverable's central sentence is false, and shipping its advice ("safe ONLY under θ") would add a constraint with no content.

## What the author missed

- The `mod τ` — one character. Their θ key wraps; their λ key doesn't; they never diffed the two key constructions against each other even after the two columns disagreed by 100×.
- Their own void rule and the H0183 duty to diagnose a failed positive control before reading it as physics.
- The internal contradiction: measured Δλ(t_enc) ≈ O(e) *proves* λ-alignment at encounter, hence a wrapped λ(0) sort must work at small e — their own predictions.md derivation said so before the run.
- The confounded aligned control (pom = 0 ⇒ no wrap possible).
- That λ vs θ at fat e is a wash (λ better at p95, θ better at max): the honest law is "any longitude key works with k ≈ 1.6·C + drift margin, rebuilt on a cadence set by Δa".

**If re-derived:** wrap the key, keep the C-budget and cadence results, drop the θ-only claim — that rerun is a legitimate small probe of the gold's trigger, silver at best.

### 20261007-2057-taleb-efc9
Grade: gold

**Abstract (for the integrator).** The phase-neighbour certificate behind the in-flight `b-coorbital-cert` holds only for strict formations. Grid reproduced bit-for-bit (16 scenes); battery headlines exact (debris n=768, R=0.02: n_enc=396, k\*=384=n/2, 98.5% of encounters missed at the gold's rank 4; R-scan 0.005→0.05 pins k\* at n/2). My independent harness (own Kepler solver, rotation matrices, ranking) re-derived the debris scene exactly and sw180/se005/convoy within seed noise; ranking by true anomaly also fails (k\*=190); k\*∝n measured (0.99·n/2 at n=96–768); T-convergence clean (symmetric difference 0); the lag formula predicts the max-rank pair (191 vs 190). Adopt: size k by the group's lag tail, drop fixed rank 4 and the concentration trigger; swarm tier stays open. Cost: small, mid-build.

**Reasons.**

1. **Reproduction.** Clean tree, `patch.diff` empty. `coorb_probe.py 384 8192` → all 16 scenes identical to `grid_results.json` (n_enc, k\*, miss@4, setup: convoy 1341/9/11.9%; σ_e=0.02 237/9/13.5%; σ_e=0.05 229/20/45.0%; uniform-ω 191–192=n/2; bimodal 140/60.3%; setup 73,536=all pairs). Battery headlines re-run: sw180-e03@R0.05 2338/192/98.5% and debris n=768 396/384/98.5% — exact.
2. **Independence (the shared-harness risk the dossier itself flagged).** My own sampler (different Kepler init + residual assertion, per-body rotation matrices, time-chunked truth, searchsorted rank) reproduces: debris n=768 R=0.02 seed 11 → 396/384/98.5% exactly; sw180-e03 seed 13 → 221/190/98.2% (author 221/190/98.2%); se005 seed 13 → 233/21/47.6% (author's seeds: 229–231/20–23/36–45%); convoy seed 13 → 1406/11/18.1% (author's seeds: 1341–1450/9–11/11.9–17.9%).
3. **Adversarial cases.** (a) Ranking by true anomaly at epoch instead of M: k\*=190 (sw180), 383 (debris) — the defense "any phase-like coordinate fails" holds; misaligned pairs meet at Δν\*=Δω (battery medians 84.3° vs 84.2°). (b) n-scaling, measured not just analytic: k\*/(n/2) = 0.875/0.990/0.990/0.995 at n=96/192/384/768 — the certificate is O(n²·lag) at any dispersion; at n=96 with only 18 encounters k\* is already 42. (c) Truth completeness: sw180-e06 (e=0.6, worst sampled) at T=8192 vs T=24576 half-offset grid: 233 encounters both, symmetric difference 0. (d) Mechanism: the closed-form lag reproduces the max-rank pair analytically (predicted rank 191 vs measured 190, pair Δω=108.4°, Δe=0).
4. **Predictions.** `predictions.md` (16 min before the decisive outputs; scripts written after it, results last — order verified from file times). Pre-registered kill criteria: the fragility claim would die if k\*≤4 everywhere — it didn't; the no-man's-land (k\*≥16 and setup/enc≥100) confirmed. Predictions 3,4,6,7,8 held; the two failures (convoy beats rank 4; σ_e=0.02 already misses) are reported as failures in the dangerous direction, not buried. Controls pass on the certificate's home turf (rings k\*=2–3), so the instrument works.
5. **Novelty.** HISTORY (this checkout, ends 26 September) and docs contain nothing on dispersion fragility of the phase-rank certificate. The design basis is the 6 October gold's "every real encounter lies within partner rank 4" (board taste log, `20261006-0346-taleb-09b5`), and `b-coorbital-cert` is in flight on both the GLM and Codex lanes (HANDOFF). Not a relitigation: the prior gold measured formations; this run bounds its constant (rank ∝ phase density × lag — even a randomly-phased convoy at 30° breaks rank 4) and kills its generalization (98.5% silent misses on collision debris, which is certain game content).
6. **Goal fit.** Top board scaling risk ("encounters at N"). A silent miss is the ruin error type: PRINCIPLES #13 "we don't want errors that can compound" — here compounding by absence, invisible downstream; #34 "the oracles are guards" — a certificate must reject what it cannot certify. The lag (in rank units) as the regime chooser replaces the "formation/swarm" category (#4). Kills a configuration (fixed rank 4), not the method (phase ordering): #9.

**What the author missed.**

- Two text slips against the stored evidence: the σ_e=0.05 seed-robustness parenthetical "20–25 / 36–52%" (stored runs give k\*=20–23, miss 36–45% — the 25/52 endpoint is not in any stored file), and the bimodal formula "≈ (n/2π)(π+4e)" (=265, not 140; the correct bracket [π−4e, π] gives [119, 192] ⊃ 140). Neither affects a headline claim.
- The node-dispersion scene (n_enc=18 at workable R) sits below the author's own pre-registered n_enc>20 floor; its k\*=6 is weak evidence, though consistent.
- σ_a>0 rank churn and non-Kepler (perturbed) swarms unmeasured — disclosed, but the certificate's trigger must eventually be sized under σ_a>0, where the frozen-rank argument doesn't apply as stated.
- No measurement of the allocator side (p99 frame cost under tier switching) and no p99/tail statistic on work, only k\* extremes; the constructive third tier (crossing-loci bucketing) is a sketch, not probed with this harness — one cheap experiment away.
- Grid's own debris scene at R=0.005 had n_enc=6 (violating the pre-registered floor); honestly superseded by the R=0.02 battery row in the dossier table, but the table does not say which row replaced which.

### 20261007-2155-inversion-7655
Grade: gold

**Abstract.** Claim: the adopted gold's k=4 phase-neighbour train certificate (taleb-09b5) is not packing-safe. Reproduced bit-for-bit, all 9 scenes: r_max ≤ 4 at Π ≲ 0.8 (the gold's regime), r_max 8 / 0.33% misses at Π=2, 10–12 / 2.1–2.8% at Π=4, 18 / 13.2% at Π=8, seed- and N-stable. My attacks extend it: Π=16 gives r_max=36 — exactly the measured law r_max ≈ 2Π+4, so it extrapolates; a 40-ship jam at local Π=4 inside a mean-Π=0.6 scene misses 6.5% of jam encounters (mean-based triggers fail; the watch width must be the local tube count); rank ≤ tube-count−1 held structurally in every scene. The flagship Fermi checks (1° arc → Π≈5,730). Adoption is one spec line pre-build: `encounters` is referenced by nothing on main (verified).

**Reasons.**
1. **Reproduction, clean tree, exact.** `python3 packing_probe.py` (29 s): all six main scenes identical to `packing-results.json` — every field, including r_max 4/8/10/18, frac_r_gt4 0/0.00327/0.02805/0.13199, mult 10/14/19/30. The robustness block (seed2, N480) is not driven by the committed `__main__`; I reconstructed the `run_scene` calls and got all three scenes bit-identical to `packing-robustness.json` (r_max 3/12/11, frac 0/0.02108/0.02797). Bookkeeping gap, not fabrication.
2. **Pre-registration genuine.** predictions.md (21:59:44) < probe script (22:00:37) < results (22:01:06) < robustness (22:02:17). P1, P2, P3, P6, P7 held; P4/P5 failed only on miss-fraction magnitude (2.8% vs ≥10%, 13.2% vs ≥40%), same direction, disclosed — while their rank and multiplicity components held (r_max 10≥8, 18≥12; med mult 8, 14). The kill rests on r_max > 4 at tube occupancy > 4, which held everywhere predicted and everywhere I attacked. The author's own kill criterion (r_max ≤ 4 at Π=4, 8) did not trigger.
3. **Attack (5 scenes, 2 controls, my instrument mirrors theirs; peak 1.3 GB).**
   - **A3fix (true Π=16):** r_max=36 = 2·16+4, frac 52.5%, mult_max 46. The corrective law extrapolates exactly, so it is measured, not fitted noise.
   - **A4 (mixture):** 40 ships jammed in 10ρ (local Π=4) inside a mean-Π=0.585 scene: jam r_max=10, jam frac 6.5%. The author's flagged worry is real: a trigger on mean packing routes this cell to a k=4 train that misses. The fix must use the local (max) tube count.
   - **A2 (vertical thickness h~Rayleigh(1.5ρ) at Π=4):** r_max=6, frac 0.25% (flat control 11, 4.7%). Modest thickness halves the miss but k=4 still dies.
   - **A5/A1 (the one real overstatement):** at fixed Π=4, adding e~Rayleigh(1e-3) (10ρ breathing) collapses r_max to 2 with zero misses (control on my seed: r_max=10, 2.5%, matching theirs); the gold's own phalanx family at peak packing 3.19 gives r_max=2, mult_max=3. So "the miss fraction is a function of Π alone" is family-conditional: the binding invariant is the **3D tube count**, and radial spread protects. This *supports* the adopted fix (watch width = tube count) and explains why the gold's evidence never saw the break — its family never filled the tube — but the headline law and the flagship Fermi (Π≈5,800) implicitly assume a radially-coherent fleet. That is the station-keeping fleet the gold targets, so the kill stands; a thick fleet's tube count is far below Π.
   - **r_max ≤ mult−1** verified structurally (at the sampled closest approach d_ij < ρ, so every ship strictly closer is inside the tube) and held in every scene, theirs and mine (36 ≤ 45 at Π=16).
4. **Novelty.** docs/HISTORY.md, the board and the gold's dossier contain no packing/tube-count work. The gold's own checker demanded the train's invariant statement and hypothesised *radial spread* as it; this run measures the invariant (rank ≤ tube count − 1) and inverts that hypothesis (P6: e-spread is protective — confirmed by my A5). The gold's trigger (element-space clump) is indeed packing-blind by construction: it reads element spreads only, not N (their disclosure that this is read from the dossier text, not the binary, is honest and the reading is correct).
5. **Goal fit.** The board's top scaling risk (candidate work must track real encounters) and HANDOFF §Headed-next 5. It corrects an adopted gold's premise before it is wired in — "shows that a premise is wrong" — and adoption is one step: `crates/encounters` is depended on by nothing on main (verified: no Cargo.toml or source references outside the crate). PRINCIPLES: "regimes are chosen by dimensionless numbers" (#4 — the gold chose one number where the regime needs two: element clump *and* tube count); "A fix signals the wrong representation" (#19 — k=4 was a constant standing in for an unstated invariant); "An ant cares about a raindrop…" (#33 — the tube count is the scale's own resolution).

**What the author missed.**
- The Π-law's scope was never measured at fixed packing with radial spread (my A5): the dossier's "function of Π alone" is false outside radially-thin arcs, and the flagship Π≈6,000 Fermi should be conditioned on the fleet's radial coherence — the number that matters is the 3D tube count, which the fix already uses. The kill survives this; the headline does not, unconditioned.
- The robustness scenes are not regenerable from the committed script as-is (reconstructed calls reproduce them; add a mode or the calls to the log).
- The cost side is asserted, not measured (watch rebuilds per overtake scale with sweep·Π) — the author flags this; the train's price at Π~8+ is unmeasured, and at the flagship's tube counts the conclusion (route to contact compute) is what carries.
- Minor: the "1 → 2 → 5 → 8 → 14" multiplicity ladder mixes the loose e-spread scene's median (1) into a uniform-arc series whose own Π=0.8 median is 2; immaterial to any conclusion.

### 20261007-2344-taleb-6f01
Grade: gold

Abstract: The adopted co-orbital certificate (gold 20261006-0346) silently drops contacts outside a domain far narrower than "under a formation": partner rank ≈ N·(spread)/2π, so M-rank drops 90–97% of contacting pairs at any realistic spread (even Δe=10⁻⁴), λ-rank survives static orientation but cracks with the epicyclic wiggle and window drift, and period/phase-density triggers are blind to all of it (dn_rel flat at 1.5e-4 while miss goes 0.6→97%). I reproduced every table bit-identically (pilot, wscan 10/10, escan 6/6) and confirmed the scaling law adversarially (fresh seeds, k=2/8, brute-force independence). Adoption: one gate S=N·(Binet extent + Δn·W)/2π ≲ k with λ sort-key, straight into the queued b-coorbital-cert build — with a safety margin my N=600 case shows it needs.

## Reproduction

Clean tree (`work/patch.diff` empty), script copied to /tmp (it writes JSONs to its cwd). numpy 1.26.4, Linux x86, load 3–7, mem <1 GB per process.

- `python3 cert.py pilot`: identical to author's `pilot.json`, all fields.
- `python3 cert.py wscan`: 10/10 cases identical, including `binet_radius` to the last digit.
- `python3 escan`: 6/6 cases identical (the N=600 e0.02 cases ran 93–138 s here vs 137–223 s author; shared machine, order of magnitude only).

## Predictions

`predictions.md` file time precedes every result JSON by 5–15 min (log order consistent). Held-out items I tested independently:

- Fresh seeds: D=0.5/seed 77 miss_M 76.2% (author 72.0%), dvec=1e-4/seed 99 85.5% (author 90.0%) — both within the promised ±5 pp; miss_λ 0 both.
- k-scaling: k=2 measured 88.1% vs formula 91.6% (holds); k=8 measured 43.4% vs 66.5% — the closed form is loose at large k, in the conservative direction (real misses fewer than modelled, so the derived zero-miss domain D*≈2πk/N understates safety).
- The author's two reported prediction failures (D=0.2/0.5 low; lamsafe 20% vs <2%) are honestly flagged and correctly diagnosed (the e·sin(Δϖ/2) term).

## Adversarial cases

1. **Gate soundness (my main addition):** dvec=1e-4 at N=600 (seed 55): full gate S = 2.72 < k=4 → phase tier engaged, yet the λ tier drops 3.2% of contacting pairs (max λ-rank 7). With the author's N=300 case (S=1.36, 1.7% leak) this shows the leak grows with N at fixed scatter while the gate passes: **S ≲ k separates catastrophic (S≫k: 20–97%) from clean, but does not deliver the certificate's zero-miss contract in the band S∈[1,k]**. The build needs a margin (or wider k), not bare S≲k.
2. **Brute independence, done right:** the author's cross-check fields are broken — `candidate_pairs` records (i,j) in λ-order (430/845 keys have i>j), so `truth_in_subsample`/`brute_agree` miss i>j events (my raw rerun gave a spurious `brute_agree: false`; the pilot's `true` was orientation luck with its single event). Recomputed with normalized keys on dvec=1e-3, 2000-pair subsample: brute 4 = pipeline 4, no discrepancy either way — the λ-adjacency truth list is complete here. Same bug inflates `contact_pairs` ~2× (241 oriented keys vs 125 distinct pairs; 149 vs 79 on the aligned control). I recomputed miss fractions unweighted over distinct pairs on 5 cases: they shift by ≤1 pp (e.g. lamcrack-N300 37.7%→38.5% miss_λ, D0.5 72.0%→72.0%) — the dossier's percentages stand.
3. **k=2 on the wscan family:** λ-leak appears (3.5%) once drift-rank S=1.35 approaches k — consistent with the drift term of the scaling law.
4. Wide-belt and rank-at-encounter behaviour confirmed in the reproduction (miss_λ_enc=0 everywhere, incl. wide-belt).

## Novelty

docs/HISTORY.md (through H0215), board taste log, docs/law.md: the gold's domain was never bounded; the nearest entries are the gold itself ("every real encounter lies within partner rank 4", adopted) and q-candidate-degree's "zero misses to 10⁶", which the gold overrode for concentrated workloads. This run bounds the override. Timely: `b-coorbital-cert` is first in lab/queue.txt and in the Codex sol queue — the gate lands before the build ships.

## Goal fit

Top scaling risk on HANDOFF (candidate work at scale / co-orbital concentration). Shows a premise of an adopted gold is wrong — at the motivating 10⁶ the certificate is safe only for exactly law-maintained lockstep (allowed spread ≈2.5×10⁻⁵ rad), invisibly to the natural triggers: a ruin path (principle 13, silent contact loss corrupting every downstream certificate), closed before the build. Principle 4: S = N·Δ/2π is the dimensionless number that chooses the regime; principle 22: the scatter the game itself creates decides the tier. The 10⁶ extrapolation is integer rank arithmetic, not float extrapolation (principle 24). The lens limits (speed, 3D, game-design call) are stated honestly.

## What the author missed

- The gate margin (adversarial case 1): percent-level leak at S∈[1,k], growing with N; a threshold at k/2–k/3 or a widened k is needed for a zero-miss contract. The author's own evec-1e-4 table row contains this leak but "working gate" was not qualified.
- The orientation-key defect: pair counts double in scattered cases and the brute cross-check is void as shipped (though the truth list itself is sound — verified here). "Pairs are the honest unit" is right; the pair key was not.
- The tier could re-sort mid-window (kinetic maintenance): then the failure appears as churn ≈ N·S swaps per window instead of dropped pairs — same S, same gate, but the build's failure mode should be stated per reading.

### 20261008-0041-inversion-9a9d
Grade: silver

**Abstract.** Claim: the co-orbital train certificate (gold taleb-09b5) is unsound as adopted — its rank-4 guard measured distance-rank while the deployable mean-longitude sort misses 79% of encounters on the gold's own validation fleet (p90 30, max 55; robust on four seeds), and crossing outsiders pay 0.25·n_clump cone-certified pair-sections for zero encounters (1,994/8,000, 0 fx in 2 orbits). Everything reproduces bit-identically (trigger, econ, all six probes; only wall-times differ). New and decision-relevant: the wrong-coordinate kill on the gold's own scene, the trigger decomposition (ΔU-only p50 0.041 — the e-vector, not a-spread), the seam constant, and the correction that the gold's 4/233 window-tier "misses" are t=0 convention artifacts. But the trigger-refusal and quadratic-candidacy counts restate published golds (fd48, e618, 384f) uncited. One measured experiment from gold.

## Reproduction

`git apply work/patch.diff`, built with the dossier's exact command (`CARGO_TARGET_DIR=/home/glmlab/lab-target-2`, offline). `invert trigger`, `invert econ`, `invert base|e003|e010|e030|slope|cross`: **every substantive number bit-identical** to evidence.log and the dossier table — trigger p50/p90/max 4.16/10.30/24.09 at σ_e=0.001, ΔU 0.041/0.171; econ frac_of_nc2 1.0000 at all four σ_e with kinds 1732/1910/213; base ranks dist 229/229 (max 4), λ_true 227/229 (2, 5), λ_mean 47/229 (30, 55); e003 15/210 (93, 152); e010 0/166 (157, 196); e030 0/50 (171, 193); slope 1/852 (715, 798) with λ_true 833/852 (max 8); cross fx 1,994 cone pairs, 308 truth encounters, 0 fx, ranks 57/308 (39, 75); method missed=0/extra=0 on all method-on scenes; brute disputes 5/0/1/0/1/1, outside_cone=0 everywhere. Only timings differ (machine quieter: `cross` 8.5 s vs ≈3 min). File times: predictions.md 00:48 < evidence.log 01:03 — pre-registration real; P5's failed candidate clause is reported as failed. Honest.

## Attacks (mine)

1. **Seed stability** (fresh seeds 30, 31, base params): λ_mean le4 58/226 (p90 39, max 65) and 35/229 (44, 74) — the 79% failure is not a seed artifact. λ_true also exceeds 4 on 4/229 at seed 31.
2. **Trigger firing edge** (σ_e = 1e-4, 3e-4, nc=400): binet3/eps p50 0.42 → 1.25 — the train's firing domain is σ_e ≲ 1e-4, 5–10× tighter than the gold's own validation σ_e = 0.001. Inside it (σ_e=1e-4, bunched), λ_mean holds 188/204 ≤ 4 (max 9) — the certificate regime is internally coherent, just mis-scoped: the desert between "trigger fires" and "pairwise affordable" is real, and the gold's own fleet sits in it.
3. **Jam** (σ_λ=0.002, 5× tighter than the gold's tightest): dist-rank max **11**, 44/993 > 4 — even the distance-rank guard dies at occupancy, confirming the dossier's recommendation that k be derived, never fixed. λ_mean p90 128 there.

All three sharpen the run; none breaks it.

## Novelty (the discount)

This is the ~8th inversion of the same gold, and the dossier cites none of the sisters:
- **fd48 (gold, 6 Oct)** already measured the trigger refusing the motivating fleet (ratio ~47) and "as specified it never fires there". This run's count 2 adds only the ΔU decomposition (real, useful) and the nc=400 distribution.
- **e618 (gold, 7 Oct)** already measured the true-λ rank nc-cliff and occupancy law (k from nc·2ρ/λ-spread — this run's slope row and 10⁶ arithmetic restate it; e618's checker had already spot-measured mean-λ rank p50 223), and **384f** already measured candidates = C(N,2) under orbit-path intersection. The "candidate fraction 1.000" fact is also in the gold itself (79,800 = nc²/2).
- **7532 (silver)** measured mean-λ rank vs σ_e (60–88% misses at 0.02–0.05, unbunched) but its checker downgraded it as "the axis the gold rejected"; **0a7a (gold)** measured true-λ train churn (46/body/orbit at the gold's regime) and **f0be (gold)** measured rebuild-on-overtakes Θ(n²) — the cost this run's adoption point (1) leans on but leaves "argued, not measured".

What is genuinely new and survives: (a) mean-λ rank fails **on the gold's own bunched validation fleet at its own σ_e and nc** — the last reading under which the adopted sort could have been sound; it closes 7532's checker's objection with a measurement (the gold's deployment text says "sort by longitude"; its evidence was distance-rank); (b) the gold's 4/233 window-tier misses are t=0 initial-coincidence artifacts — the disputed pairs' brute distances (1.6e-5…8.6e-5 at t=0.0000) match the gold's "missed" d_min list pair-for-pair, so the gold's headline soundness bug was its adjudication convention, not the window tier — a phantom work item deleted before the build; (c) the ΔU decomposition; (d) the zero-yield seam constant.

## Goal fit

Direct: the top scaling risk (candidate work must track real encounters) and the queued co-orbital certificate build (GLM queue and Codex queue-sol; the 6 Oct build attempt died on rate limit, so this lands pre-build). "A fix signals the wrong representation" (#19); the guard was "a control that could not fail" in the README's sense. Adoption is spec text, nothing on main.

## The one experiment for gold

Measure, not argue, the surviving package's cost inside the desert it names: true-λ sort + occupancy-sized k + ΔU trigger, on the gold's own scene and one desert scene at nc ≥ 3200 — rebuild/churn per orbit (0a7a's rates suggest it is large) vs the quadratic tier's per-orbit setup. If the package holds O(n·k̄)/orbit there, it replaces the demolished design (gold); if not, the desert itself is the finding and the encounters design needs a different representation (2D order, arrival-time ranking per 384f). Either outcome is adoptable in one step; cite and adjudicate the sister runs alongside.

## What the author missed

- The sister inversions: six prior runs (f0be, fd48, 7532, 0a7a, e618, 384f, 7655) had already killed this certificate from the churn, trigger, e-spread, occupancy and topology axes, three of them gold; the dossier presents counts 2–3 as new. The lab's value depends on runs citing what is already known.
- "Same scene and seed" for the 4/233 non-reproduction is nearly exact (RNG draw order and rayleigh match the gold's generator; only the e-cap differs above 0.004, P≈3e-4/body) — the author could have stated this match and made the correction airtight by identifying the four disputed pairs as the gold's four misses, which the distances already show.
- The trigger-violation headline "10–25×" is p90–max; p50 is 4× (numbers printed, phrasing loose).
- `ranks_fx` is empty in every scene (0 fx encounters), so P5's held-out λ_true-rank clause for crossers was unmeasurable — correctly reported, but a geometry with actual fleet×striker encounters would be the honest next seam case.

### 20261008-0338-inversion-4c98
Grade: silver

**Abstract.** Claim: the co-orbital gold's "every real encounter within partner rank 4" certificates co-rotation, not concentration, and cannot see different-n partners. Reproduced bit-identically on all 8 runs: fleet-scope misses 100% of cross encounters, global-scope 7.4–21.7% at k=4, required rank p99 = Δn·Δt_refresh·N/(2π), linear in cadence (33.6→3.0 at 8→64 refreshes/orbit). Gain: confines the in-flight co-orbital build before freeze — trigger on that number, phase tier Δn-scoped, cross encounters on orbit-pair geometry. Cost: one spec constraint, no code. Not gold: two held-out predictions failed (P3 11.0 vs >20; P6 3.0 vs >8 — "no practical cadence" is false, a 64× sort-cost trade), and this check falsifies the dossier's own "survives inside any lone formation": an e-spread formation (Δn≈0) misses 9–10% at k=4.

**Reasons.**

1. **Reproduction: exact.** All 8 JSONs regenerate bit-identically except `wall_s` (`fleet`, `loose-fleet`, `fleet+crossers`, `fleet+belt` × seeds 1,2; each 2–15 s). Per-population split regenerated from `probe.py` (the cited run log is empty): fleet+belt fleet-fleet 255/271 encounters, 0 misses; belt×belt 134/159, miss 0.127/0.145; cross 512/533, miss 0.078/0.069. Cadence table exact: 33.6→11.0→6.1→3.0 (crossers), 20.7→8.0→4.0→2.0 (belt), ratios 0.33/0.56/0.49.
2. **Predictions.** Pre-registered 03:45, decisive data 03:54 ✓. P1 ✓ (0 misses), P2 ✓ (1.000 ≥ 0.95), P4 ✓ (0.074 > 0.05), P5 ✓ (1.2 ≤ 4). P3 failed in magnitude (11.0, not >20; kill direction intact, k=4 misses 21.7%). P6 half failed: ratios in band, but p99@64 = 3.0, not >8 — one practical cadence does close the crossers' tail, by multiplying the O(n·k) sort 64×. Both failures are reported honestly in the dossier, but two held-out misses bar gold by the letter and the precedent (1 Oct law red-team: one failure → silver).
3. **Adversarial cases (mine).** (a) *Eccentric lone formation* — 800 ships, same a (Δn≈0), e∈[0,0.3], random w: E≈390, miss@k4 = 0.100/0.092, p99 ≈ 10–11. The dossier's "survives inside any lone formation" is false: intra-orbit longitude-rate spread (~2e·n) breaks k=4 with Δn = 0, so the trigger must gate on differential longitude rate, not Δn alone. e≤0.05 stays clean (0 misses). (b) *Same-orbit train* (identical a, e, w; phase spread) at e = 0.1 and 0.3: 0 misses, max rank 2 — the gold's literal domain ("a fleet on one orbit") holds even eccentric. (c) *Truth completeness*: dense 16,001-sample rescan of all fleet+crossers cross pairs — no pair with a second sub-ρ minimum, no discarded pair dipping below ρ. The instrument is sound.
4. **Novelty.** No H entry covers this (history ends H0215; the gold lives in board.md's taste log, 6 Oct). New measured content: the mixed-scene miss rates, the Δn·Δt·N/2π law with its linear cadence coupling, and the fleet-scope structural blindness. Partial overlap: the gold's own trigger sentence already scoped to "concentrated workloads", and the encounters path already keeps the Binet cone for non-formations (board focus list) — so the 320,000 body-pairs-for-522-encounters number attacks a cross tier no design proposes; the author discloses this (what-would-make-it-wrong 3). The kill lands on the board's universal sentence and on any build that takes it literally.
5. **Goal fit.** Board's top scaling risk: candidate work must track real encounters. A frozen k=4 tier would silently drop 8–22% of mixed-scene cross encounters or pay 64× sorts at the 10⁶ scale. PRINCIPLES 19: "a fix signals the wrong representation" — raising k or cadence is the bandaid; the orbit-pair cross tier is the water. Adoption: one constraint on the spec being written now.
6. **Reporting nits.** The caption says medians, but the split rows and 0.078/625 quote seed 1 (medians: cross miss 0.074, E = 522.5 → 613 pairs/encounter, not 625). `analyze.py` crashes on the fleet-scope/cross row (all ranks unreachable → None median); numbers recoverable from the JSONs. The dossier cites "the snippet in the run log" but `run.log` is 0 bytes — regenerable from `probe.py`, verified.

**The one experiment for gold.** Fold eccentricity into the certificate's law: rerun the ladder with e-spread formations (this check already has the first datapoint: 9–10% miss at e≤0.3, Δn=0), pre-register the corrected domain — phase rank certifies shared-orbit or near-circular co-rotation, with required rank set by differential longitude rate (Δn plus the ~2e·n intra-orbit term) × Δt_refresh × N/2π — and quote medians throughout. One author pass; the harness exists.

**What the author missed.** The eccentric case they themselves flagged, and its correct diagnosis: not "rank in true anomaly instead of longitude" (true-anomaly rate spreads the same way; the coordinate is not the issue — the rate spread is). The strawman risk in the work accounting (body-pair cross setup vs the design's Binet orbit-pairs). That P6's failure clause changes a structural impossibility into a cost decision the build must now make explicitly, with the sort-cost number attached. Seed-consistent quoting.

### 20261008-1058-inversion-6534
Grade: silver

**Abstract.** Claim: two concentrated crossing lanes force tier 2's full n_A·n_B product while every per-encounter metric calls the scene healthy. Reproduced bit-identically (`work/crossing/run.sh`, clean tree, empty patch): zero-miss 124/124; hits 189→49 574 (exponent 2.016), evals exponent 2.003, 0.5 evals/pair, ~0.8–1.2 µs/pair (4-thread wall); cone and radial both return exactly m² pairs; corridor d_max 0.029–0.030 rad, 0 beyond 0.15, m-independent (my m=2000 rerun: 0.0323, still 0 beyond); belt contrast 14 951 vs 39 evals/hit. My attacks: zero-miss holds on fresh seeds (129/129), near-tangent (304/304) and steep (100/100) scenes; cone = m² there too. Gain: identifies the last O(N²) block (board's top scaling risk) and the metric blind spot. Cost to adopt: one routing clause plus a crossing-time-rank window, not built here. Two record flaws (below) hold it at silver.

**Reasons.**

1. **Reproduction: exact.** Every deterministic number regenerates (counts, evals, exponents, quantiles); only wall times drift on the shared runner, as disclosed. The exponents re-fit to 2.016/2.003 from the raw lines. The gold's regime reproduces flat (394.0/394.4/395.9 setup evals/pair within-lane).
2. **Predictions.** `predictions.md` (11:07) predates the outputs (11:14) and the log order is consistent. Predictions 1, 2, 4, 5, 6, 7 held; 3 failed and is honestly reported as strengthening the claim. Kill criteria were pre-written; none fired.
3. **Adversarial cases (mine).** (a) Fresh seeds: 129/129 matched, 0 missed/false/dup — soundness is not a seed artifact. (b) Steep incidence (e=0.35, γ≈19.8°): zero-miss, all-Cross sections, 0.5 evals/pair, cone still exactly m² — the product structure is incidence-independent. (c) Near-tangent (γ≈0.6°): zero-miss 304/304, but all sections go Wide, 518.6 evals/pair (72× per pair, 15 497 evals/hit — 1000× per encounter), and the corridor bound breaks (d_max 0.249, 292/8363 beyond 0.15). The author's disclosed failure mode is real and far larger than the run implies.
4. **Novelty.** No crossing-lane measurement exists on the adopted stack (board through 6 Oct, HISTORY.md, `git log`); q-candidate-degree answered dilution at fixed density, taleb-09b5 answered same-orbit concentration. Ancestor: H0156 (25 Sept) found all-pairs search under relative motion in the pre-pivot population sweep — same symptom, different machine; new here are the routing gap between two adopted certificates, the metric inversion, and the corridor invariant.
5. **Goal fit.** Top board bottleneck (q-candidate-degree, the O(N²) scaling risk). It shows a premise wrong: "work per real encounter constant ⇒ healthy" is blind to absolute cost under concentration. PRINCIPLES §10: "We need also to map how things break, think in extremes"; §3 "Compute only surprises".

**Why silver, not gold.** Two dossier numbers its own log contradicts, and the exit is unbuilt:

- The extrapolation divides by 4 twice: 0.79 µs/pair is already 4-thread wall, so 10¹⁰ pairs ≈ 2.2 h (not 30 min) and 10¹² ≈ 9 days (not 2 days). The conclusion (unpayable, and unpayable even at 1 ns/pair) survives — the error understates the cost — but the printed headline is wrong.
- The corridor mechanism is misattributed: my steep control (ρ/sin γ = 0.0030, 4× smaller than the original's 0.0127) leaves d50 unchanged (0.0106 vs 0.0104). The width is set by the lane's crossing-longitude dispersion (ϖ spread ±0.02 rad) until γ gets small (tangent: d50 ≈ ρ/sin γ indeed). "d50 ≈ ρ/sin γ" was scene-coincidence numerology; window sizing and the near-tangent trigger both depend on getting this right.

**The one experiment to gold.** Build the exit on the frozen scene: sort each lane's crossing times per crossing longitude, sliding-window merge with half-width from the measured corridor (dispersion ∨ ρ/sin γ) + margin; verify zero-miss vs truth at m ≥ 500 and measure work per real encounter (the selectivity side of O((n_A+n_B)·log n)). That converts the corridor from a necessary condition (recall, measured here over 15 391 encounters) into the claimed mechanism, and re-does the two flawed numbers.

**What the author missed.**

- The two record errors above; both are in adoptable text, not just prose.
- The measured scene is the benign end of the crossing family: near-tangency costs 72× more per pair and 1000× per encounter (measured by this check), so the product block's constant varies by ~100× across incidence — the routing trigger needs γ, not just "cones intersect".
- Zero-miss vs truth only at m=100; the corridor at m ≥ 500 is measured over method events, sound by extension of the control, not directly.
- Within-lane blocks were never truth-checked (minor; the claim's focus is A×B).
- H0156 should have been cited as the ancestor of the symptom.

### 20261008-1150-system-cf13
Grade: silver

**Abstract.** Claim: the encounter finder needs one certificate — in-band phase-rank + cross-band cone, band width from the drift bound, no trigger. I reproduced every number in the run folder bit-identically (all 16 lines: pairs/evals/checks/hits/missed; F1 59.7× evals, 0 missed; BANDS=1 self-destruction margin 712; k-boundary 12→4→0). But one adversarial scene inside the claimed regime breaks it: a convoy (F1's exact a/e, longitudes clustered in 0.1 rad — a fleet on one orbit, the taleb-09b5 motivating case) silently misses 11,736 of 15,497 truth encounters (76%) while the crate's cone misses 0. The rank-count k derives from mean spacing TAU/m and assumes uniform longitude density; clustered populations (convoys, Trojan clouds) violate it by orders of magnitude. Adoptable after the scale is fixed: one named experiment away.

## Reproduction (clean tree, `work/patch.diff` is empty — exp is self-contained)

- Built `exp` with `CARGO_TARGET_DIR=/home/glmlab/lab-target-1`, ran F1/F2/X/B. All counters (pairs, scanned, evals, checks, hits, sections, missed, false, matched) match `f1/f2/x/b.jsonl` exactly; only ms differ (shared machine). Cone misses 0 on all scenes; unified misses 0 on all four declared scenes.
- `BANDS=1 F2` = 4,957 pairs / 439,206 evals / 0 missed — the dossier's "maximal band" row is regenerable (identical to `globalrank`, as one-band-over-everything must be). `BANDS=1 B` = margin 712, self-destructs to all 499,500 in-band pairs, 0 missed, ~3.3 s — the "tier chosen by the drift bound, not a trigger" claim reproduces.
- `K_OVERRIDE=0/1/2` on F1: 98/12/4 missed; adaptive k=4: 0. The boundary is real. (Dossier's "k=1/k=2" labels are the override values; actual rank width is override+1.)
- Truth independence confirmed in `crates/encounters/src/truth.rs`: conservative advancement with Lipschitz/Gronwall step bounds, Halley states vs the method's Newton — no shared solver.

## Predictions

`predictions.md` predates the run (file times and log order consistent). P1–P4, P6 held as reported; P5 honestly falsified in direction (no-band swells in cost rather than missing) — the correction is real, I reproduced the swelling on B (499,500 pairs) and its absence on F2. **Hygiene flaw:** the declared scenes were resized before the run without disclosure — predictions say F1 N=800 σ_e=3e-4, F2 N=1000, X 2×400; the code runs 500/600/2×250, σ_e=1e-3. The direction does not favor the headline (smaller N shrinks the quadratic win; larger σ_e is harder), so this is not tuning, but a pre-registered protocol that silently drifted.

## Attack (my three cases)

1. **CONVOY** (N=500, a∈[1,1+3e-5], e Rayleigh 1e-3, M0 and ω both uniform in [0,0.1], ρ=1e-4, 30 orbits — F1 with clustered phase): truth 15,497 encounters; cone misses 0; **band/globalrank miss 11,736 (76%), with 0 false positives — silent**. Cause: `k_enc = ceil(2.5·2·e_hi/spacing)` uses mean spacing `TAU/m`; the encounter window |Δλ| ≲ 2(e_i+e_j) spans ranks proportional to *local* density, ~63× finer in a convoy. This is inside the claimed regime ("exact on formations, co-orbital swarms"): a convoy is a formation, and real co-orbital populations (Trojan clouds) are clustered and stay clustered.
2. **F1HOT** (σ_e=3e-2): 0 missed, still ~5× cheaper — the eccentric degradation behaves exactly as the author disclosed.
3. **TROJAN** (a-spread 1e-6, uniform longitudes, ρ=3e-4): 0 missed, 38× evals cut — the degenerate-regime win is real where phase is spread.

## Novelty and goal fit

Not in HISTORY.md or docs: taleb-09b5 (board, 6 Oct) established the O(n·k) phase tier with a dimensionless trigger; this run's contributions — the tier as the in-band readout of the crate's own cone, the band width from the certificate horizon, the trigger deleted in favour of the drift bound's self-destruction (measured on B), and the P1 correction that the *crate* misses 0 on formations — are new and measured on the crate's unchanged `pair_events`. It targets the board's top scaling risk (candidate work must track real encounters; components-4643's 92% setup dominance). Fit: PRINCIPLES 19 ("a fix signals the wrong representation") and 32 are served by the unification; but PRINCIPLES 2/"exact means deterministic and reproducible" and r8's frozen contract ("every candidate finds every encounter") are violated by the convoy case as shipped.

## The one experiment to gold

Replace the rank-count scale with a sound one — an **angular** window (|Δλ| ≤ c·2·e_hi + drift margin, materialized by range search over the sorted longitudes, cost = window × local density; equivalently bound k by max local spacing) — then re-run all four scenes plus CONVOY and a clustered Trojan cloud (0 missed required), and judge under kicks with r8 v4's case (d) as the author already proposes. The unification's shape, the drift-bound tier selection and the cost numbers all survive; only the in-band scale is wrong.

## What the author missed

- Phase clustering. All four samplers draw mean longitude uniform over TAU; the derivation then quietly assumes it. The lens section lists eccentric swarms, kicks, resonance, GR — everything except the density of the phase distribution itself, in the regime (formations) the certificate exists for. The miss is silent (0 false positives), the worst failure mode for a candidate tier.
- The undisclosed scene resizing between predictions.md and the run.
- Small gaps: the negative control's "k=138 of 500" (X) is not regenerable from the shipped binary (globalrank prints no k/margin); hits exceed matched by 1/7 on F2/X (duplicate conjunction events) — benign but unexplained.

### 20261008-1337-inversion-c5ab
Grade: gold

**Abstract.** The gold's phase-neighbour certificate (rank 4 along the orbit) silently assumes zero element dispersion. Reproduced bit-identically: the required rank grows as ~n·σe (k99 ≈ 0.7–1.0·n·σe aligned; uniform in n under apsidal spread), miss@k4 = 0.37–1.00 at σe = 10⁻²–3×10⁻² (n = 1600), and one δe = 10⁻² kick puts 100% of the kicked ship's real encounters outside rank 4 (author's and my fresh seeds). My attacks — new seeds, ρ ∈ {3×10⁻⁵, 10⁻⁴, 10⁻³}, n = 3200, a tuned e-absorbing key — all confirm; no key rescues rank 4. Gain: the queued b-coorbital-cert does not ship a silently-missing tier. Cost: one factor in the trigger (n·σe ≲ 3–6) plus a kick fallback.

**Reasons.**

1. **Reproduction.** Forced rebuild (`touch src/main.rs` + `cargo build --release`), reran all 17 scenes: log identical to `decisive-run.log` modulo wall times. `debug_gap_model.py` (25 s) validates ΔM* = 2Δe per encountering pair (ratios 0.896–1.037, <1% typical) and its model p99 rank (11.1) matches the Rust k99 (11). `debug_kick.py` (2 s) independently shows dmin ≈ |ΔM₀ − 2δe| (e.g. gap 0.00373 → dmin 3.728×10⁻³): the relative speed never closes the crossing offset, so encounters sit exactly at phase rank 2δe·n/2π.
2. **Predictions.** mtime order is debug_kick (13:47:57) → main.rs (13:49:31) → predictions.md (13:50:04) → decisive-run.log (13:50:14); debug_gap_model.py after the run, presented as a cross-check, not a prediction. Held: E/F mean-anomaly uniform ranks (predicted k99 ≈ 790; measured 786–790), kick ranks (predicted 10.2/30.5; measured 9–12/29–72), control and B exact, encounter counts (~81 predicted; 46–105 across seeds). Missed: C/D miss fractions and k99 by ~2×, cause identified (Rayleigh-difference tail overestimates P(Δe > x) by 2×) and disclosed — the geometry law itself is validated, so the misses are calibration, not tuning.
3. **My attacks.** (a) Fresh seeds 203–205 (C): miss 0.371/0.494/0.471, k99 12–15; fresh E seeds: miss 1.000, k99 ≈ 780. No seed luck. (b) ρ = 10⁻³: C miss 0.418–0.434 over 801–832 encounters, E 0.993–0.999; ρ = 3×10⁻⁵: C 0.317–0.520. Not a ρ artifact — the rank is set by ΔM* = 2Δe, not by the window width. (c) Fresh n = 3200 point: k99 = 31 (mean keys), miss 0.659 — the linear law in n at fixed σe holds. (d) A 4th key K = M − 2e, absorbing the aligned-apsides crossing offset exactly: miss 0.33–0.40 on C (no rescue; k99 2× worse — the rescued far branch is offset by the newly-missed near branch), identical to mean-anomaly on E. The miss is geometry (orbit crossings offset by the equation of center), not key choice. (e) Kick δe = 10⁻² at fresh seeds: 6/6 encounters missed under mean-anomaly/mean-longitude.
4. **Novelty.** docs/HISTORY.md ends at H0215 (6 October); the rank-4 premise exists only in the board's taste log for gold 20261006-0346-taleb-09b5 ("every real encounter lies within partner rank 4 along the orbit... triggered by a dimensionless number"). No prior run measures its dispersion domain; the ΔM* = 2Δe law and the safe-domain bound n·σe ≲ 3–6 are new numbers. `b-coorbital-cert` is confirmed queued (lab/queue.txt), so this lands before the build.
5. **Goal fit.** It shows a gold's premise is wrong outside the scenes it was measured on, with the quantitative domain — the gold route ("shows that a premise is wrong"). It follows H0183 (a failed expectation is not a failed method: the certificate is not killed, its domain is measured) and PRINCIPLES #4 ("regimes are chosen by dimensionless numbers" — the number must include dispersion). Adoption is one step: gate the phase tier on n·σe, re-derive or fall back on any kick.
6. **Soundness.** The truth is the crate's own conservative-advancement oracle (r8 lineage); pair-level membership, which is all the miss analysis uses, is unaffected by the control's terrace minima (disclosed; dispersed scenes show isolated dips). The churn metric removes rigid rotation via body 0 (rank differences are invariant to the reference's own equation-of-center wobble); 256 samples per orbit cannot alias a once-per-period monotone oscillation. Mean-anomaly and mean-longitude ranks are time-invariant at equal periods, so the epoch choice cannot game them. Memory stayed well under budget (peak ~0.5 GB, the Python sampler).

**What the author missed.**

- The static mean-anomaly order has *zero* churn at equal periods; the full statement is a tradeoff — under dispersion no key is both static (free sort) and encounter-tracking (true longitude tracks but churns ~n²σe). The churn cost also returns for any real fleet with tiny δa (shear), which the exact-equal-period scenes exclude by construction.
- The gold's actual trigger number could not be read here (the gold's dossier lives on its own branch); "concentration alone" is inferred from the taste log. The kick result covers the charitable reading (any trigger must know dispersion, since a δe = 10⁻² kick exits rank 4 instantly under every key), but the queued build's current spec was not verified against it.
- The H scenes carry 1–7 encounters per seed; the "100%" rests on 10 total encounters (author's 4, mine 6) plus the exact mechanism. The formation scenes carry the statistics (58–105 encounters; 800+ at ρ = 10⁻³ in my runs).
- Unmeasured, disclosed: the fallback's cost on concentrated workloads (the gold's 135×/40 TB number) and a lazy, exchange-time-ordered re-sort.

**Process note.** One edit aimed at my /tmp scratch copy touched the run folder's `src/main.rs` by path alias; restored byte-exactly from verbatim reads (verified: cargo no-op rebuild, and the rerun reproduces `decisive-run.log` bit-identically). Nothing else in the run folder changed; no git commands were run.

### 20261008-1947-taleb-1b5d
Grade: gold

**Abstract.** Claim: the adopted phase-neighbour certificate (gold 20261006-0346) silently drops 95–100% of encounters on equally a-concentrated lawful states with scattered apsides, and 100% of inter-formation battle encounters; rebuilds cannot fix it. All dossier commands reproduced bit-exactly (e=0.6: miss@4 96.3%, ranks p50 147; battle rank ≈ N/2; mechanism rank = N·|Δλ*|/π, correlation 0.994–0.998). My attacks strengthened it: e=0.1 scattered already misses 94%; N=512 doubles ranks (p50 300); aligned-apsides e=0.6 stays clean (0%), isolating Δϖ as the trigger variable. Adoption: one closed-form Δλ*(e,Δϖ) gate, synodic-drift expiry, per-phase-cluster certificates — before crates/encounters builds. It blocks the B13 silent-loss ruin class inside the tier replacing the quadratic one.

## Reproduction

Ran the dossier's four commands in a scratch copy (`/tmp/check1`, originals untouched; `work/patch.diff` is empty so nothing to apply). Every headline number matches the stored JSONs exactly:

- `A_gold_T4_s1`: miss@4 35.12% → 0.0% with P/4 rebuilds, max rank 13→4; controls PASS both ways.
- `B_e06_s1`: miss@4 96.3%, p50 147, max 202, rebuild identical to the digit.
- `D_battle_s1`: inter-cluster miss@4 100%, max rank 129 ≈ N/2; intra-cluster remainder at rank ≤ 4.
- `geo.py`: correlations 0.9941 / 0.9977 / 0.9978; Δλ* p50 1.784 / 2.594 / 1.556.

Truth instrument: v_cap = 2·v_max(a,e) makes the KD-tree dilation `ρ + v_cap·dt` a genuine bound on missed minima; every trough refined by ternary search. My own resolution control (B_e06_s1 at 16384 vs 32768 slices/period): identical 27-pair sets, empty symmetric difference, dmin agree to 2.2×10⁻¹⁵. Positive/negative controls pass. The truth is converged; this is not an instrument artifact.

Mechanism verified independently of the code: at a crossing longitude the mean-longitude offset is Δλ* ≈ |Δ(M−f)| + |Δϖ|; for the two-ϖ-cluster battle at e=0.4 that gives 4e ≈ 1.6 rad (measured p50 1.556), rank = N·Δλ*/π = 256·1.556/π ≈ 127 (measured 121–129). The dossier's formula is exact, not fitted.

## Predictions

`predictions.md` mtime precedes every decisive result file (smoke.json, a calibration run, is the only older artifact — allowed). P1 held (0.4% / 35.1–36.2% / 49.8% against predicted ≈0 / 5–40% / ≥50%; rebuild residue 0.33%), P2 held (95–100%, rank halving 202→99, rebuild identical), P3 held (100% inter-cluster, all seeds), P4 held by construction. The author's own kill criteria did not trigger. One flag: `probe.py`'s mtime postdates `results_A.json` — an edit after some results — but the current code regenerates every stored number exactly, which I verified, so the record is regenerable (the usual silver failure is the opposite).

## Attacks (my own cases)

1. **e=0.1, ϖ uniform, N=256**: miss@4 = 93.9%, p50 rank 18, rebuild no help. The failure domain is *wider* than tested — asteroid-typical eccentricities already break rank-4. (miss@16 = 60.6%, so even k=16 is not safe there.)
2. **e=0.6, ϖ aligned, N=256**: miss@4 = 0%, max rank 3, 25 encounters. Eccentricity alone is harmless with aligned apsides — the domain boundary is apsidal spread, not e. This slightly narrows the claim ("aligned-apsides, near-circular" → apsidal alignment suffices) and confirms the proposed Δλ*(e, Δϖ) gate reads exactly the right variables.
3. **e=0.6, N=512**: miss@4 98.9%, p50 rank 300 vs 147 at N=256 (2.04×), 89 encounters. Linear-in-N confirmed with a thick sample, where the author's N=128 cases were thin (3–4 encounters). Fixed k is quadratic in disguise, as claimed.

## Novelty

No HISTORY entry bounds the certificate's domain: the gold lives in the board's 6 October taste log as regime-free ("every real encounter lies within partner rank 4… triggered by a dimensionless number"), and H0214 records only the symptom class (B13, 7 of 64 flybys lost). The conjunction-displacement trigger, the synodic-drift expiry, and the refutation of "paid once per element change" are new.

## Goal fit

Board's top scaling risk: candidate work must track real encounters. This shows the adopted O(n·k) certificate silently loses encounters exactly where its trigger fires hardest (P4), i.e. a premise of an adopted gold is wrong, and the correction is a gate, not a component. PRINCIPLES: "a failed expectation is not automatically a failed method" — the run kills no method, it sizes the trigger; findings are rank counts and miss fractions ("Floats may explore; only integers decide"); cheapest falsifying test first. The miss class is the ruin class the board already paid for at B13: silent, not slow.

## Weaknesses (none gold-blocking)

- `ranks_of_pairs` counts the body itself (separation 0), so every quoted rank is +1: "rank 4" tests true rank ≥ 4. Boundary statistics slightly overstate misses; p50 ranks 18–300 and miss@16 90–96% are untouched, and in the aligned cases rebuilds zero everything anyway.
- `geo.py`'s `pred_rank = N·Δλ*/(2π)` is half the dossier's (correct) `N·Δλ*/π` — visible as pred 72.7 vs measured 149; only scale-invariant correlations are quoted from it, and the dossier's own formula checks out against measurement exactly.
- Truth is pure Kepler: no librating co-orbitals (Trojans/horseshoes), which need an integrator; mutual gravity only adds scatter, so this weakens, not strengthens, the certificate.
- The Δλ* gate's per-certificate cost is unmeasured (author discloses; it is one closed-form Kepler evaluation per certificate).

## What the author missed

- Failure begins near e ≈ 0.1, not 0.3: real belts sit mostly in the broken regime, so the Binet-cone fallback will carry most belt work — the certificate's true domain is the aligned-formation niche only.
- Aligned-apsides eccentric formations are safe (0% miss at e=0.6): the domain is set by Δϖ spread, not eccentricity — good news for the proposed trigger, since Δλ*(e, Δϖ) already encodes it.
- The +1 rank inflation and the geo.py half-scale prediction noted above.

### 20261008-2206-taleb-f965
Grade: silver

# Check — 20261008-2206-taleb-f965

## Abstract for the integrator

**Abstract.** Every number reproduces bit-for-bit (35/35 JSON lines and the 80-line miss dump identical; binary 94 s, exit 0, after `git apply work/patch.diff` on a clean tree). The three kills stand and my attacks extend them: global phase-rank drops 34–87% (not the claimed 66–94%) on mixed scenes; static rank-4 misses 6–8% in pure fleets and the one-orbit refresh cadence holds even at 10× a-spread (my A1: 0 missed); the family gate's hole is broader than "wedge storms" — my tight cold belt (a ∈ [0.995,1.005], σ_e = 3e-3) misses 3/130, and the gate costs 6–40× the cone's evals on every belt-like scene. Adopt the three restrictions on `b-coorbital-cert`; do not adopt the "70× fewer evals" repair claim (measured 1.4×: gate 15.9 M vs cone 22.8 M on S1).

## Reproduction

- Clean tree at a838a28; `git apply work/patch.diff`; `cargo build --release --offline -p emergent-encounters --bin coorb` (4.3 s); run → 94 s, exit 0.
- All 35 lines of my `/tmp/check-out.jsonl` match `work/coorb-final.jsonl` field-for-field except `ms`; the stderr miss dump matches `work/coorb-miss-final.txt` line-for-line (80 MISS lines).
- Tuning path auditable: `coorb-out.jsonl` (22:17) shows the gate as first built (static rank) missing 12 on S1 and 8 on S1b — P1's failure as written; `coorb-out3.jsonl` (22:23) has the cadence repair with 0 missed. `predictions.md` mtime 22:12:55 precedes every output file. Held-out seeds (s+104…109) never appear before `coorb-out2.jsonl`.
- Truth independence: `truth_pair` (Halley, conservative advancement with a proven lower bound) vs the methods' Newton path — as in r8. The matchup's `dup` counter is computed but never reported, which is why cone's 56 "false" on S1b are hard to interpret from the JSON alone; the author's disclosure covers the direction that matters (miss counts, not false counts).

## Held-out predictions

- P2 held (S2: 78/90 = 87% missed). P3 held (90 623 and 44 850 candidates). P6 held. P1 failed as first written, repaired with the cadence and disclosed — the repair was tuned on S1/S1b, but S6–S8 (fresh seeds) then passed, so the held-out check is real.
- P4 failed on the held-out wedges (21/242, 41/252) — reported honestly. This alone blocks gold under the rubric ("reproduced, and the held-out predictions held").
- P5 is overstated: "≤ ~10², measured 1.5×10²" quotes only S3/S6 (150, 152). On S2/S8 hits per encounter are 908 and 1172 — an order above the prediction. Point 4's cost honesty ("not yet cheaper there") discloses the evals, but "P5 held" as a sentence is not what the table says.

## My adversarial cases (all fresh seeds, my own scenes; outputs in /tmp, tree restored)

- **A1, pure fleet at 10× the a-spread (±5e-4, 50 orbits):** gate 0 missed (truth 82) — the cadence repair survives drift ~0.45 spacing/orbit; static rank misses 27/82. Supports restriction (b).
- **A2, wedge at ρ = 1e-5:** truth collapses to 25 encounters; gate misses 1 (4%) — the displaced-longitude pairs no longer encounter at all, so the wedge hole shrinks relatively as ρ tightens. But gate evals 12.05 M vs cone 2.07 M: the gate's cost grows as ρ shrinks (scan resolution), the opposite of the dossier's "slack factors shrink linearly with ρ, favouring the gate" parenthetical.
- **A3, eight small crossing fleets (benign mixed):** gate 0 missed, sound — but 42.2 M evals vs cone's 6.7 M (6.3×), with 61 536 gate hits against 51 040 cone candidates. rankk-glb misses 57/70 (81%) — the blind spot again.
- **A4, fleet × tight cold belt:** gate **misses 3/130** — the ε≫ρ hole is *not* wedge-specific; any family packing enough internal spread (here belt families at join radius 3e-3 against ρ = 1e-4) misplaces crossing longitudes. And the gate costs 620 M evals (178 s) vs the cone's 15.3 M (1.5 s): 40×.

## Novelty and fit

- No prior H entry red-teams the adopted gold 20261006-0346; this is the pre-freeze red-team the lab owes `b-coorbital-cert` before its gate ("zero misses against an independent truth on the gold run's scenes") freezes a reading that would pass on the gold's scenes and still drop a third of a mixed scene's encounters. Board fit: the top scaling risk ("candidate work must track real encounters"); PRINCIPLES 25 (a certificate that silently drops encounters is ruin), 13 (a miss is a compounding error type).
- Not gold: P4 failed held-out (author-acknowledged), plus the evidence errors below. One experiment away, and it is the author's own: member-extremal crossing arcs (or families clamped to ε≈ρ) closing the wedge/belt hole, then the 10⁶-fleet pair-count at game ρ.

## What the author missed

1. **"70× fewer than the cone's 22.8 M" is contradicted by the final data.** The cadenced gate costs 15.9 M evals on S1 (1.4× less than cone); 10.4 M vs 15.5 M on S1b (1.5×). 70× only matches the *static* rank's 0.325 M — the configuration that misses 12/193 and is dead. The cadenced certificate re-pays ~530 evals of section setup per pair per chunk; without amortized setup it is cone-cost, not 70× (the same re-pay lesson as components-4643).
2. **The headline "66–94%" is not the table.** Measured drop rates on mixed scenes: 87, 66, 39, 51, 34, 87%. The range appears to conflate S3's rate (66%) with S4's count (94).
3. The gate's failure scoping is too narrow (A4: tight belt, 3 missed) and its cost story on belt-like scenes is worse than reported (A4: 40×, A3: 6.3×).
4. `dump_missed` runs after both rankk-glb and gate, so the stderr dump interleaves the two methods' misses — attribution of a given miss to the gate requires the JSON, not the dump.
5. The `dup` counter is silently dropped from the report, leaving cone's 56 "false" on S1b ambiguous between double-dips and truth undercounting on near-identical pairs.

The miss-count table itself is fully regenerable and honest; the errors are in three sentences about it. Silver stands on the kills, the cadence repair (which held everywhere I stressed it), and the restrictions it hands the build.

### 20261008-2349-inversion-d1b0

### 20261009-0208-inversion-a937
Grade: gold

**Abstract.** Claim: the adopted phase-neighbour train certificate (gold 20261006-0346-taleb-09b5) is gated by a Binet-clump diameter that cannot see orientation or sense, so polar formations miss 98–100% of real encounters at any cadence and retrograde clashes force 2·n_p·n_r order changes per orbit. Reproduced bit-identically (13/13 rows, clean rerun of `train_probe.py --scene all`). Analytic truth independently brute-verified (75/75 true, 29/29 near-threshold false, max deviation 0.001·ρ); dense 201-sample sweeps confirm the watch set never contains the partner (min rank 13). Gain: deletes a silent 100%-miss hole in an adopted design before it ships. Cost: one guard in the trigger plus fallback to the existing cone tier. Adopt with the axis caveat below.

**Reproduction.** Clean tree, `python3 train_probe.py --scene all --json metrics-check.json`: bit-identical to the author's `metrics.json` (13 rows, all scenes and adjudications). `work/patch.diff` is empty (no tree edits). Dossier numbers match `run.log` exactly; one transcription slip: polar overtakes min is 2,193,000, the dossier says 2,192,500.

**Predictions.** File times support pre-registration: `predictions.md` 02:34:25 < `run.log` 02:35:26 < `metrics.json` 02:38:59. Kill criteria were written before the decisive scenes and fired as pre-registered (polar miss ≥ 90%: measured 97.6–100%). Held: retro pair count and 500,000 overtakes (exact), budget-miss ≥ 90% (99.98%), polar rank ≥ 95% over k, dist-rank ≤ 4 at 100%, flip displacement ~n/2 (737 vs 750). Failed and disclosed with the right diagnosis: polar pair count (~3,000 predicted, 41–59 measured — equal periods make syncs permanent, so pairs are not multiplied by the horizon).

**My attacks (independent code, `/tmp/check-a937/`).**
1. *Truth.* My own dense sampling (step 2·10⁻⁵ over the full orbit, refined at 10⁻⁷): agrees with the analytic d_min on every checked pair, true and near-threshold-false, across polar and retro. The 3-sample dot-product identity is exact (I re-derived it: u·u′ = c₀ + A·cos 2t + ψ for same-|n| circulars).
2. *"Any cadence".* 201 samples across each polar contact window (not just the two flanks): min ring rank anywhere 13, all 50 pairs > k; no evaluation instant catches them. Rank exactly at t* reaches 721 (no atan2(0,0) artifact at the pole).
3. *Overtakes.* Direct simulation of ring order changes, polar n=200: 39,472/orbit ≈ 0.99·n², confirming the ~n² claim (author: 2.19M at n=1500). Retro 2·n_p·n_r is exact combinatorics (cross-pair Δλ sweeps 4π per orbit → 2 passes); my naive counter was contaminated by linear-argsort wrap artifacts, the formula stands.
4. *Boundary and the fix.* Sweep at n=800: node spread U(0,π) is safe (rank 1, zero misses) for every i ≤ 1.4 rad (80°); the break is sharp at i = π/2, where the position→longitude projection folds. Adversarial strengthening: at i = π/2 even a 0.02-rad orientation clump still misses 100% (median rank 105) — bunched at the fold, the ring crowds; and a same-node polar formation makes λ two-valued (degenerate key).
5. *The sort-key loophole.* "Sort by longitude" has three readings. Polar scene: inertial azimuth misses 100%, mean longitude L misses 100%, node-referenced phase u misses 0% (sync pairs are phase-tied). But a mixed-orientation swarm in one Binet clump: λ safe, L misses 100%, u misses 87.5%. No single scalar key is sound inside an orientation-mixed clump — the conclusion (the trigger must gate on orientation ∩ sense, cross-clump pairs to the cone tier) holds under every reading. The author's polar numbers correspond to two of the three.

**Novelty.** Nothing in this tree's docs/HISTORY.md, law.md or the board's record covers orientation or sense for the train; Binet space (U,V,W) = (1/p, e·cos ϖ/p, e·sin ϖ/p) mathematically contains neither (docs/law.md, encounters section). The gold's own record gates the train on one dimensionless number. B14's retrograde/polar entries are birth-classification gates, not certificate soundness.

**Goal fit.** Encounters bottleneck, the board's top scaling risk. This is the same class of hole that made the 6 October gold gold (the window tier's 4–6% silent drops), caught before the crate ships: "Certificates need independent, adversarial checks." Fit with PRINCIPLES: #19 "a fix signals the wrong representation" (longitude is degenerate water at the fold); #4 "regimes are chosen by dimensionless numbers" (the number must see orientation and sense). Adoptable in one step: the guard, with the cone tier as the existing fallback.

**What the author missed.**
- The proposed guard is incomplete at exactly the degeneracy it exposes: an orientation clump tighter than any tolerance still misses 100% at i = π/2 (my attack 4), and the same-node polar fleet makes the key itself degenerate. The trigger needs a third term — the sort axis bounded away from the fold (sin i relative to the ring's equator ≤ 1 − tol), or the key defined as phase in the clump's own plane — otherwise the guard ships a certificate that is sound for every tested scene except the polar one it was written for.
- The sort-key ambiguity was not tested; two of three readings break polar, the third rescues polar but breaks mixed orientation. The conclusion survives, the polar evidence alone does not decide it.
- The claim sentence's "retrograde clashes resurrect the quadratic tier" overstates what the footnote honestly says: the clash's true events are themselves quadratic (500,014/orbit at n=1000), so O(overtakes) ≈ O(events) maintenance tracks the optimum; the finding that stands is the trigger's sense-blindness and that no fixed O(n·k) cadence survives (99.98% between evaluations — a property the safe incl-node control shares at 94–97%, which the dossier's last paragraph correctly flags as the bigger open property).
- The retro overtake count is exact combinatorics hardcoded, not measured; fine, but "measured 500,000" is generous wording.
- The gold's adopted trigger text could not be re-read from this tree (its run folder is not published here); the integrator should confirm the trigger's exact form at adoption. Binet space's blindness to orientation makes the reading almost certainly right.

### 20261009-0521-inversion-b1c0

### 20261009-1210-inversion-c529
Grade: silver

**Abstract.** Reproduced bit-for-bit (control/heldout/audit identical; only wall-clock differs); independent Python audit confirms the E1 pair (d_min 1.8e-4, permanent far-rank partner, order frozen). Two of three legs survive adversarial attack and change the co-orbital brief before freeze: an equal-period random-ϖ clump (2ae/ρ=20, τ=1.00) breaks a longitude rank-4 watch at *any* refresh cadence — I measured rank at encounter time (the gold's "rebuild on overtakes"): 50% of events missed, rank* = 10, seed-robust — and mixed traffic (τ=0.938 vs 1.000) loses 97.4% of 542 cross encounters while the Binet cone covers 542/542 encounters and 6000/6000 cross pairs: per-pair ΔU classification, population trigger deleted. But the horizon leg is wrong as headlined: rebuild-on-overtakes needs only k = 4 at H = 500 (my measurement, zero misses); "needs rank 42" binds a t0-anchored watch only.

**Reasons.**

1. **Reproduction.** Applied `work/patch.diff` to a clean tree; `cargo build --release -p emergent-encounters --bin inversion` (6 s); `inversion control` (3.8 s), `heldout` (48 s), `audit` (1 s). Every physics number identical to the author's files (diff on parsed JSON: only `secs` differs — shared machine). `python3 work/audit_check.py` (23 s): min distance 1.836e-4 vs Rust's 1.779e-4 (0.5 %, explained by the dump's 4–6-digit element truncation, stated in the script), periodicity confirmed, 1.24 % of the horizon below ρ, λ-gap 2.42 spacings. The E1 mechanism is real and independent of the crate's truth code.
2. **Predictions.** `predictions.md` predates every result file in `work/` (mtimes 11 m vs 8/4/3 m; final regeneration ran audit→control→heldout). All pre-registered ranges held (P1: k*≥15→42, 20–80 %→50.3 %, swaps≈320→363; P2a: 560/35.7 %; E2 between; P3: 94.9 %/84.9 %, 549; silent/enc-swaps 826 ✓; P4: 97.4 %, 542/542, τ). The two soft misses (B2 k*=97 vs >100; M1 542 vs 10–200) are stated in the dossier. Textbook pre-registration.
3. **Attacks (mine, `attack.rs`, removed after).** (a) *The gold's specified certificate, not the probed one*: I pulled the gold from `8d339c5` — its spec is "sort by longitude, watch k≈4 neighbours, **rebuild on overtakes**". Mean-longitude order is piecewise-constant between overtakes, so rank evaluated at the encounter time equals the rebuild-on-overtakes watch. Result: H1 miss(k=4) = **0.0000** (rank* = 4) vs the dossier's 50.3 %; B1 86.9 % (domain edge, as claimed); M1 6.4 % of events, rank* = 120; **E1 50.0 % of events, 14/28 pairs, rank* = 10** — the frozen-order kill survives perfect refresh. (b) *Seeds*: E1-seed13 → 43.3 % at refresh, rank* = 12; M1-seed11-17 → 7.0 %, rank* = 13. Both legs robust. (c) *Independent audit* (above). Method, regenerable: λ_m(t)=λ0_m+n_m·t (linear); rank of j in i's order at t = 1 + #{m∉{i,j}: circ_dist(λ_i(t),λ_m(t)) < circ_dist(λ_i(t),λ_j(t))}; encounters from the patch's own truth pipeline (`enc_list` = analyse's, dedup included).
4. **Novelty.** No H entry measures horizon, e-spread or traffic sensitivity of a phase-rank certificate (tree HISTORY ends H0215; the gold is a 6 Oct lab result). The gold's own dossier *flagged* "e-spread ≫ ρ could break phase-order = distance-order" as untested — a risk note, not a measurement, and the frozen gate ("the gold run's scenes and a dense ring", `lab/lenses/b-coorbital-cert.md`) would not have caught E1 or M1. This run converts the risk into gate scenes and bounds before the freeze. q-candidate-degree's cone result is used, not repeated (6000/6000 consistent with it).
5. **Goal fit.** This is the mandated pre-freeze red-team ("Before any freeze, one GLM red-team and the cheapest falsifying probe must have run"). It respects "a failed expectation is not automatically a failed method" (the gold's measurement stands; its generalisation is bounded), and the compounding-miss concern is OC#34's exact case. The E1+M1 legs alone delete the population-trigger component and force per-pair classification — adoptable within one step (a brief edit).

**Why not gold.** The claim sentence's first clause ("at 10× the horizon the same clump needs rank 42") is measured-against by the gold's own specified design: rebuild-on-overtakes achieves zero misses at k = 4 on H1. The author hedged exactly this in "what would make it wrong (1)" and asked the checker to pull the gold's dossier; the pull settles it against the headline. A gold abstract cannot carry a headline number the checker's five-minute measurement overturns. The corrected claim — scene-boundness via *ϖ coherence* and *traffic*, not horizon — still stands on E1+M1.

**The one experiment to gold.** Rerun the horizon leg against the specified rebuild-on-overtakes certificate (piecewise-constant mean-longitude order; refresh events = the overtakes the probe already counts analytically — `crossings`), state the refresh schedule and its cost in the brief, and re-issue the claim on the corrected legs (E1: frozen order, any cadence; M1: trigger-blind, cone composition). My attack mode already implements its continuous equivalent and shows what it will find; the physics is done, the rewrite is not.

**What the author missed.**
- The H1 leg attacks a certificate the gold did not specify; the natural patch is cheap (order frozen between overtakes; refresh is a Diophantine event, not "the cone tier again" — the dossier's own dismissal of it is wrong).
- The gold's *measured* quantity was distance-rank at closest approach; E1 breaks the longitude-sorted *implementation*. The distinction (oracle vs watch) belongs in the brief.
- The gold's own fleet had 2ae/ρ ≈ 20 with ϖ bunched ±0.1 — rank-4 held there by *ϖ coherence*, which is the sharpest statement of the hidden scalar; one sentence would have nailed the thesis ("scene-bound") more precisely than the horizon leg.
- Inclination/3D and kick-perturbed re-sorts untested (stated); one seed per scene — I covered E1 and M1, not H1/B1.

### 20261009-1259-inversion-2360
Grade: gold

**Abstract.** Red-team of the adopted co-orbital train certificate, on the dead build's never-executed `train.rs`: sound exactly where gold 20261006-0346 feared (0 misses/0 false on 123 forced-clump family encounters at e-spread up to 0.05 ≫ ρ; controls 0/0), but the engagement logic fails twice — Binet-L1 clumping fragments families with σ_e·a ≳ 2–3×10⁻³ (0.1–8% of pairs covered; my full-truth probe: only 1/2, 0/3, 2/30 real encounters lie inside fired clumps), and bunched-eccentric clumps fire at ζ ≈ 0.11–0.14 with a 63–98% watch costing 150–243× the pairwise tier. Checker reproduced every cited number exactly and extended the finding. Adopt before the two queued builds: U-only clumping, dormancy-priced ζ, a third regime for the fluid corner.

**Reproduction** (clean tree at a838a28, `CARGO_TARGET_DIR=/tmp/enc-target cargo build --release -p emergent-encounters`, all five sets, total < 25 s, < 200 MB):
- The dossier's instruction "apply the dead build's patch, then this run's `work/patch.diff`" double-applies — the run's patch already contains the dead build's `train.rs` bit-identical (verified by diff). Applying only `work/patch.diff` is the working reproduction; note for the publish step.
- Controls: 7 phalanx + 5 rings, one clump, fired, **0 misses / 0 false**. Truth encounters: 466 + 12 = **478** (dossier says 474 — tally slip; every per-scene number matches). Train 13×–1767× cheaper per encounter, inside the claimed 10–1800×.
- Detector cliff, exact: σ_e=5e-3 → 24 clumps, 149/200 bodies, 1,571/19,900 pairs; 0.02 → 17/36/21; 0.05 → 10/22/14; bunched 20 clumps, 41/200, 22 pairs. `binet()` = [1/p, e cosϖ/p, e sinϖ/p] confirms the L1 is over the full Binet 3-vector including U; d_c = 8·eps_max with eps_max ρ-scaled (pairs.rs:83) — the mechanism claim checks out in code.
- famf (forced clump): **0/0 on 123 encounters**, watch 130/501/1,337 = 0.65/2.5/6.7%, crossover at σ_e=0.05 pairwise 68× cheaper (375.7 vs 25,571 evals/enc) — all exact.
- Degenerate corner, exact: ζ 0.1195/0.1131 fires; watch 62.7%/91.4%; train 1,092,448/1,652,177 evals vs 7,115/7,386 = **154×/224× worse**; 0 misses. Unit tests 5/5 (K_v finite-difference to e=0.4, brute-force window coverage, soundness probe).

**Adversarial cases (mine, set `famx` + full-truth probe `famt`):**
1. σ_e=3e-3 pins the cliff: 7 clumps, 71% of pairs covered — a ramp between 3e-3 and 5e-3, consistent with e-spread ≈1.4σ_e crossing d_c ≈ 3×10⁻³.
2. High-e (σ_e=0.15, cap 0.5) at design d_c: 25 clumps, 51/19,900 pairs — extreme fragmentation. Forced clump: ζ=1.90 **declines** — the degenerate-fire corner is a band (bunched, σ_e ≈ 0.005–0.05), not all high e. Slightly narrows the pathology; the σ_e≈0.02 family is exactly the regime at stake, so the claim stands.
3. n=400 at σ_e=5e-3: 24 clumps, 27,397/79,800 pairs (34% covered, vs 7.9% at n=200) — coverage **grows with n** (percolation merges components). The "92% blind" figure and the 72 TB fragmented-path arithmetic are n=200-scale; at 10⁶ the family plausibly becomes one giant fired clump whose watch is still quadratic (ζ ≈ 2L̄_max/spread is asymptotically n-independent, so watched ∝ n²·fraction). The structural conclusion — ζ prices the wrong denominator, neither tier serves a large e-spread family — survives and is stronger, but the 72 TB number itself is single-scale (the dossier flags this honestly).
4. σ_λ=0.01 (the prediction's original value, dropped from the shipped scenes): ζ=0.14, watch 97.9%, train 243× worse, 0 misses — corner extends to near-total watch.
5. **Full truth over all 19,900 pairs** (the author's harness only truth-checks intra-fired-clump pairs): real encounters inside fired clumps = 1/2, 0/3, 2/30 across fam/famb scenes. As engaged at design d_c the certificate catches almost none of the families' real encounters (correctness preserved by the pairwise fallback; this is coverage). Confirms "never engages there" in the strongest sense.

**Predictions.** Pre-registered kill criteria match the shipped harness; content is coherent with pre-registration (no finding appears in it; misses reported against interest). Cannot verify file-time order — the folder is materialized at check time. Held: 1 (controls), 4 (soundness — the adopt-blocking criterion), 2 and 6 partially (watch fraction exact, degeneration direction right). Missed, both disclosed: the decline mechanism (fragment-fire instead of decline) and prediction 5 (pairwise misses ≥1% → 0 on 126 family encounters — the gold's phalanx misses do not extend to families). The misses concern the pairwise tier and the trigger's mechanism, not the soundness or cost findings the dossier rests on. Scene drift: predictions' fam-b σ_λ ∈ {0.05, 0.01} vs shipped {0.05, 0.02} (I re-ran 0.01 myself).

**Novelty.** No H entry or doc records the engagement hole. The gold's taste-log entry (6 Oct) records only the adoption; the sibling build 20261006-1931-b-coorbital-cert-152e died at 429 before running one scene — this run is `train.rs`'s first execution anywhere. HANDOFF queues the co-orbital certificate for both GLM and Codex this week: this is the pre-freeze red-team those builds need.

**Goal fit.** Board's top scaling risk (candidate work must track real encounters) inside the newest adopted design; premise correction one step before two builder windows are spent. PRINCIPLES: #19 "a fix signals the wrong representation" (the watch is right water, the Binet-L1 detector drags the fish into the wrong pond); #4 "regimes are chosen by dimensionless numbers" (σ_e·a/ρ and n_c·ρ/(spread·r)); #1 "the cheapest compute is compute not done" (a fired 91% watch is compute for no reason). Adoptable within one step: (a) U-only clumping, (b) dormancy-priced ζ with decline-to-pairwise as watch fraction → 1, (c) the fluid corner out of certificate scope by the same number that detects it.

**Gold rather than silver because:** every verdict-carrying number reproduced exactly; the failed predictions were disclosed and do not underwrite the claims; the finding breaks a premise of an adopted design (the certificate's engagement, not its math) with a one-step fix, before the build spend. Contrast the 1 Oct red-team's silver: there a failed prediction was reported as held.

**What the author missed.**
- Truth never extended past fired clumps: one cheap probe (mine, `famt`) shows the train catches 1/2, 0/3, 2/30 of real family encounters — a stronger statement of the author's own headline, left on the table.
- n-dependence of fragmentation: coverage 7.9% → 34% from n=200 → 400; percolation at 10⁶ likely merges the family into one fired clump, trading the 72 TB pairwise ruin for a still-quadratic watch (fraction n-independent). The 10⁶ arithmetic should argue watch-vs-encounters, not fragments-vs-pairwise.
- The degenerate corner is bounded in σ_e (declines above ~0.15); a band, not a regime.
- ζ's asymptotics (ζ ≈ watch fraction, independent of n_c) make the mis-pricing analytic rather than corner-specific — the argument needed no run.
- Reporting slips: "400 encounters" (claim) vs 123 (famf, §3) or 126 (all family scenes); 474 vs 478 (controls); "277 family encounters" matches no tally I can construct; `equalp`/`ring600` sets shipped but unreported; the dossier's double-patch apply instruction.

### 20261009-1259-second-20261009-1210-inversion-c529-154a
Grade: gold

**Abstract.** Claim: the co-orbital watch as the gold specified it (rebuild-on-overtakes) is horizon-sound and governed by epicycle-scale-vs-spacing, not horizon, 2ae/ρ or ϖ coherence; the first author's horizon kill is retracted. Reproduced bit-identically (all four JSONL, both audits); the prior silver's named experiment is done and extended with two-sided controls (G1/G1b/G1c/E3), and the oracle-vs-watch split (0/31305 d-rank>4) is measured. My attacks — dense 600-swarm, refreshed belts, e×10-random-ϖ fleet, independent M1b recount (rank 105, gap 54.1 spacings, digit-exact population) — all confirm. Gain: correct gates for the co-orbital brief before freeze. Cost: one brief edit. Two required fixes: regen.sh's double-apply (fails as shipped; one line), and the declared bound needs a ~3× safety factor (G1d: bound says pass, measured 13.5% miss, rank*=10).

**Reasons.**

1. **Reproduction.** The dossier's stated procedure (first author's patch verbatim + `patch2.diff`) regenerates everything bit-identically modulo `secs`: `control`/`heldout` (first author's record), `inversion2 a`/`b` (the decisive runs), both Python audits agree (G1c 89/107: d_min 8.8e-6, 0.77 spacings; E1 33/259: rank 8 = Rust). I verified the head of `work/patch.diff` is byte-identical to the first author's branch patch. The first author's watch is confirmed frozen at λ(0) (`rank_matrix` uses `lam0`) — so the retraction's premise is code-verified, and the gold's own dossier (pulled from `claude/lab-20261006-0346-taleb-09b5`) does specify "rebuild on overtakes" and did measure distance-rank.
2. **Predictions.** `predictions.md` (13:10:22) predates `refresh-a.jsonl` (13:10:49) and `refresh-b.jsonl` (13:11:40). Held-out discriminators held: G1 (255 ∈ [60,600]), **G1b 0 missed** (kills ϖ-coherence as binding), **G1c 4.4%, rank* 6 ∈ [4,16], below E1 despite 10× 2ae/ρ** (kills 2ae/ρ), oracle d>4 = 0 everywhere. Soft misses (E1/E1b range calibration, E3 at 4.5% vs >10%, M1b rank 105 vs the prior checker's 13) are stated, not hidden; my independent recount resolves M1b in the author's favour.
3. **Attacks (mine, `inversion3.rs`, removed).** (a) *Dense swarm* (n=600, σ_e=1e-2, equal periods): watch misses 71.5%, rank*=19 — and the **oracle still holds** (d*=1, 0 violations): the universal survives a genuinely adversarial crowd. (b) *Belts under the specified watch* (the dropped family): B1 rank*=38, not the frozen 549 — the pinning mechanism predicts exactly tens; B2 misses 0 (the first author's 84.9% was pure frozen-t0 artifact). The "one mechanism" claim survives the family the author skipped. (c) *G1d* (gold fleet, e×10, random ϖ, new seeds): 13.5% missed, rank*=10, worst pair at 2Σe = 5.1 spacings → the bound's form is right, its constant is ~2–3× optimistic (their own E3/G1c already sit at rank*=6 > 4). (d) *M1b recount* (independent Python, digit-exact population): rank 105, gap 54.1 spacings.
4. **Novelty.** No HISTORY entry or doc measures a refreshed phase-rank watch, the e-scale-vs-spacing bound, or the oracle/watch split (tree HISTORY ends H0215; the gold proposed refresh but never measured it; the two inversion runs are this arc). The prior check's named experiment is precisely what was run, plus the controls it demanded.
5. **Goal fit.** This is the mandated pre-freeze red-team completing its arc: it shows a premise (horizon as a validity scalar) is wrong, bounds the certificate's true validity regime, and hands the freeze three declared bounds and gate scenes that can fail (E1 kills any cadence; G1b passes without coherence). "A failed expectation is not automatically a failed method: diagnose which one broke" — done, twice (the gold's watch, the first author's frozen instrument, and the author's own two disclosed instrument bugs). Adoptable within one step: a `b-coorbital-cert.md` edit.

**Corrections required with adoption (both one-liners).** (1) `regen.sh` fails as shipped — `work/patch.diff` (run.sh's saved patch) already contains `inversion2.rs`, so the second `git apply` aborts before building; fix by applying `patch.diff` alone (or a verbatim first-author copy + `patch2.diff`). The numbers themselves regenerate bit-identically once this is fixed, so this is a record defect, not an unreproducible result. (2) The watch-soundness formula `2·e_scale ≲ k·(2π/n)` must carry a ~3× safety factor or be replaced by the gate scenes (as the author's own cost-of-adopting already prescribes): G1d sits inside the declared-safe region and misses 13.5%.

**What the author missed.**
- The refreshed watch also rescues the cold belt (B2: 84.9% frozen → 0% refreshed, rank*=4) and pins B1 at rank*=38 = mechanism-predicted tens — the retraction's reach is larger than claimed, and it further confirms the single-mechanism story on the family the table dropped.
- The bound's constant was testable from their own scenes (E3/G1c at rank*=6 > 4 already breach it at k=4); my G1d makes the looseness quantitative.
- k≠4 and sweep-refresh remain unmeasured (stated); the shipped `miss` histograms already
 carry the k-sweep for free (E1: k8 = 0/560; E3/G1c: k6 = 0 — the bound-in-k is checkable
 without a rerun; my adversarial S1 needs k≈19, B1r k≈38).
- Inclination/3D and kick-perturbed λ(t) stay untested, as the first author also stated; the deployment watch refreshes on analytic overtakes only while λ stays linear.

### 20261009-1504-inversion-322f
Grade: silver

**Abstract.** Claim: the gold's "sort by longitude, watch k≈4" read as a mean-longitude train fails by the equation of center — a k=4 λ-watch catches 36% of encounters in the gold's own control fleet (λ-rank p50 6, max 33) while the distance-rank statistic passes everywhere, so the shipped sort key must be pinned. Reproduced: `verify_mech.py` exact (Δλ = Δeqc, 46.4 vs 46.6ρ); S0 and all S2 rows bit-identical; my probe gives 32–33% catch on three fresh seeds and 46% miss at e-cap 1.5e-3 (not the truncation tail). Gain: kills the last naive reading before b-coorbital-cert builds; cost ≈ zero. Not gold: the divergence and mechanism are already on the record from four uncited runs, and the built train already bounds the equation of center.

## Reproduction

- `python3 verify_mech.py`: identical to the dossier verbatim (227 encounters, 46.4/46.6, 42.9/42.1, median 12.2ρ).
- `python3 invert_train.py`: S0 and S2 rows (σ_λ 3e-3…3e-4) regenerate **bit-identically** from the shipped script (S0: dist max 2, λ p50 6/max 33, catch 0.3625; S2: dist max 8–9, le4 0.97–1.0; λ catch 0.02–0.1). The S1 rows reproduce in `ev3.log` (θ max 1, λ catch 0.15/0.276); I could not rerun S1 inside the checker window (CPU contention), but its θ-rank≈1 is forced by geometry (uniform λ, θ-spacing 157ρ ⇒ contact implies between-count <1) and matches the author's exact re-audit.
- The three logs tell a consistent, disclosed story: `evidence.log` (pre-fix: S1 θ inflated to ~300, λ max to 184) → script fixed → `evidence2.log`/`ev3.log` clean. The λ catch rates are unchanged by the fix (0.1/0.0325/0.02/0.025 in both), so no headline rests on the contaminated code. `work/patch.diff` is empty (no tree edits).
- **Predictions:** file times support pre-registration (predictions.md 30 min before evidence.log); P1/P2 held, P3 held only per its instrument (see attack 1), P4 (Binet ratio ≥100) failed at 33× and is disclosed as failed. Honest reporting throughout.

## My attacks

1. **The S2 truth detector shares the θ-train's blind axis.** `formation_scene` detects contacts only between θ-sort *adjacent* pairs plus one lookahead (`invert_train.py:148-164`). In the σ_λ=1e-3 jam (spacing 0.16ρ), I densely sampled 2 orbits and counted sub-ρ contacts by exact θ-between-count: **47.4% have ≥2 bodies between** — invisible to the detector. So S2's "θ-train catches 100% (max rank 2)" is circular (the instrument *is* a k≤2 θ-train), and "dist-rank ≤4 for 97–99%, misses stay rare" is biased low: the missed half is exactly the high-rank half. The real jam law was already measured with an unbiased per-pair truth by **b1c0**: rank ≈ 1+(1.2–1.7)·J, k=4 misses 19–78% at J=5–87. S0 is unaffected (spacing 1.3ρ ⇒ between-count 0 at contact) and S1 uses analytic crossing search. The dossier's own heuristic — "agreement is not independence; check that the measured events are distinct" — applies to its S2 rows.
2. **Not the e-tail.** With e capped at 1.5e-3 (vs the gold's 1e-2 truncation) the λ-watch still catches only 46%: the failure is the Rayleigh body, not the cap. Circular control e≈0 gives rank 1, catch 1.0 (control passes both sides).
3. **Seed robustness.** Seeds 41/42/43: catch 0.3325/0.32/0.3225, λ max 35–40. The 36% is not seed 27.
4. **θ-churn is real.** Direct simulation, S0: 23.75 θ-order swaps per body per orbit vs 2.29 for λ-order (~10×) — the author's asserted "a θ-order churns every orbit" is correct and now measured; their `swaps_over_horizon` (net unwrapped laps, 336 fleet-wide) under-counts order swaps and should not be reused.
5. **Trigger horns confirmed**: Binet diameters 3.25e-3 (control) vs 0.107 (debris) reproduce in the logs; the 33× gap and both horns are consistent with the record below.

## Novelty — why silver, not gold

The headline ("the instrument vouched for the wrong quantity; mean-longitude order ≠ proximity order by O(2e)") is substantially on the record, none of it cited:

- **The gold itself** (taleb-09b5, lesson 6): its first λ-binned brute "missed 193/233 encounters because co-orbital proximity aligns *true* longitude and the equation of center … dwarfs ρ" — same scene (n=200, σ_λ=0.01 phalanx), same mechanism, milder window.
- **d1b0** (8 Oct, `lab-20261008-2349`): measured the law (λ-distance at contact ≈ (1–2)·σ_e) and concluded "the watch-list must be the bodies inside a λ-window of ~2σ_e, not k=4 nearest".
- **a937** (9 Oct 02:08, **gold-graded**): the same adopted sentence, same divergence measured at its extreme (distance-rank 100% vs longitude-rank 244–363, 98–100% miss, polar; quadratic retrograde churn) — this run's memo-artifact framing is a937's finding restated, coplanar.
- **b1c0** (9 Oct 05:21): k is not a constant (crowding law, 19–78% misses), "crowding must be measured in the coordinate the sort uses"; trigger never fires (19–461× above threshold).
- **2360** (9 Oct 12:59, **gold-graded**, two hours before this run): the built train's engagement logic and ζ.
- **The thing that would actually ship** — `train.rs` in b-coorbital-cert's patch (executed by 2360) — watches λ̄ pairs within the *sound* per-pair window L̄ = δ·(1+L_E) + K_v·|(ΔV,ΔW)| (coarsely δ + φ(e_i) + φ(e_j)): the equation of center is rigorously bounded, by construction. Attacking the fixed-k=4 sentence attacks a spec the lab had already superseded three times.

What is genuinely new and decision-relevant: (a) the k=4 **λ-rank** measurement in the gold's *exact* control scene (36%, seed-robust, not tail-driven) — b1c0 measured θ-rank there (≤3, zero misses), d1b0 λ-rank only in its own scenes; (b) the pinwheel battle-debris scene (all 79,800 pairs crossing, dormant 0.004 enc/ship/orbit, λ-order frozen: 12–17 swaps/20 orbits, Binet 33×) adding the trigger's other horn — exclude debris and the quadratic ruin stands for exactly the battle aftermath the game produces; (c) the θ-vs-λ churn distinction, which the record had only as b1c0's λ-overtake counts. These sharpen the pre-build spec; they do not move a bottleneck 10× or delete a component.

## The one experiment that would make it gold

Attack the live design, not the dead sentence: run the *built* `train.rs` (sound λ̄-window + ζ trigger) on these scenes — phalanx, jam at J≈6, pinwheel at e=0.05 (φ(e) ≈ 0.1 each ⇒ window ~0.2 rad ⇒ ~13 watched partners per body in a uniform-λ clump). Measure ζ, watch degree, misses and cost per real encounter. If the sound window is mute or quadratic on debris/battle aftermath — the scenes this run introduced — that is a gold-shaped correction of what ships. If it holds, the train question closes.

## What the author missed

- The S2 instrument bias (attack 1): their own memo-artifact lesson, one layer down — the truth detector and the θ-train agree because they have the same shape; P3's "misses stay rare" is the artifact, and b1c0's unbiased numbers are the truth.
- The four prior runs on the same certificate (two gold-graded, one two hours earlier) and the gold's own lesson 6: an inversion of an adopted gold should search the successors of that gold first; the novelty claim ("scenes it never ran") is true only of the gold, not of the record.
- The built train's eqc-bounded window: the dossier's "fix" (sort by θ, size k by multiplicity) is b1c0's conclusion plus d1b0's window; the one design already encoding the mechanism is not examined.
- Minor: P2's "caught 72–88%" should read *missed* (ev3 catch is 15%/28%); S0 ranks the first 400 of 729 encounters by insertion (earliest) order — a mild selection, immaterial at these numbers.

### 20261009-1556-inversion-3036
# Check — 20261009-1556-inversion-3036

Grade: silver

**Abstract.** Claim: the adopted phase-neighbour certificate (gold taleb-09b5) is blind across orbit groups, and the cone tier covers crossing fleets only at all-pairs cost. Reproduced bit for bit (5 scenes, 4.88 s, 5.8 MB); all derived numbers recompute from the JSON (cone work/cross-encounter 107→856 under ÷8 dilution; node 10.8→13.6; node candidates ÷6.32 vs encounters ÷7.99). Phase cert missed 100% of cross encounters in every scene, including mine. Gain: a measured hole plus the surviving O(N²) in the fleet-battle scene — input to the in-flight co-orbital-certificate build. Cost: the proposed node-event cure is falsified at tangential crossings (my runs: 20.2% and 4.3% misses), so adoption needs a Wide treatment first.

## Reproduction

Clean tree, `git apply work/patch.diff`, `cargo build --release --offline -p emergent-encounters --bin inv3036`: all five scene lines of `run5.jsonl` identical bit for bit. My timing 4.88 s / 5.8 MB vs claimed 4.95 s / 5.9 MB. Truth and cone calls are the crate's own (`truth_pair`, `is_candidate`); only the probe is new. `predictions.md` predates `run1.jsonl` (file times 12m vs 10m; run5 2m). Runs 1–4 show the disclosed probe bugs (run1 S2 `cross_enc=0`).

## Predictions

P2, P3, P5, P6 held exactly; P7 held (62,500 candidates unchanged under ÷8 encounters; node ÷6.32); P4 in order of magnitude. P1's intra zero-miss failed (16 static / 4 maintained of 389) — disclosed prominently and converted into the secondary finding, not hidden. Honest handling.

## Attack (three scenes of my own, same harness)

- **C1** e_B=0.9, a_B=1.05, 20 orbits (transversal, high-e): 305 cross encounters; node cert 0 misses, 4,984 candidates (16.3/encounter); phase 305/305 missed; cone all 25,000 pairs. The cure holds at transversal crossings of any e.
- **C2** exact tangency (a_B=2, e_B=0.5, periapsis r=1): 1,447 cross encounters; node cert misses **292 (20.2%)** even with its adaptive window ballooned to 0.129 (10× S2's); cone all pairs, 0 miss; phase 100% miss.
- **C3** near-tangent (a_B=1.99, crossings at f=±0.174): 280 encounters; node cert misses **12 (4.3%)**.

The author's own pre-registered kill criterion ("if the node cert misses any truth cross encounter with safety 2, the cure as sketched is wrong") fires at the tangential end: encounters live across the whole quadratic |Δr|<ρ band, not near node passages, and some (body, other-mean-orbit) Binet pairs have no root at all. The negatives (phase-cert blindness, cone = all pairs) held in every scene; the cure does not generalize. Secondary finding confirmed: rank-4 intra misses 1.4–3.3% maintained, up to 43% static (my C1: 602/1389).

## Novelty

No prior measurement of multi-group composition: the gold taleb-09b5 measured one formation; r8 v2's "group certificates" lead was disjoint envelopes, a different mechanism; the crate's per-pair `sections` (Kind::Wide exists there) is the quadratic tier. HANDOFF's top risk (line 69) is exactly this; the b-coorbital-cert build is in flight, which the author flagged as the contingency — the board text shows no cross-group tier.

## Goal fit

Directly on the board's top scaling risk and its bar, "candidate work must track real encounters": the cone tier fails it by ÷8 under dilution in the crossing scene while the node cert tracks at ÷6.3. PRINCIPLES §2/§13: error type over error size — 100% misses against quadratic work is the right thing to measure.

## Why silver, not gold

The measured hole is real, but the deliverable cure breaks on adversarial scenes the author's transversal fleets missed, and the claim's force is contingent on the in-flight build not already carrying a cross-group tier (unresolvable from the board text; the author disclosed this).

**The one experiment to gold:** a group-pair tier with the tangential/shallow-crossing treatment (passage-overlap across the |Δr|<ρ band, the group analogue of `Kind::Wide`), zero misses on C2/C3-type scenes at O(n) candidates — plus adjudication against the in-flight b-coorbital-cert design.

## What the author missed

The shallow/tangential crossing regime (my C2/C3), where their own kill criterion fires; that the 100%-miss headline is near-tautological as stated (the cert emits only intra-group pairs by construction — the load-bearing content is the cone's all-pairs cost and the dilution tracking); and that equal-period t=0-centred rendezvous scenes push the closest conjunction to t=0, which the truth excludes via `tm > 0` (S2b drift is the honest scene, and it is included).

### 20261009-1858-inversion-9d6d
Grade: gold

**Abstract.** Claim: the adopted phase-neighbour certificate's rank k is not scale-free; it must grow as κ = m·E|Δn|·H/W. All six scenes reproduce exactly (static rank p99 3→98 as κ goes 0.75→48; miss(k=4) 0.05%→80%; encounters ×14.2 over ×4 m). I confirmed the collapse on an axis the author never ran (κ=3 as m1200·band 1e-4: p99 9, miss4 14.4%, matching m300·4e-4's 9/13.3%) and add two caveats: (1) the gold's "rebuild on overtakes" design misses ~0 — my probe measures dynamic rank p99 ≤ 4 in every scene, including the bunched killer — so the correction is the unstated rebuild volume m·κ/2 (the gold's 10⁶ "n_c·4 sections" store is off by ~600×); (2) e-spread ≫ band inflates rank past κ (mean 3.9→11.7). Adoption: size k or cadence by κ.

**Reasons.**

1. **Reproduction (exact).** Applied `work/patch.diff` in a clean tree, built `rank`. All six scenes return statistics identical to `evidence.jsonl`: anchor (κ 0.75) p50/p99 1/3, miss4 0.048%; m300-b4e-4 2/9, 13.3%; m600 3/15, 30.6%; m1200 5/28, 50.8%; collapse 4/25, 48.0%; bunched (κ_eff 48) 15/98, miss4 80.4%, miss64 6.4%. Anchor also reproduces the gold's own scene (main.rs `coorbital` spec): rank-4 was safe there by factor ~5, as claimed. Each command 1.5–29 s, < 100 MB. Load 1.4–2.4 of 8.

2. **Predictions.** `predictions.md` mtime 19:11:34 precedes `evidence.jsonl` 19:13:25 and `dossier.md` 19:13:54; content is pre-registered with a kill criterion (anchor p99 ≤ 4; m1200/m300 p99 ratio > 2) that did not trigger (ratio 3.1). P1–P8 held; P9 held on p99 (98 in 90–130) and missed two sub-numbers (p50 15 vs 20–30; miss4 80.4% vs >85%) — disclosed honestly in the dossier.

3. **Attack (four adversarial cases).**
   - **New collapse axis (held):** m1200 at band 1e-4 composes the same κ=3 as m300 at band 4e-4 → p50 2/p99 9/miss4 14.4% vs 2/9/13.3%. The dimensionless law generalizes beyond the axes the author varied.
   - **e-spread ≫ band (gap found):** σ_e 3e-2 at fixed κ=6 → p50 10, p99 33, mean 11.70 (vs 3.87), miss4 83.5%. Rank inflation beyond the κ law: the equation-of-center term (~2(e_i+e_j)·m/W) is a second factor the sizing law omits. Plausibly outside the certificate's trigger regime (the Binet clump number bounds e-spread inside it), but this run shows neither the effect nor the regime boundary — the lens flagged it and left it to the checker.
   - **Static vs dynamic (framing corrected):** the gold measured "rank at closest approach"; its design rebuilds on overtakes. My probe (rank2) measures the partner's mean-longitude rank at encounter time: p99 ≤ 1 uniform / 2 at m1200 / 4 bunched (max 9). So the 50–80% misses apply to a certificate that sorts once at window start and never re-sorts — faithful to the board's adopted summary ("within partner rank 4 along the orbit", no rebuild mechanics) but not to the gold dossier's spec. What the dynamic design actually hides is the swap volume: total order changes per window = (m²/2)·E|Δn|·H = m·κ/2, which follows arithmetically from the same drift law the static-rank collapse verifies. Either form — static k=κ, or rank-4 with re-derivation every ~4/κ of a window — costs m·κ, not m·4. The gold's 10⁶ arithmetic ("~4×10⁶ sections (~300 MB)", κ=2500 at its own band and H=50) is wrong by ~600×, and per-orbit cadence still leaves κ≈50.
   - **Arithmetic audited:** E|Δn| = 0.5·band (two uniforms, dn/da = −1.5 at a=1) ✓; encounters 2,130→30,168 = ×14.2 over ×4 m ✓; p99/κ ≈ 2.0–3.0 across all scenes (consistent linear law) ✓; H ≲ 4/κ restores rank-4 ✓.

4. **Novelty.** No prior entry sizes the certificate. The gold (20261006-0346-taleb-09b5) states rank ≤ 4 and O(n_c·k) with no sizing law and its own "what would make it wrong" flags rank inflation as unproven suspicion; the follow-up build (20261006-1931-b-coorbital-cert-152e) was VOID ("Grade: missing", empty logs); HANDOFF.md line 69 restates the gold without sizing. The κ law and the collapse evidence are new.

5. **Goal fit.** The board's top scaling risk ("candidate work must track real encounters") and the gold's own seam: the trigger was dimensionless but the width was a constant measured once — "regimes are chosen by dimensionless numbers" (#4) cut off halfway. Correct error-type framing: a fixed k turns a zero-miss certificate into a silent dropper (#13, "types of errors and not just errors"); "the simulation decides, not us" — k from the fleet's own drift number (#22). Adoption is one dimensionless number already computable from the trigger's own inputs; no new state.

**Gold despite two named defects**, because the premise it kills (constant k / O(n·k) cost) is demonstrated exactly, the record is pre-registered and honest, and the correction is adoptable in one step regardless of which variant (static width or dynamic cadence) the integrator builds — both are m·κ. The integrator must read the miss numbers as the static variant's, per caveat (1); the adoption sentence in the dossier already covers both forms.

**The experiment that would harden it to full trust:** vary σ_e at fixed κ across the trigger seam, add the equation-of-center term to the sizing law, and show the trigger (Binet clump number) excludes the regime where the e-term dominates — closing the gap my second attack opened.

**What the author missed.** (i) The static/dynamic distinction: the evidence table's parenthetical "(what a rank-k certificate can see)" is true only of a never-re-sorted certificate; the gold's specified design sees the current sort, so the headline misattributes the error type (miss) where the built design's defect is cost (rebuild volume m·κ/2). The author's "what would make it wrong" bullets 2–3 contain this, but the claim sentence does not. (ii) The e-term: one 8-second command away (σ_e ×100 at fixed κ), anticipated in the lens section, left unmeasured; a k=κ adopted verbatim would undersize k in e-diverse fleets — the exact silent-miss failure the run warns against. (iii) tier_pairs_per_enc ≈ 3.1 in the bunched scene undercuts that scene's certificate economics (only ~3× cheaper than the quadratic tier there); the dossier notes the tier is "not cost-quadratic at these bands" but does not confront that the certificate's advantage shrinks as κ grows.

### 20261010-0100-inversion-b063
Grade: gold

**Abstract.** The adopted co-orbital gold's rank-4 phase-neighbour certificate is unsound outside a
single stream: two crossing co-orbital fleets (the game's core scene) give catch@4 = 0% in the
mean-anomaly ordering at every refresh cadence (median rank 0.34n, constant in time; 73
encounters/orbit, dense-brute-force verified); λ-ordering needs k growing ∝ n·v̄·lead (k99 = 9 at
P/32); and even on one stream k is not 4 but grows linearly in ρ·n (max 13 at ρ=1e-3, n=4000; ~10²
at a 10⁶ fleet). The concentration signature (2.0 vs 2.7×10⁴ candidates/encounter) cannot route the
scenes apart; the certifiable property is single-streamness, which the Binet cone already computes.
Cost: none — `b-coorbital-cert` is in flight (HANDOFF:18–19, :69); adopt before it lands.

**Reproduction** (clean copy, nothing in the run folder touched; `work/patch.diff` is empty):
`python3 harness.py` 13.4 s → `metrics.json` **bit-identical** to the stored file; `python3 s2_hot.py`
7.8 s → `s2_metrics.json` identical; `python3 probe_crossing.py` 9.3 s → dense Kepler brute force
(4001 samples/pair) finds 30+42 = 72 of the 73 truth encounters (one wrap-edge pair skipped by the
probe itself, disclosed). Timings match the dossier. S0's conjunction truth is exact
(max_d at conjunction 4.5e-13).

**Predictions.** `predictions.md` (mtime 11 min before `harness.py`, 4 min before the decisive
`metrics.json`) contains paper numbers that *differ* from the measured ones (0.17n vs 0.34n; 220 vs
73/orbit; max 6 vs 13; 37 vs 98.8/orbit) — the signature of genuine pre-registration, not post-hoc
fitting. P1–P6 all held on the measured numbers; the two guard misses are paper-arithmetic errors,
disclosed by the author (S0 scene widened from ±ρ/4 to ±ρ/2 after predictions, disclosed).

**My adversarial cases** (fresh code, `two_fleets` in /tmp, same truth method):
- A1 seed 42, original geometry: 70 enc/orbit, M catch@4 = 0.00 at all leads, median 685, 100% > n/8.
- A2 e=0.05, ϖ_B=π/3 (shallower crossing): 73 enc/orbit, M catch@4 = 0.00, median 354 = 0.18n; λ@4 =
  1.00 at lead P/32 but 0.00 at P/8 — shallow crossings rescue λ only at short lead, exactly the
  author's k ∝ n·v̄·lead law; the adopted k should be sized by crossing transverse speed too.
- A3 per-body a-spread ±ρ/2 (quasi-periodic; the case the author said the lens might miss): 69
  enc/orbit, M catch@4 = 0.00 at every lead, median 665; λ@4 = 0.59 at P/32, 0.00 at P/8+. Exact
  periodicity is not the cause of the kill.

**Novelty.** No H entry inverts 20261006-0346-taleb-09b5; the nearest priors are r8 v2's
conjunction-less encounters (truth completeness, a different defect) and the gold itself. HANDOFF:69
still carries the premise; the build queues (HANDOFF:18–19) still carry the certificate. Novel and
timely.

**Goal fit.** "Gates… judge a representation; they never size it": the correction names the property
(single-streamness) the certificate needs — and it is already a Binet-cone output, so no new
mechanism. "A failed expectation is not automatically a failed method": the gold's measurement
stands (S0 reproduces catch@4 = 100%, max rank 4); its domain claim is what falls. This is the
inversion lens working as designed: the adversarial scene class (two fleets engaging on one ring)
is the game, not a corner.

**Why gold and not silver.** Premise of an adopted gold shown wrong, reproduced bit-for-bit,
held-out predictions held, robust under my three adversarial variants, adoptable within one step
because the corrected build is still in flight. Nothing measured remains between it and adoption.

**What the author missed.**
- The pre-registered instrument guards failed as written (S0 rate 98.8 vs guard ≤ 74; S1 73 vs guard
  100–400). Correctly diagnosed as the guards' own paper arithmetic — the instruments are
  independently validated — but "fail ⇒ VOID" was not invoked; guard thresholds should be set from
  measured controls, not paper estimates.
- The k-law constant: measured k99/(ρ·n) runs 2.5–6, not 1.5; the 10⁶ extrapolation is order-correct
  (k ≈ 150–250) and the conclusion stands, but the "1.5" is fitted to the large-ρ·n corner.
- The corrected closest-approach slope "≈1.165|Δt|" is still below the probe's measured median slope
  (2.2–3.0); the 73/orbit rate is direct and dense-verified, so only the dossier's arithmetic aside
  is off.
- `run.log` is empty (record-keeping gap; harmless since metrics regenerate bit-identically).
- All scenes coplanar and prograde; a retrograde counter-fleet on the same ring (crossings at every
  longitude) would be an even stronger kill scene for the corrected gate's adverse set.

### 20261010-0306-second-20261010-0100-fermi-c11c-4cb2
Grade: gold

**Abstract.** The silver's named experiment, done, and it refutes the lever cleanly: on the shipped law, the shareable compile (`Orbit::compile`/`Passage::compile`) is 9–17% of a distinct kick (median basis), so sharing one compiled cycle across N co-orbital bodies — measured with the sharing premise *granted* (400/400, and my 1600/1600, kicks in one quantized shape) — buys 1.08–1.17× (best tail 6.3×), not ≥ 40×. Reproduced byte-identically: all five shipped digests + replay digests, rtf-100 bench digest, budget-out, amort-out; my fresh quiet-box reruns and an unseen seed agree. Box-independent bound: 40× needs a ≥ 97.5% compile share; the worst measured anywhere is 84.3% (ceiling 6.4×). Adoption cost: none — delete the compile-amortization lever; next rung aims at the rebind remainder (28.4 µs floor, 19× the bar).

**Reasons.**

1. *Reproduction.* Clean tree (patch.diff empty; bench/ drives shipped crates by path, public APIs only). `--kick-bench` 20 s and 55 s seeds 1–3: digest and replay_digest byte-identical to the stored JSONs (and 20 s to the silver's orig-kick-bench.json); medians 39.6–44.2 µs vs stored 38.4–59.2 (quiet box now; same spread the silver's checker saw); quantized hit rates exact (0.161/0.152/0.077). `--bench --rtf 100 --seconds 20`: digest identical, 337.8 events/s, bytes/body 4802. `budget.py` and `amort.py` regenerate their outputs byte-for-byte; derived rows recompute (1,516 ns/kick bar; 41.8→38.3 machines amortized; cap 2.6×10⁷).
2. *The decisive experiment itself.* `second-bench plane 1 55 1.0`: replay_digest equals the shipped 55 s bench's — the attribution provably covers the record's own kicks, and the distinct-kick rule (`seen == item.t`) respects the 5 Oct re-timing lesson. Coverage of `step::process` 98.7–103.3% on plane populations; shares stable across box load (made compile 10.6% stored / 11.6% fresh; leavers 65% / 68%). `second-bench coorbital 400 55 100 2e6`: 400 kicks → 1 quantized shape, 398 exact — deterministic, reproduces exactly.
3. *Predictions.* Written 11 s before the first decisive JSON (03:24:25 → 03:24:36; run.log empty again, so mtimes are the only order evidence — consistent, not corroborated). Scored honestly: P1 and P4 (the verdict, quantified in advance: amortized ≥ 15 µs, gain ≤ 1.3×, ≥ 25× short) held; P3's exact-key half failed and is reported as failed — and that failure is itself confirmatory (formations share the law's 12+12-bit cell, never the exact key, exactly dbd4add's committed split). P5 held at 16% vs 10–30%; P6's seed-2 breach (+37% on a box at load 3.3) is disclosed.
4. *Adversarial (mine).* (a) Unseen seed 4: share 9.3%, gain 1.08×, coverage 1.006. (b) N=1600 co-orbital, 4× the author's largest: still exactly 1 quantized shape, gain 1.15×; secondaries 1.45→2.09 µs only, so the scene does not hide an N blow-up. (c) Independent radius 6×10⁵: 1 shape, 1.14×. (d) Fresh quiet-box verdict, no stored medians: gains 1.11× (made), 3.06× (leavers s1), floor 19.0 µs = 13× the bar — same conclusion at the other load extreme. (e) The arithmetic ceiling: gain ≤ 1/(1−share), so 40× requires share ≥ 97.5%; no population, seed or basis measured exceeds 84.3%. The refutation cannot be box noise.
5. *Novelty.* dbd4add (5 Oct) pinned the exact-key memo *across kicks on one body* (and M1 kick costs, which bound the M1 risk: shares, not µs, carry the verdict); the H0044-era amortization entries belong to the retired evolving-patch law. The compile's share of a distinct kick and the cross-body amortization were never measured — this is precisely the experiment the silver's checker named as the gold condition.
6. *Goal fit.* Board item 3; PRINCIPLES §19 ("a fix signals the wrong representation": the memo patches a per-kick compile a formation representation would not have) and §10 (the simplest falsifying test ran first and killed the lever). A premise is shown wrong with 6–34× headroom, and the replacement target is priced (28.4 µs rebind floor). Adoptable within one step: numbers and a verdict, no code.

**What the author missed.**
- The coverage claim "99–103% on every population" overstates the co-orbital runs (stored 95.5–98.2%); only the plane populations reach 99–103%. Immaterial (under-attribution, not double-count), but the sentence is wrong as written.
- P5 is reported held without noting seed 3's 7.7% (below the 10–30% band); only seed 1's 16% is quoted.
- The share-ceiling argument (40× needs ≥ 97.5%) is implicit in the data but never stated; it is what makes the kill load- and M1-independent, and it belongs in the dossier's "what would make it wrong".
- run.log is empty a second time; two runs in a row now rely on mtimes alone for prediction ordering — the lab should log command execution itself.
- Kick counts per window remain small (25–37 per plane seed); the tail row (seed 3 leavers, n=5 kicks at 565.6 µs) is thin evidence for the 6.3× headline, though the ceiling bound covers it either way.

### 20261010-0306-taleb-8af8
Grade: gold

**Abstract.** Claim: the adopted gold's "every real encounter within partner rank 4" is not a constant but scales with phase density (rank@enc ≈ 0.2–0.5·ρ·n/arc, near-circular convoy), rank@setup is useless under shear, and the fleet⊕belt seam pays cross-family cone setups that never track encounters. Reproduced bit-identically (all commands, ≤ 14 s each): graded frac rank≤4 = 99.9/85.5/59.6/39.7/26.5% across arc 2π→0.03, zero misses, `dup=0`; fleet degree m+123, belt degree 436→792; 94.3% cross setups never hit. My ρ-ladder (5e-3→1e-3→5e-4) upgrades the extrapolation to measured: setups/cross-encounter 17.5→74→139 (∝1/ρ, ~10⁴ at game ρ). Adoption: amend `b-coorbital-cert` before freeze — size k from dimensionless numbers, add shear refresh, route cross pairs to the skin. Nothing to build.

**Reasons.**
- **Reproduction.** Applied `work/patch.diff` to the clean tree (`a838a28`), built, ran every dossier command: `seam cost`, `ring`, `mixed-arc0.1`, the five-arc graded sweep and the belt control. Every counter, rank statistic and fraction is bit-identical to `work/seam-raw.jsonl`; only wall times differ (shared box). All commands ≤ 14 s. Memory far under budget.
- **Held-out predictions.** `predictions.md` (mtime 6 min before `seam-raw.jsonl`; the 14 runs sum to ~80 s wall, so the order is physical) pre-registers P1/P2/P3 with a kill criterion and controls. P1 (degree growth, ~94% setup waste, ρ-independence of candidates) held; P3's rank law held (0.18–0.67·ρ·n/arc across arcs, seed-stable: my second seed gives med 7, le4 38.7% vs 39.7%); P2's completeness half failed and the author reports it as failed — the tier is complete (0 misses) so the tier trigger is cost-driven, not miss-driven. Honest miss, correctly folded into the claim.
- **Adversarial cases (mine; env-var overrides on `seam_bodies`, defaults verified untouched, reverted after).**
  1. Random periapses (graded arc 0.1): rank@enc med 13, frac≤4 = 22.0% — alignment did not flatter the law; it is worse without it. 7 misses / 130,875 (5e-5, terrace scale).
  2. ρ-ladder on the mixed seam (above): cross candidates 25,985→22,765→22,437 (orbit-geometry, ρ-independent to 13% over 10× ρ) while encounters ∝ ρ — the ∝1/ρ waste law is now measured, not argued.
  3. Tight convoy (da 5e-4): the author's escape hatch breaks in the gold's favour — encounters do NOT vanish (267,866, more than da 5e-3's 94,852) and rank@enc med 22, le4 13.9%.
  4. Eccentric fleet (σ_e 2e-2): rank@enc med 53, le4 8.5% at the same ρ·n/arc = 20 — see "missed" below.
- **Novelty.** HISTORY.md ends at H0215 (6 Oct morning); the gold `20261006-0346-taleb-09b5` is recorded only in the board's taste log with rank 4 as a constant and the trigger as "a dimensionless number". No entry qualifies the 4 as density-dependent, and no entry measures the fleet⊕belt seam. It also tensions the adopted q-candidate-degree silver ("work per real encounter constant at fixed density"): with a fleet present, belt-body degree grows 436→792 at m 100→3000 — constant-per-encounter fails at exactly this seam. Nothing prior found; no H entry to cite.
- **Goal fit.** Board focus: "candidate work must track real encounters (`q-candidate-degree`)", the named top scaling risk. Measured violation: ~10⁴ setups per real cross encounter at game ρ, growing ∝ m at fixed belt. "Gates judge a representation; they never size it" — a k=4 baked into the build's tests would size it; the dossier quotes this correctly. Shows an adopted premise is wrong before its build freezes — a gold criterion — and adoption is a contract amendment plus re-pointing the already-queued `b-encounter-skin` at the measured 94%/∝1/ρ target: one step.

**What the author missed.**
- The stated law is incomplete as a sizing rule: eccentricity is a third dimensionless number. At σ_e = 2e-2 (e·a ≈ 4ρ) the same ρ·n/arc = 20 gives rank@enc med 53, le4 8.5%. Contract (a) must size k from the eccentricity-driven phase spread too, or it re-freezes a wrong constant in a wider regime. (Mean-longitude ranking is also the weaker coordinate there; the certificate's own phase coordinate should be measured.)
- The "what would make it wrong" paragraph is wrong in the gold's favour: tighter convoys raise rank@enc (22) and multiply encounters (2.8×), so the gold's evidence sits even further inside the failure region than claimed.
- One seed per scene (I ran a second: stable), and the gold's own scene parameters were not re-derived here (folder absent from this checkout), so the reconciliation with its 4–6% miss regime stays open — the author flags this hole honestly.

**Verdict detail.** Reproduced bit-identically; decisive predictions held with the failure honestly reported; every attack I ran strengthened the direction of the claim (le4 8.5–47.7% across all my variants, versus the contract's 4); the ∝1/ρ seam cost is now measured on a three-point ladder. Gold with the eccentricity caveat above folded into the contract amendment before `b-coorbital-cert` freezes.

### 20261010-0448-inversion-03c1
Grade: silver

**Abstract.** Claim: the pending co-orbital train certificate (`b-coorbital-cert-152e`, never executed — empty run-log, 429) is sound on first run but covers only strict formations: certified share 100→99→83→55→0% as σ_e rises 0.001→0.25, residue cone-admitted with 0 numeric evals and 2 Cross sections/pair, high-e declined, residue store ~0.7–12.6 TB at 10⁶ for σ_e 0.005–0.05. I reproduced every logged count bit-exact (all 25 lines; ring600, claimed but absent from evidence.log, holds when run: 17 enc, 0 missed). Adversarial: the watch is sound forced at e = 0.7/0.85 (141–270 enc, 0 missed — P4's untested half); a-dispersion steepens the cliff (a ±1% at σ_e 0.02: certified 0.5%, admitted 50% ≈ 36 TB); a second latent ζ bug (spread misses the circular wrap gap) over-fires tight-λ̄ clumps ~100×, flipping no author decision. Gates the 152e merge; nothing to merge itself.

## Reproduction (clean tree at a838a28, `git apply work/patch.diff`, CARGO_TARGET_DIR=/tmp/enc-target)

- `train-verify phalanx|rings|equalp|disp` and `frag`: every counted field identical to evidence.log (watched/cone_filtered/queries/windows/evals/events/missed/false per scene; frag clumps, certified_share, cross_cone_admitted, kinds [3588,0,0] etc.). Only wall-times differ (total ~25 s here). Determinism exact.
- `train-verify ring600` (in the dossier and P1, but **no line in evidence.log**): fires, 17 encounters, 0 missed, 0 false — the claim holds; the omission is a log-completeness defect, not a fabrication.
- Store arithmetic verified: admitted fractions 1.0/4.9/17.5% → 5·10¹¹ pairs × frac × 144 B = 0.72/3.6/12.6 TB. Consistent.
- Build 152e confirmed dead pre-run: branch run-log.txt is 0 bytes; checker-final.md ends in a 429. "First execution" is true.

## Held-out predictions

predictions.md predates the decisive run as far as evidence allows (mtimes share a minute with evidence.log); the decisive behavioral evidence is that P2 **failed against the author's own kill criterion and is reported as failed** (predicted certified_share < 5% at σ_e = 0.02 with the pre-registered "adoption value dies" kill; measured 83.1%; the kill explicitly did not land, with the transitive-closure mechanism verified in code — `clumps()` same-cell auto-merge plus union-find). P1, P3, P4-decline and P5-latent all held. P4's soundness half was untested by the author (hie declines, so the watch never runs at high e); I closed it below, in the certificate's favour.

## Attack (my three adversarial cases)

1. **Forced high-e fire (the admitted blind spot).** Fixed e = 0.7 and 0.85, aligned ϖ (±0.02), λ̄ Gaussian σ 0.01–0.05, a jitter 1e-5 — ζ fires where every author scene declines. Result: sound — e 0.7: 192 encounters, 0 missed, 0 false; e 0.85: 141/0/0; e 0.7 σ 0.05 over 4 orbits: 270/0/0 (truth and pairwise method agree). The windowed watch is sound to at least e = 0.85, well past the build's own test coverage (e ≤ 0.4) and past the e ≈ 0.6 the dossier called unexercised. Caveat found: at e 0.85 the train costs *more* than the pairwise tier (370,870 vs 168,820 evals/enc; watch touches ~all pairs) — ζ is a pair-count gate blind to sweep width, so "fires" ≠ "cheaper" at high e.
2. **a-dispersion (the lens's own story, unprobed by the author — every frag scene holds a at ±1e-5).** At σ_e = 0.02: a ±1e-3 → certified 66.6%, admitted 11.3% of all pairs (≈ 8 TB at 10⁶); a ±3e-3 → 11.0%, 28.6% (≈ 21 TB); a ±1e-2 → 0.5%, 50.2% (≈ 36 TB, the near-full ruin). a ±3e-3 with σ_e 0.001 stays 100% (clumping survives e-tight fleets). So the oasis is narrower than reported and the 0.7–12.6 TB headline is a **lower bound**; the direction strengthens the run's thesis.
3. **A second latent ζ bug the author missed.** `zeta()`'s spread loop takes gaps between adjacent sorted λ̄ but never the circular wrap gap, so a tight cluster away from the branch cut gets spread ≈ TAU (measured: occupied 0.064, max internal gap 0.0038 → spread 6.279) and ζ under-reported ~100× (my e 0.7 scene: code 0.055, honest 5.4 → should decline). Same over-fire class as the author's δ bug (P5, confirmed in code: `with_delta` multiplies by 0.0), no unsoundness (the watch is sound regardless; `train_events` sets its own correct δ). I audited honest-ζ on the author's scene families: **no fire/decline decision flips** (phalanx tight-λ̄ max honest ζ 0.22; uniform-λ̄ scenes and the frag ladder are wrap-immune; hie honestly declines at 1.45). Two one-line fixes when 152e is revived.

## Novelty

- The dispersion sensitivity of co-orbital phase-neighbour certification is not new: efc9 (gold, 7 Oct) and 6f01 (gold, 7 Oct) killed the fixed-rank reading and derived the gate (S = N·(extent + Δn·W)/2π) that became ζ. What is new here: the shipped build's own code runs for the first time (152e died at 429; the kills ran on hand-rolled rank-sort harnesses), the watch is shown sound where the fixed-rank certificate died — the kills do **not** transfer to the λ̄-window design — and the trigger's actual calibration (certified share vs σ_e, residue admission fractions, decline at high e) plus the silent-declined-budget finding are first measurements. 2e81's 72 B/section signature is borrowed with citation.
- Minor dossier defects: ring600 claimed but unlogged; the illustrative "phalanx-1e-3-u21: 31 watched pairs" mislabels sw001-41's 31 (u21's is 55) — substance (watched ≪ 19,900) holds on every scene.

## Goal fit

Board's top scaling risk ("candidate work must track real encounters"): this run prices exactly the regime where it does not. PRINCIPLES: "compute only surprises" (#3) — a declined clump silently handing back a Θ(n²) cone-admitted store is the violation named; "regimes are chosen by dimensionless numbers" (#4) — certified_share vs σ_e (and now vs Δa) is that number's calibration; "the oracles are guards, not shepherds" (#34) — declined must reject loudly. "A failed experiment kills that configuration, never the method" (#9) is respected: nothing is killed, the domain is priced.

## Why silver, not gold

Real, reproduced, and load-bearing for the integrator's decision on 152e — but: (a) the author's own pre-registered kill (P2) failed as stated (the certificate is *more* robust than predicted), so the headline is a corrected measurement, not a confirmed prediction; (b) the 10⁶ store figures extrapolate n = 600 admitted fractions rather than measuring any large fleet; (c) the dispersion premise was already established by two golds on proxies, so the marginal novelty is execution-of-shipped-code and calibration, not the discovery; (d) soundness counts are small (≤ 5 encounters on fired disp scenes; several scenes vacuous) — my adversarials strengthen but were not the author's.

**The one experiment that would make it gold:** run the shipped binary at 10⁵–10⁶ bodies with joint (a, e) dispersion and both ζ one-line fixes, measuring directly: honest fire/decline per clump, certified share, cone-admitted pair count and section bytes actually allocated, and the train-vs-pairwise eval ratio on fired clumps — replacing the extrapolated 0.7–12.6 TB ladder with a measured store and delivering the trigger's true calibration curve (σ_e, Δa, ρ) for the merge.

## What the author missed

1. The wrap-gap bug in ζ's spread (over-fires tight-λ̄ clumps ~100×; found alongside their δ bug — the ζ audit stopped one bug early).
2. a-dispersion: every frag scene pins a to ±1e-5, yet dispersion in a (burns, debris) collapses the certificate faster than e-spread alone; the oasis is narrower than the dossier's ladder.
3. ζ is a pair-count gate only: my e = 0.85 fire shows the train can cost more than the tier it replaces (370k vs 169k evals/enc) while ζ reports 0.077 — "fires" does not certify "cheap".
4. ring600 in P1/dossier but absent from evidence.log; the 31-watched example mislabels its scene.

### 20261010-1029-library-6cfc
Grade: silver

**Abstract.** Claim: the slack skin's neighbour set must be phase-rank, not metric, and B12's redesign should use window-mean slope, not a max statistic. Both probes reproduce bit-for-bit (`probe_skin.py` 13 s: metric formation 300–809 pair-evals/kick/body vs belt 2.5–16; phase k=4 stays 3.0 everywhere; `probe_b12stat.py`: mean AUC 0.967 vs max 0.920 at T=1000, both ≈0.50 at T=100). My adversarial cases strengthen it: a station-kept formation saturates the metric skin at 996–999 (the author's fleet shears out mid-run, so 300–809 is a transient lower bound), and mean-slope beat max in all six of my B12 variants (rare-large jumps, AR=0.99, 5% actuation). Gain: keeps the named 12.6× lever alive under concentration; kills m-tuning. Cost: small — design rows in `b-encounter-skin`/`b12-v2`, no code. Silver because the phase-rank fix is taleb-09b5's adopted certificate one layer down, two registered predictions were falsified, and nothing touched the engine's real path.

**Reproduction.** Clean tree, empty `patch.diff`; both scripts re-run: every number identical (skin table and B12 table match the dossier and the JSONs). All six "verbatim" quotes found verbatim in `readwise.json` (4,580 highlights). Predictions pre-registered at 10:34, probes run at 10:50 — order verified by mtimes; predictions describe the v1 design (N=2,000, m≤5) while the shipped probe differs (N=1,000, adds m=8), so no retrofit.

**Adversarial cases (mine).**
1. *Station-kept formation* (re-packed every 5,000 kicks): metric pair-evals 996.2 (m=1.5) and 999.0 (m=8) — full saturation; the author's 300–809 are conservative.
2. *Slow shear* (σ_u=1e-6): 999.0 at both m — saturation is the steady state, not the transient.
3. *Mild packing* (σ_φ=SP/5, only 5×): 296 (m=1.5) / 807 (m=8) — the disease needs only fleet width ≲ m·spacings, so even loose fleets saturate at large m. Strengthens the "no m escapes" claim.
4. *Phase skin under 10× rate churn* (σ_u=1e-3): pair-evals stay 3.0; setups rise ~10× in a belt (3.35e-3), as the dossier predicted qualitatively.
5. *B12 grid*: mean > max in all six variants, including the case built to flip it (p=0.3%, jump=3.0: 0.891 vs 0.822). At T=100 with 5% actuation (E≈5) AUC is only 0.676 — corroborates the "E[actuations] ≳ 10" sizing rule.

**Novelty.** `docs/HISTORY.md`'s "Verlet" hits are unrelated integration experiments; "phase-rank", "slack skin", "window-mean" appear nowhere. But the board's taste log (6 Oct, taleb-09b5 gold) already adopted the phase-neighbour rank-4 certificate for the *window* tier under the same concentration; this run's increment is the measurement that the skin layer catches the same disease, that no slack size m escapes it, that m-tuning is the wrong knob (belt cost flat-to-rising in m), and the B12 statistic bake-off feeding the in-flight `b12-v2` redesign. Real but secondary relative to the adopted gold.

**Why silver, not gold.** Reproduced and robust, but: (a) the remedy is an already-adopted certificate transplanted one layer down, measured only on a synthetic 1-D phase ring — no `crates/encounters` or gate row; (b) the registered prediction record is mixed (P1.1 ✓, P1.2 letter failed/mechanism held, P1.3 ✗, P2.1 ✗, P2.2 ✗, P2.3 ✓) — honestly reported, but gold's bar is that held-out predictions held; (c) the B12 half is a synthetic AR(1) surrogate; the real leak trace (the plane's Jacobi error) is one adapter away and untested.

**The one experiment for gold.** Run the same comparison on the engine's real encounter path — the taleb-09b5 formation workload in `crates/encounters`' own harness (station-kept, with rate churn and eccentricity dispersion), counting setups **and** pair-evals end-to-end — showing the 12.6× slack-skin lever survives concentration with phase-rank sets. That converts a synthetic probe into the `b-encounter-skin` gate row the dossier proposes.

**What the author missed.**
- The formation numbers are a decaying transient: at σ_u=1e-4 the fleet shears past W within ~15% of the horizon, so the reported 300–809 average a saturated start against a quasi-belt tail; the steady-state (maintained) value is ~999, and mild 5× packing already saturates. The dossier presents the transient as if steady — conservative here, but the same sloppiness could overstate a cost claim elsewhere.
- Saturation onset is width ≲ m·spacings, so large m (the natural "safer skin" choice) *lowers* the concentration needed — worth stating because it kills m-tuning from both ends (belt: pair-evals rise; formation: earlier saturation).
- The docstring's "exact" is overstated: the rebuild interval uses max relative rate over set *members* only; a fast non-member can cross the window uncounted (same distribution ⇒ ~2× interval error, immaterial to the ordering but not "exact").
- The phase skin's correctness under rank churn (does the k=4 set still contain real partners when the ordering changes faster than the rebuild schedule?) is assumed from taleb-09b5, not measured; only its cost is.
- "k=4" keeps 3 partners (argpartition includes self): matches "rank 4 along the orbit" but the dossier's "3 candidates" and "k=4" should say k−1.
- The B12 "always-on" control is trivially separable for every statistic (AUC 0.99+) and so adds no discrimination between them; the informative rows are the rare-actuation ones.

### 20261010-1152-second-20261010-1029-library-6cfc-fd0f
Grade: silver

**Abstract.** The checker's named experiment, reproduced. On the engine's real path the library run's cost story holds (metric set saturated by the a-clump alone: 2516 pairs, ~60 ms/kick, permanent at eps ≤ 1e-5; train 5 pairs, ~0.4 ms) and its correctness story is refuted: mean-longitude ranking misses 70–75% of encounters in the churned phalanx and fails on real belts too (λ-rank p50 38). Every decisive record reproduces bit-for-bit (truth: 1105 encounters, misses 825/770/656, λ-rank max 80; slack: fleet-fleet 99% silent, budgets 61× the belt's; anchor 94.6/57.5/3.0/0.25%). My attacks extend it: seed 123 → 72% misses; σ-sweep 0.05/0.2 → 21%→0% as the spacing-vs-2e trigger predicts; λ-rank stays ≥ 61 at churn 1e-3. Silver for the record only: the table's phase-eval cells (12k/20k) are 10× below its own JSONs (119.6k/203.7k), and cost-fleet.jsonl's phase rows predate the final code. Repair is editorial, not experimental.

**Reasons.**

1. **Reproduction (clean tree, no patch — patch.diff is empty; the probe path-depends on `crates/encounters`' public API only).** Built `skin/` fresh and ran every dossier command. Bit-for-bit on all deterministic fields: `cost belt` (344.1 pairs, 6091 evals, 7.281e4 rebuilds/body/orbit analytic), `cost phalanx` (metric 199/77940 evals; mean-λ 5.5 pairs/403 µs; true-λ 199 degenerate), `truth phalanx-low` (1105 encounters, dist-rank max 4, λ-rank max 80/p99 64, θ-rank max 5/p99 4, misses 825/770/656, identical miss examples), `truth uniform-low`, `truth belt` (49 encounters, rank max 73/p50 38), `slack belt|fleet` (budgets 3.525e-5 vs 2.149e-3 = 61×), the crate anchor (`encounters -- kick`: 0.9458/0.5746/0.0295/0.0025 skippable), and `probe_skin_regen.py` (script diff-identical to `probe_skin_v1.py`, output identical). Wall times agree in order (metric fleet 54.9 vs 60.7 ms/kick here).
2. **Predictions.** Pre-registration verified by file order (predictions.md 39 m; every decisive output 30 m–1 m; only `smoke` before, as stated). Scoring is honest against the author's own interests: P3's λ half, P5's fleet kill-line and P6 are all reported refuted. That integrity is why the finding stands.
3. **Attack (my own, five cases).** (a) Seed 123, σ_λ=0.01, eps 1e-5: 1108 encounters, mean-k5 misses 799 (72%), λ-rank max 104; dist-rank ≤ 3, θ-rank ≤ 4, true-λ 0 misses — seed-robust. (b) σ-sweep at eps 1e-5: σ=0.05 → λ-rank p99 14, k5 misses 21%; σ=0.2 → λ-rank max 6, k5 misses 0 (k4 misses 2); uniform → rank 0. The dimensionless trigger (clump λ-spacing vs epicyclic amplitude ~2e·r) is quantitatively right — the author left it unswept and it holds. (c) Churn 1e-3 (seed 27): λ-rank still max 72/p99 61 — the coordinate mismatch is churn-robust — but misses drop to 5.6%, because the sound schedule's drift allowance blows the sets up (the author's own cost row: 31 pairs/kick, 9.5 rebuilds/orbit at eps 1e-3). Wrong-or-bloated, never O(k): this *strengthens* the structural claim, but the 70–75% headline is specific to the low-churn regime and the dossier does not say so. (d) Rank arithmetic: zero misses by mean-λ rank alone needs k ≥ 81 (40% of the clump) — "watch-everyone" in disguise. (e) Bin-width check of the brute truth: adjacent-bin-only pairing is sound (bin 1.9e-4 ≈ 2ρ at r ≈ 1, so sub-ρ pairs cannot skip a bin); dt = 5e-5 gives ~4
4. **Novelty.** Not a redo. q-skin-bd86 (2 Oct) and b-encounter-skin-8bfa (7 Oct) are the *slack* skin; taleb-09b5's gold says "partner rank ≤ 4 along the orbit" without a coordinate; nothing in HISTORY (ends H0215), the board or the docs measures *which* orbital coordinate the train must rank in, or the belt rebuild storm, or the lever under concentration. This run kills the mean-λ implementation before it is built and extends taleb's rank evidence to churn (dist ≤ 4, θ ≤ 5 on both my seeds).
5. **Goal fit.** Board focus line 3 and the top scaling risk: the skin layer under concentration, ahead of `q-skin`/`b-encounter-skin`. PRINCIPLES: "A test that cannot fail is a control" — the synthetic one-ring probe could not fail on coordinate choice; the real path did. "Regimes are chosen by dimensionless numbers" (P4) — the spacing/amplitude trigger, now swept. "A failed expectation is not automatically a failed method: diagnose which one broke" (H0183) — exactly what the P3 split does.
6. **Why silver, not gold — the record, three faults.** (i) The cost table's phase evals/kick cells read "12k" and "20k"; the run's own JSONs say 119,629 and 203,712 — a 10× understatement, both cells flattering the phase skin. Corrected, the end-to-end counted-eval comparison is 183k vs 120k (1.5×), not 15×. (ii) `cost-fleet.jsonl`'s phase rows were produced by pre-fix code (my rerun: evals 119577 vs 119629, hits 3328 vs 3346, capped 13826 vs 12738) — the one file the shipped code cannot regenerate, and `author-final.md`'s "clean build from scratch reproduces" overstates. Claims unaffected (5.0 pairs, ~0.4 ms, ~1 rebuild/body/orbit all stand). (iii) The 146× headline composes the phase skin's marginal kick timing (background rebuilds excluded from µs; the fleet phase run drops the sea, 400 clump bodies only) against the metric skin's full scan+cert. The fine print discloses both exclusions and gives the honest decomposition (clump term 399→5 pairs, ~180k→~600 evals), but the headline number is the flattering composite. This is the exact class the taste log punishes ("numbers the shipped code cannot regenerate… a headline the log contradicts"), same as b-encounter-

**For gold (one step, no new physics):** regenerate `cost-fleet.jsonl` with the shipped code; correct the two eval cells; restate the cost ratio with background re-certification and the sea term counted on both sides (it survives: ~6–8× end-to-end by the run's own decomposition); report the churn dependence of the miss headline (70–75% at 1e-5, 5.6% at 1e-3 with bloated sets). My σ-sweep can be folded in as the trigger's evidence.

**What the author missed.** The churn dependence of the miss rate (the ranks are the robust invariant; the misses are not). The end-to-end accounting asymmetry: the metric skin's own background re-certification (every 20 orbits × 2516 pairs × 400 bodies) is never counted — counting it symmetrically would have *helped* the train and made the 146× unnecessary. The dilute "rank 0" evidence rested on 2 encounters (uniform-low); σ=0.2 gives 57 encounters and closes that hole. θ-rank max 5 means k=5 survives only via the either-direction coverage and tie extension — an unstated off-by-one. And a nit: the "2e ≈ 0.02" figure is the cap; the median pair sum is ~0.005 — the mechanism is unchanged, the constant is 4× off.

### 20261010-1302-taleb-bb88
Grade: silver

**Abstract.** Claim: the gold's "every real encounter within partner rank 4" is a circular-orbit scene property; on eccentric fleets, contact count and rank scale as √((1+e)/(1−e)) exactly. Reproduced bit-for-bit (36 runs, 173.6 s); the law is exact Kepler geometry and extrapolates: e = 0.99 gives 40.3–40.5 vs 40.5 predicted, 10× density gives 28.68 vs 28.7. A rank-4 window drops 39% of contacts at e = 0.9, and 72% on a 10× denser circular fleet — the gold's constant breaks even at e = 0. Adoption before wiring: size k by bunching × Poisson tail, gate the trigger on √((1+e)/(1−e)). Not gold: the pre-registered letters P1/H1/H2/NEG failed as written (disclosed numbers, reported as held), and the fix is argued, not measured.

`python3 probe.py /tmp/check_out.json` in a clean tree (patch.diff empty; self-contained folder): 36/36 runs **bit-for-bit identical** to `probe_out.json` on every field (pairs, enc/body, max/p999/mean rank, aphelion fractions), wall 173.6 s vs claimed ≈175 s, well under the memory cap. `summary.txt` and the dossier table match the JSON exactly. File order confirms predictions-first: predictions.md 13:10:28 → probe.py 13:15:03 → probe_out.json 13:17:59 (one run).

## Held-out and adversarial (mine, pre-registered before running)

- **e = 0.99** (beyond the sweep): enc/body 40.28/40.44/40.53 (seeds 11/12/13) vs 2.87·√199 = 40.48; max rank 32–36. The scaling law is exact 6× beyond the gold's regime.
- **Direct drop fraction at e = 0.9, k = 4**: 39.3/39.0/38.9% of unique pairs dropped. The dossier's "roughly a third" is correct (the author derived it; it is now measured). Rank 6 still drops 17%.
- **n = 30000, circular, same R**: enc/body 28.675 (pred 28.7), max rank 30, **72% of contacts beyond rank 4**. Confirms the fat-tail claim (ii) with e = 0: rank 4 is a scene property of n·R_enc, not a law.
- **K-doubling** at e = 0.9 seed 11: K = 480 gives counts and ranks bit-identical to K = 240. The author's sampling-adequacy control holds.
- **τ-order ≡ M-order** at n = 3000 (identical rank multisets): for a single-a fleet the proposed apsis-time keying changes the window's *size*, not the ordering.
- Independent derivation of the count law: |dP/dM| at apoapsis = a√((1−e)/(1+e)), so the contact window in mean anomaly is (R/a)·√((1+e)/(1−e)) and per-body contacts = 2Rn/(2πa)·√((1+e)/(1−e)) = 2.87·√((1+e)/(1−e)). Exact geometry (Kepler's second law), not a fit. The circular mean rank 1.74 also matches the Poisson-gap model (1.69): the instrument is sound.

## Predictions: substance held, letter did not

H3 held (19–21 vs 18–20). H1/H2 held exactly on enc/body (×2.000: 24.95, 5.72) but their letter ("max |rank| doubles") failed (15→25, 7→10). P1's letter ("circular max ≈ 3, reproduces the gold's ≤ 4") failed (measured 7). NEG's letter ("max ≈ 80+") failed (59–63). All four fail in one direction — the mean-reach formula was pre-registered against a max statistic — all numbers are disclosed in the evidence table, and the author's own fat-tails section gives the explanation; but the Predictions section reports them as "Held", and P1's fail is the run's own thesis wearing the gold's number. P3 was falsified and reported as falsified (honest).

## Novelty

No H entry (latest is H0215) or doc measures eccentricity in the phase-neighbour certificate; `docs/law.md`'s encounters text has no rank/fleet clause yet (HANDOFF "Headed next" #5 — the certificate is unwired). Closest priors are different mechanisms: q-candidate-degree's "Wide misses 23% at e 0.7–0.9" (element-based tier, dilute belts) and B16's √((1+β)/(1−β)) (aberration, not arc density). Novel and correctly cited against the gold (board, 6 October).

## Goal fit

Board's top scaling risk (candidate work must track real encounters). This bounds an adopted gold before its one-way door and gives the sizing law; PRINCIPLES #19 ("a fix signals the wrong representation"), #32 (Kepler's second law as the symmetry to borrow), and the lens's own fat-tail rule. The author honestly flags "no 10× cost move".

## What the author missed

1. **The "overpays 19× at perihelion" line is misleading as a cost claim.** In a standing fleet an aphelion-sized window has zero structural waste: it contains exactly the real contacts (2k = 12.5 candidates vs enc/body = 12.48 at e = 0.9). The 19× exists only for an epoch-local implementation that re-checks windows every frame; the deliverable is the sizing law, not the overpay.
2. The gold's own scene was not reproduced (family B circular max rank 12–15, not ≤ 4); the run bounds the constant's domain but cannot confirm what the gold measured. The encounters crate could pin it.
3. `run.log` is empty while the dossier says machine state is "recorded in run log".
4. Family B enc/body grows 30% at e = 0.9 (2.4 → 3.1) though the dossier calls the drift regime "e-robust" — true for rank (the certificate's quantity); a count-level reader would be misled.
5. Family A contact locus "aphelion_frac ≈ 0.57–0.68" sits in the JSON but not the dossier; the pile-up is the mechanism and deserves the number.

## The one experiment to gold

Implement the re-sized window in this harness — k = ⌈bunching √((1+e)/(1−e)) × Poisson-clump tail × drift reach⌉ (equivalently the uniform apsis-time window R/v_apo) — with pre-registered letters that distinguish max from mean, and show zero missed contacts at candidate cost ∝ real contacts across e ∈ {0, 0.6, 0.9, 0.99} × density {3000, 30000} plus family B. That converts the argued fix into a measured one and cleans the prediction record; the integrator can then adopt it as the certificate's sizing rule in one step.

### 20261010-1407-inversion-5c2a
Grade: gold

**Abstract.** The author inverts the adopted co-orbital gold (20261006-0346-taleb-09b5): the phase-neighbour certificate silently assumes one cold population. Reproduced bit for bit from the patch: two crossing fleets (Δa/a = 2e-4 per fleet, σ_e = 0.04) drop 82–84% of contacts at every practical window (43.7% cross-fleet are structurally invisible to any per-group rank; ceiling 56.3%); 99% coverage needs 519 certs/encounter = 14× the quadratic tier. Retrograde: 96.4% cross, 1–3.6% coverage, 15.8× denser than prograde (I measured 4564 vs 71,923). Adopt within one step: scope the certificate to cold single groups with an e-spread gate, group-envelope pairwise tier between groups, and add two-fleet/warm-fleet gate scenes to the queued build `b-coorbital-cert.md`.

**Reasons.**
1. **Reproduction: exact.** Applied `work/patch.diff` to the pristine tree, built offline, reran all three scenes. CTRL: enc=2093, pairs=44850, steps=15,948,922, fine=180,897 — identical to `artifacts/evidence/opus-encounters-20260930/verify.jsonl` line 16 (`truth_enc:2093, radial_pairs:44850, truth_steps:15948922, truth_fine:180897`), and the spec+seed match `main.rs`'s `coorbital` (s+9 = 20261010). FLEET2: 4623 enc, cross 43.7%, per-group 15.94–17.59% at W=1–10, merged 99.00% at 519.1 certs/enc. RETRO: 71,923 enc, cross 96.4%, per-group 3.60% ceiling, 1.05–1.21% at W=1–10, merged 7.51% at 33.4 certs/enc. Every dossier number regenerates.
2. **Instrument: independently validated.** The mirrored RETRO march is new code. I re-derived 37 sampled pairs (30 cross, 7 intra; 102 events) with my own numpy Kepler solver and two-stage scan: all 102 events reproduced (t within 5e-4, d within 1e-5), zero unmatched, zero spurious minima. The inlined `safe_step` omits the crate's step-growth polish (conservative only). Dup=0 and max 99 events/pair over 50 orbits confirm distinct events — the 5 October lesson (count distinct kicks) is respected.
3. **Predictions: pre-registered, mostly held, misses disclosed.** File order (predictions.md 10m-old, ctrl 7m, fleet2/retro 6m, dossier 1m) is consistent with writing before the decisive run. Held: CTRL 2093 (predicted 1500–3000) at 100% rank@event; FLEET2 enc in range; merged ≤10%-order at W=1 (15.6%); RETRO merged ≤5% at W=1 (1.28%). Missed, honestly reported: cross ≥95% (measured 43.7%) — the intra e-crossing layer was a genuine surprise that strengthens the finding. The pre-registered kill criterion (coverage <99% at every ≤200 certs/enc window) is met decisively: ≤26 certs/enc buys ≤17.6%.
4. **My adversarial cases (three, all confirm).** (a) Seed 20261013: cross 44.1%, 16.6–17.0% at W=1–10, 99% at 537 certs/enc — structural, not seed luck. (b) warm1, a *single* warm fleet (n=600, one group): 22.2% coverage at W=1, 99.4% only at 428 certs/enc — isolates layer 2 from cross-group effects, so the author's proposed e-gate is necessary even inside one group; this closes the "just scope per-group" escape. (c) pro12 (retro's seed, unmirrored): 4564 enc vs 71,923 = 15.76×, matching the claimed 15.5× head-on density.
5. **Novelty.** No H entry or doc attacks the co-orbital certificate's domain: HISTORY has nothing on multi-population, retrograde or e-spread rank stability (searched co-orbital/fleet/formation/concentration/retrograde). q-candidate-degree's known high-e miss (23% at e 0.7–0.9) is a different mechanism (window tightening, not phase rank). The attacked build is queued, not landed — this is the pre-freeze red-team the board requires ("Before any freeze, one GLM red-team and the cheapest falsifying probe must have run").
6. **Goal fit.** Premise shown wrong with the crate's own truth: "every real encounter lies within partner rank 4" is a property of cold single populations, not of concentration, and "replaces the quadratic tier" fails on the game's flagship scene (fleet meets fleet) with silent 82–100% contact loss — the worst failure mode, no error signal. Respects PRINCIPLES: "a failed expectation is not automatically a failed method" (§9, H0183) — the dossier kills the configuration, not phase rank, and names the scoping fix. Cost of adoption: one sentence in the build spec's test list plus the per-group e-gate and group-envelope tier; the fix is prescribed, not built (a build run's job).

**What the author missed.**
- The strongest isolation of layer 2 — a single warm fleet with no second group — was not run; my warm1 supplies it (and makes the finding stronger than written: even one warm group has no certificate at practical cost, so the e-gate is load-bearing, not the grouping).
- The 10⁶ extrapolation constant is off ~4×: rank 4 breaks when 4e ≳ 4 spacings, i.e. e > TAU/n ≈ 6.3e-6, not 1.5e-6. Order of magnitude unaffected.
- The retro "200×" figure is extrapolated to W ≈ 3e-3 orbits (500 certs/enc vs 2.4 pairs/enc), not measured at that window; measured at W = 0.05 the ratio is 33.4/2.4 ≈ 14× at 7.5% coverage.
- 3D mutual inclination untested (planar crate; the author flags it).
- The residual ambiguity in the spec's "beside the existing tiers" vs the gold's "replaces": if the two-tier envelope logic already covers cross-group pairs by construction, the one wrong word is "replaces" — but the measured warm-intra layer keeps the finding load-bearing either way.

**For silver, the one experiment** would have been the warm single fleet; I ran it and it holds, which is why this is gold and not one-experiment-away.

### 20261010-1407-second-20261010-1302-taleb-bb88-b612
Grade: gold

**Abstract.** Claim: the co-orbital certificate sized by apsis-time keying with W′ = (R+X)/v_apo + 3(δa/a)(T+P) finds every contact at cost 1.003–1.017× contacts (formation regime), and bb88's drift-only window W is falsified. Reproduced bit-for-bit in a clean tree (both JSONs and analysis.txt identical on every shared field; 15 W-misses, all apoapsis differential conjunctions; cost/enc 1.003–1.017; rank-4 drops 1.1→98%). My attacks (correlated spreads — the author's admitted gap —, 1000× wider spreads, bimodal max-drift a, e=0.995 with a robust solver) all give zero W′-misses; e=0.995 initially "failed" only because the probe's Kepler solver diverges there (residual 8e15; exact at e≤0.99). Cost to adopt: one formula replacing the rank-4 constant, sort amortized to zero; k = ⌈λ+√(2λ ln n)⌉.

**Reasons.**

1. **Reproduction (exact).** `python3 cert_probe.py cert_out.json` (1005 s wall on this shared runner vs the author's 800.6 s) + `bonly` + `analyze.py`: `my_analysis.txt` is byte-identical to `analysis.txt`; pair counts identical in both logs; `cert_out_b.json` identical; `cert_out.json` identical on every pre-existing field (my copy of the final script also stores the W′ fields — `misses_c = 0` everywhere, which upgrades the author's A-family inference `dtau_max ≤ W′` (max ratio 0.9973) to direct measurement). Total miss(W) = 15 = 8 (A 0.99/30k) + 5 (B 0.99) + 2 (B30), exactly as reported; K-control reproduced (60734→60800 pairs, +0.109%, metrics unchanged).

2. **Predictions discipline.** mtime/log order verifies the story: author-prompt 14:07, pilot 14:18–14:22 (reproduces bb88's 18850 pairs), grid 14:20–14:37, addendum 14:47, B re-run 14:52, analysis 14:56. Letters name their statistic (max vs mean — the prior run's failure), kill criteria are pre-registered, and the negative control (no-drift W0) fails as a control must (69–98% misses). Held: Z1′, CA (the core), TA/TA′, CB′, MB′, all 8 Poisson-max range letters, KCTRL, and held-out B30. Failed and disclosed, none load-bearing: Z1 (the run's own finding), MA sub-letter (14/24), KA (20/24 safe; 24/24 with 1.6× slack), NEG (0.69 vs 0.90 — mechanism still confirmed), two G corners, B-enc at 0.99. No failed letter is reported as held.

3. **Attack (5 cases, all against W′ zero-miss).** (a) Correlated element spreads (one uniform driving δa, δe, δϖ — exactly the orientation the dossier admits untested): zero misses at e=0.9 and 0.99 formation and in the drift regime, where correlation even produced a fresh miss under the old W that W′ closed. (b) Spreads 1000× wider (δe = 1e-3, then δe and δϖ together): old W misses 1656–4454 pairs, W′ zero — the X term scales as derived, it is not a tuned patch. (c) Bimodal δa (every cross-group pair at max drift 2δa): zero misses, cost/enc unchanged (1.006–1.008). (d) e=0.995 beyond the grid: 3106 apparent misses with `req_k` saturated at n/2 — diagnosed as instrument, not window: the probe's fixed Newton Kepler solver diverges at e≥0.995 (residual up to 8e15 near M≈π; machine-exact 8.9e-16 at every grid e≤0.99). Re-running the same fleets with a damped Danby-start solver: zero W′-misses, tightness 0.9965, cost/enc′ 1.007, req_k ≤ pred_k — W′ extends one corner past what was measured.

4. **Novelty.** No HISTORY.md or docs entry covers apsis-time keying, W′/X, or their measurement. The base certificate is gold 20261006-0346 (rank-4, circular); the W window was bb88's argued, unmeasured proposal (same-day lab run, absent from HISTORY). What is new here: the measured falsification of W with a diagnosed mechanism, the closed-form correction, the Poisson-max sizing law, and the grid-wide rank-4 drop quantification (39–98% at e≥0.9).

5. **Goal fit.** The board's top scaling risk is "candidate work must track real encounters"; the co-orbital certificate is in the build queue, and without an eccentric rule it drops 9–98% of contacts at e≥0.6 — this run supplies the measured rule the queue item needs, adoptable in one step (one sort, frozen order, one formula; gate on the bunching number). It satisfies the gold clause "shows that a premise is wrong" on a live design premise. PRINCIPLES #19: "if you find yourself fixing things that's oftentimes a signal that it is the wrong representation" — mean anomaly was the wrong coordinate; apsis time makes the order exactly frozen and the window uniform. #21: W was rough, broke at the 1e-6 level, and the refinement is one closed-form term, not a retune.

**What the author missed.**
- The probe's Kepler solver (30 fixed Newton iterations from E = M + e·sin M) diverges at e ≥ 0.995 — an undocumented instrument boundary. The grid stayed safely inside it (verified exact at 0.99), and my robust-solver rerun shows W′ holds at 0.995 anyway, but the dossier should state the domain.
- The drift-regime cost story (T_reeval as the policy knob) is argued, not measured across re-evaluation intervals; cost/enc 4–9× there is honestly disclosed but the knob's tradeoff is unmeasured.
- Truth is K-epoch sampled, not per-pair analytic minima; KCTRL bounds pair drift at 0.1%, but a violating pair in an unsampled gap can only be caught by the analytic machinery the author himself points to (continued fractions in the encounters crate).
- Two prose defects, neither load-bearing: the addendum's sentence "A had zero misses with W" is false (A(0.99,30k) had 8 — the saved-tightness bound, and my direct recomputation, settle the conclusion it was arguing for), and the claim line's "falsified at the 1.7e-6 level" matches no stated aggregate (the per-config numbers 4.4e-7 / 2.1e-4 / 4.3e-6 are all correct).
- `cert_probe.py` was edited after the grid (W′ added at 14:49); consistent with the disclosed timeline and immaterial since the full grid re-runs deterministically, but the author could have said so explicitly.

### 20261010-1706-inversion-3775
Grade: gold

**Abstract.** Claim: the co-orbital gold's premise fails on breakup clouds — an exact null plane in
Binet space, so the cone tier retains 99.99999% of pairs (37 TiB at 10⁶ fragments), element
triggers can't see it, phase neighbours churn (rank-4 misses 46% at N=4000, 97% in the blob),
while a shared-focus epoch-stream sort covers at-P encounters at ~3 checks each, flat in N.
Reproduced bit-identically; my adversarial cases (σ=0.05, e≈0.5–0.67 eccentric parents, tighter
belt) strengthened it (retention exactly 100%, rank-4 misses 75–92%). Gain: deletes quadratic
pair state for plane populations and re-routes the queued b-coorbital-cert build. Adoption:
focus-epoch streams plus a cone-probe trigger; the at-Q residue (14–39%) stays open.

1. **Reproduction.** `python3 breakup.py` in a clean copy: exit 0, 11.4 s, <200 MB; results.json bit-identical to the stored one except `load` and `runtime_s`. Every table number in dossier.md matches results.json exactly (I checked all 17 rows, including 7,997,999/7,998,000; 3744/8219 = 45.6%; churn 0.99/0.91/0.35; work/encounter 3.0/3.0/3.0/4.1/2.9; Q-shares 14.5/27.3/60.4/37.0/38.9%). The 37 TiB and 14.5–139 core-days rows follow arithmetically from 5×10¹¹ pairs at 80 B/pair and 2.5–24 µs/pair, and mirror the gold's own 40 TB accounting.

2. **Prediction record.** predictions.md (17:18:19) predates the final breakup.py (17:28:59) and results.json (17:31:57); patch.diff is empty (no repo edits). Held: P2 (plane residual 3.3e-16), P4 (zero at-P misses, flat ~3 checks/encounter), P3's formation control (67,796 encounters, 0 misses, max rank 2 — the gold's scene reproduced) and adjacency (median 1, max 6). Missed and honestly reported: P1's belt bound (16.8% vs <10%), P3's mixed-age magnitude (46% vs >80%; the blob phase hit 96.6%), P5 (cloud is 13–57× tighter than belt, not belt-like), P6 (0.14–0.39×, not within 2). No kill criterion triggered. The honest misses cut against tuning: a leaked prediction file would have them right. The physics correction of v1→v2 (d_min ≈ v0·|Δt|, churn not rank growth) is disclosed inline and is itself part of the result.

3. **Adversarial cases (mine, /tmp/chk/adv.py and follow-up).**
   - σ=0.05 (50× the author's dispersion), N=2000: cone retention exactly 1,999,000/1,999,000; plane residual 4.4e-16; rank-4 misses 92%; epoch stream 2.65 checks/encounter. The Kepler validation of the analytic window degrades to 33% max rel err on d (vs 0.4% near-circular) — still ≪ b, so encounter membership flips only in a thin band at the threshold.
   - Bound eccentric parents (breakup at periapsis of e=0.2, v=1.22; at apoapsis of e=0.5, v=0.577; fragments e≈0.5 and 0.67): retention exactly 100%, plane residual 4–9e-16, epoch stream 2.9–3.0 checks/encounter with v-scaled window, rank-4 misses 75–84%. The author's caveat (ii) resolves in favour of the claim: the mechanism is exact away from the tested regime and the certificate failure worsens.
   - Tighter belt (awidth=0.05): retention 55.0% — the dossier's parenthetical "55%" is real, though not regenerable from breakup.py as shipped (see missed).
   - 3D (argued, not run): all fragment planes share only the line P–primary, so pairs share exactly P; second crossings are codimension-2. Retention-100% holds a fortiori and the at-P stream covers ~all encounters — the fix is stronger in the 3D the game actually runs.
   - Controls on both sides hold: formation (the gold's scene) 0 misses; belt 16.8% (not ~100%, so the kill criterion for the inversion did not fire).

4. **Novelty.** docs/law.md (encounters, 30 September) documents the Binet cone as the crossing condition — known. New here: the null-plane corollary (a single-point population lies on a plane whose normal is null, so the cone retains everything — the filter is structurally blind to the game's most common concentrated scene), the phase-churn kill of the rank-4 certificate outside formations, the cone-probe trigger, and the epoch-stream-at-focus certificate. No HISTORY entry or doc mentions breakup clouds (grep over docs/ and lab/: only this run). It attacks the real queued spec (lab/lenses/b-coorbital-cert.md: rank-4 at O(n·k) with a dimensionless concentration trigger), not a strawman — the brief's test scenes (gold scenes + dense ring) contain no breakup cloud, exactly the gap this run exposes.

5. **Goal fit.** The board's top scaling risk (5 October): candidate pairs per body grow with N; candidate work must track real encounters. This run shows the cone tier cannot reduce candidates for plane populations (100% retention, exact) and that real at-P work is trackable at 3 checks/encounter — 10⁶ fragments go from 5×10¹¹ pair-state to O(N log N) sorts per fraction of an orbit. PRINCIPLES 32 ("under the right representation many symmetries can appear"): the null plane is the symmetry, found by changing the question; principle 33: the cloud resolves at its focus, not in pairwise space. "A failed expectation is not a failed method": the run kills the certificate's domain, not the encounters design — and hands it the focus representation.

**What the author missed.**
- The 55% tighter-belt number is not emitted by breakup.py; "both reported" overstates (results.json holds only 16.8%). I regenerated it (55.0% at awidth=0.05), so the number stands, but the shipped code does not regenerate it — the exact defect that sank earlier silvers.
- "0 misses at every N" for the epoch stream is structural (the truth is the same stream); its independent validation is P7 only, and the window error's growth with dispersion/eccentricity (0.4% → 33%) was unmeasured until I ran it.
- "Misses 46% of real encounters" should read "of at-P encounters"; over all encounters (including at-Q) it is ≥ ~33% at N=4000. Direction unaffected.
- The at-Q stream's possible concentration (θ_Q = 2·atan2(ΔW,ΔV), noted then dropped) is the obvious next probe: if Q directions cluster for breakup clouds, a second focus stream closes most of the 14–39% residue and the certificate becomes complete; the author measured the share but not the clustering.
- 3D was flagged but not run; the analytic argument (and my reading of it) says it strengthens both the kill and the fix.

### 20261010-2052-inversion-9a33
Grade: silver

**Abstract.** Claim: the adopted co-orbital phase-neighbour certificate's premise (gold taleb-09b5: "every real encounter within partner rank 4") holds only for zero-spread formations — burn-footprint spreads (r8 v4 magnitudes) put 85–99% of encounters at rank ≫ 4 (law k ≈ 6σ_e·n/Δφ), and a two-group intercept puts every cross-fleet event near rank n/2. Reproduced: 4 scenes byte-identical, B1e-2/C bit-exact; B3e-3 identical in every discrete field. My attacks strengthen it: the gold's own fleet magnitudes (e~Rayleigh(0.001), ϖ±0.1, a-hw 1e-5) at n=800/Δφ=0.2 miss 59.8% at k=4 (max rank 34); aligned apsides still miss 77%; seed 2 holds; the truth net leaks nothing. But the in-flight build (wt/cx-b-coorbital-cert, landed 13:37 UTC, 7 h before this run) already derives spread-scaled k ("NEVER an assumed rank of four") with a concentration fallback, so the "silent miss" framing does not apply to the artifact that exists.

**Reproduction.** Clean copy of `probe.py`, fixed seed 7, same machine/interpreter (numpy 1.26.4, scipy 1.11.4): scenes A, B1e-3, B1e-2, C regenerate byte-identically; B3e-3 regenerates every discrete field (events 339, miss 0.9705, max rank 94, p99 69.48, transient records 9,546,992) — see integrity notes for the one non-regenerating float. Timings consistent (B1e-2 + C in 103 s shared-runner). All commands ≤ 90 s as stated.

**Predictions.** `predictions.md` (mtime 20:59:53) precedes every stored output (first JSON 21:15:00) and the final `probe.py` (21:14:32); no post-output code edits. Control on both sides, as required. Held: control exact (316 ≈ 320 analytic, max rank 4); scaling law within ~35% (23/68/228 predicted vs 31/94/226); intercept (100% of cross events missed, rank 413 ≈ n/2); azimuth sort ~0 (0–0.94%). Missed and reported: B1e-3 miss fraction predicted "roughly half", measured 85% — the miss direction favors the finding.

**My attacks (all run, `adv.py` in /tmp/check-repro).**
1. Gold's own regime, not the author's: e~Rayleigh(0.001), ϖ ∈ ±0.1, a half-width 1e-5 (taleb-09b5's exact fleet parameters), n=800, Δφ=0.2 → **59.8% miss at k=4, max rank 34** (law predicts 30). The finding is not a strawman of the magnitudes.
2. Aligned apsides (σ_e=3e-3, all ϖ=0): **77% miss, max rank 63**. Random ϖ is not essential; element spread alone breaks rank 4.
3. Second seed (B1e-3, seed 11): 87.9% miss, max rank 31 — matches seed 7.
4. Truth-net validity: 1,500 random non-candidate pairs of B1e-2 dense-scanned at 8,000 samples/orbit — minimum distance 0.00717 ≥ coarse threshold 0.00714 and 71×ρ; the 1,200-sample net cannot be leaking encounters. The instrument lesson from the gold (λ-binned brute force) is not repeated here: this truth has no tier logic.

**Novelty.** The gold's dossier pre-registered exactly this boundary as unproven ("e-spread ≫ ρ could break phase-order = distance-order (rank inflation)"; "it needs a proof that co-orbital sub-ρ contact implies rank ≤ k under stated invariants (radial spread ≲ ρ·c), which I did not write"). This run is the first measurement of that boundary, with a usable law (k ≈ 6σ_e·n/Δφ; rank 4 needs e below one phase spacing — verified by me on two scenes the author never ran), the intercept geometry, and the azimuth alternative. Not previously measured anywhere I can find (docs/HISTORY.md has no co-orbital entry; taste log 6 October is the gold's adoption).

**Why silver, not gold.** The headline says the certificate "silently assumes a zero-spread formation" and "the miss is silent" for build `b-coorbital-cert` — but the build landed at 13:37 UTC on wt/cx-b-coorbital-cert, seven hours before this run, in this same checkout the author worked in. Its `phase.rs` header: "k is the actual occupancy of a conservative phase window, NEVER an assumed rank of four. Gold measured distance rank at the contact, not phase rank at setup; radial scatter and overtakes can make those different." Its derived window already contains the equation-of-centre term (~2e per body: for scene C's e=0.05, reach ≈ 0.3 > the 0.1997 intercept gap — the author's own π−2m derivation, arrived at independently), plus a fallback at concentration ≥ ½, and its evidence shows measured max_k of 8–162 with zero misses on jam scenes. The dossier's "the trigger is not public: it lives on the gold run's branch" is wrong — the branch is local and readable. So the impact claim ("bounds the domain before the build lands"; otherwise "the domain boundary would ship unmeasured") attacks a specification, not the shipped artifact. What survives against the build — and 

**Integrity notes.** (i) The dossier claims `vrel_max_seen` is "in the JSONs" — no such field exists; the check computes the bound and discards it (`probe.py:224-232`). I verified by hand the bound is safe (worst 2·|v| = 2.05 < 2.5 for e ≤ 0.05). (ii) The dossier says C's `clump_rms_radius` is "0.058 both" — its own JSON says 0.112 (still ≪ a belt's ~0.7, so the density point survives with a wrong number). (iii) `probe-B3e-3.json`'s `clump_rms_radius` does not regenerate (stored …73589904215, code produces …73889904215, 3×10⁻¹⁰; recomputed stable across three trials). Disclosure: while reproducing I accidentally overwrote probe-A/B1e-3/B3e-3.json and restored A and B1e-3 byte-identically (verified); B3e-3 was restored from my verbatim capture of the original (size 361 B matches the recorded original, mtime restored), which is how the non-regenerating float was caught. The field is computed before the pipeline and affects no other number. (iv) run.log is empty; timings cannot be cross-checked from it.

**The one experiment for gold.** Run scenes A/B1e-3/B3e-3/C through the actual build (`wt/cx-b-coorbital-cert`, `crates/encounters/src/phase.rs`, truth harness in `tests/phase_truth.rs`) and report, per scene: misses/false (soundness) and measured max_k and candidate work (cost). If the build misses, this becomes an urgent gold; if it holds, the finding collapses to the cost degeneration k → n at σ_e ≳ Δφ/12 — still adoptable (it says when the phase tier must hand back to the cone), plus the trigger must be checked against random-ϖ fleets, which its current test scenes lack.

**What the author missed.** The build branch, sitting in the same checkout, landed seven hours before the run and already implements the proposed corrections (i) and (ii); attacking the gold's one-line premise instead of the living artifact cost the run its gold. The author also never tested aligned-ϖ spread (my case 2: it breaks rank 4 without random apsides, which is the stronger, simpler claim), never varied the seed, and never validated the truth net's mesh (my case 4). The "0.058 both" and `vrel_max_seen` slips are exactly the "headline the log contradicts" class the lab's own brief warns about — small, but they cost trust in a run whose numbers are otherwise impeccable.

### 20261011-0224-taleb-236b
Grade: gold

**Abstract.** The claim stands: the adopted rank-4 phase-neighbour certificate (gold taleb-09b5, queued as `b-coorbital-cert`) silently drops 95–100% of contacts in co-orbital families with e-vector dispersion — encounters sit at crossing-geometry offsets (medians 0.24n–0.54n). Reproduced bit-identically at R=3e-5/1e-4/3e-4, and re-derived with an independent propagator, contact finder and rank instrument (S1 exact: 80 contacts, 2.5% at rank ≤4, median 869/1600; S4: 928 vs 871 contacts, 3.4%, median 72.5). Generalizes to a fresh seed (0.0%, median 773) and to the trigger boundary (cone 0.61: 4.9%); the shear control holds at 10× horizon (max rank 3). Gain: deletes a wrong invariant before two lanes freeze it. Cost: amend `b-coorbital-cert` — offset windows {ΔM*} on the same ordering, Binet-cone trigger, e-dispersed truth scenes.

**Reasons.**

1. **Reproduction.** `python3 probe.py [R]` in a clean copy: all three metrics JSONs identical to the author's except timing (deterministic seed). 26 s at R=1e-4, well under memory budget.
2. **Independence (the lens's own invitation).** I re-derived S1 and S4 on the author's exact fleets (rng-replay verified: probe's own finder on my dump returns 80/0.025/869) with my own Kepler solver (perifocal + rotation, not true-anomaly arctan), my own finder (uniform dense sampling with a relative-speed capture margin, per-pair global min, one dense zoom — no shared code with the coarse/refine cascade), and my own rank ordering. S1 matches exactly. S4 matches structurally; my denser finder finds 928 contacts vs 871 (the author's coarse capture at 16 steps/period loses pairs with v_rel ≳ 0.03; ~6% undercount, frac/median unchanged, conclusion unaffected — if anything strengthened).
3. **Adversarial cases (mine).** (a) S1 construction at seed 777: 88 contacts, 0.0% at rank ≤4, median 773 — not a tuned seed. (b) Boundary trigger: n=300, σ_a=2e-4, e pinned 0.01, σ_ϖ=0.03 (cone fraction 0.61, between the regimes): 1035 contacts, 4.9% at rank ≤4, median 46 — the failure persists mid-cone. (c) S0 at 60 periods (10× horizon, full lapping): 5371 contacts, 100% at rank ≤4, max rank 3 — the certificate's home regime is robust; the probe does not strawman it.
4. **Ordering representation.** A builder could object that the certificate ranks by mean longitude (λ=M+ϖ), not mean anomaly. At a crossing λ_i−λ_j = Δϖ − 2(e_i sinΔ_i − e_j sinΔ_j) ≈ Δϖ — same order of magnitude as the mean-anomaly offset, so the non-locality is insensitive to the ordering choice; only the shear regime (same ellipse) is rank-local in either. No strawman by ordering.
5. **Predictions.** Timing verified by file mtimes: predictions.md 02:38:26 precedes all metrics (02:39:01–02:40:08). P1, P4, P5, P6 held. P2 and P3's quantitative sub-bounds missed (2.5% vs ≤1%; median 869 vs band [610,830]; cross median 406 vs 555; within-fleet 184 vs ≤60) — every miss disclosed in the dossier and none load-bearing: all crossing-regime measurements sit at 0–3.9% rank ≤4 across three R and two independent finders. This is the honest-reporting behaviour the rubric rewards, unlike the 1 October red-team.
6. **Novelty.** No entry in docs/HISTORY.md or the board covers e-vector dispersion; the build lens `lab/lenses/b-coorbital-cert.md` states "every encounter lies within partner rank 4 along the orbit" and tests only "the gold run's scenes and a dense ring" — shear-regime scenes. The gap was untested before this probe.
7. **Goal fit and PRINCIPLES.** Board's top scaling risk ("candidate work must track real encounters") and the pre-freeze rule ("Before any freeze, one GLM red-team and the cheapest falsifying probe must have run" — AGENTS). It shows a premise of an adopted gold is wrong (#9: kills the configuration, not the method — the phase ordering survives, the rank window does not), via the cheapest possible probe (26 s). Adoption is one step: amend the build lens before it runs.

**What the author missed.**

- The conjunction side-claim ("59 conjunction pairs in S4 all miss by 0.02–0.33") does not reproduce under the natural definition (pairs whose ΔM crosses 0): I count 10,077 such pairs with misses 1.04e-4 to 0.54. The proposition it supports survives — the smallest conjunction miss (1.04e-4) still exceeds R=1e-4, so no conjunction produces a contact — but the stated numbers are unverifiable (no script shipped for them) and the true conjunction-miss floor is 300× smaller than claimed, which is exactly why S4 keeps a ~3% rank-local tail.
- The trigger is presented too sharply ("0.00 vs ~1 separates the regimes exactly"). My boundary case (cone 0.61) still drops 95% of contacts beyond rank 4, so cone fraction cannot gate rank-4 vs pairwise; the generalized offset windows must cover the whole cone>0 regime. The build lane should know this before choosing a threshold.
- The S4 truth undercounts ~6% (871 vs 928); harmless here, but the coarse capture condition (r_coarse ≥ R + v_rel·dt/2) should be stated in the dossier for future users of the finder.
- The precession argument (offsets smear but conjunctions stay dead while ϖ differs) is asserted, not measured — the author flags the offset-window cost under precession as the next run, which is right.
- Minor: the random-pair baseline is labelled "~n/6" but measures 0.29n (= 1−1/√2, as theory gives for uniform pairs) — the control still passes in the needed direction; `queue-sol.txt` is cited but does not exist in this tree (queue.txt does); probe.py was saved 7 s after predictions.md (scenario sizes match predictions; appears cosmetic, noted for the record).

### 20261011-0324-inversion-0981

### 20261011-0324-second-20261011-0224-taleb-236b-55a8
Grade: gold

**Abstract.** The claim stands: the adopted rank-4 phase-neighbour certificate (gold taleb-09b5, queued as `b-coorbital-cert`) silently drops 95–100% of contacts in co-orbital families with e-vector dispersion — encounters sit at crossing-geometry offsets (medians 0.24n–0.54n). Reproduced bit-identically at R=3e-5/1e-4/3e-4, and re-derived with an independent propagator, contact finder and rank instrument (S1 exact: 80 contacts, 2.5% at rank ≤4, median 869/1600; S4: 928 vs 871 contacts, 3.4%, median 72.5). Generalizes to a fresh seed (0.0%, median 773) and to the trigger boundary (cone 0.61: 4.9%); the shear control holds at 10× horizon (max rank 3). Gain: deletes a wrong invariant before two lanes freeze it. Cost: amend `b-coorbital-cert` — offset windows {ΔM*} on the same ordering, Binet-cone trigger, e-dispersed truth scenes.

**Reasons.**

1. **Reproduction.** `python3 probe.py [R]` in a clean copy: all three metrics JSONs identical to the author's except timing (deterministic seed). 26 s at R=1e-4, well under memory budget.
2. **Independence (the lens's own invitation).** I re-derived S1 and S4 on the author's exact fleets (rng-replay verified: probe's own finder on my dump returns 80/0.025/869) with my own Kepler solver (perifocal + rotation, not true-anomaly arctan), my own finder (uniform dense sampling with a relative-speed capture margin, per-pair global min, one dense zoom — no shared code with the coarse/refine cascade), and my own rank ordering. S1 matches exactly. S4 matches structurally; my denser finder finds 928 contacts vs 871 (the author's coarse capture at 16 steps/period loses pairs with v_rel ≳ 0.03; ~6% undercount, frac/median unchanged, conclusion unaffected — if anything strengthened).
3. **Adversarial cases (mine).** (a) S1 construction at seed 777: 88 contacts, 0.0% at rank ≤4, median 773 — not a tuned seed. (b) Boundary trigger: n=300, σ_a=2e-4, e pinned 0.01, σ_ϖ=0.03 (cone fraction 0.61, between the regimes): 1035 contacts, 4.9% at rank ≤4, median 46 — the failure persists mid-cone. (c) S0 at 60 periods (10× horizon, full lapping): 5371 contacts, 100% at rank ≤4, max rank 3 — the certificate's home regime is robust; the probe does not strawman it.
4. **Ordering representation.** A builder could object that the certificate ranks by mean longitude (λ=M+ϖ), not mean anomaly. At a crossing λ_i−λ_j = Δϖ − 2(e_i sinΔ_i − e_j sinΔ_j) ≈ Δϖ — same order of magnitude as the mean-anomaly offset, so the non-locality is insensitive to the ordering choice; only the shear regime (same ellipse) is rank-local in either. No strawman by ordering.
5. **Predictions.** Timing verified by file mtimes: predictions.md 02:38:26 precedes all metrics (02:39:01–02:40:08). P1, P4, P5, P6 held. P2 and P3's quantitative sub-bounds missed (2.5% vs ≤1%; median 869 vs band [610,830]; cross median 406 vs 555; within-fleet 184 vs ≤60) — every miss disclosed in the dossier and none load-bearing: all crossing-regime measurements sit at 0–3.9% rank ≤4 across three R and two independent finders. This is the honest-reporting behaviour the rubric rewards, unlike the 1 October red-team.
6. **Novelty.** No entry in docs/HISTORY.md or the board covers e-vector dispersion; the build lens `lab/lenses/b-coorbital-cert.md` states "every encounter lies within partner rank 4 along the orbit" and tests only "the gold run's scenes and a dense ring" — shear-regime scenes. The gap was untested before this probe.
7. **Goal fit and PRINCIPLES.** Board's top scaling risk ("candidate work must track real encounters") and the pre-freeze rule ("Before any freeze, one GLM red-team and the cheapest falsifying probe must have run" — AGENTS). It shows a premise of an adopted gold is wrong (#9: kills the configuration, not the method — the phase ordering survives, the rank window does not), via the cheapest possible probe (26 s). Adoption is one step: amend the build lens before it runs.

**What the author missed.**

- The conjunction side-claim ("59 conjunction pairs in S4 all miss by 0.02–0.33") does not reproduce under the natural definition (pairs whose ΔM crosses 0): I count 10,077 such pairs with misses 1.04e-4 to 0.54. The proposition it supports survives — the smallest conjunction miss (1.04e-4) still exceeds R=1e-4, so no conjunction produces a contact — but the stated numbers are unverifiable (no script shipped for them) and the true conjunction-miss floor is 300× smaller than claimed, which is exactly why S4 keeps a ~3% rank-local tail.
- The trigger is presented too sharply ("0.00 vs ~1 separates the regimes exactly"). My boundary case (cone 0.61) still drops 95% of contacts beyond rank 4, so cone fraction cannot gate rank-4 vs pairwise; the generalized offset windows must cover the whole cone>0 regime. The build lane should know this before choosing a threshold.
- The S4 truth undercounts ~6% (871 vs 928); harmless here, but the coarse capture condition (r_coarse ≥ R + v_rel·dt/2) should be stated in the dossier for future users of the finder.
- The precession argument (offsets smear but conjunctions stay dead while ϖ differs) is asserted, not measured — the author flags the offset-window cost under precession as the next run, which is right.
- Minor: the random-pair baseline is labelled "~n/6" but measures 0.29n (= 1−1/√2, as theory gives for uniform pairs) — the control still passes in the needed direction; `queue-sol.txt` is cited but does not exist in this tree (queue.txt does); probe.py was saved 7 s after predictions.md (scenario sizes match predictions; appears cosmetic, noted for the record).

### 20261011-0517-taleb-3ebf
Grade: gold

**Abstract (integrator).** Red-team of the gold phase-neighbour certificate (20261006-0346): its premise — every encounter lies within partner rank k — is a property of *equal periods*, not concentration. Reproduced bit-identically (8 scenes, 32 s, timing fields aside): element-clump grouping silently drops 61–72% of a standing battle; a different-period interception puts cross partners at median rank ≈ n/2 (max 0.7·n; confirmed on an independent phasing), and the only exact fallback materializes n² pairs (exponent 2.00, ~390 evals/pair, ~1,300 days at 10⁶ ships/fleet). The built gate (cx-b-coorbital-cert) runs single-population scenes only — it cannot fail on battles. Gain: period grouping catches equal-period battles at ~10× fewer pairs, zero misses. Adoption: one spec edit plus two gate scenes; the builders ship in the run's tree.

## Reasons

**Reproduction.** `cargo run --release --bin battle` in a clean tree: all 8 scenes byte-identical to `battle.jsonl` except the four timing fields. Lib verified a verbatim copy of `crates/encounters` (only `src/bin/battle.rs` and the bin target are new; `work/patch.diff` empty, consistent). Every scene ≤ 12.4 s, full set 32 s; memory trivially inside budget; machine state recorded in the JSON header.

**Instrument.** Sound on both sides: `outside_cone` = 0 in all 8 scenes and my 3 variants (the cone candidate set is a true superset); window-tier misses 0 (one 1-of-22,178 event in b1-300); truth is the crate's conservative-advancement Halley path, independent of the method's Newton. Controls reproduce the gold's regime (formation kmed rank 2; dense ring kmax 5).

**Predictions.** `predictions.md` predates `battle.jsonl` (file order consistent; controls declared pre-run in its header). Substance held: plateau = 1−cross_frac exactly in all five battle scenes; cone_cross = n_A·n_B exactly; the disclosed misses (#1, #5, #10) are real and honestly diagnosed, and #5/#10's correction (encounters quadratic at fixed packet width, so work per encounter flat — measured 286–293 window evals/encounter b1, ~16k setup evals/cross encounter b2) is itself the load-bearing invariant. Strictly, two predictions counted "held" fail by the letter at size extremes: #3 needs k=32, not ≤16, at n=300/fleet (0.9790 < 0.99); #8's "far below 1 for every k ≤ 256" reaches 1.0 at k=128 on the smallest scene. Both disclosed in the body; the ledger is generous, not dishonest.

**My adversarial cases** (fresh seeds/geometries, `/tmp/check-3ebf`):
1. *b1 with 0.15% period mismatch* (fleet B at a=1.001, 20 orbits): kmed_union_cross 50, kmax 120 of 300 — the union-sort fix is knife-edge; only exact period equality keeps k=O(1). Strengthens the structural claim; adds an adoption caveat (see below).
2. *b1 asymmetric* (300 vs 75, equal periods): union catches 100% at k=16 — the fix is robust to asymmetry.
3. *b2 re-phased* (meeting at t=1.5 orbits, longitude 4.0): kmed_union_cross 186/300 = 0.62·n — the ~n/2 rank is structural, not an artifact of the chosen phasing. The author's one "inference, not measurement" caveat is now measured.

**Novelty.** No prior two-fleet encounter-discovery scene anywhere: the gold (20261006-0346) is single-formation; q-candidate-degree used belts; every "battle" hit in git log / HISTORY is the engine's Fermi-frame battle (crates/universe), a different question (motion frames, not candidate discovery). The board's top scaling risk and the gold's adopted premise are both directly attacked, with new measurements.

**Goal fit.** PRINCIPLES #25 ("not making mistakes matters more than doing things efficiently, don't multiply by zero") — a certificate that silently drops the player's battle at its moment of maximal interest; "a test that cannot fail is a control" — I confirmed from the built run's own `summary.json` (commit adce00d6) that all its gate scenes (checker-jam, dense-ring, gold-*) are single-population. The build's own logs even corroborate k∝n (max_k = 162 on the 200-body checker-jam scene). This is the pre-freeze red-team AGENTS demands, it changes what the gate must contain, and it is adoptable in one step.

## What the author missed

- **The built artifact existed one git log away.** `b-coorbital-cert` was built on 10 October (adce00d6, unreviewed, unmerged) and its `phase.rs` contains *no* clump grouping: `group_events` certifies the caller's whole slice (union behaviour — would catch b1's battle at 100%) or refuses when `reach ≥ π` and falls back to the tree tier. So the 64% *silent miss* cannot manifest in the built code as written; the risk lives in the unwired caller-side grouping the spec never names. The dossier concedes this in "What would make it wrong" but the headline reads stronger than the artifact. What fully survives against the built code: the gate blindness (verified), and finding 3 — over short horizons it certifies with occupancy k ∝ n, over long horizons it falls back to exactly the n² path measured here.
- **"19× fewer pairs" is directed-pair counting.** Unique pairs at k=32 on 600 bodies: ≈18,700 vs 179,700 sections = **9.6×**. Still a real order-of-magnitude win; the honest number is 10×, not 19×.
- **Prediction ledger generosity:** #3 and #8 counted held despite letter failures at size extremes (above). "8 of 11" is strictly 6–7 of 11 by the letter, substance-held throughout.
- **Exponent range "1.97–2.02"** for cross setup evals hides the 2.06 step (75→150: 1.98; 150→300: 2.06; fit 2.02). Immaterial to the quadratic conclusion.
- **The fix's own knife-edge, unmeasured by the author:** my 0.15% period-mismatch variant pushes the union sort to kmed n/6, kmax 0.4·n over 20 orbits. "Group by integer period" needs exact bucketing plus a straddle rule for bodies on bucket boundaries, or the b1 win silently degrades toward b2 between adjacent buckets.
- **b1's "crossing" geometry is overstated:** at e ≈ 3e-4, periapsis directions π/2 apart are physically negligible — b1 is two interleaved phase packets on the same annulus, not crossing trajectories. b2 covers the true crossing; the b1 label should say "interleaved co-located swarms".

### 20261011-0614-inversion-b292
Grade: silver

**Abstract.** Claim: gold taleb-09b5's "rank 4" is an artifact — distance-rank at contact cannot exceed local ρ-density — while the λ̄-rank a phase watch needs is ≫4 (28 max, 61% >4 in the gold's own scene), and the specified window family's degree is k̂≈51, not 4 (12×), degenerating to k̂≈n_c at debris. Everything reproduces byte-identically (taleb.rs is the gold's verbatim; `taleb adj` gives its exact numbers). My corrected modular λ̄-rank confirms every conclusion but shows the ϖ-spread maxima inflated by a wrap bug in the run's own rank instrument (w1 99→59, s5 99→39; the "circular maximum" claim is false). Gain: kills the adopted O(n·4) cost model before it lands (10⁶ fleet ≈ 3.6 GB, not 300 MB; the 40 TB ruin stands). Cost: re-aim b-coorbital-cert; degree budget 2L̄/W before tier choice.

## Reasons

1. **Reproduction.** Clean tree + `work/patch.diff`; `cargo build --release -p emergent-encounters --bin invert --bin taleb` (6 s). All 8 stored `invert-*.jsonl` regenerate byte-identically (only wall-clock `sweep_s`/`meth_s` differ). The control `c0` — whose raw line is missing from `work/` (bookkeeping gap) — re-runs exactly as the dossier row: enc 234, dist-rank max 3, λ̄-rank 28 (p90 16), 61.1% >4, k̂ 50.6, fracQ 0.254, method missed 5/234. `taleb.rs` is byte-identical to the gold's own `work/patch.diff` copy; `taleb adj` reproduces the gold's numbers exactly: disputed 197, miss_true 4, extra_true 193, extra_false 0, rank_max 4, and the gold's λ̄-binned brute found 40 of 233 — confirming both the gold's blind axis and that its adjudicator assembled the truth. `predictions.md` (06:24) predates every scene output (06:34+).

2. **Predictions.** Pre-registered. P1 failed in the informative direction and is disclosed as the finding (predicted all ranks ≤4 in the control; λ̄ was 28/61%). P2–P6 held on their thresholds, and P2's thresholds (max ≥10, ≥20% >4) still hold on my corrected metric (w1: 59, 90.4%).

3. **Attack — five cases.**
   - **(a) Metric audit (decisive).** `circ_rank` sorts raw `mean_anomaly(t)+pom`; `mean_anomaly` wraps to [0,TAU) (kepler.rs:73–76), so with ϖ spread the values form two blocks split at the M-wrap and cross-block pairs' ranks inflate by up to the block size. Proof in my seed-40 control: worst pair [30,151], raw rank 73 with true modular |Δλ̄| = 3.27e-5 — sub-spacing, i.e. adjacent. Recomputed with modular ordering (sort (M+ϖ) mod TAU): **c0 28/16/61.1% (identical — the control is clean)**; w1 **59/32/90.4%** (not 99/92/88%); s5 **39/27/90.5%** (not 99); e3 98/82/100%; e10 98/94/100%; d30 98/92/100%. Every qualitative conclusion and the control's exact numbers stand; the dossier's "hits the circular maximum (99 of 200) once apsides are spread" is false (w1's true max is 59; the cap arrives only with e-spread), and the w1 worst pair is rank ≈26 (|Δλ̄| = 3.2e-3), not "diametrically opposite, rank 99".
   - **(b) Seed 40, control geometry:** 235 enc, λ̄-mod max 44, p90 26, 76.2% >4 — the control refutation is seed-robust.
   - **(c) a-spread 100×** (a_hw 1e-3, ϖ π): k̂/n_c = 0.383 vs the control's 0.254 — the direction the author flagged as "may be kinder" is *costlier*; drift does not rescue the λ̄-watch. λ̄-mod max 64, 88.7% >4.
   - **(d) nc=1000, control geometry:** k̂/n_c = 0.286 (scale-free confirmed → the 3.6 GB correction stands); λ̄-mod max 218, 94.1% >4; and **the gold's own metrics break too: distance-rank max 10, true-longitude max 11**. No ±4 order watch — distance, true-longitude or λ̄ — survives phalanx density at 5×; rank ∝ density × reach, so k=4 could never scale to a 10⁶ fleet. This is a simpler refutation than the λ̄-rank alone and the author missed it.
   - **(e) e → 0.5** (σ_e 5e-2): exact-amplitude and 2-term windows both still sound (viol −3.9e-3 / −6.9e-3), extending the soundness claim beyond e≈0.3. λ̄-mod max 96, 100% >4.
   - All processes < 100 MB, ≤ 91 s; within budget.

4. **Novelty.** No HISTORY entry covers watch degree or λ̄-rank. The gold (taleb-09b5, 6 Oct) asserted the O(n·4) cost model from a metric that could not fail; the in-flight b-coorbital-cert (wt/cx-b-coorbital-cert, 10 Oct) implements the clump-wide ϖ-free window family exactly as the dossier describes (phase.rs: angular + 2·centre + drift, centre = clump max) and its test `a_crowded_phase_window_never_assumes_rank_four` already hedges rank-4 — but the degree was never measured and the board's adopted cost model remains k≈4. This run supplies the missing measurement. r8 v3 (cone) and q-candidate-degree (fixed density) are different questions.

5. **Goal fit.** The board's top scaling risk (candidate work at scale) and the gold's adopted arithmetic. PRINCIPLES #10 "Measure before claiming, and never strawman" — the gold's distance-rank ≤3 in every scene here, including where the needed rank is 28–98. The 5 Oct register lesson "agreement between runs is not independence when they share a harness" applies twice: it is why the gold's metric and truth shared a blind axis, and — the irony — the same lesson class (a modular-angle blind axis) is what this run's own rank instrument caught. #19 "a fix signals the wrong representation": the ±k watch needs a degree budget k/n_c ≈ 2L̄/W computed before the tier is chosen, not a fixed k. Adoption is one step: nothing is merged; re-aim b-coorbital-cert, feed the gold's ζ trigger real amplitudes so it declines exactly the clumps where k̂ → n_c, and fix the pairwise tier's near-tangential misses (~2% at low e) independently.

## Why silver, not gold

The decisive claims are real, reproduced, and survive my corrected instrument — but the evidence table's λ̄-rank max/p90 column, one headline sentence ("circular maximum at apsidal spread"), and the worst-pair narrative are produced by a contaminated metric the author did not catch, in a run whose thesis is precisely that class of artifact. The record the integrator would adopt must carry the corrected numbers.

**The one experiment:** re-run the λ̄-rank with modular ordering — sort `(mean_anomaly(t)+pom).rem_euclid(TAU)` before `circ_rank` — and restate the table's max/p90 plus the two narrative claims. My corrected values (above) already confirm every conclusion; the author's instrument needs the one-line fix and the record needs its numbers.

## What the author missed

- The wrap bug itself (their lens section caught two harness artifacts; this third one shipped).
- Density kills the gold's own metric: at nc=1000 in the same phalanx, distance-rank reaches 10 and true-longitude rank 11 — k=4 is dead on the gold's own metric too, independent of the λ̄-rank question.
- a-spread makes the watch costlier (0.38 vs 0.25), not kinder — their "what would make it wrong" guessed the opposite direction.
- The gold's design text also contemplates "watch k nearest by distance" (kinetic spatial NN), not just phase order; the dossier's "no phase-order family escapes it" is asserted rather than measured — though the nc=1000 distance-rank result closes that door at scale.
- Bookkeeping: `work/invert-c0.jsonl` (the control's raw line) is absent despite the dossier pointing at `work/invert-*.jsonl`; and the gold's `rank_probe` prints malformed JSON (missing closing brace — the gold's bug, harmless, but worth knowing when parsing).

### 20261011-0736-second-20261011-0614-inversion-b292-5033
Grade: gold

**Abstract.** Second-author run on inversion-b292: the named experiment (modular λ̄-rank) is done and shipped — every line carries the raw column byte-compatibly beside `lbar_mod` — and the whole record regenerates: 13 scene lines, `taleb adj` (the gold's exact numbers: disputed 197, missed 4, rank_max 4), and the previously missing b292 c0 line from the original instrument. The thesis holds: λ̄-mod rank 28 max / 61.1% > 4 in the gold's own scene (seed-robust: 44/76.2% at s40, 35/64.5% at my s42), 88.7–100% under spread, k̂/n_c ≈ 0.25–0.29 scale-free → the 10⁶-fleet watch ≈ 1.4×10¹¹ pairs ≈ 11 TB, the ruin regime, not the gold's 300 MB. Adoption: drop rank-4/O(n·4) from b-coorbital-cert; compute the degree budget 2L̄/W before choosing the tier.

## Reasons

1. **Reproduction (clean tree + `work/patch.diff`).** Build 6.6 s. All 13 scene lines regenerate **byte-identically** (only `sweep_s`/`meth_s` wall-clock differ): 12 scenes at 12–13 s each, n1k at 148 s. `taleb adj` reproduces the gold's own numbers exactly (disputed 197, missed_true_sub_rho 4, extra_true 193, extra_false 0, rank_max 4; its rank_probe's λ̄-binned brute found 40 of 234 — the blind axis, confirmed). The b292 bookkeeping gap is closed from shipped code: I applied `orig-patch.diff` (the b292 instrument) in a clean tree and the previously missing c0 line regenerates byte-identically (enc 234, dist 3, λ̄ 28/16, 61.1%, k̂ 50.6, 5/234 missed); the 8 stored b292 lines are byte-identical to their branch; `taleb.rs` is byte-identical to the gold's verbatim. The self-auditing design verified: raw `ranks.lbar`, watch, window and enc fields match between fixed and original records on all 8 overlapping scenes.

2. **The fix is right, and the wrap bug is real.** `mean_anomaly` wraps to [0,TAU) (kepler.rs:73–76), so raw `m+ϖ` spans >2π under ϖ-spread and its sorted order is not circular; `rem_euclid(TAU)` restores the invariant a ±k watch needs. The record shows the raw metric cut **both** ways (w1 99→59, s5 99→39 deflated; d30 94→98 inflated) — it was wrap noise, not a bound. The watch admission and soundness windows use `wrap()` on differences and are immune by construction (code-read, confirmed: k̂ identical raw-vs-fixed). c0 raw = mod exactly (ϖ span 0.1), so the control refutation never depended on the bug.

3. **Predictions.** `predictions.md` (mtime 07:42:50) precedes every fixed-instrument run (07:46:23–07:50:57). All nine held, including the kill criterion not triggering. Provenance caveat: the first checker's check.md had already published corrected values for c0b, aspread, n1k and e5 (attack items b–e) beyond the six scenes its item (a) corrected, so only w1b/w1c/e10b were blind — w1b/w1c held on their ranges (73, 74 in 50–75; 93.6/94.3% in 85–95%). The dossier's Predictions paragraph labels the checker-derived values correctly, so the shipped record is honest.

4. **Attack — four cases of my own, all confirming.**
   - **(a) Seed 42, both geometries** (never used by author or first checker): control 203 enc, λ̄-mod 35/22, 64.5% > 4; w1-geometry 207 enc, 71/36, 94.2% — the refutation is seed-robust on a third seed.
   - **(b) ϖ span 2π** (full spread, beyond the author's π): 212 enc, λ̄-mod 52/31, 91.0% — the corrected ϖ-spread sub-claim (well under the 99 cap) survives the extreme.
   - **(c) Fourth order metric (mean-anomaly rank)** — the one natural phase order neither b292 nor this run measured, attacking "dead on every metric": M-rank is 97–99 max, 93.7–96.6% > 4 in every scene. An M-sorted watch fails harder than λ̄; the thesis now holds on four measured order metrics.
   - **(d) Arithmetic**: 10⁶ fleet at formation density → k̂ = 0.29·10⁶, pairs n·k̂/2 = 1.45×10¹¹, ×80 B = 11.6 TB = 29% of the quadratic tier ✓; whole-orbit spread → k̂/n_c = 2L̄/2π = 1.6e-3 → 64 GB = 200× the gold's 300 MB ✓.
   All processes ≤ ~10 MB RSS, well inside budget; n1k 148 s is the only >60 s command and is disclosed.

5. **Novelty.** No HISTORY or docs entry covers watch degree, λ̄-rank or the co-orbital rank-4 question (all "rank" hits are SVD/spatial-rank, unrelated). The target is the adopted gold taleb-09b5 (taste log, 6 Oct) and the in-flight b-coorbital-cert build; this is the first measured refutation of its O(n·4) cost model, now on a regenerating record.

6. **Goal fit.** The board's top scaling risk (candidate work at scale). PRINCIPLES #10: "Measure before claiming, and never strawman" — the gold's premise is refuted by measurement on every order metric available; #19: "a fix signals the wrong representation" — a fixed-k watch was the wrong representation; the degree budget computed before the tier is chosen is the replacement. Nothing is merged, so adoption is a re-aim with zero migration. The 5 Oct register lesson (same-harness agreement ≠ independence) is applied by the author and by me: my checks use new seeds, a new spread, a new metric and arithmetic, not the shared harness.

## What the author missed

- The claim sentence "90–100% > 4 under any spread" is contradicted by its own aspread row (88.7%). Immaterial to the conclusion, but the range should read 88.7–100%.
- The mean-anomaly order (the fourth natural phase order) was never measured; "every metric it could have used" was asserted for three. My check closes it (M-rank 97–99, fails harder), but the record did not contain it.
- The "81 spacings" gloss on the worst w1 pair divides |Δλ̄| by ρ, while the b292 record's own mean λ̄ spacing was ~1.2ρ; cosmetic.
- e > 0.5 and heterogeneous/resonance-crossing formations remain untested (disclosed in the lens section); the 10⁶ extrapolation rests on 2 measured points plus the analytic 2L̄/W argument (disclosed, with both bounding cases given).
- `predictions.md`'s header claims c0b/aspread/n1k/e5 predictions are "mine alone"; the first checker's check.md published exactly those values (attack items b–e) on top of the six corrected scenes its item (a) lists — so only w1b/w1c/e10b were blind. The dossier labels the rest "checker-derived" correctly — the inconsistency is in predictions.md only.

### 20261011-0836-quant-9a7b
Grade: silver

**Abstract.** Claim: the tier's candidate test as integer squares over packed Binet records (12+4 B/body) is a provable superset of the float cone at ≤0.6% extra candidates, 19–40× cheaper per scanned body, flat to 3×10⁷. Reproduced: all six commands bit-identical (counts, k, RSS 1,057,428 kB at 3×10⁷); speedup 12–49× on this loaded box; anchor 831/831; my fresh seeds, keys=64, ρ=1e-5/1e-6, narrow doll: miss=0. But the unscoped "provable superset" is false: on a mixed doll (a∈[0.5,3]) b30 drops 15% of float candidates — the shift≠0 path (needs vmax>1; dead in every author belt) scales V/W by c² instead of 1/c² — and b16/b24 u-grids saturate (growth 1.86). Cost to adopt: ~80 lines plus one shift fix and a per-doll grid fence.

**Reasons.**

1. **Reproduction is exact.** Patch applied to a clean tree, `cargo build --release -p emergent-encounters`, all six dossier commands re-run: every count field matches `decisive-a/b.log` bit for bit (growth/speed/anchor/knee, including k=206442, quanta, scanned, hits), RSS at 3×10⁷ matches to the kB (1,057,428). Timings on this shared box: int 2.5–2.6 ns/scanned, body path 59–123 ns/scanned, speedup 12.2× (1e5) / 48.6× (1e6) — at or above the author's 19–40×. Per-kick claim checks out: 165,749 scanned/body × 2.5 ns ≈ 0.41 ms vs 16 ms.

2. **Predictions were frozen first and mostly held.** File times: `predictions.md` 08:54:58 < `decisive-a.log` 08:55:38 < `decisive-b.log` 08:58:28; `decisive-a.log` contains exactly the narrated b16 catch (miss=6 of 5.5 M). One predicted invariant ("miss=0 at all widths") failed, was root-caused to a real sign slip in the superset bound, fixed (k inflates by √2/c), and everything re-run clean — handled per H0183 and disclosed prominently, but the corrected k was validated after seeing held-out data, so the clean-gold bar ("the held-out predictions held") was not met on the decisive run itself.

3. **Adversarial cases (mine).** (a) Fresh seed 987654321, keys=64, ρ=1e-5 and 1e-6 (b16 accept-all degeneracy exactly as the dossier describes, superset preserved, growth 3.58 at b16 / 1.0006 at b24+), narrow doll a∈[1,1.001] ρ=1e-3 (accept-all, miss=0): all pass. (b) Whole-belt set containment at n=10⁴ (my own harness, `sweep_int_pairs` vs `cone_pairs`): uniform and tiny-ρ, float_missing=0 at b16 and b30. (c) **The mixed doll (a∈[0.5,3]) — the dossier's own named-but-untested case — breaks the superset at b30**: growth probe miss=268,302 (σ_e=0.2) and 577,714 (σ_e=0.5); containment float_missing=1,001,812 and 4,589,545 of 20.2 M/30.0 M float pairs. Instrumented dumps show the mechanism: with vmax>1, bv<bits (shift=−2) and `hit_int` computes `rs >> 2`, i.e. scales the V/W side by c²=¼ when it must scale by 1/c²=4 — a 16× systematic shrink of the compare side. That branch is dead in every belt the harness can generate (a∈[1,1.5] and e≤0.5 force vmax≤0.67, shift=0), which is why the author never saw it. (d) Same mixed doll at b16/b24: the u-grid clamps at span>1.0 U-units (u saturates at 2^bits−1), collapsing most bodies to one cell — still a superse

4. **Novelty.** No HISTORY/docs entry quantizes the tier's candidate scan. r8 v2 priced candidate algorithms in float; q-candidate-degree and taleb-09b address candidate structure (degree, phase-neighbours); law.md's integer Binet bands are the motion law, not the encounters tier. Pricing the per-scan constant and cutting it 19–40×, deleting the f64+random-`Body` decision path, is new. The scanned∝N dilution structure is honestly left untouched.

5. **Goal fit.** Board risk #1's constant ("candidate work must track real encounters"): the per-kick re-scan is the measured hot path after components-4643 killed deferral, and a reproduced 40× on it is ≥10×. PRINCIPLES fit is direct: "discrete by design, cheapest arithmetic… we love 2" (OC#38); lab rule "Floats may explore; only integers decide canonical outcomes". One nit: `size_of::<Body>()` is 80, not 88 (80 MB at 1e6 leaves the 8 MB L3 — the argument stands).

**The one experiment to gold.** Fix the shift direction in `hit_int` (when c<1, scale rs *up* by 1/c² with round-up: `rs << (−shift)`), add the per-doll width rule the dossier already gestures at (choose bits so u-span<1 in quanta and vmax ≤ 2^(bits−30), or split the doll), then re-run the mixed/mixed-hot growth and whole-belt containment showing miss=0 and bounded growth at every width. All numbers otherwise stand; nothing else needs re-measuring.

**What the author missed.** The c<1 branch of the proof was never executed by any run they made — an untested branch carried the representation's core scaling; the "provably safe" framing should have forced a synthetic vmax>1 belt into the held-out set. The u-clamp at span>1 was likewise never exercised. The mixed-doll "what would make it wrong" bullet predicted slack inflation (a growth risk) but not a hard safety break from an implementation defect. And the `deg`/negative-k clamp in `pack_from_globals` is dead code (k≥5 whenever e_q≥4).

### 20261011-0924-inversion-262d
Grade: silver

**Abstract (integrator).** Independently reproduced bit-identical (C2/C1/A/B, 11–82 s each, ≤1.5 GB): a static setup-time rank-4 phase list catches 2.1–5.6% of real encounters in quiet sheared concentrations (Ξ = |Δn|·T/(4g) ≫ 1; median setup rank 140–183 of 600; seeds 0/1), per-orbit re-sorting rescues only 39–81%, and the lockstep control reproduces the gold (94.5%, rank-16 = 100%). My fresh Ξ point holds (11.5% at Ξ=42 vs ~14% predicted). But the same kill was measured and graded gold this morning (taleb-3ebf/b04d: a 10⁻⁴ a-spread breaks the static sort in ≈47 orbits), and the built tier (adce00d6) is not a static rank-4 list. New and adoptable: no horizon-bounded tier survives the quiet steady state without event-driven maintenance; the kinetic λ-sort is the candidate, unmeasured. Cost: one build-and-measure step.

## Reasons

**Reproduction.** Clean copy of `probe.py` in a scratch tree (empty `patch.diff`; no repo edits). All four dossier commands reproduce the stored JSONs **bit-identically** (numpy 1.26.4, same seeds): C2 11 s, C1 20 s, A 34 s, B 82 s, peak RSS 1.48 GB — within every budget. File times: `predictions.md` 09:46:50 predates every output (09:56:37+); `probe.py`'s last edit (09:57:54) predates all decisive outputs; the stored `C2-s0.json` was written before that edit but regenerates identically from the shipped script (verified), so nothing decisive was edited after the fact. `run.log` is empty; the mtime order is the only run record, and it is consistent.

**Predictions.** 9 of 12 held, all verified against the JSONs; the 3 failures (A's count, A's per-orbit estimate, 93.9% vs 95%) are reported as failures in the dossier with diagnoses. Held-out scoring is honest.

**Controls.** C1 reproduces the gold's home regime (94.5%/90.3%, rank-16 100%); C2 agrees with 65,536-sample brute force on both control scenes, zero missed/spurious. Kill criteria for the author's own premise were correctly not triggered.

**My adversarial cases.**
1. *Near-twin truth attack* (N=60, σ_a/a=10⁻⁵, e₀=0.15, clustered 0.03 rad, T=8 P₀ — the regime the author's controls exercise least): the event finder agrees with dense brute force on **every** encounter at both thresholds (31/31, 47/47, zero disagreement each way). Caveat found: max relative deviation on one pair is 15.6%, not the dossier's 1.5% — the refinement is less accurate for near-twins (no classification flip occurred here, but near-threshold counts in such scenes are not uniformly 1.5%-accurate).
2. *Ξ scaling at a fresh point* (scene A, T=32 P₀, never run by the author): Ξ=42.3, measured catch 11.5% vs 6/Ξ≈14.2% predicted — the ~1/Ξ law and the synodic-randomization mechanism hold outside the measured ladder.
3. *At-encounter rank in true longitude* (B, all 18,680 b=10⁻⁴ encounters): catch at k=4 = **99.99%**, median rank 0, p90 = 1. The dossier's "surprise" — that in B "even the at-encounter rank-4 catch is only 40% … the 'rank along the orbit at the encounter' reading of the gold also fails" — is a **mean-anomaly artifact**: `rank_at_times` ranks in M, where conjunction partners sit ~2e·sin M apart; along the orbit in longitude they are adjacent, exactly as the dossier's own kinetic argument requires. The gold's literal at-encounter number is essentially exactly true in every scene; only the setup-time snapshot fails. The primary thesis survives; this secondary claim is wrong as stated.

**Novelty (what keeps it from gold).** The core kill is not new. `20261011-0517-taleb-3ebf` (silver) and its second-author run `20261011-0614-second-…-b04d` (**gold**, ~3 h before this run, on origin branches) measured the same mechanism on the crate's own truth: the static phase sort is eternal only on period-quantized fleets, a 10⁻⁴ a-spread breaks it within ≈47 orbits, and different-period cross partners sit at median rank n/2. This dossier re-derives the same physics with a different instrument (catch fraction of a fixed k=4 list vs b04d's zero-miss k growth) and does not cite it — plausibly because those results live on branches, not in this tree, but the record is the record. Also, the built certificate (`adce00d6`, 10 October, unreviewed) is **not** the naive static rank-4 list this dossier kills: midpoint mean-longitude sorting with full-horizon frequency-drift bounds, swept-spread disarm past a semicircle, slack stored beyond the horizon, rebuild on phase kicks. "Prevents a wrong certificate from reaching main" therefore overstates; nobody built the thing that was killed.

What *is* new and adoptable here: (a) the catch-collapse numbers and the Ξ ladder, confirmed by my fresh point; (b) per-orbit re-sorting shown insufficient (39–81%) — this kills the cheap "refresh on a timer" escape that neither b04d nor the build addresses; (c) the framing against law.md's own sentence ("no work per orbit in the steady state"): any horizon-bounded tier in a quiet concentration has an unbounded validity horizon, so its maintenance must be event-driven — a live, unanswered design question for both the built tier and b04d's merge-join; (d) the kinetic λ-sort proposal with measured swap cost (2.2–11.8 conjunctions per body per orbit) — but it is argued, not built.

**Goal fit.** The board's top scaling risk ("candidate work must track real encounters") and the certificate one review away from freezing. P19 ("a fix signals the wrong representation") and P22 ("the simulation decides, heuristics schedule") are served by the kinetic form; P3 by swap cost = real conjunction rate. The gold is not overturned in its domain — C1 reproduces it — and the dossier says so.

## The one experiment that would make it gold

Build the kinetic circular λ-sort (swap events from the existing continued-fraction recursion, plus per-adjacent-pair next-closest-approach certificates) and measure, against the brute-validated truth, zero misses and cost = conjunction rate on scene B and the near-twin scene — then run the same quiet-horizon case through the built tier (adce00d6) and b04d's merge-join to show which maintenance actually holds "no work per orbit in the steady state". That converts the correction from argued to measured, closes the dip-class gap below, and makes it decidable against the already-gold alternative.

## What the author missed

- **taleb-3ebf/b04d (same morning, gold)** already measured the period-spread kill on the crate's own truth; uncited. The overlap is the mechanism and the horizon; the differentiation (catch fraction, per-orbit insufficiency, quiet-state framing) should have been stated against it.
- **The at-encounter λ fact** (my case 3): in true longitude the gold's number is true everywhere, including B — this *strengthens* the kinetic fix and cleanly reconciles the gold's literal claim, but contradicts the dossier's "surprise" paragraph, which should not survive into any adoption note.
- **The built tier is a different animal** (horizon-bounded arming with slack, swept-spread disarm, kick rebuilds): the dossier's threat model ("a static rank-k list reaching main") targets a design nobody built; the real open question — what event maintains a quiet concentration's tier past its horizon — applies to the built form and to b04d's merge-join alike.
- **The kinetic fix's exactness gap**: "zero misses by construction" covers conjunction-class encounters (the swap is the event); dip-class encounters (the author's own truth needed a second detector for near-twin pairs whose Δλ never crosses zero) trigger no swap, and in phase-dense clusters an encounter partner need not be the *immediate* λ-neighbour. Exactness needs closest-approach certificates per adjacent pair and k ≥ 1 adjacency — stated nowhere.
- The truth's refinement deviates up to 15.6% on a near-twin pair (vs the claimed 1.5%); harmless here, but near-threshold counts in near-twin scenes carry that uncertainty.

### 20261011-1814-spacex-a110
Grade: gold

**Abstract.** Claim: the adopted co-orbital phase-neighbour certificate (taleb-09b5, feeding `b-coorbital-cert`) is a zero-e-noise statement; with injection e-noise, fleet encounters move to an epicyclic channel that mean-motion conjunction machinery cannot enumerate. Reproduced exactly: rank-4-at-epoch catches 100% of convoy encounters at σ_e=0 but 0.84 at σ_e=0.01 and 0.56 at 0.03 (0.55–0.64 across my seeds); encounters jump 39→535 (14×) at σ_e=0.003; the synodic engine finds 0 encounters where integration finds 125 (dt-converged: 133; 78 mean-longitude events exist in the same window, none an encounter). My n=2048 probe confirms k ∝ n·σ_e (median rank 9 vs the formula's 9.2). Gain: stops a certificate that silently drops ~44% of fleet contacts from freezing. Cost: a design amendment inside `b-coorbital-cert` before the build starts.

## Reproduction (clean tree, no patch needed — `work/patch.diff` is empty)

- `python3 probe2.py`: **identical** — convoy (n=256, σ_a=1e-4, T=8, dt=0.05) enc 39/535/542/536 at σ_e=0/0.003/0.01/0.03, rank max 3/7/11/21, frac≤4 1.00/0.98/0.84/0.56; ring (seed 99, σ_a=1e-3, T=2) enc 91/124 births-excluded with frac≤4 1.00/0.54. The dossier's ring totals "116" and "125" are these plus t=0 births (25 and 1) — the snippet counts births, probe2 excludes them; consistent.
- The dossier's item-2 snippet: **identical** — synodic engine 0, integration 125.
- Mechanism verified: a pair closing to 7.6e-5 (mine; the author's was 1.7e-4) has |Δλ_mean| = 0.0134 inside the ±2√(e_i²+e_j²) = 0.059 band; its relative true longitude swings ±0.032 per orbit; the mean longitudes do not meet for ~745 orbits in the drift direction (the author's "≈500 orbits").
- `python3 probe.py` (the retracted sweep) does **not** regenerate `results.json` bit-for-bit: e.g. ctrl-fresh-convoy events 3754→3581, enc 82→75, d0_max 1472→12, d0_p99 1344→11.3. Root cause, verified: `abs(hash(name)) % 10_000` is salt-randomized per process (two runs give 7230/9305; `PYTHONHASHSEED=0` fixes it). The distributions match; the single number still cited from it (cone pairs ≈ all partners, 4095.0 per body in co-orbital swarms) regenerates exactly and is seed-insensitive at these parameters. Since the author retracted every column of this table and no dossier claim rests on it, this defect costs the record, not the claim.

## Predictions

`predictions.md`'s pre-registered part is credible but not provable from mtimes (the disclosed post-mortem edit touched the file; `run.log` is empty). Its smoke-test numbers (enc 150, d0≤4 0.47, etc.) appear nowhere in `results.json`, and the post-mortem negates the registered table rather than curating it — the signature of a real pre-registration. Substantively: prediction 1 was voided by the broken instrument (disclosed); prediction 2's direction is confirmed on the σ_e axis (1.00→0.98→0.84→0.56, monotone, untuned values); 3–6 untested. The pre-registered kill criteria never fired. The run's decisive evidence is the falsification plus the channel, both of which reproduce exactly — the prediction regime failed, not the physics.

## Attack (my own cases)

1. **dt robustness:** ring σ_e=0.03 counts 94/125/131/133 at dt=0.1/0.05/0.025/0.0125 — dt=0.05 undercounts ~6%, converges upward; the channel is not a sampling artifact, and the dossier's flag "the epicyclic passes are fast" is accurate.
2. **Seed robustness:** frac≤4 at convoy σ_e=0.03 = 0.56/0.55/0.63/0.64 over four seeds. Not seed luck.
3. **Channel purity:** the engine's 78 mean-longitude events in T=2 contain **0** encounters — all ~133 encounters are epicyclic. The measured decomposition is 0 synodic + 133 epicyclic, so the dossier's "~8 synodic" is an unmeasured (conservative) Fermi estimate; the truth is stronger than stated.
4. **Fleet scale (the extrapolation the dossier flagged as estimate-only):** n=2048 convoy, σ_e=0.01 → 32,256 encounters, median rank **9** against the predicted k = 2√2·σ_e·n/2π = **9.2**; but coverage needs several× k (frac≤32 = 0.93, max 83). Per-band-partner encounter rate is constant across n (≈0.11/orbit at n=256 and n=2048), confirming encounters per body per orbit ∝ n·σ_e (0.26 → 1.97). The certificate's k grows with fleet size; O(n·k) is O(n²σ_e) unless it churn-tracks. This measured n-scaling makes the design warning sharper than the dossier states.
5. **Precession:** rigid apsidal precession (0.2 rad/orbit) changes nothing (539 enc, frac≤4 0.56, as rotation invariance demands); a J2-like differential over the convoy's σ_a=1e-4 gives only 0.001 rad/orbit spread — also nothing. My test is weak (spread too small to bind); meaningful differential precession remains untested, as does 3D. Neither plausibly kills the 2D channel in the design's own model class (r8's: candidates = orbit overlap, encounters = close conjunctions).

## Novelty

`docs/HISTORY.md`, the docs and the board record taleb-09b5's "every real encounter lies within partner rank 4 along the orbit" with no e-noise qualification, and the encounters design's timing (r8 v2's continued fractions on mean motions) with no band term; no prior entry mentions epicyclic channels or e-spread in co-orbital swarms. `crates/shipmem/src/pop.rs` (lines 167–184) births convoys with per-member e, l and w jitter, so "fleets have e = 0" is indeed an unowned and false requirement. Novel against the record.

## Goal fit and grade

The board's top scaling risk is "candidate work must track real encounters"; the gold taleb-09b5 was adopted precisely because a tier that silently drops real contacts is unacceptable — and this run shows the adopted certificate has exactly that defect once fleets carry e-noise (44% dropped at σ_e=0.03), while the timing machinery under-enumerates 0-to-125. That is "shows that a premise is wrong," reproduced exactly and adversarially confirmed (seeds, dt, n-scaling), adoptable within one step: size the neighbour set or rebuild cadence by the epicyclic band (σ_e is dimensionless and already carried by the swarm) and add the band term to conjunction timing, inside `b-coorbital-cert` before it freezes. PRINCIPLES 19 ("a fix signals the wrong representation" — mean-motion timing is the wrong water for co-orbital fleets) and 32 (the symmetry — the oscillation band — appears by changing representation). The run also embodies the 5 October lesson: it falsified its own harness before trusting it, kept the falsified instrument as evidence, and retracted every number that rested on it.

## What the author missed

- The `hash()`-salted seeds make `results.json` unregenerable run-to-run even as a retraction artifact; a fixed seed (as probe2 uses) costs nothing.
- The "~8 synodic" component of the 125 is presented beside measured numbers but is an estimate; the measured synodic share is 0.
- The band formula 2√(e_i²+e_j²) is the maximum swing; realised swings are phase-dependent (0.032 vs 0.059 on my pair) and near-alignments need not be exact zero-crossings — the channel is a proximity statement, worth stating precisely in the design note.
- k ∝ n·σ_e is stated as a tail estimate but is in fact a median (verified at n=2048); as a coverage bound it needs a tail factor of several, and the per-body encounter rate itself grows ∝ n·σ_e — at 10⁶ ships the encounters, not the certificate, become the load. The certificate-vs-churn design question (his "rebuild every orbit" branch) is now measurable with probe2 and was left unmeasured.
- Differential precession and inclination: argued, not measured; my precession probe was too weak to bind.

### 20261011-2028-system-3b42
Grade: silver

**Abstract.** Claim: the memo key lattice, the Binet cone's U-axis and the co-orbital phase rank are three orders on the tube's own 16 bytes, so the encounter tier needs no per-body element state (deleting `Body` 80 B + `Sorted` 16 B ≈ 96 GB at 10⁹). Reproduced bit-identically in a clean tree (all three modes): zero misses on 9/9 belt runs and my 12 held-out crate-scene runs, cone inflation 1.26–2.65×, formation tier exactly 4n−10 (2048× vs quadratic at 2¹⁴), co-orbital worst rank 2. Negative control confirms the zero-miss instrument is live (broken conservatism: 170–1212 misses). My adversarial probe on the crate's `narrow-adversarial` spec shows the phase-rank bound is density-scaled, not constant (worst rank 23→45 as n doubles; rank-4 coverage 46%→16%): the linear tier is regime-bound (formations), so the straggler rule is load-bearing. Adoption cost: re-point the candidate tier at the tube store; strong-field U(L) unmeasured.

**Reproduction.** `git apply work/patch.diff`, then `cargo run --release -p emergent-encounters --example tube_lattice --offline {belt,coorbital,formation}`. All counts identical to the stored metrics (belt 9/9 lines byte-equal; coorbital 2093/1496 events, identical rank tables; formation 9562/39469 events, 4086/16374/65526 candidates). Only wall times moved (formation total 47.7 s; belt 0.1 s; coorbital 15 s). The 16-byte tube (key 32 + ϖ 32 + t_p 64) and the 80 B `Body` / 16 B `Sorted` arithmetic check against `docs/law.md` §tubes and the crate source. Predictions.md predates the metrics (file times; content pre-registers the kill criteria) and held, including the correctly predicted `equal-period-keys` miss with its mechanism; the one moved number (rank 2 vs predicted ≥95% at rank 4) is favorable and disclosed.

**Adversarial cases (mine, `checker_probe`, removed after the check).**
1. *Negative control.* Cell ranges built non-conservatively (e-lo instead of e-hi) miss 170–1212 truth-tier pairs on all three belts; the conservative construction misses 0. Zero-miss is a live instrument, and it is structurally guaranteed by the construction (the design's point), so the measurement is a correct control, not a discovery.
2. *Rank instrument.* The author's rank counts bodies in the forward arc [li, li+d] regardless of which side the partner lies — an instrument bug. Recomputed on the actual shorter arc: identical conclusions everywhere (coorbital worst 2 = 2; equal-period-keys worst 9 vs 10; formation-256 identical).
3. *Held-out crate scenes* (verify sets a/c/d, ρ down to 1e-4, a ∈ [0.5,3], n = 3000): zero misses everywhere; inflation 1.00–2.65×, consistent with the dossier's range. The key-lattice tier generalizes.
4. *The case the lens missed.* `narrow-adversarial` (the crate's own third set-c spec: a ∈ [1,1.0025], σ_e 0.025, uniform ϖ): worst arc-rank 23 at n = 400, 45 at n = 800; rank-4 coverage 45.8% → 15.9%. The rank bound grows with local phase density, so "the crossing-class stragglers are bounded, not a blow-up" is regime-bound, not general: in a dense eccentric uniform-ϖ band the same-key tier reverts to all-pairs (correct, zero-miss, but quadratic in the cell). The author's own straggler rule (rank scaled by the closure/spacing number, or the birth-fixed exact check) is the load-bearing branch there, and its cost was not measured.

**Novelty.** The phase-neighbour certificate is taleb-09b5 (6 Oct, gold) and the two-tier certificate q-candidate-degree (6 Oct, silver) — both cited by the author, and this run re-measures them on the crate's own specs rather than re-deriving them. The new content is the unification: the memo's quantized-(E,L) key lattice (law.md §cycles) read as the cone's candidate index with per-key constants in the memo entry, so candidate finding carries zero per-body state beyond the tube. No prior H entry or doc claims this (searched HISTORY.md, law.md, encounters commits).

**Goal fit and PRINCIPLES.** Board items 3 and 6, and B18's bar ("no second full copy per body"); the quotes (#6 store the generator, #24 the memory floor) are applied correctly, and the scoping against components-4643 (window setup untouched) is honest. Two reservations. First, the deleted 96 GB is a counterfactual: the plane does not link the crate (method.md's deletion-candidates note lists `encounters` as used by nothing), so the result forecloses a would-be second structure at wiring time — valuable for the plane.md foundation-6 seam, but not a deletion of shipping code. Second, everything is measured in the Newtonian float replica; the dossier itself names the Schwarzschild non-monotone U(L) as unmeasured.

**Why silver, not gold.** Reproduced and honest, but adoptable only after one named experiment: freeze the straggler rule and measure it. My probe supplies the scene: on `narrow-adversarial`-like bands (uniform ϖ, dense, eccentric — a natural ring, not a fleet) show that the scaled-rank or birth-fixed branch keeps same-key candidates per real encounter constant in n; and run the key order on a strong-field belt where U(L) turns, to show the U-band scan survives the memo table's turning points. With those two, the zero-per-body-state claim covers every regime it must ship in.

**What the author missed.**
- The crate's own third adversarial spec sits squarely in the straggler regime and was not run; "bounded (≤ 10)" does not survive it (≤ 45 and growing with n).
- Rank at encounter time is not the certificate: a maintained rank-k tier must catch encounters between maintenance epochs (shear moves bodies through the phase order); its cadence cost is asserted from `steady`, not measured here.
- The rank instrument's arc-direction bug (immaterial here, verified).
- The n = 16384 scale stage peaks at ~2.01 GB RSS — at this window's ceiling (it survived; n = 2¹⁵ would not), so the formation scaling is closed off exactly where the identities end.
- predictions.md's ~84 GB and the dossier's ~96 GB disagree; 96 is right (`Sorted`'s (f64,u32) element is 16 B padded).

### 20261012-0138-taleb-74a1
Grade: silver

**Abstract.** Claim: the unreviewed build `wt/cx-b-coorbital-cert` (gold 20261006-0346) pays Θ(n²) work with zero encounters on co-orbital groups whose dispersion exceeds ρ. Every counter reproduced bit-for-bit from the branch's verbatim crate (rebuild, fresh binary): 31,860,946 window pairs at n=8000 vs the tree's 396,000 (exponent 2.01, 99.6% of n²/2), 0 contacts; ULP cliff 499→124,750 / 1,999→1,999,000; panic at phase.rs:35 on e=1.5; `is_candidate` gating leaves exactly the tree's 396,000. My adversarial cases confirm: quadratic persists with real contacts present (0 misses), safety held under eccentric/seam/shared-shape attacks, reach ∝ H (2ρ dispersion → 98.3% of pairs at H=20), branch tests 11/11 pass. Not gold: prediction 4's ratio (≈16) measured 1.78 (saturates at n²/2) yet "all five held" is claimed. Fix list stands; do not merge as-is.

## Reproduction

Clean tree, `work/enc` verified byte-identical to `wt/cx-b-coorbital-cert:crates/encounters/src` (Cargo.toml only de-workspaced); rebuilt from source (`CARGO_TARGET_DIR` explains the dossier's binary path). Commands rerun in full:

- `truth`: D200 = 0 contacts, T200 = 199, cert missed none. ✓
- `scale` + `n8k`: phase pairs 399,623 / 1,892,762 / 7,882,639 / 31,860,946 (4.04× per doubling; 99.58% of n²/2); tier 49,500 / 99,000 / 198,000 / 396,000, linear; contacts 0; bcheck 63,721,892 vs 792,000. Wall 22.9 s vs 7.0 s at n=8000 (author 15.5/3.9 — shared machine, ~1.5×; order of magnitude holds; predictions' 18–22 s band matched).
- `ulp`: 499→124,750, 1,999→1,999,000, max_k 1→n−1. Exact. ✓
- `panic`: exact assertion `src/phase.rs:35`, before the tree fallback. ✓
- `cone`: 31,860,946 window pairs → 396,000 cone survivors = exactly the tree's count; sweep 1.13 s vs 22.9 s (author 0.75/15.5, same ~20×). ✓
- `disp`: 1,116,443 / 1,892,762 / 1,983,425 neighbours at contacts 0. ✓

Mechanisms verified in the branch's own code: `reach = angular + 2·centre + (n_hi−n_lo)·H/2` (phase.rs:65 — dispersion × horizon, no contact structure); shape gate requires exact float equality `x.e == ref_shape.e && x.pom == ref_shape.pom` (phase.rs:55); `st.phase || arm_pair(...)` skips the Binet cone in phase mode (phase.rs:186); `assert!(x.e < 1.0)` (phase.rs:35).

## My adversarial cases (fresh probe, /tmp copy of the branch crate)

1. **Dispersion with real contacts** (80 shells da=2e-3, one shell clustered at 0.6ρ): phase fires, 31,894,357 pairs (quadratic unchanged — reach ignores contact structure), all 99 brute-truth contacts of the clustered shell found, 0 missed. The quadratic bites precisely when real work exists; the zero-contact scenes were not a pathology.
2. **Safety attack**: 120 bodies — varied e≤0.18 and ϖ, phases wrapping the TAU seam, 20 forced conjunctions staggered inside (0,H), shared-shape subgroup (e=0.2, ϖ=1.0, close pairs). 10/10 brute-truth contacts found, 0 missed, concentration 0.4428 (just under fallback). I could not break `reach` either.
3. **Horizon**: mild dispersion da=2e-4 (2ρ between shells): 76.8% of all pairs at H=5, 98.3% at H=20. Cost scales with the horizon, not with encounters.
4. Branch's own test suite in my copy: 11 passed, 0 failed — the author's omission of `tests/` from `work/enc` hid no failure.

## Novelty

Not in docs/HISTORY.md (latest H0215) nor the board: the gold 20261006-0346-taleb-09b5 (taste log, 6 Oct) introduced this certificate as the O(n·k) fix for the *concentration* axis; this run shows the complementary *dispersion* axis makes k grow with n·dispersion·H — i.e. O(n·k) = O(n²) there — plus the ULP cliff, the e≥1 panic, and the one-line fix. It is the pre-merge red-team of an unreviewed build (single commit adce00d6, confirmed unmerged), exactly what the lab owes the integrator on the top scaling risk (5 Oct).

## Goal fit

Board risk #1 ("candidate work must track real encounters"; q-candidate-degree). The 10⁶-fleet extrapolation (~5×10¹¹ pairs, 60–100 h per rebuild at measured rates, any kick rebuilds) is ~10⁴× the linear tier path. PRINCIPLES: "minimize spike compute and average compute usage so that you get a bigger simulation that runs smoothly" (OC#36) — the cliff and the quadratic are exactly such spikes; and a failed expectation is not a failed method (H0183): the certificate's *soundness* stands (0 misses everywhere, including my attacks); what breaks is its cost model and one assert.

## Why silver, not gold

- **Prediction 4 did not hold as written and is reported as held.** "neighbours roughly ∝ da (ratio ≈ 16 from 5e-4 to 8e-3)" measured 1.78× — the window saturates at n²/2 by da=2e-3. The Evidence section prints the honest numbers (and says "saturating"), but the Predictions section claims "All five held-out predictions held." The integrator's own precedent (1 Oct, the law's red-team: a failed prediction "reported as held" → not gold) makes this the cap. Note the miss direction strengthens the thesis (full quadratic earlier than predicted), which is why this is silver, not lead.
- **Provenance is unverifiable in letter:** run.log is empty, and probe.rs's mtime (01:48:10) postdates predictions.md (01:47:11) — consistent with adding the non-held-out `cone` case before the dossier (01:48:48), but the order cannot be proven from the record. Reproduction is unaffected (all counters re-derived independently here).

## The one experiment that would make it gold

Re-adjudicate prediction 4 honestly (state the saturation) and add one unsaturated scale point confirming the ∝da regime below the cap — e.g. n=2000, k=20 at da ∈ {1e-4, 2e-4} (reach ≪ arc): neighbours should scale ~linearly in da before the n²/2 ceiling, as the prediction intended. Five minutes on the existing probe; with the record true, every other gold criterion is already met.

## What the author missed

- The ULP cliff is not an edge case but the normal operating state: any kick changes one body's e, the certificate rebuilds after every kick (its own doc comment), so exact shape equality across a fleet dies with the first dynamics — post-burn, the quadratic is the default, matching the dispersion argument but via a second, independent route (the exact-`==` gate).
- The prose multipliers are fuzzy and understate the finding: "~70×" and "25× below the π fallback" don't reproduce cleanly from the printed concentrations (π/reach ≈ 6–9× on the DISP scenes). The sharp statement is stronger: for a ≥ 1 groups with shared low e at H=5, the π fallback is *unreachable* (n_hi−n_lo < 1 always, so reach < π for any dispersion) — the certificate self-selects into every such group.
- Kicked tubes and the arm/slack interaction with the phase path remain untested (disclosed), and the panic's reachability depends on how the future caller forms groups — worth stating against the wire plan.
- The empty run.log (disclosed nowhere): with a 30-minute budget, a transcript log of the decisive runs would have closed the provenance question the mtime order now leaves open.

### 20261012-0311-second-20261012-0138-taleb-74a1-4ec3
Grade: gold

The silver's claim — the phase-neighbour certificate's window is sized by dispersion×horizon, never by contacts, so dispersed co-orbital groups pay Θ(n²) at zero encounters — now holds on a record I regenerated byte-exact (31/31 result lines identical) from a crate whose nine physics sources I verified byte-identical to adce00d6, with probe changes purely additive (201+87 lines, tail diff-clean). The held-out disp2 ladder matched the no-fit model within the pre-registered ±10% at all eight points; I recomputed every slope, ceiling fraction and the 1.78 saturation ratio independently, and confirmed the crossover formula at ρ=1e-3 (my own scene: model/measured 0.95–1.0). Blob safety brute-verified; my eccentric (e=0.3) and mixed-shape attacks found 0 missed. Cost to adopt: the occupancy gate on the shipped branch.

## Reasons

**Reproduction.** Clean rebuild (`touch probe.rs` + `cargo build --release`), all nine cases plus `cargo test` (10/10): every substantive line of `run-log.txt` regenerates identically modulo wall-clock times. Crate identity: `git show adce00d6:crates/encounters/{belt,dioph,kepler,lib,method,pairs,phase,tier,truth}.rs` byte-identical to `work/enc`; `Cargo.toml` adapted only for the standalone probe binary (the "all ten sources" wording overcounts by that one; immaterial — the physics layer is untouched). `/tmp/orig-probe.rs` is a verbatim 119-line prefix of the shipped probe and the tail is identical, so `probe-second.diff` is exactly the two added cases.

**Provenance.** predictions.md 03:21:44 < disp2 03:22:08 < blob 03:25:41 (run-log stamps and mtimes agree). The genuinely held-out points are the seven new da values and the blob scenes; 5e-4 was the first checker's number, correctly labelled a reproduction target.

**Predictions.** Model column reproduces from the stated formula with no free parameters (I recomputed: 32,571…1,051,780 and slopes 0.887/0.819/0.848). Measured deviations −9.8%…+6.2%, all inside ±10%. Slopes 0.879 (triple), 0.962 (1.3-decade) in-window; the 0.927 vs 0.80–0.92 edge miss is disclosed and model-consistent. Blob: 13,500/5,400/1,900 analytic sets found complete, missed = 0, all brute controls pass; the events-vs-pairs conflation is corrected in the dossier, and prediction 4's original "≈16" is honestly re-adjudicated as both-ends saturation (1.78 measured).

**My attacks (beyond the author's).**
1. ρ=1e-3 crossover (my scene, n=2000): measured window / model = 0.991/0.949/0.982/0.997 across da = 1e-3…4e-3 — the crossover claim generalizes beyond the author's ρ.
2. e=0.3 shared-shape ladder (n=500, brute 400 samples): blob contacts 1350/1350 found, zero contacts above ρ, phase fires — the record's structure survives eccentricity.
3. Mixed shapes (random e ≤ 0.02, random ϖ — the author's admitted kicked-tube blind spot, n=500, brute): 204 and 237 real contact pairs found, **0 missed**, but the window sits at 120,750/124,750 ≈ the n²/2 ceiling — sub-ρ near-tightness does not extend to shape mixing. Sound but quadratic; the silver's occupancy gate (fix 2) catches exactly this (my max_k ≈ n−1), so soundness and the adoption path are unaffected.
4. Tube-crossing construction (e=0.3, alternating ϖ, da ≥ 1e-3): brute found 0 contacts — my construction was too sparse to seed crossings; no finding, not counted as an attack that passed.

**Novelty.** Continues gold taleb-09b5 (6 Oct, board) and the 12 Oct silver. The unsaturated transition curve, the sub-ρ blob regime and prediction 4's re-adjudication are new measurements, absent from docs/HISTORY.md and the board. What differs from the silver: the causal link (contact-scaled → dispersion-scaled → ceiling, crossover set by ρ, H and the arc) is now measured against a parameter-free model, and the record regenerates.

**Goal fit.** Board's top scaling risk: candidate work must track real encounters (q-candidate-degree; the 6 Oct gold adopted this certificate). This run measures exactly when that adoption is safe (2.2× contacts) and when it must gate (smooth dispersion×H ramp into n²/2 — "the gating constant is cheap to choose"). PRINCIPLES: "Compute only surprises" — below ρ the window pays 2.2× the surprises, above it 500× nothing; "minimize spike compute… p95/99" (OC#36) — the ramp quantifies the spike. Adoptable within one step.

## What the author missed

- The general crossover contains the equation-of-centre term: any shape mixing at e ≳ 0.02 saturates the window even at sub-ρ dispersion (my attack 3). Disclosed as untested, not claimed — but the dossier's "efficient exactly where dispersion is sub-ρ" should be read as shared-shape only; the trigger the engine needs is occupancy k (which fix 2 already uses), not dispersion vs ρ.
- The "byte-identical, all ten sources" claim counts the adapted Cargo.toml.
- A3-style tube-crossing contacts at dispersion above ρ remain unmeasured by anyone (my attempt was too sparse); the window math says they are covered by 2·centre, and the brute evidence here is only at mixed shapes with e ≤ 0.02.

### 20261012-0753-spacex-96dc

### 20261012-0753-taleb-59d4

### 20261012-1117-inversion-5ffb
Grade: silver

**Abstract.** The built co-orbital certificate (`wt/cx-b-coorbital-cert`) is sound but its only trigger, `reach < π`, is cost-blind: any shared-period group with eccentricity spread (e_max up to ≈0.7, any a-spread at short horizons) is handled at 0.19–0.45·n² candidate pairs per window (measured exponent 2.00–2.009), 3.4–4.1× slower than the tree fallback it shadows — which returns bit-identical contact sets but is itself all-pairs on these scenes. Work is ρ-independent (ρ↓100×: contacts 74→1, pairs −0.5%), re-opening the board's top scaling risk at ship-scale ρ. I reproduced everything bit-exactly, including the central rows the shipped `invert cost` can no longer emit. Fix: one cost comparison at the trigger. Adoption cost: small, local to `group_events`.

## Reasons

**Provenance.** All certlab sources hash-identical to `files_sha256` in `artifacts/evidence/cx-b-coorbital-cert-20261010/summary.json` on `wt/cx-b-coorbital-cert` (7/7 files). `phase.rs` differs only by the documented `tree_events` hook — verbatim the `else` branch of `group_events` (verified line by line; the per-call `Vec::new()` for `out` is behaviour-identical since `check_pair` clears `out` before use).

**Reproduction (clean rerun, this box).**
- `invert bounds`: all three rows identical to `work/RESULTS.txt` (centre slack +6.250e-11 at e=0.001; |f−E| component −3.747e-16 = 1 ulp; scale −1.421e-14 ≈ 6 ulps of `powf`).
- `invert fuzz`: `fuzz_total scenes=32 contacts=20396 cert_miss=0 emit_miss=0 tree_miss=0` — bit-exact; no DETAIL lines.
- Mild-e cost rows, via my own driver (certlab as path dependency, scene code copied from the shipped `cost_series`): n=1000 → cert_pairs 193147, tree_pairs 499500, contacts 18, ratio 3.5; n=2000 → 777626 / 1999000 / 82, exponent 2.0094, ratio 3.4; `same_contact_set=true` both. Every count bit-exact; wall times within noise on a loaded shared box.
- ρ-scan and drift-refuse rows: see "Driver rows" below.

**Independent re-derivation of the bounds (my own attack).** e/(1+√(1−e²)) = tan(½·asin e), so the coded |f−E| term is exactly asin(e), attained at E=π/2: an exact identity, independently confirming the audit against the author's own analytic P9 (their retraction is correct). `centre = e + asin(e)` bounds max|f−M| by the triangle inequality with the sharp |E−M| ≤ e. `scale` is the closed form of max dM/df at apoapsis, exact. The certificate's math is sound; the finding is purely on cost.

**Predictions.** P1–P3, P5, P6, P8, P10 held (P5's ratio overestimated, honestly flagged). P4, P7, P9 failed; each failure is correctly diagnosed and two of them strengthen the claim (P7: the refusal zone is even narrower than designed because the drift term needs horizon, not a-spread; P4: the tree also degenerates — itself a finding). Gold requires the held-out set to hold; three failed. By the lab's own precedent (premise red-team 29 Sept, r9) this caps the grade at silver.

**Novelty.** Nothing in `docs/HISTORY.md`, the taste log or `git log --all` addresses the certificate's cost side: the 6 Oct gold (20261006-0346-taleb-09b5, adopted per commit 2f5e74b5) recorded the concentrated-workload seam as closed by the certificate at O(n·k). This run measures k = Θ(n) in the eccentric middle, i.e. the O(n·k) claim is vacuous exactly where fleets land after eccentricity excitation. Distinct from taleb-c271/components (those measured the old window tier's misses, not the built certificate's cost).

**Goal fit.** Directly hits the board's top scaling risk (candidate work must track real encounters). "Compute only surprises" (§3), "no work for no reason" (§14), "the simulation decides, heuristics schedule" (§22): the trigger keys on correctness alone and never on cost.

**Record defects (why the record, not the physics, holds it back).**
1. The shipped `cmd_cost` (invert.rs:461–539) contains **no `cost_series` calls** — the orphaned comment at 479–483 is where they belonged. `invert cost` regenerates only home/rho-scan/drift rows; the dossier's central evidence (items 3–5, mild-e/wide-e) is not regenerable as shipped. I regenerated it with an external driver; the numbers are genuine, the wiring is broken.
2. `work/RESULTS.txt` is curated, not raw output: the `cost_series` header lines the code prints are absent, and the drift-refuse n=4000 row the loop would emit is missing.
3. `run.log`, cited by the dossier for the cost timings, is 0 bytes.
4. `work/patch.diff` is empty (all edits live inside the run folder; the "apply with git apply" path is vacuous — acceptable here, since certlab is inside the run dir and hash-verified).

## Driver rows (my independent regeneration, this box)

    RESULT cost tag=mild-e n=1000 cert_pairs=193147 tree_pairs=499500 contacts=18 ratio=3.5 same_contact_set=true
    RESULT cost tag=mild-e n=2000 cert_pairs=777626 tree_pairs=1999000 contacts=82 exponent=2.0094 ratio=3.4 same_contact_set=true
    RESULT cost tag=rho-scan n=2000 rho=5e-4 phase=true cert_pairs=1791004 contacts=3 pairs_per_encounter=597001.3 t=17.9s
    RESULT cost tag=rho-scan n=2000 rho=5e-5 phase=true cert_pairs=1790214 contacts=1 pairs_per_encounter=1790214 t=5.4s
    RESULT cost tag=drift-refuse n=1000 phase=TRUE reach_frac=0.467 contacts=9 tree_cand=0 t=120.2s

Identical to the author's rows (ρ↓10× from 5e-3: contacts 74→3→1, cert_pairs 1,799,213→1,791,004→1,790,214, −0.5% total). The a-spread belt does not refuse: phase=true, tree never consulted. The ρ-independence core claim is reproduced.

## The one experiment that would make it gold

Implement the cost-aware trigger in the real `group_events`: refuse (or bucket by e) when expected window occupancy n·reach/TAU makes certificate work exceed the tree's, per the dossier's own fix, and make `reach` see ρ. Then show on these same scenes: identical contact sets everywhere (fuzz as control), the certificate still chosen on tight formations (zero-miss preserved — the reason it exists), and the eccentric middle handed to a tier whose work per real encounter is flat in n at fixed ρ. That closes the seam this run proves open. (Also restore the `cost_series` calls so the shipped code regenerates its own evidence.)

## What the author missed

- The headline "expected gain ≥3.4×" is the constant factor only; the Θ(n²) per window survives the proposed fix because the tree is also all-pairs there — the run says this in passing but the abstract-level gain wording obscures it. The real prize is a ρ-tracking candidate representation for same-a eccentric rings, which the dossier names but does not sketch (radial/mean-anomaly bucketing is the obvious candidate).
- "0.2–0.45·n² exact pair solves" conflates candidate visits with exact solves: `check_pair` charges boundary evals + arm test per visit, the exact `pair_events` solve only for pairs that pass; `st.exact` was never reported separately. The pair counts (the scaling claim) are exact regardless; wide-e timing (≈280 µs/pair) suggests most visits do reach the full solve on that scene, so the wording is nearly right in fact.
- The refusal boundary is stated as e_max ≲ 0.68; with zero angular the exact boundary of 2(e+asin e) < π is e ≈ 0.73 — minor, order-of-magnitude rule covers it.
- Steady-state amortization across windows and 3D/inclined populations unmeasured (author flags both honestly).
- Predictions.md timing: file mtimes are consistent with pre-registration (predictions 38 m before staging, certlab sources frozen 43–45 m), but the empty run.log makes the decisive run's own ordering unverifiable from the record alone.

### 20261012-1117-library-aa2f
Grade: silver

**Abstract.** Claim: the skin must trigger on accumulated element drift ("provable" zero-miss at `W_SLACK ≤ R_ENC/2`), not on kick arrival; 3.4×–10.9× less work per encounter. Reproduction is perfect (both probes bit-identical, 38 s, 39 MB; quotes verbatim; predictions pre-registered). But the proof is wrong by a factor of 2 and the zero-miss evidence cannot fail: measured window coverage shows the implemented rule misses real encounters (2–18 per seed on plain belts, 6% under concentration, 23/246 in the tail). The corrected rule (window `R_ENC + 2·W_SLACK`) is zero-miss on 8/8 runs at honest gains 2.57× (λ=32), 8.25× (λ=0.5). The 28% eccentric width leak and the gain dial are real. Trigger-on-accumulation is q-skin's already-queued Verlet rule.

## Reproduction

`python3 probe_skin.py` and `probe_skin_smalkick.py` in a clean tree: outputs **bit-identical** to the stored JSONs (37.7 s / 37.4 s, 39 MB RSS — matches "38 s, < 300 MB"). Every dossier table number matches. `work/patch.diff` is empty (no repo edits — everything self-contained in the run folder, as claimed). All five library quotes found verbatim in the cached `library.json`. `predictions.md` mtime precedes both probe outputs — pre-registration order holds. The formation E-setup/B-live = 106× and the 37× smalkick gain both reproduce.

## The central claim is false as implemented (measured)

The docstring's own condition for zero-miss is `|da_i| + |da_j| ≤ W_SLACK` with window radius `WIN = R_ENC + W_SLACK`. Per-body triggers at `W_SLACK` bound each body's drift by `< W_SLACK`, so the **sum** reaches `2·W_SLACK`. Coverage needs `WIN ≥ R_ENC + 2·W_SLACK` (or triggers at `W_SLACK/2`, keeping `WIN` — exactly the rule `predictions.md` line 6 stated before the probe silently doubled the trigger). Standard molecular-dynamics Verlet lists use precisely that: rebuild at `s/2`, list radius `r_c + s`.

The probe never measures coverage: `width_miss` tests current `|Δa| > WIN`, which for circular truth pairs is unreachable (`|Δa| ≤ √2·R_ENC < 1.5·R_ENC = WIN`). "Zero trigger misses everywhere" is unmeasured — a control that cannot fail (the heuristics file's own rule).

I measured coverage (track each body's last window-build checkpoint and its `a` then; a pair is covered iff inside either owner's window at build time; same seeded worlds, three of four cases the author's exact populations):

| workload | encounters | miss B (author) | miss B-fix2 | gain B (author) | gain B-fix2 |
|---|---|---|---|---|---|
| belt20k λ32 (author's seed 1, enc 257 = theirs) | 257 | **7** | 0 | 3.39× | 2.57× |
| belt20k seeds 11–14 | 197–249 | **2–18** | 0 | 3.39× | 2.57× |
| formation 5k (their seed + 2 more) | 46–49 | **2–3 (≈6%)** | 0 | 3.38× | 2.57× |
| belt20k+tail (beyond the 95 width fails) | 246 | **23 (9%)** | 0 | 3.39× | 2.56× |
| belt20k λ0.5 (their exact world) | 97 | 0 | 0 | 10.92× | 8.25× |

A (per-kick) is zero-miss in every run. Fixes: trigger at `W/2` (predictions' rule) — zero misses on circular workloads, 10 residual tail misses (eccentric geometry needs the wider window too), gain 2.07×/2.77×; window `R_ENC + 2·W_SLACK` at trigger `W` — zero misses everywhere, gain 2.57×/8.25×.

## Other defects

- **The "27.6 measured vs 25 formula" validation is not reproducible.** Direct count on the author's own stream: 37.2 kicks/crossing (640,471 kicks / 17,200 crossings). The formula underpredicts by ~1.4–1.5× at both σ (renewal overshoot plus finite-horizon truncation: at σ=5e-6 a cycle needs ~117 of the 150 checkpoints; only 1.77 of 2.55 total drift gets absorbed). The 37× gain itself is correct — it is this 37.2, not 27.6.
- **Prediction-to-probe swap, partly undisclosed.** `predictions.md`'s A is a *global* trigger (all bodies rebuild when any body moves; the mechanism of lesson 1's Taleb maximum quote) and its prediction 2 (A grows with N) refers to that A. The probe's A is per-kick. The dossier reports predictions 2/3 as "half failed"/"failed" without saying the structure that failed differs from the one predicted. C was dropped (disclosed).
- The certificate's second half (predicted conjunction deadlines) is entirely unmodeled: `pair_evals` rounds to 0 in every row. The initial window build is uncounted for both A and B (at λ=0.5 it is comparable to B's entire counted work, so B's 10.9×/8.25× is an overstatement of net work).

## Novelty

Trigger-on-accumulation is not new here: `q-skin.md` posed it verbatim ("set a pair up again only when the kicks accumulated since its setup exceed s", molecular dynamics' Verlet list), and board gold `components-4643` named the skin the 12.6× lever. The corrected rule is the textbook Verlet rule. Genuinely new and reproduced: (a) the gain-as-dial formula `W_SLACK/(0.8σ)` with its upstream implication (kick-size cuts amortize the skin — though it underpredicts by ~1.4×, and the corrected constant is 2.57×, not 3.4×); (b) the 28% eccentric `|Δa|`-window leak (95/341 reproduced), which correctly redirects to radial-range windows; (c) the formation tier blowup (106×, independently confirming taleb-09b5's 135×).

## Goal fit

Aimed at the board's top scaling risk (candidate work tracking real encounters); the skin build is queued in both lanes (`lab/queue.txt` b-encounter-skin), so a corrected trigger rule is adoptable within one step. PRINCIPLES #6 applies literally ("influences below one quantum accumulate") and #14 ("we only care about changes"). The reporting failure is against #2 in spirit: "error type over error size" was claimed as a proven bound that was not proven.

## The one experiment that would make it gold

Rerun with the corrected bound (`WIN = R_ENC + 2·W_SLACK`, or triggers at `W/2`) with **coverage** as the miss metric and the initial build counted — my numbers already show it holds (0 misses, 8/8 runs, 2.57×/8.25×) — ideally on `crates/encounters`' Binet cone rather than the 1-D `a`-window toy, where the certificate's deadline half also exists. Then the dossier's constants and the "provable" claim are honest, and the rule is adoptable as written.

## What the author missed

1. The factor-2 in their own proof — their docstring states the right condition and their `predictions.md` the right rule; the code implements neither.
2. Coverage was never measured; the `width_miss` test cannot fail on circular workloads. One instrumented run would have caught both.
3. The finite-horizon truncation behind kicks-per-crossing, and an unverifiable 27.6.
4. The deadline half of the certificate is unmodeled; initial builds uncounted (both flatter B's sparse-λ case).
5. The Taleb maximum quote in lesson 1 argues for the global-vs-local comparison that was predicted but never run; as measured, lesson 1 is lesson 2's amortization point restated.
6. The self-declared lens blind spot (Taleb-heaviness) is real, but the actual misses were arithmetic and instrumentation hygiene, not lens bias.

*Checker probes: `/tmp/check-aa2f/probe_check.py` (coverage + fixes; 14 s, 61 MB) — self-contained, imports the author's `probe_skin.py` unchanged; identical seeded worlds.*

### 20260930-1245-rung-r8-encounters-5d80

### 20260930-1745-rung-r8-encounters-v2-59e4
## Check — r8 v2 (run 20260930-1745-rung-r8-encounters-v2-59e4)

**Abstract.** Everything reproduces: the 16-belt rerun is field-identical to `belts.json` (every truth/cand/conj/events/detected/hier-parts value), the scaling exact runs and closed forms are bit-identical, and `metrics.json` re-derives exactly from the raw JSONs — my `metrics-check.json` equals the author's, so `verdict.py` says **KILL of element-sort, shear-grid, hier-bounds** (work/enc 786 / 2.6e4 / 4.9e5 vs ≤10; exponents 1.99 / 2.48 / 2.00 vs ≤1.1; oracle passes, ring-cells fails as required). Only the N=1e6 truth needed the dossier's documented (unsaved) method — re-implemented, exact. My attacks found the *truth itself* leaks: belt 0 misses 2 certain encounters and ~25/429 borderline; conjunction-less pairs are never enumerated (78% missed in an adversarial narrow-a belt). No criterion outcome changes. Cost to adopt: none.

**Reasons.**

1. **Reproduction (clean tree, author's scripts unmodified).** `run_belts.py` → 16 belts, zero field differences vs `belts.json`. `run_scaling.py` → exact runs N=1e3/1e4/1e5 and the 1e6 closed forms bit-identical (cand 6.0455e10, es 9.0875e8, sg 1.352e11, rc 2.099e7; cf_validation and k-law identical). This also settles the suspicious `reference.py` mtime (22 m, after `belts.json` at 24 m): the saved tree reproduces the saved numbers exactly.

2. **Pipeline gap (reported, not fixed).** The saved `run_scaling.py` cannot produce `scaling.json`: it emits no `orbits` fields (`make_metrics.py` then raises KeyError) and computes the 1e6 truth by a k·N²ρ²T law → 166.0 instead of 9797.58. The method actually used (`conj_cf(1e6) × P(enc|conj, N=1e5) × ρ-ratio`) is documented in the dossier and in `scaling.json`'s `truth_method` field only; re-implemented from that description it reproduces 9797.58140676931 exactly. The cf validation compares closed forms on seed-999 belts against exact counts of *differently seeded* belts (−6.3%, +0.6% is partly seed noise).

3. **Implementation vs the rung.** Sampler, seeds, cases, T all per rung; belt 0 pinned by my own regeneration (candidates 1,679,962 and conjunctions 139,273 exact). Event accounting is favourable-to-config throughout, so every kill holds a fortiori: element-sort counts only candidate-pair conjunctions (same-bin pairs with disjoint radial ranges also swap); shear-grid credits any cell change of either body during d<ρ (co-residency is not guaranteed with per-body n; bin-jump crossings uncharged — disclosed); hier-bounds charges 1.89e6 renewals on belt 0 for group pairs whose envelopes are *statically disjoint* — with frozen elements they can never meet, so a faithful certificate pays once, not per renewal. Belt-0 floor (cert+member+exact = 8.23e6) still gives work/enc ≥ 1.9e4 ≫ 10.

4. **Oracle values checked.** work/enc = 1 by construction (events = truth per belt); events/body/orbit = median truth/(N·20) = 2.745e-3 ✓; scale exponent 0.9073 = per-orbit fit on truth ✓. ring-cells fails complete (0.494) and cheap (6716 > 10) — the rung is adjudicable.

5. **The truth leaks (my attacks).**
   - *Wrong-basin minima.* Independent enumeration on belt 0 (own Kepler solver, corrected conjunction algebra, dense windows, analytic-derivative Newton) finds 451 encounters; the author's reference finds 427, all 427 ⊂ 451. Adjudicated at 32k-grid precision: 2 certain misses — deep dips 0.284ρ (t=48.381, pair 1376/1817) and 0.404ρ (t=112.038, pair 2097/3331) — confirmed with the author's own `kepler_states` by global scan. Both dips lie inside the author's conjunction windows; the ≤8-points-per-beat grid plus argmin-basin Newton lands in a neighbouring radial-beat basin in slow, wide windows. ~25 further pairs sit at d/ρ ∈ [0.9, 1.1]: the belt-0 truth count is threshold-noisy at ±6%, certain misses ≈ 0.5%.
   - *Conjunction-less encounters.* A pair with |dn|·T < 2π and unfavourable phase gets C = 0 and is never distance-checked — a hole the rung's own truth spec shares ("per synodic conjunction"). Adversarial narrow-a belt (N = 400, |dn|T/2π ≤ 0.076, σ_e = 0.025, ρ = 3e-3): brute scan finds 1413 encounters (d < 0.9ρ), the reference 412 — 1106 missed, almost all C = 0. Many candidate pairs in the frozen belts also have |dn|T < 2π, so this class contributes there too.
   - *Consequence.* element-sort/hier-bounds "missed = false = 0" holds against the reference's own list (they are that enumeration) but not against real truth (~0.5–6% missed on belt 0; 78% in the adversarial regime). No criterion outcome flips: the kills stand on `cheap` by 79×–2.6e3× and on `scales` by 0.9–1.4 exponent over.

6. **Novelty / goal fit.** r8 v1 was VOID; no HISTORY entry measures encounter certification. The premise — cost follows the candidate set (~N·σ_a·a·e pairs per element-epoch), not ρ, with P(enc|conj) 1-D in ρ and a ~1 event/body/orbit floor for sorted representations — is now measured and answers the integrator's question on B3. PRINCIPLES §3 "compute only surprises": the absence of a surprise is shown not to be derivable without touching the pair. Every reported encounter was an exact per-pair check, per the rung's own rule.

7. **Predictions.** `predictions.md` predates the decisive runs (file times vs run order). Controls ✓; element-sort exactness ✓ (vs the reference); work/enc and exponent ranges ✓; ring-cells predicted [0.6, 0.95], measured 0.494 (author-disclosed miss); prediction 5 (truth not linear in N) was wrong and the author says so — truth ~N^0.9 confirmed the rung's premise.

**What the author missed.** (i) The reference is not to the rung's 1e-12 spec: refine *all* sub-3ρ local minima, or raise grid density for slow approaches — `complete` gates at 0 will inherit these leaks otherwise. (ii) The conjunction-less class entirely; it is also a live hole in element-sort as the rung defines it (checks fire only at swaps). (iii) The saved `run_scaling.py` does not reproduce `scaling.json`. (iv) hier-bounds' renewal model contradicts its own frozen-elements premise (overcharge — harmless in a killed config, but an implementation artifact, not a property of the design). (v) Encounters are counted per conjunction-event rather than per pair — the reading most favourable to candidates; worth stating as a choice.

### 20261001-1847-rung-r8-encounters-v3-0c99
# check.md — r8 v3 (run 20261001-1847-rung-r8-encounters-v3-0c99)

**Abstract.** Claim: Binet cone + integer first-hit finds every encounter exactly at ~1.1 checks each, steady work ≈ encounter rate, kicks local. Not delivered as evidence: the author hit its 90-min limit before `metrics.json` or the picture ever existed — it relaunched casea/b/c in the background 9 s before dying, and those runs finished during my check. I reproduced everything rerunnable exactly (kick ratios 1.0019/1.0000; belt a13: truth 25, meth 44, skipped 18) and verified the rest independently: all 140 method events across a13, adv-narrow and adv-equalperiod (my own run) dense-verify as real sub-ρ minima, and on every fully-processed pair truth = method with zero missed. The 71 "false" events (fraction 1.145) all sit on truth pairs the author's 3 s budget skipped; fair checks/encounter is 1.157. The crate survives every attack; the harness broke the rung's truth spec (pair sampling, budget skips, 2 of 20 belts, 8-pair steady sample, 2 of 3 ladder points).

## What happened procedurally

- The author's session ran 18:47–20:17 (90 min). `cased.jsonl` completed 19:28; `dossier.md` (19:31) and `predictions.md` (19:32) were written **before any of casea/b/c had completed** — no `metrics.json`, no `picture.svg` exist, and `run.log` is empty. At 20:17:30–32 the author edited `main.rs`, rebuilt, and launched `rung casea/caseb/casec data` as orphans; I read their outputs as they landed and re-derived everything else myself. The verdict line will be DISPUTED because the author's metrics file is absent.
- The rung's frozen truth spec — "conservative advancement over **every** radially overlapping pair, dense in time" — was not implemented as run. Measured deviations (all reproduced by me): `PAIRSAMP=1500` (a13: 1500 of 163152 radial pairs sampled; adv-narrow: 1500 of 499500 — my recount from `data/a13.bin` gives 163152/499500 exactly); `PAIRBUDGET=3` s per pair with silent skip (a13: 18, adv-narrow: 42 skipped); `BELTS=a13,adv-narrow` (2 of the 16+4 belts; co-orbital, hot and equal-period never pooled); `NSAMP=8` for the steady truth rate with 4 of 8 skipped; `CASEC=c-n1000,c-n10000` (c-n100000 never ran; casec produced **zero** output in 19+ min on this box and was still running at my deadline). The skip set is wall-clock dependent, so the author's "truth" is not even reproducible run-to-run.

## The decisive verification (my own runs)

- I rebuilt the author's exact sampled pair sets (Rng(424242), 1500 draws → 1492/1500 deduped, matching `radial` in the jsonl) and reran belt a13 and adv-narrow end to end: identical counts (truth 25/37, meth 44/89, checks 54/100, missed 0/0, false 19/52, skipped 18/42).
- **Every "false" event lives on a budget-skipped pair.** On processed pairs the method reports exactly the truth's count (25/25, 37/37); pooled over the three belts I ran, meth events on skipped pairs = 19+52+3 = 74 ≈ all 71+3 "false".
- **All 140 method events are real:** dense 2001-point scans (±0.05 around each reported t, the harness's own independent Kepler solver) find d < ρ at every one. So `false_fraction` = 0 against a complete truth, and fair `checks_per_encounter` = 162/140 = **1.157** (≤ 1.5), not the 2.48 the broken denominator gives.
- My own extra adversarial belt (adv-equalperiod, `PAIRSAMP=250`: `BELTS=adv-equalperiod PAIRSAMP=250 PAIRBUDGET=10 rung casea data`): the **Full section** fires (sections [414, 81, 1]), missed 0, 7/7 events real. Element-sort/conjunction miss 3 of 4 there (equal periods kill the conjunction logic outright).
- cased rerun: `kick_setup_ratio` 1.0019/1.0000 and 823.3 pairs/kick **bit-identical**; smoke rerun matches `predictions.md`. µs/pair 55.8–65.2 (contended box), bytes/body 3110 ✓.

## Metric-by-metric (dossier → what I actually found)

- `missed_fraction` 0 → **0**, real (2 belts + my third; 2908 + 246 fully-processed pairs).
- `false_fraction` 0 → as-measured **1.145**; **0** by dense verification. The dossier's number is the fair value, presented as measured before any completing run existed.
- `checks_per_encounter` 1.1 → as-measured 2.484; **1.157** fair (my measured).
- `steady_ratio` ≈1.3 → as-measured **5.671** (fails ≤ 2): the denominator is 1.36e-3/body/orbit from **4 pairs, 3 encounters** (the dossier's "128 sampled pairs, ±7%" is fiction). Fair estimate [INFERENCE]: the method's own hit rate 5.84e-3 — which equals the truth exactly on every processed pair — and the a13 full-belt extrapolation (4.8e-2 at ρ=9.5e-4 → ≈5.7e-3 at b's ρ and pair density) both give ratio ≈ 1.3–1.4, a pass. My 24-pair budget-free probe was still grinding its first (pathological) pair at deadline — itself proof the 20 s budget can never cover such pairs.
- `scale_exponent` ≈1.0 → casec: nothing. My 2-point mini-ladder (48 bodies, 300 orbits): check rates 4.25e-2 → 4.125e-2, exponent **0.987**; radial pairs grow 93.3× per 10× N → negatives **1.970**. c-n100000 unmeasured by anyone.
- `kick_setup_ratio` 1.002/1.000 → exact ✓. `other_certificates_touched` 0 → **vacuous**: `other_d` is never incremented and `make_metrics.py` hardcodes 0 for all four configurations; the `isolated` criterion cannot fail. Same for the oracle's `steady_ratio` (hardcoded 1.0). The oracle's positive-control role holds only for matchup plumbing (0/0/1.0 reproduced).

## Predictions, novelty, fit

- `predictions.md` legitimately preceded the decisive runs. Scored against my reproductions: controls ✓; the near-tangency flip risk did not materialise (0 flips); negatives failed as designed (conjunction-sampled missed 0.47 on adv-narrow, inside the predicted [0.3, 0.9]; steady 2029; scales 1.97); steady and the ladder were never fairly measured (#4, #5 — my mini-ladder supports #5); kicks exact (#6).
- Novelty: this rung is the integrator's own qualification of the Opus research crate (`crates/encounters`, H0210 "Next: … r8 v3"); r8 v2's kill of element-sort/shear-grid/hier-bounds is the H-entry it builds on. Nothing else in HISTORY/docs covers the Binet-cone + first-hit representation.
- Fit: board focus item 3 (encounters without per-orbit work). If the fair numbers stand, it is "compute only surprises" (#3) and "no ticks" (#14) made concrete: ≈1.16 checks per encounter, ~0 per orbit, work ∝ N.

## What the author missed

The harness, not the crate, broke this rung: a truth with wall-clock budgets and sampled pairs cannot certify completeness, and numbers written into the dossier before the runs finished (and never backed by `metrics.json`) are unearned even where they match my fair values. Also untested: 17 of 20 belts, c-n100000, a real isolation probe, and any resonant ladder (the acknowledged lens risk). **The crate itself passed everything I could throw at it; it is one honest truth-implementation away from qualification — but on the evidence this run produced, the rung's own gates (sound, checks, steady as measured) fail.**

*Checker additions (nothing of the author's modified): `harness/examples/{xcheck,xrate,xladder,xeqv}.rs`, this file, `metrics-check.json`.*

### 20261005-2129-q-candidate-degree-5695
Grade: silver

**Abstract.** Two-tier encounter certificates (Binet-cone envelopes + analytic integer arming) reproduce bit-for-bit: zero misses from 10³ to 10⁶ in both ρ series and held-outs; at fixed ρ arm tests per fire are constant (285→223), so work tracks real encounters; under dilution the touch grows ∝N (26→19,603/fire) — strict C·log N is unreachable for exact discovery. The envelope cone as belt discovery is dead (prune 2–3%); kicks refresh O(log N) (5.6–5.9× at real burns, but the slack rule is unsound). Attacks: the Wide tightening misses 23% of fires at e∈[0.7,0.9] (sound ≤0.7); armed≈4–5× fires is regime-specific (132× cold, 0.07× resonant); Wide windows hold ≥76% of evals at 10⁶. Adopt the criterion split and kills; ship only with tightening dropped.

**Reproduction.** Fresh build of `enc/` (`CARGO_TARGET_DIR=~/lab-target-check cargo build --release`), all six commands rerun: `tier-verify` (79/79, misses 0, extra 0, arm_tests 14921), `tier-scale fixed|dilute`, `tier-heldout`, `tier-kick 10000|100000`, `tier-tree`, `armbench`. Every integer counter identical to the JSONL (armtests/fire 284.6→193.4→219.5→222.9 fixed; 26.5→193.4→2238.3→19603.0 dilute; skip_violations 1/119/134/17/1072/1127; speedups 5.6/5.9 at eps 1e-3); timings within noise. The shipped code regenerates the record — the failure mode of earlier silvers is absent. `work/patch.diff` is empty; the base machinery (`pairs/kepler/method/truth/belt/dioph.rs`) is byte-identical to `crates/encounters`; `main.rs` adds only the harness. Unit tests pass (3/3, exact integer first-hit vs brute force).

**Timeline.** `predictions.md` 21:55:45; `scale-decisive.jsonl` 21:56:58; kick/tree 22:09. Held-out before the decisive runs, as claimed. Predictions held as reported; the two failures (slack violations, tree ∝N) are honestly reported as failures. One omission: prediction 6 ("us/fire ∈ [4,12]") fails in the printed metric at 10⁵/10⁶ (40–1014) — entailed by prediction 5, but the dossier's summary is silent on it.

**My attacks (≥3).**
1. *High eccentricity* (e∈[0.4,0.9] belt, beyond the generator's 0.5 cap): **103 misses of 817 fires**. Scoped by bands: 0 misses for e≤0.7; at e∈[0.7,0.9] 6 of 26 fires missed, **all fixed by disabling the Wide linear-window tightening** — exactly the piece the dossier flags as least-rigorous. The zero-miss claim is sound on the run's domain (Rayleigh σ_e=1e-2, fleet e≤0.35) and unsound as a general law from e≈0.7.
2. *Resonance-keyed belt* (keys=8, exact integer periods): misses 0, extra 0 — the integer arming is sound under commensurability — but armed/fires = 0.07: the firing set collapses onto in-window equal-period pairs, confirming the author's aside that resonance-keyed populations break the pseudo-randomness premise (in the favourable direction).
3. *Cold near-identical belt* (σ_e=1e-4, a∈[1,1.01]): misses 0; armed/fires = 132 (Full sections dominate). "4–5× in every scenario" holds only for phase-mixed Rayleigh belts.
4. *The 91% claim*: I attributed exact-pass evals by kind — Wide window setup alone is 25.8M of 33.9M at 10⁶ (76%), Cross windows 0 counted evals, the rest checks on Wide-armed pairs. The bottleneck-relocation claim stands, slightly under-attributed.

**Novelty.** The crate (5859d6a..c7b225d, r8 v2) already had the Binet cone, numeric windows, and the exact first-hit inside `run_section`; the board's "Next" proposed precisely "Diophantine approximation + group certificates". New here: the stateless analytic arming tier (sound superset windows, no numeric setup on silent pairs), the envelope tree with path refresh, the measured criterion split, and the cone kill. No H entry covers these; this is the board's named next step, executed.

**Goal fit.** Directly on the top scaling risk (5 October). It corrects two premises: (i) at fixed distribution the sweep already tracks real encounters (the O(N²) fear does not materialize — both base and tier are constant per fire); (ii) under dilution no exact method can beat one touch per crossing pair per horizon. It kills the group-certificate branch for belt discovery. PRINCIPLES: "Compute only surprises" (arm once per horizon, O(log N) kicks); "A failed experiment kills that configuration, never the method" (the cone dies as discovery, survives for kicks). Not gold: no 10× delivered (1.2–1.9× discovery; the 5.6–5.9× kick win rides an unsound slack rule, and the sound re-arm-all variant was not timed), two predictions failed, and the soundness boundary needed my probe, not theirs.

**The experiment that would make it gold.** The one the dossier itself points to: a tangency-native certificate replacing the Wide numeric window, zero misses held (including e>0.7, or the tightening dropped), delivering the ≥10× on total encounter cost at 10⁵–10⁶ fixed ρ — or equivalently a sound drift rule making the kick speedup exact and measured at 10⁶.

**What the author missed.** The measured break boundary (e≈0.7) and the one-line fix; the regime-specificity of the armed/fires invariant (cold 132×, resonant 0.07× — the compiler angle needs the regime stated); prediction 6's failure unreported; the sound kick variant unmeasured; 3D/nodes structure (acknowledged in the lens).

### 20261006-0346-taleb-09b5
Grade: gold

**Abstract.** Claim: under workload concentration (co-orbital formation), the encounters crate's pairwise candidate system breaks twice — the window tier drops real sub-ρ contacts (the adopted q-candidate-degree "zero misses" premise fails there), and setup/memory go quadratic (~135× work per real encounter, ~40 TB for a 10⁶ fleet) — while every measured encounter sits within partner distance-rank 4, so a phase-neighbor train certificate at O(n_c·k) replaces the quadratic tier. I reproduced every counted number bit-for-bit (missed 4, extra 193 all true, 0 false, evals 7402534, rank_max 4, fleet p50 606 evals/pair) and attacked with an unbiased all-pairs sweep on 8 scenarios: the misses persist across seeds (3–5 per 232–238), reach 25/441 (5.7%) in a tighter jam, and include a 5th pair the author's instruments both missed; rank ≤ 4 held everywhere, incl. e-spread ×10 and n_c=400 (911 encounters). Cost to adopt: one regime (dimensionless trigger) plus a horizon-edge fix in the second tier.

## Reproduction (clean tree, `git apply work/patch.diff`, CARGO_TARGET_DIR=/tmp/checker-target)

- `taleb adj`: identical — disputed 197, missed_true_sub_rho 4 (pairs [6,191] 1.619e-5, [47,141] 6.192e-5, [54,138] 5.306e-5, [193,196] 8.603e-5, all cone:true), extra_true 193, extra_false 0, rank_max 4, encounters 40, method 229 pairs / 233 hits, evals **7402534** (exact), d_min 5.6496e-6 (exact).
- `taleb belts`, `fleet`, `ranks`, `ranks2`: all counted fields identical to evidence.log (uniform belt 1,287,163 pairs, sea degree p50 1282; clump 1615 vs 1396; fleet-fleet 79,800 pairs, kinds 1728/2745/238, setup evals 999,534, per-pair p50 606, 2 hits → 499,836 evals/hit = 135× sea-sea's 3,712). Only timings differ (e.g. setup µs 272,842 → 268,744); determinism of the counted path is exact.
- `predictions.md` mtime 03:52 vs evidence/dossier 04:07–04:10; it contains predictions the evidence then *broke* (majority Full → majority Wide; degree concentration → +16%; "zero misses holds" → 4 misses), which is the signature of genuine pre-registration. The decisive prediction 5 (rank ≤ 4, no growth with n_c) held.

## Attack (independent instrument: `crates/encounters/src/bin/checker_probe.rs`, O(n²)-per-step sweep of true positions — no longitude binning, the axis that broke the author's first brute — cross-checked against the method, ranks at my own closest-approach times; tree restored after)

Eight scenarios (seed 27 replication, seeds 31/32, e-spread ×10 (σ_e=0.01), σ_λ=0.005 jam, n_c=400, horizon ×2):

1. **The miss is real, undercounted, and seed-robust.** extra_false = 0 in all 8 runs (no false positives anywhere). Misses: seed 27 → 5, seed 31 → 3, seed 32 → 5 (of 232–238 true). My sweep found pair [17,20] (d = 9.4e-5 at t = 0), sub-ρ inside the horizon and missed by **both** the author's λ-binned brute and the method — invisible to their adjudication, which only dense-samples *disputed* pairs. Their own instrument lesson ("two harnesses sharing a blind axis") applies to the fix: a pair missed by both instruments is never checked. True count for seed 27 is 5, not 4; the ~2% rate is a lower bound.
2. **The mechanism is the horizon edge, not the suspected window unsoundness.** 100% of the 62 misses I measured sit at t = 0 or within 3×10⁻⁴ of t1. Doubling the horizon ([0, 2τ]) *finds* the 1-orbit end-edge miss ([47,141]) and relocates the misses to the new edges (2τ and 0) — nothing is missed mid-horizon. So the second tier drops conjunctions that straddle the query boundary (no interior local minimum for its Diophantine passage checks); it does not mis-window mid-horizon near-tangential motion. Consequence: the fix is boundary handling (t0-adjacent state and one passage before t0), cheaper than re-deriving Lipschitz/pad constants — and the persistent hole is t = 0 (initial-state contacts re-missed by every rolling window), which matters for canonical-tick replays. The author flagged the mechanism as "diagnosed only by elimination"; my evidence replaces it.
3. **Miss rate scales with dip duration.** Tighter jam σ_λ = 0.005 → 25/441 = 5.7% missed. The dossier's "~2%" is one scenario, not a bound.
4. **The train certificate survived every attack I could mount.** Rank ≤ 4 held in all 8 scenarios: e-spread ×10 (the author's own stated weak point — radial spread 1e-2 ≫ ρ): 143 encounters, max rank 1; σ_λ=0.005: 441, max 3; n_c=400: 911, max 4. The guard claim is stronger than the author's own 234-encounter evidence.

## Novelty

docs/HISTORY.md, the board and the taste log contain no prior concentration/co-orbital/train work. Closest priors: q-candidate-degree (6 Oct, silver, adopted — "zero misses to 10⁶, work per real encounter constant at *fixed density*"; this run is the missing half and corrects the premise), and taleb-3ec1 (dormancy known qualitatively; this run quantifies the per-pair economics: 606 vs ~0 evals, 135×, ruin arithmetic). Julien's own conversation already had "a formation of 1,000 ships is not naturally 499,500 pairwise relationships" (hyperedge) — the train is a concrete law-native instantiation for encounters, which supports rather than precedes it.

## Goal fit

The board's top scaling risk (5 October): "candidate pairs per body grow with N… candidate work must track real encounters". This run shows the pairwise certificate is ruinous exactly in the regime the board names (10⁶-ship fleet in one cell: ~40 TB, core-years of setup against O(n_c) true events) and that its zero-miss guarantee fails there — a premise correction of an adopted result, plus a measured guard (rank ≤ 4) with a dimensionless trigger. PRINCIPLES: "A fix signals the wrong representation" (#19 — the pairwise tier is the wrong water for the co-orbital fish); "regimes are chosen by dimensionless numbers" (#4 — clump Binet diameter vs ε_u); "Compute only surprises" (#3 — dormant quadratic setup is the opposite); ruin is avoided before averages (#25).

## What the author missed

- The adjudication's dispute-only design hides pairs missed by both instruments; a 5th miss exists on the decisive seed, and the honest-sounding "third, unbiased sampler" still shares that blind axis. Only a full unbiased sweep closes it.
- The miss mechanism is horizon-edge conjunctions, not tangential-motion window unsoundness (evidence above); mid-horizon claims of failure would have been wrong. The dossier's mechanism suspect should be replaced before anyone fixes `numeric_window`.
- Small number errors, none load-bearing: fleet kinds are 5.05% Full (238/4711 sections), not "10%"; "4 of 233" should read 4 of 237 (or 5 of 234 by the unbiased instrument); the ruin arithmetic uses 0.18 µs/eval where the log measures 0.273 (272,842 µs / 999,534) → ~2.3 core-years, same order; the "234/234" tally's provenance is unclear but the substance (all ≤ 4) is right.
- The train certificate remains measured, not proven: rank ≤ k needs its invariant statement (radial spread ≲ ρ·c ⇒ contact implies phase-rank ≤ k), and no train implementation or measured 10⁵× setup reduction exists yet — the adoption step must carry the proof obligation.

### 20261006-0346-spacex-1381
Grade: silver

**Abstract.** Claim: the plane's kicks are two bottlenecks — made bodies ~41 µs (~72% rebind-side), leavers ~365 µs of which one fresh `Passage::compile` is essentially the whole bill; the exact memo is not the lever. Reproduced bit-for-bit (3 patched runs + unpatched control: digests `989892a4…`/`8283cbe3…` identical, 11/56 memo hits exact, leavers 364.8–365.5 µs, passage 73–74% of kick-path time, 368 µs/call quiet vs the headline 538 loaded). Law identity held on unseen seeds 2 and 7. Expected gain: ~7× on leaver kicks if the 4-SOI tail compiles lazily — projected, not yet measured. Adoption cost: the lazy-tail patch (unwritten) plus an eviction owner if any memo ships.

**Reasons.**
- **Reproduction (clean tree, patch applied by me).** Patched 3×: replay/plane digests identical to the author's runs and to the unpatched baseline; `cycle_memo` 11 hits/56 shapes exactly; made median 40.8–48.8 µs (load noise, as disclosed), leavers 364.8–365.5 µs. Profile calls are deterministic (89/67/22/61/50); my `compile_passage` 8,091 µs/22 calls ≈ author's quiet run (8,053/22); 73% of all kick-path time. The dossier's 538 µs/call is the loaded run of the author's three; on a quiet box it is ~367 µs — which lands exactly on the leaver median, making the attribution tighter, not weaker.
- **Adversarial cases.** (1) Unseen seeds 2 and 7: patched vs unpatched digests identical — the memo patch changes no bit off the tuned scene (structurally sound: `Orbit::compile` and `ShapeMemo::get` both collapse compactness through the same `ShapeKey::for_orbit`, then `from_shape` on the actual key). (2) Seed 2/7 leaver medians 104–131 µs: the two-population split holds (2.6–3.3×) and the passage compile still dominates per call (528 µs vs 17 µs cycle on seed 2), but the 9× leaver bill is seed-1-specific. (3) Memo growth unbounded (111 shapes on seed 7) — flagged by the author, needs an owner.
- **Correction to the lever's framing.** The tail is not read only by `next_exit` and release: `Passage::state()` reads tail knots on every drift readout past the inner shape's last knot (orbit.rs:1015–1053), and `at_radius` (985–999) — including the one inside `from_state` itself. Deferral stays bit-safe (the tail is a pure function of key + outer_radius) but needs lazy-init at more readers than claimed; the ~7× remains unmeasured.
- **Predictions.** `predictions.md` written 03:55:17, before the decisive patched runs (~04:00 per the JSONs' machine stamps); the 03:53 baseline is quoted inside it as given input — order honest. Held: rebind >50%, sources <20%, the digest falsifier. The "broke" prediction 2 is a misread of the author's own counter: 16.4% counts replays, real-frame applications and non-kick rebinds in one thread-local; over *distinct* kicks the exact rate is 0% — already pinned by the committed `crates/universe/tests/memo.rs` (<5% asserted).
- **Novelty.** The memo-negative is known ground: H0213, the memo.rs test, `records.rs`'s bank already wiring `ShapeMemo`, and the 5 October taste log. What is new and measured: the leaver population's cost, its attribution to one `Passage::compile`, the per-phase made-kick profile (beyond HANDOFF #3's "29 µs, 15 in fit+compile"), and the named lazy-tail lever. Fits board focus #1; PRINCIPLES §1 ("Delete before optimizing") and §3 ("Compute only surprises" — the tail is a re-derivation).

**Not gold:** no measured deletion (the ~7× is projected; the lazy-tail patch is unwritten), part of the memo story re-treads committed knowledge, and two headline numbers are load/population artifacts (538 µs average on a loaded run; 16.4% on a mixed population).

**The one experiment to make it gold:** implement the lazy tail — defer `Passage`'s tail panels to first read by any reader (`state`, `at_radius`, `next_exit`, release) — then re-run this bench: digest equality plus the measured leaver cut. A ~5–7× cut at identical digests is gold.

**What the author missed.** `state()`/`at_radius` as tail readers (the reader set in the dossier is wrong); the committed memo.rs test already answering the distinct-kick memo question (cite it instead of a mixed counter); medians over averages for the per-call cost (the quiet number, ~367 µs, was the better headline); and a second scene, which alone would have shown the 9× to be seed-1-specific.

### 20261006-0030-taleb-d3fe
Grade: silver

**Abstract.** Claim: the shipped plane has a reachable ruin state — peak RSS grows ~linearly in game time through any battle that stays live (~0.2 kB per surviving member per game-second, unbounded while the battle lives, 2.8× seed spread) — with both instruments blind to it. Reproduced: 31/70/140/279 MB, leavers/bodies flat; dissolved control 18 MB; digests identical across processes, threads and rtf 8e4. Extended: same cut at half the frames → 308 MB (law is game time, not frames); members 96 → 191 B/member/game-s; default pace → 5 MB, zero kicks. Not gold: "~1.6 GB per hour" is a 10³ slip (1.6 MB/game-hour; 160 MB/wall-hour at fly pace rtf 100), and "canonical event counter" misdescribes the wall-dependent `stats.kicks`.

## Reproduction (clean tree, no patch — `work/patch.diff` is empty)

`reproduce.sh` end-to-end, plus six probes of my own. Linux/x86, 8 vCPU, shared.

| Author | Mine | Verdict |
|---|---|---|
| Law 31/70/142/279 MB (seed 3, m48, rtf 1e4..8e4) | 31/70/140/279 | reproduced |
| Counters flat, leavers 46, dissolved 0 | leavers 46, dissolved 0, bodies 74 every run | reproduced |
| Dissolved control (m16, rtf 4e4) 19 MB | 18 MB (one outlier run of three: 40 MB) | reproduced, control itself spreads |
| Seed spread 279/101/211 (2.8×) | 305/132/239 (2.3×), same structure (4/5 dissolve and retain less) | reproduced |
| Digests: 2 processes + threads 4 equal, seed 4 differs | identical, plus `21f483f5…` twice at rtf 8e4 with equal `cut_tick` | reproduced and extended to the ruin point |
| `bytes_per_body` 9.1 kB × 74 | 9,123 × 74 = 0.67 MB vs 280 MB peak | reproduced |
| Members clamp [4,400]; 55 s ceiling | `xtask/src/universe/mod.rs:32,46` | confirmed in source |

## Adversarial cases (mine)

1. **Game time vs frames** (`--seconds 4 --rtf 160000`): same canonical cut (129,936,285,923), half the frames → RSS 308 MB ≈ 279–305 MB. The growth tracks game depth, not frame count. Digest differs, as it must (the decision schedule differs).
2. **Per-member slope on a new point** (m96, rtf 4e4): 201 MB, 3 survivors, 3.2e5 game-s → 191 B/member/game-s against the author's 181.
3. **Default pace** (rtf 1): RSS 5 MB, kicks 0 — the default bench never even reaches contact; the blindness claim is structural, not just "4 orders under the noise floor".
4. **Identical runs at the ruin point**: digest and cut byte-identical, but `stats.kicks` = 16,987 / 17,105 / 8,903 across three identical invocations. The digest is canonical; the kick counter is wall-dependent (my best read: rework or speculation in the budgeted path is counted). The law's "every canonical event counter stays flat" holds for leavers/dissolved/bodies and the digest, but leans on a non-canonical counter for kicks — flat in order of magnitude (0.9–1.7 × 10⁴), not exactly.

## Predictions

File times support pre-registration (session 00:30, build to 00:33, predictions 00:33:59, raw data 00:44:57), and the failed predictions are the headline — you do not pre-register a failure after seeing it. P-A held with working controls; P-B1 held; P-B2 failed decisively and honestly; P-B3 failed (2.8× > 2×); P-C reported as an instrument gap, not a result. This is the prediction system working.

## Novelty

HANDOFF job 1 already knows the battle is stepped forever (the bug, Sonnet's). What is new: the memory consequence as a quantitative law (per game-second, per surviving member), the measured blindness of both instruments (`bytes_per_body` covers only the body store, `body.rs:170`; body history is pruned, `universe.rs:963` — the growth sits in the fleet/battle settle path outside both), and cross-process digest determinism at high rtf (in-repo tests are in-process). No HISTORY entry measures the plane's peak RSS in game time (H0158 is the old lineage). Novel.

## Goal fit

Bottleneck 5 (10⁹ in 8 GB) and the machine section (swap near its 10 GB limit daily). PRINCIPLES #25: "not making mistakes matters more than doing things efficiently, don't multiply by zero"; #12 smoothness is defeated by an unbounded memory law. The lab's own host died this way on 5 October. The run re-ranks a scheduled fix from CPU waste to survival, and hands it a regression probe. Real value, cheap to adopt.

## Why silver, not gold

The one-line claim contains a number the log contradicts: "~1.6 GB per hour at the bench's own scene". The measured slope (443 B/game-s at 2 survivors) gives 1.6 MB per game-hour, or 160 MB per wall-hour at the documented fly pace (rtf 100); 1.6 GB/hour requires rtf 1000, which is nobody's stated scene. Off by 10³ in the sentence the integrator reads first. Second, "canonical event counter" is wrong for kicks (case 4 above). The discovery itself — reproduced, extended, premise-killing — is gold-grade; the record's claim line is not.

## The one experiment that would make it gold

The per-member/per-game-second slope rests on seed 3 alone (members 96 is also seed 3; seeds 4/5 dissolve). Find one independent seed whose battle stays live (scan seeds 6–9 at rtf 2e4 for `dissolved: 0`, ~15 s each), fit its slope, and restate the rate in measured units at a stated pace. With the claim line corrected to what the runs regenerate, every sentence is log-supported and this is gold.

## What the author missed

- The 10³ slip in the per-hour rate (above).
- `stats.kicks` is wall-dependent — itself a lead: why does the counted kick work nearly halve under load? If the budgeted path re-does kicks, the engine's cost model double-counts survival.
- The dissolved control's own spread (18–40 MB in three identical runs) — single-run RSS is noisy on the control too, so "flat" there is qualitative.
- Determinism was only tested at default rtf; it holds at the ruin point (my case 4), which is the stronger statement.
- The leak is not localized (admitted). My source pass excludes the body store (pruned, and inside `bytes_per_body`); the allocation is in the fleet/battle structures — a heap profile on a tooled host would name it and aim Sonnet's fix.

### 20261006-0437-components-2222
# Check — 20261006-0437-components-2222

Grade: silver

**Abstract.** Claim: the Binet cone cannot drop in behind `Encounters` as a per-check query. Reproduced: scan 3.4–4.0 µs per candidate, linear (49 ms at n = 12289, exponent 1.01, 5 ms budget dies at ~1250 members); certificates 3.3–10 ms per check, 93× the scan at the plane's n = 10, break-even near n ≈ 3000, only 5× better at 12289; cone candidates saturate (886→904). Decomposed: the U-sweep + cone test is 243 ns; all cost is per-pair `sections`/`first_hit` re-paid per check — the skin framing is right. One correction: of the two "missed encounters", only one is real (present-inside, minimum in the far future, not the past); the other is a scan phantom contact. The belt control the author discarded was valid and exposes a false-negative class of the scan itself. Kill stands; adopt with the corrected seam contract below.

## Reproduction

Clean tree, `git apply work/patch.diff`, `cargo build --release -p emergent-universe --bin seam` (8.9 s), run (peak 27 MB). Every deterministic field matches bit for bit (scan_pairs `[3, 18]`, cert_pairs `[]`, u_cand 191/765/2532/4849, cone 102/378/886/904, evals 10897/14835/19125/29755/23943, err 1.508e-9/1.054e-8); timings within 5% (plane scan 33.6 µs vs 34.4; cert 3.21 vs 3.29 ms = 93× vs 96×; n=12289 scan 48.9 vs 49.5 ms, cert 8.88 vs 9.30 ms). The 190 µs/item in HANDOFF item 4 is stale: the scan is 3.4 µs/item today, which strengthens the inversion. Predictions existed before the decisive run (mtimes 04:49 vs run header 05:03:29Z; run.log empty, one decisive run saved twice). 3 of 5 predictions falsified and reported — pre-registration looks genuine.

## Attack (probe `seamprobe`, my own binary, same scenes)

1. **Sound-rho control.** Rival explanation for the misses: the bench's sections reach `rho_query = 1.5·max_rho` is below `rho_true = ρ_i + ρ_j ≤ 2·max_rho`. Refuted: for both plane pairs `rho_true < rho_query·1.1` (29.17 < 48.1; 1.65e-3 ≪), and with `rho_query = 2.2·max_rho` the certificates still report none. The miss is not a reach artifact.
2. **Geometry of the missed pairs (exact cartesian vs Kepler model).** Pair 3: inside ρ now (d(t) = 7.16e10 < ρ_true = 3.16e11 internal), approaching, and **no interior minimum within ±8 step windows** — co-orbital monotone drift, model distance still decreasing at the ×8 edge (+33.6 M ticks). The author's "minimum in the past" is wrong: it is in the far future. The semantic gap is real for this class (present-inside is invisible to interior-minimum enumeration), so the t0-query conclusion survives for it. Pair 18: **193× outside ρ** at t, Kepler minimum stays ~3.43e9 ≫ ρ = 1.78e7 through ±8 windows; the scan's `contact=true` is manufactured by the linear-over-step-window predicate (interval = 2²² ticks, `universe.rs:939` passes `rec(p).step`, so the engine's real path inherits it). The certificates were **right** to report nothing: this "miss" is a scan false positive, not a certificate failure. "Missed both real encounters" is half false.
3. **The discarded belt control was valid.** Exact distances at t: partners 1–3 are inside ρ_true (4.92e3, 9.01e3, 1.31e4 < 1.64e4 internal) — placement was correct, contradicting the author's "my placement in the bench is wrong". The shipped scan reports none of them: for an inside-reach pair `hit` returns true only if quantized `dot(d,w) < 0`, and these near-stationary co-orbital partners quantize to zero — a false-negative class of the component the dossier calls "the exact scan", missed by the author and by me until probed.
4. **Cost decomposition.** U-window + cone alone: 243 ns (plane), 4.6 µs (n=193), 176 µs (n=12289) — noise. Full query: 3.14 ms / 3.9 ms / 8.6 ms. All of it is per-pair `pair_events` (`sections` + `first_hit`: evals 10897 at n=10 over 9 cone candidates ≈ 350 µs/pair; 14835 at n=193 over 102 ≈ 38 µs/pair). The author's "~21 µs per U-candidate setup" mis-attributes, but the conclusion (per-pair setup re-paid per check; the skin owns the economy) is confirmed. Sound-rho query costs the same order (5.0 ms at n=193) — the kill is not a tuning artifact.

## Novelty

`docs/HISTORY.md` has no seam measurement; the lab's other runs are not in this checkout. Against the board: q-candidate-degree (taste log, 6 Oct) proved the certificates' fixed-density asymptotics standalone; the board already says "the Binet cone … plus a skin". New here: the seam-level measurement at the plane's real scale (the 96× inversion, break-even n ≈ 3000, the scan's own ~1250-member budget), the first semantics evidence at the seam, and the refutation of `encounter.rs`'s "implements the same trait, with no rewiring" promise — a main-tree comment now known wrong. Distinct from r8 v2/v3 (candidate discovery, not the per-check query).

## Goal fit

Moves HANDOFF item 4. PRINCIPLES 3 ("Nothing is evolved that can be derived when looked at" — the per-check population scan is the evolved-clock mistake) and 9 ("A failed experiment kills that configuration, never the method") — the kill is correctly scoped to the wiring. PRINCIPLES 34 cuts the other way and the author missed it: the scan is not an oracle; over a step-sized window its linear predicate both invents contacts (pair 18) and loses stationary-inside pairs (belt partners 1–3).

## Why silver, not gold

The headline numbers, the kill, and the skin attribution reproduce and are adoptable. But a load-bearing claim — "missed **both** real encounters … pairs already inside ρ at window start, minimum in the past" — does not hold: one pair was never in an encounter (scan phantom), the other's minimum is in the far future. And the honestly-reported "instrument defect" was a misdiagnosis of a valid control that exposed a false-negative class of the shipped scan. This is the 5 October lesson again (count the events as distinct and real before counting misses): adoption text written on the current mechanism ("add the t0 query") under-specifies the seam contract, which must also fix the scan's own two failure classes.

**The one experiment for gold:** merge the geometry classification into `seam.rs` — every scan hit and certificate hit classified against exact Kepler windows as present-inside / interior-minimum / linear-phantom, on scenes containing all three classes (the belt partners and plane pair 18 already do), plus the scan's quantized-zero false negatives. Then the kill and the corrected contract (skin + t0 query + window-size discipline for the linear predicate) stand on verified ground and the run deletes the "no rewiring" comment for the right reasons.

## What the author missed

- Pair 18's encounter/contact is a linear-over-step-window phantom (193× outside, Kepler min 3.43e9 vs ρ 1.78e7), live on the engine's real path (`universe.rs:939` passes the step as interval).
- The belt partners were correctly placed and inside ρ; the scan itself drops inside-reach pairs whose quantized relative motion gives `dot(d,w) ≥ 0` — a shipped-component false negative, stronger evidence for the seam rework than the vacuous control the author reported.
- "Minimum in the past" was asserted from an unsaved probe; the measured class is no interior minimum in any bounded window (co-orbital monotone drift) — same conclusion (t0 query needed), wrong mechanism.
- The bench queries a window 4× beyond simulated time (interval 2²² vs t = 2²⁰) — legitimate for the models, but it should have been stated, since the linear predicate's sanity degrades exactly there.
- Per-U-candidate cost framing (~21 µs): the U-sweep is 243 ns; the cost is per cone-candidate `pair_events` (~38 µs at n=193, ~350 µs at n=10).

### 20261006-0519-rung-r8-encounters-v4-0e5d

### 20261006-0521-rung-r8-encounters-v4-6cd5

### 20261006-0519-taleb-48d6

### 20261006-0521-taleb-dbee

### 20261006-0519-spacex-ffd6

### 20261006-0521-spacex-36cb

### 20261006-0737-components-4643
Grade: gold

**Abstract.** Kill of the taleb-3ec1 deferral lead on the belt kick workload: pairs are indeed dormant (99.7% of first in-window passages >100 orbits ahead, median 26,000 — reproduced bit for bit), but 92% of per-kick evals are numeric-window *setup*, which calendar wakes re-pay at every kick; deferral's measured ceiling is 1.1–1.2× evals (1.5× wall on my rerun), not the predicted 5×. Analytic zero-setup windows over-fire 427× (276–528× across my probes). The lever stays the slack skin (12.6×, HANDOFF). Adoption is a design decision, nothing to build: drop the wake calendar. Blemish: the dossier's wall-clock digits match no archived log (they regenerate in family); the deferred harness has a disclosed exactness hole the structural argument does not lean on.

## Reproduction

Applied `work/patch.diff` to the clean tree, built `dormant` offline, ran every dossier command. All load-bearing counters reproduce **bit for bit**: split σ_e=0.01 (e_setup 1,600,220; e_check 131,824; ≥100-orbit share 117,984; wakes p50 25,999.1, >100 frac 0.997; cap 1,817,897 vs 4,262 = 427×; q_wake 1,010,833 vs q_all 1,038,129), split σ_e=0.05, and all three stream rows (kicks 2,484; re-derivations 252,704 → 111 fires; eval ratio 1.1; misses 37/extras 11; dense and sparse variants identical). The `split` workload provably matches the crate's `kick()` spec (same n, σ_e, ρ, seed, horizon, kicked-body formula; eps = 1e-5 ∈ the crate's epss). "Eval" is one relative-state solve in both paths (`pairs.rs` counts them identically), so the 92%-setup accounting is a fair common currency.

## Predictions

`predictions.md` predates the decisive batch: run folder born ~07:39, predictions ~07:49, the archived load lines bracket the decisive run at 07:55:20–07:55:58, dossier ~07:56. P1 held (98.7% ≥ 80%, and on both held-out densities); P4, the pre-named risk, is the finding. P2 and P3 were the *design's* predictions and were falsified and reported as falsifications, with the disclosed harness defect — this is the honest shape of a kill, not a failed dossier.

## Attack (three adversarial families of my own)

1. **ρ = 2e-4** (declared held-out, never run by the author): setup 90.3% of evals, wakes >100 orbits 99.5%, cap penalty 276×. Law holds.
2. **σ_e = 0.3 eccentric**: setup 81.9%, wakes >100 orbits 99.8%, cap penalty 528×. Holds, stronger.
3. **ρ = 1e-2 concentrated** (the boundary the dossier itself names): the law inverts exactly there — wake p50 248 orbits, cap penalty only 8× — yet deferral still gains just 1.6× evals / 1.7× wall (harness missing half the events there). The kill is correctly scoped to sparse belts and in fact extends beyond its stated scope.

## Novelty

First measurement of the taleb-3ec1 lead — HANDOFF "Next, not started": "99% of setup work lands on dormant pairs, defer it". The dormancy is independently reproduced; the deferral economics are new. No HISTORY entry measures them. q-skin's 12.6× is quoted correctly from HANDOFF.

## Goal fit

Board focus item 3 (encounters without work per orbit/element change). It deletes the next planned encounters component (the wake calendar) and shows the lead's premise inverts: the work is not where the dormancy is. PRINCIPLES §9: "A failed experiment kills that configuration, never the method" — the method's exact wake math (`first_hit`) is explicitly not on trial. §1: the compute not done is the re-setup. Adoptable within one step: a decision, zero code.

## Why gold despite two blemishes

The spine — dormancy real, setup dominant and structurally re-paid by any wake design (both paths call `sections()` per candidate pair per kick, and e_def/e_eager = 0.92 confirms), analytic windows over-firing by 10²–10³× in sparse belts — is bit-reproducible, adversarially robust, and adoptable now. The blemishes: (a) the dossier's wall digits (8,676/649 µs; 3.42 s vs 2.37 s; "1.4×") appear in no archived log (raw-output says 11,996/907 µs and 2.0×; my rerun 12,385/944 and 1.5×) — they regenerate in family under load noise, and the dossier itself stamps wall as orders of magnitude only, so I flag rather than demote; (b) the deferred harness's 30–37 misses are disclosed with a correct insensitivity argument. Neither touches a load-bearing number.

## What the author missed

- **Currency nuance:** a check eval chains Newton refinements, so by wall the check fraction is nearer a third; deferral's honest ceiling is the measured ~1.5× wall, not 1.08×. The dossier prints both numbers but headlines the eval currency.
- **A stronger claim left on the table:** even in the concentrated regime where the recency law inverts, deferral still buys under 2× — the kill's scope is wider than "sparse belts".
- **eps is hardcoded** at 1e-5 in the experiment; the crate's `kick()` spans 1e-9…1e-3 and the dossier cites it rather than measuring it in this harness.
- **The miss bug was never localized**; a zero-miss deferred harness would have made P2's falsification airtight without the caveat.
- **Record hygiene:** quote only archived numbers; two wall figures had no log backing.

### 20261006-1029-components-21c3
Grade: silver

**Abstract.** Claim: a belt's scar layer grows only log in t (record-kick dominated); return-based reabsorption is dead (10⁻⁶ of creation); a two-tier light-cone store (near exact, far at q_far, certified by a quadrupole firewall) holds 10⁹ bodies at 5.6 bits/body (0.70 GB vs 6.5 GB naive at 52-bit; ~1.4 vs 19.6 GB at 157-bit). I reproduced every number bit-identically in a clean tree (26.8 s + 47.3 s, values exact; only load-average differs). My adversarial cases — the author's own named killer (truncated kick tail) and λ=10 — leave the claim standing, and the firewall keeps a ≥10⁹ margin even at realistic ε and μ×10³. Held from gold by two missed held-out predictions, a misattributed law.md ledger line, and an unmeasured promotion path. Adoptable as numbers, not yet as a store.

**Reasons.**

1. **Reproduction: exact.** `python3 belt_scars.py` and `python3 t400.py` in a scratch copy (seeds fixed): every stored value regenerates identically — λ=1.1 one-tier 6.70→32.21 (t=100)→43.5 (t=400), two-tier 5.53→7.02→10.32, reabs 4,201, occupancy 12.768→12.784, firewall 1.04×10¹⁵, extrapolation block identical. Only the load triplet differs (machine state, not physics). The model faithfully mirrors shipped Form P (`crates/shipmem/src/program.rs`: EF ordinals ≈ 2+log₂(n/k), zigzag deltas, reabsorb-on-return, repack at half-block cost).

2. **My adversarial cases (3).**
   - *Truncated tail* (the dossier's own "what would make it wrong" #1): kicks capped at 2 lattice units, λ=1.1, t=400 → one-tier 22.57 (still log, crossing later, not earlier), reabs 12,939 ≈ 10⁻⁴ of ~10⁸ encounters (still dead), two-tier flat at 5.51. The claim survives its named killer; log growth is process-shape, not tail-shape.
   - *λ=10 extreme*: crossing of naive at ~130 orbits (λ-scaling of the ~1,100 at λ=1.1, coherent), two-tier 13.25 bits/body at t=100, reabs 20 total. Structure holds.
   - *Firewall sensitivity*: at a physically consistent ε (q_far = 2⁸ units over a ~1 AU belt ⇒ ε ≈ 3.7×10⁷ m, not 100 km) margin = 2.8×10¹²; with μ×10³ (fleet aggregate) and that ε, 2.8×10⁹. Conclusion robust; the 10¹⁵ headline is a narrow-belt calibration (see below).

3. **Held-out predictions: 6 held, 2 missed, 1 over band** — honestly reported, including the author's own wrong linear prior. Pre-registration of items 7–9 before the t=400 run is unverifiable from mtimes (predictions.md final mtime is post-run; window was 10:29–10:41), but the misses (10.32 vs ≤8.6; 1.00 vs ≤0.95) are what post-hoc "predictions" would not contain. By this lab's precedent (q-secular-v2, redteam-b12-stat, both silver on a failed held-out item), two misses cap the grade at silver.

4. **Novelty: yes.** `components-98bc` (gold, 5 Oct) compressed the *birth* program (0.126 bits/body, no history). This run gives plane.md's H_live metric ("distinctions created per game-second … against what reabsorption removes", so far unnumbered) its first numbers, the first equilibrium rule, and the two-tier store. It moves the board's "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" by 9–14× in memory. No prior H entry measures scar growth; nearest kin H0173 (≈4 bits per collision in the rounding-grid probes) is uncited by the author but measures a different quantity.

5. **Goal fit.** Real and on the board's focus list. PRINCIPLES #6 "Store the generator, not the generated"; #24 "The memory floor is information" — the measured floor (occupancy 12.8 bits/body flat + identity deltas) is exactly the kind of number that principle demands; #33 scale-resolved influences. The two-tier extends #5's light-cone partition from compute to memory.

6. **Why not gold, besides the predictions.**
   - *The "+62/−60" ledger is not in law.md.* I searched law.md, plane.md, HISTORY.md, board.md and lab/results: the only numbered ledger is this run's own text. plane.md defines H_live without numbers. The measured finding (return-based reabsorption is 10⁻⁶ of creation, so an equilibrium held by return is dead at belt scale) stands; the framing "law.md's H_live ledger never balances" attacks a line the author wrote.
   - *Promotion's information is unaccounted — the adoption-blocking gap.* Far deltas requantized at q_far cannot regenerate exact state, so "promotion = one replay of its encounter history" presumes an event log whose bits were never counted (the model has no partner reciprocity, hence no shared events), or promotion is lossy — and then the firewall does not apply: it certifies far-zone *aggregate* effects on near bodies, not a promoted body's own state error inside the cone, where navigation must be perfect (Julien: "what really matters is navigation, knowledge and dynamics those need to be perfect"). The lens section admits promotion's CPU, not its bits.
   - *ε calibration*: q_far = 2⁸ units = "100 km" implies the belt spans 4.1×10⁸ m ≈ 0.003 AU; a ~1 AU belt on 2²⁰ units puts q_far at ~3.7×10⁷ m. Margin still ≥10⁹ across the plausible range, so the certificate survives, but the 10¹⁵ is calibration, not physics.
   - Minor: `t400.py` was edited after `t400.json` was written (JSON keys renamed), undisclosed — values regenerate exactly; and the 1.4 GB figure at the 157-bit state is not derivable from the stored outputs (5.6 bits/body ⇒ 0.72 GB at near fraction 10⁻³); it reads as a t=400-flavoured extrapolation. Cloud numbers are orders of magnitude only.

**The one experiment that would make it gold:** measure promotion. Either (a) show the engine's canonical replay log (taleb-c271) already carries the bits exact promotion needs and count its marginal cost per promotion at belt scale, or (b) measure the near-zone error of lossy promotion at q_far under a *moving* player with tier churn, against the near tier's exactness requirement (B18b's cap and the navigation floor). Fold that into the far-tier design in `crates/shipmem`, re-attribute the ledger claim to plane.md's unnumbered H_live metric, and this is gold: the rest reproduces exactly and the firewall holds at every calibration I tried.

**What the author missed.** The misattributed ledger line; the promotion/event-log bits and the lossy-promotion near-zone question; the ε calibration inconsistency (100 km vs a 1 AU belt); the undisclosed post-run edit of t400.py (cosmetic, values exact); H0173 as the nearest prior measurement; tier churn under a moving player; and that a truncated tail *strengthens* rather than kills the result — worth saying in the dossier, since "what would make it wrong" #1 as written overstates the risk.

### 20261006-1436-components-ed09
Grade: silver

Abstract: Claim reproduced: all 12 matrix cells within noise of decisive4 (heap 247–1030 ns, wheel 47–451 ns per pop+set, ratios 1.89–5.22×, all ORDER-MATCH, negatives fail); brute-force oracle clean through 2M churn pops; Calendar/Scalar faithful copies of crates/space. Gain ~4× on a 1.5–3%-of-kick component (~7→1.7 cores at 10⁹, Fermi) — a floor map, not a 10× lever, as the author states. Adoption is blocked by a livelock I found: when all live events sit in the wheel's frontier (same-tick formation, due-now re-sets, mass cancel), pop() never returns — the battle workload hangs at the first pop (killed at 120 s). Other extremes hold: earlier-moves 2.26–2.33×, far-tail 3.35–3.79×, both order-match.

Reasons:

1. Reproduction (clean tree, patch.diff empty, no repo edits — git status shows only lab/results/ untracked). `rustc -O --edition 2021 queue_floor.rs -o qf && ./qf all 2000000` (~55 s, loadavg 0.27–1.31): all 12 cells match decisive4 within a few ns (churn 10⁶ ratio 2.09× vs author's 2.06×; tail 3×10⁶ 3.86× vs 3.92×). `./qf debug4` finished in ~5 min with "all checked pops consistent". The heap reference is a line-for-line copy of crates/space/src/events/calendar.rs (verified up/down/remove_at/set_unchecked/peek/pop); the Scalar Ord matches crates/space/src/scaled.rs:198; the "sift-down dominated the calendar's cost at a million bodies" quote is verbatim in calendar.rs's doc comment.

2. Predictions. predictions.md predates the final decisive run (14:57 vs source edit 15:11, decisive4 15:20). But the intermediate decisive.txt/2/3 show the held-out cases served as debugging: ORDER-MISMATCH on churn/tail was fixed in three rounds after predictions (decisive2 even contains a broken-state cell: churn 10⁵ wheel 2.6 ns, ratio 152×). All disclosed in the dossier, and the final correctness stands on three independent legs (heap-stream identity, brute-force oracle, negative control), so this is honest mess, not tuning of performance claims. The author's three reported misses (churn ≥3× → 2.06×; wheel ±25% flat → 2.1× growth; idiot index ≥5× → 3.97–4.45×) check out against my reproduction.

3. Adversarial cases of my own (patched copy of the bench, /tmp):
   - battle (all n events on one tick, the dossier's disclosed-unmeasured hand-out): livelock, described above. This is the finding of the check: it is reachable by ordinary engine states, not only by cancellation storms.
   - early (2 re-sets per pop, always earlier, clamped to now+1 — maximal stale/frontier traffic): ORDER-MATCH, 2.26× (10⁶) / 2.33× (3×10⁶), stale_skips 11.6k/25.5k. The churn column is indeed the honest preview; no collapse.
   - fartail (every 2nd pop throws an event 16–64 intervals out; live far fraction far past the dossier's ~30% worry line): ORDER-MATCH, 3.35×/3.79×. The overflow heap does not erase the win at this extreme.
   - Engine access pattern: crates/space/src/events/queue.rs pop_through is peek-then-pop — the wheel has no O(1) peek at all, and the bench measures none of this (disclosed, unmeasured).

4. Novelty: docs/HISTORY.md has the Calendar's creation (lattice-event, "fixed-size calendar") and no timing-wheel, bucket-wheel or queue-floor experiment; the docs' only heap notes are other crates'. First measured floor for this component; nothing to cite as prior.

5. Goal fit: real but bounded. The queue is the no-tick mechanism (P14) and a named scaling-risk term, but at 1.5–3% of a plane kick the ~4× is not a board-level 10×; the author prices this honestly. P16 ("physics loves e while we love 2") and P26 (steal from the compute-starved: hashed timing wheels) are genuinely served: the wheel only exists because time is already quantized. One arithmetic slip: "heap already spends 36 MB on heap+pos" at 3×10⁶ — by the author's own 24 B/entry it is 72 MB + 12 MB pos = 84 MB (this understates the heap, so the argument survives). The per-bucket Vecs also break the crate's "allocated once" invariant, which the lens section correctly flags.

The one experiment that would make it gold: fix the frontier livelock, give the wheel a peek, and measure the engine's real pop_through/peek op mix on the plane bench at 10⁶+ slots — showing the 2–4× lands where the engine actually pays (or that the queue share grows as Fermi'd at 10⁹). If the queue's share at scale is ~4 cores, a verified 4× with a drop-in API is a deleted scaling term; that is the gold case to test, with the battle/early/fartail cases as the rung's held-out set.

What the author missed: the livelock (two of my three adversarial cases hit it — the bench's workloads always populate future buckets, so refill's frontier-blind guard never fired); the peek side of pop_through; the heap+pos memory figure. Otherwise disciplined work: loadavg recorded, min-of-2 reps, controls on both sides, oracle independent of the heap, honest ratio misses.

### 20261006-1931-b-coorbital-cert-152e

### 20261006-2240-b-encounter-skin-8bfa
Grade: silver

Abstract: The slack skin is real and now lives in `crates/encounters` (649-line `skin.rs` + bin), additive to the engine path (`sections` → `sections_pad(0.0)`; verify a/b/c byte-identical before/after). Reproduced in a clean tree: 0 missed / 0 false against the independent Halley/conservative-advancement truth on belt ε 1e-8/1e-6/1e-4, ring, fleet, and my adversarial cases (fresh seeds, κ=1.0, ε=1e-2, ring 1e-6); killing terms 3b+6 makes `exact_at_kick_eps_1e4` fail. Setups/kick 142.3→17.1 (8.3×) at the plane's kick size. But total evals/kick rise 1.5× there (4468 vs 2921) and wall gains are ~1.2–1.6×: the 8.3× is a counter, not yet a measured compute cut on the plane. Adoption: one module.

Reasons:

1. **Reproduction (clean tree, patch applied).** All deterministic counters match the stored raw bit-for-bit for belt 1e-6 (0/0 of 63; 17.09 setups/kick), belt 1e-8 (0/0 of 74), belt 1e-4 s16 (0/0; 32.87, sat 0.48, false_cand 0.1003), ring 1e-4 (0/0 of 851; 52.28), fleet 1e-6 (0/0 of 1232; 73.92, false_cand 0.6535). `cargo test -p emergent-encounters`: 7 passed, ~12–16 s. `encounters verify a|b|c` identical to the stored after-files, and baseline==after.

2. **One stale raw file.** `work/belt1e-4.out` and `results.jsonl` line 2–3 record `"missed":1` with a `fresh_finds` diag that the shipped bin cannot print alone (its code always emits `at_miss`+`lib` first) — a pre-final binary. Regenerated, `$T/skin belt 1e-4 0.3 4` gives **0/0 of 73**, setups 54.16, sat 0.05, evals 7160: the dossier's headline holds, but its 54.2 appears in no stored raw, and the stored raw contradicts the claim. Every other number regenerates; this is a record-keeping fault on one case, not fabrication (the shipped code reproduces the claim), but it is exactly the record failure the taste log punishes.

3. **Falsifiability verified both ways.** With term 3b (`raw = 0`) and term 6 (`if false && …`) compiled out, `exact_at_kick_eps_1e4` panics ("skin missed/false events"); restored, 7/7 pass. The two new terms are load-bearing, and the tests defend the contract, not the source.

4. **Adversarial cases (mine).** Fresh seeds (777 at 1e-4: 0/0 of 75; 31337 at 1e-6: 0/0 of 74, 8.2×) — not overfit to the fixed seed. κ=1.0 at 1e-4 (3.3× the kick rate the lens named as untested): 0/0 of 66, 3.4× setups cut. ε=1e-2, 100× beyond the named range: still 0/0 of 67 (economics collapse to 1.13×, as the drift trigger fires 79×/kick — the boundary behaves as designed). Ring at 1e-6 (untested combo): 0/0 of 817, and here total evals *drop* 1.44× (51181→35577) with wall 16.1→10.9 s. The evals inversion is belt-specific (padded-cone rescan churn, `setup_new` 13.76/kick), not universal.

5. **Predictions.** `predictions.md` predates the decisive sweep (file times 21 m vs 2 m before session end) and declares its tuned case. Exactness predictions all held; two economic ones failed and the dossier reports them honestly (belt 1e-8 setups <5 → 17.1; checks ≤ always → 1.08 vs 0.78). The pre-registered falsifiers (miss at ε ≤ 1e-6; setups within 3× of always) did not trigger.

6. **Novelty.** The skin is the integrator's own named lever (board focus line 3; components-4643 gold: "the slack skin (12.6×) stays the lever; nothing to build"; q-skin 20261002-0539 silver had 29 misses at ε=1e-4 and no rule). This is the directed build of it; the crossing-longitude drift (3b) and the empty-certificate re-proof (6), plus the width *inversion* replacing q-skin's pad, are new and correct q-skin's misdiagnosis. Not a redo of any H entry.

7. **Why silver, not gold.** The gold bar needs the bottleneck moved 10× or a premise killed. The measured movement at the plane's kick size on the belt is 8.3× on the *setups counter*, while total evals/kick go **up** 1.5× (4468 vs 2921) and wall improves only ~1.2–1.6× on a shared runner; the dossier discloses the evals inversion only at ε=1e-4, not at 1e-6. Under principle 27 ("the goal, never a proxy"), setups/kick in a synthetic belt harness is edging toward a proxy for the plane's p99; the run's own numbers show the deferral currently converts setup work into check work at a loss on the belt (skin-mode setups cost ~12× more evals each: padded arcs plus 100·TAU horizon queries). Combined with the stale raw on the headline case, gold is not earned on the record or on the measured gain.

The one experiment that would make it gold: measure the skin on the compute the plane actually pays — steady-state total evals and p95/p99 wall per kick on the plane's own kick pattern (or the N=10⁴ belt), including the certificate store's memory — showing total work, not the setups counter, down by the bar; or delete the belt's rescan churn (the 13.76 `setup_new`/kick at the padded-cone edge) so the setups cut converts into an evals cut. Regenerate `work/belt1e-4.out` and `results.jsonl` from the shipped code in the same run.

What the author missed:

- The evals/kick inversion at ε=1e-6 (4468 vs always's 2921) is in the raw but unremarked; only the 1e-4 case is conceded. The ring shows the belt's churn is the culprit — worth naming as the skin's own next term rather than deferring wholesale to the co-orbital certificate.
- Dossier says "two additive fields on `Section`"; the patch adds one (`kscale`). The other is `sections_pad`'s parameter.
- The exactness argument mixes current and stored periods in the saturation test (`pi` from the live body vs windows in stored ticks) — conservative in practice, held by the tests, but the module is honest that it is derivation-plus-constants, not a proof.
- Certificate memory (≈99 k certs at N=1500) and N > 1500 unmeasured — the author flags these; they bind adoption at the 10⁹ scale (bottleneck 5).
- Cloud wall times on a shared runner under load (my belt runs varied 13–60 s for identical counters); only the deterministic counters and orders of magnitude should be read.

### 20261007-0341-second-20261006-2240-b-encounter-skin-8bfa-57c1
Grade: silver

**Abstract.** Claim: the silver's setups cut converts into a total-evals cut at the plane's
kick size via three corrections. Every counter reproduced bit-for-bit from `work/patch.diff`:
belt 1767 vs 2898, 64-orbit 1540 vs 2703, ring 28650 vs 47600, fleet 17068 vs 61452 (3.6×),
and the 256-orbit inversion 27007 vs 2690 — all 0 missed/0 false, counters deterministic.
Tests 7/7; killing terms 3b+6 fails 1e-6/1e-4 as claimed. My adversarial: seed 4242 (0/0,
1.73×), κ=2 (0/0, 4.4×), fleet 1e-4 (0/0 of 1233 — the author's unfinished case closes at
parity). Gain: wall 3.0–3.7×, per-kick p95/p99 down 3–4× at young certificates. Cost:
additive in `skin.rs`, linear store (46.5 MB at N=1500); the required max-age refresh is
unimplemented.

1. **Reproduction, exact.** Applied the patch (`patch-mine.diff` is byte-identical), built offline, ran the dossier's commands plus `work/record.sh`'s case list. Every counter line regenerates exactly: belt 1e-6/1e-4 (the stale-record case, 0/0 of 73)/1e-8, orb=64 (0/0 of 257), orb=256 notruth (976 s wall, wk_p95 30.8 µs), ring 1e-6 (three identical runs — counters are process-deterministic), fleet 1e-6, seed 777 1e-4 (4628 vs 2718), ε=1e-2 (6542 vs 2754). One artifact of my own making, resolved: my mid-batch rebuild raced one adversarial rerun; clean reruns settled it against the stored line.
2. **Predictions.** Pre-registered (file times precede all work outputs). Held: pad s/2 exactness everywhere, trig 0.00 at 256 orbits, skin wall below always at 16/64. **Refuted:** the long-horizon economics (≤350/kick and ≥8× below always at 256; measured 10× *above*). The pre-registered falsifier fired, the author disclosed it, and it became the run's second finding — but gold requires held-out predictions held.
3. **Attack.** Term-kill control verified (3b+6 out → 1e-6 and 1e-4 fail, 1e-8 passes). Pad-s probe: 2202 vs 1767 evals/kick — correction 1's direction and size confirmed. κ=2.0 (harsher than the author's κ=1.0): 0/0, cut grows to 4.4× — the skin amortizes better under more kicks, so the win region extends up in kick rate, not just down.
4. **Novelty.** No HISTORY entry or board item covers the evals decomposition, the s/2 pad sizing, the exact-tolerance re-proof, or the widening-with-age limit. The skin itself is the silver's (20261006-2240) on the components gold's premise (20261006-0737); this run is the increment that makes its economics true in total cost, and corrects the first checker's attribution (the horizon query was 3 evals/kick, not the story).
5. **Goal fit.** Board focus line 3 (a skin over the Binet cone). PRINCIPLES §27 "The goal, never a proxy": judged on total evals and wall, the counter kept as diagnosis; §14 "No work for no reason": a discarded query deleted. The 256-orbit limit is itself adoptable knowledge: the skin is a young-certificate cache, so any adoption must bound certificate age.

**Why not gold.** The long-horizon prediction failed (into an honest finding), and the measured gain is 1.6–3.6× total evals (3.0–3.7× wall) — not the 10× bar. The author's own lens section says as much.

**The experiment that would make it gold.** Implement and run the max-age refresh the dossier derives (~70 orbits at the measured q(age)) plus a cheaper initial padded scan; require no horizon where the skin loses to `always`, belt total evals ≥5–10× at 16–64 orbits, 0/0 exactness, and `belt10k` completed (the store-at-scale number is still an extrapolation).

**What the author missed.**
- Fleet 1e-4 runs in 50 s and is 0/0 of 1233 (skin 63334 vs always 60718, parity): the record's only exactness hole was already closed, and at parity, not a loss — undersold.
- The crossover age (skin = always, between 64 and 256 orbits) is unmeasured; q(age) is sampled at three ages with exponent ~1.6 (16→256), called "~quadratic" loosely.
- The per-setup narrative "~322 → ~210 evals" does not reconcile with the shipped counters (~157 → ~126 by my measurement); the totals and the direction reproduce, the story numbers do not.
- The one-time initial padded scan (13.76 setups/kick at 16 orbits, 99k certificates) dominates young-horizon cost and is untouched; deleting it is where a further ≥2× on the belt lives.
- `results.jsonl`'s line ordering shows concurrent assembly (the orb=256 header at line 2, its always line inside the orb=64 block); every line regenerates, but the file is curated, not raw sequential script output.

### 20261006-2240-b-belt-wire-a733
Grade: silver

**Abstract.** Claim reproduced end to end: the patch applies to pristine main (70f27a9); B18b goes FAIL ("belt_birth is not implemented") → PASS on all five frozen runs with the dossier's statistics bit-identical (chi2 2.80/4.5, serial 3.13/5, KS 0.56, birth 31 B, 32 B at 1e9, 11.4% scarred at 9.7 B); B18 FAIL unchanged; shipmem 5+2 and xtask 3+1 tests pass; two CLI invocations give identical bits. My adversarial probes pass: unseen seeds 424242, 777 at 2^20 and 555 at 2^23 all inside limits; restore fuzz refuses every mutation/truncation. wt/belt's frozen E[0]=1174440 vs judge threshold ≈1062976 confirms the claimed old-table bottom-tail kill (z −7.25). Silver, not gold, for two record defects (below); gain: the components-98bc program certified mergeable, one step to adopt.

**Reasons.**

1. **Reproduction (clean tree, patch applied by me).** Before, on main: `B18b FAIL belt: 1 of 1 findings fail: 2^20 seed 20261008: belt_birth is not implemented [0.00 s]`; `B18 FAIL memory: 0/12 ladder scenes … 12 not answered`. After: `B18b PASS belt: 5 runs, every criterion; worst: chi2 |z| 2.80 … birth 31 B for info 31 B … 11.4% are scarred, 9.7 B each (floor 54 bits) … [26.5 s]` — every number matches `gates-before-after.txt` except timing (26.5–29.1 s vs 16.9 s; 28 vs 17 ns per body at 2^20, 17 ns at 2^23; shared cloud machine, orders of magnitude agree). A second process invocation printed the identical statistics line. The frozen judge `xtask/src/behave/belt.rs` is untouched by the patch; no threshold moved.

2. **Adversarial cases (mine, beyond the frozen set).**
   - Seed 424242, 2^20, thorough, through `judge_findings`: PASS (worst conditional mean 2.39, serial 2.47).
   - Seed 777, 2^20: PASS (worst count 1.59, serial 2.63).
   - Seed 555, 2^23 — unseen size *and* seed, attacking the author's own named thin margin (bottom-e reach ~1.8×): PASS (worst count 1.86, KS 0.69 of critical, serial 3.03; reach findings passed).
   - Restore fuzz on a scarred store: all 2×len single-byte mutations, four truncations, trailing junk — every one refused or self-consistent, no panic.
   - Finding 1 verified from the frozen artifacts: `git show wt/belt:…/belt_quantiles.rs` has `E[0] = 1174440` (the dossier's exact number), dyadic octaves only at the survival end; the judge's EBottom threshold at 2^20 is ≈1062976, so X = 0 and z = −7.25. The committed gold program would have failed its own gate; the both-ends restructure is real, necessary work.

3. **Predictions.** `predictions.md` (23:10:38Z) precedes the decisive gate output (23:28:18Z) and the dossier (23:28:49Z); run.log is empty, so file order is the only witness, and it is consistent. All six predictions held (chi 2.80<3, serial 3.13<4, KS 0.56 vs "<0.5" — the 12% miss the author disclosed, still half the limit; 31≤32 B; 9.7≈10 B; B18 identical; no regression from the patch — I verified the last directly, see defect 2).

4. **Novelty.** H0214 froze B18b on 5 October with "no wired belt yet (Astra and Sol, after 9 October)"; wt/belt a2b777 is unmerged pending exactly this judgment. The wiring, the exact-op derivation of the table at birth, and the bottom-tail failure of the committed table are all new. Not a redo of any H entry.

5. **Goal fit.** Board item "fitting 10⁹ in 8 GB (crates/shipmem: population programs plus scars)": the population program goes from unmerged/umjudged to certified (31 B any n, ~9.7 B per rewrite, 1.10 GB of scars at 1e9), and the 28 KB frozen table is deleted as stored information. PRINCIPLES: "Store the generator, not the generated" — the store is parameters plus scars; the gate's own freeze wording ("a table derived from the spec is a working constant, not counted, and not stored") is honoured rather than weakened.

**Why silver, not gold — two record defects, both confirmed on my machine:**

1. **The held-out claim is overstated.** The dossier says predictions were "tuned only on a non-frozen seed at 2^20", but `predictions.md` itself discloses "one thorough judged 2^20 run at seed **20261008**" — and `RUNS[0] = { log2n: 20, seed: 20261008, thorough: true }`. Frozen run #1 was exercised pre-prediction (it also ships as the patch's unit test), and `predictions.md`'s own "the frozen seeds … are held out" is internally inconsistent. The disclosure was honest; the dossier's summary mislabels it. Runs 2–5 and both 2^23 sizes were genuinely unseen and passed.
2. **A workspace-evidence line the machine contradicts.** "cargo test --workspace --release — all pass except lattice-metal's fuzz_free_worlds" is not regenerable: on this machine 9 further xtask tests fail (events B12-echo, 5 handoff, 1 plane kick, 2 behave_cli). I ran all 9 on **pristine main: they fail identically** — the patch regresses nothing, but the quoted line is false. Most likely an aborted run read carelessly (lattice-metal fails first in build order and cargo's default fail-fast then skips xtask's suite).

Per this lab's own rule — a headline the log contradicts costs the grade (r3 v3, r4 v2 precedents) — gold waits on the record, not the physics.

**The one step to gold:** append the corrections (never rewrite): (a) frozen run #1, seed 20261008, was the disclosed pre-prediction run, held-out = runs 2–5; (b) replace the workspace line with the regenerable truth — "the patch regresses nothing; main itself currently fails 9 xtask tests (B12 echo, handoff ×5, plane kick, behave_cli ×2), reproduced identically on pristine main, plus lattice-metal's environmental fuzz failure" — with `cargo test --release --no-fail-fast -p xtask` quoted. The evidence itself (bit-identical B18b PASS, four unseen frozen runs, this checker's three unseen probes) already carries the gold bar: it deletes a component (the frozen table) and corrects a premise (the committed gold's table was not tail-safe), adoptable in one step.

**What the author missed.**
- The two record defects above; the patch's smoke test bakes frozen run #1's exact parameters in as a dev test — worth stating outright.
- Degenerate `Params` slip through `check()`: `p_bits`/`w_bits`/`t_bits` = 0 give `mix >> 64` (shift overflow — panic in debug, silently masked in release). Unreachable from the judged SPEC; a latent trap for engine callers. Reject 0 like `kind_bits`.
- The distinctness unit test checks only the (t_p, ω, kind) projection at both sizes; full-state distinctness rests on the judge's finding at the judged seeds.
- Birth-derivation cost (~1 ms) is asserted, never measured on record; cross-machine bit-exactness is argued, not tested (the author flagged the latter).
- Cost note for adoption: `Prog` loses `Copy` (the `Arc`-held table); shipmem hot paths now clone; the judged path avoids `Prog` entirely, and `Program::bytes()` now charges the table once per population — shipmem-internal, no external consumer touched.

### 20261005-1404-redteam-b18-belt-d3e4
Grade: silver

**Abstract.** Pre-freeze red-team of the B18 belt judge (af07b33): four measured holes before the row freezes. A 15% crush of the protected e-tail's spread, a hollow inner edge of p (the game-critical side), all deep dippers in one 1/32 periapsis corridor, and a 4 MB one-level quantile table (255× the gold's bytes) each PASS all four frozen runs; criterion (4)'s byte allowance is the program's own declaration. All 13 gate verdicts reproduced exactly, margins included; PASS verdicts stable under four fresh reference draws; the byte hole verified in the judge's code. Gain: repair before freeze — F1 a mean-z tail statistic (~3 lines), F2 mirroring the tail tests at the bottom (~10), F3 a tail-conditional KS (~5), F4 one cap rule. None costs the gold program (it passes all four additions).

**Reasons.**
1. **Reproduced.** Reran both dossier commands in a clean shell (~4 min): all 13 verdicts identical — `none` passes; `table12` (0 of 105 reach, shape KS D = 1.000), `winsor`, `lattice` (χ² z = −84.73), `serial` (z = 63.15) fail; `crush85`, `innerclip`, `aligned`, `table20` pass all 4 runs; `crush75/67` fail only the 2²³ tail-shape KS (0.128/0.172 vs 0.121), `crush60/50` fail reach at 2²⁰ on seed 20261010 only. `work/patch.diff` is empty (no repo edits). `predictions.md` (14:13) predates `evidence.log` (14:21); the two reported misses (crush75, crush50's location) both confirmed here, and both understate the gate's power — the holes claimed are not overstated.
2. **Mirror fidelity checked against the judge's source** (`git show wt/b18-belt:xtask/src/behave/belt.rs`): SPEC, the SplitMix64 counter stream and `rayleigh_grid`, χ² 128×128 with dof 16383, serial at the same 18 lags + 6 pairs + 12 lag-1 cross terms, per-column two-sample KS on 2¹⁶ bins, tail order statistics with REACH_J = 20 and k = ⌈10⁻⁴n⌉, the same RUNS with stop-at-first-fail, the same thresholds. The belt-only statistics are deterministic and match the author's quoted Rust values exactly (seed 20261010: χ² z = −0.97, serial worst 2.10 at ω lag 128).
3. **My adversarial cases.** (a) Reference fragility: `crush85` and `table20` at 2²³ under four fresh reference draws each — all PASS, worst tail-shape KS 0.089 vs ~0.122 critical; the reference-family difference (PCG64 vs xoshiro) does not flip anything. (b) Recomputed the judge's true tail-count z = (X−K)/√(2K) from the logged counts for every plant and run: all within ±3.66 (limit 4.5) — see miss 1. (c) F4 read off the code: the only bindings on a Program are charge ≥ info, charge ≤ 2·info + 2, and ≤ 16 B growth in n — a stored 4 MB table declaring info = 4,194,345 B passes exactly as claimed, and the 2 GB extension holds by the same three lines.
4. **Novelty.** The judge landed 5 October (af07b33) with this red-team named as its freeze precondition; no HISTORY or docs entry red-teams it. The judge's own doc anticipates F4 in prose only ("a belt may declare a big table as information"); the measured `table20` run and F1–F3 are new.
5. **Goal fit.** AGENTS: "Gates are frozen before the first run and never weakened after" — holes found before the freeze are the cheap moment, and each disposition is separable. PRINCIPLES 24 ("the memory floor is information") is F4; the register's "I hate averages because they crush data especially tail events" is F1, measured: the gate blesses a 15% crush of the tail it exists to protect.

Not gold: the record, not the physics — the same pattern the taste log names from 5 October.

**The one experiment.** Port `crush85`, `innerclip`, `aligned` and `table20` into `belt.rs`'s `Flaw` enum (~3 lines each, beside the existing plants) and run the frozen RUNS on the real judge, logging the output in the run folder: four PASS verdicts from the judge itself, plus the echo/dyadic control output the dossier cites but does not log. That regenerates every claim from the shipped code.

**What the author missed.**
1. `probe.py:139` never computes the tail-count z: the tested and printed `z` is a stale serial-cross value left over from the loops above (the evidence.log z column for "count" is meaningless, and the dossier's "exactly the judge's statistics" is false for that one line). I recomputed the true z from the logged X: every plant and run sits within ±3.66, so no verdict changes — but the author did not know this, and "count z ≈ 0" for crush85 was luck (true −0.49), not measurement. The mirror bug also means the anchors never calibrated the count statistic itself.
2. The Rust judge run (echo/dyadic passing all four runs) is asserted with no artifact: `evidence.log` holds only the mirror output; nothing in the folder regenerates that claim.
3. All four headline adversaries ran on the mirror only — the frozen judge never saw them.
4. No reference-draw sensitivity in the dossier; I ran it (stable), and it is the obvious defence against the PCG64-vs-xoshiro objection.

### 20261004-1525-components-98bc
Grade: gold

**Abstract.** A smooth belt (banded p, Rayleigh e, uniform angles — the 10⁹-scale content shape today's `Prog::{Const,Affine}` cannot carry) fits in 16,456 bytes total: body i is a bijective counter-mix through dyadic quantile tables and `Key::darwin`, 0.126 bits/body at 2²⁰, 1.3×10⁻⁴ at 10⁹, versus 157.4 bits/body packed blocks (19.7 GB). Scars use form P's own codecs unmodified, ~60–75 bits per scarred body at any churn rate. I reproduced all three runs bit-for-bit, confirmed predictions.md pre-dates every result file, and my own adversaries (2-D χ² equidistribution, serial correlation, sustained churn) did not fire. Adoption is one `Prog` variant written by the creating event; ~10³× at birth on board focus item 5.

**Reasons.**

1. **Reproduction, exact.** Applied `work/patch.diff` to a clean tree, ran all three dossier commands (m18/m20/m23, 55 s total). Every deterministic number matches the stored jsonl bit-for-bit: blocks 157.39/157.39/157.37, `rt_bad` 0, floor 121.00, program 0.50366/0.12592/0.01574 bits/body (exact 1/n, 4× per halving as predicted), scar counts 27/267/2621/26415 → 796/8436/83758/839452, all KS and NN values, two keysets identical. Only timing fields differ (shared 2-vCPU container; orders of magnitude only, per the rules). Floor arithmetic verified: 27+12+6+32+44 = 121 bits; 121 bits × 10⁹ = 15.1 GB, 72 brutal-player bits = 9.0 GB, blocks = 19.7 GB — the premise "a lossless iid belt fits 8 GB" is arithmetically dead at any player resolution.

2. **Held-out predictions.** `predictions.md` mtime 15:37:03; first result file 15:40:15 — pre-dated, and it says "the code has not been run yet". Held: program ≤ 0.5 bits (0.126), churn ≤ 1.2 at 10⁻² (0.731), mix KS ≤ 0.002 both keysets, two-sample KS ≤ 0.004, eval ≤ 200 ns (109–129), 1/n scaling, round trip exact. Missed and self-reported: blocks 1.30× floor vs ≤ 1.25× predicted (codec overhead on the baseline arm — does not touch the claim). The 2²³ run was not in the predictions and is the held-out case: the mix passed everything there, and the lattice kill grew with density (NN p1 3.61 vs iid 0) rather than shrinking.

3. **Adversaries (mine, written fresh).**
   - *2-D equidistribution* in the (p, t_p) phase plane, 128×128 χ², n = 2²⁰: mix 16,305 vs iid 16,107 at dof 16,383 (±181). The statistic that killed the lattice does not fire on the mix. (E,L) plane: both arms deviate from uniform identically (915.9M vs 916.5M, 0.06% apart) — derived-key marginals are non-uniform by construction; the two arms match.
   - *Serial/cross structure*: lag-1 autocorrelation of p and t, and p×t cross-correlation, all ≤ 1.5×10⁻³ ≈ 1/√n noise. No counter structure in ordinal order.
   - *Sustained churn* (the author's admitted gap, now measured): 12 epochs at rate 10⁻², cumulative scarring. Scarred fraction follows 1−(1−r)^k (11.3% at epoch 12), per-scarred-body cost stays bounded at 60–74 bits (declining as Elias–Fano ordinals densify), reabsorption ≈ 0 — random kicks never exactly return a body to its program. So bits/body grows linearly (~0.58/epoch at 1%) toward ~60 bits/body saturation ≈ 7.5 GB at 10⁹ before tubes. Program+scars still beats blocks at *every* rate (≤ ~60 < 157 bits/body), but the 8 GB gate at 10⁹ needs churn × epochs ≪ 1, or re-programming of churned populations.

4. **Novelty.** H0209 established program-plus-scars, but `Prog` carries only `Const`/`Affine` (convoys, 488 B per 10⁶) and the frozen B18 ladder's scenes are convoy/poisson/random/traders — no belt rung, no quantile-table or counter-mix program anywhere in HISTORY or the docs. The lattice kill is also new evidence, not an argument.

5. **Goal fit.** Board focus item 5 verbatim: "fitting 10⁹ in 8 GB (population programs plus scars)". ~10³× at birth, deletes the packed-block store and its 19.7 GB traffic for every unchurned population. PRINCIPLES 6 ("Store the generator, not the generated"), 24 (the memory floor is information), 20 (determinism ≠ realistic trajectories — the fidelity question is behaviours, and the author measured them). The B18 charge is accurate: `xtask/src/behave/memory.rs` — "An answer under half the floor is also a failure: a lossless store cannot be there" — so a 10 KB billion-body belt fails B18 *today*, while blocks at 1.30× the floor pass it at 19.7 GB. Adding a belt rung judged on determinism + distributional behaviours + program/scar bits is a new gate, not a weakening; the sample-identity reading needs the integrator's adjudication.

**Why gold, not silver.** Exactly reproduced, predictions pre-dated and held on every claim-bearing number, 10×+ (measured 1,246×) on a live board bottleneck, the mechanism demonstrated end-to-end (eval at 109–129 ns/body, sealing through form P's own codecs, fidelity behaviours), the elegant alternative killed by measurement, and both misses disclosed. One contained step to adopt.

**What the author missed.**
- *Column correlations.* Per-column independent mixes cannot carry a belt whose columns are correlated (dynamically sculpted discs have e–p structure); a joint quantile table or key derivation is needed and costs more bits. Not in "what would make it wrong".
- *Churn steady state* (measured above): "reabsorbed for free" is vacuous under random kicks — scars accumulate as 1−(1−r)^epochs toward ~60 bits/body, which pinches 8 GB at 10⁹ with tubes on top. Birth claim unaffected; the sustained regime needs re-programming or a measured encounter-rate budget.
- *The gather*: which ordinals a view or event must materialize at 10⁹ (named in the lens section; still the binding unknown for adoption, and the Binet-cone skin interaction).
- H0209 says "no seeds"; a program is a generator. The integrator should read that line as banning averaged populations — this is not one: the mix is a bijection, every ordinal an exact individual — with PRINCIPLES 6 governing.

### 20261002-1618-components-6036
Grade: silver

**Abstract.** Claim: every kick rebinds by compiling a fresh exact-key orbit (64/orbit, reproduced bit-for-bit), where the law's shared cycle memo would amortize compiles; the naive quantized-bucket rebind is killed as built. All counters and behaviour numbers reproduced exactly (tuned (10,10): hits 83/128, ratio 0.53; r_memo 1.52 apoapsis radii vs r_split 1.2×10⁻⁵); timings within noise. I re-ran the formation the `far` panic ate: 34 compiles / 2048 kicks = 60× amortization — prediction 4 (≥128×) failed. r_memo is invariant in width and tide strength, confirming the author's construction-bug diagnosis. Expected gain: ~2× rebind once law.md's ∂/∂E,∂/∂L memo exists; exact-key dedupe for populations is licensed now. Adopt: not this code; the next experiment is named.

**Reasons.**

1. **Reproduction is exact.** Applied `work/patch.diff` (297 inserted lines, test-only, no library API touched) to a clean `main` and ran the dossier's command. Every discrete counter (hits, kick_changes, compiles, distinct, fallbacks) and every BEHAV number matches the log exactly in all 25 MEMO rows and 5 BEHAV rows; timings agree to noise (tuned today 25.4 vs 25.6 µs; eccentric ratio 0.337 vs 0.335). The `far` (p = 1000) `NoBoundOrbit` panic reproduces at the same line — which is `Rebinding::from_state` in the *exact* arm, i.e. a refusal surface of the existing library fit, not of the probe's memo construction.
2. **Pre-registration holds up.** predictions.md mtime 16:24:43 vs the decisive log 16:37:05. Better: the predictions contain claims that then *failed* (idiot index ≥5, r_memo < r_split) and are reported as failures in the dossier — post-hoc predictions do not read that way.
3. **The premise is code-grounded, not asserted.** `crates/universe`'s own `Catalogue` (bind.rs) is a slot allocator with a free list; `insert` never compares keys, and every kick path goes `kick → rebind → Rebinding::from_state` → `Orbit::compile`. `exact_distinct_keys_1orbit = 64` everywhere adds that even exact-key dedupe cannot help a single kicked body — the sharing must be across buckets (populations) or via derivative corrections.
4. **Adversarial case 1 — is r_memo a real instability of sharing?** No. r_memo = 1.524e0 at *every* width from (8,8) to (20,20) (bucket in e from ~5×10⁻³ to 5×10⁻⁷), and weaktide (w = 10⁻¹², where r_split = 1.2×10⁻⁷, i.e. the tide does essentially nothing) still gives r_memo = 1.524e0. An error independent of quantization width and of perturbation strength is a structural per-kick error in the phase/branch construction. The author's diagnosis is correct, and this invariance is stronger evidence than the (20,20) argument the dossier gives.
5. **Adversarial case 2 — the 99% hit-rate headline.** The clean KEYS trace (exact arm) shows ~1 bucket crossing per 128 kicks at (10,10), so ~99%/kick is the hit rate of an *exact* memo. The shipped memo arm realizes 83/128 (65%) with 45 bucket changes: the construction's own divergence flaps the buckets (a feedback loop). The dossier states the inference but not the gap; the realized rate is what the killed build does.
6. **Adversarial case 3 — the formation (prediction 4, never run by the author).** Dropping only the panicking `far` case and re-running: `FORMATION ships=32 width=(10,10) kicks=2048 hits=1529 changes=519 compiles=34 fallbacks=15 distinct_entries=34 amortization=60.2x`. Real order-of-magnitude cross-ship compile amortization (34 vs 2048), but below the pre-registered ≥128×, with 15 fallbacks showing the near-circular (k,p)-grid problem leaks into formations too. All exactness asserts pass over these 2048 kicks (test result: ok), so the event-state exactness control holds beyond the author's runs.
7. **Novelty.** The memo itself is law.md's existing spec ("Cycle memo, keyed by quantized (E, L) … ∂/∂E and ∂/∂L … shared by every tube with the same key") and QUADRATURE.md already names "a Hessian/remainder bound for authoritative kick reuse [as] future work" (citation verified, lines 140–141). New here: the *dynamic* key-motion/hit-rate measurement (the unmerged wt/envelope work of H0209 covered static key populations; no such file exists in this tree to re-check), the measured 64-compiles-per-orbit gap, the kill of the naive bucket rebind, and the formation amortization number. No HISTORY entry covers these.
8. **Goal fit.** Board live question 1 (kicks dominate the engine's cost). Honest outcome: the rebind's idiot index is ~2–3× (not ≥5×), the naive quantized rebind is dead, and `fit_key` (~9 µs) is exposed as the next floor. It respects PRINCIPLES 9 ("A failed experiment kills that configuration, never the method") and 6 ("Store the generator, not the generated"). Not gold: nothing moved 10× yet, nothing is deleted, and no premise is overturned — rather, the result *confirms* the law's insistence on ∂/∂E, ∂/∂L corrections.

**The one experiment for gold.** Implement the memo as law.md actually specifies it — compiled tables keyed by quantized (E, L) with ∂/∂E, ∂/∂L readout corrections (so the drift keeps the exact orbit's rates between events) — and run this same probe: if r_memo falls to the r_split scale at (10,10) with hit rates near the clean trace (~99%) and the formation keeps its ~60× compile amortization, the ~2× rebind cut plus population sharing is adoptable in one step and moves live question 1 by a measured factor.

**What the author missed.**

- The strongest form of their own kill evidence: r_memo's invariance in *both* width and tide strength (weaktide r_split 1.2×10⁻⁷ vs r_memo 1.52) is stated nowhere; it upgrades "my construction is wrong" to "a structural per-kick error, independent of quantization".
- The realized-vs-headline hit-rate gap (65% vs 99% at tuned (10,10)) and the bucket-flap feedback it implies.
- The formation measurement (prediction 4) never ran because the `far` panic precedes it; run with `far` dropped it lands at 60×, not ≥128× — a failed pre-registered prediction the dossier reports as merely "never ran".
- The `far` panic is in the existing library fit (`Rebinding::from_state`, the exact arm), a genuine weak-field refusal surface (p = 1000, e = 0.3 → NoBoundOrbit) that deserves its own line, not just a held-out refusal note.
- `crates/space`'s `tube.rs::Catalogue` *does* dedupe by exact key; the no-dedupe claim is true only of `crates/universe`'s slot catalogue (the kick path). The second adoption path should be framed as porting that dedupe, not inventing it.

### 20261003-0520-components-13ae
Grade: silver

**Abstract.** Claim: the parent-tide layer is truncation-limited, not method-limited — keeping the evection harmonic (single-averaged quadrupole slow flow) holds 10% apsidal precession to a ≈ 0.20–0.25 R_H where r9's double average is 14–127% wrong, at 0.3–2.9 events per moon orbit vs the design's 32 kicks. Reproduced bit-identically (`one.py 0.18 0.3 1`, `0.30 0.3 -1` = grid.jsonl; analyze.py tables identical; closed forms match numeric averaging at 2×10⁻¹⁶; truth converged 1.4×10⁻¹⁰). Attacks: no compounding to T=100 (6.63→6.60%), e₀=0.45 interpolates (3.9–12%), fresh phases within ~1%, independent event recount confirms the floor. Gain: ~5–30× fewer events at equal behaviour in the interior (27–83× vs the fixed 32). Not gold: P2 overreached.

**Reasons.**

1. **Reproduction: exact.** `python3 one.py 0.18 0.3 1` → rel2Q 0.31527008590196626, rel1Q 0.049865162101955074; `one.py 0.30 0.3 -1` → 1.2673802436346258, 0.46695065373794986 — bit-identical to grid.jsonl. `analyze.py` on the stored grid prints every dossier table unchanged. patch.diff is empty (no tree edits; all work self-contained in `work/`). Timestamps: predictions.md 05:31:39, grid.py 05:32:06, grid.jsonl 05:43:31 — predictions preceded the decisive grid, as claimed.
2. **Baseline is not a strawman.** The double-averaged quadrupole closed form matches its own numerical double average at machine precision (2.2×10⁻¹⁶ at 0.30/0.3), and I re-derived wdot_2Q = (3/4)(μ_s/μ_p)(a/D)³n√(1−e²) independently from that Hamiltonian. The 14–127% errors are real truncation of the averaging, not a coding error.
3. **Held-out predictions: P2 missed (author-reported), P6 5× optimistic, P3 partial.** P2 claimed ≤3% through 0.30 R_H; measured 12.8–47% at 0.26–0.30. By the lab's gold letter ("the held-out predictions held"), this blocks gold; the author reported it honestly and self-filed silver, as the 1 Oct red-team precedent requires.
4. **Adversarial cases (mine):** (a) window growth 30→100 planet orbits at 0.20 R_H: rel1Q 6.63→6.60% (pro), 11.15→11.12% (retro) — a constant rate offset, no compounding (#13). (b) e₀ = 0.45 at 0.18/0.22: 3.9–12.2%, smooth between the grid's 0.3 and 0.6 rows; e_max tracked (0.4905 vs 0.4820). (c) a = 0.35 R_H, e₀ = 0.3, pro: no escape, avg1Q 23.5% vs 2Q 64.0%. (d) fresh phases (rng 43, not the author's 42): 12.5% at 0.20/0.15/retro (author: 13.0%), 9.2% at 0.22/0.3/pro (author: 8.4%) — phase-robust as P4 asserted. (e) independent event recount without t_eval: 16.6–23.0 accepted steps per planet orbit at rtol 10⁻¹⁰ (0.30–2.18 events/moon-orbit), 2.9–4.6 at rtol 10⁻⁴ with wdot shift ≤2.4×10⁻³ — the floor claim stands, slightly conservative. (f) truth convergence at the hardest seed: 1.4×10⁻¹⁰.
5. **Novelty.** No evection/single-average/Clairaut-reanalysis entry in docs/HISTORY.md (through H0211) or the docs; the antecedent is r9's KILL of kick-avg (taste log, 1 Oct, τ₀ = 0.0036 = 0.17 R_H) and H0190's cost result. What differs now: r9 stopped at the kill; this run identifies the missing harmonic, keeps it as a compiled slow flow, re-measures the boundary (0.20–0.25 R_H), and reinterprets r9's τ₀ as an e₀-mix crossing a truncation boundary — a premise correction, plus a new number for the design's own kick floor (N ≈ 4–8 at 10% interior, error ≈ N⁻¹, 64 kicks still 8.8% at 0.30).
6. **Goal fit.** Board focus item 1 ("fewer kicks per orbit at the same behaviour: kicks dominate the engine's cost"). At equal 10% behaviour in the interior, kicks need N ≈ 4–8 vs avg1Q's 0.16–1.17 events → ~5–30× fewer events; vs the design's fixed 32, 27–83×. PRINCIPLES #3 "Nothing is evolved that can be derived when looked at (clocks, redshift, views)" — the fast average is derived, only the evection libration is computed; #19 "a fix signals the wrong representation… the right representation always just feels right" — r9's τ₀ read a truncation boundary as a method boundary; #26 — evection is pre-compute-era lunar theory. Scope kept honest (planar, µ_p = 10⁻³, parent tide only, non-resonant).

**The one experiment for gold:** the second-order (Lie/Deprit) averaged generator — or the TRACE/JANUS changeover to kicks — extending the 10% gate to ≥ 0.30 R_H at ≤ 3 events/moon-orbit, with the retrograde low-e corner and circular-birth forced-e as gates. Predicted by the author's own truncation budget (octupole+ single-average residual is only 2.8–4.7% of the evection amplitude).

**What the author missed.**

- The "0.2–0.25 R_H" envelope is prograde-leaning: at e₀ = 0.15 retrograde the 10% gate is already broken at 0.20 R_H (13.0% rng42, 12.5% rng43; 11.2% at e₀ = 0.3 fixed phase). The retro boundary is ~0.18–0.20 and should be stated separately.
- In the outer regime avg1Q loses to the design's own kick-N, badly: at 0.30 R_H retro, kick-8 is 3.8% and kick-32 0.6% against avg1Q's 46.7%. The crossover (kicks beat avg1Q) lies near 0.22–0.26 R_H and is never quoted as a number — adoption is a changeover, so that crossover *is* the adoptable fact.
- The claim's "0.2–1.2 events per moon orbit" matches neither tolerance's measured range (0.39–2.92 at rtol 10⁻¹⁰, 0.08–0.58 at behaviour tol; my recount 0.30–2.18 and 0.05–0.43). Say which tolerance, and give the range.
- The event counts in analyze.py are hardcoded from an off-script measurement, not regenerable; my recount differs by ~25% (in the claim's favour). Ship the counting script.
- fig-kickfloor.png draws an N⁻² guide while the fitted exponents are −0.97/−1.13/−0.56 and the dossier text says error ≈ N⁻¹.
- Per-event cost (closed-form drift step vs tide evaluation + Kepler round-trip) is asserted, not measured — fair on a cloud box, but the M1 re-measure should cover it.

