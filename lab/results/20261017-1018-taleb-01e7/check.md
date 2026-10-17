Grade: silver

The `allocator-ratchet` conflict is resolved and reproduced: the shipped finality assert (`alloc.rs:1451:17`, engine code, no engine edit in the patch) is a publish/rollback boundary defect. Frames crash on a no-approach churn cluster at scene start (author 3/9, regen 4/9; chronons 32–96). On-grid chunks crash (2/3; checker adds chunk 96 and 512), and single-call batch to an on-grid horizon crashed 4/4 here — 5d87's "one call per process" dies with the grid rule, leaving only the engine-side fix. `min_region 32` → rb 0 (3/3); window 32 survives 6/6 at rb 79–114. Adoption cost: a decision, no code. Not gold: the run's own regen falsifies three reported rows (P8 "batch survives", vmax-16 "0 crashes", "gaps 1–4 windows"), and rb fails as a separator at n=480 (rb 144–166, 0/3).

## Reasons

**Reproduction.** The runner's regen.sh exited 0 and its log (regen.log, on disk) reproduces every core arm; I re-applied `work/patch.diff` (one new example file — verified no engine edit), rebuilt, and re-ran. Verified: the panic is the shipped assert at `alloc.rs:1451:17` (`assert!(r.fin_hi <= s0, …)`, "Nothing published can be touched (asserted)") on worker threads `alloc-N` in the `.err` traces. Frames selfchurn vmax 2 crashes at chronons 32–96 (author 3/9; regen 4/9 — a wall-clock race, disclosed); on-grid chunk 128 crashes 2/3; `min_region 32` → rb exactly 0, 0/3; window 32 survives at rb 81–114; wave 0/5, crossing 0/4 — all as claimed.

**Adversarial cases (mine; three outside the author's tested range).**
1. *On-grid chunk generality:* chunk 96 (6×window) and chunk 512 (32×window) both crash at vmax 2 s11 (panic 32→48) — the on-grid crash is not chunk-128-specific. The driver rule is dead as a complete fix at three sizes.
2. *Single-call batch — the sharpest case:* the dossier reports P8 "held — single-call batch survives" (table row: 0 crashes). The run's own regen log contradicts it (`sc2-batch exit=101`, 32→48), and I confirm: single-call batch crashed 4/4 (horizons 1792 [on-grid], 1800, 1808; seeds 11 twice, 15; one 1792-s15 draw survived — reachability races). This *strengthens* the thesis — 5d87's rule in its strongest form ("grid-aligned targets, or one call per process") does not close the churn class — but it falsifies a pre-registered prediction reported as held.
3. *Held-out larger N:* n=480 at vmax 2 (the crashing regime; the author ran n480 only at vmax 8): rb 144–166, 0/3 crashes. The "crashing regime = rb 57–95" separator does not generalize beyond the n=240 sweep — rb is an in-band correlate; incidence also rides the load/size band (b966's gradient). The regen's vmax-16 crash (1104→1184, one of 16 pooled draws; my fresh seeds 16–21: 0/6, rb 0–2) likewise breaks "rb ≤ 8 never crashes".
4. *Window-32 lead, fresh draws:* seeds 14–16 survive 3/3 at rb 104–108 → 6/6 pooled. The lead stands.

**Predictions.** Pre-registration is genuine: `predictions.md` (10:24:17) predates the decisive traces (`work/patch.diff` 10:33, out/ 10:33–10:34) and the file times survived the runner's regen overwrite. P1/P2/P3/P5 held; P6 honestly reported inverted (a real finding: dose is sustained overlap, not spread); P4 → lead as disclosed; P8 reported "held" but falsified by the run's own regen log — a record defect, not a discovery defect.

**Novelty.** docs/HISTORY.md has no entry for the b966/5d87 dispute (lab-side, unmerged). b966 established frames reachability on a bulk-approach scene (conflicts near ~600); 5d87 established 18/18 frames survival plus the batch interior-tick channel. New and standing: the no-approach scene, the scene-start timing (chronons 32–96 ≈ 0.2 s of play), on-grid chunk crashes, the single-call crash, the `min_region 32` guard mechanism, and the reconciliation itself. My batch/chunk crashes come from distinct processes and seeds with distinct region ids — distinct events, not a harness echo (the 5 October lesson).

**The page.** Corrected in place (five overstatements): "fast-dispersing gas never crashed (0/15)" → 1/16 pooled; "all panic gaps 1–4 windows" → 1–10 windows (16–160; regen shows 80 and 160); "deterministic in batch / the batch race repeats per seed" → reachability races (panic values per seed are stable); rb separator scoped to the swept band with the n=480 caveat; window 32 updated to 6/6, rb 79–114; vmax-16 "goes quiet" softened to "mostly". The corrected page is faithful to the evidence.

**Goal fit.** Resolves the index-flagged conflict and retires one of the two candidate fixes as a complete answer — a premise shown wrong. PRINCIPLES §13 "basically we don't want errors that can compound that's the goal": the certificate aborts rather than degrades, and §25 "don't multiply by zero" — a panic in the player's first loaded second is the zero. The engine-side boundary fix (9b46 open direction 1) is now the only live door.

## The one experiment that would make it gold

Re-run the three falsified arms under the page's own protocol (≥ 6 draws, ≥ 2 replicates: single-call batch at on- and off-grid horizons; vmax-16 incidence; n=480 at vmax 2) and rewrite the dossier table so every row regenerates from regen.sh. The physics is already standing; only the record blocks gold.

## What the author missed

- P8 and the vmax-16 arm were reported from single draws (batch: 1 per vmax) against the page's own direction-4 protocol (≥ 3 seeds, ≥ 2 replicates), and P8 contradicts the run's own regen log — the dossier was not checked against regen.log before writing.
- The single-call batch crash — the sharpest kill of 5d87's rule, since "one call per process" is the rule's second limb — was missed by one draw of luck.
- "Deterministic in batch" conflated stable panic values with deterministic reachability.
- The rb separator was asserted from the n=240 sweep; the n480-vmax-2 arm (already in the harness) was the obvious falsifier and was run only at vmax 8.
- The window-32 margin lead was noticed only incidentally (the lens says so); on fresh draws it holds, and it is the only cheap partial mitigation found.
