Grade: silver

**Abstract.** The cadence split's memory ratio is the bulk's share of the kick stream, not S = 8: the history ratchet's post-onset slope measured 96% of the OFF arm's own kick stream, so at 3×10⁴ (belt 42% of the stream) `BELT_SPLIT` cuts the ratchet 1.76× and RSS 1.86× (−24.6% at 245k gs, 2.1 KB/binding), reaching 8.0× only at a 10⁹ belt. Compact-side τ ×8 is unflyed arithmetic on 0659. Reproduced from regen (1.78×, 2,097 B/binding); my adversarial 5×10⁴ pair measured 2.36 (share law 1.92; ÷S dead again; closure 88%/74%). Silver: the headline law is post-hoc (the pre-registered band [4,16] failed), and P3's letter failed identically but is reported "held". Adoption cost unchanged (law change, B-gates re-freeze); the run re-prices it on the memory market.

## Reproduction

- regen.sh exit 0 (runner) and my recomputation on its logs: OFF slope 2,457 vs author 2,432 (run jitter ~1%), ON 1,380 = author's, ratio 1.78× vs 1.76×, closure 97.1%, RSS@245k 1,253→945 MB (−24.6%), 2,097 B/binding vs 2,098. Instrument match to f80a: hist@174k 240,340 vs 241,552 (0.5%), gt1 30,065/30,064.
- Window sensitivity (140–245k, 150–240k, 160–220k, 170–210k, 125–245k, 200–255k): hist ratio 1.74–1.79, RSS ratio 1.65–2.01. The 1.76× is robust to the fit window.
- Patch applies clean at 9b0fdb9b, builds, `BELT_SPLIT` env-gated; OFF digits reproduce f80a's probes.

## Predictions

- Pre-registration genuine: predictions.md 17:04:16, smokes 17:05:39/54, dossier 17:10:34 (the decisive logs are the runner's regen, as designed).
- P1 held (first wave 110–125k vs OFF 11–16k; my 5×10⁴ arms: ON first wave 115k, OFF 15k). P4 held (held 521/521 at 245k, mints trajectories identical). P5 held (ON 975 MB at 275k; OFF 1,253 at 245k).
- **P2's letter failed** (1.76 outside [4,16], own falsifier <2 fired) — reported honestly as the run's content. **P3's letter failed identically** ("RSS slope divides by ≈S too (same band [4,16])": measured 1.86×) **but the dossier reports "P3 held"** — only the weaker re-reading (RSS tracks bindings) held. Misreported.

## Attack (adversarial, outside the author's range)

N = 5×10⁴, both arms, same binary (my pre-registered band: share law 1.92 in [1.6, 2.3]; ÷8 needs ≥ 4):
- OFF guard-stopped 180k gs (RSS 1,468), ON flew to 305k. Hist slope ratio **2.36** — ÷8 refuted a second time, harder; share-law direction confirmed (1.76 → 2.36 as belt share grows), but the formula underpredicts by 23%.
- Streams match the share law within 1–3% (OFF 3,272 vs 3,241 predicted; ON 1,642 vs 1,686) — the miss is in slope closure, which dropped to 88% (OFF, 1.4-wave window) and 74% (ON). The "slope IS the stream" identity holds to first order (74–97%), not to the precision the scaling column implies; wave-phase placement in short windows is the likely bias.
- Refusals 0, dead 0 both arms.

## Novelty

Holds. No f790/7f97/de7b/0659 entries in docs/HISTORY.md; the live nladder page has no split-memory pricing (f80a/b911 measured the channels, not the cadence lever's effect on channel 2). Nearest prior art is kick-cadence's 4e2d ledger ("one dial (split ≥ 21×) closes CPU and memory together" at 10⁹) — a composed assumption, never measured; this run measures the mechanism, confirms ÷S asymptotically at 10⁹ (share → 1), and corrects it at every mixed scene below. Not a repetition.

## The page

Faithful apart from three items, corrected in place: "the CPU crest halves" → ~20% on the author's own digits (237→190 ms, 213→175; regen ON even shows 237→158 — a drop, not a halving); missing `## Runs` line appended; a bracketed checker note with the 5×10⁴ result and the P3 letter failure added. The header's `updated:` conflict resolution is sound (body conflict f80a/b911 kept intact, per schema).

## Goal fit

Board items 1 and 4 (bodies 10⁶→10⁹; memory). Re-prices an adoption expectation before anyone pays for it — PRINCIPLES: "A failed expectation is not automatically a failed method: diagnose which one broke (H0183)" — done, and 33 ("each scale resolves only what matters at that scale"): the belt at 8× coarser cadence pays 8× less of both currencies only where it is the whole stream. Not gold: the headline law is post-hoc (the pre-registered band failed and the replacement was derived after seeing it), the compact-side τ ×8 is ledger arithmetic on another run's constants, and my second rung lands 23% off the formula with weaker closure.

## The one experiment for gold

Pre-register the share law at 10⁵ (predicted 2.63×) and fly both arms with wave-aligned windows spanning ≥ 3 full waves (guard raised for OFF), plus one second seed at 3×10⁴ (the author's disclosed gap). If the ratio lands in a pre-registered band around each prediction and slope/stream closure stays ≥ 90% at both rungs, the identity is flight-verified at two rungs beyond tuning and the scaling column's first entry is measured.

## What the author missed

- P3's letter failed, not held (the dossier's own numbers show 1.86 against the [4,16] band).
- "Crest halves" overstates the author's own digits (~20%).
- The share formula's precision at a second rung (2.36 vs 1.92 at 5×10⁴) and the closure drop (74–88%) — the scaling column is arithmetic on a law validated at exactly one scene.
- The kick-stream comparison uses a flight-wide average rate against a windowed slope (a small, undisclosed bias source).
- No `## Runs` line in the proposed page (schema).
