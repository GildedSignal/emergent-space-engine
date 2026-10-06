# dossier.md — 20261006-0030-library-39a2 (library lens)

## Claim

Five lessons from books Julien owns aim the allocator/cadence family of open items (kick cadence, encounter setup, frame p99, gravity-as-news, doll clocks) at decisions still unmade, each with a kill-test; two of the five anchors are verbatim-verified full texts cached in the run.

## Bottleneck

Board #4 (smoothness and the allocator) plus live item 1's named lever (cadence; q-cadence queued, B12 fails at exponent ~0.8, starved near-parabolic flybys, "one tick is the same time in every doll is false, 15–1,400 ticks at the sphere's edge"). Expected gain if the cadence lesson lands: B12's exponent 0.8 → ≤ 0.2 at equal kick budget, i.e. the plane's failing gate closes without buying compute (orders of magnitude in avoided cost). Encounter setup by predicted use deletes the 2.5–24 µs-per-pair-per-element-change trigger that r8 v3 left open, the measured 99%-dormant share (taleb-3ec1).

## Evidence

READWISE_TOKEN is unset in this environment (stated per lens instructions). Book list: `lab/library/goodreads.csv` (read: Poincaré *Science and Method* omnibus and Lefèvre *Reminiscences* are both on it).

Verbatim anchors, reproduced exactly (each command runs in < 2 s after the two fetches, ~2 s total):

```
cd lab/results/20261006-0030-library-39a2/work
curl -sL https://www.gutenberg.org/cache/epub/39713/pg39713.txt -o poincare-foundations.txt
curl -sL https://www.gutenberg.org/cache/epub/60979/pg60979.txt -o lefevre-reminiscences.txt
grep -n "slight differences in the initial" poincare-foundations.txt   # :15802
grep -n "business with the tape is now" lefevre-reminiscences.txt      # :190
grep -n "tell the truth on the instant" lefevre-reminiscences.txt      # :2653
```

- Poincaré, *Science and Method* (in *The Foundations of Science*, Halsted trans., Gutenberg 39713), Book I ch. IV "Chance" (part starts :14323, chapter :15687): "slight differences in the initial conditions produce very great differences in the final phenomena; a slight error in the former would make an enormous error in the latter. Prediction becomes impossible". Anchor for lesson 1 (cadence follows local divergence, not average phase).
- Lefèvre, *Reminiscences of a Stock Operator* (Gutenberg 60979): "Your business with the tape is now--not to-morrow. The reason can wait. But you must act instantly or be left." (:189–190) and "the tape doesn't lie, does it?" — "It doesn't always tell the truth on the instant." (:2651–2653). Anchor for lesson 4 (gravity is news: act on arrived information; the tape is truth delayed by transmission — the light cone).
- Lessons 2 (Belady/clairvoyant scheduling, Christian–Griffiths), 3 (scripted opening, Walsh) and 5 (tight coupling, Perrow) carry UNVERIFIED quotes: web search returned only summaries and reviews, no verbatim text (copyrighted books). The mechanisms there rest on cited lab results (r8 v3, taleb-3ec1, H0213, JANUS, B12 measurements), not on the words.

## Predictions

`predictions.md` was written before the retrieval. P1 said ≥ 4 of 5 quotes retrievable verbatim: **failed** — 2 of 5 (the two public-domain texts; three copyrighted books yielded no verbatim passage). P2–P6 stand as written; they are the falsifiable content of the five lessons and map one-to-one onto existing harnesses (behave B12, the belt-0 trace, plane `--bench`, the q-gravity-at-c falsifier, the B12/JANUS handoff sweep).

## What would make it wrong

- Lesson 1 dies if slack cadence passes B12 only by spending > 1.5× the kicks (budget, not schedule), or if the slack forecast's own cost exceeds the kick it saves.
- Lesson 2 dies on the first missed encounter in belt 0 (the element-change trigger stays), or if the continued-fraction next-conjunction time is not exact across the kick (then prediction is not free and the OS analogy with its LRU guess returns).
- Lesson 3 dies if frame-quantized execution must lose > 10% mean throughput to win p99 (an integrator trade, not a law).
- Lesson 4's planted-law probe: if the extrapolating law is *indistinguishable* from the news law on all of the falsifier's scenes, "news" is unfalsifiable as specified and the representation must be re-derived (a premise result, still useful).
- Lesson 5 dies if the root-anchored planted law *passes* the handoff-identity sweep — then the coupling is harmless and the decoupling is weightless code.

## Cost of adoption

No engine code changes by this run. Adopting lesson 1 is one cadence rule inside q-cadence; lesson 2 is a scheduling change in `crates/encounters`; lesson 3 is an allocator policy flag; lesson 4 shapes the q-gravity-at-c falsifier before it is frozen (the cheapest possible moment); lesson 5 is a statement in law.md's open simultaneity item. Each is one step for an existing queued job; none adds a component.

## Fit with PRINCIPLES

- Lesson 1: "i care about the p95/99 results i want the game to be smooth" (CL 09-25) and "the simulation tells us what's next not us" (OC#36) — slack is the simulation's own deadline signal.
- Lesson 2: "No work for no reason" (principle 14) and "the cheapest compute is compute not done" (principle 1).
- Lesson 3: "'Use idle time to compute ahead' yes this is a whole important idea of this project" (CL 09-25 14:28) — compiled scripts are the compute-ahead artifact.
- Lesson 4: "Nothing past c" (principle 23) and "gravity must travel at c we can't get lazy here".
- Lesson 5: "Errors never compound" (principle 13) — one reversible coupling point instead of per-frame re-anchoring.

## The lens

Practitioner analogies are cheap, and three of five quotes are from memory; a physics-first reader may find lessons 3 and 5 closest to analogy. The lens also biased me toward the allocator family because that is where his library is richest (traders, coaches, accident scholars), not because I re-measured the plane; the board's own evidence (B12 exponent, dormant-pair share, tick spread) is what carries the ranking. What the lens may have made me miss: representation-level objections — e.g. whether cadence starvation is a symptom of the wrong event representation (principle 19) rather than a scheduling gap, which no library lesson can rule out; only P2's probe can.
