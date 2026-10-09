# Predictions — second-author run 20261009-1259-...-154a

Written before running `inversion2 a|b` (the decisive experiment). Prior knowledge used:
the checker's attack measurements on its own code (H1 0.0 miss, E1 50.0%, rank* 10, E1-seed13
43.3%/12, M1 6.4%/120, M1-seed11 7.0%/13) — reproducing those with independent code is
confirmation, not held-out. The held-out cases are marked **[H]**; they were never measured
by anyone.

Mechanism used for the held-out calls: in a clump where λ-order is (near-)frozen, tangential
contact requires the equation-of-center (EoC) offsets to cancel the mean-longitude gap, so the
partner's mean-λ gap at contact is bounded by the *differential* epicycle scale (bunched ϖ:
~2|Δe|) or the *total* scale (random ϖ: ~2(e_i+e_j)) — never by 2ae/ρ. The watch bound is
therefore e-scale vs longitude spacing (2π/n), not 2ae/ρ. The gold fleet (e~1e-3, n=300,
spacing 0.021) sits ~5× below one spacing even at total scale; E1 (σ_e=1e-2) reaches 2–5
spacings.

## Mode a

- **H1 refresh** (rebuild-on-overtakes = λ(t) rank at closest approach): miss@k4 = 0 events,
  rank_lam_star = 4. The first author's 71.8%-of-pairs / 50.3%-of-events number was a frozen-t0
  watch the gold never specified. Refresh cost: crossings ≈ 4×10² over 500 orbits (< 1/orbit).
- **E1 refresh**: order frozen (0 crossings), refresh is a no-op: miss@k4 ≈ 50% of events
  (45–55%), rank_lam_star ≈ 10 (8–12).
- **E1b (seed 13)**: miss@k4 ≈ 43% (35–50%), rank_lam_star ≈ 12.
- **E2**: miss@k4 ≤ 10% of events, rank_lam_star ≤ 8.
- **[H] E3 (E1 with ϖ bunched ±0.1)**: bunching shrinks the contact-pinned gap from ~2Σe to
  ~2|Δe| but does not remove it (equal periods ⇒ gap frozen, contact still needs the Δe vector
  to cancel it). Predict: 10% < miss@k4 < 50%, rank_lam_star between 5 and 12, crossings = 0.
  (If ϖ coherence categorically saves the watch, miss@k4 ≈ 0 and rank* ≤ 4 — that would confirm
  the checker's sharpening instead.)
- **[H] oracle rank_d on a-scenes**: d_rank_over4 = 0 on C1/H1/E1/E2/E3/E1b — the gold's
  measured quantity (distance-rank at closest approach) holds on scenes where its watch fails.

## Mode b

- **[H] G1 (gold fleet replica, ρ=1e-4, H=100)**: enc between 60 and 600; rank_lam_star ≤ 4,
  miss@k4 = 0; rank_d_star ≤ 4 (the gold's oracle, reproduced by an independent harness).
- **[H] G1b (gold fleet, random ϖ)**: e-scale ≪ spacing (4e ≈ 4e-3 vs 0.021) ⇒ predict
  rank_lam_star ≤ 4, miss@k4 = 0. This refutes "ϖ coherence" as the binding scalar if it
  holds; if G1b misses (rank* > 4), the checker's sharpening is confirmed and mine is wrong.
- **[H] G1c (gold fleet, e×10 = Rayleigh(1e-2), bunched ϖ, 2ae/ρ = 200)**: if 2ae/ρ were the
  binding scalar this scene would miss worse than E1 (ratio 200 vs 20); by the e-vs-spacing
  mechanism the bunched-ϖ gap ~2|Δe| reaches ~2–4 spacings ⇒ predict 0% < miss@k4 < 50%,
  rank_lam_star between 4 and 16, i.e. strictly between G1 and E1, and *less* than E1 despite
  10× the 2ae/ρ.
- **M1 refresh**: miss@k4 ≈ 6–7% of events, rank_lam_star ≈ 120 (order 60–180); ≥ 90% of
  missed events are fleet×rogue (cross); cone covers cross encounters 542/542 and all
  radially-overlapping cross pairs 6000/6000 (reproduces the original record); refresh cost
  crossings ≈ 1.5×10⁵ over 50 orbits (≈ 3×10³/orbit ≈ 10 per body per orbit, O(1) each —
  the watch stays O(n·k) + O(crossings)).
- **M1b (rogue seed 11)**: miss@k4 ≈ 7%, rank_lam_star ≈ 13.
- **[H] oracle rank_d on M1**: d_rank_over4 = 0 (rogue at contact is within ρ ⇒ it is among
  the nearest by true distance; the oracle holds where the watch fails).

## Kill criteria for my own mechanism story

- If G1b misses at k=4: ϖ coherence is binding, my e-vs-spacing story is wrong as stated.
- If G1c misses more than E1: 2ae/ρ is binding after all, both my story and the corrected
  claim's ϖ framing are wrong.
- If E3 misses zero: bunching is a categorical saver (checker's sharpening, stronger form).
- If rank_d exceeds 4 anywhere in E1/M1-cross: the gold's oracle measurement is also
  scene-bound — a stronger refutation than claimed.
