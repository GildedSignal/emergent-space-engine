# Predictions (written before the belt runs; the plane's four v2 reruns above are the record
# regeneration, not the decisive experiment)

Question: on a quiescent belt (star + 3 planets, no fleet/player/input), with the plane's own
per-binding program refit, how many bits per binding does a body still owe (debt = post-refit
record), at what cadence — and does the +62/−60 scar ledger of docs/law.md survive that?

Tuned on: nothing belt-specific. The plane's v2 reruns told me bits-per-binding there (234–252);
the belt's kick sizes are Fermi-estimated from Giant's pull at ~2 AU separation acting over a
P/128 step (dv ~ 10 m/s against a 2^-60-of-20 km/s quantum, i.e. ~2^45–2^50 quanta).

## Held-out expectations

1. **Debt per binding on the belt: 120–260 bits, point ~200** (same 60-bit words, same binding
   machinery as the plane's made bodies, which show 195–196). If it is < 60 the belt's kicks are
   somehow absorbed by the fit and the ledger is rescuable as specified.
2. **Cadence (bindings/ship/game-s): 6e-7 – 2e-6, point ~1e-6** (≈128 bindings per 3–6 yr orbit;
   the root doll's ships are on the ext clock, whose step I have not read — a much finer clock
   shows up as a cadence above 1e-5 and falsifies this number, not the method).
3. **Rate: 1e-4 – 5e-4 bits/ship/game-s → the 64-bit budget saturates in 1.5–7 game-DAYS**
   (point ~3), against the plane's 18–36 game-seconds: the battle scene's rate is cadence-bound
   (orbital frequency), not bits-per-binding-bound.
4. **Fire fraction at coarser velocity words: ≥ 0.99 at w = 8, 16 and 24** (kicks are ~2^45+ quanta;
   absorbing them needs a ~2^45-coarser quantum, i.e. a ~15-bit velocity word — not a sane
   representation). If any swept width cuts the fire fraction materially, part of the dv cost is
   a word-width choice.
5. **d_peri_time on the belt: 8–30 bits/sample, p_zero < 0.2** (it moves now that it is fed; the
   plane's made bodies show 15–16).
6. **Stationarity**: the rate over years 4–5.2 within ×2 of years 0–1 (no secular diffusion
   signature at these e and separations over one orbit).
7. **Wall**: the 5.2-year belt replay finishes in under 55 s (few times 10^4 events).

## Verdict rule (fixed before the run)

If debt ≥ 50 bits/binding survives on the belt at its cadence: the +62/−60 ledger is dead as
specified (+62 is ~4x low, −60 has no mechanism), the saturation headline of the first run is
scene-bound (belt: days, not seconds), and the adoptable statement is the split — bits per
binding are law-bound, the rate is cadence-bound. If debt < 10 bits/binding or cadence < 1e-8/s:
the ledger is rescuable and the first run's saturation claim is a battle-scene artifact alone.

## Disclosure (appended after the decisive runs, not edited in above)

A 5-second feasibility smoke (`belt-smoke.json`, 0.16 yr, wall check for the 55 s budget) ran
BEFORE these predictions were written; its JSON (which contained cadence 3.56e-5) was on disk.
The brackets above were nevertheless written from the P/128 Fermi estimate, not fit to it — they
missed the smoke's cadence by 18×, which is the miss reported below. "Tuned on: nothing
belt-specific" above should read: tuned on nothing; the smoke fixed only rtf/seconds/wall, and
its cadence output was available and ignored. The decisive runs (55 s) all came after this file.
