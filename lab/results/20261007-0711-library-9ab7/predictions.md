# predictions.md — run 20261007-0711-library-9ab7

Written before the decisive probe (`probe_tail.py`). The question: does the plane's
hitch risk (one >16.7 ms frame per hour at 60 Hz = 4.6e-6 per frame) follow from the
percentiles a bench reports (plane.md "Measured on the whole"), or only from the tail
exponent of per-frame work? H0161's limitation line left exactly this unmeasured
("cost forecasts whose tail behaviour is unknown until measured").

Streams: per-frame work W = unit stream + burst stream, burst sizes Pareto(α).
Three streams tuned to share p50, p95 and the p99.9 **as seen by a 36,000-frame
(10 min) bench**: `light` (α=∞, lognormal-ish), `par30` (α=3), `par15` (α=1.5).
Truth for the once-per-hour quantile: analytic Pareto quantiles; 10x replicate
benches for sampling noise. Queue sim: budget B/frame, backlog carries over
(the plane's overflow = real-time-factor dip), utilization ρ, FIFO vs EDF
(causal-deadline order) on clustered deadlines.

Held-out predictions (not tuned on; kill criteria in brackets):

- P1 Matched-percentile divergence: the three streams' true once-per-hour
  frames differ by >10x (prediction: ~1 : ~3-5 : ~30-100, light:par30:par15)
  despite agreeing inside the bench window. [If all within 2x, percentiles
  suffice and this run's central claim dies.]
- P2 Exponent beats moments: a Hill estimator on 36k frames extrapolates the
  once-per-hour frame within 2x for both Pareto streams; a Gaussian
  mean/std extrapolation underestimates `par15` by >10x. [If Gaussian is
  within 2x on par15, moment-based sizing stands and the claim dies.]
- P3 Firemen utilization (slack sizing): for `par15`, hitch rate (>1 frame of
  backlog beyond budget, i.e. a visible dip lasting >1/60 s) rises >10x per
  +0.2 utilization above a knee near ρ≈0.6-0.75; for `light`, ρ=0.9 stays
  hitch-free over 10^6 frames. [If par15 tolerates ρ=0.9, slack sizing is
  not the lever and the firemen lesson dies.]
- P4 Ordering is second-order under fat tails: at matched ρ and clustered
  deadlines, EDF vs FIFO changes p99 backlog by <20% on `par15`, while EDF
  cuts misses by >30% on `light` with tight deadlines (positive control for
  the scheduler). [If EDF also fixes par15's p99, ordering remains the
  lever and the barbell/admission framing dies.]

Honesty note: this is a structure-level probe on synthetic streams shaped like
the engine's known work generators (perihelion-concentrated kicks, clustered
co-orbital encounters), not a run of the shipped plane — the lab tree carries
no per-frame bench trace (artifacts/ is absent on this runner). The anchor to
the engine is plane.md's own numbers: p99 2.45–2.72 ms with worst frame 14.5 ms
(ratio 5.3-5.9x), and its line: "a percentile alone can hide a 200 ms freeze
once a minute".
