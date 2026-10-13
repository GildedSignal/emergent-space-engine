# Predictions (written before the decisive run)

Question: what owns the ~25–27 µs "uncounted interior" of a plane kick's rebind
(fit → compile → readout) on shipped code — allocations, or arithmetic/iteration?
fa08/30e1 named the suspects; nobody has attributed. Fermi pre-estimate first:

- The compiled trajectory owns a `Vec<Crossing>` (Crossing ≈ 40 B: band + Words psi +
  Increments(3×Words)), plus whatever `Orbit`/`Trajectory` tables hold (wiki: ~530–970 B
  resident compiled quadrature per ship). An `Arc<Entry>` allocation (~50–100 B) per bind.
- A pure kick measured ≈ 75 µs median on runners of this class; if a kick does
  ~30–150 allocations (Vec pushes with growth, entry Arc, history segment) at
  ~50–120 ns per alloc/free pair (glibc, warm, 16 B–4 KB chunks), allocations own
  ~2–15 µs ≈ **10–60% of the interior**.

## Held-out predictions (not tuned on)

- P1 (calibration): pure kick resolve on this box, ship 14, Sparse, members 1: **55–110 µs**.
- P2 (census): allocations per kick **20–200**; bytes per kick **1–20 KB**.
- P3 (shape): the byte mass is dominated by the compiled trajectory's own tables
  (one or few large allocations ≥ 200 B), not by many tiny ones; `Arc<Entry>` is a
  distinct second class.
- P4 (attribution): priced at the measured pair cost of the observed size mix,
  allocations own **≥ 10%** of the kick's wall, and **≤ 70%** (else arithmetic is dead).
- P5 (cross-check): a never-free bump arena cuts the pure-kick wall by the attributed
  share within ×1.5, and the resolved-item stream (kind counts) is identical under
  both allocators.
- P6 (kill): if allocations own < 10%, the arena/bump lever is dead for the kick and
  the cheapest-exact-kick attack moves to the panel arithmetic itself (count/width),
  not memory management.

Failure of P1 means my probe is not measuring the shipped kick path (wrong arm), and
the run reports VOID for attribution, not a refutation.
