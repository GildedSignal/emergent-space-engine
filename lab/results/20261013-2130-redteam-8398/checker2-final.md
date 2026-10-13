Working...
Second check complete. **Grade: gold.**

**What I did:**
- **Reproduction:** applied `work/patch.diff` to base 294215b, ran the dossier's single command — output differs from the stored `transit.tsv` by zero lines. All headline numbers regenerate: 0/112 keys survive a pure transit, 10 refusals, negative control passes, circles drift dk = 2^19 Q48 ulps, u32 wrap-by-one at e = 0.9.
- **Premise verified in shipped code:** `resolve_handout` → `bind_surface` → `Rebinding::ending_at/from_state` (bind.rs:265-266) — the engine really re-fits decoded member states; `OrbitKey` is `Eq+Hash` over all words, so key identity is Catalogue/memo identity. The circle-class-loss mechanism is exact (`inverse::circular` demands BigInt-exact identities).
- **Four attacks, none rescued the premise:** depth-64 transit chains never repeat a key and the fine-word walk is *directed* (−1 k-ulp per transit, 64/64 one-signed — compounding is systematic, worse than claimed); leak persists at p = 10^4–10^7 (outside the author's ≤10³ range), retrograde, and the unbound passage branch — where the k word stays stable and the periapsis word walks, so the leak is full-key.
- **Novelty:** handoff's 11 runs cover keys/surface/tide, never the fit round trip; 152f's 0.0 memo-hit citation checks out; r5 absent from `lab/rungs/`; `identity.rs` never crosses a hand-out. New topic justified.
- **Page corrected in place:** "12/12" → 11/11 (three keys refuse silently in the control), the unregenerable "~24 M" replaced with table-backed numbers (true max divergence is 1.92×10¹¹ ulps at (8, 0.99, 3/4), not the cited row), domain extended to p = 10⁷ / depth 64. Probe archived as `work/check2-attack.rs`; tree restored to base; author's files otherwise untouched.

Verdict written to `check2.md`: a premise kill on the truth rule's partition-independence clause, measured on shipped integers, adoptable in one step (tube-carry or entry-snap, freeze r5) — gold.
