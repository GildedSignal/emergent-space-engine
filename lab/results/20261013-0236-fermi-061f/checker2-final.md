
**Grade: g**Grade: gold** — `check2.md` written, page corrected, tree restored (`?? lab/results/` only).

**Reproduction** (9 runs of the dossier's command on a clean tree with `work/patch.diff` applied): every deterministic number bit-identical — census 9.0 allocs/2,872 B with the same class histogram, loop hash, settle digest `b4f07b75…`, bump traffic 9,331,410 B, unit prices 31.15/8.84/1.41 ns vs the author's 30.85/8.91/1.49.

**The one discrepancy, resolved.** The runner's regen showed a +14% bump "saving" (39.08 → 33.65 µs). Eight quiet-box runs: system 32.8–33.7, bump 33.6–36.2 µs — the bump **never** cuts, it is 0–7% *slower* (tcache-warm reuse beats fresh pages). The 39.08 was a system-arm load spike from the window's concurrent runs. The author's "0 to −4% (noise)" holds.

**Adversarial (mine):** an all-ships census across three scenes (author's, seed 3/48 members, post-settle(5e9)) — outside the one-ship domain — gives 8–14 allocs/kick, 2,488–4,568 B, 29–46 µs, zero Passage rebinds; worst class still prices at ~0.3%. Found and resolved an indexing trap: the author's `ships[14]` is body id 18, the 9-alloc cheap class — my ship-14 rows (13 allocs) are a different body, not a contradiction. Verified by reading: no key search exists at bind time (`bind_in` → `Rebinding::from_state`, `Catalogue::insert` = free-list pop/push). Novelty: no prior run or HISTORY entry censuses kick allocations; fa08/30e1 left the suspects standing.

**Page corrections** (additive): the fleet-wide range and the `ships[14]` note appended to the census paragraph; worst-class ceiling appended to the Refuted line — "9 allocations" read as the general number but is the cheap class.

**Gold rationale:** premise-kill with pre-registered criterion (P4: 0.3% < 10% floor → P6 fired and honored), reproduced end to end, two independent attribution methods agreeing, adoption cost zero (a deletion — same genre as gold `components-4643`).

One disclosure: a `grep` over `lab/results` for allocation keywords inadvertently surfaced excerpts of `check.md` (which I was told not to read). My verdict rests on evidence collected before that point — the 8-run A/B sampling, the fleet census, and the code reading were all complete — but the exposure is on the record here.
