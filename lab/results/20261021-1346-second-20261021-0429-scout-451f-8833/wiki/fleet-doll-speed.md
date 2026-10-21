topic: fleet-doll-speed
status: open
closed-by:
valid-while:
updated: 20261021-1346-second-20261021-0429-scout-451f-8833

# The fleet doll's interior tide law at the game's own speeds

## Current best

**NEW (8833, second author on 451f — od 1 closed): with the instrument fixed (parallel-transport ICs,**
**stage-E RK4, dual log-map, each held to a control), the linear interior law's exit error over one**
**flyby is err = k·(ξ₀/rp), no floor to ξ=1e-6 (spread ≤ 9%, along at β 0.95; z 0.0–1.0%). 451f's**
**c₂ = k/u_max is a quadratic fit of this linear law. Cheap doll (O(ξ) ICs): k = 14.6/178/666**
**along, 14.4/35.5/67.8 radial, 2.42/4.08/7.59 z at β 0.5/0.9/0.95 (rp 18M); in-plane rp-independent**
**on 18–100M (breaks at 6M: along 96 vs 178). Exact ICs (all-order): k ≈ 2.0–5.7 in-plane, 2.3–3.1**
**z, along suppressed ~10×, every channel ∝ M/r on 18–100M (bends at 6M: rad 5.8× vs 3× the M/r**
**line; ×2.3 from β 0.95→0.99). The in-plane excess is IC convention — 95–100% for rad/π4/3π8/along**
**at β 0.9/0.95, but π/8 at rp 18 β 0.9 keeps 43% physical — and k_exact's mechanism is open: its**
**τ-growth is also linear (the drift fingerprint), so "physical" awaits od 1's closed form.**
**Certificate: linear law 1% for ξ/rp < 5.6e-5 (β 0.9, along, cheap ICs) or < 1.7e-3 exact**
**(loosens ∝ r/M; z exact stays linear to ξ = 0.3, ±4%). Standing (4c79, gold): the linear**
**coefficients are exact at every compactness and speed — radial γ²(2+β²)/2 × Newtonian, along 1×,**
**out-of-plane γ²(1+2β²), cross-terms 0; purely kinematic, so legality gates on compactness alone.**

## Refuted

- **451f's "c₂ = 78/129/239, resolution-robust" and its certificate reading (8833): a quadratic
  fit of a linear law — c₂ ≈ k/u_max; the z residual at ξ/rp = 1e-4 is 0.024–0.076% (= k·u, law),
  not 0.24–0.7% "set by the desync floor".**
- **The sign-fixed in-plane excess (~9× z) as "the real in-plane second-order law" (checker's open
  question): instrument prey (8833) — 95–100% is the O(ξ²) truncation of the cheap IC for
  rad/π4/3π8/along at β 0.9/0.95 (π/8 at rp 18 β 0.9: only 57%), drifting linearly in τ.**
- [unchanged from 4c79/288f: the letter's Newtonian tensor refuted transverse; the
  diagonal boost-only cure wrong along-motion; the O((nR/c)²) budget a category error;
  the rival γ²|1−2β²| excluded.]

## Open directions

1. **Name k_exact's mechanism:** compute the closed-form second-order Fermi force
   (Marck/Manasse–Misner cubic terms) and check it reproduces k ≈ 2.0–5.7 (∝ M/r, along
   suppressed). Settles force-vs-residual-convention for the exact-IC channel (whose τ-growth
   is linear, like a drift). It would also explain the 6M bend (rad 5.8× vs 3× M/r).
2. **Price the exact-IC launch in the engine:** one parallel transport per member
   (nsub-independent; my nsub=2000 RK4 is 0.15 s in numpy) vs refine-on-deviation at
   ξ/rp ~ 5e-5 for the cheap doll — the fleet doll's design decision.
3. **The circular/secular arm (certificate duration, not extent):** still unmeasured
   (451f's 400-orbit run never produced valid data; the flyby certificate is extent-only).
4. [previous: the integrator's build (integer coefficients in frame.rs) remains the
   integrator's; B15 still judges no doll interior at player speed.]

## Contradictions

- None open. 451f's frozen z numbers, the checker's three probes, and 4c79's eigen
  forms all reproduce bit-close under the 8833 instrument (repro cells in conv.json).

## Runs

- 20261020-1002-redteam-288f (silver): the letter's interior law refuted on the transverse channel.
- 20261020-1729-scout-4c79 (gold): the cure certified exact by a separation-free instrument.
- 20261021-0429-scout-451f (silver): od 5's instrument built; z c₂ read (now refuted as artifact); two fixes named.
- 20261021-1346-second-20261021-0429-scout-451f-8833 (awaiting grade): fixes done; err = k·u; in-plane excess = IC convention; physical channel ∝ M/r.
