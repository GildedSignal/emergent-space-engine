//! Monitoring, serialised as JSON (docs/work-allocation-design.md §5).
use crate::qos::Class;
use serde::Serialize;

#[derive(Clone, Debug, Default, Serialize)]
pub struct Pcts {
    pub n: usize,
    pub mean: f64,
    pub p50: f64,
    pub p95: f64,
    pub p99: f64,
    pub p999: f64,
    pub max: f64,
}

pub fn pcts(v: &[f64]) -> Pcts {
    if v.is_empty() {
        return Pcts::default();
    }
    let mut s = v.to_vec();
    s.sort_by(f64::total_cmp);
    let at = |p: f64| s[((p * (s.len() - 1) as f64).round() as usize).min(s.len() - 1)];
    Pcts { n: s.len(), mean: s.iter().sum::<f64>() / s.len() as f64, p50: at(0.5), p95: at(0.95), p99: at(0.99), p999: at(0.999), max: s[s.len() - 1] }
}

#[derive(Clone, Debug, Serialize)]
pub struct WorkerReport {
    pub class: Class,
    pub qos_accepted: bool,
    pub units: u64,
    pub ops: u64,
    pub busy_seconds: f64,
    pub utilisation: f64,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct RegionsReport {
    pub initial: usize,
    pub last: usize,
    pub max: usize,
    /// Regroups that joined bodies of two or more regions.
    pub merges: u64,
    /// Regroups that divided a region.
    pub splits: u64,
    /// Merges requested by a horizon that fresh anchors showed unnecessary.
    pub merges_avoided: u64,
    /// Windows whose true box exceeded its forecast promise (forecast misses; harmless unless
    /// another true box is within reach).
    pub promises_exceeded: u64,
    /// Two isolated true boxes of one window within reach: those lineages roll back.
    pub rollbacks: u64,
    /// Regions restored by rollbacks (scope), and how far each rollback reached back.
    pub rolled_back_regions: u64,
    pub rollback_depth_chronons: Pcts,
    pub accepted_windows: u64,
    pub wasted_ops: u64,
    /// Current widening of speed forecasts after failures (1 = none).
    pub speed_escalation: f64,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct UnitsReport {
    pub count: u64,
    /// Whole unit on the worker: stepper advance plus the allocator's measuring.
    pub ms: Pcts,
    pub ms_performance: Pcts,
    pub ms_efficiency: Pcts,
    /// Blame split: time inside `Stepper::advance` versus the allocator's world read, true box
    /// and islands at window ends, and the wait for the state lock afterwards.
    pub stepper_advance_ms: Pcts,
    pub allocator_measure_ms: Pcts,
    pub lock_wait_ms: Pcts,
    pub ops: Pcts,
    /// Units whose stepper spent more ops than the budget (its indivisible step), by how much.
    pub over_budget_units: u64,
    pub over_budget_ops: Pcts,
    pub max_ops_over_budget_ratio: f64,
    /// Largest indivisible unit the stepper itself reports (Metrics::max_unit_ops).
    pub stepper_max_unit_ops: u64,
    /// Calibrated ops per unit for each core class (≈ unit_seconds of work).
    pub budget_performance: u64,
    pub budget_efficiency: u64,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct ForecastReport {
    pub sabotage: bool,
    /// Fitted ops per chronon = k_bodies·n + k_contacts·λ.
    pub k_bodies: f64,
    pub k_contacts: f64,
    pub ns_per_op_performance: f64,
    pub ns_per_op_efficiency: f64,
    /// |log2(measured / forecast)| per unit, before sabotage.
    pub abs_log2_error: Pcts,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct SimReport {
    /// Sum over regions of chronons advanced (including work later rolled back).
    pub region_chronons: u64,
    pub region_chronons_per_wall_second: f64,
    pub present_start: f64,
    pub present_end: f64,
    /// Achieved time acceleration (chronons of the player's present per wall second).
    pub present_chronons_per_wall_second: f64,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct FrameReport {
    pub hz: f64,
    pub frames: u64,
    /// Frame thread CPU work per frame: snapshot pointer read, light-cone checks, drawing pass.
    pub work_ms: Pcts,
    /// Wall interval between frame starts (OS pacing jitter included).
    pub interval_ms: Pcts,
    /// Region-frames whose committed tick + light delay was behind the desired present.
    pub deadline_misses: u64,
    /// The same, counting only parts of small (non-giant-lane) regions.
    pub small_deadline_misses: u64,
    /// Frames where the present advanced less than the target rate (last-resort sacrifice).
    pub acceleration_drops: u64,
    pub target_rate: f64,
    /// Compute-ahead buffer: min over drawn parts of (final tick + light delay − present).
    pub buffer_chronons: Pcts,
    /// Per frame, the largest (part's final tick − global all-verified tick): how far
    /// light-cone finality publishes beyond the global frontier (0 without a hard speed).
    pub final_lead_chronons: Pcts,
    pub queue_depth: Pcts,
    pub visible_bodies_last: usize,
}

#[derive(Clone, Debug, Serialize)]
pub struct RegionReport {
    pub id: u64,
    pub bodies: usize,
    pub verified: i64,
    /// Published (final) tick: no rollback can reach it.
    pub final_tick: i64,
    /// Light delay from the region's box to the observer, in chronons (distance / c).
    pub light_delay: f64,
    /// Forecast box growth, in units of c.
    pub speed_bound_c: f64,
    /// Tick up to which the region can be computed with no rollback risk from any action the
    /// player takes now (step-6 speculation boundary).
    pub speculation_horizon: f64,
}

/// Scheduling: which round-3 changes ran, and what they are meant to move.
#[derive(Clone, Debug, Default, Serialize)]
pub struct SchedReport {
    pub lanes: bool,
    pub queues: bool,
    pub aimd: bool,
    pub eligibility: bool,
    pub hysteresis: bool,
    pub fast_finality: bool,
    pub min_region: usize,
    /// Time from a region becoming runnable to its unit's commit, by lane.
    pub latency_small_ms: Pcts,
    pub latency_giant_ms: Pcts,
    /// State-lock hold per critical section (pick + commit + publish).
    pub lock_hold_ms: Pcts,
    /// Units run from another worker's queue, and units that switched region on a worker.
    pub steals: u64,
    pub switches: u64,
    /// Strides refused because a lagging region could still reach them (EEVDF eligibility).
    pub ineligible: u64,
    pub giant_regions_last: usize,
    pub giant_workers_last: usize,
    /// Certificate stride of each region at the end, in chronons.
    pub stride_chronons: Pcts,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct FinalityReport {
    /// Per-region light-cone finality in force (needs a law-given hard speed).
    pub light_cone: bool,
    pub hard_speed: Option<i64>,
    /// Accepted snapshots above the declared hard speed (each voids light-cone finality).
    pub hard_speed_violations: u64,
    /// Global all-verified tick.
    pub frontier: i64,
}

#[derive(Clone, Debug, Default, Serialize)]
pub struct Report {
    pub mode: String,
    pub stepper: String,
    pub finality: FinalityReport,
    pub sched: SchedReport,
    pub wall_seconds: f64,
    pub bodies: usize,
    pub window: i64,
    pub regions: RegionsReport,
    pub workers: Vec<WorkerReport>,
    pub units: UnitsReport,
    pub queue_depth: Pcts,
    pub sim: SimReport,
    pub forecast: ForecastReport,
    pub frames: Option<FrameReport>,
    pub region_list: Vec<RegionReport>,
}
