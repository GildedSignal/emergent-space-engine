Working...
Fixed and proven. The defect was one line: `cd "$(dirname "$0")/../.."` landed in `<repo>/lab`, not the repo root (the run folder `lab/results/<id>/` is three levels deep), so `$OUT` resolved to `lab/lab/results/...` — cargo survived by walking up to the workspace, only the `python3` paths broke. Changed to `../../..`.

Verification, exactly reproducing the runner's sequence (`git apply work/patch.diff`, then run `regen.sh` from an unrelated cwd, `/tmp`):
- Step 1 identity suite: 9 passed (526 s debug)
- Step 2 r5 rung: 10/10 rows (32 s release)
- Step 3 metrics.json regenerated, numbers identical to the author's stored values (identical_fraction 1.0 / 1.0 / 0.0, contacts_total 116874, covered 10)
- `verdict.py`: **PASS** (`cpu-pair` passes every criterion; negative control fails as required)
- Total 568 s, under the 15-minute budget; tree restored to pristine after the reverse-apply.
