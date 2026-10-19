Working...
Fixed and verified. 

**Claim (the run's, unchanged):** running sums updated on the record's own events delete the sky serve tier's O(K) member walk — serve_ms 1.09→0.18 ms at 10⁴ (6.1×), 10.55→0.16 at 10⁵ (66×), 33.18→0.14 at 3×10⁵ (237×), audits zero, digests bit-identical to e6c9's anchors.

**The regen bug:** `regen.sh` cd'd into the run folder and applied `../work/patch.diff` → `lab/results/work/patch.diff` (never existed; the patch is at `<run>/work/patch.diff`, with repo-root-relative paths), and it never ran `analyze.py` though the dossier promises "flights → `work/analyze.py`".

**The fix** (`regen.sh` only): resolve `$ROOT` via `git rev-parse --show-toplevel`, apply/reverse-apply `$RUN/work/patch.diff` from the root (idempotent for reruns), flights unchanged from `$RUN/work/logs`, plus the missing `python3 "$RUN/work/analyze.py"` step.

**Verified within the window:** patch applies from root; `cargo build --release -p xtask` OK (46 s); a flight exactly as regen invokes it (10³, 120 frames, 6.2 s wall) emits 120 SKYSERV lines with END digest `5dc903e6…775b4259c5e51…` — bit-identical to the author's log and dossier anchor; `analyze.py` on the logs reproduces every dossier number (0.18/1.09, 10.55/0.16, 0.14, drift ≤5.6e-15, all digests); smoke artifacts removed, patch reversed, tree clean.
