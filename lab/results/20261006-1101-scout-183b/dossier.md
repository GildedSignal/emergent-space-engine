# dossier.md — rung 20261006-1101-scout-183b (scout lens)

**Claim.** The memory floor of a real, stirred belt saturates: a scar is a
bounded state-delta (not an event log), it plateaus at ≈ one 32-bit key word
(~35 bits incl. index) per scarred body after ~25 distinguishable encounters,
so 10⁹ bodies fit in 8 GB for any belt-beside-a-secondary scene —
bits/body ≈ 0.13 (program) + f_x × 35, with f_x the geometric crossing
fraction (conjunction distance ≲ 3 r_H of a massive secondary).

## Bottleneck

Focus item 5: "fitting 10⁹ in 8 GB (crates/shipmem: population programs plus
scars), decided by distinctions created per game-second" — plane.md line 36
says this "decides whether a billion bodies fit"; B18 gates bytes/body against
"the measured information floor", which existed only for the program half
(components-98bc, 0.126 bits/body). Gain: the floor becomes a computable law
(no event-log storage, no periodic refit/reabsorption machinery — saturation
is the reabsorption); ~250× headroom shown at 10⁹ for the worst case.

## Evidence (commands, each ≤ 60 s; Linux x86, 8 vCPU shared, numpy 1.26.4)

Scene: belt a ∈ [0.95, 1.05] AU, Rayleigh e (σ_e), star 1 M☉, one secondary
(m_p at a_p), impulse kicks at solved synodic conjunctions, kicks quantized on
the doll's 32-bit (E, L) key grid — a kick below one quantum is no scar.
`scar_floor.py` (static/ergodic sampler, N = 5×10⁴ × 32 conjunctions, 12 s);
`chain.py` (chained: each kick updates the state that meets the next
conjunction, 4×10³ bodies × 400 steps, 11 s). All commands:
`python3 scar_floor.py cfg_cN.json out_cN.json`, `python3 chain.py cfg_cN.json out_cN.json`.

| config | secondary | rate /body/orbit | frac hit | chained result |
|---|---|---|---|---|
| C1 | 10⁻³ @ 1.15 (belt inside 1.3–2.5 r_H) | 0.160 | 0.998 | C7: saturates, log₂\|Δkey\| 33.79→33.84 flat over last 112 steps, H(delta) flat 3.9 bits, 0 escapes |
| C2 | 10⁻³ @ 1.30 (edge 2.8–3.9 r_H) | 0.072 | 0.73 | C8: scarred fraction freezes at 0.734 (protected interior never scars), Δ 33.1 bits stable |
| C3 | 10⁻³ @ 1.60 (> 4.5 r_H) | **0 exactly** | 0 | — (program only: 0.126 bits/body) |
| C4 | 10⁻⁵ @ 1.15 | 9×10⁻⁴ | 0.11 | — |
| C5 | σ_e 0.02, else C1 | 0.189 (C1 × 1.18) | 1.0 | — |
| C6 | C1 at N = 10⁴ | 0.161 (Δ 0.7%) | | N-independent |

- Every encounter is distinguishable at q ∈ {24…36}-bit grids (scar_frac =
  1.0; median ΔE/E = 0.08–0.14 ≫ quantum). The quantum threshold bites only
  ship–ship gravity: 10⁶ kg ships give < 0.02 key units at 1 km (never a
  scar); ≳ 10⁸–10⁹ kg aggregates at km range do scar (out_*.json
  `ship_ship_control`).
- Record sizes: first scar ≈ 17.6 bits (H(Δkey_E) 4.76 + H(Δkey_L) 4.81 +
  ~8 timing proxy); repeat kicks are correlated (lag-1 autocorr +0.32, C2
  −0.03; conditional entropy 2.1 bits) — transient growth ≈ 4–5 bits per
  distinguishable encounter, matching H0173's ~4 bits/collision on the lattice.
- Floor: worst case (f_x = 1, whole belt in the chaotic zone): 0.13 + 35 ≈
  **35 bits/body ≈ 4.4 GB at 10⁹ < 8 GB**. Realistic edge (C8): **≈ 26
  bits/body ≈ 3.2 GB**. Protected belt (C3): **0.13 bits/body = 16 MB**.
- The static sampler overestimates long-run rates 9× (C7 chained rate 0.018/or
  vs C1 static 0.160): real kicks break the quasi-periodic conjunction lock —
  the scar process self-limits in time as well as in size.

## Predictions (predictions.md, written before C2–C8)

Hit: C3 exactly zero; C5 within 20% (×1.18); C6 within 5% (0.7%); ship–ship.
Missed: C2 rate 15× low and C4 15–50× high — one error twice: I conflated
orbit-crossing with conjunction radial distance (conjunction d ≈ Δa can be
< 3 r_H with no crossing). Failed and became a finding: Poisson dispersion
(var/mean = 5.15, predicted 0.8–1.3) — encounters cluster on bodies through
quasi-periodic locks, so per-body counts are not Poisson and the event-log
cost model is the wrong model; the chained saturation measurement replaces it.

## What would make it wrong; adoption cost; PRINCIPLES

- Wrong if: secular resonances (not modelled) pump e and enlarge f_x without
  conjunctions (Kirkwood-style); the impulse approximation inside ~0.5 r_H
  (kicks bigger → faster saturation, same floor); multi-secondary overlap
  (f_x sums bands; measured only for one); self-stirring (negligible here:
  ship–ship gravity is below one quantum — verified). The 0.126-bit program
  term is components-98bc's measured number, quoted not re-measured.
- Adoption: near zero. law.md's store already is program + scars; what is
  deleted is any event-log/refit machinery: reabsorption is the delta's own
  saturation. B18's floor becomes computable at birth from geometry:
  floor = 0.13 + f_x × 35 bits/body, f_x = Σ chaotic-zone widths / belt width.
  The allocator's H_live read is a geometric quantity (f_x), not a rate.
- PRINCIPLES: #24 "The memory floor is information theory" — now measured;
  #6 "Store the generator, not the generated" — the scar is a state delta
  against the generator; #13/#16 — information, like error, does not compound:
  it saturates at one key word; below one quantum is not a distinction
  ("the floor is what the player can differentiate").

## The lens (what scout may have missed)

Cross-field law over engine-native detail: the real tube key is a quantized
(E, L) memo with per-band fixed point, not my uniform E-span/2³² grid; the
real Δt_p field is 64-bit and may carry more timing entropy than my ~8-bit
proxy (floor shifts up a few bits, saturation unchanged); single-scene, 2D,
e_p = 0; the co-orbital formation regime (this morning's gold) is contact- and
decision-driven (H0173's regime), not measured here. Reported rates are
orders of magnitude for Linux x86; the M1 re-measures.
