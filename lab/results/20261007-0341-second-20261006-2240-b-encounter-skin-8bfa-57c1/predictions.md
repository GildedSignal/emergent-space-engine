# Predictions — second author, 20261007-0341

Written after the diagnosis runs (belt 1e-6 decomposition, both modes) and BEFORE the
decisive runs (pad halving, long horizons, N=10⁴, record regeneration).

## Diagnosis already measured (not a prediction)

belt 1e-6, 16 orbits, N=1500: skin evals 4468/kick = 4429 in `sections_pad` at setup
(322 evals per setup × 13.76 amortized initial setups/kick — the 99k-certificate initial
padded scan; zero post-initial rescans at this ε) + 35 in queries + ~4 in empty re-proofs.
The HQ horizon query at setup is 3 evals/kick (dead weight, but negligible: the checker's
"padded arcs plus 100·TAU horizon queries" attribution is half wrong — it is the padded
arcs alone). always: 2921/kick all steady-state. Skin steady state ≈ 37 evals/kick.

## Predictions, held-out cases

1. **pad = s/2 at build (sound: the drift trigger fires at δ ≥ s/2, so δ < s/2 at query
   time; term 1 needs arcs at eps_u + δ_max only):** belt 1e-6 init scan evals drop by
   ≥ 1.5× (arcs 3× the tolerance instead of 5×; fewer arcs cross the 0.2 rad Wide
   threshold). Exactness holds: 0 missed / 0 false on belt 1e-8/1e-6/1e-4, ring, fleet,
   and `cargo test` 7/7. If `exact_at_kick_eps_1e4` fails, pad = s/2 is refuted at large
   kicks and I revert to s.
2. **Long horizons (the amortization the 16-orbit harness hides):** skin total evals/kick
   falls ≈ init/(kicks) with horizon; at 64 orbits ≤ 1200/kick, at 256 orbits ≤ 350/kick;
   always stays 2900–3000/kick at every horizon. Skin crosses below always between 32
   and 64 orbits, and is ≥ 8× below at 256 orbits. Per-kick wall (p50/p95/p99, advance
   only) skin < always at every horizon ≥ 16.
3. **Trig resets stay rare at 1e-6 out to 256 orbits** (drift/kick ~1e-6 ≪ s/2 = 2e-4):
   trig/kick < 1 at 256 orbits. At 1e-4 they fire as before (~37/kick).
4. **N = 10⁴ (8 orbits, no truth — exactness is carried by the tests and the N=1500
   matchups):** both modes' evals/kick stay within 2× of their N=1500 values (fixed
   density); the skin's cert store scales ~linearly: ~660k certs, ~310 MB estimated —
   reported, and named as the adoption cost it is.
5. **Record regeneration:** the shipped bin reproduces belt 1e-4 as 0/0 of 73 (it did in
   the pre-prediction baseline run); all stored raw lines regenerate bit-for-bit in
   counters (wall varies with load).

## Falsifiers (pre-registered)

- Any miss/false at any ε or case with pad = s/2 → refuted, revert, report.
- Skin total evals/kick at 256 orbits > always's → the amortization story is wrong; the
  honest result is then "the inversion is real and the skin needs a cheaper initial scan",
  a clean refutation of the gold claim.
- Steady-state (post-init) skin evals/kick > 300 at any horizon at 1e-6 → same.
