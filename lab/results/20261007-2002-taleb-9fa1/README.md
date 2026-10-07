# Reproduce (each command well under 60 s; from the repo root)

- Probe: `crates/encounters/examples/phase_probe.rs` (saved in this run's `work/patch.diff`).
  Rides the crate's own truth (`truth::truth_pair`), RNG and `Body` conventions.

```
cargo run --release -p emergent-encounters --example phase_probe -- main   # 9 scenes, ~13 s
cargo run --release -p emergent-encounters --example phase_probe -- scale # 3 scenes, ~22 s
cargo run --release -p emergent-encounters --example phase_probe -- smoke # plumbing, <1 s
```

Raw output: `main.jsonl`, `scale.jsonl` (one JSON object per scene per line).
Memory: < 100 MB per process; 4 threads.

Scene = co-orbital bundle: a in [1, 1+da] (da=1e-4), Rayleigh e with spread sigma_e,
pom uniform over TAU (the belt's convention) unless pom_window=0 (apsides aligned),
lam uniform, n bodies, encounter radius rho, horizon in orbits, seed.
Truth: every pair through the crate's rigorous conservative advancement, with an exact
necessary prefilter (radial ranges disjoint by > rho can never meet; distance >= |r_i - r_j|).
Miss_k = fraction of true encounters whose circular rank distance in the t=0 sort exceeds k.
