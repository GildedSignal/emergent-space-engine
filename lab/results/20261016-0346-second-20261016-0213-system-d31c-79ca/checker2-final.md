Working...
Check complete. `check2.md` written to the run folder; the tree is restored (patch reversed, only `lab/results/` untracked); `check.md` untouched.

**Grade: gold.**

Verification record:

- **Reproduced from `work/patch.diff` in a clean tree** (applies clean on `c8cd60bd`, builds 10.9 s). My flights: 10⁴ s1 off 32.46 / on 22.36 / state 15.77 / full 10.81 — on/full 2.07×, shipped→full 3.00×, digests pair across all arms and equal d31c's own branch records (`df20c524`, `be96cd53`, `d166a8da` verified against `origin/claude/lab-20261016-0213-system-d31c`). Runner's regen matches all seven dossier cells; the flagged artifact cell reproduces quiet.
- **Adversarial, mine:** (1) 3×10⁵ s1, beyond the author's 10⁵ domain — flat at 10.80 µs/body full, on/full 2.10×, digests pair, RSS 719 MB; (2) seed 42, never flown by this author — all arms bit-identical; (3) 12,000-s cut (19,272 kicks) — all four arms bit-identical; (4) the two suite configs regen.sh skips (planets-only, constants-only) — 77/0 each, making all five knob configurations independently green.
- **Predictions:** written 93 s before the decisive grid; P1/P3/P4/P5 held, P2's substance (named lever misses 1.5×) held everywhere — that pre-registered negative is the premise correction, and the family arm crosses checker 2's frozen bar (≥1.5× further, digest-identical) at 2.07–2.15×, confirmed by me beyond the domain.
- **Novelty:** `ES_STATE_ONCE`/`ES_CONSTANTS_ONCE` nowhere prior; the counters also correct d31c's "two readouts" to three reads per clock body; d31c's Err-dropping latent catch is closed in code (`.ok()?` refusal to arm).
- **Page:** two additions only, every number matches the evidence — no overstatement, no correction needed; inherited conflict correctly left for `wiki.py apply`.

Nits recorded in "what the author missed": P2's µs-band letter breached on one cell by 1.2% (+1.39 vs 1.4 floor) yet reported flat "HELD"; 10⁶ unflown (and unflyable on this box under the 2 GB cap — M1 re-measure must carry it); the refusal-to-arm fix has no synthetic regression probe; "integer Kepler decode" is representation inference, not a separate timer.
