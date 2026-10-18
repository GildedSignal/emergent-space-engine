# Dossier — 20261018-1530-system-afff (system lens)

## Claim

The player-neighbourhood scan — the structure behind three separately-counted walls
(the frame's capture walk, nladder 96f6; the held-scan memory pin, b77d/1fcf; the
reuse compare-form) — walks a candidate set whose size is decoupled from its answer:
measured on shipped code, the answer is always ≤ a dozen bodies (every hit at every
scene flown lies within Euclidean neighbour rank ≤ 11 of the player, 55% at rank 0),
while the walked set grows with the doll population (33 → 178 → 324 candidates for the
same 1-hit answers), so one structure — a neighbour-ranked read maintained by events,
not a walk — replaces all three walls at once (K/k ≈ 20–1,500× less work and pin).

## Bottleneck

The board's #1 (bodies in the flyable engine) and the frame wall at 5×10⁴: 96f6
decomposed the break into capture walk (190 ns/body), compare-form (19.2 ns/member)
and the pinned Vec (224 B × K × held). This run measures the *information content* of
that walk, which no prior run measured: the walk is not a no-surprise machine (my P1,
refuted), it is a *local-surprise* machine — and locality, not emptiness, is the
certificate that deletes the walk. Expected gain: the capture walk's 9.6 ms at
K=5×10⁴ becomes ~16 readouts (≤ 50 µs at the measured ~1 µs/eval class); the pin
falls from K×224 B to k×224 B (k=16: 3.6 KB); the compare-form likewise k-sized.
What it deletes: the O(K) walk, the K-sized pin, and the K-sized compare — three
components, one deletion.

## Evidence

Shipped code + print-only census (`encounter.rs::census`, patch: the scan's K, its
bail, its answer's emptiness, and every hit's rank among the walked candidates by
Euclidean distance at t and by along-track phase; floats never touch a law outcome).
Flights: `nladder` example, coast, seed 1, rtf 100, 1,500 frames (2,500 game-s).
`lab/results/20261018-1530-system-afff/regen.sh` regenerates every number (~40 s
after a warm build).

| scene | scans | bail | cand/scan | empty | hits | hits' Euclid rank | hits' along rank |
|---|---|---|---|---|---|---|---|
| A: shipped (48 members) | 241 | 240/241 | 33.3 | 113 (46.9%) | 128 | all = 0 | all = 0 |
| B: crowd (600 members) | 231 | 229/231 | 323.8 | 29 (12.6%) | 292 | 100% ≤ 11 (55% = 0, 68% ≤ 1, 77% ≤ 3) | 276 ≤ 15, 16 > 15 |
| C: ladder N=20,000 (5,000 Home-doll locals + 15,000 belt) | 241 | 0/241 | 177.8 | 113 (46.9%) | 128 | all = 0 | all = 0 |

The decoupling, measured: A and C give **bit-identical answer censuses** (113 empty,
128 hits, all rank 0) while C walks 5.3× more candidates — the ladder's locals
inflate the walk and never the answer (the belt itself is structurally invisible:
belt ships are doll 0, the scan filters `other.doll != me.doll`). At B the walk
carries real surprise (87% of scans non-empty — P1 refuted: the walk is *not*
deletable by an empty-answer certificate) but the surprise is local: all 292 hits
within rank 11 of 324 walked.

Also measured: the radial apsidal filter bails (walks all bodies) on 99–100% of
scans at A and B — the filter is dead weight at these scenes, confirming 96f6's
87/87 census; at C it engages (0 bails) and still walks 178 for 1-hit answers.

## Predictions

`predictions.md`, written before the flights. P1 (≥ 90% empty) **failed** — 47% at
A/C, 12.6% at B: the scan earns its keep at crowds; an empty-answer certificate
cannot delete it. P2 (all hits within along-track rank ≤ 8) **half-held**: held in
Euclidean rank (≤ 11 everywhere, = 0 at A/C), failed along-track at B (16/292 beyond
15 — the along-track projection is the wrong coordinate once a swarm has radial
scatter; taleb-09b5's rank-4 is a formation result and does not transfer to a
swarm). P3 (the filter bails) **held** at A/B; at C it engages and changes nothing.
P4 (the belt leaves candidates unchanged) **held structurally** (belt = doll 0,
zero candidates) but the run's C arm exposed the bigger fact: the locals inflate
the walk 5.3× with zero yield change — the decoupling itself.

## What would make it wrong

The rank is computed at t among the candidates the walk found; a *fast crosser*
(a body far outside the neighbour shell at t whose swept segment x+v·h enters the
window) would hit from rank ~K and break spatial locality. These scenes are slow
(lattice speeds q/2¹⁵); the sound form of the certificate is neighbour rank in the
swept metric (x + v·h), maintained incrementally — which is exactly the
beat-resident pair record the encounters page proposes as its open direction 1
(1a29). A relativistic crossing flyby is the decisive adversarial case; not flown
here. Second risk: rank was measured for the *player's* scan only; fleet-wide scans
(another body as `body`) could differ, though the same locality argument applies.

## Cost of adoption, and fit

One structure: a k-nearest neighbour set per scanned body (k ≈ 16), updated at
events (birth, kick, death) rather than walked per scan — the same record the
encounters tier needs ("store the beat"), so two topics' open directions are one
mechanism. Cost: an incremental index to maintain (the churn questions of
encounters/1a29 apply — 0.5–1.1× armed churn per kick at bare B), and the
fast-crosser case must be indexed separately (velocity-bounded split). Fit —
PRINCIPLES 3: "Compute only surprises. Cost follows change and entropy" — the
walk computes no-surprise at K-cost; principle 32: "under the right representation
many symmetries can appear" — the answer set's rank-locality is the symmetry the
walk's representation (an unranked candidate list) cannot see.

## The lens

The whole-system lens found two mechanisms that are secretly one (the scan's
walk/pin/compare and the encounters tier's per-kick re-arm: both are "one event
wakes a wholesale walk of everyone it could touch"; both are deleted by the same
stored-neighbour record). What it may have missed: the blind spot above — elegant
unifications hide hard special cases, and mine is the fast crosser; also I did not
measure whether the *held* scans (not just immediate ones) share the locality, and
the census counts the player's scans only.
