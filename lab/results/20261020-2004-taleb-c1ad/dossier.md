# Dossier (lab 20261020-2004-taleb-c1ad, taleb)

**Claim.** v5 — per-region publish floors on both finality publishers plus merge-capping —
closes the allocator-ratchet page's named next step: it keeps every v5 draw fire-free where
shipped fires (battle 0/8+0/12 vs 1/8) and it unpins finality from a laggard under crush
(median present 355 = 92% of shipped, against v4's 256 = 66%), with the restore instrument
shut (257 RB lines, every m ≤ 0, `out=[]` on all).

**Bottleneck.** The page's own #1 (the engine-side publish/rollback boundary): f1ca's v4
global floor is exact but load-min-coupled — under crush one never-accepting region pins
`floor0 = 0` and the engine starves. v5 decouples: a laggard pins only its lineage.
Expected gain: finality that is both exact and load-robust (the fix's shape, not yet a 10×
on any board number — see "what would make it wrong").

**The mechanism (derived, then measured).** For region r, the s0 values a future clash that
asserts r can carry are: starts of live truths keyed at windows r's strides still span (r is
a party; `certify` scans only the stride's windows); for live truths of r's lineage, the
truth's start or the least stride-start of a live region whose strides can still span that
window (a stride spans ≤ stride_max windows — this bound is what keeps a far laggard from
recoupling everything); r's own verified, oldest snapshot, and least verified among its live
ancestors. `publish_floors()` computes this per finalize; both the frontier advance and the
gated coalesce cap candidates at it; `cap_final()` re-caps inherited `fin_parts` at every
merge and rollback (a merged child inherits the other parent's high parts with a
stale-truth lineage — `regroup` purges no member truths). NOT capped by the global frontier:
the floor's argument never references `front` (my first build capped it; the crush showed
v5 at 74% of shipped until the cap was removed — the cap was the residual coupling).

**Evidence** (one binary, env arms: gate 0 = shipped; gate 1 + `ESE_FLOOR=v4` = f1ca; gate 1
[+`ESE_FLOOR=v5`, default] = v5; harness f1ca's `exposure.rs` + a `mixed` class; one process
per draw, fire = exit 101 + the finality assert; Linux/x86, orders of magnitude):
- **Battle protocol** (galaxy 8704/24, rate 2400, margin 0.5, 4.5 s, seeds 11-25 odd):
  shipped fires 1/8 (s21: `FIRE id=36 s0=512 fin_hi=544`); v4 0/8; v5 0/8. Present, same
  window: shipped median 1456 (7 survivors), v4 1280, v5 1280 (v5 1792 on s11/s19 — at or
  above shipped's best). Second window (fixed build, v5 only): 0/8, present 1280-1792,
  95 RB lines all m ≤ 0.
- **Crush, 12 concurrent battle draws** (sequential blocks, same seeds 11-33 odd): shipped
  median 387, v4 256 (66%), **v5 355 (92%)**; fires 0/12 in every arm; v5's 46 RB lines all
  m ≤ 0, `out=[]` all.
- **Equality law (P4):** across all v5 arms, 116+95+46 = 257 RB lines, every `m ≤ 0`,
  `out=[]` on every one — restores never land above published ticks.
- **Quiet control:** 8-island scene clean in every arm (0 fires, 0 rollbacks, present 2698).

Commands: `regen.sh` (≈4 min) regenerates all of the above from `work/patch.diff`.

**Predictions** (`predictions.md`, written before the decisive runs): P1 held (0 fires
everywhere v5). P4 held (law shut, 257/257). P5 held. **P2 half-failed at its band:** I
pre-registered v5 ≥ 3× v4 under crush; measured 1.39× median — because v4 itself only fell
to 66% of shipped in this window (f1ca's 43-vs-529 starvation was their window's load;
mine never pushed v4 that low). The decoupling is real (92% vs 66% of shipped, every v5
draw > every v4 min) but the 3× band was tuned on f1ca's window, not mine. P3 held (v5
quiet present ≥ shipped's median draw-for-draw in the second window, 1280 floor = v4's).
**Held-out negative, disclosed:** the deterministic-laggard scene (`mixed`) does not
lagger on this box — 2500 far single-body regions get through their strides (present 544-
883, no pin) and a dense far blob verifies like an island; the class ships in the patch for
the checker, the crush stays the laggard protocol.

**What would make it wrong.** v5's exactness rests on one assumption v4 did not need:
`affected` = the clashing lineages' descendants closure (measured `out=` shut on 2,714 RBs
by e517/c749 and on 257 more here; the union-find snapshot-sharing sibling that opens it
would fire v5 where v4 stays exact). The stride-span bound (`stride_max` windows) is
config-true, not law-true: a config with unbounded strides or a future stride policy change
invalidates `lscan`. Fires are wall-clock-racy: 0/20 here is one window's evidence, the
same class as f1ca's 0/8 regen vs 3/8 — the state certificate (P1's derivation) is the
claim, the draws only failed to falsify it. Adoption cost: ~90 lines in `alloc.rs` on
f1ca's arm, O(truths + lineage edges) per finalize (present tracked shipped on every quiet
draw, so the overhead is inside the noise on these scenes; unmeasured at 10⁶ regions).

**Fit with PRINCIPLES.** "its risk of breaking makes anything you do to improve it or make
it 'efficient' inconsequential unless you first reduce that risk of breaking" — the fire is
the ruin channel and v5 closes it without the starvation tax; "the simulation tells us what
s next not us" — the floor is read off the live truths and lineages (the simulation's own
state), not a heuristic budget; deletion: no new mode, v4/v3/off are env arms of one path.

**The lens.** Taleb pushed for the ruin channel first and via negativa (the `front` cap was
my own unnecessary part — deleting it was the fix); it also made me pre-register a 3× band
on another window's starvation number — a fat-tail humility lesson applied to myself: the
honest number here is 92%-of-shipped vs v4's 66%, window-owned like every incidence on
this page.
