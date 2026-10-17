# Run 20261017-0839-fermi-2b89 — the encounters quantum anchor, measured on the live path

## Claim

The encounters page's live quantum-anchor dispute was decided on the wrong object: the live
path never stores the legacy `Key`'s E (Q48) — it stores a **60-bit-relative velocity word**
(`word_for`: exponent = `v_max.exponent() − 60`), measured here at **ev = −73** for every
sampled belt binding (locals −76/−77: per-binding), a quantum of **3.17×10⁻¹⁴ m/s** — 2.7×10⁸
times finer than the legacy anchor's SI equivalent (319.3 m²/s² ⇒ δv ≈ 8.4×10⁻³ m/s) and 2¹⁰
finer than 277d's binding-relative 2⁻⁴⁸. At the live quantum **every Dohnanyi conjunction
fires**: D* (1 quantum at b = 10⁵ m, v_rel = 10³ m/s) = **2.5 m** (word) and **40 m** (the
compiled key mints from 2¹² quanta, δv/v ≈ 2⁻⁴⁷) — both below the 70-m belt floor; the exact
tier is **full**, not empty, and f0a2's "0.03–0.6 cores" branch dies on the live path. The
10⁹ budget survives only through the flux accumulator, and the anchor itself is a dial, not
physics: coarsening the word by 5–15 bits (kick = 2³⁵ quanta today, so it keeps firing until
ev ≈ −45) moves D* from 2.5 m to 1.6 km and revives f0a2's world.

## Bottleneck

The board's #2: encounter work at 10⁹ ("~10³–10⁴ cores; what cuts it by 10³"). The page's
adjudicated resolution (f0a2: exact tier empty) determines whether encounters are on the 10⁹
critical path at all. This run moves that question from a code reading + float replicas to a
measurement on the shipped integer path — and reverses the adjudication's live-path reading
while confirming the budget outcome (the flux split, not the anchor, closes 10⁹).

## Evidence (all from `cargo run --release -p emergent-universe --example enc_quantum`, shipped main + the print-only example in `work/patch.diff`; seed 1, N = 3000; ≤ 60 s total)

Anchors, printed by the probe from the shipped binding:
- root unit = 1476.8 m (AU = 101,300,000 root units, `scenario.rs`); belt ships' radius
  34·2⁻¹⁰ root units ≈ 49 m; belt a ∈ [2,3) AU, e Rayleigh 0.07.
- **ev = −73, el = −32/−33 for all 6 sampled belt bodies; ev = −76/−77 for 2 locals** — the
  word is sized per binding by `word_for` (60 bits over the orbit's own v_max/r_max), not by
  any absolute c-fraction. Belt |v| ≈ 2⁻¹⁴ᐟ¹⁵ c; the metronome kick (2⁻²³ of speed, 3294) is
  **2³⁵–2³⁶ quanta** — every kick fires, consistent with 3294's fire rate 1.000.
- The live quantum is 2⁻⁷³ c = **3.17×10⁻¹⁴ m/s**.

The physics ladder (probe output, exact arithmetic on the measured quantum; ρ = 3000 kg/m³):
- two 49-m ships at b = 10⁵ m, v_rel = 30 m/s: Δv = 8.2×10⁻⁹ m/s = **2¹⁸ quanta** (and the
  sigma-delta carry sees it: `quantize`'s inc ≥ 1 at its 2⁻¹⁶-of-quantum floor).
- flip reach: a 49-m body flips any partner out to **0.17 AU** at v_rel = 30 m/s; a 70-m rock
  to 0.015 AU at v_rel = 10³ m/s — the belt's width.
- D* (1 quantum): 2.47 m (b = 10⁵, v_rel = 10³), 5.33 m (10⁶, 10³), 0.77 m (10⁵, 30).
  The Dohnanyi floor (70 m) is 3–90× above: **nothing in the belt is deletable per-pair.**

The rebind ladder (one belt body, dv = 2^i quanta applied to the velocity word, re-bound
through the engine's own `bind_surface` path; **control dv = 0 included**):
- **CONTROL (dv = 0): dk_word = −1, d_periapsis_angle = +59, d_periapsis_time = +2.02×10¹³
  ticks** — the readout→bind roundtrip is not bit-identical to the stored spec binding (the
  fit's floor; the two paths are different computations). Every row 2⁰–2¹¹ quanta equals the
  control bit for bit: **below ~2¹² quanta an impulse moves only the raw velocity words, not
  the compiled orbit.**
- From **2¹² quanta** (δv = 2⁻⁶¹ c ≈ 1.3×10⁻¹⁰ m/s, δv/v ≈ 2⁻⁴⁷) the key word moves
  (−1 → −2 → −3, halving per bit: linear response), the tube words follow from 2¹³ —
  **a firing impulse above 2¹² quanta mints a new OrbitKey ⇒ a new compiled entry**
  (4.4 µs at belt keys, c4d3; 52–65 µs on the plane population, a765), and efd4's intern
  cannot dedup near-identical keys.
- The belt's own kick (2³⁵ quanta) sits 2²³ above the mint threshold: every metronome kick
  rebinds and re-mints (3294's fire rate 1.000 + the kick-jet page's rebind-per-kick, both
  reproduced on this ladder from the word's own exponent).

The 10⁹ composition (`compose.py`, orders of magnitude, constants as measured):
- Per-pair exact handling on the live word is dead: 6.45×10⁶ firing pair-events/s within
  b = 2.3×10⁹ m (v_rel = 10³) ⇒ **25.8 cores of finding (4 µs) / 322 cores if each fires a
  rebind (50 µs)**, before the candidate tier's own wall (the published contiguous cascade,
  1.65×10³–8.2×10³ cores, fermi-1738 — my rate reproduces its order, as it must: at the live
  quantum the gate deletes 0%, which was the wall's assumption).
- The aggregate self-gravity flux (Dohnanyi [70 m, 470 km], N = 10⁹, belt mass 2.2×10²⁰ kg,
  μ_tot = 1.46×10¹⁰ m³/s²): 1.66×10⁻¹³ m/s per s per body = **4.7×10⁻⁹ m/s per 28,141.5-s
  interval = 1.5×10⁵ quanta/interval/body** at ev = −73 — 4×10⁻⁶ of the kick impulse: it
  **rides the kick stream at zero new events** (PRINCIPLES #6: the aggregate as a source).
  At ev = −64 it is 287 quanta/interval (still rides the kick); at ev = −45 one fire per
  ~1,800 intervals. The flux accumulator (62f7) is not an optimization at 10⁹ — it is the
  only law that closes, at any word width.
- The word-width dial: ev ∈ [−68, −45] keeps the kick firing (2⁴⁰–2⁶³ quanta ≥ 2⁷, 3294's
  floor) and moves D*_word from 7.9 m to 1.6 km and D*_key from 40 m to ~10 km: **f0a2's
  empty-tier world returns at ~5–15 bits of coarsening** — the two runs measured the same
  physics at two word widths; the anchor is a representation choice (`word_for`'s 60 bits),
  not a law constant.
- Flown-plane cross-check: the mutual-conjunction channel switches on exactly at the
  ladder's frontier — at N = 2,700 one firing conjunction per body per 2.7 yr (invisible);
  at 10⁶, 2.2/s fleet; at 10⁹, 2.2×10⁶/s.

## Predictions (`predictions.md`, written before the probe ran)

- **Held:** ev ≈ −73.6 ± 1.5 (measured −73, all belt bodies); el ≈ −31.8 (−32/−33);
  kick = 2^36.8 quanta (measured 2³⁵–2³⁶); outcome A (60-bit-relative word, exact tier
  full); the dk threshold δv/v ≈ 2⁻⁴⁷ (measured 2⁻⁴⁷: key moves at 2¹² quanta); the
  composition's insulating conclusion (flux rides the kick stream).
- **Failed, and caught by the run:** my pre-registered ship–ship Δv at b = 10⁵ m was
  2⁻¹⁰⁸ᐟ⁵ c (invisible) — a c vs c² slip in converting μ to SI (I divided the geometric μ by
  c once too few). The correct Δv is 2⁻⁵⁵ c = 2¹⁸ quanta: it fires. This strengthens
  outcome A beyond what I predicted (even the flown 49-m ships are mutually supra-quantum
  at flyby distance).
- **Partly failed:** my "1 quantum mints the key" first reading was the missing control's
  artifact (dk = −1 was the roundtrip floor); the honest mint threshold is 2¹² quanta.
  The dossier's claim above is the corrected version.

## What would make it wrong

- The word is re-sized at every rebind to the *new* orbit's v_max (`bind`'s coarsening only
  grows the word), so a body whose orbit shrinks keeps a finer word than v_max needs: the
  measured ev is an upper bound on fineness, never coarser than reported. The conclusion's
  direction is safe; the exact D* scales as (quantum)^⅓.
- The conjunction impulse model is weak-deflection 2μ/(b·v_rel), validated to 0.999+ against
  RK4 by c7eb/0b81 in this regime; deep encounters are contact-tier business anyway.
- The Dohnanyi mass function and v_rel = 10³ m/s are content assumptions (the page's own):
  mass ×52 lowers D* by 3.7×, still ≤ belt floor; v_rel 30 m/s lowers D*_word to 0.77 m.
- If `word_for` is changed (the dial), every D* row moves as (2^Δev)^⅓ — that is the point,
  not a risk. What would actually refute the claim: a shipped belt binding with ev ≈ −48
  (none in the sample: 6/6 at −73) or a per-pair certificate that deletes at the live word
  (the gate itself measured 0% deletable here).

## Cost of adopting, and fit with PRINCIPLES

Nothing to wire: this is a measurement. The decision it feeds: (1) the encounters quantum
gate as f0a2 specified it (charge the legacy E-key's Q48) is not implementable on the live
path — the live charge is the binding's velocity word, and at today's width it deletes
nothing; the routing bit (D* mass bit) must be read against the **word-width decision**,
which is the integrator's (one dial, ~5–15 bits, sets both the encounter regime and the
standing-representation's key-mint rate); (2) the flux accumulator is confirmed mandatory at
10⁹ at every width (62f7's design stands). Fits "the right question, then the representation"
(PRINCIPLES #18: "we just need to have the right representation so that math is trivial") and
"the best part is no part" (#17): per-pair work at 10⁹ is deleted, not optimized, by the flux
law. Units: every decisive number is an integer read off shipped code (ev, el, the ladder of
word deltas); floats only price orders of magnitude, as the lab requires.

## The lens (what Fermi may have missed)

The Fermi lens pushed to a single quantum anchor; the run found **two** thresholds (word vs
key mint, 2¹¹ apart) and a third floor (the fit's roundtrip instability at dk = −1, which
also bounds efd4's dedup: re-binds of near-identical states cannot share entries at the fit's
own floor). A dynamics lens might ask whether the roundtrip instability itself compounds
across a body's kick history (each rebind re-fits from the readout, so the −1 may be
path-dependent state, not noise) — out of scope here, and cheap to probe next. Also unprobed:
whether the coarsened word (the dial) collides with the clock/high-γ keys (C1's E exactness)
— the dial must be checked against the frozen gates before anyone turns it.
