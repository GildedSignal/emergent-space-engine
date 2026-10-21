# Predictions (written before the decisive matrix; smoke runs only proved it compiles and runs)

The wired form: `SCAN_NEWSFED=1` serves a candidate's read outcome from a per-body cache when
`(event_time, alive, binding_until(j, t))` proves `binding_at(j, t)` still returns the same binding
(every rebind retires and advances `event_time`, `step.rs::rebind`; a death flips `alive`; prune moves
the segment end, rechecked). Kept tuples are elementwise a rebuild's, same order — the digest must be
the shipped one. Same-tick duplicates fall out (all kept ⇒ the shipped memo hits ⇒ the answer is
shared). The dial `BELT_DESYNC=D` multiplies every ship's kick cadence by D (both laws' planning paths;
the player and planets keep theirs, so the scan cadence is invariant). Flights are budget-free
(`until: None`), hence deterministic: digests compare run to run.

Arms (all `scannews2`, 6 s wall, rtf 100): 30k coast/burn at D = 1, 8, 64; 3k coast (the radial-fallback
arm) at D = 1, 64; each arm flown shipped and newsfed. Timing on 30k burn D=1 and coast D=1
(`SCAN_TIME=1`), both modes.

1. **Digest neutrality (the exactness half):** newsfed == shipped, bit for bit, on every arm. Kill: any
   mismatch — the wired form is not exact and the run reports a refutation, not gold.
2. **The dial (the composition half):** the newsfed walk work (re-reads per near id) falls monotonically
   with D, roughly ∝ 1/D, toward a floor set by membership churn (new ids entering near as the player
   moves) and segment crossings; the shipped walk stays 1 read per near id at every D (its work is
   cadence-invariant, its information is not). Kill: re-read fraction at D=64 still ≥ half its D=1
   value — the scan does not ride the kick dial and 9b03's composition claim dies.
3. **The duplicate delete:** memo hits ≈ 45–50% of captures on burn arms (9b03 measured 47% on the
   budgeted flight), now paid at signature-check cost instead of walk cost.
4. **Cost attribution:** newsfed capture µs/call < shipped on both timed arms; the radial query and the
   per-scan fixed cost (me's read, cache lock, counters) form the new floor — expect the radial share
   visible but the walk term still dominant at D=1 on the fallback arm (3k: ~3,000 near ids walked
   shipped).
5. **Fallback arm:** at 3k coast the radial fence fails (9b03: 90% of scans), so near = every body:
   the shipped walk reads ~3,000 bindings a scan; newsfed keeps rejects as well as accepts, so its
   re-reads fall with D there too.

Kill criteria for the run: any digest mismatch (1); the re-read fraction flat in D (2). Both reported
either way.
