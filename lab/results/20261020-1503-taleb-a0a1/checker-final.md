Working...
Check complete. **Grade: silver** — written to `check.md`, with the author's wiki page corrected in place.

**Reproduction:** every dossier number regenerates from the runner's regen (draw noise only: 125 vs 126 ALL walks, 91.7 vs 91.3 ms top, 299,717 vs 299,715 cand; b1 near-exact: 0.289 µs/body capture, 4.49 µs/body top answer, 97.2% read, belt-wide scan never answered). All code anchors verified verbatim: `SCAN_BACKLOG=2048` (universe.rs:79), admission `room < 2·max(scan_ns, 750µs)` (:1190) with 1/64 decay only inside answered scans (:1205), capture inside the player's item (:772), `radial.rs:254` bail at `bodies/4 + 64`, and `encounter.rs:58-60`'s "off the critical path" premise quoted correctly. Commits `ce694696`/`72b71c56` exist.

**Four fresh arms, three outside the author's grid:**
- **3e3 (below the grid):** filter still bails (0.242 µs/body — constant holds two decades down), and a full-doll belt-wide answer finally ran: 12.2 ms, read 97%, **skip 100.0% (2715/2715)** — the central extrapolation validated on the belt-wide object itself, above the claimed 99.8%. Lock-in threshold pinned: one answer > 6 ms ≈ 1.4k candidates closes the guard at *every* belt rung ≥ 3e3 (held_max 1,390 there).
- **Coast 1e5:** zero ALL captures (idx windows 5–208, held_max 181, channel healthy) — the bail is the in-belt burn regime, bounding the claim's domain as the dossier itself named.
- **Seed 2 unfenced (kill-bar draw 2):** no ≥300 ms single-answer frame; worst 854 ms = the comb; same constants. The author's sharpened reading (lock-in, not lump) is what happens: b1's last answer lands 28.6% into the flight, none after.

**Why silver:** the premise corrections are real and reproduce, but the deletion lever (carrying the bound) is named, not flown; the kill bar was left at draw 1 of 3; a1's 5,101 MB peak (over the 2 GB cap) is undisclosed; and the O(N) structure extends d7d1's bail-walk measurement, 1250's max-gated latch (scan-queue od 4), and 9ed1's checker's 4.2–4.4 µs/body without citing them — the page now carries those citations. Gold experiment: fly the bound with digest identity on the shipped tree.

Tree restored after the arms; my raw outputs kept in `work/` as evidence; nothing committed or pushed.
