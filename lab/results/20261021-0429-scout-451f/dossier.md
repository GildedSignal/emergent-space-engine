# dossier.md — 20261021-0429-scout-451f

**Claim.** The fleet doll's second-order-in-ξ law (the member certificate at speed, the
page's named od-5 experiment) is now half-measured through a validated exponential-map
instrument: the out-of-plane channel obeys the linear law with a genuinely quadratic
residual c₂ ≈ 78 / 129 / 239 at β = 0.5 / 0.9 / 0.95 (r_p = 18M, one flyby, τ = 8r_p/β),
i.e. the linear interior law is good to ~1% for a member at ξ/r_p ≲ 10⁻² at β 0.9 — while
the in-plane channels are VOID in this run: an O(ξ) channel persists that I diagnosed as
Fermi-slice desynchronization (member proper time vs the frame's T) and did not eliminate
in the window.

## Bottleneck

Board row "families and formations" (~10² memory, ~10 kicks): "how long a member's
certificate lasts against its separation". 4c79 certified the linear tide coefficients;
od 5 named the exponential-map member ICs as the missing instrument. This run builds it
and measures what it can.

## Evidence (all from `python3 falsifier.py <mode>` in this folder, ≤ 60 s each)

**Controls (all PASS, mode `control`):** periapsis eigenvalues reproduce 4c79's
certified closed forms (−γ²(2+β²), 1, γ²(1+2β²))·M/r³ to < 10⁻⁹ at r_p ∈ {6,18,100}M,
β ∈ {0.25,0.5,0.9,0.95}; reference u·u drift ≤ 3×10⁻¹⁵; tetrad orthonormality after
transport 3.6×10⁻¹³; member geodesic norm drift 4×10⁻⁹ at ξ/r_p = 10⁻⁴ (the O(ξ²)
normalization residue of the truncated IC, exposed by the ξ sweep as designed).

**Flyby grid (mode `flyby`, r_p = 18M, exit at τ = 8r_p/β; err := |ξ_true − ξ_ODE|/ξ₀):**

| β | channel | ξ/r_p = 10⁻⁴ | 10⁻³ | 3×10⁻² | c₂ = Δerr/Δ(ξ/r_p)² |
|---|---|---|---|---|---|
| 0.5 | z | 2.46e-3 | 3.44e-3 | 7.26e-2 | **78** |
| 0.9 | z | 6.72e-3 | 7.85e-3 | 1.23e-1 | **129** |
| 0.95 | z | 1.28e-2 | 1.49e-2 | 2.28e-1 | **239** |
| 0.5–0.95 | radial/45°/along | err ≈ 22 / 75 / 146 (β 0.5/0.9/0.95), **flat in ξ** | | | VOID (O(ξ) channel) |

The z-channel is `err ≈ floor + c₂(ξ/r_p)²` with floor ≈ 2.3×10⁻³ (β 0.5) — the same
desync channel that owns the in-plane error, at its small-amplitude limit. c₂ grows
×1.65 (0.5→0.9) and ×1.86 (0.9→0.95); the latter matches γ² (×1.95), the former does not
(cleanly): the speed scaling is between γ^1.5 and γ², not settled by this grid.
The r_p = 100M arm of prediction 3 was lost to a grid edit (see `work/` diff if patched)
— the M/r independence of c₂ is UNTESTED.

**Certificate reading (z-channel, the board's question):** the fleet doll's linear
interior law stays within 1% for an out-of-plane member over one relativistic flyby if
ξ/r_p ≲ 10⁻² at β 0.9 (err = 129·10⁻⁴ ≈ 1.3%); at ξ/r_p = 3×10⁻² it errs 12–23% by
β 0.95. The 288f reading (−0.136% at ξ/r_p = 10⁻⁴, radial, "IC floor + slow growth")
is confirmed as an IC artifact in the one channel I could measure cleanly: at ξ/r_p =
10⁻⁴ the true z residual is 0.24–0.7%, set by the desync floor, not by the tide.

## Predictions (predictions.md, written before the grids)

1. **FAILED** (kill criterion): err/(ξ/r_p)² is not constant — a ξ-independent floor
   (~2×10⁻³) remains even out-of-plane, and in-plane the whole error is O(ξ). The
   instrument is not void (controls pass; the floor is separable in z) but the
   measurement is partial.
2. Untestable in-plane (VOID); in z at β 0.9, ξ/r_p = 10⁻⁴: err = 0.67%, i.e. the
   prediction "err < 1.5×10⁻⁴" FAILED even for the clean channel (the desync floor).
3. UNTESTED (r_p = 100 arm lost).
4. Partially held: c₂ grows with β between γ^1.5 and γ² (predicted γ^p, p ∈ [2,4]).
5. NOT RUN (circular mode never produced valid data inside the window).
6. Held for z (no new channel; growth tracks the linear amplification's order).

## What would make it wrong

The c₂ numbers are differential (slope between ξ/r_p = 10⁻⁴ and 3×10⁻²) and assume the
floor is ξ-independent; a ξ-dependent floor component would bias c₂ low. The in-plane
VOID is a diagnosis, not a proof: if the O(ξ) channel is instead an IC-convention error
(the comoving sign), the in-plane c₂ could differ. The checker should attack exactly
this: swap the IC sign (one line, `make_member_ic`), resample members on Fermi slices
(correct δτ = the desync along the member's worldline), and see whether the in-plane
error collapses to the z-channel's floor + quadratic form.

## Cost of adopting, fit with PRINCIPLES

Nothing to adopt in the engine yet (no law change); the deliverable is the instrument
(validated against standing gold) and the certificate reading for 3D fleet dolls.
PRINCIPLES 33 ("each scale resolves only what matters at its scale"): the member
certificate is exactly the question of when the linear scale stops resolving; P2 (error
type over size): the in-plane/instrument failure is a type result (slice convention),
not a size tweak. The desync floor is a *representation* signal in Julien's sense
(P19): a fix that patches it per-member would be a bandaid; the cure is measuring on
the frame's own simultaneity, which is one δτ correction in the log map.

## The lens (scout)

Requirements-first worked: the instrument was derived from the certificate question, and
the controls tie it to standing gold before any grid ran. What the lens missed: I
under-budgeted the congruence subtleties (Fermi simultaneity) that the EMRI literature
handles with osculating-element bookkeeping — the prior art I ranked (Manasse–Misner/
Marck frames, Drasco–Hughes-style perturbation expansions) was the right list, but I
did not verify at the source how they synchronize (all UNVERIFIED this run; no web
check fitted the window). The next run should steal exactly that piece.

## Reproduce

`bash regen.sh` (≤ 2 min): control (5 s), flyby (10 s), plus the τ-growth probe (5 s)
that exposes the floor/desync shape. Raw JSON: `flyby.json`.
