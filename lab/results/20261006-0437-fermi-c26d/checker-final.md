Working...
Check complete — `check.md` written, nothing else in the run folder touched (reproduction ran in `/tmp`; the run's own `heat.json` md5 verified unchanged).

**Grade: silver.**

Evidence basis:
- **Reproduced**: `python3 work/belt_heat.py` → stdout diff-identical to `run4.txt`, `heat.json` md5 `79fe98bb…` unchanged, 1.4 s. `patch.diff` empty. `predictions.md` (04:45:06) predates runs 1–4 (04:47–04:51) — genuinely held out.
- **Controls pass**: κ=0 → 0.0 bits; 10×κ → 80.5 vs 62.8 at 1e6.
- **My attacks**: importance-sampled paired hyperbolic scattering reduces exactly to the code's κ (CLT valid at λ=1.65e7 kicks/orbit, max single kick 0.057 m/s vs 146 m/s cumulative — no tails); seeds 7/13/101/202 → 92.1–92.2 bits; sample size and Coulomb-log sweeps move ≤0.5 bits; all sweep arithmetic (corners, tame threshold 1.6e8 kg, 11.52 GB) re-derived. Adoption targets verified in repo: B18's "2× the measured information floor" clause and shipmem's "identity is provenance" (compact repacks blocks, never reassigns ordinals).
- **Why not gold**: 3 of 7 held-out bands missed (κ, bits at 1e6 and 1e9, coherence — all disclosed, all strengthening), and the 11.5-GB headline sits at a corner with 2.5e5 collisions/body: the identities the number is computed for cannot survive there. The universal result is the collision-independent phase floor (19.9 bits = 2.49 GB, inside 6 GB) plus the mass-dichotomy and the repack cadence.
- **Gold path**: one experiment — the aged floor on the collision-tame belt the game can actually have, with real dynamics (direct scattering, mergers, tide/resonance channels).
