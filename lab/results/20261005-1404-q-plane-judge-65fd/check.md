Grade: silver

**Abstract.** The shipped plane, driven through a faithful public-API adapter, fails the frozen gates B12, B13 and B17 at every cadence the CLI can name: B13 51/64 assists with 7/64 flybys lost; B12's Jacobi error compounding (median exponent 1.026 against the 0.2 limit); B17's e-pump up to 17× with 0/3–0/5 controls. B14 is machine-VOID: echo itself times out at 60.1 s. I reproduced every row I ran bit for bit (nine rows, three unit tests, the 128-tick floor) and located the losses: the lost ships die at 1.5–3.2 planet radii where the reference passes at 1.3–11 — encounter failures, not the adapter (at the B17 scene the error grows from 3e-4·sep). The gain is a verdict: cadence is not the missing step; the encounter representation is. Cost to adopt: the ~120-line adapter, merge-ready.

## Reproduction (clean tree, `git apply work/patch.diff`, `cargo build --release -p xtask`)

Every number I ran matches the author's row exactly:

| run | author | mine |
|---|---|---|
| echo B12 | PASS, worst 3.8e-15 | PASS, worst 3.75e-15 |
| echo B13 | PASS 64/64 | PASS 64/64 |
| echo B14 | rc=1 60.1 s | rc=1 60.15 s (the judge's own limit, not my timeout) |
| planted-kick B12 | FAIL exp 0.766, worst 3.9e-4 | FAIL 0.766, 3.90e-4 |
| planted-kick B13 | FAIL 53/64 | FAIL 53/64 |
| planted-average B17 | FAIL pump [0.107, 0.963], amp 0.015 | FAIL [0.1066, 0.9632], 0.015 |
| plane B12 s7 | FAIL 15/15 above floor, median 1.026, worst inf | FAIL 15/15, 1.026, inf |
| plane B13 s7 | FAIL 51/64, worst inf | FAIL 51/64, worst inf |
| plane B17 s3 | FAIL pump [0.79, 8.8], controls 0/5, 2 unanswered | FAIL [0.7887, 8.7999], 0/5, 2 |

- `cargo test --release -p xtask plane::` — 3 passed, 1 ignored (the moon probe, not re-run: 118 s).
- `MIN_STEP = 2*64` confirmed (`crates/universe/src/step.rs:37`) — the tick-floor claim behind "B17's four rows are not four cadences". The author's B17 s7 vs s5 outputs differ only in the captured-ship counts, as claimed.
- The author's two re-run rows (`rows/plane-*-repro.*`) match their table originals.
- **Predictions record:** `predictions.md` mtime 14:26:03; `table.sh` written 14:26:21, first row 14:26:21, table complete 14:37:26 — pre-registered before the decisive run.

## Attacks (mine)

1. **The adapter at B17's miniature** — the one scene no unit test covers (μ = 3e-4/3e-3, sep = 100). I flew the gate's own control and resonant births through the adapter against the judge's reference (40 synodic periods). Result: the semi-major axis at t = 0 comes back to 2–4×10⁻³ (the plane's position quantum at this scale, not a conversion bug), the first-sample error is 3e-4·sep, and it *grows* — 4.6e-2·sep after one ship period, O(1)·sep after tens of synodic periods; the controls pump e 1.75×/1.59×. The adapter is faithful at the miniature; the engine diverges, at the finest cadence it can express there (24.6 kicks/orbit, pinned by MIN_STEP).
2. **The death cause of the lost ships** (the dossier asks the checker for this). I replayed all 64 B13 flybys through the public API, settling in 64 steps with a 32-fold refine. All 7 lost seeds die with last-alive planet distance 1.56–3.18 planet radii; the reference's minima for the same seeds are 1.32–11.08 radii. Seed 12: the plane dives to 1.56 radii where the reference never passes inside 11. `Resolved::Lost` here is a surface crossing or a planned sub-surface periapsis (`step.rs:464`/`step.rs:515`); the system edge (`leave_log2` = 2⁴⁰) is unreachable and `refused = 0`. Genuine encounter-trajectory failures, not the adapter and not the system edge.
3. **Controls both sides:** echo passes, every planted flaw fails the gate it is planted against, through the same `restricted` path the plane answers — the verdicts mean something ("a test that cannot fail is a control").

## Novelty

This is H0213's queued task, first executed: "the plane judged by B12–B17 (GLM, reviewed)". No earlier lab run measures the shipped engine through the gates — r10 (H0212) judged a float *replica* of the changeover (exponent 0.43); this run finds the shipped integer changeover at 1.0–1.5. The distinction replica-vs-engine is the point.

## Goal fit

Board focus items 1–2 (fewer kicks; the changeover near a secondary) and bottleneck 2's live path. Principle 13 ("errors never compound") is what B12 measures: median exponent ~1, linear drift. The finding kills the premise that the plane at 8–128 kicks/orbit is within one step of passing, and redirects the next token to the encounter's representation — exactly the board's "changeover near a secondary, reversible and integer".

## Why silver, not gold

- **Held-out predictions did not hold.** The adapter predictions held (exact round-trip, 5e-4·sep falling like H²). The verdict predictions failed in the direction that matters: B12/B13 predicted PASS at steps 7/5 (FAIL at all), B17 held at ~60% PASS (total failure, controls included). Honestly reported, and in the safe direction for a negative claim — but by the lab's precedent (1 Oct red-team) a failed held-out prediction blocks gold.
- **The table is incomplete.** B14 is machine-VOID on this box, and the integrator's own bar for this run was "the table is complete; whatever the verdicts are". Four plane rows and the apsides leg are missing; the moon probe covers circular births only, so the apsides stay unmeasured (the author says so).

## The one experiment that would make it gold

Run B14's four plane rows (echo included) where the judge's own 768-reference phase fits the 60 s limit — the M1 or a quiet box — with the eccentric births so the apsides leg is judged. Predictions are already on record (classes agree at every cadence; apsides pass at 5, marginal at 4, fail at 3). A complete table with the adapter faithful meets the integrator's stated gold bar, whatever the verdicts.

## What the author missed

- The B17 miniature is beyond the plane's representation floor, and the data says so more plainly than the two derived suspects: at sep = 100 the finest expressible cadence is 24.6 kicks/orbit (MIN_STEP) *and* the t = 0 binding itself is only exact to ~0.3% (position quantum). The B17 row therefore measures the plane at a scale it cannot resolve — the mantissa/aliasing suspects stay untested, and my probe shows plain under-resolution is already sufficient to explain O(1)·sep divergence there. The dossier's phrasing "not a cadence question" is true only of the 24.6-vs-12.3 pair, not of the five octaves the floor hides.
- The dossier asks the checker to re-derive the lost ships' death cause but leaves no trace of it in the record; done here, and it confirms the claim (deaths at 1.5–3.2 radii, trajectories — not surface placement — at fault, since reference minima reach 11 radii).
- Minor: the table prints B14's rows as "FAIL timeout"; the text correctly re-labels them machine-VOID, but a machine-readable table should carry the VOID verdict itself.
