# Dossier — 20261009-1556-inversion-3036 (lens: inversion)

**Claim.** The phase-neighbour certificate adopted from gold `20261006-0346-taleb-09b5` is blind
across orbit groups — in every crossing-orbit scene it misses **100% of real cross-group
encounters** (583/583, 73/73, 377/377, 4/4) — and the cone tier it was meant to replace covers
those scenes only by admitting **all** n_A·n_B cross pairs, so the board's top scaling risk
(candidates per body growing with N) is alive in exactly the scene a faction game has: two
formations meeting; a time-sorted node-event certificate finds every cross encounter with
candidates that track encounters under dilution.

**Bottleneck.** "Candidate work at scale … work must track real encounters" (HANDOFF, risks;
board focus, 5 October). Not a speed gain: a correctness hole plus the surviving O(N²) term.
What it deletes: the premise that one intra-orbit rank certificate covers concentrated
workloads; what it adds: the missing cross-group tier, measured at O(n) at fixed fleet density.

## Evidence (decisive run `work/run5.jsonl`, 4.95 s wall, 5.9 MB peak RSS, 4 threads, shared 8-vCPU runner)

Scenes: μ=1, ρ=1e-3, fleets n=250 (S2b: n_B=100), groups **given with true labels** (generous —
any per-group concentration trigger fires on each group, since per-group spreads equal the
gold's own scene: a∈U[1,1.0001], σ_e=3e-4, the crate's `coorbital` spec). Truth: the crate's own
`truth_pair` (r8 v2 truth; used unmodified). Full horizon 2 orbits (S2b: 20).

| scene | truth intra / cross | phase cert cross miss | cone cross cand (all = n_A·n_B) | node cert cand / miss |
|---|---|---|---|---|
| S1 one formation (control) | 389 / 0 | — | 31,125 intra = **all** pairs | — |
| S2 two fleets, 1:1 crossing | 950 / **583** | **583/583 = 100%** | 62,500 (**100%** of pairs) | 6,296 / **0** |
| S2c same, arcs ×10 (dilution) | 111 / 73 | 73/73 = 100% | 62,500 (unchanged) | 995 / 0 |
| S2b detuned a_B=1.05, 20 orbits | 1,313 / 377 | 377/377 = 100% | 25,000 (all) | 7,758 / 0 |
| S3 lone crosser through a fleet | 370 / 4 | 4/4 = 100% | 250 (all) | **15** / 0 |

Derived: work per real cross encounter — cone 107 (S2) → **856** (S2c: candidates did not move
while encounters fell ÷8); node 10.8 → 13.6. Dilution: encounters ÷7.99, cone candidates ÷1.00,
node candidates ÷6.32 (tracks). At 10⁶+10⁶ with this geometry the cone tier's cross candidate
list alone is 10¹² pairs (~8–16 TB) — the gold's ~40 TB blowup returns through the fleet-battle
scene. Node-certificate sensitivity (window = 3ρ/|Δv| + spread margin ≈ 0.013): s2/s3/s4 give
5,368 / 6,296 / 7,236 candidates, zero misses at every safety.

Secondary (intra, same runs): the rank-4 certificate held only approximately **within** a
fleet: static sort misses 4.1% (S1) and 43% (S2b, 20 orbits — drift walks ranks); maintained
order (re-sorted at each encounter's time) still misses 1.0–6.4%. The gold's "every real
encounter lies within partner rank 4" needs a stated a-spread/phase-spacing bound and a
re-sort cadence; it is not a property of the orbit.

**Commands** (from the repo root, each ≤ 60 s):
```
cargo build --release --offline -p emergent-encounters --bin inv3036
$CARGO_TARGET_DIR/release/inv3036        # one JSON line per scene; INV_DEBUG=1 for diagnostics
```
Everything lives in one new file, `crates/encounters/src/bin/inv3036.rs` (saved as
`work/patch.diff`); no crate file touched.

**Predictions** ([predictions.md](predictions.md), all written before the first run): P1 cone
part exact (31,125 = n²/2) but the phase cert's intra zero-miss **failed** (16 static / 4
maintained out of 389 — reported, not hidden); P2, P3, P6 held exactly; P4 held in order of
magnitude (cross rate 0.93% per pair per 2 orbits); P5 held (0 misses on all four scenes,
candidates ∝ n at fixed density); P7 held (÷8 encounters, cone ÷1.00, node ÷6.3). Debug
disclosure: runs 1–4 (`work/run1..4.jsonl`) fixed four bugs **in my probe**, not in the crate:
fleet B's arc was placed by mean instead of true longitude (the rendezvous never happened),
`mean_body` averaged ϖ linearly across the 0/2π wrap, the longitude-spread margin was not
circular, and the miss-check compared per-group against global indices. The truth and cone
calls were the crate's own throughout.

## What would make it wrong

The phase certificate as deployed could keep a cross-group tier (cone or node) beside the rank
tier — then the 100% miss becomes "only" the surviving quadratic: both readings are measured
above, and the adopted text ("replaces the quadratic tier", "overrides zero misses for
concentrated workloads") does not say which. If the integrator's design already contains a
group-pair node certificate, this run is its missing measurement, not a kill. The node-cert
cure here assumes group labels given (clustering orbits in element space is unsolved above)
and its margin is paid in element spread; it is a sketch measured against truth, not an
integrated tier.

**Cost of adopting.** One build step in `crates/encounters`: per group-pair, crossing
longitudes from Binet (closed form), per body exact `passage_tick` events, a sorted two-pointer
— O((n_A+n_B)·orbits) per group-pair, no per-pair work; it would replace the cone tier for
crossing group-pairs and leave the rank tier intra. **Fit with PRINCIPLES:** the inversion lens
did what it exists for — "a failed expectation is not automatically a failed method: diagnose
which one broke" (H0183); "candidate work must track real encounters" is the board's own bar,
and the cone tier fails it by ÷8 under dilution while the node cert tracks at ÷6.3. The scene
is not contrived: the player is "the only wildcard, and their influence travels at c" (§5) —
S3 is a transfer orbit through a fleet, and the adopted certificate misses every contact.

**The lens may have missed:** intra-orbit behaviour at other spreads (my fleets are diffusive:
spacing ≈ ρ, drift ≈ 2 spacings per horizon — tighter formations would restore the gold's
rank-4 exactly); 3-D inclined crossings (nodes still exist, same certificate); the cost of
group discovery; and whether the real adoption already scopes the rank tier per-orbit with a
cross-orbit fallback — the board text does not show one, but the b-coorbital-cert build is in
flight and may add it.
