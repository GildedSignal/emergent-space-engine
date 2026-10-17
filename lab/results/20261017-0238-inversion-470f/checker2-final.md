Working...
**Grade: silver** — written to `lab/results/20261017-0238-inversion-470f/check2.md`, with confirmations folded into the run's `wiki/memory-h-live.md`.

**What held (all fresh this session):**
- The runner's regen alone proves the headline: one binary, same seed/args — 40k arm flat at 44.6 MB, r1/r4 grew to 95/99.5 MB by 6,000 gs. The preserved instance matches the dossier to the byte (220,862,318 B / 83,768 allocs at gs 20,000; bulk drop to 5,893; hwm 206,976 kB retained; counters flat; held/pending 0).
- My adversarial flights: **2/4 quiet grew; 8/8 under 8-way load; 8/8 with the counting allocator removed** (not an instrument artifact); **N=1600 (outside every prior arm): 2/2 grew to 327 MB by 6,000 gs** — growth ∝ N, i.e. the multiplier grows on exactly the axis the N ladder is climbing. 20 of 22 fresh flights grew.
- Predictions genuinely pre-registered (02:43 vs 03:28–03:38 artifacts). P2 (slice bill one-time, events 16.5→2/gs) and P5 (counters blind) hold; P1 held on both registered sides; P3 fired its pre-registered "worse class" branch. d3fe's clean rate is dead at shipped size; nladder's named unflown case is answered; the bimodality is new (not in HISTORY, wiki, or git log).

**Why not gold:**
1. P4 is reported "held within ±20%" but the run's own log contradicts it: the first-2,000-gs slope (15.0 kB/gs) predicts ~320 MB at gs 20,000 vs the actual 220.9 MB (+45%).
2. The "~33% quiet" frequency is condition-dependent (0/3 alone per first checker, 2/4 here, 8/8 under load) — "quiet machine" is not a controlled condition.
3. Mechanism un-isolated (author says so; prune-starvation is the open lead).

**The gold experiment:** backtrace the ~78k-allocation bulk drop at 20–25k gs under the deterministic load trigger (8-way concurrent), name the structure, and fence the ladder's CI arm with the census. Zero code change to adopt the finding itself: single-run memory walls carry an unknown 4.7–7.5× schedule factor until then. Tree left as found (patch example files removed; no commits).
