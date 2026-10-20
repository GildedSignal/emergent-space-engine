# Dossier — 20261020-1116-system-bd4b (system lens)

## Claim

The scoreboard's two worst CPU/memory gaps are one object: the exact-quadrature knot vector
(`OrbitShape::knots`) that every fired kick fills and stores. Per-kick wall time tracks the
minted knot count (Spearman 0.70 on the plane's own bodies, 0.88 on handed-out fleet members,
~2.7 µs/knot), the minted heap is the knots (85–91%), and one scene holds both a 6-knot class
(~38 µs, 0.5 KB) and a 148-knot class (~376 µs, 12.5 KB per kick) — the same law, one lever:
how many panels a compile opens.

## Bottleneck

Board rows "the kick: 75–160 µs against a ~50 ns floor" (10³·³) and "memory per body
~2,460–5,100 B against ~6 B" (10²·⁶–²·⁹) are counted as independent gaps (HANDOFF: "CPU at
10⁹ = bodies × kick rate × kick cost …; memory = bodies × bits + live bodies × ~1.3 KB").
They are the same term: `bind_surface` → `OrbitShape::compile` fills the knot vector (the
fit is 84–89% of a kick, b063), and the minted knot vector is the standing bytes (58% of a
doll body, 5465) and the retired-history ratchet (Segments keep Entries alive, 225d). A
representation change on the knot memo moves both rows at once; optimizing them separately
double-counts, the same way e7ef showed kick-cost and cadence do.

## Evidence (Linux/x86, shared box — orders of magnitude only)

Instrument: `xtask universe --kick-bench` (the shipped deterministic kick replay on the
plane's own scene), extended print-only: per timed kick, the minted entry's trajectory kind,
knot count and knot/crossing heap bytes (`work/patch.diff`: kick_bench.rs census + a
read-only `Passage::shape()` accessor + a Linux footprint stub in nladder.rs; no engine code
touched). Commands (each ≤ 60 s, from the repo root with `work/patch.diff` applied):

```
cargo build --release -p xtask -p emergent-universe --example nladder
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 10        # default scene
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --members 400 --seconds 30   # x2 (control)
```

- **Every fired kick mints** (P1): 160 mints / 161 timed kicks (m400 scene), 23/23 (default).
- **The CPU bill is the knot filling** (P2): per-kick µs vs minted knots, Spearman
  **0.70** (made, n=23) and **0.88** (leavers, n=137); knot-tercile medians 203 → 376 →
  394 µs at 83/148/153 knots (**~2.7 µs/knot** slope). Reproductions across four runs:
  ρ(made) 0.57–0.70, ρ(leavers) 0.86–0.88 (shared-box µs wobble ±10%, digests exact).
- **The knot count is a property of the orbit class, not the law** (P3): made population —
  all Cycles, 6–12 knots; leavers — 55 Cycles + **82 Passages**, 22–448 knots (median 148;
  the tail is 3× the median). The panel rule is geometric (ψ-bands doubling at CAP = π/4,
  orbit.rs:450–481): a near-circular cycle costs ~6 panels; the members' arcs open 20–75×
  more. No certificate sizes this: it is the compiler's eager full-arc rule.
- **The memory bill is the same vector** (P4): knots = **85%** (made) / **91%** (leavers) of
  minted heap; the members' 137 mints allocated **1.71 MB = 12.5 KB per fired kick**, on top
  of Binding 192 B + Segment 208 B + Entry ~288 B + slot per mint (efd4's bill).
- **Controls**: digests bit-identical run-to-run (m400: `8c242b023e8b79e4` twice, replay
  `0de3a82c1926a83d` twice; default scene `b42da477294f7619` on the pre-patch binary and on
  the patched one — the census is print-only); `refused == 0` everywhere; `heap_bytes` is a
  floor (Vec capacity slack and the Passage tail uncounted).

## Predictions

All four pre-registered predictions held (P1 >95%: 99.4%; P2 ρ ≥ 0.5: 0.70/0.88; P3 ≥2×
spread: 6→448; P4 ≥60%: 85/91%). See `predictions.md`.

## What would make it wrong, adoption cost, fit

Wrong if: the fit's 84–89% share does not decompose into panel quadrature (b063's split
would need re-measuring at FIT2 granularity); or the read pattern between two mints
traverses ~the whole compiled arc (then eager compilation wastes nothing and the unification
prices no deletion — see the open measurement below).

**The unification's deletion candidate** (not flown here): the knot memo is a pure function
of the key, regenerable bit-identically (5465); nothing observes it between events except the
next event's readout, skippable boundaries (16ec) and the player's window. Two consequences
follow from this run's numbers: (a) the 12.5 KB/kick passage-class mint is the memory
ratchet's dominant term and the same 148 panels are the kick's dominant CPU — one lazy or
class-split compilation rule deletes both together; (b) retired Segments holding Entry arcs
(29% of a doll body) can keep keys only. Cost of adoption: a law-layer change (the memo's
extent), digest-neutral by construction (the readout is a function of the key, not the memo —
5465's bit-identical regeneration), so the B-gates re-freeze is cheap; the named next
experiment measures, per fired kick, the **traversed fraction** of the freshly minted arc
(phase at next rebind ÷ compiled span): if members rebind well inside their arcs the lazy
memo saves ~the unread fraction on both bills; if they traverse it all (the belt's
one-kick-per-period cadence suggests exactly that for cycles), the saving is passage-class
only and the finding re-prices to a class-split compile rule.

Fit (PRINCIPLES): "we just need to have the right representation so that math is trivial"
(18) — the knot count is the representation's resolution, currently set by the compiler's
eagerness, not by a certificate; "Store the generator, not the generated" (6) — the vector is
the generated; "the right question, then the representation" — the question is who reads the
arc before the next mint.

## The lens (what it may have made me miss)

A unification can hide a hard special case: **the belt's cycle class** kicks once per radial
period and traverses the whole orbit between mints — for it, lazy knots save nothing, and the
6-knot cycle shows the eager rule is already near-cheap there. The hard case is the opposite
of the usual one: the expensive class (passage arcs, the fleet members) is where laziness
must win or the unification only re-prices the tail. Second miss risk: the census prices the
mint, not the allocator's amortized cost — 12.5 KB/kick is allocation churn too (Arc<Vec>
per kick); a counting-allocator arm (the standing instrument) would price the malloc side.
