Grade: gold

**Abstract.** Claim: on B12's own circular-restricted-three-body Jacobi scene, the decade-local α-profile (top-decade slope of the running max of |ΔC/C₀|, frozen 0.2 threshold, median seed) separates bounded from compounding error; B12 v1's single-window slope does not. Reproduced bit-identically in a clean tree: all six artifacts (seeds.json, four series npz, b12_alpha.json) hash-match; ~16 min parallel, <200 MB per process. Numbers confirmed from the record: bounded plants α_top 0.00–0.01 (32/32 seeds), compounding 0.94–1.22 (32/32), v1 false-kills 21/32 bounded while convicting 32/32. My own cases: delayed-onset leak (orbit 5000) convicts 16/16; deeper-tide scene unpopulatable (0/60 survive); late transient (orbit 3000) still false-kills — the disclosed horizon rule. Adopt into `b12-v2` with these plants as controls: one step.

## Reproduction

- `work/patch.diff` is empty; the author edited nothing outside the run folder (`git status`: only untracked `lab/results/`). Ran `select --candidates 60`, the three `law` runs in parallel, then `analyse` from `b12_scene.py` in `/tmp/b12check`. Every artifact is byte-identical to the stored record (sha256 on seeds.json, all four `series_*.npz`, `b12_alpha.json` all match). The shipped code regenerates the record exactly.
- Every headline number re-derived from the stored JSON: medians match the dossier table verbatim (sym-fixed seed 13, 2.55e-5, α_top +0.00; sym-sched seed 0, w1e4 +0.76 → v1 false kill, α_top +0.00; sym-var seed 11, 1.06e-3, α_top +0.98; rk4 seed 8, 3.22e-4, α_top +1.05); bounded α_top ∈ [+0.000, +0.007] over 32/32; compounding ∈ [+0.942, +1.218] over 32/32; v1 false-kills 21/32 bounded (w_full > 0.2; also 21/32 by w_1e3) with 32/32 convictions; bounded finals ≤ 3.42e-5, compounding ≥ 1.38e-4; crossings 17,146–69,767; 21/60 survive selection, 16 kept.
- Scene fidelity against the repo, not the author's word: `docs/law.md` B12 (16 seeds, CRTBP Jupiter-like, ≥20 doll-edge crossings, Jacobi within 10⁻⁴, exponent ≤ 0.2 median seed above a 10⁻¹² floor) — all present in code; μ = 2⁻¹⁰ is `crates/universe/examples/jacobi.rs`'s own value; edge = sep·2^(2·Δlog₂m/5) = sep/16 = 0.908 Hill is `crates/space/src/events/records.rs::edge_radius`. The 10⁻¹² floor and the median-by-final rule are implemented in `analyse`.

## Predictions

`predictions.md` mtime 02:41:19 precedes every decisive artifact (series 02:49–02:59); the kill criteria and the operating rule were pre-registered. All four held: P1 (median α_top 0.00 < 0.15, decades d ≥ 1 ≤ +0.07, final 2.55e-5 in range), P2 (α_top 0.98, final 41× bounded, predicted ≥ 10×), P3 (1.05), P4 (v1 reads +1.01 on [1,10³] and +0.76 on [1,10⁴] — false kill — while the profile acquits at 0.00). The 10³-orbit shakedown that informed the priors is disclosed. No kill criterion triggered.

## Adversarial cases (mine)

1. **Delayed-onset leak** (sym-fixed until orbit 5000, then state-dependent dt — the dossier's operating rule asserts this convicts; it is not in the record): 16/16 convicted, α_top ∈ [+1.23, +1.39]. Holds.
2. **Deeper tide** (retrograde q ∈ [0.40, 0.55] Hill, the "deep chaotic exploration" break scenario): 0/60 seeds survive 10⁴ orbits. The author's population sits at the survivability edge of this μ and horizon; the named break scenario cannot even be populated here, so the reported margins are not obviously optimistic.
3. **Late transient** (dt/4 until orbit 3000, then dt — bounded law, schedule change inside the top decade): falsely convicted 16/16, α_top ∈ [+0.95, +1.23], finals 1.4e-5–2.8e-5. This is the disclosed "a transient must die one decade before the horizon to acquit" rule, now measured; it is not a refutation of the claim as scoped (the tested transient at orbit 300 is acquitted), but it is the rule's live failure mode and must reach `q-b12-design`.

## Novelty

No α-profile or decade-local exponent appears in `docs/HISTORY.md`, the board or the docs; the parent silver (20261008-2206) proposed it only on an integrable two-body series plus synthetics, and this run is that checker's named experiment. The B12 statistic rebuild is the live workstream (HANDOFF "B12 rebuilt and frozen": `q-b12-design`, Codex `b12-v2`; H0215 "B12 unusable until rebuilt"; the instrument is an open item — "judged by probes, not a gate"). This is the calibration on planted pairs that method.md #9 requires before a statistic freezes, done on the gate's own scene with controls on both sides.

## Goal fit

Directly serves PRINCIPLES 13 ("Errors never compound… types of errors and not just errors") and 2 ("error type over error size"): the α-profile is error type made measurable, with the level criterion kept as complement, and it repairs a gate that measurably false-kills 21/32 correct laws — a wrong-premise measurement with a one-step adoption path into the gate text `b12-v2` is already writing. Prediction discipline, exact-regenerating record, disclosed non-60-s runtimes and memory: the record meets the lab's bar.

## What the author missed

- The invariant masks error type too: |ΔC/C₀| cannot see a law whose Jacobi error stays bounded while trajectory phase walks. All bounded plants here are symplectic; no bounded-but-phase-drifting plant was tried. Inherent to B12's Jacobi choice, but the α-profile inherits it and the dossier does not say so.
- The doll handoff is a coordinate re-expression exact in real arithmetic, so it injects rounding noise only; "doll-edge handoffs" in the claim exercises the crossing topology, not handoff representation error (disclosed in the blind spot, worth top billing: the plane's tube rebinding is where this statistic is still unmeasured).
- The dead sym-var seed is counted among the 32 "usable" compounding seeds via a partial profile (its α_top 1.22 is the range's max, from a truncated series); honest, but the count's meaning shifts.
- My case 3 shows the frozen rule false-kills bounded laws whose schedule changes inside the last decade — disclosed as the horizon rule, but a plane law that re-schedules on kicks (its measured behaviour) will hit it; `q-b12-design` needs the transient/leak control, as the dossier itself says for α ≲ 0.1 leaks.
