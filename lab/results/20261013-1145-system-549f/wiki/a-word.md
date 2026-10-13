topic: a-word
status: open
closed-by:
valid-while:
updated: 20261013-1145-system-549f

# The acceleration word: one slot per binding, three bottlenecks

## Current best

**The three per-consumer second-order re-derivations are one missing word, and its
price is measured: free to write, 4–5 orders stale-safe at read windows on plain
scenes, still sub-quantum on the dive, ~10⁻³-stale across light windows
(20261013-1145-system-549f).** The view's per-read `force::field` in `observe::partial`
(81% of readout, 51bf), the news version payload's missing total acceleration
(7ab4, gravity-news), and the burn waterfall's generator piece (174d, frame-cost)
re-derive or absorb the same term; every kick already computes it and discards it
(`step.rs:669–671`). Census on shipped code (plane seed 1, 48 members, rtf 100, 8 s
per flight, `partial`'s own window gate, doll units, c = 1): stale-word error
|a(mid)−a(B)|·τ²/2 median 2.8×10⁻¹⁰, max 3.0×10⁻⁹ against the shipped term's max
2.0×10⁻⁴ (the stale error is Δa/a × the term by construction; Δa/a ≤ 3.1×10⁻⁴ max,
3.5×10⁻⁵ median) on coast and held L8; on the held
reverse-L15 dive (player handed to the root doll, r 9.3×10⁷, β 0.254) Δa/a p99
1.7×10⁻², err max 1.0×10⁻⁸ — the windows shorten faster than the field grows, so the
word holds; across a **light window** the word goes 10⁻³-stale on plain scenes and
4.0×10⁻¹ stale at the dive's handoff, **depth-growing, not capped** (checker: 8.0×10⁻¹
at β 0.49 on the same dive held to 16 s) — the news payload's word must refresh at
rebinds, not ride a light window. Structural: the shipped code already has the
stored-word path — `credit`'s ramp applies the stored `kick.dv` (the burning player
rides it; no field eval) — so the unification is one read rule for both paths, and
`partial`'s per-read field eval + `ctx.secondaries` doll-chain walk (the ~10-line
`step()` closure; the gates and base resolution stay for the word read — checker)
deletes while *keeping* the term's accuracy where it will be visible (strong-field
dolls — 7b86's pure deletion only works where the term is invisible). The write rides
the kick: zero extra field evaluations.

## Refuted

- "The dive breaks the word at readout windows" (this run's own prediction): Δa/a
  max 3.0×10⁻² there, 0% of reads over 1; the break appears one window longer out
  (the light window), not at reads (20261013-1145-system-549f).
- "The plane's light-window staleness is negligible (≤ 10⁻⁶)" (this run's P3):
  measured median 6.3×10⁻⁴, max 1.9×10⁻³ coast, 4.0×10⁻¹ at the dive's handoff
  (20261013-1145-system-549f).

## Open directions

1. **Wire the word on the readout** (the cheapest): store `f.accel` per binding at the
   kick, read `Δx = a·τ²/2` in `partial`; digest-identity expected everywhere the
   term is invisible, error ≤ 1.0×10⁻⁸ doll units bounded on the dive — the deletion
   7b86 priced, without its strong-field caveat.
2. **The word on the news payload, with thrust** (7ab4's r-news): total acceleration
   = field (this census) + the heading's analytic thrust; refresh at rebinds (the
   light-window staleness 0.4 at the handoff says a ridden word is not enough).
3. **The quantized width at 10⁹** (memory-h-live): the word must pack like `kick.dv`
   already does; the census prices the refresh rate (per kick), not the width.

## Contradictions

None open. 7b86's "the slot buys the view nothing in this regime" and this census
agree: the win is not accuracy on plain scenes (the term is invisible there) but
keeping the term for free where it becomes visible, and deleting the 81% cost
everywhere.

## Runs
- 20261013-1145-system-549f (pending grade): the three second-order consumers priced as one word — write free (step.rs:669), err/term ≤ 1.5×10⁻⁵ plain, sub-quantum on the dive, 10⁻³-stale across light windows.
