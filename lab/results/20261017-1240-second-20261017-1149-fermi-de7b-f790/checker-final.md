Working...
Check complete, tree restored. Verdict: **Grade: gold** — written to `check.md` in the run folder.

**What I verified:**

- **Reproduction (3 ways):** runner's regen.log matches all dossier rows and stored flight logs; my own rerun of the decisive `BELT_SPLIT` flight is byte-identical to `split.txt` (mod `build_s`); arm-7/6/8 outputs match de7b's archived branch record number-for-number.
- **Patch provenance:** crates hunks (`ext.rs`, `step.rs`, `binding.rs`) byte-identical to 98cb's published patch; negative control (toggle off, same args) reproduces the shipped arm exactly with the welding still exact at a later crest (B/2h = 6.0001) — the instrument measures the real schedule.
- **Mechanism:** re-confirmed in this tree at step.rs:849-862 — one `full`, Boundary at `t+full/2`, Kick at `t+full`.
- **Predictions:** predate all decisive arms (mtimes); held on substance, two label misses honestly disclosed.
- **Adversarial (beyond the author's domain):** split at base lever 8 (effective 5, never flown by anyone), split seed 2, split at N=3×10⁴ — 9,700/9,700 and 29,700/29,700 welded, every identity 1.0000, dead 0; the N=3×10⁴ early window lands exactly {kick at h, boundary at 2h}, confirming the K,B alternation directly.
- **Novelty:** 98cb never measured boundaries (grep of its dossier); this is the first direct flight of the composed arm — the exact experiment de7b's checker named.
- **Page:** fold was faithful; I added my adversarial confirmation in the page's checker-note style. Topic correctly stays open (split legality at S≈20; only two golds agree).

**Named flaws (all cosmetic, none touching substance):** `arm7.txt` and the rtf-12k log claimed but not stored; the record-diff sentence omits the added mixture-counter field; ledger.txt's "~4.1-4.3 intervals" label is wrong for arms 6/8 (rates themselves correct); mixed-belt minority remains untested (disclosed). With this second check agreeing, **de7b's gold stands**.
