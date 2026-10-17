# predictions.md (written before the decisive census and arithmetic)

Run: 20261017-1330-library-7bd9, library lens. Target: memory-h-live's newest hole —
inversion-470f's bimodal play-time FLOW (peak 44 MB or 221 MB on the same flight;
~11 kB/game-s growth; ~78k allocations bulk-dropped; peak RSS retained forever;
every shipped counter flat; mechanism unattributed).

Cases I have NOT tuned on (I have not yet run any grep of the wall path nor the
arithmetic below at 10^6):

- **P1 (code census).** The accumulation is per-event/per-member bookkeeping on a
  budget-guarded path: I predict `crates/universe` contains at least one branch where
  the frame/wall budget or backlog state defers or skips a prune/settle/publish of
  per-event records (the class c304 priced as rebind-history, ~10 kB/ship-kick, and/or
  the observer's 216 B held candidates), and that no allocation on that path is counted
  by any shipped counter. Kill: if the wall path has no such guard (every prune
  unconditional), P1 dies and only the site list stands.
- **P2 (arithmetic, published constants only).** 470f's growth is ~27–39 B per member
  per game-s (N=100:3.9, 400:11, 800:29, 1600:54 kB/gs). At the ladder's 10^6 that
  would be 27–39 MB/gs — a 6 GB machine is ruined in ~3 minutes of play. The merged
  10^6 "bits held, 20 s flight" claim therefore cannot have carried this class at that
  rate: I predict the class either does not fire on the belt population or the 10^6
  flights all took the flat path (no load axis flown). Decisive held-out case for the
  checker: one counting-allocator flight at N=10^6 under 8-way load — growth > 0 kills
  the 10^6 headline as stated; flat confines the class to fleet scenes.
- **P3 (quotes).** All 5 lesson quotes verify byte-identical against the fresh fetch
  (readwise.json, 4,590 highlights, cached here); regen.sh re-verifies.
- **P4 (corpus).** The practitioner shelf (Kelly Skunk Works, Perrow, Gall, Gordon,
  Ignition!) has < 5 highlights total in the corpus on coupling/margins/systems
  growth — the lessons must draw from the mental-models/Taleb corpus; a checker
  recounting should agree.

What I expect to be wrong about: P1's specific site (I have not read the wall path
yet); the 83,768-allocation identity (2.6 kB mean) may not decompose cleanly into the
c304 class.
