# Predictions (written before the decisive arms: the S-sweeps, belt and formation)

Instrument: 9edc's print-only census (`ES_KICK_NEWS`; off = shipped path, flag-off arm reads
zero) extended for this run — mint kind split (birth / kick / other-rebind), a carried-kick
counter, and a shadow refcount of live intern keys (`(doll, mu, clockwise, OrbitKey)`, the tuple
`crates/space`'s own catalogue interns by) that counts every mint landing on a key another live
binding holds: the hit a key-dedup insert would score. Scenes: the formation = efd4's 512-ship
one-(E,L) fleet rebuilt to survive (1 AU, planet 2^-10 at 0.39 AU, ~22 Hill radii clear, no
conjunction in the window; smoke flight already run at S=7: births 513 mints / 511 cross = efd4's
standing number re-derived at mint level; first crest: distinct keys 2 → 323, cross_kick 0;
second crest: 513 distinct = full spread, 0 same, 0 cross) and the scatter control (512 distinct
orbits: birth_cross 0, kick cross 0 — the intern's null, smoke-flown). The dial is the shipped
`Config::step_log2` (the Δs octave de7b flew as `BELT_SPLIT`'s global form): each coarser octave
doubles Δs, so each fired kick carries ~2× the tide impulse and the fleet's key drift per mint
widens ~2×; each finer octave halves it.

- **P1 (the formation's kick mint is never intern-able, at any split):** `cross_kick = 0` at
  every S ∈ {5, 6, 7, 8, 9} on the formation. Mechanism: the tide's phase spread moves the 512
  ships' keys apart by many key quanta per kick (at S=7 the spread already exceeds the fleet's
  size within two crests); halving the drift (S=5) leaves ~2^? quanta of spread — I expect it
  still ≫ 512 buckets. Band: cross_kick/fired < 1e-3 at all S.
- **P2 (the belt's self-same fraction stays 0.000 at every split):** `belt_same = 0` at
  S ∈ {5, 6, 7, 9} on `nladder 10000 coast 150 1800`. Coarser S grows the per-kick dv (2⁻²³·v at
  shipped → 2⁻¹⁹·v at S=9) — same-key can only appear on the FINE side, where the belt's
  dv/kick shrinks to 2⁻²⁵·v at S=5; the key resolved 2⁻²³·v with zero same in 2M kicks (9edc),
  so a flip needs the key's periapsis quantum to sit in the narrow [2⁻²⁵, 2⁻²³]·v δa band. I
  predict it does not. Falsifier: belt_same > 0 at any S.
- **P3 (carried kicks):** `notfired ≈ 0` at every S on both scenes (the belt's fired impulses
  were ≥ 2⁷ word units at S=7; two octaves finer still leaves ≥ 2⁵ — the carry never engages).
- **P4 (the mint-rate law):** fired kicks per body per game-second scale ≈ 2^−(S−7) (de7b's
  cadence law), so minted bytes per body per interval halve per coarser octave with no
  content-side rescue: the dial collapses the mint by RATE only.
- **P5 (held-out, cross-scene):** the formation's numbers at S=8 and S=9 (unflown anywhere) sit
  on the same laws: distinct = live within three crests, cross 0; the belt at S=6 (a cadence
  de7b flew, never censused) reads 0 same with ~2× the shipped fired count of S=7's window.

**Kill criterion for the coupling dial (the checker's own):** if same-key mints (self or cross)
appear at some split S — belt_same > 0, or formation cross_kick/fired > 1e-3 — then the mint
collapses by a measured dial: report S*, the fraction, and the mint-bytes curve; the dial is
adoptable in one step. If no S in {5..9} shows one on either scene, the resolution-coupling hope
dies: no cadence value makes the kick mint intern-able, and the memory ratchet must delete the
mint outright (the intern pays at births under concentration — measured 511/513 here — and the
cadence pays by rate, also measured).

**What would make a number suspect:** `dead > 0` on the formation (a death changes the standing
stock mid-census), `apply ≠ fired + handoffs + carries` accounting drift, `shadow_keys ≠
distinct` from the independent end-of-flight census (two instruments must agree), or the flag-off
arm reading nonzero.
