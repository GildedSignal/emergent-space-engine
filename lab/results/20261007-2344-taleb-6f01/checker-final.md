Working...
Check complete. **Grade: gold** — written to `lab/results/20261007-2344-taleb-6f01/check.md`; nothing else in the run folder touched, all reproduction ran from an isolated copy in `/tmp/taleb-check`.

**Verdict basis:**

- **Reproduced bit-identically:** pilot, wscan 10/10 cases, escan 6/6 cases (including `binet_radius` to the last digit; only wall-times differ on the shared machine).
- **Predictions:** `predictions.md` timestamps precede every result JSON. Fresh-seed runs held within the promised ±5 pp; the k-formula holds at k=2 and is loose-but-conservative at k=8; the author's two self-reported failures are honest and correctly diagnosed.
- **Adversarial findings:**
  1. **Gate margin (my main addition):** at dvec=1e-4, N=600, the full gate S=2.72 < k=4 passes while the λ tier still drops 3.2% of contacting pairs (1.7% at N=300) — the leak grows with N inside the gate's "safe" band. The gate separates catastrophic from clean but needs a margin for a zero-miss contract.
  2. **Instrument defect, contained:** `candidate_pairs` keys pairs by λ-order orientation (430/845 keys i>j), voiding the brute cross-check fields and inflating `contact_pairs` ~2× (241 vs 125 distinct). I recomputed with normalized keys: brute agrees 4/4 on a 2000-pair subsample (truth list sound), and unweighted miss fractions shift ≤1 pp — the dossier's headline percentages stand.
  3. k=2 on the wscan family shows λ-leak (3.5%) once drift-rank approaches k, consistent with the scaling law.
- **Novelty & fit:** no prior entry bounds the gold's domain; `b-coorbital-cert` is first in `lab/queue.txt`, so the gate lands before the build ships — a premise correction on an adopted design, adoptable in one step (gold criterion: shows a premise is wrong).
