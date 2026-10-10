# Check 2 — 20261010-1029-taleb-5c01 (blind second checker)

Grade: gold

**Abstract.** Claim: the pairwise encounter tier silently drops every real encounter whose minimum sits at a horizon edge (t=0 or t=H) — 20.2% of true encounters for a bunched fleet — not a concentration corner, and not guardable by a·(e_i+e_j)/ρ. Reproduced bit-for-bit in a clean worktree (main + patch.diff): controls 5/234 and 284/1407, 2-orbit 281/2250, 20-orbit 162/8279, full sweep, and the k=256 probe including `setup_evals` (48158654/734999 identical). My independent numpy Kepler adjudicated 193 missed pairs across 5 scenes: all at edges, zero interior, zero false truths; fresh seeds 77/91 give 21.1/21.9%, uniform-phase 19%. Gain: kills the tier's completeness premise (10× the gold's drop rate) exactly at every kick/handover horizon re-open; fix is two unconditional edge checks, one step. Cost: amending the tier plus main's `matchup` judging utility.

## Reproduction

Clean worktree at main (a838a28) + `work/patch.diff`. Note: the dossier's "apply the gold 20261006-0346 patch first" fails literally — main already merged that gold's `taleb.rs`, and the run patch is a new-file diff replacing it; the run patch alone on main is the effective tree and compiles and reproduces everything. All dossier commands re-run (each ≤ 60 s; the 20-orbit run took 13 s here): every number matches, including verdict splits, kind histograms and `method_only = 0` (the tier never reports a false encounter — sound but incomplete).

## Held-out predictions

`predictions.md` (10:39) predates all raw JSONL (10:50–11:03). Honest scoring: P1 positive control held (2.1% inside the pre-registered 1–5%); the negative control failed and that failure is the finding; P2/P3 (the author's own cliff and Δa stories) failed and are reported as failed; P5, P7 held; P6 was modified with disclosure. No tuning on held-out cases — the discovery ran against the author's own expectations.

## My attacks (beyond the dossier)

1. **Independent-language adjudication, 24× the author's sample.** Pure-python Kepler over every dumped missed pair (60/scene): 1-orbit 29@t0/31@tH, 2-orbit 33/27, gold-adj 4/1, uniform-λ 3/5, seed 91 31/29 — **193 pairs, all edge, 0 interior, 0 above ρ**.
2. **Fresh scenes.** Seeds 77/91: 21.1/21.9%. σλ=0.3: 17.5%. Uniform phase with Δa=1e-2 (no bunching; only random initial closeness): 19.0% — the hole is not bunching-specific, strengthening the claim beyond the dossier's framing.
3. **The `check`-verdict second mechanism ruled out.** Seed 91 shows 79 `check`-verdict misses (window contained the offset, exact check found nothing) — I adjudicated them: edge-located like the rest.
4. **k=256 reproduced from source** (`d_of_s`, pairs.rs `let k = 32` → 256, rebuilt, reverted): misses identical (5, 284), `setup_evals` exactly match the stored files — the reverted experiment was real.
5. **Reconciliation with 0306-taleb-8af8's "zero misses" verified in code, not inference:** `matchup` on main (`crates/encounters/src/main.rs:97`) filters truth events with `inside = |t| t > 0.05 && t < t_end − 0.05` before counting misses — that measurement structurally excluded the edge band. The dossier's "shared blind axis" is true and understated: it is the judging utility on main, so every run judged by it inherits the blindness. The 5 October taste-log lesson (agreement ≠ independence) is a live instance here.
6. **Contract violation confirmed:** `pair_events`'s own doc promises "All minima below ρ … with time in [t0, t1]"; the misses violate the closed interval, and the t=H half is unambiguously inside the requested horizon. Under horizon refresh, an encounter straddling the boundary is reported by neither adjacent horizon — the compounding route (#13).

## Novelty

Prior art: r8 v2 (candidate-set completeness, board 30 Sep — different layer), the 6 Oct gold's 4–6% window-tier drops (attributed to co-orbital concentration), 8af8's zero-miss (edge-excluded by construction). This run reattributes the mechanism (horizon edges, not concentration), quantifies 10× worse at fleet geometry, shows no guard number exists, and exposes the harness blindness that hid it. Nothing in docs/HISTORY.md covers scheduling-tier edge completeness.

## Fit

Board focus: "candidate work must track real encounters"; every kick re-opens a horizon. PRINCIPLES #13 ("basically we don't want errors that can compound") — a silently wrong event list; #19 ("a fix signals the wrong representation") — steady-state windows misrepresent the boundary. Fix cost ~zero against the certificate's accounting.

## What the author missed

- The decisive reconciliation fact sits on main, not in 0306's branch: `matchup`'s `inside` predicate — the blindness is structural and will corrupt future judging too; the fix owner should patch that utility alongside the tier.
- The straddling-encounter leak (missed by both adjacent horizons under refresh) is implied but never stated; it is the exact reason this is the ruin class, not a cosmetic boundary convention.
- Bookkeeping: the aggregate "window 546, check 4" does not reconstruct from the stored files (I count 566/4 over the natural scene set); every per-scene number is exact. "Misses vanish at R1≥30" is loose (σe=1e-2 → 0.6% at R1≈250; my uniform scene shows 19% at R1≈1) — the correct statement, which the data supports, is "no monotone guard exists".
- Whether the t=0 side belongs to the tier or to a current-state contact check is a design call the dossier leaves to the fix owner; the t=H side admits no such deferral.
