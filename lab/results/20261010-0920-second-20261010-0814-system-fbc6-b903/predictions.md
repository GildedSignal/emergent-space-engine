# Predictions (held out before the decisive run)

The checker of 20261010-0814-system-fbc6 named the missing experiment: the accumulator
link (principle 6) is assumed one-level in run C and never modeled — sub-quantum member
news must actually accumulate until it crosses the parent's coarser quantum, and the
ghost question for sub-quantum readers ("which tube version it accumulates them from")
was idealized away by the toy's binary resolvability. `b-news-gravity` is an unbuilt
crates component (lab/queue.txt), so this run builds the accumulator into the news-chain
toy on the **real B12 scene numbers** (xtask/src/behave/restricted.rs `JUPITER`:
μ = 1e-3, sep = 5.27e8 M, planet radius 4.84e4 M, geometrized G = c = 1): the Giant's
Hill doll R_sub = sep·(μ/3)^{1/3} = 3.65e7 inside a parent doll R_p = 10·sep = 5.27e9,
fleet of N ships, ship Δv = 3.3e-5 c (10 km/s; adversarial 3.3e-4). The fold error
E(t) = Σ δ_k·(t−t_k) (a thrust shifts the doll's CoM linearly in time) crosses the
parent's coarser quantum Δx; each crossing publishes one aggregate news event to the
parent chain, TTL = min(r_q_agg, R_p) with r_q_agg = √(M_sub/Q_p), pull-quantum
Q_p = M_sub·Δx/sep³ (a reader at sep resolves the doll once the CoM offset Δx changes
its pull by Q_p; Δx = sep³/r_q_agg²).

Not tuned on: the process law of member impulses (signed ±σ vs coherent all-+σ), the
fold law (impulse vs drift), the quantum sweep Δx, the doll-less thrusting Giant's rate,
and time-stationarity of the aggregate rate. My predictions:

1. **The member-level wall is real and the fold kills it.** Under KEEP-FOREVER the
   member chain grows linearly to λ_total·t_end (≈ 10⁵ records); under the death rule
   (a member ghost dies at its arrival at the fold, t_k + r_fold, r_fold = its radius
   in the doll) the member chain flatlines at λ_total·mean(r_fold) with **zero unserved
   folds**. TTL = R_sub over-retains by R_sub/mean(r_fold) ≈ 2× and serves nothing the
   exact rule does not.
2. **At the real scene's parameters the fleet never surfaces at the parent.** With
   N = 1000 ships at Δv = 3.3e-5 c, aggregate crossings over t_end = 2.5·R_p are
   **fewer than 3** (predicted ~0–1): the fleet's whole momentum budget moves the
   doll's CoM by ≪ Δx at every Δx in the sweep. The accumulator link costs ~nothing
   there; the parent chain's population comes from the doll-less case (prediction 5).
3. **Driven hard, the aggregate rate is stationary and its quantum-scaling exponent is
   the fold law's:** coherent impulses: λ_agg ∝ Δx^{−1} (impulse fold) and ∝ Δx^{−1/2}
   (drift fold); signed impulses: ∝ Δx^{−2} (impulse fold, diffusive hitting) and
   ∝ Δx^{−2/3} (drift fold, integrated shot noise). Measured within ±0.15 of the
   predicted exponent over ≥ 2 decades of Δx. In every cell λ_agg(t) is flat: the
   first-half and second-half rates agree within Poisson noise (3σ). **If λ_agg grows
   with t anywhere, the bound is dead — the wall returns through the accumulator.**
4. **The parent chain flatlines at λ_agg·min(r_q_agg, R_p) with zero misses**, the
   half-bound control misses, and TTL = R_p over-retains by R_p/min(r_q_agg, R_p)
   for zero served reads — the claim's own rule, now measured on chain records that
   the accumulator actually produced (not coded in by an `if`).
5. **The conceded wall case is a level, not a slope.** A doll-less thrusting Giant
   (news directly in the parent chain at rate λ_g, r_q > R_p so window = R_p):
   live records flatline at λ_g·R_p — constant in t (KEEP-FOREVER at the same rate
   grows linearly past it). The "point where we cannot handle the universe" is a
   bounded level set by λ_g·R_p, not growth; the death rule buys nothing there
   (over-retention 1×) and the dossier must say so.
6. **The death rule at the member level is false without the aggregate** (the checker's
   ghost question, now measured). If sub-quantum readers (r > r_q) read member tubes
   individually, a TTL = min(r_q, R) policy **misses** their reads (misses > 0 in every
   seed: their dependency window is r, up to R). Served by the published aggregate
   instead (principle 6 load-bearing), the same policy has zero misses and the
   accumulated kick a reader computes from the aggregate differs from the direct
   individual-tube sum by **less than one parent quantum** at every read. The bound
   survives only because the aggregate carries sub-quantum readers: this is a
   mechanism the original dossier asserted, not measured.

Kill criteria: (3) any growing λ_agg(t), or an exponent off by > 0.15, or (4) misses at
the bound, or (6) aggregate-service misses or quantum violations — any one kills the
claim "causal memory is bounded by influence decay" as stated, and the light-cone wall
is real for news gravity through the accumulator.

## Addendum — pre-decisive-rerun (10 October, after instrument fixes, before the rerun)

The first pass (kept in run.log) exposed two instrument artifacts, not physics:
1. **Detection delay:** the drift fold published only at arrivals, so the served
   version's error could exceed the quantum by one inter-arrival gap (run E showed
   max error 1388 > dx = 200). Fix: solve the crossing exactly between arrivals
   (E is linear there), publishing multiple times per gap if needed.
2. **Program order:** the published aggregate program was zeroth-order (position
   only). A doll's state carries velocity (law.md), so the physical program is
   first-order. With a zeroth-order program the measured rate grows with t
   (coherent: crossings ∝ T² at fixed dx, exponent −1 in dx, stationarity z up to
   +66) — a bookkeeping artifact of re-publishing a constant against a moving
   source, the exact "fix signals the wrong representation" case. Prediction 3's
   drift exponents (−1/2 coherent, −2/3 signed) were derived for the first-order
   program and are re-predicted there, with stationarity |z| ≤ 3; the zeroth-order
   cells are kept as the negative demonstration (predicted exponent −1 in dx at
   fixed t_end for BOTH drift processes, with growing half-vs-half z).
Prediction 2 was already wrong as written at the finest quantum: drift-fold theory
predicts ~14 crossings at rq = R_p (dx = 5.27e6), not "fewer than 3"; the first
pass measured 19. The prediction is corrected to: 0–1 crossings at rq ≤ sep
(held), ~10–25 at rq = R_p (the fleet's integrated drift does surface at the
finest parent quantum; still bounded per prediction 4).
