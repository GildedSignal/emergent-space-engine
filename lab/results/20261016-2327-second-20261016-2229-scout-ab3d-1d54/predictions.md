# Predictions (written before the decisive run)

Question: does the scout's two-stage angular certificate still close the player's in-belt
scan answer walk at the TRUE shipped operating point — near = 68 root units = 6.713×10⁻⁷ AU
(the belt branch ships `Scalar::raw(34, -10)` = 49.06-m ships, not the 12,850 km of the
silver run's misread) — with truth checks on every seed, and is it sound for querents the
player can actually fly (e < 1, not the belt's capped e ≤ 0.4)?

The fixes this run carries (the checker's named gold experiment):
1. every constant re-derived from `scenario.rs`/`encounter.rs`/`radial.rs`: root unit
   = AU/101_300_000 = 1,476.9 m (the Moon's 260,000-root periapsis = 383,990 m ✓),
   ship radius 34·2⁻¹⁰ root = 49.06 m (belt branch, doll 0; the 34·2⁸ constant is the
   same radius in Home-doll units), near = 2¹⁰·(r_a+r_b) = 68 root = 6.7127×10⁻⁷ AU;
2. truth checks on EVERY scene, every seed (the silver run checked seed 1 only);
3. the margin no longer clamps at e = 0.4: max|ν−M| has the closed form
   cos ν* = ((1−e²)^{3/4} − 1)/e, margin = ν* − M*, exact for any e < 1 — cross-checked
   against the dense grid table on (0, 0.99] (K0: closed form must dominate the grid
   table within 1e-6 everywhere; the grid table only ever underestimates the true max);
4. the series tail table extended to e ≤ 0.99 (belt bodies need ≤ 0.4; the querent enters
   stage 2 exactly, so its tail never applies), tail sound at the bin top × 1.5 as before;
5. adversarial co-located hits at querent e ∈ {0.6, 0.8, 0.95} — a belt body at periapsis
   placed exactly on the querent's position at t (truth hit by construction, d0 = 0),
   the querent at its max-margin phase, so the old clamped margin misses it by ~0.2–1.5 rad
   while the exact margin keeps it.

Numbers I expect, derived by arithmetic before running (held-out cases marked †):

1. Truth density at the true point: essentially zero — the swept area per scan is
   2·near·v_rel·h ≈ 2·6.7e-7·0.5·8.9e-4 = 6×10⁻¹⁰ AU² against a belt area density of
   6.4×10³/AU² → 3.8×10⁻⁶ expected hits per 10⁵-body scan. Prediction: 0 truth hits in
   almost every natural scene (0–1 by Poisson); 3999's ZERO encounters is then EXACT,
   not "the log froze". The silver run's "0.53%·N truth wall" describes the
   counterfactual 0.176-AU point (one labeled row keeps it on the record).
2. Keep fractions (long h = 28,141.5 s): stage 1 is margin-dominated
   (tk ≈ (π/2)·(vmax_j+vmax_q)·h/min peri ≈ 5×10⁻³ rad; margins 0.14–0.82) → keep1
   5–15% for the e=0.01 player querent, 25–38% for the e=0.39 belt querent.
   Stage 2 (series): tk-dominated → 0.15–0.35% at long h; at short h (1,000 s) the |w|h
   term shrinks 28× → 0.005–0.02%. Newton stage 2 ≈ half the series keep.
3. † Composed S(10⁵) with the shipped 4.2-µs readout: c1·N (≈ 0.3 ms) + series·k1
   (≈ 0.5–0.8 ms) + 4.2 µs·k2 (≈ 0.6–1.5 ms) → **1.4–2.6 ms, under the 6-ms bar**.
   At 10⁶: with the standing λ-index and the 0.5-µs closed-form readout,
   series·k1 ≈ 5–6 ms + readout ≈ 1 ms → **6–7 ms: marginal, just over the bar** —
   I predict the bar is MET at 10⁵ and MARGINAL (over by <1.5×) at 10⁶ on x86 costs.
4. † Costs: stage-1 λ pass 2.5–4.5 ns/candidate, series stage-2 40–55 ns, Newton
   260–280 ns (same machine class as the silver run; K3 stays 200 ns for the series).
5. † Soundness: zero missed true hits in EVERY scene (K1), including the co-located
   adversarial rows (miss must be 0 with exact margins) and the true-scale formation
   (500 bodies within near/2 of the querent: 450–500 truth hits, keep1 = 1.000).
   Under the OLD clamped table the co-located rows must show miss ≥ 1 (the fix is
   load-bearing, not decorative).
6. † Querent-e degradation (cost, not soundness): at e = 0.6 the stage-1 window grows by
   margin(0.6) = 1.2615 rad → keep1 ≈ 40–55%, stage-2 tk grows ~4× (vmax at periapsis
   8.5 AU/yr) → keep2 ≈ 0.6–1.3%; composed S(10⁵) ≈ 4.5–6.5 ms — the bar survives to
   e ≈ 0.6 and dies somewhere above it (at e = 0.95, margin 2.38 rad, keep1 ≈ 80%,
   S ≈ 25 ms: dead). The certificate degrades gracefully with querent e; that is the
   honest domain boundary, recorded not hidden.
7. † Held-out fresh seeds (5, 7): all keep fractions within ±30% of seed 1's; held-out
   10⁶ (seed 7) inside the same bands as seed 1's 10⁶.

Kill criteria, pre-registered: K0 the closed-form margin is below the grid table by more
than 1e-6 anywhere on (0, 0.99] (the derivation is wrong — the certificate stays on the
tabulated form, domain e ≤ 0.4 only); K1 any true hit rejected with exact margins (the
configuration is unsound as built); K2 composed S(10⁵) > 6 ms at the true point with the
shipped readout; K3 series stage-2 > 200 ns/candidate. A KILL kills configurations, never
the method (PRINCIPLES 9).

Free parameters fixed before looking at any miss count: the series tail is tabulated on a
dense (e, M) grid against exact Newton, widened ×1.5; ε_θ widened by 10⁻⁶ rad; the
closed-form margin widened by 10⁻⁹ rad; nothing else tuned.
