# Predictions (written before the probe runs)

Question: what is the live binding quantum of a ladder belt body on the shipped path
(`bind()` → `Rebinding::from_state` → OrbitKey + velocity word), and which impulse
sizes fire? This decides the encounters page's live contradiction (f0a2: exact tier
empty at an absolute E-quantum 319.3 m²/s²; 277d: 62–571 cores at a binding-relative
2⁻⁴⁸) — both anchored on the **legacy** `Key` (E Q48), which the live v3 path never stores.

Anchors used here (from shipped code): AU = 101,300,000 root units (scenario.rs);
root unit = 149,597,870,700 m / 101.3e6 = **1476.8 m** (= GM☉/c² to 3 digits: a solar-mass
star); belt ships' radius 34·2⁻¹⁰ root units ≈ 49 m; belt a ∈ [2,3) AU, e Rayleigh 0.07;
`word_for` (bind.rs:192) sets the velocity exponent to `v_max.exponent() − 60`.

## The pre-registered ladder (all sizes in doll units, c = 1)

| quantity | my estimate | basis |
|---|---|---|
| belt speed \|v\| | 2^(−13.8) c | 18.8 km/s at 2.5 AU about 1 M☉ |
| velocity exponent ev | **−73.6 ± 1.5** | word_for: v_max.exponent()−60; v_max ≈ 2^−13.6 c |
| length exponent el | −31.8 | r_max = apoapsis ≈ 3.04e8 root units = 2^28.2; −60 |
| velocity quantum (SI) | 2^(−73.6)·c ≈ **1.6e-15 m/s** | 60-bit word over [0, ~2·v_max) |
| belt's own kick (2⁻²³·v, 3294) | 2^(−36.8) c = **2^36.8 quanta** → fires every time | 3294's fire rate 1.000 |
| ship–ship conjunction (2×49 m, b = 1e5 m, v_rel = 30 m/s) | Δv ≈ 2^(−108.5) c = **2^(−34.9) quanta** → invisible; even below the sigma-delta carry floor 2^(ev−16) = 2^(−89.6) c | Δv = 2μ/(b·v_rel), μ(49 m) = G·(π/6)ρD³ |
| D* (partner that flips 1 quantum at b = 1e5 m, v_rel = 1e3 m/s) | **D ≈ 0.8–0.9 m** → every Dohnanyi body (≥ 70 m) flips at any flyby b | μ_min = quantum·b·v_rel/2 |
| flip reach b_max of a 70-m rock (v_rel = 1e3 m/s) | 2μ/(quantum·v_rel) ≈ **4e10 m ≈ 0.3 AU** (belt width) | ⇒ every crossing pair is supra-quantum |
| km-rock close approach (D = 1 km, b = 200 m, v_rel = 1e3 m/s) | Δv ≈ 1.05e-3 m/s = 2^(−38) c = **2^35 quanta** → flips hard | weak-deflection Δv |
| OrbitKey (shared compile) moves when | δv/v ≳ 2^−47 ⇒ **~2^11 quanta** (k word is Q48, k ≈ 0.93) | dk/dv ≈ k²/v |
| tube periapsis_angle (2⁻³² turn) moves when | δv/v ≳ 2^−32·(v_tangential fraction) ⇒ ~2^26–2^30 quanta | orientation shift |

## The three outcomes I pre-register

- **A (my expectation, p ≈ 0.8): ev ≈ −74 (60-bit relative).** Then the live binding
  quantum is ~10^68× finer than the legacy E-key's SI equivalent (319 m²/s² ⇒ δv ≈ 8.5e-3 m/s):
  f0a2's "exact tier is empty" is an artifact of the legacy key — on the live path
  **every** Dohnanyi conjunction (≥ 70 m) at any flyby distance flips the velocity word,
  and the full exact tier reverts to the published contiguous wall (~1.6e3–8.2e3 cores at
  10⁹, 3.9e8 pair-events/s at v_rel ≈ 1e3 m/s). 277d's "survivors everywhere" direction is
  right, at a different quantum (live ≈ binding-relative 2⁻⁶⁰, i.e. 2¹² finer than 277d's 2⁻⁴⁸).
- **B (p ≈ 0.15): ev ≈ −48 to −44 (absolute-ish c-fraction word).** Then f0a2's branch
  survives on the live path, with D* ≈ 0.2–0.8 km at b = 1e5 m — the tier is empty-ish and
  routing (0.03–0.6 cores) is the whole 10⁹ encounter bill.
- **C (p ≈ 0.05): ev varies widely across the belt (per-body word, not per-orbit).** Then
  the anchor is body-dependent and the gate must read each body's own exponent — a wiring
  cost, not a physics one.

## Composition whichever way (pre-registered)

The aggregate self-gravity flux at 10⁹ Dohnanyi (total belt μ_tot ≈ G·2.2e20 kg ≈ 1.5e10
m³/s² over 15.7 AU²) is per body 4·Σμ ≈ 1.7e-13 m/s per s ⇒ per 28,141.5-s interval
≈ 4.8e-9 m/s. At a 60-bit word that is ~3e6 quanta/interval/body (must ride the kick
stream: 1.6e-5 of the kick impulse — PRINCIPLES #6, the aggregate as a source, zero new
events); at a kick-matched ~30-bit-relative word it is 2.8e-4 quanta/interval/body
(one fire per ~3,500 intervals — nothing). So the 10⁹ CPU ledger is insulated from the
anchor dispute **iff** per-pair exact work is deleted (D* routing or flux split); if it is
not, outcome A prices the tier at the contiguous wall (~10³ cores) and the budget dies.

The one dial that decides between f0a2's and 277d's world is the velocity word's width
(a representation choice, `word_for`'s 60 bits, not a law constant): at ~30-bit-relative
words (kick scale 2⁻²³·v fired at ≥ 2⁷ units needs ev ≤ log2 v − 30) ship/rock flybys are
sub-quantum and f0a2's D* ≈ 0.7 km route revives; at 60-bit words everything real fires.

## What would make me wrong

- If `readout`/`bind` choose coarser units than `word_for` implies (e.g. a doll-wide
  exponent policy), ev lands near −48 and B holds.
- If the belt body's binding is a Passage, not a Cycle (a < b belt edge case), the
  periapsis/k ladder shifts but the velocity-word ladder does not.
- If my μ(D) Dohnanyi mass is off by ≫ 10×, D* moves by (10×)^(1/3) ≈ 2.2× — not
  outcome-changing (D* sits 2 decades below the 70-m floor either way in A).
