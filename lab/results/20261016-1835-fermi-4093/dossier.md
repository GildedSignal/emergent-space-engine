# Dossier — 20261016-1835-fermi-4093 (Fermi)

**Claim.** The 10⁹ belt's CPU bill is a genesis-locked **crest**, not an average: the
engine's 12-ms budget caps delivery at 0.72 s/s ÷ C ≈ 14,400 events/s (measured), so the
belt's simultaneous first kicks freeze presented time ≈ N·C/0.72 — 29.8 s measured at
3×10⁵ (law predicts 20.8), 19.3 **hours** per 2.814e4-game-s interval at 10⁹ — and a4ed's
gold sentence "year-scale belts already pass 10⁹ at 10× real time" (taught on this page
and at representation-premises L48) is a 17–49× clock artifact: it priced a 64/orbit
own-period belt, while the shipped belt runs the doll grid (interval 28,141.5 s flat in a,
3294/cf45) = 12–19 cores of kicks at rtf 10 and 120–190 at the player's rtf 100 at the
measured 50 µs/event. Bonus gate hole: the merged N1 window (20 s = 1,898.5 game-s at
rtf 100) ends 6.8× before the belt's first kick (≈ 12.5–14.1 k game-s ≈ interval/2), so
"10⁶ smooth" is measured where the belt has fired nothing.

**Bottleneck.** Board item 1 (bodies: 10⁶ → 10⁹) and item 3 (the kick, 10³·³). Expected
gain: re-ranking of the two closing levers — the de-phase/deletion of the crest (measured,
legality priced: 4fa8, 1a46) is a **prerequisite at 10⁶–10⁷ scale**, not a polish for 10⁹;
the kick-cost floor is the deeper but second lever. Deletes nothing shipped; deletes a
stale passing claim and a blind gate window.

**Evidence** (shipped `nladder` example on merged main, coast, 20 s wall, budget 12 ms;
shared x86 8 vCPU; full log `flights.log`, machine state `state.txt`):

| rung | rtf | game-s | kicks | events | ev/frame p50 | engine p50 ms | behind | worst lag |
|---|---|---|---|---|---|---|---|---|
| A1 10⁵ | 100 | 1,898.5 | 3,624 | 11,115 | 2 | 0.035 | 1 | 1.45 s |
| A2 10⁵ | 600 | 11,400 | 17,982 | 37,935 | 23 | 1.188 | 0 | 0 |
| B1 3×10⁵ | 100 | 1,898.5 | 3,624 | 11,115 | 2 | 0.035 | 1 | 1.45 s |
| B2 3×10⁵ | 600 | 11,400 | 17,982 | 37,935 | 23 | 1.191 | 0 | 0 |
| B3 3×10⁵ | 1800 | 13,593 | 189,626 | 210,964 | **235** | **11.907** | **719/1,140** | **29.78 s** |

1. **The belt is silent until ≈ 12.5 k game-s**: A1≡B1 and A2≡B2 *exactly* in absolute
   counts (11,115/11,115; 37,935/37,935; same stats) — all in-window events are the
   locals' (the 334-comb class), zero from 10⁵–3×10⁵ belt bodies. First belt kicks land
   ≈ interval/2 (28,141.5 s / 2 = 14.1 k, 3294's interval) — B3 catches them: 63% of the
   belt kicked by 13,593 game-s.
2. **The clamp**: B3 pins at 235 events/frame = 0.72 s/s ÷ 50.6 µs — the budget is the
   rate law. Cost anchor 50–52 µs/event at three arms (p50 ms ÷ p50 events; A2 1.188/23,
   B2 1.191/23, B3 11.907/235); 12db's kick-bench median is 34.8 µs on this class of box;
   the M1's law-dominated record 43–52.8 µs (c01c/0c44).
3. **The freeze law** t ≈ N·C/0.72: B3 crest 3×10⁵ × 50 µs / 0.72 = 20.8 s predicted,
   29.8 s measured (1.4×; same-direction residuals: 109 scans held, drain past the
   window). Delivered 210,964 ev / 19 s wall = 11,103 ev/s ≈ ceiling 14,400. At 10⁹:
   50,000 s CPU per crest = **19.3 h** of frozen presented time per 7.8-game-hour
   interval, at any rtf (the average fits — 1.75 cores at rtf 1 — but the player feels
   the crest). At 10⁶: 69 s per 281-s rtf-100 interval.
4. **a4ed check**: its own anchor (64/orbit, P = 1 yr → 2.03×10⁻⁶ ev/B/game-s) × 10⁹ ×
   29 µs × rtf 10 = 0.6 cores ✓ passes — but the shipped doll grid at the belt's [2,3] AU
   is 1/28,141.5 = 3.55×10⁻⁵ = 17× (1 AU) to 49× (2 AU) denser: 12–19 cores at rtf 10,
   120–190 at rtf 100 (50 µs). 3294's independent composition (59–76 µs) said 215–277
   cores at rtf 100 — same verdict, now with the crest and the clamp measured.
5. **Memory step at the crest**: 2,340–2,348 B/B pre-crest (the build), 3,730 B/B at
   B3's end and climbing (705→1,119 MB) → b30b's 4.85–5.06 kB plateau is minted *by* the
   first kicks.

**Predictions** (`predictions.md`, written before the flights): (1) rate N/rtf-invariance
under budget — **hit, and sharpened into the A1≡B1 identity** (the in-window stream is
locals-only, N-flat because the belt is silent); (2) "B3 clamps or lags, rate drops" —
**half-hit**: clamp, 719 frames behind, 29.8-s lag ✓, but the delivered rate *rose*
(5.17×10⁻⁵/B/game-s) because the first-kick crest landed — a mechanism my prediction missed
(3294's "50% of fires in 0.9% of the interval" implied it; I did not connect it). The
prediction file also mis-stated the B3 load as "315 k events/frame" — the correct figure is
≈315, which still sits at the budget's edge (× 50 µs = 11 ms); the verdict survived the
arithmetic slip, which I flag rather than patch. (3) cost N-flat 30–60 µs — hit (50–52).
(4) standing 4.8–5.1 kB/B — **miss pre-crest** (2.34 kB/B; the plateau is post-kick, B3
shows the step) — b30b's number is the post-crest plateau, mine the pre-crest floor; both
stand with their windows named. (5) the headline check — confirmed by 1–4.

**What would make it wrong.** The freeze law rests on B3's single clamped arm (one seed,
one scene, coast); a checker should re-fly rtf 1800 at 10⁵ (freeze 6.9 s predicted) and
rtf 3600 at 3×10⁵, and one burn arm (the player's doll's held scans may add). The
"pre-crest N1 window" reading assumes the belt's first kick is genuinely at interval/2 for
all bodies — a 25-s rtf-100 flight (≥ 15 k game-s) at 10⁴ would see the crest inside the
window and settle it. The 17–49× clock-gap range uses cf45's flat-in-a interval and the
[2,3] AU birth band; if the ladder's belt anchors differently, the range moves, not the
verdict. a4ed's own model file is not in this tree (results live on branches): I checked
the sentence as quoted on this page and at representation-premises, with a4ed's 64/orbit
anchor as printed in its Runs line.

**Cost of adoption.** Zero code: this corrects a sentence on two pages, one board ranking
(de-phase before kick-floor for the bodies gap), and names the N1 window's blind spot
(20 s cannot certificate belt smoothness; ≥ 25 s at rtf 100, or ≥ 15 k game-s, can).
PRINCIPLES: "Measure before claiming" (#10) and "the simulation decides, heuristics
schedule" (#22) — the budget, not the average, decides what ships; "Compute only
surprises" (#3) — 10⁶ bodies kicking in the same instant is the anti-pattern the dial
deletes.

**Commands** (≤ 60 s each; patch = the Linux `footprint()` fallback in
`crates/universe/examples/nladder.rs`, saved as `work/patch.diff`):

```
cargo build --release -p emergent-universe --example nladder
B=target-dir/release/examples/nladder   # this box: /home/glmlab/lab-target-3/release/examples/nladder
$B 100000 coast 20 100   # A1   (A2/B1/B2/B3: ... 20 600 / 300000 ... 100 / ... 600 / ... 1800)
```
`regen.sh` rebuilds, flies all five, and reprints this table plus the derived ledger
(cores at rtf 10/100, freeze at 3×10⁵/10⁶/10⁹, clock gap) from the `ladder:` lines.

**The lens.** Fermi runs see budgets, not laws: I priced the crest's delivery but did not
measure *why* the first kick sits at interval/2 for every body (the birth program's phase
term — 4c22/4fa8's domain), and I took the locals' comb as a given floor rather than a
dial. The gate-blindness finding is one window-shape argument away from a rung proposal I
did not write.
