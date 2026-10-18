Grade: silver

**Abstract.** The flown fleet's contact-skip channel is measured on the shipped plane (contact-speed od 3): closed at shipped speeds — 0 skips in 1,620 contacts at ρ = reach/|w| ≥ 10⁴ (checker adds 1,532 contacts on seed 2, still 0; the census at 55 s is bit-identical to 30 s, the battle completes) — and reopened only at ~0.84 c closing: 2–12% of detected contacts ghost at ρ = 0.93–9.6, where the driven-pair law max(0, 1−ρ) predicts exactly zero; bit-identical across steppers (reproduced on a fresh seed). Gain: a measured boundary that keeps the root-normal fix unscheduled for today's plane. Cost: none (print-only census, deleted with the patch). Silver because nothing is adopted and the τ*-window mechanism was overstated (5/46 skips at 400 members reach τ\* = −8.4; page corrected); one experiment from gold — the ship-scale-radius companion scene plus the v1-operator re-derivation (od 1's gates a+b), with this run's rate as the number to beat.

## Reproduction

- The runner's `regen.sh` (clean tree at 994cc61e + `work/patch.diff`, private target dir) reproduced every dossier number exactly: ship48 49/0, ship400 1571/0, sd128 50/0, sd8 53/0, sd4 44/2 (4.55%), sd2 41/5 (12.195%), sd2s2 32/3 (9.375%), sd2m400 1451/46 (3.170%), dense/sparse `cmp`-identical. I re-derived the ρ/|w| percentiles independently from the raw censuses; they match.
- I re-flew two author arms from separate processes with the run's own binary: members=1000 (CLI-clamped to 400) produced a census **bit-identical** to sd2m400, and ship400 at 55 s a census **bit-identical** to ship400 at 30 s — determinism holds across processes, and the 55 s identity shows the battle is over well before 30 s, so the author's 30 s arms already capture the whole engagement.
- Census hygiene: zero duplicate CENSUS lines in any arm; in code the print sits inside `resolve_law`'s pair loop after the Bounce/consumed filters, immediately before the receding gate, and both steppers reach it through `law::respond` — it logs exactly the pairs the gate decides on.
- `predictions.md` predates the sweep by file order; the two post-freeze arms (sd4, sd2m400) are disclosed as dose-response additions, not tuning.

## Held-out and adversarial (mine)

1. **Seed 3, sd 2** (fresh, outside the author's seeds): 49 contacts, 1 skip (2.0%), τ\* = −0.50, **ρ = 1.92 > 1** — the ρ ≥ 1 violation of the driven-pair law holds on a third seed; the dense 3 s census is again `cmp`-identical.
2. **sd = 1**: panics at world construction (`body 3 at or beyond light`) — speed_div 2 is the legal floor, so the author's "any legal speed" boundary is structural, confirmed.
3. **Beyond the tested range:** `--members` is clamped to [4, 400] and `--seconds` to [1, 55] by the shipped CLI — the author's 48/400 × 30 s already spans the surface's entire N and time domain; "larger N" residues need a new scene, not more members. Worth recording on the page (done).
4. **Shipped speed, seed 2, 400 members, 30 s:** 1,532 contacts, 0 skips, min ρ 1.04×10⁴ — the headline survives attack.
5. **The mechanism sentence does not.** "Every skipped contact has τ\* ∈ (−1, 0)" is false over the run's own data: in sd2m400, 5 of 46 skips have τ\* ≤ −1 (min −8.36, at ρ = 9.59). The author's `tau-star.txt` table covers only sd2 and sd2s2 — the two arms added after the predictions freeze (sd4, sd2m400) were never fed to the mechanism table, and one of them breaks its universality. Also "every resolved contact has τ\* > 0" is definitional (resolved ⟺ d·w < 0), not a discovery. Corrected in place on the proposed page; the substantive mechanism (skip = resolved after the crossing completed; window mostly ≤ 1 chronon at 48 members, widening with N) stands.
6. **Seed noise:** the sd-2 rate is 12.2 / 9.4 / 2.0% on seeds 1/2/3 (n = 41/32/49) — the "~12%" headline is seed 1. Page corrected to 2–12%.

## Novelty

`lab/wiki/contact-speed.md` open direction 3 read "the real rate in a flown fleet … unmeasured"; docs/HISTORY.md has no flown-fleet skip measurement (8144 = driven pairs on Chronon, 1648 = gas twins, 6362 = the fix's integer design in a toy). This run closes od 3 and refutes the page's working premise that the driven-pair law bounds the flown fleet (skips at ρ up to 9.59). Not a repetition; the proposed page folds it in with correct citations (its three new Refuted entries match the evidence).

## Goal fit

Encounters-class question on the board's focus list. It buys a decision (fix stays unscheduled for the plane) with a measured structural margin, and its honest prediction failure follows "a failed expectation is not automatically a failed method: diagnose which one broke" (H0183) and "Measure before claiming, and never strawman". Print-only instrumentation, deleted with the patch — "the cheapest compute is compute not done".

## Why silver, not gold

Reproduced bit for bit, novel, held-out held — but nothing moves 10× and nothing is adopted (the dossier's own conclusion: the shipped plane needs no fix). The premise corrected is a page-level mechanism premise, not an engine premise, and one detail of the stated mechanism (the τ\* window) was overstated rather than confirmed. **The one experiment that would make it gold:** freeze the ship-scale-radius lattice scene (reach ~10²–10³ quanta) as r5's companion with 6362's closed-form fix on the shipped v1 operator — od 1's adoption gates (a)+(b) — where this run supplies the negative control (shipped arm) and the rate to beat (~0.1–0.2/ρ, resolve-window law, not max(0, 1−ρ)).

## What the author missed

- Their own sd2m400 arm contradicts the τ\* ∈ (−1, 0) universality; the mechanism table was never extended to the post-freeze arms. The resolve window grows with members — itself a finding (batch/calendar latency scales the ghost window), left unmined.
- The headline 12% is seed 1 of a 2–12% band; per-arm contact counts (32–49) are too small for a rate stated to three digits.
- The CLI's own `--members`/`--seconds` clamps bound every residue named in "what would make it wrong"; the next run needs a new scene, and the page now says so.
- The dense control was run on one seed only (I extended it: identical on seed 3).
