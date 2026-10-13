Working...
Run complete. Deliverables in `lab/results/20261013-0037-components-009b/`: dossier, predictions (pre-registered), regen.sh (verified end-to-end: 3× DIGEST_MATCH, all suites 0 failed), wiki page for kick-jet, patch and probe example.

**Claim:** the shipped `bind` chose the integer word from the *compiled* entry, so every word transition compiled a full trajectory and threw it away (5–6% of binds but 14.5–18.2% of bind time — transitions are the leaver-class binds, 278–310 µs discarded each); the word is a function of the fit's key alone, and choosing it before the compile (`fit_of`/`from_fit` split + `word_of_key`, ~60 lines) is bit-identical on all three probed scenes and cuts total bind time 12.9–17.5% digest-identically.
