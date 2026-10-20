Working...
Check complete. `check.md` written to `lab/results/20261020-1002-fermi-8994/check.md`, the author's wiki page corrected in place, tree restored (only `lab/results/` untracked, no commits).

**Grade: silver.**

**What reproduced (my own runs, not just the runner's):** regen.sh end-to-end exit 0 in 74 s — item-scope 11.35 KB/kick coast @ 91.3% of naive, 15.17–15.19 burn @ 71.2%, 9.13–9.15 at 3×10⁴ @ ~92%; anchors to <2%; waves and neutrality identical. The od-6 decision stands: **the allocation wave is marginal**, f623's OLS attribution is dead, the stream's own marginal (~1.4–1.6 KB/kick) closes the 10⁹ byte row at ~11–23% of 60 GB/s.

**Adversarial arms (mine):** K=10⁵ coast — outside the author's range — holds marginal-not-base at **95.6%**; burn at 3×10⁴ (untested combo) is 91.7% item-carried with burn/coast 1.35.

**The defect that bars gold:** `stats.items` is `[planet, moon, ship, player, fleet]`, and analysis.py divides player traffic by `items[4]` — the **fleet** count (219) — not the player count (5,551). The dossier's "4.90 MB = 490 B/body per player item", "0.5% of the items", the "~490 GB per player item at 10⁹" pricing, and the `with_capacity(doll)` lever are all built on that wrong denominator. Corrected from the run's own logs: **194 KB per player item, K-flat 10⁴→10⁵** (193.4/193.7/194.0) — a bounded ~19 KB/game-s for one player, *not* doll-proportional; the doll-scaled object is the burn's rare full chains (terminus 3,670,016 B at 10⁴, 7,340,032 B at 3×10⁴ ≈ one ~244–366 B entry per pulled body). The tell was in every regeneration: the "constant" silently became 770–787 B/body while its numerator held to 0.04%, because fleet counts vary with schedule and player counts don't.

**Gold path:** one re-analysis flight — fix the class index, de-hardcode 490/10028/3670016/2.27, add one seed; I flew the K=10⁵ and 3×10⁴-burn halves already.
