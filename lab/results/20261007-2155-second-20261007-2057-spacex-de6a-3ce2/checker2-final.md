Working...
**Grade: gold** — written to `check2.md`.

**Reproduction (clean tree, patch applied via `git apply`):**
- All 7 digests bit-exact; additionally verified against the **pristine tree** (no patch): seed 1 gives the same `29f440d6…`, so the instrumentation is provably read-only — the VOID criterion is dead.
- Every integer/scar field matches to 1e-6; tests 2+6+10 pass; all cross-checks hold (77/58/116 contacts = fleet counters, 310 epochs, 12 of 5,856 dk firings, carries 100% distinct, Δk ≤ 8 bits); all extrapolation arithmetic checks.
- Only divergence: entropy floats wobble in the last 1–2 ulps (HashMap order) — recorded as a nit on the "every digit reproduces" claim.

**Attack:** unseen seed 5 (widths hold: tide 74.63, contact 15.51 inside the pre-registered band), unseen horizon 3200 s (battle dead at ~1984 game-s, entropy frozen — transient confirmed), and 100 s (all 77 contacts already done; scene scar rate decays monotonically 1215→77 bits/s over 100→5000 s — "no single scene rate exists" is correct, and sharper than the author stated).

**Predictions:** P1/P3/P5/P6 held; P2's contact rate and P4's zero-delta epochs failed — both pre-registered, reported against the author, diagnosed, and the claim re-based on widths + H(T) + the fixed protocol. H0183 discipline.

**Gold rationale:** the dense order was the unmeasured 99.7% of the memory bottleneck's decision quantity; measured, it is 10.9× the sparse order's scar — an order-of-magnitude correction (57 GB/h now printed beside its 160 GB/h face), plus the first number for `b-h-live` (8 GB < 6×10⁵ member-game-hours). Novelty clean against HISTORY; adoption is a default-off +240-line recorder.

**Misses recorded:** float-entropy not process-stable; "per body touched" wording; the scene sum spans two representations (storage accounting, not an information bound); 100 s transient; ~6% tide-width drift.
