# Dossier — 20261017-1535-spacex-f1e6

## Claim

The `(doll, tick)` memo on `Ctx::secondaries` flies bit-identical on the whole frozen digest
record (13 cases × 4 schedules, wave and burns included), deletes 65-83% of the secondaries
calls in every flown regime including the belt's kick wave (hit 0.65 against 5ade's 0.029 on
the spread belt), and halves the view's one-gather cost (2038→1010 µs at 10⁵) — adoptable as
shipped, scoped as a read-stream lever, not the kick's cure.

## Bottleneck

The board's live question 3 (the kick, 75-160 µs against ~50 ns) and the read-stream page's own
convergence: two same-window censuses (5eb2, 6671 — the page's standing conflict) measured
64-90% of the per-event sources rebuild sharing its `(doll, tick)` key with 0 bit-conflicts,
and both named the same open direction: adopt the memo, "the cheapest item on this page".
Nobody had flown it; 5ade's spread-belt counter-case (hit 0.029) was unresolved. Gain: not
10× on the kick (5eb2 priced the rebuild at only ~13.5% of the kick's calls); the 10×-class
gain is on the read stream itself (65-83% of calls deleted; the view gather halves) and on
closing the page's adoption question with one flight instead of two more censuses.

## Evidence

All numbers from `out/` via `regen.sh` (≤ 13 min: digests ~6 min, 12 flights ~4 min). Linux/x86,
8 vCPU shared: wall numbers are orders of magnitude and within-window paired deltas only.

1. **Bit-identity (the correctness proof).** `ladder_digest`, all 13 cases × 4 schedules
   (1/4 threads, 3 budgets): every digest, kick, encounter and contact count IDENTICAL with
   `ES_MEMO=1` and without (`out/dig_off.txt` vs `out/dig_on.txt`; the only diff lines are the
   `[x s]` wall annotations), and the OFF arm reproduces the frozen record
   `artifacts/runs/nladder/ladder_digests_wave.txt` exactly, the two wave cases included
   (df0e87…, d2632d…, kicks 32537/34537). The patch with the arm off is pristine bits.
2. **Hit rates (memo: lines).** coast rtf600 10⁴: **0.793**; coast rtf1800 10⁴ (the crest):
   **0.826**; burn rtf600 10⁴: **0.768**; 10⁵ rtf100 pre-wave: **0.751**; 10⁵ rtf1000 through
   the belt's kick wave (20,000 game-s, the wave at 13,000-14,500): **0.646** cumulative.
   No flown regime is anywhere near 5ade's 0.029.
3. **Wall, within-window pairs (OFF→ON).** 10⁴ coast rtf600: engine p50 1.616→1.344 ms (rep
   window 1.251→1.158; across-window OFF noise ±22%, so within-window deltas only: −17% and
   −7.5%), p99 11.60→10.32, over 3→0; crest rtf1800: p50 5.295→4.863, over 5→1; burn: p50
   1.119→1.078; 10⁵ rtf100: p50 0.025 flat (pre-wave quiet), rtf1000 wave: 4.378→4.132.
   **The view's one-gather cost halves in every pair**: 203.8→103.3, 211.7→105.9, 236.3→106.0,
   202.6→103.4, 2076.9→1045.4 µs (the view's `force::field` reads ride the same memo,
   `observe.rs:145`).
4. **Honesty notes.** (a) In wall-budget flights the ON arm presents slightly more game-time
   (it is faster), so per-game-second rates differ ~2% between arms (7.18 vs 7.36e-5 kicks/B/gs
   in the wave arm) — canonical cuts prove the outcomes identical (evidence 1); the p50 deltas
   are if anything conservative (ON resolved more events per frame). (b) The memo's entries
   counter confirms the map is cleared per frame (entries ≈ misses at 10⁵ ≈ 1.1×10⁵, ~33/frame).
   (c) `threads=4` digest arm: no deadlock, no divergence.

## Predictions

`predictions.md` was written before the flights. Scored: (1) digest identity HELD, including
the OFF-frozen-record control; (2) steady-plane hit 0.55-0.9 HELD (0.79); (3) crest 0.85-0.9
PARTIAL (0.826, at the band's edge); (4) burn HELD (0.768); (5) the wave adjudication HELD in
direction but not in extremity — I predicted bimodal with a post-wave collapse toward ≤0.1;
measured 0.646 cumulative over a flight that includes 5,500 post-wave game-s, i.e. no collapse
visible at this dilution. 5ade's 0.029 is not reproduced by the shipped comb at any flown
regime; its regime (a differently-keyed memo, or a longer post-wave horizon) remains the one
open case. (6) threads HELD.

## What would make it wrong

- A source rebinding between two same-tick events without the generation bump catching it: the
  bump sits in `Universe::apply`, the one place a body's plan changes (the doc comment's own
  contract); the burn and key-mashing digest cases are exactly the player-between-belt-events
  case, and they hold. A regime where bindings change outside `apply` would break it — none is
  known in the crate.
- The `except` normalisation (test particles share entries) is only sound because a test
  particle is never in `sources[d]`; if a body could be a source of a doll it does not sit in,
  the normalisation would need the `contains` on that doll's list only — which is what it does.
- The wall numbers are one shared box, ±22% across windows; only the paired deltas and the
  view-gather halving (6/6 pairs) are claimed as signals.

## Cost of adopting, and fit

a 153-insertion patch across `crates/universe/src/{ctx,universe}.rs` and the
nladder example (a third of it the example's Linux port and the stats print; the engine change
is the `SecondaryMemo` in ctx.rs plus 25 lines in universe.rs), env-gated `ES_MEMO`, default
off = pristine bits, proven by evidence 1: a `Mutex<HashMap>` lookup per
`secondaries` call and a per-doll generation bump in `apply` when a source rebinds (planets
rebind at their own cadence, so the bump is rare). Deletes 65-83% of the calls whose mass is
3×`state_of` each. PRINCIPLES: #1 ("the cheapest compute is compute not done"), #3 ("compute
only surprises... nothing is evolved that can be derived when looked at" — the field at a tick
IS derived-on-demand state re-derived identically), #15 (local law: the memo is per-doll).
It is NOT the kick's cure (the fit owns the kick — 5eb2's pricing stands, and my p50 deltas
agree: single-digit to -17%).

## The lens (SpaceX)

Delete before optimize: this deletes redundant reads instead of making them faster, and the
patch ships with its own negative control (arm off = frozen record). What the lens may have
made me miss: the memo is a cache, and caches are state — the generation bump is the one-way
door here, and I tested it only through digests (the strongest instrument available, but a
regime where `apply` is bypassed would be invisible to this run's flights).

## Regeneration

`regen.sh` from the repo root after `work/patch.diff` is applied: digests OFF/ON + diff vs the
frozen record, the 12 flights (6 pairs), and a summary table. ~13 min.
