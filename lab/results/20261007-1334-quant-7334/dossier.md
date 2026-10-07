# Dossier — 20261007-1334-quant-7334 (Quant lens)

## Claim

A Jupiter-forced belt scars **100% of its bodies within one orbit** under the shipped scar
semantics (deviation from the birth program) at the store's native grids — a scar field of
22–38 bits/body, i.e. **2.8–4.3 GB at 10⁹ bodies, with ~zero growth per game-second after
that** (flat from 1 to 100 yr): the naive "program + per-body scars" population store is not a
cache in the secular regime, it stores the derivable; the live memory budget survives at scale
only if the program's prediction includes the compiled secular field (the law's own
orbit-averaged kick machinery), which turns the whole-belt term to ~0 and leaves
individualizing events (encounters, chaos, player) as H_live.

## Bottleneck

HANDOFF risk "**Distinctions created per game-second (H_live): they, not the body count, decide
whether 10⁹ fit in 8 GB; not measured yet**"; B18's "measured information floor" of a *live*
belt (the born floor, 0.126 bits/body, is `components-98bc`). The measured quantity is an
information floor of a float reference dynamics (floats explore; no canonical outcome is
decided here).

## Evidence

Instrument: `belt_hlive.py` — 2D test-particle Wisdom–Holman (exact universal-variable Kepler
drift, verified: round-trip 2×10⁻¹⁵, energy drift 1.4×10⁻¹¹ over 100 yr; Jupiter's tide as
direct+indirect kicks, μ_J = 9.54×10⁻⁴, a_J = 5.2, e_J = 0.048), belt a∈[1,1.5] AU, e₀
Rayleigh, dt = 1/32 yr. Scar = quantized (Δa/a, Δ(e cos ϖ), Δ(e sin ϖ)) from the birth state.
Estimators: marginal entropy per body (H_raw), zlib-packed field (zraw), and a kNN-in-birth-state
"generator" floor (H_knn; metric chosen after the first run showed an a-only model fails —
disclosed). i7-4790 shared VM (load 4.6), 8192 bodies, one seed, grids 2⁻²⁰/2⁻²⁴/2⁻²⁸
pre-registered in predictions.md.

Reproduce (40 s, < 100 MB):

```
python3 lab/results/20261007-1334-quant-7334/belt_hlive.py   # prints table; saves hlive.json
```

Main scene (σ_e = 0.01), bits/body, three columns:

| t (yr) | scarred | H_raw @2⁻²⁰ | @2⁻²⁴ | @2⁻²⁸ | H_knn @2⁻²⁰ | ledger @10⁹ (@2⁻²⁰) |
|---|---|---|---|---|---|---|
| 1 | 1.000 | 23.1 | 33.8 | 38.4 | 23.8 | 2.9 GB |
| 10 | 1.000 | 22.5 | 33.4 | 38.4 | 22.8 | 2.8 GB |
| 100 | 1.000 | 23.4 | 34.0 | 38.5 | 22.6 | 2.9 GB |

- **Everything scars in one orbit** (secular forced response ≈ 10⁻⁴ e-units ≫ 2⁻²⁰): P1 held.
- **The field is regular, not diffusive:** H_raw and H_knn are flat (±5%) from 1 to 100 yr;
  H_knn(100 yr) < H_raw — the entropy at t=1 yr never grows. The belt creates ≈ **0 bits per
  game-second**; a deterministic generator that knows the program and the shared ephemeris
  re-derives every body (principle 3). What my estimators *cannot* do is capture the wound-up
  field cheaply: it shears in a (precession gradient), smooth only below ~10⁻³ AU, so smoothing
  or zlib (33–65 bits/body) fail — only an exact secular map (re-simulation or H0190's compiled
  averaged field) reaches the 0-bit floor.
- **Tail scene (σ_e = 0.1):** H only +8–10% over σ_e = 0.01 (25.6 vs 23.4 bits at 30 yr);
  p99.9 residual ≈ 6–7× the median quanta. Eccentricity is not the multiplier at belt scale;
  the wound secular field dominates. (P3's "≥3×" falsified.)
- **Store widths:** the tube's E is Q48 and L Q32, finer than my 2⁻²⁸ grid, so 38.5 bits/body
  is a **lower bound** on the shipped packed-delta cost per scarred body.

## Predictions

`predictions.md` was written before the first decisive run; seeds, scenes and grids unchanged
since. P1 held (100% scarred ≤ 1 yr). P2 falsified as stated (residual ≫ 1.5 bits/body: the
smooth-in-a model is the wrong generator — the field is wound, not diffusive) but its core
survives in exact form: growth is ~0, so the information is derivable, by an exact secular
generator, not by cheap smoothing. P3 falsified (+10%, not 3×). P4 untested: test particles
carry no mutual gravity, so the in-sim encounter rate is undefined; asteroid-mass mutual
scattering is negligible by magnitude (Δv ~ 2Gm/bv_rel with m ≪ 10⁻¹⁰ M_sun), so in a *belt*
the encounter term binds only at ship/fleet masses — r8's rates, not measured here.

## What would make it wrong

The whole belt is forced by one Jupiter on a fixed orbit in 2D; multiple strong perturbers,
near-resonance strips (r4: averaging dies) and 3:2-crowded regions create real diffusion that
my flat-in-t result would miss at 10²–10³ yr. One seed, one forcing. If the engine's population
store is *defined* to re-seal (program.rs `fold`) on a cadence, the 2.8–4.3 GB figure becomes a
peak-between-seals figure — but the measured scar rate (100%/orbit) means re-sealing is O(N)
per orbit, i.e. not a cadence but the entire cost — the conclusion stands either way.

## Cost of adoption, and fit

Nothing to build here; a constraint for `b-h-live`, `b-belt-wire` and B18's live ladder: the
population program must predict the secular drift from the compiled averaged field (H0190's
machine, already the kick path), or the belt's memory is the wound field (≈ the whole 8 GB
budget). PRINCIPLES: "**Compute only surprises** … Nothing is evolved that can be derived when
looked at" — the shipped scar semantics evolve the derivable; "6. Store the generator, not the
generated." The generator here is the secular field, not the birth program alone.

## The lens

The quant lens priced the cache and its entropy but measured a float reference, not the design's
integer kick layer; the 0-bit/sec conclusion rests on regularity it did not test to the tail of
time (10³–10⁴ yr) or near resonance. It also could not measure the encounter term that a
ship-mass population would create — the term the fleet gold (taleb-09b5) shows is where
concentration bites.
