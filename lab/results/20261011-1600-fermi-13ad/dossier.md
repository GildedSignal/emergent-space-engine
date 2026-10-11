# Dossier: H_live at 10⁹ — what creates scar bits per game-second, and what reabsorbs

## Claim

Ship-to-ship gravity creates **exactly zero** scar bits at any belt density up to 10⁹ (measured:
every ship–ship kick, down to contact range, is ≥9 orders below the (E,L) quantum, and the
accumulated random walk at 10⁹ crosses one quantum per ≥10¹¹ orbits), so H_live's only growing
channels are contacts, massive-body encounters and decisions — and the contact channel alone,
on one close-in 10⁹-body belt, exhausts the 4 GiB budget in **9–18 play-hours** for immortal
ships unless contacts are terminal or herds re-program, in which case H_live is bounded.

## Bottleneck

Board risk "Distinctions created per game-second (H_live): they, not the body count, decide
whether 10⁹ fit in 8 GB; not measured yet" (HANDOFF, 6 October); queue item `b-h-live`. This
run supplies the physics half the frozen gates lack: B18b gates the scar *codec* against a
synthetic 50-bit churn kick; nothing measured what real dynamics create or destroy. Gain: the
encounter skin ρ is freed for ships (any ρ above the contact radius creates no gravitational
scar memory — one design constraint deleted), and the allocator gets its signal: watch the
contact-scar count, not the body count.

## Evidence

Machine: GitHub Actions Linux, 8 vCPU, load 0.24–0.70, 14 GB free at start; all processes
≤ 2 GB except one bug (below). Commands (from `lab/results/20261011-1600-fermi-13ad/work/`):
`python3 hlive_probe.py` (241 s, writes `hlive.json`; per-run walls 9–78 s), then the kick
table (`kicks.json`, 0.2 s: `hp.kick_entropy` over `events_B18b_N1e4_geom.npy`, sweep μ ×
quantum), and `python3 analyze.py` (extrapolations, 0.2 s).

Belt: B18b's frozen geometry (p one octave a∈[1,2), e Rayleigh σ=0.07 capped 0.6, uniform
angles). Units G·M=4π², time in a=1 orbits. Encounters found by exact Kepler propagation,
spatial hashing, per-event impact parameter b = |Δr×Δv|/|Δv| (resolves ρ ≪ step size), deduped
to one row per conjunction.

1. **Rate law (warm belt, flyby regime).** Encounters per body per a=1 orbit at ρ=10⁻⁴:
   N=2×10³: 1.25×10⁻²; N=10⁴: 6.33×10⁻²; N=5×10⁴: 3.17×10⁻¹. rate/N = 6.25/6.33/6.33 ×10⁻⁶ —
   mean-field linear (exponent 1.00 over 25× in N). b-distribution slope α ∈ [1.0, 1.25]
   (two estimators; see "wrong" below). At N=10⁹: **6.3×10³ encounters (ρ=10⁻⁴) per body per
   a=1 orbit** — 6.3×10¹² per orbit in one belt, all sub-quantum for ship masses.
2. **Channel A is dead, per kick and cumulatively (ship–ship gravity).** Kick entropy per
   participant (b<10⁻⁴): ship (10⁶ kg): **0.000 bits at every quantum 2¹²–2²⁴ over the belt's
   E range**; sub-quantum fraction 1.0000. 10¹⁵ kg: 0.005–2.4 bits. 10²⁰ kg (μ=5×10⁻¹¹): 7.7–
   12.6 bits (the scar threshold mass sits between 10¹⁵ and 10²⁰ kg, as estimated). Planet
   (μ=10⁻³): 12.57 bits = log₂ n, sample-limited floor — strong encounters fully re-state the
   orbit (consistent with B18b's frozen 50-bit churn model at the strong end). Cumulative at
   10⁹: RMS kick 1.8×10⁻⁹ quanta of E; √(6.3×10³) kicks/orbit → **1.3×10⁻⁷ quanta/orbit** —
   one quantum per ≥10¹¹ orbits (10¹³ at q16). The belt's collisional diffusion is invisible
   at the law's quantization for any playable time.
3. **Channel B (contacts) — the only channel that scales into the budget.** Contact radius
   R/a = 4.4×10⁻¹⁰ (100 m ship at 1.5 AU). Extrapolated rate at 10⁹ (α=1): 2.8×10⁻² per body
   per a=1 orbit = 5.1×10⁻² per own orbit — **~5% of a 10⁹ belt contacts per orbit**. At
   α=1.25: 3×10⁻⁴ (90× less). Per play-hour at rtf 100 (1 h = 1.14×10⁻² yr sim):
   - belt at 1.5 AU: 1.7×10⁻⁴ contacts/body/h → 0.02%/h individuated → 1–3 MB/h → wall ≥ 1400 h.
   - close-in belt at 0.05 AU (one orbit ≈ 1 play-hour): 2.8×10⁻² /body/h → 2.8%/h →
     **0.23–0.46 GiB/h → wall 9–18 h** (64–128 bits/survivor; 8.8 h at 128 bits). At α=1.25
     the wall stretches ~90×.
   - If contacts are terminal (km/s impacts on real materials): the same rate becomes churn
     (2.8%/h destroyed and re-born); death records ~7 bits each (Elias–Fano) ≈ 45 MB/h, births
     on a scheduled grid 0 bits/ship (law.md) → **H_live bounded**. Boundedness is a design
     choice at this channel, not a physics given.
4. **Channel C (massive bodies):** ≥12.6 bits/event measured (floor), full re-state at the
   strong end; rate not measured here (needs the plane's planet/moon census) — scales with
   N×crossing-fraction, same order as contacts at 1.5 AU. Channel D (decisions): bounded by
   the c-cone (principle 5); unmeasured, AI off-plan.

## Predictions (predictions.md, written before the decisive run)

- P1 (ship–ship gravity sub-quantum, 0 bits at all distances): **held exactly** — the run's
  strongest result.
- P2 (rate ∝ N, ∝ ρ, 0.01–0.3 at N=10⁴ ρ=10⁻⁴): held (6.3×10⁻²; exponent 1.00; α 1.0–1.25).
  The σ_e scaling leg was **not measured cleanly** (see P3).
- P3 (r8 anchor within factor 3): **failed on the cold end.** At r8's low-σ_e belts my rates
  exceed belt-0's truth by 10–30× at any ρ in their box. Mechanism: below σ_e ≈ 0.02 the
  "encounters" are persistent co-orbital companionships (v_rel ~ 10⁻², approach duration ~
  orbits), not flybys; my window-per-conjunction convention over-counts there, and r8's
  dip-quantum definition (r8 v4) is the right one — the same regime the taleb-09b5 gold
  flagged for concentrated workloads. The load-bearing warm-belt numbers are in the flyby
  regime (98% of b<10⁻⁴ events have v_rel > 0.05).
- P4 (contacts at 10⁹: 10⁻³–10⁻² per body per orbit): bracketed by the measured
  [3×10⁻⁴, 2.8×10⁻²] (α uncertainty).
- P5 (strong-event bits 20–60): the measured floor 12.6 is sample-limited (log₂ n); the
  strong regime re-states the orbit, so B18b's 50-bit model stands at that end. Ships: 0 ✓.
- P6 (close-in wall ~10–100 h unless reabsorbed): measured 9–18 h at α=1 — just below my
  bracket's low end, same order.
- P7 (falsification condition): triggered at α=1 for one close-in 10⁹ belt with immortal
  ships; not triggered at α=1.25 or with terminal contacts.

## What would make it wrong

- The contact-rate extrapolation spans 6 decades of b on a slope measured over ~4 (α 1.0 vs
  1.25 moves the wall 9 h ↔ ~1 month). A dedicated small-b run (finer steps, b down to 10⁻⁸)
  would pin α. The kick table is insensitive to this (9 orders of margin).
- The impulse approximation and the (E,L)-key quantum split (16/16 assumed; swept 2¹²–2²⁴)
  could shift the scar-threshold mass by ~an order either way; it cannot rescue ship–ship
  gravity from 9 orders down.
- Co-orbital/formation belts (fleets on one orbit) invalidate the uniform-phase rate: the
  gold 20261006-0346-taleb-09b5 shows concentrated workloads have their own certificate; my
  rate is the smooth-belt floor, and formations sit on top of it.
- One bug, disclosed: the first run's dedupe kept the min-distance flag whose local b is
  contaminated for slow approaches (23% undercount at b<10⁻⁴); fixed to min-b, and the first
  run was also OOM-killed (my row stream flooded on slow flybys, >2 GB) before its cold-belt
  runs — both fixed in the shipped `hlive_probe.py`, which regenerates every number above.
- Costs nothing to adopt: no engine code changes; it deletes a constraint (the skin is free
  for ships) and names the allocator's signal.

Fit with PRINCIPLES: "Compute only surprises" (§3) — quantization makes ship–ship gravity a
non-surprise forever; "The memory floor is information" (§24) — the floor is the contact
channel, not the body count; "each scale resolves only what matters at that scale" (§33) — an
ant's raindrop: 10⁹ sub-quantum kicks never reach the quantum. And per §9, the cold-belt
failure kills my event convention for that regime, not the method.

## The lens (Fermi)

The estimate came first and the run confirmed its strongest claim (P1) with 9 orders of
margin — but the lens also led me to underweight one thing: I predicted rates before
checking which *regime* the rate lives in (flyby vs co-orbital companion), and the estimate
was blind to the dedupe-convention sensitivity exactly where events are slow. A Fermi lens
catches orders of magnitude, not conventions; the cold-belt miss is a convention error, and
only the run caught it. What the lens may still have missed: the player-decision channel's
bits per action, and whether formation-dense belts multiply the contact channel the way the
taleb gold showed for candidate work.
