# Predictions (written before the decisive flights; the 20-s rtf-600 calibrations below tune nothing)

Binary: main 9b0fdb9b + f80a's probes verbatim (print-only + LADDER_RSS_MB guard) + the BELT_SPLIT
lever re-derived from f790's patch (env-gated, off = the shipped tree; f790's checker verified
off ≡ shipped byte-for-byte). Scene: shipped `nladder 30000 burn … 1000 12`, seed 1 (hardcoded),
48 fleet members, 1 thread — f80a/527a's OFF arm exactly.

The question: the cadence split is the belt's measured CPU lever (8×, 7f97/de7b/f790). Is it also a
memory lever? Channel 2 (history retention) ratchets per kick wave; the split stretches the wave
period S=8×. On the compact side, 0659's p = 1.0 makes promotion rate = item rate λ, so τ (the
residency dwell the 8-GB budget allows) should scale ×S — arithmetic, no flight.

## P1 (engagement, calibrating): the split actually defers the belt
At 60k game-s the ON arm's kicks/body/game-s ≈ the locals' stream only (≪ OFF's), because the belt's
first wave moves from ~13–14.5k gs to ~110–115k gs (de7b: 14,072 → 112,574). Falsifier: ON's kick
rate at 60k within 2× of OFF's.

## P2 (the claim): channel 2's post-first-wave slope divides by ≈S
Bindings per body (hist_total / N) grow ~+1 per wave on OFF (f80a: 8.03/body at 174k gs ≈ 7 waves).
ON: the same +1 per wave, waves 8× rarer → slope per 1k game-s ≈ OFF/8. Band: ratio in [4, 16]
(wave-edge placement and the 2²⁶ keep margin eat precision). Falsifier: ratio < 2.

## P3: RSS follows bindings
Post-first-wave RSS slope per 1k game-s divides by ≈S too (same band), and hist_gt1 saturates at the
ON arm's first wave (~all 30k bodies hold ≥1, exactly as OFF's did at 11–16k gs). The OFF arm's own
late slope re-measures f80a's +3.3–4.6 MB/1k gs (instrument match).

## P4 (control): channel 1 is untouched by the split
The scan channel (mints/answers/expired, held=) is player-driven, not kick-driven: its onset
(< 50k gs) and its counters at matched game-s stay in the same-arm load spread between OFF and ON.
Falsifier: ON's held/mints trajectories leaving the OFF band by > 2×.

## P5 (the budget line): the split alone buys ~S× horizon on the memory wall
At matched game-s ≥ 130k (OFF's channel-2 onset), ON's RSS stays below OFF's by more than the
channel-1 saturation alone explains; ON does not reach the 1,600-MB guard before 240k gs, where OFF
projects past 1,250 MB. (f80a's OFF: 900 MB at 174k gs, climbing.)

## Compact-side arithmetic (no flight; constants from 0659's dossier and b911's law)
Promotion rate λ = 3.6–4.3×10⁻⁵ /body/game-s at p = 1.0 → τ = 43.6 game-s (8 GB, 5.1 KB/live) or
171 game-s (1.3 KB/live). With S = 8: λ → λ/8, τ → 349/1,368 game-s; b911's retained-extra
≈ 1.4·λ·(2·ld + 330 s) divides by 8 on the live plane. The contacts arm (0659's checker, τ ≲ 0.02
orbit) is cadence-free and does NOT move. Kill: none of this arithmetic is a flight claim — it is
ledger composition on published constants, and it dies with 0659's p = 1.0.
