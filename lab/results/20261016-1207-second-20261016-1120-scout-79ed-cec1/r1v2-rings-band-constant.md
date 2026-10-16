# Rung r1v2: orbits in rings around one mass — the band-constant rule named

Proposed re-freeze of r1 (the integrator owns the freeze; this file is the letter this
run executes, hashed before the run). Everything in `lab/rungs/r1-rings.md` stands
verbatim — question, bands, in-band law, dt/dφ rule, light model, sampler, cases,
metrics, oracle, bars — with these three changes, all additions, none weakened:

1. **The band-constant rule is part of the configuration name.** `binet-mM-centre`:
   u_k is the band's geometric centre (the r1 letter's rule). `binet-mM-refit`: the
   one-law refit of 20261016-1120-scout-79ed — every visited band's u_k is the
   geometric mean of the u-extremes the orbit itself attains inside that band, a
   self-consistent fixed point (≤ 12 rounds, |Δu_k|/u_k < 1e-15); a band the orbit
   merely crosses keeps the frozen centre **exactly** (crossing test: attained range
   covers the band). Constants resolve at first cycle and stay fixed (deterministic
   law; the repeat criterion audits them).
2. **Deterministic near-circular rows (new cases).** For each m: 12 bands k covering
   r ∈ [6.5, 1000] geometrically, u0 at offsets u_k·2^{f/(2m)}, f ∈ {−0.99, −0.5, 0,
   +0.5, +0.99} (60 rows): e = 0, start (u0, u′=0), same bars as the sampler
   (|Δφ − Δφ_GR| ≤ 0.01·|Δφ_GR|, period within 0.1%). A row passes only if both hold.
3. **Hyperbolic strong-field rows (new cases, held out by fe85 and by
   20261016-1120-scout-79ed's broken channel).** (p, e) ∈ {(8.5, 0.9), (7.7, 0.7),
   (6.9, 0.3), (6.5, 0.1), (9.5, 0.5), (12, 0.7)}: r_peri < 6 for the first four
   (the periapsis band obeys u″ − λ²u = 1/L² − 3u_k²); same bars as the sampler.

Sampler draw pinned to the letter (one `random()` for p, one for e, redraw both on
reject; the light b's continue the stream) — no dead draws. Bands are half-open in u,
(lo, hi]; a body exactly on an edge belongs to the band it is the upper edge of.

**Output.** `metrics.json` per configuration, plus the r1 picture.

```configs
binet-m8-centre candidate
binet-m8-refit candidate
binet-m16-centre candidate
binet-m16-refit candidate
binet-m32-centre candidate
binet-m32-refit candidate
```

```criteria
prec behaviour precession_pass_fraction >= 0.99
prog type prograde_fraction >= 1.0
period behaviour period_pass_fraction >= 0.99
defl behaviour deflection_pass_fraction >= 0.99
capture behaviour capture_misclassified <= 0
isco behaviour isco_correct >= 1
shape type shape_kept_fraction >= 0.99
repeat type cycle_repeat_fraction >= 0.99
cost cost crossings_per_cycle <= 512
nearcirc behaviour nearcircular_pass_fraction >= 0.99
strongf behaviour strongfield_pass_fraction >= 1.0
```

Controls. Negative: `binet-m8-centre` must fail `prec` (known: ~250/256 at m8). The
freeze discriminates the rule if, at the same m, the centre arm fails `nearcirc`
while the refit arm passes it. If a criterion fails for **both** arms at every m, the
configuration family dies there, never the method.
