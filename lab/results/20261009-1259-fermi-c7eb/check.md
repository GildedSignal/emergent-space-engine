Grade: silver

**Abstract.** Claim: at 10⁹ bodies the binding term on 8 GB is the flat 16-B tube store (14.9 GiB, 1.9× over), and belt encounters create zero canonical distinctions below m_crit≈8×10⁻¹⁹ M☉ (≈500-m rock), so H_live is set by consumers, not belt self-evolution. Everything reproduces bit-for-bit (verify a/b/d truth counts, 17–32 s; analysis.py; rate.json); the target (HANDOFF: H_live "not measured yet") is real and unclaimed in HISTORY. My adversarial integration of real encounters shows the (2/3)θ Δa coefficient is ~13× high (measured scaling 1/v_rel, not 1/v²): true m_crit ≈1×10⁻¹⁷ M☉ (~1-km rock). The threshold structure and every ledger conclusion survive, conservatively. Adoption cost zero (decision input; argues against deleting shipmem). One experiment from gold: pin m_crit and the sub-threshold crossing flux on the crate's real (d, v_rel) distribution.

## Reproduction

Clean tree (patch.diff is empty; the author changed no repo code). `cargo run --release -p emergent-encounters --bin encounters -- verify a` = 17 s (dossier: 18 s), `verify b`+`verify d` = 32 s (34 s). All 10 belts' truth_enc counts identical to verify-a/b/d.jsonl (fixed seeds, deterministic). `analysis.py` rerun in /tmp: analysis-out.txt and rate.json byte-identical. Arithmetic spot-checked independently: tick quantum 1.503e-11 AU at a=2.7 ✓; 14.9 GiB / 1.9× / 545× / 20 ev/s / 2% / 0.27 s sweep ✓; m_crit algebra ✓. Machine: shared 8-vCPU Linux, light load, all runs ≪2 GB.

## Predictions

predictions.md predates every output file (mtime 7 min before the verify/analysis artifacts) and pre-registers ranges plus kill criteria. P1 half-held (spread wider than predicted), P2 **split** — the central prediction ("<1% of encounters cross a tick even for Ceres") failed opposite: Ceres crosses 1.2×10⁹ ticks — reported honestly and diagnosed into the threshold claim. P3 held for storage; the events margin was 200× optimistic (self-reported). P4 unmeasured (admitted).

## Attack (3+ adversarial cases)

1. **The Δa coefficient is wrong by ~13×.** I integrated real encounters (Sun + two belt bodies, RK4, osculating a before/after; /tmp/adv-integrate.py). Doubling v_rel halves Δa (ratio 0.50) — the impulse form 4√a·m·cosψ/(q·v_rel), not the author's (2/3)·2atan(μ/qv²) ∝ 1/v² (which predicts 0.25). Mass scaling linear ✓. At σ_e=0.1, q=1e-4: measured Δa ≈ 0.5×impulse(cos=1); author's value 13× high. Corrected m_crit ≈ 1.0×10⁻¹⁷ M☉ ≈ 1-km rock. Direction conservative (attractor stronger than claimed); the author's own bracket (50 m / 500 m / 5 km / Ceres) contains every corrected value, so no conclusion flips: ships and 50-m rocks ~10⁻³ ticks, 5-km ~65 ticks, Ceres ~10⁸ ticks.
2. **"Exactly zero" is per-encounter, not forever.** Sub-tick kicks random-walk. First-passage: 500-m rock ~90 orbits, 50-m rock ~9×10⁷ orbits; steady crossing flux 8.8×10⁻⁵/body/orbit (50 m) → ~6×10⁻⁴ crossings/s at 10⁹ — negligible against consumers, so the quantitative H_live conclusion survives, but the "exact, 0 crossed ticks" framing is horizon-scoped and the hard floor is really a smooth rate in mass.
3. **Thin belts.** The author's own output: σ_i=0.005 → 77.6 encounters/body/orbit (28× thick) → 55% of one core at RTF 100, not "~2%". Still under one core, but the event margin is belt-geometry-dependent by ~30× and the ledger uses only the thick number.
4. **Co-orbital case** (verify c, unrun by the author): with the corrected 1/v scaling, m_crit ∝ q·v_rel; at fleet geometry (q~10⁻⁸ AU, v_rel~6×10⁻⁶) m_crit ≈10⁻²⁵ M☉, far below a 1-Mt ship — their "fleets individualize" caveat survives, driven by q as much as v.

## Novelty and goal fit

docs/HISTORY.md has no prior H_live measurement; HANDOFF's risk list says "not measured yet" and this run measures the belt-encounter channel of it. The 0.126-bit program (components-98bc), the 16-B tube (law.md) and shipmem's spec are cited, not re-claimed. Directly on the board's "fitting 10⁹ in 8 GB … decided by distinctions created per game-second", and it argues against method.md's deletion of `crates/shipmem` before B18b wires the belt. PRINCIPLES fit: "the floor is what the player can differentiate"; "Compute only surprises" — nothing is stored that no consumer can distinguish.

## Why silver, not gold

Gold requires the held-out predictions to hold; P2, the core physics prediction, failed and was reinterpreted post hoc into the threshold headline, and the headline number (m_crit ≈ 500-m rock) is ~13× low. Not lead: fully reproduced, on an unmeasured registered risk, kills a premise (belt self-evolution does not force tubes below ~1-km rock — stronger than claimed), zero adoption cost, honest self-grading throughout.

## The one experiment for gold

Dump per-encounter (d, v_rel) from the truth encounters (the crate's `Enc` already carries d), apply the impulse coefficient validated above, and report m_crit plus the sub-threshold random-walk crossing flux on the measured distribution — over the verify belts and one game-density 3-D case. If the threshold and negligible-H_live conclusions hold there (my arithmetic says they will, with margin), it is gold.

## What the author missed

- The (2/3)θ coefficient is asserted, never derived; a 30-line integration would have caught the 13× and the wrong v-scaling. The lens note prices this at "2× tighter"; it is 13×, still non-fatal.
- The cumulative random walk of sub-tick deflections (first passage ∝ (m_crit/m)²); "zero bits" is exact only per encounter.
- The thin-belt 28× event-rate spread is in their own output but absent from the ledger and the abstract.
- H0190's 0.3 distinct kicks/orbit is transplanted from the plane's secondary-adjacent context to main-belt bodies without argument; secular-kick distinctions (differential precession, Kirkwood structure — partly flagged) are the other self-evolution channel and stay unmeasured.
- analysis.py hardcodes the truth counts instead of parsing verify-*.jsonl (they regenerate identically, so no integrity issue).
