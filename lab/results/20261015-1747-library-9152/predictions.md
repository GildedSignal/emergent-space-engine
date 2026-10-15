# Predictions (written before the flights)

Held-out cases: I have not run any flight yet in this session. The shipped-code
numbers I know from the wiki (672 B/body knots, 962 B/body standing store,
rss ~538-554 MB at N=10^5) came from patched arms; I have not seen shipped
Linux footprints.

## The decisive measurement (Lesson: marginal cost is the product class)

`nladder N coast 10 100 12` for N = 0, 10^3, 10^4, 10^5 on this Linux host,
slope of peak footprint vs N (after subtracting the N=0 plane).

- P1: the shipped marginal cost per belt body is **300-1000 B/body**
  (my Fermi: the belt is born from a seed as compact records, then compiled
  orbits stand — knots ~672 B + slots/entries; allocator slack at small N).
- P2: therefore the extrapolated footprint at 10^9 belt bodies is
  **0.3-1 TB** — the record class cannot fit an 8 GB machine at 10^9
  (needs < 8 B/body all-in), so the ladder's next class change (belt as
  program, lazy mint) is not optional. The gap I expect: **~40-125x** over
  the 8 B/body budget.
- P3 (linearity): the slope is flat in N (same order at 10^3-10^4 and
  10^4-10^5). If the slope *falls* with N by >3x, records are already
  amortizing and the class-change claim weakens.

## Kill criteria

- If marginal cost < 8 B/body (P1 badly wrong, shipped already fits 10^9 on
  8 GB), Lesson "product class" is wrong as stated and the dossier says so.
- If the slope is non-monotone or >2 KB/body, my Fermi was wrong; report the
  measured number and re-derive, do not smooth.
- Controls: N=0 gives the plane's own footprint (subtracted); each flight is
  fresh-process; 10 s coast only (no burn: burn's compile path changes the
  resident mix and is not what this lesson prices).

## What I will NOT claim

- No M1 numbers (Linux/x86 host; orders of magnitude only).
- No cache-policy claims: the cap family is out of scope (frozen by
  20261015-1615 runs); I only cite their published integers.
