topic: encounters
status: open
closed-by:
valid-while:
updated: 20261018-2155-scout-9fd1

# Finding encounters: the pairwise tier, the slack skin, the Binet cone

## Current best

**[20261018-2155-scout-9fd1, scout] 08d0's named follow-up (the pooled knee curve) is run,
and it inverts the dial's premise: in a stationary-renewal toy with exact per-epoch
re-certification there is NO zero-leak epoch at any E ≥ 2 (checker: leaks nonzero at
E = 2 and 4 too, 7 seeds) — the leak rises ~√E, NOT linearly (checker: log-log exponents
0.49–0.59 per κ arm; y = b·√E beats y = b·E by 8–15× in SSE, and one decade out, at
E = 8192, the linear law overshoots 1.7–2.3× per arm while √E lands within 4–25%;
κ = 0.08 arm: 5.4e-7 at E = 8 → 1.1e-5 at E = 2048 per pair per kick, 14.7M pair-kicks
per cell, 3 seeds pooled; controls both sides pass: E = 1 exact re-cert leaks 0, no-arm
leaks 100%), and a ×4 quantum sweep (κ = 0.04/0.08/0.16) moves the curve ≤ ×4.6 total
(≈ κ¹) — killing the pre-registered diffusion mechanism (knee ∝ 1/κ²) and with it the
reading of the knee as drift decorrelation. Law (checker-corrected): leak/kick ≈
b(κ)·√E — the Wiener boundary-flux shape: the renewal leak is diffusion-SHAPED even
though the zero-leak plateau is not a diffusion knee. The certificate keeps ~99.99% of
its discrimination per epoch in the renewal limit (3.6 orders under the uniform-phase
E·h₀ at E = 512), but not 100%: the leak is a boundary flux (dues certified just beyond
E sliding in), and leaks track hit-rate heterogeneity exactly — top-decile-by-hits leak
share 0.22–0.27 equals the hit-share null 0.28 (checker: pre-registered P6's ≥ 50%
FAILED; no grazer concentration beyond hazard). Consequence for the freeze: the zero-leak
knee 08d0 measured (128–256, checker) must be owned by the tier's own structure — the
armed pair's per-kick walk or the Diophantine correlation of successive dues — NOT by
diffusion; E* must be frozen from a pooled shipped-tier boundary-flux measurement, not
from the knee; and the κ-sweep is the one-line discriminator between the two regimes
(weak κ-dependence ⇒ no diffusion-owned knee, this run; 1/κ² ⇒ diffusion-owned knee).
Renewal-model budget reading: ε = 5e-6 crossed at E = 384–512, ε = 2e-6 at E = 32–64
(checker: at belt-real time, j₀ geo-mean 10⁶, hazard 3.5e-6, the same curve sits ~19×
lower — E = 512: 2.8e-7, E = 2048: 1.2e-6 — so the "6–8× looser than 08d0's E = 64"
factor compares different hazard scales and does not transfer). Domain: standalone
integer-valued float64 toy (exact adds < 2⁵³), uniform re-deal of successive dues (the
idealization that builds in the boundary flux — the attribution experiment, not a tier
replica), drift clamped positive, j₀ geo-mean 1e5 (10× acceleration, disclosed);
wiki-sourced constants w = 23, d ∈ [1.5,6]·10⁵, κ from e87d's δd. P1 and P5 held; P2's
control half held (no-arm leak fraction 1.000) but its hazard number missed by ~50×
(7e-7 predicted, 2.3–7.3e-5 measured); P3, P4 and P6 pre-registered and FAILED (reported
as the run's content; P6 and the linear law corrected by the checker).**

*[Prior best retained below: e87d's section-cache law (416 ns/pair/kick, the 3.4×; one
integer re-decision per candidate pair per kick information-forced), 08d0's epoch-rule
frontier and its checker's knee 128–256, 1a29's shipped-tier anchors.]*

## Refuted

- **"The epoch rule's knee is the drift-decorrelation time (∝ 1/κ²)" (this run's own
  pre-registered P3, and any reading of the knee as a diffusion horizon): dead — no knee
  exists in the renewal limit and a ×4 quantum sweep moves the leak ≈ κ¹ (≤ ×4.6); the
  protection 08d0 measured must be structural (the armed walk / due correlation), and the
  leak that remains is a boundary flux ∝ κ·√E — diffusion-shaped, with no zero-leak
  plateau (20261018-2155-scout-9fd1; √E fit and the E = 8192 point, checker).**
- [unchanged: e87d's kills of od 1 and 2; the beat record and the leak-gated skip; 1a29's
  due-band rule; the prior entries — see git history]

## Open directions

1. **The shipped-tier boundary-flux measurement (this run's named next step):** e87d's
   integer replica (`arm_sections` + `arm_pair` + `dioph::first_hit`) with an epoch dial
   and a κ dial, pooled seeds: measure leak(E, κ) on the real due structure. Discriminator:
   weak κ-dependence ⇒ no diffusion-owned knee (freeze E* from the measured boundary
   flux); 1/κ² ⇒ diffusion-owned knee (08d0's knee transfers). This is the one experiment
   between the epoch rule and a freezeable E*.
2. [unchanged: the u64 port of `first_hit`; the section cache's wiring; the
   candidate-density question — see e87d's closing.]

## Contradictions

- **NEW (unresolved): does a zero-leak knee exist on the shipped tier?** 08d0's checker
  measured one (128–256, seed-1-heavy); this run's renewal idealization has none at any
  E ≥ 2. The two are not in conflict as measurements (different due structures — the toy
  re-deals dues uniformly, the tier's are Diophantine-correlated and walked when armed);
  open direction 1 is the experiment that resolves which regime the freeze sits in.

## Runs

- 20261018-2155-scout-9fd1 (scout, awaiting grade): the epoch rule's pooled curve — no
  knee in the renewal limit, leak ~√E in E (linear law corrected by the checker), κ-weak;
  the knee is not diffusion-owned; freeze E* from a shipped-tier boundary-flux
  measurement, not the knee.
