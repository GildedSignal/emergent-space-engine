Working...
Check complete: **Grade: gold**, written to `lab/results/20261018-1717-fermi-dcf1/check.md`. Tree restored (patch reverted, scratch removed); the author's wiki page needed no correction.

**What I did:**
- **Reproduced** — applied `work/patch.diff` myself, rebuilt, flew the 3×10⁵ burn anchor: digit-identical stream (kicks 1495, events 5527, boundaries 1398), HWM 705→718, held 13. The runner's fresh regen logs match every row of the dossier's table (held varies 13↔17, 187↔223 — stochastic, same orders).
- **Path-independent core verified** — max frame-to-frame VmHWM jump is 1 MB in all 18 logs; one old-law mint at 3×10⁵ would show ≥67 MB. The byte-term death cannot be an artifact of the mint rate.
- **Three adversarial arms, all outside the author's grid:** 6×10⁵ burn (slope 0.026 MB/game-s vs the law's 94; stream byte-identical there too; gather 5.09 µs/seen-body, linear), 4,398 game-s burn (slope 0.006, held 213, zero over 12 ms), and a 1 ms budget corner (held 334, HWM +5 MB). No arm resurfaces the wall.
- **Novelty** — the killed inference stood on today's page (taleb-2403, [INFERENCE], its second checker flagging the unflown decade); e28f flew the branch cure but nothing had measured shipped main. I also confirmed the author's [INFERENCE] mechanism in code: `encounter.rs`'s `Arc<Scan>` reuse, merged in the `frame:` commits — now dated for the integrator.
- **Predictions** — pre-registered kill criterion fired; the author's own coast lean was wrong and reported as held.

Gold because: reproduced, the falsification is ~10³×, it answers the board's "which term breaks first" with a measured re-ranking, and adoption is a zero-cost deletion. Caveats recorded: 10⁶ unflown (cap), load/paced axis open for held elasticity (irrelevant to the byte term), mint rate untouched.
