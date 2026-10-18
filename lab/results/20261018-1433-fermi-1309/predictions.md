# Predictions (written before the decisive checks)

Question audited (Fermi lens, attack #3): today's 10⁷-rung decision composition
(20261018-1126-library-686f + the ef63 fix): "lazy birth + the RES delete passes
EVERY term with ≥3× margin ... at 10⁹ in one doll the wave still fails 18.1–31.4×
and the steady spared stream is 0.61–1.02 s/s — NOT cleared on one thread."

My independent estimate (constants: cadence 3.5e-5 ev/B/gs from ladder.txt's own
"357 kicks a game-second at 10⁷"; event cost 29.3–50.4 µs M1; wave window
13,051–14,534 gs ⇒ 1,483 gs = 14.8 s wall at rtf 100 ⇒ 10.8 s of 0.72 s/s budget;
smallest wiring 34–38 µs/event, promotion 4.6 µs):

- P1 (cadence from code): the shipped cadence law (step_log2 + the doll's anchor
  period) yields the belt interval 2.8(±0.1)×10⁴ s ⇒ rate 3.5(±0.2)×10⁻⁵
  events/body/game-second. [check: ext/constants + Config::step_log2 in crates]
- P2 (survival geometry): recomputing the frozen resonance exclusion (q/r ≤ 8
  within 2%, three planets) on the ladder's belt draw (2–3 AU, e ≤ 0.4, uniform
  angles, scenario.rs) from the shipped planetary constants gives a spared
  (surviving) fraction in 45–75% — the page's 434/712 = 61% is geometrical, not
  an artifact of that run.
- P3 (the s-mixing find): each 686f cell reproduces within 2× iff the 10⁷ row's
  composed arm uses belt survival s ≈ 0.5–0.7% (the RES widened delete,
  708/712) while the 10⁹ row uses s ≈ 61% (the frozen exclusion): specifically
  10⁷ steady "0.006–0.010 s/s" = 10⁷·3.5e-5·rtf100·(29.3–50.4 µs)·s with
  s≈0.56%, and 10⁹ steady "0.61–1.02 s/s" = the same formula at N=10⁹, rtf 1,
  s≈61%. In bodies×pace units (N·rtf = 10⁹ both rows) the two rows should be
  equal under one legality; the table's 10⁷-passes / 10⁹-not-cleared contrast is
  the legality call flipped, worth ~110×, not a scale effect.
- P4 (corrected margins, one legality each):
  - RES legal (s=0.56%): 10⁷ steady 0.006–0.010 s/s (72–120× margin, not "≥3×"
    — the wave is the weak term at 3–5×); AND the 10⁹ stream/wave terms also
    clear (steady 0.006–0.010 s/s, wave ≈ 0.2×) — the "not cleared" 10⁹
    sentence dies; 10⁹'s honest blockers are memory (15.75–28.4 GB) and the
    re-kick (0.55 s/s).
  - Frozen legality (s=61.5%): the 10⁷ rung FAILS: unstaggered wave 19–35× over
    the window; steady 0.63–1.08 s/s = 0.9–1.5× the single-thread 0.72 budget;
    with the birth stagger (already in the composed law) spreading the wave over
    one interval (≈ 281 s wall, 202 s budget) the wave merges into the steady
    stream ⇒ parity at s ≈ 42–70%. The shipped plane is 1 thread: the rung then
    needs rtf ≤ ~46, a second thread, or the cadence dial (own-period anchor,
    ~24×).
- P5 (cheapest falsifier): the legality probe is nladder's open direction 2
  (the r9 tide-bound transfer to heliocentric bodies is assumed, margin
  5.5–6.4×, no gate) plus a resonant-belt-body drift probe under the delete —
  until it runs, a green 10⁷ flight certifies nothing (the pass is the
  assumption).

Kill criterion for MY claim: if the code cadence differs from 3.5e-5 by >3×, or
the 10⁷ composed cells do NOT close under s≈0.56% within 2×, or the 10⁹ cells do
NOT close under s≈61%, my mixing reading is wrong and this dossier reports the
composition as confirmed uniform instead.
