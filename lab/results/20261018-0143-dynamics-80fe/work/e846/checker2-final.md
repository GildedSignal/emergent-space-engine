Working...
**Grade: gold** — written to `lab/results/20261016-1319-dynamics-e846/check2.md`, with one in-place correction to the author's wiki page.

**What I did as checker2 (blind to checker 1):**

1. **Reproduction** — the runner's regen (exit 0) matches every dossier number; my own φ=105° plane rerun is bit-identical to `plane.jsonl` (−1.45 dies at 85.9688 P, `planet_kick`), so the census and dead set are deterministic and the 3-IC b9be discrepancy is real, honestly flagged.

2. **Instrument, attacked with zero shared code** — I rebuilt the CR3BP in scipy: the model reproduces the judge's control digits exactly (1180.7452/1064.8157/1097.3360), J(L1) = 5.768404e-9 exact, and an event-resolved 512 P integration confirms Rp-scale dives on a dead-IC crosser (0.26 Rp). The `tracking()` instrument is sound.

3. **Outside the author's range** — 1024 P oracle: class separation strengthens (dead-truth median 0.70 Rp vs alive 105 Rp). Plane at 1024 P on the kept-crossing ICs: **5/16 die `planet_kick` at 527–950 P** — the 512 P "mirror error" misses convert to kills at later real encounters, the strongest possible confirmation of the encounter-parity reading.

4. **Outcome-free census** — no consumer of the new `Resolved::Lost*` variants outside the census files; every changed return follows an unchanged `alive = false`.

**Gold grounds:** a premise kill (b9be's "false death" reading refuted on both ends: the oracle keeps everything by construction, and the P/256 grid was a control that could not fail — its 2.89 Rp floor vs a resolved 0.016 Rp), adoptable in one step as the B12-family encounter-parity gate, zero engine change. The decisively failed pre-registered predictions (P2: 0% terminals) are the signature of genuine pre-registration, reported as failures.

**What the author missed** (now on the page): the 19/47 and 20/97 counts are themselves shadow statistics — my independent integrator gets 1.85 Rp where the judge gets 0.046 Rp on the same IC, so the certificate must be the *rate*, not per-seed membership; plus a 1088-vs-1120 dossier typo and the un-bisected driver lead.
