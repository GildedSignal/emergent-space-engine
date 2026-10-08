Working...
Check complete. `check.md` written to the run folder (the only file touched there; no git commands run; all scratch work in `/tmp/check-ecfd`).

**Grade: silver.**

Verdict basis:

- **Reproduced bit-identically** — `falsifier.py` regenerates every number in `falsifier-out.json` and the dossier's table (3.6 s wall on this box, order-of-magnitude per lab rules).
- **Controls verified independently**: my quadrature of the geodesic's first integral matches the ODE `shipped` column to ≤1e−6 where it decides (p̄ ≤ 100); e→0 converges to the circular closed form; and the decision-relevant D̄ sign is settled from the primary source — Damour 1212.3169 eq. (19) gives D₂PN = 1 − **6**νu², the author's `s=−1` branch.
- **The core finding survives every attack**: B11's tolerance (1% + 16/p) verified against `law.md:70`; the sign-flipped-2PN law passes B11 at every seed with ≥5.9× margin; below the gate floor (p̄=10–15) the pattern holds; novelty clean against H0183 (the 2PN gap flagged, never run), H0203 (r3 v1's contaminated oracle), H0206 (the widened tolerance built on an estimated 8/p next term that actually measures 4.5/p).
- **Why not gold — the record, not the physics** (the 1 October precedent): prediction 1 failed low at 2 of its 3 named points (0.36% vs a [1%,20%] floor at p̄=20) yet the dossier reports "Held: scale" — hiding, incidentally, that their own pre-registered <0.5% survival criterion fired, which is the strongest form of the claim. And the "5–170×" oracle-distance range does not regenerate from the shipped code (actual: 34–718× at ν=0.25). Both slips understate the effect; the gold path is a record correction, not a new experiment.

Bonus verification of their attack 2: `representation.md:32` does still present the Minsky/Binet map as "the primary in-cell solution" although `law.md:20` records it killed by `space-darwin16-v1` — a live doc hazard for the next builder.
