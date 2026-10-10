Working...
Check complete. `check.md` written; grade **silver**; tree restored to its pre-check state.

**Reproduction (clean tree + `work/patch.diff`):**
- Benches: rtf 100 gather share 69.9%/engine 17.4% (author 69.8/17.7); rtf 1 gather 71.2% (author 73.5%). Digest `41343a14…` bit-identical.
- Probes: m48 and m400 digests reproduce **exactly across machines** (`09e40859…`, `aadaa1c8…`); invisible fractions 0.629/0.773 exact; gather p50 within 1–2%; overflow 139 vs 136.
- Kick-bench (reverted the patch's hunk that replaces `--kick-bench`, ran, re-applied): 1158 kicks, 95.47% quantized memo hit, 0% exact — matches.
- `behave --law space --gates G1,G2,B7` → PASS, confirming the gate-artifact diagnosis. Code premise verified: `gather_with` loops all bodies, no floor (`view.rs:300`), on the shipped per-frame path.

**Adversarial:** rtf 10 → 92% invisible (waste larger at low rtf); m400 at 25 s → 62% invisible persists (not a transient); repeated runs agree bit-for-bit.

**Why not gold:**
1. Novelty is partial — H0210 already records "the view gather is 83% of a light frame", H0211 added the gather cache, and representation.md already queues rung r6 and prescribes screen-capped aggregates. The dossier cites none of these; its genuinely new part is the quantified headroom (63–77% invisible, ~10.5 µs/emitter, engine overflow tail at m400).
2. The 3–4× gain is estimated, never built or measured.
3. One inflated number: "view 2.2–3.1× engine per body" mixes per-emitter with per-body; honest per-body ratio from the author's own sums is 1.6–2.7×.

The gold experiment is named: build the rate-bounded refresh skin on `ViewCache` (r6) and measure the actual frame cut with unchanged digests. Pre-registration of `predictions.md` was genuine (file times verified) and the author's bookkeeping of failed predictions (P4, P5) was honest.
