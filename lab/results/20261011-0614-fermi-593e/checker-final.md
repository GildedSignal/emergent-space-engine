Working...
Check complete — `lab/results/20261011-0614-fermi-593e/check.md` written, nothing else touched in the run folder.

**Grade: silver.**

**Reproduced:** both plane benches bit-identical (digests `01c9be77…`, `29662bc6…`; ship 59–71 µs, fleet 18–25 µs per item, events/s 367.5/1,744), the galaxy 10⁹ scene deterministic (13,963 compiles, hit 0.98717, 0.43 s build; view medians 25.9–35.4 ms vs stored 25.8–37.2), and `budget.py` output identical. The 178-cores re-derivation, hot-body counts, and scar budget all re-derive exactly.

**Why not gold:** two held-out predictions failed (bytes/body 40–600 B predicted vs 5,044–6,227 measured; events/s 368 vs ≥ 500) — honestly reported, but under this lab's own precedent that caps the grade; and the headline 150–350× memo lever rests on an unmeasured 0.2 µs memo-hit cost — my adversarial `--kick-bench` run shows distinct-kick median 37 µs with **exact memo hit rate 0.0**, so the lever is a projection on an unwired mechanism.

**Found beyond the author's report:** the 106 MB scene RSS regenerates only via `galaxy --png` (104.2 MiB), a command absent from the dossier; the "~64 ns" bandwidth crossover is actually 6.4 ns by the script's own numbers; "~150–400× above the 34 b envelope" is actually ~1,200–1,500× (the quoted ratio matches the 16 B tube target); player per-item cost is 1,658 µs in the m4096 scene, 4.7× the quoted 352 µs; and 4×10⁹ ships measure 0.33 b/ship — the memory claim is conservative and survives 4× scaling.

**Gold path:** one experiment — wire the cycle-keyed memo behind `--kick-bench` and measure the hit-cost median against the 37 µs miss. That converts the first wall's lever and the whole ranking from projection to measurement.
