Grade: silver

**Abstract.** Claim: 8994's one-seed allocation constants are laws, and the player item's
194 KB/item is two array-builds plus small calls. Reproduced from the clean tree (runner's
`regen.sh`, exit 0; every dossier number regenerates — A1 193.4 KB/item, 3.7 KB/ship-item,
11.35 KB/kick; A2–A5 within 0.3%, the pre-declared cadence jitter) and re-derived
independently from the raw logs (rung starts 2.07→1.03 at the cap; capped ladder 108.8 KB ≈
1.9× top; small calls 57.4 KB). My adversarial arms: the law holds at 3×10⁵ (195.1) and at
seed 3/10⁵ (199.4); the ship per-kick marginal keeps RISING (3.88 KB/kick at 3×10⁵ → band
top 54%, not 42%); burn reads 311 KB/item (coast-scoped). Adoption cost zero, no decision
changed — the run hardens evidence, it does not move a bottleneck 10× or delete a part.

**Reasons.**
- **Reproduction.** `regen.sh` (runner) exit 0; regen.log matches the dossier table digit for
  digit except flight-jittered counts (A1 kicks 107,965 vs the author's 108,282, 0.3%;
  control band was 5%). I recomputed the whole census from `data/A1.log` with my own parser:
  193.4 KB/item, 70% >2KiB share, 57.4 KB small calls, rung starts 2.086/2.077/2.069 at
  rungs 1–3 and 1.032/1.030 at rungs 4–5, capped-ladder sum 108,847 B — the "two
  array-builds" arithmetic closes (109 + ~23 + 57 ≈ 193 KB).
- **Predictions.** `predictions.md` predates the decisive arms (file order in the folder; the
  Outcome section is appended, the letter intact). P1–P5 held, P6 half-held, all disclosed in
  the dossier itself. No kill bar fired; none should have.
- **Adversarial arms** (mine, `/tmp/chk5f76/`, same instrument and args):
  1. **B1 — the next K decade, outside the author's range** (K=3×10⁵, seed 2, coast): player
     195.1 KB/item — the K-flat law survives its fourth decade (+0.7%); top mean 57,341 ≈
     57,344; but ship reads **3.88 KB/kick** (from 2.99 at 10⁵) — the rise the author flagged
     as "one point of curvature" continues, slope ~K^0.3, decelerating. Re-based 10⁹ top:
     8.4×10⁶ × 3.88 KB = 33 GB/s = **54%** of 60 GB/s, not 42%. Still closing; no saturation
     measured. Page corrected in place.
  2. **B2 — fresh seed at the top rung** (K=10⁵, seed 3): player 199.4 (seed-3 level, as at
     10⁴); ship 3.11 KB/kick — the K-rise reproduces across seeds; rung structure identical.
  3. **B3 — the burn regime** (K=10⁴, seed 2, `burn`): player **311.3 KB/item**, realloc
     92%, ladders running past the 56-KiB cap out to **3,670,016 B** — 8994's rare burn
     chains reproduced to the byte, and the coast scope of the law drawn exactly. The author
     never flew burn; the page now carries the scope.
- **Novelty.** The current page's od 6(c) asked verbatim for "one more seed before the 194
  KB/item … constants are cited as laws" — this run is that, plus two refutations the page
  lacked (the singular "56-KiB pull ladder" reading; the "1.6 KB/kick" flat constant). Not a
  repetition. HISTORY's allocator entries are the work-scheduler design, unrelated.
- **Goal fit.** Budget-1e9's memory/bandwidth row. "Measure before claiming" — a constant
  cited at 10⁹ now has three seeds and four decades under it. No engine change (PRINCIPLES:
  the instrument is env-gated, off = shipped bits).
- **Why not gold.** No 10× move, no component deleted, no premise killed: both decision rows
  the run supports ("no pooling subsystem mandated"; "player term negligible at 10⁹") stand
  exactly as 8994 left them — this run hardens their base. 8994, which resolved an
  attribution artifact and re-based the row, earned silver; a confirmation-and-decomposition
  step on top of it cannot earn more. The "two array-builds" mechanism is a rung-multiplicity
  count, honestly hedged, but still unnamed.

**The one experiment that would make it gold.** The backtrace that names the two arrays
(od 6(a)'s residue): it converts the census count into a deletable target — `with_capacity`
on two named sites, deleting ~0.3–1.2 M realloc calls per flight (a measured deletion, and
half the player term), with the ship marginal's saturation arm (K=10⁶) folded into the same
flight to pin the 10⁹ row's top.

**What the author missed.**
- The next decade was one 35-s flight away and moves the cited number: the band top is 54%,
  not 42%; the caveat "one point of curvature" understated a still-rising trend with less
  than one doubling of headroom to 100% (7.1 KB/kick at λ = 8.4×10⁻⁵).
- The burn arm (one flag) bounds the law's domain and reproduces 8994's 3,670,016-B chain
  terminus — strong free evidence left on the table.
- A fresh seed at the top rung (B2) would have shown K-flatness is not seed-2-specific.
- `analyze.py`'s `calls/item` display field has an operator-precedence bug
  (`allocs + reallocs/items`); display-only, no dossier number rests on it, but it will
  mislead a future reader.
- The dossier's "A1 reproduces D1 to 0.1% on kicks" is the best of three flights (re-flights
  read 0.3–0.4%); inside the declared control, worth citing as a band.
