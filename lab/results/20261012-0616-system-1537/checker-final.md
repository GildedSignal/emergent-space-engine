Working...
Check complete. `lab/results/20261012-0616-system-1537/check.md` written; tree restored; nothing else in the run folder touched.

**Grade: silver.**

**Reproduced (clean tree, `git apply work/patch.diff`):**
- Unpatched quiet: 237 / 865 / 3,925 / 34,934 µs per frame at 1k/4k/16k/64k, `events=0` on every row (author: 215/971/7,088/37,436; same superlinear shape, 147× vs 174× for 64× bodies).
- Unpatched digest: A=B=C=`645d0367…` bit-for-bit.
- Patched quiet: 0.10–0.11 µs flat through 256k (rss ~494 MB).
- Patched digests: `e1078737…/ebaa6ae7…/6931638f…` — exact match with `digest-after2.txt`. Prediction mtime order is consistent with pre-registration.

**Adversarial (3 cases):**
1. Cut 6e10: unpatched still A=B=C (not a one-cut artifact); patched still divergent.
2. Fixed the author's broken fleet-free discriminator (`mu` is `mu_log2`, not a mass): patched R=R2=baseline bit-for-bit over 11,628 kicks — the core rewrite is sound, the leak is exactly the fleet, as suspected.
3. Stats: patched frame schedules leave the battle 97–99.7 % unresolved after the same canonical settle (2,927/245 kicks vs 73,372; 1–3 slices vs 76) — under-resolution, sharper than the author's "commit interleaving" reading. Mechanism found: `resolve_fleet`'s early return drops the entity from the calendar; the per-frame rekey was resurrecting it — so the named fix (i)–(iii) is incomplete as written.

**Novelty/quotes/gates verified:** no prior `rekey` cost measurement anywhere; the Calendar doc quote, B10's exponent gate (blind to a linear per-frame term), and law.md "Ties" (the shipped queue violates its own stated key) all check out.

**Why not gold:** the decisive pre-registered prediction (digest identity) failed by the author's own kill rule, and the adoptable artifact — the deletion itself — doesn't exist yet. The gold experiment is named and half-done: requeue at every calendar touch (including the early return), a cap that converges to the canonical cut, three-schedule digest identity at flat 0.1 µs frames; my `restricted` scene already passes as the non-fleet control.
