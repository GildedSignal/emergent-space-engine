topic: nladder
status: open
closed-by:
valid-while:
updated: 20261016-0023-quant-404b

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The birth rail is first-plan-dominated, not compile-dominated: at the ladder's true belt keys one
belt body costs 42–44 µs/body to build on the lab box (Linux/x86; the M1's own anchor is 28–31),
of which draw+`add_body` is 9.3–9.7 µs (22–24%, matching c4d3's 9.2 µs measurement of the same
path — a lab Linux i7-4790 number, same box class but a different harness, so this is cross-run
agreement, not box-invariance) and `Universe::start`'s tick-0 `replan`+`apply` pass is 32.5–33.5
µs/body (76–78%), flat in N from 10⁴ to 3×10⁵ (slope exponent ≈ 1.0), seed-stable (held-out seed
3: 42.6 slope, plan 33.0), requeue+alloc+rekey ≤ 0.1 µs/body
(20261016-0023-quant-404b; `ES_BIRTH_SPLIT` print-only instrumentation, digests identical to the
pristine tree at the same commit).** Consequences: (1) the 10⁹ fill is ~8 M1-core-hours, ~6 of
them the plan pass — the exact work a program-store birth (b29a's smallest promotion) never does,
so the compact store's CPU case is 3.3× its compile-path case, not just a memory case; (2) any
lazy-birth wiring that promotes-then-plans inherits the 10⁷-wave ruin at 3.3× the quoted compile
bill; (3) the pass's interior (event search vs apply's walk) is unattributed — the named next
experiment. The plane's own 28 bodies pay 25.8–29.9 µs/body in the same pass (heavier dolls).

*[Checker (silver): every number reproduced — the runner's regen (exit 0, 13/13 digest identity)
plus my own flights on the re-applied patch: seed 1 re-fly 42.0–42.5 µs/body; the registered
held-out seed 7 (never flown by the author) slope 45.1, plan 35.0 (78%); 5×10⁵, beyond the
author's 3×10⁵, plan 34.2, slope 46.0, peak RSS 1.17 GB (no cache cliff); ES_BIRTH_SPLIT off is
timing-identical (42.5); my own ladder_digest run md5-equals the record. Three corrections: (1)
c4d3's 9.2 µs is a lab Linux i7-4790 number (its dossier names the machine), not an M1
measurement — the agreement is same-box-class cross-harness, and the 3.4× plan/add ratio is
single-box until the M1 re-measure, so read consequence (1)'s ~6-of-8 M1-core-hours as
conditional; (2) the pass's interior, measured by the checker at 10⁵: `step::replan` 28.2
µs/body vs `apply` 4.2 (87/13) — the irreducible-vs-bookkeeping question is now `plan_interval`'s
search alone; (3) P3's kick-side comparator is not regenerable from the record (its 0.3–3× band
held regardless).]*

**[Prior best retained — see lab/wiki/nladder.md's standing text: the depth axis (the history
stack's growth law, 398f/57ec), the seam/retention family (e0f9, 0757, b0ed, quant-0619, f55d),
8b89's ES_LAZY_ALL, b172's formation falsifier, 1343/3dc8's passage pricing). This proposal folds
the birth-rail result in; the merge resolves against whatever side of the page's conflict stands.]**

## Refuted

- (prior refutations stand, per the page's record)
- **New: "the 10⁷ rung's build wall is a compile wall" (the ladder's break-4 reading and its
  "~250 s of compiles" promotion pricing): the compile path (`add_body`)
  is 22–24% of the birth rail; the dominant term is `start`'s one-shot first-plan pass, which no
  per-body compile lever touches (20261016-0023-quant-404b).**

## Open directions

1. **Attribute the plan pass's interior** (`step::replan`'s event search vs `apply`'s position
   walk vs the binding readouts): if it is one irreducible exact search per body it is the floor
   of birth-on-the-shipped-law; if bookkeeping, part of 33 µs is deletable. One run, the prof
   feature already covers `apply`'s stages.
2. The M1 re-measure of the ratio (plan/add ≈ 3.4× on the lab box): the box-invariance of the
   integer half suggests the ratio holds, but the integrator's re-measure decides the 10⁹
   arithmetic.
3. (prior directions stand: the compact store itself, the cadence law, the comet class)

## Contradictions

- (the page's standing conflict — 398f vs 57ec on `updated:` — is the integrator's to resolve;
  this run's section is additive and sides with neither.)

## Runs

- 20261016-0023-quant-404b (this run): the birth rail split — plan pass 32.5–33.5 µs/body (76–78%
  of 42–44), add_body 9.3–9.7 (c4d3's M1 anchor confirmed), flat in N, seed-stable, digests
  identical; the 10⁹ fill is first-plan-dominated.
