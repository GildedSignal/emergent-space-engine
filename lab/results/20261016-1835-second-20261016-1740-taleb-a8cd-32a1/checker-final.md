Working...
Check complete. `check.md` written: **Grade: gold**.

**What I did and found:**

**Reproduction (the strongest form).** I found the tree genuinely clean (patch unapplied, HEAD `c9657cd1`, `git diff a523ace9 HEAD -- xtask crates` = 0 bytes) and ran the delivered `regen.sh` unmodified: exit 0, 266 s, step 0 "applied", every step non-empty and **bit-identical** to the runner's log (only step-0's line and one interleaved `ok` differ). All parent numbers reproduce: crossings vector, census 14/11/8 + musl 15/16, B12-false for Echo, #57 = 7016 kicks / `24.37109375` / `8.409466703853747e-8`, freeze control `c84f5787` bit-identical, +0 ulp vs CR. The parent's silver cause (vacuous regen) is closed.

**The named experiment verified with controls on both sides:**
- `crseeds.py` mirrors the Rust source exactly (checked line-by-line against `sample.rs:112-121`, `handoff.rs:57-60`, `restricted.rs:94-96`).
- Recomputed the CR table at **dps=120** (outside the author's dps=60): bit-identical, same sha — no tie exposure.
- **Perturbation wiring controls:** a flipped α bit trips the probe's own `draw alpha moved at rank 0` assert; one flipped seed bit of #57 moves the corpus *and* `j_run`(#57) to 7013 kicks / **3.697e-8 (pass)** — the probes can fail, so the 0-ulp/CR results are real comparisons, and the flip lands inside the parent's ±1 ulp scatter.
- Suite in my window: **203/8/21 in 503 s** — one fewer failure than the author's 202/9: the load tail wandering exactly as the dossier's load-class reading predicts.

**Page corrections (in place).** The "on every machine" portability claim now carries the residual the dossier discloses (`powf` in `period()`/`omega()`, absorbed ~6.4×10³ by the seed quantization — I sized it) plus my flip datapoint, in both the Current-best block and the [32a1] direction-4 line.

**Why gold:** the parent's silver had one cause and one named missing experiment; both are closed and independently verified (my own clean-tree run, not the runner's log), predictions were pre-registered (18:43 < 18:44 < all runs) and held — PC2/PC3 sharper than registered — novelty is clean (no HISTORY/wiki prior; the fix leg deleted by measurement), and it's adoptable in one step (freeze the assessed corpus fields). Left the tree, `regen.log`, and `cr_seeds.txt` exactly as found.
