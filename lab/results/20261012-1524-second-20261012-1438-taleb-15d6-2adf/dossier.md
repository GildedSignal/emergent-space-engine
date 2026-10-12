# Dossier — second author on 20261012-1438-taleb-15d6: the built co-orbital certificate is sound everywhere; its cost is set by a number its gates never measure — the fleet's worst-eccentricity window, quadratic in n at fixed e-spread

## Claim (one sentence)
The named experiment, run against the built certificate (`phase.rs` on `wt/cx-b-coorbital-cert`, adce00d6), flips the original headline: the built cert misses **zero** contacts on every break scene and at both 10⁶ headlines, but its O(n·k) promise degenerates at the gold's own 10⁶/gold-e headline to k p50 **3411** (3.41×10⁹ visits, 1379 per contact, vs 3.1 for the tight fleet) because reach = ρ + 4·e_max + shear·H/2 is 99.5% equation-of-centre — the e-tail **order statistic** (4.5× the median, untrimmable: worst→median −3.7%, top-10→p99.9 −10%) — making the phase tier quadratic in n at fixed e-spread (measured exponent 2.04), invisible to every gate on the branch (whose only scale test is a shared-shape ring where the EoC term is exactly 0), while the rank-4 premise it replaced stays false (88%/43% beyond rank 4) in the lens and board text that still carry it.

## Bottleneck
The board's top scaling risk (candidate work must track real encounters) at the freeze about to
happen (`b-coorbital-cert`, in lab/queue.txt; branch built 10 Oct). The certificate's cost
guard is the missing piece: the regime number is neither the rank-4 of the gold's premise nor
the ρ-occupation of the author's census, but the window occupancy k = reach × local λ-density,
free to compute (two-pointer over the sorted mean-λ the cert already builds) before any visit.
Expected gain: the integrator adopts the cert with an honest cost model instead of a k=4
promise that is 853× off at its own headline — and knows the tree-tier fallback is C(n,2) at
co-orbital concentration, so cost must be budgeted in k, not escaped by tier change.

## Evidence
All in `evidence.log`, raw JSON in `run-log.txt`; every command ≤ 20 s except treefall (146 s,
documented); peak RSS 211 MB. Build line and sources at its head (author's and checker's
instruments verbatim; phase.rs/tier.rs verified byte-identical to the branch and to the
checker's patch copies; my `second.rs` adds decomp/surgery/scaling/treefall).
1. Record regenerates: `redteam control|pileup` bit-identical to the author's numbers (314/313/one-5; 757/14.4%/max 9).
2. Soundness: `checkadv built` 0 misses on all six scenes; `checkadv builtsnap` 0 window misses at 1e5/1e6 tight and 1e6 gold-e.
3. Cost: k p50 3411 at 1e6-gold-e (1379 visits/contact), 48 at 1e6-tight (3.1); reach decomposition EoC 99.5%; k_pred = reach·n/TAU within 0.1% on uniform fleets, lower bound on clumps.
4. Scaling: visits 3.09e7 → 3.41e8 → 3.41e9 over n = 1e5 → 3.16e5 → 1e6 (exponent 2.04); surgery shows order-statistic robustness (−3.7%/−10%, contacts unchanged).
5. Gates blind by construction: branch's only scale test asserts k=1 on a uniform shared-shape ring (measured eoc = 0.0 on that fleet).
6. Fallback: tree tier = C(1e5,2) = 5.0e9 candidates at gold-e concentration (146 s), so a refuse-when-k-large guard preserves soundness and honesty, not cheapness.

## Predictions
`predictions.md` written before any run. Held: all reproductions (R1–R3), H1 (every bound:
gold-e reach 0.0214 ∈ [0.018, 0.024], k 3411 ∈ [2800, 3900], tight EoC 2/3 → 66.9%), H3 on
uniform fleets (0.999–1.056), H4 (branch gate k=1, shared-shape), H5 (stale texts read).
Missed, reported: **H2** — one hot body does NOT set the cost (predicted 5× drop, measured
−3.7%): at n=10⁶ the Rayleigh tail is dense, so k rides the order statistic e_max ≈ σ√(2 ln n),
which no small trim moves; and **H3's implication** — the tree-tier fallback is itself
quadratic at concentration, so the guard is a cost-honesty device, not a cheaper tier. Both
misses sharpen the claim rather than weakening it.

## What would make it wrong
The t=0 soundness check at 10⁶ tests the cert's own guarantee (mean-λ gap ≤ reach at the
midpoint) against a position-grid truth, not a full-horizon brute force (impossible at 10⁶);
the six-scene probe does run full brute truth over the horizon, and the cert's window proof is
then the metric, and I did not time a full 3.4e9-visit `group_events` at 10⁶ — visits are the
measured proxy here; a builder should time it. The e-band splitting alternative is design,
unmeasured here. The contact model remains the gold's own (conjunctions below ρ, Keplerian, no
mutual gravity), inherited from both prior runs.

## Cost of adoption, fit with PRINCIPLES
Adopt in the merge review of b-coorbital-cert: (1) correct the stale premise in
`lab/lenses/b-coorbital-cert.md` and board.md's gold entry (rank 4 is false at the headline;
the cert's text already knows); (2) require the free k measurement (two-pointer on the sorted
λ, before any visit) in the cert's gates, with a clumped-λ and heterogeneous-e scale scene —
the branch's shared-shape-only scale test cannot see the regime it must guard; (3) treat
k as the budgeted quantity in the allocator (PRINCIPLES #12, smoothness: 3.41e9 visits is a
spike, not an average). Fit: "Certificates need independent, adversarial checks" (Truth) —
this is the second check, aimed at the built artifact; "regimes are chosen by dimensionless
numbers" (#4) — the number is k (EoC-reach × λ-density), not occupation alone; "a failed
expectation is not automatically a failed method" (#9/H0183) — the method stands, the cost
model was the broken expectation; error types over error size (#2): zero misses, quadratic
cost — the failure mode moved from correctness to smoothness.

## The lens
Second-author lens: the checker named one experiment; doing it and only it would have
re-reported their numbers. What it may have made me miss: I did not time the shipped
`group_events` end-to-end at 10⁶ (visit counts stand in for cost), did not test the e-band
splitting that would actually cap k, and did not re-run the author's full snap/espread
battery (checker-reproduced; nothing here rests on it). The run inherits both prior runs'
contact model (ρ-conjunctions, no mutual gravity) — if that model is wrong at formations,
all three runs share the bug: agreement here is not independence on that one point.
