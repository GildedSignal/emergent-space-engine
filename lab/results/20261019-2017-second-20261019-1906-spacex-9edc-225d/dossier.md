# The mint's only duplicate is the birth: the checker's named experiment kills the resolution-coupling dial at every octave

## Claim

The checker's one-experiment-to-gold is run whole, and it lands on its second branch: **no
cadence value in the flyable range makes a kick mint intern-able — the flip fraction is 1.0000
at every Δs octave flown (4× coarser to 4× finer than shipped, both scenes, self and cross), so
the coupling dial dies and the memory ratchet must delete the mint outright.** On the co-orbital
formation (efd4's 99.6% case, rebuilt to survive) the standing duplication is a **BIRTH-only
property**: 513 birth mints land 511 on an existing key (99.6%; 2,047/2,049 = 99.9% at 4×
fleet), and **one kick per ship evaporates it** — distinct keys 2 → 323 → 513 within two
crests, after which every kick mints a key no live binding holds (cross_kick = 0 in 54,783
formation mints across five octaves; 0 again in 29,724 at 4× fleet). On the belt the same
census reads **0 same and 0 cross in 1,102,700 fired kicks across four octaves** (19,637 /
48,548 / 91,709 / 96,364 belt-fired at S = 5/6/7/9; tube 0 same in 1,043,306), including the
finest cadence ever flown (dv ≈ 2⁻²⁵·v per kick — the key still moves every time), with the
shipped S=7 arm reproducing 9edc's record arm (91,709/406,387 against its 92,737/407,984, the
same load-spread class). Mint rate is exactly the cadence law (formation: 1,921 / 3,719 / 7,432
/ 14,917 / 29,794 fired = 2.00× per octave), so the dial collapses the mint **by rate only,
never by content**. What an intern can delete is measured precisely: the birth mint under
concentration (Δs-independent — a spec compile, not a fit), plus efd4's corpse term; the kick
mint's ~688 B + table per few bits of news is the representation error the ratchet must delete
outright.

## Bottleneck

Memory at 10⁹ (the board's fourth live question) and the 9edc handback: whether the Δs/cadence
dial (`BELT_SPLIT`'s lever) couples the kick's dv quantum to the key's grid tightly enough that
same-key mints appear and the mint collapses. Expected gain: not a speedup — the decisive
premise check the checker named, on the two scenes that could disagree (concentration vs belt).
It kills the resolution-coupling direction across its whole flyable range and re-scopes the
intern to births.

## Evidence

Binary: shipped tree + `work/patch.diff` — 9edc's print-only census (`ES_KICK_NEWS`; off = the
shipped path, flag-off arms read every counter at zero on both scenes) extended with: mint-kind
split (birth / kick / other-rebind), a carried-kick counter, and a **shadow refcount of live
intern keys** (`(doll, mu, clockwise, OrbitKey)` — the tuple `crates/space`'s own catalogue
interns by) that scores every mint landing on a key another live binding holds: the exact hit a
key-dedup insert would ask, which the shipped catalogue cannot (no lookup; `cat_inserts` =
fired + handoffs exactly, re-confirmed). Two independent instruments agree everywhere
(`shadow_keys` = the end-of-flight distinct-key census = `cat_live` on every arm). The dial is
the shipped `Config::step_log2` via `ES_STEP_LOG2` — de7b's own octaves, the global form of the
`BELT_SPLIT` lever (S=5 is exactly the split-8 bulk effect, 4× coarser; f790 proved the split is
this lever per body). **Label correction, reported honestly: `step_log2` counts kicks per
period, so S=9 is the FINE side** (my predictions.md had the fine/coarse labels inverted; the
flown set {5,6,7,9} spans both directions regardless, and every prediction is evaluated on the
physics, not the label).

Formation (efd4's fleet rebuilt to survive: 512 ships on one circular orbit at 1 AU, one exact
(E,L), 512 phases; planet 2⁻¹⁰ at 0.39 AU ≈ 22 Hill radii clear, no conjunction in the window;
dead 0, handoffs 0, refusals 0 on every arm; 500k game-s ≈ 15 intervals at shipped):

| S (Δs) | fired | same | flip | cross_kick | birth mints | birth cross | distinct end |
|---|---|---|---|---|---|---|---|
| 5 (4× coarse) | 1,921 | **0** | 1,921 | **0** | 513 | 511 (99.6%) | 513 |
| 6 (2× coarse) | 3,719 | **0** | 3,719 | **0** | 513 | 511 | 513 |
| 7 (shipped) | 7,432 | **0** | 7,432 | **0** | 513 | 511 | 513 |
| 8 (2× fine) | 14,917 | **0** | 14,917 | **0** | 513 | 511 | 513 |
| 9 (4× fine) | 29,794 | **0** | 29,794 | **0** | 513 | 511 | 513 |
| scatter control | 7,661 | **0** | 7,661 | **0** | 513 | **0** | 513 |
| 4× fleet (S=7) | 29,724 | **0** | 29,724 | **0** | 2,049 | 2,047 (99.9%) | 2,049 |

Divergence dynamics at shipped: after the first crest distinct = 323 = 321 kicked ships + the
shared birth key + the planet — **every kicked ship's new key is unique on its first kick**;
full spread (513) by the second crest. The rate law is exact: 1,921 → 3,719 → 7,432 → 14,917 →
29,794 = 1.94 / 2.00 / 2.01 / 2.00 per octave.

Belt (9edc's own scene, `nladder 10000 coast 150 1800`, 9,700 belt bodies + locals):

| S | belt fired | belt same | tube fired | tube same | clock fired, same | birth cross | cat_inserts | notfired |
|---|---|---|---|---|---|---|---|---|
| 5 (4× coarse) | 19,637 | **0** | 102,860 | **0** | 38, **0** | **0** / 10,076 | 122,553 | tube 423 |
| 6 (2× coarse) | 48,548 | **0** | 204,950 | **0** | 80, **0** | **0** | 253,596 | tube 319 |
| 7 (shipped) | 91,709 | **0** | 406,387 | **0** | 154, **0** | **0** | 498,268 | tube 283 |
| 9 (4× fine, truncated 5,278 frames) | 96,364 | **0** | 429,109 | **0** | 35, **0** | **0** | 525,513 | tube 475 |

- Accounting exact on every arm: `apply_kick` = clock + belt + tube fired; `cat_inserts` =
  fired + handoffs (9edc semantics preserved); `shadow_keys` = `cat_live` = bodies + 48;
  `self_ok=1`; dead 0; flag-off arms (both scenes) read every counter at zero with the flight
  intact.
- The carry engages only marginally and only on the tube path (283–475 per arm, ≤0.5% of tube
  kicks); the belt and clock paths never carry at any octave — 3294's fire-rate-1.000 extends
  across the dial.
- The fine side's memory bill, measured: end footprint 58 → 61 → 68 → 119 MB across S=5→9 —
  minted history (retired `Segment`s hold their `Arc<Entry>` alive) grows with the mint rate;
  the mint's bill is not only the standing slot.
- Sizes (printed by the probe): `Binding` 192 B, `Entry` 288 B, `Segment` 208 B (+ the shape
  table per compile) — ≈688 B + table minted per fired kick, for ~log₂(1 dv quantum) ≈ a few
  bits of news (9edc's arithmetic, now at every octave).


Reproduce: `lab/results/20261019-2017-…-225d/regen.sh` (build + all arms above + controls,
~5 min warm end-to-end, verified: every zero and every formation number regenerates — the
formation digests are bit-identical run-to-run, and the flag-off arm's digest equals the
flag-on S=7 arm's (`7029bca3…`): the census is digest-neutral, not just counter-zero; the
belt arms' fired counts move ≤0.4% on the untruncated windows (91,709 → 91,310 at S=7) and
the truncated S=9 arm banks 91,984–96,364 mints depending on load — zeros unchanged; every
number is in `work/*.txt`).

## Predictions

`predictions.md` was written before the decisive arms (the S-sweeps; the S=7 formation smoke and
both controls predate it and are marked there). **P1 held** (cross_kick = 0 at every S, band
<1e-3, measured 0). **P2 held** (belt_same = 0 at every S, both scenes — including the fine
side once the label is read correctly). **P3 held** (notfired ≈ 0: belt and clock exactly 0;
tube ≤0.5%). **P4 held** (rate 2× per octave, measured exactly on the formation). **P5 held**
(S=8/9 formation and S=6 belt sit on the same laws). The pre-registered kill criterion fired
its second branch: no same-key at any flown split ⇒ the coupling dial dies; the memory ratchet
must delete the mint outright. The label inversion (fine/coarse) is a reporting error in
predictions.md, corrected here; no prediction changes sign under it.

## What would make it wrong

- The shadow intern scores a hit only against LIVE bindings (deaths keep their key, mirroring
  the shipped corpse retention); if the engine ever releases on death, birth-cross under
  concentration rises slightly — the kick-side zero cannot become nonzero by that.
- The flown range is 16× in Δs (S=5..9); a same-key regime could exist beyond it (S≥10: dv ≈
  2⁻²⁷·v per kick — but S=9 already shows the key resolving 2⁻²⁵·v with zero same, and finer
  cadences are memory-dominated: the 119 MB fine-side bill). The formation's per-kick tide is
  ≈2⁻¹⁴·v by design against the belt's measured 2⁻²³·v (~500×): a fleet in a much weaker tide
  at the same cadence sits nearer the key's grid — the scatter control (distinct orbits) and
  the belt (the weakest tide flown) bound that side at zero.
- The formation has no conjunction inside its window (synodic 5.6×10⁶ game-s > 5×10⁵ flown):
  encounter-driven rebinds (news by construction) are out of scope; the belt arms carry the
  stirred-stream case. A Trojan (L4/L5) formation — the one case whose tide's phase-average
  could cancel — is unflown.
- efd4's intern adoption needs its own digest-identity flight (its dossier names it); this run
  prices what it would hit, it does not fly the intern.

## Cost of adopting, and fit with PRINCIPLES

The premise correction is free: the resolution-coupling direction is dead — no `BELT_SPLIT`
value need ever be evaluated for mint-sharing again. What the record now supports: (1) efd4's
30-line intern for the birth mint under concentration (99.6–99.9% measured at mint level,
Δs-independent; the birth compile itself measured 13.0–13.7 µs/ship on this box, inside efd4's
16.4) and the corpse term — unchanged; (2) the cadence dial for mint RATE (2× per octave,
exact), with the fine side priced (footprint doubles at 4× finer); (3) the kick mint itself is
the deletion target: ~688 B + table per few bits, at every cadence. PRINCIPLES: "Compute only
surprises" (P3) — the kick stream surprises every time, at every octave, self and cross; "The
memory floor is information" (P24) — the mint's floor is bits, its bill kilobytes, and no dial
closes that gap; "A fix signals the wrong representation" (P19) — the fix is not a dedup
catalogue on kicks (it would hit nothing anywhere flown) but the mint's deletion.

## The lens

The second-author lens ran the checker's named experiment verbatim and reports both halves
dead-on-arrival for the coupling hope: same-key never appears, and the formation's celebrated
99.6% is a birth property that one kick erases. What this lens may have missed: the census
prices mints, not compile CPU (the intern would also delete 511 of 512 formation birth
compiles); no arm flies a moving lens (B16) or the Trojan formation; and the belt S=9 arm is
delivery-truncated (its census stands — 96,364 belt mints banked — but its rate is a lower
bound).
