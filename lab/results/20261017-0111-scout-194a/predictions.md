# Predictions (written before the decisive flights)

Question: what is the plane's read stream FOR, and does a shared, versioned read
table (the "ephemeris" representation: a body's binding is immutable between its
own events, so every read is `(target j, version v, tick t)`) delete it?

Instrument: print-only. `crates/universe` gains a read log at the five read
classes (`SRC` = `Ctx::state_of`, the kick/tide/centre reads; `CLOCK` = a v2
clock's source read; `HANDOFF` = capture/release centre readout; `SCAN` = the
player's neighbourhood scan; `VIEW` = the view's readouts). The default build's
digest must equal the pristine digest `5b2d998b4449d556...` (cut 406050894);
every arm is `--unpaced`, rtf and N as stated, `ES_N` adds ladder ships.

Cases tuned on: none. The instrument is built, then all flights run once.

## Pre-registered expectations (decisive flights: A–C)

- **P1 (broadcast, not pull).** At `ES_N=10⁴`, rtf 100, 20 s: `SRC` reads are
  ≥ 70% of all reads, and ≥ 90% of `SRC` reads go to ≤ 16 distinct targets
  (the dolls' sources and centres). The read stream is every kicker re-reading
  the same few shared bindings — a gather/broadcast, not a data pull.
- **P2 (the table deletes it).** The version-memoisable share of `SRC` reads
  (reads whose `(j, version)` was already read by an earlier event) is ≥ 90%:
  a per-`(j, version)` shared entry answers the stream; the invalidation rate
  is the sources' own kick rate (small).
- **P3 (why retention misses).** `SCAN`/`VIEW` reads of ladder ships have
  median read lag `t − version_birth` above 100 game-s (≈ 2.03×10⁷ ticks,
  log₂ ≈ 24.3), so any dwell ≤ 80 gs finds them demoted — the 8792 cliff;
  `SRC` targets have median inter-read gap under 1 game-s (always hot).
- **P4 (rate cross-check).** Total reads per body per 20k game-s land within
  ×3 of 8792's 11.48 (different instrument, shared harness — consistency is a
  check, not independence).

## Held out (run after A–C and not tuned on)

- **H1:** seed 2 at `ES_N=10⁴`, rtf 100, 20 s: P1–P3 structure holds within ×2.
- **H2:** `ES_N=10⁵`, rtf 100, 20 s: read counts scale ~linear in N; the
  `SRC`-target set does not grow with N (the broadcast's fan-in is doll
  structure, not population).

## Kill criteria for the candidate

If `SRC` < 50% of reads, or the version-memoisable share of `SRC` < 50%, the
shared-table representation does not delete the stream's mass: the stream is
then scan/view pulls of cold bodies, and the dossier reports that instead (the
table still answers `SRC`; the deletion question moves to the scan's own
certificate).
