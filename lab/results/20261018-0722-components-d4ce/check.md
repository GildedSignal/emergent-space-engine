Grade: silver

**Abstract.** Claim: `fast_quad`'s four per-node wide `u128/u128` divisions are exactly
replaceable by `div_word`, bit-identically, buying ~5% of strong compiles (not od 7's ~25%).
The exactness reproduced completely and beyond the tested domain: 75 tests in debug (asserts
live) and release, ~50k bank rows with 0 non-timing diffs (`.c` and `.q`, all ten rungs),
N=3000 digests equal to the record, plus checker additions — 180 dense near-separatrix keys
in the unflown `word_root=false` band, the `N=1000 belt crossing` digest, a site-shape
boundary sweep, and a structural proof making exactness domain-wide. The magnitude did not
reproduce as a number: four passes span 0–15% (checker's clean drift-controlled triple:
p50 0.9%, patched arm 1–2% *slower* per panel; clean banks mixed). Adopt as a free exact
four-line cleanup; book no speed. Decisive prediction P3 failed (honestly reported).

## Reasons

**Reproduced (load-independent instruments).**
- regen.sh exit 0 (runner); I verified its stored artifacts myself: `digest_baseline.txt`
  ≡ `digest_patched.txt`, all five N=3000 cases × 4 schedules, digests equal to the committed
  record (`d2632de9…` in `artifacts/runs/nladder/ladder_digests_wave.txt`,
  `4995f384…` in `ladder_digests_newpop.txt`); all ten bank rungs identical in every column
  except compile-µs, in both `.c.tsv` and `.q.tsv` (the author only compared `.c`).
- `cargo test -p emergent-space`: 75 pass in debug (div_word's `debug_assert` tripwire live)
  and 75 in release — both re-run by me, plus the author's 2M composed-quotient sweep.
- Adversarial 1 (outside the author's domain): my own probe hashed full `Orbit::compile`
  Debug output over 180 keys at p = (6+2e)(1+t), t ∈ [3×10⁻¹⁰, 10³], e ≤ 0.99999 — the dense
  near-separatrix `word_root = false` band the dossier names as "the one unflown corner".
  Base ≡ patch on every key, no refusal drift.
- Adversarial 2 (outside the author's digest set): `N=1000 belt crossing`, 4 schedules,
  `ef19d3de…` — bit-identical.
- Adversarial 3: temporary crate test sweeping `div_word` vs wide division on the four
  sites' exact operand shapes at the precondition boundary (root ∈ (2⁴⁰, 2⁶²] dense;
  a·g ≤ 6·2⁶²·2⁵⁸; q≪62 quotients ≤ 2⁶²) — equal everywhere.
- Structural (stronger than the author's argument): on the *whole* compiled fast-path
  domain the shipped casts cannot truncate — the fast gate (delta ≥ 2³⁰) forces root ≥ 2⁴⁶
  (g ≤ 2⁵⁸) and a ∈ (0, 6·2⁶²) with a·g < 2¹²³ against ONE+root ∈ (2⁶², 2⁶³]; the join
  clamp keeps floor ≤ x on every walked node (ratio ≤ 2⁶²); the separatrix refusal
  (p > 6+2e) forces horizon > 2⁶¹ (rt ≤ 2⁶³). The author's "what would make it wrong"
  corner is structurally empty — they under-claimed their own proof.

**Not reproduced as stated (the magnitude).** The dossier's headline numbers (ns/panel
1216→1118, p50 5.3%; bank R4 29.9→25.4, G24 928.8→722.5) come from the author's own passes,
whose CSVs/TSVs were overwritten in `work/` by the runner's regen — the stored pair reads
p50 9.3%, ns/panel 1373→1165 (−15.1%), banks 10/10 faster. My clean pass (nothing else
running; BASE→PATCH→BASE with a −0.3% base-vs-base drift control) reads probe p50
0.8–0.9% and the patched arm 1–2% *slower* per panel; my clean strong-rung banks are mixed
(G24edge −1.3%, G24 +0.1%, R4 +5.9%). Four passes of the same paired instrument therefore
span 0–15% with the sign unstable on a quiet box. The claim's core — far under the micro's
~25%, the division slice dead as a compile lever — survives every pass; the number "~5%"
does not. The wiki page also overstated: "weak/Taylor rungs R2/R5 unchanged" is contradicted
by the stored pass (R2 −10.8%, R5 −5.3%); I corrected the page in place.

**Predictions.** P1 (exactness) held — and is now structural. P2 held in direction (Δ
24.5–52 ns loaded; ~0 clean: the out-of-order-overlap reading holds to its own limit).
P3, the decisive one, failed (15–40% predicted, 0–15% by load measured) — honestly reported
by the author, with the right lesson (the isolated-op sum is the wrong cost model for a
pipelined node). P4 held. Gold requires the held-out predictions to hold; P3 did not.

**Novelty.** The published read-stream page's open direction 7 was exactly this change,
"found and micro-measured, unflown"; no HISTORY entry covers `div_word`/`fast_quad`. The
run flies it, closes the direction with an in-situ answer, and supplies the exactness
proof od 7 lacked. New work, not a repetition.

**Goal fit.** Board bottleneck: the kick (compile = 49% of the fit stage sum, d399). The
run does not move it 10× and deletes no component; its value is a premise kill (od 7's
arithmetic-width lever) plus a certified free cleanup, redirecting the floor hunt to the
node's remaining ~280 ns and the shape-class memo. PRINCIPLES 1: "The cheapest compute is
compute not done" — here the reading deletes a planned optimization; PRINCIPLES 16:
"it's about what's cheapest to compute" — measured, not assumed. "Measure before claiming"
was respected; the magnitude instrument lacked a drift control, which is why the number
escaped.

## The one experiment that would make it gold

An interleaved-arms paired measurement (base/patch alternating per key or per rung, not
per whole pass), CPU-pinned on a quiet box or the M1, putting a confidence interval on the
in-situ Δ per node. A stable positive (≥5% of strong compiles) lands the claim's number and
this becomes a gold premise-kill with a free certified patch; a stable ~0 makes the
refutation total (the four divisions were never a lever at all) — also gold as a closed
answer. Either outcome fixes what today is an unfixed number.

## What the author missed

1. Their exactness argument is stronger than they claimed: the "one unflown corner"
   (delta < 2⁶²/4) threatens only `num::isqrt`'s cost, not these four sites' preconditions —
   both root branches keep root ∈ [2⁴⁶, 2⁶²], so the replacement is exact on the entire
   compiled domain by structure, not by sampling. The run under-claimed its own certificate.
2. The timing instrument had no drift control and sequential whole-arm passes on a shared
   box; worse, the quiet-pass artifacts were overwritten by regen.sh writing to the same
   paths — the headline numbers are not regenerable from the run's own folder (the exact
   "numbers the shipped code cannot regenerate" trap the lab README names).
3. The page's "R2/R5 unchanged" and the precise 5.3%/−8.1% were stated as stable facts;
   four passes disagree. Corrected in place.
4. P2's lower bound (40 ns/node) excluded the true quiet-box answer (~0); no prediction
   registered the possibility that the in-situ cut vanishes entirely.
