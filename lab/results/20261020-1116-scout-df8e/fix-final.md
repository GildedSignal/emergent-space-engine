Fixed. The `regen.sh` is fixed and verified: the failure was a wrong checkout-depth assumption (`cd ../../../../..` landed outside the repo, the build error was piped into `tail` so `set -e` missed it, and the relative `$R` sent flights and `analyze.py` to a bogus path) — the rewritten script walks up to `Cargo.toml`, uses an absolute run dir, resolves the binary from cargo's own build JSON, fails loudly on build errors, and inlines the analyzer; tested end-to-end at a two-levels-deeper path with the patch applied (3m11s, all five flights), it regenerated every dossier integer — crest bin 14,250 gs in every arm, peak/mean 7.57–7.62, busiest-29% share 0.75, events/body 4.486–4.490, four standing eras — with the tree restored clean afterwards.
 is parsed from cargo's own
  artifact record (no hardcoded CARGO_TARGET_DIR — this box sets it, the checker's may not),
  and a build failure now aborts loudly instead of piping into `tail`;
- the analyzer is inlined (`<<'PY'` heredoc, code identical to analyze.py, which stays for
  individual use), so regen is self-contained.

Verified end-to-end at a path TWO levels deeper than the run folder, patch applied:
root found, binary resolved, 5 flights + analysis in 3m11s. Every dossier integer
reproduces: crest bin 14,250 gs in all arms (the kill claim), peak/mean 7.57-7.62,
busiest-29% share 0.75, events/body 4.486-4.490, four standing eras, ev/frame max ~17k.
Test artifacts deleted, tree restored (`git status` clean apart from `lab/results/`).

Two notes for the checker:
1. `determinism on1==on2: False` contradicts no dossier number: P6 was reported "not
   flown", and it cannot pass by construction — the probe's CSV prints per-frame wall-clock
   ms, and the 12 ms budget shifts event counts per frame, so cross-process byte-identity
   is unattainable on a loaded box. The integer family (above) is the reproduced part.
2. First run on a cold target dir pays the release build (this test was incremental);
   regen now fails loudly rather than silently if that build breaks.
