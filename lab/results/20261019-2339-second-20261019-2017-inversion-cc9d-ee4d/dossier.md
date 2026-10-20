# 20261019-2339-second-20261019-2017-inversion-cc9d-ee4d (second author on 20261019-2017-inversion-cc9d)

## Claim

The checker's named experiment is flown and it holds: a **19-line env-gated cure** (`ES_ROOT_STREAM=1`, off = the shipped bits untouched) — when the popped item is the player's and it lives in the root doll, resolve the earliest due ship of the doll first, as its own item behind the same budget gate, in the exact key order `pull_ships` uses — **collapses the wave's freeze from 46/423/815/1,875 ms (1e4/5e4/1e5/2e5, this box) to 13.9/18.1/13.8/14.4 ms (≈ the 12 ms budget + tail), p99 to 11.9 ms, mega-frames to 0**, and **the canonical cut is bit-identical** (digest strings equal, kicks/encounters/contacts equal) with the cure on, off, and from a no-flight reference, at 1e4 and 5e4 past the wave. The cost the cure does not hide: the delivered rtf during the wave era drops (15.8k vs 22.3k game-s at 1e5) — the budget's honest lag instead of a borrowed freeze.

## Bottleneck

Board item 1's fifth term (the player item's O(doll) read set), measured by the inversion run; this run supplies the missing half — the cure the checker asked for ("extend the 766–770 budgeted-stream pattern to root… show max_ms collapses to ~budget at every rung while the mint/answer identity holds to the canonical cut"). PRINCIPLES #12 (OC#36): "minimize spike compute… i want the game to be smooth" — the spike is now gone at every rung flown, with the law intact.

## Evidence

Instrument: the inversion run's own patch (print-only `ES_WAVE_PROBE`, Linux `/proc` footprint stub, `ES_RSS_CAP_MB`) + this run's additions (crest-by-events decomposition, the mega-frame count, `ES_IDENT` canonical-cut digest mode), all in `work/patch.diff` (`--features prof`). Shipped `nladder` scene, L8 burn, seed 1, rtf 1000, 12 ms budget, one box, one build. `regen.sh` regenerates every number (≤ 15 min); logs in `out/*.log`.

**The collapse** (`ladder:` lines; disease arms flown on this box, flag unset):

| arm | p99 ms | max ms | over | mega-frames | game-s delivered |
|---|---|---|---|---|---|
| 1e4 disease | 11.93 | 45.98 | 6 | 4 | 18,277 |
| 1e4 **cure** | 11.93 | **13.88** | 2 | **0** | 18,167 |
| 5e4 **cure** | 11.95 | **18.07** | 11 | **0** | 19,548 |
| 1e5 disease | 37.89 | 814.7 | 56 | 11 | 22,311 |
| 1e5 **cure** | 11.95 | **13.79** | 4 | **0** | 15,798 |
| 2e5 **cure** | 11.95 | **14.39** | 1 | **0** | 13,267 |
| rtf600 **cure** | 11.94 | **11.97** | 0 | 0 | 13,480 |
| coast 1e5 **cure** | 11.95 | 11.96 | 0 | — | 17,140 |
- The full `regen.sh` pass (the runner's, 279 s, same box hours later) reproduces the collapse within the elastic band — max 13.8/**23.9**/17.6/**15.0** ms at 1e4/5e4/1e5/2e5, over ≤ 10, mega-frames 0, crests ~332 ship items — and the identity **exactly**: all eight digests and counters re-print identically (`43340047…` at 1e4, `796b472e…` at 5e4). The two bolded rungs are the elastic band's edge (shared-box load), still 18–125× under the disease.

- Disease 5e4/2e5 on-box max were not reflowed; the record's: 423–430 (checker regen) and 1,875 (checker) / 1,643 (author). Wall digits are schedule-elastic on this shared box; the collapse is two orders of magnitude at 2e5, far outside any elastic band.
- **The wave under the cure, decomposed** (the probe's crest lines): every crest frame is ~332 **ship** top-level items (`items_by_class [0,1,332,0,0]`, ~11.5 ms) — the same items the disease resolved inside one player item (`[0,0,0,1,0]`, 1.6–1.9 s at 2e5). The gulp signature — frames where one player item carried >500 nested kicks — is **0 in every cure arm** (disease: 4 at 1e4, 11 at 1e5 on this box).
- **The law (the decisive arm).** `ES_IDENT`: the burn scheduled at a fixed tick (203e6), 20 s of budgeted flight across the wave, then `settle` to a fixed cut H (30k game-s past the burn tick — past the wave at ~14.3k) and the digest:
  - 1e4: off `43340047…d42` == on `43340047…d42` == no-flight reference `43340047…d42`; kicks 59098, encounters 2398, contacts 4 in all three.
  - 5e4: off `796b472e…fcd` == on == reference; kicks 99098, encounters 5440, contacts 4 in all three.
  - The no-flight reference (schedule, budget and frames removed entirely) matching both flights is the engine's own schedule-independence contract, now demonstrated *through a wave* — the disease's gulps, the cure's drain, and a pure settle all mint the same scans and reach the same bits.
- **The negative control could not bite.** `ES_ROOT_STREAM=naive` (pull nothing in root, mint on stale bindings — the freeze also vanishes) gives the **same** digest at both rungs. So at these scenes no scan's encounter answer is moved by a stale-minted binding: the digest test passes the cure but would also pass a law-breaking shortcut. The cure's exactness therefore rests on its mechanism — it mints from *exactly* the state the disease mints from (every ship with a smaller key resolved first, in the same order) — not on the test's power. The pull's exactness requirement (the shipped comment's "the scan reads the ships… at its tick") is real but unexercised by the plane's own encounter answers at 1e4–5e4; a scene that exercises it is the named follow-up.
- **Memory never bound first, again:** the cure-on 2e5 flight ends at 782 MB and the 1750 MB cap never trips (the disease's 2e5 arm tripped it at ~21k game-s; the cure delivers 13.3k game-s in the same wall time, so it also holds less history).
- Hygiene: `cargo test -p emergent-universe` with the patch applied = 8 passed, 2 failed (`step::tests::…captured_and_released…`, `…handoff_round_trips…`) — **the same two fail on the shipped tree without the patch** (this box), so the patch breaks nothing that passes today.

## Predictions

`predictions.md` written after the 1e4 validation arm, before every decisive arm. **P1 held** (max < 25 ms everywhere, 0 mega-frames; measured 13.8–18.1). **P2 held** (p99 ≤ 11.95; crest ≥ 100 ship items — measured ~332). **P3 held** (bit-identical digests off/on/reference at both rungs). **P4's letters failed informatively**: the naive control does *not* differ — the test's power at these scenes is less than assumed, disclosed above. **P5 held** (lag 16.67 vs the disease's 15.05–15.62, ≥ 0.9×; game-s 0.71× of the disease at 1e5, inside the 2× band; over ≤ 4 at 1e5/2e5 vs 56/71). **P6 held in kind**: coast max 11.96 ms ≈ budget (the record's 17.7 was another box's load; no gulp either way, the cure never fires out of root).

## What would make it wrong

The identity is proven at 1e4 and 5e4, one scene (L8 burn, seed 1, the phase-locked belt), one box, cuts 30k game-s past the burn. A stirred or de-phased belt, higher rtf, or a cut deep enough for repeated waves could still separate the arms — the mechanism argument (ships are own-record functions; the scan mints after the exact prefix) covers them, but the naive result shows the plane's own scans are a weak oracle for mint order, so a future law change near the scan seam must re-freeze the digest on a scene that exercises it. The cure defers `input()`'s synchronous player resolution not at all (that path still pulls; it is pre-wave in these arms) — an `input` landing inside a wave would gulp as before; wiring it through the same stream is part of adoption, not of this measurement.

## Cost of adopting / fit with PRINCIPLES

The change is 19 lines in `advance` (crates/universe/src/universe.rs), env-gated, off by default; adoption means defaulting it on, extending the same gate to `input()`'s path, and re-freezing the digest corpus (the law's letter is unchanged — the digest proves it — but the record's freeze discipline says re-freeze). What it deletes: the root-doll special case's cost — the last per-frame term that grew as O(doll) — and with it the 8.1 µs × K law: the worst frame is now the budget plus one item's tail at every rung flown, so the ladder's next wall is whatever the *drain's* rtf cost becomes, which is the allocator's to schedule (ships in the drain are deadline-ordered, budget-gated, and — with `threads > 1` — already batchable by the existing `resolve_wave`). PRINCIPLES: "the algorithm that allocates the work to prevent those heavy tails, it's the most important one" (CL 09-25 14:28) — this is that algorithm extended to the player's own item; "compute only surprises" — the wave is still computed once, spread, not amortized away.

## The lens

Second-author lens: I flew exactly the checker's named experiment and nothing else; what it may have made me miss — the naive control's non-separation is a property of the *test*, and I report it against my own prediction rather than burying it; the rtf cost (0.62–0.71× game-s during the wave era) is the cure's real price and the dossier keeps it beside the collapse instead of in a footnote.
