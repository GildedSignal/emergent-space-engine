Working...
Check complete. `check.md` written; tree restored to pristine (only untracked `lab/results/` remains); nothing else in the run folder touched; no git commit/push.

**Grade: lead** — the run's headline survives partially, but its one kept change fails its own pre-registered kill criterion.

What I did and found, in order:

1. **Reproduced the timing claims.** Pristine seed 1/rtf 10: leaver median 120.3 µs, made 36.5, digest `adc434a4…` (all match). Profile build: rebind 87.2%, bind 80.9%, `OrbitShape::bound` 61%, `Passage::compile` 339 µs/call × 60 = 31%, quad panels exactly 105,948/11,861 — the attribution is real.
2. **Refuted the bit-identity claim.** Applied `work/patch.diff`, rebuilt: rtf-10 and rtf-1 digests match pristine, but **seed 7/rtf 100 flips** (`29a40cdc…` → `5a4c42cd…`) and my own adversarial **seed 5/rtf 100 flips** too (`fed002a9…` → `9a1c039a…`); pristine seed 7 is stable across loads, so the bench is deterministic and the flip is the patch. Mechanism: the patch shadows `exact` with tube-unit positions in `bind_in`, so the residual subtracts doll-unit decoded positions from tube-unit positions whenever `Unit.unity` is false (secondary dolls with mantissa ≠ 1 — bound only at the player's flight speed). The dossier's "P1 held exactly, all three held-out digests identical to the pristine tree (`03dcd421…`, `5a4c42cd…`, `35f786a5…`)" cites the *patched* seed-7 digest as the pristine one — a headline the reproduction contradicts, and the author's own predictions.md declares any digest change a KILL of the change.
3. **Novelty.** Memo-0%-on-distinct-kicks is the taste log's 5 October correction re-derived (the bench ships that instrumentation); the "compile count, not constant factor" conclusion is the already-adopted components-4643 gold. New content is the stage split and the `profile` instrument — worth a line on the board, not a bottleneck move.
4. **P3 verified**: test suites green on the patched tree — which is precisely how the scale-mixing bug rode through.

Salvage noted in check.md: the attribution stands; the `profile` feature is adoptable after a one-line fix (`let tube_state = …` instead of shadowing `exact`) plus a pristine-vs-patched digest check at rtf 100; the `node()` change as shipped must not be merged.
