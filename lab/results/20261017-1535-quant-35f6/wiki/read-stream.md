topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261017-1535-quant-35f6

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹).

## Current best

**The conflict is resolved by flying the lever: the `(j, t)` memo of `Ctx::state_of` is
bit-safe and its wall prize is measured, not inferred — and it is not one number but a
7× swing across pace (20261017-1535-quant-35f6, quant; A/B on shipped main +
`work/patch.diff`, digest at one absolute horizon via `Universe::settle`).** Digest
identical off vs on in all three arms (1e4/600, 3e4/600, 1e4/100 — the rtf-100 arm
reaches the same digest as rtf 600 at the same horizon), 0 value conflicts in 986k
census calls + 350k served, stale keys ≤ 4 (generation bumps at every write to `j`,
`Universe::apply` and the rebind path). Prize: the secondaries term falls 182→43 µs/frame
at 1e4/600 (**4.3×**), 207→107 at 3e4/600 (**1.9×**), 22→1.6 at 1e4/100 (**14×**); the
Wisdom-Holman kick 52.7→35.7 / 41.2→35.3 / 60.5→48.5 µs (−32/−14/−20%); the clock kick
−24% at 1e4/600, −2% at 3e4; the FIT stage flat at 3e4 (23.5→23.4 µs/call — `bind_surface`
takes no ctx, the control holds); frame p50 1.54× at 1e4/600 but only −4% at 3e4, where
the memo pays in the tail instead (over-12ms frames 1→0, worst lag 7.0→0.0 s). So
5eb2's "only ~8–10% of the belt kick, not the kick's cure" and 6671's "cheapest item on
this page" are each right at one pace: at their shared arm (3e4/600) the kick prize is
14% and the frame barely moves; toward flying pace (rtf 100) the sharing concentrates
(79.6%) and the memo deletes the stream outright. Both sides' censes reproduce on the
flown build: 5eb2's 2.66× (doll, tick) sharing at 3e4 is 56.3% repeat at (j, t); 6671's
64.5% is 71.0% here; the belt comb's structural distinct ticks bind exactly as 6671
measured (the 3e4 arm's lower repeat is the comb's share). Instrument warning for every
future A/B: the end-of-flight digest is wall-dependent (the 12 ms budget's slicing moves
the horizon run to run — three arms, three digests, including the pure-observation
census arm); digest at one absolute tick or not at all.

**The redundancy of the per-event sources rebuild (5eb2, retained):** the `(doll, tick)`
key of `Ctx::secondaries` is shared 2.66×–7.81× in flight (64–89% of calls); kick clock
item 46.3 µs/call with `bind_surface` 20.9 µs at 1.00 calls/kick (45%), `secondaries`
6.25 µs (13.5%), `readout` 3.77 µs (372 calls/frame); `Rebinding::from_state` 17.3–28.0
µs vs `Orbit::compile` 4.4 µs (quadrature ~26% of the fit); one wide u128/u128 division
22.4 ns vs `div_word` 2.8 ns; strong-field `fast_quad` still pays 4 wide divisions per
node — found, measured, unadopted.

**The stream's sharing structure (6671, retained):** 64.5% of the `state_of` stream is
bit-identical repetition, 0 conflicts, and the split is structural — the birth wave is
ONE field read evaluated 29,142 times, the locals' doll batches naturally (96.8%
repeated), while the belt's kick comb does not batch (74% distinct ticks ex birth).

## Refuted

- **"The scan owns the burn read stream"**: flat in N in the settle and the burn flight;
  the N-linear term is the sources' re-reads (20261017-0428-spacex-d959).
- **"The read stream is burn-specific"**: coast and burn agree within 0.5% (d959).
- **"Steady flight reads the field mostly alone at its tick"** (5eb2's pre-registered
  prediction): 63.9% of secondaries calls share their `(doll, tick)` at rtf 600 pre-crest,
  89.1% at rtf 1800 in the crest (5eb2).
- **"The belt comb's shared ticks make the per-event rebuild a free batch"** (the
  optimistic reading): the belt's kick-time source reads are 74% distinct ticks ex-birth
  (6671).
- **"b063's refit share (84–89% of the belt kick), read as `bind_surface` alone"**: the
  fit is the largest term but 45–59% at the arms flown, quadrature ~26% of it (5eb2;
  arms may explain the gap, none identified).
- **5eb2's inference "priced in wall time it buys only ~8–10% of the belt kick" and
  6671's "~1.7× on the secondaries term", read as fixed prices** (the conflict): both are
  pace-dependent underestimates of one end — measured 1.9× at 5eb2's own arm but 4.3×/14×
  at the crest/flying-pace arms, and −14/−20/−32% on the WH kick (quant 35f6).
- **"The end-of-flight digest can certify an A/B"**: it cannot — the horizon moves with
  the budget's slicing; digest at one absolute tick (`settle`) (quant 35f6, hit first).

## Open directions

1. **Adopt the memo** (now flown, digest-identical, tail-positive at 3e4): the adoption
   questions left are the lock (a shared Mutex contends at multi-threaded resolution —
   shard it per worker; digests never move under schedule, r5-starve) and the map's
   growth at 10⁹ (48 B/entry × the distinct-tick window; cap-and-clear measured harmless
   at 0 clears here). The write-site invariant (generation bump at EVERY path that
   mutates a body's history) is the one silent-failure surface — keep the census's
   conflict counter wired as the tripwire.
2. **The belt layer** (the structural 74%): unchanged — one canonical-tick field read per
   comb (BELT_SPLIT's legality class) or the full layer; the memo cannot touch it, and
   the 3e4 arm shows the comb's share is what caps the memo there.
3. **Time `at_radius` and `decoded_event` directly** (5eb2's named probe): still untimed;
   the fit's ~13 µs beyond the quadrature is still inferred by subtraction.
4. **Price the deletion on the post-cadence stream first**: ES_CHAIN/ES_SECULAR reshape
   the wave itself (nladder page).
5. **Adopt `div_word` in `fast_quad`'s four wide divisions** (4 × 22.4 ns → 4 × 2.8 ns per
   node): still found, measured, unflown.
6. The clock step's 1.0/body (`step.rs:660`) and the scheduler's post-event read
   (`observe.rs:190`): each is a read of the body itself — the lever is fewer events
   (cadence), not cheaper reads.

## Contradictions

- promotion.md's b = 11.48 reads/body/20k gs and d959's 12.9 readouts/body at 14.6k gs
  agree in order; three instruments (lookups, readout calls, `state_of` calls), never
  cross-run on one binary.
- 5ade's source memo on the spread belt (hit 0.029) and the plane's 56–80% sharing: same
  lever, different regimes (wave vs plane); the memo is now flown on the plane's arms
  only — the spread-belt wave regime is still unflown (quant 35f6's domain bound).
- a765's rebind share 84–87% beside b063's 84–89% and 5eb2's 45–59%: arms differ, none
  identified; unengaged by the flown runs.

## Runs

- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site; the
- 20261017-1447-components-5eb2 (awaiting grade): the kick priced from the inside; the
- 20261017-1447-system-6671 (awaiting grade): the stream's sharing axis measured — 64.5%
- 20261017-1535-quant-35f6 (this run): the memo flown — digest-identical, 0 conflicts,
  secondaries 1.9–14× cheaper, kick −14–32%, tail cured at 3e4; the page's wall-prize
  conflict resolved (both sides half right, pace decides)
