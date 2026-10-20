Grade: gold

**Abstract.** The live plane's scheduler — five per-body `Calendar`s plus the 16 B deadline `pos` cache, all reserved at `body_cap` — is 156 B/body of schedule-only state that no 10⁹ ledger row prices: unresized 156 GB ≈ 19.5× the 8 GB machine; live-sized (λ·τ·N, 0659's constants verified in the record) 0.272 GB, a ×574 flip. Reproduced exactly: 28.00 B/slot N-flat (counting allocator, 2 allocs); census `ship_ticks` = `waiting` = 1.000–1.002×N with identical counts, locals 311–333 / 105–108 absolute, queue 5–6. Checker2 extensions: N = 10⁵ identical; rtf 10⁵ waves drain `waiting` to 0.10×N with `queue` at 0.90×N, yet `ship_ticks` ≈ N and queue+waiting ≈ N at every census, so 156 B/body capacity and ≈72 B/body content are regime-independent. Adoption: a ledger row plus live-sizing with dense ids or 25ce's cursors.

## Reproduction (clean tree, patch applied by me)

- `schedbytes` (my run): `scalar_size 16`, `slot_size 24`, `pos_row_size 16`; `calendar_new` n = 10⁴/10⁵/10⁶ → allocs 2, bytes 28.0000/slot exactly; apparatus 156 B/body → 156.0 GB at 10⁹, live(L = 1,744,000) 0.272 GB; heap ops 29.9/37.9 ns fill/update, 345.7 ns/pop (author 30.8/37.6/364; regen 33.5/38.4/368 — timing jitter only). All match.
- `schedcensus` (my run, same driver): K = 10⁴ and 3×10⁴ reproduce the dossier line for line (10,028/30,028 bodies; 30,043/30,043 identical counts; `child_ticks` 311–333, `prunable` 105–108 absolute; `queue` 5–6; `pos` = N; ≈3,000 kicks per census window).
- Code claims read and confirmed: five `Calendar::new(body_cap + fleets.len())` at universe.rs:481–490, `pos = vec![[0.0;2]; n]` at :479; `Calendar::new` = `Vec::with_capacity(n)` (24 B) + `vec![NONE; n]` (4 B) — exactly the measured 28. Schedule-only contract: universe.rs:14–17 ("nothing it breaks a tie by reaches an outcome"), observe.rs ("deadlines … never an outcome"). λ = 4×10⁻⁵/body/game-s (0659; budget-1e9.md:108) and τ = 43.6 game-s at 8 GB (budget-1e9.md:136) both real, so L = 1.744×10⁶ is the record's own live population.

## Held-out predictions

`predictions.md` (00:45) precedes the dossier (00:47); census numbers regenerate exactly. P1/P2/P3/P6/P7/P8 held; P4/P5 failed and are reported as failed. The failures were pre-flagged as the uncertain arms, and they point *away* from the author's initial four-container story toward two — the opposite of tuning. The pre-registered kill criterion (P2 ∧ P4) did not fire. Honest pre-registration.

## Adversarial arms (mine)

1. **N = 10⁵** (next decade above the tested range): identical law — 100,023/100,023 identical counts at build, `ship_ticks`/`waiting` 1.000–1.001×N throughout, locals 311–333/105–108 absolute (N-independent), queue 5–6, pos = N.
2. **rtf 10⁵** (1667 gs/frame, outside the author's regime): `waiting` oscillates 0.978 → 0.102 → 0.968×N and `queue` swings 261 → 9,023 (0.90×N) → 336. Two consequences: (a) "`waiting` = N at every census" is coast-regime — the page's annotation already says so, and my numbers confirm it (my queue peak 9,023 vs the annotation's 9,642; same phenomenon); (b) the regime-invariant facts hold on my flights: `ship_ticks` = 1.000–1.001×N always and queue+waiting = 10,033–10,048 ≈ `ship_ticks` at every wave census, so the ≈72 B/body live content and the 156 B/body capacity (reserved once at `start`) are regime-independent. The headline survives its worst case.
3. **`Calendar` semantics vs "policy alone"**: `set` returns `Error::Range` for slot ≥ `pos.len()` and `pos` is indexed by body id (calendar.rs:112–117) — slots are body ids, so live sizing requires dense live ids at promotion (or 25ce's cursors). The ×574 flip stands at the orders measured; the dossier's "sizing-policy change … promotion machinery already exists" underplays this (the page's checker annotation corrects it; I confirm from the code).

## Novelty

No prior pricing of the five-calendar apparatus: budget-1e9.md's memory terms are build (2,348–2,464 B/body) + wired store (1.7–2.4 B/live-body, 07b4) only — f623's new rows are CPU/traffic, not calendar bytes; HANDOFF:67's identity carries no scheduler term; the record's only queue-byte entries are 6a0e's single-calendar 16→8 B scan and 25ce's design (both characterized accurately). This is the first shipped-code measurement, and it corrects a composition premise: "wired 0.2–2.0×" silently excludes the scheduler, which unresized is 19.5× the machine. Not a repetition; the lens section positions it honestly against 25ce.

## Page

Faithful. The NEW entry's numbers all trace to evidence I reproduced; the checker annotations in it match my independent measurements. Minor hygiene: the author's page drops d520's superseded "Prior standing" paragraph; its facts survive in 45c0's paragraph and Refuted — defensible compression, not overstatement. No corrections needed beyond what the page already carries.

## Goal fit

Board bullet "memory at 10⁹"; PRINCIPLES #24 ("The memory floor is information … why do you need so many bytes per entity?") — the non-due body's scheduler floor is ~0 B and the next-due word is already carried (calendar page, od 4). Gold bar met by the premise-wrong route: the ledger's wired-memory closure is shown store-only, with the missing term measured on shipped code at ×574 leverage; adoptable within one step (carry the row; wire 25ce's cursors or live sizing with dense ids).

## What the author missed

- Live sizing is not "capacity policy alone": calendar slots are body ids (`set` errs, no `pos` growth path) — dense-id promotion is real wiring work, named only in the page annotation, not the dossier's cost section.
- The dossier's parenthetical "the always-queued rule keeps `queue` small" under burn is falsified in kind by the wave regime: `queue` transiently holds ~0.9×N. Capacity is unaffected, so the composition number stands, but the mechanism claim is wrong.
- λ ambiguity in the record unacknowledged: 4×10⁻⁵ (0659) vs 3.55×10⁻⁵ (a9d7, "1/28,141" in nladder) — L moves ~13%; immaterial at orders, but the citation should name both.
- No burn or fleet-doll arm (`child_ticks` under a 10⁶-fleet doll unflown) — disclosed, and the page's od 7 names it.
