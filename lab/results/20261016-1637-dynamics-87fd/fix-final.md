Working...
Fixed and verified. Two unbound variables were the whole failure: `B` (the doll_probe binary) and `R` (the flights output dir) were used at line 17 but never defined.

**The fix** (`regen.sh` only):
- `B` is now derived from `cargo metadata`'s `target_directory` + `/release/examples/doll_probe` — hardcoding `target/` would still fail, because this workspace redirects cargo's target dir to `/home/glmlab/lab-target-1`. A `-x` guard catches a missing binary.
- `R` points at the run's `flights/` dir with `mkdir -p`.

**Verification** — full end-to-end run from the restored tree (patch re-applied, example rebuilt in 11 s, 5 flights in ~7 s, exit 0, prints "DONE"). Every headline number in dossier.md's table regenerates exactly: off s1 251/136 ev/fr, enc 183, kicks 7,736, drift med 2.0e−6 / p99 3.2e−4 / max 6.3e−4; chain+stagger s1 52/25, 184, 7,937, 7.4e−6; phase s1 53/25, 183, 7,928, 7.9e−6; off s2 274/140, 208, 7,939, 1.9e−6; cs s2 66/26, 210, 8,143, 7.1e−6; E₁ medians and r₁ = 1.179520e10 match to the digit; doll census {2: 310, 3: 3} = 313 in all arms.

Claim: regen.sh now regenerates every dossier number from the restored tree in under 30 s, bit-identical to the committed flights.
