# H_live is bounded — at ≈ 61 bits per scarred body, 1.8× the universe budget

## Claim

A belt's live distinctions saturate at **≈ 61 bits per body** (≈ the entropy of one kick's
residuals: Σ log₂(δ/quanta) ≈ 50 bits, + ~10 index/framing), reached as the *scarred
fraction* → 1, not as residual width grows; re-kicks are ~free (overwrite + block-width
quantisation), re-sorting into a new family recovers only ~3 bits, so **10⁹ kicked belt
bodies cost 7.6 GB — 1.8× the 4 GiB universe budget — and the flow (seal+compact ≈ 4 µs
per kick, ~10 kicks/s at 10⁹) is irrelevant: the stock, not the flow, is the verdict.**

## Bottleneck

Board risk #2: "Distinctions created per game-second (H_live): they, not the body count,
decide whether 10⁹ fit in 8 GB; not measured yet" (HANDOFF, 6 Oct; `b-h-live` still queued).
Expected gain: closes the question with a measured law instead of a guess; deletes nothing
yet, but redirects `b-h-live`/`b-belt-wire` from "measure H_live" to "choose the residual
quantum" (the only lever: bits/scar ≈ Σ_col log₂(δ_col/q_col) + 10).

## Evidence

Instrument: the shipped `shipmem` (form P = program + Elias–Fano scars; form B = packed
blocks with repack), driven by its own `Pop::Convoy.kick` magnitudes (δ_t = ±2¹⁶ on t_p,
δ = ±2¹⁰ on E, L, ω; 4 of 5 columns). New example `crates/shipmem/examples/hlive.rs`
(~90 lines; saved in this run's patch): iterated rounds, each kicking a fresh f·m of
m = 131,072 members, seal + compact every round, bit-exact round trips.

Commands (each ≤ 60 s incl. build; Linux/x86 shared — orders of magnitude only):

```
cargo build --release --example hlive -p emergent-shipmem
target…/hlive 131072 0.125 24 7  main.jsonl     # 1.6 s wall
target…/hlive 131072 0.0625 40 99 heldout.jsonl # held-out seed/path
target…/hlive 131072 0 8 7  f0.jsonl            # positive control
target…/hlive random 131072 random.jsonl        # negative control
```

Trajectory (main.jsonl, full table there):

| k̄ (mean kicks/body) | scar frac | chosen bits/body | bits per *scarred* body |
|---|---|---|---|
| 0.125 | 0.117 | 7.07 | 60.3 |
| 1.0 | 0.632 | 37.99 | 60.1 |
| 3.0 | 0.949 | 58.66 | 61.8 |

- **chosen ≈ 61 × scar_frac.** Growth is the fraction, not the width: per-scarred-body cost
  is 60.3 → 61.8 while k̄ grows 24× (residual widening is absorbed by block-width
  quantisation; ≈ +0.3 bits per doubling of k̄, not my predicted 2).
- **Re-family fails:** re-sorted by t 55.0, by E 56.2 bits/body (vs 58.7 scars) — the
  diffused population's floor is its residual entropy in any order.
- **Form B never crosses P** (B = P + 1.92 flat): delta-vs-program beats full-value blocks
  at every scar fraction here.
- `infer` (launch program) dies at cumulative kicked fraction 0.31 (round 3), as majority
  requires >50% untouched pairs.
- Controls: f = 0 flat at 0.03 bits/body; `random` rung 211.8 bits/body (incompressible
  ceiling). Held-out seed 99, f = 1/16, 40 rounds: 56.13 at k̄ = 2.5 vs 56.09 main — the
  law depends on k̄, not on the path.
- Costs: update ≈ 0.14 µs, seal ≈ 2 µs, compact ≈ 2 µs per kick (loaded shared x86).
- Round trips: form P bit-exact over **all** 131,072 ordinals at rounds 8/16/24
  (`bad_p = 0`); shelf decode bit-exact on every decoded row (`bad_b = 0`); my probe's
  "mismatches" counter was a group-reorganisation artifact (65,536 of 131,072 decoded —
  not data loss).

Game-time conversion (repo numbers): kick cadence 0.3/orbit (H0190) ⇒ k̄ = 3 after 10
orbits ≈ 10 game-years at 1 AU (≈ 5 weeks of play at rtf 100). So H_live hits its
asymptote fast; **capacity at the asymptote: 4 GiB / 61 bits ≈ 5.6×10⁸ scarred bodies**;
10⁹ need 7.6 GB. Distinction *flow* at 10⁹: λN ≈ 10 kicks/s × 4 µs ≈ 40 µs/s of idle-time
work — noise for the allocator.

## Predictions

`predictions.md`, written before the run. Held: P1 (both controls), P4 (58.66 in the
predicted 20–60 band, still walking), P5 (infer dies at 0.31 vs predicted ≈ 0.3–0.4).
Partially held: P2 (walk yes, but slope is fraction-driven: +0.3 not +2 bits per doubling;
per-scar base ~60 not decomposed as I predicted), P6 (overwrite confirmed — per-scar cost
flat while k̄ triples — but marginal per unit k̄ stays ~6 bits while the fraction grows).
**Failed: P3** — form B never crosses form P (predicted crossover at k̄ ≈ 1–2); delta
coding wins at every fraction for a single-family population. The failure is informative:
within one family, repack is never the out; the out is a new family, and re-sorting shows
families don't exist in diffused noise.

## What would make it wrong

The kick magnitudes are the crate's model, not measured plane residuals; if real averaged
tide residuals are ±2^k quanta, bits/scar ≈ Σ log₂(δ/q) + 10 rescales accordingly (±2⁶
quanta ⇒ ~30 bits/body ⇒ 10⁹ fit in 3.8 GB). Also: my population is one family on one
orbit; a real belt spread over many orbits has a higher program floor but the same
per-scar law. `b-belt-wire` should re-plug the law's real quanta. And if ties/reabsorption
in the real law return ships exactly to their program (my kicks never do), the asymptote
drops by the reabsorbed fraction.

## Cost of adoption, and fit

Adoption is a number and a redirection, not code: H_live(belt) = 61 × scar_frac bits/body
governs B18's belt arm; `b-h-live` becomes "choose the residual quantum" — coarsening
stored residuals 8× per column saves ~12 bits/body (61 → 49; capacity 6.9×10⁸), lawful only
if the player cannot differentiate it (B18's "what the player can differentiate", Julien:
"the floor is what the player can differentiate").

PRINCIPLES, verbatim: "The memory floor is information-theoretic (entropy given shared
structure), not bytes × count" — measured: storage sits ~20% above the 50-bit residual
entropy, and no ordering recovers it, so the floor is real. And "nothing is evolved that
can be derived when looked at" — the 61 bits are exactly what cannot be re-derived: they
*are* the physics the belt received. "Less is more": the only cheap left is not storing
what the player cannot see.

## The lens

Fermi first: the decomposition (fraction × entropy-per-first-kick, overwrite economics)
predicted the shape and the straddle; it under-predicted the per-scar base (50 → 60 with
index/framing) and over-predicted the diffusion slope. What the lens may have made me miss:
the *distribution* of kick magnitudes (real tides are heavy-tailed, not uniform ±2¹⁰ — a
tail of deep kicks stores at column width, and a mass of tiny kicks may store below 1 bit
each in shared blocks); and the player as a source of distinctions (off-plan AI aside, the
wildcard's own actions are distinctions the budget must also hold).
