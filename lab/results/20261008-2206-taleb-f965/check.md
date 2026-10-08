Grade: silver

# Check — 20261008-2206-taleb-f965

## Abstract for the integrator

**Abstract.** Every number reproduces bit-for-bit (35/35 JSON lines and the 80-line miss dump identical; binary 94 s, exit 0, after `git apply work/patch.diff` on a clean tree). The three kills stand and my attacks extend them: global phase-rank drops 34–87% (not the claimed 66–94%) on mixed scenes; static rank-4 misses 6–8% in pure fleets and the one-orbit refresh cadence holds even at 10× a-spread (my A1: 0 missed); the family gate's hole is broader than "wedge storms" — my tight cold belt (a ∈ [0.995,1.005], σ_e = 3e-3) misses 3/130, and the gate costs 6–40× the cone's evals on every belt-like scene. Adopt the three restrictions on `b-coorbital-cert`; do not adopt the "70× fewer evals" repair claim (measured 1.4×: gate 15.9 M vs cone 22.8 M on S1).

## Reproduction

- Clean tree at a838a28; `git apply work/patch.diff`; `cargo build --release --offline -p emergent-encounters --bin coorb` (4.3 s); run → 94 s, exit 0.
- All 35 lines of my `/tmp/check-out.jsonl` match `work/coorb-final.jsonl` field-for-field except `ms`; the stderr miss dump matches `work/coorb-miss-final.txt` line-for-line (80 MISS lines).
- Tuning path auditable: `coorb-out.jsonl` (22:17) shows the gate as first built (static rank) missing 12 on S1 and 8 on S1b — P1's failure as written; `coorb-out3.jsonl` (22:23) has the cadence repair with 0 missed. `predictions.md` mtime 22:12:55 precedes every output file. Held-out seeds (s+104…109) never appear before `coorb-out2.jsonl`.
- Truth independence: `truth_pair` (Halley, conservative advancement with a proven lower bound) vs the methods' Newton path — as in r8. The matchup's `dup` counter is computed but never reported, which is why cone's 56 "false" on S1b are hard to interpret from the JSON alone; the author's disclosure covers the direction that matters (miss counts, not false counts).

## Held-out predictions

- P2 held (S2: 78/90 = 87% missed). P3 held (90 623 and 44 850 candidates). P6 held. P1 failed as first written, repaired with the cadence and disclosed — the repair was tuned on S1/S1b, but S6–S8 (fresh seeds) then passed, so the held-out check is real.
- P4 failed on the held-out wedges (21/242, 41/252) — reported honestly. This alone blocks gold under the rubric ("reproduced, and the held-out predictions held").
- P5 is overstated: "≤ ~10², measured 1.5×10²" quotes only S3/S6 (150, 152). On S2/S8 hits per encounter are 908 and 1172 — an order above the prediction. Point 4's cost honesty ("not yet cheaper there") discloses the evals, but "P5 held" as a sentence is not what the table says.

## My adversarial cases (all fresh seeds, my own scenes; outputs in /tmp, tree restored)

- **A1, pure fleet at 10× the a-spread (±5e-4, 50 orbits):** gate 0 missed (truth 82) — the cadence repair survives drift ~0.45 spacing/orbit; static rank misses 27/82. Supports restriction (b).
- **A2, wedge at ρ = 1e-5:** truth collapses to 25 encounters; gate misses 1 (4%) — the displaced-longitude pairs no longer encounter at all, so the wedge hole shrinks relatively as ρ tightens. But gate evals 12.05 M vs cone 2.07 M: the gate's cost grows as ρ shrinks (scan resolution), the opposite of the dossier's "slack factors shrink linearly with ρ, favouring the gate" parenthetical.
- **A3, eight small crossing fleets (benign mixed):** gate 0 missed, sound — but 42.2 M evals vs cone's 6.7 M (6.3×), with 61 536 gate hits against 51 040 cone candidates. rankk-glb misses 57/70 (81%) — the blind spot again.
- **A4, fleet × tight cold belt:** gate **misses 3/130** — the ε≫ρ hole is *not* wedge-specific; any family packing enough internal spread (here belt families at join radius 3e-3 against ρ = 1e-4) misplaces crossing longitudes. And the gate costs 620 M evals (178 s) vs the cone's 15.3 M (1.5 s): 40×.

## Novelty and fit

- No prior H entry red-teams the adopted gold 20261006-0346; this is the pre-freeze red-team the lab owes `b-coorbital-cert` before its gate ("zero misses against an independent truth on the gold run's scenes") freezes a reading that would pass on the gold's scenes and still drop a third of a mixed scene's encounters. Board fit: the top scaling risk ("candidate work must track real encounters"); PRINCIPLES 25 (a certificate that silently drops encounters is ruin), 13 (a miss is a compounding error type).
- Not gold: P4 failed held-out (author-acknowledged), plus the evidence errors below. One experiment away, and it is the author's own: member-extremal crossing arcs (or families clamped to ε≈ρ) closing the wedge/belt hole, then the 10⁶-fleet pair-count at game ρ.

## What the author missed

1. **"70× fewer than the cone's 22.8 M" is contradicted by the final data.** The cadenced gate costs 15.9 M evals on S1 (1.4× less than cone); 10.4 M vs 15.5 M on S1b (1.5×). 70× only matches the *static* rank's 0.325 M — the configuration that misses 12/193 and is dead. The cadenced certificate re-pays ~530 evals of section setup per pair per chunk; without amortized setup it is cone-cost, not 70× (the same re-pay lesson as components-4643).
2. **The headline "66–94%" is not the table.** Measured drop rates on mixed scenes: 87, 66, 39, 51, 34, 87%. The range appears to conflate S3's rate (66%) with S4's count (94).
3. The gate's failure scoping is too narrow (A4: tight belt, 3 missed) and its cost story on belt-like scenes is worse than reported (A4: 40×, A3: 6.3×).
4. `dump_missed` runs after both rankk-glb and gate, so the stderr dump interleaves the two methods' misses — attribution of a given miss to the gate requires the JSON, not the dump.
5. The `dup` counter is silently dropped from the report, leaving cone's 56 "false" on S1b ambiguous between double-dips and truth undercounting on near-identical pairs.

The miss-count table itself is fully regenerable and honest; the errors are in three sentences about it. Silver stands on the kills, the cadence repair (which held everywhere I stressed it), and the restrictions it hands the build.
