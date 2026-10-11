Working...
Check complete. `check2.md` written; the run folder is otherwise byte-identical to the author's state.

**Grade: gold**

**Reproduction** — clean tree, empty patch (all edits confined to `work/encounters`; lib verbatim vs `crates/encounters`, only `fix.rs` new):
- `battle` (31 s): 8 scenes, 0 mismatches vs the frozen parent record ex timing, identical to the author's copy ex timing.
- 7 fix stages (102 s, each < 60 s): 24 records, 0 mismatches ex timing; `analyze.py` output identical to `analysis.txt`.
- Every dossier number verified against the records, including recomputed arithmetic (pairs = n·k − k(k+1)/2; H* ≈ 47; the 2.1% silent miss at k=16 comes straight from the parent's own `caught_union_k` = 0.9790 — the parent's "19×, zero misses" really did conflate k=16's ratio with k=32's zero-miss).
- Predictions (06:32:40) precede `battle.jsonl` (06:33:50) and `fix.jsonl` (06:43:04); 9/11 held; the two misses are disclosed and diagnosed — and #8's failure is itself the correction that kills the parent's O(participants) claim. Genuine pre-registration signature.

**My six adversarial cases** (modified crate copy in /tmp; binary re-verified against the author's records first):
1. q at H=1280: kmax 5, caught(8)=1.0000, curves identical — eternal extends 4×.
2. Packet width 2.0 / 0.125: kmax 2 / 11, both flat — k ∝ 1/w, width-robust.
3. q at n=600: kmax 8, zero-miss k=8 → 37.7× vs the cone — favorable, sub-linear in n.
4. **Same key, e=0.05 fleet**: eternal (kmax 75 frozen 20→320 orbits) but caught(32)=0.0000, zero-miss k=128 → **1.5×** — the 19× win collapses via the mean↔true anomaly gap at the crossing. The adoption clause needs a near-circular (or anomaly-aware) qualifier.
5. **Oblique crossing** (17° flight path, fast transit): the mean-longitude merge-join key is broken (142/211, 0% at k=128) while the true-longitude key is perfect (2/7, 100% at k=8, 9.5×) — the parent's geometry hides this because mean=true exactly at perihelion. The mechanism survives with the right key; the gate needs an oblique scene.
6. Perfectly synchronized volley: all sorts degenerate to index ties — a group event, not a rank problem.

None of this contradicts a measured claim; cases 1–3 strengthen, 4–5 bound the adoption note's clauses (i) and (iii). Gold on the premise-is-wrong clause (twice: 19×-zero-miss and O(participants) both wrong as stated), the measured 19.0× zero-miss closure on quantized fleets, and one-step adoption — with my two clauses appended to the spec edit.
