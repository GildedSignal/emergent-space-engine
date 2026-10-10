Working...
Check complete. `check2.md` written — **Grade: silver**.

**What I did:**
- **Reproduced** the record in a clean tree: `python3 deferral.py out.json` → bit-exact (`cmp` clean), 12.2 s, ~60 MB. Every dossier number matches `deferral.json`.
- **Verified the clock bug** from the kept `deferral-orig.py`: `t` advances 1.5H per kick against the body's H; lead 0.5·1000·(2/5.2)^1.5 = 119.3 jovian rev/1000 orbits (dossier: 119.2); scene B's effective ratio 1.333 = 4:3, so the "2:1" retraction is correct. Prediction ordering holds by mtime (script 19:24:49 → predictions 19:25:07 → record 19:25:22).
- **Attacked** (3 fronts): 3000-orbit horizon; equal-q deferred-vs-quantcarry ladder sweep; scene-B ejection sweep (2 seeds × 9 quanta).
  - Kill strengthened: deferred walks at every q (exp 0.78–1.02); ejections recur at 32/40·dvr both seeds; ψ scrambled in all 18 cells.
  - Headline falsified as a general property: the "28–46× lower at equal q" separation is one ladder point — 8.2×/45.8×/4.7×/**0.4×** at 2/8/32/128·dv; at q ≫ per-kick dv quantcarry degenerates into quantized timing (the pathology it isolates), and grows late at 32·dv (second-half exp 2.89).
  - Prediction #4's letter fails a second untested point (48·dvr: pump 1.01, no ejection, both seeds).
- **Novelty/fit**: no HISTORY entry covers impulse deferral (the 6-Oct gold killed encounter-*setup* deferral, a different mechanism); quotes verified at `docs/archive/engine.md:51` and `law.md:29`.

Silver, not gold: the kill and the record are gold-quality and the two retractions are honest, but the claim sentence generalizes the instrument beyond what was measured, and one pre-registered, ~1-minute sweep (q-ladder × horizon, fold in the domain rule) makes it gold.
