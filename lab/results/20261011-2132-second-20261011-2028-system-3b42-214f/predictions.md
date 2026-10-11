# Predictions (written before the decisive run)

The checker's two named experiments, run from the original's own script (extended, saved as
`work/second_lattice.rs`, wired as `crates/encounters/examples/second_lattice.rs`):

1. **Freeze the straggler rule and measure it** on `narrow-adversarial`-like bands.
2. **The key order on a strong-field belt where U(L) turns.**

The frozen straggler rule (no per-body state; every constant from the key cell = the memo entry):

- Certificate: within a key cell, a body's candidate partners are those within **mean-longitude
  arc W** at the epoch, in the tube store's own phase order, where
  `W = 1.5·(4·e_hi + 3·e_hi²) + dn_cell·t_end` (capped at π).
  Derivation: two same-key bodies can only meet near a shared true longitude θ, where their mean
  longitudes differ by ≤ 2(e_i+e_j) + O(e²) (equation of centre); unwound to the epoch by shear,
  |λ_j(0)−λ_i(0)| ≤ 4e_hi·1.5(cover e²) + dn·t_end. A rank-k tier is only this window's
  uniform-density shadow — members can cluster, so rank-k alone is NOT sound (found on the smoke
  run at 4 orbits: a rank-3 event inside a sound arc window). The window is what the phase-sorted
  store serves natively.
- The birth-fixed branch: keys with one integer period (equal-period-keys) have dn = 0 exactly,
  the λ(0) order is permanent, so the window has no closure term and is paid once at key entry.

Cases I have NOT tuned on (the smoke run used 4 orbits, not the decisive 20; no 20-orbit
straggler or strong-field-belt number has been seen):

1. **Soundness.** `misses = 0` on every straggler line (narrow-adversarial n ∈ {400,800,1600,3200}
   at two quanta: engine nca=1, closure-matched nca=16; equal-period-keys n ∈ {300,600,1200}).
   Margin instrument `arc_over_w_max < 1` everywhere (if ≥ 1 the derivation leaks and the claim dies).
2. **Negative control.** The window without the closure term (`misses_nocl`) misses on the
   narrow band at 20 orbits for n ≥ 800 (closure-dominated events exist). If it also holds with 0
   misses, the closure term is dead weight and the rule is mis-derived.
3. **Scaling (the checker's question).** Same-key candidates per real encounter
   (`cand_per_enc`) is constant in n within ±40% at each dial (both candidates and encounters
   grow ∝ n² at fixed distribution), and the window beats all-pairs by 2–5× at dial A, more at
   dial B and on equal-period keys. If `cand_per_enc` grows ∝ n, the straggler tier is quadratic
   per encounter and the claim dies.
4. **Rank shadow.** `kappa_req` (worst (rank+1)/m over events) constant in n within ±40%,
   ≈ 0.04–0.12 on the narrow band (the checker measured 0.0575 at n=400/800).
5. **Strong-field U(L).** Across the bound strong-field domain (200 E-columns × 512 L-steps,
   E ∈ [~0.95, 1), L from L_sep to L_circ): `u_turn_cols = 0` — U(L)|E is monotone (decreasing)
   through the separatrix-adjacent region (pre-registered from the sweep prototype with
   residual-checked cubic roots; the dossier's "U(L) can turn" was conjecture). If turns > 0,
   the naive L-window scan's miss count decides whether the memo table's turning points are needed.
6. **Strong-field zero-miss.** On the (E,L)-quantized lattice (64×256, per-cell constants
   compiled on a 5×5 sub-grid clipped to the bound domain): `cell_violations = 0` (the compile
   covers every member), `missed = 0` (radial zero-miss vs the exact per-body tier), inflation
   ≤ 1.3, `naive_miss = 0` (the Newtonian contiguity scan stays complete) and the Newtonian
   control line also `naive_miss = 0`.

Kill criteria: any miss in (1) kills the frozen rule; `arc_over_w_max ≥ 1` kills the bound;
`cand_per_enc` not constant in n kills the scaling claim; `missed > 0` or `cell_violations > 0`
in (6) kills the conservative strong-field compile.

Post-script (record hygiene): the straggler matrix was first run strictly after this file was
written. The strong-field mode had one earlier identical-seed run before this file existed (its
numbers were already seen), so predictions (5) and (6) are confirmations, not held out.
