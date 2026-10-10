# predictions.md — second-author run 20261010-0100 (Marck-frame coupled certificate)

Written BEFORE the decisive sweeps. Tuned-on (calibration, disclosed): rp=100,
e=0.3 (band structure, validation and unit machinery were developed there; its
numbers appear in this file and must not count as held-out). Held-out: every
other (rp, e) in the sweeps — rp in {10, 30, 100, 1e4, 1e6} x e in {0, 0.3, 0.6}.

The experiment (the second checker's gold item): the Floquet certificate on
the full 2x2 coupled member tide in the parallel-transported (Marck/Fermi)
setting — both in-plane channels plus their shear (exact closed forms:
Lambda11 = w(2+3 u_ph^2/N^2), Lambda33 = w(3 u_r^2 u_ph^2/N^2 - 1),
Lambda13 = -w 3 gam u_ph u_r/N^2, out-of-plane Lambda22 = -w(1+3 u_ph^2)),
the frame precession omega = -gam u_ph u (f-u)/(N^2 sqrt(f)), with the lambda
tables quantized to fixed-point grids Q = 2^16 and 2^12. Truth: tide from a
direct coordinate-Riemann wedge projection + psi/omega from exact tetrad
transport (DOP853); closed forms cross-validated at machine level (dL ~ 1e-15,
dom ~ 4e-6, circular Delta psi = -2 pi sqrt(1-3u) to 8e-5) and monodromies
cross-checked against an independent integrator to 1e-6 at band peaks.

## Pre-registered predictions for the held-out cases

P1 (chart = truth). In every case the chart (closed forms, no transport) and
the coupled truth have equal band counts, and every matched band's center lies
within 1 grid step (601-point log grid). Because both coefficient sets agree
to ~1e-15 by construction, this mostly re-tests the end-to-end pipeline; a
failure would falsify the omega/psi machinery, not the algebra.

P2 (avg blindness, law.md reading). The orbit-averaged law (constant decoupled
channels) finds zero parametric bands of the coupled truth outside its static
Hill-loss region, in all e > 0 cases: it misses >= 90% of truth band area.
Its static edge is also misplaced relative to the coupled truth's low-Omega
boundary (by > 5% in at least one e = 0.6 case).

P3 (avg + exact kinematics — the steelman). Keeping the exact precession
omega(tau) and averaging only the tide yields a THIRD answer: it detects some
bands the plain avg misses (Coriolis pumping at k near 1), but misestimates
peak growth by > 20% in at least half of the e = 0.6 cases and misses >= 25%
of truth bands. So neither reading of "orbit-averaged" is safe inside dolls.

P4 (quantization). Quantizing all four coefficient tables to Q = 2^16
fixed-point levels (each as a share of its own max) shifts band edges by at
most 1 grid step in every case; Q = 2^12 shifts edges by at most 2 grid steps;
where a shift is measurable it scales like 1/Q. The certificate is robust to
the law's fixed-point grid.

P5 (the scout's frozen certificate fails as shipped). The scalar decoupled
drive lam = u^3 (3 gam^2 - 1) (the original run's certificate, alpha = +1)
misses at least one truth band in >= 3 of 4 e = 0.6 radii and shifts k >= 2
band centers by > 2 grid steps in >= 2 cases; at e = 0.3 its centers shift by
about 1 grid step (the correction it lacks is O(u_r^2, shear, omega)).

P6 (compressive channel stays safe). The out-of-plane channel (Lambda22 =
-w(1+3 u_ph^2), stiffness-adding) has at most 1 band per case with peak
<= 0.1/orbit: the coupled certificate confirms the scout's alpha = -1 finding.

P7 (coupling changes band structure, not just edges). In >= 3 of 4 e = 0.6
radii the coupled truth has more bands than the frozen scalar drive (merging
and splitting through the shear + Coriolis coupling), i.e. the coupled chart
is not a small correction to the scalar one.

P8 (rotation confines the Hill region — new physics). In >= half of the e > 0
cases the coupled truth is STABLE in a window between its low-Omega Hill-loss
band and the k = 1 parametric band, where the averaged law reports unbounded
ruin (its static region covers the gap). The averaged law therefore both
misses pumping bands and overstates the ruin region.

Failure of any of these is reported as failed, with the number.
