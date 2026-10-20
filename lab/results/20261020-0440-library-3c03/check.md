Grade: lead

**Abstract.** Claim: da23's surviving fire is pinned on the regroup mint, so the fix is a
mint-time cap in `regroup`. Apparatus reproduced (regen exit 0; tests 14/0; quotes 5/5 on a
fresh 4,590-highlight fetch; arm table, starvation and gas numbers all match). But the
headline is contradicted by the author's own kept logs: 3 of their 4 fires (and all 4
checker-window fires; 7/8 pooled) are minted by the **rollback restore** (`make_region` at
alloc.rs:1480, `union_parts`-fed, the one raise site the instrument does not label — hence
`why=[""]`), not by `regroup`; a regroup mint notes itself unconditionally and reuses ids
for single members. The cap as designed would not close the class. Corrected pin, arm
pricing, DECIDED domain and the next experiment are recorded in the corrected wiki page;
nothing adoptable this run.

**Reasons.**

1. **Reproduced.** `./regen.sh` exit 0 in a clean tree: tests 14/0; chase fire caught
   (try 3); interleaved table arm1 2/3 fires, arm2 1/3, arm3 0/3 with 126 DEFERs, merges 0,
   present 538; gas 1024 identical on arms 0/1/3; quotes byte-identical on a fresh fetch.
   Author's kept matrix matches the dossier: arm1 3/10, arm2 0/10 (author window), arm3
   0/10, present 538 ×10, merges 0 ×10. predictions.md (04:49:13) precedes every decisive
   draw (04:53+). Pre-registered refutations reported honestly.

2. **The headline is contradicted by the author's own log.** The dossier's pin ("it is
   minted by `regroup`") rests on one fire (`ix.1.a1`: `why=["merge@864"]`, three donors —
   a genuine regroup mint). The other three author fires (`s19g1.2`, `s19.a1.2`,
   `s19.a1.3`) and all four checker fires show `why=[""]` with a single donor part, each
   immediately preceded by `RB lid=<donor> s0=<mint tick>` restoring exactly that donor at
   exactly the fired region's `verified`. Proof this is the restore path: (a) the `merge`
   note at the regroup site is unconditional for fresh ids and cannot have been drained
   (the mint is the newest buffer entry; the fire follows within lines); (b) a regroup of a
   single member reuses its id (`reuse` in `regroup`), so a fresh id holding one donor's
   parts is not a regroup mint; (c) `make_region(Some(fin))` has exactly two callers —
   `regroup` (instrumented) and the rollback restore (not). The dossier reads these
   fires as "a giant at its merge tick" — that tick is the restore tick. Per the lab rule
   (a headline the log contradicts), the run loses its grade.

3. **"0 DECIDED, every arm" is false, and the domain matters.** The author's own
   `matrix/s19.a0.err` (shipped arm) holds 91 DECIDED lines (self-truth only); zero holds
   only on the gated 8704 arms. My outside-range case (galaxy 12288/36, margin 0.5, gate 1,
   6 draws clean — incidence agrees with c749's checker) shows 8 DECIDED, two of them
   single-member groups publishing past **foreign** truths starting 512 at t=656:
   the author's predicted hole (d) is live at the next scale, so arm 2 (truth ids) is
   inert only at 8704, not by construction. The draw count "22" matches no subset of the
   34 kept battle draws. The 514 DECIDED I measured on `quiet` confirms the instrument
   works (author said 255).

4. **Arm 3's 0 fires is not evidence for the pin.** It defers every regroup (42 DEFERs per
   draw, flat — the dossier's "42–168" regenerates as 42 on all 13 draws) and collapses the
   scene to present 538; since the fatal mints were restores, the gate never touched the
   mechanism it was credited with killing. The starvation measurement itself is real and
   stands, as does the author's own "not a fix" conclusion.

5. **What survives.** The fatal `fin_hi` is never a finality decision on the gated 8704
   class; it is inherited publication minted onto a fresh id with no alone-ness check — at
   the restore (7/8) or regroup (1/8) — right when live truths sit below the mint tick.
   The author's lesson 3 (the mint must inherit its members' live truths) already points
   at the correct fix; lessons 1–2 and the dossier name the wrong site. The NED/END
   protocol point (arm 2 ≈ arm 1 at 8704, fires return under load — regen 1/3) is
   reproduced and correct. Novelty: no prior run instruments fire provenance; da23 left
   the survivor open, and this run's kept data answers it — with the correction above.

6. **Goal fit.** The bottleneck is real (the engine's one reachable crash; PRINCIPLES #25
   "don't multiply by zero") and the run respects #10/#26. But the deliverable — the fix
   site — is wrong, so nothing is adoptable within one step.

**The one experiment that would make the next run gold.** Instrument and cap the restore
mint (and the regroup mint) — inherited parts publish only down to the touchable truths'
floor, the mint inherits its members' live truths — then fly this run's own paired
interleaved protocol at 8704 and 12288 (where decisions and foreign-truth publication
exist) under load.

**What the author missed.** The `why=[""]` fires were in their own logs with the
preceding RB restore lines; the instrument's missing site (restore `make_region`) was the
one that mattered; "every arm" and "22 draws" were checkable against their own files; the
arm-2 inertness claim was generalized from one scale; the DEFER range and the quiet count
were not regenerable as stated.
