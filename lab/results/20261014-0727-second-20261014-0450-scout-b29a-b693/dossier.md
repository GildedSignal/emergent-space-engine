# Dossier — 20261014-0727-second-20261014-0450-scout-b29a-b693

## Claim

The checker's named gold experiment is done and the conditional is **discharged in the strong
direction**: with c7eb's validated encounters-tier contact (Δv_i = 2 m_j b/(|b|² v_rel), geometry
from 482 measured game-density truth encounters) as the ΔE/ΔL source, the tier's conjunction
geometry **does** deliver ΔE/ΔL as exact integers on the key's own Q48/Q32 quanta — arm B
(polar readout (r, v_r, v_t) + (d/a, v_rel/v_circ, cosψ, side, m_j), closed-form metric algebra,
**0.06 µs**) agrees with the exact refit arm at the shape grid (relk median 4.6–7.7×10⁻¹¹,
impulse-independent across **11 decades** of Δv/v, 10⁻¹⁵ → 4×10⁻⁴ median) and with the f64 truth
at the birth floor (median 5.8–7.8 quanta of max(E,L), both belts, **zero refusals and zero
plunges at every mass from 50-m rocks to Ceres**) — but the promote threshold is set by the
**store's column grid, not the kick**: the integer Δ is zero for 100 % (50-m), 90–92 % (1-Mt
ship), 78–83 % (600-m rock) of real encounters (the law call is deletable there), while at
m_crit (1.35 km) 93–98 % of encounters carry nonzero integer ΔL (median 1–2 quanta) yet the p/e
columns still do not move (column-visible only above ~5–28 km; Ceres is 99.9 % Wide) — so
sub-store-quantum influences must **accumulate** (PRINCIPLES #6), and a naive per-event scar
writes ±1-quantum glue noise instead. The σ-dependence is priced: composed refit arm
**28.5–32.7 µs cold / 70.2–71.3 µs at σ0.3** (two runs, load 1.1–4.5) = 15–21× / 6.8–8.3× under
the sticky 486–585 µs (b29a's 13× is cold-only). The darwin-domain statement is folded in and
**shrinks to a converter artifact**: the far band [16384,18432) M composes 100 % (compile 7.6 µs
= the cold band's, refit 16.8 µs, zero refusals at m_crit and Ceres) via v3 `OrbitKey::bound`
(no p cap), and the invariants-direct row→key (`darwin`'s algebra in f64 + `Key::new`; its
L ≤ 4096·2³² cap sits at p ≲ 1.7×10⁷ M — beyond every store band) agrees with v3's key to relk
3.0×10⁻¹⁰ p50: the composed promotion serves **every band the store accepts**.

## Bottleneck

Board focus 1, ask (b) (bodies 28 → 10⁹, the furthest gap): the smallest promotion between a
compact body and a live one. b29a priced the composed event on a synthetic impulse ladder; this
run re-prices it on the real contact-impulse distribution (the checker's named experiment),
which moves the answer from "the kick is the cheapest arm" to "the store's grid sets the promote
threshold": at 10⁹ quiet (3.6×10⁴ events/s), the refit arm is ~1.0–2.5 Linux cores (cold/ecc
σ-mix), while the tier-side integer filter + accumulator is ~0.002 cores with the law called
only on store-grid crossings (at m_crit, signed-walk arithmetic: one crossing per ~(300/2)² ≈
2×10⁴ encounters ≈ 3.6×10³ orbits at game density → amortized ~0.07 µs/event, a further ~400×
under the unconditional refit arm — arithmetic, not measured; the wiki's new direction 9 names
its measurement).

## Evidence

Linux/x86 shared (8 vCPU; two runs at load 1.1–1.6 and 4.5), every number regenerable:
`regen.sh` (one dumper build + one 30–90-s truth run + one bench build + one 30-s run; **the
482-encounter dump regenerates bit-identically from the shipped encounters crate**). Bench:
`crates/shipmem/examples/promo_contact.rs` (this run's patch), N = 4096 bodies/belt; belts: cold
(lab spec σ0.07, e ≤ 0.6, p ∈ [2048,4096) M Darwin Q16) and eccentric (σ0.3, e ≤ 0.9); masses
as ratios to the central mass: 6.6×10⁻²¹ (50-m rock), 5×10⁻¹⁹ (1-Mt ship), 1.3×10⁻¹⁸ (600-m),
1.3×10⁻¹⁷ (m_crit, 1.35 km — c7eb's threshold), 6.6×10⁻¹⁶ (5-km), 1.3×10⁻¹⁴ (28-km),
4.7×10⁻¹⁰ (Ceres). Impulse geometry bootstrapped per body from the 482 measured triples (d/a med
1.8×10⁻⁵, v_rel/v_circ med 0.17, cosψ bimodal: |cosψ| > 0.9 in 83 %, sign 50/50 —
shear-dominated conjunctions), scaled by each body's own a: Δv = 2 m_j/(d·v_rel) in the law's
geometric units; conjunction phase uniform (the tier's Diophantine phase is the exact input it
would supply). Deterministic fields identical across both runs; timings quoted as ranges.

- **Arm-vs-arm (the shape grid):** median 0.94–1.9×10⁴ quanta of max(k, periapsis) below
  m_crit, 8.7–1.1×10⁵ from m_crit to Ceres; relk median 4.6–7.7×10⁻¹¹; p95 ≤ 5.5×10⁵ — flat
  across 8 decades at ≥ m_crit (impulse-independent), both belts.
- **Arm-vs-truth (the invariant grid):** median 5.8–7.8 quanta of max(E Q48, L Q32) at **every**
  mass, both belts (birth floors re-measured: E 3.3 / L 6.8 cold, 4.1/5.5 ecc — b29a's 3.0/7.6
  reproduced). Zero refit refusals, zero plunges, zero `Key::new` refusals anywhere, including
  Ceres's extreme tail (Δv/v max 2.7×10⁻² — the real distribution tops out ~40× below the
  refusal regime b29a placed at Δv/v ≈ 1).
- **The integer skip predicate** (arm B's ΔE_q/ΔL_q == 0): 50-m 100 % skip, ship 90.0/92.0 %,
  600-m 77.8/82.5 %, m_crit 1.9/7.4 %, 5-km ~0, Ceres 0 (cold/ecc). At m_crit the per-event
  |ΔL| is median 2 (cold) / 1 (ecc) quanta, signed by cosψ. Store columns move only above
  ~5–28 km (ΔL_q ~ 10²–10³: p Δ 3, e Δ 19 at 28 km); a naive per-event scar writes the glue's
  own ±1-quantum p/e noise at **every** rock mass (unchanged fraction 0–1.7 % at ≤ m_crit —
  b29a's 0/4096 column identity, now shown to be the wiring's noise floor, not physics).
- **Costs (µs p50, quiet load):** cold compile 7.6 / read 3.0 / cartesian 0.35 / refit 16.5 /
  **keykick-from-geometry 0.056** / scar 0.23 → composed refit arm **28.5** (32.7 at load 4.5);
  σ0.3: compile 27.9, refit 33.1 → composed **70.2–71.3** (2.2–2.5× σ-factor; under the sticky
  486–585 µs: 15–21× cold, 6.8–8.3× ecc). `OrbitKey::from_invariants` (the (E,L)→shape inverse)
  is **311 µs — not on the store path** (it is the comparison instrument); a key-arm composition
  that routed through it would cost 328–371 µs, worse than the refit arm — the key arm's value is
  the 0.06 µs filter/accumulator, not column glue. Scar accounting: 40.00 B/event under the
  naive hot-batch growth policy (12-B payload; matches b29a's checker measurement; anchored
  wiring gives 12.07).
- **Far band [16384,18432) M:** `Key::darwin` refuses 4096/4096 (clean `Err`, the p ≤ 8192 M
  cap); v3 `OrbitKey::bound` composes 4096/4096: compile 7.1–7.6 µs (the cold band's own cost —
  no far-band penalty), refit 15.9–16.8 µs, refit OK 4096/4096 at m_crit **and** Ceres; the
  invariants-direct row→key is accepted by `Key::new` 4096/4096 and agrees with v3's bound key
  to relk p50 3.0×10⁻¹⁰ / p95 1.5×10⁻⁹ (the same floor as the two arms' mutual agreement).

Full record: `run.log` (regenerated, exit 0); dump regeneration: `dump-regen.log`
("bit-identical to the stored record").

## Predictions (`predictions.md`, written before the run)

- **P1 held** (arm-vs-arm med ≤ 3×10⁵ quanta predicted; measured ≤ 1.1×10⁵, p95 ≤ 5.5×10⁵,
  impulse-independent).
- **P2 held** (≤ 8 quanta predicted; measured 5.8–7.8 at every mass, both belts).
- **P3 held, stronger than predicted** (0 refusals everywhere; I allowed ≤ 10 % at Ceres).
- **P4 held** (cold 28.5–32.7 vs predicted 30–50; ecc 70.2–71.3 vs 60–110; the kick is not the
  tail) — with one correction P4 did not anticipate: the key arm's *composition* through
  `from_invariants` is worse than the refit arm (311 µs inverse, off the store path).
- **P5 FAILED** — the sharpest result of the run: I predicted ≥ 90 % of ≤ m_crit events leave
  the store columns unchanged; measured 0–1.7 % unchanged. The physics is sub-column below
  ~5 km, but the composed path as wired cannot see that: the refit→columns roundtrip writes
  ±1-quantum noise per event, and at m_crit the key's own integer grid (200× finer than the
  p column) already resolves 93–98 % of kicks. The store-grid-absorbs-everything reading is
  refuted as wired; the tier-side accumulator between the two grids is the correctness path,
  not an optimization.
- **P6 half-held, half-wrong in a way that strengthens the claim:** darwin 100 % clean Err and
  v3 100 % composition as predicted; but my predicted `Key::new` L-cap refusal (~100 %) was an
  arithmetic error (Newtonian L = √p ≈ 128 ≪ 4096 at p = 16384; the cap sits at p ≲ 1.7×10⁷ M,
  beyond every store band). The corrected statement is stronger: the invariants-direct row→key
  extends the key-space arm to all store bands, verified against v3 to 3.0×10⁻¹⁰.
- **P7 failed under the naive accounting** (40.00 B/event hot-batch growth vs ≤ 12.05
  predicted; the 12-B payload matches; same wiring artifact b29a's checker measured).

## What would make it wrong

1. The conjunction phase is uniform-random, not the tier's Diophantine conjunction phase:
   conjunctions cluster where orbits actually cross, so the per-event ΔL_q distribution (and
   the accumulator's crossing rate) is correlated, not i.i.d. — the arm-vs-arm floors should be
   unaffected (they are grid properties), but the ~2×10⁴-encounter crossing arithmetic is not a
   measurement (r8's quasi-periodic repeated conjunctions make kicks arrive in signed bunches).
2. The impulse approximation degrades at the slowest v_rel (co-orbital, w = 0.013 present in
   the ladder): c7eb measured 24 % agreement there (vs 0.998 median); and it is weakest exactly
   in the Ceres tail (closest d × slowest v_rel) that reaches Δv/v ~ 2.7×10⁻².
3. cosψ's side (which side the perturber passes) is randomized 50/50 — the dump records cosψ
   but not the side; real belts correlate it with the conjunction geometry.
4. Planar, prograde, one orientation, no 3-D inclination, no GR doll — the same domain hole
   b29a and the encounters page carry; now with the real impulse distribution.
5. Cloud timings (shared box); the M1 sets the real frame budget. Costs are orders of magnitude
   only. c7eb's RK4 validation of the impulse coefficient is the prior run's, not re-run here
   (the dump regenerates bit-identically, which covers the geometry but not the impulse's
   physics).

## Cost of adoption

Small and local: the encounters tier gains a per-body integer ΔE/ΔL accumulator (two i64
registers + the conjunction-geometry closed forms, ~20 lines); the law is called (b29a's
composed refit arm) only when the accumulated Δ crosses the store's column grid or the refit's
refusal regime (the promote-to-live trigger); w/t column anchoring is settled at wiring as in
b29a. No law change, no gate touched. It deletes the per-event law call for m ≲ m_crit/10
outright and amortizes it to ~0.07 µs/event at m_crit (arithmetic above).

PRINCIPLES: "The cheapest compute is compute not done" (#1 — the law call is deleted for the
sub-threshold bulk); "influences below one quantum accumulate" (#6 — the accumulator is now a
measured necessity, not an option); "we only care about changes" (#14 — the scar is the change,
and the change is what the integer Δ measures); "one mechanism at every scale" (#19 — the same
integer ΔE/ΔL serves rocks, ships and Ceres-grade flybys).

## The lens (second author)

I started from the checker's one experiment and ran it whole rather than its cheapest part; the
lens cost me one prediction written from un-derived arithmetic (the L-cap claim in P6 — √p, not
p) and it was the checker's own adversarial case that had the right far-band question. What the
second-author lens may miss: I trusted c7eb's validated coefficient wholesale (not re-validated
here), and I did not measure the accumulator's crossing rate on correlated conjunctions (left
as the wiki's direction 9) — the two places where a third run could still move the numbers.
