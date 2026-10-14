Grade: silver

**Abstract.** Claim: the compiled orbit a kick stores is write-only engine memory (the belt's retired tables: 0 flight reads) and exactly its `OrbitKey`, so of 1,806 B/body standing (74.3% derived knots; floor 673) the knots are deletable via the two-word completion. Reproduced: all `regen.sh` numbers; at 3×10⁵ bodies flight reads stay 107–191/frame with identical splits; at 40,000 game-s 2.0 tables/body is steady and regen is exact knot-for-knot for all 300,520 current and retired tables. Correction: an all-path counter finds 56,454 in-flight retired fetches (player's encounter scan, ~1.4/game-s, the cast's, not the belt's): deletion costs ~0.1–1% CPU, not zero. Gain: −37% standing free, ~−60% with kernel; wall 4 GiB@10⁶ → ~1.4–2×10⁶. Cost: one storage-seam build.

## Reasons

**Reproduction.** `regen.sh` exit 0 (runner); `frame_digest` identical pristine vs patched on all 9 flights, 4 schedules each (I re-diffed the saved digests). My independent reruns on the applied patch cross-check: probe at the author's params gives the same flight table (107–191 decodes/frame pre-wave, 2,199,316-flight-read class), gather 10.73 reads/row, cold-gather retired fetches 215,134 — exactly the census's implied cold share of its 309,227 two-gather total. Census at N=3×10⁵ (outside the author's range): decodes/frame 107–191 pre-wave — identical to 10⁵, flat in N; post-wave steady 109–140 (the burst subsides, confirming "read only at their own kick"); held 2.0 tables/body; split 672/670, share 74.3%, floor/standing identical; footprint linear (1,359 MiB = 4,754 B/body); regen 1001/1001.

**Predictions.** `predictions.md` (12:31:21) precedes the decisive `census_1e5.txt` (12:31:43) by 22 s; v2/v3 are re-runs that only extend the instrument (adding the `PARTIAL_RETIRE` print), every overlapping number identical — so the P3 retired-read measurement postdates its prediction. P1 held (and at 3× N). P2 held exactly (670 vs 672; history +100,491 ≈ +N). P4 held and is strengthened: my full-knot check (`PartialEq` on knots, crossings, three increments) passes for **every** current (100,028/100,028) and **every** retired (200,460/200,460; 200,492 at 40k game-s) table — "the cache holds nothing beyond the key" is now closed, not sampled. P3's second half failed as the author disclosed (gather ≥1/row post-wave).

**The adversarial finding that caps the grade.** The author's instrument counts retired reads at ONE call site (`observe::partial`); `binding_at` has seven callers. My counter on the history branch of `binding_at` itself (all paths): **22,605 retired fetches during the author's own 16k-game-s flight**, 56,454 over 40,000 game-s — attributed entirely to the player's encounter-candidates loop (`encounter.rs:180`; `state_of` 0, other 0), where `Scan::compute` then decodes each candidate. The rate is flat across the wave (±0.1%), so the **belt's** retired tables are indeed 0-read in flight — but the dossier's universal sentence "the retired generation is read 0 times in flight… Every retired-table read in the process comes from the view's gather" is false, and "zero CPU cost" is really ~281 recompiles/wall-s at rtf 200 (≈0.1–1% CPU), or one kept exception for the cast. The design survives (`binding_at` recompiles on the rare non-window read — the author's own line anticipated it); the claim as written does not.

**Second correction.** The "≥1 retired read per gathered row post-wave" is the phase peak of a synchronized cadence, not a steady rate: at 40,000 game-s the gather's retired fetches collapse to 2,185 (0.02/row). The author's caveat guessed the direction; the magnitude (100× swing) matters for pricing the completion word's value.


**Goal fit.** Directly on the board's furthest-gap row (bodies in the flyable engine; memory 10^2.6–2.9 over the ≤6 B goal) and on PRINCIPLES #6 verbatim ("Store the generator, not the generated") — the knots are the generated, stored, and (for the belt) never looked at; #3 ("Nothing is evolved that can be derived when looked at"); #1/#24.

**Page.** Faithful fold-in at the right rank; I corrected three overstatements in place (belt-scoped "0 reads" with the cast exception and CPU cost; "≈zero flight CPU"; the gather share as a phase peak with the 0.02/row steady number) and strengthened the regen line to the full-knot result.

**Minor nits (not grading).** Plan heap bytes (~2 items × 16 B/body) are counted in neither standing nor floor (both shift equally; idiot index unchanged at ~2.6×); the census header's own floor (~736) disagrees with the quoted 673; "bit-identically" overstated a counts+totals comparison until my full-knot check closed it; MiB/kB mixing (4.59 KB/body is 4.71 KiB); the ~2×10⁶/~4×10⁶ wall extrapolation shows no multiplier — using the measured marginal (3.7 B footprint per accounted B) it lands at ~1.8×10⁶/~3.5×10⁶, same order.

## The one experiment that would make it gold

Fold the all-path retired counter into the census (my ~30-line patch on `binding_at`, kept as the checker diff), rerun `regen.sh`, and restate the claim belt-scoped with the recompile cost priced (≈0.1–1% CPU or a cast exception) and the wall arithmetic's multiplier shown. No physics changes; every other number already stands, including at 3× N and 2.5× flight time.

## What the author missed

- The player's encounter scan as a live retired-table reader today (the dossier deferred it to "once wired, H0216" — but `PlayerNeighbourhood` is the shipped finder and reads candidates at scan ticks now).
- The gather's retired-read share is cadence-phase, not a constant ≥1/row (100× swing measured).
- A regen check that compares the knots themselves (closed here: exact for all 300,520 tables, current and retired).
- The plan heap in the floor/standing split.
