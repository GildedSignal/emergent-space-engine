Grade: silver

**Abstract.** Claim: memo R5's cursor — one integer index per (body, source) pair — selects the retarded news prefix exactly at ~1 test/kick, and a frozen single-version ghost is structurally unstable. Reproduced bit-identically in a clean tree (7,203,000 kicks, 0 mismatches, ties exact; tests/kick = 1 + arrivals, flat while K ×100; news bound at every β, cursor≡brute bit-identical; ns0 unbound 5.05 orbits, dE 310). My independent mirror matches E3 exactly; my refresh-cadence sweep quantifies the L3 claim (bound at 64-step refresh, unbound at 256). But the cost gain is overstated: against a cursor-seeded binary search it is ~8× at sparse news and negative (99 vs 18 tests/kick) at dense, and the composed news-kick cost is unmeasured. Adopt: 4 B/pair + version ring.

## Reproduction

Clean tree (`work/patch.diff` is empty — no edits outside the run folder; `cursor.rs` md5 matches). `rustc -O` (2 cosmetic warnings), all five commands: exact 8.6 s, cost 21.7 s, burst/laplace/ghost 0/3.3/0 s — every output **bit-identical to `out-all.txt`**, `results.json` numbers trace to it. E1's accounting checks (7 configs × 900k + 900k photon + 3000 head-on = 7,203,000). Lag numbers re-derived analytically from the circular-motion chord (13/37/89 versions at β=0.1/0.3/0.9, including the β=0.9 shortfall vs naive 2β/dt = 114.6). Ghost arithmetic correct (0.01·499 s ≈ 5 s … 8 kpc = 26,080 yr).

## Predictions

`predictions.md` (15:44) predates every decisive output (`out-all.txt` 16:03, `results.json` 16:04). The genuine misses are disclosed (P3's |dE| and |Δa| bands, P4's one-version-suffices — falsified and reported as such), which is the held-out process working. One blemish: P2's "p99 ≤ 3 tests/kick at λ ≤ 1" is reported "fully held", but the stored output has **p99 = 5 on every adv/kick ≈ 1 row**; it holds only under the "events per light-crossing" reading of λ, an ambiguity the dossier resolves silently in its favour. Also P3 was run at 60 orbits, not the predicted 100 (narrowing undisclosed).

## Attacks (mine)

1. **Superluminal source chain (A1).** The integer reverse-triangle inequality gives both monotone k\* (consumer steps causal) *and* the prefix property (**source news chain causal**). The dossier's "what would make it wrong" names only the consumer side. A chain with two ~50c gaps (teleport away and back): brute k\*=2, cursor k\*=0 — mismatch. Law #23 covers it in-engine, but the memo's contract must state both preconditions.
2. **ns0 structure quantified (A2).** My independent Python mirror reproduces E3 exactly (news dE 8.130e-3; ns0 unbound 5.0525 orbits, dE 310.3). Noise sweep: unbound time invariant (5.0525) for seeds ≤ 1e-8, earlier at 1e-4 — departure is truncation-seeded and grows structurally. Refresh-cadence sweep at β=0.3: versions every 1/4/16/64 steps stay bound (dE 0.8–1.3e-2); every 256 steps (0.64 orbit) → unbound at 6.13 orbits. So "per-rebinding versions" is confirmed with a measured staleness boundary ≈ 0.2–0.6 orbit — new design content the author left unquantified.
3. **Honest competitor baseline (A3).** Cursor-seeded binary search on the same random-worldline style: 15.7 tests/kick at K=60,000 (cursor 2.02 → gain ~8×, not 30,000×) and 17.9 at dense news where the cursor pays 99.1 — the cursor **loses 5.5×** at dense news; E2b's 1000-test burst kick would cost ~20 with a gallop. "Brute pays K" is a strawman baseline; the strong form of the claim (the identity tests ≤ kicks + events — the information floor, cursor-optimal at sparse news, the engine's regime) does hold.

## Novelty

The cursor is Opus memo R5's (`lab/refs/opus-math/memo.md` §R5, including the k\* formula, O(1) amortization and this exact probe list); this run is the commissioned falsifier (HANDOFF: "R5 `q-gravity-cursor`"). a237 (silver) measured the news *physics* via an iterative retarded solve. New here: the exactness measurement, the cost identity, the ns0 falsification of R5's ghost/memory premise, and per-scale depth. Not a duplicate; the mechanism is not the author's either.

## Goal fit

Moves law.md "Gravity travels at c" (Julien, 5 October), a live focus; PRINCIPLES #23 ("Nothing past c… cheaply partition compute" — the cursor is that partition as data), #3 (total work = kicks + events), #13 (selection exact in integers). The ns0 result respects #6 the hard way: generators must be re-anchored where the dynamics bind.

## Why silver, not gold

Reproduced bit-identically, one real premise falsified (the frozen ghost), honest held-out discipline — but (a) the headline cost gain is measured only against brute force; the natural log-K competitor is absent and *wins* at dense news; (b) "adoptable at ~0 cost above the force" is asserted, not measured — every news kick still pays a Kepler evaluation (uv_prop, 24 secant iterations) per source per kick, and no composed news-kick cost exists (a237's 6× included the solve this run deletes); (c) a prediction clause contradicted by the stored output under its natural reading is reported as held "fully" — the exact class the taste log dinged a237 for.

## The one experiment for gold

Wire the cursor into the news kick and measure the composed cost — cursor selection + tube evaluation vs an instantaneous kick and vs a237's 6×, with the binary/gallop control at sparse and dense news, on the plane's own kick path. If the composed news kick lands at ~1–2× instantaneous (tubes read closed-form per R1, not uv_prop), R5 is adoptable as stated and this is gold.

## What the author missed

- The source-side causal precondition (prefix property) — the cursor's exactness needs both worldlines causal; only the consumer side is stated (A1).
- The log-K/galloping competitor; the right engine default may be cursor-advance for sparse news plus gallop-on-burst (2⌈log₂ arrivals⌉ instead of the burst size on one kick).
- The refresh-cadence boundary of version recording (A2c): "per-rebinding" now has a number, and the plane's kick epochs (many per orbit) satisfy it with margin — worth stating so the star-system depth~1 case is not read as license for rare rebinds.
- P2's p99 ambiguity and P3's 100→60-orbit narrowing, both silently in the author's favour.
- (Self-flagged, agreed: photons only as gravity consumers, handoff cursor rebuild O(pairs), galaxy generator-ghost analytic.)
