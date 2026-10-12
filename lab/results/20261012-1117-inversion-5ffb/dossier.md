# dossier.md — 20261012-1117-inversion-5ffb (lens: inversion)

## Claim

The co-orbital phase certificate as built (`wt/cx-b-coorbital-cert`,
`crates/encounters/src/phase.rs`, from lab gold 20261006-0346-taleb-09b5) is
sound but cost-blind: its only trigger is `reach < pi`, and inside that zone
— any group with one shared period and eccentricity spread (a fleet after
eccentricity excitation, an eccentric ring) — its candidate work is
`0.2–0.45 · n^2` exact pair solves per window (measured exponent 2.00–2.009),
independent of the encounter rate, while the general tree tier it silently
shadows returns the identical contact set 3.4–4.1× faster; the tree itself
also degenerates to all-pairs on these scenes, so in the concentrated-but-
eccentric regime nothing in the adopted design is subquadratic per window.

## Bottleneck

Board item "finding encounters without work per orbit" and the top scaling
risk ("candidate pairs per body grow with N; candidate work must track real
encounters"). The gold closed the tight-formation seam (135× work per
encounter, dropped contacts); this run shows the seam moved, not closed, for
the eccentric middle. Expected gain of a fix: delete the constant-factor loss
(≥3.4×) now, and the Θ(n²) term needs a representation that tracks encounter
rate (ρ), not shape spread — the certificate's `reach` is ρ-independent to
first order, so at ship-scale ρ (ρ/a ~ 1e-10) it pays ~n²/2 checks per window
for zero encounters.

## Evidence

All numbers from the branch's own sources, verbatim (`files_sha256` in
`artifacts/evidence/cx-b-coorbital-cert-20261010/summary.json`), extracted to
`work/certlab/` (see `work/RESULTS.txt` for all rows), plus one added pub
measurement hook `phase::tree_events`
(the unmodified `else` branch of `group_events`) and `src/bin/invert.rs`.
Machine: shared Linux x86 runner, 8 vCPU, load average 2.1, release build.
Orders of magnitude only (cloud timing rule).

Commands (each ≤ 60 s where possible; `cost` rows are the exception, noted):

    cd lab/results/20261012-1117-inversion-5ffb/work/certlab
    cargo build --release          # sources: git archive wt/cx-b-coorbital-cert crates/encounters
    $CARGO_TARGET_DIR/release/invert bounds   # ~220 s
    $CARGO_TARGET_DIR/release/invert fuzz     # ~86 s
    $CARGO_TARGET_DIR/release/invert cost     # series rows 5–490 s each; see run.log

1. **Soundness held (both-sides controls).** 32 seeded scenes, 20,396
   golden-section-refined sampled contacts: `cert_miss=0 emit_miss=0
   tree_miss=0`. Scenes cover the transition zone (mixed e 0.25–0.65, reach
   2.81, k≈0.8n), shared-shape e=0.9 at epochs up to 9e7 (numerical guard),
   drift 0.53, seam-straddling pairs swept through the certificate's exact
   boundary (1,935 contacts/scene), and the home regime (k=2–3). Tree control
   agreed everywhere. The bounds audit: `centre` is a true bound (min slack
   +6.3e-11, tight as e→0); the `|f−E|` component is an exact identity
   (min slack −3.7e-16 = 1 ulp); `scale` differs from max dM/df by −1.4e-14
   (~6 ulps, float rounding of `powf(1.5)` at e=0.981) — negligible against
   the 64·EPS·(1+n·t) guard.
2. **Home regime reproduced (their gate):** shared shape e=0.02:
   `pairs == n, k == 1` at n = 10^4, 10^5, 10^6. Linear, as sold.
3. **Transition zone is quadratic, measured.** Shared period (drift = 0
   exactly), e ~ U[0.05,0.30] ("battered fleet"): reach 1.22, k = 0.21n,
   cert_pairs = 193,147 / 777,626 / 3,113,680 at n = 1,000 / 2,000 / 4,000;
   exponents 2.009, 2.001. e ~ U[0.05,0.65]: reach 2.83, k = 0.47n,
   cert_pairs = 446,849 / 1,798,708; exponent 2.009. Wall time follows
   (86 s at n=4,000 mild-e on this box).
4. **The certificate loses the A/B on its own trigger.** Same scenes through
   `tree_events` (the exact fallback branch): identical contact sets
   (`same_contact_set=true` at every n), t_cert/t_tree = 3.5 / 3.4 / 3.5
   (mild-e) and 4.0 / 4.1 (wide-e). `group_events` never compares cost: it
   takes the phase certificate whenever `Neighbours::new` succeeds.
5. **The tree degenerates too.** tree candidate count = C(n,2) exactly
   (499,500 at n=1,000) on these scenes: same-a eccentric orbits all cross,
   so the Binet cone prunes nothing. Both tiers are Θ(n²) per window here.
6. **ρ-independence (the inversion core), wide-e n=2,000:** ρ = 5e-3 →
   cert_pairs 1,799,213, contacts 74, 24,314 pairs/encounter; ρ = 5e-4 →
   1,791,004 (−0.5%), contacts 3, 597,001/encounter; ρ = 5e-5 → 1,790,214
   (−0.5%), contacts 1, 1,790,214/encounter. A 100× thinner encounter tube
   leaves candidate work unchanged: `reach` enters through ρ only via
   `angular ≈ 2·asin(ρ/2·r_min)`, negligible against 2·centre. Candidate
   cost tracks shape spread, not surprise rate — at ship-scale ρ (ρ/a ~
   1e-10) this is ~n²/2 exact pair solves per window for ~zero encounters.
7. **Refusal is narrower than designed (falsified toward the worse):** the
   a-spread belt (a ∈ [0.4,2.2], e ∈ [0.05,0.65], H = 0.05) did NOT refuse:
   phase=true, reach 2.93 < π, tree never consulted (tree_cand=0), 120.9 s.
   The drift term is (nhi−nlo)·H/2 — with short horizons a-spread is
   irrelevant, so the quadratic zone is "any group with e_max ≲ 0.68",
   regardless of period spread. Only long horizons push groups out to the
   tree.

## Predictions

`predictions.md` was written before the decisive `cost` run. P1–P3, P5, P8,
P10 held (P5's ratio "tens to hundreds" was too high: it is 3.4–4.1). Three
failed, each honestly: P4 (tree subquadratic) FAILED — the tree is also
all-pairs on crossing rings, itself a finding; P7 (a-spread refusal)
FAILED — short horizons zero the drift term, so the belt stayed inside the
certificate (strengthens the claim); P9 (|f−E| bound violated by ~2e-3)
FAILED — my analytic disproof contained an arithmetic error, the audit
shows the bound is an exact identity. The core falsifier, ρ-independence,
held with the numbers above. P9 FAILED and I am glad it did: I derived analytically
that the `|f−E|` bound was ~2e-3 too tight at e ≥ 0.35; the exhaustive audit
shows it is an exact identity (my arithmetic error — the audit is decisive).
The ρ-scan prediction (work does not track encounter rate) is the run's
core falsifier and held.

## What would make it wrong

Scenes with mixed e but *different* periods drift out of the certificate's
zone (refusal), so the quadratic window requires near-shared periods — but
that is exactly what a formation is after any eccentricity excitation, and
the gold's own scenes (gold-adj max_k=85 of n=200) already sat at 0.4n²
occupancy. The cost comparison could flip on hardware where `pair_events`
is relatively cheaper than the tree's arming; the contact-set identity and
the pair-count exponent are hardware-free. If in the real engine fleets
always share (e, ω) exactly (pure formations), the transition zone never
fires and the finding is moot — but then any single scattering event breaks
that purity, and the certificate does not notice.

## Cost of adopting / fit with PRINCIPLES

Fix is one comparison at the trigger: refuse (or bucket by e) when expected
occupancy `n·reach/TAU` exceeds the tree's per-body cost, and make `reach`
see ρ. Deleting the phase certificate entirely would cost nothing on these
scenes (tree wins them) and keep the tight-formation win only if the tree
keeps its zero-miss guarantee there — which their `before` numbers show it
does not (dense-ring: 512 misses before). So: keep the certificate, add the
cost term. This is "compute only surprises" (§3) and "no work for no reason"
(§14) applied to a trigger that currently keys on correctness alone; also
"the simulation decides, heuristics schedule" (§22) — the scheduler here
(group_events) is not looking at what the work costs.

## The lens

Inversion asked "how does the adopted gold fail silently?" and found the
cost blind side rather than a correctness hole — the certificate's math held
under every adversarial scene I could build, including my own wrong
disproof. What the lens may have missed: I did not test 3D/inclination or
retrograde populations (Body is 2D prograde by construction — a domain
assumption of the whole crate, worth a named invariant), and I did not
measure steady-state amortization across windows (a real horizon schedule
might spread the quadratic work; the certificate is rebuilt per window, so
I doubt it, but it is unmeasured).
