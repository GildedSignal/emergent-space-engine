Working...
Check complete. **Verdict: silver**, written to `lab/results/20261011-0324-fermi-c211/check.md` (nothing else in the run folder touched; scratch work in /tmp removed).

**What I did:**
- **Reproduced exactly**: clean rebuild of `emergent-shipmem` (14 s), `reproduce.sh` (24 s) — every deterministic field bit-identical (populations, bits, codecs, scar counts, inferred flags, 0 mismatches, checksums); `budget.py` output equal except three machine-timing fields. Empty `patch.diff` is consistent: shipped code only.
- **Predictions audit**: `predictions.md` (03:30:51Z) predates all stored data (03:37:43–53Z). Structure held; P1 calibration and P3 (the declared held-out physics) failed and were honestly disclosed.
- **Four adversarial cases of my own**, all of which *confirmed* the core claims: 10 kicks/member saturates at one 61–65-bit scar per member-ever-kicked (the admission rule's load-bearing assumption); intermediate fractions f=0.05/0.2/0.5 match `1+61f` within 8% (conservative); scar cost scale-stable m=1024–16384; high-f rungs saturate the same way.
- **Novelty**: first measured H_live ledger, admission curve, and 190-core re-derivation (no prior entry in HISTORY/docs); feeds the queued `b-h-live` and B18b.

**Why silver, not gold:** (a) P3 failed — the same bar that held the 1 October red-team at silver; (b) the headline "re-derives to **0.5%**" regenerates from no table row — it's exactly 1/191 (dividing by the 191 cores instead of 8/191); the true sustainable fractions at that corner are 4.2–4.5% or 0.04%. Plus minor table slips (convoy max 19 µs not ≤13; rand 251–650 not 230–650; seal spans 100–128 ns).

**The one experiment to gold:** sweep kick magnitude up to family-jumping element changes — the 61-bit scar constant rests on one hardcoded delta — and restate the 0.5% from the table.
