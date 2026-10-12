# Dossier — the phase-neighbour build is quadratic on dispersed co-orbital groups

Run: 20261012-0138-taleb-74a1 (lens: Taleb). Target: `wt/cx-b-coorbital-cert` (Codex build of the
gold `20261006-0346-taleb-09b5`, not yet reviewed or merged).

## Claim

The phase-neighbour certificate in `wt/cx-b-coorbital-cert` (`crates/encounters/src/phase.rs`) pays
Θ(n²) exact-path work — with zero real encounters — on any co-orbital group whose radial/frequency
dispersion exceeds the contact scale ρ, because `reach` is sized by `(n_hi−n_lo)·H/2` (dispersion ×
horizon, never contact structure), every pair inside the window gets boundary Kepler solves and
`pair_events` with no geometric prefilter, and the π fallback trigger is ~70× further out; one
1-ULP eccentricity difference widens the window from ~2 neighbours to all n(n−1)/2 pairs, and one
hyperbolic body (e ≥ 1) in the group panics `group_events` outright.

## Bottleneck

Board risk #1 ("candidate work must track real encounters") and the gold's own target (the 135× /
40 TB quadratic under fleet concentration). This build resurrects that quadratic on the natural
post-dispersion fleet state: a 10⁶-ship formation with δa ≳ ρ costs ~5×10¹¹ window pairs ≈ 60+ hours
per certificate rebuild (measured 15.5 s at n = 8,000; pairs scale exactly as n²·0.996), where the
tier path it displaces is exactly linear in n at fixed per-shell count. Nothing is deleted; the
tree's envelope pruning is switched off precisely when it matters.

## Evidence

Scenes (all μ=1, ρ=1e-4, horizon H=5): **D** = dispersed formation, k shells spaced da=2e-3
(≫ ρ), m=100 bodies/shell on a 0.1 rad arc, e=0 — zero contacts by construction and by brute-force
truth; **T** = tight formation (spacing 0.6ρ) as positive control. Probe: `work/enc` (the branch's
crate, verbatim, plus `src/bin/probe.rs`). Commands (each ≤ 60 s):

```
cd lab/results/20261012-0138-taleb-74a1/work
cargo build --release --manifest-path enc/Cargo.toml
/home/glmlab/lab-target-1/release/probe truth   # D200: 0 contacts; T200: 199, cert misses none
/home/glmlab/lab-target-1/release/probe scale   # n = 1000/2000/4000 phase vs tier
/home/glmlab/lab-target-1/release/probe n8k disp ulp panic cone
```

- **Quadratic with zero encounters (scene D):** window pairs 399,623 → 1,892,762 → 7,882,639 →
  31,860,946 at n = 1000/2000/4000/8000 (4.04× per doubling, exponent 2.01; 99.6% of n²/2 at n=8000),
  events = 0 everywhere, wall 0.57 → 15.5 s. Tier on the same scenes: 49,500 → 396,000 pairs —
  exactly linear — 0.48 → 3.87 s. Boundary Kepler solves: 63.7M at n=8000 (phase) vs 0.79M (tier).
- **Work follows dispersion, not encounters:** n=2000, da ∈ {5e-4, 2e-3, 8e-3} → neighbours
  1,116,443 / 1,892,762 / 1,983,425 (saturating at n²/2), contacts 0 at every da; concentration
  0.006 → 0.076, still 25× below the π fallback.
- **1-ULP cost cliff:** tight formation e=0.05 shared → 499/1,999 neighbours (k=1); ONE body's e one
  representable step higher → 124,750 / 1,999,000 (k=n−1), a 250–1000× jump in pair visits from an
  unobservable input change (the shared-shape fast path requires exact float equality of e and ϖ).
- **Panic, not fallback:** one e=1.5 body in a 9-body group → `panicked at src/phase.rs:35:
  assertion failed: x.e >= 0.0 && x.e < 1.0`. A hyperbolic flyby inside a co-orbital group crashes
  the frame; the tree path is never reached.
- **The fix is one line that already exists:** gating the 31,860,946 window pairs with the crate's
  own `pairs::is_candidate` leaves exactly 396,000 — the same candidates the tree finds — and the
  whole sweep (sort + visit + cone) runs in 0.75 s vs 15.5 s. The phase path's `check_pair` runs
  `pair_events` unconditionally (`if st.phase || arm_pair(...)` short-circuits straight to exact work),
  skipping the Binet cone the tier path applies.
- **Safety held:** zero missed contacts on every scene (T200: 199/199 vs brute force; the `reach`
  derivation is sound, including the seam and the shared-shape cancellation). The failure mode is
  cost and crash, not misses.

Extrapolation is order-of-magnitude only (Linux/x86): pairs scale as measured; a 10⁶ fleet in this
dispersion class costs ~5×10¹¹ window pairs per rebuild, and any kick rebuilds.

## Predictions

`predictions.md` was written after the truth checks and the n ≤ 4000 scaling smoke runs (disclosed
there and above) and before the decisive held-out cases. All five held-out predictions held: the ULP
cliff numbers (499/124,750 and 1,999/1,999,000, exact), the e=1.5 panic (exact line), n=8000 ≈ 3.2e7
pairs / ~15–22 s vs tier ~4e5 / ~4 s, neighbours ∝ da with contacts pinned at 0, and no safety break.

## What would make it wrong; adoption cost; fit

Wrong if the engine never forms co-orbital groups with dispersion above ρ or horizons long enough
for drift to cover the arc — implausible: dispersion above ρ is the post-burn state of any fleet,
and the gold itself was motivated by fleets. Also wrong for the build's purpose if the intended
caller pre-filters groups by shape equality — no such gate exists in the patch.

Adoption (for the integrator's review of `wt/cx-b-coorbital-cert`, before merge): (1) apply
`is_candidate` (or the arm tier) to every window pair before boundary states — measured 21× at
n=8,000, ratio grows with n; (2) fall back to the tree when window occupancy k exceeds a constant
(the tree is linear where the window is quadratic); (3) replace the e ≥ 1 assert with fallback;
(4) drop the exact-float-equality shape gate or pay `centre` smoothly. None of this weakens the
certificate's soundness — all changes are pre-filters below the same exact check.

PRINCIPLES: "minimize spike compute and average compute usage" (OC#36) — the cliff is a spike
quadratic in fleet size; "its risk of breaking makes anything you do to improve it or make it
'efficient' inconsequential unless you first reduce that risk of breaking" — the panic and the
quadratic are the breaking risks to close first; "we know we have a fish, we need to find its
water" — the right water for a phase window is propose-and-cone, not propose-and-integrate.

## The lens

Taleb looks for ruin and fat tails, so it stressed cost and crash, and spent no time hunting a
soundness break in the `reach` bound beyond spot checks — a missed-contact bug (silent loss) would
outrank everything here, and only the T-scene control and the D-scene brute truth cover it. The
scenes are Kepler-tube-only, matching the certificate's stated domain; kicked tubes and the
arm/slack interaction with the phase path are untested. The build's own test suite (on its branch)
was not rerun here.
