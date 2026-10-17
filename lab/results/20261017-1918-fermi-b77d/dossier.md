# Dossier — 20261017-1918-fermi-b77d (Fermi lens)

**Claim.** The FLOW's held-scan pin is one law on every scene — **~0.4-0.55 kB per window
candidate per held scan** (four scenes, two load regimes, and 7bd9's counting-alloc
instrument: 415-541 B/candidate here against its ~428) — so the wall-path memory exposure
is the window's candidate count times a count-sized fence: ~145 MB-class worst for the
ladder's near set (~150 candidates), ~1.0 GB at a K = 1,000 crowd, and 2,048 × 475 B ×
candidates **passes the whole 8 GB machine at ~8,500 window candidates (K ≈ 8.5×10³ ships
at the measured 1.00 candidate/ship)** — the fence must bound pinned bytes, not scan count.
And the ladder's letter is load-dependent after all: under true oversubscription (ambient
loadavg 9-14 on 8 vCPU) its drain starves like every other scene (held 375-431 at the full
0.0966 scans/game-s arrival, RSS +6.9 kB/game-s), killing this run's own first reading
("cannot starve") — an insufficient-load artifact, reported as such.

**Bottleneck.** Board item 1 (memory per live body on the ladder) and the page's named
unflown experiment (7bd9's checker: "a quiet-machine claim until flown under load").
Closes it with a dose-response the page lacked: the drain starves under oversubscription
on every scene, and what differs between scenes is the PIN, not the trigger — which is
what makes the fence's unit (bytes, not count) the load-bearing fix. No 10⁹ consequence
on spread-belt scenes (near-set pins, ~145 MB worst); a K-proportional ruin channel on
crowds that the shipped fence cannot stop.

**Evidence** (Linux/x86, 8 vCPU, seed 1, threads 1, coast, rtf 100, 12 ms engine budget,
3,000 frames ≈ up to 5,000 presented game-s; the probe is a print-only patch on the
shipped `nladder` example — `/proc` footprint instead of the macOS-only
`proc_pid_rusage`, a `MEMBERS` override, one `probe` line per 60 frames:
`work/patch.diff`, 74 lines; loaded arms add 7 spinners pinned to cores 1-7).

Run 1 — controlled, ambient loadavg 0.4-1.2 (one free core):

| arm | scene | spinners | held_max | RSS end | per-scan pin | held/game-s |
|---|---|---|---|---|---|---|
| A1/A2 | 400-member battle (470f's) | no / 7 | 1 / 1 | 44.4 MB flat | — | 0 (VOID, P1) |
| B1 | ladder 1e5 (100,028 bodies) | no | 1 | 244.0 MB | — | 0 |
| B2 | ladder 1e5 | 7 | 1 | 243.9→244.0 MB | — | 0 |
| C | K=1,000 crowd | 7 | 268 | 168.1 MB | 514 kB | 0.0968 |
| C1 | K=1,000 crowd | no | 411 | 200.9 MB | 403 kB | 0.0966 |

Run 2 = `regen.sh` — ambient loadavg 9.25-13.79 (another window's jobs; recorded in the
log head), true oversubscription:

| arm | spinners | held_max | RSS | per-scan pin | held/game-s |
|---|---|---|---|---|---|
| A1 | no | 73 | 44.7 MB | 339 kB (partial starvation) | 0.0137 |
| A2 | 7 | 394 | 89.1 MB | 178 kB (cat 428 → **415 B/cand**) | 0.0968 |
| B1 | no | 375 | 267.3 MB | 63 kB (~150 cands → **~420 B/cand**) | 0.0849 |
| B2 | 7 | 431 | 273.6 MB | 71 kB, slope **6.9 kB/game-s** | 0.0966 |
| C | 7 | 218 | 155.7 MB | 556 kB (**541 B/cand**) | 0.0966 |
| C1 | no | 391 | 199.1 MB | 420 kB (**409 B/cand**) | 0.0969 |

- **The pin law:** 415/541/409 B per catalogue candidate on A2/C/C1, and the ladder's
  63-71 kB/scan at the near set (~150 candidates, c439 measured 70-184 by window) — one
  constant ~0.4-0.55 kB/candidate across scenes, loads and two instruments (7bd9: ~428
  B/cand by counting GlobalAlloc). The crowd/ladder pin ratio is the candidate ratio
  (~7-8×), not a body-count ratio: growth is per-scan × candidates, never per-body.
- **The trigger is oversubscription, not the scene:** at load ≤ ~8 with a core free, only
  the crowd froze (its ~4.4 ms answer makes the drain's margin ~9-10 ms exceed room);
  at load 9-14 every scene froze at the same arrival rate 0.0966-0.0968 held/game-s
  (held == held_max at every probe — zero answers in flight). Load decides WHETHER the
  drain starves; the scene decides only HOW MUCH each starved scan pins.
- **The fence:** linear with no reabsorption in every growing arm (C1: 411 × ~0.43 MB ≈
  177 MB observed ≈ 199 MB). SCAN_BACKLOG bounds the count at 2,048, so the byte bound is
  2,048 × 475 B × candidates ≈ **0.97 MB × (candidates/1000)**: ~145 MB for the ladder's
  near set, 0.97 GB at K = 10³, 2.33 GB at K = 2,400, 9.7 GB at K = 10⁴ — past the
  machine before the fence fires (470f's 220.9 MB peak is the same arithmetic at ~105
  kB/scan). Crowd candidates scale 1.00/ship (604c), so ~8,500 ships in one window bust
  8 GB through a fence that believes it capped memory.
- Cross-instrument arrival: 0.0966-0.0969 held/game-s here against 7bd9's checkers'
  0.096 — a third harness, same rate.

**Commands** (from the repo root; ≈ 2-4 min total, each flight 3-25 s wall):
```
lab/results/20261017-1918-fermi-b77d/regen.sh     # patch + build + A1 A2 B1 B2 C C1 + analyze
python3 lab/results/20261017-1918-fermi-b77d/analyze.py lab/results/20261017-1918-fermi-b77d/flights
```
`regen.sh` applies `work/patch.diff`, builds, flies all six arms and prints every number
above. NOTE: run 2's dose-response arm (the oversubscribed regime) is ambient-load-owned:
a regen on a quiet box reproduces run 1's table instead (held 1 on A/B). Both logs ship in
`flights/` — the run-1 logs are `*.log` as first written only if regen is not rerun; the
committed logs are run 2's. The load state is printed in every log head (`machine:` and
the arm banner's loadavg) so any checker can see which regime it holds.

**Predictions** (`predictions.md`, pre-registered, with a dated postscript). P1 VOID in
run 1 (my 7-way load left a core free; nothing counted from A), validated instead on C
(disease reproduced with 7bd9's constants). P4's pin estimate held (0.4-0.8 MB/scan
predicted; 0.40-0.56 measured) but its "load is the multiplier" framing was refuted by
the quiet crowd control C1. P2/P3 **refuted by the regen run**: the ladder's drain does
starve under oversubscription — my first "cannot starve" reading was an insufficient-load
artifact of exactly the kind P1's VOID clause warned about, killed by regenerating on a
loaded box. The pre-registered kill criterion (+0.5 GB monotone) did not fire — the
ladder's exposure is ~30 MB per 4,300 game-s — but the claim it guarded ("never starves")
is dead on the record above. The Fermi pin estimate itself (30-60 kB ladder, ~0.45 kB/cand
crowd) held within 2×.

**What would make it wrong.** (1) The oversubscribed arm is ambient, not controlled — a
deliberate 9-way rerun should reproduce it (the mechanism, `room < 2·max(scan_ns, 750 µs)`
against 12 ms, leaves no other reading, and 470f's 9/9-under-load agrees). (2) The
per-candidate constant uses catalogue entries as the candidate proxy on A2/C/C1 (7bd9
measured candidates directly; the two agree within 30%). (3) The unpaced loop gathers the
view once, not per frame — the real player loop can only add pressure, never remove it,
so the starvation side is a lower bound, but the PIN side (the law) is loop-independent
(it is the capture's own allocation). (4) The near-set size at 1e5 under load (~150) is
inferred from the pin law, not separately counted.

**Cost of adoption.** The measurement is free. The fix is one constant and one counter:
bound **pinned bytes** (candidates × ~475 B, already computed at capture) and drop past
the byte budget — it composes with the page's direction 1 (canonical game-s-cadence
drop), it does not replace it.

**PRINCIPLES.** "Measure the way the player will run it: heat and load are part of
reality, not noise to sidestep" (Tests) — the dose-response across two load regimes is
the run's spine, and it killed my own first reading. "Minimize spike compute and average
compute usage" (12): the fence is a smoothness term whose byte size, not count, must be
bounded. "Errors never compound" (13): a wall-path accumulation whose only bound
compounds linearly in the crowd is the same risk class. "A failed expectation is not
automatically a failed method: diagnose which one broke" (H0183) — the regen refutation
was diagnosed to the load regime, not buried.

**The lens.** The Fermi estimates held where they were load-independent (the pin law,
the fence arithmetic); where they touched load they were refuted by regenerating on a
loaded box — the estimate discipline caught its own error because the record regenerated.
What the lens prices poorly: the representational cure (canonical scan drops, the page's
direction 1) is measured around here, not against.

*The page's 4b8c/7bd9 conflict (same window) is folded in the proposed page: the sides
agree on the accumulator (held scans) and differ in emphasis (mechanism vs attribution);
both entries kept verbatim, mine on top. This run's evidence reconciles their one open
number: 4b8c's 84-112 kB/scan and 7bd9's 171 kB/scan are the same ~450 B/candidate law
at different window populations.*
