# Predictions — run 20261011-0134-autoresearch-2d92 (written before the decisive experiment)

Tune set (what I optimise on): `worlds::gas` n ∈ {256, 1024, 4096}, fill 0.1, q 1024, vmax 256, seed 1, horizon 1024 — via `cargo run -p emergent-lattice-event --release --offline --example bench -- tune`.

Change under test: exact i64 fast paths (`hit64`, `first_hit64`) for the visit predicates in
`EventCore::predict` and `EventCore::scan`, guarded by |d_c| ≤ 2^26, |w_c| ≤ 2^16, reach ≤ 2^24
(the lattice-metal GPU's own exactness certificate, extended to `first_hit`), with the existing
i128 predicates as fallback. Same bits by construction; the guard is the certificate.

Held-out set (run once at the end, never tuned on):
- `gas` n = 64 and n = 16384 (same fill/q/vmax/seed)
- `gas` n = 1024 at fill 0.3 (denser: 4× the events per body)
- `random` n = 4096, area 10^6, Pass (dilute; predict-dominated, almost no events)
- `crowded_axes` n = 4096 (pure prediction workload, zero events)
- the engine's cost test (`cargo test -p emergent-engine --release --offline --test cost -- --nocapture`), the real consumer (Fermi frame + tide kicks)

## Predictions

1. **Digests bit-identical** on every held-out case (world digest + log digest equal to the
   baseline recorded in `work/baseline.txt`). This is the constraint, not a prediction — if it
   fails the change is reverted whatever the speed.
2. **ns/fired on gas drops 25–45%** at n = 64 and 16384 (firsts/fired ≈ 27–42 there; at
   ~100 ns per i128 first_hit, cutting it to ~30–40 ns should remove roughly a third of the
   2.8–4.3 µs per event).
3. **Fill 0.3 gains less per event** (pred/ops 0.699 → more of the time is scan `hit`, which
   is one-shot, and response/publish): I predict 20–35%.
4. **random and crowded gain more than gas** (their wall time is nearly all `first_hit`:
   8.4k firsts per fired, 26.8 firsts per body): 30–55% off ns/body.
5. **The engine's cost test shows the same direction** on its frame/sparse-order numbers
   (ns per body per epoch-kick down 20–40%), outcomes equal in both orders.

Kill criterion for the change: median tune-set gain < 10%, or any digest or test failure.
