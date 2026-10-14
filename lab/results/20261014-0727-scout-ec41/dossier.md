# Dossier — 20261014-0727-scout-ec41 (scout)

**Claim.** The cold rail's ~1.9×10³ encounter cut at 10⁹ is the kick cadence, and it is deletable by
renewal-on-certificate-failure (EDMD/KDS-style): under a real cumulative kick stream at belt kick
sizes, a pair's exact horizon windows need re-running only 4.5×10⁻⁴–8.7×10⁻⁴ times per kick — a
measured 1,150–6,400× cut against the shipped per-kick re-certification, at ~0.6–3.4 exact checks
per renewal — composed with effb's ledger the 7.7×10³-core row falls to ~4–11 cores [INFERENCE,
cross-harness composition].

**Bottleneck.** Board #2: encounter work at 10⁹ (~10³–10⁴ cores → a few cores), named "ahead of any
kick-cost work"; nladder's ledger prices it at 7.7×10³ cores skin-on, 1,925× over, all of it the
per-kick re-certification cascade (0.077 cores per 10⁴-cell × 10⁵ cells). Expected gain ~10³ on
that row; it deletes the coupling between the belt's `step_log2` content policy and the encounter
budget (each then prices only its own term).

**Evidence** (all on shipped code, planar-Kepler belt n = 10⁴, σ_e 0.01, ρ 1e-4, band [1, 1.5],
horizon 1000 orbits; Linux/x86 shared cloud, orders of magnitude only):

Shipped grounding (`target/release/encounters kick|scale n|steady`):
- `kick`: 812.8 pairs re-certified per kick at 7.20 ms/kick (8.86 µs/pair, full 1000-orbit
  re-run — the shipped policy pays this **per kick**); single-kick `changed_fraction` 0.24% /
  7.8% / 8.8% / 8.6% at eps 1e-9/1e-7/1e-5/1e-3; slack-skippable 94.6%/57.5%/3.0%/0.25% with
  **0 violations up to 1e-5, 5 violations at 1e-3**; per-pair silent budget (relative period
  change absorbable) p01 4.3e-9, p10 4.7e-8, median 3.1e-7.
- `scale n` (ρ·n held): cone degree/body = 95.9 → 870 → 8,598 at n = 10³/10⁴/10⁵ (≈ 0.09·n:
  e-extent physics, ρ-independent here); encounters/body/orbit 0.039–0.041 **constant** in n;
  checks/hit ≈ 1.10 constant; crossover ≈ 40 orbits constant.
- `steady`: work/encounter 2,140 → 222 → 23.3 as horizon 10 → 100 → 1000 orbits; checks-only
  1.55 → 1.15 → 1.11 (the frozen-belt floor is ~1.1 exact checks per encounter).

New probe (`examples/cycle.rs`, this run's patch; 30 sampled bodies, 24,505 pairs each, 1024
sequential kicks ≈ 4 orbits of pair-level kick arrivals at step_log2 7, log-spaced checkpoints,
hits compared exactly at each checkpoint — renewal counted when consecutive exact hit sets
differ; co-signed and random-walk a-drift):
- eps 1e-9: renewals/pair/kick 4.5e-4 (co) / 1.6e-4 (rw) → **cut vs per-kick 2,226× / 6,429×**;
  checks/renewal 1.16 / 3.39; first-change median 128 kicks.
- eps 1e-7: 8.7e-4 / 7.6e-4 → 1,147× / 1,317×; checks/renewal 0.60 / 0.70; first-change median 16.
- eps 1e-5: 8.4e-4 / 7.9e-4 → 1,187× / 1,266×; checks/renewal 0.57 / 0.67; first-change median 8–16.
- Certificate-check overhead (integer drift vs stored slack per kick per pair, ~ns) ≈ 1 ms/orbit/body
  vs renewals ≈ 0.9–1.7 ms/orbit/body → overhead-adjusted cut ≈ **700–2,200×**, holding ≥ 10²·⁸ at
  every probed belt eps.

Composition [INFERENCE]: 7.7×10³ cores ÷ (700–2,200) ≈ 3.5–11 cores ≈ the goal's "a few cores".
Reproduce: `bash lab/results/20261014-0727-scout-ec41/regen.sh` (~2 min; shipped trio ~75 s +
cycle ~18 s).

**Predictions** (`predictions.md`, written before any run): #3 soundness held (0 violations ≤ 1e-5,
break at 1e-3 exactly as the hot rail expects); #4 over-fire held (no explosion — renewal recomputes
exact windows, the calendar's failure mode does not apply); #5 held with the honest overhead range.
Two honest misses: #1's "degree constant in n" is wrong — degree ≈ 0.09·n grows with belt filling
(the encounters/body/orbit rate is the constant, not the degree; work/encounter ≥ 10³ held);
#2's skip-formulation ("budget ≫ one orbit of kicks") holds only for the median pair at eps 1e-9
(207 kicks > 128) and dies at 1e-7 (p10 = 31 kicks) — this is precisely why the *renewal* form, not
the *skip* form, is the surviving mechanism.

**The cross-field scan (the lens).** Requirements first: 10⁹ bodies, exact (zero-miss) discovery,
no per-tick work, amortized, kicks as the only state-change events. Ranked by fit: (1) **Event-driven
MD / kinetic data structures** (Alder–Wainwright 1959; Rapaport 1980; Basch–Guibas–Hernandez, KDS
1997) — per-certificate failure repair, zero per-step pair work: the exact shape of the measured
mechanism; their known failure mode (certificate churn under dense event storms) is bounded here by
the measured renewal rate and dies only at battle-scale kicks. (2) **The slack skin** (our own, 317c/
8bfa/73f0) — the ρ-space instance of the same certificate; shipped lever, 3–12×, subsumed as the
renewal trigger. (3) **SSA conjunction screening** (CARA/COLA): the per-pair world — no exact 10⁹
answer exists there (covariance screening is probabilistic, off-goal); their coarse filter is our
cone. (4) **MD cell lists / PIC** — rebuild-per-step structures; ticks are forbidden (PRINCIPLES #14).
Mapping: the trigger is integer accumulated drift vs a per-pair slack — b29a's key-space arm (0.11 µs,
ΔE/ΔL in Q48/Q32 quanta) already produces the integer kicked key; the slack can be analytic (73f0's τ;
a smaller-than-true slack is sound, it only renews early) so no per-pair store is required at 10⁹
(the 12 B/pair store is already impossible at 10⁹: `scale` per_pair_bytes_per_body = 51.6 kB at 10⁵).

**What would make it wrong.** (a) Only the a-drift channel was streamed; e and ϖ channels and
differential precession (71a5, 8f99) may exhaust slack faster — the renewal *rate* would rise (the
policy stays sound: it renews at failure). (b) Battle-scale kicks (eps ≥ 1e-3): 5 slack violations —
unsound there, and consistent with the rails split (the hot rail is kick-bound, not
encounter-bound). (c) The composition multiplies effb's M1-implied pricing by Linux-shared-box
ratios. (d) Concentrated workloads (co-orbital formations, fleet packets) are other ruins with their
own escapes (sibling pages). Fit with PRINCIPLES: #3 "Nothing is evolved that can be derived when
looked at" and #14 "no work for no reason, so no ticks" — the pair's future is derived once and
re-derived only when its own certificate fails.

**The lens.** What the scout lens may have missed: the literature's events are physical collisions;
our renewals are certificate failures — an event class no field prices, so the 4.5e-4 rate is
measured, not borrowed; and I did not test the e/ϖ drift channels or the GR doll's apsidal advance
(`4e7c` flags that domain untested for the whole tier).
