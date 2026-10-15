Working...
Check complete. `lab/results/20261015-0724-components-e0f9/check.md` written: **Grade: gold.**

**What I did**
- **Reproduced from the record**: applied `work/patch.diff` to the clean tree at base `6067af6` myself (applies clean, 11 s rebuild); the runner's regen (exit 0, ALL ARMS IDENTICAL) matches the dossier's table arm for arm, including the 10⁵ anchor `2109a2e0…` with 273,200 demotions — b9ae's exact published count (verified against b9ae's dossier on its branch).
- **Four adversarial arms of my own, all beyond the author's domain** (N ≤ 10⁵, cut ≤ 48 k, seeds 1/7, coast@10⁵/burn@10⁴): N=2×10⁵ (`af43df43…` identical, rss 1,059→749 MB, −42 % B/body), 96 k cut (`e75c90f2…` identical — and equal to b9ae's independent build at the same cut), 10⁵ burn (`d3542eea…` identical), unseen seed 42 (`5ff9487e…` identical). Every law counter equal in every pair; the wall decomposition reproduces (machinery free, re-mints are the bill).
- **Code audit**: `release(u32::MAX)` is a genuine no-op; no `cat.get(key)` reader exists; `same()` is the scan memo only, so demotion degrades to answer-neutral memo misses; seam-off is value-identical to shipped, anchored by the digest chain shipped→760f→b9ae→this control.
- **Suite**: `cargo test -p emergent-universe` cannot link on Linux (shipped `nladder` example uses macOS's `proc_pid_rusage`) — regen.sh's suite line is inert here. With `--tests`: 18 binaries, 72 passed / 0 failed / 2 ignored.

**Corrections made on the author's page** (`wiki/nladder.md`): the "~64 B inline" demoted record is actually **104 B** (probe: key 56 + sense + unit 40 + discriminant; `Binding` 192→288 B); d7bc's standing current-best block (the `ES_SCAN_STANDING` fence) was restored after the author dropped it resolving the merge conflict; three pre-20261014 Runs lines restored (append-only violation).

**Named in check.md as missed**: prediction 6's "at 10⁴ the delta is lost in build noise" clause failed as written (×1.87–2.0 visible) while the dossier says "all seven held" — reporting flaw only; and contacts = 0 on every arm, so the encounter-memo identity path with demoted candidates has never produced a non-empty answer — a contact-rich scene with the seam on is the one open corner.

Repo tree restored to clean at base; nothing outside the run folder touched.
