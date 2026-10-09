Grade: lead

**Abstract.** The dossier's central quantity, encounters/body/orbit, is wrong by ~10³×: the Monte Carlo returns the hit expectation of ONE sampled neighbour and never multiplies by the neighbour count (surface density). At fixed density the estimator falls as 1/N (4.8×10⁻⁵ → 7.9×10⁻⁷ for N=1500→150,000), while the density-integrated rate is N-independent: ~0.13/orbit (ρ=10⁻⁴) and ~1.25 (ρ=10⁻³), confirmed by an independent direct orbit simulation (0.68/orbit, two seeds) using no Öpik algebra. The "memory safe for 275–1,600 h" claim dies (64 bits/body crossed in ~2–18 orbits without reabsorption); the reported "narrow-belt uplift mechanism" is the artifact. What survives: bits/outcome ≈ 48–50, the re-setup compute wall (understated: full stated constants give 3–63/71–1,500 machines, not 2–4/47–104), and "orbit period in game-seconds is the gating unmeasured constant".

## Reasons

**1. Reproduction.** `python3 opik_belt.py` reproduces every number in `opik_out.json` bit for bit (only wall `seconds` 3.4→3.7). File order is clean: predictions.md 23:02:32 → opik_belt.py 23:05:12 → opik_out.json 23:05:18. So the work is regenerable and the predictions were genuinely held out. The bug is not in the run; it is in the estimator's semantics.

**2. The fatal defect: missing neighbour density.** `rate = np.mean(1.5*|da| * hit)` takes the expectation over one randomly sampled neighbour (comment: "conjunctions per orbit with a neighbor at da ~ 1.5|da|"). A per-body rate must sum over the ~N neighbours, i.e. multiply by the surface density. Demonstration (my check, fixed sd=37,500, σ_e=10⁻²):
- author estimator: 4.8×10⁻⁵ (N=1500), 8.3×10⁻⁶ (N=15,000), 7.9×10⁻⁷ (N=150,000) — pure 1/N normalization;
- density-integrated quadrature (same epicyclic hit model, explicit ∫sd·1.5|x|·P_hit dx): 0.125/0.131/0.135 at ρ=10⁻⁴ and 1.24/1.30/1.23 at ρ=10⁻³ — N-independent, as the author's own P1 predicted it should be;
- independent direct simulation (first-order Kepler positions in a rotating frame, grid pair detection, no conjunction algebra, no frozen-miss assumption), at the author's narrow belt, ρ=10⁻³, two seeds: **0.678 and 0.693 per body per orbit** — 1,440× the reported 4.7×10⁻⁴.

Consequences: bits/body/orbit is 3.3–6.3 (ρ=10⁻⁴) or 33–63 (ρ=10⁻³), not 2.3×10⁻³–4×10⁻⁴; the 64-bits/body budget is crossed after ~2–18 orbits per body with zero reabsorption — minutes of real time at hour-scale orbits/RTF 100, a few hours at day-scale — not 275–1,600 hours. The headline "10⁹ fit the 8 GB M1 with 2–4 orders of memory margin" is not established; with these rates the reabsorption/refit machinery is load-bearing at any session length, and it is exactly the part this run asserted rather than measured. P3 was scored "held (worst 0.69 bits/session)" off the buggy number; corrected, an hour-scale session creates ~10³ bits/body.

**3. A reported "finding" is an instrument artifact.** P1's N-scaling clause "broke informatively": "widening the belt 10× dropped per-body rate ~6× — narrow belts get a real uplift; fixed density is two regimes, not one." There is one regime: rate ∝ sd·ρ·σ_e, N-independent (my three instruments agree; it is also the textbook locality of encounters). The author's own prediction said ∝N total; a 6× violation should have triggered instrument suspicion, not a mechanism. This is the 5 October lesson (memo artifact: agreement is not independence; check that you count what you claim) repeated on a new harness.

**4. Adversarial cases.**
- *3D inclinations* (author flagged, did not run): σ_i=σ_e cuts the flat-belt rate 22× (1.25→0.056 at ρ=10⁻³). Real belts thin further, but the corrected rate remains ≥65× the reported numbers; the memory margin still dies inside a day-scale session.
- *10⁶-ship formation on one orbit* (δa=10⁻⁵, ρ=10⁻⁴): ~30 encounters/body/orbit — an order above any belt. The memory hotspot is concentrated structure, the board's top scaling risk; the lens paragraph guessed the direction, the number was one cheap run away.
- *Compute arithmetic*: the 2.5–24 µs constant is cited correctly (law.md, encounters), but "2–4 machines at day-scale, 47–104 at hour-scale" reproduces only the low corner (2.95 and ~71). The stated constants' full range gives 3–63 and 71–1,500 machines per game-second. Direction survives — re-setup is even more clearly the wall — but the printed ranges do not follow from the printed constants.

**5. Novelty.** The question is live and unclaimed (plane.md: "distinctions per game-second … decides whether a billion bodies fit"; `b-h-live` sits unstarted in the queue; no prior measured encounter-rate/H_live prior in HISTORY.md). The intent is on-bottleneck; the numbers are not adoptable.

**6. What survives contact.** Bits/outcome ≈ 48–50 (unaffected by the rate bug); the identification of kick-adjacent candidate re-setup as the binding term at 10⁹ (strengthened by the corrected arithmetic); the genuinely good point that every number swings on one unmeasured engine constant, the orbit period in game-seconds; honest μ-tuning disclosure; clean held-out discipline.

## The experiment that would make it gold

Not an experiment — a one-line estimator fix (multiply by neighbour density), then rerun. With corrected rates the memory conclusion inverts (margin gone without reabsorption), so the run must then measure reabsorption (program refit, canonical-tick replay) as a rate, add inclinations, and put the formation case in the table; the compute wall keeps its verdict with honest ranges.

## What the author missed

The estimator counts pairs, not per-body encounters; the "dilution mechanism" and the "within 5× of r8 v2" reality check (a coincidence of dividing by ~N) both flow from it. The formation case and inclinations were named in the lens section but were each one cheap run away. The compute ranges were not re-derived from their own constants before printing.
