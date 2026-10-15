Working...
Check complete. Summary of what I did and found:

**Grade: gold** (`lab/results/20261015-0358-redteam-8144/check2.md`)

**Reproduction** — applied `work/patch.diff`, ran `regen.sh`: exit 0, output byte-identical to `out/passthrough.txt` (diff empty, twice). All headline numbers regenerated: 294/294 boundary arms, the game cases, both controls, the threshold table. Mechanism independently verified in code: `relativity.rs:236` and `law.rs:598` (identical skip gate in both laws), `chronon.rs:71/118-121` (detection admits full crossings; every detected pair logged + consumed regardless of exchange).

**Adversarial cases (3 outside the author's domain, via `crates/lattice/examples/checker2_probe.rs`):**
- **Oblique b≠0** (author tested b=0 only): 453 arms, effective-reach form **0 misses** — but the dossier's headline equivalence `d0 ≤ |w|` fails 47/453 (it's the longitudinal projection ≤ |w|; head-on-only phrasing).
- **Mass 1:65535** (author always 1000/1000; 2¹⁶ is the lattice cap) + **reach 100–1000× beyond the author's max** (up to |w| = 1.35×10⁶): boundary holds everywhere.
- **Reflecting-box eternity**: 0.9c pair, 3000 chronons — 334 contacts, **0 exchanges**, confirmed exactly by revision accounting (rev0+rev1 = 666 = wall count). The ghost survives re-encounters.

**Novelty** — exactly f50d's named open direction ("the geometric decomposition is open"), not a repeat. **Rung audit verified and stronger than claimed**: the "independent" reference `xtask/src/gas.rs:152` shares the gate, so even the Chronon↔gas cross-check is blind.

**Corrections recorded** (dossier prose only, no measured number touched): ×10³ unit slips (1.409 mm not m; "10 m–1 km" is 1 cm–1 m), |w| max is 9.4×10⁵ not 1.9×10⁶ (fixed on the wiki page), the phase-ladder "at each reach" is an idealization, negative-control ρ is 8.5×10⁻⁵. The author's wiki page was otherwise faithful; I corrected the one log-contradicted number and appended the checker note.
