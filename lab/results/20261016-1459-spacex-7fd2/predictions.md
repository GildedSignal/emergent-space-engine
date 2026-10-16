# Predictions — 20261016-1459-spacex-7fd2 (written before the decisive run)

Question: is the kick's recompile redundant at its own integer resolution? The compile's
expensive layer (roots -> cuts -> Gauss-Legendre panels) is a pure function of the integer
root triple (ua, up, m3, newton); the exact key (E, L) enters only the final `convert`
(a few wide multiplies per crossing). A kick that moves no integer root recomputes
bit-identical panels. Measurements: `xtask universe --kick-bench` with a print-only
census patch, plus a memo prototype (ES_TRIPLE_MEMO=1) that caches the quadrature
(cuts + cumulative sums) keyed on the triple.

Author arm: seed 3, rtf 100, 30 s. Held-out (not tuned on): seeds 7 and 11, threads 4,
and the digest identity between memo-on and memo-off.

1. **Triple-repeat rate (distinct kicks, global over all compiled cycles): members
   (plane bodies) ≥ 60%**, while the exact-key repeat rate stays ≤ 1% (the known 0%).
   Leavers repeat less (their impulses are larger): ≥ 20%.
2. **Root displacement on triple-miss is small:** the median nearest-previous-triple
   displacement max(|Δua|, |Δup|, |Δm3|) ≤ 2^20 Q62 units (warm-bisect lever plausible);
   worst case can be large (births, refusals near boundaries).
3. **The quadrature is ≥ 50% of compile ns** (stage 0 roots < 50%), so a triple hit
   deletes at least half the compile; converts stay.
4. **Memo-on vs memo-off: kick median −20% or better on members, digests identical**
   (replay_digest and digest-at-cut equal), refused 0 in both. If digests differ, the
   design claim is wrong and the run reports it as a kill of the memo (not of the census).
5. Nodes per compile on members are ≥ 16 (enough arithmetic for the reuse to matter).

Kill criteria: triple-repeat < 10% on members (the premise dies: roots move every kick);
or stage 0 > 80% of compile (the memo deletes almost nothing; the lever is then the
bisections, not the panels).

## Addendum (before any bench arm ran; after reading the shipped compile)

Pivot recorded honestly: predictions 1-5 above were written for a root-triple memo on
`crates/space/src/lib.rs` (darwin16). Reading the shipped kick path showed the production
compile is `crates/space/src/orbit.rs` (`Rebinding::from_state` -> `fit_key` ->
`Orbit::compile`), whose shape layer is keyed by exact Scalar mantissas (p significand,
Q48 k; compactness collapses only below q = 2^-18) — there is no integer root-triple seam
on that path. Predictions 1-5 are therefore untestable as stated; the design they describe
is dead by code reading, not by measurement. Re-registered predictions for the replacement
experiment (the key-displacement census, written before the first bench arm ran):

A. Zero exact repeats of p or k between consecutive kicks of one body, at every seed
   (the exact-key memo premise, already on the record, is structural).
B. A kick moves the key's own inputs by ~2^-22..2^-30 relative (median): p by about
   2^-26, the shape mantissa k by about 2^-28, with 15-23 low bits of k's 48-bit field
   changing per kick — the recompile consumes genuinely new bits every kick.
C. Same-bin (reuse) rate at g significant bits decays with no plateau: ~1.0 at g <= 12,
   ~0.95-0.99 at 16-20, ~0.5-0.84 at 24, < 0.3 at 28, ~0 at >= 32 — every point between
   the refused 12+12 memo and exact keys trades reuse for re-rounding at the complementary
   rate; there is no bit-identical reuse regime in between.
D. Leaver kicks move their key by *less* than made bodies (smaller relative displacement)
   yet cost ~5x more — their cost is knots (shape size), not key displacement.
E. Held out: seeds 7 and 11 reproduce A-D within a few bits (no tuning on them).

What happened: A-E all held (see dossier; medians p -25.5..-27.6 bits, k -26..-32 bits,
dk low-bits median 15-23 max 30-31; same-bin 0.9269-1.0 @20, 0.4942-0.8354 @24,
0.0643-0.2593 @28, <=0.0171 @32; leavers dp_bits -26.4..-27.6 vs made -25.5..-26.6 with
knots 37-195 vs 6). Original P2's "displacement <= 2^20 on miss" holds at the median,
fails at the tail (max 31 bits).
