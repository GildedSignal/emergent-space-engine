# Fix: regeFixed and proven: regen.sh failed because it applied `work/patch.diff` to a tree that already carried the run's edits (preimage/postimage mismatch, half-applied by `--reject`) and settled the rtf-100 arm at 8,000 instead of the dossier's common 40,000 game-s horizon — it now applies atomically with a restore-and-retry self-heal and settles all arms at 40,000, regenerating every dossier number end-to-end in 93 s (digests off=on `16096c78…`/`c264ab6a…`/`16096c78…`, census 0.710/0.563 with 0 conflicts, memo-on arm field-identical to the author's artifact, kicks 73,025/93,166/73,025), with only regen.sh touched.
 litter, and apply once more. Idempotent across repeated regens (exercised: the second
verified run began on an already-patched tree and self-healed).

**Root cause 2 — wrong horizon on the rtf-100 arm.** regen.sh passed `ES_DIGEST_GS=8000`
for the 1e4/100 arm, but every dossier number for that arm lives at the common 40,000
game-s horizon (the author's own artifact settles there: digest `16096c78…`, kicks 73,025;
the dossier's digest table and horizon counters say the same; 8,000 regenerates numbers the
dossier never cites). Fix: `40000` for all three arms.

**Verified** (`regen-verify.log`, from a clean apply): digests off=on at all three arms —
`16096c78…` (1e4/600), `c264ab6a…` (3e4/600), `16096c78…` (1e4/100, schedule independence);
census repeat 0.710 / 0.563, conflicts 0; memo-on rtf-100 arm field-identical to the
author's artifact (`calls=338747 hits=269738 stale=4 map=69005 repeat=0.796`); horizon
kicks 73,025 / 93,166 / 73,025; stage timings same orders (dossier scopes timings to orders
of magnitude on the shared box). Nothing outside regen.sh was touched.
