# dossier.md

**Claim.** The equatorial Kerr cycle compiles in exactly the crate's
Schwarzschild representation — Darwin's phase ψ with x = R/r = k+(1−k)cos ψ,
k = 1/(1+e), q = M/R, the cubic factored by its roots, Gauss–Legendre in ψ —
with only the integrands changed: (du/dσ)² is Schwarzschild's cubic under
L² → L²−a²(E²−μ²) and 2ML² → 2M(L−aE)² (standard Mino time dσ = u²dλ,
re-deriving and correcting the Opus memo's inverted fraction), and dφ/dψ,
dt/dψ, dτ/dψ are [rational in u] × g, g = 1/√(2(u₃−u)). A float reference
compiler (kerr_ref.py) regenerates (E, L, χ) → (Δφ, Δt, Δτ) per radial
period, verified against independent direct geodesic integration to ~10⁻¹⁵,
plus test vectors to 1e-12 (test_vectors.json).

**Bottleneck.** law.md line 31 ("a tube is still compiled from (E, L), now
with the doll's χ") and the board's compiler question: this run removes the
derivation risk from Astra's builder path (9 October). It deletes any thought
of a separate rotating-hole law: χ = 0 is ENVELOPE.md bit for bit (measured:
integrand agreement 4×10⁻⁴⁰ at 40 dps), so no second law, second memo format,
or category boundary exists.

**Evidence** (commands ≤ 60 s unless noted; M = c = 1):

- `python3 kerr_ref.py` — selftests: Kerr integrands at a = 0 equal
  ENVELOPE.md's three integrands to 4×10⁻⁴⁰ (rounding); ISCO(χ) matches
  Bardeen's closed form at χ = 0.5/0.9/0.998 both senses (1.236970655…M,
  8.994374455…M at χ = 0.998); b± matches the closed forms.
- Direct verification: `direct_check.py` derives the inverse metric with
  sympy from the BL line element and integrates Hamilton's equations with
  RK4 in mpmath (h vs h/2, Hamiltonian drift ≤ 10⁻¹⁷; RHS asserted equal to
  sympy's in exact rational arithmetic). Tuning-phase 6-case run
  (χ ∈ {0, 0.5, 0.9}, both senses, k = 3/4, q = 1/8): all three increments
  agree with the compiler to ≤ 3.6×10⁻¹⁵ relative. Pre-flight near-separatrix
  pro χ = 0.998 (q = 0.999 q_sep): Δφ = 178.8 rad/cycle (the whirl).
- `python3 vectors.py` — the decisive grid (written before the run:
  predictions.md): bound χ ∈ {0, 0.9, 0.998} × senses × e ∈ {0, 0.1, 0.3,
  0.6, 0.9} at q = 0.5 q_sep, weak field q = 1/200, near-ISCO
  (q_sep(1−10⁻⁵)), near-separatrix (q_sep(1−10⁻³)), unbound E ∈ {1.05, 1.3},
  photons near and far from b±, E < 0 ergosphere plunges at χ = 0.998;
  output `test_vectors.json` (incremental — whatever the 8-minute window
  finished is on disk with per-vector direct errors).
- `python3 series_nodes.py` — weak-field structure (series_nodes.json): the
  odd-in-χ part of Δφ first appears at q^{3/2} (Lense–Thirring) — e.g.
  retro k = 5/8: c_{3/2} = −6.266 at χ = 0.5 and −11.306 at χ = 0.9
  (clean linear-in-χ), against my predicted −12πχk^{3/2} = −9.31/−16.76:
  the held-out coefficient prediction FAILED by a consistent factor
  0.674 (≈ −8.05πχk^{3/2}; the k-power still to confirm on the k = 3/4
  rows); even-in-χ corrections enter at q², so one memo per (k, χ) per
  sense carries the q-series exactly as ENVELOPE does per k.

**Predictions** (predictions.md, written before the decisive runs):
P1 (agreement ≤ 1e-12 with direct integration) held everywhere tested
(≈10⁻¹⁵). P2 half-held: odd-χ first at q^{3/2} confirmed AND the k^{3/2}
power held (c_{3/2} ratio k=0.75/0.625: measured 1.320 vs (0.75/0.625)^1.5
= 1.3145), but my LT coefficient −12πχk^{3/2} was 1.49× too large: measured
c_{3/2} = −8.05±0.1 πχk^{3/2} (8π sits just inside the fit error; the
checker should fix it analytically — I did not derive it). P5: no bound
E < 0 orbit exists (0 found; all plunge) — held after fixing a root-finding
bug (below) — but the maximum E < 0 apoapsis found is 2.079M, slightly
OUTSIDE the equatorial static limit r = 2M; future-directedness
(dt/dλ > 0) at that turning point was NOT checked before the window closed,
so "E < 0 strictly inside the ergosphere" is an OPEN point for B19, not a
settled one. P4 (node counts) did not finish in the window: series_nodes.py
was still running (its series half completed; the node half must be rerun
by the checker: `python3 series_nodes.py`, ~5 min).

**What would make it wrong.** The direct check shares only the metric and
(E, L) with the compiler — not the cubic, the roots or ψ — so a shared
algebra error is unlikely; a shared *bug* class is not: both were written by
one author in one session. The verification dps (22–30) caps distinguishable
agreement at ~10⁻¹⁴; "1e-12" is therefore a safe claim, not a measured
floor. The χ⁰/integer-power series fits for retrograde were corrupted by a
sign convention (Δφ < 0; constants cancel in the odd part, so the LT numbers
stand). test_vectors.json's coverage is whatever the 8-minute compute window
finished (incremental dump) — a checker should rerun `python3 vectors.py`
(~10–15 min, 6 workers, < 2 GB) for the full grid.

**Fit with PRINCIPLES.** "χ = 0 is the Schwarzschild law, bit for bit" is
the same representation, one law at every scale (19, 32); the memo question
("one memo per (k, χ)") resolves to (k, χ, sense): sense is one bit per
tube, χ one constant per doll (5: the player's wildcard budget is spent
nowhere); no orbit categories were introduced — bound, unbound, photon and
plunge use one phase (35), with the horizon's logarithmic BL divergence
pushed to the compiler's existing "no horizon arrival times" boundary
(ENVELOPE.md). Cost: adoption is Astra writing the integer integrands;
nothing else in the law changes.

**Process notes (for the checker).** Two self-caught defects, both recorded:
(i) mpmath's `polyroots` silently returned roots violating the cubic's own
root identities for clustered/negative-energy cases — my first E < 0 scan
"found 4255 bound negative-energy orbits", contradicting B19; with verified
bisection root-finding every E < 0 orbit has a single outer turning point
(all plunge, none bound) — the same shared-harness trap as the 5 October
memo artifact. (ii) my first separatrix parametrization put the whirl root
at apoapsis; corrected, it reproduces Schwarzschild's p_sep = 6+2e exactly.

**The lens may have missed:** cost and integer realization (Astra's step:
the integrands are rational in u times g; the crate's Q62 arithmetic, band
cuts and mirror all carry over unchanged, but I did not measure compile
times or write integer code); the fifth/sixth integral columns (Marck's
tidal angle Φ); non-equatorial orbits (Carter's Q enters as a fourth root
pair in Θ — likely the same machinery, unverified).
