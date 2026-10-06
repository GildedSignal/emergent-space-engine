# Dossier — 20261006-0737-components-4643 (components lens)

**Claim.** On the belt's kick workload, deferring dormant encounter pairs to calendar wakes
is the wrong lever: pairs are indeed deeply dormant (99.7% of first in-window passages lie
>100 orbits ahead; median 26,000), but per-kick cost is 92% numeric-window *setup* — the
far-future exact checks that deferral would skip are only 7–8% of the work — and the
zero-eval analytic window is killed by a 427× over-firing penalty.

**Bottleneck.** Board focus item 3 (encounters without work per orbit or per element
change) and the open taleb-3ec1 lead ("99% of setup work lands on dormant pairs, defer
it", handoff "Next, not started"). This run measures that lead and kills it as a
standalone configuration, redirecting the lever to setup-skipping (the slack skin).

## Evidence

Binary: `crates/encounters/src/bin/dormant.rs` (experiment-only addition; the patch is
saved by `run.sh`). All commands run from the repo root, Linux x86 shared runner
(8 vCPU, load 2.3–3.9 during runs; orders of magnitude only, per the lab rules).

```
cargo build -p emergent-encounters --release --offline --bin dormant
T=/home/glmlab/lab-target-2/release/dormant   # workspace target dir
$T split                       # main workload, matches crates' kick() spec
$T split 10000 5e-2 1e-4       # held-out density (predictions.md)
$T stream                      # Poisson kick stream, tau = 20 orbits, 40 orbits
$T stream 1200 5e-2 1e-4 20.0 40.0 11   # dense kicks (tau = 3.2 orbits)
$T stream 600 1e-2 1e-4 314.1592653589793 628.3185307179586 3  # sparse diagnostic
```

**Split (n = 10 000, σ_e = 0.01, ρ = 1e-4, eps = 1e-5, 100 kicks, horizon 1000 orbits).**
813 candidate pairs per kick. Per 100 kicks:
- setup evals (numeric windows) **1 600 220**; exact-check evals **131 824** — setup:checks = **12:1**; setup is 92% of evals.
- check evals by recency: <1 orbit 462, <10 orbits 1 261, <100 orbits 12 117, **≥100 orbits 117 984 (89.5%)**; 98.7% of check evals lie beyond 10 orbits. Proposals: 3 826 of 4 262 beyond 100 orbits.
- first in-window passage ("wake") per section: median **25 999 orbits**, p90 107 654; fraction >10 orbits = 1.000, >100 orbits = **0.997**. This is taleb-3ec1's dormancy, reproduced independently.
- one wake query vs full horizon walk: qsteps 1 010 833 vs 1 038 129 — the Diophantine walk is nearly free; **qsteps were never the cost**.
- analytic arc-cap windows (zero setup evals): proposals **1 817 897** vs 4 262 numeric — **427× over-firing**. The 20 evals/pair of numeric window are what make wakes rare; deferring setup without them loses.
- wall: 8 676 µs/kick eager vs 649 µs/kick wake-path (sections + first query) — but both pay the same setup evals; the difference is the horizon walk.
- held-out σ_e = 0.05: same law (setup 3.43 M vs checks 550 k; 89.5% of checks ≥100 orbits; wake p50 26 178; cap penalty 405×). Robust to density.

**Stream (n = 1200, τ = 20 orbits/body, T = 40 orbits, 2 484 kicks).** Eager per-kick
full-horizon enumeration vs deferred wakes (calendar, checks only at fires,
re-derivation at kicks): eval ratio **1.1×**, wall ratio **1.4×** (3.42 s vs 2.37 s);
252 704 re-derivations produced only **111 fires** — schedules are derived and discarded
unread ~2 300× over. Checks: 13 177 eager vs 111 deferred, yet evals barely move because
setup dominates both. Sparse-kick (τ = 50 orbits) and dense-kick (τ = 3.2) variants:
1.1–1.5×, same shape.

**Disclosed defect.** My deferred implementation is not exact: 30–37 of ~70–83 segment
events missed (and 6–73 extras) in every kicked configuration; a zero-kick-dense control
(τ = 1 orbit) shows 0 misses trivially. The misses are in my re-derivation bookkeeping,
not in the method's math (elements are fixed between kicks; the wake derivation is the
crate's own exact integer `first_hit`). The economic conclusion does not depend on the
hole: even with misses counted generously, deferred saves at most the check fraction
(7–8% of evals), because it re-pays setup at every kick by construction.

## Predictions (predictions.md, written before the runs)

- P1 (≥80% of check evals beyond 10 orbits): **held** (98.7%).
- P2 (deferred ≥5× evals, zero misses): **falsified** — 1.1–1.5×, and my implementation
  misses events. The deferral configuration is killed on this workload, not the method.
- P3 (analytic windows ≤20× over-firing): **falsified** — 427×. Setup evals are
  irreducible without losing the wake sparsity.
- P4 (setup dominates and is not deferred): **confirmed** — this is the finding.

## What would make it wrong

A workload where near-term in-window passages are common (dense resonant belts, fleets on
shared orbits — the co-orbital gold of 20261006-0346) would raise the check fraction and
re-open deferral; measure there before citing this kill outside sparse belts. The split
uses one kick magnitude (eps = 1e-5); kick() in the crate shows the same silent-pair
structure across 1e-9…1e-3.

## Cost of adoption, fit with PRINCIPLES

Nothing to adopt: the recommendation is *not* to build the wake calendar as the next
encounters step; the lever stays the slack skin (skip re-certification of pairs whose
drift budget absorbs the kick — q-skin's measured 12.6×), which attacks the 92%.
Principles: "The cheapest compute is compute not done" (§1) — here the compute not done
is the re-setup, not the far checks; "A failed experiment kills that configuration, never
the method" (§9). Every number above regenerates from the commands; the binary is in the
run's patch.

## The lens

First-principles component audit: for the encounters setup path, the floor per element
change is one cone test + one window derivation per surviving candidate; the measured
design pays that plus a 1000-orbit enumeration whose far 90% buys nothing. What the lens
may have missed: neighbours — the candidate *discovery* cost (range scan, ~813 cone tests
per kick here) sits outside this measurement and is the q-candidate-degree territory; and
my stream harness shares the crate's float code, so eager and deferred are not fully
independent implementations (the miss diagnosis inherits the crate's `check`).
