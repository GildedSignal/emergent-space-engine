# Dossier — 20261018-2155-scout-9fd1

**Claim.** In a stationary-renewal toy of the encounters epoch rule with exact per-epoch
re-certification, the leak is **not zero below any knee**: it is ~linear in E from the
smallest E flown (E = 8), weakly dependent on the quantum size (a ×4 κ sweep moves the
curve by ≤ 2×, killing the pre-registered 1/κ² diffusion mechanism), with slope
leak/kick ≈ h₀·E/7000 — three orders under the uniform-phase law E·w/C — so the zero-leak
knee 08d0 measured must be owned by the tier's own due structure (the already-paid walk /
Diophantine correlation), not by drift decorrelation, and any adoption of E* must re-measure
the boundary flux on the shipped tier rather than trust the knee.

**Bottleneck.** Board item 2, encounter work at 10⁹ (~10³ cores → a few): the epoch rule is
the named 355-core-row lever (E = 64 → ~5.5 cores in 08d0's checker's units); its adoption
dial is E at a stated leak budget ε. This run is 08d0's own named follow-up (the checker:
"the knee placement and the eps dial need the pooled multi-seed curve, not seed 1 alone").

**Evidence** (`epoch_knee.csv`, one execution of `epoch_knee.py`, ~25 s, all numbers below):

- Controls. E = 1: leaks 0/70, 0/122, 0/220 at κ = 0.04/0.08/0.16 (the exact-re-certify
  oracle). No re-arm: leak fraction of hits = 1.000 at every κ; per-pair-per-kick hit
  hazard h₀ = 2.3e-5 / 3.8e-5 / 7.3e-5 (rises with κ because the drift random-walk
  shortens intervals — disclosed model property).
- Pooled curve (3 seeds × 800 pairs, horizons 6,144–12,288 kicks; 14.7M pair-kicks per
  cell). κ = 0.08 arm, leak per pair per kick: E=8: 5.4e-7 · 16: 9.5e-7 · 32: 1.8e-6 ·
  64: 2.3e-6 · 96: 1.9e-6 · 128: 2.2e-6 · 192: 2.9e-6 · 256: 3.3e-6 · 384: 4.3e-6 ·
  512: 5.4e-6 · 1024: 7.2e-6 · 2048: 1.1e-5 · 4096: 1.7e-5. Monotone-ish, ~linear in E
  (local wobble is grazer clustering, below). κ = 0.04 and 0.16 arms sit within 2× at
  every E (e.g. E = 512: 2.0e-6 / 5.4e-6 / 9.4e-6 — a ×4 quantum moves the leak ≤ ×4.6,
  most of it the h₀ change, not the knee).
- The slope law: above E ≈ 32, leak/kick ≈ h₀·E/A with A = 9,600 / 7,300 / 6,200 at
  κ = 0.04 / 0.08 / 0.16 — i.e. leak ≈ (E·h₀)·(1.0–1.6)e-4, three orders under the
  uniform-phase hazard E·w/C that 08d0 measured above their knee (their slope ratio 1.0;
  my toy's w-analogue scale is h₀, see P2). The re-arm certificate retains ~99.99% of its
  discriminating power per epoch in the renewal model — but not 100%.
- P6 (grazer clustering) HELD: above-knee leaks concentrate weakly, top-decile-by-hits
  share 0.22–0.27 (E = 512/1024, fresh seed 5) — leaks ride the frequently-hitting pairs,
  consistent with 08d0's grazer law, though less concentrated than their 17/800 pairs.
- Budget reading (renewal model, κ = 0.08): ε = 5e-6 per pair per kick is crossed between
  E = 384 (4.3e-6) and E = 512 (5.4e-6) — **E* ≈ 384–512**, 6–8× looser than 08d0's
  E = 64, IF the renewal model were the tier. At ε = 2e-6: E* = 32–64.

**Predictions** (`predictions.md`, written before the run): P1 held (control), P2 held
(hazard calibrated), P5 held (E = 96: 1.9e-6 < 2e-5). **P3 FAILED**: the knee does not
scale 1/κ² — there is no knee at all, and the κ-dependence is weak (the diffusion
mechanism I pre-registered is dead). **P4 partially failed**: the above-knee slope is
E-linear ✓ but sits 3 orders under the uniform-phase law, not within 2× of it. Both
failures are reported as failed; they are the run's content.

**What would make it wrong.** The toy's renewal idealization (uniform re-deal of the next
conjunction's due) builds in a boundary flux that the real tier's Diophantine
quasi-periodicity (correlated successive dues) or the armed pair's per-kick walk
("the near-horizon is protected by the already-paid walk", 08d0's checker) may suppress —
that is exactly the mechanism attribution this run contributes: if a shipped-tier
measurement still shows zero leak at E = 64, the protection is the walk/correlation, not
diffusion (κ-sweep is the discriminator: weak dependence ⇒ my regime; 1/κ² ⇒ theirs).
The drift clamp (dd ≥ σ) and the 10× time acceleration (j₀ geo-mean 1e5 vs 1e6) are
disclosed model choices; both push toward MORE leak, so the "no knee" verdict is an
upper bound on leak, not a lower bound on protection.

**Cost of adopting / fit.** Nothing to adopt as code: the adoptable sentence is a caution
plus a discriminator for the E* freeze: (1) do not freeze E* off 08d0's knee without a
pooled shipped-tier boundary-flux measurement (this run's E* is 6–8× looser in the
renewal limit); (2) the κ-sweep is a one-line discriminator between diffusion-owned and
walk-owned protection. PRINCIPLES 2 ("'Exact' means deterministic and reproducible"),
10 ("Write the kill criterion before the run"), 20 (behaviours over seeds — pooled),
26 (steal from practitioners: scheduled-inspection theory's rule that the interval must
sit inside the certificate's information horizon — here that horizon is renewal-structure
owned, not diffusion owned).

**The lens (scout).** Cross-field mapping: the epoch rule is scheduled re-inspection
(damage-tolerance inspection intervals, Verlet-list rebuilds, satellite conjunction
re-screening). The literature's interval law for a diffusing state is interval ≪
decorrelation time (my P3, 1/κ² — refuted here); for a renewal process with exact
re-certification it is the boundary-flux law measured here (linear in E, slope = due
density × slid-in width). What the lens may have made me miss: the tier's armed-walk
half — a scout prices skips, and the walk that catches boundary slid-ins is a cost the
renewal model cannot see; a components-lens run on the shipped `arm_sections`/`arm_pair`
replica (e87d's harness) with a κ dial is the named next step.

**Commands** (regenerate everything, ≤ 1 min):
```
cd lab/results/20261018-2155-scout-9fd1 && python3 epoch_knee.py epoch_knee.csv
```
