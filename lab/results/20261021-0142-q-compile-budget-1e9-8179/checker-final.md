Working...
Check complete. Verdict written to `lab/results/20261021-0142-q-compile-budget-1e9-8179/check.md`: **Grade: silver**.

**What I did:**
- **Reproduced**: `regen.sh` exit 0, deterministic output identical to the runner's log; verified `audit.py`'s counting reimplements `wiki.py:87-88` exactly, and its "411 lines / current best 240" matches the live index flag.
- **Attacked with a stricter instrument** (word-boundary matching instead of the author's substring test): literal coverage is 272/341 (79.8%, not 84.5%) — 16 tokens were substring-only hits. No material loss: all 16 are also record-backed.
- **Tested the claim the audit never executes** — that the non-literal tokens sit on cited runs' records: pulled all ten runs' full branch records (dossiers, checks, `data/*.csv`, regen logs, excluding their `wiki/` page proposals, which are live-page copies and would trivially match). All 69 non-literal tokens backed, 0 unbacked. The three apparent misses (2,842/6,276/12,550) turned out to live only in 5f76's `regen.log` and `data/A*.csv` rung buckets — resolved.
- **Reverse sweep** for fabricated numbers: clean (only the run's own id in the header).
- **Semantic fidelity**: every current-best line checked against the old page; the flagged today-cost union (22.5–43.4) carries its provenance split inline and both endpoints are on 3aec's record; all seven old open directions kept or closed with their deciding run. No page corrections needed.
- **Novelty**: no prior compile of this page; fd4f (coorbital-cert compile) is the precedent and was graded silver.

**Why silver, not gold**: fully reproduced and independently confirmed, but it moves no board row, deletes no engine component, and refutes no premise — the lab's own gold bar and the integrator's precedent both say silver. The gold case is integrator-side: publish, then one budget-1e9 run working off the 15-line page without re-deriving closed numbers.

**Key author misses** (detailed in check.md): `audit.py`'s rule (b) structurally cannot fail, so its "0 dropped" pass is uninformative — the record-level backing the dossier asserts was never executed by the instrument; substring matching inflated the coverage headline; "Eight NEW blocks" is actually seven. Shipped tree left untouched (`git status` clean apart from the untracked results folder).
