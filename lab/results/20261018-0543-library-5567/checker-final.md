Working...
Check complete. Verdict written to `lab/results/20261018-0543-library-5567/check.md`: **Grade: gold**.

**What was verified:**

- **Reproduction** — author's flight JSONs match the dossier table exactly; runner's regen exit 0; `predictions.md` (05:49) precedes every flight (05:51+). Counts wobble ±5 (decision-tick), disclosed; rates hold.
- **Code anchors** — all six verified in-tree: `frame.rs:37` (epochs/period 1,600–3,200 is a construction invariant, `ω·E ≤ 2⁻⁸`), `frame.rs:80` (`r_p/32`), `universe.rs:513` (one-fleet assert), `:733–737`, `:787–796`, `fleet.rs`. Patch is one inert-unset env-gated clamp. The scene generator (`scenes.rs`) confirms the dissolution edge is geometric (extent ∝ √m at fixed density).
- **Premise** — read cf2a's branch: the 4,510-core fleet row is real, and cf2a's checker explicitly named this exact experiment as the missing arm. Novel: no page or H entry prices the frame route.
- **Attacks (8 flights)** — flew the author's *named but never actually flown* held-out case (their m3072 died on an unbuilt binary): m=6,144 holds, exponent **0.714** across ×128 members, per-member rate falls 0.89→0.22 µs (the 0.89 anchor is the worst arm — conservative), extent gate sheds overflow as leavers, no quadratic onset. Third seed (3) reproduces.
- **Two flaws found, neither fatal:** the "~0.8 cores" batch term is 10³× its own printed factors (slip, conservative direction); and the contact flow is period-independent (epoch scaling discounts kicks, not battles) — but even the absurd all-battle bound composes to ~220 cores, still 20× under the row.

Corrected the proposed page in place with a bracketed checker note (slip, domain extension, contact-flow caveat), left topic `open`, and restored the tree (patch reverted). Gold rationale: a premise kill on 99.77% of the encounters ledger's dominant row, measured on shipped code, adoptable as three wirings plus a birth rule — no new finder.
