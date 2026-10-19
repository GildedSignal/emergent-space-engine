# Predictions (written before the decisive flights)

Scene: shipped `nladder` flights, print-only env-gated census (`ES_KICK_NEWS`; off = the
shipped path, plus one inert `Arc` clone at the census site when off). The census counts,
per FIRED kick (the quantized dv ≠ 0, i.e. every rebind): whether the re-fit's compiled
orbit has the SAME `OrbitKey` and sense as the standing binding's entry (a duplicate mint),
or a different one (real orbit news); split by the belt's radial band (r > 1.1 AU) and by
path (clock vs tube). `cat_inserts` counts `Catalogue::insert` calls on the universe side
(there is no hit path in code: every insert stores a fresh `Arc<Entry>`).

- **P1 (the duplicate-mint premise):** on the belt's clock path, `belt_same / belt_fired ≥
  0.90` — the kick's one-quantum dv almost never moves the `OrbitKey`, so ≥ 90% of fired
  kicks re-compile an orbit the engine already holds. Band: [0.90, 0.999].
- **P2 (no dedup on the mint):** `cat_inserts == clock_fired + tube_fired` exactly (every
  fired kick allocates a fresh catalogue entry; no key lookup exists on this path). This
  one is code-verified already; the flight confirms the counter wiring.
- **P3 (flip rate):** `belt_flip / belt_fired ≤ 0.02` — a belt body keeps its orbit key
  ≥ ~50 intervals (≥ half a doll period) between flips.
- **P4 (held-out, second seed):** seed 2 within ±2 percentage points of seed 1 on
  `belt_same/belt_fired` (the fraction is a population property, not a seed accident).
  Held out: also the tube path (locals) — I predict `tube_same/tube_fired ≥ 0.99` (the
  locals' tide is weaker than the belt's star-field gradient... uncertain: their dolls are
  smaller, so their tide is SMALLER, so fewer flips — direction: more same).

**Kill criterion for the deletion claim:** `belt_same / belt_fired < 0.50` ⇒ "the kick's
mint is mostly duplicate" dies; the flip rate is then the mint's honest information bill
and the report flips to pricing the cadence dial as the only memory lever.

**What would make each number suspect:** `clock_plunge` > 0 at scale (plunges carry no key;
the belt should have none), `cat_inserts ≠ fired` (counter wiring wrong, abort), or
`belt_fired` ≉ the kicks the ladder line reports (census misses the path the belt rides —
abort and re-derive).
