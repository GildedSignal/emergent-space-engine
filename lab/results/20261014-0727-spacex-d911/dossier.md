# Dossier — 20261014-0727-spacex-d911

## Claim

One kick re-rolls the encounter tier's armed set — 79% of armed pairs flip out at Δa/a = 1e-7 and
93% at 1e-5, against 95.5% for a full re-roll — so the kick→certificate cascade (812.8 full window
re-derivations, 17k evals per kick) is paying to recompute a per-pair verdict the kick itself
destroys: per-pair horizon arming cannot be maintained incrementally at real kick sizes, and the
~10³ cut at 10⁹ must **delete** the per-pair arming pass (lazy per-passage arming at the doll door,
or group envelopes), not cheapen it (the skin's 12.6× is the ceiling of the cheapening path).

## Bottleneck

Board #2: encounter work at 10⁹ (~7.7×10³ cores skin-on, 1,925× over), "what cuts it by 10³ … what
never needs a pair test at all". The cascade term is the only term near a core at 10⁶ (wiki
`encounters`, 90fb). This run measures what that term actually buys per kick.

## Evidence

All numbers from shipped code (`crates/encounters` @ 7ce71fa8) plus `work/patch.diff` (adds the
`kick2` experiment: armed-set churn, horizon knife edge, hit-time transform, cost anatomy).
Regenerate: `sh lab/results/20261014-0727-spacex-d911/regen.sh` (~14 s: build 7 s, `kick` 5 s,
`kick2` 3 s; ≤ 10 MB RSS). Scene: shipped belt n = 10⁴, ρ = 1e-4, σ_e = 1e-2, seed 20261050,
horizon 1000 orbits, 100 kicks, Linux/x86 shared cloud (orders of magnitude only).

Baseline (`kick`, shipped): pairs/kick **812.8** (the published 90fb anchor, reproduced exactly),
scanned/kick 3,122.6, **7.16–7.3 ms/kick**, 8.8–9.0 µs/pair; changed_fraction 0.24% / 7.8% / 8.6%
at eps 1e-9 / 1e-7 / 1e-3.

Decisive (`kick2`):

| eps (Δa/a) | armed/kick | **armed_stay_frac** | flip_in / flip_out per kick | full re-roll would stay |
|---|---|---|---|---|
| 1e-7 | 36.4 (4.5%) | **0.214** | 28.7 / 28.6 | 0.045 |
| 1e-5 | 36.4 | **0.067** | 35.4 / 33.9 | 0.045 |

- **The churn is kick-size-insensitive**: flips rise 1.2× for a 100× larger kick (57→69 pairs
  1e-7→1e-5); with the shipped 1e-9 point (~2 pairs) the curve saturates at the re-roll value
  2·p·(1−p)·812.8 ≈ 70. There is no drift-proportional regime in between.
- **Horizon knife edge refuted** (my prediction 1): knife_share = 0.0000 at both eps; no silent
  pair has a first hit within 4·rel_dt·horizon beyond the edge (at_risk 0.0000). The flips are not
  passages drifting across the horizon edge; the hitting pattern itself re-rolls (Diophantine
  rotation-hitting, consistent with `9834`/`5c16`'s rotation identity).
- **Survivors transform smoothly**: matched hits move as t_new ≈ tk + (t_old−tk)(1+c·rel_dt) with
  median residual 1.0e-5 (eps 1e-7) / 1.7e-3 (eps 1e-5) of the synodic period (p99 1.3e-2 / 2.5e-2);
  the c tails (p10 −111, p90 +104 at 1e-7) are passage swaps, not drift.
- **Candidate set frozen**: cone edge churn ≤ 0.56 pairs/kick (prediction 4 held). The news is in
  time, not geometry.
- **Cost anatomy** (prediction 5 held): 1,612 sections/kick, 1,654 Diophantine queries, 10.4k
  qsteps, **16.9–17.3k window evals** per kick against **41.5–42.7 exact checks** and 37–39 hits.
  The exact tier already runs at the news scale (~70 flips + ~37 hits); ≥ 98% of the 7.3 ms is
  window/first-hit machinery re-deciding arming; the U-scan + cone test is 107–156 µs (1.5–2%).

Composition (orders of magnitude): per kick, news ≈ 70 flips + 37 hits; the shipped path pays
~250 evals per flip. Deleting the arming pass (lazy per-passage detection at the doll door — the
wired 4ea2 gold — or tier.rs's O(log N) envelope tree) leaves scan ~0.11 ms + ~813 O(1) margin
updates + ~70 exact re-derivations ≈ **0.76 ms/kick ≈ 10× on the shipped cascade**, and removes the
term the skin cannot amortize. The remaining 10² to the few-cores target then lives in the scan and
the per-body aggregate, exactly where the board pointed ("cells, setup, what never needs a pair
test").

## Predictions

`predictions.md`, written before `kick2`. Held: 4 (edge churn < 5/kick), 5 (setup ≥ 80% of cost;
measured ≥ 98%). Refuted: 1 and 2 (horizon knife edge: knife_share 0.0000 — the flip mechanism is a
re-roll, not edge drift), 3 partially (the transform holds only for surviving hits, median
1.7e-3 of synodic; membership itself does not transform — c tails ±100). Reported as held/refuted
above.

## What would make it wrong

- Single scene: one belt (n = 10⁴, ρ = 1e-4, σ_e = 1e-2), planar Kepler, horizon 1000 orbits, 100
  kicks. The re-roll statistic should be re-measured at the wired horizon (a shorter horizon holds
  fewer passages and less re-roll mass) and at other ρ.
- The dichotomy protects the conclusion: below eps ~1e-9 arming is static (0.24% churn — the
  certificate is simply cheap), above ~1e-7 it is a re-roll; no middle regime where incremental
  per-pair maintenance pays is visible between the measured points. If the wired belt's true kick
  stream sits far below 1e-9, the cascade never engages (but then the tier is already cheap, per
  `c7eb`: sub-critical rocks never cross a period tick).
- 3-D inclination, kick-perturbed λ(t), the GR doll: untested here (the page's standing domain
  caveat, `4e7c`).

## Cost of adopting, fit with PRINCIPLES

Adoption cost: zero for the negative — it forbids spend (per-pair arming maintenance, and any
slack/skin successor that still re-derives windows per kick); the positive arm (per-passage lazy
arming at the doll door) is a wiring decision for H0216, not new code in the crate. Fit: #19 "if
you find yourself fixing things that's oftentimes a signal that it is the wrong representation" —
the horizon-arming verdict is the wrong unit, the kick destroys it; #3 compute only surprises —
17k evals to deliver 70 bits of news is the surprise-free term; #1/#26 — delete before cheapen:
the skin cheapened (12.6×) what this measurement says to delete.

## The lens (SpaceX)

Idiot index: 250 evals per delivered flip (17.3k / 69). The lens's "question the requirement"
found the requirement wrong: the cascade maintains a certificate whose content the input
invalidates. Blind spot: delete-and-rebuild bias — the skin's measured 3–3.7× wall cut is real and
survives this result (it amortizes window *geometry*, which the kick does move); this run only
caps the path, it does not retract the skin. And one scene, one machine, orders of magnitude.
