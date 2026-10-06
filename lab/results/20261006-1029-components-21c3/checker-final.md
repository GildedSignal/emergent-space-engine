Working...
Check complete. **Grade: silver.**

**What I did:**
- **Reproduced exactly** in a scratch tree: both runs regenerate every stored value bit-identically (32.21/43.5 one-tier, 7.02/10.32 two-tier, 4,201 reabsorptions, occupancy 12.768→12.784, margin 1.04×10¹⁵); only the machine load triplet differs. The model faithfully mirrors shipped Form P in `crates/shipmem`.
- **Three adversarial cases:** (1) the author's own named killer — truncated kick tail — survives and *strengthens* the claim (growth stays log, crossing moves later, two-tier flat at 5.51); (2) λ=10 extreme — structure holds, crossing scales ~1/λ; (3) firewall sensitivity — margin stays ≥10⁹ even at a physically consistent ε (~3.7×10⁷ m, not 100 km) and μ×10³.
- **Novelty:** first numbers ever for plane.md's H_live metric and the board's "10⁹ in 8 GB" item (9–14× memory move); distinct from components-98bc's static birth program.

**Why silver, not gold:** two held-out predictions missed plus one over band (honest, but lab precedent caps at silver); the "+62/−60" ledger attributed to law.md exists nowhere in the docs (the measurement stands, the framing doesn't); and the adoption-blocking gap — promotion's information is unaccounted (far deltas at q_far can't regenerate exact state; the firewall doesn't cover a promoted body's own near-zone error where navigation must be perfect).

**Gold experiment:** measure promotion — event-log bits via the canonical replay log, or lossy-promotion error under a moving player with tier churn — folded into the far-tier design.

Minor finds: `t400.py` was edited after its output (key rename, undisclosed, values regenerate) and the 1.4 GB/157-bit figure isn't derivable from stored outputs. Verdict written to `check.md`; nothing else in the run folder touched.
