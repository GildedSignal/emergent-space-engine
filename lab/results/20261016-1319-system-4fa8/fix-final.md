Working...
Fixed and verified end-to-end: regen.sh now runs to DONE in 484 s (well inside the 15-minute budget), regenerating every dossier number — the one-line bug was `env "${envs[@]:-}"` passing an empty-string argument for no-env arms (`env: '': No such file or directory` → exit under `set -euo pipefail`), replaced with the empty-array-safe idiom `env ${envs[@]+"${envs[@]}"}`.

Verification of this full pass (flights + digests, exit 0):

- **Every deterministic number exact**: all ten table rows (240/146/11111…; 52/27/15596…; 334/136/22219…; 52/24/26670…; N=0 51/36/6011 and 44/13/5827; N=600 240→50; N=10⁴ 240→50/27), the envelope (`212 240 207 251 229 195 334` → `52 27 26 12 13 13 12`), incremental rates past 1,900 s (3.17 vs 3.16), kicks +0.6% / boundaries +0.5%, and every digest hash (OFF `6895ce06…` = pristine bit for bit with kicks 3,767 = 3,767; chain `27d28007…`, stagger `de3c14c1…`, chain+stagger `a5e2bcde…`, all 13 cases "4 schedules agree" — the author's own digest_off.txt had been a truncated 12-line pass).
- **Wall-clock only varies as the dossier's "ms are box-relative" caveat anticipates**: total engine 2,556.0 → 2,307.9 ms (−9.7% this pass vs −11% recorded; shared-box load inflates both arms).
- The `thread 'main' panicked … Broken pipe` line is the pristine control hitting SIGPIPE after `head -1` (guarded by `|| true`); its control line printed correctly first. The N=0 flight files, absent from the author's record, now regenerate too.

Claim: the locals'-comb run's record regenerates — regen.sh's empty-env invocation is fixed and the full regeneration reproduces every number in the dossier, with digests bit-identical to pristine main.
