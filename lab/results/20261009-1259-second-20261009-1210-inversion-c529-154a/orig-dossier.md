# Dossier — 20261009-1210-inversion-c529 (lens: inversion)

**Claim.** The co-orbital gold's "every real encounter lies within partner rank 4 along the
orbit" is a property of the scene it was measured on (50 orbits, σ_e = 3e-4 so 2aσ_e < ρ),
not of co-orbital concentration: at 10× the horizon the same clump needs rank 42 (72% of
encountering pairs beyond rank 4), an equal-period formation with 1% eccentricity spread
misses 36% of encountering pairs at *any* rank cadence because the order is frozen while the
partner set is wrong, and a fleet with crossing traffic (identical concentration τ = 0.94 vs
1.00) loses 97% of its 542 cross encounters under a wholesale phase-rank tier — so the
certificate must be per-pair (Binet ΔU classifies intra-clump vs cross; the cone caught
6000/6000 cross pairs) with a declared validity regime, not population-triggered.

**Bottleneck.** "Candidate work at scale" (HANDOFF's first risk): the co-orbital certificate
is being built now (`lab/lenses/b-coorbital-cert.md`, GLM + Codex lanes). This run is the
pre-freeze red-team for it. The gain is not a speedup but avoiding a wrong freeze: a
certificate adopted with the gold's gate ("zero misses on the gold run's scenes and a dense
ring") ships misses that scale with horizon, eccentricity spread and traffic — exactly the
compounding kind ("errors that can compound", OC#34). It also says what to delete: the search
for a population-level concentration trigger (any scalar blind to 2ae/ρ and to sweep cannot
separate the scenes below).

**Evidence.** All scenes are Keplerian rings in the encounters crate's own harness (truth =
per-pair conservative advancement over the radial superset, `truth_pair`; certificate = rank
in mean longitude at t = 0, symmetric-min, the liberal reading). Probe:
`crates/encounters/src/bin/inversion.rs` (reverted by run.sh; kept in `work/`).

```
cargo build --release -p emergent-encounters --bin inversion   # 5 s
$CARGO_TARGET_DIR/release/inversion control   # 3 s  -> work/control.jsonl
$CARGO_TARGET_DIR/release/inversion heldout   # 42 s -> work/heldout.jsonl
$CARGO_TARGET_DIR/release/inversion audit     # 6 s  -> work/audit.jsonl
python3 work/audit_check.py                   # 22 s -> work/audit-check.txt
```
(target dir is shared: /home/glmlab/lab-target-1)

| scene | enc events | pairs | pairs beyond rank 4 | k* | silent λ-swaps |
|---|---|---|---|---|---|
| C1 gold shape (H=50, σ_e=3e-4) | 2202 | 142 | **0 (0%)** | 4 | 32 |
| H1 = C1, H=500 | 20810 | 1185 | **851 (71.8%)** | 42 | 363 |
| E1 equal periods, σ_e=1e-2 | 560 | 28 | **10 (35.7%)** | 8 | 0 (order frozen) |
| E2 equal periods, σ_e=3e-3 | 480 | 23 | 1 (4.3%) | 5 | 0 |
| B1 belt n=1000, σ_e=1e-2 | 6195 | 5882 | 5580 (94.9%) | 549 | 49567 |
| B2 belt n=1000, σ_e=3e-4 | 1735 | 1249 | 1060 (84.9%) | 97 | 8153 |
| M1 fleet + 20 rogues | 2744 | 667 | 513 (76.9%) | — | 155571 |

M1 detail: 542 cross (fleet×rogue) encounters; 14 of them λ-rank-4 at t0 (**97.4% missed**
by a wholesale phase-rank tier); **542/542 are Binet-cone candidates** and all 6000
radially-overlapping cross pairs pass `is_candidate` — composition (rank intra-clump + cone
for the rest) loses nothing and stays linear. τ_band = 0.938 vs C1's 1.000: any threshold
that fires for the gold's clump fires for the mixed scene.

E1 audit (independent Python solver, `work/audit_check.py`): pair 33/259, equal exact
periods, e = 1.08e-2 / 1.84e-2, mean-longitude gap 2.4 spacings (rank 8), minimum distance
1.8e-4 < ρ repeating every period (t = 0.088 + k·2π), below ρ for 1.24% of *all* time — a
permanent encounter partner that no re-ranking ever surfaces, because the order never changes
(0 crossings in any horizon). The miss is epicycle reach: encounters at 2aσ_e/ρ = 0.6 / 6 /
20 give 0% / 4.3% / 35.7% of pairs missed.

**Predictions** (`predictions.md`, written after controls C1/E0 only): all held. H1: k* ≥ 15
(got 42), event-miss in 20–80% (50.3%), silent swaps ≈ 320 (363). E1 fork (a): enc ≥ 100 and
miss > 5% (560, 35.7%); E2 in between (4.3% > 0). B1: miss > 80% (94.9%), k* > 100 (549),
silent/encounter-swaps > 50 (826). M1: ≥ 95% of cross missed (97.4%), 100% cone (542/542).
Two soft misses, both stated: B2's k* came at 97 against a predicted > 100 (mechanism
unaffected: B2 ≈ B1 with 33× less σ_e, so a-spread — not σ_e — rules belts); M1 produced 542
cross encounters against a predicted 10–200 (under-guess, in the direction that strengthens
the claim).

**What would make it wrong.** (1) If the built certificate ranks in *true* longitude evaluated
at query time rather than mean longitude at t0 — my probe tests the gold's stated "rank along
the orbit" reading; note that continuously re-evaluated geometry is the cone tier again, and
the O(n·k) claim then has to say when ranks are refreshed (λ(t) is analytically known per
body, so lazy re-rank on sweep is possible — that is a design answer my probe demands, not
one it disproves). (2) If kicks in the live engine re-sort elements so often that ranks stay
fresh: E1 shows freshness is not the failure — the partner *set* is wrong while the order is
frozen. (3) If the build exhibits a population-level trigger that separates C1 from E1 and
M1: both have the same clump, so the number would have to see σ_e and traffic — i.e. stop
being a concentration number; the burden is on that build. (4) Planar, unperturbed Kepler
only; inclined crossings and kick-scheduled re-sorts are untested.

**Cost of adopting.** Nothing in the crate changes (probe is a separate bin, reverted). The
build brief gains: three gate scenes (long-horizon clump, equal-period formation with e-spread,
fleet + crossing traffic), two declared validity bounds — rank validity horizon
k*(H) ∝ 3π·(Δa/a)·H/spacing, and the epicycle bound 2ae ≲ ρ — and per-pair (ΔU)
classification instead of a population trigger. Composability is already free: the cone
covers cross pairs exactly (6000/6000 here).

**PRINCIPLES fit.** "A failed expectation is not automatically a failed method: diagnose
which one broke" — the gold's measurement is right and its generalisation is wrong; the
certificate survives with bounds. "Write the kill criterion before the run, with controls on
both sides" — the gold's gate has the passing side only; C1/E0 and B1/M1 are the two sides
here. "Behaviours over many seeds; no engineered outcome" — k* and misses are behaviours, not
trajectory identity; seeds are fixed and listed in the probe.

**The lens.** Inversion found the gold's hidden scalars (horizon, 2ae/ρ, traffic) by asking
what the scene silently assumed. What it may have missed: I did not test a
true-longitude-ranked or sweep-corrected certificate (the natural patches — the run's job was
to break the assumption, not to build the fix); one seed per scene (fat tails in k* across
seeds unmeasured, though dose-response is monotone and mechanism-backed); inclination (3D
nodes would only add cross-encounter structure); and the gold run's own dossier was not
readable from this tree, so "partner rank along the orbit" is my stated reading of the
board's summary — if the original meant something subtler, this dossier attacks that reading,
and the checker should pull `lab/results/20261006-0346-taleb-09b5` from its branch.
