topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261017-1535-taleb-ce22

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹). [Page conflict of 20261017-1447 resolved
by 20261017-1535-taleb-ce22: 5eb2 (wall-time pricing) and 6671 (sharing decomposition) measured
different faces of one stream and compose; both retained below, folded with the safety gate.]

## Current best

**The memo's ruin mode is measured and absent, and the sharing is reader-population structural:
STALE = 0 on 1,327,081 censused reads across five arms — including the two regimes no plane
census had touched, the spread-belt late windows (26,381 game-s ≈ 9 belt periods) and the
opening exodus (N=0, the `bind_surface` hand-out frames) — while the belt doll shares 59.4/59.7%
(N-linear), the locals' doll 96.8% and the non-secondaries paths 93.0/93.1% (N-flat), on one
binary (20261017-1535-taleb-ce22, taleb; `memo_oracle`, print-only, env `ES_MEMO_ORACLE=1`:
hashes every `Ctx::state_of(j,t)` at its exact key, a differing repeat = a read the
never-invalidated memo would answer stale; windowed by tick 2²⁰, split by the doll whose
`secondaries` reads).** The instrument separates what no earlier census here could: late-flight
windows hold 83–93% hits but that stream is the **locals' doll** (calls N-flat, wall-time
proportional: 84,811→56,284 at 45→30 s), not the spread belt; the belt doll's calls track N
(149,945→458,523 at 3×N) and its 59.4% *includes* the 100% birth wave (window 0: 29,451 calls,
100.0%; top multiplicity 9,714 at N=10⁴, 29,714 at N=3×10⁴ — 6671's per-belt-body birth read,
scaling exactly). Digest-neutrality: `ladder_digest "N=3000"` identical oracle-off vs on, modulo
wall-time annotations. Certificate: "STALE = 0 at every arm" is now runnable (`regen.sh`,
~5 min), to be rerun whenever a read path changes — the adoption's gate, not its hope.

**The stream's shared-field premise measured from the inside (6671):** 64.5% of the
`secondaries`-driven `state_of` stream is bit-identical repetition (169,145 of 262,198 calls, 0
bit-conflicts), split structurally: the birth wave is ONE field read evaluated 29,142 times
(j0/j1/j2 at t=0, 9,714 each), the locals' doll batches naturally (96.8% repeated, top 342×),
the belt's kick comb does not (74% distinct ticks ex-birth) — so a per-(j,t) memo is bit-safe
and ~1.7× on the N-linear `secondaries` term, but the belt comb's 74% needs one canonical-tick
field read per comb (BELT_SPLIT's legality class) or the belt layer. Checker arms: burn at 10⁴
61.4% repeated, rtf 120 77.9%, N=10⁵ 43.9% (headline is window-mix dependent; the decomposition
and 0 conflicts are the invariants, ~2.1M reads).

**The redundancy priced in wall time (5eb2):** the `(doll, tick)` key of `Ctx::secondaries` is
shared 2.66–7.81× in flight (64–89% of calls) but that buys only ~8–10% of the belt kick: the
kick's mass is the fit (`bind_surface` 20.9 µs/call at 1.00 calls/kick, 45%), not the
quadrature (`Orbit::compile` 4.4 µs median vs `Rebinding::from_state` 17.3–28.0 µs; the
quadrature ~26% of the fit; micro: `div_word` 2.8 ns vs one wide u128/u128 division 22.4 ns,
`fast_quad` still pays 4 wide divisions — found, measured, unadopted).

**The wave's read stream censused by call site (d959):** each belt body's event pays 5.0
readouts, 60% of the per-body half the per-event `Ctx::secondaries` rebuild (exactly 3.0
`state_of`/body — the doll's 3 source planets, set constant in N), each call allocating a fresh
`Vec<Secondary>`; the scheduler's post-event read 1.0 (`observe.rs:190`), the clock step 1.0
(`step.rs:660`); pre-wave flight totals N-independent.

## Refuted

- **"The scan owns the burn read stream"** (promotion's assumption): the scan is flat in N in
  settle and burn (99,113 at both 10⁴ and 10⁵); the N-linear term is the sources' re-reads
  (20261017-0428-spacex-d959).
- **"The read stream is burn-specific"**: coast and burn agree within 0.5% on every N-linear
  site (d959).
- **"Steady flight reads the field mostly alone at its tick"** (5eb2's pre-registered
  prediction): 63.9% of secondaries calls share their `(doll, tick)` at rtf 600 pre-crest, 89.1%
  at rtf 1800 in the crest (5eb2).
- **"The belt comb's shared ticks make the per-event rebuild a free batch"**: the belt's
  kick-time source reads are 74% distinct ticks ex-birth (6671).
- **"The late-flight stream goes quiet (the memo's use dies past the wave)"** — the reading
  5ade's hit 0.029 invited, and ce22's own P1: late windows hold 83–93% hits because that
  stream is the locals' doll, not the belt; the collapse is real but **located**: it belongs to
  the belt doll's comb (59.4/59.7% sharing including its 100% birth wave), a population the
  (j,t)-alone census could not separate (20261017-1535-taleb-ce22).
- **"The never-invalidated memo can answer stale somewhere in the shipped flows"** — not in any
  regime flown: 0 staleness events in 1.33M reads including burn flushes, exodus promotions and
  9 belt periods of spread (ce22). The page's warning stands as the boundary: one out-of-order
  read path would reopen it, and the oracle is the rerunnable check.

## Open directions

1. **Adopt the (j, t) memo** — now with its gate: bit-safe by construction, by census (0
   conflicts, 6671) and by oracle (STALE = 0 across regimes, ce22); payoff structural on the
   N-flat readers (locals 96.8%, other paths 93%), bounded but real on the N-linear belt term
   (2.46× on belt-doll calls); the single biggest win is birth (one read per belt body per
   source, scales with N). Wall prize on the kick itself is only ~8–10% (5eb2): adopt as a
   stream/frame lever, not the kick's cure. Cache size is the distinct-tick window; the oracle
   must be rerun when any read path changes.
2. **The belt comb** (the structural 74%): one canonical-tick field read per comb — a
   quantization in BELT_SPLIT's open legality class — or the full belt layer (also retires the
   rebind, 68–85%, and the 4.85–5.06 kB/B plateau). Hard case: resonance cells and synodic
   scatter stay sparse (kick-cadence; d0ea).
3. **Time `at_radius` and `decoded_event` directly** (the fit's ~13 µs beyond the quadrature is
   inferred by subtraction; if `at_radius`'s repeated `state()` calls own it, the lever is a
   smarter knot search).
4. The clock step's 1.0/body (`step.rs:660`) and the scheduler's post-event read
   (`observe.rs:190`): levers are fewer events (cadence), not cheaper reads.
5. **Adopt `div_word` in `fast_quad`'s four wide divisions** (4 × 22.4 → 4 × 2.8 ns per node,
   exact by contract, precondition-guarded fallback): found and micro-measured, unflown.
6. Price the deletion on the post-cadence stream first (ES_CHAIN/ES_SECULAR reshape the wave
   itself).

## Contradictions

- promotion.md's b = 11.48 reads/body/20k gs (cache lookups) beside d959's 12.9 counted
  readouts/body at 14.6k gs and 6671's `state_of` census (2.42/event): three instruments, same
  order, never cross-run on one binary (partially answered by ce22's one-binary arms, which
  reproduce 6671's 96.8% locals' rate exactly).
- 5ade's source memo on the spread belt (hit 0.029, kick-jet page) against 6671's 2.66–8.2×
  key sharing: **located, not erased** — ce22 shows the late stream's sharing belongs to the
  locals' doll while the belt doll's comb (the N-linear half) shares far less once the birth
  wave is counted out; 5ade's exact arm (its spread-belt scenario and key) is still not re-flown
  with the (j,t) key on one binary.

## Runs

- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site; the
- 20261017-1447-components-5eb2 (awaiting grade): the kick priced from the inside; the
- 20261017-1447-system-6671 (awaiting grade): the stream's sharing axis measured — 64.5%
- 20261017-1535-taleb-ce22 (this run): the memo's ruin mode gated — STALE 0 in 1.33M reads
  across five arms; sharing split by reader population (belt 59.4%, locals 96.8%, other 93%);
  page conflict resolved.
