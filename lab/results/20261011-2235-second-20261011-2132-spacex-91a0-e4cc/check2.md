# check2.md — second checker, blind to the first (checker2-prompt.md; check.md not read)

## Reproduction (clean tree, `git apply work/patch.diff`, fresh `cargo build --release -p xtask`, my own runs)

| config | shipped | mine | notes |
|---|---|---|---|
| s1 m400 2000s | 7443 (×3 runs) | 7469, 7469 | 0.35%; determinism pair identical on every headline |
| s7 m400 | 9196 (work) | 9160 | lands exactly on the quoted range's low end |
| s99 m400 1000s | 5277/5287 | 5287 | exact on the work value |
| m48 | 1113 | 1113 | exact |
| s1 4000s | 10339 | 10339 | exact; catalogue flat at 428 from s1861 (shipped 1860); contacts dead after s543 |
| m1600 | 20647 | 20495 | 0.74% — one noisy shared-machine sample, above the quoted ≤0.4% band; catalogue [28,1537], peak 1415, vel 22.3, ship 49.9 all exact |

All bits/slopes identical to 2–5 decimals everywhere; `work/metrics.py` regenerates `work/all-metrics.jsonl` line-for-line from the shipped rows. Catalogue endpoints, monotonicity, spawn-vs-gain accounting (417/406/388–389/71/1500 spawns vs 400/390/368–369/48/1509 gained), s7-keeps-400-and-gains-390, contacts dead in the last 100 game-seconds, bytes/body 1183→5766–10046→4809–6843: all reproduced. Tick drift confirmed and stronger in my determinism pair (first divergence game-s 70, 1160/1200 rows differ entirely, headline quantities identical) — the range-not-row-identity correction is the right reading of this harness.

## Adversarial

1. **Unseen seed 42, m400:** kicks 6097 firing to s1993; slopes −6e-05 (ship) / 0.0 (vel); keys all distinct; catalogue monotone [28,403] on 390 spawns; contacts a transient (last s1563 — later than any author seed, still ends). Invariants hold.
2. **The leak in code:** `Catalogue::release` fires only at rebind (`universe.rs:373` retune, `universe.rs:512` retired segments) and handoff (`step.rs:710`). Every death path (`step.rs:593,599,664,668,697,703,748,778,783`) sets `alive=false` without releasing the tube key. Churn-leak mechanism is a code fact, not just rows.
3. **The coder:** bits/ship = 40·(d/n) + log2(d) with d=n always ⇒ ≈40 + log2(n_ships); flatness is structural under the engine's own tube quantum (32-bit angle + 8-bit time). Coding at the representation's native resolution is the right question, and the author's lens note flags the coder-family caveat honestly; it does not touch the store-vs-floor conclusion.

## Predictions

Written before the genuinely held-out runs (4000s at 13m-to-go, m1600 at 12m, both after predictions.md at 16m; the base-config rows at 18m predate it, but those reproduce an already-published defect whose numbers are quoted inside predictions.md — disclosed framing, accepted). P1's strict row-exact reading failed via tick drift and was reported, not papered over; the usable form (≤0.4% headline agreement) held except my m1600 sample at 0.74%. P2 held (max slope 0.00045 vs kill 0.1). P3 held with the saturation at ~1860 vs predicted ~1500 (jitter, disclosed). P4 held (22.3 ≤ 22.5; log-shaped state; churn-bounded catalogue).

## Novelty and fit

No H_live entry in docs/HISTORY.md; HANDOFF names it an unmeasured risk ("distinctions created per game-second (H_live) … not measured yet") and the queue lists H_live as this build. First measured record. `docs/law.md:13` really does carry "+62 bits per kick and −60 per reabsorption", so decision (3)'s annotation target exists. Board focus item 5 (10⁹ in 8 GB): the 370–1140× idiot index over the 6–13 byte floor redirects the memory gate from compression to store structure — a premise correction, the lab's own gold ground ("shows that a premise is wrong"): two of them (zero-kicks reading; shed-based catalogue mechanism refuted by s7).

## Blemishes (recorded, none decision-bearing)

- metrics.json says m1600 "additionally applies work/clamp-1600.diff", but `patch.diff` already contains that exact change (identical hunks; applying both would fail). Reproduction works with `patch.diff` alone — verified by my m1600 run.
- My m1600 kicks delta 0.74% exceeds the quoted ≤0.4% band; single shared-machine sample, order unchanged.
- The 4000s run has no second-half velocity mean (fleet dead); correctly omitted rather than faked.
- Base-config rows predate predictions.md (nuance above).

## Verdict

Grade: gold

**Abstract for the integrator.** Claim: H_live saturates on the flying plane and the store, not information, bounds 10⁹-in-8 GB; the catalogue is a churn leak. Reproduced from a clean tree on every headline number (kicks 1113/7443–7469/9160–9196/5287/10339/20495–20647; catalogue 28→76/396–428/1537, monotone; ship tubes 45–50 bits, slopes ≤ 0.0005; velocity 18–22 bits/member flat; store 370–1140× over the 6–13 byte floor), plus an unseen seed 42 and a code-level confirmation that death never releases a catalogue slot. Cost to adopt: near zero — decisions (1)–(3) (memory gate on store-convergence ranges; catalogue reabsorption by death-time release plus (E,L) sharing; annotate law.md's "+62" as an allocator worst case) and the harness fixes (range-quoting, members clamp). Two premise corrections, both verified.

**Reasons.** The first run's silver was exactly one record defect away from gold, named by its checker; this run fixed it, carried the two refinements (4000 s horizon, 1600 members) as its own shipped rows instead of unshipped assertions, corrected the catalogue mechanism with a counterexample run (s7) and a code cause, and reported its own failed strict prediction honestly. Every number I regenerated agrees; the adversarial seed and the code audit support the mechanism; novelty against HISTORY and HANDOFF is clean; adoption is within one step.

**What the author missed.** (i) The redundant clamp instruction (clamp-1600.diff vs patch.diff) — a checker following the dossier verbatim hits an already-applied patch. (ii) The 0.4% reproduction band is machine- and load-specific; my m1600 landed at 0.74% — quote the band as load-dependent or widen it. (iii) Flatness of bits/ship under a 40-bit-capped tube coder is close to structural; the stronger, un-run statement would code (E,L) residuals at kick resolution and show bits/kick → 0 there too — one cheap follow-up that would make the "no distinguishing bits" claim coder-independent. (iv) Seed 42 shows contact transients lasting to s1563 (vs 468–905 in the author's seeds): "transient that ends" is seed-dependent in duration, worth a word in any gate that leans on it.
