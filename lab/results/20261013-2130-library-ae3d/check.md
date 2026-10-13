Grade: silver

Library lens on board focus 1 (28 vs 10⁹ bodies). Reproduced: regen exit 0, deterministic
fields bit-stable, my reruns match — hot update 6–9 ns, the storm rung costs memory not
latency (12.3→48.4 bits/member, inference fails gracefully, 0 mismatches), convoy spike
anatomy holds (append p99 1.3 µs vs a 1.26 ms compaction step); all ten quotes verbatim
(4,580 highlights, 762 sources). Extensions: rung 1 → 64.1 bits, graceful; `battle` →
12.1 ms worst compaction step at zero repacks; 10× event rate → append max 36 µs, still
33× below compaction. Not gold: prediction 3 half-failed; the event-flat update cost is
by construction (only shelf 0 timed) and inside noise; the 6–7 ns "promotion" is the
store's kick path, not the plane's 486–585 µs `resolve_handout`. Gain: ladder rules plus
the compaction-spike measurement. Cost to adopt: one instrumented run.

## Reasons

1. **Reproduction.** Clean tree, empty `work/patch.diff`, shipped examples
   (`crates/shipmem/examples/{ladder,measure}.rs`). regen.sh exit 0; my reruns of all
   five probe commands reproduce every deterministic field exactly (ck
   3473012231995915456 / 11356900963643782561, scars, repacks 2,570) and every timing
   to the same order, with the sign of the 6→7 ns population delta flipped (7→6 on my
   box). The dossier table matches the author's original `probe/row-*.jsonl` first
   lines exactly. Arithmetic checks: 55× compaction spike over its mean, 37× append
   p99/median, 137× repack/append-max, ×3.9 storm memory, floor 2.3→18.1. This run
   passes the 5-October bar (numbers the shipped code regenerates).

2. **Predictions.** Content: (1) held but unfalsifiable — see 3; (2) held (0.15% vs
   ~20% allowed); (3) half-failed, honestly reported and confirmed by the data;
   (4) held, but the "300× churn" is a data-density proxy, not an event-rate stress:
   the update section applies exactly 20,000 kicks to shelf 0 at every rung
   (`ladder.rs:254`), so the append is never hammered 300× harder — the parenthetical
   in `predictions.md` concedes this. Timing: **the pre-registration claim is not
   supported by the record.** The surviving author captures `probe/row-*.jsonl.out`
   (the runs behind the dossier table) are dated ~1 minute *before* `predictions.md`;
   regen overwrote the `.jsonl` mtimes, so nothing evidences "written before the
   probe". The honestly reported half-failure argues against tailoring, but the
   held-out credit cannot be given as stated.

3. **The headline "cost follows events, not bodies" is a control, not a measurement.**
   `ladder.rs` times updates only on `shelves[0]`/`progs[0]` (population 0, 64
   members) — identical work at any `npop`; population-independence of the update path
   is a property of the 2²⁰-member sharding, demonstrated, not measured. The author's
   own repeats span 6–9 ns within single rows (trickle hit 9; n2e4 spans 6–8), so the
   reported ×1.17 is noise. What is genuinely measured across populations — bits/member
   12.347→12.329 and per-member streaming — does hold.

4. **Adversarial cases (mine; one outside the author's range).** (a) rung 1, the
   unswept edge: 64.13 bits/member ≈ the known fully-mixed ~63 (a91f cross-check),
   `inferred` false, 0 mismatches, updates 6 ns — graceful degradation holds to the
   edge. (b) `battle`, a shipped population the author never probed: worst compaction
   step **12.1 ms** (10× convoy's worst) with **zero repacks**, append tight (p99 48 ns,
   max 2.9 µs) — "spikes live in compaction, not the append" holds and strengthens,
   but "the repack is the allocator's enemy" dies as a general attribution. (c) 10× the
   event rate (200k updates): append max 9.2→36 µs, still 33× below the compaction
   step, round trip true — the bounded-option claim survives the next decade of the
   swept number.

5. **Novelty.** No prior `nladder` page; the topic is new. But the memory half of the
   storm row sits on known gold curves (a91f: ~50 bits once + ~2 per doubling, 63
   fully mixed; b30e: Form P dies on the first kick), and rules 1 and 5 restate
   PRINCIPLES #1/#19 in ladder terms. Rule 4's plane-level content is already measured
   stronger, the same day, uncited: `resolve_handout` is 486–585 µs, sticky, no
   demotion path (20261013-1915-fermi-367f, frame-cost), dormancy — deferred,
   no-ahead-of-demand promotion — cures the first N-wall with canon caveats
   (20261013-2005-spacex-3989), and the shared-shape memo is priced
   (20261013-2005-quant-7055). The dossier's sentence "deletes the fear that promotion
   itself is expensive: it is 6–7 ns" conflates the store's kick append with the
   compact→live promotion the board names; at that layer the fear is measured and
   real. Genuinely new: the spike anatomy on the shipped store (ms-scale compaction
   steps vs ns-scale appends — a direct feed to the allocator/smoothness bottleneck),
   and rules 2 and 3's named falsifiers as open directions.

6. **The page.** Corrected in place: the event-flat overstatement, the repack
   attribution, the missing frame-cost cross-reference and layer caveat, and the run
   line's "spikes are repacks".

7. **Goal fit.** Board focus 1, and PRINCIPLES #12: "minimize spike compute … the
   algorithm that allocates the work to prevent those heavy tails, it's the most
   important one" — the compaction-step finding serves exactly that. Rules quote
   PRINCIPLES faithfully (#1, #5, #14, #19 as cited).

## The one experiment to gold

Rule 2's falsifier: one instrumented run on a shipped scene logging kicks per body per
orbit. Heavy-tailed → the rank rule plus this store baseline deletes the headroom and
second-promotion-path rungs from the in-flight ladder (a component deletion, one step
to adopt). Not heavy-tailed → rule 2 dies, the fixed fraction stands, and the gold path
becomes folding the compaction-spike scheduling into the plane's allocator (open
direction 4).

## What the author missed

- The same-day frame-cost record (fermi-367f, spacex-3989, quant-7055): the plane's
  promotion is `resolve_handout` (486–585 µs, sticky, no demotion) and the
  no-ahead-of-demand direction is already measured there; rule 4 as written ("the hot
  append *is* the promotion", "no separate promotion path") argues at the wrong layer
  and ignores that the actual fear — stickiness — is unaddressed by a cheap append.
- The population row's tautology and the 6–9 ns noise band (the ×1.17 and ×0.999
  digits lend false precision to one real measurement — bits/member — and one control).
- The `battle` regime, where the repack story inverts (0 repacks, 12.1 ms step).
- The prediction pre-registration is unevidenced (probe stdout captures predate
  `predictions.md` by ~1 minute); next time, write predictions before any probe
  capture survives, or timestamp both.
- `goodreads.csv` is cited in the dossier ("the engineering shelf is present in
  goodreads.csv") but is not in the run folder — that sub-claim is unverifiable.
  Minor: no quote is affected.
