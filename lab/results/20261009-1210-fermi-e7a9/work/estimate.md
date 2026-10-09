# Fermi estimate and extrapolation (the numbers behind the dossier)

## Measured (the plane, seed 1, 48 members, unpaced, Linux x86)

| run | game-s | live bodies | carried by | bits/body | created /game-s | reabsorbed /game-s | net /game-s | kicks | bits/kick |
|---|---|---|---|---|---|---|---|---|---|
| rtf 1, 55 s | 55 | 39 | 17 | 44.9 | 32.7 | 0.95 | +31.7 | 16 | 98* |
| rtf 100, 55 s | 5,500 | 49 | 34 | 66.2 | 1.61 | 1.02 | +0.59 | 1,937 | 4.4 |
| rtf 1000, 55 s | 55,000 | 45 | 43 | 72.7 | 0.375 | 0.321 | +0.054 | 9,287 | 2.2 |
| --members 5000, rtf 100, 20 s | 2,000 | 221 | 201 | 85.4 | 23.4 | 12.7 | +10.7 | 7,399 | 6.1 |

*rtf 1's bits/kick is the initialization jump (the first frame's 0 → ~1,500 bits) over 16 kicks.
Decisions: 28 words = 224 bits at every rtf (the canonical log scales its ticks with rtf, so
decision density in game time falls as 1/rtf).

Digest: seed 1, rtf 100, 6 s, unpaced → `a7d089f9…1ca8df7` before the patch and after it.
All 52 `emergent-universe` tests pass after it, including the plane's digest tests.

## Reading

1. **The stock is a stable width, not a growth.** A body carrying a remainder carries ~70–90 bits
   (four integers of ~18 significant bits), from 45 to 221 live bodies. H_live's stock is
   (kicked fraction) × ~80 bits + program bits.
2. **The flow decays with game time in this scene** (creation 32.7 → 1.61 → 0.375 bits/game-s as
   game time grows 55 s → 1.5 h → 15 h): the battle ends, ships leave (leavers 48, lost 31) and
   encounters collapse (354 → 84 for 10× time). Reabsorption tracks creation at 86–97% once past
   the transient.
3. **The dashboard's bytes/body vs bits/body:** 5,143–6,089 bytes stored against ~73–85 bits of
   live information — ~600×. The representation, not the information, is the memory bill.

## Extrapolation to 10⁹ (Fermi, orders only)

- Program (belt, gold components-98bc): 0.126 bits/body → ~16 MB. Irrelevant.
- Exception stock: 80 bits × kicked fraction × 10⁹. Even every body distinguished: 10 GB — at the
  8 GB line; any generator coverage puts it far under. The 64-bit line is the all-exceptions
  worst case, and the plane's fully-distinguished scene sits at 72.7 bits: within 1.1×.
- Distinction flow at the 15 h per-body rate (0.0083 created, 0.0012 net bits/game-s/body):
  ~1 MB/s created, ~0.15 MB/s net at 10⁹ bodies — bandwidth-trivial on a 60 GB/s M1. The
  rebind machinery must annihilate ~86% of 1 MB/s: also trivial.
- So **H_live does not break 8 GB at 10⁹; the per-distinguished-body representation width does**
  (5,143 B/body × 10⁹ = 5 TB as stored today). The floor argument says the compression headroom
  is ~600×, which is shipmem's premise, now with a measured numerator.

## Caveats

- The plane is a war scene: every body is individually managed (an exception). A belt's H_live
  needs b-belt-wire's population programs; this run gives the exception side and the ceiling.
- The net slope (bounded but positive at +29 bits per 10× game time) is measured on a scene that
  quiets; a steady-encounter belt may hold creation flat. Next rung: H_live on the belt.
- Linux/x86 cloud timings; orders of magnitude only.
