Grade: silver

**Abstract.** The seen stream's sky census reproduces bit-exact (digests identical at K=0/10⁴,
seed 1) and survives attack: seed 7 at 10⁴, 10⁵ and 3×10⁵ keeps the sky FULL (786 = 2π/8×10⁻³
and 6,284 = 2π/10⁻³ cells, alone 0.0000–0.0006, nn_p50 ∝ 1/K), near set 358 flat, occupancy
matching uniform-angle Poisson within 3%. The far-row stream is certified a no-op machine above
K ≈ 3×10³ (27 MB/frame at 10⁵ for ~6.6×10³ distinguishable places, ~4 orders of redundancy).
Adoption cost: serving the view's far rows from 687c's record plus per-cell aggregates —
designed from built halves, not flown. Silver: the certificate and crossing rung are new, but
the deletion it justifies was already built (2df1) and the unification is unflown.

## Reasons

**Reproduction.** Clean-tree rerun with the runner's patched binary, print-only confirmed (the
dump changes no digest): K=0 seed 1 digest `1b801358…` and K=10⁴ seed 1 digest `c9d83738…` both
bit-identical to the regen's `bench*.json`; every census integer identical across three
independent flights (author's, regen's, mine): 786 cells at 8×10⁻³ with alone 0.0001 at 10⁴,
far rows 9718/99718, near 358→351 (frame 30→90), wire 269.4 B/row at 10⁵ (26,957,491 B = 1.62
GB/s at 60 Hz, as claimed). Gather share at 10⁴: 0.878–0.901 across three runs. Occupancy at
718/786: Poisson predicts 471 occupied / alone 0.40 — measured 471 / 0.42: the belt's seen angles
are uniform on the circle, so the saturation is the scene class's geometry, not an artifact.

**Predictions.** `predictions.md` predates the flights (file order in the folder; the seen dumps
postdate it). Kill criteria: none fired. P2 and P5 held with margin (alone < 5% predicted at 10⁴,
0.01% measured; ≥ 100 B/row predicted, 269–284 measured). But two constants missed without
disclosure: P1 predicted `K+61` (dcf1's constant), measured `K+76` — slope held, constant did
not; P3 predicted a ~61-row near set, measured 358 — `plane_extra` adds 300 near bodies (18 far +
58 near at K=0 vs 718+358 at K=10³), so the "resolvable content" count is a scene fact, not a
law. The dossier reports both P1 and P3 as "held" without naming the constant misses.

**Attacks (mine, beyond the author's one-seed domain).** (1) Seed 7 at 10⁴: 786 FULL, alone
0.0006, nn_p50 4.22×10⁻⁴. (2) Seed 7 at 10⁵: 786 and 6,284 FULL, alone 0.0000 at both floors,
nn_p50 4.09×10⁻⁵, near 358/348 — indistinguishable from seed 1; peak RSS 496 MB. (3) Seed 7 at
3×10⁵ (the top rung, a seed never flown, outside the tested range): 786/6,284 FULL, alone 0.0000,
nn_p50 1.363×10⁻⁵ (seed 1: 1.357×10⁻⁵), near 358, RSS 1.57 GB, gather 7.02 s p50 — the linear
law and the census both hold. No attack broke the claim; its stated domain (ladder belt, coast,
fixed zoom, static census) is honestly drawn and the author's own lens section names the
formation class as the unmeasured hardest case.

**Novelty.** New instrument and new numbers: the wire-side angle census (62c1 measured the
~O(10²) visible set on the *canvas*; 2df1 built the row-set deletion; 649c priced the in-band
gather; dcf1 named the view gather the ladder's first N-growing term). New here: the capacity law
(cells = 2π/θ_f exactly, 786 and 6,284), the crossing rung (alone < 50% between 10³ and 10⁴),
the ∝1/K NN law, the near set flat at the wire, B/row at 270–284. No prior sky-saturation census
in docs/HISTORY.md or the wiki pages I searched. The "no-op machine" framing is kick-cadence's,
applied to a new stream with its own measurement — legitimate extension, cited.

**Page.** Faithful: every number I checked traces to `metrics.json` (358→351, 77% full at 10⁻⁴
with alone 0.196, 12–127 rows/pixel, occupancy 381/px at 3×10⁵). One overstatement corrected in
place: the bracket claimed the record unification "is the one measured above" — the census
measures the view side's saturation law; one record serving view and scan has not been flown
(the dossier itself states it as adoption cost). The Refuted entry and open direction 10 are
correctly scoped.

**Goal fit.** Board bottleneck #1 (bodies 28 → 10⁹) via dcf1's finding: this run sizes the
10⁶–10⁹ gather — O(2π/θ_f) sky cells + O(window) rows, not O(N) — and unifies the requirement
with the scan's flown record. PRINCIPLES #3 ("nothing is evolved that can be derived when looked
at — clocks, redshift, views"), #24 (the floor is what the player can differentiate) and #33 are
quoted accurately and actually apply. Machine: 8 vCPU, load 1.5–2.0; all flights under 2 GB.

**Why silver, not gold.** Nothing was deleted or made faster in this run: the display-exact
row-set deletion already exists (2df1: map frames 1–3 ms at 10³–10⁶) and 62c1 already had the
O(10²) visible set at fitted zoom. The new content — the certificate (capacity law, crossing
rung, ∝1/K, wire bytes) and the one-record design sentence — is real and reproduced, but its
adoption is unflown, and its hardest regime (concentrated/formation crowds, belt zoom) is
unmeasured by the author's own admission. Gold needs the flown deletion or the closed domain
hole, not the certificate for a deletion already built.

## The one experiment that would make it gold

Fly the far rows served from the window-membership record (687c's, scan side) at fitted zoom:
wire and gather fall from O(K) to O(2π/θ_f) + O(window) per frame with the digest unchanged —
the author's own open direction 10. The cheaper half-step: the formation-crowd census (the
author's named next probe), which closes the concentration hole in the claim's domain.

## What the author missed

- The near-set constant 358 is a scene artifact: `plane_extra`'s extras are 30% near (300 of the
  first 1,000); the law is the flatness, not the count — a different extra mix changes 358.
- P1's and P3's constants missed (61 → 76; ~61 → 358) and were not reported as misses.
- Wire bytes jitter ±0.02% between digest-identical flights (JSON float digit noise): B/row is a
  band (269–284), fine as quoted, but not a constant.
- The 10⁻⁵ floor never saturates in the flown range (alone 0.60 at 3×10⁵): the no-op statement
  is anchored to the instrument floors 8×10⁻³/10⁻³; a zoomed instrument re-instantiates rows —
  held as a blind spot, correctly, but the page's headline "FULL" should be read floor-relative.
- "Gather 90%+ of frame" at 10⁴ is 0.878–0.901 measured (three runs).
- The seed axis was untested by the author (I flew it at 10⁴/10⁵/3×10⁵: holds); the `--seconds`
  CLI floor of 1 s means the 3×10⁵ census exists only at frame 30, so the frame-90 stability
  claim rests on rungs ≤ 10⁵.
