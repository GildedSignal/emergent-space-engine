Grade: lead

**Abstract.** Everything reproduces — all six digests byte-identical, timings within noise — but both central claims fail. First, the saved filter measures A at 1889 vs 1497 ns/item, 26% *slower*: it decodes every skipped pair for its self-check. The "445 vs 1495 (3.4×)" came from an unsaved self-check-free build (I measure 432 vs 1503 after deleting that block). Second, the kill's root cause is wrong: on the cited item j=16 the decoded |xj| sits *above* its key's periapsis — the band premise held. The real mechanism, new to HISTORY: `hit()`'s `cross*cross` overflows i128 and wraps, so the shipped finder reports phantom encounters — 22 of 69, and **all 19 plane contacts** (exact: 47/0). Adopt the engine bug, not the run's conclusions.

## What reproduces

- Clean tree + `work/patch.diff`, `cargo run --release -p emergent-universe --example enc_bench -- <scene> 48`: all digests match `heldout-final.txt` exactly (A `6f47379f…`, B `2adf5e51…`, P `222c2a06…`, HO3 `d5d4f5b6…`), encounter/contact counts match, timings within noise (A 1522 vs 1483–1515; HO1 1523 ≈ flat in N; decode share 91%). Kill-event reproduction with the saved filter (`round1-filter-encounter.rs` over `crates/universe/src/encounter.rs`): P → 47 vs 69 encounters, 0 vs 19 contacts, `UNSAFE SKIP: j=16 r_lo=1.4126e9 … x_hi=1.2426e9 margin=1.0765e8`, digest `f5dd7a47…` = `round1b.txt`; A skips 18424/18800 (98%), bit-identical; B +12%. Predictions discipline is genuine (`predictions.md` 14:44 precedes every measurement file; P2 held; P1's shortfall honestly reported).

## What fails

1. **The headline is not regenerable from the saved artifact.** The dossier: "code saved in `round1-filter-encounter.rs`; rebuilt from it to re-measure: A: 445 vs 1495 (3.4×)". Rebuilt from exactly that file: A = **1889 vs 1497 (+26%)**, matching `round1-final.txt` (1850 vs 1457), because the saved code runs the full decode self-check on every skipped item. 432 vs 1503 (3.5×) appears only after I delete the self-check block — a build variant that was not saved. Same defect as the silvers the taste log killed on 5 October: "results that the shipped code could not regenerate." Also `round1-final.txt` is a hand-stripped summary (no raw bench line contains those fields), and HO3 "+8%" is really +12.5% (mixed baselines: 3807 vs the *other run's* 3527).
2. **The root cause and boundary are falsified.** Decoding the very item the run cites: P j=16 `|xj| = 1.4135e9 > periapsis = 1.4126e9`. The "readout sits ~1.7e8 inside the key's periapsis" claim is wrong — 1.7e8 is the player-band gap (`r_lo − x_hi`), not a readout position; the author printed the player's norm, never j's. My adversarial belt `E09L` (pure test-particle ships about doll 0, e = 0.9, interval 2^30 — no secondaries anywhere) shows the identical failure, so "sound on test-particle tubes / broken only for secondaries" is wrong in both directions, and the proposed one-flag fix ("gate on centred-on-doll's-origin") fixes nothing.

## The real mechanism (checker's finding, new)

`hit` (`crates/lattice/src/law.rs:332`) computes `cross * cross` in i128. On the plane's own step (h = 2^40 doll time), cross ≈ 6.46e20 → cross² ≈ 4.2e41 > i128 max 1.7e38 → silent release-mode wrap → negative → `cross² ≤ rr·ww` passes. Verified in exact bignum: P j=16 and E09L j=73 both hit=false exactly, true as shipped. Quantified with a replay judge (f64 exact evaluation of the same integers, `enc_phantom`, deleted after use):

- P: shipped 69 encounters/19 contacts vs exact **47/0** — 22 phantom encounters and *every* contact is phantom, in the live player-encounter check (bottleneck #4's own seam).
- E09L: all encounters phantom (orig 16/4, exact 0/0).
- A, B, HO3: no overflow terms; the predicate is exact there, which is why bit-identity held on those scenes. Trigger: |d|·|w| ≳ reach²·2²³ after the `q_exp = reach.exponent() − 20` amplification — long intervals (the plane's step) or small reach.

Consequences: the filter's skips were geometrically justified everywhere measured (on P its 47 encounters equal the exact-truth count — the filter was right, the engine's predicate wrong); the pre-registered kill criterion fired on oracle noise. No HISTORY/docs entry records this overflow ("exact in integers" is claimed in `encounter.rs`); HISTORY's other overflow mentions (powered rotation `R^n` over i128, Q20 period overflow) are unrelated.

## Goal fit

The run targets a real, live bottleneck (HANDOFF #4, 190 µs/item) with the right method (exact pre-filter, bit-identity constraint, pre-registered kill). The instrument survives and is the seam's bench. But its deliverable — the falsified premise with its exact boundary — is itself falsified, and the headline cost is unregenerable: lead, kept. The gold it seeded: fix `hit()` (i256 cross, or a pre-scale/refuse guard when |d|·|w| could overflow), re-run this bench — the plane loses 22 phantom encounters and 19 phantom contacts per sweep, and the filter question can then be judged against a truthful oracle. PRINCIPLES 34, quoted: "the oracles are guards, not shepherds" — here the oracle was the thing that was broken.

## What the author missed

- The self-check's `actual_hit=true` is the same broken predicate it guards against — an oracle validated by itself. One decode print (`|xj|` vs periapsis) or one float cross-check inverts the whole conclusion.
- The saved artifact and the timed artifact differ (self-check decode); neither log nor dossier discloses it.
- `ns_per_item_median`/`p99` in the committed bench index an *unsorted* alternating-order vector (only `ns_orig` is sorted) — the labels are not quantiles; the alternating cold/warm cycle-memo effect is real but the fix to the statistic was not made.
- E09L-class scenes (long interval, eccentric sparse belts) were never tried; HO2-with-filter was claimed "measured" but no record exists (I measure 521 vs 3465, 6.6×, bit-identical — prediction HO2 would have held).
