Grade: silver

**Abstract.** The checker's named experiment, run on the shipped plane's real kick path (4.1 h fine + 20 d coarse, deterministic; digests and every table row reproduced bit-for-bit; adversarial span and seed-2 runs hold the decision). The 20261011-1332 identity holds in structure, but "jet 1.6× short" is refuted favorably: `crossing_state` 0.34–0.42 µs and re-anchor ρ = 0.001–0.002/rebind (0.007 seed 2; escaped debris 0.22) close rtf 100 at 10⁹ with ~2× margin (rtf 170–233), robust to law.md's design ρ = 0.05 (rtf ≥ 133). New binding constraints: raw LEO active ceiling ≈ 9×10⁶ bodies at rtf 100; the escaped-debris tail (rtf ≈ 13). Cost to adopt: none (measurement); it replaces the jet budget's assumed ε, ρ and cadence with measured ones.

## Reproduction

Clean tree, `git apply work/patch.diff` (two new example files, nothing else touched — verified by `git status`), then the dossier's commands.

| item | record | this check |
|---|---|---|
| fermi_budget regen (sinks, knots, collapse, cycle bytes) | 99,361 / 99,799 / 2,704; 752/1744/3376 B | **bit-for-bit identical**; timings ±3% (8,364 vs 8,542 ns) |
| jet_anchor digests (fine / coarse) | 0ecd100e… / 25c4de00… | **identical** |
| stream caches | 7118/3627/54 (67.17×); 3752/1909/271 (7.04×) | **identical** |
| class tables, ρ, rates, rebinds/orbit, sinks, encounters 96,486 | — | **identical**; timings ±10% (readout 3,359 vs 3,525 ns; jet rtf 230 vs 221) |

Timeline: `predictions.md` 15:12:48 < bench1 15:31:15 < bench2 15:34:37 < dossier 15:38:45; no earlier `jet_anchor` bench exists in the folder. The prediction failures themselves (P1 2–5× off, P5 25–50× off) are the strongest evidence against tuning. Journal inputs verified in source: law.md's jet (0.05 compiles/kick, the √(floor/C) drift-floor criterion, the red-team 730-kick bound); H0190 K1/K2 (32.5/orbit, 114×); H0210 (29 µs kicks); `Config::default()` has `step_log2: 7` → 128 planned kicks/orbit, so the P1 diagnosis is source-verified; `crossing_state` is genuinely a direct table read (orbit.rs:678).

## Adversarial cases (four, all run)

1. **Different spans** (1.5e9 fine / 1e11 coarse): rates stable (hauler 3.38×10⁻⁵ vs 3.51×10⁻⁵ /s; ship/Home identical 1.286×10⁻²; ρ stable 0.001–0.002), jet rtf 168–233 — the decision holds. Bonus finding: the escaped-leaver ρ is window-dependent (0.638 vs 0.221) and its compile hit 71 µs at 106 knots, confirming the dossier's caveat (c) and the first checker's high-e tail.
2. **Seed 2** (one flag-flip): LEO rates identical (cadence is config-driven), hauler ρ = 0.007 (7× seed 1; still 7× below the design 0.05), escaped-leaver ρ = 0.211 (stable vs 0.221), jet rtf 191–229. The conclusion holds on a second seed; but "0.001–0.002 for every stable class" is seed-1-specific.
3. **Escaped-tail arithmetic**: at the escaped ρ = 0.221 and 52 µs compile, jet/kick = 6.2 µs → rtf ≈ 12.9 at 10⁹ all-active. The debris tail genuinely does not close at 10⁹; the identity table's leaver row (jet rtf 170) carries the battle-epoch ρ (0.002), and the escaped constraint lives only in prose.
4. **Identity audit**: every table row recomputes from the printed inputs (jet/kick = crossing + 0.5·ρ·compile; N_max = 8/(100·rate·cost); headline rtf = 8/(10⁵·cost); realized all-in rtf 2.1 = 8/(10⁵·37.7 µs); 752 B → 1.06×10⁷ cycles per 8 GB). One wobble: the "even at ρ = 0.05 … rtf 133" hand-calc gives ~150 at its stated inputs (crossing 0.36, compile 3.5 µs); 133 matches the planet class's 4.9 µs compile. Both > 100 — direction unchanged, band understated favorably.

## Novelty

HISTORY.md ends at H0215 (6 October); neither 11-October run is journaled. No prior measurement exists of the realized re-anchor rate on the plane's stream, the per-class rebind cadence, `crossing_state` on plane entries, or the cold-store integer floor (31–33 ns independent / 124–134 ns dependent vs the 5 ns L2 control — the first checker's un-run critique, now measured: the "rtf 27,000" floor tier is 11–45× optimistic, not ~300×). H0215 names "second authors on silvers" as the mechanism; this run executes the first checker's named experiment exactly.

## Goal fit

Board #3 (cost at a billion) and #5 (memory), the focus item "fitting 10⁹ in 8 GB". It replaces the jet budget's two assumed inputs and the worst-case active rate with measured ones and flags law.md's 0.05 compiles/kick as ~30× conservative against both the measurement and the red-team's own 730-kick bound — actionable before the jet is built. PRINCIPLES: #10 "Measure before claiming"; #3 "Compute only surprises" (the identity is the surprise rate made arithmetic, now on realized rates); #27 "i just care at about how fast it runs compared to real time"; #24 "The memory floor is information" (752 B/body active-set floor). H0183 is honored in spirit: the failed predictions are diagnosed, not hidden.

## Why silver, not gold

The work is reproduced, decision-grade and robust — but the gold letter requires the held-out predictions to held, and three of eight failed: **P1** (rebinds/orbit 141–250 measured vs [25, 130]), **P5** (ρ 0.000–0.002 vs 0.02–0.15), **P2** (belt rate 3.5×10⁻⁵ vs ≤1.5×10⁻⁵), with P6 and P7 split (collapse 7–67× vs ≤2×; independent wave 31 ns below the bracket). Lab precedent bars gold on failed held-out predictions (1 October red-team; the original 20261011-1332 itself, barred on one). The mitigation is real — the failures are of the design constants the run set out to measure, disclosed with diagnosis, and the decision-level prediction P8 held (jet closes within ~2×; measured margin 1.7–2.3×) — but P5's band even contradicted the journal the author cites: the red-team's 730-kick bound implies ρ ≥ 0.0014/kick, below P5's 0.02 floor, so the failure was avoidable from the record. That is exactly what a held-out sheet is meant to catch.

## The one experiment that would make it gold

Measure the re-anchor rate by law.md's own criterion — the accumulated offset reaching √(floor/C), the drift floor — on the same recorded rebind stream (the jet's offset arithmetic, or a faithful simulation of it), at ≥ 2 seeds, plus the belt-scale cross-body collapse (B18). The "jet closes" headline leans on cell-stickiness ≈ offset-stability, and the gap is visible in the run's own numbers: the measured per-kick cell rate (0.0005–0.001) sits marginally *below* the 730-kick floor (0.0014/kick) the dossier calls "consistent". If the drift-floor rate lands in [0.001, 0.05] per kick, the conclusion is closed; above 0.05 it flips.

## What the author missed

1. **Seed variance was one flag-flip away** and un-run: hauler ρ 0.001 → 0.007 on seed 2. The conclusion survives (jet rtf 191), but "every stable class" and the ρ headline are single-seed numbers where the falsification criterion ("a measured ρ ≥ 0.3") deserved at least a second draw.
2. **The identity's leaver row is optimistic by construction**: it uses the fine-phase (battle-epoch) ρ = 0.002 while the escaped population's own ρ = 0.221 affords rtf ≈ 13 at 10⁹ and N_max ≈ 9.6×10⁷ — the dossier's "~10⁷" ceiling is conservative, but the table row reads favorable where the prose constraint is the real one.
3. **The "rtf 133" hand-calc** does not match its stated inputs (~150 at ρ = 0.05, 3.5 µs compile; 133 matches the planet's 4.9 µs). Direction unchanged; still, a headline band should recompute from its own inputs.
4. **Per-rebind vs per-kick ρ is compared loosely**: 0.001–0.002 per rebind is 25–50× below law.md's 0.05 *per kick* only via the 0.5 rebinds/event factor; stated per kick (0.0005–0.001) it is 50–100× below and marginally under the 730-kick bound — the more honest comparison, and the one the gold experiment must settle.
