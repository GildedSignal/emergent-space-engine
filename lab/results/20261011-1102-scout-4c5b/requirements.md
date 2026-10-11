# Inspiral (radiation reaction) — requirements as numbers

The bottleneck: HANDOFF "Headed next" #4, third item — "inspiral (Peters' generator)". Julien:
"i like both" (law.md §rotating holes). law.md line 35 adopts the mechanism on paper ("Inspiral
is not a jet: Peters' a(t) is its generator") with zero numbers behind it; b-news-gravity-e300:
"radiation reaction (2.5PN, Peters' generator on the tube) — named, neither claimed". redteam-df81
killed inspiral-as-kicks (|Δa/a| = 1.1e-2/orbit at a = 20M, ν = 0.25) and left the generator unbuilt.

What the engine needs, as numbers (each tied to a doc):

| Requirement | Number | Source |
|---|---|---|
| mass-ratio domain | ν ≤ 0.25, p 20–1000M | B11's frozen domain |
| behaviour bar (merger time, chirp shape) | 1% | B1's style (behaviour, not trajectory) |
| period bar for a watched binary | 0.1% | B2 |
| events per orbit, unperturbed body | 0 | B9 ("zero work per orbit until an event") |
| inspiral must not cost this: the readout is the tube | 0 work/orbit between re-keys | law.md §State (tube, memo) |
| one calendar event per re-key, slack = quantum/drift-rate | min-plus queue | law.md §Causality |
| error type | bounded, resets at each re-key — never compounding | PRINCIPLES 13; df81's C·drift² |
| integers decide / floats explore | floats here | lab README |
| tests | ≤ 60 s, < 2 GB | lab README |
| every player-visible effect at c | the chirp is news on the light cone | PRINCIPLES 23 |

The representation under test (already the law's own words): the binary is one doll with M = m₁+m₂
(B11); its relative orbit is the exact Schwarzschild tube compiled from (E, L); radiation reaction
is a slow drift of (E, L) under orbit-averaged flux balance; the tube is recompiled only when the
memo key is crossed (a calendar event); plunging ends as the plunge tube (a1a4's compile) at the
separable boundary in (E, L).

Three questions decide adoption:
1. **Accuracy**: is the Newtonian-quadrupole flux (Peters) evaluated on the *exact* orbit good to
   the 1% behaviour bar inside B11's domain (p ≥ 20M)? The known 1PN flux correction says no at
   small a — where exactly does the 1% bar break?
2. **Cost**: the re-key rate = |d ln P / dt| / ε_bar (a telescoping sum: total re-keys =
   ln(P_start/P_end)/ε_bar). Where does it reach 1 per orbit (the "wall")? What is left between
   the wall and the plunge?
3. **The handoff surface**: is it the exact Schwarzschild separatrix (the boundary where the
   cubic R(u) = 2L²(u−u_a)(u−u_p)(u−u_3) loses its bound root pair — the same boundary where
   a1a4's plunge-tube compiler takes over), and where does it sit in (a, e) for eccentric births?
