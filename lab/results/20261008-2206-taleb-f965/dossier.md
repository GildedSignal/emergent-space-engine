# Dossier — 20261008-2206-taleb-f965 (Taleb)

**Claim.** The adopted co-orbital certificate is unsafe as a tier replacement in three measured
ways — a global phase-rank trigger drops 66–94% of real encounters on any mixed scene, the static
rank-4 silently drops 6–8% of tail convergences inside pure fleets (fixed by a one-orbit refresh
cadence), and family-level crossing gates are sound only while a family's internal spread stays
near ρ (wedge scenes miss 8–16%, held-out confirmed); the concentration trigger must therefore
gate only the *intra-family* pairs, never the tier.

**Bottleneck.** The board's top risk: candidate work must track real encounters (q-candidate-degree,
co-orbital gold 20261006-0346). This run measures where the gold's certificate breaks before the
queued build (`b-coorbital-cert`) freezes it into the encounters design.

**Evidence** (all from `crates/encounters`' own independent truth: `truth_pair`, Halley states;
scenes coplanar Kepler, µ=1, a≈1, ρ=1e-4; JSON lines in `work/coorb-final.jsonl`):

| scene (n, horizon) | truth enc | cone missed/cands/evals | rank-global missed | gate missed/hits |
|---|---|---|---|---|
| S1 r8-coorbital swarm (300, 50 orb) | 193 | 0 / 44 850 / 22.8 M | 12 | 0 / — |
| S1b true fleet, one orbit (300, 50) | 103 | 0 / 44 850 / 15.5 M | 8 | 0 / — |
| S2 fleet×belt (550, 15) | 90 | 0 / 90 623 / 13.7 M | **78** | 0 / 81 758 |
| S3 fleet×fleet crossing (300, 20) | 70 | 0 / 44 850 / 26.8 M | **46** | 0 / 10 476 |
| S4 wedge storm (240, 20) | 242 | 0 / 28 680 / 17.1 M | **94** | **21** / 6 921 |
| S6 held-out fleet×fleet | 67 | 0 / 44 850 / 27.0 M | **34** | 0 / 10 174 |
| S7 held-out wedge | 252 | 0 / 28 680 / 17.2 M | **85** | **41** / 6 829 |
| S8 held-out fleet×belt | 93 | 0 / 88 707 / 13.7 M | **81** | 0 / 108 986 |

1. **The blind spot (P2 held, all seeds incl. held-out).** Ranking every body by λ(t₀), k=4 —
   the reading "the trigger replaces the tier" — misses 66–94% of encounters on any scene where
   encounters cross populations. The trigger's dimensionless number measures *internal*
   concentration; the risk arrives from outside it (Taleb: one observation dominates).
2. **The tail inside the fleet (P1 as first written failed; repaired).** Static rank-4 on a pure
   fleet with a-spread ±5×10⁻⁵ misses 8/103 (7.8%) over 50 orbits: pairs converge from beyond
   rank-k at the family's synodic rate Δn·T. The dump (`work/coorb-miss-final.txt`) shows every
   miss is a converging pair 3+ spacings out. Re-ranking every orbit (drift/chunk ≪ one spacing)
   gives 0 missed on S1, S1b at ~10 M evals — 70× fewer than the cone's 22.8 M on the same scene.
   The gold's claim is true only with an explicit refresh cadence: T_refresh ≲ spacing/Δn_max.
3. **Family gates (P4 partially failed — the honest hole).** Greedy Binet families + rank intra +
   time gates at representative crossing longitudes: 0 missed on S1/S1b/S2/S3/S6/S8, and
   hits/encounter is a seed- and N-independent constant (S3 150, S6 152; S5 scale 37/75/150 per
   side: hits 577/2 443/10 476 track candidates' ×4 per doubling while cone candidates 2 701/
   11 175/44 850 ignore ρ entirely). But wedge storms miss 21/242 and 41/252 held-out: with
   family internal spread ε≈1.5×10⁻³ ≫ ρ, member pairs encounter at longitudes the
   representatives' crossings misplace. Fix is named, not built: member-extremal crossing arcs
   per family pair (the same widening the per-pair sections already do), or families clamped to
   ε≈ρ — in the engine, fleets are programs (shipmem), tight by construction.
4. **Cost honesty.** On fleet×belt the gate's exact checks (adaptive resolution for near-tangent
   crossings) cost 51–64 M evals vs cone's 13.7 M: not yet cheaper there; it is structurally
   better only where concentration makes the cone degenerate (S3: 10 476 gate pairs vs 44 850
   candidates, and gate pairs scale with ρ·encounter density, cone candidates with orbit overlap
   alone). The 10⁶-fleet extrapolation: cone = n_f·n_o setups regardless of ρ (the 40 TB number
   reborn one level up); gate = pairs that actually pass within S·(ρ+ε) — work tracks real
   encounters (slack measured ≈ S·(ρ+ε)/ρ ≈ 84 here, set by family tightness, not by N).

Reproduce (each scene×method line ≤ 22 s; whole binary ≈ 110 s):
```
cargo build --release --offline -p emergent-encounters --bin coorb
$CARGO_TARGET_DIR/release/coorb          # JSON lines; stderr = missed-pair dumps
```
Scenes and methods: `crates/encounters/src/coorb.rs` (added this run; everything else in the
crate untouched). Data: `work/coorb-final.jsonl`, `work/coorb-miss-final.txt`; earlier
configurations (static rank, global-ε windows) in `work/coorb-out*.jsonl` — kept so the tuning
path is auditable.

**Predictions.** `predictions.md` was written before any run. P2, P3, P5 held (P5's ≤10² is
1.5×10² measured); P1 failed as written (static rank missed 12/193 — the gold does not reproduce
without a cadence) and was repaired, not discarded; P4 failed on wedges (S4 21, S7-hold 41) —
the failure mode was exactly P6's named risk (member spread vs ρ). Kill criterion for the rung:
any method that misses while claiming to certify is dead at any N — the global-rank trigger and
the spread-family gate are dead as tier replacements; the cadenced intra-family rank is alive.

**What would make it wrong.** Coplanar, µ=1, ρ=1e-4 of a=1 (≈10⁵× a game's ship/AU ratio):
slack factors shrink linearly with ρ, favouring the gate, and inclined or precessing fleets add
crossing longitudes my two-ellipse geometry undercounts. Truth and method share `Body::state`
(Newton) — mitigated as in r8 by Halley-state truth and a disjoint refine path, but the truth's
own oracle-domain is Kepler-with-fixed-elements over ≤ 50 orbits. My matchup counts cone's
double-dipped Full-section minima as "false" (56 on S1b, 0 missed) — a dedup artifact of this
run's matchup copy, not a cone defect.

**Cost of adoption.** Nothing lands in the engine from here; the adoptable statements are
restrictions on the `b-coorbital-cert` build: (a) the trigger may only replace *intra-family*
pairs; (b) rank certificates carry a refresh cadence T_refresh ≲ spacing/Δn_max; (c) families
must be tight at ~ρ or their crossing arcs member-extremal. Fit: "candidate work must track real
encounters"; PRINCIPLES 25 (don't multiply by zero: a certificate that silently drops encounters
is ruin), 22 (the simulation — here the truth — tells us what's next), 13 (a miss is an error
type that compounds: it deletes every downstream contact).

**The lens.** Taleb's fragility hunt found the black swans (crossing populations, the wedge
storm, the converging tail) but prizes vetoing: the gate's honest partial failure is why this is
silver, and the lens says nothing about making the cheap path cheaper — the evals win on
fleet×belt is left to the next run.

**Grade: SILVER** — real, reproduced on fresh seeds where it holds, with the failing cases held
out and confirmed failing; one named experiment from gold (member-extremal arcs / ρ-tight
families, then the 10⁶-fleet pair-count measurement at game ρ).
