# Predictions — 20261015-1926-taleb-d6ba

Question: on the seam adoption candidate (`ES_LAZY_ENTRY` [+ `ES_LAZY_PASSAGES`]), what owns the
belt's standing compiled-arc store at depth, and is it bounded (a floor) or growing (a leak)?
Instrument smoke (10⁴ coast, cut 5k — BEFORE the first kick settle, so not the decisive domain):
current bindings 97% Live (9,791/10,049), all 8,446 apply-mints demoted, history 679 segments,
plunges 0, dead 27 holding 11 arcs. Bodies are born Live and demote at their first kick settle
(kick_len ≈ 5.35e9 ticks ≈ 26k game-s ≈ one belt period).

The decisive matrix (not tuned on): 10⁴ coast at cuts 20k/48k/96k (seam + variant; ctl at 20k),
10⁴ burn 20k/48k (variant), 10⁵ coast 20k (variant), mixed comet 1000 at 1.2k and stargraze 500
at 4.8k (variant), held-out seed 3 on 10⁴ coast 48k (variant).

- **P1 (the depth collapse):** by 48k (≈ 2 kick-settle periods) the current-Live fraction on
  10⁴ coast falls below 20% and the pinned store falls below ~250 B/body in the variant arm.
  KILL: if the Live fraction stays above ~70% at 48k and 96k, a standing kick train keeps the
  belt Live in flight — the seam never demotes the belt in flight and its belt win is birth-only.
- **P2 (the residue classes):** at depth the residue is bounded classes only — retired history
  segments (prune-bounded, ≤ ~2 Live arcs/body), nokick-mint arcs (O(10²) per 10⁴ at 5k), and
  plunges (expected ~0 minted on belt scenes; priced per-arc if any). KILL: any class whose
  count or bytes grow superlinearly with cut depth at fixed N (leak ⇒ seam shifts ruin, does
  not delete it).
- **P3 (the dead):** dead bodies' held arcs track the loss count (≤ ~2 arcs each, ~700 B), a
  priced constant per death, not a compounding term. KILL: dead-held bytes per lost body growing
  with depth.
- **P4 (variant ≡ seam on the belt):** the belt is bound, so demote-passages changes little on
  belt scenes at depth (Δ ≤ 10% of the pinned store); its 16–19× win is comet-scene-only
  (re-checked on the mixed/stargraze arms: pinned per body there collapses under the variant).

Registered after the smoke at 5k only (pre-wave), before any depth flight.
