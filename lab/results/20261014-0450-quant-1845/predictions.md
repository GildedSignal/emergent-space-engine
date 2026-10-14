# Predictions (written before the decisive runs)

Instrumentation: sub-stage `prof` counters inside the fired Wisdom-Holman kick
(`P_KICK`) — readout+scalars, secondaries+tide, `force::acceleration`,
quantize/burn, `rebind`'s non-fit interior (tau pair, retired clone, entry
clones), `plan_terminal`, the `next_impact` bisection inside it, the word
quantize, and a wall+call census of the whole readout family (`decode`).
Shipped code, battle arm `m4000/s3/rtf1/8s` (ad26's scene), `m1500/s3/rtf1/8s`,
held-out seed 7 at m4000. `ES_MEMBERS` lifts the clamp; prof off = untouched
engine (the digest must equal the published `5c8fe1a8e439221d` at the m4000/s3
arm — reproduction gate).

P1 (reproduction). P_KICK lands at 230–280 µs/call at m4000/s3/rtf1 (ad26's
ship item mean was 248.6 µs), FIT+FIT2 at 100–125 µs (ad26: bind 112 µs ≈ 45%),
and the digest equals `5c8fe1a8e439221d`.

P2 (the shape of the non-bind half). The readout family (`decode` wall, counted
by call) owns the largest share of the non-bind remainder: ≥ 40% of it, with
≥ 15 `decode` calls per fired kick (kick readout 1 + tau pair 2 + searches).
The alternative — that the three `Entry` clones (`retired`, `rec.b`,
`new_entry`/catalogue) own it — is falsified if clones (K_REST minus its two
orbit_states) stay < 15% of the kick.

P3 (the bisection). `next_impact`'s bisection (K_IMP) fires on most fired kicks
of members whose tube dips under the doll surface, each ~log2(half-period in
ticks) ≈ 30–45 `decode` calls, and K_IMP alone is ≥ 25% of the non-bind wall.
If the battle members' periapses sit above the surface, K_IMP calls ≈ 0 and P2's
weight shifts to the tau pair + clones — that outcome kills P3, not P2.

P4 (the cheap terms). force::acceleration + secondaries + tide + quantize +
word together ≤ 10% of the kick (0083 measured forces at 9% of a different
kick class; I expect less here).

P5 (scaling). Per-kick stage costs are flat in members (the kick touches its
own body and a fixed secondary set): m1500 vs m4000 P_KICK within ±20%.

P6 (capacity consequence). If P2+P3 hold, deleting the per-kick impact
bisection (carry the retired tube's impact tick as a warm start, or bisect only
when the new tube's periapsis crosses the surface) removes ≥ 25% of the fired
kick's wall — a named deletion for the queue, priced by this run's numbers.
