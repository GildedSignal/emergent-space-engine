Working...
Check complete. Final state:

**Grade: gold** — written to `check.md`, first line exact, abstract ≤ 120 words, reasons, and "what the author missed."

**Verification performed:**
- **Reproduction (total):** my clean rerun of `regen.sh` — `bugdemo.out` md5-identical; `confirm2.out` identical on every measured digit (only the 4 disclosed elapsed-timer lines moved). My independent adversarial script reproduces the geom headline row (0.00279/0.00621) and be13's shipped PASS row exactly.
- **Provenance:** `galprogram.py` byte-identical to be13's shipped branch copy; `confirm.py.orig:21` carries bug 3 exactly as described (`hi = gal.R_MAX`); `bugdemo.py` regenerates the 148599-vs-221937 mismatch mechanically; C2's assert demonstrated live (counts matched at every grid in my run).
- **Predictions:** 7/8 held, two honest disclosed sub-misses (m ≤ 8, geom's finest point) — the signature of genuine pre-registration; instrument frozen before the first run (mtime order verified).
- **Adversarials (4, two outside the author's range — all strengthen, none breaks):** m ≤ 16/32 at the passing grid still fail p90 (1.3–1.8× bar, slow decay in m\* — full-azimuth clause confirmed to m\*=32); exterior r ∈ [5,11] essentially exact (~10⁻⁵ — covers the doll's r_a ≈ 11 orbits); COM's p99/max under the bar (0.00719/0.00879); same-budget 128×2048 fails both centring schemes (radial resolution binds; COM > geom at every shape).
- **Novelty:** real increment over the published page (which held the corrected numbers only as checker probes, not a regenerating record) — the 512×2048 order point, COM-clusters 128×512 pass, inner-disc p90 erased, m ≤ 8 dead, C1–C5 in-instrument.
- **Page:** faithful, Runs append-only (+1, 20→21, no deletions; the 41 deleted lines are the header + the allowed in-place rewrite of Open direction 5). I corrected two overstatements in place ("no m-truncation passes p90 **at any grid/anywhere**" scoped to the passing grid and extended with my m ≤ 16/32; exterior-probe fact folded in); a mis-landed hunk during my edit was caught and fully repaired — final diff verified clean.

Gold basis: the be13 checker's named experiment, executed on a regenerating record — three premises dead (COM-worse, inner-disc-fails, m-truncatable), adoptable within one step at zero cost, under P6/P19/P22/P33. Per lab rules, gold still needs a second blind checker before it stands.
