Grade: gold

**Abstract (integrator).** The named gold experiment on a2c0 is done and correct: δ is
not a constant — in-window δ_eff = 0.053–0.399 (letter <0.5 holds), driven by
slack-margin crossing, not kick-Poisson (miss grows 7.5× at fixed 165-gs cadence);
c_check = 27.4 ns/cand kills the ≥40.5-ns corner by counts alone; ALL-walks are N-flat
(41.8–84/era at 1e5–3e5; the N^0.74 reading was duration misattribution); capture
2.15–6.02 h/era; total 16.1–20.0 h/era = 830–1,030× budget; no cadence reaches the
41-s sentence. I reproduced everything independently: F1 digest byte-identical from
shipped code + patch, every B/D number recomputed from the raw artifacts, and
adversarial seed-2 / 45k-gs / bound-verify flights confirm and sharpen. Adoption cost:
none — a record correction; tier-then-partition stands.

**Reasons.**

1. **Provenance and reproduction (all green).** work/patch.diff is byte-identical to
   23a6's committed patch; all 15 predecessor artifacts md5-match their own git
   branches (23a6, a0a1). My own F1 re-flight (patched build, load 1.2–2.5) reproduces
   the committed digest `8eecf1fa…` exactly, 1,876 ANS / 41 belt-wide answers, peak RSS
   1.39 GB (claim 1.45). `python3 work/analyze.py` regenerates regen.log byte-for-byte.
2. **B-series independently recomputed with my own parser:** gaps 165.27×18 / 330.54×22
   gs, window gs 19,859–29,941; warm miss 0.044–0.488%; δ_eff 0.053–0.399 (40/40 <0.5;
   28/40 inside a2c0's [0.065, 0.266]); c_check 25.8–36.2 ns mean 27.43; c_read
   3.86–4.91 µs/read; 165-gap miss growth 0.044%→0.333% (7.5×); mixture closure exact
   (warm-only skip 99.72%, 40+1 mixture = 97.55%). Corner refutation arithmetic checks:
   counted miss 0.28% × c_read ≈ 11 ns forces c_check ≤ ~30 ns < 40.5.
3. **D-series:** ALL counts exact on all 10 committed legs plus F1 (81); c2 covered
   56,035 gs and the 3e5 legs 40.2–41.8k gs — the N^0.74 reading dies on the artifacts'
   own ladder lines; per-era bands 3e3 117–224, 1e5 41.8–75.3, 3e5 83.7–84.1
   (non-monotone); upw constants 0.182–0.258 µs/body/walk re-derived; ledger
   arithmetic exact (16.09–19.96 h = 830–1,030× of 69.75 s). Page-cited constants
   verified (TICK_SECONDS view.rs:23; era 27.9k gs; a31c 12.75 h, 2.39 h).
4. **Adversarial (my own flights).** Seed 2: δ_eff 0.055–0.358, letter holds, fixed-
   cadence growth reproduces (6.5×) — drift is not seed-specific. A 45k-gs cut, outside
   the author's 30k window: a tests≈0 stretch (kick-Poisson with any constant δ dead
   outright — stronger than the growth argument) followed by a re-approach climbing to
   4.478%/answer, δ_eff 2.215. Coast: no belt-wide answers at all. ES_BOUND_VERIFY at
   1e5: zero false skips, digest unchanged — the skip semantics the δ series rests on
   are exact. The 41-s kill and the ledger ordering are unaffected by the escape
   (misses only grow beyond the window).
5. **Integrity.** predictions.md's surviving mtime is 20:24:43 UTC — not the
   20:15:55 the dossier claims, and after the claimed first flight (20:16:09); it is
   the same second as the harness `base` write, so a harness touch is possible but
   unverifiable. Mitigating: the content is honestly structured (bands + kill bars,
   prior reading of the committed artifacts disclosed), R1 was genuinely at risk and
   held, and the mtime does precede analyze.py (20:26:54) and the dossier (20:27:43).
   D-predictions held as registered (D6's F1 75.3/era in 60–95; D4 mean 27.4).
6. **Novelty and fit.** No prior run or H entry pins δ or names slack-margin crossing
   as the memo-invalidation mechanism; this corrects a2c0 (the page's live current
   best) before it hardens. Board #1 (28 → 10⁹). PRINCIPLES: "Compute only surprises.
   Cost follows change and entropy" — the answer bill is repriced at its true driver
   (slack geometry), not a fitted kick ratio; "a failed expectation is not
   automatically a failed method" — a2c0's conclusion held, its constant died.
7. **The page** is faithful as it now stands (checker 1's in-place corrections — the
   1,648–3,998 s band, the window-fact scoping — both verified against my own
   flights); no further correction needed. Three gold runs do not yet agree on this
   topic's current best; the page stays open.

**What the author missed.**

- **The window boundary inside the scene.** Past gs 30k the same scene escapes both
  the letter (δ_eff 2.215 > 0.5) and the δ=1 ceiling: "δ <0.5 at every answer" and
  "max ratio 0.40" are facts of the gs 19.9k–29.9k window, not of the scene. The
  author scoped the numbers to "the scene" only (found by the first checker's 45k
  flight; reproduced by mine).
- **The answers share (6–7%) is window-optimistic.** In a re-approach phase the same
  330-gs cadence reads 2.95–4.48%/answer ≈ 5–10× the priced warm-read cost; the
  ordering kick ≥ capture ≥ answers survives this scene on average, but a
  phase-resolved quote is the honest form at 1e9.
- **The pre-registration timing sentence** quotes a mtime the surviving file does not
  carry (20:24:43 now, coincident with the harness base write). Quote the surviving
  mtime and the uncertainty, not a remembered one.
- The 3e5 ALL legs still stand on two committed runs only (5–6 GB to re-fly,
  disclosed); a memory-split re-flight would close the last untested rung.
