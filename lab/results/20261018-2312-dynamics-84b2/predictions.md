# Predictions (written before the decisive runs)

Setup: shipped `Chronon` + `Law::RelativisticV1`, Q = 2^20, the ladder's own trapped-gas
genesis (`worlds::gas` mirrored; knobs default = bit-identical), fill 0.7 (cell 2, the
touching lattice), vmax 2^16 units (β ≤ 0.09, ρ = reach/|w| ≥ 11: no skip boundary),
burn-in 1024, horizon 8192 unless said. Cases below are **not tuned on**: they are the
arms I will run once and read.

- **P0 (calibration, not a prediction):** my harness reads the checker2 ladder's orders:
  Fano₆₄(post-burn) ≈ 1.2 at n = 400, ≈ 2.6 at 1600, ≈ 33 at 6400 (fill 0.7).
- **P1 (the N-law, the decisive half).** Fano₁(post-burn, per-chronon contacts) grows
  with n on the touching lattice: the global-coherence reading predicts Fano₁ ∝ n within
  a ×1.8 band from 400 → 12800 (i.e. Fano₁(12800)/Fano₁(400) ≥ 10 if Fano₁(400) ≈ 0.15).
  The local-cages reading predicts saturation (Fano₁ ≤ 1.5 at every n). The ladder
  separates them. Fano₆₄ should track Fano₁ × (a window factor that depends on the
  mode's period vs 64).
- **P2 (the allocator letter).** The *relative* per-window tail is n-independent: the
  per-64-chronon count's p99/p50 and max/p50 at n = 12800 sit within ±35% of their
  n = 400 values (a global mode modulates a rate ∝ n; relative depth is a property of
  the mode, not of n). Per-chronon p99/p50 stays ≤ 1.25 at every n. If instead the
  per-window tail *grows* with n, the breathing mode is a real smoothness cliff and I
  will say so.
- **P3 (mechanism).** The post-burn per-chronon contact series has one dominant spectral
  peak whose frequency falls as the box grows at fixed fill: f_peak(n)·side(n)
  approximately constant from n = 400 → 6400 (acoustic reading: the box's fundamental,
  period ≈ 2·side/⟨|v|⟩ chronons), against the cage-rattle reading f_peak ∝ ⟨|v|⟩/cell
  (n-independent at fixed fill and vmax). The x-band count series are mutually
  correlated at the peak (|mean pairwise corr| > 0.3 at n = 1600): a global mode, not
  independent cages. The velocity V-rows oscillate at the same frequency.
- **P4 (attractor vs transient).** Fano₆₄ computed in four successive 2048-chronon
  blocks of the post-burn horizon decays by less than 2× from first to last (sustained
  attractor). If it decays ≥ 5×, the mode is the genesis ringdown and its allocator cost
  is a startup cost only (the lens's blind spot: a transient that ruins early frames).
- **P5 (dephasing, held out until the main analysis is read).** At n = 6400, fill 0.7,
  mass spread {1,2,4} (pattern i%3, same genesis draws otherwise) cuts Fano₆₄ by ≥ 3×;
  radius spread {0.75,1} cuts it by ≥ 2×. Both knobs leave n, fill and the box
  unchanged; if the mode is a resonance of identical cages, any detuning must kill it
  ("the system does the work for us"). If it survives both, the mode is the box's, not
  the cages' — stronger than P3's acoustic reading.

Kill lines (stated before running): P1 decides the scaling law either way; a result is
only a kill of a *configuration* (monodisperse touching genesis), never of the method.
No run here touches gates, crates on main, or frozen evidence.
