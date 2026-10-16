# Predictions (written before the decisive run)

Attack: representation.md §3 ("A cycle's derivatives are stored with it, so a kick updates
the cycle by a multiply-add") and §6 ("Tidal kicks … ~50 ns each, incremental") against the
shipped resolver, regenerated on this machine with `xtask universe --kick-bench`.

Held-out expectations (this machine is a shared Linux/x86 box, not the M1; orders of
magnitude only, per the lab README):

1. **The per-kick cost is 10⁵–10⁶× the doc's ~50 ns**: I predict `kick_us` p50 in the
   20–300 µs range (the record says 43–52.8 µs resolver-adjacent on the M1, c01c/0c44, and
   the board says 75–160 µs for the kick today). I predict NOT ONE sample under 1 µs.
2. **Zero reuse**: `kick_us` ≈ `kick_us_all` ≈ `kick_us_leavers` to within noise (the
   record: "one full cycle rebind per distinct kick, zero reuse"). If a memo were hitting,
   `kick_us` would show a fast tail that `kick_us_all` dilutes; I predict no such tail.
3. **No multiply-add path exists in the shipped code**: grep for the stored-cycle
   derivative update (the jet) returns only retired remnants, none on the kick path.

If (1) or (2) fails in the doc's favour — samples under 1 µs or a memo tail — the doc's
premise stands and this attack dies (that would be a result too).

Secondary falsifier (already on the record, checked not re-measured): the §6 row
"Undisturbed orbits ≈ 0" — the census (3294) says every belt body fires a kick every doll
interval at rate 1.000; the row survives only because the *rate* per body is tiny, not
because undisturbed bodies cost ~0. Predicted reading: "≈ 0 until looked at" is true only
in the between-kick windows, and the doc's own next row prices the kicks wrong.
