# Red-team of docs/representation.md: the premise census, and the cost premise refuted by shipped code

**Claim.** Of representation.md's six load-bearing premises, one (kicks absorbed cheaply by
cycle derivatives) is refuted by the project's own gold record and by shipped code — the
per-kick cost is ~700× the doc's number and the memo it relies on hits 0.0% exactly — two
more of its letters (the Minsky in-cell law, "crosses once") are already dead in law.md and
the wiki, and the doc, which every builder reads first, still teaches all three.

**Bottleneck.** Not a physics bottleneck: a representation-contract bottleneck. The doc is
the input to every specialist and lab run (`run.sh` prepends it by reference through
PRINCIPLES; law.md L90 assigns its falsifiers r5/r6 to GLM). A design doc teaching refuted
premises seeds wrong builds at zero physics gain — principle 19's alarm ("if you find
yourself fixing things that's oftentimes a signal…") now applies to the document itself.

## The census (ranked by how likely the player is to see the failure)

**1. Kicks and cycle derivatives absorbing perturbations — REFUTED, regenerated here.**
The letter (representation.md L67): "A cycle's derivatives are stored with it, so a kick
updates the cycle by a multiply-add"; the cost row (L114): "Tidal kicks … ~50 ns each,
incremental: < 1% of a core". The record: the jet was retired 12 October with three golds
("a one-signed phase error that fails both frozen budgets on every orbit within its
margin", law.md L36); the shipped code says "Derivative prediction never substitutes for
authoritative rebinding" (`crates/space/ENVELOPE.md`) and "A kick is a multiply-add
**prediction**; recompilation remains authoritative" (`crates/space/QUADRATURE.md`). My
regeneration on the shipped resolver (`xtask universe --kick-bench`, this machine, Linux
x86 shared, loadavg 0.47, orders of magnitude only; three runs, digest and all counts
bit-identical):

- `kick_us` (plane-made bodies): **median 34.8 µs** (stable to 0.1 µs across runs), p99
  53–63 µs (1398 samples).
- `kick_us_leavers` (handed-out fleet members): **median 203.3–203.7 µs**, p99 399–408 µs
  (955).
- Against the doc's ~50 ns: **~700× at the median, ~8×10³× at the p99 of all**; at the
  doc's own kick rate (6×10⁴/game-s) that is ~2 cores of tide compute per game-second, not
  "< 1% of a core" (~200× end-to-end). The M1 record agrees in order of magnitude
  (43–52.8 µs, kick-cadence c01c/0c44; 75–160 µs, board).
- The memo the cheap path needs: **`exact_hit_rate` 0.0** (2262 cycle rebinds → 2262
  distinct exact shape keys; zero reuse), while the law's quantized 12+12-bit key would hit
  **98.0%** (46 distinct keys) — and that key is a recorded law change (taste log 5 Oct:
  94.5% there, "changes orbits"). The premise is squeezed from both sides: exact keys never
  repeat, the repeating key is not the law. This regenerates, in one shipped tool, the
  5-October correction and 3294's "fire ⇒ rebind" (fire rate 1.000).
- **Rung that should have caught it: none exists.** r2 gates carry widths; B9/B10 gate
  crossing counts and scaling exponents; the §6 cost table has no rung or gate at all, and
  the jet died by lab golds (kick-jet), not by any frozen criterion. The doc's §7 ladder
  contains no kick-cost falsifier.

**2. The view gathered at the past light cone — letter dead, physics holes open, no gate.**
"Each visible tube crosses the observer's past light cone once" (L57): refuted — ≥2–3
images on 100% of azimuths at r_o 100–3.2 M (6eae, silver); no time-transfer law exists
(flat light-time off 2–176° within ~50 M, 5977 **gold**; 4.3–10.1° phase error near a
mass); the deflection memo key is broken for rotating dolls (8be2 **gold**: needs
(b, sense), (b, Q)). Newton-from-previous-frame holds at 3.00 iterations warm-started at
every β, but misses newborn photon-ring images (a616, ungraded). **Rung: r6 is named in
§7 and assigned to GLM (law.md L90) and was never created; "no view gate exists" (0fe0).**
This is the player-facing hole: navigation and knowledge must be perfect (principle 30),
and light delay near a mass is a navigation error of degrees.

**3. Binet cells as "the primary in-cell solution" (L32) — replaced a day after the doc.**
law.md L20: the in-band area-preserving map was replaced on 30 September by the Darwin
compilation ("band-centre tangents carried a first-order slope error in every cell holding
a turning point"). Research rehabilitation is partial (fe85; scout-79ed today: the one-law
u_k refit passes 256/256 precession at m ∈ {8,16,32}) with four instrument channels broken
(circle family, strong-field, capture, ISCO) and r1 never graded by the lab. **Rung: r1
exists, frozen, ungraded; the doc cites it as the guard while teaching the law r1's own
history killed.**

**4. The two-body doll at 1PN, ν only in the energy map — SURVIVES, domain named.**
Confirmed by r3 v3 (precession 1024/1024, periods 632/632, the ν effect 500/504, assists
64/64) and B11 on the integer law. The unlicensed flank: comparable-mass strong field (p ≲
20M, plunge/inspiral) is gated only against a 1PN **oracle** (B11: "of the 1PN oracle"), so
the doll's fidelity to GR there is bounded by nothing; binaries merging are the drama the
game sells (Julien: "yeah i like both especially rotating black holes"). **Rung: none
covers the merger flank; B19 gates test-body Kerr (ν = 0) only.**

**5. Dense order bit-identical to sparse — SURVIVES in the lab, unguarded in the field.**
The tie rule (redteam-6254, law.md L48), the contact law's canonical batch rule, the
locality licence ("pair errors telescope… resolving components separately gives the same
bits", `lattice::law`, tested), B8 and the flight-replay tests across threads and budgets.
No refutation on record. The hole is the field guard: the replay gate cannot fail for a law
regression and certifies a reverted contact fix as its greenest output (replay-gate wiki,
8e84) — so a future order regression would ship green. **Rung: B8 claims it; r5 (dense
order), assigned to GLM, was never created.**

**6. Undisturbed bodies cost ≈ 0 — SURVIVES in letter, by rate not by cost.** Belts pass
10⁹ at 10× real time today (a4ed **gold**), but every belt body fires a kick+rebind every
doll interval (3294: fire rate 1.000, impulses ≥ 2⁷ units) — "≈ 0" holds between kicks and
rests entirely on the kick *rate*, while the neighbouring cost row is the fiction. **Rung:
B9 gates crossings per cycle and "zero work per orbit until an event" — it passes, and
prices nothing.**

**Principles at stake.** "Measure before claiming" (10): §6's table was never measured and
now contradicts three golds. "A fix signals the wrong representation" (19): the jet's
one-signed phase error is the recorded instance. Text budgets (AGENTS): "Truth now lives in
docs/*.md … rewritten in place" — representation.md has not been rewritten since 29
September while law.md moved under it three times (Darwin, jet retirement, tie rule).

## Evidence (commands, each ≤ 60 s here)

```
cargo build --release -p xtask -j 2                      # 44 s here (CARGO_TARGET_DIR set by the lab)
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 20 --rtf 600
# → lab/results/20261016-1207-redteam-12db/kickbench.json (both runs, digest-stable)
grep -n "multiply-add" docs/representation.md            # L67
grep -n "50 ns" docs/representation.md                   # L114
grep -n "authoritative" crates/space/ENVELOPE.md crates/space/QUADRATURE.md
grep -n "replaced the in-band" docs/law.md               # L20
```

## Predictions

Written before the run (`predictions.md`). Held: the µs range (predicted p50 20–300 µs;
measured 34.8, leavers 203.7); zero reuse (predicted no memo tail; measured exact_hit_rate
0.0); no multiply-add path on the kick route (code says prediction-only). **Miss, my own
arithmetic:** I predicted the gap as "10⁵–10⁶×" the doc's 50 ns; the true multiple is
~7×10² at the median (~8×10³ at p99-of-all). The prediction's headline was wrong, its
range right; the refutation is unaffected.

## What would make it wrong

A measurement showing a memo-hitting fast path on the shipped kick route (exact_hit_rate >
0 on a stock scene), or a doc amendment landing before the checker runs (then the claim's
object disappears and the run is a census only). Timings are one shared x86 box — orders of
magnitude only; the M1 re-measures.

## Cost of adoption

One editing pass on representation.md (integrator-owned): strike L67's multiply-add and
L114's ~50 ns for the recorded 43–160 µs and "rebind per kick, zero reuse"; relabel Binet
cells as research (Darwin is the shipped law); mark "crosses once" with the 6eae/5977
caveats; note r5/r6 as uncreated. No code changes. It deletes future readers' false
premises; it touches no frozen evidence.

## The lens

A premise red-team reads the design against the record; I re-measured the one premise with
a shipped instrument and cited the rest. What the lens may have missed: I did not run a
fresh physics falsifier for premises 1, 4 or 6 (premise 4's order-independence rests on
code-embedded tests I read but did not execute); and the census format risks grading the
doc's *staleness* where the integrator may judge the *design intent* (a DRAFT that says
"supersedes nothing until the falsifiers in §7 have run" is arguably honest about its own
provisionality — the fix is the same either way).
