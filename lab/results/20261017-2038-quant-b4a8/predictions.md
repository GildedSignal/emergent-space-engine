# Predictions (written before the decisive run)

Question: which schedule law does the shipped engine actually run for the 10⁹ bulk (the
belt), what does its fire-time distribution look like frame by frame, and does a
kicked-then-demoted body need carried per-body state (the calendar page's falsifier,
`lab/wiki/calendar.md` open direction 1)?

Reading of the shipped code before any measurement (crates/universe/src/step.rs):
- `plan_interval_inner` → `on_clock()` (doll 0 ships: the belt) → `plan_clock`/`kick_clock`:
  the chained clock. Next kick at `t + full`, `full` a per-body whole-tick count from the
  body's own energy `y` with a fractional carry (`ext.ticks`); no absolute-grid re-anchor.
- Non-clock bodies (planets, moon, ships inside a planet's doll) → `aligned`: absolute grid,
  items at `T + S/2` and `T + S`.

Held-out predictions for the run (extra = 12,000 ladder ships, seed 1, settle past ~3
fire generations):

- **P1 (law split).** ≥ 99% of doll-0 ladder ships are clock-stepped at genesis (one Kick
  item in the plan); the planets, the moon and Home-doll ladder locals run `aligned`
  (dues ≡ 0 or S/2 mod S exactly). Held-out: the exact percentages.
- **P2 (the genesis train).** The belt's first-kick ticks concentrate on few distinct
  values ("battalions"): largest battalion ≥ 10% of the belt, max/μ of the per-tick
  census ≥ 100× the uniform-over-support baseline. Held-out: battalion count and max size.
- **P3 (the train is standing).** After ≥ 3 settled fire generations, ≥ 90% of belt bodies
  still share their next tick with a battalion (group sizes persist); step-change re-key
  rate per fire < 1%. If battalions dissolve, the calendar's "bulk never re-keys" premise
  dies on the other side (everything re-keys continuously).
- **P4 (no grid, no id-closed-form).** Clock bodies' next-tick mod step is not concentrated
  on {0, S/2} (spread anchors); and the next-due of a body that has fired a kick is not
  derivable from its genesis state alone (the chain re-derives `full` from the post-kick
  `y`). Measured as: step-changers' dues ≠ genesis-anchor prediction.
- **P5 (the burst).** Belt items per 338-tick frame window (60 FPS at rtf 100):
  max/mean ≥ 50× un-staggered. At 10⁹ bodies the max frame carries the whole largest
  battalion (linear extrapolation, reported as orders of magnitude only).

Kill criteria: P1 failing falsifies my code reading (report as such — the calendar page's
`aligned`-only reading would then be right). P2/P3 failing kills the train/comb premise on
shipped code. P4 failing (dues ≡ 0/S/2 for the belt too) would confirm the page's premise
in its strong form. Controls: planets/moon must show the exact `aligned` residues (else my
instrument is broken); a no-settle census must equal the settled genesis census (no
instrument drift).
