# Dossier — the survivor pinned to the ungated publisher; the naive close starves

**Claim.** The checker's named experiment is done in its cheapest decisive form: the
s19-class fin_hi is published by an ungated `set_final` path — on the battle class the
**entire stride gate is dead code in quiet windows (219 frontier publishes, 0
coalesce-gated in the armed draw), and the fire-time state (`fin_hi=976 > front=960`)
shows the gate never made the publishing path safe either way**. Closing the hole
naively (v3: under `stride_gate`, no publish bypasses the coalesce) takes the paired
protocol to **0 fires against shipped 2-3**, but **starves finality (present 43-141 on
5/8 seeds)** — so the disarm channel is a *prerequisite* of the close, not a follow-up:
the checker's gold recipe ("close it, add the disarm channel, then re-measure")
inverts.
(present 3-15× down, all seeds)** — so the disarm channel is a *prerequisite* of the
close, not a follow-up: the checker's gold recipe ("close it, add the disarm channel,
then re-measure") inverts.

**Bottleneck.** allocator-ratchet direction 1 (the engine's one reachable crash, exit
101). Ruin-side, no compute multiple matters until it closes (PRINCIPLES #25).

**The pin** (env-gated replay instrument, `ESE_STRIDE_DBG=1`, print-only, one sequential
s19 gate draw, `work/draws/seq1.err`):
- `PRE id=43 s=896 e=928 D=Some((16, 31, 880))` — an armed pair of exactly the survivor's
  topology (stride [896,928) vs a live truth, start 16 below the published fin_hi) —
  triggers a one-shot state dump.
- The dump's publish events: region 43's dangerous fin_hi=896 was set by
  `SF front id=43 t=896` (the frontier advance, front=896) while truth lineage 31's start
  sat at 880. Whole-draw counts: **`SF front` 219, `SF shared` 0, `SF bisect` 0** — every
  publish takes the ungated path; `alone_at`/`final_through` never decided anything.
- So of da23's three candidates it is the third class (a publish path raising fin_hi
  without an alone_at decision), except the path is the frontier advance, not the merge.
  The gate's measured 7/8→1/10 was never the truth-block working: it was beyond-front
  publishes disappearing (finality pinned to the frontier), which lowered fin_his and
  hence armed margins. The v2 survivor (`FIRE id=52 s0=944 fin_hi=976`, regen t2)
  reproduces on this machine (`s19t1.err`: same state, id shifted 50) — same class.
**v3 (the close) and its measurement.** Under `stride_gate`, skip the frontier advance;
the shared coalesce's candidates already cover every complete tick above fin_hi. Paired
protocol, 8 seeds × both arms, one build — **the contrast landed in the regen window
(`regen-draws/v_s*.err`): shipped arm 2-3 fires (s19: the exact survivor state
`FIRE id=51 s0=944 fin_hi=976 verified=976 front=960 box c=[266,166] s=[2040,2316]`),
v3 arm 0 fires.** The s19 fire's front (960) sits *below* its fin_hi (976) at fire time:
either the frontier published 976 and a later rollback dipped front to 960 (frontier
class — my pin; consistent with 0 gated publishes observed), or the publish went
beyond-front through the gate's coalesce and the truth-block failed on it (da23's
geometry candidates 1-2 reopen for hot windows). The publish-time path was not captured
— no instrumented fire landed; both readings route through a publisher the gate does
not make safe.
- present: v3 collapses to 43-141 on 5/8 seeds (shipped clean 832-1536) and flows at par
  on 3/8 (768-1732): starvation is topology-dependent, not universal;
- v3 draws were identical back-to-back in a quiet window but differ under load (present
  varies with the window: s19 spanned 43-1732) — no determinism claim survives load;
- the equality law holds under v3 (RB lines on gated draws, all m ≤ 0), armed HAZ pairs
  (A > 0) still appear transiently with no FIRE following (P4 held).
- **Not adoptable as a switch flip**: the starvation is structural — the blocking truths
  are recent (start near front), so prune cannot expire them; in a dense field every
  region's grown box touches some live truth at every candidate tick → `decided` is
  empty → nothing publishes. This is the checker's crush case (final lead 0, F=32)
  promoted from load-coupled to seed-dependent-always-on: **the disarm channel is what
  makes the close viable, and it comes first.**

**Predictions** (`predictions.md`, written before the v3 runs): P1 fires — **held with the
full contrast** in the regen window (shipped 3/8, v3 0/8). P2 present — **failed**: 3-15×
down on 5/8 seeds (43-141 vs 832-1536), at par on 3/8. P3 equality — held (all m ≤ 0).
P4 armed-without-fire — held. Kill criterion (a gated fire with the s0 < front ≤ fin_hi
signature) — not triggered.

**What would make it wrong.** The pin rests on an *armed* PRE (the fire's exact
precondition, same topology and margin sign) plus the path counts, not on a dump taken
inside a v2-gate fire itself — that fire never landed under instrumentation (100+
draws; incidence is a wall-clock race). If a future instrumented fire shows its fin_hi
published by `SF shared` instead, the coalesce geometry (da23's candidates 1-2) reopens.
v3's starvation was measured on the battle class only.

**Cost of adopting.** Nothing to adopt as a switch flip: v3 starves. What is adoptable
is the *diagnosis*: any fix must gate the frontier advance (or fold it into the
coalesce) **and** add a channel that lets the blocking danger line advance — candidates:
truth expiry by clash-window causality (bounded by the rollback depth the sync grid
allows), or publish-blocked ⇒ force-merge with the blocker's lineage. Neither is built
here; both are one named experiment away, now with a deterministic reproducer (v3 s19)
to measure against.

**PRINCIPLES.** #19: "if you find yourself fixing things that's oftentimes a signal that
it is the wrong representation" — the gate patched a path that never runs; the
measurement, not more code, found the real publisher. #9: v3's starvation kills that
configuration, not the method. #22: "the simulation tells us what's next" — the armed
dump did.

**Lens (second author).** Ran the checker's cheapest decisive part (the pin) and the
close it enables; the disarm channel and the paired hot-window contrast (fires > 0
shipped vs 0 gated with present within 10%) exceeded the window and stand as the named
next experiment. What the lens may have missed: the crush/starvation axis was measured
only at quiet-to-moderate load; and the pin's transfer from margin-16 to the original
margin-32 fire is by topology, not by identity.
