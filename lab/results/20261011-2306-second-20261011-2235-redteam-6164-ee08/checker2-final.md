Working...
Check complete. `check2.md` written to the run folder; scratch tree removed; nothing else touched, no git commands beyond read-only ones.

**Grade: gold** (second checker, blind to the first).

**What reproduced** — every dossier command reran in a clean tree (patch.diff empty):
- `probe.py` → `probe_out.json` **byte-identical** (md5 match); probe2 parts A, a0, hcheck, a0998lite → **identical ex-machine**; a05/a09 record rows match the dossier table point-for-point.
- a0 control vs parent P3: dφ/T ≤ 1.0·10⁻¹², |∂T/∂E| ≤ 1.07·10⁻¹⁰; E_c = √(9/10) exactly.
- `equality` 10/10 (170 s), `identity` 9/9 (384 s) — premise 4's substance is real, passing crate tests, including the planted-late-kick negative control.

**Adversarial probes of mine (all confirming):**
1. **Retrograde** (author's named open case), via (a,L)→(−a,−L) at a=−0.9: |∂T/∂E| 5.9·10⁵→6.6·10⁶ per decade; quantum kick breaches the floor at ε=10⁻⁴ (7.2·10⁻⁶); α=10⁻³ → plunge-after-kick. The failure holds at every spin state, beyond what the author measured.
2. **Off-grid (15/8) law**: T/((15/8)(δE/(1−E))²) = 0.96–1.00 at three off-grid points — the parent's inverted decomposition is genuinely corrected.
3. **0.998 whirl h-refinement**: 1.3·10⁻¹¹ — the longest whirl is integration-converged, closing the gap the author's h_check left.

**Predictions**: pre-registered (mtimes), with a real falsification branch in P8 that resolved against the parent's gold-adopted mechanism — held.

**Named misses** (not load-bearing): `metal_identity.rs` named in the dossier **does not exist** (metal tests are `equivalence.rs`/`kickable.rs`); "byte-identical to parent" is unverifiable in this checkout (parent folder absent — only self-regeneration checks, and holds); χ=0.998 deep-ε slope and the Kerr T-channel belt grid stay open (honestly costed); my retrograde ε=10⁻³ base-cycle failure shows the oracle's band guard needs care before any retrograde rung.
