# Run 20261016-0213-second-…-taleb-51b7-e28f — the cure's first rung: the mint per candidate-set change

## Claim

Checker 2's named gold experiment is flown: the player-neighbourhood scan's candidate list moves
behind an `Arc` and is **shared with the previous scan whenever every entry is the same** (the
`same()` invariant the shipped reuse rule already trusts), so the mint becomes **one snapshot per
candidate-set change instead of one per player binding change** — during a burn only the player
changes, so **one 11.3 MB snapshot serves the whole burn**: the record's fenced arm (10⁵, dead at
148 scans / 1.92 GB / 2.5 s of burn) **completes all 720 frames at 307 MB with `mints = 1`** (regen-identical, digest `36f8e1a4…` twice), and
a held throttle at 10⁴ rides **971–973 consecutive binding changes on one snapshot**; the minted-bytes
rate during a sustained burn drops from ~3.3–4.4 MB/frame (shipped, fences at ~430 changes) to
≤ 12 kB/frame amortized (**steady-state ≤ ~7 B/frame at 10⁴, ~9×10⁵×; ~109 B/frame at 10⁵,
~10⁵×**), while **every flushed encounter is identical**: five robust ship-vs-cure A/B digest
equals (10³/10⁴/10⁵-quiet word-and-sustained arms, budget-free or far-from-budget — the trusted classes), the 10⁴ word digest equal to the record's `73972744…`, and
all ten `ladder_digest` rows — burns and the wave included — are bit-identical with the cure
compiled in. The 10⁵ answer bill, held out by the record ("never measured directly"), is measured
here: **116.5–118.4 s of end-of-run flush for 304 distinct scans ≈ 0.38–0.39 s/scan** (~3.9 µs/body — the
record's 150–190 ms extrapolation was 2× optimistic), and it buys nothing: enc = 0 in every arm.

## Bottleneck

Board #1 (bodies 28 → 10⁹). The record priced the ruin (one scan = every candidate's binding =
113 B/body, minted per player binding change, monotone to swap death; d7bc's fence as the only
guard). This rung **deletes the ruin** (~40 lines in `encounter.rs`, adoptable in one step,
answers bit-identical) instead of fencing it, and hands the encounters tier two corrected
anchors: the answer is 0.39 s/scan at 10⁵ (not 0.15–0.19 s), and the capture walk (p50
25.7–26.9 ms standing at 10⁵) is now the whole remaining burn cost — the candidate-set
certificate is the only lever left on this seam.

## Evidence

All on the lab box (Linux/x86, shared; orders of magnitude only). Probe: `cargo run --release -p
emergent-universe --example belt_ladder -- <N> <arm> [s [rtf [budget [noflush] [hold_every]]]]`,
the record's own probe extended with mint counters (`encounter::mint_stats`), a flush timer and a
per-frame RSS curve; `SCAN_SHARE=0` restores the shipped mint **inside the same binary** (the
A/B is one build). `beltburnhold` = the word re-issued every `hold_every` frames (a held
throttle). Raw: `raw/*.txt`; everything regenerates via `regen.sh` (~10-13 min under load).

**Identity (answers identical) — A/B pairs, digest ship = cure (five robust; one wall-capped witness):**

| arm (budget-free) | ship mints | cure mints | digest (both) |
|---|---|---|---|
| 10³ word 3 s | 212 | **1** | `5a2dd13c…` (= ×2 each, smoke) |
| 10⁴ word 8 s | 324 | **1** | `73972744…` (= the record's own budget-free digest) |
| 10⁵ word 2 s | 21 | **1** | equal (`f969d848…`) when both sides truncate at the same wall-capped frame (first run, 64/64); a regen rerun under load split the truncation frames (63/59) and the digests with it — this pair is the **mint-law witness, not an identity claim** (schedule artifact, disclosed) |
| 10⁵ quiet 3 s | 0 | **0** | `c459ac4b…` (far-from-budget, the robust 10⁵ pair; also identical at budget 10000) |
| 10⁴ held ×30 20 s | 429 | **1** | `688d606f…` (sustained burn) |
| 10³ held ×30 4 s | 253 | **1** | `742fa68d…` |

Plus: quiet 10⁴ = the record's `612c1388…`; quiet 10⁵ `c459ac4b…` identical at budget 12 and
10000 with **mints = 0 by direct counters** (the record's held-based "quiet mints zero", now
observed at the mint site); and `ladder_digest` on the cured tree = the record's pristine values
**on all ten rows** (`4b822570…/9e46f10f…/bab8d6f5…/6895ce06…/8eb769bd…/484ccce0…/ddd5b1cc…/69d7abbb…/253d8aed…/df0e87cd…`)
— burns and key-mashing included, so the cure changes nothing observable on the shipped plane (regen went further than the record: 14 rows, adding a second wave and two L10 belt crossings, 4 schedules agreeing on each).

**The mint deleted (budget-on arms, the record's ruin class):**

| arm | shipped (record/SCAN_SHARE=0) | cured |
|---|---|---|
| 10⁴ word 8 s | 730–732 MB, held 632–634 (the record) | **44 MB, held 631, mints=1, shares 315** — same backlog count, no memory |
| 10⁵ word 12 s | **fenced: 1,916 MB, held 148, dead at 2.5 s** (record, ×2 identical) | **completes 720 frames, 307 MB, held 606, mints=1, shares 303**; flush 116.5-118.4 s → **0.38-0.39 s/distinct scan** |
| 10⁴ held 45 s | **fenced: 1,902 MB at frame 387** (431 mints, held 550–553; RSS curve 186→1,827 MB, **3.34 MB/held** — sustained input mints heavier than the word's 1.11) | **completes 2,700 frames, 59 MB, mints=1, shares 838–840** |
| 10⁴ held 90 s | (dies sooner) | **mints=1, shares 971–973**, RSS 59 MB |
| 10⁵ held 12 s | (dies at ~148) | **mints=1, shares 606**, RSS flat 305→309 MB |

Derived: per-frame minted bytes, sustained burn — 10⁴ ship ≈ 6.1 MB/frame (RSS slope frames
90→360) vs cure (59−27−11.1 MB)/2,699 ≈ **7.8 B/frame** (~8×10⁵×); 10⁵ ship ≈ 10.4 MB/frame
(fences in 2.5 s) vs cure (309−237−11.3)/659 ≈ **92 B/frame** (~10⁵×). Count ratio: 971:1 at
10⁴, 606:1 at 10⁵ — and unbounded in principle (one snapshot per candidate-set change; the
belt's own re-key window, ~13.5k game-s, never arrives inside these arms). The count cap
(2048) is correctly sized again: 2048 small scans ≈ 360 kB + one live snapshot ≈ the "about
10 KB each" its comment always claimed; past the cap the failure is the designed presented-time
lag (an answer forced into a frame), not memory death.

**The answer bill, measured (the record's held-out number):** 10⁵ word 12 s cured, end-of-run
flush: **116.5–118.4 s for 606 held / 304 distinct scans ≈ 383–389 ms per distinct answer** (195 ms/scan
if the 302 cached re-answers are averaged in — the truth is the distinct ones). Cross-check:
budget-free 10⁵ frames pay ~2.3 s each (capture + one inline answer + events) — same order.
enc = 0 everywhere: at belt radii the whole bill buys no knowledge (the record's cadence +
density reading, unchanged).

## Predictions

`predictions.md` was written before the decisive arms (tuned on the 10³ smoke only). Outcome:
(1) A/B identity **held** on every completing pair; the 10⁵ burn pair proved schedule-fragile
(equal when both sides truncate at the same wall-capped frame — first run 64/64; a regen rerun
under load split the truncation frames and the digests with it, so it is reported as the mint-law
witness, and the robust 10⁵ quiet pair — added for exactly this reason — carries 10⁵ identity);
the 10⁴ word digest matching the record's `73972744` held exactly. (2) `mints = 1` **held** on every burn arm (shares 303–973).
(3) The fence deleted **held** (720 frames at 307 MB vs dead-at-148); the ≥10³× framing in the
prediction ("by count 1140×") was **wrong in denominator** — binding changes per arm are bounded
by the word/throttle program (~1,000), so the count ratio tops out near 10³; the honest ≥10³× is
the per-frame bytes ratio (10⁵×–10⁶×, above), reported as such. (4) The answer bill **held** at
0.39 s/scan vs the predicted 150–190 ms — 2× over, the prediction inherits the record's
extrapolation and is scored a miss (a useful one: encounters.md's µs/body is 2× optimistic on
this path). (5) Quiet and pristine digests **held** (all ten rows). (6) Standing costs
**held**: p50 25.7–26.9 ms at 10⁵ (ship 29.2), over-budget counts and lag the same class; the
cap never engages inside 12 s (held 606 < 2048).

## What would make it wrong

- The exactness rests on `same()` covering every field the answer reads — it does (the answer
  reads `entry/tube/clock_exp/units/turn/residual` via `readout`; `same()` compares exactly
  those plus `doll`), and the shipped whole-scan reuse already bets on the same invariant. A
  field the answer reads but `same()` misses would be a **shipped** bug my patch inherits, not
  introduces; the five robust A/B digest equals and the ten-row `ladder_digest` equality bound it
  empirically.
- Not flown: a handoff arm (born mid-belt, as the record), a multi-snapshot arm (a burn long
  enough to cross the belt's 13.5k-game-s re-key window — ~2.3 min wall at rtf 100), and N
  beyond 10⁵ (the box's fence). The mint law (113 B/body × candidates, once) has no N-dependent
  term, but the first re-key-while-burning snapshot pair is the natural next flight.
- The 10⁵ sustained arm and the 45-s ship arm run under a shared box: timing-class numbers
  (p50, fence frame) wobble; every mint/share/digest number above is load-independent content.
- Adoption: ~40 lines in `crates/universe/src/encounter.rs` (`Arc<[…]>` + a compare-and-share +
  two counters + the `SCAN_SHARE` switch, default on). Cost: one O(candidates) comparison per
  capture (~0.2–0.4 ms at 10⁵, inside the 29 ms walk). The cure deletes the memory ruin only —
  the capture walk and the answer bill stand, and both belong to the candidate-set certificate
  (the page's Open 2 / the phase-neighbour tier), not to this rung.

## Fit with PRINCIPLES

- "Compute only surprises" (#3): a per-binding-change full copy of an unchanged candidate set is
  the anti-surprise; the share is the fix at the representation, not a fence over the symptom.
- "A fix signals the wrong representation" (#19): one scan holding every candidate's binding was
  the representation error the record named; this rung retires it (d7bc's byte-cap bandaid can
  follow it out once adopted).
- "Errors never compound" (#13): the compounding term (+11.3 MB/frame) is gone; what remains
  (backlog count) is bounded by a cap that is suddenly the right size again.
- "his direct influence is bounded" (#5): the player's own changes no longer cost the universe's
  memory — one snapshot while nothing else changed is the bounded-influence statement itself.

## The lens

Second-author lens: the record priced the ruin; this rung had to delete it without moving one
answer. The risk the lens carried was scoring identity on wall-coupled arms — the record's own
digest discipline (budget-free and far-from-budget only) is what made the five pairs decidable,
and the one wall-capped 10⁵ pair is disclosed as such. Missed by the lens, found anyway: the
shipped sustained-burn mint is 3× the word's (3.34 vs 1.11 MB/held at 10⁴) — every-frame input
piles player entries; worth one look when the certificate lands.
