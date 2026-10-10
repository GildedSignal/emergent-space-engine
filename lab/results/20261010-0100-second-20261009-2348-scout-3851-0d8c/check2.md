Grade: gold

# check2 — second checker, blind to the first

**Abstract.** Claim: on the full 2×2 coupled member tide (both channels,
shear Λ₁₃, precession ω) in the Marck frame, the closed-form Floquet chart
matches exact-transport truth on 144/144 bands (≤0.03 grid steps), survives
fixed-point quantization, while the orbit-averaged law misses 127/144 and
overstates ruin speed 1.8–3.6×, and the scout's frozen scalar certificate
misses 142/144. Reproduced: `run-all.sh` regenerates every output file
byte-identical (4:15 total, ~148 MB, each command < 60 s). I re-derived Λ and
ω from scratch (sympy metric → full Riemann and connection): Λ to 2.1×10⁻¹⁵,
ω to 6×10⁻⁶, circular Δψ geodetic. Gain: the certificate's adoptable form is
fixed (4-column quantized table per (E,L) tube); the scout's scalar
certificate dies. Adoption: one table per tube key plus 4×4/2×2 monodromies.

## Reasons

1. **Reproduction, bit for bit.** Clean /tmp copy, empty `work/patch.diff`:
   `val.json`, all six `results2-*.json` and `analysis.txt` regenerate
   **byte-identical** (cmp), 4:15 wall, max RSS 148 MB — comfortably inside
   60 s per command and the 2 GB budget. Every dossier number (144/144,
   0.026 steps, 127/144, 1.8–3.6×, 142/144, 73% peak error, 0.253/orbit
   chan2, 0/12 gaps) prints from the regenerated files.

2. **The physics is true, verified from scratch.** I built the equatorial
   Schwarzschild metric symbolically, derived Christoffels and the full
   Riemann, anchored the sign on the physical radial stretch
   (R_{t̂r̂t̂r̂} = −2w), and contracted the tide at grid points through this
   third path: Λ₁₁, Λ₃₃, Λ₁₃ agree with the closed forms to ≤2.1×10⁻¹⁵
   (w_max-relative) on (30, 0.6), (100, 0.3), (10, 0). ω = −⟨∇_u f1, f3⟩ with
   the symbolic connection agrees to 6.0×10⁻⁶ / 3.0×10⁻⁷ / 4.4×10⁻¹⁶; I also
   re-derived the circular limit by hand (−γu_φu(f−u)/√f = geodetic
   −2π√(1−3u)/T_r, weak-field 3πM/r ✓). Frame vectors verified unit and
   mutually orthogonal at 10⁻¹⁶. The closed forms — the object the tube would
   compile — are correct.

3. **Pre-registration stands.** marck.py final save 01:59:06, predictions.md
   02:01:51, recorded sweep files 02:11:09–02:14:26: a 12-case sweep needs
   ~4.5 min, so no held-out band structure existed when predictions were
   written. The dossier quotes numbers from an earlier overwritten pass
   (dossier.md mtime 02:11:17 sits mid-pass) — since the recorded pass is
   byte-identical, the record is sound, but the two-pass structure is
   undisclosed (see misses). Predictions: P1, P2, P3, P5, P7 held; P4 held
   stronger than predicted; P6 and P8 failed and are reported as failed with
   numbers. Calibration (rp=100, e=0.3) disclosed.

4. **Attacks (mine).** (a) Grid hole (1e6, 0.6): truth 18 = chart 18, avg 1 —
   consistent with the e=0.6 column. (b) Strong field rp=6, e=0.3 (scout's
   tool crashed at rp=5): 16 = 16, conv 3.2×10⁻⁷, domain guard raises on
   unbound (rp, ra). (c) Threshold stress: recounting at 0.01/0.02/0.05/orbit
   gives chart 0 missed of 150/144/128 truth bands, frozen ~90% missed at
   every threshold — the 144/144 is not a threshold artifact. (d) Quantization
   stress beyond the run: Q=2¹⁰ keeps all 20 bands of (30, 0.6) with 0.000-step
   shifts and ≤0.4% peak error; even Q=2⁸ keeps every band (worst shift 1.7
   steps) — the ∝1/Q claim holds four orders below the law's 32-bit packets.
   (e) Extremes e=0.9 (outside E9's grid): at (30, 0.9) chart=truth 8=8, but
   at (100, 0.9) truth 12 vs chart 14. Adjudicated as the truth's artifact:
   my independent ω agrees with the closed form there (3.9×10⁻⁵) while the
   transported ψ's spectral derivative is off by 3.5×10⁻³ (∫ω vs Δψ 1.1×10⁻²);
   truth bands are converged in sub (12 at sub=2/4/8), so the chart's ω is
   the accurate side and the transport side degrades first at extreme e. This
   strengthens adoption (the chart is the robust object) but bounds the
   truth=transport cross-check to e ≲ 0.7.

5. **Novelty.** The closed-form kernel and ω derivation are prior art in the
   lineage (20261002-0539-q-fermi2-tide-0dee, 20261006-0220-…-26a7: kernel
   −w(3γ²−1), +w; the b-fermi-phase2 build graded "missing", never
   delivered). New here: the Floquet certificate on the *coupled* system —
   exactly the gold-lock experiment the scout run's checker named — plus the
   quantization answer (the scout lens's own open worry) and the kill of the
   scout's shipped scalar certificate (P5/P7: 142/144 missed, 18–23 truth
   bands vs frozen's 9–14 at e=0.6, Coriolis bands even at e=0). No HISTORY
   entry (ends H0215) or doc covers member band certification.

6. **Goal fit.** Board item 4 (the Schwarzschild tide in the Fermi frame),
   fencing H0190's 114× averaging lever. PRINCIPLES #13 "Errors never
   compound": the averaged reading is blind to 127/144 bands and mis-sizes
   ruin speed 1.8–3.6× — an error-type failure, not error size. #4 "regimes
   are chosen by dimensionless numbers": band membership read from the
   tube's compiled (Λ, ω) tables. #3 "Compute only surprises": the chart is
   computed once per (E, L) key, not per body. The claimed theft with skin in
   the game (Courant–Snyder rotating-frame structure) is apt — the member ODE
   is exactly their machine-orbit equation with geodetic precession as the
   lattice's spin.

## What the author missed

- **Provenance disclosure.** The dossier's mtime note ("predictions 02:05,
  sweeps 02:0x") is wrong (02:01:51; 02:11–02:14) and hides the two-pass
  structure: a first sweep pass was overwritten by the recorded one, and the
  dossier was finalized from the first pass mid-way through the second. The
  scout run disclosed its equivalent; this run should have too. Nothing rides
  on it here (byte-identical regeneration), but on a less reproducible run it
  would.
- **The e ceiling on the truth, not the chart.** At e = 0.9 the
  transport-derived ω is the polluted side (3.5×10⁻³ vs my independent check);
  the run never probes e > 0.6, and its lens names only the Ω ceiling. The
  certificate's own validation inverts there — worth one sentence in the
  build's domain guard.
- **"Reproduced to 8×10⁻⁵"** (circular Δψ) is the *relative* error; absolute
  is 5×10⁻⁴. Predictions inherited the same gloss. Immaterial, but the
  corporal could misread it.
- **P2's second clause** (avg static edge misplaced > 5% in an e = 0.6 case)
  is tallied "held" in the dossier without a printed number; only the
  blindness and ruin-speed clauses are measured.
- Q=2¹⁶'s "0.000 steps" is grid-bin luck (quantization at 2⁻¹⁶ happens to
  land inside the same bins); the honest statement is the one the Q=2⁸ stress
  supports — structure-invariant to ~2¹⁰.
