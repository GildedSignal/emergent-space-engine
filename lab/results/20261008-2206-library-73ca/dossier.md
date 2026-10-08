# Dossier — 20261008-2206-library-73ca (library lens)

**Claim.** From Julien's own library: B12's broken statistic is a sampling-horizon error (Taleb), and the fix — a decade-local growth-exponent profile of the running max — is validated on frozen probe-1 data: it separates bounded (top-decade α=0.00) from walking-then-saturating (α-profile 0.99→0.51) where B12's current single-window slope reads +0.62 on a provably bounded case.

**Bottleneck.** Handoff "Risks to attack first" #3: B12 cannot tell bounded from compounding error on chaotic ships; the board (6 Oct): the recurrence ratio "does not separate a slow leak from a bounded error". Three builders (q-b12-design, b12-v2, wt/b12-v2) are rebuilding it now; this run hands them a tested statistic. Expected gain: an instrument that stops killing bounded laws (false positive measured) — no 10× speed gain claimed; this is an instrument fix, not an engine change.

## The five lessons (lens deliverable)

1. **Sample at the horizon you judge.** *"Over a short time increment, one observes the variability of the portfolio, not the returns."* — Taleb, Fooled by Randomness. Mechanism: any error statistic integrates oscillation and drift; they separate only by how amplitude scales with horizon. Change for B12: judge by the **α-profile** — running-max |error| local slope per decade of horizon — never one window-fitted slope. Cheapest test: **done below** (this run).
2. **Never average before taking an extreme.** *"By a law of probability called distribution of the maximum of random variables, the maximum of an average is necessarily less volatile than the average maximum."* — Taleb, Fooled by Randomness. Mechanism: subsampling/batching before an extremum understates tails. Change: B15 and the allocator's feedback read per-frame frame-times at the player's native frame quantum; smoothing only after the extremum. Cheapest test: p99 of a 60 s plane bench, raw vs 10-frame-averaged (predict ≥ 2× understatement; not run here — no plane on this host).
3. **Screen convexly: lose small often, never miss the rare.** *"These traders lose money frequently, but in small amounts, and make money rarely, but in large amounts. I call them crisis hunters."* — Taleb, Fooled by Randomness. Mechanism: a certificate tier has convex payoff iff worst-case miss is zero at a bounded frequent cost; average-work savings that can miss tails are concave and rejected by construction (the killed "Wide" tightening, which missed 23% at e 0.7–0.9, was this exact failure). Change: in-flight encounter builds (co-orbital certificate, slack skin) order their gates zero-misses-first, work-second. Cheapest test: add a negative control — a fleet at exact co-orbital resonance, partners within phase rank 4 (taleb-09b5's regime, sharpened to resonance).
4. **Question → delete → … → automate, in that order.** *"Always wait until the end of designing a process—after you have questioned all the requirements and deleted unnecessary parts—before you introduce automation."* — Isaacson, Elon Musk. Mechanism: automation multiplies whatever it is fed, waste included (Tesla production line, paid for in skin). Change: the 12-October review resolves the 7-Oct deletion candidates **before** merging the 14 builds that automate near them; each build states what it deletes. Fact-checked (this run, one command): `shipmem` and `encounters` have zero callers on main outside their own tests/examples — automation is about to be built around research code the engine does not reach.
5. **Small batches beat drained queues, even when draining looks efficient.** *"They will ask to go back to the old way of working, in which they had the opportunity to 'stay efficient' by working in larger batches."* — Ries, The Lean Startup. Mechanism: batch size is the root of variable flow delay (Toyota/lean, paid for on real lines); large batches lower average cost and create the tail. Change: per-frame event work is a fixed small batch with certificate deferral — never a drained queue; orbit recompiles amortize across frames (the plane recompiles on ~99% of kicks today). Cheapest test: plane bench p99 under drain vs fixed-budget at equal throughput.

## Evidence (all commands ≤ 60 s, run in `lab/results/20261008-2206-library-73ca/`)

- `python3 horizon_exponent.py` (18 s, < 50 MB): regenerates the frozen probe-1 energy series with the frozen code (`artifacts/evidence/gravity-v1-freeze-20260929/probe-scripts/`, untouched, verdicts on record = held out) and prints α-profiles; writes `exponents.json`.

| case (verdict on record) | α per decade [10→10² … 10³→10⁴] | reads |
|---|---|---|
| fixed-dt control (bounded, 1.8e−8) | +0.00, +0.01, +0.01 | bounded |
| variable-Δ rule (walks→saturates 8.25e−4) | +0.99, +0.92, +0.51 | leak, bending to saturation |
| fixed-dt, e=0.5 (held-out orbit) | +0.00, +0.00, +0.00 | bounded |
| variable-Δ, e=0.5 (held-out) | +0.97, +0.81, +0.32 | leak, bending |
| random walk (calibration) | +0.52, +0.46, +0.41 (settles after early decades ~0.8) | diffusive |
| bounded + transient (adversarial) | +1.02, +0.69, +0.16, +0.00 | bounded (transient decays) |

Calibration bands read off the data: **bounded** top-decade α < 0.1; **diffusive** settles 0.35–0.6; **systematic/chaotic** holds ≳ 0.8. The adversarial transient case is the one that matters: its single-window slope over [1,10³] (B12's style) is **+0.62** — a false KILL on a bounded law, the miscalibration the board already suspects.

**Predictions** (predictions.md, frozen before the run): P1 held (fixed < 0.10 every decade), P2 held (early ≥ 0.30, bends late), P4 held exactly (+0.62 vs 0.00), P5 held at the held-out eccentricity. **P3 partially failed, honestly:** a random walk's running max reads α≈0.75–0.89 at the first two decades (LIL transient), settling to ≈0.5 only from decade 2. Correction adopted: classify on the **settled top-decade α and the profile shape**, never on one early-decade number — which strengthens the case for reporting the whole profile instead of one slope.

## What would make it wrong

The α-profile is calibrated on one Hamiltonian probe's energy error plus synthetics; chaotic-light-cone scenarios, multi-body dolls, or integer laws with error feedback may not sit in these bands. The bands are also sample-count dependent (fewer than ~4 decades cannot separate drift from diffusion — itself a gate-design constraint: B12 needs runs long enough to buy the decades). Adoption cost: small — a function over an existing series; the rebuilds are in flight. Fit with PRINCIPLES: *"Errors never compound… types of errors and not just errors"* (13, OC#42) and *"error type over error size"* (2) — the α-profile is error *type* made measurable. Lesson 3 quotes *"we don't want errors that can compound"* (CL 09-25 14:28).

**The lens's blind spot.** A Taleb-shaped lens reads everything as tails and horizons; lessons 2 and 5 are stated from analogy (not run here — no plane on this host) and the integrator should demand their bench numbers before acting. Lesson 4 is process, not physics — it changes a review order, nothing more.

**Grade sought:** silver-to-gold for lesson 1 (reproduced, held-out held, one experiment: the chaotic-doll case on the rebuilt B12 candidates); the rest are decisions, not results.
