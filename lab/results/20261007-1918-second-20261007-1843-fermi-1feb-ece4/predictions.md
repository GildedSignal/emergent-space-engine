# Predictions (written before every run of this window)

The experiment the checker named: scar bits per kick measured on the shipped
shipmem store, with kick deltas captured from the plane's own kick path
(`step::process` on the plane, the same replay as `--kick-bench`), replacing the
ladder's synthetic uniform deltas. Then re-derive reabsorption (MB/game-s at
10⁹) and the affordable hot fraction from measured scars + the slice-free
per-body belt rate.

## Capture (plane kick deltas in the belt's column space)

Columns: E Q48 and L Q32 through the shipped `Key::darwin` on both keys
(belt-native quantization), Δt_p in root-doll ticks, Δω in u32 turns.

1. Distinct kicks captured at seed 1, rtf 100, 10 s: 650–670 (the kick-bench
   counted 663 rebinds on the same replay; my loop must land on the same
   number, else my replay differs from the shipped bench).
2. Excluded (unbound passage, darwin range, doll ≠ 0): 10–40 % of kicks
   (leavers rebind through hyperbolic passages; made ships stay bound).
3. Median magnitudes: |ΔE| ~ 2^24–2^38 quanta, |ΔL| ~ 2^20–2^34, |Δt_p| ~
   2^16–2^28 ticks (kick step H = period/64), |Δω| ~ 2^16–2^26 turns. I.e.
   the plane's per-kick deltas are LARGER than the ladder's synthetic ones
   (|Δt_p| ≤ 2^16, others ≤ 2^10), because a real rebind moves periapsis time
   by a good fraction of a step.

## Shelf (belt 2²⁰, perfect program, plane deltas replayed)

4. Scar bits per kick (marginal, steady rounds, sparse rate 1e-4): 80–260
   bits (10–33 B row: 4 changed columns × varint of a 2^20–2^30 delta, plus
   row/sparse-index overhead). The synthetic ladder kick on the same shelf:
   40–90 bits. So the plane's real kicks cost MORE per kick than the ladder's
   synthetic ones — the 16-bit-scar assumption in the silver dossier is
   optimistic by ~5–15×.
5. At a dense rate (1e-2), bits per kick falls as repack amortizes (groups
   repack when scars > half the blocks): 40–150 bits.
6. Reabsorption requirement at 10⁹, belt rate 0.015–0.025 ev/body/game-s:
   250–800 MB/game-s — ABOVE the silver dossier's 37–292 MB bracket (which
   assumed 16–64 bit scars). The H_live term gets worse, not better; the
   ranking compute > H_live > bandwidth is unchanged.

## Record fixes (checker's list)

7. Slice-free belt rate re-measured with `--members 0` on this box: 0.012–
   0.030 per body per game-s (checker had 0.0155; seed scatter 1.4–1.7×).
8. If the capture count (prediction 1) or the belt rate (7) misses its band,
   the bridge from plane to belt is suspect and I say so in the dossier.

Kill criterion for the whole experiment: if ≥ 80 % of plane kicks cannot be
expressed in the belt's column space (darwin exclusions), the belt column
bridge is the wrong representation for this measurement and the result is
VOID, not negative.
