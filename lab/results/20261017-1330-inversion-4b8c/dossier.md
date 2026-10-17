# Dossier — 20261017-1330-inversion-4b8c

**Claim.** The play-time memory growth (470f's bimodality) is the idle-time inversion: the engine's
two cleanup channels — the held encounter scans and the frame-start history prune — are both
scheduled behind the wall budget, so the engine hoards memory ∝ game-s exactly on the slow-machine
path, while the game state stays digest-identical; the "bounded" backlog cap is itself the measured
220 MB peak of 470f, and it scales with concentration, not with the comment's "about 10 KB".

**Bottleneck.** Memory at 10⁹ in 8 GB (board item 4; the memory-h-live page's open mechanism lead:
"prune-starvation"). The inversion: what makes the frame *worse* (a slow, hot, loaded machine)
makes memory *worse* — opposite coupling to the game's requirement. Names the mechanism the page
left open and deletes the "bimodal, wall-path-dependent" mystery: one knob (`--engine-ms`) flips
both paths at will.

**Evidence** (Linux/x86, shared box, threads 1, seed 1; `RUIN_PROBE` adds eprintln lines only;
regen: `sh lab/results/20261017-1330-inversion-4b8c/regen.sh`, ~3 min):

- **Dose-response, members 400, rtf 100, 20 s (cut 3,980 game-s):**
  | engine-ms | held backlog | RSS | presented |
  |---|---|---|---|
  | 50 | 0 throughout | flat 45.0 MB | 1,998 game-s |
  | 5.0 | bimodal at the shipped default (3 executions: flat ≤1 held; grew held 8→83, +8 MB; grew held 67, 48→52 MB) | 47-52 MB | 1,317-1,610 game-s |
  | 0.5 | grows while the game crawls | play growth, settle spike to 81.7 MB | 67 game-s (P5 lag) |
  Digests **identical** across all three (`2713edb5639d7a16…`): wall-path only, law innocent.
- **The drain margin is marginal at the shipped default:** three executions of the same 5.0 arm
  split by ambient load (2 grew, 1 flat) — 470f's bimodality reproduced by knob, not by luck. The
  drain condition (`room ≥ 2·max(scan_ns, 750 µs)`, universe.rs:1190) sits at the edge of 5 ms.
- **Play-phase channel = held scans** (universe.rs:772 → encounter.rs `Held::capture`, pushed per
  resolved player item): members 100, rtf 300: held 11→157 over 124→2,892 game-s, RSS +12 MB →
  **4.5-4.9 kB/game-s** (470f measured 3.9 under load) ≈ **84-94 kB per held scan** (the code
  comment says "about 10 KB each"). 470f's 220.9 MB peak at members 400 ≈ `SCAN_BACKLOG`(2048) ×
  ~105 kB/scan: **the cap, not a leak**.
- **Catch-up spike, cut 27,500 game-s (rtf 300, 0.5 ms):** END RSS after the settling flush
  (held→0) is itself wall-path-dependent with the digest fixed: under load, first pass, 46.1 MB
  (m100) / 163.4 (m400) / 163.8 (m800); quiet regen pass (the saved `data/` logs), 24.0 / 44.9 /
  46.1 MB — same digests (`ea80d6e6…` m100; `a35637d9…` m400 = m800). The loaded pass's spike
  exceeds what the (≤19) player-item scans pin: the second channel is the settle's prune bypass
  (c304's ~10 kB/ship-kick, 4,751 ship items here) — same disease, one cause: cleanup runs behind
  the wall. The per-scan pin saturates with the scan window's concentration capacity (m400 = m800
  in digest): the "bound" is ∝ bodies-in-window — the concentrated-fleet case, not the spread belt.
- All scans flush at the cut (`settle` → `drain_scans(None)`); RSS stays at the peak afterwards
  (allocator retention, as the page recorded).

**Predictions** (predictions.md, written first): P3 (digest equality) and P5 (presented lag) held;
P1 ("control flat at 5.0") was refuted under ambient load and held on the quiet box — that is the
bimodality itself, now knob-controlled; P2 held with a location correction (the cap-scale spike
lands in the catch-up settle, not in starved frames — the crawl slows scan generation as much as
draining); P4 held to window saturation (400 = 800, same digest), disclosed above.

**What would make it wrong.** A checker run on a quiet box where the 0.5 ms arm shows no growth
and the 50 ms arm is indistinguishable (then the knob claim collapses); or held-scans growing
without RSS tracking (then the per-scan attribution is wrong). The 84 kB/scan figure is
RSS-slope/held-slope on one arm — an instrument counting the pinned `Arc`s directly could move it
×2. The settle-spike decomposition (scans vs prune-bypassed history) is arithmetic, not separately
instrumented; c304's per-kick figure carries that half.

**Cost of adoption, fit.** The fix direction is one sentence: cleanup must be game-time-owned, not
wall-owned (prune on a game-s cadence; scans answered or *dropped* at a game-s cadence, since their
answer feeds only the count/log/hash — universe.rs:206). Cost: a small law-visible-none change
(scan answers are hashed, so *when* they are answered must stay canonical — dropping must be
canonical too); deletes the 2048-scan cap as a memory term and the catch-up spike. PRINCIPLES:
"the algorithm that allocates the work … is the most important one" (12) and "no work for no
reason" (14) — cleanup behind the wall budget is work done *because* the machine is slow, the
purest inversion of both. "Errors never compound" (13): this is memory compounding on the same
schedule.

**The lens.** Inversion found it: I asked what the engine does when the machine is *worst*, and
the answer is "hoard". The lens may have missed the spread-belt case (the page's flat 3,000-body
belt: the apsidal window holds few bodies there — the bomb is concentration, the board's first
risk, not population), and it did not fly a burn arm (thrust changes the player's item rate and so
the scan rate; the burn's backlog dynamics are unmeasured here).
