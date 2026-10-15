# Predictions (written before the decisive matrix)

Topic: nladder, open direction 4 — the checker's named gold experiment for 20261015-1615-spacex-1343:
fly the demote-passages variant of the lazy-entry seam digest-identical, and price its bill.

The variant (`ES_LAZY_ENTRY=1 ES_LAZY_PASSAGES=1`): a kick-settled Passage binding keeps
`key + outer_radius + sense/unit` (measured record: 113 B; the slot 128 B) and reads re-mint
through the pure `Passage::compile(key, outer)`. Arms: ctl (nothing demotes), seam (cycles
demote, passages never — the rule as e0f9 flew it), variant (passages demote too).

Scenes: the standard ladder (1000 coast, 10000 coast, 10000 burn; cut 20,000 game-s, rtf 1000,
seed 1 — e0f9's arms) and the comet stream at rtf 100 (player pace): comet (500 at peri 1.2 AU,
w≈14 minted), stargraze (500 at peri 0.006 AU = 1.3 R_star, w≈20 minted), mixed (500 + 500),
all cut 1,200 game-s, seed 1.

- P1 (identity, the decisive one): `Universe::digest()` at the canonical cut is bit-identical
  across ctl, seam and variant on every scene. Any mismatch on any scene kills "demotion
  extends to passages": the never-demote rule is then load-bearing for correctness, and this
  run reports the refutation.
- P2 (the seam is still the seam): on the standard scenes the seam and variant arms reproduce
  e0f9's published counters (10^4 coast cut 20k: demotions ≈ 41,053, digest
  `5e8c9e24…fbab6f`), and the ctl digest equals it too — my merged patch (seam + comet
  plumbing + census) must not perturb the shipped plane. The variant's passage demotions on
  standard scenes are the planes' own flyby passages: O(10²) over 20k game-s, not zero.
- P3 (the bill's shape, comet scenes): passage promotions ≈ 4–8 per passage demotion (the read
  multiplier of an unbound body — always a scan candidate), compile p50 300–500 µs at the
  1.2 AU class (w 10–14) and 500–900 µs at the star-grazing class (w 16–20), p99 within 1.3×
  of p50. The re-mint compile time dominates the variant's wall on comet scenes.
- P4 (memory): on comet scenes the variant's census holds ≈ zero standing passage arcs for
  kick-settled comets (only never-kicked birth arcs and the plane's own flybys stay), its rss
  ≤ half the ctl arm's, and ctl's standing arcs match the run's curve: ≈ 18.8 kB × alive
  comets (1.2 AU class) and ≈ 25–26 kB × alive (star-grazing class) — the corrected worst
  case folded into the working-set arithmetic.
- P5 (the record): the demoted-passage record is 113 B (OrbitKey + outer Scalar + sense +
  unit), so the retention arithmetic for a demoted passage is ~113 B against 18.8–25.7 kB
  standing — the 166–227× range, not 1343's 157×.

Kill criteria: P1 failing is the kill of the claim (reported as the refutation, not a void).
P2 failing on the ctl digest means my merge broke the plane — stop and fix before any comet
claim. P3 off by > 2× in either direction: report the measured multiplier and p50 as the
result, and name what the model missed. P4's rss clause failing (variant rss > ctl) while P1
holds: the arcs are deleted but something else pins memory — diagnose before claiming the win.
