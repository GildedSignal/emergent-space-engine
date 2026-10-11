Working...
Check complete. `check.md` written to the run folder; nothing else there touched; no processes left running.

## Verdict: silver

**What I reproduced independently** (shipped code, fresh hash-salted angles, same seeded a₀/e₀, in `/tmp/check8269`):
- **Controls**: C1 quiet ring — 0/256 hits at 3×10⁻⁴ (author: 0/256), λ floor 1.48×10⁻³ vs 1.56×10⁻³, end-deviation 8.9×10⁻⁶ vs 7.6×10⁻⁶ AU. C2 planted 3:1 chaos — 97.3% vs 98.4% at 10⁻³, end median 1.52×10⁻³ vs 1.55×10⁻³ AU, λ ratio 1.66 vs 1.65 (confirming the λ instrument's disclosed resolution limit).
- **Belt scene** (full R1f rerun): hit fractions 30.1/18.0/11.9% vs 28.2/18.0/12.1%; diffusing classifier 11.9% vs 12.2%; quiet median 5.6×10⁻⁶ vs 4.8×10⁻⁶ AU; 2:1 edge 78% vs 82%. R1 itself couldn't be re-run (a sibling job killed my processes mid-flight), but its saved `bodies_R1.npy`/`metrics.json` verify every R1-specific claim including localization.

**Why not gold** — the record, not the physics:
1. **The steady flux is one event, not "4 events; Poisson ±50%."** The author's own metrics show one body (a₀=3.073) crossing four quanta — one walker, ±100% (95% upper ≈2×10⁻³), so the 7.7×10⁵× headline could be ~1.4×10⁵×. Order of magnitude survives; the stated precision doesn't.
2. **The e-channel "exactly zero late flux" is first-crossing saturation**, not evidence crossings stop — at q_e=10⁻² (never computed by the author) my rerun shows 43/512 late crossings.
3. **The C2 classifier calibration "255/256" is the ever-crossed rate, not the end-deviation classifier as defined** (mine: 222/256 = 86.7%).
4. Headline numbers (12.2%, 4.8×10⁻⁶, 87.8% e-channel) regenerate only by rerunning — raws deleted, ad-hoc analysis unshipped, hash-salted angles prevent bit reproduction — the exact failure mode that capped silvers on 5 October.

**One experiment to gold**: same instrument at T=2×10⁴ (or N=8192) for ≥10 late walkers, with the full analysis committed so every dossier number regenerates, plus a re-crossing-aware e-channel metric. The adoptable policy (write scars on filtered-quantum crossing, not on kicks) stands and feeds b-belt-wire/B18.
