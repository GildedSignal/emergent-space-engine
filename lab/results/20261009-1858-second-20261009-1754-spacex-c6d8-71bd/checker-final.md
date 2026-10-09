Working...
Check complete. `check.md` written: **Grade: silver.**

**What I did (45-min budget, ~28 min used):**
- Applied `work/patch.diff` in a clean tree, built, reproduced everything: all four plane digests (`83d96bed…`, `e56d1c12…`, `e3eb62e6…`, `6ddafe96…`) regenerate exactly; the decisive belt JSON is byte-identical (13.2 s wall); `--kick-bench` runs again.
- Ran my own adversarial belts: 0.15–0.25 AU (inside Cinder) → cadence 3.547e-5, debt 174.9; 8–12 AU (beyond Giant) → 3.311e-5, debt 177.8; cause dv ≡ 0 and EMA-reabsorption negative in every scene. The radius-invariance and debt stability hold over a ~200× orbital-period range.
- Verified the mechanism in source (`ext.rs:26`, `ext::constants`: doll-wide clock from the shortest secondary, power-of-two grid) and that law.md line 13 really specifies "+62 bits per kick and −60 per reabsorption" — the claim kills a live spec line.
- Novelty: no prior H_live measurement anywhere (HANDOFF: "not measured yet"); components-98bc's static-program floor is a different question.

**Why silver, not gold:** the physics reproduces and survives adversarial extremes, but the held-out apparatus is weaker than presented — `belt-smoke.json` (disclosed as pre-predictions) already contained **both** headline numbers (debt 175.1, cadence 3.56e-5), and the disclosure names only the cadence as available; the verdict rule was determinable before the brackets were written. Gold-making experiment named: the cause-journal twin (~2 bits/binding) with bit-identical replay on read.

Tree left clean (patch reverted); nothing else in the run folder touched; no git commit/push.
