# Dossier — 20261017-0005-system-efd4

**Claim.** The plane's compiled-trajectory catalogue is a cache pretending to be state: its entries
are a pure function of an intern key it already holds, nobody queries it, and the digest ignores its
slot ids — so one structure (key → shared compile) deletes the co-orbital standing duplication
(measured 99.6% on a 512-ship formation), the creation compile for program-minted bodies on shared
orbits (16.4 µs × duplicates), and, with the same fact read as evictability, the belt's standing
stock; the kick-CPU half of the memo idea stays dead (memo.rs).

**Bottleneck.** Memory in the flyable engine (scoreboard: ~5,100 B/body after the first kick, gap
10^2.6–10^2.9 to ≤ 6 B), standing-representation lever ("75–615×", memory-h-live open direction 1).
Expected gain: 10².3 on the compiled-trajectory stock under co-orbital concentration (fleets,
formations, program births on shared orbits); deletes the per-binding mint, not the law. It does
NOT move the scattered belt (0.4% duplication measured) — there the same fact pays as eviction
(5465: 58% of doll-body bytes regenerable bit-identically from the exact key).

**Evidence** (Linux/x86 cloud, orders of magnitude only; `cargo test --release -p emergent-universe
--test cache_duty -- --nocapture --test-threads=1`, ~12 s build warm, 0.6 s run):
- Formation, 512 co-orbital ships (one circular orbit, 512 phases; cae7's control at 512):
  **513 live bindings, 513 standing entries, 2 distinct intern keys** — 511/513 = 99.6% of the
  compiled-trajectory stock is exact duplicates; creation 16.4 µs/ship.
- Scatter control, 512 ships on 512 distinct orbits: 513 standing, 513 distinct (0% duplication),
  11.3 µs/ship — the intern's null case, and the belt's shape.
- The flown plane (48 members): 39 standing for 38 distinct; with a 2,000-ship ladder belt:
  2,044 standing for 2,036 distinct (0.4%) after 2,550 kicks — rebind churn is net-zero here
  (retire releases the old slot), and the ladder's distinct-orbit population shares nothing.
- Reading, verified by grep across `crates/`: (a) `Catalogue::get` in `crates/universe` has **zero
  callers** — every reader holds the `Arc<Entry>` in its `Binding`; (b) `crates/space`'s own
  `Catalogue` interns by `(OrbitKey, bool, Option<Scalar>)` (`tube.rs:52`) and `CyclePool` interns
  by `OrbitKey` — the plane's fork (`bind.rs:39`) kept the free list and dropped the intern;
  (c) the digest leaves slot ids out by design (ties.rs: "the catalogue slot a tube's key indexes
  is an allocation, not a history"); (d) `Orbit::compile(key)` is deterministic integer code, so
  equal `(doll unit, OrbitKey, sense)` ⇒ identical entry bits.
- The formation's ships die on the planet within 0.5 s at rtf 100 (their orbit passes within the
  planet's radius; every body is real): their 512 entries stay standing after death — the
  corpse-retention term (a11b) reproduces as a second copy of the same fix (release on death).

**Predictions** (predictions.md, written before the run): P1 held (2 distinct keys, duplication
99.6%); P2 held (513/513, no gain); P3 held (creation 11–16 µs/ship, compile-dominated);
P4 held (belt duplication 0.4% < 5%); P5 partially — standing did not grow beyond live + 8 over
2,550 kicks, so e4cc's churn leak does not reproduce on this stream; the corpse term is the
growth channel here instead.

**What would make it wrong.** A reader that resolves a tube through the catalogue (none exists; if
one lands, sharing still cannot change bits — the entry is identical — but eviction must then keep
or re-serve it); a second doll whose mass mantissa makes equal keys compile differently (covered:
the intern key includes the doll's `Unit`); a digest that covers slot ids (it does not, ties.rs).
Cost of adopting: ~30 lines in `bind.rs` (intern map + refcount beside the free list; copy the key
tuple from `crates/space/src/tube.rs`), no law change, no gate re-freeze — digests are unchanged by
construction and should be re-proven by one flight in the adopting step. Fit with PRINCIPLES:
"Store the generator, not the generated" (6); "the best part is no part" (17); "a fix signals the
wrong representation" (19) — three shipped villains (per-binding mint, corpse retention, belt
standing stock) are one representation error, not three optimizations.

**Grade suggested: silver.** Real, reproduced, controls both sides, but the intern patch itself is
argued from reading (purity + zero `get` callers + digest scope) and not flown here; the one
experiment to gold is the 30-line intern + `--replay-all` digest identity.

**The lens (whole system).** What it unifies: the memory villain (cae7/4a62/5465), the churn/corpse
terms (e4cc/a11b) and the creation cost of program births are one missing structure — the memo the
law's own State section already names ("Cycle memo … shared by every tube with the same key").
What it deletes: the per-binding compiled orbit (58–75% of a doll body's bytes under concentration),
511 of 512 creation compiles per formation, and the dead-body entries. Where the trees hid the
forest: five runs and a frozen test fought over the kick's memo (CPU); the catalogue's actual job
(ownership of a pure cache) was never priced. Blind spot named: the unification's hard case is the
*driven* belt, where every body's key is distinct AND hot (kicks every orbit) — there sharing pays
nothing and eviction pays only if reads are bursty; that case is the promotion page's dwell
question, not this one.
