# Lens: Flight past γ ≈ 2,000 (crates/universe thrust and rebinding) (a directed build)

Flying at the top throttle (11,561 g), kicks start refusing past γ ≈ 2,000 and the ship is eventually lost (HANDOFF, "Julien can feel the flight"). Find where the range breaks (rapidity, the rebinding's numbers, the compiler's unbound tubes) and extend it so a ship can reach γ of 10⁶ under thrust and coast there, exactly. Tests: a burn to γ = 10⁶ and back gives the identical state under replay; the burn's work test holds at every throttle level. Gates: B13 (`--law plane`), G1–G6, B16.

**How to build.** Work in this tree against `main`; your edits become `work/patch.diff`, which a reviewer applies later (you never commit, push or merge). Read docs/law.md, docs/HANDOFF.md ("In flight", "Astra's queue") and the references named above before writing code. Ship tests (each under 60 s) and run the named gates before and after; report every gate's detail line both ways. A gate is frozen: never edit a gate, a threshold or frozen evidence; if a gate seems wrong, say why and leave it. Keep every process under 2 GB. If the change cannot pass its gates, a clean measured failure with its diagnosis is a result: say so rather than patch around it.

Gold: the patch applies to main, its tests pass, and the named gates improve or hold, measured, with nothing else regressing.

Also (6 October): since the motion law v2, a thrusting root-doll ship is lost already at β ≈ 0.05–0.125 (the energy register's i64 word and the kick's range); fix that first (see `b-energy-register` and branch `wt/loss-fix`), then the γ ≈ 2,000 limit.
Fixed on main at 741d05e (6 October): `p_t` is an i128 and a held burn caps the first step after a handoff; an L15 burn reaches β 0.999 (test `a_ship_burning_at_the_top_level_reaches_beta_0_999_without_a_refusal`). Build from there; the open part is the GR register (the drift is GR, the register Kepler's) and γ beyond 2,000.
