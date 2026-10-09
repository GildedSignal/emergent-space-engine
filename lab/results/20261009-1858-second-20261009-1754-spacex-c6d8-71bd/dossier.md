# Dossier (second author on 20261009-1754-spacex-c6d8): the ledger is dead on the belt too — and the rate is the doll's grid, not the orbit

## Claim

With the instrument completed (dperi fed, --kick-bench restored, per-binding multiplicities
counted — the first run's headline was ~2.2× low) and the checker's named experiment run, the
first run's claim **holds and sharpens**: the plane's battle scene creates 234–252 bits per
rebounded binding (debt after the per-binding refit 177–196; ≥ 98 % of it not absorbable by any
mean-style refit), saturating the 64-bit budget in **18–36 game-s**; and on a **quiescent belt**
(a star, three planets, no fleet, no player, no input) the per-binding program refit still leaves
**173.5–175.1 bits/binding** at a radius-independent cadence of **3.55–3.58e-5 bindings/ship/s**
(set by the ext clock's grid — the doll's shortest secondary's period, ext.rs:26 — not the body's
orbit), so even the belt saturates 64 bits/ship in **2.85 game-hours**: law.md's "+62 bits per
kick and −60 per reabsorption" is dead as specified — the +62 is ~3× low for the record-journal
the plane actually writes, and the −60 has no mechanism (a slow-EMA reabsorption removes 2 % on
the belt and is *negative* on the plane); the measured law change is representational — journal
the cause (the kick is ~1 readout-quantum: its ramp dv rounds to zero in the refit's word, ~2
bits) and recompute the refit, per Principle 6, "store the generator, not the generated".

## Bottleneck

Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; HANDOFF risk
"H_live … not measured yet". This run supplies the belt's number and the cadence law, the two
missing decision variables for the allocator and for `b-h-live`.

## Evidence

All commands in `commands.md` (each ≤ 60 s; belt 13 s); JSONs in this folder; digests reproduce
bit-for-bit across reruns. The four plane flights are **identical to the first run's** (digests
83d96bed…, e56d1c12…, e3eb62e6…, 6ddafe96…): the record regenerates from shipped code, only the
instrument changed.

| scene | bindings/ship/s | bits/binding debt (± EMA) | bits/ship/s | 64 bits gone |
|---|---|---|---|---|
| plane seed1 rtf100 (v1: 0.875) | 0.0041/0.0153 (made/members) | 185.6 overall (207 with EMA) | 2.04 | 31 s |
| plane members400 / rtf20 | — | 185.6 / 179.7 | 3.51 / 3.53 | 18 s |
| belt 2.1–3.5 AU, 120 ships, 1.74 yr | 3.577e-5 | 175.05 (171.03) | 6.26e-3 | 10,223 s |
| belt seed 2 | 3.566e-5 | 174.58 | 6.23e-3 | 10,279 s |
| belt 0.55–0.85 AU (inner) | 3.549e-5 | 173.5 | 6.16e-3 | 10,393 s |
| belt 0.63 yr vs 1.74 yr; belt 240 ships; rtf 3e5 vs 1e6 | 3.57e-5 (all) | 174.8–175.05 | 6.24–6.26e-3 | 10,256–10,268 s |

- **Cadence law:** inner vs outer belt (orbital periods differing ~7×) give the same cadence to
  0.8 % — every clock-stepped ship of the root doll is kicked on the doll's grid: Δs = P_D/2^7
  with P_D the doll's shortest secondary's period (Cinder), "rounded down to a power of two"
  (ext.rs:26); measured grid 28.1 ks ≈ P_D/256 = 29.7 ks. H_live's rate is a property of the doll,
  not the population — a belt at any radius inherits Cinder's frequency.
- **Cause vs debt:** items/binding = 2.00 and kicks ≈ bindings (237,766/236,055) — every kick
  fires and rebinds — yet the stored ramp dv is **0 in 100 % of belt bindings**: each fired kick
  is ~1 quantum of the readout word and rounds to zero in the refit's word. The kick's own
  information is ~1–2 bits; the 175-bit debt is the refit record's rewrite (residual 66.2,
  carry 36.0, dk 29.8, dperi 27.7, dangle 15.3), a deterministic function of (old record + kick
  + shared state).
- **Reabsorption:** a per-body slow EMA (gain 1/64) on the three delta fields removes 2 % on the
  belt (175.05 → 171.03) and makes the plane *worse* (185.6 → 207): the delta fields are white
  fit jitter, not predictable advance. Mean-style reabsorption is dead in both scenes.
- **Regression fixed:** `--kick-bench` runs again (cadence instrument reachable); plane digests
  unchanged by all v2 edits.
- Belt wall 13 s for 475,601 events; bytes_per_body on the belt store: 6,293.

## Predictions

`predictions.md` was written before the decisive belt runs (a 5-s feasibility smoke preceded it; disclosed there, and its cadence output was ignored — the brackets missed it by 18×). Held: debt 175 in [120, 260] (1); dperi 27.7 in
[8, 30], p_zero 0 (5); stationarity within ×2 — measured 0.2 % (6); wall < 55 s (7). Failed,
honestly: cadence 3.56e-5 against a bracket of ≤ 2e-6 (2) — 18× above the top; I had
pre-registered the falsifier ("a much finer clock shows up as a cadence above 1e-5"): the ext
clock's doll-wide grid is exactly that; consequently saturation is 2.85 h, not 1.5–7 days (3).
Untestable as built: the word-width fire fraction (4) — the sweep's raw stream loses the fired
quanta whenever the ramp dv rounds to zero (which is every belt binding), so its 0.0-at-w≥8 is an
instrument artifact, not a measurement; disclosed rather than dropped. The pre-registered verdict
rule (debt ≥ 50 bits/binding on the belt ⇒ the ledger is dead as specified; the saturation
headline is scene-bound) fired on the debt branch.

## What would make it wrong

The debt journal prices the plane's current representation (refit-record rewrites at 60-bit
words), and part of it is recomputable from the shared state by an exact replay — a store that
journals causes and recomputes fits on read would measure ~2 bits/binding on the belt, so the
*ledger's replacement* is a representation choice, which is the finding, not a confound. The
belt is one system (this star, these planets) at e ≤ ~0.2 and no resonance sweep; a resonant or
eccentric belt could raise the debt. The 60 Hz journal merges bindings only when two land in one
frame (measured ≤ 0.3 % between rtf 3e5 and 1e6 — the clock's regular grid aliases against frame
boundaries). The ±1-exponent mechanism behind "ramp dv ≡ 0" is an inference from the measured
zeros plus `word_for`'s stated 2× margin, not read line-by-line.

## Cost of adoption, and fit with PRINCIPLES

The patch touches `xtask` only (one bench file, one flag set); no crate, gate or digest changes;
`b-h-live` can lift it into `universe --bench` unchanged in approach. Principle 24 ("The memory
floor is information … why do you need so many bytes per entity?") — the belt's floor is ~2
bits/binding as cause, 175 as record: the ledger must say which it prices. Principle 6 ("Store
the generator, not the generated") — the refit record is the generated part. Principle 3
("Compute only surprises") — the kick is ~1 bit of surprise wrapped in 175 bits of rewrite.
Principle 19 ("A fix signals the wrong representation") — the −60 reabsorption line is the fix
that never had a mechanism.

## The lens

The second-author lens made me reproduce before extending, and pre-register the falsifier that
fired (the doll-wide clock grid). What it may have missed: the compute twin (what 3.6e-5
bindings/ship/s costs at 10⁹ — ~3.6e4 binding-events per game-second per billion, the
allocator's real load), and the replay-exactness question (whether a cause-journal store can
regenerate bit-identical refits on read, which decides if the 2-bit floor is real).

## Grade (author's self-assessment)

Gold by the run's own criterion ("the claim now holds on the shipped record with the named
experiment done"): the record regenerates (digests identical), both named instrument defects are
fixed, and the named experiment ran with held-out cases (seed, inner belt, density, horizon,
rtf) all within 1 % — the ledger is dead as specified, and the cadence law (the doll's grid)
plus the cause/debt split (1–2 bits vs 175) are the adoptable replacements.
