# Predictions (written before the decisive run)

Topic: encounters open direction 1 (the beat-resident pair record, opened by
20261018-1126-second-20261018-1025-scout-fbf9-1a29). Question: can a stored
(k, d) beat record certify "no early hit post-kick" soundly and cheaply, per
pair, under belt-quantum kicks, at the design reach (deep beat)?

Model (derived before the run, from the three-distance theorem): a silent
pair's phase at conjunction j is phi_j = phi_0 + j*d mod C. A kick changes d
by dd; sound keep of the stored due k requires |dd| < S := min_{j<k}
(m_j - w/2)/j, where m_j = distance(phi_j, window). For a rotation the
closest returns sit at continued-fraction convergent denominators q, giving

  S ~ 3*C/k^2   (order; constant measured here)

and the survival boundary k* ~ sqrt(3*C/dd).

Cases NOT tuned on (held out until after the headline arms are frozen):
- P1: S/k-scaling. Measured median S at k shall be within a factor 3 of
  3*C/k^2 (three-distance structure), NOT of C/k (generic-return structure)
  and not of C/(4k) (uniform-phase structure).
- P2: survival at the quantum. With C ~ 2.3e7 ticks, w = 23 ticks, mean
  k = C/w ~ 1e6, d ~ 3e5 ticks (all from the 1a29 page, UNVERIFIED at
  source), a relative kick kappa = dd/d = 2^-23 gives dd ~ 0.036 ticks, so
  predicted survival P(dd < S) < 10% (k* ~ sqrt(3*2.3e7/0.036) ~ 4.4e4,
  P(k < k*) ~ k**w/C ~ 4%). At kappa = 2^-26 survival rises but stays < 50%.
- P3: dv-independence reproduction. Flip-on rate (silent -> due < H after one
  kick, H in conjunctions) shall be ~ H-independent of kappa across
  2^-26..2^-14 once kappa >= 2^-23, matching 1a29's dv-independence.
- P4: the epoch curve. Skipping M kicks between exact re-arms, the per-pair
  miss probability grows ~ linearly in M at rate ~ min(1, dd*k^2/C) per kick
  (the early-hit rate), so the leak-gated epoch length M* for a budget eps
  per pair per interval is M* ~ eps * C/(dd*k_bar^2) (measured curve;
  reported as the design's missing constant).
- P5 (control, must hold): full exact re-arm each kick -> 0 missed events by
  construction; no-re-arm control -> miss rate = the flip-on rate.

Kill criterion for the direction-1 premise: if measured survival at the
quantum is < 10% AND the S-scaling is C/k^2 (P1), the beat-resident record
cannot carry per-kick slack at the design reach and direction 1 is dead as a
sound per-pair certificate; the surviving structure is the two-clock split
(slack-classified: pairs with k < k* carry slack, the rest epoch re-screen).
