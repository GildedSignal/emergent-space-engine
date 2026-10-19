# Predictions — 20261019-0628-second-20261019-0141-fermi-097e-a67e

Written before every flight below. Context: the checker's named experiment for 097e (the
promotion fraction) was run by 0659 and graded gold twice (p = 1.0). This run re-verifies its
decisive held-out arm, then measures the one constant the checker named as still unwired —
the shipped build's **steady-state live bytes per body at ladder N** — because 097e's memory
row (2,348 B/body → 294×) is a **birth-state** number: the 10-s rtf-100 probe flights end at
~1,000 game-s, before the belt's first clock wave (~14,280 gs), while the same ledger's τ dial
uses 5,100 B (the post-first-kick cost). Every belt body receives one clock item per wave and
0659 measured every item fired ⇒ rebind ⇒ the compiled orbit is minted. Nobody has measured
the post-wave bytes at ladder N.

## Census re-verification (deterministic; same seed, same patch family as 0659)

- **C1.** `10000 coast 52 280` (0659's held-out A2): clock items 9,710, fired 9,710 —
  share 1.0000, exact counts. If the share is < 0.999, 0659's p = 1.0 fails at its own
  held-out rung on this box and the dial reopens.
- **C2.** `30000 coast 52 280` (A1): clock 29,710/29,710.
- **C3.** `30000 coast 46 1050` (A3, waves 1+2): clock 59,425/59,425.

## Memory per body at flight end (the new measurement; rss from /proc, dashboard exact)

- **M0 (birth, pre-wave control).** `10000 coast 10 100`: b_per_body (build-end footprint/N)
  ∈ [2,300, 2,550]; flight-end bytes/body ≤ 1.15× the build-end value (only the player's
  stream has run).
- **M1 (post-wave-1).** At both 10⁴ and 3×10⁴ (52 s rtf 280): end-state bytes/body
  (footprint delta over the whole flight, (rss2−rss0)/N) rises to **≥ 1.5× birth**; central
  band **4,000–7,500 B/body** (HANDOFF's ~5,100 for the post-first-kick state ± 47%).
  - *Kill A (the other way):* if end-state ≤ 1.2× birth (≤ ~2,800), the scoreboard's 5,100 B
    does **not** transfer to the belt class at ladder N — 097e's dial byte end is then
    smaller than assumed and τ loosens; I report that as the refutation of the transfer.
  - The dashboard's exact `bytes_per_body` (BodyRec + plan + trajectory + history) should
    rise in the same direction; if footprint and dashboard disagree in direction, the
    difference is allocator/catalogue overhead — report both, never blend.
- **M2 (accumulation vs steady).** End bytes/body at two waves (C3's flight) minus one wave
  (C2's) ≤ +25%: history prune keeps retired segments bounded, so the post-first-kick state
  is the steady state. If it grows ≥ +80% per wave, **memory compounds per cadence step** —
  a law-level leak at 10⁹ (each wave retires one Segment per body) and the row's worst fact.
- **M3 (noise).** RSS is machine-state dependent: a repeat of one arm must agree within 5%;
  the dashboard counters are exact integers and must agree bit for bit.

## Ledger, after the anchors (arithmetic, page-cited constants unchanged except the two fixes)

- **L1 (view-serve unit fix).** e3a4's own arithmetic (≤ 250 repairs/frame × 100 ns × 60 fps)
  = **0.0015 cores**, not the 0.1 the ledger hardcoded: CPU total 10.8–16.6 → **10.7–16.5
  cores**; no conclusion moves.
- **L2 (steady-state memory row).** If M1's central band holds, the shipped build at 10⁹ in
  steady state is **4.0–7.5 TB = 500–940× over 8 GB** (not the birth-state 294×), and
  build/floor = 5,100-ish/2.4 ≈ **1,700–3,100×** (not 978×). Direction unchanged: wiring,
  not physics (the wired-store rows move not at all).
- **L3 (the τ dial with both ends priced).** At measured p = 1.0 (C1–C3 re-verified) and
  ladder-measured live bytes b: τ = 8 GB/(λ·b) with λ = 3.6–4.3×10⁻⁵/B/gs →
  at b = 5,100: 43.6 gs; at b = 7,000: 31.8 gs; at HANDOFF-interlock's 1.3 KB: 171 gs.
  All-in orbit-scale arm (contacts 0.22/s + SOI): unchanged ≲ 0.02 orbit (contacts-led).

## Honest misses will be reported as misses.
