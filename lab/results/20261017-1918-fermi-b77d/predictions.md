# Predictions (written before the flights)

Question: is the ladder scene's memory headline (flat, ~5 kB/body, the 10⁵-10⁶ record) a
quiet-machine claim, or does the wall-path FLOW growth (470f/4b8c/7bd9: held scans pinning
window candidates when the frame's wall budget is starved) also grow it under load?

Arms (all coast, rtf 100, 12 ms engine budget, seed 1, threads 1, 50 s wall ≈ up to 5,000
game-s presented, Linux/x86 — orders of magnitude only):

- **A1/A2: MEMBERS=400, N=0** — the 470f FLOW scene, quiet vs 5 pinned spinners. The probe's
  positive control: under load I expect held to grow past ~50 and RSS to grow (4b8c: held
  8→83, RSS +8 MB in one window; 9/9 loaded flights grew in 470f). Quiet is bimodal (5/15).
- **B1/B2: MEMBERS=48, N=1e5** — the ladder scene, quiet vs the same load.
- **C: MEMBERS=1000, N=0, loaded** — the crowd arm (concentration), if time allows.

## Fermi estimate (before any flight)

Per held scan the capture pins ~candidates × ~400 B (7bd9's 171 kB at 428 candidates) plus
~73 small live allocations. On the ladder the player's scan sees a bounded near set —
c439: ~74 candidates/scan, identical at N=1e4 and 1e5 — so:

- pin/scan on the ladder ≈ 30-60 kB (near-set-sized), NOT belt-proportional;
- latch bound SCAN_BACKLOG × pin ≈ 2,048 × 50 kB ≈ **0.1 GB** — bounded, no ruin;
- growth under fully-starved drain ≈ scan_rate (0.1-1/gs) × pin ≈ **5-50 kB/game-s**;
- second channel (settle prune bypass, c304's ~10 kB/ship-kick): at N=1e5 the belt fires
  ~3.6 kicks/gs total (3.55e-5/B/gs), ship items are the 48 members — if the bypass scales
  with kicks it adds ≤ ~40 kB/gs; if with ship items (as c304 measured), ~nothing here.

## Held-out predictions

- **P1 (instrument validation):** A2 grows — held_max ≥ 50 and/or RSS slope ≥ 0.1 MB/s
  under load. If A2 stays flat with held_max < 10, my probe or my load is too weak and
  nothing below counts (VOID, not evidence of innocence).
- **P2 (ladder quiet, the record):** B1 flat — held_max ≤ 10, RSS end-to-end drift < 10 MB.
- **P3 (the question):** B2's growth is ≤ 10× B1's and bounded by the latch arithmetic:
  RSS growth over the whole loaded flight ≤ 0.3 GB, held_max ≤ 2,048 (the latch
  force-answers), per-scan pin (RSS slope / scans answered) in the 30-60 kB class.
  **Kill criterion for the "quiet-machine claim" defence:** B2's RSS grows monotonically
  past +0.5 GB in 50 s, or held pins scale with N (compare a B3 at N=1e4 if flown: pin/scan
  must not fall 10× going 1e4→1e5 if it were belt-proportional; equal pins ⇒ near-set).
- **P4 (crowd):** C under load grows faster per scan than B2 by roughly the candidate
  ratio (1,000 vs ~74 ≈ 13×): pin/scan ≈ 0.4-0.8 MB, so even held_max ≈ 100 pins
  ~40-80 MB; the GB-scale pin needs K ≥ ~2,000 AND held in the hundreds — the fence
  question, not flown to the latch here.

What I do NOT expect: a digest change (the FLOW is wall-path; 4b8c proved digest-equality
across budgets — I make no digest claim, my arms differ in presented game-s by design).

---

## Postscript (written after the flights and the regen run — the pre-registered text above is untouched)

- First flight set (ambient loadavg 0.4-1.2): A flat (pre-registered VOID — my 7 pinned
  spinners left a free core), B1/B2 held_max = 1, RSS flat; C loaded grew (held 268,
  514 kB/scan). On that record I first wrote "the ladder cannot starve" — **refuted
  below**.
- C1 (crowd, quiet): also grows, same per-game-s arrival (0.0966 vs 0.0968) — kills my P4
  framing "load is the multiplier" at crowd scale in this unpaced loop.
- The regen rerun landed under another window's ambient load (loadavg 9.25-13.79 on 8
  vCPU — recorded in its log): **B1 and B2 both grow** (held 375/431 at the full 0.0966
  scans/gs arrival, pin 63-71 kB/scan, RSS slope 6.9 kB/gs). P2 and P3 as stated are
  refuted: the ladder's drain starves under true oversubscription (every core contended);
  my controlled 7-way load was one core short of it. What survives across both load
  regimes and all four scenes is the pin law (~0.4-0.55 kB per candidate per held scan)
  and the fence arithmetic it implies — see the dossier.
