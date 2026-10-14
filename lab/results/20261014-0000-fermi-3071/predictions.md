# Predictions — 20261014-0000-fermi-3071 (written before the held-out runs)

Model to falsify (built ONLY on the two prior runs' saved data, no engine run yet):
ea91's per-body surprise distribution is **manufactured** — (i) natives = compiled
period ladder (rates 0.0484 … 3e-5 /s, a 1600:1 spread by construction; same-rate
bodies identical), (ii) members = birth-burst then quiescence/death, (iii) head = the
player (driver). No intrinsic per-body surprise tail. Fitted quantities: NONE
(alpha = items/kicks = 2.04–2.07 is reported, not fitted; Gini is scale-invariant).

Held-out cases (neither author ran these with the census probe):

**A — seed 11, m120, rtf 100, 55 s** (ea91's checker seed, unused by the author):
1. G_all(items) ∈ [0.64, 0.78]; G(nat items) ∈ [0.70, 0.78].
2. Native per-body counts within ±10% of ho1/ho2's (seed-invariance: the ladder is
   compiled, seed moves members only); Orbiters 1–2 exactly equal; Orbiters 3–5 exactly equal.
3. spearman(nat items, roster-rate × T) ≥ 0.93; the Player is the top native.
4. Dead-member fraction ∈ [0.45, 0.70]; alive-member second-half median ≤ 5 items.

**B — seed 3, m400, rtf 100, 110 s** (ho1's exact scene, window doubled):
5. Native counts ≈ 2× ho1's (±10%) while G(nat items) = 0.736 ± 0.02 **exactly
   T-invariant** — the discriminator: an intrinsic heavy tail has no law forcing its
   Gini to hold while every count doubles; a compiled rate ladder does (Gini of
   {r_i·T} is T-invariant).
6. G_all < 0.737 (member burst amortizes; direction predicted, not size).
7. Zipf slope (all) stays in [−2.3, −1.5].

Kill criterion for the model: any of 1–5 failing its band. Then rule 2's measured-rank
reading revives and this dossier reports it. If all hold: ea91's numbers stand as a
correct description of a manufactured distribution; rule 2 dies as a ladder rule
(7497's verdict), and ea91's death/avalanche findings stand untouched.
