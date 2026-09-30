Working...
Check complete. Both deliverables are in the run folder; nothing else in `lab/results/…59e4/` was touched, and no git commands were run.

**Verdict (via `lab/verdict.py` on my metrics-check.json + author's):** `KILL; killed: element-sort, shear-grid, hier-bounds` — oracle passes all four criteria, ring-cells fails as required, so the rung adjudicates cleanly. My metrics are identical to the author's, so there are no disputed outcomes.

**What I did and found:**

1. **Reproduction — exact.** Clean tree, author's scripts unmodified: the 16-belt rerun is field-identical to `belts.json` (every truth/cand/conj/events/detected/hier-parts value); scaling exact runs (N=1e3/1e4/1e5) and all closed forms are bit-identical; `metrics.json` re-derives exactly from the raw JSONs. The only unreproducible number is the N=1e6 truth: the *saved* `run_scaling.py` computes 166.0 by a k·N²ρ²T law and emits no `orbits` fields (making `make_metrics.py` crash); the method actually used is documented only in the dossier/JSON, and re-implemented it reproduces 9797.58140676931 exactly. Reported, not fixed.

2. **Implementation checks.** Belt 0 pinned by independent regeneration (candidates 1,679,962, conjunctions 139,273 exact). Accounting is favourable-to-config throughout (element-sort undercounts real swaps; shear-grid credits any cell change; hier-bounds overcharges nothing but *pays bogus renewals* for statically-disjoint envelopes — its belt-0 floor alone is still ≥1.9e4 work/enc), so all kills hold a fortiori. Oracle values verified individually.

3. **Adversarial attacks — the truth itself leaks.** On belt 0 my independent solver finds 451 encounters vs the author's 427 (all 427 ⊂ 451): 2 certain misses are deep dips (0.28ρ, 0.40ρ) confirmed with the author's own `kepler_states` — wrong-basin Newton in slow wide windows — plus ~25/429 borderline at d/ρ ∈ [0.9,1.1]. Structurally, pairs with |dn|T < 2π and no conjunction are never enumerated (a hole the rung's own truth spec shares): an adversarial narrow-a belt shows **78% of encounters missed**. None of this flips a criterion; it's all in `check.md` under "what the author missed" with fixes.

`check.md` holds the ≤120-word abstract, the reasons with numbers, and the author's blind spots.
