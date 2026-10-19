Working...
Check complete. `check.md` written: **Grade: gold**, with one correction folded into the page.

**What I verified:**
- **Reproduction**: applied `work/patch.diff` myself, ran `regen.sh` (exit 0, 17 s) — all six outputs bit-identical to the author's, and book/smallh/dv0/777-stream bit-identical to e828's committed outputs on its own branch. The harness is e828's verbatim.
- **Quotes at source**: 1a29's 355-constants, 1176's E_cell/3.5×10⁻⁴/7.2×10⁻⁹/140×-under, the ledger's 10.8–16.6/2.8–5.5/363-cores, view.rs:23, kepler.rs's 2³² clock, and the ~27.4k game-s doll step — all exact.
- **The decisive arithmetic, independently**: equilibrated Monte Carlo of the per-pair epoch counter lands on (n−1)/E_pair at every size (3.063/12.437/0.766 vs 3.062/12.438/0.766); 1176's (n/2)·E_pair divisor is refuted 25–100×. Row at their own dial = 0.35 cores; the 363-core arm is dead by measurement.
- **Adversarial**: 512×κ at P=1 (leak *falls* 8× — quantum is conservative) and fresh seed 31337 at the quantum (P=1 = 7.2×10⁻⁶, same order — the composition column is seed-robust). Both beyond the author's grid, both pass.
- **Predictions**: written 15:59, before every output; the disclosed fix phase moved no number. P2–P5 held fully.

**The one thing the author got wrong** (checker correction, page edited in place): the coupling constant r = 5×10⁻⁶ "cross-checked" — the cross-check divides game ticks by replica ticks, drops kepler's TAU (2π×), and cites a = 2.5 where the harness belt is a ∈ [2.0, 2.0001]; it reproduced e828's number through the same formula (agreement, not independence — PRINCIPLES 31, the one the dossier itself quotes). Clock-consistent r ≈ 7×10⁻⁹–2.6×10⁻⁸ per kick interval. Conservative in every downstream use, so the adjudication, the leak certification and the 0.35–1.4-core row stand a fortiori — 1176's P=4 is ~10⁸–10⁹× off, not 7.9×10⁵×. Gold stands on the divisor/ledger substance, not on r's value.
