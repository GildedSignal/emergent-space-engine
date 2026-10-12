# Predictions — 20261012-1904-q-wiki-handoff-40f6 (compiler run)

Written before the page `wiki/handoff.md` and the dossier are final. These are the
statements I could not settle by reading the abstracts alone; each is checked against
the branches in `verify.py` (re-run by `regen.sh`).

1. **The integrator's cluster grades are stale for exactly two runs.** Both
   `20261006-1738-b-kerr-compiler-fa4b` and `20261009-2348-scout-3851` are listed
   "(silver)" but their own records show gold from the first checker AND gold from a
   second checker (`-6586`, `-0d8c`), so by the two-checker rule they are gold. I expect
   no other listed grade to rise; `20261011-1729-scout-6765` stays below gold because
   no second-checker branch exists for it.

2. **Every one of the 13 runs has a branch**, including the "(missing)"
   `20261011-1102-autoresearch-11de` (its branch holds dossier and author/checker
   finals but no `check.md` — ungraded, not absent).

3. **At least four of the 13 runs belong to other topics** (kick cost attribution and
   the frame/calendar), by the scope of the standing pages `lab/wiki/kick-jet.md` and
   `lab/wiki/frame-cost.md`.

4. **No two runs in the cluster contradict each other on physics**, so the compiler
   rule holds and no probe is run: the only adjudications are within one run (18d2's
   P4 number) or bookkeeping (fa4b's grade line, ae29's empty patch).

5. **Adoption state on `origin/main` today**: `crates/space/src/kerr.rs` exists (via a
   commit whose message says "not reviewed, not merged") but without fa4b's 19-line
   guard; `shear_time`/`root_key` (root-clock keys) are absent; the shipped capture is
   still the changeover levels (`soi.scale(1 - LEVELS)`), not a single surface.

6. **Held-out for the checker:** of the ~50 distinct numbers the page quotes, every one
   appears verbatim in a `check.md` or `dossier.md` on a `claude/lab-*` branch; any
   number that appears only in an author dossier contradicted by its checker is quoted
   in the checker's corrected form (ecfd's 34–718×, not the author's 5–170×).
