# Check 2 — 20261020-2004-spacex-26fc

Grade: silver

**Abstract.** The attribution is real and reproduced three times (author, runner's regen, this check): the 2 bench-depth "lost" emitters are dead handed-out fleet members (bodies 10,054/10,069, `from=Some((0,25/47))`, died 3,915/6,012 gs; `worst = seen_max − dead` exactly in every coast arm; drop-none 0 in all 384+ gathers, rtf 12k and N=3×10⁴ included). But the run's deletions overreach its coast-only evidence: at one-leg **burn** depth (every=300, 233k gs, digest `1a49d75b5055`) the crossing search drops **3 live ships** (12 `drop none`, warm guess past the floor by 39–960 gs), and the "dead-weight" clamp rescues 2 of 3 on the **same trajectory** (digest-paired A/B: drops 12→4, final view 10,043→10,045). The keep margin has a job exactly where one-leg's saving lives. Cost to adopt: nothing on the coast; the burn-side case needs the margin (or clamp, or cadence) priced first.

## Reproduction

- Clean tree + `work/patch.diff` applied by hand; `cargo build --release -p emergent-universe --example keep_probe2` (12 s); all five `regen.sh` arms rerun (~4 min). Every certificate line reproduces: alive-missing 0, drop-none 0, the same dead ids at both depths (fleet 25/47 bench; +13/27 at depth), worst 10,048/10,046, clamp a statistical no-op (readouts 19,813 vs 19,887, ms 382 vs 388). Digests drift run to run, as disclosed.
- Attribution verified in the raw logs: `drop dead` census lists bodies 10,054/10,069 at 3,915/6,012 gs, all 26 other deaths before the first gather (~3,300 gs), zero `from=None` deaths, 30 unique dead at depth. First loss at f=78 = member 25's death gather; miss counts (111, 96 of 120) match death timing within the frame-timing slop. The probe's fleet-id hole (no alive check for ids ≥ n_bodies) is closed arithmetically: `worst_seen = seen_max − dead_at_end` in every coast arm — a live drop would break the identity.
- `predictions.md` (20:14:22) precedes all four decisive arms (20:15:19+); its held-out cases P1–P3 concern exactly those arms and held. P4/P5 failed and are reported as failures (honest, informative).
- Code-reading verified: `observe.rs:130–135` is the soft probe (`None => return raw()`), so the census nones are indeed not drops; the shipped alive gate (`view.rs`) skips dead bodies by design.

## Attack (this check's own arms)

1. **Burn, the dial's adoption regime (outside the author's flown domain; inside the dossier's claimed domain "coast and burn").** `10000 burn 60 6000 300`, one-leg: **alive-missing in 3 of 9 gathers (live belt ids 24/25/26), drop-none 12** — `eval → None` fires on live emitters; `floor` 14.6k–70k gs, `guess` overshooting by 39–960 gs; final view 10,043 = 10,050 − 4 dead − 3 live-dropped. Bench burn, rtf 12k coast (233k gs), and N=3×10⁴ coast all read drop-none 0, alive-missing 0 — the coast claims hold everywhere tried.
2. **The clamp A/B on the identical flight.** The clamp arm survived on the same schedule (digest `1a49d75b5055` both): drops 12→4, alive ids 25/26 rescued, id 24 still dropped (its failure is not cured by clamping to the floor). The clamp is not a universal no-op; it is a partial cure exactly where the disease exists.
3. Stock deep-burn comparison is schedule-luck: the stock arm dies at 2,996 gs deterministically on most wall schedules (digest-identical across keeps), so no stock-at-depth arm was obtainable in budget; c8d5's checker measured stock None probes ×40 lower at depth, and the overshoots here (≤ 1k gs) fit under one extra ld leg — consistent with stock keeping what one leg drops, but unproven on a paired flight.

**Consequence for the run's claims.** "The 2 lost emitters are dead members" — stands. "The search defect does not exist" — stands on the stock view on every arm flown; **false through the one-leg dial at burn depth**, where the run sends the integrator to adopt it. "The clamp is dead weight" — coast-true, burn-false (partial cure). "The completeness margin is jobless" — false at burn depth: the margin's measured job there is covering the stale warm-guess overshoot (≤ ~1k gs ≪ one ld leg). The dossier's domain sentence ("coast and burn, 10⁴–10⁵") also overstates what the author flew (coast, N=10⁴ only; burn and 10⁵ are the first checker's extensions).

Minor: "264 gathers" undercounts the author's own table (384); the "−2.5%" coast saving is overprecise (stock alone spans 2.32–2.49 segments/body across runs); the retained-depth p50 comparison flips sign run to run (already annotated).

## Novelty

The live page (c8d5) left "identity still unattributed" and od 2's first step was "attribute the 2 ids". This run does that, corrects c8d5's mechanism reading, and resolves the c7a6/c8d5 contradiction — new, not in `docs/HISTORY.md` (no c8d5/c7a6 entries there either). The cadence-bound coast finding refines od 1. No repetition found.

## Goal fit

Memory at 10⁹ (board channel 2). Real progress: the attribution deletes the stock-view fix and unblocks the keep decision — "the best part is no part". But the same dossier then declares the dial's margin jobless and closes od 2 outright; the counterexample shows that closure would hand the integrator an adoption case missing its completeness cost. Premise correction cut both ways; that is why silver, not gold.

## The one experiment that would make it gold

A **paired deep-burn flight at one pinned schedule** (same digest; pin the wall coupling, e.g. by replaying a recorded frame budget): stock vs one-leg vs one-leg+clamp at every=300 to ≥ 200k gs, reading alive-missing/drop-none/segments/body on all three. It decides whether the burn-side halving costs live emitters and whether the cure is the clamp, the cadence, or a margin of one overshoot (~1k gs) instead of a full ld leg — and it folds the resulting law into od 1's adoption sentence. This check flew the one-leg ± clamp half (digest-paired); the stock survivor is the missing half.

## What the author missed

- No burn arm was flown, yet the dossier claims the "coast and burn" domain and the wiki page's completeness sentence ("no live emitter is ever lost, at one leg or two") generalizes coast evidence into the dial's target regime — where the author's own instrument (the `floor`/`guess` fields of `drop none`) was built to catch exactly this and was never pointed at it.
- The clamp verdict ("can only act on a crossing `eval → None`, which never happens") treats the shipped configuration as the only one worth curing; the dial the run promotes is the configuration that makes the path fire.
- The lens section prices mechanisms but the run's deletions were graded on a scene family half of which (burn) was never run — the fastest falsifier of a "disease does not exist" claim is a flight through the sickest regime.
