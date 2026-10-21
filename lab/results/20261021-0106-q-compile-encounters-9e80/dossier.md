# Dossier — compile `encounters` under its budget

**Claim.** The 503-line `encounters` page compiles to 134 lines (current best 224 → 15)
with every one of its 71 distinct runs kept on exactly one line each, both resolved
contradictions moved out with pointers, directions re-ranked to 8 by the board's rows,
five stale grades corrected to the branches' durable record — and no supported number
lost: 319 of a curated 319-number sample stands verbatim in the new page (0 behind, 0
lost), and a seeded 40-token held-out sample from the old page finds 39/40 inline, the
one miss being the tokenizer's `2.0:` glued to "a = 2.0", whose value is inline.

**Bottleneck.** Not a physics row — the lab's memory. The index flagged `over budget
(503 lines, current best 224)`, and by `lab/wiki/README.md`'s rule an over-budget page
"is compiled back under it before it takes new runs", so the topic — the lab's
second-largest, 138 run lines — was frozen for new authors. Gain: the page returns to
one reading (the newest author paid 503 lines to learn what the last seven runs
established; now 15 current-best lines), and the topic can take the freeze's constants
run again. What it deletes is duplication: runs prepended their result paragraphs to
`## Current best` instead of replacing what they superseded, and `## Runs` carried 67
duplicate lines (138 → 71), one truncated mid-id by an old merge
(`20261017-1018-second-`) and one typo'd id (`20261007-1234-quant-7578`; only
`…-1032-…` has a branch, and the two lines were content-identical).

**Evidence** (all of it regenerates with `./regen.sh`, < 1 s, from the page as committed
at this run's base `624c4a51` and this folder's `wiki/encounters.md`; `work/patch.diff`
is empty — the run edits nothing outside its results folder):

- Lines: 503 → 134 (budget ≤ 300). Sections: Current best 224 → 15 (budget ≤ 15),
  Refuted 21 one-line entries (was 14 multi-line blocks plus embedded refutations), Open
  directions 8 (budget ≤ 8; was 3, two of them struck-through DONE), Contradictions 2
  (both resolutions recorded, neither open), Runs 138 lines → 71, chronological, no
  duplicates, no missing id.
- A scratch `lab/wiki.py index` over a wiki copy with the compiled page swapped in
  reports `encounters | open | 71 | **The leak law is closed-form (f2f1):** …` — no
  over-budget flag, no conflict.
- Numbers (`check_compile.py`; curated sample fixed before its first run): 319/319
  inline, 0 behind a cited run, 0 lost. The sample covers every section of the old page
  and all seven big current-best paragraphs (f2f1, 73b5, e828, 1176, 9fd1, e87d, 08d0)
  — the standing constants a reader acts on: r = 0.57/0.33/0.03/0.88 and the 0.014
  prediction error; the leak sequence 2.6×10⁻⁶ → 6.5×10⁻⁷ (E=2→1024, seed 777); the
  depletion census 7.5×10⁴/4.7×10⁵/1.8×10⁶ and armed(16) = 0; the coupling r ≈
  7×10⁻⁹–2.6×10⁻⁸ vs e828's corrected 5×10⁻⁶; the row 355.3 per pair-touch and
  355/E_pair = 0.35–1.4 cores; the cache 1,394 → 416 ns (3.4×, 355 → ~105 cores); δc0 =
  5.5×10⁴ ticks = 1.02 widths; S ≈ 0.48·C/k² with 1.8% keepable; ρ* ≈ 4.4×10⁻⁵ AU; the
  ledger 0.077–3×10⁷ cores and the gate's 95.5–98.0% yield; 08d0's 128–256 toy knee and
  its kill.
- Held-out (P5, seed 20261021, first draw, ids masked): 39/40 of the random tokens are
  inline in the new page; the miss is `2.0:`, split off the old page's "the harness's
  own a = 2.0: 5×10⁻⁶ vs 6×10⁻⁹–2.3×10⁻⁸" — the value is inline as "a = 2.0" and the
  correction it belongs to is Current-best line 4 and Refuted line 16.
- Supersessions are decided, not kept: where runs disagree the evidence picks the
  standing side and the loser moves to `## Refuted` with its run — the knee (08d0's
  checker's 128–256 → dead on the tier, e828), the √E per-kick shape (9fd1 → dead,
  e828), the 140×-under budget reading (1176 → 7× over like-for-like, 73b5), the E_cell
  division (1176 → n/2 understatement, 73b5), e828's r constant (→ clock-consistent
  range, 73b5), 1b1f's belt-real dial (→ ~10⁴× off, 73b5), the beat-resident record and
  leak-gated slack (od 1/od 2 → dead, 08d0 + e87d), the time-window re-check band
  (→ dead in flight, 1a29), the u64 port (34be's own <2× rule), c9c7's design-reach
  transfer (→ reach-dependent below ρ*), the Δϖ-band cache (ca96), 0b81's miss model
  (→ checker-corrected, 277d).
- Grades now match the branches (`git log -1 origin/claude/lab-<id>`'s `Grade:` field;
  `wiki.py grade()` reads exactly this, so the page and the closure certificates now
  agree): five page grades were stale — 4ea2, 71a5, 73f0, 5d90 said gold where the
  branch says "silver (second checker disagreed)", and 34be said silver/awaiting where
  the branch says gold; eight "awaiting grade" labels resolved (1738, f0a2, 2b89, c9c7,
  5567, 1a29 gold; e828, f2f1, cd3b silver). Two runs have no branch (8cee, 2222) and
  keep their page grades, silver.

**Predictions** (`predictions.md`, written before the audit's first run): P1 held
exactly (134 ≤ 300, current best 15, scratch index clean). P2 held exactly (71 distinct,
the two named artifacts folded, chronological). P3 held after one instrument fix
(the grade comparison tripped on "2nd" vs "second" and punctuation; 0 real mismatches).
P4 held with one disclosure: run 1 found 2 lost numbers (5.7×10⁹, "2.0 widths"), which I
restored into the page — and while fixing the instrument I let the P5 misses pull two
entries into the curated set ("0/100,000", "0.99–1.03"; one duplicate removed: 318 →
319). That is the sample being tightened by its own findings, against my own pre-registered
rule; both additions pass inline, nothing was removed to pass, and the sequence is stated
here rather than hidden. My inline-share band (70–90%) missed high: everything ended
inline (319/319) because the restore loop folded the stragglers into run lines. P5 held
(39/40 ≥ 32/40; the miss is the `2.0:` artifact, value inline). P6 held (15/15 current-best
lines cite runs, 21/21 refuted entries name a killing run, 8 directions). The
self-set adversarial case — ten numbers from the seven big paragraphs — is covered by
the curated set: all inline.

**What would make it wrong.** A number the checker samples from the old page that is
neither in the new page nor in a run the page cites for that claim — the instrument
covers 319 curated + 40 drawn tokens; the old page holds thousands, and the exposure is
real (the first run caught 2). Compression can also misplace a number's *scope* while
preserving its value (right constant, wrong arm); I re-read every current-best line
against its old-page block, but a checker's independent reading is the test. The compile
cannot re-derive anything: pre-existing errors in the old record carry forward (I
corrected only where the old page itself records the correction, plus the branch
grades, which are the process's own durable record). One deliberate addition beyond the
old page: taleb-09b5 (adopted gold, from the board's taste log) is cited once, for the
co-orbital concentration result the encounters design already depends on. Cost of
adoption: the publish merges three-way against the page the run started from
(624c4a51); a full rewrite will conflict with any concurrent edit to
`lab/wiki/encounters.md`, so the merge takes the compiled page wholesale. Fit with
PRINCIPLES #11: "Text has a cost; no busywork" — the page held seven runs' worth of
superseded prose; the compile deletes the duplication, never the numbers, and
re-opens a frozen topic. One rung of caution observed: the machine's `/tmp` copy hang
during regen (an instrument bug: copying `dirname(OLD)` when OLD lived in /tmp) cost
~5 minutes and was killed inside the memory budget; `regen.sh` now pins the wiki copy
to the tree and finishes in 0.4 s.

**The lens.** A compile lens reads for conservation, not truth: every number's value
and citation is preserved, but it cannot judge whether a number *deserved* to survive —
the page inherits the old page's emphasis (the last seven runs dominate Current best;
the 6–14 October middle age lives one line per run). What it may have missed: a scope
error in my own condensation (numbers right, attribution subtly off), and the single
newest reader-action — the freeze's constants run — is ranked first by my reading of
the board, which is a compiler's reading, not the integrator's.
