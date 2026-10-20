# Dossier (lab 20261020-2102-second-20261020-2004-taleb-c1ad-b41f, second author)

**Claim.** v6 — c1ad's v5 rebuilt with a geometric pair scan (touch test grown to the truth's
death horizon), a verified-only base term, and coverage-aware merge-capping — meets the
checker's gold criterion: it matches v4's present on every multi-cluster class the checker
killed v5 on (clumps 2695 = v4 2695, mixed 2698 = v4 2698, streams 2698 > v4 2577/819; v5
reproduces its 0/0/1024 stall in the same window) while staying 0-fire where shipped fires
(battle 1/6 vs 0/6, crush 0/12, equality law shut on 97+44 RB lines, `out=[]` on all).

**Bottleneck.** The page's #1 (the engine-side publish/rollback boundary): the checker
killed v5 as a configuration — its floor terms were keyed by window with no geometry, so
distant clusters' live truths pinned unrelated regions and the heterogeneous family stalled
at present 0. Two mechanisms found and fixed here; v6 is f1ca→c1ca's line at
protocol strength on the full shipped scene family.

**The two stall mechanisms (measured).**
1. *Ignition deadlock* (clumps/mixed present 0, deadline misses 1080/1080 frames): v5's base
   term `history[0].tick` is a restore-POINT term, not a clash-s0 term — but prune keeps
   history[0] at the last sync floor (quantized at `stride_max·window` = 256), so while the
   frontier is inside its first sync grid every floor is 0, nothing publishes, the present
   stalls at the observer's own cluster, the goal cap (`present + ahead·rate` = 180 at rate
   600) keeps the frontier below 256 forever. The assert compares against the clash tick
   (a stride start or truth start, both ≥ `verified`), never the walk-back point — the term
   was over-conservative, and fatal. Dropped: base = `verified`.
2. *Window-keyed coupling* (streams 1024, cross-cluster pins): v5's suffix-min `sm` and
   scanner-min `lscan` aggregate truths by window across the whole universe. Replaced by one
   pair scan mirroring certify's clash predicate: region r can scan a live truth keyed at
   window w ≥ w(r.verified) only from `s ≥ boundary(w − stride_max)`; the pair pins both
   lineages at `min(s, t.start)` iff the truth touches r's hull — grown to the truth's
   DEATH horizon (`boundary(w+1) + sync() − verified + stride_max·window`), because the scan
   can happen at any start until the truth is pruned and r keeps approaching until then.
   Distant truths pin nothing: cluster gaps (460k units) exceed the death-horizon growth
   (~80–230k) at lockstep advance rates.

**Two v6 build bugs found by their own panics (not in v5's flown windows but latent in it).**
- `cap_final`'s retain can drop a whole parent's lineage from the view — `fin_parts`
  partition bodies by parent lineage (`a view holds every body once`, 5891/8704 then
  8190/8704). Fix: retain, then if coverage breaks, rebuild from the deepest complete
  history entry ≤ cap (completeness in `merged_history` = every then-lineage held a
  snapshot = all bodies covered at one tick); deepest complete at all as last resort
  (`CAPGAP`, logged — 0 occurrences in the whole protocol).
- The first geometric build FIRED on battle s13 (victim = the truth's own writer, fin_hi 768
  vs s0 640): the earliest-scan hull missed a pair a LATER scan clashed on (r grows toward
  the truth until the truth dies). The death-horizon touch test is the fix; s13 and 5 more
  battle seeds now clean. This is also a hole in v5's `lscan` (it reads only current
  verifieds; a region dropping into range later is invisible to it) — v5's 0-fires were
  incidence, not closure, on this class.

**Evidence** (one binary, env arms: gate 0 = shipped; `ESE_FLOOR=v4|v5|v6` under gate 1,
v6 default; harness f1ca's `exposure.rs` (classes gas/battle/streams/quiet/clumps/mixed),
one process per draw, fire = exit 101 + FIRE lines; Linux/x86, orders of magnitude;
`work/protocol.log` holds the run, `regen.sh` regenerates every number):
- **Battle** (galaxy 8704/24, rate 2400, margin 0.5, seeds 11–21 odd): shipped **1/6**
  (s21 exit 101), v4 0/6 (present 1390–1792), **v6 0/6** (present 1440–1792). Held-out
  seeds 19/21 clean under v6; shipped fired 21.
- **Family** (rate 600, min_region 32, seeds 11+13): clumps 2695/2695/**0**/2695,
  mixed 2698/2698/**0**/2698, streams 2698/2577–819/1024–819/**2698**, quiet 2698 all arms
  (shipped/v4/v5/v6). The checker's criterion — v6 at v4's 2695/2698/2698 — met on every
  class, exceeded on streams.
- **Crush** (12 concurrent battle draws/arm): v6 0/12 fires, present median 529.5
  (289–769); v4 0/12, median 272.5 (43–435) — **v6 ≈ 1.9× v4** under crush, 0 CAPGAP.
- **Equality law:** v6 97 (battle) + 44 (crush) RB lines, every `m ≤ 0`, every `out=[]`;
  family draws had 0 rollbacks.

**Predictions** (`predictions.md`, written before the protocol; the death-horizon fix and
the family/battle smokes preceded it — s13's fire and its fix are disclosed above): P1 held
(0 fires everywhere incl. held-out seeds and crush). P2 held exactly. P3 marginal: v6 battle
median 1536 vs shipped 1676 — same window band (shipped swung 1456–1984), below the letter
of "≥ shipped's median". P4 held. P5 held — and better than feared: the death-horizon
growth does NOT recouple under this crush window (v6 1.9× v4, not v4-like).

**What would make it wrong.** The crush recoupling is window-owned: a laggard that stalls
the frontier keeps truths alive and the death horizon grows without bound — the pin then
degenerates toward v4's global floor (this window's laggards moved; a pinned-forever
laggard was not flown). The pair scan is O(regions × live truths in range) per finalize and
at every merge/rollback cap: unmeasured at 10⁶ regions (spatially prunable — the page's
cost note). The `affected`-closure assumption is inherited (measured shut here on 141 more
RBs). `CAPGAP` (a parent younger than the pin) never fired, but if it ever does, the child
sits above its pin and holds publication — a liveness wait, not a fire, but it must be
observed before adoption. The descendants-closure derivation (open 1(a)) remains
load-bearing.

**Fit with PRINCIPLES.** "if you find yourself fixing things that's oftentimes a signal
that it is the wrong representation" — v5's two window-keyed terms were the wrong
representation of "can these two lineages still meet", and the fix is certify's own
predicate, not a tighter window heuristic; via negativa: the base term DELETED (the
restore-point term) is what un-stalled ignition — the cheapest compute is compute not
done. "the simulation tells us what's next not us": the floor now reads geometry (the
law's own reach bound), not window arithmetic.

**The lens (second author).** The instruction was "do exactly the checker's named
experiment"; the honest path needed two unplanned stops (the view-coverage rebuild and the
death-horizon fix) because v5's cap and scan were never exercised on heterogeneous scenes —
the checker's kill was the first real load on them. What this lens may have missed: the
10⁶-region cost of the pair scan, and a held-out adversarial scene of the checker's own
(beyond the shipped family) — the window ran out before composing one.
