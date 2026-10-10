# Predictions — second author on 20261010-0656-autoresearch-cc88 (written before any decisive run)

The checker's named gold experiment: "Gold on this bottleneck is deleting the rebind
compile itself (the re-anchored jet, law.md 'Not adopted', gold-graded once) … Next run
should take the jet; on adoption, cos4 rides along either way."

This run does three things, in order:
- **E1 regeneration**: cc88's record from shipped code (keep.patch on a clean tree).
- **E2 cadence** (no law change): the plane's own per-kick shape drift |Δk|/k measured
  from the shipped kick bench; with the re-anchor threshold θ = √(floor/C) it decides
  whether the jet deletes the compile on the plane's real workload.
- **E3 mechanism**: a first-order integer jet in k for the compiler's weak path (the
  plane's path: 123/134 panels, q = 0, so the table depends on k alone), run against
  df81's named criterion on the *shipped* compiler (increments vs exact recompute over
  correlated kicks), plus update-cost timing. This doubles as the second check df81
  never got (law.md: "Graded gold by one checker; the second never ran").

## Pre-registered predictions

- **P1 (regeneration).** Applying keep.patch to a clean tree: seed 1 kick_us all-median
  improves 13–17%, replay/universe digests equal the baseline's, `refused` 0; seed 2 same
  sign. If not, cc88's record does not regenerate and the run reports that.
- **P2 (cadence).** At least 95% of the plane's per-kick |Δk|/k are ≤ 10⁻⁵ (post-averaging
  belt tides per df81), so with θ = 7.3×10⁻⁴ (floor 10⁻⁶, C ≈ 1.9) the mean anchor
  cadence is ≥ 50 kicks per exact recompile (≤ 0.02 compiles/kick amortized).
  **Kill:** mean cadence < 5 kicks ⇒ the jet re-anchors per kick and deletes nothing on
  the plane; that is a refutation of "delete the rebind compile" for this workload.
- **P3 (mechanism, df81's criterion on the shipped integer compiler).** Over 10⁴
  systematic kicks of ε ∈ {10⁻⁶, 10⁻⁴} at e ∈ {0.3, 0.9, 0.99}, the jet-updated
  increments (Δφ advance, Δt period) stay within 10⁻⁶ relative of exact recompile while
  the accumulated drift δ ≤ θ; the measured error follows C·δ² with C within a factor 4
  of df81's 1.9 for Δφ; halving ε (same kick count) divides the peak error by ≈ 4
  (quadratic check). Negative control: the frozen table (no derivative update) crosses
  the 10⁻⁶ floor at least 10× earlier in kicks than the jet.
- **P4 (cost).** One jet update (all knots + rescale) costs ≤ 8 µs, versus ≈ 63 µs per
  exact compile measured by cc88 — so on the jet path the per-kick compile is deleted,
  replaced by update + amortized anchor. If time remains after E1–E3, the end-to-end
  kick median is measured with the jet wired into the rebind; otherwise the end-to-end
  number is assembled from measured parts and labelled as such.

## What would make the claim wrong

Any of: digests change under the cos4 patch where cc88 claims identity; the plane's
kicks re-anchor per kick (P2 kill); jet error > 10⁻⁶ at δ ≤ θ or non-quadratic in δ;
update cost approaching the compile's. Then the honest result is "the re-anchored jet
does not delete the rebind compile here, and here is the measured reason".
