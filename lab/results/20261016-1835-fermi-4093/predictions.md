# Predictions (written before the flights)

The question: the kick-cadence page's budget paragraph (a4ed, gold) says "year-scale belts
already pass 10⁹ at 10× real time even at today's 29 µs per kick". Re-derivation says that
holds only under an own-period clock the shipped code does not use. The flights below anchor
the three constants of the re-derivation on this box and test one thing nobody has measured:
whether the delivered event rate is invariant in rtf (the engine has a 12 ms/frame budget;
`Budget.until`), which every ledger extrapolation by rtf — mine included — assumes.

Flights (shipped `nladder` example, coast, 20 s wall, budget 12 ms):
- A1 `100000 100` — control: rate ≈ 3.3–3.6×10⁻⁵ ev/B/game-s (a9d7 gold, b30b), kick cost
  ≈ 30–60 µs x86 (12db's 34.8 µs median), standing ≈ 4.8–5.1 kB/B (b30b plateau).
- A2 `100000 600` — same at 6× pace; the control must be game-second-invariant.
- B1 `300000 100`, B2 `300000 600` — N-invariance of all three, still under the 2 GB cap.
- B3 `300000 1800` — held-out: at rtf 1800 the belt stream needs ≈ 3.5e-5 × 3e5 × 1800 / 60
  ≈ 315 k events/frame × ~35 µs ≈ 11 ms — at the budget's edge.

## Held-out predictions

1. **Rate invariance in N and rtf while the budget holds** (A1=A2=B1=B2 within a few %).
2. **B3 clamps or lags**: engine p99 at the 12 ms budget and/or presented-time lag grows
   past B2's, and delivered ev/B/game-s drops below 3.3×10⁻⁵ (work deferred). If instead B3
   delivers the full rate with bounded lag, linear rtf extrapolation is licensed to at least
   rtf 1800 at 3×10⁵; if the rate drops already at B2, every rtf-scaled ledger (effb's,
   a4ed's, mine) overstates delivered work — the honest statement is lag, not cores.
3. **Kick cost per event is N-flat** (engine ms / events within ±30 % across A and B rungs,
   both rtfs) — the law-dominated claim (c01c/0c44) transplanted to the stream's own events.
4. **Standing memory 4.8–5.1 kB/B at every rung** (b30b), so 10⁹ needs the compact store —
   the wired plateau alone is 5 PB against ~6 GB.
5. **The headline check itself needs no flight**: with the shipped doll-anchored clock
   (measured rate 3.3–3.6×10⁻⁵, cf45 + 3294's fire rate 1.000 per doll interval), the 10⁹
   quiet-belt kick rail is N·R·rtf·C ≈ 10⁹ × 3.5e-5 × rtf × 45 µs = **160 cores at the
   player's rtf 100, 16 at rtf 10, 1.6 at rtf 1**. "Passes at 10×" is false under the
   shipped clock on an 8-core M1 that also owes the frame; it survives only as "passes at
   1×" or behind the cadence dial (~148× over the behaviour floor, cf45 — my independent
   140–560× agrees), which is law work, not "today's". The anchors from A/B decide the
   constants; the direction cannot be rescued by them (all cited rates and costs move the
   rail the same way within their ranges).

Kill criterion for my own composition: if (1)+(3) fail — the rate is not rtf/N-invariant or
the per-event cost is not flat — then the rail is not N·R·rtf·C and this dossier reports the
clamp law instead, with the a4ed check left to the checker's own arms.
