# Predictions — 20261019-1656-components-3aec (components lens)

Written before any command of the decisive set ran. The component: the kick/event
stream (the 10⁹ CPU ledger's binding row after 73b5 killed the churn row's wholesale arm).

Cases I have NOT tuned on, and what I expect there:

- **P1 (anchor reproduction).** `nladder 10000 coast 10` and `nladder 100000 coast 10`
  on this box reproduce 097e's same-day anchors within load wobble: p50 engine frame
  ≤ 0.15 ms at both rungs, bytes/body 2,300–2,600, total kicks at 10⁵ within 1.3× of
  10⁴ (the belt inert over 10 s wall).
- **P2 (the stream's per-event cost on main, end-to-end).** From the ladder lines'
  own numbers (engine ms/frame ÷ events/frame at rtf 100), the implied per-event
  engine cost on main lands in 30–90 µs x86 (cd3b's composition assumed 29.3 µs M1
  ≈ 50 µs x86; main does not carry 5ade's −9…−11% belt carry, so I expect the high
  side, 45–90 µs). If it reads < 10 µs the engine frame is not event-bound and the
  stream row's cost constant cannot be read this way — report that as the instrument's
  limit, not as a cost.
- **P3 (corrected total).** Re-composing 097e's ledger with 73b5's measured churn
  (0.35–1.4 cores, replacing 2.8–5.5) and mint held at 0–1.9 gives CPU 6.5–12.4 cores
  = 1.6–3.1× the 4-core M1 budget (down from 10.8–16.6 = 2.7–4.2×), and the stream
  row is ≥ 65% of the total in every arm.
- **P4 (the floor ladder, the lens's kill test).** At the belt's measured cadence
  (7.1×10⁻⁵ events/body/game-s planned, cd3b; 3.6–4.3×10⁻⁵ fired, 0659) and rtf 100,
  the stream at 10⁹ is: ≥ 30 cores at a765's ~6 µs arithmetic floor (i.e. NO cost
  lever alone closes it — closure forces the cadence octave), 5.3–8.4 composed with
  split 8 × survival (cd3b), 0.30–0.36 cores at the 42–56 ns write floor. If the
  arithmetic-floor arm computes < 10 cores, the cadence octave is optional and my
  reading of the board's "kick: 10³·³ gap" as rate-bound (not cost-bound) is wrong.
- **P5 (belt_first anchor).** `belt_first 10000` reproduces cd3b's first-item p50
  14,071 game-s within 15% (the rate anchor the stream row stands on).

Kill criteria named in advance: P4's arithmetic-floor arm is the decisive one; P2
reading < 10 µs voids the end-to-end cost reading (instrument limit, disclosed).
