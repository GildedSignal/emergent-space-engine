Grade: silver

**Abstract.** Claim: the doll-boundary chatter is Zeno, cured by the decision variable (decide once per apsis on r_apo vs f(Λ)·R_H±m), not by the band. Reproduced bit-identically (regen.sh 49 s): R0 chatters 180–201/20P, 942/100P, μ-invariant 179–187; R3 = 0 on all chatter cases, 1 per actual transition, 1 after a 3% kick vs hysteresis's 76; dwell pays 20/97. My arms beyond the author's domain — 200P (R0 1871, R3 0), eccentric births, the never-exercised capture arm, prograde 0.55/0.6 — all hold; one hit: (0.62,ret) wanders apoapsis 0.62–0.87 R_H through the f±m band, 89 handoffs/40P (0.32/orbit; R0 = 1 there). Gain: the boundary's per-body event bill ~9.4/planet-orbit → 0, per-tick check deleted. Cost to adopt: the engine arm on 18d2's build plus one f/m freeze. Not engine-measured: replica only.

## Reasons

**Reproduction.** `regen.sh` in a clean run of the committed tree: exit 0, 49 s, and every committed artifact regenerated **bit-identically** (results.json, both held-out μ logs, longwindow-kick.txt, main table). No repo-tree patch (work/patch.diff empty) — the run's only instrument is `handoff_rule.py`, self-contained. All dossier numbers trace to regenerable output: 180/201/942, 20/97 (R2), 76 (R1 kicked), 179–187 (μ-invariance), 1-per-transition on every ejection, the (0.7,ret) edge dial (1, max 1.06 R_H at 100P — the dossier's "1.07" is a fair bound of 1.06). |ΔC_J| ≤ 8.4e-10 everywhere (K5 pass).

**Predictions.** `predictions.md` mtime 12:47:21; first execution (pycache) 12:48:40 — pre-registered before the decisive run. The author reports its failures honestly: P1 half-failed (the 0.9-class does not chatter in this replica — the probe's 21,403/4,455 magnitudes are a relativistic-window phenomenon, disclosed as not reproduced), P2 failed (R0f is sampling-invariant, not 2×: the flips are dynamical, ~20 samples apart — arguably the stronger result), P4 half-failed (hysteresis cures quiet chatter; fails under kicks, 76 vs 1). Held-out axes (μ ∈ {1e-4, 1e-2}, kicks, 100P windows) all held.

**Adversarial cases (mine, 12 arms, script reusing the author's module; all |ΔC_J| ≤ 9.4e-10).**
1. *200P on (0.5,ret)* — one decade past the author's longest window: R0 = 1871 (linear, 9.35/planet-orbit), R3 = 0. The unbounded-chatter premise and the cure both extrapolate.
2. *Eccentric births* (vfac 0.6–1.2, all births in the run were circular): classification = truth on all four; R3 = 1 on both ejections, 0 on both retentions.
3. *The f±m band* — the one real hit. A plain **circular** (0.62,ret) birth wanders apoapsis 0.619–0.866 R_H across both thresholds: **R3 = 89 handoffs/40P (0.32/moon-orbit)**. K3 survives (bounded ≤ 1/orbit — the Zeno-free claim is intact), but "0 handoffs on stable bodies" is band-dependent, and on this body R3 (89) is worse than R0 (1). The dossier disclosed this mode as unmeasured ("none measured here"); it is reachable without chaos or kicks. Neighbouring births (0.66/0.68/0.72,ret) give R3 = 1. I folded this into the page as a third dial class.
4. *Capture arm* — never exercised by the author (every replay starts planet-owned): with owner0 = star, R3 captures deep cases in exactly 1 (0.3-ret, 0.5-ret) and never captures the 0.7-ret edge body (the mirror of the disclosed edge dial).
5. *Prograde 0.55/0.6 R_H* (between f_pro and the shipped radius): truth ejects both; R3 = 1 each; also beats R0 (5/7).

**Novelty.** `lab/wiki/handoff.md` open direction 2 framed the rebuild as "a chatter-free condition (hysteresis or rate-based) at r_c"; this run *measures both field-standard cures insufficient* (R1: 3–9 slow-escape churn, 76 kicked; R2: 20/97 forever) and demonstrates a third rule class (per-apse, on the cycle's radial extent, Λ-continuous). No HISTORY entry or wiki page has an apsis-decided ownership rule; the closest prior art on the page is 18d2's refutation of the shipped predicate. The Zeno framing (Johansson et al. 1999) is apt and correctly mapped. Not a repetition.

**Instrument caveats accepted as disclosed.** Replay-only (no rebind feedback — the scar law prices it, untested); planar Newtonian CR3BP (the shipped probe's 21,403 relativistic chatter not reproduced, its mechanism possibly different); f(Λ) empirical (0.5/0.7 literature values verified at abstract level only; the replica itself reproduces the qualitative table, and my prograde arms corroborate the 0.5 edge). The event-budget framing (~9.4/planet-orbit vs ≤ 512/orbit) is the right unit for board bottleneck 2's bar.

**Unit error found and corrected in the page.** The claim said "~9.4 per moon-orbit"; 942/100P is 9.4 per **planet** orbit — per moon-orbit (radial cycle, the author's own `R3_rate_per_orbit` denominator, n_apo = 742) it is ≈1.3. Magnitudes were always stated with their P units, so nothing else moves; I corrected the page (current-best line, refuted entry) and added the band-wander arm to open direction 2's judged set.

**Goal fit.** Moves the handoff page's open direction 2 (the motion law v2 step 3 blocker). PRINCIPLES #14: "no work for no reason, so no ticks … you don't advance a ship tick by tick" — the per-tick boundary check is deleted for one compare at the simulation's own apsis event. #13 "errors never compound" — chatter × rebind-scar is the compounding channel; 1-per-transition makes it one-shot. #4 "no categories" — Λ replaces the pro/retro class. The gain (≥ 10² on the chatter cases: 942 → 0 per 100P) clears the 10× bar *on the replica*.

**Why silver, not gold.** The rule class is proven on a float replay replica, and the author says so: adoption is gated on the engine arm (18d2's build, the relativistic probe where the 21,403 chatter lives, the rebind-feedback error) plus a freeze decision on f and m — "It can be adopted within one step" is not yet true of the shipped code. That is exactly one named experiment away.

## The one experiment that would make it gold

Wire R3 (per-apse, f(Λ)·R_H±m) into 18d2's relativistic surface build (nine shears, rebind feedback live) and pass: the checker's six-case table, P5, the moon test — and the band-wander arm (a 0.62-class body, judged on its bounded ≤ 1/orbit rate and the m that suppresses it). Zero chatter cases must stay 0 through the shears; the f/m dials frozen.

## What the author missed

- The f±m band is not an exotic corner: a plain circular retro birth at 0.62 R_H sits in it and re-decides 89 times per 40P — worse than the shipped rule on that body. The margin m against band-wandering was sized on quiet-case apsidal drift only and never tested against a wanderer.
- The capture arm was dead code in every reported run (owner initialized to "planet"): untested until my owner0 = star arms. It works, but the 0.7-ret mirror shows a star-owned truth-retained body is never captured — symmetric edge dial, undisclosed.
- The rate unit (moon-orbit vs planet-orbit) was internally inconsistent with the script's own rate metric — caught above, page corrected.
- Literature verification stopped at abstracts (Domingos coefficients UNVERIFIED, marked as such); the Λ-ramp shape is invented and unvalidated against any eccentric/inclined table — the replica corroborates the circular table only.
- All births at θ = π/2, one launch geometry; no survey of where in the synodic phase the chatter worst-cases.
