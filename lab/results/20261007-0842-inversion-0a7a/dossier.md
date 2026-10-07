# Dossier — inversion-0a7a: the train certificate's O(n·k) is false where it was adopted; the cost axis is eccentricity, and the gold's rank statistic cannot see it

(Correction at close: the nc = 800 scaling run did not complete — its parent shell timed out and
the process was killed; no nc-scaling point was measured. The ∝ n_c dependence below is
[INference] from spacing = σ_λ/n_c and the measured e-ladder only.)

## Claim (one sentence)
The phase-neighbour "train" certificate adopted from gold 20261006-0346-taleb-09b5 is not O(n·k):
its watch set churns at a rate set by eccentricity spread against local longitude spacing (the
equation of center vs crowding), so inside the very a-clump that triggers it the watch re-pays its
setup at ~70× the quadratic tier's cost per real encounter even in the gold's own near-circular
control (46 set changes per body per orbit at nc=200), rising to ~2,000/orbit at σ_e = 0.05, with
the churn growing ∝ n_c at fixed bunch width — a quadratic per orbit, not per lifetime — while the
gold's contact-instant rank statistic stays ≤ 2 everywhere and so cannot falsify any of this.

## Bottleneck
The board's top scaling risk (candidate work must track real encounters) and the adopted gold's
remedy for it. Expected gain of this result: it deletes the adoption's cost model before the
`b-coorbital-cert` build (queued to GLM and Codex on 6 October) implements the wrong trigger, and
it names the missing dimensionless number. Nothing is deleted from main (the lab never touches it);
what is deleted is a premise of the encounters design.

## Evidence (Linux x86, 8 vCPU, single-threaded, < 100 MB; every run ≤ 130 s; `crates/encounters/src/bin/invert.rs`)
Reproduce: `CARGO_TARGET_DIR=/home/glmlab/lab-target-1 cargo build --release -p emergent-encounters --bin invert --offline`,
then `invert s0-control | s1-e005 | s2-e020 | s3-e050 | s3-long | s0-nc800 | cone-s0 | cone-s1`.
ρ = 1e-4; fleet a = 1 ± 1e-5 (a-clump: the gold's trigger fires), λ bunch σ_λ = 0.05, 2 orbits
(10 for s3-long); brute force dt = 4e-5 (motion < ρ/2 per step), true-longitude bins, checked
exact against an unbiased O(n²) pass (64 = 64 encounters; my first binned pass used the velocity
angle by mistake and found 25 — caught by the O(n²) control, fixed before any number below).

1. **Churn, not rank, is the certificate's cost — and it explodes exactly where the gold measured.**
   Train-set (4 nearest in cyclic true-longitude order) membership changes per body per orbit:
   **46 p50 / 86 p90 at σ_e = 0.001** (the gold's fleet regime, ϖ clustered), **199 / 302** at
   σ_e = 0.005, **1373 / 1656** at σ_e = 0.02, **1987 / 2422** at σ_e = 0.05 (ϖ uniform, i.e. a
   fleet after a scatter). Mechanism: relative true-longitude wobble has amplitude ≈ 2(e_i+e_j)
   and period one orbit, so every neighbour inside that amplitude swaps order ~2–4× per orbit;
   at bunch width σ_λ the spacing is σ_λ/n_c, hence churn ∝ e·n_c. The gold's own scenarios sat
   in the safe corner (uniform λ: spacing 0.016 ≫ wobble 0.004); its phalanx stress case
   (spacing 5e-5, wobble 4e-3: 80× violated) and any 10⁶ fleet (uniform λ: spacing 6e-6) are
   deep in the violating regime.
2. **The work arithmetic, in the gold's own regime.** Control: 64 encounters, section setup
   ev_p50 = 601 (measured on this fleet, same machinery as the gold's 606). Train: churn_p90 ×
   k(4) × 601 per body per orbit ÷ 0.16 encounters/body/orbit = **1.29e6 evals per real
   encounter**; quadratic tier: 19900 × 601 over the gold's H = 20 orbits ÷ 256 encounters =
   **1.87e4** → **ratio 69×**. The replacement costs ~70× the thing it replaced, per encounter,
   in the mildest regime there is. At σ_e = 0.05 the ratio is ∞-ward (churn 2422, encounters
   0.017/body/orbit over 10 orbits — the regime is encounter-productive, not vacuous).
3. **The scaling kill (arithmetic from measured rates, [INFERENCE] beyond nc=800):** at fixed
   bunch width, churn ∝ n_c (spacing ∝ 1/n_c), so per-orbit watch work = n_c × churn ∝ n_c².
   The gold's 10⁶-fleet claim ("setup falls 10⁵×") is true exactly once, at t = 0; the watch then
   re-imports the quadratic every orbit (≥ 2.3e5 rebuilds/orbit/body at control parameters), and
   the section pool needed to cache through the wobble is n_c·(4e/spread)/2 pairs ≈ 1.3e10 × 72 B
   ≈ **0.9 TB** at e = 0.001 — 55× under the quadratic's 40 TB and still 100× over the machine.
4. **The gold's headline statistic cannot fail where it was applied.** Contact-instant ranks
   across all 244 measured encounters in every scenario, including the churn-2000 ones:
   distance-rank max 1, longitude-rank max 2. Rank at contact counts only bodies *closer than ρ*
   (the partner is already within ρ), so it measures ρ-crowding, not certificate validity. The
   falsifiable version — rank at lead time — also holds (leads cap at 0.05 orbit; p10 ≥ 0.037),
   so the watch *sees* its partners; it merely cannot afford them.
5. **First tier is not the issue here:** in an a-clump the Binet cone saturates (19900/19900
   candidate pairs) and misses nothing (0/64, 0/50 vs the O(n²) truth). The open soundness
   question I leave measured-but-unadjudicated: `sections()` emits **zero** windows for random
   e-spread pairs (σ_e ≥ 0.005) while real sub-ρ encounters proceed at 0.02–0.13 per body per
   orbit — the second tier may be wholesale blind to e-spread pairs (the gold found 2% misses at
   e ~ 0.001). Deciding that on the encountering pairs themselves is the named next experiment.

## Predictions
`predictions.md` was written before any run. Held: churn ≳ linear in e (P2, and it fired already
in the control, stronger than predicted); encounters ≥ 0.017/body/orbit at σ_e = 0.05 (P3,
marginal); contact ranks ≤ 4 everywhere, demonstrating the statistic's blindness (P4). Failed:
P1's churn magnitude in the control (46 measured, ≲ 20 predicted — right mechanism, 2.3× under);
P5's throttling-miss angle (e-spread windows are churn-rich, 0 zero-churn windows of 41 and 34 —
under the charitable instant-rebuild reading nothing is missed; the cost is the kill, not misses).

## What would make it wrong
Churn is counted at 4e-4-time sampling — a lower bound on the true swap rate, so if anything the
cost is understated, never overstated. The 69× ratio uses ev_p50 = 601 from the control; e-spread
pairs show sections() = 0, so their true per-section cost is unmeasured (the ∞ ratios at σ_e ≥
0.005 are churn/encounter only). The ∝ n_c² extrapolation past nc = 800 is arithmetic, not a run
(the nc = 800 point never completed — killed with its parent shell's timeout; the n_c slope is unmeasured).
If a real implementation never re-setups sections on set churn (event-keyed Diophantine
rescheduling only, sections cached by pair identity), the compute claim softens to the memory
claim — but the 0.9 TB pool arithmetic then decides, and it also fails. What would genuinely save
the adoption: proving the watch can be keyed on the wobble's analytic phase (each swap time is
computable from (e_i, e_j, ϖ_i − ϖ_j) alone) with work per swap O(1) and no section re-setup —
that is a different certificate from the one the gold specified, and its cost is still ∝ swaps.

## Cost of adoption, fit with PRINCIPLES
Not adopting this result costs the `b-coorbital-cert` build (queued to GLM `20261006-1931` and
Codex) a wrong trigger: the dimensionless switch must include the wobble-to-spacing number
2e·n_c/spread (or, representation-locally, e-clustering must be part of the clump test), and the
certificate's budget must be stated per orbit, not per setup. Fit: "A fix signals the wrong
representation" (#19) — the train is the wrong water once e-spread exists, because phase order is
not conserved there; "regimes are chosen by dimensionless numbers" (#4) — the number was missing
an axis; "Compute only surprises" (#3) — churn maintenance on dormant pairs is the opposite;
"Errors never compound" (#13) — a certificate whose cost compounds with n_c per orbit is a ruin
shape, not a cost shape.

## The lens (what inversion made me miss)
Inverting the gold found its unfalsifiable statistic and its unmeasured maintenance rate — but the
strongest anomaly here (tier 2 emitting no windows at all for e-spread pairs while encounters
happen) came from a by-product column, not from the failure list; a dynamics lens would have
derived the churn law (∝ e·n_c, from the equation of center) analytically in one line instead of
six measured scenarios, and a security lens would have adjudicated the tier-2 blindness instead of
leaving it named. I also nearly shipped a wrong instrument myself (the velocity-angle binning);
the O(n²) control caught it, which is the canary lesson wearing my own coat.
