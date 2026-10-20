# Predictions (written before any arm ran)

The question: `history-demand`'s open direction 1 — is retention at **one** light leg
(`ES_KEEP_LEGS=1`, margin 2²⁶ ticks ≈ 330 game-s untouched) enough for the view at the game's
cadence, and what does it delete? Basis: c7a6's census (demand = one leg, p50 4.6–4.9k game-s,
max ≤ 7.3k, against keep_med 8.3–12.9k; no read *returns* a binding past one leg + cadence
slack), and the shipped search's failure mode read in code: one `binding_at` → `None` inside
`crossing` drops the emitter from that gather entirely (`view.rs` `else { continue }`).

Scene: the shipped ladder scene (`plane_extra` seed 1 Sparse 1 48, N = 30,000), `nladder`'s loop,
12 ms engine budget, rtf 2000; one `gather_cached` every `every` frames. Held-out cases = the
ones I have not tuned on: the sparse cadence, the burn (ld grows), and the engine's own share of
the census.

- **P1 (game cadence, coast, every frame):** the one-leg arm loses **zero** emitters —
  `losses = 0`, final `seen` equal to the stock arm's at the same tick, engine **digest equal**,
  and the **view hash equal** (no row shifted, none missing). The census shows gather nones = 0.
- **P2 (the delete):** retained segments/body drop **≥ 20%** vs stock (the second leg is pure
  supply), retained-depth p50 drops toward ~half; RSS drops by at least the segments' share.
- **P3 (cost):** warm gather ms and readouts/gather within **±20%** of stock (the search reads
  the same bindings; the None path is never taken) — the deletion is free at the game's cadence.
- **P4 (adversarial, sparse gathers every 60 frames ≈ 2,000 game-s apart):** the one-leg arm
  **loses emitters** (losses ≥ 1; the stale warm guess probes ~the cadence gap below the
  crossing, past the 330 game-s margin), the stock arm loses none. This is the kill-side control:
  the instrument must be able to fail. If instead the one-leg arm also holds at every=60, the
  margin question is reopened downward (the keep could sit below one leg).
- **P5 (burn, the ratchet scene):** zero losses at game cadence (ld grows smoothly, one frame of
  staleness is tiny), and the memory slope halves where ld dominates: segments/body and RSS
  measurably below the stock burn arm at the same tick.

Failure handling: P1 failing (a lost emitter at every=1) kills the one-leg keep **as a bare
dial** and confirms the margin is load-bearing at cadence; P4 passing is expected and prices the
cadence dependence; P3 failing (gather cost up) means the shorter history widens the Newton
bracket search (more readouts), a real adoption cost to report.
