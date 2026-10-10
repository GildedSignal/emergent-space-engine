# Dossier — run 20261010-0920-scout-e5f5 (lens: scout)

**Claim.** Gravity-as-news at scale needs quantum-gated cell accumulation: it holds news work and
memory per body constant in N at fixed density (measured exponent 0.027; 2.1×10⁴× cheaper than
the cursor-taken-literally at 10⁶), but **every plain per-cell accumulator scheme I built leaks**
(three distinct compounding bookkeeping errors, 15q–3.6×10⁴q), because an aggregate and its
direct rings must partition receivers exactly at every scale — the partition is the FMM
interaction-shell structure, and building it that way is the one experiment this run did not
finish.

**Bottleneck.** The board's risk "the light cone keeps growing" / the memo's step 5 ("gravity as
news, U_P from R5's cursor"). law.md adopts "gravity is news" on the physics side (q-gravity-at-c:
news = instantaneous to 10⁻⁷ in free fall), but nothing measures the *cost* side. R5 taken
literally is O(N) deliveries per news event and N² cursor words — the candidate-degree problem
again, this time inside the adopted representation. Expected gain: O(N)–O(N²) → O(1) per body per
game-second; deletes the growing news frontier as a memory term (what remains is O(√N) frontier
events *total*, → 0 per body).

**Requirements as numbers** (from the docs): 10⁹ bodies in 8 GB → news state ≤ ~1 byte/body
(B18); surprises 1.1 events/body/orbit (r8); work per body per game-second constant at fixed
density (B10 exponent ≤ 1.1); error type bounded, never compounding (principle 13); deterministic
order-independent accumulator sums (B8, the tie rule); p99/median smooth (principle 12).

**Evidence.** Toy: 2D periodic patch, σ = 1 body/unit², c = 1, news Poisson λ = 1/body/time,
strengths log-uniform [0.005, 0.5] (mean 0.107), receiver quantum q. Schemes: **naive** (every
body processes every front), **gated** (direct ring r_q = √(s/q); residue accumulates in nested
cells flushing at θ = q·ρ²), **drop** (negative control). Floats explore; no canonical outcome
depends on them.

- Cost (analytic + patch MC, `out/results.json`, `out/results-v2.json`):
  - naive: deliveries per body per time = λN (fitted exponent **1.000** — the instrument's
    positive control). In-flight fronts per body = 5λR/3, exponent **0.500** (29.7 at 10³ → 940
    at 10⁶): the growing light cone, made concrete.
  - gated: per body per time **40 → 48** over N = 10³ → 10⁶ (exponent **0.027**; the direct-ring
    term λπE[s]/q dominates and is N-independent, the emission annuluses add ~log₄N). MC at
    16 384 bodies: direct 34.8 + flush 18.6–53 per body per time, matching the closed form
    within 1.25×. Ratio to naive at 10⁶: **2.1×10⁴**.
  - Coherent fleet (10⁴ simultaneous news, one region, N = 10⁶): naive 10¹⁰ deliveries; gated
    6.8×10⁵ (**1.5×10⁴×**): the aggregate becomes the source (principle 6).
  - Memory: gated ≈ 9.5 words/body in flight (constant, exponent 0.009) + 0.083 words/body
    accumulators; the disk-wide frontier is O(√N) events *total* → 0 per body. R5's literal
    cursors: N² words (10¹⁸ at 10⁹ — dead on arrival as stored state; they must be derived, as
    R5's k* formula allows).
  - Smoothness: per-body deliveries per time bin, median 17–66, p99/median **1.3–1.5**.
- Error (exact all-fronts reference at 256 receivers, times 2/4/6; q = 0.01 and 0.001):
  - **v1** (routing: cell circumscribed radius ≥ r_q): boundary double-count, max error
    0.029 → 0.95 → **2.32 (232q, growing)** — worse than dropping.
  - **v2** (ring inscribed in cell; flush = square complement): interior receivers unserved →
    behaves like drop: max **0.238 (24q)**, median 5q, growing; drop control: max 0.147 (15q),
    growing — "never dropped" violated by both.
  - **v3** (leaf member-residue accumulator, member quantum q·d_near²): double-counts
    ring-covered members: max **358q** (persistent), 1.4×10⁴q at q = 0.001.
  - Each leak is a different bookkeeping error; the common cause: an aggregate plus the direct
    rings must be an exact partition *per receiver at every scale*, and any single-cell scalar
    accumulator breaks the partition somewhere (boundary, interior, or member shell).

Reproduce (each config ≈ 75 s, whole script ≈ 155 s — over the 60 s preference; trim the config
list in `main()` for a single 75 s config):

```
cd lab/results/20261010-0920-scout-e5f5 && python3 news_scale.py
```

**Predictions** (`predictions.md`, written before the decisive run): cost held (naive exponent
1.0 ✓, gated per-event ≤ 0.3 ✓ at 0.027, fleet ≥ 10³× ✓ at 1.5×10⁴, in-flight exponent 0.5 ✓,
gated memory ≈ 0 ✓, bursts ≤ 10 ✓ at 1.3–1.5). Missed: the ≥10⁵ ratio at 10⁶ (measured
2.1×10⁴); the error bound (predicted ≤ 6q non-growing for the gated scheme — it compounds to
24–232q; prediction 7's drop-growth held). The v2/v3 fixes were post-hoc (not held-out) and are
reported as such. My first in-flight memory model was wrong (counted instantly-consumed
emissions as disk-crossing fronts, 2646 words/body); the MC's emission rate × ring lifetime
(≈1 word/body) disproved it; the corrected model is in the shipped code.

**What would make it wrong.** The cost claim fails if real news strengths are heavy-tailed near
the quantum (the direct-ring term λπE[s]/q blows up as q tightens: at q = 0.001 deliveries rise
to 384/body/time — the certificate's quantum, not N, sets the bill; that is the right trade, but
it must be measured on real kick/thrust distributions). The error claim would be rescued only by
the FMM-shell partition actually measuring bounded (≤ L·q, non-growing); if it also compounds,
"gravity is news" as a lazy derived field needs a different bookkeeping entirely (e.g. per-pair
residue logs, which reintroduce the N² risk).

**Cost of adoption, fit.** One mechanism: nested cells already exist (dolls, cells hold
multipoles); this adds per-cell integer accumulators (a commutative monoid — the polymath scan's
"commutative-monoid messages between regions", instantiated), quantum-gated flushes scheduled by
slack, and FMM interaction shells as the delivery partition. Determinism is free (sums commute,
flush at exact integer thresholds). PRINCIPLES: "Compute only surprises" (3), "influences below
one quantum accumulate… aggregates can become a source" (6), "Errors never compound" (13 — the
run's negative results are exactly this principle biting), "light cones partition compute" (5).

**The lens (scout).** Cross-field sources: FMM multipole-acceptance/tolerance ε (Greengard–
Rokhlin; every MD/astrophysics tree code — the quantum is ε, and the interaction-shell partition
is what my accumulators lacked; verified family via search, the incremental-update amortization
claim UNVERIFIED); MMO interest management / relevance filtering (the update-storm problem;
UNVERIFIED at source); δ-CRDT delta batching (UNVERIFIED); lazy cache invalidation (UNVERIFIED);
Carlip 2000 already in law.md. The lens's blind spot bit as warned: those fields optimize for
their requirements — FMM has no retardation (I had to add c myself, and the ghosts remain
unpriced beyond the radius argument: gated ghost lifetime = r_q/c per event, bounded, vs naive
= distance/c, unbounded), and MMO relevance has no conservation law to violate. What the lens
may have missed here: whether the engine's existing Binet-cone encounter tier can carry the news
rings for free (same cone, same quanta — a build question, not a representation one).

**Grade proposed: silver.** Real and reproduced (two independent runs, controls both sides: naive
passes the cost instrument, drop fails the error instrument), one named experiment from gold:
implement the FMM-shell partition with member quanta and measure the deferral error bounded
(≤ L·q, non-growing) at the same O(1)-per-body cost. Three compounding variants killed are the
configurations, never the method (principle 9).
