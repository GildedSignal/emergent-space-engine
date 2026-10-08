# Dossier — 20261008-0615-library-83f9 (library lens)

**Claim.** From Julien's library: level-triggered scheduling (the practitioners' transplant) is exactly right for the slack skin but is KILLED, by measurement, as a kick-cadence rule — local field derivatives (magnitude, jerk) carry no kick-allocation information, so cadence must be decided by the certificate residual (the energy register), and near the unpredictability wall the rule must choose a representation, not a rate.

**Bottleneck.** Board #1: kicks dominate engine cost (q-cadence: "what rule gives each body its cadence"); spatial twin: the slack skin (b-encounter-skin, building now). Gain: kills a dead-end family of cadence rules before two builders spend windows on it; makes the skin refresh a scheduled event (zero per-frame checks) instead of a poll.

## Evidence

Surrogate of the kick layer (`exp_cadence.py`; N=1000 belt, a∈[0.95,1.05] AU, μ=1, one perturber μ_p=3e-3 at 1.6 AU, T=10 orbits, exact Kepler drift + impulse kicks, truth = same machinery at 512/orbit, medians over seeds 1–3):

```
cd lab/results/20261008-0615-library-83f9 && python3 exp_cadence.py cold   # 28 s
cd lab/results/20261008-0615-library-83f9 && python3 exp_cadence.py hot    # 29 s
```

Cold belt (σ_e=0.05); hot belt agrees (JSONs in this folder):

| policy | med_err | total kicks |
|---|---|---|
| fixed16 | 6.0e-5 | 160,000 |
| fixed32 | 2.9e-5 | 320,000 |
| mag δ=1e-5 | 1.7e-5 | 812,804 |
| jerk δ=1e-6 | 1.5e-4 | 206,746 |

- **Magnitude trigger** (schedule at dt=δ_v/|a_pert|): reaches fixed16's med error at ≈550k kicks — 3.4× more than the clock. Pre-registered kill P4 fired.
- **Jerk trigger** (dt=√(2δ_v/jerk_est), jerk from d, ḋ, n_rel — all local, closed form): across the sweep error ∝ δ^0.5 and kicks ∝ δ^−0.5, so matching fixed16 needs δ≈1.7e-7 → ≈500k kicks — 3.2× more than the clock. P5 failed; P8's antecedent holds.
- Kick distribution under both triggers is nearly flat (k_p99/k_med ≈ 1.2–2.3): triggers spread kicks uniformly; they cannot see conjunction phase. The clock is not allocating anything either — it just doesn't pretend to.

**Predictions.** `predictions.md` was written before the run. P1 (4× fewer kicks) and P2 (fat tails, ≥8×) **failed**; P4 (kill criterion) **fired**. A diagnosed variant (jerk) was then appended, disclosed as post-hoc, with P5–P8; P5–P7 failed, P8 fired. Two wrong predictions and one pre-registered kill — the kill is the result.

## The five lessons (each changes a decision; quotes verbatim from the library, `highlights.tsv`)

1. **Schedule kinematic staleness; never poll it.** — *"A rocket ship requires just this kind of in-advance calibration… every thrust, every firing of a booster, and every change in direction… too many startup business plans look more like they're planning to launch a rocket ship than drive a car."* (Eric Ries, The Lean Startup). Mechanism: Åström's event-based sampling; GROMACS predicts the next Verlet-list rebuild from max displacement instead of checking every step. **Change:** b-encounter-skin's refresh is a scheduled event, dt = (skin/2)/v_rel,max, one division per refresh, zero per-frame checks — kinematic quantities only, where the transplant is sound. **Test:** count refresh checks vs refreshes on a belt scene; checks → 1/refresh at unchanged encounter sets.
2. **The cadence transplant is killed: error allocation is not a local field quantity.** — *"Step one should be to question the requirements… Make them less wrong and dumb, because all requirements are somewhat wrong and dumb. And then delete, delete, delete."* (Elon Musk, Walter Isaacson). Mechanism: measured above — the per-orbit cadence requirement and the local-derivative replacement are both deleted; what survives is cadence decided by the projected residual against the energy register's quantum (rate-distortion: kicks are bits; spend them where the register is about to flip). **Test:** this run (P4/P5/P8). Cost: q-cadence must read the register, not the field — matches b-energy-register (queue #2).
3. **One bar, two scales: the skin is the cadence in space.** — *"Chunking relates to the mind's ability to take lots of information, find a harmonizing/logically consistent strain, and put it together into one mental file that can be accessed as if it were a single piece of information."* (Josh Waitzkin, The Art of Learning). Mechanism: r-RESPA slow-force averaging (H0190 already measured 114×); the same residual bar δ sets the temporal chunk (kick interval) and the spatial chunk (skin width). **Change:** b-encounter-skin and q-cadence share one δ in the register's units — one law at every scale (principle 33). **Test:** once both exist on the plane, sweep one δ and hold B12–B17.
4. **Ship the rule that emits cadences, not cadences.** — *"It's not the product that leads to success. It's the ability to make the product efficiently… how do you design the factory?"* (Elon Musk, Isaacson). Mechanism: the six disagreeing cadence runs are six hand-built products; the factory is one rule whose inputs are each scene's local numbers. **Change:** q-cadence's acceptance includes reproducing each prior run's necessary cadence from its scene and explaining the disagreement, not averaging it; constraint added by this run: the rule may not read the field's local derivatives. **Test:** refit the published scenes from their dossiers.
5. **Barbell the wall: choose a representation, not a middle rate.** — *"So just as Stoicism is the domestication, not the elimination, of emotions, so is the barbell a domestication, not the elimination, of uncertainty."* (Nassim Taleb, Antifragile). Mechanism: dynamics-a9c2 — inside resonance no rate to 64 matches a librating truth; a middle cadence pays the tail twice (too many kicks for coasters, too few for the wall at 1−a ≈ C·μ^(1/4)). **Change:** the cadence rule's output near the wall is a representation choice — coast on the generator or drop into the exact regime (rotating binary doll) — never an intermediate rate. **Test:** resonant pair scene: the rule must escalate, and B14's libration must hold.

**What would make it wrong.** The surrogate is not the plane: one perturber, no encounters, no resonance, impulse-at-end kicks; the plane's kick layer (averaged tides, J2, two-body parents) could allocate differently. The kill is on the rule family (local closed-form rates), tested on magnitude and jerk — a smarter local invariant (resonance phase distance) might still beat the clock; the run cannot exclude that, but P2's flat distribution says the phase information is what's missing, and phase is not a field derivative. Adoption of lessons 1/3 costs nothing in physics (scheduling only); lesson 2 redirects q-cadence to the register. Fit with PRINCIPLES: "no work for no reason, so no ticks" (14), "the simulation decides; heuristics schedule" (22), "A failed experiment kills that configuration, never the method" (9), "Steal what works, from skin in the game" (26 — and the steal failed where the skin in the game differs: MD schedules kinematics, not physics error).

**The lens (blind spot).** Business-book quotes dressed as engineering can smuggle false authority; here every mechanism was re-grounded by measurement, and the two "obvious" transplants died. Anchors are Julien's self-help/business shelf (Kelly, Boyd owned but unhighlighted, so unused); a physics-practitioner shelf (Bate-Mueller-White, Encke's actual correspondence) might anchor lesson 2 better. The 60-minute window allowed one δ sweep per scene, no resonant scene, no plane run — adoption requires the plane's builders to re-measure.
