# Dossier — 20261006-0030-m-obscure-8202 (lens: mathematical representations, the old, the forgotten and the new)

## Claim

The view's per-frame readout streams are dense diagonal slices of a 2-torus, so **no finite-order
sequence predictor can replace the light-cone gather** (measured: an order-insensitive error
plateau of 5×10⁻⁵ rad at e ≥ 0.3 for orders up to 96, while single-orbit streams are *exactly*
recurrences of order = samples-per-orbit: 5×10⁻¹⁴ at e = 0.9, k = 64) — and the frame budget's
worst hitch has an **exact integer certificate** W* = max window surplus that equals, bit for bit,
the worst backlog of every work-conserving schedule (528 = 528 and 620 = 620 measured).

## Bottleneck

Probe A aimed at the plane's measured #2: **the view gather is 83% of a light frame** (HANDOFF,
first flight). Expected gain was ≥ 10× (replace per-frame Newton solves with one multiply-add per
frame). The measured gain is a starter only: Newton 3.0 → 1.0 iterations per frame at e ≤ 0.3 —
marginal, not adoptable as a representation. Probe B aimed at **smoothness as a service level**
(plane.md: p50/p95/p99, hitches per hour): the certificate deletes the *guesswork* in those
numbers, not compute. Neither moves a bottleneck 10×; this dossier is offered as silver-quality
evidence (probe B, one builder step from adoption) plus a protective kill (probe A).

## Evidence

All commands run in `lab/results/20261006-0030-m-obscure-8202/`, each under 5 s, under 200 MB.
Machine: Linux, 8 vCPU, shared. `python3` 3.12.3, numpy 1.26.4.

```
python3 probeA_recurrence.py          # writes probeA_out.json (3.9 s)
python3 probeB_maxplus.py             # writes probeB_out.json (2.7 s)
```

**Probe A — linear recurrences (Prony 1795; Berlekamp–Massey 1968/69; Bareiss 1968; forward–backward
stabilization, Lang & McClellan 1980; finite rate of innovation, Vetterli 2002).**

Scene: emitter and observer on two incommensurate Kepler orbits (a = 1 and 1.7, c = 10 scene
units), 64 frames per emitter period, 8192 frames, light-cone root by vectorized bisection to
2⁻⁵². Streams: apparent angle θ (unwrapped) and emission eccentric anomaly E.

Instrument controls (after two bugs found and fixed — a sign error in Newton and a wrong
orientation of the backward identification rows):

- synthetic 6-sinusoid stream recovered at 2×10⁻¹⁰ at the true order 12 (the identifier works);
- cold Newton from the previous frame's root: **3.0 iterations per frame** (the physics works);
- two independent simulations of the identical work-conserving schedule give identical lateness
  multisets (probe B's accounting cross-check, same discipline).

Results:

| measurement | value |
|---|---|
| minimal order for one-step 1e-6 (two-orbit stream) | 12 at e = 0.05; **none ≤ 96 at e ∈ {0.3, 0.7}** |
| plateau of one-step error, two-orbit stream | ~5×10⁻⁶ (e 0.05), ~5×10⁻⁵ (e 0.3), ~1.6×10⁻¹ rad (e 0.7); insensitive to order 16→96 and fit window 1 024→4 096; fit residual equals held-out error (the model class fails, not the fitting) |
| single-orbit stream, k = 64 = samples/orbit | **9×10⁻¹⁴ (e 0.05), 1.3×10⁻¹² (e 0.3), 5.0×10⁻¹⁴ (e 0.7), 6.8×10⁻¹⁴ (e 0.9)** — exact for every eccentricity |
| single-orbit, k = 8 | 7.9×10⁻⁹ (e 0.05) but 2.8×10⁻² (e 0.7): sub-period orders only work at low e |
| Q24 fixed point, self-feeding, 4 096 frames | bounded (marginal stability holds: **no exponential compounding**), but drift reaches 0.12 stream units (k = 8) and 1.7 units (k = 16): coefficient rounding dominates at higher order |
| Newton iterations with predicted starter | 3.0 → 1.0 (e ≤ 0.3), 3.0 → 2.1 (e 0.7); never 0 at 1e-13 tolerance |
| kick 1e-4 at frame 3000, 1-D stream monitor | false alarm 66 frames *before* the kick (residual nonstationarity); re-identification 64 frames after |

Reading (principle 32 made concrete): a single orbit sampled at s samples per orbit is *exactly*
a linear recurrence of order ≤ s — aliasing folds its Fourier series into finitely many digital
frequencies; this is the sequence form of the cycle memo the engine already has. The two-orbit
apparent stream is a dense diagonal on the 2-torus: its digital spectrum is infinite, the
required order scales like the product of the two harmonic contents (~10³ at e = 0.7), and no
finite order pays. The right representation is the torus (advance two phases by additions, read
positions from tables), which is what the tube + cycle memo already is. **The alternative was
measured and died.**

**Probe B — (max,+) window certificates (Lindley 1952; Baccelli–Cohen–Olsder–Quadrat 1992;
network calculus, Cruz 1991; Karp's integer cycle mean, 1978).**

Scene: 50 000 frames, C = 8 workers × 1 integer unit/frame, deadline = arrival + 2 frames;
arrivals = deterministic base 5 + single-cause Pareto bursts (α = 2.5 at 67.3% utilization and
α = 1.5 at 66.7%). Certificates from integer prefix sums, one O(T) pass:

- **W\*** = max over windows of (arrivals − capacity): the backlog **any** work-conserving
  schedule must reach. Measured: 528 (α 2.5) and 620 (α 1.5), each **exactly equal** to the
  simulated maximum backlog, bit for bit.
- **M** = W* − C·D: deadlines that no schedule can meet. Sound: no simulated miss ever occurred
  with M ≤ 0; misses occur (5.9% / 6.6% of units) exactly when M > 0.
- Policies: central queue ≡ rotating round-robin shards ≡ shards+stealing (**identical lateness
  multisets** — provable for unit-granular instantaneous assignment, and verified). The
  *non-rotating* `id % 8` split of the deterministic base saturates shards 0–4 permanently:
  p99 lateness 2 198 vs 9 frames (**244×**), 97% missed. A 1-frame handoff latency (units visible
  to their shard one frame late, deadlines unchanged) costs p99 9 → 10 and misses 5.9% → 8.5%.
- Tail: α 2.5 → 1.5 at equal utilization moves p99 from 9 to 24 frames (2.7×) and nothing else —
  the tail index sets the p99, confirming that the frozen gates judge tails, not means.

## Predictions

`predictions.md` was written before the decisive runs. Against the final, debugged instrument:

- **A1 failed** (order ≤ 24 at e ≤ 0.7): only e = 0.05 passes; the plateau is structural.
- **A2 failed at Q24** (bounded drift holds — the compounding half was the point — but 0.12
  units ≫ 1e-6; the integer form needs ~16 more coefficient bits or re-anchoring, which eats the win).
- **A3 partially held**: iterations 3.0 → 1.0 (≥ 2×) at e ≤ 0.3, but never 0, so the gather
  saving is marginal, not a representation change.
- **A4 failed**: false alarm before the kick (nonstationary residual); re-identification 64
  frames ≈ 4k (2× my bound).
- **A5 failed**: no order was reachable at e ≥ 0.3 at all.
- **B1, B2, B5 held** (sound, exact, < 1 s). **B3 failed** in its premise: fair unit-granular
  sharding ties the central queue exactly, so there is nothing to steal in this model; the
  measured fragmentation costs are the remainder-skew trap (244×) and handoff latency (+1 p99
  frame, +45% misses). **B4 failed** as a number (2.7×, not ≥ 10×) while confirming the
  direction (the tail decides the p99).

## What would make it wrong, adoption cost, fit

Probe A's kill could be wrong if the engine's actual view streams are single-frequency-dominated
(circular orbits everywhere): then order ≤ samples/orbit recurrences are exact and the gather
becomes table reads. That is a special case of the existing cycle memo, so nothing new is adopted
either way. Probe B's certificate is exact for the *given* trace; it would mislead if the
engine's real arrival process is not captured by single-cause bursts (correlated fleets, the
player). Adoption cost: probe B is one function on a measured arrival trace plus a line in the
plane's bench output (`W*`, `M`, `max backlog`, `p99`) — it turns "hitches per hour" into a
frozen, precomputable bound and separates "the workload forces it" from "the scheduler wasted
it" (never split work by `id % k` against a constant base; handoff latency costs its own
duration in p99; beyond that, order only chooses *who* is late — the view first).

PRINCIPLES fit: probe B is "gates are frozen before the first run" for smoothness (AGENTS);
both probes are "measure before claiming" and "a failed experiment kills that configuration,
never the method" (9): the configuration killed is the 1-D sequence predictor, and the method
it points back to — phases on a torus, positions from tables — is principle 32 ("under the right
representation many symmetries can appear") and principle 6 ("store the generator, not the
generated").

## The ranked catalogue (the lens's survey)

Ranked by gain × probability ÷ cost. "Probed" entries have numbers above. Everything here was
checked against `docs/law.md`, `docs/representation.md`, the Opus memo (`lab/refs/opus-math/memo.md`,
R1–R5 and its rejected list) and `docs/HISTORY.md`; what those already cover is not resold.

1. **(max,+) window certificates for the frame budget** — *probed*. The algebra where addition
   is max and multiplication is addition makes synchronisation systems linear (Baccelli et al.,
   train networks and semiconductor plants: skin in the game). For us: W* and M are integer,
   one-pass, order-independent, and *tight* (measured exact). Level: the allocator/plane service
   level. Replaces: nothing structural; adds the missing frozen bound behind plane.md's hitch
   metrics. Kill test (done): exactness against simulation — passed.
2. **Linear recurrences as the engine's "boring-stream" representation (Prony/BMA/FRI)** —
   *probed, killed for the view*. Positive residue: (a) the kill articulates that the torus
   (phase pairs) is the right water, matching the existing cycle memo; (b) a 1-line starter cache
   (last k roots → k-term predictor) cuts gather Newton 3.0 → 1.0 iterations where e ≤ 0.3;
   (c) the exactness theorem "sampled single orbit = order-s recurrence" is the sequence-side
   statement of the cycle memo and could close B9-style cost arguments cheaply. Bareiss
   fraction-free elimination (1968, the compute-starved era) is the exact-integer backbone if
   identification is ever needed at runtime (e.g. fitting elements from states in integers).
3. **Zobrist / XOR-monoid universe digests** (chess engines, 60 years of production; skin in the
   game). The universe-level B8 digest ("one digest covers the whole universe", plane.md
   foundation 2) as a commutative monoid: per-entity random 64-bit keys, XOR on add/remove,
   incremental and parallel by construction, order-independent on any thread count. Cost: ~zero;
   replaces a serial fold that must otherwise be canonicalized by hand. Trade-off: multiset, not
   sequence (pair with the provenance order where order matters). Kill test: collision audit on
   10⁶ random entity sets (birthday bound 2³² sets) — cheap.
4. **Jacobi elliptic functions by Landen/Gauss duplication for resonant librations.** The second
   fundamental model of resonance (Henrard; the pendulum-like resonant Hamiltonian of the
   rotating binary doll) has solutions in Jacobi sn/cn, evaluable by the AGM duplication
   (quadratic convergence, +,×,÷ only; the human-computer elliptic tables were exactly this).
   Level: B17's regime — compiled zero-kick librations inside the doll instead of dense
   integration. The Opus memo rejected AGM loops for *strong-field cycles* (kicks rare there);
   resonance is where kicks are *not* rare, so the objection does not transfer. Cost: one
   Landen loop per compiled resonance; integers: fixed-point with table seeds. Kill test: on
   r4 v3's frozen resonant cases, compare libration amplitude and e-pumping of the exact
   sn/cn solution against converged Wisdom–Holman at the same tolerances as B17; kill if the
   separatrix crossing count differs on any seed (the closed form is only as good as its
   separatrix).
5. **Sturm chains / continued-fraction root isolation (Vincent–Akritas–Strzeboński) for the
   encounter skin's per-pair exact check.** Integer polynomial arithmetic that answers "does
   ‖r(t)‖² − b² have a root in this window" with an exact yes and a root count — no step sizing,
   no floats deciding. Skin in the game: 19th-century exactness, and computer algebra ever
   since. Level: `crates/encounters`' second-order window + per-pair distance check. Cost: a
   Sturm sequence on a degree-4/6 model is ~tens of integer ops. Kill test: adversarial
   near-tangency pairs (b within 1e-3 of the minimum) — count false candidates against a
   bisection reference; kill if slower than interval bisection at equal exactness.
6. **α-stable aggregation (Lévy; Gnedenko) for the promotion rule of sub-quantum deposits.**
   "Influences below one quantum accumulate" (PRINCIPLES 6): if per-event deposits are
   heavy-tailed (encounters are), the accumulation is α-stable, not Gaussian, and
   variance-based promotion thresholds *underestimate* how soon a cell's aggregate must become a
   source. Rule-level; cost: one tail-index estimate per doll per epoch. Kill test: simulate
   deposit streams from a realistic encounter distribution (Pareto α from r8's belt), compare
   promotion times under Gaussian vs α-stable bookkeeping; if they differ by < 2× the rule is
   not worth its text.
7. **Paterson–Stockmeyer / Estrin evaluation for the kick's derivative jets.** A kick is a
   multiply-add on the cycle's stored derivatives (law.md); when that jet grows past degree ~8,
   P–S halves the multiply count. Micro; adopt only if a profile shows jet evaluation. Kill
   test: bench, as with all implementation-level claims (representation.md's law/implementation
   split).

Considered and dismissed here (not reselling the memo's rejections — these are my own): **Grassmann–Plücker
ray space** for the gather (it is the existing bit-parallel shift-AND light-cone in different
words); **Möbius inversion on the doll tree** (the monoid rollup already pays; the inverse push-down
is implicit in handoffs); **Weyl/Kronecker equidistribution** for averaging nodes (R2's closed
forms removed the quadrature that would have needed it); **sorting networks** (R4's Foata normal
form is the canonical parallel schedule; a bitonic order adds nothing the tie rule lacks);
**de Bruijn/LFSR birth programs** (shipmem's belts already judge equidistribution exactly, B18b);
**Chebyshev compact residuals** (old lineage, H0103–H0108: "do not retry a 10⁻⁸ Chebyshev" — the
recurrence differs by being online and self-certifying, and the probe killed the 1-D form anyway).

## The lens: what it may have made me miss

This lens reaches for algebraic elegance, so it over-trusts sequence-predictability and
under-weights the boring truth that the engine's streams are products of several bodies' phases —
the probe had to be killed by its own instrument to see the torus. It worked at the readout and
scheduler level and barely touched the two places where old mathematics has the most skin in the
game: the *compiler* (Darwin-phase quadrature, Kerr's Mino-time cubic — Astra's ground) and
*memory* (population programs — Sol's ground); a lens with better taste for "what the builder
touches next week" would have spent one of my two probes on the encounter skin instead of the
view. Both probes are simulations of structure, not measurements on the plane: adoption claims
here are one builder step away from being anchored to `xtask universe --bench` traces.
