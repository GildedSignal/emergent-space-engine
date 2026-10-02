# Predictions — run 20261002-1618-components-6036 (lens: first principles, one component)

Component: the kick's **rebind** (`crates/universe` `step.rs::kick` → `bind` → `Rebinding::from_state`:
fit + `Orbit::compile` per kick). The law already specifies the shared memo (docs/law.md "Tube":
"the memo key's index (quantized E and L, 32 bits)"; "Cycle memo … It is shared by every tube
with the same key"); the build compiles a fresh exact-key trajectory per kick and the universe's
`Catalogue` never dedupes. So the build is behind its own law; the run measures the gap and the
memo's hit rate on a *dynamic kick sequence* (envelope.rs only measured static key populations).

Model: one body in a doll (M = c = 1), toy linear tide `a = diag(+w, −w)·x`, 64 kicks per radial
period (the law's step), dv quantized to the velocity word exactly as in all arms. Tuned case:
p = 100, e = 0.3, w = 1e-10. Held-out cases (not tuned on): strong tide w = 1e-8; eccentric
e = 0.6; near-circular e = 1e-3; weak field p = 1000; and a 32-ship formation (e spread 1e-6).

## Predictions (written before the decisive run)

1. **Cost split.** `Rebinding::from_state` on this cloud box is dominated by `Orbit::compile`:
   compile ≥ 50% of from_state (order tens of µs each). The fit-only remainder (fit_key +
   at_radius + residual) is the per-kick floor once compiles amortize.
2. **Hit rate (tuned case).** At key width (10, 10) (k bits, scale bits), a kick leaves its
   bucket with probability ≤ 1/16; distinct buckets visited per orbit ≤ 6 (vs 64 compiles today).
   At (12, 12) the changes grow roughly 4× (bucket 4× finer per axis).
3. **Held-out hit rates.** Strong tide w = 1e-8: hit rate at (10,10) falls below 0.5 but stays
   above 0.05 (graceful, no cliff); at (8,8) it recovers above 0.6. Near-circular e = 1e-3:
   within 2× of the tuned hit rate (k ≈ 1/2 makes the e-bucket absolute, not relative).
   Eccentric e = 0.6: hit rate lower than tuned by ≤ 4× (larger de near apoapsis… per kick at
   periapsis is where H in phase concentrates). Weak field p = 1000: hit rate not worse than
   tuned (bucket is relative; the tide's de scales out).
4. **Reuse cost.** The memo arm (fit + lookup + phase + residual, compile only on bucket change)
   costs ≤ 50% of from_state at (10,10) on the tuned case, and ≤ 25% on the formation
   (compiles shared across ships). Per-orbit compile count across a 32-ship formation at (10,10)
   ≤ 16 (≥ 128× amortization vs 32×64 today).
5. **Exactness control (must hold 100%).** Every memo rebind's `reconstruct()` equals its input
   `IntegerState` bit for bit: sharing a compiled trajectory cannot drift, the remainder absorbs
   the bucket offset exactly. Any failure KILLs the memo configuration, not the method.
6. **Behaviour.** Over one orbit at 64 kicks/orbit, the memo's position drift vs the exact-key
   law (r_memo) stays below the split's own grid error (r_split = |x@64 − x@512|/r): the
   coarsening adds less than one halving of the kick cadence would. If it fails, the next
   experiment is the law's derivative fields (∂/∂E, ∂/∂L) in the memo, not wider keys.
7. **Idiot index.** from_state / (fit-only floor) ≥ 5 on the tuned case at (10,10) — the gap the
   memo closes; the residual non-compile cost of a kick (readout, tide, sigma-delta) is outside
   this probe's scope (Sol already cut it 8%).

Cloud caveat: Linux/x86 shared 2 vCPU; orders of magnitude only; the integrator re-measures on
the M1 (the plane's own kick bench says 29 µs median there, 15 µs in fit+compile).
