Working...
Check complete. `check.md` written: **Grade: gold**.

**What was verified:**

- **Reproduction (fresh build):** applied the patches myself; every digest bit-exact — grid cells (m4/m400 at 0.2/5 ms), paced worst cell (`f5c0c9f7` equal across budget and pacing), and all four row-1 originals against `orig/` including a fresh rtf-300000 run (`475f4db2`). Numbers within shared-box scatter: prologue 15.4 µs vs 15.0; paced cell 5.16× vs 5.16×, 92% frozen, 40 jump frames of 1.29 game-s; e(B) 3.05/73.1 vs 3.09/75.7; cliff 21,631×→28.3× with T/D exact in every cell. `tables.py` regenerates every table.
- **Predictions:** `predictions.md` (19:27:16) precedes the grid (19:27:28); P1–P6 all held, partials disclosed in advance.
- **Adversarial:** 0.1 ms budget — no knee between grid points, digest unchanged; seed 2 — T/D exact, cliff not seed-1-specific; prologue scaling (raised the `--members` 400 clamp locally) — linear to 2,190 bodies at 90 µs, so the floor stays dead below ~5k bodies.
- **Named flaws** (none touch the result): `work/patch.diff` alone can't run the dossier's commands (missing `--coast` arm, lives only in `orig/patch.diff`, and the two won't stack — one-line union needed); the "293× the 5 ms/60 Hz budget" line is really 19.5×; "~29 ns/body" is 34.5 average / 35–50 marginal; the "load 0.18–0.25" claim is contradicted by the JSONs' uptime lines (0.53–2.1).

Gold rationale: it kills the silver's premise by direct measurement (no 0.2–1 ms prologue exists; "0.00×" was a median artifact over a 28.8× run-average), regenerates the record bit-exact with provenance fixed, and replaces the wrong gate with arithmetic the dashboard already has — adoptable in one step. Repo tree restored, only `check.md` added, nothing committed.
