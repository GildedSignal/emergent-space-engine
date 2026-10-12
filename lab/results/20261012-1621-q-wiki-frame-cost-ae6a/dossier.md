# Dossier — 20261012-1621-q-wiki-frame-cost-ae6a (lens: compile the wiki page `frame-cost`)

## Claim

The 68 clustered runs of 6–12 October compile into a `frame-cost` page the integrator can act
on without opening a dossier: 30 runs belong to the topic (8 gold), and they establish, measured
on shipped code, (a) a Θ(N)-per-frame fixed tier at zero events (unconditional `rekey` plus the
defer/drain/requeue passes, `universe.rs:493/790`) that breaks 16.7 ms at ≈1.5–6×10⁴ root
entities with no digest-safe fix built yet, (b) a kick at ~1,400–1,800× its measured floor
whose cost is 70–89% rebind bookkeeping (`Orbit::compile`'s certified quadrature), with the
exact memo dead (0% hits) and every bit-identical micro-deletion capped at ≈1.2–1.4×, and
(c) a frame loop that already is the allocator (schedule-independent, at its floor) whose real
openings are per-region staleness, a density/throughput gate, and one live canon leak
(`session.rs` logs the player's keys at the presented tick; the fix is built and held on an
ungraded branch, not on main). The compile's one sanctioned probe resolved the cluster's
fleet-exodus contradiction into a regime boundary: on shipped code the delivered frame's worst
hitch is 39/100/98/146 ms at 1,600/3,200/4,000/6,400 members, so the 5 ms budget does split
the fleet's work through at least 6,400 members and the claimed 0.6–1.5 s indivisible slice,
if real, binds only at ≳12,800 members.

## Bottleneck

The board's `frame-cost` line ("O(N) per frame with zero events, and a kick at ~1,800× its
floor; what deletes the per-frame rekey and the rebind bookkeeping, measured on shipped code").
This run does not move the bottleneck; it makes the record navigable so the next runs and the
integrator stop re-measuring the same shares (the wiki's purpose, Julien 12 October). Expected
gain: deletes the ~20 duplicate "the frame is view-bound / the gather is X%" rediscoveries from
the frame-cost conversation by separating them to `view`.

## Evidence

The compile is mechanical and reproducible (`regen.sh`, ~6 min including the probe):

```
python3 work/verify.py        # from this folder; PASS printed at the end of the run
bash work/probe.sh            # the contradiction probe (needs work/patch.diff applied)
```

- All 68 checker abstracts extracted from the immutable branches
  (`git show origin/claude/lab-<id>:lab/results/<id>/check.md`); all 8 frame-cost gold dossiers
  read in full. `work/abstracts/` and `work/dossiers/` hold the extracts.
- **Classification** (a partition, asserted by `verify.py`): frame-cost 30 (8 gold, 20 silver,
  1 lead, 1 missing), view 34 (9 gold), memory-h-live 3, kick-cadence 1. Grade tally
  regenerated from the branches: 50 silver, 15 gold, 2 lead, 1 missing.
- **Grade drift found:** `20261006-0220-redteam-fermi2-v2-b7a4` — its branch's check.md says
  "Grade: gold", the cluster list says silver. It is a kick-cadence run, absent from the page;
  recorded for that topic's compiler. All other 67 grades match.
- **The missing run** (`20261008-0743-second-20261008-0615-taleb-40c0-a342`) has a dossier and
  no check.md: it built the decision-tick quantization (`Universe::input_frame`, 0.25 s quantum)
  and reports one digest per seed across frame rates and load plus a 12 s regression test
  (`crates/universe/tests/decision_tick.rs` on its branch). Verified by me on main (12 October):
  `session.rs step` still logs `input(now, keys)` at the presented tick and the test is absent —
  the fix is not adopted; the page says so and keeps the run marked `(missing)`.
- **Faithfulness checks in `verify.py`:** every page Runs-line id is classified frame-cost and
  its grade matches the branch; every claim line ≤ 20 words; every id cited in the body exists
  in the cluster; the ungraded run is marked missing; header/schema intact.

**The one sanctioned probe** (two runs contradicted; the lens allows ≤ 10 minutes to decide it).
3cfc (silver, checker-confirmed) attributed the fleet's smoothness break to one indivisible
`Fleet::advance` item of 630–742 ms at 3,200–25,600 members; ba35 (silver, two days later)
instrumented the same ~0.9 s and found one 20 ms slice plus 2,091 hand-out events of 443 µs
already split across frames by the budget. Decisive observable on shipped code: the delivered
frame's worst hitch at the overlapping member counts. Method: the documented one-line clamp lift
(`--members` 400 → 40,000, `xtask/src/universe/mod.rs:32`, this run's `work/patch.diff`), fresh
release build (57 s), `xtask universe --bench --seconds 10 --rtf 100 --members {1600,3200,4000,6400}`
(`work/probe.sh`; seed 1, paced 60 Hz, load ~1.0–1.3 on the 8-vCPU shared box):

| members | worst hitch ms | events/s | digest (canonical cut) |
|---|---|---|---|
| 1,600 | 39.0 | 2,449 | 98d82563… |
| 3,200 | 100.0 | 604 | 5a7cfcbe… |
| 4,000 | 97.8 | 585 | 7956ca73… |
| 6,400 | 146.3 | 275 | 6c482f6d… |

Reproducibility: a second full pass (`regen.sh`) gives 36/79/100/135 ms with **all four digests
bit-identical** — the hitches wobble with shared-box load, the scene does not.

No frame anywhere stalls ≥0.6 s — and paced timing *inflates* hitches (~4×, per
20261009-2212-constraint-2380), so the absence is robust. The budget splits the fleet's work
through at least 6,400 members: ba35's reading holds in its whole domain, and 3cfc's ≥0.6 s
item, if real, binds only at ≳12,800 members (12,800 exceeded the probe's 110 s window on this
box; unmeasured, disclosed). Events/s collapse 2,449 → 275 across the same range: the exodus
owns the scene either way. The page records this as a resolved contradiction, cited to this run.

The page's other load-bearing numbers, each traced to its run's check.md/dossier (the five the
checker samples will find these): 75.6 µs vs 42–56 ns, refit 84–89%, memo 0%/94–97% (b063,
3367); rekey 43–60 ns/body to 1.1 µs/entity, ceiling ≈1.5–6×10⁴, 721 ms at 10⁶ (d540, 115e,
b29b, 2439, 762d-119f); prologue 15 µs at 428 bodies, freeze = throughput ÷ density, opening
needs 293× (762d-119f); horizon cliff 309→0.03 (2517); player events 1.3–3.4 ms via the
O(all-bodies) scan (ae40, df79, d540); canon leak encounters 68–102, contacts 0–14 (40c0);
naive queue fixes break digest identity (6766, 1537).

## Predictions

`predictions.md` was written before the compile; its addendum before the probe's last runs.
Held: P1 (counts: 30/34/3/1 + 1 missing, inside the bands), P4 (digest-safety unresolved — 6766
and 1537 both break it), P5 (the floor claim is one gold, b063, corroborated in shares by 2300
and 115e), P6 (no run closes the topic; page stays open), P7 (later runs refute earlier
abstracts: the 428-body "saturation" is an xtask clamp, the 0.95 s slice is split hand-outs,
"delivers 0.00×" is a median-frame artifact, the prologue floor is 15 µs), P8 (the missing run
has a dossier, no check.md), P9 (the probe: worst hitch ~linear in members — 146 ms at 6,400 —
no ≥600 ms stall below 12,800). **Failed: P2's first clause** — I predicted at most 9 golds in
the cluster; the branches carry 15 (one more than the list's 14, via the drift above). P3
half-held: the zero-event tax spans 29 ns–1.1 µs per body per frame, so the low end sits below
my predicted 40–90 ns band; the page states the range with scopes rather than one law, as
predicted.

## What would make it wrong, cost of adoption, fit

Wrong if: a run's check.md misgrades its dossier (the canaries' lesson — the page weighs by
grade and by later refutation, both read from the branches); if the integrator's intended split
differs (e.g. the player-scan tail belongs to `encounters`, the members-clamp to `view`) — the
split is my judgement, stated in the handoff table below so it can be re-cut; if the probe's
single seed and 10 s windows hid a rare ≥0.6 s stall at ≤6,400 members (unlikely: the exodus
front-loads in the first seconds and the worst-hitch frame sits at 274–432 of 600); or if a
gold I compiled was later refuted outside this cluster (I found none: the only in-cluster
refutations are recorded under Refuted/Contradictions). Adoption cost: `lab/wiki.py apply`
merges the page; nothing else. Fit: "Text has a cost… One home for kind of text" (AGENTS.md)
and the wiki's rule 1 ("every author reads first… its result must add what the page lacks") —
34 of 68 runs were re-measuring a fact already on record; this page is the fix. PRINCIPLES #11:
"Start clean, build messy-ish, finish clean."

## The lens

A compiler trusts the checkers' grades; it cannot re-derive the physics. Two risks it accepted:
grade drift between the cluster list and the branches (found once, disclosed), and abstracts
written before a later run refined them — mitigated by reading every gold dossier in full and
by dating claims through the Runs list. The probe was run only because two runs contradicted
and one observable decided it, per the lens's charter; it stayed inside 10 minutes of compute.
What it may have missed: runs outside the cluster that touch frame-cost (the list is the
integrator's keyword clustering; earlier months' `claude/lab-*` branches were not surveyed, and
the parent runs behind the four `second-` checks, e.g. 20261009-0621-constraint-51bf and
20261011-1814, are cited only through their checkers).

## Runs that belong to other topics (for those compilers)

- **view (34):** 20261007-0528-constraint-6094, 20261007-0800-constraint-7a39,
  20261007-0842-constraint-0411, 20261007-1550-constraint-578e, 20261007-1801-constraint-3126,
  20261007-1843-constraint-2658, 20261007-2155-constraint-b952, 20261008-0743-constraint-4588,
  20261008-1058-constraint-caa2, 20261008-1719-constraint-1fe2, 20261008-2031-constraint-4b27,
  20261009-1210-constraint-c10d, 20261009-1210-second-20261009-0621-constraint-51bf-97bc (gold;
  its parent 20261009-0621-constraint-51bf is not in the cluster), 20261009-1259-constraint-2666
  (gold), 20261009-1504-redteam-2320, 20261009-1556-redteam-18fc,
  20261009-1556-second-20261009-1504-redteam-2320-56bc (gold), 20261009-1936-constraint-8af7,
  20261009-2212-constraint-2380 (gold), 20261009-2257-constraint-842c (lead),
  20261010-0100-constraint-c97d, 20261010-0352-quant-3435,
  20261010-0448-second-20261010-0352-taleb-cb7c-c2f8 (gold), 20261010-0814-constraint-f3f1,
  20261010-1029-redteam-435b (gold), 20261010-1152-constraint-c575,
  20261010-1407-constraint-775f, 20261010-1920-quant-9464, 20261011-0324-constraint-986f,
  20261011-1600-constraint-2094, 20261011-1729-second-20261011-1600-constraint-2094-07b8,
  20261011-1814-quant-f8f9, 20261012-1019-spacex-3463, 20261012-1227-constraint-cf31.
  Shared fact for that page: the gather's atom is one exact tube readout, ~5–15 µs, ~1
  readout/emitter/frame, and the `--members` 400 clamp invalidates capacity claims above 400
  until lifted.
- **memory-h-live (3):** 20261007-1843-fermi-1feb (10⁹ budget ranking, hot fraction 5–10%,
  reabsorption 37–292 MB/game-s), 20261010-1706-fermi-2914 (the "~20 bits/kick" floor refuted:
  ≥49.7 bits/kick measured, ≥6 B/body), 20261010-1816-components-6273 (stirred belt 2.2–2.4
  bits/body at μ_b=10⁻¹⁸; three of six predictions missed).
- **kick-cadence (1):** 20261006-0220-redteam-fermi2-v2-b7a4 — **branch check.md says gold,
  the cluster list says silver**; that compiler should re-read the grade. (Cadence pricing also
  appears in 20261007-1801-second-…-18df, listed on my page: work exponent ≈1, ≈4× B13 error
  per kick-halving.)
- **Missing (1):** 20261008-0743-second-20261008-0615-taleb-40c0-a342 — recorded on the
  frame-cost page as `(missing)`; if graded, it closes 40c0's open direction 5.
