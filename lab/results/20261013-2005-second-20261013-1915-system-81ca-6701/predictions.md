# Predictions (written before the first run of carlson_compile_probe.rs)

The checker's named gold experiment: port RD/RJ as certified integers on the 81ca
pattern, price the readout's crossing table (incomplete Carlson forms), and measure
the **whole compile replacement** (three channels, knots and all) on the shipped kick
path.

Formula under test (derivation in the probe header; the t/τ algebra is new here, the
φ channel is 21ba/81ca's twice-verified form):

- basis: `K = RF(0,1−m,1)`, `E = K − (m/3)·RD(0,1−m,1)`, `Π(n|m) = K + (n/3)·RJ(0,1−m,1,1−n)`,
  with `A = 1−q(8k−2)`, `B = 1−q(4k+2)`, `m = 4q(1−k)/B`, `n = 2(1−k)`, `n_h = −2qn/(1−2q)`,
  `H0 = 1−2q`, `tn = k·H0·H1`, `H1 = 1−2q(2k−1)`, `d = k−q(3k²+(1−k)²)`;
- `advance = 4·RF(0,A,B) − 2π` (standard Carlson notation; 81ca's form);
- `τ_half = √d·(2/√B)·[Π(n|m) + n·∂Π/∂n]`, `∂Π/∂n = [nE+(m−n)K−(m−n²)Π]/(2n(m−n)(n−1))`;
- `t_half = √tn·(2/(√B·H0))·[a·Π(n|m) + b·(Π+n∂Π/∂n) + c·Π(n_h|m)]`,
  `a = −n·n_h/(n_h−n)²`, `b = n/(n−n_h)`, `c = n_h²/(n_h−n)²`.

Truth: shipped `Orbit::compile` (advance/period/proper_period), plus an in-probe
dense quadrature of the raw ψ-integrands and a 50-dps mpmath check in regen.sh.

## Tuning grid (I may look at these)

p_slr ∈ {12·2^j, j=1..16}, e ∈ {0, 0.1, …, 0.9, 0.99}; strong branch only (q > 2⁻¹⁸).

## Held-out / attack cases (not tuned on)

- 81ca's held-out: (7.3, 0.05), (100.7, 0.55), (4192.9, 0.95), (37, 0.985),
  (99991, 0.3), (8, 0.995);
- the checker's attack keys: (20, 0.9999), (50, 0.99999), (7.801, 0.9), (7.81, 0.9),
  (7.85, 0.9), (7.01, 0.5);
- refusal keys (5, 0.0), (5.5, 0.9999) — recorded as refusals this time, never dropped.

## Predictions

- **P1 (control, φ):** integer advance ≤ 1.5×10⁻⁹ relative vs shipped on every strong
  grid key (81ca reproduced; any deviation means my re-derivation broke it).
- **P2 (τ, the new algebra):** f64 τ-half vs the in-probe quadrature ≤ 10⁻¹² on every
  strong key (formula right); integer vs shipped ≤ 10⁻⁹ (the walk's own channel
  precision; fast path carries ~48 weighted bits, slow path full Q62 — the achieved
  level itself is a measurement).
- **P3 (t, new algebra):** same two bars as P2.
- **P4 (cost, whole compile):** my three-channel integer wall (1 RF + 1 RD + 2 RJ + a
  few mults) ≤ 1/2 of that key's `Orbit::compile` wall at e ≤ 0.5 and ≤ 1/20 at
  e ≥ 0.9. I expect it to FAIL to beat compile at the two cheapest keys (p = 12,
  e ≤ 0.1, compile ~6 µs vs my ~4 Carlson chains ~6–8 µs) — flagged, like 81ca's P6.
- **P5 (readout):** incomplete Carlson (c = csc²φ forms, Carlson eqs 4.5–4.7 + the
  incomplete ∂Π/∂n) reproduces shipped `at_radius` times to ≤ 10⁻⁹ relative at matched
  radius (same ψ by construction), and one 3-channel incomplete evaluation costs
  ≤ 10 µs f64 — the crossing table (knots + crossings, 88·knots bytes per shape)
  is then deletable storage, not just deleted compute.
- **P6 (weak control, must NOT match):** weak keys (q ≤ 2⁻¹⁸) disagree on τ and t at
  ~q-level (the branch's own first-order truncation), as 81ca saw on advance.
- **P7 (conditioning):** the ∂Π/∂n form has poles at m = n, n = 1, n = 0; the strong
  domain excludes n ≥ 1 and n = 0, but m = n is interior (q = 1/(4k+4)). No grid or
  held-out key sits within 2⁻¹⁰ of it (checked symbolically); if an attack key does,
  the row is flagged, not hidden.

## What would make the claim wrong

- Any strong key where f64 closed form ≠ in-probe quadrature beyond 10⁻¹²: the t/τ
  reduction is wrong.
- Integer vs shipped > 10⁻⁷ anywhere on strong keys: the RJ/RD port (correction terms,
  e_m signs, polynomial tail) is wrong, not just imprecise.
- RJ iterations unbounded or RC(1,1+e_m) hitting e_m ≤ −1: the port's domain handling
  is broken on this domain.
