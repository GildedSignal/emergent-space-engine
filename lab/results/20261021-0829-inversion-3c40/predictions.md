# Predictions (written before any flight past 25 s of page time at the 7e5 rung)

## The setup

The scoreboard's certified top rung ("10⁶ keep smooth flight for 20 s", N1, f416ea93) is a
**short-flight certificate**: at rtf 100, 20 s of page time ≈ 2,000 game-s, which ends ~420 gs
after the player's SOI switch (~frame 948 ≈ 1,580 gs) and ~7× before the belt's first kick-comb
era (~14k gs ≈ 140 s page). The wave behind it was measured at 1e5/3e5 (03f4: 704.7/2,395.3 ms
worst frame) and the burn-mode memory ratchet at 1e4/3e4/1e5 (4447, gold: slopes 5.7/16.3/42.8 MB
per 1k game-s, ~K-proportional, onset at the SOI switch). Neither was flown at the certified
rung class. This box caps a process at ~2 GB, so the certified rung itself (10⁶ = 2,346 MB on
Linux, 03f4) does not fit: **7×10⁵ bodies (700,028; ~1.65 GB baseline) is the largest flyable
rung class here**, one decade above 4447's top arm and the closest point to the certified rung
this machine can hold. The M1 re-measures at 10⁶.

Shipped default dials throughout (no ES_STAGGER_GS, no TTL fence, no ES_ROOT_STREAM — all law
changes awaiting their digest re-freeze, nladder od 5). rtf 100, 12 ms budget, seed 1, 1 thread,
L8 burn from 1 s where noted. Harness: the shipped `nladder` example + a cfg-gated Linux port of
its macOS-only footprint instrument (03f4's named, still-unfixed 6-line gap) + a memory guard
(ES_NL_GUARD_MB) + window telemetry (print-only). No engine change; the macOS path is untouched.

## Held-out predictions

- **P1 (the certificate juxtaposition).** The shipped 20-s gate at 7e5 **burn** still reads
  F1-class after the first second (no frame over 12 ms; worst lag small but > 0 on Linux, 03f4's
  caveat) — the certificate passes with the ratchet already lit (the SOI switch is at 15.8 s).
- **P2 (the ratchet at the certified rung class).** Burn 7e5, guard 1,900 MB: past the SOI
  switch RSS climbs monotonically at **180–330 MB per 1k game-s** (4447's per-body law
  2.6–4.7×10⁻⁴ MB/1k gs × 7×10⁵) and the guard trips **within 2.5k gs of the switch** (≤ ~42 s
  page, ≤ 2.1× the certificate horizon). Falsifiers: slope < 60 MB/1k gs (the K-law dies at the
  top rung), or no monotone climb.
- **P3 (control, one decade down).** Burn 1e5, same harness: slope **30–55 MB/1k gs** (4447's
  42.8 class). If my instrument reads a different law than 4447's, every number above is VOID.
- **P4 (the wave at the certified rung class).** Coast 7e5 through ≥ 2 comb eras: the first era
  (~14k gs ≈ 140 s page) carries ONE worst frame of **4.5–7 s** (03f4's 7.05–7.98 µs × K law).
  Falsifiers: worst < 1.5 s (the unstaggered law collapses at the top rung) or > 12 s
  (super-linear: 7da3's corrected ≈ 6×10⁵ break biting early).
- **P5 (coast memory at the top rung).** Peak footprint through 2 eras stays within **+500 MB**
  of the build baseline (channel-1 churn bounded; no monotone growth past era 2). Falsifier: a
  monotone coast climb ≥ 100 MB/1k gs (never measured, would be new).
- **P6 (the order of the walls).** Under burn, the guard trips before the first comb era is
  reachable (~2k gs ≪ 14k gs): at the certified rung the walls are disjoint in time — burn =
  memory inside the first minute past the certificate; coast = one multi-second frame at ~7×
  the certificate horizon.

Machine state recorded per run (loadavg, free) as the rules require; the box is quiet at the
start (load 0.03, 8.5 GB free).
