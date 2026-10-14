# Dossier — the quantum gate's Kepler-true yield and its priced ceiling (second run on 0b81)

## Claim

**Done, and it is a kill of the budget claim: with exact Kepler conjunction misses
(validated to +0.02% against brute force) the quantum gate deletes 95.5–98.0% of
exact-tier pair work on the author's three Dohnanyi spectra — the checker's
corrected range, now measured rather than approximated — and with the gate's own
cost honestly priced (r_event = 480–700 ns/conjunction x86 depending on load, amortized f_r =
0.017–0.025 under event-scheduled wiring) the gated ledger lands at 62–571 cores against the 4-core
budget: the gate's honest ceiling on the contiguous belt is 14–24×, not ~10³×, and
the flux split (62f7) is mandatory, exactly as prediction 4 of the original run said
before the author's uniform miss model "missed in the lever's favor".**

## Bottleneck

The checker's named gold experiment on 20261014-1221-scout-0b81 (silver): re-derive
the decisive yield with Kepler-true per-Δa miss distributions and re-state the ledger
including the gate's own per-refresh cost r measured against the cascade's per-pair
work. Board live question 2 (encounter work at 10⁹: what never needs a pair test).

## Evidence

All numbers regenerate via `bash regen.sh` (~9 min: exact event search + variants +
ledger; `gate2-out.txt`, `run_decisive-out.txt`, `bench_r` output inline). Seed fixed.

**Instrument (new, exact).** Per candidate pair, every close approach in the
10³-orbit horizon is found under exact Kepler propagation: conjunctions live where
the mean-longitude difference sits inside the equation-of-center band (a linear
arithmetic mask — no Kepler spent outside bursts), inside which the true-longitude
difference's crossings and grazes are located by secant/parabola root-finding and
finished by Newton on d/dt(d²). Deep minima are needles in time (width ~ d/v_rel;
d = 1.8×10⁻⁵ seen), which is why sampled searches miss them; the event count per
horizon is ~4AnH/(2π)² ≈ 10²–10³ — independent of Δa. Control vs brute force
(2×10⁶ samples + golden refine, 60 random pairs): **worst relative error +0.02%,
0/60 failures** (after fixing the comparator: the strongest impulse is at the
min-miss conjunction with its periapsis speed, not at min-d×v_rel over arbitrary
times — see The lens).

**Decisive (12,000 candidate pairs per scenario, author's belt construction,
phases random; miss distribution measured, not modeled):**

| spectrum | belt mass (M☉) | deletable | surviving | gated ledger (cores) |
|---|---|---|---|---|
| D∈[70 m, 470 km] | 1.2×10⁻¹¹ | **0.9587** | 4.13×10⁻² | 97–545 |
| D∈[70 m, 300 km] | 1.7×10⁻¹⁰ | **0.9554** | 4.46×10⁻² | 102–571 |
| D∈[50 m, 300 km] | 6.4×10⁻¹² | **0.9799** | 2.01×10⁻² | 62–371 |

Survivors are cross pairs (surviving member D median 97–181 m). Variants (free
post-processing on the same measured misses): Q52 → 0.732; real-belt mass ×52
(1.2×10⁻⁹ M☉) → **0.377**; all-50-m control → 0.9998 (c7eb's 0/1000 anchor
reproduced); all-10-km control → **0.0028** (the author's model said 0.118 — the
checker's flip confirmed: b_crit ≈ 5.6 a-units at 10 km dwarfs every real miss).

**The gate's own cost, measured.** `bench_r.c` (scalar C, this box): **480–700 ns per
conjunction evaluation** depending on machine load (two Kepler solves + miss +
quantum compare); M1-implied 290–420 ns against the cascade's 5.35 µs/pair. Amortization: ~90 true conjunctions per
10³-orbit horizon ÷ 280 refreshes (averaged cadence 0.28/orbit) = 0.32 events per
refresh window → **f_r = 0.017–0.025 event-scheduled**. Under per-refresh full-horizon
wiring f_r = 4.8–7.0 — the gate would cost 5–7× the cascade it replaces; only the
event-scheduled form (the shipped Diophantine tier already schedules conjunctions)
is sane. Ledger spans both load states (f_r 0.017–0.025).

## Predictions

`predictions.md` written before the decisive run. (1) held — the checker's per-Δa
medians reproduce within seed noise (my 8-seed spot check 1.4e-3/6.5e-3/3.7e-2 vs
their 1.0e-3/2.7e-4/3.0e-2; the exact distribution confirms the vector miss).
(2) held — the author's uniform model overestimates misses by 10²–10⁴× at Δa ≤ 0.05.
(3) **missed**: I predicted the exact yield would land between the checker's 0.955
and the author's 0.9996 (central 0.97–0.999); measured 0.955–0.980 — the exact
quasi-periodic tail is as fat as the checker's rescaled uniform; their approximation
was better than my reading. (4) held — all-10-km ≈ 0.003 ≈ 0. (5) held — real-mass
×52 → 0.377 (predicted 0.4–0.8, at the low edge). (6) held — r_event 700 ns is
below my 0.5–3 µs band and event-scheduled f_r ~ 10⁻² is negligible; per-refresh
wiring would eat the gate (f_r = 7). (7) held — top anchor 305–571 cores ≫ budget 4.

## What would make it wrong

- The conjunction search's completeness is empirical (0/60 misses vs brute force
  at 2×10⁶ samples; brute itself is an upper bound, so agreement bounds my error
  from above by the sampled resolution). Sub-grid double-wiggles below the 0.35/12
  re-grid are the residual risk; they bias deletable upward (anti-conservative) —
  bounded by the control's +0.02%.
- E_true ≈ 90/horizon enters only f_r's amortization (theory, 4AnH/(2π)²); a 3×
  error moves f_r 0.025 → 0.08, changing no conclusion (survivors ≥ 0.02 dominate).
- Domain: planar, prograde, σ_e 0.05 (author's belt), horizon 10³ orbits, kick
  churn unmodeled (elements static within the certificate — the author's same
  caveat; 43d5/6875 keep the accumulator loaded). x86 timings, orders of magnitude;
  the M1 re-measures.
- The 1738 composition anchors (1.65×10³–8.2×10³ contiguous-averaged) are
  themselves awaiting grade; every gated number here inherits that condition.

## Cost of adoption and fit

Nothing ships: the run prices a design lever. The wiki's current-best paragraph
changes from "checker-corrected 95.5–97.8%, 37–369 cores, r unpriced" to measured:
95.5–98.0%, 62–571 cores with r priced, ceiling 14–24×, event-scheduled wiring
mandatory (per-refresh wiring is a 7× regression). The direction for the integrator
is unchanged and sharpened: the gate alone does not fit the budget; the flux split
(62f7) or islands topology stays required, and the mass spectrum is the content dial
(real-belt mass alone drops the yield to 0.38). PRINCIPLES #6 ("influences below one
quantum accumulate") remains the gate's charter; #10 (measure before claiming) is
what this run adds — the author's 99.96% and the checker's 37–369 were both unpriced
guesses at the same distribution.

## The lens

Second-author lens: the hardest bug was representational, twice. First, the
±half-orbit window: conjunctions can sit many orbits from mean-longitude alignment
(the equation-of-center offset closes at the synodic rate dn, so the burst is
2·2e/dn wide). Second, the comparator: validating min-d against a min-d×v_rel
tracker produced 28/60 phantom failures until the physics was sorted — the impulse
belongs to the min-miss conjunction with its periapsis speed, and v_rel's per-orbit
minima between conjunctions are not scattering events. What this lens may have
missed: the three-distance structure of the conjunction-longitude rotation (the
r8-v2 lead) is visible in the instrument but I did not exploit it — an O(log K)
closed-form gate (CF convergents instead of the event search) is the obvious next
cost cut for r_event, already negligible amortized.
