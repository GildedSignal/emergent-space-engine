Grade: silver

**Abstract.** Claim: the plane's 1/64 kick cadence is already at the uniform cliff — no coarsening and no higher-order split cuts events/orbit at equal behaviour, so bottleneck 1's 10× must come from the averaged/doll path. Reproduced bit-for-bit (tuning, decisive, verdict, RK4 invariant 1.9e-13 over 200 orbits); references converged (1024 vs 4096: ≤0.3%); y4 stays dominated at every budget ≤64 events (fails H2 apsis +14% at 48 events, J error ~20× kdk at equal events even at 96); J* walks linearly (α≈1) at every cadence. One half of the named premise is untested: `q-correctors` names correctors proper (WHFast-style modified kick), and only coarsening + Yoshida-4 were tried. Cost to adopt: none (a redirect decision) — after that one run.

## Reproduction (clean copy in /tmp; nothing in this folder touched)

- `cc -O2 -o cadence cadence.c -lm`, `bash tuning.sh`, `bash decisive.sh`, `python3 verdict.py`, `./rk4`: every JSON row of both sweeps **identical bit-for-bit to the stored files**, including the same two crash positions in tuning (T3 kdk-4, y4-8) and H4's 1024-reference crash in decisive. Total 35 s on this 2-vCPU shared container; rk4 2.2 s.
- `verdict.py` prints the stored verdicts: kdk-64 PASSes all judged-in seeds (apsis −5.2/+0.5/−0.2%); H1 fails at 32 (−10.6%); H2/H5 pass at 16; minimum uniform cadence 64 (gain 1×). One cosmetic bug (the `<- ...` annotation also prints under PASS rows); verdicts unaffected.
- **Timing order holds:** tuning.jsonl 06:09:26 → predictions.md 06:10:35 → decisive.sh 06:10:58 → decisive.jsonl 06:11:07 → verdict.py 06:12:29. Held-out seeds appear nowhere in tuning.jsonl. `work/patch.diff` is empty (no tree edits).
- All dossier numbers I recomputed match: y4-8 apsis −8.0% (T1), −56.6% (T2), +534% (H1), −43.2% (H2); B1 negative control e 1.66×, apsis −47.5%; B1 reference pumps e 0.02→0.129 (frozen chaotic rule); H4's reference itself ejects (guard e=1.00016 in decisive.jsonl).
- Faithfulness: step.rs/force.rs confirm the target — `1/64` of the radial period, phase-stepped, drift H/2 + midpoint kick of weight H + drift H/2, rebind per kick, SyMBA only near secondaries. J* = v²/2 − 1/r − μ/d − h_z + μ(r·r_p) verified exact for the coded ODE both symbolically (I derived dJ*/dt ≡ 0) and by rk4.

## Novelty

No HISTORY entry tests cadence or higher-order splits for this layer. H0190's 114× is the *averaged* path (different mechanism); H0210/H0211 record "kicks cost 29 µs / kicks still dominate"; law.md already makes averaging the design away from resonance — so the redirect was the intent, and this run's contribution is the measured kill of the raw-layer route the board still lists first ("correctors, higher-order splits"). r4 v1/v2 (phase feedback near resonance) is a different regime; r2 (carry widths) a different question.

## Goal fit

Board #1 verbatim. PRINCIPLES 19: "if you find yourself fixing things that's oftentimes a signal that it is the wrong representation" — the cliff is the representation's, not the integrator's. PRINCIPLES 13 ("errors never compound"): the linear J walk is exactly the compounding type, correctly flagged for B12.

## Attacks (five, all run here)

1. **Reference convergence** (kdk 2048/4096 on H1, 4096 on H2/T1): domdt within +0.26%/−0.03%/+0.01% of the 1024 refs — the 10% gate is meaningful. H1-32 is −10.9% against the converged reference: a real fail, by a ~1% margin.
2. **y4 at 48 and 96 events** (T1, H2): apsidal bias decays with cadence (T1 −8%→−2.1%→−1.3%; H2 −43%→+14%→+7%) — "wrecked" is not permanent. But at 48 events y4 still fails H2's apsis (+14%) where kdk-16 passes, and at 96 events it still fails the frozen dJ gate (~20× the kdk error at equal event count). Domination at every budget ≤64 is confirmed; the kill stands.
3. **H1 neighbourhood** (a=0.61/0.62/0.63, M0=1/2/2.5/3, own 1024 refs): kdk-32 passes 3/5 (−2.2%, −2.7%, −5.9%), fails 2 (−19.7%, −10.1%). The uniform cliff is 64 on this sample but 32 on half the neighbourhood: sample-dependent between the author's own frozen "32–64". Uniform gain ≤2× either way; the 8× bar remains unreachable, so the headline negative is robust.
4. **Quiet floor** (a=0.55, e=0.05, μ=1e-5, own ref): kdk-**2 events/orbit** matches apsis to +0.09%. Per-body headroom is ≥32×, not the conceded 4×.
5. **The 4096-cadence claim** (no stored evidence): reproduced — α = 1.000/1.012/1.034 at 4096/orbit on T1/H2/H1. But the walk's *size* scales ∝ 1/cadence (T1: 3.1e-4 at 64 → 4.8e-6 at 4096), so "will see ~1e-4–3e-4 regardless of cadence" is right in type, wrong in size outside the plane's own 64.

## Why silver, not gold

The load-bearing negatives are reproduced and survived every attack: uniform cliff (1–2×, never 8×), y4 dominated, linear J walk, judged-out regimes. What blocks gold: the queue item is `q-correctors` and the board lists "correctors" *first* — in N-body practice that means a symplectic corrector / modified kick (WHFast family), which specifically attacks the map-vs-flow gap at coarse steps. The run tested coarsening and Yoshida-4 only. Killing the premise's named half needs one more configuration; until then "stop spending on cadence/higher-order splits" is adopted, but "the raw layer is dead for the 10×" is one experiment short. Secondary dents: the "regardless of cadence" size claim (attack 5), the permanence wording on y4 (attack 2), and the knife-edge 64 (attack 3).

## The one experiment that would make it gold

Add a WHFast-style corrector (modified kick, or corrector-initialized rebind) to `cadence.c` and run the same frozen gates at 8–16 events on the same held-out seeds. If apsidal rate and e-pumping still break, the premise-kill is complete and the redirect to the averaged path is gold; if it passes, the queue's premise was right and the raw layer lives.

## What the author missed

- The quiet floor is ≥32× per body (2 events/orbit at μ=1e-5): the per-body dimensionless cadence selector — their own proposed follow-up — is undersold at "4×", an artifact of freezing μ ≥ 3e-4. Most of a real system's bodies sit there.
- The cliff's 64 is knife-edge in phase across the near-2:1 band (3/5 nearby seeds pass at 32); reporting "32–64" (their own frozen prediction) rather than "64" would have been the honest pin.
- "Regardless of cadence" conflates the walk's type (linear, cadence-independent — true) with its size (∝1/cadence — false at 4096).
- The 4096/orbit rows backing prediction 7 were not saved (reproduced here); the disclosed "13 variants per seed" exceeds the 8 per seed visible in tuning.jsonl.
- H3/H4 were excluded by ejection-at-all-cadences, a *post-hoc* extension labelled "frozen rule" (the frozen rule covered only reference e-pumping). Disclosed and defensible — no reference behaviour survives — but mislabelled.
- `decisive.sh`'s `|| echo crash` never fires (sed masks the exit status), so crashed rows are silently absent rather than recorded; `verdict.py`'s annotation prints under PASS rows.

Machine state: GitHub Actions cloud container, 2 vCPU x86 shared, 7 GB, idle besides these runs; costs reported as counts (events/orbit), which are machine-independent.
