# Predictions — second-author run 20261009-2043 (written before the decisive run)

Tuned on: the dev smoke scene only (`mk_constp(200, (0.02,0.2,0.45), H=12, seed=99)`).
Everything below is held out: fresh seeds (≥100), the checker's adversarial class at
fresh seeds, and fresh variants of the original scenes. The rule's 5(e_i+e_j) constant
is untouched from the original run — fixed a priori this time, as the checker demanded.

## P1 — index = rule (the repair; control that must pass, by construction)

On every registered scene (equiv, equiv3, scale2): the repaired index emits exactly
the naive per-pair rule set — `new_drops = 0, new_adds = 0` — including the const-p
adversarial class, the beyond-domain scenes, and N=2048 fleets. Grounds: the per-bin
window uses the exact sup of |Δn| over the bin's occupants (their own n = a^-1.5
extremes) and eb = max(e_i, e_max_bin) ≥ ebar; every factor dominates the rule's, so
the bisect window never excludes a rule-passing pair and emission applies the full
rule. If any drop/add appears, my domination argument is wrong somewhere (e.g. a
float-boundary effect in the bisect) — that would refute this run's claim.

## P2 — the old index's defect reproduces (control on the failing side)

`equiv` on the original scenes (belt seed 1, mixed seed 3): old drops ~9 and ~11
rule-passing pairs respectively (the checker's numbers); on fresh const-p bimodal-e
H=16 (seed 311): old drops ≥ 100 pairs and its recall vs truth is < 0.95 (checker
measured 0.867 at his seed). On the belt e∈[0.4,0.55] scene old may drop 0 (the
defect needs e-spread at near-constant U to bite).

## P3 — recall on fresh seeds (held out)

truth3: repaired index recall = 1.0 on F1–F4, B1, B2, M1, A1, A2 (all within the
claimed e ≤ 0.4 domain). Controls: cone-only also 1.0 everywhere; ideal-trigger < 1
on the fleets and the mixed scene (the rank-4 design stays falsified), = 1.0 on
belts. This is the genuine held-out test of the 5(e_i+e_j) constant on scenes never
tuned on. A miss would be a formula failure (window too tight), not an index failure
— P1 separates the two.

## P4 — beyond the e-domain (held out, expected to expose the boundary)

A3 (e up to 0.55, H=24) and A4 (belt e∈[0.4,0.55]): set equality still holds (P1 is
e-independent), but recall may be < 1.0 there: the chart bound 4e+2.5e² ≤ 5e fails
for e ≳ 0.42, so the rule itself is out of its claimed domain. I predict equality
holds, recall ∈ [0.9, 1.0], and any miss has e ≥ 0.4. Reported as the domain edge,
not as an index defect.

## P5 — the scale record (regeneration, and an honest re-report)

scale2 (fleets, arc 0.5, e0 ∈ {0.02, 0.002}): unified candidates ≈ 0.7 and ≈ 0.22 of
C(N,2) respectively, roughly constant in N (window/arc fixes the fraction); per-body
candidates grow LINEARLY with N at fixed arc — the original run's prediction 5
("≤ ~√N·log") was falsified by its own data and stays falsified; I re-report it as
such rather than reframing. evals ≤ candidates × small factor for the index; cone
evals = C(N,2) exactly.

## P6 — truth resolution (control)

truthres: at T=4096 vs T=1024 on a fresh belt N=256, zero or near-zero new true
pairs; recall vs the T=4096 truth stays 1.0.
