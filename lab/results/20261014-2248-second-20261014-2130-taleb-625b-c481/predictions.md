# Predictions (written before the decisive arms; smoke only at N=3000, 8 s, probe 2.5 AU)

The instrument (this run): `scanmem` counters on the scan path — created/reused/answered, candidates per mint,
the candidates vectors' standing bytes (capacity × 224 B/item, Drop-decremented), capture/answer ns, and which
branch `radial::candidates` took (walk-all vs windowed) — plus RSS from /proc/self/statm every frame. The record's
arms re-flown as digest controls (home coast/burn, band coast) must reproduce `2c16867e…`/`48a29edf…`/`d467a24f…`
bit for bit: the counters must be outcome-neutral.

What the smoke (N=3000, L8, 2.5 AU) already showed and the arms must confirm at scale:

- **S1 the site:** the minted scans' `candidates` vectors are the retaining site. At 10⁵ in-band I predict
  standing bytes ≈ the RSS growth above the scene base within ~25% (capacity counts untouched tail pages;
  RSS lags standing). Per mint ≈ candidates × 224 B × ~1.3 (Vec growth), i.e. ~30–45 MB at 10⁵.
- **S2 the drain freezes:** exactly ONE scan is answered in flight (the smoke: answered = 1 at 10.6 ms). The first
  answer sets `scan_ns`; the drain's `room < 2·scan_ns` guard then exceeds every 12-ms frame's remainder forever.
  At 10⁵ the kill arm dies with answered = 1 and `held` growing ~1/frame (the SCAN_BACKLOG cap of 2,048 never
  reached: death at ~25 mints × ~40 MB). At 10⁴, where the record says the burn "completes flat at 1,330 MB", I
  predict the plateau is NOT the idle drain but the SCAN_BACKLOG cap churning (answered grows in bursts, standing
  plateaus ≈ cap × per-mint × the mint fraction of enqueues): the record's "flat" is a cap, not a drain.
- **S3 the sweep (the transit's integrand):** candidates(radius) is bimodal — small (~10–40: the planets, the
  haulers) below the belt's registrations and windowed; belt-scale (walk-all, ~10⁵, the whole doll) inside 2–3 AU.
  At 3.5 AU I predict it is STILL belt-scale (Rayleigh-e belt ships' apoapsides reach ~4.2 AU, so their registered
  hulls cover 3.5): the ruin band is wider than the belt.
- **S4 the crossing (the transit arm):** a=2 AU, e=0.95, r₀=1.9992 AU crosses 2.0 AU at t≈6,000 game-s (frame
  ~360 at rtf 100). Before: scans µs-cheap, RSS flat. After: candidates jump to belt-scale, mints cost ~tens of
  MB, the RSS slope switches on within a few hundred frames and the arm self-limits (the record's kill, caught
  early). The coast crossing control completes flat with a digest. If the L8 burn's Δv moves the crossing
  materially the measured r column will show it; the switch is what matters.
- **S5 the cadence:** the mint cadence under L8 ≈ the player's kick cadence (the smoke: one mint per ~2.4 game-s);
  the ruin arithmetic is mints/s × per-mint bytes, both now measured constants.

Kill criteria (written before the arms): if standing bytes do not track RSS growth at 10⁵ (another site retains:
the Entry Arcs, the queue), or the drain answers steadily at 10⁵/10⁴ (the freeze story wrong), or candidates stay
belt-scale at 1.0 AU (no radius window at all), the dossier claims what is measured instead, and the fix target
moves. If the digest controls differ by one bit, the instrument is not neutral and everything stops there.

Held out for the checker: seed 2 on the crossing arm; the 3.5 AU sweep point (the widest prediction); a kill arm
flown with `ES_RSS_LIMIT_MB=1500` (the growth rate, not the plateau, must be the invariant).
