topic: kick-jet
status: open
closed-by:
valid-while:
updated: 20261016-1459-quant-ff8c

# The kick jet: updating a compiled cycle from stored derivatives (law.md line 36)

## Current best

**5ade's named apply-walk deletion is built and exact: `ES_POS_CARRY` (~55 lines) hands `rebind`'s
`scalars(exact)` to `apply` (the binding holds it bit for bit at its event tick — verified, not
assumed) and skips the walk outright when nothing rebound (the cache already holds the same
binding's state at the same event tick, `pos_tick`): one belt flight N=10⁵ to 20,000 game-s
(through the first wave), the walk stage falls 0.797–0.992 s → 0.126–0.127 s (−84…−87 %,
4,951–6,164 → 783–790 ns/call), the counter structure is hits 130,434 = every fired kick's
rebind, skips 30,481 ≈ the boundaries, walks 100,075 = one per birth (O(births), not O(events)),
and the identity holds everywhere it was tested — `ES_POS_VERIFY` re-walks every hit: mismatch 0,
walk_err 0 over 130,434 carries; digests identical on that flight's canonical cut (a287f479…,
5 runs × 3 arms), on all 8 frame_digest flights (4 schedules each) and on all 13 ladder_digest
cases (4 schedules each, planet-doll locals included) (20261016-1459-quant-ff8c).** The walk was
15.2 % of the sampled event cycle (ROOT / ROOT + kick items, OFF arm), so the deletion buys
~−13 % of the belt's event cycle — 5ade's pricing, now measured on the built change; at the 10⁹
rail the per-event walk is gone whole (kicks carry, boundaries skip), and what remains of the
stage is the birth walk (1.26 µs per body, once) plus the ancestor half for planet-doll ships
(inside `root_pos_from`'s centre walk). The next two levers it names: the birth walk
(`add_body`/hand-out already hold the state they bind — the same carry, O(births), the wave's
own opening bill), and the centre chain (a per-doll (tick, state) memo would collapse the
locals' shared-tick walks, the comb's own shape). x86 shares, shared box (kick-item wall wobbles
±25–30 % between runs; the stage table and the counters are the stable instrument).

[The standing entry below is main's page as it was; this run's entry is additive above it.]

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
  the tested range: N=2×10⁵ first wave, and a WH-dominated 70–400 ks window at 2×10⁴ (digests
  identical, W_TAUT→13/0, W_TAU0→1/first-kicks-only).]

## Refuted

- **"Apply's position walk re-reads what the resolver just read" as a half-truth (5ade's framing):
  there are two duplicates, not one.** A rebound body's walk re-reads the state `rebind` bound
  (deleted by the carry), and an unrebound body's walk recomputes a value the position cache
  already holds exactly — the same binding at the same event tick (deleted by the skip). The skip
  half is the larger class on the belt (boundaries), and neither half needs the resolver's value:
  only the binding's own bit-for-bit promise (20261016-1459-quant-ff8c).

[The page's standing refutations are unchanged; see main's page for the batched-promotion and
read-priority refutations (262f, c4d3, cd6e).]

## Open directions

1. **The birth walk** (this run's naming): `replan`'s apply walks every body once at birth
   (100,075 walks = the whole surviving stage on the belt flight, 1.26 µs each, the wave's own
   opening bill). `add_body` and the hand-out bind from a state they hold exactly
   (`bind_exact`); the same carry deletes it. O(births): it matters exactly where the wave and
   the battle mint bodies.
2. **The centre chain**: `root_pos_from` still walks the doll chain above a carried state
   (planet-doll ships, the locals). A per-doll one-entry (centre, tick) memo — valid while the
   centre's binding covers the tick — collapses the locals' shared-tick walks; the comb is its
   workload. Unmeasured on this run (the belt has no ancestors).
3. [Standing from 5ade:] the fit's 41 % (the compile-wall program) and the cadence split
   (kick-cadence open 2) still dwarf both deletions; the integer port of the kernels remains.

## Contradictions

- None new. (The kick-item wall's ±25–30 % run-to-run wobble on this shared box means paired
  A/B runs, not cross-run comparisons, are the instrument for wall claims; the stage table,
  counters and digests are stable.)

## Runs

- 20261016-1459-quant-ff8c (this run, awaiting grade): apply's position walk deleted two ways
  (rebind carry + pos_tick skip), −84…−87 % of the stage, mismatch 0 over 130,434 carries,
  digests identical (belt N=10⁵, 8 frame_digest flights, 13 ladder_digest cases).
[The page's standing run list is unchanged; see main's page.]
