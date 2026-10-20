Working...
Check complete — `Grade: silver`, written to `lab/results/20261020-1210-library-a31c/check.md`, page corrected in place.

**Reproduction (all clean):**
- `regen.sh` re-run in a fresh shell: exit 0, output byte-identical (770 books / 4,590 highlights, 5/5 quotes, every composition number).
- Quotes verified a second way — direct grep of the raw export JSONs, bypassing the author's script: 5/5 byte-identical; full-highlight context read for L1/L4 confirms no strawmanning.
- All four code anchors verbatim in-tree (the comb inserts at step.rs:717-718, kick_clock's per-kick crash checks with no leave compare, boundary_clock = surface+leave+anchor, the anchor hash at universe.rs:1327).
- Prediction ordering holds by mtime: predictions 12:17:09 → verify_quotes 12:18:21 → compose 12:18:50. P1/P2/P3/P5 held; P4 honestly declared unflown.

**Why silver, not gold:** everything reproduces, but the run composes — the base page (8365) already held the 12.8 h/2.4 h pricing, the ~50% event share, and "cheapest next target". New is the budget/floor composition (658× over the 69.75 s budget; one term left after deletion; deletion = 1.2× on the wall, complementary to the interleave), the pre-registered digest-identity guard, and the byte-verified lessons. The deletion arm itself is unflown — the run's own dossier says so.

**My attacks found three things the author missed** (folded into the page as a checker bracket): a second unpassable-digest path (plan items hashed at universe.rs:1330-1336, `What::Boundary => 300`); a real view-path consumer — `Kick.lead`/`Kick.boundary` feed observe.rs `partial()`, so moving the anchor stamp changes the readout ramp and the gate set was incomplete; and domain limits ("0.72× fits" is rtf-400-only — at rtf 1000 it's 1.79× budget; "halves the alternation" → the boundary-era wall halves, the ratio grows).

**Gold path:** fly the env-gated deletion arm at 1e5/2e5 with leaves-within-one-full-step, crash-latency, cut_digest schedule-invariance, walls, and a readout comparison — P4's pricing is the falsifier.
