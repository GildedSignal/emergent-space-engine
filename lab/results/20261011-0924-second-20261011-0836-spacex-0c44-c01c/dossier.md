# Dossier — 20261011-0924-second-20261011-0836-spacex-0c44-c01c (second author on 20261011-0836-spacex-0c44)

## Claim

The silver's named experiment is done and the original claim stands, sharpened by one
correction: **no fixed kick cadence passes the plane's frozen gates** — B13 fails at every
N=1..9 (twice reproduced; the tail is `NoBoundOrbit` kick refusals on heliocentrically bound,
nearly radial states, multiplying with cadence and felling a 39 R_p *far* flyby, not the deepest
ones), and B14 fails on behaviour at every N=1..7 (classification 187–244 of 255, capped by
9–13 moons the plane loses; apsides 0→52 of 53, one short of the bar even at the 128-kicks/orbit
default) while its 60 s phase budget is **law**-dominated (oracle 12.9 s; law 26.4→1292.4 s,
doubling per step), so only N=1 (and N=2 on a quiet machine) can even complete. B17, now
measured at every cadence, passes only at N=4–6 — where B13 sits at 3–41/64. The correction:
the author's "oracle-dominated, wall ~flat ≈ 60 s" reading of B14 is wrong, which turns the
budget verdict from a 0.25 s load coin flip into a machine-independent order of magnitude.

## Bottleneck

Board focus #1 (kicks dominate the engine's cost; the lever is cadence) and `q-cadence`'s brief.
This run closes the silver's two gaps so the re-aiming can be adopted: (a) B14's cost split and
behaviour verdicts on the record at every cadence (was: one unlogged 59.75 s run), (b) the B13
tail's mechanism on the record (was: a wrong "deepest flybys" sentence). What it deletes: the
search for a passing fixed cadence (there is none, on behaviour or on budget), and any framing
of B14's timeout as a judge-cost problem (the law's own kicks eat the budget: ≈52.8 µs/kick
measured in B14 scenes, the bench's 43 µs anatomy confirmed in situ).

## Evidence

All from the repo root; release binary `cargo build --offline --release -p xtask` (38 s), test
binary `cargo test --offline --release -p xtask --no-run` (59 s). Cloud Linux/x86, 8 vCPU
shared: walls are order-of-magnitude only; every count, error magnitude and verdict below is
exact and machine-independent. Logs in `work/`: `b14-cli.log` (shipped CLI), `b14-split.log` +
`b14-split.trace` (the harness this run adds; its diff is saved with the run), `b13-bydraw-{7,8,
9}.log`, `b13-refusals-{40-8,5-9}.log`, `b17-sweep.log`, `b12-default.log`.

```sh
# B14 from the shipped CLI, the cadences a 60 s phase can hold (quiet machine)
xtask behave --law plane --gates B14 --plane-step 1   # FAIL 36.1 s
xtask behave --law plane --gates B14 --plane-step 2   # FAIL 59.2 s (load-marginal)
# the cost split + behaviour at every cadence, no 60 s wrapper (this run's harness;
# each step regenerates its row independently — B14_STEPS=2 costs ≈62 s, the point of the record)
B14_STEPS=1,2,3,4,5,6,7 PLANE_TRACE=1 \
  cargo test --release -p xtask b14_cost_split -- --ignored --nocapture
# the B13 tail, per draw (shipped probes)
B13_STEP=7 cargo test --release -p xtask b13_by_draw  -- --ignored --nocapture  # and 8, 9
B13_DRAW=40 B13_STEP=8 cargo test --release -p xtask b13_refusals -- --ignored --nocapture
# B17 at every cadence (shipped CLI)
for n in 1 2 3 4 5 6 7; do xtask behave --law plane --gates B17 --plane-step $n; done
```

**B14's cost split (the harness; oracle = `hill::moons`, 768 law-independent reference runs):**
oracle **12.9 s** once per process; the law's own share, exact counts:

| N (kicks/orbit) | law s | phase ≈ oracle+law | classification | apsides ≤10% | verdict |
|---|---|---|---|---|---|
| 1 (2) | 26.4 | 39.4 (CLI 36.1) | 187/255 (73%) | 0/53 | FAIL behaviour |
| 2 (4) | 48.8 | 61.7 (CLI 59.2) | 243/255 (95.3%) | 0/53 | FAIL behaviour |
| 3 (8) | 86.9 | 99.8 | 243/255 | 2/53 | FAIL both |
| 4 (16) | 167.0 | 179.9 | 242/255 | 11/53 | FAIL both |
| 5 (32) | 330.0 | 342.9 | 244/255 | 22/53 | FAIL both |
| 6 (64) | 644.7 | 657.6 | 242/255 | 51/53 | FAIL both |
| 7 (128, default) | 1292.4 | 1305.3 | 242/255 | 52/53 | FAIL both |

255 of 256 moons judged, 53 with a stable apsidal rate (law-independent, matches the author's
denominators; the bars are 253/255 and 53/53). The two halves of the gate fail differently, and
the decomposition is on the trace:

- **Classification is capped by moons the plane loses, not by wrong classes.** Flat at
  242–244/255 (94.9–95.7%) across N=2..7. The trace's `lost` lines count 49, 9, 11, 13, 11, 12,
  13 for N=1..7: at N=4, 242 agree with 13 lost, i.e. **every moon the plane keeps classifies
  correctly**; at N=7, 13 lost + 0 flips. The lost moons carry no refused kicks (one refusal
  event in the whole B14 sweep), and two of the thirteen are lost within 0.4 planet periods of
  birth — a drop path ("a surface, the system's edge, a state no tube can hold", plane.rs)
  distinct from B13's refused kicks, and cadence-stable, so no refinement can lift
  classification to 99%.
- **Apsides converge only toward the finest cadence** (0, 0, 2, 11, 22, 51, 52 of 53 — the
  tide's phase is h² in the cadence), and even the default's 52/53 = 98.1% misses the 99% bar;
  at the budget-admissible cadences (N≤2) it is 0/53. The closest B14 ever comes to passing is
  at a cadence whose law alone costs 21.5 min against the 60 s gate.

The CLI at N=2 regenerates the author's unlogged numbers exactly (243/255, apsides 0/53, 102 of
155 without a stable rate); it completed at 59.2 s here and timed out at 60.0/60.1 s in the
checker's runs — a load coin flip, which the harness removes by having no timeout at all.

**The correction (cost attribution):** the author read the B14 wall as "~flat ≈ 60 s,
oracle-dominated". Measured: the law dominates at every N≥2 (79% of the phase at N=2, 93% at
N=4, 98% at N=6, 99% at N=7); law(N) doubles per step (26.4→48.8→86.9→167.0→330.0→644.7→1292.4,
ratios 1.85–2.005), so phase(3) ≈ 100 s and phase(7) ≈ 22 min — the N≥3 timeouts are the law's
own work, not the judge's, and no machine class where N=2 fits 60 s can admit N=3. Cross-check
from the trace: kicks/moon 1300→3014→5952→11906 (exact ×2 per step, cadence-linear by
construction), giving ≈52.8 µs/kick in B14 scenes after ~10 s of fixed scene builds (256 moons)
— the kick bench's 43–44 µs anatomy (one rebind per distinct kick, twice reproduced bit-for-bit
by author and checker) holds in situ: B14's phase is kick-cost-bound.

**The B13 tail's mechanism (shipped probes, now on the record):**

- N=7 (60/64): failures #18, #27, #50, #57, all marginal (1.34–2.12e-2 against the 1e-2 bar),
  **zero refused kicks**, fault None.
- N=8 (62/64): failures #40 (q 39.1 R_p, dE 1.26e-1/dL 4.39e-1, 48 refused) and #68 (5.5 R_p,
  6.9e-2/6.3e-2, 51 refused), both `Some((Kick(0), Space(NoBoundOrbit)))`. Draw #40's closest
  approach is 42.3 R_p — a **far** flyby, second-worst ΔE: the author's "deepest flybys"
  sentence is wrong, exactly as the checker suspected.
- N=9 (58/64): failures #5, #14, #27, #40, #57, #68 — every one alive, fault
  `Space(NoBoundOrbit)`, 10–330 refused kicks. The failing set is cadence-dependent (#18, #50
  leave; #5, #14 enter), and refusals multiply with cadence even on passing draws (#0: 2→5→19;
  #21: 0→5→23; #68: 0→51→330).
- The refused state (`b13_refusals`, draw #40 at N=8): heliocentrically **bound** (E = −1.45e-9),
  nearly radial (vr 3.0e-5, vt −1.5e-7), r ≈ 5.264e8 root units with the planet at 5.275e8
  (~21 R_p away), and all refusals land on the **same tick** (one kick re-refused). The raise is
  in `crates/space/src/events/kicks.rs:157–176`: the kick applies the tide's (ΔE, ΔL) and then
  requires the **post-kick** state to be a real bound orbit through the current position
  (`den > 0`, `e² > 0`, `radial² ≥ 0`); during a flyby no bound tube through the state exists,
  so the kick refuses — the doll's bound-only tube store meeting a flyby, the shipped probe's
  own words: "a heliocentric state with no tube".

So the tail is a representation gap (no tube for flyby states), not depth and not a cadence
error: refining the cadence multiplies the refusals (more kicks inside the flyby window) and
moves the failing set around, while the coarse direction degrades as h² — no 2^N passes, for
two different reasons at the two ends.

**B17 (shipped CLI, every cadence, `work/b17-sweep.log`):** FAIL at N=1–3 (N=1: pump
[0.65, 18.9], amplitude 0.001, regime 5/12), **PASS at N=4–6** (pump [0.990, 1.003] and
amplitude 0.981–0.998 at N=4; walls 15.1/24.9/44.2 s), FAIL timeout at N=7 (60.0 s) — law.md's
citation, now measured. The pass band N=4–6 is exactly where B13 sits at 3–41/64 and B14 at
11–51/53: no single fixed cadence passes the set. **B12 (one record run, N=7, 37.6 s):** FAIL,
median growth exponent inf — consistent with H0214/H0215's "statistic miscalibrated, being
rebuilt" (`q-b12-design`); recorded as evidence only, as the original dossier framed it, and
only at the default cadence.

## Predictions

`predictions.md` was written before the decisive runs. **Held:** the judged population (255/53,
exact); the negative control (N=1 fails decisively, 187/255 and B17's pump [0.65, 18.9]); the
author's N=2 numbers regenerate from the shipped CLI (243/255, 0/53); the B13 refusal mechanism
reproduces exactly (the checker's draw sets, magnitudes and refusal counts, now in this run's
logs); and no N in 1..7 passes B14 — held on both bars (classification 187–244 vs 253; apsides
0–52 vs 53, closest at the default). **Missed (and reported as held-out misses):** I predicted
the oracle at 40–60 s dominating the phase — it is 12.9 s; and the law at N=2 at 2–10 s — it is
48.8 s. Both misses point the same way: the phase budget is spent on the law's kicks, not the
judge — the opposite of the author's attribution and of my prior. Not predicted: the apsidal
half's near-convergence at fine cadence (51/53 at N=6, 52/53 at N=7) — the classes, not the
apsides, are what cadence cannot fix.

## What would make it wrong

- If a cadence outside 1..9 (finer than 512 kicks/period) passed B13: the refusals grow with
  cadence (330 at N=9 on draw #68), so this is not a convergence-in-progress; a finer cadence
  makes it worse, not better.
- If B14's apsides reached 53/53 at some N>7 while classification reached 253/255: measured to
  N=7, classification is capped by 9–13 cadence-stable lost moons (every kept moon classifies
  correctly at N≥4), so lifting it needs the loss path fixed, not the cadence.
- If the 12.9 s oracle were machine-class-dependent enough to matter: it is 21–33% of the phase
  only at N=1–2 and shrinks from there; the law's doubling dominates any plausible oracle
  variation.
- The mechanism sentence rests on the shipped probes' own reading of the refused state; if the
  kick's post-state check fails for a different reason than "no bound tube through the state"
  (e.g. a units bug in the probe's energy print), the refusal evidence stands (fault, counts,
  cadence dependence) but the wording would need the universe crate's own audit.

## Cost of adoption, and fit

Adoption is a re-aiming with one correction to carry: (1) `q-cadence`'s brief should say that no
fixed 2^N passes the plane's frozen set on v2 — B13 at every N=1..9 and B14 at every N=1..7 are
now on regenerable records, and B17's only pass band (N=4–6, now measured) is buried under
B13's 3–41/64 there; that the deep-flyby tail is a tube-representation gap (kick refusals,
multiplying with cadence) while B14's classes are a second gap (moons the plane drops, both
early and late, cadence-stable); and that B14's timeout is the law's own kick cost (≈53 µs/kick
in situ), not the judge's; (2) the jet (law.md, one compile per kick) stays the cost lever —
this run measures it in B14 scenes too. PRINCIPLES: "A failed expectation is not automatically
a failed method: diagnose which one broke" (#9 — the broken premise is the fixed cadence, and
this run names the mechanisms); "Compute only surprises" (#3 — a kick that rebinds a cycle it
cannot distinguish from the last one, 100% of distinct kicks, is compute done for no reason);
"a test that cannot fail is a control" (the N=1 negative controls failed as required, on both
B14 and B17).

## The lens

The second-author lens optimizes for closing the checker's named gap with the run's own scripts,
and it nearly missed three things: the chance to *correct* the record rather than only complete
it (the oracle/law attribution inverted under measurement — a completion-only lens would have
logged the numbers without flagging that the author's flat-wall story was wrong); the B12 run
(the checker's "missed" list named it; one run costs 38 s); and B17's sweep (cited from law.md
in the original, measured here at every cadence for 3 minutes' cost). What it may still have
missed: the loss reason for B14's 13 dropped moons (the trace names the sample, not the fault —
a body-record probe would say which of "a surface, the system's edge, a state no tube can hold"
it is), and the identity of the one apsidal moon that still misses at the default (52/53: which
moon, and by how much, is one probe away). Both are follow-ups for the encounter-representation
work this record points at, not for the cadence question.
