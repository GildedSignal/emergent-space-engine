# Requirements: H_live (the scar floor) of a stirred belt — rung 20261006-1101-scout-183b

## The question, one sentence

What is the rate and the bit-cost of live distinctions (scars) that real orbital
encounters create per body per orbit in a belt stirred by a massive secondary —
the number plane.md line 36 says "decides whether a billion bodies fit" and B18
needs as "the measured information floor" — and at what density/quantum does it
break the 8 GB budget?

## Why this, why now (scout lens)

- Focus list: "fitting 10⁹ in 8 GB (crates/shipmem: population programs plus
  scars ...), decided by distinctions created per game-second". Unmeasured.
- law.md state §: populations = program + sparse scars (Elias–Fano), allocator
  reads H_live. The program half is measured (components-98bc: 0.126 bits/body,
  gold). The scar half has **no number anywhere** (HISTORY checked: only H0173's
  "about 4 bits per collision" for lattice-gas contacts, a different regime).
- B18 gates bytes/body ≤ 2× the measured floor + 2 B. Without a scar-floor
  measurement the gate cannot be evaluated for any stirred population.

## Requirements as numbers

| Requirement | Number | Tie to PRINCIPLES |
|---|---|---|
| Bodies | 10⁹ (report per-body; simulate 2×10⁵) | goal |
| Memory wall | 8 GB total ⇒ 64 bits/body absolute; target ≤ 32 for shipmem (engine takes the rest) | #24 "the memory floor is information" |
| Every body real | no averaging, ever; scars are exact integer deltas | #6 store the generator; #33 aggregates only below significance |
| Exactness | scars = integer deltas on the law's grid (32-bit key words); a kick below one quantum creates **zero** scar | #16 discrete by design; Julien: "the floor is what the player can differentiate" |
| Regeneration | bit-identical under any order (B18b(1)) | determinism |
| Test cost | ≤ 60 s, ≤ 2 GB | AGENTS |

## Stolen structure (sources checked)

1. **CRAM** (reference-based compression; CRAM 3.1, Bioinformatics 38(6),
   PMC8896640): store only differences against a shared reference = program +
   scars. Already law.md's design; the *rate* of differences is what I measure.
2. **Planetesimal stirring** (Ida 1990 Icarus 88; Greenberg et al. 1978;
   Wisdom's chaotic zone Δa_c ≈ 1.3–1.5 μ^(2/3) a for a secondary): synodic
   conjunction rate, impulse Δv = 2Gm_p/(b·v_rel), coherent distant kicks vs
   chaotic close kicks. UNVERIFIED constants: I measure them instead.

## Fermi estimate (before any run)

Belt a∈[0.95,1.05] AU, σ_e=0.05, star 1 M☉, secondary m_p=10⁻³ M☉ at a_p=1.6 AU
(r_H,p ≈ 0.11 AU). Synodic conjunctions per orbit for edge body: ~0.5.
Close-encounter probability per conjunction (b < 3 r_H): ~0.1–0.5 for bodies
with Δa ≲ 3 r_H, ~0 beyond. Impulse at b ≈ r_H: Δv/v_K ~ 10⁻³–10⁻² ⇒ ΔE/E ~
10⁻²: **far above any 32-bit-grid quantum** ⇒ every close encounter scars.
Distant conjunctions (Δa > 3 r_H): Δv/v ~ 10⁻³ × (3 r_H/Δa)² — near the finest
plausible quanta, and quasi-periodic (r8 v2: conjunction miss distances are
quasi-periodic) ⇒ compressible/absorbable.
Ship–ship (10⁶ kg at km ranges): Δv/v_K < 10⁻⁶ ⇒ zero scars at any playable
quantum; only lattice contacts scar (H0173's 4 bits/collision).

**Fermi verdict preview:** the scar load of a belt is set by the chaotic-zone
band (width ~4 r_H per massive secondary) and by the quantum only at its edge;
a 0.1-AU belt beside a Jupiter sits fully inside it, so the interesting number
is bits/body at horizons 10²–10⁴ orbits.

## What would make the 10⁹ fit fail

Scar bits/body(T) = scar_rate × record_bits × T_active exceeding 32. Records:
sparse index (Elias–Fano ~ log₂(N/S)+1.6) + quantized deltas (Δkey_E, Δkey_L,
Δt_p). If repeat kicks on the same body are uncorrelated, deltas random-walk and
each adds bits; if quasi-periodic (coherent regime), they compress.
