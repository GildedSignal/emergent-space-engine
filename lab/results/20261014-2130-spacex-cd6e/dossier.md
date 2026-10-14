# Dossier: 20261014-2130-spacex-cd6e (Spacex lens)

**Claim.** The incomplete-Carlson readout of the scaled Darwin cycle is now derived and verified
(the squared-pole Hermite reduction included), and its honest price REFUTES the record's priority
reading: the shipped time->state readout is ~4 us and FLAT in e, so the closed form buys ~parity
on the read half — its real, measured value is that with the certified increment forms (de99) the
knot/crossing table never gets built, deleting the compile wall (measured here 5-256 us, e-monotone,
49-97% of every kick per 21ba's checker) and the 7-16 KB/body standing memory, for a composed kick
of ~8-13 us flat in e.

**Bottleneck.** Board #3: one kick at 75-160 us against a ~50 ns floor (~10^3.3). b8fc measured
the read side at 66-69% of the kick's integrand point-evals and concluded "the incomplete Carlson
forms must land first"; de99 certified the complete forms (all three increments, 2.9 us, verified
to the f64 roundoff floor) and fenced the incomplete readout as "unpriced". This run derives,
verifies and prices it.

**What was built.**
1. Closed forms for all three channels as incomplete elliptic integrals, on the shipped
   representation (orbit.rs `node()`): with u = psi/2, x = k+(1-k)cos(psi) = 1 - n3 sin^2 u
   (n3 = 2(1-k); a0+e = 1 identically), 1-q a = A(1-m cos^2 u), m = 4q(1-k)/A, A = 1-q(8k-2):
   - advance: 2/sqrt(A(1-m)) * F(u | mg) - psi, mg = -m/(1-m);
   - tau:     2 sqrt(k - q(3k^2+(1-k)^2)) / sqrt(A(1-m)) * I2(-n3; u | mg);
   - t:       one 3x3 partial fraction of 1/((1-n3 v)^2 (1+n4 v)), n4 = 2q n3/(1-2q), then
     a3*Pi1(n3) + b3*I2(-n3) + c4*Pi1(-n4), all at parameter mg.
   The squared pole (the x^-2 of dt/dpsi) has no standard Carlson formula; it is reduced by
   Hermite reduction (sympy-solved, exact): int dth/((1+n sin^2)^2 sqrt(1-m sin^2)) =
   q1(F-E)/m + q0 F + c Pi1(-n) + (1/2)(n^2/((n+1)(m+n))) sin cos sqrt(1-m sin^2).
2. A read-only Rust probe (`crates/space/examples/readout_price.rs`, in the run's patch): times
   the shipped `Orbit::state` and `Orbit::compile` and dumps (psi, r, tau, adv, vr, vt) at 23
**Evidence** (regenerate: `regen.sh`, ~6 min; Linux shared box, 8 vCPU, load ~2-6):
- The reduction and all three closed forms vs direct quadrature (mpmath 30 dps):
  I2 3.6e-16, t 2.2e-30, tau 2.3e-17, adv 4.9e-31 (`closed_form_check.py`).
- Against the shipped walk's dumped states, every 3rd key (12 keys x 23 phases, 276 rows):
  **275/276 agree** (bracketed Newton on the closed t; the same reflection as the walk for the
  inbound half). Worst relative errors: psi 9.0e-9 (p=10, e=0.001, near apoapsis), radius 3.8e-9,
  proper time 2.8e-11, advance 4.5e-6 at the weak-field corner (p=1e6, e=0.001: cancellation in
  the 3x3 partial fraction at n4 -> 0; the advance itself is ~2e-5 there). The walk's own
  certified output quantum is 2^-30 = 9.3e-10; psi/r sit within ~4-10x of it and tau well inside
  (`verify_fast.out`; full-grid `verify.py` in regen.sh).
- Shipped readout wall, 36 keys, this box: **2,479-9,217 ns, p50 3,991 ns — flat in e**
  (e=0.999 with 175 crossings reads at 3,870-4,031 ns, same as e=0.3 with 14). The read is
  bracket + ~2.8 partial panels + ~1.9 rate evals (b8fc's census), NOT a table walk.
- Shipped compile wall, same keys: **5.2-255.8 us, p50 76.0 us, monotone in e**
  (e=0.001 -> 5-80 us; e=0.999 -> 120-256 us; 175 crossings).
- Composition of the closed readout (kernel walls from de99, same kernel class, f64 black_box):
  t(psi) = 4 RF + 3 RJ + 1 RD; a readout = ~4-6 Newton steps + state = **~21 RF + 16 RJ + 6 RD
  ~ 8-13 us** at de99's certified stop (RF 129 ns; RJ/RD ~0.3-0.5 us), constant in e.
  So on the read half: **parity, not a 10x.** (An f64 Carlson kernel timed at the readout's own
  2^-30 stop, ~4-5 duplications, would land near the low end; not timed here — that is the
  named next step.)
  Outcome notes: prediction 3 (Newton <=5 steps) was optimistic — the bracketed solver takes
  ~7-10 steps at e >= 0.9 from a linear start (a warm start from the previous readout's psi, the
  engine's actual access pattern, needs 1-2); prediction 1 held (weak-field degradation is the
  adv 4.5e-6 corner, graceful); prediction 2 was not exercised at its hardest (p=7, e=0.999
  converged at 3.8e-9 in r; the true separatrix m -> 1 remains the open spot check).

**Composed consequence (the adoption case).** Kick today = compile (5-256 us, this box; the a669
finding makes it per-flip) + read (~4 us) = **~7.5-260 us**. Closed-everything kick = de99's
certified increments (2.9 us, all three) + this readout (8-13 us) = **~8-13 us, flat in e**:
~2-4x at belt-like e (e <= 0.3), ~20x at the e >= 0.99 tail, and the 77-176 knots x 88 B +
crossings per body (7-16 KB standing, the memory bottleneck's term) never exist — toward de99's
48 B of increments. The read-side census led b8fc to sequence the incomplete forms first; the
wall says the compile is where the microseconds are, and the incomplete forms are the second half
of one adoption that deletes the table, not a standalone 10x on the read.

**Predictions** (`predictions.md`, written before the decisive verification): the Newton-count,
weak-field and near-separatrix predictions; the shipped read_ns prediction ("grows with e like
the knot count") was WRONG — it is flat — and that miss is the run's finding. The others: see
`verify_fast.out` (full-grid check in `verify.py`).

**What would make it wrong.** (a) The walk-vs-closed-form agreement failing on the full grid
(only the every-3rd-key subsample was affordable in-window; the full check is in regen.sh).
(b) The composed 8-13 us resting on de99's kernel walls rather than a fresh f64 timing at the
2^-30 stop — if an honest Carlson kernel at that stop costs 2x de99's certified-stop numbers,
the readout parity claim weakens to ~1.5-2x WORSE than shipped on the read half (the compile
deletion stands regardless). (c) m -> 1 (the separatrix, e -> 1 with q at the barrier): mg =
-m/(1-m) -> -inf, so the mixed-pole form degrades exactly where the walk's own certified 2^-30
also degrades (de99's second checker measured the closed form beating the walk there, 3.6e-10 vs
6.7e-7, for the complete case); the incomplete case needs the same spot check before adoption.

**Cost of adopting.** The readout layer of `orbit.rs` (outbound_at + read + the knot table's
readers) replaced by closed-form evaluation + Newton; the compile keeps only de99's increment
forms; the belt's first-kick memory doubling (ladder break 2, 2.6->5.1 KB/body) deletes with the
retired tables. The integer port (isqrt-closed, the law-level decision, 9384) is unchanged in
scope. Not adopted by a lab run regardless: floats explore, integers decide.

**Fit with PRINCIPLES.** #1 "the cheapest compute is compute not done" — the table is computed
and never read (8-10% of cells, b8fc); #3 "compute only surprises" — a readout re-integrating
panels at every query derives what the key already knows; #16/#32 — one representation (the
key's own elliptic invariants) makes the math trivial at every e; #19 "a fix signals the wrong
representation" — the knot table was the wrong representation for a question (time -> state)
whose native answer is one Newton step on a closed form.

**The lens.** SpaceX: question the requirement, delete, then idiot-index. What this lens may
have missed: the allocator/streaming view (a closed-form readout is stateless and branch-free
— SIMD/GPU-friendly, which the table walk is not; unpriced here), and the possibility that the
readout should never be called at all (derive states from neighbors / event keys, the a-word
direction), which would delete both sides of the parity comparison.

**Grade suggested:** silver. The derivation is exact and verified against shipped outputs; the
pricing is composed from measured kernel walls (de99) plus a fresh shipped-side timing, not from
a timed f64 implementation of this readout; that timing (one C/Rust file, the kernels are in
de99's run) is the named experiment to gold.
