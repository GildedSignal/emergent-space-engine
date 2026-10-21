topic: scan-news
status: open
closed-by:
valid-while: crates/universe@00696555 + 20261021-1551's patch (scanpre example, stat module, per-row/reg epochs; no law change)
updated: 20261021-1551-spacex-eb24

# The player's scan: the one comb still walked as if everything changed

## Current best

**NEW (eb24, spacex — od 1 executed; od 3 executed and refuted as a certificate).** The walk's price
per arm (instrument `scanpre`, clock bias 36.2 ns/call): 3e3 coast fallback — loop 90% of ~280 µs/capture
(build 43%); 3e4 coast fences — **radial 73%**, loop 26%; 1e5 burn rtf100 — radial 52%/loop 48%; 1e5
burn rtf2000 — loop 1.155 ms (fallback near = 100,076, the wave-era bail). Overpayment in time:
memo-discarded walk **37%** of walk time at rtf100, **60%** (2.43 s of 4.0 s) at rtf2000. **Od 3 is
dead as any mutation-counting certificate** — three exact forms, 0 hits each, digest-identical
(c1e220b4… across off/v1/v2/v3): global epoch (dead by construction: every capture follows the
player's own `apply`, which puts the row — universe.rs:761→772; checker-verified); per-row+reg
epochs — miss_me **861/861** (same call site); `me` by value + epochs — miss_near 723, miss_reg 138
(checker: 721/140): history-retiring rebinds preserve `binding_at(j,t)` through the retired segment,
so **the reuse law is value-equality through history, not absence of mutation — the exact pre-walk
certificate costs the walk it skips.** The news-fed window (membership at kick/birth events) is the
only lever and must eat the whole walk, radial query included. **Prior standing (9b03):** news_frac
1.2–11.4%; player binding changes 49–51% of scans; memo 47% same-tick burn; radial fence
belt-N-fragile (checker: flight-dependent too — 3e3 burn fences, 0 fallback).

## Refuted

- **NEW — "the exact pre-check deletes 47–50% of captures' walks" (od 3, as a cheap guard):**
  refuted as wired — three exact forms (global epoch; per-row epochs over near + per-doll
  registration epochs; value-compared `me` + per-row epochs) all 0 hits on the shipped plane,
  digest-identical to off; the domain is value-equality through history (rebinds preserve
  `binding_at(j,t)`), which only the walk itself checks (20261021-1551-spacex-eb24).
- **"The news-fed ceiling is only the build term" (od 1's implicit risk): refuted by attribution —**
  the fence arm's walk is 73% radial query; only the fallback arm is build-dominated (43%)
  (20261021-1551-spacex-eb24).

## Open directions

1. **The news-fed window, now priced:** maintain the candidate set at kick/birth events (9b03's
   composition), evaluate the predicate per scan. Its target is the whole walk per arm (eb24's
   table), of which 37–60% is currently pure repeat (memo-discarded). The radial query must go
   with it (73% of the fence arm's walk).
2. **The wave-era fallback capture** (129/3427 at rtf 2000, near = 100,076 = the whole doll):
   the one regime where the walk is milliseconds; a capture-side bail or streaming form (scan-
   locality od 2/od 3) is worth more than everything else combined at rtf > 1000.
3. ~~Attribute the walk's internal cost~~ **Executed (eb24): radial/loop/build/lookup split per
   arm, bias-calibrated at 36.2 ns a timed call.**
4. ~~Wire the pre-check~~ **Executed and refuted (eb24) — see Refuted.** What survives of the
   idea: the reuse is already exact post-walk (the memo, 37–38% hit rate); making it pre-walk
   needs the value domain, which is the walk.

## Contradictions

None open. 9b03's caution (the pre-check needs a nothing-resolved-since dirty bit) is resolved
by measurement: no dirty bit at this call site can be clean — the player's own apply precedes
every capture, and the near rows' rebinds are history-invisible to the values the scan reads.

## Runs
- 20261021-1443-system-9b03 (system): the scan walk measured for news on three arms — news_frac 0.012–0.114, memo 47% same-tick on burn, radial fence belt-N-fragile; the scan row is information-coupled to the kick dial.
- 20261021-1551-spacex-eb24 (spacex): od 1 executed (walk priced per arm, radial 73% on the fence arm) and od 3 refuted (0 hits × 3 certificates, miss mechanisms named; overpayment 37–60% of walk time).
