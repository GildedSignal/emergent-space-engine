# Dossier — 20261009-2257-fermi-5f45 (Fermi lens)

**Claim.** At fixed belt density, 10⁹ bodies fit the 8 GB M1 with 2–4 orders of memory margin (encounter-driven H_live creation is ~10⁻⁵–2×10⁻³ bits/body/orbit, crossing the 64 bits/body budget only after 275–1,600 real hours at RTF 100 with zero reabsorption); the binding term at 10⁹ is kick-adjacent compute (candidate re-setup at 0.3 kicks/orbit × k≈340–750 pairs × 2.5–24 µs), which burns 2–4 whole M1s per game-second at day-scale orbits and 47–104 at hour-scale — and every one of these numbers swings on one unmeasured engine constant: the orbit period in game-seconds.

**Bottleneck.** Board risks "candidate work at scale" + "H_live decides whether 10⁹ fit; not measured yet" (HANDOFF 6 Oct). Gain: deletes the memory fear at plane scale (no new machinery needed for 10⁹ *storage*) and names the compute wall and its gating measurement.

## Evidence

Instrument: fresh Öpik–Arnold-style conjunction Monte Carlo (`opik_belt.py`, numpy, 3.5 s, 5×10⁶ samples/run, seed 20261009; shares no code with `crates/encounters` or the r8 harness). Belt: a uniform in [1−w, 1+w], e Rayleigh(σ_e=10⁻²), surface density 37,500 bodies per unit Δa/a; encounter radius ρ/a ∈ {10⁻⁴, 10⁻³} (r8 v4's range); m/M★ = 10⁻⁹ (chosen so the median kick ≈ the design's own case-d scale δa/a ≈ 10⁻³ — **not an independent measurement**). Reproduce: `cd lab/results/20261009-2257-fermi-5f45 && python3 opik_belt.py` → prints + `opik_out.json`.

| quantity | narrow belt (w=0.02, N=1500) | wide belt (w=0.2, N=15000) |
|---|---|---|
| encounters/body/orbit, ρ=10⁻⁴ | 4.6×10⁻⁵ | 8.0×10⁻⁶ |
| encounters/body/orbit, ρ=10⁻³ | 4.7×10⁻⁴ | 8.0×10⁻⁵ |
| bits per encounter outcome (3 components + timing, 10⁻⁶ quantum) | 50 | 48 |
| bits/body/orbit (ρ=10⁻⁴) | 2.3×10⁻³ | 4.0×10⁻⁴ |

Reality check: r8 v2's belt 0 gave 427 encounters / 20 orbits ≈ 2×10⁻³/body/orbit (N≈10⁴, ρ presumably ~10⁻³) — my ρ=10⁻³ narrow belt is within 5×.

Memory stack at 10⁹ (analytic, from law.md constants): materialized tubes 16 B × 10⁹ = **14.9 GB > 8 GB** (the naive store breaks, ×2); population programs 0.126 bits/body = **15 MiB** (gold components-98bc); budget for everything ≈ 64 bits/body. H_live stock with **no reabsorption at all**: 64 bits/body crossed after 275 real h (narrow, hour-scale orbits, RTF 100), 1,600 h (wide, hour-scale), 6,600–38,000 h (day-scale), ≥2.4×10⁶ h (year-scale). With canonical-tick replay + program refit as absorbers, bounded far inside any session.

Compute (analytic over measured constants: 0.3 kicks/orbit/body [H0190], setup 2.5–24 µs/pair [law.md §encounters], k = 340 [r8 v2 belt 0: 1.7M pairs] to 750 [2·sd·σ_e]): whole-M1 machines burned per game-second = 2–4 at day-scale orbits, 47–104 at hour-scale; ÷12.6 with the slack skin → 0.16–0.34 (fits) vs 4–8 (does not). Kick *evaluation* itself (≈10³–10⁵ ops) is never the wall.

Claim-check (board: "10⁹ orbiting bodies ≈ 190 cores", 29 Sep): implied cost per kick at 32 kicks/orbit is 4×10⁴ ops (hour-scale orbits, plausible), 6.5×10⁵ (day-scale, marginal), 2.4×10⁸ (year-scale, absurd). The headline is consistent within 10× **only** under hour-scale orbits: it hides a ~10⁴–10⁵× time compression. Not wrong — under-determined; the falsifiable form needs the game's orbit period in game-seconds.

## Predictions (predictions.md, written before the run)

- P1 rate ∈ [10⁻⁴, 10⁻²]/body/orbit: **missed low** by 2–12× (measured 8×10⁻⁶–4.7×10⁻⁴; I neglected the ρ/σ_e geometric factor). The N-scaling clause also broke informatively: at fixed surface density, widening the belt 10× *dropped* per-body rate ~6× — narrow belts (w ≲ few σ_e) get a real uplift; "fixed density" is two regimes, not one. This is the dilution direction the board already flagged, now with a mechanism.
- P2 bits/outcome ∈ [30, 300]: held (48–50).
- P3 H_live ≤ 1 bit/body/3 h session: held (worst 0.69, hour-scale orbits).
- P4 first-breaking term = candidate re-setup, crossover RTF 10²–10³ at 1 AU: held in structure; sharper: the crossover is set by orbit scale, not RTF alone.
- P5 190-cores within 10×: **ambiguous** — hidden time-compression variable; see above.

## What would make it wrong

3D inclinations (I ran a flat belt) thin the encounter rate further (~ρ/H ≤ 10⁻² possible), which only strengthens the memory side and weakens the compute side's encounter contribution — but kick cadence (0.3/orbit) is independent of encounters, so the re-setup wall stands. μ was tuned, not measured. The bits/outcome quantum (10⁻⁶) is the law's floor; a finer per-cell quantum moves bits/outcome by log₂. Öpik shares the epicyclic approximation with intuition but no code with r8 (memo-artifact lesson: this is instrument independence, not full independence of *premise*). Biggest gap: the orbit period in game-seconds is assumed, never measured — `xtask universe` could read it off the flying plane in minutes (it is also the b-h-live build's first number).

## Cost of adoption, PRINCIPLES fit

Adoption = one line on the board (memory is safe at plane scale; the wall is re-setup) and one added measurement (orbit period in game-seconds, plus H_live as already queued in `b-h-live.md`). Fits "the memory floor is information-theoretic" (H_live ≪ 64 bits/body: the floor is not near), "cheapest compute is compute not done" (tubes must never be materialized for all bodies: programs + on-demand tubes), and "compute only surprises" (encounter surprises are rare per body; the cost lives in the *maintenance* around kicks, not the events).

## The lens (what Fermi may have missed)

Fermi estimates freeze a regime into constants: my belt is cold, flat, isolated — no resonance clustering (r4), no co-orbital formations (gold taleb-09b5 showed those break the *candidate* tier, and they would raise encounter rates locally), no player-driven structure (fleets: the board's top scaling risk). The 275-hour figure is for uniform belts; a 10⁶-ship formation on one orbit concentrates creation enormously and could eat the memory budget orders sooner. The lens also cannot see dynamics I didn't model: e-growth raising σ_e over session time raises rates ~linearly. Machine: shared runner, loadavg 0.37 during the run, 3.5 s wall, ~400 MB peak.
