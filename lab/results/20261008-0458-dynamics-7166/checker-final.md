Working...
Check complete. Tree restored; only `check.md` added to the run folder.

**Grade: lead** — `lab/results/20261008-0458-dynamics-7166/check.md`

**Reproduction:** all dossier numbers reproduce bit-for-bit (gas 13 rows, battle 4 rows, controls, EventCore≡Chronon identity); the author's `fleets()` is a faithful copy of the engine's stock scene.

**Why lead, not silver:** the author's two named-but-unrun falsifiers kill the headline claim:
- **Grid-free gas at matched density** (same box/radius/speeds/walls, rejection-sampled placement): Fano **0.93** flat at n=4096/16384 vs 6.44/30.53 on the grid — the gas growth is the generator's zero-jitter crystal start (`worlds::gas` cell quantization), not dynamics.
- **Battle window split** at n=25,600: all-window Fano 40.2 reproduces, but first half = 30.5 and **second half = 3.2** (1.6/1.2 at smaller N — post-front Poisson at every scale); 4× velocity scatter drops it to 7.7. It's the synchronized crossing transient inside a nonstationary window, not a growing steady-state tail.
- The allocator's own quantities stay thin: ops p99/p50 ≤ 2.79, max/p50 *shrinks* with N (29→13). No missing gate.

**Also flagged:** the energy claims (E/E0 flat, exact equal-mass cradles to 10⁶ ticks) verify qualitatively under my throwaway but are regenerable by no shipped code — the exact record-keeping failure the 5 October taste log names.

**What's kept:** a control-solid instrument, the premise confirmation the author themselves priced in ("Poisson-smooth everywhere reachable"), and two documented instrument traps (cumulative-delta bug, gas genesis degeneracy). One surviving kernel for a future run: `max_batch` grows ≈ N^0.75 and survives de-synchronization — the connected-component probe (pairs vs indivisible clusters) was never run.
