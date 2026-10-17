topic: kick-jet
status: open
closed-by:
valid-while:
updated: 20261017-0739-spacex-4ea0

# The kick jet: updating a compiled cycle from stored derivatives (law.md line 36)

## Current best

**Compile-on-read is dead in both forms, and the reader was never the view: one build serves
98–224 reads, 99% engine-side, and the mint itself is the first reader of every rebind
generation (20261017-0739-spacex-4ea0, spacex; census instrument digest-identical to pristine on all
four runs, three bench arms incl. two held-out).** On the player's own loop (`universe
--bench`, 1,200 frames = 2,000 game-s): 1,071 generations (32 spec + 1,039 rebind),
never-read 0 in every arm; 240,114 attributed reads = observe 65.9% + secondaries 19.2% +
step 12.0% + **view 1.0%**; 77.4 reads per rebind generation (400 members: 69.8; seed 7:
68.1); the 32 spec-born sources absorb 66.5% of all reads (4,992 each — every event in
their doll re-reads its 3 sources). **The first reader of every rebind generation is the
mint's own birth-read** (1,039/1,039): `bind_in` decodes the fresh trajectory at the binding
event to build the turn and residual, so "compile at first read" defers nothing — the
compile stays inside the kick's own event. Eviction (b9ae's knots→0 standing) pays a build
per read: ×98 builds, ×71 on the build term (240k reads × 21.7 µs ≈ 5.2 s on a 20 s flight
vs 73 ms shipped) — the standing table amortizes one 22 µs build over 98–224 reads
(0.1–0.2 µs/read): it is the engine's working set, not a lazy cache. Consequences: the
kick's 84–87% compile term (a765) can only get cheaper (open 1, the Carlson wiring), never
moved or deleted by laziness; the memory lever that avoids this bill is sharing (efd4's
intern), not eviction; and the read side's two engine deletions are now sized — the
per-event sources rebuild (19%, read-stream open 1) and observe's per-event reads (66%,
cadence territory). [Instrument: builds counted/timed at `OrbitShape`/`Passage::compile`,
reads per Entry generation attributed by caller site; space-side total 476,696 vs decode
240,114 — engine-internal reads outside decode only raise the bill, so the kill is
conservative; 2.29 builds/generation (word re-binds, memo builds) un-decomposed.]
[Checker-2, blind: all four arms reproduced (patch re-applied, re-built, digests bit-identical
to pristine) and everything held on four arms outside the tested set — seed 7 × 400 members
(65.6 reads/rebind-gen, never-read 0, birth-read first 10,573/10,573), kick-bench seed 7
(32.0), seed 3 at rtf 300 = 3× flight (51.9, birth-read 1,908/1,908, view 2,400 = 2/frame);
the CLI clamps `--members` to 400, so the 400 arm is this bench's whole member axis (the belt
stays unmeasured, as flagged). One correction: "view 1%" counts view.rs's direct decodes
only — the view's per-frame gather reads through `observe::root_state` (view.rs:282) and the
engine's per-event apply walks land in the same observe bucket (universe.rs:673), so observe
66% is a mixed bucket and "the reader is the engine" holds as immediate-caller attribution;
0e37's guess dies as the bill's owner, not to the last read. The kill is attribution-independent:
never-read 0 and the birth-read are structural in `bind_in`, and 52–77 reads/rebind-gen stand
whichever bucket they sit in. Nit: amortized build per read is 0.21–0.49 µs measured, not
0.1–0.2; ×98 is the no-cache upper bound on eviction.]


**The kick's floor is derived and measured, and the premise under 71 runs is inverted: the
rebind is compile-bound, not fit-bound (20261016-2229-components-a765, stage timings
inside `Rebinding::from_state` behind `ES_FLOOR_AUDIT`, three seeds incl. two held out,
4,553 rebinds, clean anchor 35.7 µs made / 203.3 µs leaver, digest-stable).** Per rebind:
compile 52.8–65.3 µs (84–87% of the rebind), fit_key 4.4 µs (6%), tail 5.3–5.6 µs
[checker: regen.sh's printed tail subtracts the prototype's 2.3 µs although the stage-2
timer already excludes it — corrected here; the reading is unchanged]; the
128-step bisection's whole deletion is worth 2.1 µs (3% of the rebind) — a Newton-from-seed
prototype (closed-form prefix + 8 steps from the `root_witness` seed, verbatim key tail)
runs 2.3 µs and reproduces the shipped key **exactly at the law's census quantum on
4,553/4,553 rebinds** (bit-identical 2,896 = 63.6%; all 1,657 bit-disagreements
sub-quantum, `disagree_quantum = 0`; only k is 48-bit worded, `periapsis` carries its
full 63-bit significand, so ulp-level root differences move bits but not the law's key).
The exact BigInt path (`inverse::fit`) fired 0 times; the circular branch 0. The derived
arithmetic floor is ~6 µs (Carlson compile ≤2.9 µs [de99] + key 2.3 + tail ~1), so the
shipped rebind (62.6–75.4 µs mean, corrected as above) sits **~10–12× above its floor** — the three floors in
the record reconcile as three different quantities: 42–56 ns (b063) is the **write**
floor (the binding's output bits), ~26 µs (1e74) is the **jet arm's own machinery**
residue, and ~6 µs is the law's arithmetic floor, carried almost entirely by the cycle
compile at the plane's eccentricities (cd6e's e-monotone domain; c4d3's 4.4 µs belt keys
are the other end — there the rebind's wall moves to the tail and the reads, gap ~3–4×).
The exact key's non-repetition is not unbound precision: at 2⁻²⁰ the keys still do not
repeat (836→811 distinct exact→census); the reuse domain is the coarser 12+12-bit memo
(93.6% hit here).
[Checker, reproduction: counters bit-identical on the author's three seeds and the clean
bench digest-identical to the unpatched binary; five further arms outside the tested range
(seeds 3, 11, 12345; rtf 300, a different population at 2,536 calls; a 3× longer flight)
hold every claim — 14,278 audited rebinds total, `disagree_quantum = 0`, `proto_errors = 0`,
compile share 82–87%. The dossier's passage arithmetic ("~350 µs each ≈ 1.3–1.6 µs of the
mean") does not follow from its own counters (66 passages × 350 µs / 1,467 calls ≈ 16 µs;
the leaver-kick median 203 µs bounds the plane's passage compiles below that) — the
cycle-compile-dominates split stands by residual either way.]
[Checker-2, blind: counters again bit-identical on seeds 1/7/42 (third independent
execution); six further arms (seeds 2026, 777, 5, 13; rtf 300 = 2,536 calls; 30 s flight)
add 11,382 rebinds — `disagree_quantum = 0`, `proto_errors = 0`, `exact_path = 0`,
`circular = 0`, compile share 82.4–87.1% — total 15,935 rebinds across both checkers.
Patched vs unpatched binaries: clean-bench digest identical. Corrected the stale 85–90%
and 60–72 µs bands and Open-2's ~7.5 µs (tail arithmetic) in place. The quantized-hit
drift vs 12db's 98.0% is flight length, not contradiction: 93.6% at 653 rebinds, 96.0% at
the 30 s arm here.]

**The wave's attendants are decomposed and two of them are exact duplicates, deleted bit for bit: one
fired belt kick (shipped `kick_clock`, steady state, N=10^5) is 49.6 µs = fit 41% + 3 source reads 23% +
own readout 8% + bind decode 8% + the tau pair 15% + 5% rest (walks+fit 95% of the item), and the tau
pair — the kick's own decode discarded then re-walked, plus the binding walked at its own anchor, a
value `bind_in` already computed — is deleted by `ES_TAU_CARRY` (~60 lines: the orbit state handed to
`rebind`, the anchor's proper time cached in the Binding): W_TAUT 389,211→11 calls, fired kick
49.6→41.3 µs (−17%), event cycle −12%, digests identical at both cuts and on all 8 frame_digest
flights × 4 schedules (20261016-1120-quant-5ade).** A third exact duplicate is named and priced: `apply`'s
`root_state_raw` position walk re-reads at the event tick what the resolver just read — 5.0 µs × 2.06
per kick, another −13% of the cycle, not built. A source-read (body,tick) memo is dead on the spread
belt: repeat share 0.029 at the first wave (0.296 steady, worst 322 = the locals' comb, not the belt).
At 10^9 the built carry is ~17 cores per billion, ~30 with the apply walk (−22%), x86 shares; the M1's
cheaper fit (compile 4.4 µs, c4d3) makes the walks' share larger there. The deletions are bookkeeping,
not law: the fit's 41% remains this page's compile-wall program and the cadence split (kick-cadence
open 2) still dwarfs both.
[Checker: the anchor half re-derives 2833's unadopted `proper_at_event` cache
  (20261010-1947-autoresearch-2833, silver, pure-kick microbench, 9–10%) on the shipped wave path;
  the t-walk carry, the decomposition, the memo kill and the apply-walk pricing are new. The item
  decomposition double-counts the bind decode (W_BIND's clock sits inside FIT's): walks+fit is ~93%
  of the item, the item ~45 µs on the author's box. Bit-identity reproduced by the checker outside
  the tested range: N=2×10^5 first wave, and a WH-dominated 70–400 ks window at 2×10^4 (digests
  identical, W_TAUT→13/0, W_TAU0→1/first-kicks-only).]
**The shipped compile is timed at the belt's true keys and the batched promotion's belt
adoption is dead: `Orbit::compile` runs p50 4.4–4.5 µs (mean 4.7, p99 8.0, max 12.5) on
the ladder belt's own key mix — e-monotone 3.4→8.3 µs across the belt's e, flat in p
across the band — and the full shipped promotion path (`add_body`: compile + catalogue
insert + bind + store) p50 9.2 µs, flat in N from 25k to 200k (20261015-1926-quant-c4d3).**
Keys bit-identical to the flight's (`ladder_ship` → `add_body` → `spec_binding`, doll-0
unit ONE), three seeds incl. two held out, predictions pre-registered. So 262f's batched
promotion (11.7 µs as timed, 12.8 honest) is a ~2.9× regression per promotion against the
shipped compile it replaces (1.4× against the whole 9.2 µs `add_body` path; checker's
arithmetic), its native ~4 µs projection is parity, and the
"wave compute cuts ~3–8×" sentence (priced against a669's ~30 µs/kick anchor) dies at the
belt: compile is ~7% of the wave's 59–76 µs/kick CPU, and b172's in-flight
promote-compile counters (0.56 s/132,061 = 4.2 µs; 4.74 s/940,718 = 5.0 µs) corroborate
the 4.4–4.5 µs from inside the flight. The closed forms keep their win where the grid
still reads 29–192 µs (strong field, e ≥ 0.5–0.999) — the belt's redraw cap at e = 0.4
is what the belt wave never pays; the wave's next lever is its ~85–93% non-compile
attendants, and the promotion path's own second half (bind+insert+store ≈ 4.8 µs).
[a765 prices the plane population's compile at 51–64 µs/rebind — the strong-e end of the
same e-monotone curve, where the closed form's 18× is available.]

**The batched promotion is priced: 11.7 µs on the true belt mix, exact to 2e-16, and the
reduction is now derived twice independently (20261015-0250-quant-262f).** Standalone
`bench.py` (no tree edits): the shipped `node()` integrands closed in Carlson form with
the squared-pole reduction solved by exact rational arithmetic — boundary coefficient
κ = n²/(2(n+1)(M+n)), digit-identical to cd6e's independent derivation — and the t-channel
3×3 partial fraction (n4 = 2q·n3/(1−2q)) solved exactly. Verification against adaptive
Simpson of the shipped integrands on the belt mix (a ∈ [2,3) AU, e Rayleigh-0.07 re-drawn
at 0.4, q ∈ [3.3,7.2]×10⁻⁹, the weak branch): t 3.45e-16, τ 3.59e-16, advance 1.75e-8
(1/q-amplified f64 cancellation, not a quadrature artifact — checker: it persists at quad epsabs
1e-14, and 40-dps mpmath shows the closed form algebraically exact to 7.7e-34 while its own f64
evaluation carries 1.3e-8 at belt q; neither f64 instrument resolves advance below ~1e-8 there).
Batched over 10⁶ promotions (SoA numpy/AVX, vectorized Newton with the analytic slope):
**11.7 µs/promotion, 6 iterations, recovered phase 2.2e-16 p99**; kernel composition at
de99's measured prices (2×RF + 3×RJ per readout) puts a native port at ≈ 4 µs. Against
the record's shipped anchors (wave CPU 59–76 µs/kick incl. attendants, b30b; ~30 µs/kick
compile, a669) the adoption's wave compute cuts ~3–8× and the knot table never exists.
Named before gold: the SIMD-vs-native-scalar ratio, the shipped-compile-at-belt-keys
timing, and the integer port (f64 is an instrument, not the law).
Checker audit (20261015-0250-quant-262f check): the timed batched arm carries a factor-2 slip —
read_batch's t and τ are exactly 2.000× the Simpson-verified scalar channels (adv matches); the
price, the 6 iterations and the recovered-u are unaffected (the Newton is self-consistent and its
slope is right to O(q) at belt q), but the batched path was never value-verified, and the excluded
per-body coefficient solves (two batched np.linalg.solve) add ~1.1 µs/promotion → ~12.8 µs honest.
The 6-iteration Newton is belt-scoped: 7–11 iters at e ≤ 0.9 / q ≤ 1e-6, and slow linear
convergence at e = 0.999 (40-iter cap, ~3e-13). Corners the author did not run (e → 0.999,
q → 1e-6, u → π/2): t/τ ≤ 4.4e-13, adv ≤ 3.1e-8 — under the run's own 1e-6 kill bar.

**The incomplete Carlson readout is derived and verified, and its price corrects the record's
priority reading: the shipped read is ~4 us FLAT in e, so the closed form buys at best warm-start
parity on the read half (checker-timed 4.4-6.9 us warm, 7.9-18.6 lean-cold, 32-73 as the run's own
algorithm runs) — its value is completing the one adoption that deletes the compile wall (5-256 us
measured, e-monotone) and the 7-16 KB/body tables (20261014-2130-spacex-cd6e).** All three channels closed
on the shipped representation (u = psi/2: x = 1 - n3 sin^2 u, n3 = 2(1-k); 1-qa = A(1-m cos^2 u),
m = 4q(1-k)/A; mixed pole mg = -m/(1-m)): advance = one F; tau = one squared-pole I2; t = one 3x3
partial fraction (n4 = 2q n3/(1-2q)) of Pi1/I2/Pi1. The squared pole (x^-2 of dt/dpsi) had no
Carlson formula; Hermite reduction (sympy-solved, exact):
int dth/((1+n sin^2)^2 sqrt(1-m sin^2)) = q1(F-E)/m + q0 F + c Pi1(-n) + (1/2)(n^2/((n+1)(m+n)))
sin cos sqrt(1-m sin^2). Verified: vs direct quadrature 2e-30/2e-17/5e-31 (mpmath 30 dps); vs the
shipped walk's dumped states on a 36-key grid (p 7..1e6 M, e 0.001..0.999), 275/276 rows agree
under bracketed Newton: psi 9.0e-9, r 3.8e-9, tau 2.8e-11, adv 4.5e-6 at the weak-field corner
(e=0.999/175 crossings = e=0.3/14), compile 5.2-255.8 us p50 76 us monotone in e. Composed closed
readout, priced by the checker as a BUILT f64 implementation (de99 kernels verbatim, stop 2^-30,
kernels rf 50 / rd 78 / rj 152 ns): the author's own verify.py algorithm runs 32-73 us/query
(10.8-17 Newton iters, 4 t-evals/iter from the per-iteration bracket check); a lean port (hoisted
check, 1 t-eval/iter) runs 7.9-18.6 us cold, 4.4-6.9 us warm — read-half parity holds warm/lean
only, NOT as implemented, and 6701 had already measured the shipped read at 4.0-5.4 us and one
incomplete evaluation at 11-28 us (closed-form-kernel page): b8fc's census stands on the plane mix
(~48-60 readouts per compiled table: 224,233 readouts / 4,348 compiles — the read side is ~2/3 of
orbit wall there; warm closed readouts at +0.4-2.9 us each outweigh the compile saved once at
belt e; the deletion wins at the e >= 0.99 tail and via memory). With de99's certified increments
(2.9 us all three), the composed kick is ~8-19 us lean-cold flat in e vs shipped compile+read
~7.5-260 us, and the knot/crossing table never exists (ladder break 2's 2.6->5.1 KB doubling
deletes with it). Named to gold: fold the honest timed readout and the readout-amortization
census into the adoption case, then the integer port. Checker attacks: grid one decade out
(e=0.9999/0.99999, p=1e8, e=1e-6) agrees 274/276 (worst r 1.2e-8); 177 random (k,q,psi) channels
vs quadrature worst t 1.7e-36 / tau 1.3e-16 / adv 3.7e-32 including m=0.9999998 — the
near-separatrix spot check (open item 2) passes at channel level; the Hermite and partial-fraction
identities are exact (sympy); the weak-field adv corner is cancellation in pref_adv*F - psi, not
the 3x3 solve (analytic: a3=n3n4/(n3+n4)^2, b3=n3/(n3+n4), c4=n4^2/(n3+n4)^2, c4->0 cleanly).

## Refuted

- **"The kick sits ~1,800× above a ~50 ns floor" (b063's headline, the board's premise,
  repeated by 12db's census): the 42–56 ns figure is the write floor (the binding's output
  bits, 1–2 cache lines); the law's arithmetic floor is ~6 µs on the shipped
  representation (measured key extraction 2.3 µs + Carlson-priced compile ≤2.9 µs + tail),
  and the shipped rebind sits ~10–12× above it (20261016-2229-components-a765).**
- **"A ~26 µs machinery floor remains" (1e74, jet arm): that is the shipped jet arm's own
  walk residue, not a floor — the Carlson-priced composition (~8–19 µs, cd6e) already
  beats it, and the derived floor is ~6 µs (20261016-2229-components-a765).**
- **"Deferring the compile off the kick path moves the rebind to ~10 µs" (open 2's premise)
   and "the view's ramp is the reader" (0e37's, inherited by the page):** the mint's own
   birth-read is the first reader of every rebind generation (bind_in decodes at the binding
   event to build the turn/residual), so deferral is a no-op; and the reader is the engine —
   observe 66%, secondaries 19%, step 12%, view 1.0% — with 68–77 reads per rebind
   generation, never-read 0 in every arm, so eviction pays ×98 builds (20261017-0739-spacex-4ea0).
- **"The fit is the kick's wall" (the reading under the jet program's 71 runs, and
  8c81/620e/f797's decompositions of it): on the plane's fired-kick population the fit is
  6% of the rebind (fit_key 4.4 µs of a 63–75 µs mean rebind [checker-2: corrected as in
  Current best], 4,553 rebinds, three
  seeds); the compile is 82–87% (20261016-2229-components-a765). The belt-wave reading
  (5ade: fit 41%) is the same machinery at the belt's e, where the compile is 4.4 µs
  (c4d3) — regime, not contradiction.**
- **"The adoption's wave compute cuts ~3–8×" (262f, priced against a669's ~30 µs/kick-compile
  anchor) at the belt mix: the shipped compile at the belt's true keys is 4.4–4.5 µs p50
  (e-monotone 3.4→8.3, flat in p, three seeds incl. two held-out) and the shipped promotion
  path (`add_body`) 9.2 µs p50 flat in N to 2×10⁵ — the batched 12.8 µs is a ~2.9× regression
  against the shipped compile it replaces (1.4× the whole path; checker); b172's in-flight
  promote-compile counters (4.2/5.0 µs) corroborate, so a669's anchor was not the belt's compile
  (20261015-1926-quant-c4d3). The batch/closed-form program survives at the strong-field, e ≥ 0.5
  grid where the shipped compile reads 29–192 µs (same binary, shape control) [a765: and on the
  plane population, 51–64 µs/rebind].**

- **"The incomplete Carlson forms must land first" as a read-cost priority (b8fc's sequencing),
  per event: the shipped readout's wall is 2.5-9.2 us flat in e across 36 keys — the read is
  bracket+Newton on ~2.8 partial panels, not a table walk; the closed form composes to warm parity
  there (checker: 4.4-6.9 us warm). The build (5-256 us, e-monotone) is where the per-event wall
  is (20261014-2130-spacex-cd6e).** Correction [checker]: b8fc's census stands on the plane mix —
  ~48-60 readouts serve each compiled table (224,233/4,348), so the read side is ~2/3 of orbit
  wall there; the wall shares DO follow the census at fleet level, and they bound the deletion's
  net win to the e >= 0.99 tail plus memory.

## Open directions

1. **Wire the Carlson compile into the fired kick (the integrator's one step):** on the
   plane population the compile is 82–87% of the rebind (52.8–65.3 µs) against a verified
   ≤2.9 µs closed form (de99, exact to the walk's quantum on 29 keys) — the largest
   measured deletion on this page, ~18× on the compile term, ~10× on the whole rebind.
   What a765 adds to cd6e/de99's case: the population share (the plane's kicks sit in the
   strong-e end where the shipped compile reads 51–64 µs), so the composed closed-form
   kick (~8–19 µs) lands at the derived floor's edge. Remaining gate: digest identity at
   the composition (the channel-level quantum agreement is done; the resolver-level wiring
   is the integrator's).
2. **Compile-on-read for the fired kick: KILLED as a lever on the shipped representation**
   (20261017-0739-spacex-4ea0): the mint's own birth-read is the first reader of every
   generation (deferral moves nothing), and eviction pays ×98 builds (the read bill, 99%
   engine-side: observe 66%, secondaries 19%, step 12%, view 1%). b9ae's "read ~once per
   binding" is dead as a population reading: 68–77 reads per rebind generation on the
   player's loop. The compile term's only levers are open 1 (cheaper build) and the read
   side's own deletions (read-stream open 1: the per-drain sources rebuild).
3. **The bisection → Newton key extraction is measured, not adoptable as-is:** 2.3 µs vs
   4.4 µs, key-equal at the law's quantum on 4,553/4,553 — but keys move at ulp level
   (`periapsis` is full-precision in the key), so it is a law change by the 5 Oct rule
   unless the exact rounding is kept; its whole prize is 3% of the rebind. Kept as the
   fit's floor measurement (a765).
4. [fe85's, standing] The multiply-add cycle update on the separatrix family
   (kick-cadence's territory); unguarded by any rung.
5. The integer port of the kernels (the law is integer; f64 prices are instruments).

## Contradictions

- None new. (b8fc's point-eval shares vs this run's wall shares are reconciled above: both true,
  different instruments.)

## Runs
- 20261006-0346-redteam-df81 (gold, one checker): multiply-add error C·drift² unbounded; inspirals need Peters' generator; re-anchor rule proposed.
- 20261006-1249-redteam-4978 (gold): jet invalid near the Schwarzschild separatrix; 10³–10⁹× the floor; plunge fabricated as bound.
- 20261007-0621-components-8306 (silver): per-anchor-C jet holds 10⁻⁶ at 0.0065 compiles/kick, belt sizes; gold first check, silver second.
- 20261008-0338-second-20261008-0234-spacex-0083-492f (silver): jet with knot correction cuts the rebind 3×, not 10×; integer-law C grounded at 1.7–4.7.
- 20261008-1337-redteam-2040 (silver): multiply-add fails by type at the separatrix; the bound predicate wrong for E ≥ 1 escapes.
- 20261008-1419-second-20261008-1337-redteam-2040-9a04 (gold): E-axis failure (15/8)(δE/(1−E))², 1.2×10⁸ stiffer; tri-predicate complete, freeze-ready.
- 20261008-1521-spacex-8016 (silver): the compile is ~half of every ship kick at one compile per kick; the jet needs 0.05.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e)^(2/3); 25 kicks at e 0.99 versus 342 at 0.5.
- 20261008-1613-second-20261008-1521-spacex-8016-6c47 (gold): the digest-identical jet cannot be wired; the realizable prize is the QuantizedMemo, ~70×, a law change.
- 20261008-1719-second-20261008-1613-redteam-7922-e86c (silver): horizon 543·(1−e²)^(2/3) on the shipped law; the per-cycle curvature trigger holds everywhere.
- 20261008-1719-system-0ccd (silver): every rebinding kick rebuilds from scratch; the compiler is 53–71% of it; jet prize 1.7–2.7×.
- 20261008-1757-second-20261008-1719-system-0ccd-b33f (gold): the wired jet renews 2.75× but cancels the physics: B13 41/64, lifecycle 12× off.
- 20261009-0401-quant-ea6b (silver): kick medians 35/70 µs; the stage table measured the wrong path (corrected by 96b4).
- 20261009-0521-second-20261009-0401-quant-ea6b-96b4 (silver): the rebind is 84.6% of kick wall; mean kick ≈79 µs; capacity ≈10⁴ ships/core.
- 20261009-1858-redteam-075b (silver): compounding curvature bias rad-level near the separatrix; overlaps df81's C·drift² already in law.md.
- 20261009-1936-second-20261009-1858-redteam-075b-a059 (gold): the re-anchored policy holds navigation or cost, never both, inside s ≲ 0.05–0.1.
- 20261010-0541-components-8c81 (silver): the kick rebinds every kick, 33.3 µs against a ~1.5 µs floor; the named fixes buy ~2.7×.
- 20261010-0814-second-20261010-0656-autoresearch-cc88-8ce2 (silver): the integer-compiler jet holds Δφ but not period/readout (156 at e 0.99); cadence churn-limited.
- 20261010-0920-quant-30e1 (silver): one kick = one compile; the compile's uncounted interior owns most of ~86 µs.
- 20261010-1706-second-20261010-1544-system-97ce-b18f (gold): the wired re-anchor walks |Δa|/a 1.5×10⁻³ on Jupiter seeds; no threshold reaches 10⁻⁶.
- 20261010-2141-system-eea5 (silver): the rebind-per-kick compile sits behind three bottlenecks; the jet ceiling is ~1.6× median, ~10× p99.
- 20261011-1456-components-f797 (silver): the fired kick's generator update runs 9–16× above its floor; the jet lands within ~2×.
- 20261011-1729-system-2c68 (silver): the frozen-tube carry holds 10⁻⁶ for median 34–790 kicks on plane bodies; cuts the kick 1.5–1.9×.
- 20261011-1814-second-20261011-1729-system-2c68-b242 (missing): no check.md; its dossier reports the carry compounds across rebinds (2c68's bound was a shadow artifact).
- 20261011-2235-redteam-6164 (silver): the multiply-add is false outside a corner: 190× the floor at p 100, e 0.9; every kick recompiles at r_apo 2000.
- 20261011-2306-second-20261011-2235-redteam-6164-ee08 (gold): Kerr confirms at every spin; the T-channel (15/8) dominates; one both-ends root-distance certificate.
- 20261012-0036-second-20261011-2306-system-3367-1e74 (gold): the jet pays 0.002–0.012 compiles/kick but cuts the kick only 1.3–3.8×; a ~26 µs machinery floor remains.
- 20261012-0358-components-fa08 (silver): the rebind is ~270× above a two-integer floor; the jet closes to 7–13× only with period derivatives.
- 20261012-1117-redteam-4808 (silver): a one-signed truncation error whose gain diverges at the plunge separatrix; no gate tests it.
- 20261012-1227-second-20261012-1117-redteam-4808-d617 (gold): fails both frozen budgets at μ ≤ 0.3; the band is fed by 30–40% of captures; residents linger.
- 20261006-0220-autoresearch-c3a5 (silver): a weak-hyperbolic quadrature shortcut is bit-identical and cuts the leaver-kick ladder 40–45%.
- 20261006-0437-constraint-ec9d (silver): the leaver-kick tail is Passage::compile (318–356 of 365–381 µs), not the rebind fit; every passage rebind is a leaver.
- 20261007-1843-second-20261007-1801-fermi-bb60-152f (silver): exact-key memo hit 0.0 on 3,108 distinct rebinds, held on unseen seeds and a 200-member fleet.
- 20261008-0234-spacex-0083 (silver): compile-bound kick: compile 64.5% of a 97 µs median, rebind 78.7%, forces 9%; the cheap jet is dead everywhere.
- 20261008-1419-components-620e (silver): the fired kick is ~25× above its floor: rebind 68%, shared secondaries 27%, forces 6%; integer evaluator not adoption-ready; gold first check, silver second.
- 20261008-1521-autoresearch-a48d (silver): fit_only deletes one dead trajectory decode per kick: −10.9% (33.1→29.5 µs), digest bit-identical, adoptable.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e)^(2/3); 25 kicks at e 0.99 versus 342 at 0.5; gold first check, silver second.
- 20261008-1719-second-20261008-1613-redteam-7922-e86c (silver): horizon 543·(1−e²)^(2/3) on the shipped law; the per-cycle curvature trigger holds everywhere; gold first check, silver second.
- 20261009-0521-second-20261009-0401-quant-ea6b-96b4 (silver): the rebind is 84.6% of kick wall; mean kick ≈79 µs; capacity ≈10⁴ ships/core; gold first check, silver second.
- 20261010-0306-second-20261010-0100-fermi-c11c-4cb2 (gold): sharing one compiled cycle across co-orbital bodies buys 1.08–1.17× (tail 6.3×), not ≥40×: the shareable compile is 9–17%.
- 20261010-1947-autoresearch-2833 (silver): a proper_at_event cache plus cartesian-free orbit_state cuts the pure kick ~9–10%, bit-identical.
- 20261011-1729-system-2c68 (silver): the frozen-tube carry holds 10⁻⁶ for median 72/314/705 kicks on the intended plane bodies (dossier's 34–790 mixes mislabeled rows); cuts the kick 1.5–1.9×.
- 20261011-2235-redteam-6164 (silver): the multiply-add is false outside a corner: 190× the floor at p 100, e 0.9; every kick recompiles at r_apo 2000; gold first check, silver second.
- 20261013-0037-components-009b (this run, awaiting grade): the word-transition double compile measured (5–6% of binds, 14.5–18.2% of bind time) and deleted digest-identically; bind −12.9 to −17.5%.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e)^(2/3); 25 kicks at e 0.99 versus 342 at e 0.5; gold first check, silver second.
- 20261013-0236-fermi-061f (pending): the interior closed by elimination — 9 allocs/kick at 0.3%, bump within noise, digests identical; i128 division 30.9 ns; the lever is panel/division count.
- 20261013-0037-components-009b (pending): the word-transition double compile measured (5–6% of binds, 14.5–18.2% of bind time) and deleted digest-identically; bind −12.9 to −17.5%.
- 20261013-0350-components-c914 (this run, awaiting grade): the division half measured dead — divq 1.04×, exact Newton reciprocal 1.05×; divisions 20–35% of the compile, all three named ingredients 42–56%; open direction 1 bounded at ~1.4×.
- 20261013-0350-scout-7d2b (this run, awaiting grade): reciprocal division killed (repeat fraction 0.019, cold 40.4 > libcall 23.6 ns); division only 29% of the node — isqrt 30%, cos 24%.
- 20261013-1145-components-9384 (this run, awaiting grade): bit-identical isqrt (f64 seed + Newton + fix-ups) 96.5→54.2 ns, compile −9.5% A/B/A, digests identical; isqrt lever closed, mul-only reciprocal open.
- 20261013-1145-second-20261013-0350-components-c914-00d2 (silver, second check): the arm64 half of the division floor — Newton loses 2.8× (TCG wall) / 1.49× (instructions) on every decade tested; `__udivti3` executes ~2.8 `udiv`/div (the run's "zero udiv / multiply-only" was a print-cutoff artifact), so the lever stays open on M1 silicon.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e²)^(2/3); 25 kicks at e 0.99 versus 342 at e 0.5; gold first check, silver second.
- 20261013-0037-components-009b (silver): the word-transition double compile measured (5–6% of binds, 14.5–18.2% of bind time) and deleted digest-identically; bind −12.9 to −17.5%.
- 20261008-1613-redteam-7922 (silver): the recompile horizon shrinks as (1−e²)^(2/3); 25 kicks at e 0.99 versus 342 at e 0.5; gold first check, silver second.
- 20261013-0236-fermi-061f (silver): the interior closed by elimination — 9 allocs/kick at 0.3%, bump within noise, digests identical; i128 division 30.9 ns; the lever is panel/division count.
- 20261013-0350-components-c914 (silver): the division half measured dead — divq 1.04×, exact Newton reciprocal 1.05×; divisions 20–35% of the compile, all three named ingredients 42–56%; open direction 1 bounded at ~1.4×.
- 20261013-0350-scout-7d2b (silver): reciprocal division killed (repeat fraction 0.019, cold 40.4 > libcall 23.6 ns); division only 29% of the node — isqrt 30%, cos 24%.
- 20261013-1145-components-9384 (silver): bit-identical isqrt (f64 seed + Newton + fix-ups) 96.5→54.2 ns, compile −9.5% A/B/A, digests identical; isqrt lever closed, mul-only reciprocal open.
- 20261013-1428-components-2368 (this run, awaiting grade): cos closed bit-identically by 4-way interleaving of the panel's Gauss nodes — primitive 42→14.1 ns/cos (3.0×), compile −10.6–12.4% A/B/A, plane digest identical, kick resolve 33.2→28.3 µs; unrolling alone refuted (1.01–1.03×).
- 20261013-1428-scout-21ba (this run, awaiting grade): the φ channel of the shipped panel compile is one Carlson RF call, exact to the compile's Q30 quantum on every strong key; panels 5→176 (e→0.999, band cuts), wall 3.2→197 µs vs ~90–420 ns closed form (checker-corrected; the run's 37–39 ns was a timing artifact); panel-count lever now has a named replacement mechanism.
- 20261013-1915-second-20261013-1428-scout-21ba-de99 (awaiting grade): the honest Carlson kernel (paper-verbatim, r=10⁻¹⁵, black_box) delivers φ/τ/t as a drop-in to the walk's quantum on 29 keys; φ 129 ns flat, all-three ≤2.9 µs vs 307 µs walk (42–2378× per channel); walk degrades to 6.7×10⁻⁷ at m→1 where the kernel holds 10⁻¹⁰; first run's DE weight bug found and fixed.
- 20261014-1221-system-b8fc (this run): knot-table census — 8–10% of cells read, 13.4 point-evals re-integrated per readout, read side 66–69% of point-evals; the incomplete-form readout is the one deletion for kick cost, search cost and standing memory.
- 20261014-2130-spacex-cd6e (silver, this run): incomplete Carlson readout derived+verified
- 20261013-1428-components-2368 (silver): cos closed bit-identically by 4-way interleaving of the panel's Gauss nodes — primitive 42→14.1 ns/cos (3.0×), compile −10.6–12.4% A/B/A, plane digest identical, kick resolve 33.2→28.3 µs; unrolling alone refuted (1.01–1.03×).
- 20261013-1428-scout-21ba (silver): the φ channel of the shipped panel compile is one Carlson RF call, exact to the compile's Q30 quantum on every strong key; panels 5→176 (e→0.999, band cuts), wall 3.2→197 µs vs ~90–420 ns closed form (checker-corrected; the run's 37–39 ns was a timing artifact); panel-count lever now has a named replacement mechanism.
- 20261013-1915-second-20261013-1428-scout-21ba-de99 (silver): the honest Carlson kernel (paper-verbatim, r=10⁻¹⁵, black_box) delivers φ/τ/t as a drop-in to the walk's quantum on 29 keys; φ 129 ns flat, all-three ≤2.9 µs vs 307 µs walk (42–2378× per channel); walk degrades to 6.7×10⁻⁷ at m→1 where the kernel holds 10⁻¹⁰; first run's DE weight bug found and fixed.
- 20261014-1221-system-b8fc (silver): knot-table census — 8–10% of cells read, 13.4 point-evals re-integrated per readout, read side 66–69% of point-evals; the incomplete-form readout is the one deletion for kick cost, search cost and standing memory.
- 20261014-2130-spacex-cd6e (silver): incomplete Carlson readout derived+verified against the shipped walk; value is the compile-wall deletion and the knot-table memory, not read parity.
- 20261015-0250-quant-262f (this run, awaiting grade): the batched belt promotion priced — 11.7 µs over 10⁶ bodies (numpy/AVX, 6-iter Newton, cold start included), scalar arm exact to 2e-16 vs the shipped integrands (timed arm 2× slip on t/τ, price unaffected); the squared-pole reduction re-derived independently (κ digit-identical to cd6e's); native projection ≈ 4 µs at de99's kernel prices; SIMD-vs-scalar ratio and the integer port remain.
- 20261015-1926-quant-c4d3 (this run, awaiting grade): the shipped compile timed at true belt keys — 4.4–4.5 µs p50 (e-monotone 3.4→8.3, p-flat, three seeds, two held out, predictions pre-registered), the promotion path 9.2 µs flat in N to 2×10⁵; the batched promotion's belt adoption refuted (~2.7× regression), b172's in-flight counters corroborate, the strong-field tail keeps the closed forms.
- 20261016-1120-quant-5ade (silver, proposed): the wave kick decomposed — fit 41%, sources 23%, tau pair 15% (2 exact duplicate walks, deleted −17% digest-identically), apply's position walk the next (−13%); source memo dead on the spread belt (0.029).
- 20261012-0036-second-20261011-2306-system-3367-1e74 (gold): the jet pays 0.002–0.012 compiles/kick but cuts the kick only 1.3–3.8×; a ~26 µs machinery floor remains [re-read by a765: the jet arm's own residue, not a law floor].
- 20261014-2130-spacex-cd6e (silver): incomplete Carlson readout derived+verified
- 20261015-0250-quant-262f (silver): the batched belt promotion priced — 11.7 µs over 10⁶ bodies (numpy/AVX, 6-iter Newton, cold start included), scalar arm exact to 2e-16 vs the shipped integrands (timed arm 2× slip on t/τ, price unaffected); the squared-pole reduction re-derived independently (κ digit-identical to cd6e's); native projection ≈ 4 µs at de99's kernel prices; SIMD-vs-scalar ratio and the integer port remain.
- 20261015-1926-quant-c4d3 (silver): the shipped compile timed at true belt keys — 4.4–4.5 µs p50 (e-monotone 3.4→8.3, p-flat, three seeds, two held out, predictions pre-registered), the promotion path 9.2 µs flat in N to 2×10⁵; the batched promotion's belt adoption refuted (~2.7× regression), b172's in-flight counters corroborate, the strong-field tail keeps the closed forms.
- 20261016-1120-quant-5ade (silver): the wave kick decomposed — fit 41%, sources 23%, tau pair 15% (2 exact duplicate walks, deleted −17% digest-identically), apply's position walk the next (−13%); source memo dead on the spread belt (0.029).
- 20261016-2229-components-a765 (this run, awaiting grade): the kick's floor derived and measured — rebind compile-bound 84–87% (52.8–65.3 µs of 62.6–75.4 µs mean, 4,553 rebinds, three seeds), fit_key 6%, bisection premium 3%, Newton prototype key-equal at the law's quantum 4,553/4,553 (checkers: 0 quantum disagreements on 25,660 rebinds over fourteen arms, digest-identical patched vs unpatched); floor ~6 µs, gap ~10–12×, the record's three floors reconciled as write/jet-arm/arithmetic.
- 20261017-0739-spacex-4ea0 (spacex, gold, checker-2): compile-on-read killed both ways —
