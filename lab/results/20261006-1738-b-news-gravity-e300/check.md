Grade: silver

**Abstract.** News gravity — one cursor per (body, source) over the store's existing version chain, an exact integer cone test — is implemented in the plane's kicks, as law.md specifies. Reproduced on a clean tree, patch applied by me: G1–G6 and B17 byte-identical before/after (B17's every number equal), B13 at its shipped 60/64 both ways, B14 box-timeout both ways, suite green, cone test green. My probes: the cone agrees with a float oracle 20000/20000; News ≡ Instant **bit-for-bit in every scene the API can express** (whole plane, 10751 kicks, the moon's rebinds read through cursors by 9 bodies; restricted, 2064 kicks); Retarded differs everywhere, so the path is live. The two lens-named scene tests were removed and the cited run log is empty: no shipped test can tell News from Instant. One experiment from gold.

## Reproduction (clean tree, `work/patch.diff` applied by `git apply`)

Every dossier number regenerated, both sides, my own runs:

- `behave --law space --gates G1..G6`: PASS before and after, identical lines (G1 worst 6.60e-4, G2 5.50e-4, G3 6.40e-12, G4 0/10, G5 0.000/0.000, G6 256/256).
- `behave --law plane --gates B13,B14`: B13 FAIL 60/64, worst ΔE = ΔL = 2.12e-2, the same 9 replaced draws at the same radii, both ways; B14 FAIL timeout 60.1 s both ways (no detail line exists on this box, so "byte-identical" is vacuous for B14 — disclosed).
- `behave --law plane --plane-step 6 --gates B17`: PASS both ways, identical (e-pump [0.999493, 1.000089], libration 0.998, regime 34/34, controls 5/5).
- `cargo test --release -p emergent-universe`: all green with the patch (lib 11/11 including the cone test; every integration file).
- Author's own before/after logs match my runs exactly; only wall-time brackets differ. P1 held fully.

## Attack (three-plus adversarial cases; temporary probe file, removed after)

1. **Cone vs float oracle**: 20 000 random integer cases, 20000/20000 agree; extremes behave as documented (t < t_k never arrives; components beyond 2⁶³ quanta; dt beyond 2⁴¹ takes the whole-unit quantum; an exact lightlike tie arrives).
2. **Restricted scene** (one planet, no perturber; 2064 kicks over 2.6 planet orbits): News ≡ Instant bit-for-bit on the planet and all ships; Retarded differs. P1's mechanism verified where it was claimed.
3. **Whole plane scene**, horizon 1.2×10¹⁰ ticks (10 751 kicks; the moon rebinds 11 times and 9 bodies — 8 doll-2 ships and the player — hold cursors on it; 4 versions in flight at the cut): **all 28 bodies' final states are bit-identical under News vs Instant**, while Retarded differs. So the news path is exercised and wired, but at the plane's real scales light delays between massive bodies (≲4×10⁸ ticks) are ~10³× their rebind intervals (~1.4×10¹¹), the cursor is caught up, and the rare stale read (the delay window, ~0.1–2 % of an interval) rounds below the integer kick quantum.
4. **Forcing the regime** (step_log2 = 20, rebinds outrunning light): the engine's plan machinery passed 5 GB before one planet orbit — the news regime is unreachable by cadence on this box. This independently confirms the author's E3 diagnosis (cadence floor vs light delay) was real, not an excuse.
5. **Structural**: the player is massless (gm = 0) and no planet thrusts, so the lens's stated purpose — "a thrusting planet's or ship's pull reaches others at light speed" — is unobservable in every scene the current API can express.

**Consequence:** deleting the cursor walk entirely (always read the current binding) leaves every shipped test and every gate green. The run's falsifier is exactly what was removed.

## Predictions, novelty, fit

- `predictions.md` (mtime) sits between the baseline logs and every after-log: fixed before the decisive patched runs. P1 held (independently reproduced); P2 held (suite green), though the dossier never reports which pinned digests moved — in fact none could, since nothing observable moves (my probes measure why); P3/P4's shipped forms missed, honestly disclosed, and my probes confirm the disclosed causes.
- Novelty: the representation is law.md's (00a2d25, 5 October) and was measured standalone (q-gravity-at-c, q-gravity-cursor — both silver); no commit touches `crates/universe/src/news.rs`. The implementation, cursor plumbing and the two controls are new. Correctly framed by the author.
- Fit: PRINCIPLES #23 ("Nothing past c … cheaply partition compute") — the partition is now data, one cached integer test per kick per source, zero new memory (verified: cursors are the only added state; wall time indistinguishable). HANDOFF "Headed next" #3 names this work. Safe to adopt: it cannot move anything today.

## Records defects

- `run.log` is empty (0 B) while the dossier cites it three times (E3's three-way free-fall measurement, the twins' bit-identity). Those numbers cannot be regenerated from the folder; the probe code is not in the patch. Consistent with physics and with my probes, but not evidence.
- `suite-after.txt` records "11 passed; 2 failed" (the two removed tests, failing mid-build) while E2 describes a different mid-build state ("10 passed, one failure"); the stored artifact is stale relative to the final patch.
- The reproduce block's comment ("the cone, the arrival, the Laplace control") — only the cone ships.

## The one experiment that would make it gold

A consumer whose cadence resolves a massive source's light delay — the Fermi-frame member the author names, or the massive doll-centre player of motion law v2 — shipped as the test that fails if the cursor is deleted: every kick before the cone bit-identical to the no-burn twin, the first differing kick the first at or after t_e + |x|/c, never before; plus the Laplace spiral control at the fastest β the API expresses.

## What the author missed

- The quantified invariant E3 gropes for: **news bites only when light delay ≳ rebind interval**; at the plane's scales that ratio is ~10⁻³ for every massive pair, so all news traffic rounds below the kick quantum. One measured line; my probes measure it.
- The moon's rebinds *are* read through cursors by 9 bodies in the shipped plane (the dossier presents the tide/fleet frames as the only instantaneous reads and the gates' scenes as the only no-op); the stale reads happen and round away — the sharpest fact in the run, and it went unmeasured.
- The retention fallback in `news.rs` degrades to the **current binding** (the acausal read) when the delivered version's segment is pruned — stronger than the dossier's "stale (still causal) version" wording; reachable when consumer→source distance exceeds 2×(source→player) + 2²⁶ ticks.
- A source's birth version is read before its light cone arrives (existence is initial data; only changes travel at c) — unstated, benign, but belongs in law.md when adopted.
- The digest now hashes cursor state, so digests distinguish gravity modes even where every trajectory is identical (observed: digests differ while all 28 bodies' states are equal).
