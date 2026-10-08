# H_live: Fermi estimate before any code (the lens's rule)

**Question (one sentence).** How many bits of live distinguishing information per body per game-second does the plane's belt create, and does the steady state fit 10⁹ bodies in 8 GB?

## Budget decomposition (M1, 8 GB unified)

- Usable for the universe after OS/GPU/view: ~5.5 GB ≈ 4.6×10¹⁰ bits.
- At 10⁹ bodies: **~46 bits/body ceiling** for everything (tubes, scars, programs, log).
- Naive tube storage: 16 B/body (law.md §State) = 128 bits → 16 GB. **Over budget 2–3×.**
- Birth program (components-98bc, gold): 0.126 bits/body → 16 MB at 10⁹. **4 orders of magnitude under.**
- The whole memory question lives in the gap between 0.126 and 128 bits: **scars** — bodies whose exact tube deviates from what their program regenerates, at the law's quantum (~10⁻⁶ relative ⇒ ~20 bits/dimension).

## What creates distinguishing information in a belt (star + Jupiter-like + belt)

| Channel | Bits/body/orbit (estimate) | Reabsorbed? |
|---|---|---|
| Mean-anomaly shear (phase mixing) | 0 — decohered phase ≡ uniform ≡ the program's own draw | instantly |
| Secular precession / forced e (Laplace–Lagrange) | 0 per body — a deterministic, low-dim drift; the program carries it (family + forced vector) | by program drift |
| Secular diffusion of the ensemble (e widens, gaps carve) | ~0 — smooth in a; the refit family absorbs it (a histogram's K·32 bits amortizes to 0 at 10⁹) | by periodic refit |
| Resonant/chaotic a-diffusion (Kirkwood zone) | up to 128 bits once decorrelated (secular conserves a, so Δa ≠ 0 is the chaos marker) | only by **shuffle** (exchangeability) or death |
| Mutual encounters (massive belts only) | ~log₂(spread/quantum) per correlated pair | pair shear decorrelates; orders spread below floor |
| Player singling-out | bits actually received ≈ screen ≈ ≤10⁸ bits/session = 12 MB total | never — but bounded by the view, not by N |

**Key structural fact (Fermi, no code needed):** for massless test particles the map ordinal→tube is *fully exchangeable* — physics never reads labels — so any "shuffle" (re-program + deterministic PRNG, a law event) is trivially observation-safe. The memory question therefore reduces to:

1. **f_chaos**: fraction of belt bodies whose Δa leaves the quantum (scars if no shuffle).
2. **Is the shuffle observationally legal for the ensemble** (does a synthetic re-programmed belt evolve statistically like the true one)? — needs mass in the loop or structure beyond one-point marginals; testable by evolution-matching, not by label permutation.
3. Player singles and news log: bounded by the view and by c-decay; separate small terms.

## Steady-state verdict formula

- No re-programming at all: ~128 bits × 10⁹ = 16 GB → **fails**.
- Refit program, keep identity (each body keeps its exact tube): f_chaos × 128 bits + ~0 ⇒ at f_chaos = 0.05–0.15 → **0.8–2.4 GB → fits**.
- Refit + legal shuffle of unobserved bodies: ≈ programs + singles + log ≈ **tens of MB → fits with ~100× headroom.**

So the measured deliverables that matter: f_chaos(t) for a plane-like belt (Jupiter at 5.2 AU, belt 2.2–3.4 AU), whether a static birth program scars everyone (motivating drift-programs), and whether a synthetic re-program preserves the belt's observable future (the shuffle's legality, tested by evolving both).

## Events per game-second (secondary, compute side)

At rtf 100 (the plane's flight setting), 1 game-hour = 36 s wall; a 3-year orbit takes ~10⁶ game-seconds. Kick cadence per orbit ~32 (H0190) → ~3×10⁻⁵ kicks/body/game-second ⇒ at 10⁹, ~3×10⁴ kick-evals/s — ~10 orders below the 10¹⁰ ops/s machine. Memory, not events, is the binding term. (Orders of magnitude only; integrator re-measures on M1.)
