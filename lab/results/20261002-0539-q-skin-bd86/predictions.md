# Predictions (written before the decisive sweep)

Validation so far (tuning runs, not held out): ring (the crate's own narrow-adversarial shape),
eps = 1e-4, kappa = 0.3, s = 4·eps_u: skin and always both 0 missed / 0 false against the
independent dense truth (conservative advancement per segment). A harness bug (cert bodies stored
in scan order, queried in key order) was found and fixed before any prediction below was written.

Held-out cases (not yet run at the time of writing): the plain belt (N = 2000, sigma_e = 1e-2,
rho = 1e-4, a in [1, 1.5]), the fleet (clustered Binet points, Full-section heavy), belt10k,
eps = 1e-6 and 1e-8, kappa = 3.

1. **Soundness.** `skin` (padded arcs eps+s, window widened by accumulated |Delta period| x
   revolutions since setup, stretched check intervals) misses 0 events vs `always` on every case
   and every s, and `always` itself misses 0 vs the dense truth where checked. The naive
   certificate (deferral with stored windows, no widening) breaks: at eps = 1e-4 I predict
   misses > 0 for s_frac >= 4 on belt and fleet (phase drift beats the 1.1x window slack within
   the 20-orbit horizon), while at eps = 1e-8 even naive stays exact over this horizon (slack
   >> drift). So the answer to "exact for every s?" is: no, not for free — exactness needs the
   slack bookkeeping, not just the cone pad.
2. **Setups per kick.** At the plane-like small kicks (eps = 1e-8, kappa = 0.3) the skin performs
   ~0 re-setups and ~0 scans per kick: essentially the whole per-kick setup cost of `always`
   disappears (> 100x fewer setups). At eps = 1e-4, s_frac = 4 cuts setups per kick by >= 10x
   vs `always`.
3. **The tradeoff.** false_cand_frac (pairs held by the padded cone that are not true candidates)
   grows with s but stays small (< 5% at s_frac = 16 on the belt); the skin's extra cost is the
   widened-window checks in the per-segment pass, which grow with time-since-setup and with s.
   Total us/kick is minimized at intermediate s: I predict s* in [1, 16] x eps_u at eps = 1e-4,
   and the curve is shallow (within ~2x of the optimum over a decade of s).
4. **Rule.** The measured optimum should collapse (within a factor ~3) to a rule of the form
   s* ~ sqrt(C_setup/C_check x kappa x eps x eps_u) — the Verlet balance between re-setup cost
   and false-proposal cost. If it does not collapse, the rule is instead "s such that re-setups
   per orbit ~ 1 per pair", and I will report that.
5. **Fleet.** The fleet's near-identical orbits make Full sections (whole-period checks), which
   are drift-robust; I predict skin misses 0 there as well, with larger widening overhead because
   periods are near-commensurate (more proposals per widened window).
