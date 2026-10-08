Working...
Check complete — `lab/results/20261008-2031-fermi-9d49/check.md` written, nothing else touched.

**Grade: gold.**

What I did:
- **Reproduced in a clean tree** (patch.diff is empty — everything runs on shipped code): all six `measure` runs identical to the author's numbers — bits/body 17.29/29.60/196.62/149.73, floors 13.73/19.92/189.51/145.51, kick deltas +14.13/+15.33, matching checksums, `roundtrip_mismatches: 0`; `fermi_hlive.py` output byte-identical.
- **Predictions verified pre-registered** (mtime 20:36:55 before the 20:37:11 measurements); the two misses (formation width, the 3D→2D contact flip) are honestly held — and the flip is correct for a 2D game with the frozen B18b geometry (8.4×10⁶ = 2²³).
- **Adversarial:** measured the author's one unmeasured inference myself — re-kicks are bounded and *cheaper* with multiplicity (per-kicked 78 → 64.5 → 62.3 bits at 1.0/1.33/1.58 kicks each); widths stable at 4×10⁶ bodies and bsize 64; re-derived the promoter physics by hand (contacts: 71.6 yr turnover for 1-km rocks; b_cross 16 m ≪ 2 km so mutual gravity never promotes; embedded masses 8×10¹⁷ kg/Myr with v_rel cancelling; ceilings arithmetic exact; 4 GiB is the approved plan's open budget per HANDOFF:74).
- **Novelty/goal fit:** fills HANDOFF's "H_live not measured yet", kills representation.md §4's 12–16 bytes/individual (measured 18.7–24.6 bytes), and hands `b-h-live` exact counters (promotions/retirements, not the ~6×10⁴ kicks/s) — adoptable in one step, no engine change.

Misses named in the check: per-kicked arithmetic off by the 18.1% vs 20% distinct fraction (scarred ceiling 24.2% → ~21.9%), the census "rest" ignores the belt gold's 0.126-bit program (ceilings conservative, conclusion robust), resonance coverage is a linear ratio, and the runner's machine-state fields came back empty (nothing load-bearing rests on timings).
