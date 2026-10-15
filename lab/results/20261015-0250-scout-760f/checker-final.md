Working...
Check complete. **Grade: gold** — `check.md` written; the author's wiki page left unchanged (nothing overstates).

**What I did:**

1. **Reproduced.** `regen.sh` exit 0, all three digests and every counter/census number match the dossier. My independent variant of the instrument re-flew seed 1 to the identical digest `f8b52855…`, then was deleted. Verified the arithmetic by hand: 4,886 B/body plateau, 13.7% knots share, 1.16× eviction, 0.16–0.9 cores, `Binding` 192 − `Arc` 8 = 184 B, `Knot` = 88 B.

2. **Held-out predictions.** P1/P2/P4/P5 held; P3 fired honestly — and the firing *is* the result: the record's 43-knot doll body does not exist on the belt (672 B/body, 13.7%), killing the eviction lever.

3. **Attacked beyond the author's domain** (seed 1, N ≤ 10⁵, ≤48 k game-s, cycles only):
   - seed 2: mismatch 0, knots 670 B/body — same class;
   - **N = 3×10⁵** (next decade): 300,028 cycles, mismatch 0, knots 672 B/body, plateau 4.84 kB/body — scale-free;
   - 150 k game-s burn (~5 waves): mismatch 0;
   - the **Passage** class the author counted but never recompiled: regenerated bit-identically at 9 radii.
   - Code audit: `Orbit` is a pure function of `OrbitKey`, no interior mutability — the certificate has content exactly where eviction needs it.

4. **Novelty.** Board's named item answered first time; bit-identity mechanism extends 5465's doll-body proof to the belt where the answer inverts; belt compile price is new (stress-scene pricing existed on kick-jet — noted in check.md so the record stays honest).

**Caveats recorded (decision-neutral):** compile max is wall noise (24–262 µs across runs; p99 stable 8.4–9.7); knots census is current-binding-scoped, bounded by the measured flat plateau; the killed eviction half also lives on memory-h-live's page — cross-reference owed at publish. Not gold-blocking: the one remaining build (flown lazy-`Entry` in `decode`) is adoption work, and the author already named it.
