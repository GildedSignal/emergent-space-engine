# Predictions (written before the decisive census run)

The run: engine-side key census for formation families (formation-family od 2). Families of
F = 16 members on one circular orbit (same r, same e = 0), members at phase offsets δx along
the orbit, restricted problem (star + one planet of 1/1000 at 1 AU, families co-orbital at
1 AU, base phases far from the planet). Shipped engine, shipped 61-bit word, no patch to the
law. Read every member's `next_time` (the calendar's own key stream) each census slice; a
family shares one intern calendar key while all members' due streams are equal.

Held-out cases (not tuned on): the δx ladder itself {10², 10³, 10⁴, 10⁵, 10⁶} root units and
the clone control (all 16 members at identical spec).

## Predictions

1. **Clone control (δx = 0):** due streams bit-identical forever (determinism of the engine on
   identical bodies). If not, the census instrument is broken — VOID, not a result.
2. **The word split does not reach the calendar at kick 0.** a877 measured the 61-bit state
   word splitting at every kick; I predict the DUE stream (anchor + step H, H a power of two,
   anchor common at birth) stays shared far longer: the first due fork comes only when the
   members' accumulated differential moves H by a factor of two or the anchor. So
   g_fork(δx) ≫ 1 at the shipped word, at least for δx ≤ 10⁴.
3. **g_fork shrinks with δx**, roughly inversely (the differential tide h·H·δx accumulates
   ∝ δx): each decade of δx costs about a decade of shared fires. Belt-scale δx = 10⁶ forks
   within the run; δx ≤ 10³ does not fork inside a bounded run (≤ 400 fires/member).
4. **Calendar compression while shared:** while the family's dues are equal, the family's 16
   `ship_ticks` slots hold one distinct key — the intern-key memory is 1/F per member for the
   certificate's lifetime g_fork.
5. **The certificate is re-earned, not monotone:** after a fork the members' steps re-quantize
   to the same power of two often, so due streams RE-JOIN (spread returns to 0) — the
   shareable set is time-varying; the census fraction (not just first fork) is the number to
   report.

What would make the sharing claim dead: dues forking at fire 1 for every δx > 0 (then the
intern key needs a877's w11 law change even for the calendar, and od 2's answer is "no, not at
the shipped word").
