# Predictions (written before the view-drift probe runs)

The probe (`crates/universe/examples/viewdrift.rs`) steps the plane exactly as the
benchmark does (rtf 100, 60 Hz frames, engine budget 5 ms, the same burn script,
members 400) and measures, per presented frame, for every emitter the gather
returns: how much its *displayed* quantities change — direction (rad), colour
(max channel diff), angular radius (rad), Doppler shift (relative) — against
display quanta: one 1080p pixel across a 90° FOV (1.6e-3 rad), one 8-bit sRGB
step (1/255), 1% shift. Cases here are NOT tuned on: I have not run this probe;
the numbers come from orbital arithmetic below.

- **P1 (the sub-pixel majority).** At rtf 100 one frame is 1.67 game-seconds.
  Heliocentric bodies at ~1 AU move ≈3e-7 rad/frame (a 1-year orbit), so
  planets, the moon and heliocentric ships — the majority of bodies — sit far
  below one pixel per frame. The low-orbit population around Home (the player,
  nearby ships, ~1.6 h period) moves ≈1.8e-3 rad/frame ≈ 1 px. Prediction:
  **≥60% of bodies are sub-pixel in direction per frame (median frame), and
  ≥95% are below a 10-px quantum.** Fleet members (already carried, no Newton)
  are the borderline ~1–2 px group.
- **P2 (Newton runs regardless).** `readouts` (light-cone crossing evaluations
  inside the gather) ≈ one or more per body per frame — every body is
  re-solved every frame whether or not anything displayed changed. Prediction:
  readouts/frame ≈ (number of bodies) × (1–3), independent of the sub-quantum
  fraction.
- **P3 (streaks).** A body that is sub-quantum this frame is sub-quantum for
  long runs of consecutive frames (drift is smooth and slow for the distant
  population). Prediction: the **median sub-quantum streak exceeds 10 frames**
  for the heliocentric population; i.e. a re-solve cadence of ~10 frames loses
  nothing displayed for most bodies.
- **P4 (colour is nearly static).** Colour (blackbody × shift⁴-luminosity
  channel changes) moves far slower than position except during the player's
  burns: prediction — **≥95% of bodies below one colour step per frame** in
  almost every frame.

If P1–P3 hold, the gather's per-frame Newton work is ~P1's redundant fraction,
and an event/quantum-driven readout (re-solve on: an event on the emitter's
worldline, or a display-quantum crossing) is the Goldratt *exploit* of the
frame's dominant cost — no new part, no law change. If P1 fails (most bodies
super-pixel every frame), the carry buys little and the readout's answer at
scale is aggregation only (the galaxy splat), not carrying.

Kill criterion for my constraint claim: if the gather is NOT the frame's
dominant cost at the plane's own scale, or its cost per body per frame is
already « the engine's, the constraint named in the dossier is wrong.
