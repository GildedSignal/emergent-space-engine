# Dossier — 20261007-1032-taleb-ab03

**Claim.** A cold belt's H_live is event-quantized, not drift-continuous: at rtf 100 no
distinguishing event fires within a whole play-session (a belt orbit is 350–580 play-hours, the
synodic averaging period 440–1,400), so the birth program's compression survives sessions; the
real distinctions are discrete encounter steps, concentrated in the Giant-crossing minority
(293/4096 within the Hill radius and 94–104/4096 scattered to unbound — full 144-bit
individuals — within 20 game-years), while the belt proper is *not* fat-tailed at these
horizons (p99/mean = 1.2).

**Bottleneck.** Board risk "Distinctions created per game-second (H_live)… not measured yet"
(the decision of whether 10⁹ fit in 8 GB). Expected gain: not an order of magnitude of compute
but the first measured rate; it deletes the fear that secular drift erases the belt's program
within hours, and it redirects B18b's churn model.

**Evidence.** Scene = the plane's own (Giant μ=2⁻¹⁰ at 4.94 AU e=0.05, B18b belt shape
2.0–3.5 AU + 4,096 crossers 5.5–6.5 AU; N=69,632 test particles, Wisdom–Holan drift-kick with
the indirect term, solar units). Columns = the tube's (E Q48, L Q32, ω/λ u32) vs the frozen
program. Two harness iterations, both kept:
- v1 (`hlive_probe.py`, `hlive.json`): its μ=0 control FAILED (17,885 scarred, 3.5 bits) —
  comparing *osculating* elements charges every body with the Giant's short-period forced
  wiggle (~10⁻² AU in a), which the law never stores (kicks are orbit-averaged). Rebuilt.
- v2 (`hlive_probe2.py`, `hlive2.json`): orbit-averaged mean elements, LSB floors from the μ=0
  control. Key rows (mean bits/body vs frozen program, belt only): 1 play-hour ≈ 0
  distinguishable mean-element bits (coverage of the averaging window 0.00 — the mean element
  does not exist yet); 5 yr: 102.5 (p99 117, scarred 100%); 20 yr: 108.8 (p99 123). dt-halving
  check (0.0625 → 0.03125): median |ΔE| = 4.325e-3 at both, so the drift is physical, not
  discretization. Crossers: min distance 0.004 AU, 293 within 0.34 AU (Hill), 94–104 unbound,
  in 20 yr. Machine: load 4.2, 15 GB RAM, 8 vCPU shared; each run ≤ 60 s wall.
- Reproduce: `python3 lab/results/20261007-1032-taleb-ab03/hlive_probe2.py` (≈ 30 s).

**Predictions** (`predictions.md`, written before the decisive run). Held: μ=0 control gates the
harness (v1 failed on it and was rebuilt); reabsorption never fires on mean columns (monotone
drift, 0 events); encounters scar within 20 yr (I predicted none — falsified, and it is the
main result). Failed: frozen scar 6–14 bits at 1 play-hour (measured ≈ 0 — I overestimated the
danger); belt tail p99/mean ≥ 3 (measured 1.2 — the tail lives in crossers, not the resonant
belt); smooth-in-a program absorbs the mean but not p99 (absorbs neither: the drift is
phase-locked to the synodic angle, a function of shared state, not per-body information).

**What would make it wrong.** (1) The "drift is machinery" reading assumes the program can
carry the Giant's deterministic response; a program cannot absorb it if kick history is
path-dependent per body (chaos) — untested beyond 20 yr; the separating experiment is a
secular-shadow twin (same birth state under the averaged field only; the difference is the
irreducible part). That experiment is the named gap: my 100-bit 20-yr figure is an UPPER bound
on irreducible bits. (2) rtf: at rtf ≈ 10⁴ one play-hour ≈ 1.1 yr and the 85–95-bit rows apply
— the frozen program is erased in the first hour at those speeds. (3) Test particles: belt-belt
encounters excluded (optical depth ≪ secular rate at these horizons; r8's 427/1.7M supports
this). Cost of adopting: B18b's churn model ("10⁻² per epoch for 12 epochs") should be replaced
by event-quantized churn with a crossing-population tail and unbound individuals, before it
freezes a wrong regime into a gate.

**Fit with PRINCIPLES.** "Nothing is evolved that can be derived" (P3): the synodic response is
derived, and storing it as scars would be the violation; "the simulation decides, heuristics
schedule" (P22): H_live's cadence is the law's kick epochs, not a per-tick rate; "a test that
cannot fail is a control" (P10): the μ=0 control killed the first harness.

**The lens.** Taleb's fat-tail hunt found the tail where it lives (crossers 2.3% unbound,
steps, self-concentrating) but the lens predicted the wrong tail (resonant belt bodies) and
overrated the mean's fragility — the belt is Mediocristan at game timescales. The blind spot
the README warns about (freezing progress) did not bite: the probe deletes a fear rather than
adding a guard.
