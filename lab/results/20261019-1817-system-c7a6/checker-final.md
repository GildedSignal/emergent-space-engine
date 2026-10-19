Working...
Check complete — `check.md` written with **Grade: gold**, and two overstatements corrected on the author's wiki page.

**What I verified:**

- **Reproduction.** The runner's regen (exit 0) regenerated every load-bearing digit within 0.2%: 7,268,353 reads / 20,649 history (0.28%) / deepest 5,276.5 gs / keep_med 105,339 / 272,324 segs (9.07/body) / 20.0× keep-over-demand; coast 5,271.3. Wall-clock truncation explains the residue. Code audit: `probe_keep_ticks` is verbatim the law at `universe.rs:1247`; `light_distance` is one leg; keep_min=331 for the player = 2²⁶ ticks exactly; every history read demand passes through `binding_at` (all six call sites grepped), `bindings_of` is writer-side only — the census sees every reader, and it is counters-only.
- **Adversarial arms of my own** (`work/adv*.log`): **coast+view60** (never flown by the author): the lawful leg is *constant* (max 3,153.7, p50 1,230.6 = the belt's ld), probes past it reach 17.8k, return None against a 1-segment stock, bracket down — every gather still delivers all 30,046 emitters. **N=10⁴ burn** (a rung outside the author's domain): the 5,271.0 constant reproduces at the same ramp site and nearly the same game-time (gs 84,668 vs 84,740 — a game-time-keyed event, not load), keep/demand 9.7× and growing. View at 10 Hz: partial, consistent.
- **Predictions.** Pre-registered with falsifiers; P3/P4 held exactly; P1/P2 letter failures (β misestimate, cadence-slack overshoot) reported by the author himself.
- **Novelty.** The record (4447, 527a, b911, e181, f80a on `nladder.md`; memory-h-live) is entirely supply-side; this is the first demand census, and it explains b911's freeze result while going further (constant floor, one leg in game).

**Page corrections (in place):** the f80a-digit citation (8.03/body@174k is f80a's rtf-1000 digit; this run reads 7.01 there — cadence-coupled, wave-saturation shape does reproduce), and "the second light leg is read by nobody" → probe *attempts* pass two legs and return None; no read *returns a binding* beyond one leg + cadence slack.

**Why gold:** premise shown wrong (two legs paid, one read, none headless) on the memory-at-10⁹ bottleneck, killing the channel-2 half of the fence line f80a's gold left open; adoptable in one line; integers decide. Missed items (claim-line overstatement, arm B's non-regenerable p50, arm D absent from regen.sh, the un-derived 5,27x constant) are listed in check.md.
