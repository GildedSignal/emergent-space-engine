# Predictions (written before the decisive runs)

Question: does H_live — live distinguishing bits per game-second, net of the light-cone
reabsorption the plane already runs (`prune`, keep = 2·d(body, player) + 2²⁶ ticks) — admit
10⁹ bodies in 8 GB, measured on the shipped plane (`crates/universe` at 70f27a9)?

Not tuned on (I have not run the probe yet; sizes and rates are Fermi estimates from the
source: `size_of` guesses, H0190's 32 kicks/orbit, prune's keep rule, TICK_SECONDS = 4.925 µs).

1. **Widths.** `size_of::<Segment>()` lands in 96–144 B; `size_of::<BodyRec>()` in 240–330 B
   (Binding + carry + proper + plan Vec + Option<Thrust> + Option<Ext> + counters).
2. **The flown plane (30 s of game time, members 48):** `bytes_per_body` ≈ 300–450 B, of which
   history segments are < 10%; the fleet members (lattice bodies) are not in that number.
3. **Where the bits are created.** Per-body event rate ≈ 32/orbit (H0190). At 1 AU
   (period ≈ 1 yr) that is ~1e-6 events/body/s; retention ≈ 2·(1 AU/c) + 331 s ≈ 1,330 s of
   game time, so a steady-state belt body holds ≈ 1.4e-3 segments ≈ 0.2 B of live history:
   **history is not the binding term at belt scale; the per-body record itself is.**
4. **Catalogue.** Bodies on the same orbit (same shape) share one compiled Entry; distinct
   radii do not. A belt of N distinct radii grows `catalogue_live` ≈ linearly in N, each Entry
   ~0.5–3 KB (a Cycle's knots), so at N = 2,000 the catalogue is 1–6 MB.
5. **The 10⁹ verdict (extrapolated, wide-separation belt):** records ≈ 280 GB, catalogue up to
   TBs if radii are distinct, history < 1 GB/h. So at today's widths 10⁹ misses 8 GB by ~35×
   on the record width alone, and the miss is *not* the creation rate — it is the stored width
   per body and per distinct orbit. If the measurement instead shows history or plan growth
   dominating (rate × retention × width > record), prediction 3 is wrong and that is the result.
6. **Idiot index.** Live record ≈ 280 B/body against the representation floor (12–16 B for an
   individual in a doll, §4 of representation.md) gives ≈ 20×; a segment ≈ 112 B against its
   law-native content (the fit's remainder + kick + times ≈ 24–40 B) gives ≈ 3–4×.

What would make each wrong: (1–2) size_of outside the ranges or history > 10% on the flown
plane; (3) measured kicks/body/s ≫ 1e-6 at 1 AU or retention ≫ 1,330 s; (4) catalogue_live
growing sublinearly with distinct radii (sharing I did not see) or per-Entry < 0.5 KB;
(5) history/catalogue terms overtaking records at belt scale.
