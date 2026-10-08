# Dossier — 20261008-1947-second-20261008-1859-scout-141c-3186 (lens: second author)

**Claim.** On the plane's **real kick stream** (the shipped engine's own events, dumped through
its public API), the naive per-(body, source) news channel grows ∝ R² with the cone radius,
while the cell-owned octave accumulator's arrival rate does not grow at all beyond the largest
source's individually-firable radius — it **saturates** (measured flat to 3 digits), because the
engine's impulse news falls as 1/d³ (measured exponent −0.973 per octave shell), not the toy's
1/a² — so Julien's growing-cone risk (OC#50) is a budget choice about Q, with a tighter law than
the silver run claimed: log R was the toy's law; the engine's is O(1).

## Bottleneck

The named gold experiment from the silver run's checker: "wire the two channels into the
engine's own news path and run them on the plane's real event stream at a growing horizon …
the log law and the r_cut crossover either hold on real events or the toy's identity is missing
engine physics (directional cancellation, correlated kicks)." Done: the stream comes from
`emergent-universe` itself (no crate edits; a crate in this folder drives the public API), the
receiver's Q is anchored to the player's own registers, and both engine-physics risks are
measured. Gain: naive/accumulator = 358× at R = 1024 AU at the engine's own Q (1.4×10⁴ at
Q·10³; 4×10⁶ at Q·10⁶), and the ratio is unbounded (∝ R²) — at a 10⁶ AU horizon the naive
channel extrapolates to 5×10⁴ arrivals per 33 ms frame (impossible) against the accumulator's
4×10⁻⁶ (free). This deletes the per-source cursor as a galaxy-scale structure and bounds what a
body must consume, on the design's own cheap path.

## Evidence (every command ≤ 60 s; the whole record regenerates bit-identically, md5-checked)

```
cd lab/results/20261008-1947-second-20261008-1859-scout-141c-3186/kicks && cargo build --release
$CARGO_TARGET_DIR/release/kickdump massive 40000000000000 > ../kicks_massive.csv   # 1.6 s
$CARGO_TARGET_DIR/release/kickdump full 20000000000 32       > ../kicks_full.csv   # 5.0 s
python3 news_engine.py --selftest                                                  # 0.2 s
python3 news_engine.py                                   # 4.5 s -> news_engine.json
```

**The stream is the engine's.** 24,525 kicks on the four massive bodies (Cinder, Home, Giant,
Moon) over 4×10¹³ ticks, walked out of the bindings' own history; the full plane (23 ships,
fleet of 32, player) produces **bit-identical** massive-body kick streams over the shared 2×10¹⁰
window (md5 per body: Cinder 347771aa…, Home d0a611c4…, Moon cac0bd29…), because ships are
massless and never kick sources — the long massive-only run *is* the plane's gravity news.
Ships still matter as the receiver: the player's registers (step 2²² ticks, velocity quantum
2⁻⁷⁴ of c, sigma-delta carry 2⁻¹⁶ of it) set **Q_engine = 2⁻¹¹² tick⁻¹ ≈ 1.93×10⁻³⁴** — the
acceleration that moves the receiver's velocity by one sub-quantum per window. News of a kick
is not assumed: a receiver at d that ignores an impulse dv over window T accumulates
retarded-force error G·m·|dv|·T/d³ by the source's next kick.

**Channels.** The plane's system replicated on a disk at fixed surface density (1 per (16 AU)²,
12,867 systems, receiver at the star), real kick times/sizes/directions, arrivals at t_e + d,
10 decades of Q sweep, octave shells, toy semantics (s ≥ Q fires once individually; the rest
accumulate per shell per window and fire floor(Σs/Q); unit-tested in `--selftest`).

- **Naive ∝ R²: exponent 1.957** (staggered 1.956; the residual is placement noise of a drawn
  disk; rates 3.1×10⁻⁹ → 7.9×10⁻⁶ tick⁻¹ over 16 → 1024 AU).
- **The accumulator saturates.** Shell news sums fall as r^−0.973 (fit over 6 octaves): the
  engine's news is 1/d³, so per-octave increments halve (measured ratios 0.49–0.64) and the
  total fire rate goes flat: at Q·10³, 5.39→5.62→5.62×10⁻¹⁰ tick⁻¹ at R = 256→512→1024 AU.
  The silver run's log R was the toy's 1/a² mass-change model; the engine's impulse law is one
  power steeper and the toy's claim *tightens* — exactly the direction the toy's own caveat
  anticipated ("the law only tightens").
- **Crossover r_cut ∝ Q⁻¹/³** (cube root, not the toy's Q⁻¹/²): per-source individually-firable
  radius r_b = (s_loc/Q)^{1/3}, slope −0.333 for all four sources × 10 decades of Q; aggregate
  crossovers 64/32/16 AU at Q/Q·10/Q·10² (slope −0.301). At **Q_engine**: r_b = 4.8 AU (Cinder),
  8.2 (Moon), 35 (Home), **970 AU (Giant)**.
- **Directional cancellation is real and bounded:** vector accumulation fires 0.52–0.74 of
  scalar (26–48% fewer; the toy's "cancellation only lowers" holds, and by how much is now
  measured).
- **Correlated kicks cannot inflate the channel:** the adversarial case (all 12,867 systems on
  the engine's identical aligned power-of-two kick grids) fires 0.92–0.99× the staggered-epoch
  case — within the Σs/Q + 1/window bound; the aligned real grid is if anything slightly
  cheaper. My frozen ±5% band was exceeded at 9% (Q1–Q3), in the safe direction: staggering
  spreads arrivals more evenly and loses less to flooring.
- **Plane scale (P6, the adoption question):** at Q_engine every source of the receiver's own
  system is individually firable (s/Q = 565, 2.2×10³, 4.4×10⁴, 8×10⁶ for Moon, Cinder, Home,
  Giant) — the per-(body, source) cursor (b-news-gravity's design) is right inside systems; the
  accumulator engages at 8–35 AU for common sources, and massive outliers (a Jupiter) keep
  cursors to ~10³ AU at a negligible count (2 kicks per 10¹² ticks per system). The handover
  radius is per source-mass-class, not one number.

**The checker's π defect, corrected on the record.** The silver dossier's toy constant was
mis-derived: the simulated naive rate is λπR² (ρ_eff = 1, not the stated 1/π), and the correct
per-octave quantum increment is λ·2πδρ_eff·ln2/Q = 43.6 (verified: ∫_r^{2r} (δ/a²)·ρ·2πa da =
2πδρ ln2, times λ, over Q), which matches its measured 44 — the "~6% deficit from r_cut" story
was wrong accounting. Exponents, crossovers and ratios were unaffected, as the checker said.

## Predictions

`predictions.md` was frozen before the decisive run, with one pre-run addendum (timestamped
before any output existed) correcting an arithmetic slip I caught in my own P2: r² sources ×
r⁻³ sizes = Σ ∝ 1/r, so increments **halve**, not hold. Outcome: P1 held (1.957); P2's frozen
text failed exactly in the predicted tightening direction (measured r⁻⁰·⁹⁷³, saturation);
P3 held (−1/3 per source exactly, aggregate −0.301); P4 held (0.52–0.74 ∈ [0.25, 1.0]); P5 held
in substance at 9% vs my 5% band, safe direction, cause identified (flooring loss); P6 held
(r_b(Q_engine) ≥ 4.8 AU ≫ 1 AU kill line; own system all-individual).

## What would make it wrong

- One system's physics replicated: a universe whose systems have more or heavier secondaries
  raises the largest r_b (the Giant is the whole 970 AU tail); the *law* (per-source Q⁻¹/³,
  saturation beyond max r_b) stands, the *constant* is per mass function.
- Q anchored to one receiver (the player's registers); a certificate demanding finer Q moves
  every r_b up as Q^{1/3} and the saturation floor up as 1/Q — measured, not assumed.
- The window semantics (fires per T_win = T_meas/4, the toy's construction): rates carry an
  O(1/window) flooring granularity; both channels share it.
- 2D, one seed for placements, central receiver (off-centre was checked on the toy by the prior
  checker; the counts here are 7.9×10⁶ events, so placement noise shows only in the 1.957).

## Cost of adoption and fit

Cell-owned octave accumulators beyond per-source r_b(Q); per-source cursors inside it, mass-class
by mass-class. The saturation also answers the silver run's unexamined memory tension: channels
beyond ~r_b(Giant) fire ~never, so far octaves can live at coarser cadence — the 32-accumulator
Fermi (2.6 GB) is an upper bound, not a requirement. PRINCIPLES: P6 ("influences below one
quantum accumulate" — now measured on engine events), P3/P14 (compute only surprises), P23
(nothing past c: arrivals at t_e + d throughout), P33 (each scale resolves only what matters at
it: r_b is the scale's own quantum crossover).

## The lens (what the second-author lens may have missed)

I ran the checker's named experiment on the scout's structure, which fixed the news model as
one impulse per kick; a comet burst or a handoff inside a source system (rare large dv) would
appear as a heavy tail the accumulator absorbs one quantum at a time — the stream here has no
encounters (no ships near the planets), so that tail is unmeasured. The view (photon) channel
and H_live affordability remain where the scout left them (b-readout-cost, b-h-live).

## Grade (author's self-assessment)

The silver run's named gap is closed: the record regenerates from shipped code bit-for-bit
(md5-verified), the experiment ran on the engine's real event stream, and the claim held — and
tightened (saturation, not log). Gold-shaped; the checkers decide.
