# Predictions (written before the staggered flights C and D)

The rung: fly the belt's first-kick wave BUDGET-FREE (engine budget 10^6 ms, rtf 100, coast,
seed 1, 60 fps, the page's loop) with ES_STAGGER armed (my rebuild of ed3a's stagger: a ship's
first clock kick offset by a uniform id-derived fraction of one step, ~13 lines, default off),
at N = 10^5 and 3x10^5, against same-box unstaggered anchors. The wiki's open direction 1
(nladder): "predicted peak ≈ 487/16.7 ≈ 29 events ≈ 0.9 ms at 10^5, and the staggered-break
at ~1.4x10^6". The unstaggered anchors on this box class: 487 events / 22.95 ms at 10^5,
1,328 / 71.7 ms at 3x10^5 (1a1c checker, budget-free).

Cases I have NOT tuned on (the stagger hash is fixed before any flight; no staggered flight
has run at the time of writing):

1. **P1 — staggered peak at 10^5 (budget-free):** events/frame peak in [25, 90] and engine
   peak ms < 5 ms (the steady stream ~25 events/game-s = ~42 events/frame at rtf 100, plus a
   spike factor; the wiki's own arithmetic says ~29 events ≈ 0.9-1.4 ms). KILL of the
   flattening's survival: any staggered peak > 200 events or > 10 ms means the 12-ms-budget
   instrumentation was hiding spikes the budget-free dial shows.
2. **P2 — staggered peak at 3x10^5:** events/frame peak in [90, 350]; engine peak 4-17 ms.
   The letter (12 ms) is marginal here: I predict it HOLDS (< 12 ms) but with < 2x margin.
   If the peak exceeds 12 ms, the staggered-break is BELOW 3x10^5 and the wiki's 1.4x10^6 dies.
3. **P3 — the ratio:** staggered peak / unstaggered peak at 3x10^5 in [1/12, 1/4] (the
   16.7x window flattening, measured at frame level, budget-free).
4. **P4 — the wave still completes:** kicks counted > 0.95 N per body by the end of each
   staggered flight (every body's first kick still fires inside the window), dead = 0,
   refusals = 0, player alive.
5. **P5 — off-arm identity:** ladder_digest (13 cases x 4 schedules) bit-identical between
   the pristine binary and the patched binary with ES_STAGGER unset.
6. **P6 — scaling:** staggered peak events/frame scales ~linearly in N between 10^5 and
   3x10^5 (exponent 0.8-1.2), which would put the letter-break at N ≈ 5x10^5 - 1.5x10^6
   (250 events at ~48 us/event); the memory break (1.3-1.6x10^6 at 4 GiB) then lands at or
   before the staggered letter-break, i.e. on THIS configuration the wave stops being the
   binding constraint before the letter-break can be separated from the memory break.
7. **P7 — the unstaggered anchors on this box:** 10^5 peak 380-600 events / 18-28 ms;
   3x10^5 peak 1,100-1,600 events / 60-85 ms (reproducing 1a1c's checker within box noise).
   If the anchors land outside these bands, this box's rate differs and all ratios stand
   but the absolute ms do not (M1 re-measure decides).

Kill criterion for the rung as a whole: if P5 fails (off is not bit-identical), the stagger
implementation is not the record's and every number is VOID pending a fix.
