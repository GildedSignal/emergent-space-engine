Working...
Check complete: **Grade: silver.**

**What I reproduced** (clean tree, `git apply work/patch.diff`, both binaries built):

| Case | Author | My box | Digest |
|---|---|---|---|
| Tuning n=200k | 771→542 (1.42×) | 772.9→580.3 (1.33×) | identical, base==fast |
| 8 held-out | 1.07–2.12× | 1.30–1.58× | all 8 stored digests match exactly |
| `lattice-check` / `-rel` | 3/3, 4/4 | 3/3, 8/8 EQUAL | with patch applied |

**Adversarial (4 of mine):** fill 0.01 → **1.92×**, fill 0.4 → 1.32×, n=5000/h=512/0.3/512/seed-99 (long-horizon `consumed`-retain path) → 1.40×, dense relv1 → 1.39×. Digests equal in all. The digest-invariance argument holds structurally: `pairs` is duplicate-free (`i >= j` guard) and canonically re-sorted; `local`/`consumed` are get/insert/retain; `predicates` is order-independent — any exact hasher preserves outputs.

**Findings against the author:** held-out horizon (16) missing from the dossier — I recovered it from the digests; "the tree carries it" was false at check time; the dilution wrongness-model is inverted (gain grows at fill 0.01); the P4 relv1 "dilution" (1.07×) didn't reproduce (1.46× on mine) — load noise, not mechanism. Novelty confirmed: no hasher work in HISTORY.md or chronon.rs history.

**Silver, not gold:** real and adoptable in one step (~60 lines, no dependency, law unchanged), but a capped 1.4× — two orders short of a 10× board move, no component deleted, no premise killed. The author self-assessed the same. The honest gold path (per-body reach tiers / event-sorted frontier, the 77% cache-miss pair loop) is named in predictions.md and belongs to the next run.

Tree left clean (patch reverted); only `check.md` written to the run folder; no commits or pushes.
