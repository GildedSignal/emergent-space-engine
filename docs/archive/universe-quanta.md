# Universe quanta: floors, Q and the energy quantum

Status: adopted 26 September 2026 (Julien: "proceed" on the recommendation below). Evidence: H0170 (tick length), H0173 (probes), H0174 (law v1).

## One floor, no ruler

The engine needs exactly one kind of floor: the canonical grid that stored state is rounded to after every interaction. It needs no ruler (no uniform tick loop, no fixed spatial pixel that everything pays for), and no floor needs a physical meaning.

- **Why a floor is unavoidable.** Determinism plus finite memory means every interaction's result must be stored in finite bits. Exact storage grows without bound (contact times involve square roots, and each collision composes them), so the state has to be rounded, and bits that are rounded away cannot be recovered later.
- **Why refinement cannot replace it.** Chaos spends precision fast. In the lattice gas a one-quantum difference grows about 4 bits per collision, reaches a ship's radius after 14–17 collisions per ship, and gives half the gas a different history after about 43. Ten extra bits buy about 2.6 collisions of shared history (H0173). "Refine until outcomes agree" works for a *computation* on exact inputs, never for a *history*: after a few collisions the outcome depends on bits that exist nowhere.
- **Why the floor loses nothing real.** The rounded history is an exact history of the lattice law, with exact conservation through the carries. No finite machine could keep the continuous history past about 15 collisions anyway.
- **Where adaptivity belongs.** Computation adapts. The event core pays per event, not per chronon (H0170). Predicates are exact integers, and a float filter may decide them when its error bound allows, with an exact fallback. The *state* grid is uniform and fine. A refinement rule for state would become part of the law, and it could never depend on observation or scheduling.
- **Stopping rules.** A refinement stopped by wall-time budget would make the universe depend on the machine's temperature (about 30% thermal swing on the M1). Every stopping rule must be a fixed function of the state.

## Q is a coherence time

Light moves Q position quanta per chronon, so the velocity quantum is c/Q: Q counts the distinguishable speeds between rest and c, independently of the chronon's length.

- Coasting is exact integer motion. Rounding happens only at interactions (collisions, thrust, and later gravity events), and leaves a velocity error of at most c/Q.
- After a coast of duration T, the position error is c·T/Q.
- The tolerance is one light-chronon, by the chronon's own definition: 5% of the smallest object, a 50 cm missile, gives c·δt = 2.5 cm and δt ≈ 83 ps.
- A coast therefore stays within tolerance while T ≤ Q·δt, which gives:

**Q = T_coherence / δt**: the longest unguided coast, in chronons, that must land within 2.5 cm of where exact physics would put it.

| Q | Velocity quantum | Coherence Q·δt |
|---|---|---|
| 2^20 (today's range) | 286 m/s | 87 µs |
| 2^32 | 7 cm/s | 0.36 s |
| 2^36 | 4.4 mm/s | 5.7 s |
| **2^40 (target)** | **0.27 mm/s** | **91 s** |
| 2^44 | 17 µm/s | 24 min |

**Target: Q = 2^40.**
- 91 s of coherence covers an unguided slug crossing a 1,000 km battle at 10 km/s, or a docking coast. 0.27 mm/s is finer than any docking needs.
- Earth-orbit speeds span 10⁸ quanta. Mercury's relativistic precession, about 5×10⁻⁷ rad per orbit, is resolvable within one orbit.
- The carries should keep repeated rounding bounded instead of random-walking, so Q covers one coast between corrections, not a whole voyage. This is to be verified once gravity events exist.

## Widths

Absolute positions need log2(span / 2.5 cm) + log2 Q bits.

| Item | Bits at Q = 2^40 |
|---|---|
| Galaxy (10²¹ m) | 115 (i128 holds it with 13 bits, about 8,000×, to spare) |
| Region-relative i64 coordinates | 2^23 light-chronons, about 210 km |
| Speeds (\|k\| < 2^40) | i64 |
| 10 Gyr | 2^92 chronons |

Cost is stepwise in word width (32 → 64 → 128 → 256 bits), not smooth in Q.

- **Collision predicates:** for missile-scale bodies they fit i128 up to about Q = 2^36 at 30 km/s. At Q = 2^40 they need 256-bit products, or a float filter with an exact fallback, which the Metal kernel already uses.
- **Near-c contacts:** always need the wide path. They are rare, and checked arithmetic makes only them pay.
- **Metal's dense path:** needs 64-bit cell-relative positions (32-bit today).

## The energy quantum must match the velocity quantum

`es-lattice-relativistic-v0` floors Γ = ⌊F·Q/√(Q²−|k|²)⌋ (F = 2^16) before multiplying by Q. Γ = F for every speed below √(2/F)·c ≈ 0.0055c (1,650 km/s), so v0's energy ledger cannot see kinetic energy there. A gas at 0.001c drifts 2.9×10⁻³ in kinetic energy over 31 collisions per ship, with its energy carry at exactly 0 (H0173). Everything in a solar system moves slower than that.

**v1 (`es-lattice-relativistic-v1`, H0174)** keeps v0's reflection, candidates and carries, and changes only the fixed-point 4-momentum, per unit mass:

E = ⌊2Q³/√(Q²−|k|²)⌋ = ⌊2Q²γ⌋,  p_c = sgn(k_c)·⌊2Q²|k_c|/√(Q²−|k|²)⌋ = sgn(k_c)·⌊2Qγ|k_c|⌋.

The scale is 2Q, and each floor is taken after the products. Since 2Q²γ = 2Q² + |k|² + 3|k|⁴/(4Q²) + …:
- E = m(2Q² + |k|²) exactly while 3|k|⁴ < 4Q²; that is the Newtonian energy m|k|² above the rest energy;
- p = 2Q·m·k exactly while |k_c|·|k|² < Q;
- above that, relativistic corrections enter as whole units.

At Q = 2^20 everything fits u128/i128 (4Q⁶ = 2^122). At Q = 2^40, E reaches about 2^97·γ, which needs the wide path at high γ.

## Staging

1. **Done (H0174):** law v1 at today's ranges (Q ≤ 2^20), checked against an independent reference, with every mode bit-identical.
2. **Wider ranges:** Q ≤ 2^40 and region-local coordinates up to 2^62, with filtered predicates (f64 filter, exact 256-bit fallback) and a wide v1 energy. Metal ports the v1 bounce and gets 64-bit cell-relative positions.
3. **Wide origins:** i128 region origins, with narrow local arithmetic inside regions. This is the galaxy track's G2/G3 rungs.
4. **Ladder v7:** law v1, a realistic-scale track, the galaxy cluster track (G1 fits today's range; G2/G3 fail with a machine-readable range result until stage 3), and the regions mode.

## Open

- The coherence target (91 s at Q = 2^40) is a game-design choice: "hours" would mean Q = 2^46 and i64 regions of about 3 km.
- Whether the carries keep guided and gravitational motion bounded has to be measured once gravity lands.
- The Newtonian law (`es-lattice-elastic-v0`) stays for laboratory comparisons. It is not the universe's law, because it lets bodies exceed c.
