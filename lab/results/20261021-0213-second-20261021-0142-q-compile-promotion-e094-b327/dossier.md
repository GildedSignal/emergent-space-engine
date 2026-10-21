# Dossier — 20261021-0213-second-20261021-0142-q-compile-promotion-e094-b327

## Claim

The e094 checker's named one-experiment-for-gold is done and the claim it
gated now holds on the shipped record: with the publisher's Runs union patched
id-aware (6ccc's flight-proven `fold_runs` + this run's skip-as-heal and
corpus `heal`, `work/patch.diff` = +118/−10 on `lab/wiki.py`), re-presenting
e094 through the real `apply` + `index` lands the promotion page at **14 run
lines, one per id, 0 duplicated ids, no flag, Runs byte-identical to e094's
compiled proposal, body untouched** — and the same one-sweep invocation heals
every page the 02:12 window compounded (promotion 32→14, budget-1e9 26→10,
cell-rebind 11→4, kick-jet 92→57), idempotently, with `wiki.py heal` clearing
the whole standing corpus (468 duplicate lines → 0, zero run ids lost).

## Bottleneck

Not a physics row: the wiki's own publish path. e094 compiled `promotion`
under budget (silver), but adoption was not real — the shipped `apply`'s
literal Runs union (lab/wiki.py line 129) compounded the published page to
**32 run lines / 14 ids / 13 duplicated ids** (measured at HEAD 046d8d9c, the
checker's exact numbers, now live on main), and the same 02:12 window added
34 duplicate lines across four pages (promotion 13, budget-1e9 10, kick-jet 7,
cell-rebind 4); 29/40 pages carry 468 in all. The gain: the dup-line disease
is deleted for every future compile (the fold lands one line per run at
publish), for every past window (the skip heals at the window's own next
sweep), and once for the standing corpus (`heal`) — what it deletes is 468
duplicate lines plus the re-add mechanic that grows them ~34/window.

## Evidence

`./regen.sh` (~2 s; `python3 replay.py` then `verify.py`) rebuilds every
number below from pinned commits (`046d8d9c829b` = the shipped record,
`5c06c9cc` = e094's base), the run branches, and the stored diffs
(`work/6ccc-fold.diff` verbatim from 6ccc, `work/b327-ext.diff`); it exits
non-zero on any failed assertion. Full record: `work/record.json`; 20/20 PASS.

- **P1 harness fidelity (control):** replaying e094's 02:12 publish (ours =
  its base's page, theirs = its graded proposal) through a *pristine* wiki.py
  reproduces the shipped `lab/wiki/promotion.md` **byte-for-byte** — the
  sandbox is the real publisher.
- **P2:** the shipped publisher, re-presented e094 on the diseased page, is a
  no-op: 32 lines / 14 ids / 18 duplicate lines stand (the disease neither
  heals nor grows).
- **P3:** 6ccc's patch **alone does not heal it** — its skip (87d0's
  anti-amplifier) no-ops an already-published run. This was the gap; hence the
  skip-as-heal: on skip, ours' Runs is rewritten with `fold_runs(ours, [])`
  (later wording wins, first-occurrence order, fixed point).
- **P4 — the named experiment:** patched publisher, re-presented e094, real
  `apply` + `index`: **32 → 14 lines, 14 ids, 0 dups**; Runs byte-identical to
  e094's compiled proposal; body byte-untouched; index row `| open | 14 |`,
  no over-budget flag.
- **P5:** a second identical sweep is byte-identical (idempotent; the fold is
  a fixed point, the skip still blocks the amplifier).
- **P6 — one sweep heals the window, not just this page:** staging all four
  graded 02:12 runs (the publisher's exact artifact: `DONE` = "Grade: silver")
  and running one `apply` + `index` heals every page that window compounded —
  corpus 468 → 392 dup lines; promotion/budget-1e9/cell-rebind land Runs
  **byte-identical** to their compiled proposals; kick-jet lands the same 57
  lines (set-identical) in the page's stable first-occurrence order — its
  compile had reordered the list, and fold order is ours', not theirs'.
- **P7:** folding every page's own Runs list clears 468/468 duplicate lines
  with **zero run ids lost** corpus-wide (every id token in every Runs
  section survives, range lines included).
- **P7b:** `python3 lab/wiki.py heal` (extended here to fold Runs as well as
  defuse markers) clears the standing corpus 468 → 0, idempotent, no ids lost
  — the 392 older dups do not have to wait for their topics' next runs.
- **P8 (control):** the patched `index()` on the untouched corpus is
  byte-identical to the shipped index — no regression (6ccc's claim, re-held
  at this HEAD).
- **P9 — the next real publish:** staging this run's own two proposed pages
  (mechanism replay; its DONE carries a declared hypothetical grade token —
  the publisher folds gold/silver only and this run's real grade is not yet
  written) lands promotion at 15 Runs lines (one per id, b327 added, current
  best 14 ≤ 15) and wiki-memory at one line per id (5, current best 7), both
  unflagged.

## Predictions

`predictions.md` was written before the replays (P1–P9 pre-registered; the
disease census 29/40, 468, 32/14/13 was measured before, as setup). Outcome:
**P1, P2, P3, P4, P5, P7, P8, P9 held**; P3's predicted gap is what the
extension closes. **P6 partially held, two disclosed misses:** (a) I predicted
"0 duplicated ids anywhere in the wiki afterwards" — wrong scope: one window's
sweep heals only that window's pages (468 → 392); the corpus-wide zero needed
the `heal` extension (P7b), which I built *after* seeing P6's honest scope, so
P7b is a post-prediction tool change, not a held prediction; (b) I predicted
each healed page "byte-identical in Runs to its own compiled proposal" — held
for 3/4; kick-jet is set-identical (order is the page's stable
first-occurrence order, not the compile's reorder).

## What would make it wrong

The fold keys on the **first token** after `- `, so a page whose one line
legitimately needs two lines with the same leading run id would collapse them
— no such line exists in the corpus (P7's id-token census proves the stronger
property: no id token disappears). The heal-on-skip writes ours' Runs folded
but leaves the body untouched, so a page whose *body* needs the run's newer
prose still waits for a real publish — correct (the skip exists to block the
amplifier, not to re-merge). `heal` rewrites pages in place: run it once, at
adoption; it is idempotent (P7b). Adoption cost: one `git apply` of
`work/patch.diff` (context: lab/wiki.py untouched on main since 2b394f70, so
it lands clean) plus one `wiki.py heal` for the standing corpus; no crate, gate
or docs change. Fit with PRINCIPLES: "Text has a cost; no busywork" (P11) —
468 duplicate lines are pure re-read cost on every author's wiki read; and the
wiki's own README rule the compile series serves ("an over-budget page is
compiled back under it before it takes new runs") is only real if the compile
survives its own publish.

## The lens

A second-author lens inherits the first checker's framing: it asked for the
skip-as-heal's exact behaviour ("preferring the compiled variant") and I
built to that letter, including its blind spot — byte-identity of healed Runs
is only meaningful when the compile preserves page order (kick-jet's doesn't;
set-identity is the honest invariant). What this lens may have missed: the
replays pin two commits and four branches; a *future* publish that conflicts
in the body (not Runs) still exercises 87d0's defuse path, which I re-tested
only through 6ccc's recorded claims (P8), not with a fresh conflicting
publish. And the mechanism replay's grade token is a prediction about the
publisher, not about this run's grade.
