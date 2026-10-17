# Dossier — 20261017-1535-taleb-ce22 (Taleb)

**Claim:** the `(j, t)` state memo's ruin mode — a stale read silently corrupting canonical state —
is unreachable in every regime the shipped flows can fly (1,327,081 censused reads, **STALE = 0**
in all five arms, including the two no plane census had touched: the spread-belt late windows and
the opening exodus), so direction 1's adoption is gated by a certificate, not a hope; and the
sharing the memo feeds on is **reader-population structural**, not uniform: on one binary the
belt doll shares 59.4/59.7% (N-linear), the locals' doll 96.8% and the non-secondaries paths
93.0/93.1% (N-flat) — 6671's 96.8% reproduced exactly, the birth wave's top multiplicity 9,714 at
N=10⁴ and 29,714 at N=3×10⁴.

## Bottleneck

Not a cost bottleneck: a **ruin gate** on the read-stream page's own "cheapest item" (direction 1,
the `(j, t)` memo, ~30 lines, "bit-identical by construction"). The page's evidence for that
"by construction" was plane-regime censuses plus one checker probe (0 stale keys in 292k calls);
the page itself names the hole — "the memo must be dropped or versioned if an out-of-order path
ever reads a source before its own event lands" — and the 5ade contradiction (memo hit 0.029 on
the spread belt) marked the regime no census had covered. Taleb: never adopt a cache on the
average regime; measure its corruption mode in the worst one. Gain: removes the last unmeasured
risk from a named adoption; if it had failed, it would have killed the adoption as specified.

## Evidence (all from `regen.sh`, Linux/x86, one shared box; logs in `work/`)

Instrument: `memo_oracle` (`crates/universe/src/memo_oracle.rs`, print-only, env `ES_MEMO_ORACLE=1`):
hashes every `Ctx::state_of(j, t)` Ok-value at its exact key; a repeat with a different hash is a
staleness event (the never-invalidated memo would answer stale). Windowed by tick (2²⁰) and split
by the doll whose `secondaries` loop is reading (`enter_doll`/`leave_doll` in `ctx.rs`). One
example line added to `nladder` (the report call) plus a Linux `/proc` arm for its macOS-only
memory reading — no engine behaviour touched: `ladder_digest "N=3000"` (mashing case, 4,723 kicks)
**identical with the oracle off and on, modulo wall-time annotations** (work/dig_off3.txt,
dig_on3.txt).

| arm | calls | hits | STALE | per-doll hits |
|---|---|---|---|---|
| N=0 coast 8 s (exodus, promotions) | 1,976 | 83.6% | **0** | — (pre-split build) |
| N=10⁴ coast 45 s rtf 600 (26,381 game-s ≈ 9 belt periods) | 277,522 | 76.0% | **0** | belt doll 0: 59.4% · locals 2: 96.8% · other 93.1% |
| N=10⁴ burn 45 s rtf 600 (held out) | 286,992 | 74.4% | **0** | — (pre-split build) |
| N=3×10⁴ coast 30 s rtf 600 (held out) | 543,151 | 65.3% | **0** | belt 59.7% · locals 96.8% · other 93.0% |
| ladder_digest N=3000 (both arms) | censused | — | **0** | digests identical |

- **The regime curve in one flight** (A1): window 0 = 29,451 calls at **100.0%** (the birth wave);
  late windows (≈ 26,000 game-s, the spread belt) fall to ~100–190 calls at 83–93% — but those
  late windows are the **locals' stream** (N-flat, doll 2), not the belt comb: the doll split is
  what separates them, which no earlier census on this page could.
- **Scaling:** doll 0's calls track N (149,945 → 458,523 at 3×N); dolls 2 and 65535 track wall
  time, not N (84,811→56,284 at 30/45 s; 42,766→28,344). Belt doll = the N-linear term d959 named.
- **Birth wave:** top multiplicity 9,714 (= belt body count at N=10⁴) and 29,714 at N=3×10⁴ —
  6671's "ONE field read evaluated once per belt body" scales exactly with N; the memo's single
  biggest win is birth, on every body, for free.
- **Mechanism reading (why 0):** `binding_at` returns the committed binding for `t ≥ event_time`
  and searches immutable history below it; values change only at the source's own events, and the
  scheduler resolves in tick order, so the only theoretical stale window is a same-tick
  read-then-write-then-read — not taken by any flow flown (including the burn's rebinding flushes
  and the exodus's `bind_surface` fits at frames 62–64, the worst frame, N=0 arm).

## Predictions (predictions.md, written before the decisive flights)

- **P1 (hit rate separates by regime) — partially wrong, and the miss is the finding:** the late
  windows do NOT collapse to ≤ 10% (they hold 83–93%), because that stream is the locals' doll,
  not the spread belt; the collapse 5ade saw is real but belongs to a population my oracle now
  isolates — the belt doll, whose sharing is 59.4/59.7% *including* the 100% birth wave, i.e.
  the spread-belt comb's own rate is far lower still (the ex-birth majority of its calls). The
  contradiction is regime, and now it is **located**: the memo's payoff is structural on the
  N-flat readers, bounded on the N-linear one.
- **P2 (0 staleness everywhere) — held**, in all five arms including the two held-out regimes.
- **P3 (oracle cost, digest identity) — held** on the case flown (identity modulo wall times).

## What would make it wrong

A flow that reads a source at a tick it has already read *after* that source's event at the same
tick lands — none exists in the arms flown; the certificate must be re-run when any out-of-order
path is added (the page's own warning). The hash is of the formatted value (FNV over `{:?}`): a
collision would mask one staleness event (probability ~2⁻⁶⁴ per pair, immaterial); a value that
changes and changes back identically is invisible by definition — that is not a corruption the
memo could cause. Arms not flown: the M1, seeds other than 1 (nladder's is fixed), the encounter
and view-only paths beyond what these flights exercise, rtf arms other than 600/100.

## Cost of adopting

The oracle stays a lab instrument (env-gated); the memo itself is the page's existing direction 1
(~30 lines, `Ctx`-local). This run adds its gate: **"STALE = 0 at every arm" is now a runnable
certificate** (`ES_MEMO_ORACLE=1` + `regen.sh`), to be rerun whenever a read path changes —
principle 22's simulation-decides, applied to safety.

## Fit with PRINCIPLES

- "Errors never compound" (P13): a stale memo read is a silent compounding error class; measured
  absent, then gated, before the cheap win is taken.
- "A failed expectation is not automatically a failed method" (H0183): P1's miss (no late-window
  collapse) is the reader-population split, not an instrument failure.
- "Agreement is not independence" (lab heuristics): 6671, 5eb2 and 5ade shared a harness family;
  this run cross-ran the sharing question on one binary with a population split, and 6671's 96.8%
  reproduced exactly.

## The lens (what Taleb may have missed)

The survival lens gates but does not build: it priced the memo's ruin mode and left its speedup
unflown (the memo itself was not adopted here — that is the integrator's one-step call, now
de-risked). The barbell's speculative end (does an adopted memo shift the p99?) is a different
run. And the oracle itself is young code: it ran five arms, not five days.
