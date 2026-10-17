Grade: gold

**Abstract.** Claim: the allocator's finality-assert crash is a window-grid defect of
chunked batch `run_to`, not a live-path hazard; frames mode never fires it, and a one-line
driver rule (grid-aligned targets) replaces the engine-side fix the page expected.
Reproduced clean-tree: crash at interior 100 ("from 96 … published 100"), bit-identical
quiet-14k crash ("region 13279 from 112 … published 150"), on-grid 96/112 survive with
bit-identical digests, 18/18 frames arms survive. Checker2 extends: batch under
`Law::Relativistic` (interior crashes, on-grid survives) and on-grid 28k — the rule is
law- and scale-independent. Gain: deletes the expected engine change; adoption is one
driver-discipline line (`xtask/src/regions.rs` `advance` passes arbitrary targets today).

**Reasons.**
- **Reproduction (all verdicts).** Patch applied by me, rebuilt, rerun: b-864-chunk100
  crashes (region 158 vs regen's 157 — the tripping region is a draw, the signature is
  not: `published tick` = the interior target every time); chunk96/112 survive with
  digests bit-identical to the regen's (`9d398da5…`, `f5485e72…`); quiet-14k chunk150
  crashes bit-identically to author, regen and both checkers; the frames arm survives.
  The regen (exit 0) matches the dossier's tables; per-arm counters mix author-window and
  regen draws, disclosed as such.
- **Mechanism, code-verified on the shipped tree.** `goal_tick` Frames branch rounds up
  to the window grid (567), `next_unit` truncates stride ends only via `goal` (762),
  `finished()` demands `verified == target` in batch only (1671), `run_to` force-publishes
  (1943), the assert (1451), `certify` files truths under every covered window and clashes
  on hull overlap regardless of temporal disjointness (1091–1108). Interior stride ends are
  reachable only through a batch target off the grid; frames cannot manufacture one.
- **Held-out predictions.** P1's pre-registered kill criterion ("no arm crashes anywhere →
  batch-driver-only") fired against the author's own hypothesis; P4 held where measurable
  (18/18 `hard_viol = 0`, `accel_drops > 0` under load); P2/P5 wrong and disclosed.
  Precedence is not provable from mtimes (scorecard appended after; the regen overwrote the
  author's matrix traces; `run.log` is empty), but the failed-prediction content is
  anti-fabrication: a post-hoc author would not pre-register "frames crashes" and
  "relativistic crashes more readily" and then report both wrong.
- **Adversarial (mine), one outside the author's domain.** (1) Batch under
  `Law::Relativistic` — the author's `rel` prefix is dead code in batch mode (never used in
  `main`; my first "rel batch" arms silently ran Newtonian, digests prove it), so I fixed my
  copy: interior 100 crashes "from 80 … published 100", on-grid 96/112 survive with
  law-specific digests (`712efa9c`/`32528ab8`). The driver rule is law-independent — this
  closes the strongest objection to adoption. (2) On-grid 28k chunk 256 (author's on-grid
  batch stopped at 14k): survives. (3) Interior 200 at 864: survives — consistent with
  "interior necessary, never sufficient". (4) Frames `ahead = 0.0` (below the author's
  min): survives. (5) Reachability: the only shipped non-test allocator driver is
  `xtask/src/regions.rs:35`, `run_to(target)` with caller-chosen targets — the rule's
  addressee is real.
- **Novelty.** The prior page's open directions 1 (engine-side fix) and 2 (frames decides
  it) are exactly this question, untested before; docs/HISTORY.md has no finality-assert,
  run_frames or window-grid entry. The run also corrects 9b46's dossier in code:
  `loose_gas` builds from `World::new` with no law, so the wave/quiet family is Newtonian.
- **Page.** Faithful; folds the result in with the honest caveats kept (restored-lineage
  channel open, draw-dependence disclosed). I amended item (3) in place: the checker2
  rel-batch and 28k extensions, and the auditable portion of the interior tally (of the
  "7/11 on this box", only 3/5 survive in the regen traces — the rest were the author's
  overwritten window; my window adds 100-s1 1/1 crash and interior-200 0/1).

**What the author missed.**
- The instrument's `rel` prefix is silently ignored in batch mode — the battery's only law
  gap, and the one case (light-cone finality + interior publish) where the grid rule could
  plausibly have broken. It holds (above), but the author's Evidence section describes the
  prefix as "switching the scene to `Law::Relativistic`" without saying frames-only.
- The "live path" framing deserves one sentence of precision: `run_frames` is the
  allocator's player-facing mode (FrameConfig, View), but no shipped non-test code calls it
  either — today the allocator's only shipped driver is the xtask ladder, i.e. the batch
  chunk pattern. The crash is a driver-discipline defect either way; "not a live-path
  hazard" is about the designed continuous-publication path, not a wired game loop.
- The interior-tally letter: counts that the surviving artifacts cannot regenerate (the
  run's own rule: "numbers the shipped code cannot regenerate" lose their grade — here the
  verdicts all regenerate, only the 7/11 denominator does not).
