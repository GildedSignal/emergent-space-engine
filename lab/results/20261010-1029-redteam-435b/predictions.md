# Predictions (held out before the decisive run)

Written 2026-10-10 before any scene was integrated. Units: M = 1 (Schwarzschild), 2D plane,
static observer at r_o, static point source at (r_s, Δφ). Truth = backward RK4 ray trace of
u″ + u = 3u² (exact equatorial null geodesic). "Memo gather" = the design's mechanism
(representation.md §2: "Lensing adds crossings, from each doll's memoized deflection(b)"):
one bend event on the connecting path, of the exact tabulated deflection α_d(b), one root
tracked from the previous frame; |b| < b_c = 3√3 M ⇒ captured ⇒ no crossing.

## A. Flat control (M = 0) — must PASS
- A1: every source has exactly 1 crossing; memo and truth agree to < 1e-9 rad.
- A2: Newton on the retarded-time root from the previous frame's guess converges in ≤ 3
  evaluations for an observer coasting at β up to 0.999 (g is monotone for subluminal emitters).

## B. Weak-field control (M = 1, r_o = 1e4 M, r_s = 3e4 M, off-axis by 0.1 rad) — must PASS
- B1: 1 image; single-pass memo (exact α_d(b), one bend) within 1% of the true bend, i.e. the
  everyday star-scale case (θ_E ~ 1.4e-4 rad at AU scales) is fine. The premise survives here.

## C. Near a compact mass (M = 1, r_o = 10 M, sources at r_s ∈ {20, 30, 50} M, Δφ ∈ [π−0.6, π]) — the attack
- C1: true crossing count ≥ 2 for most sources inside the Einstein region; ≥ 3 (relativistic
  wraps) for Δφ within ~0.15 rad of π. Count above a 1%-of-brightest magnification cut is
  finite but > 1.
- C2: the memo gather finds 0 crossings for every source whose connecting line has
  |b_line| < b_c: a blind patch around the anti-hole direction. Predicted angular radius
  ≈ asin(b_c·√(1−2M/r_o)/r_o) ≈ 27.7° at r_o = 10 M (the truth shows those sources as a
  bright pair just outside the shadow, never absent). Fraction of a behind-the-hole source
  grid that vanishes: tens of percent.
- C3: where the memo does find a crossing (|b_line| slightly > b_c), its direction is off by
  > 10° near the transition (exact α_d diverges at b_c; one bend cannot compose the geometry),
  and > 1° (B3's tolerance scale) for ≥ 20% of sources behind the hole.
- C4: as the source sweeps behind the hole (player orbiting), the memo view shows a gap (0
  crossings) for a contiguous Δφ interval of order 2·θ_E·(r_s/(r_s+r_o)) — a station blinking
  out — while the truth is continuously visible with ≥ 2 crossings throughout.
- C5: at r_o = 100 M with sources ~1000 M behind, the > 1° mislocation region remains ≥ 2×
  wider in angle than the blind patch (θ_E ≈ 11° > shadow ≈ 3°): the failure is not cured by
  standing off.

## Kill criteria (mine, frozen here)
- The premise ("each visible tube crosses the observer's past light cone once" + memo
  deflection supplies any extra crossings) SURVIVES if in C the memo gather recovers ≥ 99% of
  crossings above the 1% magnification cut with directions within 1% of exact at r_o ≥ 10 M.
- It is FALSIFIED if the memo-blind region is non-empty at r_o = 10 M, or direction error
  exceeds 1° for a double-digit fraction of background sources near a compact mass.
- Controls: A and B must pass, else the instrument is broken (VOID).

## Negative control
- The same memo with the weak-only bend 4M/b (no strong branch) must fail strictly worse
  than the exact-bend memo in C (else my bend model, not the single-pass structure, is at fault).
