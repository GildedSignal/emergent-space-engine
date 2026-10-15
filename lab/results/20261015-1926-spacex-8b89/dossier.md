# Dossier — 20261015-1926-spacex-8b89 (spacex)

## Claim

The seam's demote-set class list is deleted, not extended: **`ES_LAZY_ALL=1` demotes every
keyed entry — at birth, at every settle (kick or not), passages included — and the flight
stays digest-identical on all seven scenes** (VERDICT: ALL IDENTITY, anchors = e0f9's and
3dc8's published digests), while the standing compiled arcs collapse to the 3–4 structural
doll-centre cycles everywhere (10⁴ pre-wave belt: 10,030 arcs/6.98 MB → 3 arcs/1.7 kB;
mixed comet stream: 22.5 MB → 2.3 kB; rss 979 → 20 MB, 2.4× below the demote-passages
variant's 51) — the bill is the same read stream as the variant's (+5.5% promotions on
mixed), so the only remaining never-demote class is the un-keyed Plunge, which **no
state-birth scene mints at all** (dives at peri 0.001 AU, inside the star, bind as passages:
w up to 23, ~27 kB/arc, census `plunges 0` at every cut).

## Bottleneck

Memory per live body at 10⁹ (the board's first live question; the nladder page's next rung
break: 2.4–2.7 kB a body, 4 GiB at ~1.7×10⁶). 3dc8 closed passages but named the open edge:
boundary rebindings are not kick-settled, so the seam "halves the standing arcs rather than
zeroing them", and births mint Live arcs that no kick ever settles (the belt pre-wave, the
comet bound half). The deletion: drop the class list (kick-settled / passages / rebinds /
births) — a binding stores only its generator (PRINCIPLES 6: "store the generator, not the
generated"), whatever minted it. Expected gain: the standing-arc term → 0 at every N (not
just post-kick-wave), i.e. ~3.5× on the memory rung's census (2.4 kB → 0.68 kB/body at the
belt's birth state), and it deletes `Catalogue::insert`'s per-birth slot (cae7/e4cc's churn
channel) at birth rather than after the first kick.

## Evidence

All numbers from `regen.sh` (build + `matrix.sh`; `flights/*.txt`, `regen.log`); Linux x86
8-vCPU box — orders of magnitude only, per the lab rules. The variant is `ES_LAZY_ALL=1` on
3dc8's merged patch (base reproduced bit-for-bit first: seam arms equal e0f9's counters and
digests; mixed variant equals 3dc8's `61c3a24a…`); the delta is ~60 lines: `try_demote()`
in `bind.rs`, the update site's gate `kick.len > 0 || lazy_all`, and birth demotion at
`add_body` / `add_body_state` / the hand-out spawn (heading read before the swap, so the
birth itself never mints). Doll centres stay Live (structural, ~3–4).

**Identity (P1, decisive): 7 scenes × 2–4 arms, bit-identical.**

| scene (cut) | digest (all arms) | anchor |
|---|---|---|
| 10³ coast (20k) | `df0e87cd…a45030c` | = e0f9's published ctl |
| 10⁴ coast (20k) | `5e8c9e24…5fbab6f` | = e0f9's |
| 10⁴ burn (20k) | `5caeb1b6…64c451` | = e0f9's |
| 10⁴ coast pre-wave (10k) | `561f3f58…` | new scene |
| mixed 1k comets (1.2k) | `61c3a24a…d8de06` | = 3dc8's |
| dive 200 (1.2k) | `d7751c27…1902bc5` | new scene |
| dive 200 deep (6k) | `0117488f…dad990f` | new scene |

**The deletion (P2, P5 held).** Census at the cut, ctl → all:

| scene | standing arcs ctl | standing all | rss ctl → all | b/body | catalogue_live |
|---|---|---|---|---|---|
| 10⁴ coast, cut 10k (pre-wave) | 10,030 cycles + 18 pass, 6.98 MB | **3 cycles, 1,720 B** | 36 → 17 MB | 1,373 → **680** | 10,076 → **3** |
| 10⁴ burn, cut 20k | 6.98 MB | 1,720 B | 73 → 40 MB | 1,748 → 1,055 | 10,076 → 3 |
| mixed comets | 22.5 MB (1,018 passages, w 10–20) | **2,264 B** | 979 → **20 MB** | 14,433 → 10,337 | 1,071 → 4 |
| dive (peri inside star) | 5.97 MB (218 passages, w 10–23) | 2,264 B | — | 12,622 → 8,525 | 271 → 4 |

The variant (demote-passages) holds 11.5 MB / rss 51 MB on mixed — `all` beats it 2.4× on
rss because the bound half's births and the no-kick rebinds (the class 3dc8 named open) now
demote too, so held scans and retired segments pin 113-B records, never arcs. At the belt's
birth state the standing store is 680 B/body — the nladder memory rung's 2.4 kB/body census
term falls ~3.5× before the first kick wave exists at all.

**The bill (P3 held).** Promotions are the read stream, not the demote set: mixed all
206,323 vs variant 195,659 (+5.5%); 10⁴ burn all 864,461 (seam 624,994) at p50 3.8 µs
(cycle) / 311–658 µs (passage, on 1343's curve); walls 31.0 s vs ctl 5.3 s at 10⁴ burn
(5.9×), 136 vs 39 s on mixed (3.5×) — the no-retention tax the bounded cache (0757's
`ES_RETAIN_HOT`, gold) exists to pay down; both patches compose (this one changes only what
a binding stands on, not the read paths).

**P4, half-held (reported):** dives bind as passages, zero Plunge trajectories minted by any
state birth — the never-demote rule now guards a class no flown scene can even mint (the
Plunge comes from bound plunging orbits, `NoBoundOrbit`-adjacent, none reachable from
`add_body_state`). The self-deletion at impact is slower than predicted: dead 19 → 27 of 200
from cut 1.2k → 6k (the fall from 2.5·2¹² AU outlasts the cut), so ctl's 27 kB/arc dive tail
stands for most of the fall — in `all` it is a record throughout.

## Predictions

`predictions.md` was written before the matrix. **P1 held** (ALL IDENTITY). **P2 held**
(mixed rss 20 MB ≤ 35 predicted; standing → the centres everywhere; pre-wave b/body 680,
better than the 1.0–1.2 kB predicted). **P3 held** (mixed +5.5% ≤ ±30%; 10⁴ burn 0.86 M
inside 1–3 M; wall 5.9× ≤ 6×). **P5 held** (catalogue_live 3–4 at every N). **P4 half-held:**
the passage-not-plunge half and the zero-Plunge census held; the death-rate half failed
(27 ≥ 100 predicted) — the dives' fall time exceeds the cut, an honest miss on a rate, not
on the class.

## What would make it wrong

A read path that needs more than key(+outer)+sense+unit — none exists on seven scenes, but
the Plunge class is untested by construction (no scene mints it); if one is built and its
re-mint is not pure (1343's lifetime argument), the never-demote rule must grow a compact
plunge record. The bill numbers are Linux/x86 cloud timings (orders of magnitude only); the
integrator re-measures on the M1. The wall tax (3.5–5.9× ctl without retention) is the
adoption cost — unacceptable alone, composed with 0757's bounded cache it is the cache's
input set that grows (every read mints once per eviction), so the knee arithmetic
(0619/f55d: cap = the horizon's mint bill) still governs.

## Fit with PRINCIPLES

- #6 "Store the generator, not the generated" — now with no class list: whatever mints the
  arc, the binding keeps the generator.
- #4 "Everything is emergent. No central control and no categories" — the kick-settled /
  passage / rebind / birth categories were ours, not the law's; `ES_LAZY_ALL` deletes them.
- #1 "The cheapest compute is compute not done… Delete before optimizing" — the demote-set
  rule shrinks to "has a key", and the per-birth catalogue slot dies at birth.
- #9 "A failed expectation is not automatically a failed method" — P4's death-rate miss is
  a rate miss on the dive scene, not on the class reading.

## The lens (what SpaceX may have missed)

Delete-and-rebuild is cheap for a rocket; a frozen law is a one-way door. This run deletes
a *rule of the cache layer* (not the law) with digest identity as the certificate, but it
flies no 10⁶+ rung (time): the 3.5× census claim at the next rung is an extrapolation from
bytes_per_body, not a flown MiB number, and the composed-with-retention arm (ALL + RETAIN)
is unwon — the natural next flight, and the integrator's adoption question.
