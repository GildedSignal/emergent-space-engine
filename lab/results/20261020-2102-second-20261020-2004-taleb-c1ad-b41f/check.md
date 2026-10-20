Grade: silver

**Abstract.** v6 — v5's floors rebuilt as a geometric pair scan mirroring certify's clash
predicate (death-horizon touch), verified-only base, coverage-aware cap — un-stalls the
checker's kill scenes at v4's exact present: reproduced bit-exactly in the runner's regen
(clumps 2695, mixed 2698, streams 2698 vs v4's 2577-2624/819; v5 still 0/0/1024; crush 0/12
both arms, v6 median 1.9-2.6× v4 across two windows). But the safety half did not fully
reproduce: the regen window fired v6 once on battle s19 — the finality assert itself
(region 53, fin_hi 896 > s0 816, RB m=80 > 0); four immediate re-runs clean, v4 clean — a
rare interleaving, not a deterministic kill, yet it falsifies "exactly safe" as stated.
Patch applies clean to 2a2afff2; adoption cost small but the fire must be closed first.

**Reasons.**
1. *Reproduction (regen.sh, runner-executed, exit 0; I applied nothing further — patch was
   already in the tree at base 2a2afff2).* Family: identical to the author in both windows
   — clumps 2695/2695/0/2695, mixed 2698/2698/0/2698, streams 2698/2624-819/1024-819/2698,
   quiet 2698 everywhere (shipped/v4/v5/v6); v5's kill reproduces. Crush: 0/12 fires both
   arms in both windows; v6/v4 median 1.94× (author) and 2.6× (regen); 0 CAPGAP. Numbers
   that differ, all in battle: shipped 1/6 → 3/6 fires (s15/s17/s21 vs s21; window
   raciness the author disclosed for P3), v6 0/6 → **1/6: s19 exit 101**, equality law
   97 RB all m ≤ 0 → 78 RB with **1 m>0** (the firing rollback itself).
2. *Predictions.* Pre-registered: predictions.md mtime 21:32:33 precedes the decisive
   protocol (21:32:45–21:36:43); the smokes and the disclosed s13 fire/fix preceded them.
   P2 held exactly in both windows; P5 held in both; P3 marginal exactly as disclosed
   (regen v6 battle median 1536 vs shipped-clean 1792). P1 and P4 held in the author's
   window and broke in the regen window: one fire, one m=80. A "0 fires on every draw"
   claim is a window-free claim; it did not survive the first independent window.
3. *Attack.* (a) The fired seed re-flown: v6 s19 ×4 clean (present 833 each) + v4 s19 ×2
   clean — the fire is a rare interleaving, not deterministic. (b) Fresh seed 41, outside
   the author's battle set: clean, present 928. (c) 2× scale (galaxy 17408/48, beyond the
   author's range, the previous checker's probe): v6 s11/s13 clean (present 432/560);
   shipped clean this window too — no fire reachable there in one window. (d) The regen
   window itself. Diagnosis hook: the regen's non-fired battle draws sit at zero slack —
   44 of 57 RB lines exactly m=0 — so any publish that slips one event past the pin
   computation goes positive. The FIRE victim (aff=[(53,896)] only, verified=s0=816,
   fin_hi=896) published past a tick its own later stride restored to; the suspect paths
   the author did not examine: `cap_final` after rollback re-caps only `restored.last()`
   (one id, and only after the assert has already run), and a truth born after the
   publisher's floor computation (floors cap future publishes; they cannot retract a past
   one except through the restore path).
4. *Novelty.* Not a repetition. f1ca's checker named the shape ("per-region floor, deepest
   restorable tick among truths that can still touch this lineage"); c1ad built the
   window-keyed version (killed); this run builds the geometric one and adds two measured
   mechanisms absent from the page: the ignition deadlock (v5's `history[0]` base term is
   a restore-point term; prune pins it at the sync floor, so the goal cap holds the
   frontier inside the first sync grid forever — the checker's clumps/mixed present-0
   explained) and the death-horizon touch test (the earliest-scan hull misses pairs a
   later scan clashes on — which also voids v5's lscan closure, so v5's battle 0-fires
   were incidence). Both fold into the page; the page's measured lines match the evidence
   bar the bracket I added (the "0 fires" headline overstated window-free; corrected in
   place).
5. *Goal fit.* The engine-side publish/rollback boundary is the ratchet page's #1 and the
   board's smoothness line ("the algorithm that allocates the work … it's the most
   important one"). The liveness half deletes v4's global-floor starvation at ~2× v4's
   present under crush. PRINCIPLES: "if you find yourself fixing things that's oftentimes
   a signal that it is the wrong representation" — the window-keyed terms were the wrong
   representation of "can these two lineages still meet", and v6 replaces them with
   certify's own predicate; "the simulation tells us what's next not us" — the floor now
   reads the law's own reach bound, not window arithmetic.

**The one experiment to gold.** Diagnose the s19-class fire to its publish path (ESE_STRIDE_DBG
on repeated battle s19 draws until it fires, or derive it: the two suspects above), close it,
then re-fly the battle protocol across ≥3 windows (≥18 draws): 0 fires and every RB m ≤ 0 in
all windows, with the family and crush halves re-checked once. The liveness criterion the
previous checker named already stands.

**What the author missed.** A zero-slack floor (44/57 margins exactly m=0) is one
interleaving away from m>0 in a multi-threaded, wall-clock-paced allocator; the author
disclosed window raciness for cost (P3) but claimed fire-freedom (P1) off a single window —
a Taleb lens should have flown the second window before claiming exactness, and the lens
note admits the adversarial scene was never composed. The rollback re-cap's single-id scope
(`restored.last()`) and its ordering after the assert were not examined despite being the
natural place a past publish escapes a floor. The pair scan's cost is unmeasured beyond 23
regions (disclosed). The page headline "0 fires" and P4's "every m ≤ 0" needed window
qualifiers; corrected in the page.
