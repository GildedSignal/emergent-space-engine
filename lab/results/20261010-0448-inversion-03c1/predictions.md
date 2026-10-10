# Predictions — inversion-03c1 (written before any train-verify/frag run)

Setup: the pending build's train certificate (patch from `claude/lab-20261006-1931-b-coorbital-cert-152e`,
VOID at 429 before running anything) applied to main, plus two new experiment sets it never had:
`train-verify disp` (dispersion ladder) and `frag` (which share of a fleet's pairs the train certifies
vs hands to the pairwise tier). ρ = 1e-4, a = 1, uniform λ̄ unless said, 2 orbits, seeds 41–55
(none tuned on; the build's own seeds are 21–37).

## P1 — controls (the build's home scenes, never run anywhere)
`train-verify phalanx|rings|equalp|ring600`: train missed = 0, false = 0 on every scene;
train_evals_per_enc < meth_evals_per_enc (the watch is sound and cheaper where it fires).

## P2 — the e-dispersion cliff (the inversion's headline)
The clump trigger d_c = 8·eps_max ≈ 3e-3 in Binet L1; an e-vector spread σ_e enters (V, W) at full
strength, so a fleet fragments once σ_e ≳ d_c:
- σ_e = 0.005: certified_share (fired intra-clump pairs / all pairs) drops below 50%.
- σ_e = 0.02: certified_share < 5%, clump_max ≤ ~50 on n = 600, and ≥ 90% of cross pairs are
  cone-admitted (same-a, e-spread ⇒ ΔU tiny, cone condition passes) — the pairwise tier keeps
  ≥ 95% of the n²/2 store: the train deletes the quadratic tier only for strict formations.
- σ_e = 0.25: certified_share ≈ 0%.

## P3 — ϖ spread at tiny e
pom15 (σ_ϖ = 15°, e ≈ 1e-3): e-vector spread ≈ 2.6e-4 < d_c → one clump, fires, cheap, missed = 0.
(The taleb-efc9 rank kills needed σ_e ≳ 0.02 with ϖ spread; at e ≈ 0 the λ̄ window barely widens.)

## P4 — high e (K_v and φ verified only to e = 0.4)
hie (Rayleigh e 0.25, cap 0.85): soundness holds (missed = 0) — K_v = 2+6e looks generous — but
windows widen via φ(e) ≈ 2e, so I expect ζ ≥ 1 (declined) or watched/all_pairs → 1: high-e fleets
never ride the train. If missed > 0 here, the watch is UNSOUND at game eccentricities (a kill).

## P5 — the ζ scale bug (noted, not decisive)
`zeta()` ignores its ρ (δ hardcoded to π/2·1e-9 instead of (π/2)·ρ/r_min): ζ under-estimated
~ρ/(1e-9·r_min) ≈ 10⁵× in the δ term → over-fires at game ρ. In these scenes the K_v·dv term
dominates l_max, so I predict no visible effect; latent until a near-circular clump at large ρ.

## Pre-registered kill criteria
- The certificate's adoption value dies if P2's σ_e = 0.02 numbers hold (certified_share < 5%,
  cross cone-admitted ≥ 90%): the quadratic tier is back for any real (dispersed) fleet.
- The watch's soundness dies if train missed > 0 on any fired clump in any scene.
- The certificate survives if certified_share stays > 50% through σ_e = 0.05 (my model of the
  Binet trigger is then wrong and the train is more robust than the gold's own open item said).
