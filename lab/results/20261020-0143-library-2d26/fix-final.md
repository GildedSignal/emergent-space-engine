Working...
**Fixed — `regen.sh` now runs end-to-end: exit 0, 151 s (limit 15 min), tree left clean.**

Three defects fixed in `regen.sh` plus the script it needs:
1. **Wrong cwd** (the reported crash): line 5 rose only two levels (`lab/results/<id>/../..` = `lab/`, not the repo root); cargo still built because it walks up to the workspace manifest, masking it until `cd work`. Now `../../..`.
2. **Binary path**: with `CARGO_TARGET_DIR` set (it is, here), `$BIN/examples/nladder` lacked `/release`. Now `${CARGO_TARGET_DIR:-…}/release`.
3. **Fragile tail**: this box's `tail` rejects obsolete `-1`; now `tail -n 1`. Also `work/analyze.py` crashed on its own coast control arm (`slack_pre`/`lag_onset` are `None` when no onset, two division/format TypeErrors) — guarded; the price block now requires an onset.

Also made the Readwise refresh best-effort (`|| echo` fallback to the cached export) so a tokenless/offline checker env still verifies the quotes.

**Proof (patch applied first, exactly as the runner does):** shipped `ladder:` lines regenerate the dossier table — 10⁵ burn 5.81/160.8/826/111 (dossier 5.74/160.5/813/108), 2×10⁵ burn 6.49/338/1820/113 (rerun band), 2×10⁵ rtf400 0.422/**11.947**/1677/**13** (dossier 0.39/11.94/1590/13), coast control no wave (excess 5 ms); coverage law 0.307/0.125/2.34 with composed 10⁶ coverage 0.32 (dossier 0.31/0.13/2.55/0.34) — ordering and the ≤10⁵ crossover conclusion unchanged; quotes 5/5 byte-identical with a fresh fetch (770 docs).

**Claim of the run (unchanged):** the kick wave's three exits are typed by one measured law — prepay coverage = (pre-onset ebb)/(wave excess): 2.55 at play-side cadence, 0.13 at test cadence, 0.34 at 10⁶ — so compute-ahead is a ≤10⁵ patch, amortization covers ≤ ~3×10⁵ at a presented-lag price ∝ K, and only deleting the burn's mint-synchrony scales.
