# Dossier — 20261006-1029-dynamics-6875 (lens: dynamics and attractors)

**Claim.** The encounter design's steady state does not exist under endogenous kicks: at
belt-realistic stirring, certificate work per orbit is ×87 and work per real encounter
×109 versus the frozen-element belt, grows ∝ t^{~1/4} without bound (self-stirring widens
the overlap set; real-encounter yield stays flat), and each conjunction re-pays ~60 pair
certificates — while the event process itself stays Poisson (Fano 0.9–1.3) and a single
player relocation leaves a bounded, slow wake (+1.5–3% for >200 orbits), not a cascade.

**Bottleneck.** Board item "finding encounters without work per orbit or per element
change" / the top scaling risk. r8 v2's premise ("cost follows the candidate set") is
confirmed, but its next step — "judge steady-state work per orbit (→ 0), with each pair
paid once per element change" — assumes element changes decay. They don't: they are the
belt's own dynamics. Expected gain of the fix (per-quantum re-pay + birth-side tail
control): removes the ×10² and the unbounded growth; deletes nothing today (the tier
itself is untouched).

## Evidence (all commands ≤ 60 s except the sweeps, ~60–90 s each, N=200)

- Simulator: `belt_sim.py` — discrete events, no ticks; first order in e; GM=1; belt =
  repo's r8 convention (a ∈ [1, 1.5] uniform, Rayleigh σ_e = 1e-2, ρ = 1e-3); impulse =
  rotation of v_rel (pair momentum and |v_rel| exact); elements via first-order Gauss.
  Certificate = radial-overlap pairs, updated incrementally on kicks; **resched = pair
  rebuilds = the certificate cost the engine would pay.**
- Sweep: `python3 belt_sim.py --gm {0,5e-8,1.5e-7} --orbits {2000,2000,800} --n 200 --seed {0,1,2} --out data/…`
  (gm=0 seeds at 2000 orbits; hot tier at 800 orbits for the time budget), then
  `python3 analyze.py`. Numbers (3 seeds each):

| tier | σ_e slope (log-log) | overlap (t0→t1) | conj slope | enc slope | Fano | drift Σ1/a |
|---|---|---|---|---|---|---|
| gm=0 (control) | 0.000 | 2199→2199 (flat) | 0.001 | ~0 | 0.89–1.02 | 0 exactly |
| gm=5e-8 | 0.119–0.130 | 2202→3060 (+39%) | 0.17–0.18 | ~0 | 0.99–1.08 | 4e-3–1e-2 |
| gm=1.5e-7 | 0.183–0.205 | 2195→3676 (+67%) | 0.32–0.38 | ~0 | 1.02–1.31 | 2.2–2.6e-2 |

- Certificate amplification: resched/conj = 44–59 early → 65–78 late (grows with
  heating). resched per orbit: control 54; gm=5e-8 4234→5660 (+34% between orbit windows
  800 and 1600); hot ≈ 6500–7300. Work per real encounter (b<ρ): control ≈ 2.2×10³;
  gm=5e-8 ≈ 2.3–3.6×10⁵ (**×10²**), and rising with the budget.
- Avalanche pair (same seed 7, deterministic; injection = tangential δv 4.5e-3 ≈ 5×
  typical v_rel at orbit 200): `--inject-orbit 200 --inject-dvt 4.5e-3`. Excess over
  control, orbits 200–399: resched +22 783, conj +191, encounters +2. Immediate burst ≈
  O(degree) as predicted; the sustained wake is ≈ 5× the victim's own future budget
  (≈4.4k), mean +1.5–3% of belt work, no runaway, per-orbit swings ≈ Poisson
  decorrelation noise (two independent processes after divergence).
- Conservation (P6): drift of Σ1/a exactly 0 in the control; 2×10⁻⁵–1.6×10⁻⁴ relative
  in kicked runs (second-order Gauss error, disclosed).

**Predictions** (`predictions.md`, written before the sweeps; one amendment after a
20-orbit debug pilot, disclosed inside): P1' σ_e ∝ t^{1/4} predicted; measured slopes
0.12–0.21 over the accessible window — right family (sub-diffusive, not ½, not flat;
control pins 0.000), below the asymptote because the transient (colder ⇒ stronger
focusing) dominates a run where σ_e only grows 1.4–1.7×. P2 (budget ∝ σ_e) held:
slope ratio 0.68–1.03. P3' held: encounters flat, work/encounter grows. P4 held: Fano ≈ 1.
**P5 failed as written**: no supercritical cascade (the worry), but the wake does not
decay "within a few orbits"; it is a slow viscous excess. P6 held within the stated error.

**What would make it wrong.** The toy is first order in e (emax ≤ 0.052, safe) and
idealizes the certificate as the radial-overlap set with whole-neighbourhood re-pay —
if the real tier re-pays only rank-k phase neighbours (the 6 Oct gold), the ×60
amplification shrinks toward ×2k and the growth law, though not the growth itself, may
drop out of budget. The stir rate is a free parameter (α_typ = 0.05–0.15 disclosed); at
game masses it could sit far lower, and then the ×10² arrives over proportionally longer
game time — the growth law (t^{1/4}, from focusing, robust) sets the shape, gm sets only
the clock. Strong-scattering tail capped at α = 0.5 (under-kicks). Drift is nonzero in
kicked runs (above).

**Cost of adoption.** None as code; two design inputs: (1) re-pay pairs per certificate
**quantum**, not per element change (sub-quantum drift accumulates toward the next re-pay
— principle 6), or per epoch amortization; (2) the belt program's births must re-absorb
the heated tail, else the "→ 0" steady state never arrives (B18b's tails exist already).
A gate candidate: certificate-work per real encounter must not grow across epochs at
fixed birth parameters.

**Fit with PRINCIPLES.** "Compute only surprises" (3): the surprise rate here is flat,
so the ×10² in certificates is pure representation debt, not physics. "Aggregates:
influences below one quantum accumulate" (6) is the exact fix for the re-pay rule.
"A failed experiment kills that configuration, never the method" (9): the killed
configuration is pay-per-element-change under feedback. "The simulation decides" (22):
the belt's own stirring decides the budget, so measure it, don't assume steady state.

**The lens.** Dynamics looked for the attractor and found a direction, not a fixed
point (t^{1/4} climb toward the κ→1 cliff the co-orbital gold found statically). What
the lens may have missed: spatial structure (clumps, resonances at specific commensurabilities
— `keys` belts) where Fano could exceed 2 and the wake could localize; and the player's
own cadence of relocations, which sets the wake叠加 rate. Both are one cheap follow-up
each on this harness.

**Grading note for the checker:** reproduction is `python3 belt_sim.py …` + `python3
analyze.py` in this folder (data/ holds the raw rows). Everything regenerates from the
shipped scripts; no post-run edits to data.
