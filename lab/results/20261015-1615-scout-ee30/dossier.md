# dossier — 20261015-1615-scout-ee30 (scout)

**Claim.** The view's missing engine half — the birth/death feed that replaces 2df1's
240-frame membership rescan (the flyable frame's p99 owner) — is priced and it is free
at steady state: the row-set's membership flux is the observer's own orbital sweep of
the map window through the belt (2.4–3.4×10⁻⁸ flips/s per belt body, i.e. one flip per
body per ~year), composed to ~10⁻⁴ cores at 10⁹ against the scan's 8.75 cores; at
fitted zoom the belt is envelope-disjoint from the window (margin 79–86×W, permanent at
coast, held under a 0.05c burn), so the tracked set is O(locals) and the Θ(N) term is
deletable at every N; the one moment that needs a drain is the zoom-out fill (worst
frame 2,722 entries at 10⁵ = 9.5 ms at 3.5 µs/entry, 5,539 = 19.4 ms at 2×10⁵ — the
16.7 ms budget crossing sits between 10⁵ and 2×10⁵, linear in N), and a 0.05c radial
burn adds only 507 entries at 10⁵ (worst frame 6).

**Bottleneck.** Board live question 1 (bodies in the flyable engine, 10³·⁵ gap): the
per-frame walks as the plane grows. The view page names this hole twice — open 1: "the
missing engine half is still the birth/death feed (the p99 owner)"; 2df1's checker:
"the birth/death scan stand-in costs ~3.5 µs/body … recurring every 240 frames, so
against the smoothness rule the probe still crosses 16.7 ms at ~10⁴ until the engine's
birth feed replaces the scan". Expected gain: the scan composes to 8.75e-4 cores at
10⁵ and **8.75 cores at 10⁹** — it alone would eat the 4-core budget; the feed composes
to ~10⁻⁴ cores. What it deletes: the rescan component itself, at every N.

**Evidence** (float replica of the ladder scene's own birth law — scenario.rs:333-344,
belt a ∈ [2,3) AU, e Rayleigh 0.07 capped 0.4, uniform angles — with the shipped
client's map criterion verbatim from page.html `drawMap`: a square window in the star's
frame centred on the observer's *current* position, testing each body's *retarded*
offset, half-width W; fitted W from `fitLog` ≈ 7× the nearest local = 3.5 ls; belt zoom
W = 750 ls. Observer circular at 1 AU; burns add a linear-β radial ramp. Kepler solver
bracketed-damped Newton, residual ≤ 4.4e-16, self-check `validate_solver()`):

| arm | N | W | events | rate | worst frame |
|---|---|---|---|---|---|
| coast, fitted | 10⁵ | 3.5 ls | **0** / 5×10⁶ s | 0 | 0 (min belt distance 0.552 AU = 79×W) |
| coast, belt zoom | 10⁵ | 750 ls | 16,733 / 5×10⁶ s | 3.35e-3/s (held-out seed 7: 3.37e-3) | 0 |
| coast, belt zoom | 2×10⁵ | 750 ls | 9,577 / 2×10⁶ s | 4.79e-3/s (per-body 2.4e-8 vs 3.3e-8: orbital-phase dependence of the sweep) | 1 |
| straddle control | 10⁵ | 400 ls | 259 / 2×10⁶ s | 1.3e-4/s | 0 (sensitivity ✓) |
| burn β→0.05 radial, 600 s, belt zoom | 10⁵ | 750 ls | 507 | 0.56/s | **6** |
| burn, fitted | 10⁵ | 3.5 ls | **0** | 0 | 0 (envelope holds: excursion 0.03 AU ≪ 0.55 AU margin) |
| zoom 3.5→750 ls, ~1.5 dex/s | 10⁵ | sweep | 14,714 (= the full in-window set, 14.7% of the belt) | — | **2,722** (9.5 ms) |
| zoom, same | 2×10⁵ | sweep | 29,629 | — | **5,539** (19.4 ms) |

Compositions (r_event entry 3.5 µs — 2df1's own per-body scan cost, same work class;
exit 0.5 µs; scan 3.5 µs/body per 400 game-s at flying pace):
- scan: 8.75e-4 cores at 10⁵, 8.75e-3 at 10⁶, **8.75 at 10⁹**;
- feed steady: 1.2e-8 cores at 10⁵ → **1.2e-4 at 10⁹** (ratio 7×10⁴, both linear in N);
- burn at 10⁹: 5.6e3 entries over 600 s, worst frame ~600 (2 ms) — under budget;
- zoom at 10⁹: worst frame ~2.7e7 entries (~95 s of certificate work) — **the drain is
  mandatory** (budgeted admission, the 4487 pattern; entries are exact, only their
  serving is deferred);
- the row-*value* rail (not membership): emission steps 3.55e-5/s/body (cf45's doll
  interval 2.814e4 s) × in-window fraction × ~4 µs → **~0.14 cores at 10⁹ at full
  zoom** — the view's engine-side steady total at 10⁹ is ~0.15 cores, 25× under budget.

The certificate form (the engine half to wire, in `view.rs`'s gather): (i) one
**group envelope** — window box vs belt annulus in retarded coordinates — covers every
untracked body while disjoint (re-check on observer radius change and zooms, O(1));
(ii) per tracked row, membership changes only when the frozen emission offset crosses
the moving box edge — a 1-D root on the *observer's* compiled tube, computable at
row-update time (the emission step), so it rides the doll's own clock and adds no
state; (iii) the zoom drain. Prior art, mapped: kinetic data structures' scheduled
certificates (Basch–Guibas–Hershberger 1997 — the flight plan is our compiled orbit,
already exact); incremental view maintenance / differential dataflow (the map is a
materialized view over the bodies; cost ∝ delta, not size); netcode interest
management (relevance sets with boundary hysteresis — the anti-flap slack). Known
failure modes carried over: KDS retiming cascades = the zoom burst (measured above);
IVM boundary flapping = slack; interest-management pop-in = none (entries exact,
deferral only touches serving, and 649c's rows are bit-reproducible between steps).

Reproduce: `cd lab/results/20261015-1615-scout-ee30 && python3 feed.py feed_out.json`
(~4 min wall, each arm ≤ 32 s, < 2 GB); `python3 -c "import feed; print(feed.validate_solver())"`
→ 4.4e-16. No tree edits outside this run folder (work/patch.diff is empty).

**Predictions** (`predictions.md`, written before the decisive run): P1 held (3.3e-3/s
≪ the 1/s kill and under the 0.01/s expectation); P2 held on events (0) but the margin
threshold was mis-set (79×W measured, not >100×W; disjointness is permanent at coast
regardless — both radii bounded); P3 held (507 < 10³; worst frame 6 events ≪ 1 ms);
P4 held in direction, crossed the budget 5× earlier than predicted (between 10⁵ and
2×10⁵, not at 10⁶ — the in-window fraction 14.7% and the wheel's 1.5 dex/s were the
mis-priced factors); P5 held (0 and 259 > 0); P6 held by arithmetic above. One
instrument bug found and fixed en route (my first Kepler Newton omitted the e factor in
f — positions of the e ≳ 0.15 tail jumped AU-wide, chattering ~2,000 memberships/frame;
bracketed damped Newton + residual self-check now guard it).

**What would make it wrong.** (1) The client's criterion is exactly `drawMap`'s
(map: star's frame, north up, ship centred, retarded offsets) — any future coupling of
membership to per-frame observer *rotation* or aberration re-couples the flux to the
frame rate; the sky mode already differs (log-polar placement) and is not priced here.
(2) The replica is unperturbed-Kepler between doll steps; real kicks land at emission
steps so the certificate is safe by construction, but the in-window fraction's secular
drift under stirring is unmodelled (second order; the belt page's stirring rates).
(3) The locals (the near set, O(313)) are not modelled — their churn is the near set's
own read path, not the Θ(N) term, but a formation-heavy scene could differ.
(4) Costs are Linux/x86 orders of magnitude; per-event prices are borrowed from the
page's measured constants (2df1, 277d), not re-measured on this certificate's final
shape. Adoption cost: one seam in the gather (envelope + per-row boundary root riding
the doll clock) plus the zoom drain — digest-neutral by 2df1's display-exactness, with
the drain inside the presented-tick discipline (4487's bit-exact-at-canonical-cuts).
PRINCIPLES fit: "Nothing is evolved that can be derived when looked at" (#3 — the scan
re-derives a set whose answer changes once per year per body); "a body resolves only
the influences that are significant at its own scale" (#33 — the belt enters the
fitted-zoom feed as one envelope, zero per-body state); "i care about the p95/99
results" (#12 — the scan is the p99 owner; the drain is the one burst left).

**The lens.** The scout mined representation and rates, not the wire: the client-side
draw of the zoom fill (2df1's named page question) and the sky mode's log-polar
placement are unpriced here; and cross-field habits (KDS, IVM) bias toward elegant
scheduling where the engine may prefer the dumber amortized rescan at small N — the
numbers above say that preference ends at ~10⁴ bodies, where the rescan's burst already
crosses 16.7 ms.
