Working...
Check complete. `check2.md` written to the run folder — nothing else in `lab/results/<run>/` touched (scratch in `/tmp/chk2`, builds in the shared `lab-target-0`).

## Verdict: **gold**

**Reproduced** (clean tree, `patch.diff` empty — no crate edits):
- `ledger.py`, `ledger2.py` → bit-identical; `plane` → 2349 B/body, 28 bodies, exact
- `verify a` → all counts identical (truth encounters 35/68/189/248; rates 1.75e-4 → 4.96e-3 /body/orbit)
- `livebelt` row 1 → **bit-identical** (270 crossings, 2198 kicks), rebuilt from source
- `kick` → count-identical; SI arithmetic (209.3 MB/game, 31.0 writes/s, 18.2 KB, 32× = 6.02×5.29) re-derived by hand

**Predictions**: written 09:45:45, before every decisive run; the Part B predictions that carry the refutation all held; two Part-A band misses disclosed with correct diagnosis.

**Five attacks, all inside the claimed bands**: seed 777 (ratio 1.14), σ_e = 3e-2 (rate flat while v_rel tripled — the no-Coulomb-log premise measured), q = 1e-5 (∝1/q, kicks/crossing → 1.04), N = 8000 (exponent 1.13, no super-linear term), m = 10¹⁹ re-run (ratio 1.38). Premise verified in code: `make_belt` is planar, so the refuted ≤ 1 MB/game claim fails by ~200× in the only geometry the engine ships.

**Named defects** (in check2.md): the dossier's "16.5–19.6 ms per recertification" contradicts its own `kick.json` (7.2–7.5 ms; my rerun 11.6–13.4) — the recert-compute conclusion survives at 0.2–0.4 CPU-s/s; and the unreported `word_writes` run 8–11× crossings, making 209 MB a lower bound while shrinking the 3-D margin to ~5×.
