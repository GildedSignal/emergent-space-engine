Working...
**Grade: gold** — written to `lab/results/20261020-0036-components-6b9a/check.md`, with three corrections folded into the author's `wiki/calendar.md`.

What I did and found:

**Reproduced exactly.** Applied `work/patch.diff` to the clean base (3a8277e4), ran `regen.sh` myself (27 s warm, exit 0): 28.00 B/slot N-flat 10⁴–10⁶, 156 B/body → 156 GB = 19.5× the machine at 10⁹, live arm 0.272 GB, flip 573×; census identical at both rungs. Code claims verified by reading universe.rs:479–490, calendar.rs, and the schedule-only header contract; λ/τ citations traced to budget-1e9.md.

**Adversarial arms (one beyond the author's range, one beyond the regime):**
- **N = 10⁵** (next decade): holds — `ship_ticks` = `waiting` = 1.000×N, locals 311–333/105–108 absolute.
- **2.5 belt steps** (vs the author's ~1): no drain, `prunable` stays ~105 absolute — P5's failure is robust.
- **rtf 10⁵ wave arm** (the burn-shaped regime left unflown): `waiting` oscillates 0.04–0.98×N and `queue` reaches 9,642 — so "waiting ≈ N" is coast-regime and the author's "queue stays small" caveat is wrong. But the load-bearing facts are regime-invariant: `ship_ticks` = 1.001×N always, queue+waiting ≈ N in every census, so the 72 B/body content and 156 B/body capacity stand everywhere.

**Novelty confirmed:** no row anywhere in the record prices the five-calendar apparatus (6a0e priced one container; 25ce designed the deletion; the ledger's wired row is store-only). P4/P5 reported as failures against the author's interest — genuine pre-registration despite an empty run.log.

**Why gold:** reproduced, predictions held where claimed and failed honestly, and it shows a premise of the central 10⁹ ledger is wrong — the "wired 0.2–2.0×" memory closure silently assumes a calendar deletion no row names; the missing term alone is ~20× the machine. Adoptable in one step: correct the ledger, then the ×573 sizing flip (which I corrected: slots are body ids with no growth path — it needs dense live ids at promotion, not capacity policy alone) or 25ce's cursors.
