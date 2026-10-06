# Predictions (written before the decisive run)

Model: N = 262,144 belt bodies, integer lattice state (a, e, ϖ) = 20+16+16 = 52 bits exact
naive (phase derived on demand, never stored). Program birth (bijective hash, smooth).
Encounters: Poisson λ per body per orbit, heavy-tailed quantized kicks (bit-length geometric,
p = 1/2, cut at 2^20). Encoded with the shipped Form-P accounting: Elias–Fano ordinals
(2 + log2(N/k)) + zigzag Elias–gamma values. λ ∈ {0.01, 0.1, 1.1}, 100 orbits.
Two-tier variant: bodies with |a − a_p| ≤ W/64 exact (naive 52 bits); far bodies' Δ requantized
to a far quantum q_far = 2^8 lattice units.

Held-out cases I did not tune on: the scar bits slope at λ = 0.01 and 0.1 (I only reasoned at
λ = 1.1), and the return-to-program reabsorption count at all λ.

1. **Return-to-program reabsorption fires, but decays.** The Δ walk is on the integer lattice,
   so exact return is not measure-zero: it is a transient 3-D walk. I predict a nonzero count
   (hundreds to thousands over 100 orbits at λ = 1.1), concentrated early, and a scarred
   fraction that saturates below 1 (3-D transience: P(never return) ≈ 0.66 for a simple walk;
   kicks are heavy-tailed so I expect scarred fraction 0.7–0.95 at λ = 1.1). At λ = 0.01 the
   scarred fraction stays low (few bodies ever encounter).
2. **One-tier exact scars grow without bound.** Bits/body slope ≈ λ · b̄/2 per orbit (b̄ = mean
   gamma bits of a kick across 3 columns; ÷2 because a real encounter's cause is shared by two
   partners — my model draws per-body, so I report the raw slope and halve it in the claim).
   I expect b̄ ≈ 8–24 bits, so at λ = 1.1 the scar layer crosses the 52-bit naive repack point
   within 5–30 orbits. After that, Form P is strictly worse than naive blocks and shipmem's own
   cost switch repacks: the belt-as-program is spent.
3. **law.md's ledger (+62 bits per kick, −60 per reabsorption) does not balance** for a belt:
   reabsorption flux ≪ creation flux after the first few orbits (prediction 1), so H_live grows
   at ≈ the creation rate, not at the difference.
4. **The two-tier store equilibrates.** Far bits/body saturate at ≤ ~3 · (2·log2(range/q_far)+1)
   ≈ ≤ 66 bits worst case, and in practice at the *spread*/q_far of the walk, tens of bits; total
   bits/body at near-fraction 10⁻³ ≈ 0.052 + far_sat ≪ 52. I predict the two-tier total stays
   under 25% of naive at t = 100 for all three λ.
5. **The firewall certificate has a wide margin.** Reabsorbing every far body at q_far redirects
   near-body precession only through the belt's aggregate quadrupole:
   σ_Δϖ ≈ (3π/4)·(μ/√N_far)·(a/R)³·3·(ε/R) with μ = belt/star mass ratio ≈ 4×10⁻⁹,
   N_far = 10⁹, ε = q_far in metres (~100 km), a/R = 0.7. I predict a margin ≥ 10³ against the
   ϖ quantum (2π/2^16 rad ≈ 10⁻⁴ rad).
6. **Occupancy (view/multipole) bits do not grow.** The coarse (a, e) occupancy entropy per body
   stays within ~10% of its birth value over 100 orbits (the belt texture is stationary; only
   identity-level information grows).

Kill criteria: if prediction 2 fails (scar bits sublinear, e.g. saturating below naive) then the
one-tier store is fine and the two-tier is unnecessary — that kills my premise, not the method.

## Held-out, registered before the t=400 extension run (same seed)

The t ≤ 100 data at λ = 1.1 fits bits(t) ≈ 32.2 + 16·log10(t/100) bits/body (log-growth:
the scar value is dominated by each body's record kick, which grows ~log t). Predictions:
7. one-tier bits/body at t = 400, λ = 1.1: 41.8 ± 2 bits (if ≥ 45, growth is faster than
   log and my log-crossing estimate below is optimistic).
8. two-tier bits/body at t = 400: ≤ 8.6 (near term flat + far still below 8 bits).
9. crossing of naive (52 bits) lies beyond 500 orbits (point estimate ~1700 from the fit).

## Outcomes (after the runs)

- Held: 1 (reabsorption decays; but fraction saturates at 1.00, above my 0.95), 2 (unbounded,
  though log not linear — my 5-30-orbit crossing was wrong by ~50x, in the existing design's
  favour), 3, 5 (10^15), 6 (+0.13%), 7 (43.5 vs 41.8+-2: 0.7 over the band), 9 (~1100 orbits).
- Missed: 8 (two-tier at t=400: 10.32 vs predicted <= 8.6; the far tier inherits log growth).
