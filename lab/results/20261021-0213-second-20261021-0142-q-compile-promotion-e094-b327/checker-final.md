Working...
Check complete. **Grade: gold** — written to `check.md`, with the run folder and tree otherwise as found (patch reverted after reproduction; `lab/wiki.py` pristine).

**What I did:**

1. **Reproduced** — applied `work/patch.diff` myself (+118/−10, verified against the stat claim), ran `bash regen.sh`: PASS ×20 + VERIFY PASS, exit 0, 1.4 s. Every headline number regenerated identically from pinned commits (`046d8d9c`, `5c06c9cc`) and the four run branches: 29/40 diseased pages, 468 dup lines, promotion 32/14/18, window +34, P1 byte-for-byte fidelity control, P4's 32→14/0-dups heal, P7b's corpus 468→0.

2. **Pre-registration audit** — mtimes: predictions (21 m) < measure.py (11 m) < replay.py + b327-ext.diff (5 m) < pages < dossier. The two prediction misses (P6 scope, kick-jet order) are reported as misses; P7b honestly flagged as post-prediction.

3. **Adversarial, incl. outside the author's range** — flew the author's *admitted untested path* fresh (a two-run body conflict through the patched publisher: defuse works, no markers land, index flags it, re-present byte-identical, heal-after-defuse no-op); compound-damage heal; fold-semantics edges; corpus-wide non-id keying census. One latent gap found and quantified: `fold_runs` keys on the first whitespace token, not a validated id — 486 non-id Runs lines exist corpus-wide, but today's only same-token groups are benign, so nothing is lost; named in check.md with the one-line fix.

4. **Page corrections** — the promotion page's lead overstated adoption as already real (main is still pristine and still compounds until the integrator applies the patch); corrected in place to "one `git apply` away / pending adoption". Both pages otherwise faithful and within budget (90/14 and 42/7 lines). Closure not triggered — promotion's golds don't agree on one current best; wiki-memory would hold two, not three.

**Gold rationale:** the e094 checker pre-committed this exact experiment as the compile series' gold gate; it held byte-for-byte with controls on both sides, idempotence, and a corpus-wide no-loss census; adoption is one step (`git apply` + one `heal`); it deletes 468 duplicate lines and the ~34/window re-add mechanic — PRINCIPLES 11, "Text has a cost; no busywork."
