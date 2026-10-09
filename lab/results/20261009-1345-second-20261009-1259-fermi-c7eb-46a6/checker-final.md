Working...
Check complete. **Grade: gold** — written to `lab/results/20261009-1345-second-20261009-1259-fermi-c7eb-46a6/check.md`, nothing else in the folder touched, no git operations.

**What I did and found:**

**Reproduction (all pass):**
- Shipped `verify a|b|d` rerun: physics fields identical to the prior record (only timing fields differ); `verify c` truth counts 3034/2093/1496 match the dumper exactly.
- `enc-dump c` rerun: byte-identical dumps (deterministic).
- `validate.py` (65 s) and `ledger.py` incl. the 22-s walk: outputs identical to the author's saved files.
- Timeline: `predictions.md` (13:55:58) precedes every decisive artifact (first dump 13:56:14, RK4 14:18, walk 14:21).

**Adversarial attacks (all survive):**
1. Closest-approach geometry re-derived from raw dumped states with my own leapfrog: |r_j−r_i| = d to 1.6×10⁻⁸, d·v_rel = 0 to 4×10⁻⁸.
2. Independent leapfrog 3-body at my own mass choice (1-km rock) across 6 belts: meas/impulse median 1.003 where my control is clean; co-orbital degrades to 1.29 as disclosed.
3. Walk re-run with fresh seeds: still 0/1000 period-tick crossings for 50-m rocks; robust even at 4× the encounter rate, max accumulated offset 0.216 ticks (≈5× headroom).
4. The borderline-Lévy claim verified: var(x) grows ×1.8 over N=10³→10⁶ (log-slope 0.09 ≈ 1/ln N), justifying quoting walk bounds over the Gaussian 4.7×10⁶-orbit figure.
5. All headline arithmetic recomputed: 16.5× threshold revision, 97× co-orbital drop, 14.9 GiB, 1.9×10⁷ ticks/pixel.

**Noted blemishes (recorded in check.md):** V3 labelled "held" though the control floor is 0.19× the signal, not the promised 10⁻³; the 3-D rate never calibrated against the crate's own planar rate; the i.i.d. walk ignores signed conjunction bunching; one belt label loose ("hot" vs mixed). None threatens the headline claims; gold stands per the two-finder rule pending the second blind checker.
