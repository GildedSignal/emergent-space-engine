# Dossier — 20261020-1503-library-b57f (library lens)

**Claim.** On the answer channel 9ed1 left open (one held-scan answer walks
the belt; two named exits), the library and the measured laws compose to ONE
standing exit — the Binet-cone tier — because incremental answering is killed
by two already-measured laws (f102: no change-signal below the candidate set
certifies an unchanged answer, so its maintenance signal does not exist, P5
verified in-tree; a31c: per-body maintenance rides the 658× kick comb), and
the walk itself is killed by form: at 1e9 one answer is 4.2–4.4 ks = 60–63×
the 69.75 s era budget, discarding ≥3×10⁶ reads per answer of O(10²) content.

**Bottleneck.** The board's #1 (bodies in the flyable engine, 28 → 10⁹), at
its newest measured hole: the freeze that regrows through the staggered arm
(9ed1). Expected gain: the ask's per-answer cost from O(population) to O(k),
k ≤ 4 [0346] — ≥6 orders of magnitude at 1e9; deletes the walk term
(4.2–4.4 µs × N per answer) and, with it, the last per-ask term the stagger
cannot fix (be73's "the form, not the policy, carries the cost", generalized
from the pin's memory side 0.34% vs 124.93% at 10⁶ to the freeze channel).

**Evidence** (every number regenerates: `regen.sh` ~1 min cached, ~15 s +
fetch fresh; all commands ≤ 60 s each):
- Quotes: 5/5 byte-identical against the fresh 770-book / 4,590-highlight
  export (`work/verify_quotes.py work/readwise.json`).
- The walk at 1e9: `work/compose.py` — 4,200–4,400 s per answer = 60.22–63.08×
  the era budget; the 4.2–4.4 µs/BODY law reproduces 9ed1's measured answers
  at 1e5/2e5/3e5 within ratios 0.96–1.05.
- Discard asymmetry: walked spans 4,127× across the flown scenes (72.7 → 3e5)
  while kept/answered spans 10.6× (32.5 → 333; en = 178): discard 2.2 (plane)
  → 1,685 (3e5) → ≥3×10⁶ (1e9, kept O(10²)).
- Exit (a) killed: P5 (`work/anchors.sh`) — no epoch/generation/dirty/version
  signal in encounter.rs or radial.rs; the memo (`same_inputs`,
  encounter.rs:80) compares the full candidate list, exactly f102's finding.
  Exit (b) priced: the seam is wired (universe.rs:469), the trait needs no
  rewiring (encounter.rs:1–4), the rank law k ≤ 4 is gold [0346].
- The regime partition is the shipped code's own sentence (radial.rs:17): the
  apsidal filter is O(few) out-of-band and degenerates in-band — so the tier's
  k-window carries in-band, the doll hull (P6: verified absent, the hull is a
  body's bindings, radial.rs:14) carries out-of-band.

**Predictions** (`predictions.md`, written before verify_quotes.py,
compose.py and anchors.sh ran): P1 held (5/5). P2 held (60.22–63.08 ∈
[50,75]). P3 held on the mechanism and MISSED on its letter: the discard
ratio's span across scenes is 753×, not ≥10³ (kept 10.6× vs walked 4,127×) —
the miss is the finding's sharpening: at plane scale the walk is nearly all
signal (discard 2.2), so the discard law is a BELT-scale property, exactly the
regime partition of L3/L1. P4 held (5/5 anchors verbatim). P5 held. P6 held.

**What would make it wrong.** (1) The rank census: if 9ed1's en=178
encounters (or the 3e5 scene's own) contain a partner rank > 4, the tier
cannot replace the walk at that scene and L5 dies (it is the named flying
rung, unflown here — the honest gap). (2) A coarser sound change-signal found
in the tree or built (f102 searched global/binding/per-doll grains and found
0 hits; a content-hash grain below the candidate set would revive exit (a)).
(3) The kept count tracking the population across scenes (P3's kill bar) — it
did not across four scenes, but 1e9 in-band is unflown. Cost of adopting:
wiring the Binet cone into the seam (research crate exists:
crates/encounters), a law change on the finder path — recertified on
ladder_digest's 13 cases × 4 schedules, as the seam's own comment promises
("no rewiring"). Fit with PRINCIPLES: "Compute only surprises" (P3) — the
walk computes and discards ≥10⁶× what the answer keeps; "we just need to have
the right representation so that math is trivial" (P18) — in Binet
coordinates the near question is a rank/interval test; "an ant cares about a
raindrop but the lion does not" (P33) — L2/L3's kinds and chunks.

**The lens.** Analogies are cheap and the library is not the code: this lens
may have missed that the tier has its own cost structure (the encounters
page's 138 runs price the cone's own work — my composition prices only the
ASK side), and that 9ed1's answer channel and the scan queue's capture side
may not share the same term (the walk measured at answer time vs the reads at
capture time — f102's ~44 µs duplicates are capture-side). The five quotes
were chosen to hold decisions, but a different lens (flying, not reading)
would have flown the rank census instead of naming it.

No flight: no shipped binary was run; every number is composition on
published page constants (each cited in compose.py's header) and in-tree
anchors. The patch to the tree is empty (read-only run); `work/patch.diff`
records that.
