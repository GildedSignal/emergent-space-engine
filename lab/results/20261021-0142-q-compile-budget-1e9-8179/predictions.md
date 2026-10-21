# Predictions (written before the audit run)

The decisive experiment is `audit.py` (the compile's verifier), not a physics run:
it re-derives the compile's own claims from the two artifacts (the old page as shipped
in the tree, `lab/wiki/budget-1e9.md`, and the compiled page,
`wiki/budget-1e9.md`). Held-out cases below were not measured when written.

## P1 — budgets (wiki.py's own counting)
- New page total ≤ 80 lines (expect ~71; old 411).
- Current best non-blank lines = 15 exactly (budget ≤ 15; old 240).
- Open directions = 8 (budget ≤ 8); Refuted = 14 one-line entries; Runs = 10 lines.
- Header keys and five-section order match the schema (topic/status/closed-by/valid-while/updated).

## P2 — runs
- The old page's 16 run lines carry 10 distinct run ids (097e ×3, 0659 ×2, d4ff ×2, f876 ×2, f623 ×2 duplicated).
- Prediction: the new page keeps all 10 ids, each exactly once; no id lost, none added.

## P3 — number coverage (the gold criterion, exhaustive, not a sample of ten)
- Every numeric token of the old page is either (a) literally present in the new page,
  or (b) on an old-page line that cites a run id the new page also cites ("behind a cited run").
- Prediction: literal coverage ≥ 80% of distinct tokens; residual < 80 distinct tokens; and
  **zero** tokens fail both (a) and (b) — that is the kill bar. Expected residual classes:
  5f76's rung means (2,842–13,312, 28,658), 8994's ladder mean 3,263 and control 12,321–12,353,
  d4ff's superseded dossier numbers (5.6/game-s, +0.054, 7×10⁶, 3.2×10³, 22.9 km/s, 2.7 km/s, 1.74, 4.9),
  3aec's frame arithmetic (286.8, 3.48, 208/355, 14,071), f876's event counts (596, 2,264, 1.5–10⁶ M range),
  instrument internals (0.56→ kept, 12 ms, 18 s, 48,803, 96,108, 36,404, 87,380, rtf 2000 numbers).

## P4 — headline constants (what a checker samples first)
All literally present: 6.21, 422, 82.5, 44.7, 29.3, 193.4, 57,344, 11.35, 12.42, 23–48%,
0.35–1.4, 43.6, 2,348–2,464, 978×, 294×, Γ's band 5.4–7.0, wake-up 2.6–3×10⁷,
C 4.3–5×10⁴ / 42–50, −7.1%, 179.7, 311, 3,670,016, 7,340,032, 1.45→2.99→3.88, 10–42%, 95.7%.

## P5 — disagreements decided by evidence (each names the standing side)
- d4ff's 84.09/root vs f876's 6.21: f876 stands (two independent instruments + KDTree; d4ff's number reproduced as θ-mixing artifact) — in Refuted.
- 5f76's "doubling ladder" vs 6e76's reserve-exact: 6e76 stands (micro-test fingerprints sizes) — in Refuted.
- 8994's 1.6 KB/kick K-flat vs 5f76's K-rising: 5f76 stands (three decades measured) — in Refuted.
- f623's OLS marginal vs 8994's scope attribution: 8994 stands — in Refuted.
Prediction: all four appear in the new page's Refuted with both ids.

## Kill criteria
- Any token failing both (a) and (b) in P3 → the compile dropped a supported number: fix before the dossier.
- Current best > 15 lines or page > 300 → VOID against the lens's budget.
- A run id of the old page absent from the new page → VOID.
