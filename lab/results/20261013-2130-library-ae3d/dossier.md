# Dossier — 20261013-2130-library-ae3d (library lens)

## Claim

On the board's top bottleneck (28 live bodies against 10⁹), Julien's library yields five
falsifiable design rules for the N ladder — delete before measuring cheaper, promote by
rank in the surprise distribution, judge promotion on event time, buy the promotion option
rather than headroom, one mechanism at every scale — and a probe on the shipped body store
shows its cost already follows events, not bodies, with the spikes living in compaction.

## Bottleneck

Board focus 1: bodies in the flyable engine (28 vs 10⁹), in flight as Sonnet's N ladder
(`wt/nladder`). Expected gain: not a speedup claim but the deletion of the wrong
experiments — the rules say which ladder rungs to build first (deleted variants, rank
measurement, event-time hysteresis) and which to never build (a second promotion path,
head-of-distribution special cases, per-frame threshold evaluation). The measured half
deletes the fear that promotion itself is expensive: it is 6–7 ns and population-flat.

## Evidence

All verbatim quotes are retrieved from the Readwise export (cached in `readwise/`,
4,580 highlights, 762 sources; fetched with `READWISE_TOKEN`, see `regen.sh`). No quote in
this dossier is UNVERIFIED. The goodreads shelf (Kelly's memoir, Ignition!, Boyd, Structures)
is largely un-highlighted to-read; the practitioner material that exists verbatim is
Isaacson's Musk, Taleb, Ries, Waitzkin and Farnam Street.

Commands (repo root; each ≤ 60 s after a warm build; shared Linux runner, orders of
magnitude only):

```
cargo build -p emergent-shipmem --release --example ladder --example measure
T=$(cargo metadata --no-deps --format-version 1 | python3 -c 'import json,sys;print(json.load(sys.stdin)["target_directory"])')/release/examples
$T/ladder 1e-3 64 20000  20000 probe/row-n2e4.jsonl
$T/ladder 1e-3 64 200000 20000 probe/row-n2e5.jsonl
$T/ladder 1e-4 64 20000  20000 probe/row-trickle.jsonl
$T/ladder 3e-1 64 20000  20000 probe/row-storm.jsonl
$T/measure convoy 1000000 20000 128 probe/spikes-convoy.jsonl
```

Numbers (from `probe/*.jsonl`, JSON fields as printed by the shipped examples):

| row | members | rung | b_update_ns | b_compact_ns_per_update | bits/member | inferred |
|---|---|---|---|---|---|---|
| n2e4 | 1.28e6 | 1e-3 | 6 | 6 | 12.35 | true |
| n2e5 | 1.28e7 | 1e-3 | 7 | 7 | 12.33 | true |
| trickle | 1.28e6 | 1e-4 | 6 | 6 | 12.17 | true |
| storm | 1.28e6 | 3e-1 | 7 | 9 | 48.38 | false |

- Population ×10 at fixed events: per-update cost ×1.17, bits/member ×0.999 — cost follows
  events, not bodies.
- Churn ×300 (promotion storm): per-update cost ×1.17; memory ×3.9 (12.3→48.4 bits/member);
  `floor_bits` 2.3→18.1; the program inference fails and the store falls back to packed
  form B without round-trip loss (`mismatches: 0` everywhere).
- Spike anatomy (convoy, 1,000,464 ships, 20k updates): hot p50/p99/max = 34/1,271/9,217 ns;
  compaction 22.9 µs per update on average but **1.26 ms in one step** (arena compaction
  1.28 ms, 2,570 repacks). The repack is the allocator's enemy; the append is not.

### The five lessons (≤ 40 lines)

1. **Delete before you measure cheaper.** "Delete any part or process you can. You may have
   to add them back later. In fact, if you do not end up adding back at least 10% of them,
   then you didn't delete enough." — Elon Musk, Walter Isaacson. Mechanism: a part's
   interaction cost outlives its function, so optimizing it bakes it in ("Always wait until
   the end of designing a process … before you introduce automation", same source). Change:
   each ladder term — per-frame walks, rekey, the queue, memory per live body — gets a
   **deleted** rung before any **cheaper** rung. Test: count what the per-frame walk visits
   that the hot tier did not already touch (one counter, one build).
2. **The live set is a rank, not a count.** "When we learn a new language, it's always a
   good idea to start by learning the 100 or so most used words." (Zipf's law) — Power Laws,
   Farnam Street; with "In Extremistan, inequalities are such that one single observation
   can disproportionately impact the aggregate, or the total." — The Black Swan, Taleb.
   Mechanism: if per-body surprise is Zipf-shaped, the frame cost is set by the head and the
   mean budget lies. Change: promotion is by rank in the measured per-body surprise-rate
   distribution; live-set size k is a certificate re-derived when the distribution shifts
   (the player arrives). Test (falsifier): log kicks per body per orbit on one shipped
   scene; if the distribution is not heavy-tailed, this rule dies.
3. **Judge promotion on event time, not frame time.** "Darwinian fitness applies to species
   developing over a very long time, not observed over a short term—time aggregation
   eliminates much of the effects of randomness" — Fooled by Randomness, Taleb. Mechanism: a
   threshold read per frame sees sampling noise as signal. Change: the rebuilt handoff
   surface (and the compact↔live rule) evaluates its predicate on the body's own event
   clock, hysteresis measured in kicks or orbit fraction. Test: re-run the shipped chatter
   case (retrograde 0.49 R_H, 210 handoffs / 20 periods) with event-time evaluation.
4. **Buy the option, not the headroom.** "An option is what makes you antifragile and allows
   you to benefit from the positive side of uncertainty, without a corresponding serious
   harm from the negative side." — Antifragile, Taleb. Mechanism: promoting ahead of demand
   is linear memory with capped benefit; the shipped O(1) hot append (measured: 6–7 ns,
   population-flat, churn-flat, graceful fallback under storm) is the bounded-latency
   option. Change: no separate promotion path, no ahead-of-demand promotion; budget the
   repack (1.26 ms steps) as the scheduled spike. Test: the storm row above; remaining:
   feed it to the allocator and check the p99 frame.
5. **One mechanism at every scale.** "The key was to recognize that the principles making
   one simple technique tick were the same fundamentals that fueled the whole expansive
   system of Tai Chi Chuan." — The Art of Learning, Waitzkin. Mechanism: a special case for
   the distribution's head is a second convention, and second conventions compound (the
   5 Oct taste-log lesson). Change: a ladder rung that needs a second mechanism for the
   head fails the rung, whatever its numbers. Test: every rung runs the identical store
   code path — grep-able invariant, no N-dependent branches.

## Predictions

`predictions.md` was written before the probe. What happened: (1) held — per-update cost
×1.17 over a 10× population (predicted <2×); (2) held — bits/member flat to 0.15%
(predicted ~20%); (3) **half-failed** — compaction is the spike (1.26 ms max = 55× its
per-update mean, as predicted) but the hot path's own p99/median is 37×, not the predicted
≤3×: the append also has a fat tail (9.2 µs max; still 137× below the repack peak); (4)
held — 300× churn raised per-update cost ×1.17 (predicted <2×), with the honest extra that
the storm quadruples bits/member and kills program inference, gracefully.

## What would make it wrong

The rank rule (2) dies if shipped scenes' surprise distributions are not heavy-tailed —
that instrumented run has not been done. The event-time rule (3) dies if the chatter case
does not collapse under event-time evaluation — not run here. The probe numbers are a
shared-runner Linux/x86 bench of the store in isolation, not the plane: the ladder must
re-measure on the flyable engine, and the M1 re-measure is the integrator's.

## Cost of adoption, and fit with PRINCIPLES

Adoption cost is negative for rules 1, 4, 5 (rungs not built, paths not designed) and one
instrumented run each for rules 2 and 3. Fit: "Less is more … The cheapest compute is
compute not done. Delete before optimizing" (rule 1); "The player is the only wildcard …
Priority is slack, not proximity" and "Compute only surprises" (rules 2, 4); "Spacetime,
not space plus time" / "no ticks … we only care about changes" (rule 3's event clock);
"A fix signals the wrong representation; one law at every scale" (rule 5).

## The lens

A library lens quotes practitioners who never simulated a galaxy: nothing here comes from a
physics-engine author, so the rules may underweight what is specific to relativistic
dolls (the event clock of rule 3 is the closest). Analogies are cheap; I kept only rules
with a named falsifier, but the falsifiers for 2 and 3 are unrun — this dossier is a lead
until one of them is. The corpus also skews business/self-help; the engineering shelf
(Kelly, Clark, Boyd) is present in goodreads.csv but un-highlighted, so its lessons were
not available verbatim and were not invented.
