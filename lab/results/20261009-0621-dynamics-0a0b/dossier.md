# Dossier — 20261009-0621-dynamics-0a0b (lens: dynamics and attractors)

## Claim

In the shipped plane, a one-quantum perturbation of one body propagates through exactly one of
three channels, measured: **contact frames cascade near-critically and quantum-blind** (a 1.4 mm
offset rewrites ~90% of a fleet's handed-out tubes, bimodally by seed, always contained inside
the frame), **orbital peers have zero coupling** (a perturbed ship stays private for 6×10⁸ ticks),
and **doll geometry is an instant global channel** (a 1-root-unit planet-orbit change rewrites
every ship's record at the first read, before any kick).

## Bottleneck

`q-candidate-degree` / the scaling risk and H_live: does per-body memory cost stay proportional
to real encounters, or does chaos couple bodies and blow up distinctions? Answer at belt scale:
the law has **no peer coupling between orbital bodies** — nothing reads a ship — so the belt's
H_live is fed by kick streams and encounters only, not by Lyapunov growth between bodies. The
chaos budget lives entirely inside contact frames, where it is bounded by the frame (contained,
measured) and costs ≈ 0.35 tubes per contact once triggered. This deletes the "chaos floor" worry
for populations and localizes the H_live burst to battles.

## Evidence

Harness: `crates/universe/examples/twin.rs` (added by this run; everything else untouched).
Twin universes from the shipped scenes, identical seeds, one perturbed body, `settle(t)` at 16
geometric checkpoints to 6×10⁸ ticks, per-body `BodyRec` hash diff, fleet digest, universe digest.
Determinism control: `--perturb 0` → `digest_eq=true`, `ndiff=0` at every checkpoint (data/member-0.csv).

Commands (each ≤ 3 s wall on this 8-vCPU runner; build ≈ 50 s):

```
cargo build --release -p emergent-universe --example twin
T=$CARGO_TARGET_DIR/release/examples/twin   # /home/glmlab/lab-target-2/release/examples/twin here
$T member --perturb P --members M --seed S --max 600000000   # P in {0,1,262144,1048576}, M in {48,96,200}
$T ship   --perturb 1 --max 600000000
$T planet --perturb 1 --max 600000000
```

Raw CSVs in `data/`. Numbers:

- **Threshold ladder (m=48, seed 7):** perturb 1, 262144, 1048576 fine units (q = 2²⁰; 1 unit ≈
  1.4 mm at the frame) → `ndiff` 40, 42, 42 of 46–48 leavers at 6×10⁸ ticks. **No propagation
  threshold**: the lattice contact law resolves the finest unit. (P1 falsified.)
- **Cascade shape (m=48, seed 7):** contacts run t≈3×10⁵–3×10⁶ (116 total); handout wave
  t≈6×10⁶–2×10⁷; divergence appears at the *first* handout (14 of 16 leavers differ) and
  saturates at 40. Propagation is contact-gated (0 differing bodies before handouts begin).
- **Seed sweep (perturb = 1 unit):** m=48 → ndiff/leavers ≈ {87%, 81%, 77%, 8%, 88%, 83%};
  m=96 → {1%, 1%, 90%, 1%, 94%, 92%}. **Bimodal, all-or-nothing**, uncorrelated with contact
  count (m=96 seed 7: 263 contacts, cascade dies; seed 9: 244, saturates). A near-critical
  branching process: either no contact outcome flips and the offset stays private to the
  perturbed member (ndiff = 1), or one flip's descendants capture the giant component (~90%).
- **Containment:** in every run (12 seeds × 2 sizes + ladder), differing bodies are leavers only;
  all 28 made bodies — planets, moon, player, haulers, orbiters, skimmers — stay bit-identical.
  The frame-origin/COM channel does not leak the cascade out of the frame. (P2's mechanism half
  held; its closure-size half did not.)
- **Ship channel (P3 held):** `ndiff = 1` (the ship's own tube registers the 1-root-unit change),
  constant through 6×10⁸ ticks; no other body ever differs. Ships are never sources; kicks = 0
  on this horizon (circular ships at 5.27×10⁸, planet period ≈ 7.6×10¹³ ticks — the claim is
  structural: nothing reads a ship, `sources` holds planets/moon only).
- **Planet channel (P4 held, stronger):** `ndiff = 9` (planet + all 8 ships) at the first
  checkpoint, with `kicks = 0`: the doll's edge radius derives from the orbit, so every ship's
  plan reads the change at construction. Global coupling at the read rate, not a growth law.

## Predictions

`predictions.md` was written before these runs (smoke at 10⁶ ticks only). Outcome: **P1
falsified** (no quantum blocking in the contact law), **P2 half falsified** (closure is
all-or-nothing per seed, not a bounded contact closure; COM non-leak held), **P3 held**,
**P4 held** and strengthened (doll geometry couples before kicks).

## What would make it wrong

The twin diff hashes whole `BodyRec`s including plans; a differing rec could in principle carry
an unchanged observable state (plan ordering). The bimodality rests on 12 seeds at 2 sizes — a
finer sweep could reveal a continuous middle. The ship-channel horizon (10⁻² planet periods)
does not exercise kicks; a longer run could couple ships through the encounter tier, which this
scene does not instantiate (`PlayerNeighbourhood` only). Containment is measured, not proven:
a denser doll (ships crossing the fleet's doll edge) could hand the cascade to the doll's
handoff machinery.

## Cost of adopting, and fit

No engine change proposed; this is a map of the law's coupling channels. Adoption cost ≈ 0:
two design consequences worth the integrator's eye — (1) a fleet's population program cannot
survive its battle: budget ≈ 1 individual tube per contact's descendant (≈0.35 tubes/contact
measured) as the H_live burst of a battle, folded into B18/b-h-live's accounting; (2) replays
of a contact frame are all-or-nothing (one unit off ⇒ ~90% of tubes differ), so the replay
unit is the frame, not the member (bears on taleb-c271's replay granularity). A gate we lack,
suggested: **containment** — perturb one member by 1 fine unit; every body outside the frame,
and the player, must stay bit-identical (it passes today; nothing freezes it).
PRINCIPLES fit: "Compute only surprises" (3) — the cascade *is* the surprise budget of a battle;
"influences below one quantum accumulate" (6) — measured false inside contacts, true across the
frame boundary; "the player is the only wildcard" (5) — the wildcard's damage radius is the
frame, not the system.

## The lens

The dynamics lens looked for attractors and found a channel map; what it may have missed is the
*cost* tail: near-critical cascades have the worst variance for the allocator (a battle's
individualization arrives as one burst at handout time), and that p99 structure — not the mean —
is what principle 12 gates. Also unexamined here: whether the m=48-vs-96 saturation difference
is a scene-geometry artifact (grid shape, rng offset) or a real density law.
