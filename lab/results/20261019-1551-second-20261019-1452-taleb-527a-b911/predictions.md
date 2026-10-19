# Predictions — b911, second author on 527a (written before the decisive flights)

The checker's named experiment: a channel-2 bisect with byte decomposition at 3×10⁴ past
130k gs — per-channel byte counters, crossed with the visit key's `2·light_distance` term
frozen. Arms (all nladder K=3×10⁴, burn, seed 1, rtf 100, 12 ms, guard 1600 MB):
**A** live (no freeze) to the RSS guard, **B** `ES_FREEZE_LD_AT_GS=30000`, **C** `=60000`.
The freeze snapshots every body's light distance once (at T) and stops the retention terms
there (`key_prune`'s visit key and `prune`'s keep); physics, views, scans and fleet deadlines
keep the live distance. It is a control, not a candidate law (it drops history the live cone
would keep; digests differ under the flag by construction).

Mechanism under test (527a's inference): channel 2's late ratchet is the retention law's
`2·light_distance` term growing as the observer recedes, so histories are never visited with a
passing threshold. Recession measured by the probe's own `ld0_gs` (the star's light distance):
≈ 420 s at departure, slope ≈ 0.108 s/s mid-flight.

- **P1 (switch-off).** In B and C the history census's per-wave growth collapses back to its
  baseline within `K_T = 2·ld(T) + 330 s` after each kick wave; the live arm A keeps its
  +~30k-per-wave ratchet through the same window (onset ~95–130k gs). Wave map (d839): kick₂ at
  ~41–43.5k gs, kick₃ at ~69–72k gs, wave gap ~27.6k gs. Predicted collapses: B's kick₂
  retention at ~48–51k gs; C's kick₃ retention at ~82–86k gs (K_30k ≈ 7.2k gs with
  ld(30k) ≈ 3.4k s; K_60k ≈ 13.7k gs with ld(60k) ≈ 6.7k s).
  **Kill:** if a freeze arm's census does not fall to ≤ 2× its pre-onset baseline by
  (wave + K_T + 5k gs), the `2·light_distance` term is NOT channel 2's binder and 527a's
  mechanism is refuted (its growth measurement would stand, its mechanism would fall).
- **P2 (the lag is the law).** The measured collapse lag (wave end → census trough) matches
  2·ld(T) + 330 s within ±3k gs (wave width + probe cadence), with ld(T) read from the frozen
  probe trace; the two arms' lags differ by ≈ 2·(ld(60k) − ld(30k)) ≈ 6–7k gs. If the lags
  are equal instead, the freeze works some other way and the mechanism story is wrong.
- **P3 (byte constants from one regression).** On A's probe series, rss_mb regressed on
  (scan_mb, hist_mb) — both deep counters, deduped by pointer — gives coefficients ≈ 1
  (accept 0.75–1.25: allocator slop, my 48 B shape-header estimate, swap-out noise on this
  shared box). A coefficient < 0.5 discredits that counter and the attribution fails.
- **P4 (distinct scans; 527a's per-scan constant corrected).** The capture path re-arms the
  same `Arc<Scan>` while nothing it reads changes, so held ENTRIES ≈ 2× DISTINCT captures and
  the per-distinct-scan bytes ≈ 5.5–7 MB late (the candidates' window widens with recession;
  smoke: 49 distinct of 96 held, 5.98 MB/distinct at 28k gs). 527a's 1.94 MB/scan divided an
  RSS slope by entries; the fence arithmetic (SCAN_BACKLOG licenses GBs, never engages first)
  survives with corrected units: 2048 entries ≈ ~1,000 distinct ≈ ~6 GB at 3×10⁴ late.
- **P5 (the control breaks nothing observable).** Freeze arms finish with refusals 0 and
  kicks/events rates equal to A's at matched game-time (forgetting changes no outcome).
  Refusals > 0 or a material rate change means the frozen control cut a live read: report it
  and treat that arm's census evidence as unsound.

Instrument notes: `hist_mb`/`scan_mb` are in-process exact counts (load-independent); RSS is
the load-elastic readout. The census (hist_total) is the ratchet's instrument, not RSS.

## Added before the term-split arms (flown after A/B/C, before reading them)

The freeze above stops the term in BOTH places it appears (the visit key and the keep).
527a's letter says "the drop threshold is not the binder — the body is simply never visited
again". The mechanism says both terms carry the same `2·ld` and either alone keeps the
ratchet alive:

- **P6 (key-only freeze, `ES_FREEZE_LD_WHERE=key`).** Keys become visitable, but at each
  visit the live keep refuses (before = now − 2·ld_live − 330 is deep in the past while the
  observer recedes), nothing drops, and the body re-keys at now+1 — visited every frame,
  dropping nothing. Prediction: the census ratchets like the live arm (hist_total > 150k by
  160k gs), with the every-frame re-visit showing as a frame cost (p99/max ms up).
- **P7 (keep-only freeze, `=keep`).** The threshold would drop if visited, but the visit key
  still rides the live 2·ld and recedes ~3× play time — never visited, never dropped.
  Prediction: ratchets like live; no frame cost.

If either arm alone goes flat, the two terms are NOT equivalent blockers and 527a's letter is
half right; report which.
