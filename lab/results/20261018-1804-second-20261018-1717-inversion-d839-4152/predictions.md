# Predictions (written before the decisive flights)

Second author on 20261018-1717-inversion-d839 (silver; check2's named gold experiment). The run's
checkers flew the burn arm only to 45,498 gs ≈ 1.65 root-doll steps, where the mint-channel growth
(RSS 150→571 MB at 3×10⁴, held 8→198, ≈2.25 MB per held scan) had *just* flattened (RSS 558→571→571
over the last 5k gs). The named experiment: burn at ladder scale through ≥ 2 full doll steps, plus
the same-N steady rate folded in (replacing the N-mixing "~11×"). Scene and instrument: d839's
print-only patch verbatim (probe every 300 frames = 500 gs); seed 1, rtf 100, 12-ms budget,
1 thread; box load 0.83, 7.8 GB free at start (state recorded in raw/state.txt).

Flights (mine): `30000 burn 456` (baseline = the checkers' arm, reproduced), `30000 burn 760`
(→ ~75,900 gs: kick₁ ~14k, boundary₁ ~28k, kick₂ ~42k, boundary₂ ~55–58k, **kick₃ ~69–72k** — five
belt-wide waves, 2.75 steps), `100000 coast 590` (→ ~58,500 gs: the steady-rate flight, two full
steps at 10⁵), `100000 coast 20` (the rung's own 2,000-gs window at the same N).

- **P1 (the decisive one: the burn mint channel is a bounded transient, not a play-time wall).**
  At 3×10⁴ burn past 45k gs the net backlog reaches equilibrium — mints ≈ in-frame answers — so
  RSS(75.9k) ≤ 900 MB (≤ +330 MB over the 571 at 45k), held_max ≤ 400, growth monotone-decelerating,
  and the process survives (< 2 GB). Basis: the observed deceleration into 45k (RSS +51/+47/+13/+0 MB
  per 2.5k-gs probe bin over 37.5–45k) with held ≈ 190–200 and λ_mint ≈ 0.7/gs mostly answered
  in-frame (p50 0.010 ms, margin most frames). FALSIFIED — and d839's burn scope flips to "grows with
  play time" — if RSS(75.9k) > 1.2 GB, or held_max reaches the 2,048 backlog cap (forced O(K)
  answers), or the guard kills the process.

- **P2 (per-body history terms stay wave-flat under burn).** Through kick₃ and boundary₂: bpb within
  ±10% of the 1,477 class, cat = 30,076 constant after the first wave, and the 760-s flight's probe
  counters at gs ≤ 45,000 bit-identical to the 456-s baseline's (determinism; the baseline itself
  reproduces the checkers' kicks 130,472). FALSIFIED if bpb drifts > +10% past wave 2, cat grows per
  wave, or the counters diverge.

- **P3 (frames hold through five waves under burn).** 0 frames over 12 ms at 760 s, max ≤ 12 ms.
  FALSIFIED if forced backlog answers (the 2,048 cap's O(K) drain) or a wave breaks frames — that
  would make the mint channel a frame wall too, not just a memory channel.

- **P4 (the honest same-N rate).** At 10⁵ the rung's own 20-s window lands in the 10⁶ rung's class
  (6e-6–2e-5 ev/b/gs — pre-wave at the same N, so the window, not N, is the under-read's mechanism);
  the step-inclusive all-body rate at 58.5k ≈ 9.5–10e-5 (d839's 9.79e-5 at 45.6k extended); the
  belt-cadence locals-out rate (2 kicks + 2 boundaries per belt body per 2 steps) ≈ 6.5–7.5e-5, so
  the honest under-read of the 10⁶ rung's 8.53e-6 is **≈ 7.5–8.8×**, replacing the dossier's "~11×"
  (which divides 10⁵-with-locals by the 10⁶ rung). FALSIFIED if the belt-cadence rate falls outside
  that band — then the correction factor needs a third convention and I report all three.

- **P5 (coast control at 10⁵ through boundary₂).** RSS 477–485 MB flat (reproduces check1's 590-s
  arm), cat 100,076, 0 over. Reproduction, not a new claim.

- **Held-out for my checker (not flown by me):** `10000 burn 760` (a decade down in K — boundedness
  of the mint channel at 10⁴, where the rung's own table already showed held 570 in 2,000 gs on the
  loaded M1), and `30000 burn 590` (an intermediate horizon between my two).
