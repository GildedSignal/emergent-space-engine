# Predictions — 20261020-0036-second-20261019-2339-inversion-1d47-4063

Written before the decisive arms (the 10⁵/2×10⁵ canonical-cut runs and the burst flights).
Scene: `cut_digest` — the nladder burn (forward L8, decision at its canonical tick 200,000), rtf 1000,
cut 17,000 game-s (past the first kick wave), `frame_to(limit = cut)` + `settle(cut)`, digest/kicks/
encounters/contacts. Arms by env: none = shipped (OFF), `ES_ROOT_SHIPS_TO_QUEUE` (ON, 1d47's gate),
`ES_ROOT_SHIPS_REACH=16` (REACH: resolve before the scan only ships within 16 ticks ≈ 24,000 km of
light distance — two orders past any conjunction window, four orders inside the belt's scale — leave
the far wave to the queue). Probe `ES_FIX_PROBE` counts stale candidates and, new this run, answered
encounters that came from a stale candidate, with how far past the encounter window the read sat
(|d| / 2¹⁰·reach) and the staleness age.

Smoke (N=3000, before these predictions were finalized): OFF 12 ms flight ≡ OFF no-flight settle,
digest 436fff40…, kicks 30671 — the contract holds on shipped code where nothing defers.

- **P1 (the control).** OFF at 10⁵ and 2×10⁵: one digest across unl / 12 ms / 3 ms / no-flight, and
  across reruns of 12 ms. If OFF itself moves, the shipped schedule-invariance is already broken at
  these rungs and every comparison below is against the no-flight digest instead.
- **P2 (the reproduction).** ON at 12 ms, ≥3 reruns per rung: not stable — at least one rerun leaves
  the OFF digest (the checker's bistability), and the probe shows stale > 0. If ON is stable but ≠
  OFF, the gate is a law change outright.
- **P3 (the mechanism).** The probe's `stale_enc` (answered encounters from stale candidates) is > 0
  in ON exactly when its digest leaves OFF's; the offenders sit at |d|/window ≥ 1 (the window is
  2¹⁰·reach). If stale_enc = 0 while digests still move, the stale-read story is incomplete and the
  reach form is not implied — reported as such, whatever REACH does.
- **P4 (the decisive arm).** REACH=16 at both rungs, 12 ms ×3 + unl + 3 ms: (a) the burst stays
  deleted — `nladder` burn max_ms ≤ 60, p99 ≈ budget, refusals/dead 0; (b) every digest equals OFF's
  P1 digest, with stale_enc = 0. If (b) fails while (a) holds, the reach form is refuted at the rungs
  that matter: the burst deletion is real but the gate is a law change, and adoption owes a re-freeze.
- **P5 (the price).** REACH's flight lags like ON's (~+1.5 s presented-time lag at the wave): the
  wave drains at the budget either way.

Kill criteria: P4(b) is the rung's verdict. P1 failing kills the comparison frame (and is a finding
about shipped code, not about the gate).
