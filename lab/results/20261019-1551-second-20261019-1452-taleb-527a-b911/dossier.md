# Dossier — 20261019-1551-second-20261019-1452-taleb-527a-b911 (second author on 527a)

**Claim.** The interstellar burn ratchet's late channel is now **measured, not inferred**: its
binder is the retention law's `2·light_distance` term itself — freezing that term (an env-gated
control stopping it in both places it appears, the `key_prune` visit key and `prune`'s keep)
switches the ratchet off completely and permanently (census flat to ±50 bindings for 180k
game-s, RSS flat 611–638 MB, while the live arm guard-stops at 1,615 MB with the census at
610k and climbing +25.7k bindings per 10k gs), **freezing either half alone leaves the ratchet
alive** (key-only: 204,864 bindings at 168k gs plus 4a71's every-frame walk cost, max frame
248 ms; keep-only: 116,479), and the byte decomposition splits the guard window: **channel 2
is the larger channel there** (≈1,022 of 1,578 MB = 65%, channel 1 ≈ 472 MB = 30%), because
channel 1 **saturates at 444 MB by 46k gs** — all growth past onset (~118–142k gs) is
channel 2.

**Bottleneck.** The board's memory-at-10⁹ line. 527a left channel 2's mechanism as a one-arm
inference and its guard-window bytes confounded; the checker named exactly this experiment.
It decides what gets built: the retention fix must scope **what** is kept (which bodies the
view reads), not the margin — at 10⁶ bodies a cone-wide keep is ruin by arithmetic on the
measured 1.76 KB/binding, and the level law below prices any candidate fix before it is built.

**Evidence** (all: shipped `nladder`, K=3×10⁴, burn, seed 1, rtf 100, 12 ms, guard
`LADDER_RSS_MB=1600`; binary = 527a's patch verbatim + this run's disclosed probe additions —
per-channel deep counters, the `ES_FREEZE_LD_AT_GS`/`ES_FREEZE_LD_WHERE` retention-freeze
control, `ld0_gs` in the probe; logs in `work/logs/`, analysis in `work/analysis.txt`):

| arm | gs end | census end | hist deep | RSS end | verdict |
|---|---|---|---|---|---|
| A live (no freeze) | 328,274 (guard) | 610,481 | 752 MB | 1,615 MB | ratchets, guard |
| B freeze both terms @30k | 179,299 | 34,188 | 44 MB | 611 MB | **off, flat from ~39k** |
| C freeze both terms @60k | 239,399 | 45,551 | 57 MB | 638 MB | **off, flat from ~69k** |
| D freeze key only @30k | 168,140 | 204,864 | 253 MB | 882 MB | ratchets; max frame 248 ms |
| E freeze keep only @30k | 168,141 | 116,479 | — | 760 MB | ratchets (slower); p99 4.4 ms |

1. **The switch-off (the checker's named experiment).** A/B/C at matched game-time: at 168k
   gs the live census is ~200k bindings and RSS ~875 MB; B sits at 34.2k / 611 MB (flat since
   39k gs), C at ~45.5k / 638 MB (flat since 69k). Post-settle slopes per 10k gs: live
   +25,699 bindings / +31.7 MB hist / +41.9 MB RSS; B −1 / −0.0 / +3.5; C −0 / −0.0 / +0.7.
   Pre-freeze probe rows are digit-identical to the live arm's; refusals 0 in every arm.
2. **The level law.** With the keep frozen at K = 2·ld(T)+330 s, retained-extra = (1.35,
   1.43) × K bindings (B: 4,148/3,084; C: 15,524/10,866 — two runs, K 3.5× apart, one
   constant). The live arm reads 1.5 × K at onset and **rises to 2.3 × K late**: the visit
   key re-keys at each visit with the live distance, so horizons extend as the observer
   recedes — the compounding is measured, not assumed.
3. **The term-split bisect (new, beyond the checker's ask).** Freezing only the visit key
   (D): bodies become visitable but the live keep refuses every drop — census tracks the live
   arm (204,864 vs ~205k at 168k) **and** the re-keyed-at-now+1 bodies are re-walked every
   frame: p99 13.0 ms, max 248 ms (4a71's pinned-prune wall, reached by a different door).
   Freezing only the keep (E): drops would pass but visits still recede ~3× play time —
   116,479 at 168k, unbounded. **Neither half alone suffices; 527a's letter "the drop
   threshold is not the binder — the body is simply never visited again" is refuted in its
   exclusion: both terms carry the binder, the term itself is the mechanism.**
4. **The byte decomposition (one regression, both constants).** Live arm, 155 probes:
   RSS = 64.6 + **1.063·scan_mb + 1.359·hist_mb** (rmse 15.8 MB over a 1,347 MB span). The
   scan counter (deep, deduped) is honest to 6%; the history counter under-counts RSS by 36%
   (per-allocation rounding and deque blocks on ~1.3 KB segments): per extra binding
   **1,295 B deep / 1,760 B in RSS**. Guard window split at RSS 1,578 MB: channel 2
   ≈ 1,022 MB (65%), channel 1 ≈ 472 MB (30%), baseline 65 MB.
5. **Channel 1 corrected, conclusion unchanged.** The capture path re-arms the same
   `Arc<Scan>` while nothing it reads changes: held entries = **×1.99–2.00 distinct captures
   in every arm**. Per-distinct bytes fall as the flight ages (≈6 MB at 24k candidates near
   28–46k gs; 1.5–2.4 MB late) and the channel **saturates at 444 MB by 46k gs** in all
   five arms — it is early-flight memory, not the ratchet. 527a's 1.94 MB/scan divided an
   RSS slope by entries; corrected, the fence licenses ~1.6 GB late and ~4.6 GB at the
   46k-gs worst state (2048 entries ≈ 1,024 distinct), still never engages first (guard at
   held 585 ≪ 2048), and 4447's answer-or-expire + pinned-bytes fix remains the right unit.
6. **Reproduction anchors.** Guard at gs 328,274 vs 527a's 332,277 and 4447's 332,604;
   kicks 8.497e-5 vs 8.498e-5; gap 1.7 s; gt1 saturates at 30,043; hist_max 5,845-shape
   growth reproduced (5,312 at 310k, climbing).

**Predictions** (`predictions.md`, written before each decisive flight). P1 HELD (the
switch-off is total; kill criterion never approached: B settles at 1.14× baseline). P2
**letter-MISSED, law-HELD**: there is no per-wave collapse lag to measure — the visit key
rides the *front* segment's `droppable_until`, so the pre-freeze stock drains within K
frozen of the freeze (B flat by ~39k ≈ 30k+K, C flat by ~69k ≈ 60k+K) instead of collapsing
per wave; the settle time ≈ K matches within probe cadence. P3 HALF-HELD: c1 = 1.06 inside
the pre-registered 0.75–1.25 band, c2 = 1.36 outside it (the deep counter's miss, honest as
measured). P4 HELD (×2 duplication exact; per-distinct 1.5–2.4 MB late — the early 5.5–7 MB
state also measured, at 28k gs). P5 HELD (refusals 0; pre-freeze rows digit-identical;
end-rates 8.34–8.50e-5 across arms of different lengths). P6, P7 (pre-registered before the
split flights) both HELD, including D's frame cost and E's absence of one.

**Commands** (`regen.sh` reproduces all five arms + the analysis, ≈11 min on the lab box;
each arm ≤ 6 min wall, every process ≤ 1.7 GB):
```
cargo build --release -p emergent-universe --example nladder
BIN=$CARGO_TARGET_DIR/release/examples/nladder
ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=700 LADDER_RSS_MB=1600 $BIN 30000 burn 7200 100 12   # A
ES_FREEZE_LD_AT_GS=30000                ES_PROBE_EVERY_GS=1000 ES_WALL_CAP_S=400 ... $BIN 30000 burn 1800 100 12   # B
ES_FREEZE_LD_AT_GS=60000                ES_PROBE_EVERY_GS=1000 ES_WALL_CAP_S=500 ... $BIN 30000 burn 2400 100 12   # C
ES_FREEZE_LD_AT_GS=30000 ES_FREEZE_LD_WHERE=key  ES_PROBE_EVERY_GS=2000 ES_WALL_CAP_S=500 ... $BIN 30000 burn 1700 100 12  # D
ES_FREEZE_LD_AT_GS=30000 ES_FREEZE_LD_WHERE=keep ...                                                        # E
python3 lab/results/<run>/work/analyze.py <five logs>
```

**What would make it wrong.** The freeze control changes what history is kept (a retention
law change under the flag, digests differ by construction): if a live read needed a frozen
dropped binding we would see refusals or digit divergence — none appeared (P5), but the
soundness battery is the coast/arm pre-freeze rows, not the full digest suite. The deep
counters are my estimates of Arc/shape overhead (c2 = 1.36 quantifies the miss); the RSS
regression shares this harness with the counters it validates (agreement is calibration, not
independence — the freeze arms' census evidence is counter-based and independent of RSS).
Timings (p99/max) are load-elastic on this shared box; counts and bytes are not. Unflown: a
far-doll scene (two stars), and the same bisect at 10⁵.

**Cost of adopting.** Nothing to adopt in the engine: the control is a probe, off = shipped
bit for bit. What the measurement buys: the retention fix is now scoped (keep-what-is-read,
not margin-tuning) and priced (1.76 KB/binding; extra ≈ 1.4·λ·(2·ld+330 s) unbounded in
play time), and 527a's fence constants are corrected on the same conclusion.

**Fit with PRINCIPLES.** "we don't want errors that can compound" (#13 — the visit key's
re-key-with-live-ld is a measured compounder, 1.5× → 2.3× and rising); "a fix signals the
wrong representation" (#19 — the keep is cone-wide for bodies nobody reads); "Compute only
surprises" (#3 — a receding observer's unread past is the opposite of a surprise); "the
simulation tells us what's next not us" (#22 — the level law came out of the flights, not
the plan).

**The lens.** Taleb's via negativa: delete the term (in one half, in the other, in both) and
watch what dies — the only deletion that kills the ratchet is the term itself, in both
places. Missed by this lens: the swap-vs-RSS reading on a shared box (I trusted in-process
counters instead — the right call here, but the RSS regression would not survive heavy
swap); and no measurement of what the view *actually* reads (the fix's "what", left to the
view page).
