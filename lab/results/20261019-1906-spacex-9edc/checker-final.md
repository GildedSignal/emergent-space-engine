Working...
Check complete. **Grade: silver** — written to `lab/results/20261019-1906-spacex-9edc/check.md`, with two in-place corrections to the proposed `wiki/kick-cadence.md`.

**What held:**
- **Reproduced.** Applied the patch to base 07bc5379 myself; the runner's regen and my own flights agree on every zero. Truncation-load deltas on arms B/C (+6–10% fired counts) change no result; the 2,037,393 total checks against the per-arm sums.
- **Instrument sound.** `OrbitKey` is quantized invariants with derived `Eq` — no unique ID or phase, so 0-same is a measurement, not an artifact. Off-arm reads zero, `self_ok=1`, pre-wave control clean. Predictions were pre-registered; P1/P3 died honestly against the pre-registered kill criterion, P2/P4 held.
- **Three adversarial arms, two outside the author's range:** seed 3 (437,733 fired, 0 same), **burn** — the regime the author never flew (467,610, 0), and **10⁵** — the decade the author called the box cap (625,270, 0; 496 MB peak). The claim now covers 10⁴–10⁵, three seeds, coast and burn.

**Why not gold:** the killed direction was already substantially dead in the record — gold efd4 (17 Oct, memory-h-live) measured 0.4% standing duplication on a ladder belt and "exact keys never recur on distinct kicks"; this page itself held "zero reuse" for the plane (c01c, 0c44). The run's real additions are the consecutive-mint census at 2M kicks on nladder proper, the insert accounting, and the information-bill framing.

**What I corrected in the page:** `cat_live` is a free-list slot count and cannot show key privacy (insert has no lookup); and "the duplicate-mint delete is dead" is now scoped to the stirred belt — efd4's flown intern hits 99.6% under co-orbital concentration, a case this run never flew. That formation arm plus the `BELT_SPLIT` flip-fraction pricing is the one experiment to gold.

Tree restored to clean at base; my arm outputs kept in `work/chk_*.txt` as the reproduction record.
