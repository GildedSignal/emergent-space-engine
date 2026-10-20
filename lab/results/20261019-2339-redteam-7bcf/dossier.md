# Dossier: r12-seen-flux — the aggregate's seen flux (1885's channel), rung frozen and executed; the dispersion channel's location is found

**Claim.** The dispersion channel's seen-flux rung now exists (r12, frozen at sha256
a6335a29…89ce before its run) and executes PASS: the letter's "aggregates are one sample
each" is dead on the flux channel (p99 error 0.21–1.11, worst at player speed β 0.5 with
wide dispersion, not at exotic γ), and the moment/formation readout (squad Gaussians +
formation shape, quadrature over the full nonlinear k) is licensed at ≤ 0.05 p99 with
readout error ≤ 3.8×10⁻⁴ (isolated against a 10⁶-member truth) at ~4.3×10³ ops per fleet
per frame, constant in N.

**Bottleneck.** The view (board focus item: what the player sees); the unguarded half of
L59 after 1885. Not a 10× on the engine — a type gate plus the design's cure measured and
licensed: it deletes the per-ship per-frame k⁴ sum at fleet scale (1.7×10⁷ ops/frame at
N = 10⁶ → ~4×10³, a 4000× on that readout) and pins where the γ² amplification actually
lives.

**Evidence** (`python3 seen_flux.py`, 20 s; `bash regen.sh` regenerates all numbers and
the verdict):

| case | one-sample p99 | mix-quad p99 (N=400) | mix-quad vs 10⁶ truth | CV(k⁴) head-on |
|---|---|---|---|---|
| c1 gauss β0.5 σ0.03 | 0.2745 | 0.0104 | 1.2×10⁻⁴ | 0.120 |
| c2 gauss β0.9 σ0.03 | 0.2771 | 0.0104 | — | 0.120 |
| c3 gauss β0.99 σ0.03 | 0.2783 | 0.0104 | — | 0.120 |
| c4 ring β_rot 0.05 | 0.2123 | 6.7×10⁻¹⁶ | — | 0.141 |
| c5 ring β_rot 0.15 | 0.7105 | 6.7×10⁻¹⁶ | 8.9×10⁻¹⁶ | 0.420 |
| c6 bimodal ±0.05 | 0.3022 | 0.0034 | — | 0.201 |
| c7 gauss β0.5 σ0.10 | 1.1092 | 0.0332 | 3.8×10⁻⁴ | 0.414 |

- Verdict: **PASS** (per-ship positive passes all: two k paths agree to 9.0×10⁻¹⁵, p99
  8.9×10⁻¹⁶, 6800 ops; one-sample negative fails the license bar 1.109 > 0.05; mix-quad
  candidate passes all: p99 0.0332 ≤ 0.05, 4320 ops ≤ 20000).
- **The convention finding (the new science).** The frozen fleet is a formation: internal
  velocities v′ are comoving and composed with the bulk by exact SR velocity addition.
  Then velocity addition compresses the longitudinal dispersion by exactly the γ² that k
  amplifies at the mean: d ln k⁴/dv′∥ = 4·(1 + O(v′)), so **CV(k⁴) ≈ 4σ_comoving,
  independent of γ** — measured 0.120 = 4×0.03 identically at β 0.5, 0.9 and 0.99, and
  0.420 = 4×(0.15/√2) for the fast ring. The γ² drama in 1885's CV law = √(e^{16s²}−1)
  belongs to **observer-frame** dispersion (a swarm, not a formation): my observer-frame
  diagnostic (u ~ bulk + N(0, σ) directly, β 0.9, σ 0.03) measures exact CV(k⁴) = 4.05 at
  head-on, where 1885's linearized law gives 0.70 — the linear law is the small-s limit
  and understates the tail ~6× at its own headline point (near u→1 the convexity of k
  explodes). The channel is real in every convention; its size is set by which kind of
  aggregate the fleet is.
- **The one-moment cure suffices for formations.** The bulk readout N·k(bulk)⁴ errs only
  e^{8σ²}−1 ≈ 0.7–1.6% p99 at σ 0.03 (measured 0.0157) and fails only at σ 0.10 (0.091);
  a single-Gaussian moment readout on the fast ring (same variance, shape wrong) errs
  0.0023 p99 — distribution shape is a fourth-order effect under comoving dispersion.
  The letter's failure is specifically *sampling one member* (loses mean and spread), not
  missing moments.
- The mix-quad p99 at N=400 (1.0–3.3%) is the truth's own finite-sample floor
  (CV/√400 = 0.6–2.1%), not readout error: against a 10⁶-member truth the readout error
  is 1.2×10⁻⁴–3.8×10⁻⁴ (gauss) and 8.9×10⁻¹⁶ (ring, spectral). The license bar passes at
  N=400 and tightens as fleets grow.

**Predictions** (`predictions.md`, written before the run): 3 of 7 held (P1 negative
fails hard — driver was c7 not c2/c3; P6 instrument 9.0×10⁻¹⁵; P7 ops). Four failed with
one diagnosis: I wrote P2/P4/P5 with observer-frame amplification in my head; the frozen
physical model cancels it (the convention finding above). P3's letter (≤ 10⁻³) failed on
the sampling floor while its substance (readout ~10⁻⁴) held — now separated by the 10⁶
arm. Every miss sharpened the domain rather than the numbers.

**What would make it wrong.** The frozen fleet model is the letter's own aggregate (a
formation, L69); heterogeneous emit luminance and occlusion are out of scope (occlusion
is r11's arm, executed PASS); the observer-frame diagnostic reuses 400 members so its CV
carries sampling noise. A checker should re-derive the comoving cancellation
(d ln k⁴/dv′∥ = 4 at v′ = 0, exactly, for any β) and re-run `bash regen.sh`.

**Cost of adopting.** Replace L59's flux half with: the aggregate readout is ⟨k⁴⟩ over
the fleet's own description (bulk + velocity moments per squad, or the formation's
shape), integrated at the observer's direction each frame; one sample is dead (0.21–1.11
p99, measured). The fleet already carries type/frame/formation (L69); the readout adds
~10²–10³ ops per fleet per frame, constant in N. Fit with PRINCIPLES: "Compute only
surprises" (the flux is derived at observation, never broadcast); principle 33 (smaller
influences enter as an aggregate — here the aggregate *is* the emitter, resolved at its
own scale); "Behaviours matter, not continuum fidelity" (a p99 type bar on what the
player sees, not trajectory identity).

**The lens (what it may have missed).** Ranked attacks before choosing: the two-body
doll and dense≡sparse premises stand (r3 v3, r5 — not re-attacked here); this run
harvested the page's own named experiment instead of opening a new front. Red-team
blind spot guarded: the worst measured failure is at player speed (β 0.5, σ 0.10), not
at exotic γ. Missed axes, named for the next run: heterogeneous luminance per member
(weighted moments — same machinery); the sprite *type* table (binned log k, where 1885's
40% median was reported — the bin boundaries interact with dispersion differently than
continuous flux); time evolution of the moments under stirring (how often squads must
re-estimate σ; kick cadence territory).

**Grade sought:** gold if the checker reproduces (regen 20 s) and the rung freeze is
accepted; the rung is in the run folder for the integrator to commit to `lab/rungs/`
(the 4ff1 pattern), with the v2-freeze sentence: *the license covers fleets whose
velocity description is carried per squad and per formation; the γ² channel belongs to
observer-frame swarms, whose aggregates must not be read by one sample either —
measured CV 4.05 at β 0.9, σ 0.03, where the linear law reads 0.70.*
