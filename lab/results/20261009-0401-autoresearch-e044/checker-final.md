Working...
Check complete. Verdict: **silver**, written to `lab/results/20261009-0401-autoresearch-e044/check.md`; tree restored to HEAD, scratch removed, nothing else in the run folder touched.

**What reproduced:**
- **Exactness, the core claim.** Digests identical baseline vs patched on both author banks (`11806c4030d5dd5f` tune, `f8c456a28a52db9a` heldout) and on my own 350-case adversarial bank (branch cut at ±1 significand quantum, dense k sweeps at exponents 0–44, near-UNIT, strong field, fresh RNG): digest, knot totals, and — a check the author's harness lacks — the error set (`Err` compiles are skipped by their fingerprint) all match.
- **The small win.** Patched faster everywhere: tune −9.0%, heldout −5.2% median under load 3.7 (author: −3.0%/−3.6%). Single-digit percent, matching their negative conclusion; nothing near the predicted 25%.
- **50/50 crate tests** on the patched tree; **756-knot near-separatrix corner at 1.03 ms** (claimed 1.0–1.24 ms).
- **Pre-registration is genuine**: predictions.md at 04:09 vs log at 04:21, and P1's falsification (≥25% predicted, 3% measured) is not what post-hoc predictions look like.

**What did not reproduce — why silver, not gold:**
- The cos attribution ("~33% of per-knot, 842→567 ns") is ~2× overstated. Direct microbench: 40.7 ns/call × 3.99 calls/knot (instrumented count) ≈ 18% of the 879 ns/knot; like-for-like ablation gives −8.6%/knot on totals. Their log records no ablated knot totals, so the 567 derivation isn't inspectable — the ablation shifts knot counts and conflates ladder redistribution with node cost. Direction survives (serial chain, no bit-identical scalar lever); the number doesn't.
- The "~1 ms corner" is actually a broad class (0.70–0.88 ms across many near-separatrix keys) — which strengthens their point but was never tied to real rebind frequency in the plane.

**The gold-making experiment named in check.md:** count near-separatrix rebinds and their total ms in the plane's B13 flyby population — if frequent, a certified-cheap rebind is the actual 10× lever this run's lens admits it cannot see.
