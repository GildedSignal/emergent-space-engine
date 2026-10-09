# Predictions (written before the decisive run)

Question: is H_live (live per-body distinctions, bits/body) bounded under iterated kicks, and
where does it sit against the 4 GiB / 10^9 = 34.4 bits/body universe budget?

Setup I will run (not tuned on): convoy population (perfect program, m members, 5 columns),
each round a fresh f = 1/8 of members kicked with the crate's own `Pop::Convoy.kick`
(deltas ±2^16 on t_p, ±2^10 on E, L, ω), seal + compact each round, 24 rounds.
Controls: f = 0 (must stay at the program floor) and `random` rung members (incompressible side).

Held-out predictions:

P1 (controls). f = 0: chosen bits/body stays ≤ 1 bit for all rounds. Random rung: chosen
    bits/body ≥ 60 (form-B floor for law-range-uniform columns).

P2 (walk, not plateau). Form-P bits/body grows ≈ ½·log2(mean kicks per body) per kicked
    column: slope ≈ 2 bits/body per doubling of k̄ once most bodies hold a scar
    (4 kicked columns × 0.5 bit per doubling), plus an Elias–Fano index ≈ 2 bits/body
    once scar fraction → 1. No hard plateau within 24 rounds.

P3 (crossover). Form B (shelf with repack) crosses below form P at mean kicks/body
    k̄ ≈ 1–2 (scar fraction ≈ 0.5–0.7); chosen = min(P,B) thereafter follows B.

P4 (budget straddle). chosen bits/body at k̄ = 3 (round 24, f = 1/8) lands in 20–60
    bits/body. If it lands < 34.4 the belt fits the budget at that diffusion depth;
    the walk direction at round 24 is still upward (logarithmic).

P5 (no self-reabsorption). `infer` (majority program) on the kicked members fails
    permanently once the cumulative distinct-kicked fraction passes ≈ 0.4 (both-unkicked
    pair fraction drops below ½ around cumulative f ≈ 0.3): the launch program cannot
    reabsorb diffusion; only repack (form B) or a new family (sort by element) can.

P6 (overwrite economics). dH per kick (marginal bits per additional kick, from the
    trajectory) falls like 1/k̄: at k̄ = 3 it is ≤ 1/3 of the per-kick cost at k̄ = 1.
    Stored distinctions ≠ distinctions created: re-kicks overwrite.

What would make the whole picture wrong: if form B's dictionaries compress the diffused
residuals to a hard plateau below ~10 bits/body (then H_live is bounded and cheap), or if
chosen bits/body exceeds ~100 bits/body at k̄ = 3 (then the belt breaches the budget an
order of magnitude early and shipmem's family needs redesign, not tuning).
