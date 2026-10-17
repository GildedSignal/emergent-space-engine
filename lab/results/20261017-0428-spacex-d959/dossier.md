# Dossier — 20261017-0428-spacex-d959 (lens: SpaceX)

## Claim
The burn read stream's N-linear half is named and split: through the belt's first kick wave each
belt body pays ~4.7 readouts per event, and **60% of them (2.8/body) are `Ctx::secondaries`
re-reading the doll's ~3 source planets and re-allocating a fresh `Vec<Secondary>` per event** —
a constant set re-read per event, the exact shape a per-drain source readout deletes — while the
player's scan (`encounter.rs:137`), the suspected owner, is **flat in N** (160,663 readouts at
every N from 10⁴ to 3×10⁵).

## Bottleneck
Board focus 1 / promotion.md open direction 1 ("what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹: 5.74×10⁷ reads/s wall of pure hit-path
ε). This run does not cut it yet; it points the deletion at the right site: the per-event
`secondaries` rebuild is ~60% of the per-body wave stream, so the deletion ceiling for the read
stream's N-linear half is ~1.7× (and the per-event `Vec` allocation churn goes with it). The
scan — the previously assumed owner — is not the N-linear term at all on shipped main.

## Evidence (all from shipped code + the print-only instrument below; Linux x86, orders of magnitude)
Instrument: `readstat`, a `#[track_caller]` census on `Binding::readout` (and a tagged count on
`Ctx::state_of`), armed after the build; no arithmetic touched. 13/13 `ladder_digest` cases
digest-identical to pristine (stripped of wall-time annotations, md5 equal; `work/digest_*.txt`).

The wave (readwave: settle straight to 14,600 game-s; no page, no view; `p.u.settle`):

| site (caller of readout) | N=10⁴ | N=10⁵ | N=3×10⁵ | shape |
|---|---|---|---|---|
| `ctx.rs:89` `secondaries`' `state_of` loop | 75,245 | 345,245 | 945,245 | flat 75k + **2.7–2.9/body linear** |
| `observe.rs:190` the settle's own ramp read | 102,256 | 192,256 | 392,256 | flat 102k + ~0.95/body linear |
| `step.rs:660` the clock step's own read | — | 99,710 | 299,710 | **~1.0/body linear** |
| `encounter.rs:137` the player's scan pair test | **160,663** | **160,663** | **160,663** | **flat (not N-linear)** |
| `step.rs:291` surface check / `ctx.rs:109` tide | 31,408 / 23,265 | same | same | flat |
| total reads / body (TOTAL incl. tag double-count) | 57.1 | 12.9 | 9.6 | falls: flat terms / N |

Per-event terms (each belt body's first settle ≈ one event): secondaries ≈ 2.8, own ramp ≈ 0.95,
clock ≈ 1.0 ⇒ ~4.7 readouts/event, of which the sources' re-reads are 60%. The `secondaries`
count is ~2× the ~1.4 source-reads one evaluation needs: the kick path asks for the sources more
than once per event (kick + settle + clock paths each rebuild), and each call allocates a fresh
`Vec<Secondary>`. At 10⁹ the wave's per-body half alone is ~4.7×10⁹ lookups over ~1,483 game-s
(rtf 100 ⇒ ~15 s wall) ≈ 3×10⁸ lookups/s — several cores of pure hit-path ε, the promotion
page's knee re-derived from the inside with the sites named.

Flight-only totals (nladder, 20 s flights, census ends before the one-shot view gather;
"flight" line): 10⁵ coast 109,230 / burn 190,718 readouts per ~1,900 game-s — ~1.1–1.9
reads/body pre-wave, all flat sites (the scan 34–99k, the locals' settles); the N-linear
term turns on only with the wave (13,051+ game-s), and the one-shot end gather adds exactly
3 readouts + 3 source-reads per emitter (`observe.rs:144/149` + its `secondaries`) — the
view's own ∝N bill (view page), excluded here.

## Predictions
Written before the decisive runs (`predictions.md`). Scored:
- **P1 wrong** (the interesting result): the scan was predicted ≥60% owner of burn; measured
  flat in N and 3rd–5th by size. The N-linear owner is `secondaries`.
- **P2 half-wrong**: the scan does not grow with N (it reads the player's window, not the
  belt); the resolver's *sources* term is the linear one.
- **P3 held**: coast and burn agree within 0.5% on every N-linear site (952,967 vs 956,505
  total at 10⁵ pre-wave) — the stream is flight-independent.
- **P5 held in form, moved in target**: the deletion is not (only) the scan's certificate; it
  is the per-event sources rebuild — see "what would make it wrong".

## What would make it wrong
- The settle path is not the flown path: `p.u.settle` runs the engine's events without the
  page's budget slicing; if the page's drain batches already share source reads across events
  in one drain, the per-drain deletion buys less than the 1.7× ceiling. (The nladder "flight"
  totals show the same sites, so the sites are right; the batching question is unflown.)
- The wave is the pre-wired cadence's artifact (every root body kicked 2⁷/Cinder-period): a
  cadence law that de-phases the wave changes the *rate* the stream arrives at, not the
  per-event 4.7.
- Reads were counted, not timed: on Linux/x86 the readout's µs are not the M1's; the 10⁹
  arithmetic uses the promotion page's ε pricing, not a measured per-read cost.

## Cost of adoption
Zero to adopt the census (print-only, digest-identical, +49 lines in `bind.rs`, +4 in `ctx.rs`,
+1 example, +1 Linux `footprint`). The deletion it names (share one source readout per drain,
reuse the `Vec`) is a small, local change in `Ctx::secondaries`' callers — priced next.

## Fit with PRINCIPLES
- "the cheapest compute is compute not done" (§1): the sources are a constant set of exact
  tubes; re-reading them per event is work the drain already did.
- "Compute only surprises" (§3): a planet's state between its own events is derived, not news.
- Idiot index (lens): the sources' re-reads carry zero surprise per event — the worst ratio in
  the stream.

## The lens
SpaceX's delete-first reached for the scan (the biggest *suspicious* site) and was wrong about
the owner; the census, not the instinct, named the target. What the lens may have missed: the
cadence runs (ES_CHAIN/ES_SECULAR, awaiting grade) already reshape this wave; the deletion
should be priced on the post-cadence stream before it is built.

## Reproduce
`regen.sh` (≈4 min): rebuilds with `work/patch.diff` applied, runs readwave at 10⁴/10⁵/3×10⁵,
nladder 10⁵ coast/burn, and the pristine-vs-patched `ladder_digest` identity check.
