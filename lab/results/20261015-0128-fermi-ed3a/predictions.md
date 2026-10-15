# Predictions (written before the decisive flights)

Question: does staggering the belt's birth grid over one step flatten the first-kick wave
(bf21's "~24x" estimate, unmeasured; cf45: "birth-phase staggering is not optional" at 1e9),
and does the flattening persist through the later waves of the train?

Estimate first (Fermi): all belt bodies are born at tick 0 and take their first kick at
`half ~ ds/2` (plan_clock, step.rs:652), with ds nearly common across 2-3 AU (cf45: quartile
means 2.818->2.805e4 s). The observed wave width is ~1.4-1.5e3 game-s (13,051-14,534).
Spreading the first-kick anchors uniformly over one full step (2*half ~ 2.8e4 s) should
flatten the wave's peak arrival rate by ~(2.8e4 / 1.5e3) ~ 19x, and because every body's
next interval is again ~2*half (nearly common, +7.9% f' refinement), the offsets persist:
later waves inherit the spread (4af4 measured natural shearing widens the train further).

Held-out cases (not tuned on; the arms below run after this file is written):

1. **Wave-1 flattening at N=1e5 coast**: peak events/frame in the wave window drops
   >= 10x vs the gate-off control (prediction: ~15-25x). KILL if < 5x.
2. **Persistence at wave 2** (N=3e5, flown to ~45k game-s): the staggered train's peak
   events/frame stays >= 10x under the control's wave-2 peak. KILL if the staggered
   train re-concentrates to within 3x of control.
3. **Total work is conserved**: kicks per body per game-s unchanged (3.3-3.6e-5 within
   +/-10%); memory (B/body) unchanged within +/-5%; refusals 0, dead 0, player alive.
4. **Lag**: the worst presented-time lag at wave 1 drops >= 5x at 1e5 (control ~1.4-1.7 s).
5. **Default-neutrality**: with the gate unset, `frame_digest` on a short arm is
   byte-identical to the pristine build (the patch changes nothing when off).
6. **Frame budget**: at 1e5 coast both arms hold max frame <= 12.5 ms (the control does;
   the staggered arm should too - the drain's per-frame cap, not the arrival, decides).

What would make the claim wrong: if the offsets do not persist (the grid re-anchors to a
common phase after the first boundary), wave 2 re-forms and the stagger buys one wave only;
if the longer first drift breaks something (refusals, crashes, digest-level law breakage),
the stagger is not a legal generation choice at any width.
