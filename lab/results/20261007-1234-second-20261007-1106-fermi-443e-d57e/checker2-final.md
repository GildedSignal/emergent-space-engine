Working...
**Grade: silver** — written to `check2.md`.

**Reproduction (clean tree, patch applied):** everything matches. The plane stream is bit-identical to the original silver author's `hlive_deltas_s3600_seed1.bin` on the branch; the belt N=10³, held-out-seed, and N=10⁴ runs match line for line with bit-identical `.bin`s; both fermi tables regenerate every headline (belt 2,562 B/s, all-inner 79 MB/s vs 60 GB/s); zlib savings match the disclosed 9.0/9.0/12.5% split. Predictions were genuinely pre-registered (smoke 12:47:09 → predictions 12:48:00 → decisive artifacts 12:49–12:54).

**My four attacks all held:** seed 7 (+1.2% on rate), 2 orbits / 24 game-years (ratio 1.05, same 0.19 GB peak), 8× denser sampling (+6% — no undersampling artifact), 4× crossers (29.5 bits/event, handoff path still ~50 bits). Both code claims verified in shipped source (`step.rs:397` doll-0 no-capture; `universe.rs:970` prune's `oldest − 2²⁶` floor).

**Why silver:** fully reproduced, but it confirms the parent's premise-kill on a restricted class — massless test bodies, one planet, circular ring, handoffs only by construction (law v2 can't yet build the real-capture scene), thin doll-change population. The one experiment to gold: rerun the instrument on a massive co-orbital formation where encounters re-bind bodies.

**New finding the author missed:** `seed | 1` collapses even seeds — the "held-out seed 2" is byte-identical to seed 3, so the run rests on two realizations, not three; my seed 7 supplies the third (agrees).

Scratch files removed, tree restored, nothing else in the run folder touched.
