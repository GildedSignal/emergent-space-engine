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
