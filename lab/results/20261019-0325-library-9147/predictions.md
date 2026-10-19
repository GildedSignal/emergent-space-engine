# Predictions (written before the decisive composition and the quote verification ran)

The decisive experiment is the composition `compose_e9.py` (arithmetic on page-cited constants
only) plus the byte-identity verification of five quotes against a fresh Readwise export. Held-out
cases — none of these numbers was tuned on:

- **P1 (quote reproduction).** All five quotes (Musk/Isaacson, FS Second-Order, Waitzkin,
  Kahneman, FS Gather-and-Synthesize) reproduce byte-identically in a fresh export. Any text
  edit by Julien breaks this.
- **P2 (the ruin regenerates with zero new constants).** Using only 4a71's measured constants
  (wave period 27.6k gs, per-retained-binding 1.7–2.35 KB) the global rule's far-item ruin at
  4 ly composes to 8.8–12.2 MB per body, covering 4a71's stated ~9.2 MB/body, and the tick→gs
  scale implied by "2.56×10¹³ ticks ≈ 4,576 wave periods" is (2.56×10¹³)/(4,576×27,600) ≈
  2.0×10⁵ ticks/gs, i.e. the same number 4a71's own sentence already assumed.
- **P3 (the control regenerates from the gap law).** The control flight's flat 1.02–1.07
  retained/body is what the gap law predicts: 4a71's measured max pending light gap at one star
  (2,302.5 s) is under one wave period (27.6k gs), so retained = 1 + ⌊gap/period⌋ ≈ 1 for every
  body. The per-reader rule's near-body bound IS this same number — the far item adds no
  generation to any body it cannot yet read.
- **P4 (play-time boundedness).** Under the global rule, retained per body follows 4a71's
  second-checker law 1 + ⌊min(D, elapsed)/27.6k⌋ + ~1 — unbounded in play time while the far
  item is in flight. Under the per-reader rule, body i's horizon is bounded by the light
  diameter of i's own doll (scene geometry), a constant in play time. The composition will show
  the two laws differ by exactly the far item's transit window at every near body.
- **P5 (adoption surface, code fact).** The change is confined to the `oldest` computation in
  `Universe::prune` (crates/universe/src/universe.rs:1231-1242): today one `ship_ticks.peek()`
  over ALL ships (`apply` sets it with no doll filter, :664). The doll-filtered calendar germ
  already exists in the same struct (`child_ticks`, :170/:665, filter `doll(i) != 0`), and
  `ship_ticks` has ≤ 8 uses, every one a set/peek with no other consumer. If the file shows a
  third consumer of the global min, this prediction fails.
- **P6 (the library's own blind spot, held out).** The 770-book export contains no systems or
  database engineering book (no Kleppmann, no distributed-systems text): the verdict on
  reader-pinned retention must arrive by principle transfer from decision books, and every
  production precedent I cite outside the library (Kafka, Postgres vacuum) is my knowledge,
  marked UNVERIFIED-by-library, never a quote.
