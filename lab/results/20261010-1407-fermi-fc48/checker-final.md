Working...
Check complete. `lab/results/20261010-1407-fermi-fc48/check.md` written — **Grade: silver.**

**What reproduced (grounded):**
- `hlive.py` full run, same seed: bit-identical to the shipped `hlive.json` (fields 126.4/128.6/149.3, slope 2.95, σ_e 0.0189, 874 kicks/body); `floor.py` gives 75.5/76.1 bits/body on both the shipped and regenerated state.
- `predictions.md` mtime precedes the run outputs by 6–7 min; pre-registered with a kill criterion; the dossier reports misses honestly.
- Spec provenance verified: law.md lines 12–13, `belt.rs`, B18's bar, H0190's 0.3–32 band, the HANDOFF "H_live … not measured yet" risk line. Novel: components-98bc measured the *smooth* belt only.

**What broke (my attack):** the 10⁹ headline. The sorted floor carries a −log₂N term in the author's own `floor.py`; measured across N = 4096/2¹⁶/2²⁰ the per-body floor drops exactly as log₂ predicts, so at 10⁹ it is **61.6–62.2 bits/body = 7.7–7.8 GB — under** the 8 GB budget, not 9.4–9.5 GB over. The dossier extrapolated the N=65536 number directly. Scars (126 bits/body = 15.8 GB, ~2× over) keep the requantization/t_p-anchoring conclusion alive, but "no exact encoding at the tube's own quanta fits 8 GB" is false as stated — hence silver, one line of arithmetic from gold.

Secondary findings recorded: the claim's "107 bits/body" matches no shipped number; `hlive.json`'s stored floor (65.5) is the capacity-capped estimate `floor.py` silently supersedes; the T=2 quick path crashes after printing rows; seed 777 reproduces everything (ensemble statistics, genuinely robust).
