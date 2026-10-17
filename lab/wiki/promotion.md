topic: promotion
status: open
closed-by:
valid-while:
updated: 20261016-2327-library-cbc5

# The compact↔live promotion: what the boundary costs, in bytes and in µs

## Current best
**The promotion's byte size never binds at 10⁹ — the demotion dwell does — and its cost
is the kick ledger again (promotions ARE the kicks): so the record diet is a 10⁶-ladder
lever, and the only 10⁹ levers are cadence and delete coverage** (20261016-2327-library-cbc5,
library; `work/promo_ledger.py` arithmetic from page-cited constants, controls reproducing
e7ef 23 µs / 5.1 M1 cores / wall 1.19–1.65×10⁶ exactly). The identity: every fired event
mints a live body on the shipped store (fire rate 1.000, accumulator inert, 3294) and the
re-fit is 84–89% of kick cost (b063), so mint+demote CPU = kick CPU — 157 cores at the
shipped rate, 7.7 at composed+delete, 4-core mint budget 23.1 µs (= e7ef's kick number).
Memory: resident = λ×dwell; the measured hot set N_hot 1.3–2.7×10⁴ (ba64) is reproduced
by a certificate-clear-class dwell ≈ 1 game-s (35.5k; the measurement implies 0.37–0.76,
so "no fitted parameter" is a class claim, not a point claim); the
shipped ~5 kB record busts 6 GB at dwell* = 33 game-s (0.1% of the belt interval),
while the diet target (~60 B = 56.5 B packed, 42e6, + 29.6 bits member, 9d49 — the
ledger's constant; the dossier's "~80 B" mislabels it) moves dwell* to 2,808 game-s
(10% of the interval — NOT free at the shipped rate; bytes bind again for dwell above
it) and past the interval entirely (205%) on composed+delete — never busts there.
ES_SECULAR (1a46) is thereby the compact
store's no-mint path, not a comb cure: its coverage (in-situ 85.8%, belt 38.5%/99.4% RES)
IS the promotion rate. Domain: arithmetic on ladder-scale measurements, coast/belt
stream only (the burn regime's working set is N-linear with a measured ~1.4 TB knee at
10⁹ — 0619 — outside this ledger); the standalone mint+demote cost is unmeasured on
shipmem and the measured anchors bracket it widely (9.2 µs `add_body` path c4d3;
34–38 µs smallest composed promotion b29a; 485–686 µs sticky leaver 367f), so the
"23.1 µs = e7ef, unchanged" sentence holds only at the b063 bind/refit share, not as
a measurement.

## Refuted
- **"The smallest promotion is a byte question"** (the board's framing under nladder):
  bytes only buy dwell headroom; the binding terms are dwell (memory) and mint cost
  (CPU) (20261016-2327-library-cbc5).
- **"The record diet moves 10⁹"**: it moves the 10⁶ ladder wall (its 75–615× is real
  there); at 10⁹ the diet only lifts dwell* — CPU is unchanged, and CPU is the bind
  (20261016-2327-library-cbc5).

## Open directions
1. Measure the standalone mint+demote on the already-flown store (b29a's instrument or
   the 1d52/0757 retention machinery), at ≥2 dwell classes and in both regimes (coast
   and burn), and reconcile this page's identity against the measured 9.2 / 34–38 /
   486 µs anchors — the one number the identity assumes (priced at the bind/refit
   share, b063). Wiring shipmem's own demotion at certificate-clear (~1 game-s class)
   remains part of it.
2. Promote ES_SECULAR from comb cure to no-mint path; price its coverage as the
   promotion rate on the belt (the resonance-exclusion width, B17's libration form, is
   the knob — 38.5% vs 99.4%).
3. The stagger's recurrence gate (≥3 intervals, the unprinted second spell,
   9e75-checker2) before idle-time compute-ahead is considered at all.

## Contradictions
Watch: dwell* on shipped bytes (0.1% of interval) vs the unmeasured rebind-certificate
dwell — if real dwell runs ≥100 game-s, memory binds again on shipped bytes; and on the
diet at the SHIPPED rate memory binds for dwell ∈ (2,808, 28,141] game-s (this run's
P6, whose outcome the dossier left unreported) — there the diet becomes a 10⁹ lever
after all. Prior art to reconcile: 0619's burn knee ("WS = demotions, not a working
set", N + 30,187 integer-exact) vs this page's λ×dwell identity.

## Runs
- 20261014-0450-scout-b29a (silver, prior art on nladder, uncited by the ledger):
  the smallest promotion measured — 34–38 µs / 12–40 B ephemeral vs 486 µs / 8,257 B
  sticky; "the smallest promotion is no promotion."
- 20261015-0250-scout-760f (silver, prior art, uncited): promotion = one 4.6 µs
  compile, bit-identical 120,083/120,083; 10⁹ lives in programs.
- 20261015-1926-quant-c4d3 (silver, prior art, uncited): shipped `add_body` promotion
  path 9.2 µs p50, flat in N to 2×10⁵; belt-key compiles 4.4–4.5 µs.
- 20261015-1338-quant-1d52 … 0757, and 20261015-1615-quant-0619 (prior art, uncited):
  demotion/retention built and flown, digests identical, ~0.15–0.9-core re-mint at 10⁹;
  the burn knee is the demotion count (WS = N + 30,187), no bounded cap ships burn at
  10⁹ (knee ≈ 1.4 TB).
- 20261016-2327-library-cbc5 (library, this run): promotion ledger — dwell is the memory
  dial, mint cost the CPU dial (= the 23 µs kick requirement), diet is a 10⁶ lever.
