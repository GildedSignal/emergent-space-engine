Working...
Check complete. Verdict written to `lab/results/20261020-1729-second-20261020-1621-system-7fd3-aa42/check.md`.

**Grade: gold.**

What I did and found:

- **Reproduction, three independent ways.** Runner's regen reprinted every load-bearing ratio inside the disclosed load bands. I applied `work/patch.diff` to the clean tree myself, built, and re-ran: counters identical, ratios in band. Cross-run independence: the bench `digest`/`replay_digest` are **bit-identical to a765's audit and clean JSONs from 16 October** (a different instrument, a different day) on all three seeds, and this run's mints equal a765's stored calls exactly (1467/1737/1349) — the instrument is digest-neutral. `work/census.patch` diffs verbatim against 7fd3's branch patch; the additions are exactly the two `Stage` timers, the print fields, and the bench hookup.
- **The adjudication is mechanically sound.** Both metrics read off one binary's counters as claimed; the outside-from_state arithmetic is conservative where it can bias (bench mints exceed rebinds ~10%, which can only understate the scaffolding). Code references verified (bind.rs retry/post-fit, step.rs τ-reads/retirement).
- **Predictions.** `predictions.md` (17:33) precedes the dossier (17:39) and the regen logs (17:42). The mixed band (0.35–0.55) was pre-declared as a third exit — and it fired — which is the signature of genuine pre-registration. Kills reported at their own bands. One nit: P3's belt stage metric grazed below its band (0.438–0.441 vs [0.45, 0.75]); "held, at the edge" is generous but the numbers are disclosed.
- **Four adversarial arms, three outside every swept axis:** bench seed 2026 (cell reproduces: wall 0.421, stages 0.857, outside 50.9%); bench seed 3 rtf 30 (wall 0.552 — at the fork edge, outside 37.3%: the bands are rtf-100-scoped, not universal); belt 10⁵ coast (holds, outside 41.2%); belt 10⁴ burn (outside 35.2%; compile 15 µs/mint sits between coast 7–8 and bench 53–79, confirming the e-monotone scene story; scaffolding still second-largest everywhere).
- **Page corrections (in place):** "41–57% on every scene" → scoped to tested scenes with my probe readings; belt wall range fixed to 0.254–0.266 (the 3×10⁴ readings were omitted); checker arms added to the domain line.
- **Flagged for the integrator:** d4f1's compile/bind 0.85–0.90 dropped rather than adjudicated; mint-knots' a765 line still needs the denominator qualifier; the patch quietly deletes `machine_after`/`wall_seconds` from the bench JSON (harmless — digests untouched — but not strictly "print-only").

Tree restored clean; my build dir removed. No commits, no pushes.
