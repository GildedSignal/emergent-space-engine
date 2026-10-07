Working...
Check complete. `lab/results/20261007-1550-constraint-578e/check.md` written; tree restored to clean main; patch reverted after reproduction.

**Grade: silver.**

**What I did:**
- **Reproduced** every dossier command in a clean tree with the patch applied: shares match within points (gather 66.6–70.6% vs author's 67.9–72.0; engine 19.5–20.5%); the members-400 bench produced a **bit-identical digest** (`aadaa1c8…` at cut 203025447) with late-run 25 µs/body at 1.05 readouts/body (author: 21 µs, 1.07); kick-bench matched exactly (60.3 µs rebind, 366.5 µs leavers, memo hit 0.0% both). Absolute frame times differ up to ~4× — shared-machine load, covered by the orders-of-magnitude rule.
- **Verified code claims**: `crossing` (view.rs:170) closes a bracket on the true interval — the guess affects cost, never the result; plane.md §7 names "a gather" verbatim; behave/plane.rs:78 answers `None` (vacuous gates confirmed).
- **Four adversarial cases**: seed 7 (robust), rtf 1 × members 400 (found the **fleet loop is a second unbudgeted O(members) walk** — 389 µs/frame — the dossier understates), 20 s × members 400 (steady churn ~226 live, story holds), and cross-machine digest identity (view is pure cost, decides nothing canonical).
- **Novelty**: the headline is partially known — H0210 already recorded "the view gather is 83% of a light frame" and H0211 landed the cache this run audits. New: the operating-point budgeted/uncapped asymmetry, the ~25 µs readout unit, and the measured 1.07-readout achievable contract.

**Why silver, not gold:** reproduced and honest, but no 10× moved, nothing deleted, no premise overturned — and the one quantified defect (2–3 readouts vs the cache's 1-readout contract) was diagnosed but not fixed, so the 2–3× gather gain is inferred, not measured; per-readout cost varied 2× across my runs. The named gold experiment: implement the 1-readout guess and A/B the gather at rtf 100 with the digest unchanged.
