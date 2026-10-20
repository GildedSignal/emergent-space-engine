# Predictions (written 18:41, before the decisive flight A1)

Control C0 (5e4 coast rtf 1800, 4.27 eras, 34 s) already flown to anchor the instrument:
comb structure matches the record (first kick comb gs 14.2-15.7k, 0.96 kicks/body; boundary comb gs ~29.1k;
second kick comb gs ~42k; live 127->242 MB; held_max 209; cat_live constant 50,076).
The record's longest belt flight is ~9.5 eras (267k gs); every 1e9 composition extrapolates
constants measured within 8 eras. The decisive flight A1 flies 1.0M game-s ≈ 35.8 eras
(≈ 21 min of Julien's play at rtf 400) on shipped bits, print-only instrument.

Held-out predictions for A1 (`longflight 50000 coast 556 1800`):

- **P1 (the ratchet — primary).** Live counting-allocator bytes keep growing with comb
  index beyond era 2: sustained >= 2 MB/era on average through era 30 (a memory ratchet:
  ~130 B/body/era at 5e4; at 1e9 that is ~130 GB/era if linear). Kill bar: average growth
  over eras 20-35 < 0.5 MB/era (saturating => the ratchet is bounded and the failure mode
  is cleared for the coasting belt).
- **P2 (the comb's fate).** Belt kick-comb arrivals (kicks inside the comb window /
  bodies) continue to decay past era 8 (record: -26% by era 8) but floor above 0.4/body:
  era-30 arrivals in [0.4, 0.8] of era-1. If they decay below 0.2 the comb is a dying
  birth transient and the "recurring floor forever" framing on the page dies.
- **P3 (cost drift).** Served ship-class µs per event inside comb windows stays within
  ±25% of C0's era-1-4 level through era 35 (no super-linear drift from growing history).
  Kill: monotone growth exceeding +50% by era 30 (a new era-count-dependent cost term).
- **P4 (the held queue).** held_max stays below the 2048 latch and per-comb held peaks
  show no monotone era trend (O(100-200) like C0). A monotone climb with era = the scan
  queue going unstable at long horizon (new finding; b8e2's utilization law read on the
  time axis).
- **P5 (shipped counters).** cat_live constant, dead = 0, bytes_per_body constant. If
  bpb grows with era, the dashboard itself sees the ratchet (would contradict 470f's
  "shipped counters flat" at 9.5 eras).
- **P6 (safety guard, disclosed).** Self-imposed: flight breaks if RSS > 1.7 GB
  (machine cap ~2 GB shared). Not a law.

Delivery caveat, disclosed: at rtf 1800 the frame loop runs the budgeted-drain regime
(worst frame 15.3 ms in C0 vs the ~277 ms gulp class at rtf 400), so worst-frame columns
here measure the drain ceiling; counts, arrivals and memory are game-lawful and
delivery-independent (digest-path aside, which this run does not compare across arms).
