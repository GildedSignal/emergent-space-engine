# Dossier — 20261014-0450-scout-b29a

**Claim.** The smallest promotion between a compact belt body and a live one is no promotion at
all: on shipped pieces, one belt event composed as a stack-local function (row → `Key::darwin` →
`Orbit::compile` → readout → kick → `Rebinding::from_state` → `Population::scar`) costs **~38 µs
p50 / ~78 µs p95 and 12–40 B of standing state per event**, ~13× cheaper than the wired sticky
path (`resolve_handout`, 486–585 µs, 8,257 B, no demotion), and the kick itself can land directly
on the key's own Q48/Q32 quanta at **~0.1 µs**, reproducing the kicked state's true invariants to
7.6 quanta at every impulse scale measured (Δv/v ≤ 1e-1) — so the live bind is a regime change
(the refit's refusal), not an event.

**Bottleneck.** Board focus 1 (bodies 28 → 10⁹, the furthest gap, 10^6.4), ask (b): "the smallest
promotion between a compact body and a live one." The ledger (effb) sized the streams but left the
promotion's composed cost and floor unmeasured; 367f measured only the sticky wired path. This run
deletes the promotion as a per-event structure and re-prices it as a function. At 10⁹ quiet
(3.6e-5 events/body/game-s → 3.6e4 events/s): refit arm ≈ **1.4 Linux cores**, key-space arm ≈
**0.004 cores** — the kick term stops being the quiet-belt CPU wall and encounter discovery
remains the cold rail's only large term, consistent with effb's ranking.

**Evidence** (Linux/x86, 8 vCPU shared, load 2.6–3.6; orders of magnitude only; the integrator
re-measures on the M1). Bench: `crates/shipmem/examples/promo_floor.rs` (this run's patch), the
shipped lab belt spec (p ∈ [2048, 4096) Darwin Q16, Rayleigh e σ0.07 cap 0.6, w 32 bits, t 44
bits), N = 4096 bodies, integer impulse at Δv/v ∈ {0, 1e-8, 1e-6, 1e-4, 1e-2, 1e-1}, position
quanta 2⁻³⁰ M, velocity quanta 2⁻⁴⁰ c, zero refusals everywhere:

- p50/p95 µs: compile 9.5/25, readout 5.4/8.1, cartesian 0.47/1.2, **refit (`from_state`) 21/63**,
  **key-space kick 0.11/0.19**, scar 0.87/44 (batch growth spikes). Composed event ≈ 38/78.
- Key-space arm: |E−truth| median **7.6 Q48-quanta** at *every* scale 0…1e-1 (the same distance the
  f64 invariant formulas sit from the birth key: 3.0 E / 7.6 L quanta); against the refit's own
  `OrbitKey`, shape agreement ≤ 1e-9 relative in k and periapsis, impulse-independent (a double
  quantization floor, not error that grows with the kick).
- Wide grade: p/e columns never overflow at Δv/v ≤ 1e-6 (0/4096); at 1e-4 they overflow 92% — the
  8-byte scar's domain ends near Δv/v ~ 1e-5; stronger kicks pay a 40-B `Wide` record. My naive w/t
  column glue forced 53%/47% Wide at 1e-6 (an encoding/policy wiring point, not a store limit:
  `SCAR_ROUNDTRIP exact=true`, the store's own tests assert scar exactness).
- Identity: the composed column loop (f64 glue) returns the birth key to 8e-13 (E) / 1.4e-10 (L)
  relative — glue-bound, not a law bound.

Reproduce: `lab/results/20261014-0450-scout-b29a/regen.sh` (one release build + one 15-s run).
Full output: `run.log` in this folder.

**Predictions** (`predictions.md`): P1 cost held (38 µs in 60–400). P5 held and sharpened (1.4
cores refit arm, predicted 2–15; key arm 0.004). P4's substance held *better than predicted* (7.6
quanta to truth at all scales; I predicted divergence by 1e-2 — none), but my OrbitKey-level
threshold ("≤8 quanta of k") was mis-specified: the shape grid resolves ~2e5 Q48-quanta
(6e-10 relative), so the arms can never meet at 8 quanta there. P2 partially failed (40 B/event
measured with naive w/t wiring vs ≤12 predicted; still ≥ 200× under sticky). P3 failed at face
value (0/4096 key identity through f64 columns, 8e-13 relative) — the distance is my glue's
flooring, not the law's; the integer scar loop is exact by the store's construction. P6 failed:
overflow crosses 50% already at Δv/v = 1e-4 (92%), the i16 grade ends near 1e-5.

**What would make it wrong.** (1) The key-space arm's ΔE/ΔL must come from the encounters tier's
conjunction geometry as *exact integers in the law's quanta*; if the tier can only deliver a
state-space impulse, the refit arm (21 µs) is the floor — still 13× under sticky. (2) The
7.6-quanta agreement is measured on one belt band, one orientation convention, planar, no GR doll
(`cartesian` prograde only); 3-D inclination and the rotating doll are untested (the encounters
page flags the same domain hole). (3) All costs are shared-cloud Linux; the M1's 4 P-cores set the
real frame budget. (4) The 12-B scar claim assumes the w/t column policy is anchored at wiring
(measured: naive wiring forces Wide).

**Cost of adoption.** Small and local: the plane's belt wiring (H0216 follow-on) routes belt
events through a `Population` batch instead of `resolve_handout`; the refit arm composes three
existing pub APIs; no law change, no gate touched. It *deletes* work planned on the sticky path
(nladder direction 3's compaction-as-spike stays, ephemeral demotion arrives free).

**PRINCIPLES fit.** "The cheapest compute is compute not done" (#1: no standing body, no queue
entry); "you don't advance a ship tick by tick" / "we only care about changes" (#14: the scar is
the change); "store the generator, not the generated" (#6: the transient is a function of row +
event); "kicks are integers native to the law" (r2's finding, here made the *cheapest* exact arm);
one mechanism at every scale (#19: the same scar grade serves rocks and fleets).

**Cross-field (scout), with sources marked.** The mechanism is demand paging with a write-through
journal: fault in, compute, drop the page, append the delta — the OS page-fault path (materialize
on touch, no standing copy; UNVERIFIED at source this run), LSM point-reads without cache (the
`Population` *is* an LSM: hot batch → `compact()` merge → cold sorted runs; `scar` is the WAL
append; UNVERIFIED at source), and ECS structural-change batching at sync points (Unity DOTS'
`EntityCommandBuffer` ≈ demote-at-commit; UNVERIFIED at source). None of these fields pays a
standing representation for a transient — that is the shared lesson the sticky hand-out violates.

**The lens.** Scout optimized for mechanism-from-elsewhere and under-measured the plane's own
scheduling semantics (who calls this path, at what deadline — e49d's deadline-streaming is the
complement). The falsifier's impulse is my own, not the encounters crate's validated contact
impulse (c7eb) — magnitudes, not the real distribution.
