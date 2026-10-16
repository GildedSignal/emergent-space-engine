# Dossier — 20261016-1319-dynamics-e846

## Claim

The plane's co-orbital deaths (47/144 here; 48 in b9be) are **kick-time planet-disk crossings** — the real conjunction-encounter class of the chaotic layer, not spurious planned terminals: 40% of the dead ICs' own float truths cross the planet's disk within 512 P when the conjunction is resolved (19/47 < 1 Rp, 15 of them within ±2 P of the plane's death epoch — the same conjunction), the plane's kept set is dominated by never-encounters (truth median 3676 Rp), and the prior "false death" reading was an instrument artifact on both ends: the oracle has no surface to hit, and grid sampling is blind to conjunction crossings by ~180× (P/256 grid min 2.89 Rp against a radial-turn-resolved 0.016 Rp; my own P/64 window grids see 0 of 15 crossings).

## Bottleneck

Not a board bottleneck: chaos-shadowing open direction 4 (decide the 48 deaths), itself the named prerequisite for a survival/false-death bar in B12's family (HANDOFF risk: "B12 cannot yet tell bounded from compounding"). Gain: the gate question inverts — the missing certificate is not "no ship lost that the oracle keeps" (the oracle keeps everything by construction) but **encounter parity**: the plane's kills AND its misses must each stand for the truth's crossings. The mirror error is now measurable: 20/97 kept ICs' truths also cross the disk (the plane passed over them between kicks — contact-speed's skip at conjunction cadence).

## Evidence

Scene/ensemble: b9be's own (`restricted::JUPITER`, 144 ICs = 12 synodic angles × du ∈ {±0.35…±1.45}·w). Arms (all this run, `xtask/src/behave/trojan_dive.rs`, tree b07f5a0b, shared x86, 8 vCPU):

- **Channel census (new engine counters, outcome-free: `Resolved::Lost*` variants counted in `Stats`; 3 plane reruns bit-identical incl. the dead set).** All 47 deaths are `planet_kick` — `kick_clock`'s sources loop finds the ship's readout position inside the planet's surface at a kick tick. Zero planned terminals (`LostTerminal`), zero star kills, zero edges, zero plan failures, `refused=0` throughout. Earliest deaths 10.73 / 11.89 P (b9be's checker: 10.75 / 12.0 — the same ships). Death epochs spread 10.7–497 P; 39/47 at |du| ≥ 0.85. The plane's osculating periapsis at death stays 35–1088 star surfaces (median 663) — the star is never involved; the J walk to death is tiny (−3×10⁻⁷…−2.8×10⁻⁶ relative).
- **Periapsis-resolved oracle conjunctions (the judge's own `tracking` integrator, rtol 1e-12, whole horizon):** dead-IC truths min 0.046 Rp, p10 0.09, median 1.94; alive-IC truths median 3676 Rp, min 0.016. Truths crossing the disk (<1 Rp): 19/47 dead-IC vs 20/97 alive-IC; <2 Rp: 24 vs 26. The checker's P/256 numbers (2.89 Rp ensemble, 4.75 dead) were grid floors, not periapses.
- **Windowed parity (P/64 grid + fresh tracking integrator over ±2 P of each death epoch):** truth crosses the disk at the death conjunction for 15/47 (min 0.004 Rp); ≤2 Rp for 17; ≤5 Rp for 22; >10 Rp for 21. The P/64 grid itself catches 0 of the 15 — only radial-turn resolution sees them.
- **Analytic arm:** no zero-velocity confinement anywhere — every IC has J₀ 1.0–1.3% *below* J(L1)=5.7684e-9 (and below L2, L3): all necks open, both surfaces energetically reachable for every ship (this falsifies my frozen P1's confinement half; the "spurious by invariant" shortcut does not exist in this scene — the ensemble lives just inside the open-neck regime, which is why it is the chaotic layer).
- **Controls:** a state born inside the star's surface dies on its first item via the crash-periapsis channel (channel wiring's positive control); the elements pipeline reads its q/S = 0.9000 exactly; oracle rtol 1e-12 vs 1e-13 identical; oracle J drift ≤ 2.35×10⁻⁹ relative over 512 P.
- Reproduce: `regen.sh` (~8 min: plane 310 s dominant). Machine: shared Linux x86 — orders of magnitude only.

## Predictions

`predictions.md` was written before the 512 P arms. P2 (≥90% planned terminals) **failed decisively — 0% terminals, 100% planet_kick**: I looked for the tube compiler's plan and the deaths were the runtime disk check. P1's confinement half **failed** (no IC is confined; necks open for all). P3 half-held (the J walk is real but tiny, ~10⁻⁶; it does not cross any neck — the mechanism is not a J walk). P4: dead-IC q_min/S = 15.6 vs alive 138 — the dead ICs are the low-periapsis population, direction right. P5 passed (epochs 10.73/11.89 vs 10.75/12.0; controls green; no class changes at 1e-13). P6 passed trivially (survivors' J on their side of nothing — there is no barrier). The honest miss: I predicted the compiler's bookkeeping kills ships; the engine's own trajectory meets the planet.

## What would make it wrong

- The `tracking()` oracle resolves the conjunction around the PLANET with the planet's pull regularized inside its radius (uniform sphere): a crossing <1 Rp is a genuine disk entry under the judge's own model of the planet; if the game's planet were porous this class would need re-reading (it is not: surfaces kill in the plane).
- Per-ship phase parity (15/47) is horizon-scrambled by chaos; the class-level statement (40% of dead-IC truths cross; kept-IC truths median never-encounter) is the shadowing-level claim, and it rests on one ensemble, one μ, one horizon.
- My dead set (47) differs from b9be's (48) in 3 ICs, all at φ = 105° (they kill −0.85/+1.25; I kill −1.45), deterministic across 3 of my reruns; `crates/` and `xtask/` have had no commits between their run and mine. Unexplained — a knife-edge conjunction whose outcome differs between drivers that should be equivalent (a lead, priced below).
- The plane's kill radius is `surface_in(planet, doll 0)`, converted through the planet doll's octave; I did not separately verify it equals 4.84e4 judge units (the death epochs' agreement with b9be and the census's cleanliness bound it, but the exact number is unmeasured).


Nothing to adopt in the engine (the census counters are print-parity: stats only, zero outcome bits, and they are this run's instrument). What changes is the gate: B12-family survival bars must (a) judge only seeds whose *resolved* reference stays outside the planet (B13's rule, now with the radial-turn instrument this run used), and (b) count both error directions — the plane's kills at real encounters (this run) and its misses of real crossings (20/97 kept ICs whose truths cross; the skip again). Fits principle 2 ("error type over error size": the error is which encounters resolve, not a magnitude) and principle 10's instrument rule (a control that cannot fail is broken: the P/8/P/256 oracle-min instrument could never have seen a crossing — its dwell is ~P/10⁴⁻⁵). Cost of the gate: the tracking integrator exists (`restricted.rs`), one filter in the B12 harness.

## The lens

The dynamics lens went hunting for the invariant that forbids the deaths and found no barrier — instead the encounter manifold itself: the layer's transport channel to the planet is thick (27% of all 144 truths cross the disk in 512 P), and the plane samples it honestly at kick cadence. What the lens may have missed by framing deaths as an attractor problem: the *rate* view — a birth–death process between the layer and the disk, whose matching statistic (crossing rate per synodic period, plane vs truth) is the actual certificate, and which one ensemble at one μ cannot pin (μ = 1e-2 unrun; time).
