# Dossier — 20261015-1450-library-3793 (library lens)

**Claim.** The nladder seam's bounded retained-entry cache is priced by replaying the engine's own
read trace: at every cut reachable in shipped time the flight read stream touches only 428 keys
(of a 10^4-member catalogue), so a plain LRU of K=512 entries holds 100% of the reads
(N-independent, ~1 MB) — no admission machinery — and 2Q's scan resistance is a named contingency,
not a need (my own pre-registered kill criterion fired).

**Bottleneck.** nladder open direction #1 (the checker of 1d52: "the adoptable bounded cache is
named, not built — one ~30-line flight away"). The blocker was *which policy and size K*: 1d52
proved global retention erases the memory win (retained set = every kicked body, 1.0-2.0× N). This
run replaces that guess with a measurement, and deletes the policy debate at the measured knee.

**Evidence** (all from `regen.sh`, ~6 min; probe = 51-line patch, env-gated `ES_KEYTRACE`, digest
bit-identical traced vs untraced: `ca195a2c…` both):
- Three traced flights (seed 1, members 10^4, bench script, unpaced; cuts 5.5×10^3 / 55×10^3 /
  1.1×10^6 game-s): 2,403,417 / 4,849,379 / 7,058,654 reads; **distinct keys = 428 at every cut**,
  and `bodies` = `catalogue_live` = 428 at every cut — the 10^4 belt does not open its births
  within 1.1×10^6 game-s of shipped time on this scene, so N never exceeded 428 live bodies.
- Concentration: top-64 keys carry 67.6% of reads, top-256 carry 96.5% (5.5k cut).
- Replay (post-burn-in; LRU/2Q): K=512 → LRU **1.000 at all three cuts** (2Q 1.000/0.998/1.000).
  Tight regime K=64: LRU 0.653/0.845/0.909, 2Q 0.726/0.881/0.930; K=128: 0.658/0.852/0.914 vs
  0.798/0.922/0.955 (2Q +8-14 points). At K≈distinct the 25% A1in split *costs* (K=256, 5.5k cut:
  2Q 0.924 vs LRU 0.968).
- Wall consequence: at 0% hits the bill is reads × 4.6 µs (scout-760f's re-mint) — 11 s against a
  14 s flight at the shallow cut; the knee is a wall decision, not only memory.
- The trace's longest distinct run is 689 keys (a bisection walk), never a whole-population sweep:
  no scan poisoning is reachable at N=428, exactly why prediction 3 failed.

**Predictions** (`predictions.md`, written before the flight): #1 (hot set ≤ 1,024 keys) held but
vacuously — every cut's distinct set is 428 because the belt's births never opened; #2 (2Q@1024 ≥
70%) held vacuously (100%); #3 (LRU(1024) < half of 2Q(1024)) **failed** — its kill criterion
("then plain LRU is the adoptable cache; say so") fired and is reported.

**What would make it wrong.** Any scene where live bodies exceed K≈512 with re-reads spread over
them (the born belt): then plain LRU slides and the 2Q/ARC comparison must be re-run on that
scene's trace — the probe answers it offline in minutes. The N-scaling question (does distinct
grow with born N?) is untested and is one flight away on a birth-accelerated scene. Cost of
adopting: trivial (the cache is K-bounded, off the frame path, digest-neutral by construction).
Fit with PRINCIPLES: "Compute only surprises" (#3) — the cache exists only for measured re-reads;
"Delete before optimizing" (#1) — the policy machinery is deleted at the measured knee; "Measure
before claiming" (Evidence). The digest-neutrality check honours "never let one experiment take
the machine".

**Commands** (each ≤ 90 s): see `regen.sh`; per-flight:
`ES_KEYTRACE=1 ES_KEYTRACE_OUT=t.bin <target>/release/xtask universe --bench --seed 1 --rtf 100 --seconds 55 --members 10000 --unpaced --no-record`
then `python3 work/replay.py t.bin out.json`.

**The lens** (see `author-final.md` for the five lessons, quotes verbatim from the Readwise
cache, `work/readwise.json`, 4,580 highlights): the library holds no systems practitioners (no
database, kernel or low-latency trading books among 770), so every mechanism beyond the quotes is
from outside it and labelled; the quotes anchor structurally, not technically. What the lens may
have missed: a survey-shaped deliverable is a lead — the probe is the substance; also the library
bias toward founders' aphorisms can dress a decision it did not change (I kept only the five that
name a change).
