Grade: silver

**Abstract.** Claim: the prior check's digest flip (`6ce6…`↔`56f4…` at cut 406050894) does not reproduce; the canonical state is schedule-invariant per body; the smoothness frontier is machine-state-dependent. I reproduced all of it on a clean tree, 26 fresh cells: paced/unpaced/3 seeds → `6ce636fa`/`c9794984`/`1e05437c`; load 3.6–7.6, contended core, `--dt-ms` 16.7–100, `--engine-events` 1–64, threads 8 (worst hitch 32.8 ms), cut drift ±1–5 s, 8 paced repeats, and a fresh unpatched rebuild of a838a284 — never `56f4…`. `ES_DIGEST_PARTS=1` diff: all 76 per-body lines identical, only the un-hashed `resolved` counter moves. Gain: the digest control stands or the doubt is localised to the first checker's harness. Cost: none (probe not for merge).

## Reproduction

Every command from the dossier's "Reproduce" block, from a clean scratch dir, plus the clean-tree rebuild (`cargo build --release -p xtask`, 36 s) run paced/unpaced/b5: all `6ce636fa` at cut 406050894. My totals: 26 runs, zero flips. The author's 57 data JSONs match every dossier number I checked (digests per seed and per neighbouring cell, worst-hitch 6.5/6.8/7.0 ms, overflow 3–4, low1 100, gather share 0.63–0.65 at load ~4; the low-load dip pattern low1 9.9 in paced-1/2). All cells ran the disputed configuration by default (b5, threads=1, members 48): `ENGINE_BUDGET_MS = 5.0`, CLI default threads 1 — the coverage is faithful to the first checker's cell.

## Predictions

`predictions.md` (38 m old) predates every data file (37 m and later): held out properly. Scored honestly by the author: P1 held; P2 (flip reproduces within ≤6 repeats) **wrong**; P3 (flip localises to bookkeeping) wrong — the field-group dichotomy was built for a phenomenon that never appears; P4 vacuous; P5 untested; P6 right in substance. Under the gold bar ("held-out predictions held") this is the binding failure: the pre-registered market pointed at a flip that is not there — the author says so themselves in the lens section.

## Attacks (mine, beyond the author's)

1. **Load and contention:** 6 CPU spinners (load 3.6→7.6), paced runs floating and pinned to a contended core — `6ce6…`, worst hitch 11 ms.
2. **Extreme schedules:** `--engine-events 1` (max deterministic deferral) and 64 with threads 8 and a 32.8 ms worst hitch — `6ce6…`; `--dt-ms` 100/16.6667 — `6ce6…`.
3. **Cut drift (H-cut):** `--seconds` 19/21/25 → cuts 385.7M/426.4M/507.6M, digests `dd1f…`/`284c…`/`c55b…` — `56f4…` is not a neighbouring cut either.
4. **Build state (the author's named confound, untested by them):** fresh `cargo build --release` of the unpatched tree — `6ce6…` on paced/unpaced/b5. A standard rebuild does not recreate the flip, and the probe patch is confirmed digest-neutral by code read plus this control.
5. **Burst:** 8 consecutive paced repeats, events/s 336–338 (the prior checker's `6ce6` attractor was 338; their `56f4` sat at 227) — all `6ce6…`.

## Novelty

H0213 recorded the digest-over-schedules claim; the prior run's check attacked it (new then); this run is the demanded independence test of that attack, plus `ES_DIGEST_PARTS` (a one-step bisect tool) and 3-seed invariance — no prior H entry covers the non-reproducibility of a falsification. Not a redo.

## Goal fit

Direct: the digest is the plane's certificate control (PRINCIPLES #2 "exact means deterministic and reproducible"; #10 "measure before claiming"; the 5 October lesson — agreement between runs sharing a harness is not independence — is applied against the first checker's 3 agreeing runs). Nothing to adopt in the engine; the caveat both checkers now share (frontier is machine-state-dependent) is correctly priced.

## Why silver, and the one experiment for gold

Everything reproduces, but gold needs the flip **resolved**, and this run cannot: `56f4…` remains real-as-reported (3/9 runs, one unpaced, on the first checker's harness) and unexplained. Two checkers now disagree across harnesses — a DISPUTED state, exactly the case the rung rules anticipate. The named experiment: rerun the **first checker's** exact session (their tree state, `cargo run --release` invocation, their box) with `ES_DIGEST_PARTS=1` exported; if the flip shows, one line moves and names the field group and body, finishing the bisect in a step (the M1 remeasure serves the same role). If it cannot be produced even there, the flip closes as a harness artifact and this becomes gold.

## What the author missed

- **The "wall 5/10/15 ms" axis in the claim is not in the data:** all 57 JSONs record `engine_budget_ms = 5.0`, and the probe patch *removed* `--engine-ms` from the CLI, so the sweep as described was impossible with the shipped probe binary. Harmless here (b5 is the disputed cell, and ev1→64 spans more deferral than 5→15 ms), but the sentence overstates the recorded coverage.
- The events/s discriminator (227 vs 338) and their own `resolved` variance (6742/6780/5870) are two ends of the same handle — what "fewer events at the same cut" means for a digest taken after `settle` — and the dossier never connects them; that is where a mechanism story would start if the flip is ever real.
- The first checker's commit/build state is asserted "same shipped semantics" but not evidenced (no `git rev-parse` of their session in the record); my rebuild control narrows this but only for a838a284.
