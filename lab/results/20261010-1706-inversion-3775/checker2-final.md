Working...
Check complete. `check2.md` written — **Grade: silver**.

**What I did** (30-min budget, all processes <130 MB):

1. **Reproduced**: ran `breakup.py` in a /tmp copy (the script overwrites `results.json` beside itself) — every measurement key bit-identical to the author's, 11.2 s. Empty `work/patch.diff`, so no tree edits to apply. Prediction timing consistent (predictions.md 17:18 < breakup.py 17:29 < results.json 17:32; `run.log` is empty, so mtime is the only order evidence).

2. **Attacked** (4 independent cases):
   - **σ sweep to 50×**: null-plane retention exactly 1.0, residual 3.3e-16, phase-cert miss 86% at σ=0.05 — the core theorem is dispersion-robust.
   - **Brute-force Kepler truth** (the decisive hit): at the author's exact parameters the at-P∪at-Q machinery sees only 23 of 44 close pairs (age 4) and 4 of 8 (age 256). Diagnosed mechanism: near-tangent pairs with conjunctions 2.5e-3 rad off the crossing point, v_eff ≈ v0 — invisible to any focus-stream epoch window. Over the full truth the phase certificate misses 6/72 = 8.3% at N=150, not 46%; the lingering-companion channel (64/72 events) is what phase-adjacency catches and the machinery can't see. The "epoch-stream covers the main stream exactly / 0 misses" claim is falsified; P7 validated precision, never recall.
   - **θ_Q structure**: genuinely bimodal (0/π, resultant 0.34) but ~0.5 rad wide — 3 orders too broad for a b=1e-4 certificate, so "no shared structure at Q" survives; the author's open parenthetical closes.
   - **Cadence**: 8 sorts/orbit drops the miss to 0.3% at N=4000 — churn mechanism confirmed.

3. **Novelty**: no breakup/null-plane/epoch-stream prior art anywhere in `docs/` or `lab/` outside this run.

**Why silver, not gold**: the exact core (null plane, 100% cone retention, churn, trigger blindness, gold re-routed before `b-coorbital-cert` ships dead) survives everything and is theorem-backed — but the headline miss fraction is inflated by an incomplete truth and the proposed repair's zero-miss claim failed my independent truth at the author's own parameters. One experiment away: rebuild the truth with the near-tangent channel and respecify the fix as focus streams + phase adjacency for near-tangents.
