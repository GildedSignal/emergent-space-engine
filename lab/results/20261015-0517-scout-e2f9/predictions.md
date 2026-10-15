# Predictions (written before the first flight of the rebuilt seam)

The seam is rebuilt from the design description (b9ae's silver record named this build as the one
experiment between it and gold): `EntrySlot::Live/Demoted` on `Binding.entry`, demote-after-kick
through a settle queue in `apply` (`ES_LAZY`), promotion (re-mint by pure `Orbit::compile(key)`) at the
`BodyStore` boundary, and — new this run, b9ae's named fix — retention (`ES_LAZY_RETAIN`): the minted
entry is cached until the body's next rebind, so one promotion per kick instead of one per read.

Nothing below has been tuned on; the code has compiled and never run.

1. **Digest identity (the certificate).** On every arm — 10⁴ coast, 10⁵ coast, 10⁴ burn (forward L8),
   and held-out seed 7 at 10⁴ coast, 48,000 game-s cut, canonical `settle(cut)` instrument — the
   digest is bit-identical across the three processes: seam off, `ES_LAZY=1`, `ES_LAZY=1 ES_LAZY_RETAIN=1`.
   Ground: 760f's 120,083/120,083 recompile bit-identity and b9ae's four-arm control-vs-lazy identity.
   **Kill:** any mismatch in any arm — the seam as rebuilt is not outcome-free and the run reports it
   as failed.

2. **The retention fix moves the wall, not the digest.** As flown by b9ae (re-mint every read), wall
   at 10⁵ coast is 1.3–2.0× the off arm (they measured ×1.5–1.9 on a shared box). With retention it
   falls back to within ~1.1× of off. The digest does not move in either.

3. **Promotions per demotion.** No-retain: of the same order as b9ae's 8.7–23.2 (several reads per
   event chain, each a fresh mint). Retain: ≈ 1 (one mint per kick, cached until the next rebind),
   within 0.5–2.0.

4. **Memory.** At 10⁵ coast, rss at the cut drops by roughly a quarter to a third with the seam on
   (b9ae: 545→377 MB, −31%), with or without retention (the cache holds only bodies read since their
   last kick; the coast flight reads almost none between kicks). The burn arm drops less (the player's
   own doll and passages never demote).

5. **Held-out seed 7** (never flown here before this file was written): identity holds; counters and
   memory in the same ranges as seed 1.

6. **Passages and plunges never demote** (the burn arm flies the player through the star's doll): the
   demotion counter at 10⁴ burn stays well below the kick count of the belt bodies alone, and the
   digest is identical — a passage demoted would move it or refuse.
