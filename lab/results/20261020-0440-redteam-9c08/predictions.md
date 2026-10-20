# Predictions — 20261020-0440-redteam-9c08 (written before the decisive run)

**The attack.** `docs/representation.md` L59: "Aggregates are one sample each, and the screen caps
the work at about one sample per pixel" (§6 again: "The view ≤ 1 sample per pixel per frame — GPU").
Dead already on two channels (occlusion c78d/4ff1; formation velocity-dispersion 1885/7bcf). The
unmeasured third channel is the observer's OWN γ with a perfectly COLD sky (every emitter at rest
in the sky frame; zero velocity dispersion — exactly where 1885's and 7bcf's channels read zero):

ln k(θ′) ≈ ln 2γ − γ²θ′² near the forward direction, so a sky cell of half-width w carries a
k-spread of e^{γ²w²} across it. Any single shift per cell errs the forward (headlight) sky.

The current view record (e6c9/959a, the view page's current best) keeps one lum-weighted shift per
cell and was flown only to β = 0.65 (γ = 1.3). No rung guards this (r6 gates per-emitter
cost/presence; r11 occlusion; r12 formation flux).

**Setup.** Isotropic cold sky at rest, observer at β along the axis; directions aberrated into the
observer's frame; binned into rings of width θ_f (the record's floors: stock 8e-3, fine 1e-3).
Equal luminosity per emitter. Brightness of a ring = Σ lum·k⁴. Truth by MC (2×10⁶ samples) and by
1-D quadrature (k is φ-independent). Analytic small-angle law: best-single-k brightness error
≳ 1.15·(γw)²; k-span e^{γ²w²}.

## Held-out predictions (not tuned on)

- **P1.** At the stock floor (w = 4e-3), even the ORACLE-tuned single shift (k̄ = ⟨k⁴⟩^{1/4}) errs
  the forward ring's brightness by ≥ 5% by γ ≈ 50–60; by ≥ 25% at γ = 125.
- **P2.** At the fine floor (w = 5e-4), the same 5% crossing happens near γ ≈ 400–450 (×8 later,
  not ×8 exactly: the law is quadratic in w).
- **P3.** The k-span (k_max/k_min) across the forward stock cell crosses ×2 near γ ≈ 200–220, and
  across the forward fine cell near γ ≈ 1600–1700.
- **P4 (control, both sides).** At γ = 1.0001 and at the record's flown edge β = 0.65 (γ = 1.33),
  the oracle error is < 0.2% at both floors — this is why the record's flights saw nothing; and at
  γ = 10⁶ the whole sky compresses into one stock cell (k-span ~2×10⁶) — the readout is meaningless,
  no fixed cell width serves the engine's own clock-gate scale (E = 10⁶).
- **P5 (colour channel).** One number cannot hold both channels: the gap between the
  brightness-best shift ⟨k⁴⟩^{1/4} and the colour-best shift e^{⟨ln k⟩} is Δlog₂k ≈ 2s²/ln2 with
  s = std(ln k) — fourth order in γw, so colour survives roughly a decade in (γw) beyond brightness;
  measurable in octaves against the letter's own type × log k sprite table.
- **P6 (cure, priced).** (a) Per-cell log-k histograms over the cell's [k_min, k_max] hold the
  oracle error ≤ 5% with B ≈ ln(k_span)/ln(1.05)·(1/4-ish) bins — order 10² bins at γ = 250 stock,
  O(1) per cell (the cap survives). (b) The exact cure is a running sum Σ(lum·k⁴) updated at the
  events the record already pays for (the shipped per-body gather already computes k at the event,
  `view.rs` L308–319): brightness exact for one extra multiply-add per event; colour from the
  letter's own log-k table. Prediction: (b) costs zero new reads; the bin count of (a) grows only
  as ln γ².
- **P7.** The error lives in the forward cells only: rings beyond θ′ ≳ 2/γ carry < 1% of the
  total error budget at every γ tested (aberration compresses exactly the cells that err — the
  failure is on the game's marquee visual, the headlight sky).

A premise that survives: if the measured oracle error at γ = 50, stock floor, is < 1%, my analytic
law is wrong and the one-sample-per-cell readout is licensed on this channel — I will report that.
