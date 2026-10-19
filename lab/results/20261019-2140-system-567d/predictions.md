# Predictions — written before the decisive run

**Question.** Who does a resident compiled trajectory (`Arc<Entry>`, the plane's dominant
live-memory object per the record: 58% of a doll body's 5,186 B; 1.3–1.9 KB per retained
binding) actually *serve*, between the events of its own body, on the shipped ladder scene?

Reader paths all funnel through `decode(entry, …)` (view, observe, encounter, own-body
readouts). The census stamps every minted Entry with its mint frame and counts decodes per
frame. "Served later" = at least one decode in a frame strictly after the mint frame.

- **P1:** ≥ 90% of Entries dropped during the flight have **zero** decodes after their mint
  frame (their only reads are the minting kick's own boundary search, same frame).
- **P2:** of Entries live at the end, ≥ 80% have zero decodes after their mint frame, and
  their estimated byte mass is ≥ 50% of the process's live-footprint growth over the flight.
- **P3:** decodes concentrate: the top 1% of entries by decodes carry ≥ 50% of all decodes
  (the player's doll — scans and boundary searches).
- **P4 (falsifier).** If ≥ 30% of entries are decoded in later frames, residency is a working
  set, not dead weight, and the deletion claim dies on this scene.
- **P5 (control).** The census changes no canonical number: ON and OFF arms of the same
  binary print identical event/kick/refusal counts in the ladder line.

Scene: shipped `nladder`, N = 3×10⁴ (belt), burn, 25 s wall, rtf 1000, 12 ms budget (reaches
the first kick wave at gs ≈ 11k–16k). The example's one cold+warm view gather at the end is
printed separately (a pre-gather census line separates flight reads from view reads).

Instrument cost, disclosed: one relaxed atomic load per decode when OFF; a mutex-registry
insert per mint, lookup per decode, and a compacting counter per drop when ON; the registry
itself holds ~24 B per live entry.
