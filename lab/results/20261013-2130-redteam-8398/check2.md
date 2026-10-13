Grade: gold

**Abstract.** Claim: the order boundary (tube→Cartesian→tube, `Rebinding::from_state` behind
`resolve_handout`) changes the law-level `OrbitKey`, so "both orders, identical bits"
(representation.md §3, law.md:51, B8) fails at the seam both orders share. Reproduced
bit-identically from `work/patch.diff` on base 294215b: 0/112 transits keep the key, circles
lose their exact class (dk = 2^19 Q48 ulps), no fixed point. My attacks extend it:
64-transit chains never repeat a key and drift one-signed at fine words (−1 k-ulp per
transit — directed, not diffusive); the leak persists at p = 10^4–10^7, retrograde sense,
and unbound passages (k word stable, periapsis word walks). 152f's 0.0 memo-hit on 3,108
rebinds corroborates. Page corrected in place (11/11 not 12/12; one unregenerable number
replaced). Cost to adopt: tube-carry or entry-snap, freeze r5 — one step.

## Reasons

**1. Reproduction.** `git apply work/patch.diff` on the base commit (294215b, matches
`base`), `cargo run -p emergent-space --release --example transit_roundtrip`: output
differs from the stored `transit.tsv` by **zero lines**. Summary `0/112 round trips kept
the key; 10 refused`, negative control (one velocity ulp moves the refit) passes, circle
rows show dk = 524288 = 2^19 Q48 ulps = 2^−29 relative, the e = 0.9 fixed-point row shows
dang = 4294967295 (u32 wrap-by-one), residual2 ≈ 2.9×10⁻⁹ relative at the 2^60 fine-word
scale. All dossier headline numbers regenerate.

**2. Premise is the shipped path.** `resolve_handout` (universe.rs:743) → `bind_surface`
(bind.rs:224) → `Rebinding::ending_at`/`from_state` (bind.rs:265-266): the engine re-fits a
decoded member state on every fleet hand-out. `OrbitKey` derives `Eq + Hash` over
(periapsis, k, null, gap) — key identity *is* Catalogue/memo identity, so "key moved"
means a different compiled orbit, not a cosmetic word change. The circle-class mechanism is
real: `inverse::circular` demands exact BigInt identities (x·vx + y·vy = 0 and vv²·ss = 1),
which decode rounding generically breaks.

**3. Predictions.** `predictions.md` exists (21:37, before dossier 21:42). P1 half-failed
toward the attack (circles do *not* round-trip — stronger than predicted); P2 held; P3 held
in direction. P5's positive control failed and was reported as the finding rather than
declaring the probe VOID — the fixed-point control taking its place is a fair substitution,
and the failure direction (P1) is evidence the file was genuinely written before the run.
Caveat: the runner's regen overwrote the original raw table (transit.tsv 21:43); mitigated
by the bit-identical re-reproduction.

**4. My attacks (4; A2 outside the author's range, p ≤ 1000).** Probe archived as
`work/check2-attack.rs`.
- **A1, depth-64 chains (author measured 2 steps):** no key ever repeats on six
  configurations — no fixed point, no cycle. At fine words the walk is **directed**:
  64/64 steps one-signed at (8, 0.5), net −64 k-ulps after 64 transits (~−1 ulp per
  transit, a floor bias). At plane-scale coarse words: +7.0×10^7 ulps over 64. The
  compounding is systematic, not diffusive — worse than the dossier claimed (principle 13
  exactly).
- **A2, p = 10^4–10^7 (0/26 kept):** the relative step shrinks (2^−50-ish at 10^7) but the
  key never survives; at (10^6, 0.9999) the k word even stays put while the key still
  differs — the periapsis word walks. The leak is full-key, not k-specific.
- **A3, retrograde (clockwise = true; author tested prograde only): 0/14 kept.**
- **A4, unbound passage branch:** key changes with dk = 0 (periapsis word moves); the
  steep boost refuses `NoBoundOrbit` — `ending_at`'s domain, disclosed as a refusal.

None of the attacks rescues the premise; each widens the breach.

**5. Novelty.** The handoff wiki page (11 runs) covers root-clock keys, the doll surface
predicate and the tide payload — never the tube↔Cartesian fit round trip. kick-jet's 152f
measured the *cost symptom* (exact-key memo hit 0.0 on 3,108 rebinds) without the
mechanism; the composition here is sound. No HISTORY entry measures transit identity.
`lab/rungs/` has no r5 (verified), and `identity.rs` compares Chronon vs EventCore without
any hand-out crossing (verified — no handout references). New topic page justified.

**6. Page.** Corrected in place: "12/12 keys" → 11/11 (three high-eccentricity keys refuse
silently in the control loop, plus the separatrix compile-refusal — the control's printed
rows are 11); the unregenerable "~24 M at (p 20, e 0.7, 3/4)" replaced with table-backed
numbers (that row's coarse dk = 655665 Q48 ulps ≈ 2^−28.7 relative; the table's max fine
future divergence is 1.92×10^11 ulps at (8, 0.99, 3/4), ~9× the cited row); domain extended
to p = 10^7 and depth 64 with the directed-walk result. Not three gold runs agree — the
topic stays open.

**7. Goal fit.** This is a premise kill on the truth rule itself: "Laws are versioned.
Canonical outcomes are exact and independent of cache, **partition**, observation, schedule
and hardware" (AGENTS). Principle 13: "errors never compound … divergence is not a joke and
it compounds" — measured as a directed, non-converging walk. Principle 19: "a fix signals
the wrong representation" — the residual layer is doing rearguard duty at a seam no
representation was chosen for. The cost half (per-transit compile 5.8–374 µs, corroborated
by 152f) ties it to the frame-cost lever. Adoptable within one step: two named fixes with a
ready negative control (shipped `from_state` fails by ≥ 1 key ulp).

**Dossier prose nits (not grade-changing, all disclosed or minor):** "10/122" refusals
bookkeeping vs the machine summary (10 refused within the 112 counted); "three decode
overflows" undercounts (10 cartesian refusals across 4 (p, e) keys at fine words); "B8's
engine tests stay inside one order's law" is loose shorthand — identity.rs does compare both
orders, just never across a hand-out (the dossier's own parenthetical is exact).

## What the author missed

- The walk is **directed** at fine words (one-signed, ~−1 k-ulp per transit) — linear in
  transit count, not a random walk; and it never cycles to depth 64. "Unmeasured beyond
  step 2" was the right instinct; measuring it made the finding stronger.
- The leak is not k-specific: at large p, extreme e, retrograde and unbound passages the k
  word can be the stable one while the periapsis word walks. Any fix that only stabilizes
  k misses the full-key identity.
- The fixed-point control silently skips refusing keys (11 rows, not 12) — a control that
  cannot run on part of the grid is a weaker instrument than it looks.
- One derived number ("~24 M") was not regenerable from the stored log; the table's true
  worst row is elsewhere.
- Still unmeasured (named by the author, confirmed open): an end-to-end `resolve_handout`
  scene through `bind_surface`'s unit rescaling (strictly lossier than the idealized probe,
  so the direction favors the claim), and the canonicity of the Knudsen order assignment
  itself.
