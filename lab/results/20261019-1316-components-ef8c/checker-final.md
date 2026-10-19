Working...
Check complete. `Grade: silver`, written to `lab/results/20261019-1316-components-ef8c/check.md`; tree restored to main-verbatim; one correction applied to the author's wiki page header.

**Evidence summary:**

- **Reproduced bit-identically**: applied `work/patch.diff`, ran `regen.sh` — all 5 arms match the stored grid exactly (float tails included), 12.3 s wall, 230 MB peak.
- **Mechanism verified in shipped main, not just the patch**: `orbit.rs:114` (`k = 2⁹⁶/(2⁴⁸+e)`), `orbit.rs:960-965` (weak `shape_bits` drops periapsis), `Knot` = 8 + 5×16 = exactly 88 B, and the 644 B/body baseline is real shipped code (`universe.rs:346` compiles one `Orbit` per body; `QuantizedMemo` is wired nowhere in the flight crate) — not a strawman.
- **Adversarial arms beyond the author's range**: seed 11 at 10⁵ (1,743 cells, 47.9×, knot 0.87%, max ΔP 4.8e-4) and seed 1 at 10⁷ (2,141 cells — log growth continues, 3,369× deletion, knot 0.83%, mean ΔP 1.198e-4 identical across four decades). Every claim holds; the 10⁹ projection stays consistent.
- **Novelty**: the cell-rebind page named exactly this measurement as "(unmeasured)"; view.md's "peaks at 37" is confirmed a coarser 2⁻³ grouping; nothing in HISTORY.md; all cited runs exist on their branches.
- **Why silver, not gold**: two pre-registered predictions failed as written (P6's kill criterion at 10⁵, P8's zero), the census is birth-only (kicked-key same-cell recurrence unmeasured), and only the census half of 9eeb's named gold rung ("gates + belt census + 0355 pricing") is flown. The one gold experiment: the `Rebinding::from_state` key dumps across a belt kick wave, with the knot guard flown.
- The knot finding (B9's invariance does not transfer, 0.80–0.87% constant across 4 seeds and 4 decades) is the run's genuine premise refutation and is correctly priced in the page.
