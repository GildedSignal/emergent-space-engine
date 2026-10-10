# Dossier — 20261010-1407-inversion-5c2a (lens: inversion)

**Claim.** The phase-neighbour certificate adopted from gold `20261006-0346-taleb-09b5` (build
`lab/lenses/b-coorbital-cert.md`, queued on both the GLM and Codex lanes) fails its own contract
("zero misses at O(n·k)") on the scene it was adopted for — concentrated *fleets*: with two
co-orbital fleets whose orbits cross, it drops 82–100% of real contacts at every practical window,
and even the most favourable (merged-order) variant needs 519 certificates per real encounter —
14× the quadratic tier it replaces — to reach 99%, not zero, misses.

**Bottleneck.** Board item "encounters at N / the co-orbital certificate" (HANDOFF "Risks to
attack first": candidate work at scale). Inverted the newest adopted gold instead of building on
it: what does "every real encounter lies within partner rank 4 along the orbit" silently assume?
Answer: **one population, and a cold one** (e ≈ 0 so mean-longitude order is stable). The build
spec's test list ("the gold run's scenes and a dense ring") bakes both assumptions in.

## What actually breaks, in three measured layers

1. **Cross-group contacts are structurally invisible.** Two fleets, each with the gold's own
   concentration (Δa/a = 2e-4, twice the gold scene's width — any period-concentration trigger
   that fires there fires per fleet here), orbits crossing through e-spread (σ_e = 0.04): 43.7%
   of all truth encounters are cross-fleet. A per-group phase rank cannot see them at any window
   length: coverage ceiling = intra fraction = 56.3%. The game's fleet-meets-fleet battle is
   exactly this scene. The design dilemma: keep inter-group windows and the quadratic tier
   returns precisely for battles (two 10⁶ fleets → 10¹² window pairs, the gold's 40 TB); drop
   them and 43.7% of contacts vanish silently.
2. **Even intra-group, rank stability is a property of e ≈ 0, not of concentration.** At σ_e =
   0.04 the equation-of-center difference oscillates the partner's true-longitude offset by
   ~4e ≈ 0.16 rad per orbit ≈ 7.6 mean spacings (n = 300): per-group coverage of intra events is
   28% at W = 1 orbit and reaches 100% only at W = 0.05 orbits (519 certs/enc). The gold's belt
   had e = 3e-4 → oscillation 6e-4 rad ≪ spacing: that is why rank 4 held there. Scaling inverts
   it: at 10⁶ ships in one annulus the spacing is 6.3e-6 rad, so any e > 1.5e-6 breaks rank 4
   within one orbit. A fleet under thrust (the game's wildcard) has e where it likes.
3. **Retrograde (counter-orbiting fleet):** measured 71,923 encounters, **96.4% cross-sense**;
   head-on geometry makes the battle also the *densest* encounter scene (15.5× the prograde
   two-fleet count at identical density and ρ). Per-group ceiling = 3.60% (= the intra
   fraction); windowed per-group coverage 1.0–1.2%. Even the merged order — salvageable at
   ~500 certs/enc for prograde fleets — stays at 1.3–7.5% for W ≥ 0.05 orbits: the partner
   sweeps relative longitude at ~2n, so rank 4 (spacing TAU/600) pins the window to
   W ≈ 3×10⁻³ orbits, ~500 certificates per encounter against a quadratic tier that here
   touches 2.4 pairs per encounter — 200×, and still not zero misses.

## Evidence (all runs ≤ 12 s, 4 threads, < 100 MB; Linux x86 cloud — orders of magnitude only)

Truth = the crate's own `truth_pair` (conservative advancement, every radially overlapping pair
at 2ρ margin, local minima below ρ), **unmodified** for CTRL/FLEET2; RETRO uses a mirrored-state
copy (mirror preserves rmin, hence the same Lipschitz bounds) — `crates/encounters/src/bin/invert.rs`.
Instrument checks: CTRL reproduces the crate's published evidence bit for bit (same spec+seed
20261010 → 2093 encounters = `truth_enc: 2093` in `artifacts/evidence/opus-encounters-20260930/verify.jsonl`);
zero duplicate (pair, t) events in any scene; events are distinct local minima (max 99/pair over
50 orbits ≈ 2/orbit, the shearing-pair rate). Coverage counted per event; a pair counts covered
only in windows where `min(rank_i→j, rank_j→i) ≤ 4` (either side monitoring suffices — the
favourable reading). Rank by **true longitude** (mean longitude is wrong at e = 0.04:
equation of center = 0.08 rad = 80× the encounter scale).

| scene | enc | cross | dup | pairs (quad. tier) | best per-group cov. | merged cov. @W=1 | merged @W=0.05 |
|---|---|---|---|---|---|---|---|
| ctrl (gold's, seed 20261010) | 2093 | 0% | 0 | 44,850 | **100%** (W≤10; 2.9 certs/enc) | 100% | 100% |
| fleet2 (seed 20261011) | 4623 | 43.7% | 0 | 171,049 (37/enc) | 56.3% ceiling; 16–17.6% at W=1–10 | 15.6% (26 certs/enc) | 99.0% (519 certs/enc) |
| retro (seed 20261012) | 71,923 | 96.4% | 0 | 169,431 (2.4/enc) | 3.6% ceiling; 1.0–1.2% at W=1–10 | 1.28% (1.7 certs/enc) | 7.51% (33 certs/enc) |

Kill criterion (fixed in predictions.md before the run): broken if, at every window with ≤ 200
certificates/encounter, FLEET2 coverage < 99%. Measured: at ≤ 26 certs/enc coverage is ≤ 17.6%
(per-group) / 15.6% (merged); 99% needs 519. **Broken, decisively — and RETRO is worse still.**
VOID conditions checked: CTRL rank@event = 100.00% ✓, duplicates = 0 ✓.

## Predictions (predictions.md, written before the run)

Held: CTRL 2093 enc (predicted 1500–3000; and exactly the crate's 2093), 100% rank@event;
FLEET2 4623 enc (predicted 1000–5000), ≥95%... measured 43.7% cross — **miss**: I predicted
cross-dominance, but intra e-crossing encounters (2602) outnumbered my drift-based estimate
(0–100) — the intra layer (finding 2) was a genuine surprise, found only because the truth was
run, not modelled. Merged coverage at W=1 ≤ 10% predicted, 15.6% measured (direction held,
magnitude slightly high). 99%-needs-W≤0.05 with ≥10³ certs/enc predicted: W=0.05 held, certs 519
(half the prediction; same order). Kill verdict held. RETRO: per-group ≈ 0% predicted
("0% as in FLEET2"), measured ceiling 3.6%, windowed 1.0–1.2%; merged at W = 1 orbit ≤ 5%
predicted, 1.28% measured — both held.

## What would make it wrong

- The concentration trigger could be defined to include an e-spread term (then it simply does
  not fire on warm fleets — but then nothing replaces the quadratic tier for them, which is the
  adoption's whole purpose; and my layer-1 cross-group argument survives any per-group trigger).
- If groups-as-meta-bodies between co-orbital groups is already the intended design (it is not
  in the spec or the gold's text: "replaces the quadratic tier"), layer 1 is already handled and
  only layer 2 (e-spread re-ranking, the window cost) remains.

## Cost of adopting the fix, and fit with PRINCIPLES

The fix is scoping, not mechanism: the certificate stays O(n·k) *inside* each cold co-orbital
group; between groups the existing pairwise tier runs on **group envelopes** (O(C²) in the number
of groups; two fleets = one envelope pair), refining only where envelopes overlap; the trigger
must be per-group and must gate on the group's e-spread vs k×spacing (4e < k·2π/n), with rank by
true longitude and window ≤ spacing-sweep/4e. One sentence in `b-coorbital-cert.md`'s test list:
add two-fleet and warm-fleet (σ_e = 0.04) scenes with an independent truth. Fit: "Compute only
surprises" and "the right representation" — the certificate is the right representation for
*one cold population*, and only for that domain; "a failed expectation is not automatically a
failed method" (H0183) — this kills the configuration "phase rank replaces the pairwise tier
under concentration", not phase rank itself.

## The lens: what inversion may have made me miss

I attacked the newest adopted gold and its pending build, not the older two-tier silver
(q-candidate-degree) whose window tier may already handle cross-group pairs by construction
(envelope overlap) — if so, the correct statement is "the certificate must not *replace* the
tier between groups", and the build spec's "replaces" is the one wrong word. I did not test 3D
mutual inclination (the crate is planar; crossing planes should behave like my crossing
e-ellipses but with the whole orbit plane as the crossing set — likely worse). Single-seed per
scene; the effects are structural (partner outside the ordering set; oscillation amplitude vs
spacing), not seed-sensitive, but the checker should vary seeds. Cloud/Linux timings, orders of
magnitude only.

## Reproduce (each ≤ 60 s)

```
cd crates/encounters
CARGO_TARGET_DIR=/tmp/invert-target cargo build --release --offline --bin invert
/tmp/invert-target/release/invert ctrl   > $R/ctrl.jsonl    # 1.9 s
/tmp/invert-target/release/invert fleet2 > $R/fleet2.jsonl  # 8.7 s
/tmp/invert-target/release/invert retro  | gzip -9 > $R/retro.jsonl.gz  # 11.7 s (raw 6.0 MB > 5 MB cap)
python3 $R/analyze.py $R/ctrl.jsonl $R/fleet2.jsonl <(zcat $R/retro.jsonl.gz)
```

`invert.rs` and the Cargo.toml `[[bin]]` entry are in this tree (saved as the run's patch);
`analyze.py`, `predictions.md` and the `.jsonl` outputs are in this folder.
