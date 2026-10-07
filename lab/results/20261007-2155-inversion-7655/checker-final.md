Working...
Check complete. Verdict written to `lab/results/20261007-2155-inversion-7655/check.md` — the only file I touched; all my runs lived in `/tmp/check7655`.

**Grade: gold.**

**What held:**
- **Reproduction, bit-for-bit:** all 6 main scenes via the committed script; the 3 robustness scenes (not driven by its `__main__`) by reconstructed `run_scene` calls — every field identical, including the load-bearing r_max 4/8/10/18 and miss fractions 0/0.33%/2.8%/13.2%.
- **Pre-registration genuine:** predictions.md (21:59:44) predates the probe script (22:00:37) and results (22:01:06). P1/P2/P3/P6/P7 held; P4/P5 failed only on fraction magnitude, disclosed, same direction, rank components held.
- **My attacks strengthened it:** true Π=16 gives r_max=36 — exactly the measured law 2Π+4, so it extrapolates; a local jam inside a mean-Π=0.6 scene misses 6.5% of jam encounters (mean-based triggers fail, confirming the tube-count fix); rank ≤ tube-count−1 verified structurally and empirically everywhere; vertical thickness halves the miss but k=4 still dies; the flagship Fermi arithmetic checks (1° arc → Π≈5,730).
- **Adoption cost as claimed:** nothing on main depends on `crates/encounters`.

**The one substantive flaw (in "what the author missed"):** "a function of Π alone" is family-conditional. At fixed Π=4, 10ρ of radial breathing collapses r_max from 10 to 2 with zero misses — the binding invariant is the 3D tube count, not 1D packing. The gold's own phalanx family at peak packing 3.2 never filled the tube (r_max=2), which explains rather than contradicts its evidence. The adopted fix (watch width = tube count) is precisely the right invariant; only the headline law and the unconditioned flagship Fermi needed the radial-coherence caveat. The kill itself — k=4 universal is dead at tube occupancy > 4, and the game's flagship scene sits 3 orders of magnitude beyond it — survived every attack I mounted.
