You are re-running a premise probe for a draft physics law. Write and run pure Python 3 (standard library only). You may create files only in /private/tmp/glm-scratch/gv1b/. Do not touch anything else, and do not run git commands.

**Context.** Your earlier probe is in /private/tmp/glm-scratch/gv1/ (gv1.py and the run_*.py scripts). Its report is /Users/julien_laurent/Research/emergent-space/artifacts/runs/gravity-v1-freeze/probe-out.md. Read both first and reuse your integrator: PG river Hamiltonian, exact drift and kick, S2 and Yoshida S4. That probe found:
- Precession, capture and deflection pass.
- The energy criterion KILLs. The cause is the per-body step rule Δ = η·r^{3/2}(current state); fixed Δ stays flat.
- The same rule also cannot bend distant-anchored light.

The owner's principle is "no ticks, not even per body": the step must never be a function of the body's own state. A failed experiment kills the configuration, never the method. So this probe tests replacement configurations.

**Configurations to test (the step belongs to the cell, never to the body).** Space is cut into cells: radial shells [2^k, 2^{k+1}) in r, with k an integer. Here dyn(r) = r^{3/2}.

- **C1:** inside shell k the step is the constant Δ_k = η·dyn(2^k). When a step would cross a shell boundary, the body is advanced exactly to the boundary crossing, and the new shell's Δ is used from there. Find the crossing point by bisection on the drift or kick, or any exact sub-step.
- **C2:** like C1, but switching between shells is made time-symmetric. For example, use the step of the shell containing the step's midpoint, chosen by a symmetric fixed-point iteration, or any reversible adaptive scheme you know (Hut–Makino–McMillan symmetrized steps, or a Sundman time transform with a fixed step in fictitious time). Name the scheme you use.
- **C3 (control):** a single global fixed Δ, as in your earlier control.

**Measurements**, with thresholds frozen now, before any run. For each configuration, order 2 and order 4, and η ∈ {1/16, 1/32, 1/64}:
1. **Energy:** the growth exponent of |ΔE| over 10^4 orbits at p = 20, e = 0.2 and p = 20, e = 0.5, fitted over [10^3, 10^4] orbits. KILL if the exponent is > 0.2 or the maximum |ΔE/E| is > 10^-6.
2. **Precession:** the relative error at p = 20 and p = 1000 (e = 0.2 and 0.5), against your elliptic oracle. KILL if no η ≤ 1/32 keeps it within 1% at both p.
3. **Distant light:** a photon anchored at r0 = 10^4 with impact parameter b = 10 and b = 30, integrated to r = 10^5 outgoing. Compare the deflection with the oracle, correcting the finite-radius tail analytically as you did before. KILL if it is > 1% off.
4. **Capture:** E = 1 anchors at r0 = 100 with L = 4(1 ± 0.01). KILL on any misclassification.
5. **Cost:** events per orbit (steps plus shell crossings) at p = 20, 100 and 1000. KILL if > 512 at p ≥ 20.

Keep every script under 60 s of wall time; for the 10^4-orbit runs, pick the case sizes that fit. Report the machine load (`uptime`) and swap (`sysctl vm.swapusage`) at the start.

**Output (your final reply):**
- a table with one row per configuration × order × η, giving each criterion as PASS or KILL with its number;
- the scheme names;
- run times;
- limitations, where your implementation may be at fault rather than the configuration.

Recommend the cheapest configuration that passes everything, or say that none does. Don't overclaim: this is orders of magnitude and 1% tolerances.
