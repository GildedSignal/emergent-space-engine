Working...
Check complete. Summary of what was done and found:

**Grade: silver** (`check.md` written, first line exact).

**Reproduction — exact.** Applied `work/patch.diff` to the clean tree, rebuilt, reran both arms: every deterministic field matches the stored JSONs bit for bit (digests `b42da477…`/`8c242b02…`+replay `0de3a82c…`, refused 0, mints 23/137, kinds, knot ranges, 1.71 MB heap, shares 0.853/0.911). Only wall-µs stats wobble, inside the disclosed ±10%. The panel rule (CAP = π/4, ψ-band doubling, orbit.rs:450–481) is as described.

**Adversarial cases — all pass, one outside the author's domain.** Seeds 2/3/7 (author ran only seed 1; `--members` clamps at 400): P1 99–100%, ρ 0.65–0.94, knots 19–244, share 0.85–0.91, monotone terciles, no-mint 16.6 µs vs minted 214–365 µs. A temporary per-row probe (reverted) showed the coupling is *not* a class artifact — within-cycles ρ = 0.96 over knots 6→448 — and found the 448-knot tail is a **Cycle**, not a passage, contradicting the page's guess.

**Why not gold.** The unification's halves are already on the record: a765 (compile 84–87% of the rebind — the dossier's "b063" citation is a mix-up; b063 owns the ns write floor), ec9d (leaver tail = Passage::compile, ~365 µs, same number re-measured), 5465 (knots 58% of a doll body), c304 (~10 kB/ship-kick), and library-directions already prices one adoption (Carlson) deleting compile wall + knot table together. The lazy lever is half-killed by 4ea0's uncited birth-read census and half-flown at nladder (b9ae, 0757-gold). New here: the per-kick ρ coupling and class census — real, but a new axis on a known object.

**Page corrected in place** (marked `[checker]`): the Refuted entry now cites the standing shares; open direction 1 scoped to span coverage; open direction 2's "e→1 passages?" corrected to cycle-class; open direction 3 cites f623/8994's existing allocation anatomy. Tree left clean (patch reversed, only `lab/results/` untracked, as the runner left it).
