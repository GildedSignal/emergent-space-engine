topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261017-1447-system-6671

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹).

## Current best
**The stream's shared-field premise is now measured from the inside: 64.5% of the
`secondaries`-driven `state_of` stream is bit-identical repetition — 169,145 of 262,198
calls repeat an exact (source, tick) key, 0 bit-conflicts anywhere — and the split is
structural, not uniform: the belt's birth wave is ONE field read evaluated 29,142 times
(j0/j1/j2 at t=0, 9,714 identical reads each, once per belt body), the locals' doll batches
naturally (its source read 112,277 times at 3,579 distinct ticks, 96.8% repeated, top 342×),
while the belt's kick comb does not batch at all (74% distinct ticks ex-birth) — so
direction 1's lever splits in two: a per-(j,t) memo in `Ctx` is bit-safe (mechanism:
bindings change only at the source's own events, resolved in tick order; measurement: 0
conflicts) and free (~1.7× on the N-linear `secondaries` term), but it cannot touch the
belt comb's structural 74%, whose cure is one canonical-tick field read per comb (BELT_SPLIT's
legality class) or the belt layer itself (dossier: three taxes — shared field, rebind,
tube memory — one payer, the per-body tube) (20261017-1447-system-6671, system;
`nladder 10000 coast 60 600`, print-only census, digest-identical on `ladder_digest
"N=3000 coast through"` both arms).** Prior best retained below: the census by call site
(20261017-0428-spacex-d959) — 5.0 readouts/body/event, 60% the per-event `Ctx::secondaries`
rebuild — stands unchanged; this run answers its open question 1 (no, the drain does not
batch the belt's kicks at shared ticks; yes, the locals' doll does).
Checker arms (20261017-1447 check): burn at 10⁴ (61.4% repeated, 0 conflicts, comb ex-birth
74.6% distinct), rtf 120 (77.9%, 0 conflicts) and N=10⁵ (43.9% overall, 0 conflicts, same
split: comb 74.1% distinct ex-birth, doll 96.8%, birth 99,714×3) — the headline fraction is
window-mix dependent (birth-wave share falls as the crest widens); the decomposition and the
0 conflicts are the invariants, over ~2.1M reads.

## Refuted
- **"The scan owns the burn read stream"** (the assumption under promotion's direction 1):
  on shipped main the scan is flat in N — in the settle (160,663 at every N from 10⁴ to
  3×10⁵) **and in the burn flight itself** (99,113 at both 10⁴ and 10⁵, checker-measured:
  the N-comparison the author's P2 promised but never ran); the N-linear term is the
  sources' re-reads (20261017-0428-spacex-d959).
- **"The read stream is burn-specific"**: coast and burn agree within 0.5% on every
  N-linear site; the stream belongs to the events, not the flight (20261017-0428-spacex-d959).
- **"The belt comb's shared ticks make the per-event rebuild a free batch"** (the
  optimistic reading of direction 1): the belt's kick-time source reads are 74% distinct
  ticks ex-birth; only the locals' doll and the birth wave collide exactly
  (20261017-1447-system-6671).

## Open directions
1. **Adopt the (j,t) memo** (`Ctx`, keyed on exact ticks, no invalidation needed while
   resolution is in tick order): 64.5% of the secondaries stream measured deletable,
   bit-exact by construction and by the 0-conflicts census; digest-identical adoption, the
   cheapest item on this page. Watch: cache size is the distinct-tick window (locals' doll
   ~3.6k keys/source here), and the memo must be dropped or versioned if an out-of-order
   path ever reads a source before its own event lands.
2. **The belt layer** (the structural 74%): one canonical-tick field read per comb — a
   quantization in BELT_SPLIT's open legality class — or the full layer (one field pass
   per comb, compact-store members, one compiled cycle per cell) that also retires the
   rebind (68–85%, 620e/96b4) and the 4.85–5.06 kB/B plateau (b30b). Hard case: resonance
   cells and the synodic scatter stay sparse (kick-cadence; d0ea).
   Checker caveat: P3's pre-registered smoothness line (relative drift ≤ 1e-2) is crossed at
   whole-flight scale by j0 (3.1e-2) and j3 (9.8e-2), and the census has no per-comb grouping,
   so comb-scale smoothness — the quantization's actual premise — is unmeasured.
3. The clock step's 1.0/body (`step.rs:660`) and the scheduler's post-event read
   (`observe.rs:190`, `root_state_raw`, 1.0/body) are the next terms; each is a read of the
   body itself, so the lever there is fewer events (cadence), not cheaper reads.

## Contradictions
- promotion.md's b = 11.48 reads/body/20k gs (cache lookups, patched binary,
  20k-gs horizon incl. post-wave) and spacex-d959's 12.9 counted readouts/body at 14.6k gs
  agree in order; the instruments differ (lookups vs readout calls) and have not been
  cross-run on one binary. The new census counts `state_of` only (2.42/event here): a
  third instrument, same order.

## Runs
- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site; the
  scan is flat in N, `secondaries` is 60% of the per-body half; digest-identical instrument.
- 20261017-1447-system-6671 (awaiting grade): the stream's sharing axis measured — 64.5%
  bit-identical repetition, 0 conflicts, the birth wave = one field read ×29,142, the belt
  comb 74% distinct; the memo/layer split of direction 1.
