# Predictions — 20261017-1018-taleb-01e7 (written before any churn-scene run)

Question: what separates frames-mode draws that trip the shipped finality assert
(`alloc.rs:1451`) from those that don't? b966 (crash reachable, 14/35 at the keeping-up
rate, 3 windows) and 5d87 (18/18 survive; batch-only grid defect) ran different scene
families. Hypothesis under test: **the separator is the conflict's origin — split-then-
reclash churn from internal velocity spread — not the driver grid, not bulk approach.**
Panics observed so far (b966) sit on the 16-chronon grid (gaps 16–64), so 5d87's
"stride ends stay on the grid" cannot be the frames protector; something about *which*
conflicts appear must be.

Cases (held out: none of the churn scenes below has ever been run by me; wave smoke run
only — it survived, rb 1, present/s 598):

- P1 **Generality**: `selfchurn` (ONE loose gas cluster, n=240, vmax 8, no approach)
  crashes in frames at rate 600, ≥ 1 of 6 draws. If neither selfchurn nor crossing ever
  crashes (≥ 6 draws each) while drift does, churn alone is insufficient — the
  two-cluster approach is implicated; that is a lead, and b966's generality weakens.
- P2 **Control class**: `wave` (zero-spread Pass slabs, planned merge, no churn)
  survives every draw: 0 crashes in ≥ 5 draws at rate 600 and ≥ 2 at rate 1200. Any
  wave crash breaks my separator and favors "load alone".
- P3 **Driver rule is not the fix**: on-grid chunked batch (chunk 128 = 8×window) on
  `selfchurn` crashes ≥ 1 of 3 draws. If on-grid chunks never crash on churn scenes,
  5d87's driver rule survives as a complete batch fix and the engine question narrows
  to frames.
- P4 **Grid spacing is not the protector**: `selfchurn` at window 32 still crashes at
  rate 600. If window 32 eliminates it while window 16 crashes, 5d87's grid story gains
  a frames leg.
- P5 **Exposure**: `selfchurn` at min_region 32 (no tiny splits) → 0 crashes in 3
  draws. Alternative I consider live: big splits churn too (then it still crashes; the
  churn source is splits per se, not their size — reported as such).
- P6 **Dose**: vmax 2 crashes less often than vmax 8 at rate 600 (churn rate is the
  dose). Flat or inverted dose-response weakens the churn mechanism.
- P7 **Load gradient**: rate 300 incidence < rate 600 incidence on `selfchurn`
  (b966/checker2 gradient: rare-not-never, not a wall).
- P8 **Batch single call**: `selfchurn` single-call batch to horizon 1800 survives
  (continuity with b966 P3).

Panic shape to log: `fin_hi − s0` per panic (expect 1–4 windows, on grid).

Kill criterion for the whole run: if nothing crashes anywhere (all arms 0/N), the
instrument disagrees with b966's reproduced panics — VOID my adjudication and report the
harness difference; if everything crashes including wave, my control is confounded —
VOID the separator, keep the incidence table.
