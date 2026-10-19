# Dossier — 20261019-1316-second-20261018-2155-scout-9fd1-1176 (second author on 20261018-2155-scout-9fd1)

**Claim.** The checker-named gold experiment — leak(E, κ) on the shipped tier's own due
structure (e87d's integer replica, epoch dial, κ dial, pooled seeds) — is run, and it
closes the page's knee contradiction in one law: **there is no zero-leak knee at any
(E ≥ 2, κ, P); at the belt quantum the miss fraction follows 1−1/E and the leak
saturates E-flat at the event rate (7.2×10⁻⁶/pair/touch at belt-real coupling, i.e.
7.2×10⁻⁹ per candidate per cell kick — 140× under 1a29's 10⁻⁶ budget at every E), so
the epoch dial's E* is cost-limited, not leak-limited: E_cell ≈ (n/2)·E_pair up to
~10⁶ cell kills the 355-core row to ~3.5×10⁻⁴ cores.** The mechanism is e87d's missing
constant: δc0 per quantum kick = 1.02 window widths (one kick fully re-rolls the
near-phase; the flip flux is κ-saturated at the fresh-uniform 2w/pi) — 08d0's knee was
the φ₀-fixed idealization plus a 4×10⁴×-weak kick, and 9fd1's no-knee verdict transfers
while its √E law does not (the leak is per-touch, not span-accumulating).

**Bottleneck.** Board item 2 (encounter work at 10⁹): the epoch rule is the named
355-core-row lever, and its adoption dial was the leak budget ε. This run replaces the
freeze question "where is the knee?" with "the leak never binds" — the adoption's open
question moves to the caught-but-late (armed staleness) channel, one run away.

**Evidence** (`regen.sh`, ~7 min: build + grid + heldout + anchors + flips; all numbers
below; instrument `crates/encounters/examples/epoch_leak.rs`, e87d's replica verbatim
plus the epoch/time-coupling dials; make_belt 2,000-body cell at ρ = B = 3.34×10⁻⁶ AU,
seeds 20261018/777 pooled, 5,000 pairs/pass, T = 2,048 touches, book logic exact in
integers; floats only build sections, as shipped):

1. **δc0 (the constant that decides everything; e87d measured δd/δπ/δw but not δc0).**
   One quantum kick moves the rotation anchor by p50 5.47×10⁴ ticks = **1.02 window
   widths** (w p50 53,920; 20,000 pairs; linear in κ: 6.8×10³ at 2⁻²⁶ → 2.8×10⁷ at
   2⁻¹⁴). δd p50 2.39×10⁴, δπ 1.9×10⁴, δw ~ 0 — e87d's anchors reproduced (w 53,920;
   k_first p50 8.72×10⁵).
2. **The flip primitive** (200,000 pairs, one kick each): dv=0 → 0 flips at every H
   (bit-exact control). For H ≥ 64 the flip rate per opportunity is 1.1–1.4×10⁻⁶ ≈
   2w/pi (fresh-uniform) and **κ-independent over 2⁻²⁶…2⁻¹⁴ (512×)**; at H = 1–16 the
   counts (0–6 per 200k) are consistent with fresh-uniform within noise — no
   protection at any horizon.
3. **The epoch grid** (the decisive run; miss = a true in-window conjunction firing
   before the tier examines it): at the quantum, P=1 (the toys' clock): miss_frac
   0.48/0.68/0.77/0.82/0.97/1.00 at E = 2/4/8/16/64/256 — the 1−1/E law, leak/touch
   saturating at 3.0×10⁻⁶. Belt-real P=4: 0.16/0.44/0.69/0.86/0.98/1.00, saturating at
   **7.2×10⁻⁶/pair/touch** (147 events). P=16: 2.5×10⁻⁵. At 512× weak kicks
   (2⁻²⁶) the quasi-static book (δc0 = 0.13w) dips small-E: 0.04–0.09 at E=2 — but
   **nonzero at every E ≥ 2, and 0.95+ by E = 1024 at every κ**. No knee anywhere.
4. **Controls, both sides.** dv0: 0 misses at every E ≤ 256 (55 events, CI ≤ 0.065;
   one boundary artifact at E=1024, disclosed below); E=1: 0 misses at all (κ, P);
   no-arm: 1.000 leak fraction at all cells. The dv0 control is what caught and killed
   two instrument bugs in the first run (float-τ anchor grid; k=0/l=P boundary
   double-fire) — no number below predates those fixes.
5. **Held-out** (seed 424242, first run after predictions): 81 events, miss_frac
   0.25/0.56/0.83/0.88/0.98/1.00 — the pooled curve reproduced, leak saturating at
   7.9×10⁻⁶.

**Predictions** (`predictions.md`, written before the first grid attempt; the two
instrument fixes changed no prediction's content). P1 HELD (all controls). P2 HELD in
its main assertion (no knee; 1−1/E at the quantum: 0.48 vs 0.5, 0.49 vs 0.5 at E=2) and
PARTIALLY FAILED in its letter at 2⁻²⁶ — the miss fraction dips ~10× below 1−1/E at
small E (quasi-static book; honest miss: the flat law is the quantum-and-above regime,
and the weak-κ dip is the correlation e87d's full decorrelation kills only at the
quantum). P3 PARTIALLY FAILED: the event rate varies 1.48× over 512× κ (saturated at
quantum+: 3.03 vs 3.17×10⁻⁶ — 5% over 512×; the 2⁻²⁶ arm sits 29% low), not the
predicted ±30%-flat everywhere. P4 FAILED in the letter: events/touch ∝ P^0.66
(1 : 2.37 : 8.40) — the per-opportunity rate declines with P because a frozen rotation
serves at most one event per touch plus a P-free anchor-landing channel (~1.5–1.8×10⁻⁶
/touch, the k=0 kicks); the decomposition P·1.3×10⁻⁶ + 1.5×10⁻⁶ fits all three P arms.
P5 HELD: 7.2×10⁻⁹ per candidate per cell kick — 140× margin at every E; row → 3.5×10⁻⁴
cores at E_cell ~ 10⁶. P6 HELD (held-out seed reproduces).

**What would make it wrong.** The two sections per pair are treated as one opportunity
clock (both pj-spaced, min-indexed): the true pair event rate may be up to ~2× — the
law and the 140× margin are robust to that, the constant is not. P's belt-real value
(1/(2R) per section, R = 0.1–0.25/orbit from 1b1f's rising rate, ×2 sections) spans
2–10; the P=4 arm is representative and the P-law lets the integrator rescale. The
caught-but-late channel (scheduled dues firing under stale rotations) is counted as
caught, not leaked — the shipped tier processes it late; if late processing counts as
error, the freeze needs open direction 1. No event-impulse model (post-event books go
far; ~1 event per 68 pair-passes at P=4 — the aftermath cannot shape the leak
statistics). One dv0 boundary artifact at E=1024 (1/55): the standing-list refresh
ordering; disclosed, does not touch any quoted number.

**Cost of adopting, fit with PRINCIPLES.** Nothing to wire to read the verdict; the
adoption it unblocks: the per-cell re-arm epoch E_cell up to ~10⁶ cell kicks (leak
140× under budget, measured, not extrapolated), the row to ~3.5×10⁻⁴ cores — with the
freeze's remaining question the armed-staleness channel (one run on this harness).
PRINCIPLES 3 (compute only surprises: the leak is the surprise rate, now measured
E-flat), 10 (kill criterion pre-registered; controls on both sides — the dv0 control
earned its keep twice), 13 (errors that compound: a per-touch flat leak of 7×10⁻⁹
cannot), 22 (the simulation decides: the toys' knees were instruments, not laws).

**The lens (second author).** What the lens may have missed: I price the leak in the
arm-certificate's own units (in-window conjunctions), not real contacts — the arm
window is a sound superset, so the real-event leak is ≤ the measured one; and the
thin-window class (1a29's w ≈ 23) is unflown here (δc0/w ~ 2000× larger — saturation a
fortiori — but the anchor channel and E_cell pricing deserve one re-anchoring run).

## Commands

```
cd lab/results/20261019-1316-second-20261018-2155-scout-9fd1-1176 && ./regen.sh   # ~7 min
```
