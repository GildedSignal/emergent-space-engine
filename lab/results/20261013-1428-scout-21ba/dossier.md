# Dossier — 20261013-1428-scout-21ba (lens: scout)

## Claim

The shipped kick compile's certified panel walk computes **complete elliptic integrals**:
the cycle's azimuth advance is exactly `2·[2K(m)/√A − π]` (one Carlson `RF` call,
constant cost in e and q), verified against shipped `Orbit::compile` to 3–5×10⁻¹⁰
(the compile's own Q30 output quantum) on every strong-branch key of the grid — so the
panel-count law change the record keeps deferring has a named, closed-form replacement
mechanism, and the Opus memo's "revisit only if strong-field compiles show in a profile"
condition is now met: the compile **is** the profile (49–97% of every kick).

## Bottleneck

`kick-jet` / `frame-cost` open direction 1: "fewer panel evaluations per compile (the
law's π/4 quantum and band cuts — a law change with recertification)". The interior is
closed by elimination (divisions at hardware floor, allocations 0.3%, isqrt closed by
9384), so panels are the only ≥10× lever left. Measured here on shipped code: the panel
count (knots−1) is **5 at e≈0.001 → 26 (e 0.5) → 68 (0.9) → 81 (0.94, the plane's
median kicked e) → 123 (0.99) → 176 (0.999)**, and compile wall tracks it exactly:
**3.2 → 197 µs** (median of 31, shared box). The growth is the u-band cuts (one cut per
dyadic band edge between apastron and periapsis; ~11 octaves at e 0.999) — i.e. the
cost that explodes is paid precisely on the leaver/plunge tail (`Passage::compile`
89–97% of a 365–381 µs leaver rebind, ec9d). The closed form's cost is **O(1)** in e:
one Carlson duplication chain, ~6 iterations by the quadratic spread trajectory
(0.25 → 0.06 → 4e-3 → 2e-5 → 4e-10 → ~1e-16; my probe's stop rule over-runs and
prints 27 — instrument, not mechanism).

## Evidence

All numbers from `regen.sh` (< 1 min: `cargo run --release -p emergent-space
--example elliptic_probe`, output in `probe-out.txt`; the example is this run's patch).
Grid: `OrbitKey::bound(2^pe, e·2^48)` — note `bound`'s argument p is the **semi-latus
rectum**; the key stores periapsis = p·k, so q_key = 1/(p·k). 18 keys, q_key
9.5×10⁻⁷ … 7.5×10⁻², k 0.999…0.50025.

1. **φ channel, exact.** For every strong-branch key (q_key > 2⁻¹⁸; 15 rows):
   `|advance() − 2[2K(m)/√A − π]| / advance = 3.0–4.8×10⁻¹⁰`, where
   `A = 1 − q_key(8k−2)`, `m = 4·q_key(1−k)/A`. The φ increment is stored Q30, so the
   shipped compile's own output quantum is 2⁻³⁰ = 9.3×10⁻¹⁰: **the closed form and the
   shipped integer walk agree to the compile's last stored bit's order**. My f64 closed
   form vs an independent 8192-panel GL4 f64 truth of the same integrand: 10⁻¹³–10⁻¹⁵
   (weak rows 10⁻¹¹: the GL truth's own roundoff on a small excess).
2. **First-order check:** the closed form expands to advance = 6πM/p (e-independent at
   first order) — matches the shipped values' e-independence (all e at fixed p agree to
   5 digits), and is the textbook periastron advance 6πM/p_semi-latus.
3. **Weak branch (q_key ≤ 2⁻¹⁸, 3 rows):** agreement 4.3×10⁻⁶ relative — the branch's
   own first-order-in-q truncation (its integrand is the Taylor excess 3k+(1−k)cosψ),
   not the closed form's error. The weak branch is closed-form-able as the Opus memo's
   R1 already said (prediction 4 confirmed).
4. **Cost.** Shipped compile wall (median 31): 3.2 µs (5 panels) → 197 µs (176 panels,
   e 0.999). The entire closed-form advance in f64: **37–39 ns** (median 20k; one RF,
   ~6 duplication iterations, no cos, no general division — the duplication step is
   adds + one isqrt, the primitive 9384 just took to 54 ns). That is 10²–5×10³× on
   this box for the φ channel, integer-vs-float caveat stated.

Instrument failures disclosed: my tanh-sinh level loop never reported convergence
(returns at its h floor), so prediction 3's DE node count is **untested**; my RF
iteration counter's stop rule over-runs (27; trajectory says ~6). Neither touches the
φ verification, which rests on the shipped compile's own output.

## Predictions

`predictions.md` written before the run. Outcome: 1 confirmed (stronger than
predicted: 3×10⁻¹⁰, not 10⁻⁵); 2 half-confirmed (panel counts confirmed, incl.
the band-cut mechanism — which I had mis-attributed to the λ-ladder in the prediction;
Carlson cost constant confirmed only analytically, counter broken); 3 untested
(instrument); 4 confirmed (4.3×10⁻⁶ = the branch's own truncation). One wrong guess
during the run, corrected by measurement: I first used q = 1/p; the shipped `advance()`
is e-independent at first order, which exposed q_key = 1/(p·k) (p is the semi-latus).

## What would make it wrong, cost of adopting, fit

- **Wrong if:** the τ/t channels do not reduce the same way (mechanism cited —
  ∫R(cosψ)dψ/√(1−q·a(ψ)) with R rational is the Legendre Π/E/K family in Carlson's
  symmetric forms RF/RD/RJ, with the squared (1−n sin²θ) denominator handled by
  Π + n·∂Π/∂n — **not verified in this run**; the horizon factor 1/(1−2q·x) adds one
  more first-degree rational factor, same family); or the integer port cannot carry
  Carlson's certified per-iteration bounds at the law's quanta. The known failure
  mode is m → 1 (the true separatrix, P = 1−q(4k+2) → 0): K diverges logarithmically —
  physical (the period diverges), and exactly the regime where the shipped walk's
  panels also explode; the closed form stays finite-cost there (the log is the answer),
  but relative accuracy near the degenerate limit needs Carlson's complementary forms
  (literature, UNVERIFIED here).
- **Cost of adopting:** a law change with recertification (as the record already
  states): the crossing table and the readout's in-cell Newton solve are built on
  panels; incomplete elliptic integrals (same duplication algorithm, amplitude-carrying
  Carlson forms) replace them. The readout's "t mod T, mirror, search, solve" pipeline
  shape survives. Integer Carlson needs its own error analysis — the memo's objection —
  but the shipped compile already pays certified integer quadrature; the duplication
  loop's per-step bound is simpler than a panel's fourth-derivative majorant (the
  certified bank R5 already prices isqrt-based kernels). Kerr (kerr.rs, quartic radial
  polynomial) is the same family — Fujita–Hikida solved equatorial Kerr exactly in
  these forms (UNVERIFIED at source).
- **Fit with PRINCIPLES:** #7 "Multipoles are the mechanism" / "Geodesics are as
  trivial as straight lines… make compute cheap"; #1 "The cheapest compute is compute
  not done"; #18 "we just need to have the right representation so that math is
  trivial"; #19 "if you find yourself fixing things that's oftentimes a signal that it
  is the wrong representation" — the band cuts, the λ-ladder and the crossing table are
  all fixes for representing an elliptic integral as panels.

## The lens

Scout searched for the structure in another field and found it 19th-century-old
(Legendre/Carlson); what the lens may have missed: (a) everything above is the
φ channel only — τ/t are cited, not measured; (b) the EMRI literature's integer
implementations and their error analyses were not read at the source (marked); (c) a
components-lens run should price an integer Carlson RF against the shipped node before
anyone believes the 10²–10³×; (d) the readout path (crossing table → Newton solve) was
not costed — if the table must exist for other consumers (the kick tier's windows?),
deleting panels deletes only half the walk.
