# Predictions — second-author run 20261011-1102 (before the decisive A–F runs)

Question (the checker's gold experiment for 20261011-0924): the retrigger rate of the
rotation certificate under real kicks at the plane's rate (kappa=0.3/body/orbit, eps
kicks to a, slack-skin quantum s = 4*eps_u(rho)), and whether amortized certificate
work per real encounter stays O(1) including window rebuilds.

Instrument: probe2.py. Truth = piecewise-exact Kepler under kicks (M continuous),
per-synodic-interval dmin with conjunction refinement. Uniform work unit = one
Kepler-pair evaluation; arithmetic counted at 1 arith = 0.01 eval (stated).
Frozen control G validates the pipeline (no kicks: the frozen record must not break).

Findings already made while building the instrument (smoke, 10 pairs; full runs decide):
- F1 (frame defect): the original probe's kepler() never rotated positions by varpi,
  so its belt was effectively aligned-pericenter, not "random varpi" as registered.
  My probe uses inertial positions; numbers are not comparable one-to-one.
- F2 (the strobe is 2D under kicks): the relative longitude at strobe, D_j, walks by
  ~radians per skin epoch (measured +-2.9 rad in one epoch), and the theta-window
  shifts by (n1/dn)*dD -- amplified 23-700x. The theta-space record is the wrong
  variable; the invariant-ish object is the conjunction longitude
  psi = w1 + M1 - (n1/dn)*D (exact anchors, O(1)/kick).
- F3 (reversal regime): for e_max > 0.75*da/a the relative longitude rate reverses
  within an interval (equation of center beats the synodic rate); ~96% of the
  original's belt pairs are in this regime, and a 1D psi certificate (arcs from
  radial gap + impact parameter at the principal conjunction) cannot cover their
  hits without fatting to ~the whole circle.

Registered predictions for the decisive runs (config A rho=1e-4 eps=1e-6 T=60k;
B rho=2e-3; C rho=5e-3; D eps=1e-5; E eps=1e-4; F co-orbital da<=0.003; 300/100 pairs):

- P1 (the retrigger rate, as-stated). The frozen theta-record's phase error crosses
  the window slack after a median of < 25 intervals at plane eps (all rho), i.e.
  10-100x faster than the slack skin (measured skin periods 300-1500 intervals) and
  comparable to or faster than the median return gaps (13-430). [If the median
  phase-retrigger period exceeds the skin period, the claim as stated survives
  kicks and my F2 analysis is wrong somewhere.]
- P2 (the inversion, as-stated, charged). With rebuilds charged at the record's own
  construction cost (a theta-window scan, ~12k evals here; the original's was
  1024x48 = 49k), as-stated work per interval exceeds per-interval scanning
  (scan_per_as_stated < 1) in every kicked config. [If scan_per_as_stated > 3 in
  B or C, the 33-146x claim survives with honest accounting and I am wrong.]
- P3 (frozen control). In G (no kicks) the frozen record must not break:
  phase_retrig_med = full epoch, and as_miss/nhits small (resolution-limited:
  windows thinner than 1/256 of the phase circle fall through; I accept up to 3%
  as instrument resolution, not method failure). [If as_miss/nhits > 10% in G,
  my instrument is broken and no other prediction counts.]
- P4 (the repaired psi certificate). In the non-reversal regime (e_max <= 0.75*da/a)
  the psi-certificate has zero coverage misses at plane eps (A, B, C, F) with
  false alarms < 50% of arrivals. In the reversal regime misses are expected and
  reported as the boundary: the record must be 2D there (conjunction longitude plus
  wobble), which this run maps but does not build. [Zero non-reversal misses with
  false alarms < 50% would make the repaired form adoptable for that regime;
  non-reversal misses at plane eps kill the psi form too.]
- P5 (scaling). The skin retrigger period scales ~ rho/eps (linear in both):
  ~6 intervals at rho=1e-4 eps=1e-6, ~145 at rho=2e-3, ~365 at rho=5e-3, and
  ~10x shorter per decade of eps (D, E). The phase quantum scales the same way
  (it is the same kick physics, amplified). [Deviations from linearity in eps
  beyond 2x indicate my drift model is wrong.]
- P6 (co-orbital F). Reversal fraction ~100%, psi false alarms dominate, no win;
  consistent with the first checker's 7.4x, now with the mechanism named.

Kill criteria: P1 failing kills the "three numbers replace the scan" claim as
stated under real kicks; P4's non-reversal half failing kills the repaired form;
P3 failing kills my instrument (VOID).
