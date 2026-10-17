# predictions — 20261017-2142-second-…-e1a4 (second author on scout-8dfb)

Written BEFORE the decisive instrument run. Context: the J(n|m) = Pi + n dPi/dn
reduction was machine-derived (sympy partial fraction of the total-derivative
identity) and standalone-grid-verified to 8e-15 at 40 dps during derivation; that
is disclosed. Everything below is about the full instrument (the six-constant
pure-float port), which has not been run end to end when this file is written.

- **P1 (J identity on the instrument's own values).** For every (n, m) the port
  actually evaluates (radial nh/m, polar up2/mth, pole n0/m across all rows),
  J_closed vs 40-dps quadrature: **≤ 2e-14 relative.**
- **P2 (port fidelity, CF-pure vs CF-orig).** The rewritten pure-float arm (all
  elliptic elements as counted Carlson kernels; J closed form; no mpmath) vs the
  original arm (ellipk/ellipe + 40-dps mpmath dPi/dn), same (E, Lz, Q): **≤ 5e-13
  on all six constants, all rows.** The port must change nothing in the answer.
- **P3 (exactness preserved, CF-pure vs QD).** Against the 30-dps separated
  quadrature on the 21-row grid + 4 held-out rows: **≤ 1e-11 on every constant
  and every row** (the original was 3.7e-12; the pure assembly adds the
  1/(2(n-1)(m-n)) conditioning in J, so I allow one decade, not more).
- **P4 (kernel count and price).** Per six-constant key, with shared K(m)
  reuse (Pi(n|m) = K(m) + (n/3) RJ(0,1-m,1,1-n)): **2x RF, 6x RJ, 2x RD — 10
  kernels total, 1.17 us** at de99's measured prices (rf 50 / rd 78 / rj 152
  ns). Range I accept: 10-16 kernels, 1.0-2.5 us. Per-key without reuse: up to
  ~2x that.
- **P5 (the 4real/0below root case is the separatrix edge, not a new algebra
  case).** In a census over a in {0.1,0.2,0.3,0.6,0.9,0.998} x p in {6.5,6.8,
  7.5,8,10,12,20} x e in {0.1,0.3,0.5,0.7,0.9} x th in {30,60,85}: rows with
  zero real roots below rp are **confined to e ≥ 0.5 with p within ~1 of the
  separatrix, and there the gap rp - r2 < 1e-4 and Lambda_r is the largest in
  the census** (the m->1 blow-up: the refusal path's domain, not a missing
  reduction). Prevalence **< 5% of the census.** The port asserts loudly on it.
- **P6 (read class).** The per-frame readout after compile is arithmetic plus a
  Newton amplitude inversion, **0 Carlson kernels**; the compile is once per
  (E, Lz, Q) key. So the torus read stays in the shipped read class (~4 us
  lean, de99) and the six-constant compile (P4) sits at the a765 floor (~6 us),
  i.e. **~5-60x below the shipped plane compile (4.4 us belt keys, 76 us p50
  plane mix)** — a number, not a kernel-count argument.

Predictions I explicitly do NOT make: no timing claim for Python wall clock
beyond order of magnitude (Linux/x86 shared runner); the port's float64 is the
oracle-side instrument — the engine's integer conventions are the build's step,
not this run's.
