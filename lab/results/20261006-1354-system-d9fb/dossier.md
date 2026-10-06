# Dossier — 20261006-1354-system-d9fb (system lens)

## Claim (one sentence)
The encounters subsystem's three adopted components (Binet-cone tier with per-pair numeric
windows, co-orbital phase train, slack skin) are NOT one storeless mechanism: the storeless
band watch (per-body exact equation-of-center constants + closed-form alignment epochs) is a
sound necessary filter that deletes the store and the setup, but it misses 16–28% of real
encounters — the tangency dips, closest approaches with no resolvable true-longitude
crossing — which is precisely the population the tier's per-pair second-order windows exist
to catch; the kill criterion I pre-registered fired.

## Bottleneck
Board focus item 3 (encounters without work per orbit or per element change) and this
morning's gold (components-4643: window setup is 92% of per-kick evals; deferral re-pays
setup; "the slack skin stays the lever"). The system-lens question: is the setup — the
expensive part — a per-pair re-derivation of per-body information, such that the whole tier
collapses into one kinetic watch with nothing materialized?

## What the watch is (the tested unification)
Per pair, O(1) unless an epoch exists: (1) r-range theorem filter; (2) band epochs from the
linear mean-longitude drift |Δλ(t)| ≤ C_i + C_j, where C is each body's EXACT max
equation-of-center — a per-body constant, in fact a table in e alone (this is the "two
mechanisms secretly one" candidate: the crate's per-pair numeric window setup re-derives,
20 evals per pair per kick, information that is per-body); (3) inside epochs only:
alignment roots by sign-change bisection + per-epoch golden-section d² minimum. No sections,
no windows, no store: 2N certificates. Reproduce (each ≤ 60 s except uniform:1000):
`cd lab/results/20261006-1354-system-d9fb && python3 watch.py uniform:250:1 uniform:500:1`
and `python3 watch.py phalanx:250:4 clumped:250:3` (numpy only; results in metrics.json).

## Evidence (Linux x86, shared 8 vCPU, < 300 MB; ρ = 1e-4, T = 20 orbits, σ_e = 0.01 belt /
0.05 adversarial, truth = theorem-filtered dense sampling + 2% unfiltered audit + ultra-dense
adjudication of every dispute; every disputed pair was adjudicated, none trusted from either
instrument alone)

| scene | truth enc | watch found | misses | conj-less (caught) | evals/enc | epochs/body | cone pairs vs certs |
|---|---|---|---|---|---|---|---|
| uniform:250 | 7 | 7 | 0 | 0 | 5.95e4 | 5.0 | 4,286 vs 500 |
| uniform:500 | 29 | 21 | 8 (28%) | 2 (1) | 7.80e4 | 5.3 | 19,864 vs 1,000 |
| phalanx:250 | 43 | 36 | 7 (16%) | 16 (13) | 1.39e5 | 69 | 17,618 vs 500 |
| clumped:250 | 34 | 26 | 8 (24%) | 3 (1) | 2.32e5 | 97 | 21,418 vs 500 |

- **Soundness KILLED (P1).** Every miss adjudicated REAL by ultra-dense sampling (d down to
  6.6e-6, 15× inside ρ). Diagnosed mechanism (measured, pair 13–134, uniform:500): two
  alignment roots 0.125 apart at d ≈ 1.4e-3 each, with the true minimum 8.1e-5 BETWEEN them —
  a tangency dip where the pair's radii and longitudes nearly coincide without a crossing;
  pair 141–303: a no-crossing dip 0.3 wide that a 12-points-per-orbit grid never samples.
  Golden-section on the epoch is not the cure: multi-minima epochs send it to the wrong dip.
- **The band mechanism itself held where it applies:** 13 of 16 conjunction-less encounters
  caught in the phalanx (the mean-longitude band covers quasi-satellite geometry), and the
  r8 v2 leak population is real and counted: 6.9% conjunction-less at belt scale (P2 held:
  predicted 1–10%), 37% in the phalanx.
- **What survives of the unification (measured):** the store is deletable — cone-passing
  pairs are 14–69% of N²/2 (4,286–21,418 pairs) against 2N certificates, so the tier's
  memory (the gold's 40-TB ruin arithmetic) becomes O(N) with zero setup by construction
  (the skin's reason to exist disappears). Epochs per body are flat and small (5.0 → 5.3
  from N=250→500; ≤ 6 per pair at σ_e = 0.01): the event schedule itself is linear and
  bounded — the O(N²) never materializes as work in my harness.
- **Per-event cost is NOT competitive (honest deficit):** 6e4–2e3e5 evals per encounter,
  per-pair max 2,626–20,956 evals (P4 killed): without the crate's Diophantine jump over
  distant alignments, grid+roots is ~10³× the tier's ~32 evals per pair-kick. The tier's
  cheap walk, not its windows, is the part worth keeping.

## Predictions
`predictions.md` was written before any run. Held: P2 (conjunction-less fraction 1–10% at
belt scale; caught by the band where mean-longitude structure exists), P6 (cone fraction
0.14–0.69 of N²/2; the memory deletion arithmetic). Killed: P1 (misses everywhere but the
smallest scene — the pre-registered kill), P4 (fat per-pair tails), and P3/P5 were not
decidable in the window (no N ≥ 1000 truth run; the rank check was dropped in a rewrite).
The lens told me to name the case that could break the unification; I named the
conjunction-less population, and the actual breaker was its second-order cousin.

## What would make it wrong
The miss diagnosis rests on ~15 adjudicated pairs across two seeds and four scenes, one
orbit solver (Newton Kepler, shared by both instruments — the audit path differs in sampling
bias, not in the solver), and no kicks (fixed elements between events, as in the crate's
spec). The 28% miss rate is specific to ρ = 1e-4 and σ_e = 0.01–0.05; the mechanism
(tangency dips) is not.

## Cost of adoption, fit with PRINCIPLES
Nothing to adopt whole. The adoptable fragment: per-body C_e constants + closed-form band
epochs as the crate's candidate filter (deletes the materialized store and re-prices setup
from per-pair to per-body), keeping the per-pair second-order window and the Diophantine
walk inside epochs. That is a reorganisation of `crates/encounters`, not a law change. Fit:
"A fix signals the wrong representation" (#19) cut both ways here — the tier's window is not
a bandaid, it is the second-order structure; "compute only surprises" (#3) and the memory
floor (#24) are what the storeless epoch filter serves. The negative result itself is the
deliverable: a one-mechanism encounters layer is falsified at ρ = 1e-4; the search space for
q-skin's successor narrows to "setup → per-body constants, windows stay".

## The lens (what the whole-system view made me miss)
Hunting for the elegant collapse, I under-built the tangency resolution and nearly ran out
of time in the harness (five index bugs burned a third of the window; the first smoke run
would have shown the misses had the instrumentation lesson — adjudicate disputes — not been
applied). A dynamics lens would have derived the dip-width-to-grid-spacing condition before
writing code; a components lens would have kept the tier's walk from the start. The measured
flame: my own negative control (pre-registered kill criteria) is what makes this report
trustworthy.
