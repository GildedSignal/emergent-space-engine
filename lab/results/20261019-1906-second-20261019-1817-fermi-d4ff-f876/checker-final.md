Working...
Check complete. **Grade: silver** — written to `check.md`, page corrected in place, no commits made.

**What I did**

*Reproduction.* Runner's `regen.sh` exit 0 (Γ 6.232, TP bar 423.8, contacts 0.414, +0.0040 cores — all inside the dossier's bands). My bit-exact rerun of one regen config matches field-for-field. Genesis port verified line-for-line against `crates/universe/src/scenario.rs` (`draw`/`mix64`, `rayleigh_q48` with the lane-16 redraw, a∈[2,3) AU at 2⁻⁸, p=a(1−e), r=34·2⁻¹⁰, D_ENC=2¹⁰·2r=68 root). One recorded mismatch: the dossier's 10⁵ point (116 events, Γ 6.19) is not the regen line's config (94, 6.267) — "all numbers regenerate" is loose for that one config.

*Attacks — five, all landing on the author's side:*
- **The disputed reach with weight**: d=10⁵, T=10⁵ → 596 events, Γ=**6.274** (author had 94 events on 3 transitions) — refutes d4ff's checker 27.75 as a pair-event rate by 4.4×.
- **Outside the author's range**: d=2×10⁵ → 2,264 events, Γ=**5.96**, falling per root — the d4ff rising table (40.3/48.8) cannot be pair events at any reach.
- **Third counter** (scipy cKDTree, own debounce, new seed): **5.65** at 3×10⁴.
- **N² rescale** (load-bearing for 10⁹): M=2×10⁵ at quarter T → **6.02**.
- **Sampling-cap bias**: vmax 30 km/s → **6.098** vs 6.103; the ≈2% claim is conservative.

*Why silver, not gold:* the headline "measured at the reaches the ledger prices" overstates — 68 root and 0.0664 root are carried by kinetic flatness from 10⁴, and the run's own MC rises below 10⁴ in both cuts (safe 6.3→10.8, full 8.9→13.8); P2's kill criterion fired exactly there, and the adopted band [5.4, 7.0] excludes those bookends. Every ledger conclusion survives a 2× rise, but the priced-reach constant is extrapolated. Gold experiment: a propagation bridge at 3×10³→3×10² root (my 3×10³ probe ran ~9 min before my timeout killed it — the rung costs minutes, not the 10⁴× the author claimed). I corrected the page on precisely this point and added my confirmations to the Refuted entry.
