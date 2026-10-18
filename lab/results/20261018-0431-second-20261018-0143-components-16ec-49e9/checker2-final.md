Working...
Check complete — `check2.md` written, grade **gold**.

**Reproduction (my own `regen.sh` in a clean tree, `patch.diff` applied):** every deterministic arm bit-identical to the dossier and the author's `a_*` flights — pinned burn `1198b23ec9b91432` ×4 at 19,423/19,423 skips with 338 passages, straddle `0c3b1c7dcd0dfeeb` with 5,126 refusals and 1,753 deaths both arms, coast `a725217f…` (16ec's known answer), probe zero excursions. The patch's delta vs 16ec's base is harness-only; the `step.rs` physics hunk is byte-identical. Mechanism verified in shipped code: `digest()` hashes `self.inputs`; presented ≤ nominal by construction at rtf 1800, so the pin is never refused.

**Adversarial, all outside the author's range, all digest-identical ctl vs fast:** N=30000 (3× largest flown, under 10-way load), held-out seeds 2 and 3, `leave_log2=27` (refusal branch at 99.9%, 9,707 deaths), and burn+straddle combined — a branch interaction never flown. My first (botched) battery accidentally gave 8 more shipped-harness burn digests under load, each explained by its logged tick — the instrument demonstrated harder than the author did.

**Corrections:** one, in the author's wiki page — the "unequal ticks → unequal digests" half now anchors on the persistent cross-window pair (`247,463,935 → 37efae11` vs `343,400,821 → 08b6399c`), with the overwritten fix-window `c3038c23` figure labeled per the dossier's provenance note. Nothing else in the folder touched; tree restored clean.

**Misses named for the record:** the decision *stream* (one pinned decision per flight so far), the 4.4–5.6 µs shipped range being author-window only, and the decomposition measured only at N=10⁴ (my loaded N=3×10⁴ window read clock_share 0.40 — a window artifact, not an N-law).
