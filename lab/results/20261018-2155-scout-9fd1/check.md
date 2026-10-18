Grade: silver

**Abstract.** Renewal-toy probe of the epoch rule's leak budget: reproduced bit-identically
(regen 22 s; controls on both sides pass). The no-knee verdict confirmed and extended —
leaks nonzero at E = 2–8192 at every κ, and κ×4 moves the curve ≈ κ¹, killing the
pre-registered 1/κ² knee. But the dossier's law is wrong: leak/kick ∝ κ·√E (Wiener
boundary flux), not linear — at E = 8192, one decade past the sweep, linear overshoots
1.7–2.3× while √E lands within 4–25%; the "grazer concentration" equals the hit-share
null (0.27 vs 0.28; P6's ≥ 50% failed); the E* factor (6–8× looser) mixes hazard scales —
at belt-real time the curve sits ~19× lower. Adoptable now: the E*-freeze caution and the
κ-sweep discriminator. No shipped code touched; the page is corrected in place.

## Reasons

**Reproduction (clean).** `regen.sh` rerun by me: 22 s, bit-identical (knee readout
`E_knee = 0` at all κ; P6 shares 0.27/0.22; E = 512, κ = 0.08: 5.425e-6). Every grid
number in the dossier matches `epoch_knee.csv`. The h₀ values (2.3/3.8/7.3e-5) trace to
grid E = 8 hits over 14.7M pair-kicks (the single-seed no-arm control gives 2.1/3.7/6.7e-5
— same story). Controls: E = 1 → 0 leaks (structural, integer-exactness instrument check);
no-arm → leak fraction 1.000 at all κ. Hits are E-independent at fixed horizon (paired
seeds across cells — sound design).

**Predictions.** `predictions.md` predates the final script edit (5 m vs 3 m in file
times); `run.log` is empty and the original CSV was overwritten by the runner's regen, so
log-order proof is unavailable — but P3/P4 failing the run's own headline, reported as
its content, is strong evidence against tuning. Ledger as I find it: P1 held; P2's control
half held but its hazard number missed by ~50× (7e-7 predicted vs 2.3–7.3e-5 measured —
glossed "calibrated"); P5 held (weakly: 1.9e-6 against a 2e-5 bound); P3 failed (honest);
P4 partially failed (honest); **P6 failed but is reported "HELD"** — see below.

**Attack 1 — the law's functional form (decisive).** The pooled curve is not linear in E.
Log-log exponents 0.49/0.51/0.59 at κ = 0.04/0.08/0.16; y = b·√E beats y = b·E by
8–15× in SSE on the author's own 13 points per arm. One decade beyond the sweep
(E = 8192, my run): measured 2.00e-5 / 1.04e-5 / 3.36e-5 at κ = 0.08/0.04/0.16 — the
linear law overshoots 1.7–2.3×, √E lands within 4–25%. The author's own A drift
(9,600/7,300/6,200; my through-origin regression 10.9k/8.2k/7.8k over the same data) is
the symptom of the wrong form. Consequence: the renewal leak is **diffusion-shaped**
(∝ κ·√E, a Wiener boundary flux under interval-E re-inspection). The run kills the
diffusion **knee** (the 1/κ² plateau edge) — solid — but not diffusion as the leak
mechanism; the dossier's "not diffusion ⇒ tier structure" dichotomy overstates. The
mid-range budget reading survives (both fits cross ε = 5e-6 near E ≈ 430), the
extrapolation and the law statement do not.

**Attack 2 — below the swept floor.** E = 2 and 4 (7 seeds, 34.4M pair-kicks): 5 and 8
leaks — no zero-leak epoch exists except the structural E = 1. The headline verdict is
robust at the bottom; I folded this into the page.

**Attack 3 — belt-real time.** Undoing the disclosed 10× acceleration (j₀ geo-mean 10⁶,
hazard 3.5e-6, within 3.5× of the belt's w/C = 1e-6): leak/kick = 8.1e-8 / 2.8e-7 /
1.2e-6 at E = 64/512/2048 — ~19× below the accelerated curve, and ~2 orders under 08d0's
pooled-zero CI (≤ 5e-6 at E = 64), so no conflict with their measurement. But the
headline "6–8× looser than 08d0's E = 64" compares the toy's accelerated hazard to
08d0's belt hazard; at matched scale the factor is meaningless. The E* numbers are
toy-internal, as the dossier concedes ("IF the renewal model were the tier").

**Attack 4 — the P6 null.** In the same seed-5 runs the author cites: top-decile-by-hits
**hit** share = 0.28; leak share = 0.27/0.22. Leaks concentrate exactly as hits do —
hazard heterogeneity, no grazer effect. Pre-registered P6 (≥ 50%) failed, and
"consistent with 08d0's grazer law" is unsupported in this toy.

**Novelty.** The wiki page holds 08d0's knee (checker-measured 128–256) and its named
need for the pooled curve; no HISTORY entry or prior run does the κ-sweep or the
renewal-limit curve. New: the no-knee renewal limit, the κ¹ dependence, the freeze
discipline. Not new (and not claimed): the epoch frontier itself (08d0), the shipped-tier
kills (e87d, 1a29).

**Page.** Corrected in place, six fixes: √E law (current-best, Refuted, Runs), P6 null,
the hazard-scale caveat on E*, the P2/P6 prediction ledger, "≤ 2×" → "≤ ×4.6 (≈ κ¹)".

**Goal fit.** Board item 2 (encounter work at 10⁹); the epoch rule is the named
355 → ~5.5-core lever, and this run guards its adoption dial. PRINCIPLES 10 ("Write the
kill criterion before the run") and 20 (behaviours over seeds, pooled) are respected; the
honest failure reporting is the lab's culture working. But by its own statement there is
"nothing to adopt as code": no measured bottleneck moved, nothing deleted, and the one
premise reversed (P3) was the author's own, pre-registered and killed inside the run.
That is real, one named experiment short of gold.

## The one experiment to gold

Run the leak(E, κ) measurement on the shipped tier's own due structure — e87d's integer
replica (`arm_sections` + `arm_pair` + `dioph::first_hit`) with an epoch dial and a κ
dial, pooled seeds (the run's own open direction 1). Either it yields a freezeable E* at
a stated ε — the adoption this whole line is waiting for — or it shows 08d0's knee
transfers (1/κ²), closing the contradiction the page now records. The harness exists;
it is one run.

## What the author missed

- The √E law, and with it that their own data is diffusion-shaped: the mechanism story is
  "no diffusion-owned plateau, diffusion-shaped leak", not "not diffusion".
- The P6 null comparison (leak share vs hit share in the same runs).
- The hazard-scale non-transfer of the E* factor (acceleration disclosed, then ignored in
  the 6–8× headline).
- P2's ~50× hazard miss reported as "calibrated"; the A-fit range undisclosed; "≤ 2×"
  vs their own ×4.6 total.
- Credit where due: the paired-seed design, the integer-exactness control at E = 1, and
  the disclosures (clamp, acceleration, uniform re-deal) are exactly right.
