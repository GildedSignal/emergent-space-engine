# predictions.md — 20260930-2250-library-71a7 (library lens)

Written BEFORE the decisive checks below. Cases not tuned on: exact byte-match of quotes,
crossover arithmetic, and the anchored control on rejected lessons.

## Held-out predictions

- **P1 (verbatim).** Each of the 5 chosen quotes matches the cached Readwise export
  (`readwise.jsonl`, fetched this run) byte-for-byte modulo whitespace. I have not yet
  run `grep -F` on the final wording; if any fails, that lesson is dropped or marked UNVERIFIED.
- **P2 (crossover inside cadence range).** From the board's published numbers only
  (setup 2.5–24 µs per candidate pair per element change; 1.7M candidate pairs, 427
  encounters per 20 orbits on belt 0; 786 work per encounter for element-sort), the
  setup cost amortized over an element's lifetime exceeds encounter work unless elements
  outlast ≈ 0.1–1 orbits at σ_e ≈ 0.4–1. I predict the crossover lands INSIDE the law's
  plausible kick cadence (0.3–32 kicks per orbit, H0190), so kick cadence must be measured
  before r8 v3's cost criterion freezes.
- **P3 (anchored control bites).** At least one candidate lesson I was tempted to ship —
  Feynman's committee quote ("summing it all up") mapping to commutative-monoid messages,
  and Korzybski's "map is not the territory" mapping to the zoom-is-the-minimap — will
  FAIL the lens's own control: each names a decision the board has ALREADY taken
  (monoid messages are a recorded lead; minimap is OC#30). Ship only what changes a decision.
- **P4 (concentration already visible).** The one published concentration number
  (427 encounters among 1.7M candidate pairs per 20 orbits, ≈ 2.5e-4) is consistent with
  a heavy-tailed (Zipf-like) surprise distribution; if instead encounters were uniform
  over candidates, L4's store-sizing argument would be moot.
## Outcome (after running `python3 verify.py` → verify.log)

- P1: PASS 5/5 (whitespace- and quote-glyph-insensitive match; the Simons transcript
  keeps its own concatenated spelling, e.g. "iunderstood").
- P2: **FAIL, and the failure is the useful result.** Crossover K* = 4e-4–4e-3
  kicks/orbit (element lifetime 253–2,431 orbits) — OUTSIDE the plausible cadence
  range 0.3–32/orbit. At any plausible cadence, per-element-change setup exceeds
  encounter work by 76×–78,000× (1 work-unit ≈ 1 µs), or 1×–778× even if a work-unit
  is 100 µs. So measuring cadence (HANDOFF's plan) is necessary but insufficient:
  r8 v3's certificates must be kick-robust (re-pay only when envelopes touch), else
  the encounter layer is unpayable. A failed expectation, not a failed method (H0183).
- P3: PASS. Both pretty analogies rejected by the control: "commutative-monoid" is
  already HANDOFF line 78; the minimap is already OC#30 (PRINCIPLES line 19). They
  confirm decisions; they do not change them.
- P4: PASS. 427/1.7e6 = 2.5e-4 encounters per candidate pair per 20 orbits
  (n ≈ 1,843 bodies): uniform over candidates is dead; the tail is where the mass isn't.

