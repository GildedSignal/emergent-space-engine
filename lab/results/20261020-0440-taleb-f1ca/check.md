# Check — 20261020-0440-taleb-f1ca (v4: the disarm channel as an exactly-safe publish floor)

Grade: silver

## Abstract

v4 (the frontier advance publishes only up to `floor0`, the deepest restorable tick; five
lines in `finalize()`) reproduces: 0 fires on 50+ gated draws; shipped's fires reproduce on
the checker's fresh seeds 37/39/41 (3/8, exit 101) with the claimed signature
`fin_hi > s0 = front` (1136>1104, 960>912, 784>768) — the shipped coalesce is the second
unsafe publisher — and v4 runs clean on those very seeds at 1280-1536 present. Equality law
held (77 further RB, all m ≤ 0, `out=[]`); crush min-coupling reproduced (v4≡v3, the
f=0 F=0 S=0 pin vs shipped F=368 S=0 armed). Adversarial beyond the author's range: 2×
scale (17408/48) and 9 s horizon clean at 82-83%; the 2-way load boundary is clean (96%).
Present ratios are window-owned (51-100%, median 74%, vs the author's 71-94%/93%) but above
the pre-registered thresholds in both windows. Not adoptable as the close: it starves under
crush. Silver; the gold experiment is named below.

## Reproduction (clean tree, `work/patch.diff` applied by me; runner's regen exit 0)

- The runner's regen window: 0 fires anywhere, including shipped (pre-declared wall-clock
  race; the fix session's regen saw 1). All deterministic content regenerates: v4 0 fires on
  15 gated draws, equality law 77 RB lines all m ≤ 0 (max 0) with `out` empty on all,
  12-way crush v4≡v3 (43/341/153/119), and the mechanism line itself: crush_v4_s11 ends
  `f=0 F=0 S=0` while crush_shipped_s11 ends `f=80 F=368 S=0` armed `A=80` — shipped hides
  the laggard behind the coalesce publishing above a live truth start, exactly as claimed.
- My own fire hunt, shipped arm, seeds 27-41 odd (outside the author's 11-25), sequential:
  **3/8 fires (s37, s39, s41), exit 101, every one signed `fin_hi > s0 = front`
  (1136>1104, 960>912, 784>768)** — the second-unsafe-publisher finding reproduces on a
  fresh seed set with the author's incidence. v4 on the same three fired seeds: clean,
  0 fires, present 1280/1536/1536. The full paired contrast landed in one window.
- Present ratios, quiet pairs, my window: 0.512-1.000, median 0.743 (author: 0.71-0.94,
  median 0.93). The pre-registered criteria (≥0.5 every seed, median ≥0.7) hold in both
  windows; the dossier's "71-94%" is window-flattering and now qualified on the page.
- E1 s19 my window: shipped 833 / v4 730 (88%) / v3 341 (41%) — the author's "even v3 does
  not starve on s19" is window-owned; their P1-v3 failure report stands, and the load axis
  (not the seed axis) discriminating is confirmed by my boundary mapping below.

## Adversarial cases (mine; ≥1 outside the author's tested range)

1. **Fresh seeds 27-41** (above the author's set): fires + signature + v4 clean.
2. **2× scale** (galaxy 17408/48 fleets, s27 — above the author's 8704/24): shipped 608,
   v4 496 (82%), 0 fires both arms, v4 final lead 0 by design. Domain extends.
3. **9 s horizon** (s19, 2× duration): 3072/2560 (83%), 0 fires — the floor lag does not
   compound with duration.
4. **2-way concurrency, s11** (the quiet↔4-way boundary the dossier left unmapped):
   1280/1232 (96%), no starvation. In the regen's 4-way block v4 s11 was 286 vs shipped
   180 (v4 above) — the 4-way starve is itself window-flaky; only 12-way starved reliably
   (43). Consistent with the dossier's reading (a scheduling failure), but its "4-way:
   43/529" presents one window's numbers without the flakiness flag it gives the fires.
5. **Churn class** (gas, rate 600, min_region 1, n 2048 and 8192): no splits occur inside
   4.5 s on this machine — both arms identical at present 0-1, 0 rollbacks. Uninformative
   for the v4 contrast; the churn-class question stays open (the page already flags it).

## Exactness of the floor

Statically corroborated beyond the dossier's "argued": `prune` keeps ≥1 history entry per
region (`len() > 1` guard), so `history[0]` is always defined, and drops truths only below
the window of the oldest kept snapshot — the engine's own documented invariant ("truths and
plans older than the oldest kept snapshot can never be read"); rollback's restore walk
reads only kept history entries. So `floor0` = min(kept `history[0]` ticks, kept truth
starts) is exactly the deepest restorable tick, and a publish at ≤ floor0 cannot fire. No
counterexample in ~50 gated draws pooled (author 30, regen 15, mine 8+).

## Predictions

P2-fires held (v4 0/8; shipped in-band — 3/8 on my fresh seeds). P2-present held on the
pre-registered thresholds in both windows. P2-equality held. P1-v3 failed (author-reported;
my window fails it differently, 341 not ≤250 but 41% of shipped). P3 held 6/8, failed s11
twice (0.08-0.12× vs ≥0.3×) — and the failure is the min-coupling finding. Kill criterion 3
is arguably met in letter by the s11 crush draws (v4 final lead 0 while shipped advances);
the author discloses this and reads it as the finding — defensible (under crush shipped also
barely advances) but generous.

## Novelty

The live page (through da23) and docs/HISTORY.md hold no v4, no coalesce-as-second-publisher,
no min-coupling/laggard pin, no load-axis discrimination. 541d — the direct predecessor,
whose checker 429'd (grade: missing, commit b6bdae84) — established v3, its starvation and
the frontier-advance pin; f1ca's delta over it is real, measured, and now independently
reproduced. Not gold: one load-bearing prediction (P3) failed on 2/8 seeds, and v4 is not
adoptable as the close within one step (under load it trades the crash for a stall: s11
crush 43 vs shipped 118-529). The run says this itself.

## The one experiment that would make it gold

Fly the per-region floor (deepest restorable tick among truths that can still touch *this*
lineage, with merge-capping) — or the scheduler variant refusing to let one region pin
finality — under the same 12-way crush protocol: 0 fires AND ≥0.3× shipped present on s11
crush closes direction 1's design.

## What the author missed

- The laggard's cause is unopened (parked? blocked? oversubscribed?). One SDBG state dump of
  the never-accepting region would decide between the two proposed closes (geometry vs
  scheduler) — cheaper than flying either blind.
- The fire's publishing call site is attributed by elimination (`fin_hi > front` excludes
  the frontier advance). One `ESE_STRIDE_DBG=1` armed dump on a fired draw pins the SF kind
  directly; nobody ran it.
- The 4-way starvation boundary is window-flaky (my regen: v4 above shipped on s11) — the
  dossier flags the fire counts as races but presents the mid-block numbers as stable.
- The churn class remains unflown for v4 (my probes could not fly it here either).

## Page

Corrected in place: the present range is now window-qualified (51-100%, medians 74-93%)
in the NEW block, the open-directions note and the Runs line, and a checker bracket with
the fresh-seed fires, the adversarial domain extensions and the churn gap was added after
the NEW block. Three gold runs do not agree on this topic's best; the page stays open.

## Goal fit

Board direction 1 (the engine's one reachable crash, exit 101) — ruin-side, so nothing else
on the plane multiplies until it closes (PRINCIPLES #25, "don't multiply by zero"). #13:
"we don't want errors that can compound" — safety by construction (publish only below the
deepest restorable tick), not by margin. #19: "if you find yourself fixing things that's
oftentimes a signal that it is the wrong representation" — two shipped publishers above
live truths; v4 makes finality's invariant explicit instead of patching publishers.

## Provenance note

The author's original draw logs were overwritten by design (regen.sh `rm -f` + the fix
session's rerun), so the author-window numbers (3/8 fires, 1440-1984 presents, 136 RB) are
checked only against the fix session's report and my independent windows, not their raw
stderr. The predictions file predates the final patch/dossier (fix session rebuilt
regen.sh); the honest failure reporting (P1-v3, P3-s11) supports pre-registration.
