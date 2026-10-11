# Predictions — 20261011-0324-fermi-c211

Written before any measurement in this run. Machine: GitHub Actions Linux x86, 8 vCPU; orders of
magnitude only (the integrator re-measures on the M1). The question: at 10⁹ bodies on one 8 GB M1,
which budget term breaks first — program memory, scar memory (H_live), kick compute, or bandwidth?

Constants carried in from the record (not tuned here): kicks cost 29 µs on the plane (H0210);
32 kicks/orbit, 0.3 with secular averaging (H0190); a smooth belt stores at 0.126 bits/body
(components-98bc); r8 v2 belt 0: 427 encounters over 20 orbits at N ≈ 1841 (ρ ∈ [10⁻⁴, 10⁻³]),
≈ 0.012 encounters per body per orbit.

## P1 — bits per body by population (measure example)

- traders (smooth doll population, exchangeable): ≤ 0.5 bits/body.
- stream (belt-like, 4 orbit keys): ≤ 5 bits/body.
- battle (Fermi frame, 8 columns, fresh contact randomness): ≥ 5 bits/body.
- random (fully distinguished, the scar-cost ceiling): between 100 and 250 bits/body.
- Held-out consequence: the scar-to-program ratio is ≥ 100×.

## P2 — access costs (this machine, orders only)

- streaming decode: 5–50 ns per body.
- random access: 30–300 ns per body.
- hot-tier update p50: 100–1000 ns.
- compact (reabsorption) ≤ 10× the hot update per update.

## P3 — reabsorption (the held-out physics of the run)

For orbit populations whose kicks are small relative to the store's resolution
(traders/stream/convoy, kick deltas ±2¹⁰ on 48-bit fields), compaction reabsorbs the kicks:
bits_after − bits_before ≤ 1 bit/body. For battle (two fields re-drawn at 48 fresh bits),
distinctions persist: bits_after − bits_before ≥ 10 bits/body.

## P4 — the H_live curve (ladder example)

Bits per body against the kicked fraction f: at f ≤ 10⁻² the program+scar form stays within
2× of the f = 0 program (scars are small deltas, not full states); the packed form B wins only
at f ≥ 0.1–0.3. So the memory cost of a scar is ~10–40 bits (a delta), not ~157 bits (a state).

## P5 — the budget verdict at 10⁹ (derived, not tuned)

- Program memory: ≤ 1 GB even at 5 bits/body × 10⁹ — at least one order under the 4 GiB budget.
- Kick compute is the binding term, and it binds on the short-orbit (active) population only:
  the M1 at 29 µs/kick sustains ≈ 3×10⁵ kicks/s, i.e. ≈ 9×10³ orbit-completions/s at 32
  kicks/orbit (3×10⁵ at 0.3 averaged). A billion bodies on ≥ 1-year orbits with averaging cost
  < 0.1 core at RTF 100; a billion on ~80-minute orbits (the board's 190-core corner) is ~200×
  over the whole machine.
- Steady-state scar memory: if every body carries a ~30-bit delta, that is ~3.75 GB at 10⁹ —
  within a factor of 2 of the 4 GiB budget, so H_live must be admission-controlled by re-fit
  cadence, and the re-fit is itself compute (measured compact + stream rates), not memory.
- Bandwidth: at ~10⁹ events/s the 60 GB/s bus is saturated only if each event touches ≥ 60 B —
  the measured hot-update path decides; predicted not binding below the compute term.

## What would make this wrong

- P3 failing (bits_after jumps on small kicks) would mean scars are not deltas but states, and
  memory, not compute, is the first-breaking term — the opposite verdict.
- The r8 encounter rate not carrying to 10⁹ at fixed density (the q-candidate-degree silver says
  work per encounter stays constant; if the encounter *rate* per body grows with N instead, both
  the scar term and the kick term break together).
