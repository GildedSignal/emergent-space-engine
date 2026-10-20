# Dossier — 20261020-0440-library-3c03 (library lens): the stride-gate survivor is the regroup mint

**Claim.** da23's surviving finality-assert fire is pinned on shipped-code state: the
published `fin_hi` that the fatal clash restores under is never set by a finality decision
— it is minted by `regroup`, which publishes the merge members' final parts (`union_parts`
→ `make_region`'s `set_final`) with no alone-ness check, right when rollbacks have left
live truths below the merge tick; blocking exactly those mints kills the fire class
(3/10 → 0/10, paired interleaved) but, as a deferral, starves every merge on the class
(merges 11→0, present 1792→538, final lead pinned at 0) — so the shippable fix is a
mint-time publication cap, not a merge deferral.

**Bottleneck.** allocator-ratchet direction 1 (the engine's one reachable crash,
`alloc.rs` "would revise its published tick", exit 101) — the ruin side (PRINCIPLES #25/#12;
"the algorithm that allocates the work … is the most important one"). Not a 10× gain: a
correctness closure that unblocks da23's gate ("the gate must not ship as the fix until the
survivor is pinned and closed" — his own dossier).

**The pin (all numbers from this run's flights; `battle 19 2400 32 8192 0.5 24 8704 4.5`,
one process per draw, Linux x86, load 2–4).**
- The fire, with provenance (interleaved draw): `PRE id=50 s=960 e=976 D=Some((32, 44,
  944))` → `RB lid=44 s0=944 aff=[(51, 976)] m=32` → `FIRE id=51 s0=944 fin_hi=976` and
  **`FIREWHY id=59 why=["merge@864"] fin_parts=[(768,11), (768,3), (864,37)] verified=960`**
  — the fired region is merge-born; every part is a donor's (owner ≠ own id); the logged
  raise site is `merge`. Earlier fires without surviving chains show the same signature:
  `fin_parts=[(976, 49)] verified=976 tick=976 giant=true` and `[(976, 48)]` — a giant at
  its merge tick holding one inherited part at exactly the merge tick.
- **Zero `alone_at` decisions on the battle class**: 0 `DECIDED` lines in 22 instrumented
  battle draws, every arm (they appear normally on other classes — 255 on `quiet`). With
  the gate on, all publication is the frontier advance (safe: bounded by min `verified`)
  plus the regroup mint (unchecked). da23's candidates (a) truth-hull radius and (b) base
  staleness are excluded: no decision exists for either to corrupt; the survivor is his
  (c), now with the exact site (`regroup`'s inherited publication) and the enabling
  condition (a live truth — often an ancestor's, spanning the merge tick — below it).
- **Arms (one build, `exposure`'s 10th arg; arms 0/1 byte-identical to da23's by
  construction, all prints env-gated `ES_FIRE_WHY`):** arm 1 = da23 gate v2: **3 fires/10**
  (2/4 block, 1/6 interleaved — the race is load-coupled; shipped s19 clean this window,
  present 1872). Arm 2 = gate + truth pseudo-members carrying their lineage id (my
  pre-registered P4): **0/10 in the author's window, then 2 fires/3 in the regen's**
  (load 6.7–15.6, the window's other runs) — inert on this class by construction (0
  decisions), so its quiet window was NED, not END, and under load it fires as arm 1
  does (lesson 5, now measured as an inversion, not an argument). Arm 3 = gate + `merge_gate` (defer a
  regroup whose union hull, slack-grown, touches any live truth starting below the
  members' max `fin_hi`/tick): **0/10 fires, 42–168 DEFERs/draw, merges 11→0, regions
  23→23 (vs →1), present 538 flat (the no-conflict floor, 3.3× down), rollbacks 0, final
  lead max 0** — the class is killed by deleting the merges, a capability delete
  (`min_region`'s splits all over again), not a fix.
- Churn class (`gas 11 600 1 8192 2.0 12 4352 4.5`, da23's unflown P4): present 1024
  identical on arms 0/1/3, one region, no merges — the gates neither starve nor change it
  (weak control: this seed collapses to a single region; 01e7's selfchurn protocol was not
  re-flown).
- `cargo test --release -p emergent-allocator`: 14 passed, 0 failed with every switch in
  (defaults off).

**Predictions** (`predictions.md`, written before the decisive runs): P1 refuted on its
letter — I predicted `alone`, measured `merge` (da23's (c); the mechanism this run adds:
the mint's enabling condition and its proof chain). P2 refuted (no decisions exist on the
class; the ids-empty hole (d) I added from reading the gate is real as a design gap but
unreachable here). P3 moot (the recompute at `t = fin_hi` is empty: the fired region is
skipped from its own coalesce — itself a fact: the fire's region is outside its own
finality view). P4 refuted as a fix (arm 2 inert, 0/10 is the race). P5 held, weakly
(single-region gas). The pre-registered kill criterion (arm-2 fires with truth-touch, or
arm-2 starvation) never fired because the arm never acts on this class.

**Evidence commands.** `./regen.sh` (~4 min): applies `work/patch.diff` (da23's base +
this run's instrument and arms; saved from the tree, 500 lines), builds, tests, chases the
arm-1 fire with the instrument, runs the interleaved 3×3 incidence matrix, flies the gas
class, and verifies the five quotes byte-exactly against a fresh Readwise fetch (4,590
highlights; falls back to the kept `highlights_flat.json` offline). Raw draws kept in
`work/matrix/` (this window's full record).

**What would make it wrong.** The pin rests on three independent prints (PRE's D, RB's
affected, FIREWHY's owner/chain) agreeing on every fire; a fire whose FIREWHY shows
`alone@…` or `frontier@…` with the same topology would reopen (a). The arm-3 conclusion
(kill-by-starvation) rests on `present 538` being the no-conflict floor; if a load-matched
shipped arm also sits at 538 in some window, the 3.3× is overstated. The mint-cap fix is
designed, not built (lesson 2's decision): its adoption cost is one bounded change in
`regroup`/`make_region` plus the empty-parts case (`set_final`'s `expect`), and the freeze
bar is the same paired-interleave protocol with ≥ 3 windows (lesson 5).

**PRINCIPLES.** #25 "not making mistakes matters more than doing things efficiently, don't
multiply by zero" — the crash deletes the process, so the mint gate precedes every
throughput argument (da23's own framing, continued). #19 "a fix signals the wrong
representation": two gates on finality decisions could not see a publication path that
never decides — the representation of "publishing" (three call sites, one unchecked) was
the wrong place to stand. #12/#27: arm 3's 538 present is the honest price of a blunt
gate, measured the way the player runs it.

**The lens** (Julien's library, 5/5 quotes byte-identical, `work/check_quotes.py`):
reversibility prices the mint (FS); downside-clipping must not delete the upside
(Taleb, Antifragile); the map/territory split is the id-vs-snapshot asymmetry that makes
the fire (Korzybski); don't fool yourself with guards over paths that never run (Feynman);
clean draws on an inert arm are NED, not END, and only paired interleavings count (Taleb,
The Black Swan). What the lens may have missed: the quotes frame decisions, but the fix's
engineering (the empty-parts case, the cap's floor choice) is builder work; and I did not
re-fly 01e7's selfchurn protocol, so the churn-class safety of the eventual cap is still
da23's open P4 in its strong form.
