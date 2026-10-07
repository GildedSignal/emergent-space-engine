# Dossier — 20261007-1420-inversion-384f

The gold's phase-neighbour certificate is valid only for concentration that is *standing along one
shared orbit*: under the two other concentration topologies a game must have — lanes crossing at a
node (247/247 cross-family encounters missed, at any k) and traffic funneling through one
pericentre (413/413 missed, phase rank checks nothing) — it silently drops every encounter, the
window tier it was meant to replace is forced quadratic by orbit-path intersection alone
(candidates ×4.01 per fleet doubling at fixed density, 265 candidates per real encounter at n=800),
and the routing "dimensionless number" cannot exist as a scalar because the two topologies are
independent axes; the certificate that covers all three is the same O(n·k) trick with the ordering
variable changed to **arrival time at the exact orbit-intersection locus** — measured 1.000 recall
on the funnel (0.993 at k=4, 1.000 at k=8), 1.000 on the crossing node in its fine-seeded
configuration, and 0.101 with the final script's coarser gate: the gate must be a
certificate-grade exact intersection (a gate off by δ smears the arrival order by ~δ·sinθ/v),
which is one named experiment away.

## Bottleneck

Board risk #1 (5 October): candidate work must track real encounters (`q-candidate-degree`), and
the 6 October gold replaced the quadratic tier with phase rank under formations. This run measures
where that replacement silently fails, i.e. the seam between representations (PRINCIPLES #13:
errors never compound — a dropped encounter is not an error, it is a lost event).

## Evidence

All commands from `lab/results/20261007-1420-inversion-384f/`, each ≤ 60 s where possible
(truth passes are 6–70 s on this shared 8-vCPU runner; nothing else runs in-process):

```
python3 invert.py s1        # control: the gold's regime           (~15 s)
python3 invert.py s2        # crossing lanes                       (~70 s)
python3 invert.py s3        # pericentre funnel                    (~10 s)
python3 invert.py s2scale   # fixed-density scaling n=100/200/400  (~110 s)
```

Two-body Keplerian truth (μ=1, R_ENC=1e-3, window ≈ 1 orbit), brute-force KD-tree closest
approach with hop-proof coarse radius + per-pair refinement. Certificates: **phase-rank** (group
by quantized elements, k neighbours in mean-longitude order at window start and end), **window
tier** (pairs whose orbit paths pass within R_PATH), **time-rank@locus** (rank by per-body arrival
time at the refined orbit-intersection locus). Seeds fixed in the script; scenes not tuned after
first decisive run.

| scene | N | real enc (cross/int) | phase-rank k=4 | window tier | time-rank@locus |
|---|---|---|---|---|---|
| S1 formation (control, gold's regime) | 240 | 393 (0/393) | recall .964 (k8: 1.000) | 28,680 cand = 73/enc | n/a (degenerate: IS phase rank) |
| S2 crossing lanes | 400 | 660 (247/413) | **cross recall 0.000**, int .986 (k8: 0.000) | 79,800 cand = 121/enc | 0.101 (final, coarse gate); 1.000 (fine-seeded run); 2.3k checks |
| S3 pericentre funnel | 160 | 413 (413/0) | **recall 0.000** (55 checks; k8: 0.000) | 12,720 = C(N,2) = 31/enc | **1.000** (k8: 1.000), 2.9k checks |
| S2 scaling n=100/200/400 per family (fixed linear density) | 200/400/800 | 270/601/1204 (×2.0 per doubling) | cross 0.000 at all n | 19,900/79,800/319,600 (×4.01 per doubling → **quadratic**; 74→133→265 per enc) | — |

Machine state: Linux 8 vCPU, load 1.3–7.2 (shared with the window's other runs), 15 GB, temps
28–60 °C, memory used ≪ 2 GB per process.

## Predictions (predictions.md, written after tuning S1 only, before S2/S3)

- P1 cross-lane miss at any k: **held** (0.000 at k=4 and k=8, both scenes). Predicted
  cand/enc > 300 for S2, measured 121 — magnitude wrong (I underestimated internal encounters,
  413 vs ~200); the *composition* held exactly (candidates = n_A·n_B + 2·C(n,2), all cross pairs).
- P2 quadratic at fixed density: **held** (×4.01 candidates, ×2.0 encounters per doubling).
- P3 funnel total miss + C(N,2) candidates: **held** (0.000 recall; candidates exactly C(160,2)).
  Predicted > 200 cand/enc, measured 31 — encounters more numerous than my estimate (413 vs ~60).
- P4 repair ≥ 0.95 at k=4: **held on the funnel** (0.993 at k4, 1.000 at k8); **partially held on
  the skew crossing node** — an early complete configuration measured 1.000 cross recall there
  (locus from fine mutual-proximity sampling, 6,391 checks), but the final script's
  sampling-tolerant gate (needed to detect loci cheaply across many groups) leaves cross recall at
  0.101. Root cause measured: a gate displaced by δ smears the arrival ordering by ~δ·sinθ/v, and
  the encounter window is R_ENC/v_rel ~ 6e-4, so the gate must sit within ~1e-4 of the true
  curve intersection. That exact-intersection refinement is the named next experiment; P4 is
  therefore NOT fully held and the repair is one experiment short on skew crossings.
- P5 no scalar trigger: **held** (S3: phase-concentrated 126× uniform AND max group fraction
  0.019 — concentrated in phase and space yet on zero shared orbits; S2: element-concentrated
  per family with all real encounters cross-family).
- Kill criteria for my own claim: not triggered (cross recall under phase-rank is 0.000, not ≥ 0.5).

## What would make it wrong

The miss claims are structural (pairs in different orbit groups are never checked by construction),
so they are wrong only if the shipped certificate groups differently than "same orbit family" —
e.g. if it ranks *all* bodies in one global arrival-time-like order, it is no longer the gold's
phase rank and is closer to the repair proposed here. The quadratic-tier claim assumes the
candidate tier keys on orbit-path overlap; a tier that keys on something coarser (spatial cells in
time, like the funnel locus) would change the constant, not the crossing-scene miss. The repair's
crossing-node result depends on gate placement: measured exactly with the gate on the true
intersection; a gate off by δ smears the arrival ordering by ~δ·sinθ/v (my own intermediate
implementation at δ≈0.05 dropped cross recall to 0.065 — kept as the honest failure mode, see
run history in git patch).

## Cost of adopting, fit with PRINCIPLES

The repair is not a new mechanism but the same O(n·k) rank certificate with its ordering variable
derived from the encounters' own geometry: "an encounter is a near-coincidence of two worldlines at
a shared locus; rank by arrival time there." A formation is the degenerate locus (the whole orbit;
arrival-time rank at any fixed longitude *is* phase rank), a node and a pericentre funnel are point
loci. That is PRINCIPLES #32 ("symmetry is found, not given … under the right representation") and
#35 (simplest form from the dynamics); it also matches "the same law at every scale". Cost: loci
must be exact curve intersections (a certificate-grade geometric object, computable once per
orbit-pair family change), and arrival is per-body closest approach to that point. No changes to
main, docs or crates: this run edits only its own folder.

## The lens (what inversion may have made me miss)

Inversion finds how the design fails; it does not measure how *frequent* crossing lanes and
pericentre funnels are in the game Julien wants (the traffic argument is from the goal — factions,
trade, interception — not from a measured scene distribution). I attacked the board's one-line
summary of the gold; the gold's own artifacts (on its branch) may already scope its certificate to
formations only, in which case this run's kill lands on the *routing rule* ("concentrated → phase
rank") rather than the certificate itself, and the funnel/crossing scenes plus the arrival-time
repair are the new content. The window-tier model here is geometric candidacy only, without the
conjunction-window arithmetic of r8/q-candidate-degree, so the 121–265× constants are lower bounds
of that tier's true cost, not reproductions of its 135×.
