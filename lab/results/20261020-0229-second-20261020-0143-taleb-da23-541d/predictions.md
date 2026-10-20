# Predictions — pinning the s19 survivor (written before the decisive fix runs)

## The pin (already observed, armed-PRE dump `work/draws/seq1.err`)

`SDBG armed id=43 m=16 tid=31 s0=880 front=896`: region 43's stride [896,928) is armed
against truth lineage 31 (start 880) because 43's own fin_hi=896 was published by
`SF front` (the unconditional frontier advance) while the truth's start sat 16 below it.
In the whole draw: **219 `SF front` publishes, 0 `SF shared`, 0 `SF bisect`** — every
publish goes through the frontier path; the stride gate (all three parts, `alone_at`/
`final_through`) is dead code on the battle class. The s19 survivor
(`FIRE id=52 s0=944 fin_hi=976`) is the same topology: fin_hi published by the frontier
advance at front ≥ 976 while truth start 944 < front was live nearby.

So of the author's three candidates it is the third class — a publish path that raises
fin_hi without an alone_at decision — except the path is not the merge but the frontier
advance in `finalize`'s first loop.

## The fix under test (stride_gate v3)

Under `stride_gate`, skip the unconditional frontier advance; every tick > fin_hi
(including ticks ≤ front) is decided by `finalize_shared`'s coalesce, whose truth
pseudo-members (part 3) then guard the frontier publishes too.

## Predictions for the paired protocol (8 seeds, both arms, one window)

- P1 (fires): the gate arm's s19-class fires disappear — 0 FIRE lines on the gated arm
  across the paired seeds (the frontier hole was the surviving publisher; merges cannot
  raise fin_hi above what some set_final published, and now every set_final is gated).
- P2 (present): gate arm present within ~15% of shipped on the same seed when the window
  is not crushed; under 8-way crush the gate arm may pin finality (lead ~0) — that is the
  disarm-channel gap, reported, not fixed here.
- P3 (equality law): every RB line on clean gated draws stays m ≤ 0.
- P4 (hazard): on gated draws, `A` lines may still arm (D>0 at PRE) transiently, but no
  FIRE follows, because the armed fin_his are now capped by the coalesce.

Kill criterion: if a gated-arm draw still fires with the same s0 < front ≤ fin_hi
signature, the frontier fix is wrong or incomplete — KILL v3 and report.
