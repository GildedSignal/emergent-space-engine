//! Spacetime compiler for the versioned inertial causal laboratory law.
//! The runtime compiles generators, certificates, scripted interactions and
//! family enclosures rather than stepping entities through ticks. After SAP,
//! connected components of certified overlaps are independent compile islands
//! on a finite horizon; each family/component compiles a guarded IR segment
//! until the earliest conservative invalidation. Search, swept-box construction
//! and caches are derived. Only completed causal cuts and event facts commit.
use crate::{
    archive::LiveArchive,
    geometry::{self, TickInterval},
    math::{r, Rational, Vec2},
    policy::{Broadcast, BroadcastReception},
    population::Family,
    propagator::Inertial,
    scheduler::CompositionScheduler,
    LAW_ID,
};
use serde::{Deserialize, Serialize};
use std::{
    cmp::Reverse,
    collections::{BTreeMap, BTreeSet, BinaryHeap, VecDeque},
    ops::Bound::{Excluded, Unbounded},
};

#[derive(Debug, thiserror::Error)]
pub enum EngineError {
    #[error("invalid request: {0}")]
    Invalid(String),
    #[error("unknown identity {0}")]
    UnknownIdentity(u64),
    #[error("unsupported capability: {0}")]
    Unsupported(String),
    #[error("resource limit: {0}")]
    ResourceLimit(String),
    #[error("checkpoint: {0}")]
    Checkpoint(String),
}
impl From<String> for EngineError {
    fn from(x: String) -> Self {
        Self::Invalid(x)
    }
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Body {
    pub id: u64,
    pub name: String,
    pub radius: Rational,
    pub mass: Rational,
    /// Physical, law-defined trajectory changes. Queries never add segments.
    pub segments: Vec<Inertial>,
    pub revision: u64,
    pub stop_on_contact: bool,
    pub notify_on_contact: Option<u64>,
    /// Elastic contact response (H0159): bounces off other bouncing bodies and container walls.
    #[serde(default, skip_serializing_if = "is_false")]
    pub bounce: bool,
    /// Kinetic energy owed from lattice rounding (energy carry). Only the sum over bodies is
    /// physical: total kinetic energy minus the sum of residuals is conserved by bounces.
    #[serde(default = "zero_rational", skip_serializing_if = "is_zero_rational")]
    pub energy_residual: Rational,
}
fn is_false(b: &bool) -> bool {
    !*b
}
fn zero_rational() -> Rational {
    r(0)
}
fn is_zero_rational(x: &Rational) -> bool {
    *x == r(0)
}
/// Reflecting axis-aligned container for bouncing bodies.
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Container {
    pub min: Vec2,
    pub max: Vec2,
}
/// Elastic-law configuration and ledger (`es-elastic-lattice-v0`, H0159).
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ElasticState {
    pub container: Option<Container>,
    /// Bounce responses round velocity changes to multiples of 1/Q (momentum exact, energy
    /// carried). `None` keeps exact fractions, whose size grows without bound.
    pub response_quantum: Option<i128>,
    /// Exact momentum delivered to the container walls since genesis.
    pub wall_momentum: Vec2,
}
impl Body {
    pub fn new(
        id: u64,
        name: impl Into<String>,
        flow: Inertial,
        radius: Rational,
        mass: Rational,
    ) -> Self {
        Self {
            id,
            name: name.into(),
            radius,
            mass,
            segments: vec![flow],
            revision: 0,
            stop_on_contact: false,
            notify_on_contact: None,
            bounce: false,
            energy_residual: r(0),
        }
    }
    pub fn flow(&self) -> &Inertial {
        self.segments.last().expect("validated nonempty trajectory")
    }
    pub fn at(&self, t: i128) -> Vec2 {
        self.segments
            .iter()
            .rev()
            .find(|s| s.epoch <= t)
            .unwrap_or(&self.segments[0])
            .state_at(t)
    }
    pub fn velocity_at(&self, t: i128) -> Vec2 {
        self.segments
            .iter()
            .rev()
            .find(|s| s.epoch <= t)
            .unwrap_or(&self.segments[0])
            .velocity
            .clone()
    }
    /// True when the remaining generator from `t` is a single inertial `velocity`.
    pub fn future_is_inertial(&self, t: i128, velocity: &Vec2) -> bool {
        &self.velocity_at(t) == velocity
            && self
                .segments
                .iter()
                .filter(|s| s.epoch > t)
                .all(|s| &s.velocity == velocity)
    }
    pub fn from_segments(
        id: u64,
        name: impl Into<String>,
        segments: Vec<Inertial>,
        radius: Rational,
        mass: Rational,
        revision: u64,
    ) -> Result<Self, String> {
        if segments.is_empty() {
            return Err("empty trajectory".into());
        }
        Ok(Self {
            id,
            name: name.into(),
            radius,
            mass,
            segments,
            revision,
            stop_on_contact: false,
            notify_on_contact: None,
            bounce: false,
            energy_residual: r(0),
        })
    }
    pub fn proper_time(&self, t: i128) -> Result<Rational, EngineError> {
        let mut total = r(0);
        for (i, s) in self.segments.iter().enumerate() {
            let end = self.segments.get(i + 1).map_or(t, |n| n.epoch.min(t));
            if end > s.epoch {
                total += s.proper_time_ticks(s.epoch, end)?;
            }
        }
        Ok(total)
    }
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub enum Payload {
    Ping,
    /// Scripted velocity change, independent of mass.
    Impulse { delta: Vec2 },
    /// Physical momentum transfer: velocity changes by `impulse / mass`.
    Momentum { impulse: Vec2 },
    /// Addressed scripted heading change; applied on reception, not a force law.
    SetCourse { velocity: Vec2 },
}
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Signal {
    pub id: String,
    pub source: u64,
    pub target: u64,
    pub tick: i128,
    pub position: Vec2,
    pub payload: Payload,
}
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct EventRecord {
    pub id: String,
    pub tick: i128,
    pub kind: String,
    pub subjects: Vec<u64>,
    pub predecessors: Vec<String>,
    pub detail: String,
}
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub enum Command {
    SetVelocity { velocity: Vec2 },
    SendSignal { target: u64, payload: Payload },
    /// Scripted external course change (`scripted-interaction-v1`). `at` is a
    /// committed tick; extract a family member only if its generator changes.
    SetCourse { at: i128, velocity: Vec2 },
    /// Parametric family burn (`scripted-interaction-v1`). Sugar for an
    /// immediate `SetCourseRange` over the observer's family identity range.
    FamilyPhaseBurn { at: i128, velocity: Vec2 },
    /// Shared scripted course as one range/hyperedge IR object over `{lo..=hi}`.
    /// Not a clique of per-ship commands. Extract iff a member's generator changes.
    SetCourseRange {
        lo: u64,
        hi: u64,
        at: i128,
        velocity: Vec2,
    },
    /// Shared emission toward `{lo..=hi}`. Reception is per-receiver.
    Broadcast { lo: u64, hi: u64, payload: Payload },
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RecordedIntervention {
    pub tick: i128,
    pub observer: u64,
    pub command: Command,
    pub event_id: String,
}

#[derive(Clone, Copy, Debug)]
pub struct WorkBudget {
    pub operations: usize,
    pub max_events: usize,
}
impl WorkBudget {
    pub fn new(operations: usize) -> Self {
        Self {
            operations,
            max_events: 1024,
        }
    }
}
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct AdvanceResult {
    pub committed_through: i128,
    pub target: i128,
    pub complete: bool,
    pub operations: usize,
    pub events: usize,
    pub pending_jobs: usize,
}
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ObserveResult {
    pub observations: Vec<Observation>,
    pub complete: bool,
    pub operations: usize,
    pub pending_jobs: usize,
    /// Cumulative WorkBudget operations charged to this query.
    pub charged_sensor_ops: usize,
    /// Family-range pops; this is what `max_pending_jobs` caps.
    pub refinement_steps: usize,
}
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq)]
pub struct Metrics {
    pub search_operations: u64,
    pub certified_rejections: u64,
    pub exact_leaf_queries: u64,
    pub committed_events: u64,
    pub scans: u64,
    pub broadphase_boxes: u64,
    pub broadphase_pairs: u64,
    pub box_builds: u64,
    pub sort_steps: u64,
    pub expire_ops: u64,
    pub group_ops: u64,
    pub frontier_ops: u64,
    pub commit_prep_ops: u64,
    pub aabb_compares: u64,
    pub family_range_ops: u64,
    pub sap_repairs: u64,
    pub invalidated_pairs: u64,
    pub quiet_commits: u64,
    pub pairs_total: u64,
    pub pairs_rechecked: u64,
    pub sensor_ops: u64,
    pub sensor_refinements: u64,
    /// Last SAP causal-component count (finite horizon; isolated items are islands).
    pub components: u64,
    /// Largest SAP item count in the last component grouping.
    pub component_size_max: u64,
    /// Compiled guarded family/IR segments in the last grouping.
    pub ir_nodes: u64,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CanonicalState {
    pub law: String,
    pub seed: u64,
    pub branch: String,
    pub genesis_digest: String,
    pub genesis_bodies: BTreeMap<u64, Body>,
    /// Families at genesis; retained so in-place parametric burns replay.
    #[serde(default)]
    pub genesis_families: Vec<Family>,
    pub interventions: Vec<RecordedIntervention>,
    pub clock: i128,
    pub bodies: BTreeMap<u64, Body>,
    pub families: Vec<Family>,
    pub signals: BTreeMap<String, Signal>,
    pub events: BTreeMap<String, EventRecord>,
    pub emitter_sequence: BTreeMap<u64, u64>,
    pub contacts: BTreeSet<(u64, u64, u64, u64)>,
    /// Explicit external actuator momentum accounting for burns and contact stops.
    pub actuator_momentum: Vec2,
    /// Future scripted course changes; compiled as scheduled certificates.
    #[serde(default)]
    pub scheduled_courses: BTreeMap<String, ScheduledCourse>,
    /// Shared scripted courses over an identity range; one IR object, not N commands.
    #[serde(default)]
    pub scheduled_range_courses: BTreeMap<String, ScheduledRangeCourse>,
    /// Shared broadcasts still awaiting individual receptions.
    #[serde(default)]
    pub broadcasts: BTreeMap<String, Broadcast>,
    /// Per-broadcast, per-receiver receptions. Never a single heard-it bit.
    #[serde(default)]
    pub broadcast_receptions: BTreeMap<String, BTreeMap<u64, BroadcastReception>>,
    /// Policy programs that already produced a burn for an observer.
    #[serde(default)]
    pub policy_fired: BTreeSet<(String, u64)>,
    /// Elastic law configuration and wall ledger; absent for the inertial law.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub elastic: Option<ElasticState>,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ScheduledCourse {
    pub id: String,
    pub observer: u64,
    pub tick: i128,
    pub velocity: Vec2,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ScheduledRangeCourse {
    pub id: String,
    pub lo: u64,
    pub hi: u64,
    pub tick: i128,
    pub velocity: Vec2,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum ItemKey {
    Body(u64),
    Family { index: usize, lo: u64, hi: u64 },
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Item {
    Body(u64),
    Family { index: usize, lo: u64, hi: u64 },
}
impl Item {
    fn key(&self) -> ItemKey {
        match *self {
            Item::Body(id) => ItemKey::Body(id),
            Item::Family { index, lo, hi } => ItemKey::Family { index, lo, hi },
        }
    }
    fn involves(&self, id: u64) -> bool {
        match *self {
            Item::Body(other) => other == id,
            Item::Family { lo, hi, .. } => lo <= id && id <= hi,
        }
    }
}
impl ItemKey {
    fn item(self) -> Item {
        match self {
            ItemKey::Body(id) => Item::Body(id),
            ItemKey::Family { index, lo, hi } => Item::Family { index, lo, hi },
        }
    }
    fn involves(self, id: u64) -> bool {
        self.item().involves(id)
    }
    fn involves_any(self, dirty: &BTreeSet<u64>) -> bool {
        dirty.iter().any(|&id| self.involves(id))
    }
    fn representative(self) -> u64 {
        match self {
            ItemKey::Body(id) => id,
            ItemKey::Family { lo, .. } => lo,
        }
    }
    fn intersects_range(self, lo: u64, hi: u64) -> bool {
        match self {
            ItemKey::Body(id) => lo <= id && id <= hi,
            ItemKey::Family {
                lo: a,
                hi: b,
                ..
            } => a <= hi && lo <= b,
        }
    }
}

#[derive(Clone, Debug)]
enum Job {
    Pair(Item, Item),
    Signal(String),
    Scheduled(String),
    ScheduledRange(String),
    Wall(u64),
}
#[derive(Clone, Debug)]
enum Action {
    Contact(u64, u64),
    Arrival(String),
    Course(String),
    RangeCourse(String),
    Wall(u64),
}
#[derive(Clone, Debug)]
struct Candidate {
    tick: i128,
    key: String,
    action: Action,
}
#[derive(Clone, Debug)]
struct SweptBox {
    item: Item,
    min: Vec2,
    max: Vec2,
}
#[derive(Clone, Debug)]
struct BuildingPrep {
    items: Vec<Item>,
    boxes: Vec<SweptBox>,
    next: usize,
    drift: Vec2,
    cx_min: Option<Rational>,
    cx_max: Option<Rational>,
    cy_min: Option<Rational>,
    cy_max: Option<Rational>,
}
#[derive(Clone, Debug)]
enum Prep {
    CollectBodies {
        next_after: Option<u64>,
        items: Vec<Item>,
    },
    CollectFamilies {
        family_index: usize,
        cursor: Option<u64>,
        items: Vec<Item>,
    },
    Building(Box<BuildingPrep>),
    Sorting(Box<SortPrep>),
    Sweeping {
        i: usize,
        active_j: usize,
        active: Vec<usize>,
        expire_read: Option<usize>,
        expire_write: usize,
        expired: bool,
    },
    /// Union-find over certified SAP overlaps; isolated boxes are islands.
    Grouping(Box<GroupingPrep>),
    /// One guarded family/IR segment per SAP item.
    CompilingTraces { next: usize },
    /// One pair, signal, or scheduled IR per charged step.
    EnqueuingFrontier { phase: FrontierPhase },
}

#[derive(Clone, Debug)]
struct SortPrep {
    boxes: Vec<SweptBox>,
    scratch: Vec<SweptBox>,
    x_axis: bool,
    width: usize,
    run: usize,
    i: usize,
    j: usize,
    k: usize,
    dest_is_scratch: bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum GroupPhase {
    Index,
    Union,
    Collect,
    Overlaps,
    Finish,
}

#[derive(Clone, Debug)]
struct GroupingPrep {
    parent: Vec<usize>,
    rank: Vec<u8>,
    index: BTreeMap<ItemKey, usize>,
    edge_next: Option<(ItemKey, ItemKey)>,
    collect_i: usize,
    phase: GroupPhase,
    groups: BTreeMap<usize, Vec<u64>>,
    sizes: BTreeMap<usize, usize>,
    overlapping: BTreeSet<ItemKey>,
}

#[derive(Clone, Debug)]
enum FrontierPhase {
    Pairs(Option<(ItemKey, ItemKey)>),
    Signals(Option<String>),
    Courses(Option<String>),
    Ranges(Option<String>),
    Walls(Option<u64>),
}

#[derive(Clone, Debug)]
struct BatchEffects {
    deltas: BTreeMap<u64, Vec2>,
    courses: BTreeMap<u64, Vec2>,
    stops: BTreeSet<u64>,
    records: Vec<EventRecord>,
    contacts: Vec<(u64, u64, u64, u64)>,
    received: Vec<String>,
    fired_courses: Vec<String>,
    fired_ranges: Vec<ScheduledRangeCourse>,
    notifications: Vec<(u64, u64)>,
    bounces: Vec<(u64, u64)>,
    walls: BTreeSet<u64>,
    /// Bodies changed only by bounces or walls this batch.
    elastic_only: BTreeSet<u64>,
    residuals: BTreeMap<u64, Rational>,
    wall_momentum: Vec2,
}

#[derive(Clone, Debug)]
enum CommitPrep {
    Collect {
        tick: i128,
        next: Option<String>,
        batch: Vec<Candidate>,
    },
    Accumulate {
        tick: i128,
        batch: Vec<Candidate>,
        index: usize,
        acc: BatchEffects,
    },
    ValidateAffected {
        tick: i128,
        acc: BatchEffects,
        affected: Vec<u64>,
        next: usize,
        velocities: Vec<(u64, Vec2)>,
    },
    ValidateNotes {
        tick: i128,
        acc: BatchEffects,
        velocities: Vec<(u64, Vec2)>,
        note_i: usize,
        notification_counts: BTreeMap<u64, u64>,
    },
    Publish {
        tick: i128,
        acc: BatchEffects,
        velocities: Vec<(u64, Vec2)>,
    },
}

#[derive(Clone, Debug)]
enum AfterCommit {
    Reduce {
        tick: i128,
        dirty: Vec<u64>,
        range_rebased: bool,
    },
    RebuildHeap {
        dirty: Vec<u64>,
        range_rebased: bool,
        next: Option<String>,
    },
    Apply {
        dirty: Vec<u64>,
        range_rebased: bool,
    },
    Discard,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum TraceGuard {
    Horizon,
    EnclosureOverlap,
    SetCourse,
    SetCourseRange,
    ContactStop,
    InboundSignal,
    Wall,
}

#[derive(Clone, Debug)]
struct GuardedTrace {
    valid_until: i128,
    guard: TraceGuard,
}
#[derive(Clone, Debug)]
enum Repair {
    Update { items: Vec<Item>, next: usize },
    /// `a_at` caches the dirty box's index; boxes do not move during a retest.
    Retest { dirty: Vec<ItemKey>, di: usize, j: usize, a_at: Option<usize> },
    Enqueue,
}
#[derive(Clone, Debug)]
struct Scan {
    target: i128,
    prep: Option<Prep>,
    repair: Option<Repair>,
    commit: Option<CommitPrep>,
    after: Option<AfterCommit>,
    boxes: Vec<SweptBox>,
    x_axis: bool,
    overlaps: BTreeSet<(ItemKey, ItemKey)>,
    overlap_certs: BTreeMap<(ItemKey, ItemKey), i128>,
    overlap_seen: BTreeSet<(ItemKey, ItemKey)>,
    traces: BTreeMap<ItemKey, GuardedTrace>,
    /// SAP items that share an overlap edge; used as conservative enclosure guards.
    overlapping_items: BTreeSet<ItemKey>,
    signal_certs: BTreeMap<String, i128>,
    scheduled_certs: BTreeMap<String, i128>,
    jobs: VecDeque<Job>,
    heap: BinaryHeap<Reverse<(i128, String)>>,
    candidates: BTreeMap<String, Candidate>,
    wall_certs: BTreeMap<u64, i128>,
}
impl Scan {
    fn pending_work(&self) -> usize {
        let prep = match &self.prep {
            Some(Prep::CollectBodies { items, .. }) => items.len().saturating_add(1),
            Some(Prep::CollectFamilies { items, .. }) => items.len().saturating_add(1),
            Some(Prep::Building(build)) => build.items.len().saturating_sub(build.next),
            Some(Prep::Sorting(sort)) => sort.boxes.len().saturating_sub(sort.k).max(1),
            Some(Prep::Sweeping { i, active, expire_read, expired, .. }) => {
                self.boxes.len().saturating_sub(*i)
                    + if *expired {
                        0
                    } else {
                        expire_read.map_or(active.len(), |r| active.len().saturating_sub(r))
                    }
            }
            Some(Prep::Grouping(g)) => match g.phase {
                GroupPhase::Index => self.boxes.len().saturating_sub(g.index.len()).max(1),
                GroupPhase::Union => self.overlaps.len().saturating_sub(g.index.len().min(self.overlaps.len())).max(1),
                GroupPhase::Collect => self.boxes.len().saturating_sub(g.collect_i).max(1),
                GroupPhase::Overlaps => self.overlaps.len().max(1),
                GroupPhase::Finish => 1,
            },
            Some(Prep::CompilingTraces { next }) => self.boxes.len().saturating_sub(*next).max(1),
            Some(Prep::EnqueuingFrontier { .. }) => {
                self.overlaps.len()
                    + 1
            }
            None => 0,
        };
        let repair = match &self.repair {
            Some(Repair::Update { items, next }) => items.len().saturating_sub(*next),
            Some(Repair::Retest { dirty, di, .. }) => dirty.len().saturating_sub(*di),
            Some(Repair::Enqueue) => 1,
            None => 0,
        };
        let commit = match &self.commit {
            Some(CommitPrep::Collect { batch, .. }) => batch.len().saturating_add(1),
            Some(CommitPrep::Accumulate { batch, index, .. }) => batch.len().saturating_sub(*index).max(1),
            Some(CommitPrep::ValidateAffected { affected, next, .. }) => {
                affected.len().saturating_sub(*next).max(1)
            }
            Some(CommitPrep::ValidateNotes { acc, note_i, .. }) => {
                acc.notifications.len().saturating_sub(*note_i).max(1)
            }
            Some(CommitPrep::Publish { .. }) => 1,
            None => 0,
        };
        let after = match &self.after {
            Some(AfterCommit::Reduce { .. }) => self.candidates.len().max(1),
            Some(AfterCommit::RebuildHeap { .. }) => self.candidates.len().max(1),
            Some(AfterCommit::Apply { .. } | AfterCommit::Discard) => 1,
            None => 0,
        };
        let certified = if self.candidates.is_empty() { 0 } else { 1 };
        prep + repair + commit + after + self.jobs.len() + certified
    }
}

#[derive(Clone, Debug)]
enum SensorInner {
    SelectTarget,
    OccludeFamilies(Box<FamilyOcclusion>),
}

#[derive(Clone, Debug)]
struct FamilyOcclusion {
    target: u64,
    emission_tick: i128,
    emission: Vec2,
    ray: Inertial,
    domain: TickInterval,
    family_index: usize,
    ranges: Vec<(u64, u64)>,
}

#[derive(Clone, Debug)]
struct SensorJob {
    observer: u64,
    now: i128,
    targets: Vec<u64>,
    receiver: Vec2,
    index: usize,
    inner: SensorInner,
    observations: Vec<Observation>,
    complete: bool,
    refinement_steps: usize,
    charged: usize,
}
impl SensorJob {
    fn matches(&self, observer: u64, now: i128, targets: &[u64]) -> bool {
        self.observer == observer && self.now == now && self.targets == targets
    }
    fn pending_work(&self, family_count: usize) -> usize {
        if self.complete {
            return 0;
        }
        let remaining_targets = self.targets.len().saturating_sub(self.index);
        let family_work = match &self.inner {
            SensorInner::SelectTarget => 0,
            SensorInner::OccludeFamilies(work) => {
                work.ranges.len() + family_count.saturating_sub(work.family_index)
            }
        };
        remaining_targets.saturating_add(family_work).max(1)
    }
}

#[derive(Clone, Debug)]
pub struct Engine {
    pub state: CanonicalState,
    pub metrics: Metrics,
    pending: Option<Scan>,
    sensor: Option<SensorJob>,
    /// Individually tracked ships allowed in memory. Derived from the memory budget
    /// (`resident_body_capacity`), not a fixed count; the engine refuses explicitly above it.
    pub max_resident_bodies: usize,
    pub max_pending_jobs: usize,
    /// Persistent kinetic SAP; disable only to compare against rebuild-all.
    pub incremental_sap: bool,
    /// Last finite-horizon SAP causal components (representative identities).
    /// Isolated generators are singleton islands. Empty before the first scan.
    pub causal_components: Vec<Vec<u64>>,
    /// Diagnostic coupled compiler. Not `production_law`. Not canonical gravity.
    pub coupled: Option<Box<crate::coupled_adapter::CoupledDiagnostic>>,
    /// Hosted moving compact map. Diagnostic; not canonical gravity.
    pub moving_compact: Option<Box<crate::coupled_adapter::MovingCompactDiagnostic>>,
    /// In-world received-knowledge program. Evaluated on committed receptions only.
    pub policy: Option<crate::policy::PolicyProgram>,
    /// Policy course-change during a commit requires a new scan for later contacts.
    pub(crate) force_rescan: bool,
    /// I2 unequal certified cuts. Derived; not a second physics clock.
    pub scheduler: CompositionScheduler,
    /// Sealed chunk archive handle after `seal_archive`.
    pub archive: Option<LiveArchive>,
    /// When set, SAP/commit only includes this identity range (two-region advance).
    pub(crate) scan_filter: Option<(u64, u64)>,
    /// Derived knowledge index: observer → signal arrivals. Rebuilt from
    /// events; not a canonical fact. Avoids full-history scans in
    /// `received_knowledge`.
    pub(crate) signal_arrivals: BTreeMap<u64, Vec<(i128, Vec<String>)>>,
}

pub(crate) fn digest<T: Serialize>(value: &T) -> String {
    blake3::hash(&serde_json::to_vec(value).expect("serializable canonical facts"))
        .to_hex()
        .to_string()
}
pub(crate) fn event(
    tick: i128,
    kind: &str,
    subjects: Vec<u64>,
    predecessors: Vec<String>,
    detail: String,
) -> EventRecord {
    let id = digest(&(LAW_ID, tick, kind, &subjects, &predecessors, &detail));
    EventRecord {
        id,
        tick,
        kind: kind.into(),
        subjects,
        predecessors,
        detail,
    }
}

/// Runtime memory budget from the operating-envelope target (4 GiB on the 8 GB M1).
pub const DEFAULT_MEMORY_BUDGET_BYTES: u64 = 4 << 30;
/// Measured process memory per individually tracked ship including search state
/// (scale ladder X1, H0157: 177 MB at 65,536 bodies ≈ 2.7 KB), rounded up.
pub const RESIDENT_BODY_BYTES: u64 = 3 << 10;
/// How many individually tracked ships fit in a memory budget.
pub fn resident_body_capacity(memory_budget_bytes: u64) -> usize {
    (memory_budget_bytes / RESIDENT_BODY_BYTES) as usize
}
impl Engine {
    pub fn new(
        seed: u64,
        bodies: Vec<Body>,
        mut families: Vec<Family>,
    ) -> Result<Self, EngineError> {
        families.sort_by_key(|f| f.first_id);
        let mut normalized: Vec<Family> = Vec::new();
        for f in families {
            f.validate()?;
            if let Some(a) = normalized.last_mut() {
                if a.first_id.checked_add(a.count) == Some(f.first_id)
                    && a.offset.checked_add(a.count) == Some(f.offset)
                    && a.compatible_generator(&f)
                {
                    a.count = a
                        .count
                        .checked_add(f.count)
                        .ok_or_else(|| EngineError::Invalid("family count overflow".into()))?;
                    continue;
                }
            }
            normalized.push(f);
        }
        let families = normalized;
        let genesis_families = families.clone();
        let mut map = BTreeMap::new();
        for b in bodies {
            if map.insert(b.id, b).is_some() {
                return Err(EngineError::Invalid("duplicate identity".into()));
            }
        }
        let genesis_digest = digest(&(LAW_ID, seed, &map, &families));
        let engine = Self {
            state: CanonicalState {
                law: LAW_ID.into(),
                seed,
                branch: "main".into(),
                genesis_digest,
                genesis_bodies: map.clone(),
                genesis_families,
                interventions: Vec::new(),
                clock: 0,
                bodies: map,
                families,
                signals: BTreeMap::new(),
                events: BTreeMap::new(),
                emitter_sequence: BTreeMap::new(),
                contacts: BTreeSet::new(),
                actuator_momentum: Vec2::zero(),
                scheduled_courses: BTreeMap::new(),
                scheduled_range_courses: BTreeMap::new(),
                broadcasts: BTreeMap::new(),
                broadcast_receptions: BTreeMap::new(),
                policy_fired: BTreeSet::new(),
                elastic: None,
            },
            metrics: Metrics::default(),
            pending: None,
            sensor: None,
            max_resident_bodies: resident_body_capacity(DEFAULT_MEMORY_BUDGET_BYTES),
            max_pending_jobs: 1_000_000,
            incremental_sap: true,
            causal_components: Vec::new(),
            coupled: None,
            moving_compact: None,
            policy: None,
            force_rescan: false,
            scheduler: CompositionScheduler::default(),
            archive: None,
            scan_filter: None,
            signal_arrivals: BTreeMap::new(),
        };
        if engine.state.bodies.len() > engine.max_resident_bodies {
            // Refuse up front instead of accepting a world that fails at its first event.
            return Err(EngineError::ResourceLimit(
                "individually tracked ships exceed the memory budget".into(),
            ));
        }
        engine.validate()?;
        Ok(engine)
    }
    /// Configure the elastic law (H0159) before any advance: an optional reflecting container
    /// and an optional response quantum Q (velocity lattice 1/Q). Bodies opt in with `bounce`.
    pub fn with_elastic(
        mut self,
        container: Option<Container>,
        response_quantum: Option<i128>,
    ) -> Result<Self, EngineError> {
        if self.state.clock != 0 || !self.state.events.is_empty() {
            return Err(EngineError::Invalid("elastic law must be set at genesis".into()));
        }
        if response_quantum.is_some_and(|q| q <= 0) {
            return Err(EngineError::Invalid("response quantum must be positive".into()));
        }
        if let Some(c) = &container {
            if c.min.x >= c.max.x || c.min.y >= c.max.y {
                return Err(EngineError::Invalid("empty container".into()));
            }
        }
        self.state.elastic = Some(ElasticState {
            container,
            response_quantum,
            wall_momentum: Vec2::zero(),
        });
        Ok(self)
    }
    pub fn validate(&self) -> Result<(), EngineError> {
        if self.state.law != LAW_ID {
            return Err(EngineError::Unsupported(format!(
                "law {} requires a compatible evaluator",
                self.state.law
            )));
        }
        if self.state.clock < 0 {
            return Err(EngineError::Invalid("negative committed cut".into()));
        }
        for family in &self.state.families {
            family.validate()?;
            if !family.self_disjoint() {
                return Err(EngineError::Unsupported(
                    "internally overlapping affine family must be materialized".into(),
                ));
            }
        }
        // Random identity access relies on this canonical ordering after restore too.
        for pair in self.state.families.windows(2) {
            let (a, b) = (&pair[0], &pair[1]);
            if b.first_id <= a.first_id + (a.count - 1) {
                return Err(EngineError::Invalid("overlapping identity ranges".into()));
            }
        }
        for (id, b) in &self.state.bodies {
            if *id != b.id || b.segments.is_empty() || b.radius < r(0) || b.mass <= r(0) {
                return Err(EngineError::Invalid("invalid body".into()));
            }
            let mut prev = None;
            for s in &b.segments {
                Inertial::new(s.epoch, s.origin.clone(), s.velocity.clone())?;
                if prev.is_some_and(|p| p > s.epoch) {
                    return Err(EngineError::Invalid("unordered trajectory history".into()));
                }
                prev = Some(s.epoch);
            }
        }
        Ok(())
    }
    pub fn in_scan_filter(&self, id: u64) -> bool {
        self.scan_filter
            .map(|(lo, hi)| id >= lo && id <= hi)
            .unwrap_or(true)
    }

    pub(crate) fn clear_pending_scan(&mut self) {
        self.pending = None;
    }

    fn range_intersects_filter(&self, lo: u64, hi: u64) -> bool {
        self.scan_filter
            .map(|(flo, fhi)| lo <= fhi && flo <= hi)
            .unwrap_or(true)
    }

    pub fn logical_count(&self) -> u128 {
        self.state
            .families
            .iter()
            .map(|f| f.count as u128)
            .sum::<u128>()
            + self
                .state
                .bodies
                .keys()
                .filter(|id| self.family_for(**id).is_none())
                .count() as u128
    }
    pub fn inspect(&self, id: u64, t: i128) -> Result<Body, EngineError> {
        if t < 0 || t > self.state.clock {
            return Err(EngineError::Invalid(
                "inspection requires a committed time; advance first".into(),
            ));
        }
        self.decode(id)
    }
    pub fn position(&self, id: u64, t: i128) -> Result<Vec2, EngineError> {
        Ok(self.inspect(id, t)?.at(t))
    }
    pub fn decode(&self, id: u64) -> Result<Body, EngineError> {
        if let Some(b) = self.state.bodies.get(&id) {
            return Ok(b.clone());
        }
        if let Some(f) = self.family_for(id) {
            let segments = f.member_segments(id).ok_or_else(|| {
                EngineError::Invalid("family member decode failed".into())
            })?;
            return Ok(Body::from_segments(
                id,
                format!("{} · {}", f.name, id),
                segments,
                f.radius.clone(),
                f.mass.clone(),
                f.revision,
            )?);
        }
        Err(EngineError::UnknownIdentity(id))
    }
    fn family_index(&self, id: u64) -> Option<usize> {
        let n = self.state.families.partition_point(|f| f.first_id <= id);
        n.checked_sub(1).and_then(|i| {
            self.state
                .families
                .get(i)
                .filter(|f| f.contains(id))
                .map(|_| i)
        })
    }
    fn family_for(&self, id: u64) -> Option<&Family> {
        self.family_index(id)
            .and_then(|i| self.state.families.get(i))
    }
    fn materialize(&mut self, id: u64) -> Result<(), EngineError> {
        if !self.state.bodies.contains_key(&id) {
            if self.state.bodies.len() >= self.max_resident_bodies {
                return Err(EngineError::ResourceLimit(
                    "distinct ship capacity reached".into(),
                ));
            }
            let b = self.decode(id)?;
            self.state.bodies.insert(id, b);
        }
        Ok(())
    }
    pub fn intervene(&mut self, observer: u64, command: Command) -> Result<String, EngineError> {
        self.sensor = None;
        let id = self.apply_command(observer, command.clone())?;
        self.state.interventions.push(RecordedIntervention {
            tick: self.state.clock,
            observer,
            command,
            event_id: id.clone(),
        });
        Ok(id)
    }
    fn apply_command(&mut self, observer: u64, command: Command) -> Result<String, EngineError> {
        let body = self.decode(observer)?;
        let t = self.state.clock;
        match command {
            Command::SetVelocity { velocity } => {
                Inertial::new(t, body.at(t), velocity.clone())?;
                let before = body.flow().velocity.clone();
                self.apply_course_change(observer, t, velocity.clone())?;
                let e = event(
                    t,
                    "burn",
                    vec![observer],
                    vec![],
                    digest(&(before, velocity, self.state.interventions.len())),
                );
                let id = e.id.clone();
                self.state.events.insert(id.clone(), e);
                self.invalidate_or_repair(&[observer]);
                Ok(id)
            }
            Command::SetCourse { at, velocity } => {
                Inertial::new(at, body.at(at), velocity.clone())?;
                if at < t {
                    return Err(EngineError::Invalid(
                        "cannot schedule a course in the past".into(),
                    ));
                }
                if at == t {
                    let before = body.flow().velocity.clone();
                    self.apply_course_change(observer, t, velocity.clone())?;
                    let e = event(
                        t,
                        "burn",
                        vec![observer],
                        vec![],
                        digest(&(before, velocity, self.state.interventions.len())),
                    );
                    let id = e.id.clone();
                    self.state.events.insert(id.clone(), e);
                    self.invalidate_or_repair(&[observer]);
                    return Ok(id);
                }
                if self.state.scheduled_courses.len()
                    + self.state.scheduled_range_courses.len()
                    + self.state.signals.len()
                    >= self.max_pending_jobs
                {
                    return Err(EngineError::ResourceLimit(
                        "pending scripted course capacity reached".into(),
                    ));
                }
                let id = digest(&(
                    LAW_ID,
                    self.state.seed,
                    t,
                    observer,
                    at,
                    &velocity,
                    self.state.interventions.len(),
                ));
                self.state.scheduled_courses.insert(
                    id.clone(),
                    ScheduledCourse {
                        id: id.clone(),
                        observer,
                        tick: at,
                        velocity,
                    },
                );
                let e = event(
                    t,
                    "course_scheduled",
                    vec![observer],
                    vec![id.clone()],
                    format!("course {id}"),
                );
                self.state.events.insert(e.id.clone(), e);
                if let Some(scan) = self.pending.as_mut() {
                    if scan.prep.is_none() && scan.repair.is_none() {
                        scan.jobs.push_back(Job::Scheduled(id.clone()));
                    }
                }
                Ok(id)
            }
            Command::SendSignal { target, payload } => {
                self.decode(target)?;
                if let Payload::SetCourse { velocity } = &payload {
                    Inertial::new(t, Vec2::zero(), velocity.clone())?;
                }
                if self.state.signals.len() >= self.max_pending_jobs {
                    return Err(EngineError::ResourceLimit(
                        "pending signal capacity reached".into(),
                    ));
                }
                let seq = *self.state.emitter_sequence.get(&observer).unwrap_or(&0);
                let id = digest(&(LAW_ID, self.state.seed, t, observer, target, seq, &payload));
                let next = seq.checked_add(1).ok_or_else(|| {
                    EngineError::ResourceLimit("emitter sequence exhausted".into())
                })?;
                self.state.emitter_sequence.insert(observer, next);
                self.state.signals.insert(
                    id.clone(),
                    Signal {
                        id: id.clone(),
                        source: observer,
                        target,
                        tick: t,
                        position: body.at(t),
                        payload,
                    },
                );
                let e = event(
                    t,
                    "signal_emitted",
                    vec![observer, target],
                    vec![id.clone()],
                    format!("signal {id}"),
                );
                self.state.events.insert(e.id.clone(), e);
                if let Some(scan) = self.pending.as_mut() {
                    if scan.prep.is_none() && scan.repair.is_none() {
                        scan.jobs.push_back(Job::Signal(id.clone()));
                    } else {
                        self.pending = None;
                    }
                }
                Ok(id)
            }
            Command::FamilyPhaseBurn { at, velocity } => {
                let index = self.family_index(observer).ok_or_else(|| {
                    EngineError::Invalid(
                        "FamilyPhaseBurn requires an unextracted family identity".into(),
                    )
                })?;
                if self.state.bodies.contains_key(&observer) {
                    return Err(EngineError::Invalid(
                        "FamilyPhaseBurn requires an unextracted family identity".into(),
                    ));
                }
                let (lo, hi) = {
                    let family = &self.state.families[index];
                    (family.first_id, family.last_id())
                };
                self.schedule_or_apply_range(lo, hi, at, velocity, "family_burn", vec![observer])
            }
            Command::SetCourseRange {
                lo,
                hi,
                at,
                velocity,
            } => self.schedule_or_apply_range(lo, hi, at, velocity, "range_burn", vec![lo, hi]),
            Command::Broadcast { lo, hi, payload } => {
                self.emit_broadcast(observer, lo, hi, payload, t)
            }
        }
    }
    /// Extract a family member only when its future generator actually changes.
    pub(crate) fn apply_course_change(
        &mut self,
        id: u64,
        t: i128,
        velocity: Vec2,
    ) -> Result<(), EngineError> {
        self.sensor = None;
        let body = self.decode(id)?;
        let unchanged = body.future_is_inertial(t, &velocity);
        let still_generated =
            self.family_for(id).is_some() && !self.state.bodies.contains_key(&id);
        if unchanged && still_generated {
            return Ok(());
        }
        self.materialize(id)?;
        self.set_velocity(id, t, velocity)
    }
    fn ensure_range_known(&self, lo: u64, hi: u64) -> Result<(), EngineError> {
        if lo > hi {
            return Err(EngineError::Invalid("course range must satisfy lo <= hi".into()));
        }
        let mut cur = lo;
        while cur <= hi {
            if let Some(f) = self.family_for(cur) {
                cur = f.last_id().saturating_add(1);
                continue;
            }
            if self.state.bodies.contains_key(&cur) {
                cur = cur.saturating_add(1);
                continue;
            }
            return Err(EngineError::UnknownIdentity(cur));
        }
        Ok(())
    }
    fn schedule_or_apply_range(
        &mut self,
        lo: u64,
        hi: u64,
        at: i128,
        velocity: Vec2,
        kind: &str,
        subjects: Vec<u64>,
    ) -> Result<String, EngineError> {
        Inertial::new(at, Vec2::zero(), velocity.clone())?;
        self.ensure_range_known(lo, hi)?;
        let t = self.state.clock;
        if at < t {
            return Err(EngineError::Invalid(
                "cannot schedule a course in the past".into(),
            ));
        }
        if at == t {
            self.apply_range_course(lo, hi, at, velocity.clone())?;
            let e = event(
                t,
                kind,
                subjects,
                vec![],
                digest(&(lo, hi, velocity, self.state.interventions.len())),
            );
            let id = e.id.clone();
            self.state.events.insert(id.clone(), e);
            self.pending = None;
            return Ok(id);
        }
        if self.state.scheduled_courses.len()
            + self.state.scheduled_range_courses.len()
            + self.state.signals.len()
            >= self.max_pending_jobs
        {
            return Err(EngineError::ResourceLimit(
                "pending scripted course capacity reached".into(),
            ));
        }
        let id = digest(&(
            LAW_ID,
            self.state.seed,
            t,
            lo,
            hi,
            at,
            &velocity,
            self.state.interventions.len(),
        ));
        self.state.scheduled_range_courses.insert(
            id.clone(),
            ScheduledRangeCourse {
                id: id.clone(),
                lo,
                hi,
                tick: at,
                velocity,
            },
        );
        let e = event(
            t,
            "range_course_scheduled",
            subjects,
            vec![id.clone()],
            format!("range-course {id}"),
        );
        self.state.events.insert(e.id.clone(), e);
        if let Some(scan) = self.pending.as_mut() {
            if scan.prep.is_none() && scan.repair.is_none() {
                scan.jobs.push_back(Job::ScheduledRange(id.clone()));
            }
        }
        Ok(id)
    }
    /// Apply one range/hyperedge course. Family partitions update in place.
    /// Already-extracted members in the range are updated without re-grouping
    /// merely adjacent identities into one generator.
    fn apply_range_course(
        &mut self,
        lo: u64,
        hi: u64,
        at: i128,
        velocity: Vec2,
    ) -> Result<(), EngineError> {
        self.sensor = None;
        self.ensure_range_known(lo, hi)?;
        let extracted: Vec<u64> = self.state.bodies.range(lo..=hi).map(|(&id, _)| id).collect();
        for id in extracted {
            self.apply_course_change(id, at, velocity.clone())?;
        }
        let mut keep = Vec::new();
        let mut rebased = Vec::new();
        for f in self.state.families.drain(..) {
            if f.last_id() < lo || f.first_id > hi {
                keep.push(f);
                continue;
            }
            let (remainders, mid) = f.split_off_range(lo, hi)?;
            keep.extend(remainders);
            for part in mid.phase_aligned_parts(at)? {
                rebased.push(part.rebase_as_affine(at, velocity.clone())?);
            }
        }
        keep.extend(rebased);
        keep.sort_by_key(|f| f.first_id);
        self.state.families = Self::normalize_equivalent_families(keep)?;
        self.pending = None;
        Ok(())
    }
    /// Merge only adjacent partitions that share a generator or an exact affine
    /// future. Causal adjacency or permutation alone is not an equivalence group.
    fn normalize_equivalent_families(families: Vec<Family>) -> Result<Vec<Family>, EngineError> {
        let mut normalized: Vec<Family> = Vec::new();
        for f in families {
            f.validate()?;
            if !f.self_disjoint() {
                return Err(EngineError::Unsupported(
                    "internally overlapping affine family must be materialized".into(),
                ));
            }
            if let Some(a) = normalized.last_mut() {
                if let Some(joined) = Family::exact_remerge(a, &f) {
                    *a = joined;
                    continue;
                }
            }
            normalized.push(f);
        }
        Ok(normalized)
    }
    fn set_velocity(&mut self, id: u64, t: i128, velocity: Vec2) -> Result<(), EngineError> {
        self.decode(id)?
            .revision
            .checked_add(1)
            .ok_or_else(|| EngineError::ResourceLimit("trajectory revision exhausted".into()))?;
        self.materialize(id)?;
        let b = self.state.bodies.get_mut(&id).unwrap();
        let next = Inertial::new(t, b.at(t), velocity.clone())?;
        self.state.actuator_momentum = self.state.actuator_momentum.clone()
            + (b.flow().velocity.clone() - velocity) * b.mass.clone();
        // Several simultaneous effects create one physical segment.
        if b.flow().epoch == t && b.segments.len() > 1 {
            b.segments.pop();
        }
        b.segments.push(next);
        b.revision += 1;
        Ok(())
    }
    fn begin_scan(&mut self, target: i128) -> Result<(), EngineError> {
        if self.state.bodies.len() + self.state.families.len() > self.max_pending_jobs {
            return Err(EngineError::ResourceLimit(
                "broad-phase object budget exceeded".into(),
            ));
        }
        self.pending = Some(Scan {
            target,
            prep: Some(Prep::CollectBodies {
                next_after: None,
                items: Vec::new(),
            }),
            repair: None,
            commit: None,
            after: None,
            boxes: Vec::new(),
            x_axis: true,
            overlaps: BTreeSet::new(),
            overlap_certs: BTreeMap::new(),
            overlap_seen: BTreeSet::new(),
            traces: BTreeMap::new(),
            overlapping_items: BTreeSet::new(),
            signal_certs: BTreeMap::new(),
            scheduled_certs: BTreeMap::new(),
            jobs: VecDeque::new(),
            heap: BinaryHeap::new(),
            candidates: BTreeMap::new(),
            wall_certs: BTreeMap::new(),
        });
        self.metrics.scans += 1;
        Ok(())
    }
    fn pair_key(a: ItemKey, b: ItemKey) -> (ItemKey, ItemKey) {
        if a <= b {
            (a, b)
        } else {
            (b, a)
        }
    }
    fn axis_min(b: &SweptBox, x_axis: bool) -> &Rational {
        if x_axis {
            &b.min.x
        } else {
            &b.min.y
        }
    }
    fn build_box(&self, item: Item, target: i128, drift: &Vec2) -> Result<SweptBox, EngineError> {
        if let Item::Body(id) = &item {
            let b = self.decode(*id)?;
            if b.segments.len() == 1 {
                return self.swept_from_inertials(
                    item,
                    b.flow(),
                    b.flow(),
                    &b.radius,
                    target,
                    drift,
                );
            }
        }
        let t0 = self.state.clock;
        let t1 = target;
        let (samples, rad) = self.item_samples(&item, t0, t1)?;
        let mut min_x = None;
        let mut max_x = None;
        let mut min_y = None;
        let mut max_y = None;
        for (t, p) in samples {
            let shifted = p - drift.clone() * r(t);
            min_x = Some(min_x.map_or_else(|| shifted.x.clone(), |v: Rational| v.min(shifted.x.clone())));
            max_x = Some(max_x.map_or_else(|| shifted.x.clone(), |v: Rational| v.max(shifted.x.clone())));
            min_y = Some(min_y.map_or_else(|| shifted.y.clone(), |v: Rational| v.min(shifted.y.clone())));
            max_y = Some(max_y.map_or_else(|| shifted.y.clone(), |v: Rational| v.max(shifted.y.clone())));
        }
        Ok(SweptBox {
            item,
            min: Vec2 {
                x: min_x.unwrap() - &rad,
                y: min_y.unwrap() - &rad,
            },
            max: Vec2 {
                x: max_x.unwrap() + &rad,
                y: max_y.unwrap() + &rad,
            },
        })
    }
    fn swept_from_inertials(
        &self,
        item: Item,
        a: &Inertial,
        b: &Inertial,
        rad: &Rational,
        target: i128,
        drift: &Vec2,
    ) -> Result<SweptBox, EngineError> {
        let mut min_x = None;
        let mut max_x = None;
        let mut min_y = None;
        let mut max_y = None;
        for flow in [a, b] {
            for t in [self.state.clock, target] {
                let p = flow.state_at(t) - drift.clone() * r(t);
                min_x = Some(min_x.map_or_else(|| p.x.clone(), |v: Rational| v.min(p.x.clone())));
                max_x = Some(max_x.map_or_else(|| p.x.clone(), |v: Rational| v.max(p.x.clone())));
                min_y = Some(min_y.map_or_else(|| p.y.clone(), |v: Rational| v.min(p.y.clone())));
                max_y = Some(max_y.map_or_else(|| p.y.clone(), |v: Rational| v.max(p.y.clone())));
            }
        }
        Ok(SweptBox {
            item,
            min: Vec2 {
                x: min_x.unwrap() - rad,
                y: min_y.unwrap() - rad,
            },
            max: Vec2 {
                x: max_x.unwrap() + rad,
                y: max_y.unwrap() + rad,
            },
        })
    }
    fn item_samples(
        &self,
        item: &Item,
        t0: i128,
        t1: i128,
    ) -> Result<(Vec<(i128, Vec2)>, Rational), EngineError> {
        match item {
            Item::Body(id) => {
                let b = self.decode(*id)?;
                if b.segments.len() == 1 {
                    return Ok((vec![(t0, b.at(t0)), (t1, b.at(t1))], b.radius));
                }
                let mut samples = vec![(t0, b.at(t0)), (t1, b.at(t1))];
                for s in &b.segments {
                    if s.epoch > t0 && s.epoch <= t1 {
                        samples.push((s.epoch, b.at(s.epoch)));
                    }
                }
                Ok((samples, b.radius))
            }
            Item::Family { index, lo, hi } => {
                let f = &self.state.families[*index];
                let samples = f.range_samples(*lo, *hi, t0, t1).ok_or_else(|| {
                    EngineError::Invalid("family enclosure failed".into())
                })?;
                Ok((samples, f.radius.clone()))
            }
        }
    }
    fn item_positions(
        &self,
        item: &Item,
        t: i128,
    ) -> Result<(Vec<Vec2>, Rational), EngineError> {
        match item {
            Item::Body(id) => {
                let b = self.decode(*id)?;
                Ok((vec![b.at(t)], b.radius))
            }
            Item::Family { index, lo, hi } => {
                let f = &self.state.families[*index];
                let samples = f.range_samples(*lo, *hi, t, t).ok_or_else(|| {
                    EngineError::Invalid("family enclosure failed".into())
                })?;
                Ok((
                    samples.into_iter().map(|(_, p)| p).collect(),
                    f.radius.clone(),
                ))
            }
        }
    }
    fn insert_sorted(boxes: &mut Vec<SweptBox>, item: SweptBox, x_axis: bool) {
        let pos = boxes.partition_point(|b| {
            Self::axis_min(b, x_axis) <= Self::axis_min(&item, x_axis)
        });
        boxes.insert(pos, item);
    }
    fn aabb_overlap(a: &SweptBox, b: &SweptBox) -> bool {
        a.min.x <= b.max.x
            && b.min.x <= a.max.x
            && a.min.y <= b.max.y
            && b.min.y <= a.max.y
    }
    fn enqueue_pair(
        &mut self,
        scan: &mut Scan,
        a: ItemKey,
        b: ItemKey,
    ) -> Result<(), EngineError> {
        let key = Self::pair_key(a, b);
        if scan
            .overlap_certs
            .get(&key)
            .is_some_and(|cert| *cert >= scan.target)
        {
            return Ok(());
        }
        if scan.jobs.len() >= self.max_pending_jobs {
            return Err(EngineError::ResourceLimit(
                "dense interaction frontier exceeds job capacity".into(),
            ));
        }
        if !scan.overlap_seen.insert(key) {
            self.metrics.pairs_rechecked += 1;
        }
        scan.jobs.push_back(Job::Pair(a.item(), b.item()));
        Ok(())
    }
    fn record_overlap(&mut self, scan: &mut Scan, a: ItemKey, b: ItemKey) {
        let key = Self::pair_key(a, b);
        if scan.overlaps.insert(key) {
            self.metrics.pairs_total += 1;
        }
    }
    fn remove_item_overlaps(&mut self, scan: &mut Scan, key: ItemKey) {
        let before = scan.overlaps.len();
        scan.overlaps.retain(|(a, b)| *a != key && *b != key);
        scan.overlap_certs.retain(|(a, b), _| *a != key && *b != key);
        self.metrics.invalidated_pairs += (before - scan.overlaps.len()) as u64;
    }
    fn candidate_involves(&self, candidate: &Candidate, dirty: &BTreeSet<u64>) -> bool {
        match &candidate.action {
            Action::Contact(a, b) => dirty.contains(a) || dirty.contains(b),
            Action::Arrival(id) => self
                .state
                .signals
                .get(id)
                .is_some_and(|s| dirty.contains(&s.target)),
            Action::Course(_) => false,
            Action::RangeCourse(_) => false,
            Action::Wall(id) => dirty.contains(id),
        }
    }
    fn invalidate_dirty_certificates(&mut self, scan: &mut Scan, dirty: &[u64]) {
        let dirty_set: BTreeSet<u64> = dirty.iter().copied().collect();
        scan.candidates
            .retain(|_, c| !self.candidate_involves(c, &dirty_set));
        scan.heap.clear();
        for (key, c) in &scan.candidates {
            scan.heap.push(Reverse((c.tick, key.clone())));
        }
        scan.overlap_certs
            .retain(|pair, _| !pair.0.involves_any(&dirty_set) && !pair.1.involves_any(&dirty_set));
        scan.wall_certs.retain(|id, _| !dirty_set.contains(id));
        scan.signal_certs.retain(|id, _| {
            self.state
                .signals
                .get(id)
                .is_none_or(|s| !dirty_set.contains(&s.target))
        });
    }
    fn frontier_needs_resume(&self, scan: &Scan) -> bool {
        self.wall_frontier_pending(scan) || scan.overlaps.iter().any(|key| {
            scan.overlap_certs
                .get(key)
                .is_none_or(|cert| *cert < scan.target)
        }) || self.state.signals.keys().any(|id| {
            let cand = format!("signal:{id}");
            !scan.candidates.contains_key(&cand)
                && scan
                    .signal_certs
                    .get(id)
                    .is_none_or(|cert| *cert < scan.target)
        }) || self.state.scheduled_courses.keys().any(|id| {
            let cand = format!("course:{id}");
            !scan.candidates.contains_key(&cand)
                && scan
                    .scheduled_certs
                    .get(id)
                    .is_none_or(|cert| *cert < scan.target)
        }) || self.state.scheduled_range_courses.keys().any(|id| {
            let cand = format!("rcourse:{id}");
            !scan.candidates.contains_key(&cand)
                && scan
                    .scheduled_certs
                    .get(id)
                    .is_none_or(|cert| *cert < scan.target)
        })
    }
    fn start_frontier(scan: &mut Scan) {
        let first = scan.overlaps.iter().next().copied();
        scan.prep = Some(Prep::EnqueuingFrontier {
            phase: FrontierPhase::Pairs(first),
        });
    }
    fn wall_frontier_pending(&self, scan: &Scan) -> bool {
        self.state.elastic.as_ref().is_some_and(|el| el.container.is_some())
            && self.state.bodies.iter().any(|(id, b)| {
                b.bounce
                    && !scan.candidates.contains_key(&format!("wall:{id:020}"))
                    && scan.wall_certs.get(id).is_none_or(|c| *c < scan.target)
            })
    }
    fn first_bouncer_after(&self, after: Option<u64>) -> Option<u64> {
        let mut it: Box<dyn Iterator<Item = (&u64, &Body)>> = match after {
            None => Box::new(self.state.bodies.iter()),
            Some(id) => Box::new(self.state.bodies.range((Excluded(id), Unbounded))),
        };
        it.find(|(_, b)| b.bounce).map(|(&id, _)| id)
    }
    /// First tick in [start, end] at which the body touches or is beyond a container wall while
    /// moving outward. Linear motion, exact.
    fn first_wall_tick(b: &Body, c: &Container, clock: i128, start: i128, end: i128) -> Option<i128> {
        let p = b.at(clock);
        let v = b.velocity_at(clock);
        let mut best: Option<i128> = None;
        for (x, vx, lo, hi) in [(&p.x, &v.x, &c.min.x, &c.max.x), (&p.y, &v.y, &c.min.y, &c.max.y)] {
            let tick = if *vx < r(0) {
                let w = lo + &b.radius;
                if *x <= w {
                    Some(start)
                } else {
                    let dt = ((x - &w) / (-vx.clone())).ceil().to_integer();
                    i128::try_from(dt).ok().map(|d| (clock + d).max(start))
                }
            } else if *vx > r(0) {
                let w = hi - &b.radius;
                if *x >= w {
                    Some(start)
                } else {
                    let dt = ((&w - x) / vx.clone()).ceil().to_integer();
                    i128::try_from(dt).ok().map(|d| (clock + d).max(start))
                }
            } else {
                None
            };
            if let Some(t) = tick.filter(|t| *t <= end) {
                best = Some(best.map_or(t, |b: i128| b.min(t)));
            }
        }
        best
    }
    fn step_enqueue_frontier(
        &mut self,
        scan: &mut Scan,
        phase: FrontierPhase,
    ) -> Result<(), EngineError> {
        self.metrics.frontier_ops += 1;
        match phase {
            FrontierPhase::Pairs(next) => {
                if let Some((a, b)) = next {
                    self.enqueue_pair(scan, a, b)?;
                    let following = scan
                        .overlaps
                        .range((Excluded((a, b)), Unbounded))
                        .next()
                        .copied();
                    scan.prep = Some(Prep::EnqueuingFrontier {
                        phase: FrontierPhase::Pairs(following),
                    });
                } else {
                    scan.prep = Some(Prep::EnqueuingFrontier {
                        phase: FrontierPhase::Signals(
                            self.state.signals.keys().next().cloned(),
                        ),
                    });
                }
            }
            FrontierPhase::Signals(next) => {
                if let Some(id) = next {
                    let following = self
                        .state
                        .signals
                        .range((Excluded(id.clone()), Unbounded))
                        .next()
                        .map(|(k, _)| k.clone());
                    let cand = format!("signal:{id}");
                    if !scan.candidates.contains_key(&cand)
                        && scan
                            .signal_certs
                            .get(&id)
                            .is_none_or(|cert| *cert < scan.target)
                    {
                        let target_ok = self
                            .state
                            .signals
                            .get(&id)
                            .is_some_and(|s| self.in_scan_filter(s.target));
                        if target_ok {
                            if scan.jobs.len() >= self.max_pending_jobs {
                                return Err(EngineError::ResourceLimit(
                                    "combined frontier exceeds job capacity".into(),
                                ));
                            }
                            scan.jobs.push_back(Job::Signal(id));
                        }
                    }
                    scan.prep = Some(Prep::EnqueuingFrontier {
                        phase: FrontierPhase::Signals(following),
                    });
                } else {
                    scan.prep = Some(Prep::EnqueuingFrontier {
                        phase: FrontierPhase::Courses(
                            self.state.scheduled_courses.keys().next().cloned(),
                        ),
                    });
                }
            }
            FrontierPhase::Courses(next) => {
                if let Some(id) = next {
                    let following = self
                        .state
                        .scheduled_courses
                        .range((Excluded(id.clone()), Unbounded))
                        .next()
                        .map(|(k, _)| k.clone());
                    let cand = format!("course:{id}");
                    if !scan.candidates.contains_key(&cand)
                        && scan
                            .scheduled_certs
                            .get(&id)
                            .is_none_or(|cert| *cert < scan.target)
                    {
                        if scan.jobs.len() >= self.max_pending_jobs {
                            return Err(EngineError::ResourceLimit(
                                "combined frontier exceeds job capacity".into(),
                            ));
                        }
                        scan.jobs.push_back(Job::Scheduled(id));
                    }
                    scan.prep = Some(Prep::EnqueuingFrontier {
                        phase: FrontierPhase::Courses(following),
                    });
                } else {
                    scan.prep = Some(Prep::EnqueuingFrontier {
                        phase: FrontierPhase::Ranges(
                            self.state.scheduled_range_courses.keys().next().cloned(),
                        ),
                    });
                }
            }
            FrontierPhase::Ranges(next) => {
                if let Some(id) = next {
                    let following = self
                        .state
                        .scheduled_range_courses
                        .range((Excluded(id.clone()), Unbounded))
                        .next()
                        .map(|(k, _)| k.clone());
                    let cand = format!("rcourse:{id}");
                    if !scan.candidates.contains_key(&cand)
                        && scan
                            .scheduled_certs
                            .get(&id)
                            .is_none_or(|cert| *cert < scan.target)
                    {
                        if scan.jobs.len() >= self.max_pending_jobs {
                            return Err(EngineError::ResourceLimit(
                                "combined frontier exceeds job capacity".into(),
                            ));
                        }
                        scan.jobs.push_back(Job::ScheduledRange(id));
                    }
                    scan.prep = Some(Prep::EnqueuingFrontier {
                        phase: FrontierPhase::Ranges(following),
                    });
                } else if self.state.elastic.as_ref().is_some_and(|el| el.container.is_some()) {
                    scan.prep = Some(Prep::EnqueuingFrontier {
                        phase: FrontierPhase::Walls(self.first_bouncer_after(None)),
                    });
                } else {
                    scan.prep = None;
                }
            }
            FrontierPhase::Walls(next) => {
                if let Some(id) = next {
                    let following = self.first_bouncer_after(Some(id));
                    let cand = format!("wall:{id:020}");
                    if !scan.candidates.contains_key(&cand)
                        && scan.wall_certs.get(&id).is_none_or(|cert| *cert < scan.target)
                        && self.in_scan_filter(id)
                    {
                        if scan.jobs.len() >= self.max_pending_jobs {
                            return Err(EngineError::ResourceLimit(
                                "combined frontier exceeds job capacity".into(),
                            ));
                        }
                        scan.jobs.push_back(Job::Wall(id));
                    }
                    scan.prep = Some(Prep::EnqueuingFrontier {
                        phase: FrontierPhase::Walls(following),
                    });
                } else {
                    scan.prep = None;
                }
            }
        }
        Ok(())
    }
    fn union_parent(parent: &mut [usize], mut x: usize) -> usize {
        while parent[x] != x {
            let p = parent[x];
            parent[x] = parent[p];
            x = p;
        }
        x
    }
    fn start_grouping(scan: &mut Scan) {
        let n = scan.boxes.len();
        scan.prep = Some(Prep::Grouping(Box::new(GroupingPrep {
            parent: (0..n).collect(),
            rank: vec![0u8; n],
            index: BTreeMap::new(),
            edge_next: scan.overlaps.iter().next().copied(),
            collect_i: 0,
            phase: if n == 0 {
                GroupPhase::Finish
            } else {
                GroupPhase::Index
            },
            groups: BTreeMap::new(),
            sizes: BTreeMap::new(),
            overlapping: BTreeSet::new(),
        })));
    }
    fn step_grouping(&mut self, scan: &mut Scan, mut g: GroupingPrep) {
        self.metrics.group_ops += 1;
        match g.phase {
            GroupPhase::Index => {
                let i = g.index.len();
                if i >= scan.boxes.len() {
                    g.phase = GroupPhase::Union;
                } else {
                    g.index.insert(scan.boxes[i].item.key(), i);
                }
                scan.prep = Some(Prep::Grouping(Box::new(g)));
            }
            GroupPhase::Union => {
                if let Some((a, b)) = g.edge_next {
                    if let Some((&ia, &ib)) = g.index.get(&a).zip(g.index.get(&b)) {
                        let mut ra = Self::union_parent(&mut g.parent, ia);
                        let mut rb = Self::union_parent(&mut g.parent, ib);
                        if ra != rb {
                            if g.rank[ra] < g.rank[rb] {
                                std::mem::swap(&mut ra, &mut rb);
                            }
                            g.parent[rb] = ra;
                            if g.rank[ra] == g.rank[rb] {
                                g.rank[ra] = g.rank[ra].saturating_add(1);
                            }
                        }
                    }
                    g.edge_next = scan
                        .overlaps
                        .range((Excluded((a, b)), Unbounded))
                        .next()
                        .copied();
                    scan.prep = Some(Prep::Grouping(Box::new(g)));
                } else {
                    g.phase = GroupPhase::Collect;
                    scan.prep = Some(Prep::Grouping(Box::new(g)));
                }
            }
            GroupPhase::Collect => {
                if g.collect_i >= scan.boxes.len() {
                    g.phase = GroupPhase::Overlaps;
                    g.edge_next = scan.overlaps.iter().next().copied();
                } else {
                    let i = g.collect_i;
                    let root = Self::union_parent(&mut g.parent, i);
                    g.groups
                        .entry(root)
                        .or_default()
                        .push(scan.boxes[i].item.key().representative());
                    *g.sizes.entry(root).or_default() += 1;
                    g.collect_i += 1;
                }
                scan.prep = Some(Prep::Grouping(Box::new(g)));
            }
            GroupPhase::Overlaps => {
                if let Some((a, b)) = g.edge_next {
                    g.overlapping.insert(a);
                    g.overlapping.insert(b);
                    g.edge_next = scan
                        .overlaps
                        .range((Excluded((a, b)), Unbounded))
                        .next()
                        .copied();
                    scan.prep = Some(Prep::Grouping(Box::new(g)));
                } else {
                    g.phase = GroupPhase::Finish;
                    scan.prep = Some(Prep::Grouping(Box::new(g)));
                }
            }
            GroupPhase::Finish => {
                let mut members: Vec<Vec<u64>> = g.groups.into_values().collect();
                for group in &mut members {
                    group.sort_unstable();
                }
                members.sort();
                self.metrics.components = members.len() as u64;
                self.metrics.component_size_max =
                    g.sizes.values().copied().max().unwrap_or(0) as u64;
                self.causal_components = members;
                scan.overlapping_items = g.overlapping;
                scan.traces.clear();
                if scan.boxes.is_empty() {
                    self.metrics.ir_nodes = 0;
                    Self::start_frontier(scan);
                } else {
                    scan.prep = Some(Prep::CompilingTraces { next: 0 });
                }
            }
        }
    }
    fn compile_guarded_trace(&self, scan: &Scan, item: ItemKey) -> GuardedTrace {
        let start = self.state.clock.saturating_add(1);
        let mut valid_until = scan.target;
        let singleton = !scan.overlapping_items.contains(&item);
        let mut guard = if singleton {
            TraceGuard::Horizon
        } else {
            TraceGuard::EnclosureOverlap
        };
        for s in self.state.scheduled_courses.values() {
            if item.involves(s.observer) && s.tick >= start && s.tick <= valid_until {
                valid_until = s.tick;
                guard = TraceGuard::SetCourse;
            }
        }
        for s in self.state.scheduled_range_courses.values() {
            if item.intersects_range(s.lo, s.hi) && s.tick >= start && s.tick <= valid_until {
                valid_until = s.tick;
                guard = TraceGuard::SetCourseRange;
            }
        }
        for s in self.state.signals.values() {
            if item.involves(s.target)
                && matches!(
                    guard,
                    TraceGuard::Horizon | TraceGuard::EnclosureOverlap | TraceGuard::ContactStop
                )
            {
                guard = TraceGuard::InboundSignal;
            }
        }
        if let ItemKey::Body(id) = item {
            if !singleton
                && matches!(guard, TraceGuard::Horizon | TraceGuard::EnclosureOverlap)
                && self
                    .state
                    .bodies
                    .get(&id)
                    .is_some_and(|b| b.stop_on_contact)
            {
                guard = TraceGuard::ContactStop;
            }
        }
        GuardedTrace {
            valid_until,
            guard,
        }
    }
    fn tighten_trace(scan: &mut Scan, item: ItemKey, tick: i128, guard: TraceGuard) {
        if let Some(trace) = scan.traces.get_mut(&item) {
            if tick < trace.valid_until {
                trace.valid_until = tick;
                trace.guard = guard;
            }
        }
    }
    fn step_construction(&mut self, scan: &mut Scan) -> Result<(), EngineError> {
        if scan.repair.is_some() {
            return self.step_repair(scan);
        }
        let Some(prep) = scan.prep.take() else {
            return Ok(());
        };
        match prep {
            Prep::CollectBodies { next_after, mut items } => {
                let next = match next_after {
                    None => self.state.bodies.range(..).next().map(|(&id, _)| id),
                    Some(id) => self
                        .state
                        .bodies
                        .range((Excluded(id), Unbounded))
                        .next()
                        .map(|(&id, _)| id),
                };
                if let Some(id) = next {
                    if self.in_scan_filter(id) {
                        items.push(Item::Body(id));
                    }
                    scan.prep = Some(Prep::CollectBodies {
                        next_after: Some(id),
                        items,
                    });
                } else {
                    scan.prep = Some(Prep::CollectFamilies {
                        family_index: 0,
                        cursor: None,
                        items,
                    });
                }
            }
            Prep::CollectFamilies {
                mut family_index,
                mut cursor,
                mut items,
            } => {
                self.metrics.family_range_ops += 1;
                if family_index >= self.state.families.len() {
                    if items.len() > self.max_pending_jobs {
                        return Err(EngineError::ResourceLimit(
                            "broad-phase object budget exceeded".into(),
                        ));
                    }
                    let drift = self.scan_drift();
                    scan.prep = Some(Prep::Building(Box::new(BuildingPrep {
                        items,
                        boxes: Vec::new(),
                        next: 0,
                        drift,
                        cx_min: None,
                        cx_max: None,
                        cy_min: None,
                        cy_max: None,
                    })));
                } else {
                    let f = &self.state.families[family_index];
                    if !self.range_intersects_filter(f.first_id, f.last_id()) {
                        scan.prep = Some(Prep::CollectFamilies {
                            family_index: family_index + 1,
                            cursor: None,
                            items,
                        });
                        return Ok(());
                    }
                    let end = f.first_id + (f.count - 1);
                    let cur = cursor.unwrap_or(f.first_id);
                    if let Some((&id, _)) = self.state.bodies.range(cur..=end).next() {
                        if cur < id {
                            items.push(Item::Family {
                                index: family_index,
                                lo: cur,
                                hi: id - 1,
                            });
                        }
                        cursor = if id == end { None } else { Some(id + 1) };
                        if cursor.is_none() {
                            family_index += 1;
                        }
                    } else {
                        items.push(Item::Family {
                            index: family_index,
                            lo: cur,
                            hi: end,
                        });
                        family_index += 1;
                        cursor = None;
                    }
                    scan.prep = Some(Prep::CollectFamilies {
                        family_index,
                        cursor,
                        items,
                    });
                }
            }
            Prep::Grouping(g) => {
                self.step_grouping(scan, *g);
            }
            Prep::CompilingTraces { next } => {
                if next >= scan.boxes.len() {
                    self.metrics.ir_nodes = scan.traces.len() as u64;
                    Self::start_frontier(scan);
                } else {
                    let key = scan.boxes[next].item.key();
                    let trace = self.compile_guarded_trace(scan, key);
                    scan.traces.insert(key, trace);
                    scan.prep = Some(Prep::CompilingTraces { next: next + 1 });
                }
            }
            Prep::EnqueuingFrontier { phase } => {
                self.step_enqueue_frontier(scan, phase)?;
            }
            Prep::Building(mut build) => {
                if build.next >= build.items.len() {
                    let x_spread = match (build.cx_min, build.cx_max) {
                        (Some(lo), Some(hi)) => hi - lo,
                        _ => r(0),
                    };
                    let y_spread = match (build.cy_min, build.cy_max) {
                        (Some(lo), Some(hi)) => hi - lo,
                        _ => r(0),
                    };
                    scan.prep = Some(Prep::Sorting(Box::new(SortPrep {
                        boxes: build.boxes,
                        scratch: Vec::new(),
                        x_axis: x_spread >= y_spread,
                        width: 1,
                        run: 0,
                        i: 0,
                        j: 0,
                        k: 0,
                        dest_is_scratch: true,
                    })));
                } else {
                    let built =
                        self.build_box(build.items[build.next].clone(), scan.target, &build.drift)?;
                    let cx = &built.min.x + &built.max.x;
                    let cy = &built.min.y + &built.max.y;
                    build.cx_min = Some(match build.cx_min {
                        Some(v) => v.min(cx.clone()),
                        None => cx.clone(),
                    });
                    build.cx_max = Some(match build.cx_max {
                        Some(v) => v.max(cx),
                        None => cx.clone(),
                    });
                    build.cy_min = Some(match build.cy_min {
                        Some(v) => v.min(cy.clone()),
                        None => cy.clone(),
                    });
                    build.cy_max = Some(match build.cy_max {
                        Some(v) => v.max(cy),
                        None => cy.clone(),
                    });
                    build.boxes.push(built);
                    build.next += 1;
                    self.metrics.box_builds += 1;
                    self.metrics.broadphase_boxes += 1;
                    scan.prep = Some(Prep::Building(build));
                }
            }
            Prep::Sorting(sort) => {
                self.step_sort(scan, *sort);
            }
            Prep::Sweeping {
                i,
                active_j,
                active,
                expire_read,
                expire_write,
                expired,
            } => {
                self.step_sweep(scan, i, active_j, active, expire_read, expire_write, expired);
            }
        }
        Ok(())
    }
    fn finish_sort(scan: &mut Scan, boxes: Vec<SweptBox>, x_axis: bool) {
        scan.boxes = boxes;
        scan.x_axis = x_axis;
        scan.overlaps.clear();
        scan.overlap_certs.clear();
        scan.prep = Some(Prep::Sweeping {
            i: 0,
            active_j: 0,
            active: Vec::new(),
            expire_read: None,
            expire_write: 0,
            expired: false,
        });
    }
    fn step_sort(&mut self, scan: &mut Scan, mut sort: SortPrep) {
        let n = sort.boxes.len();
        if n <= 1 {
            self.metrics.sort_steps += 1;
            Self::finish_sort(scan, sort.boxes, sort.x_axis);
            return;
        }
        if sort.scratch.capacity() < n {
            sort.scratch.reserve(n);
        }
        let mid = (sort.run + sort.width).min(n);
        let right = (sort.run + sort.width.saturating_mul(2)).min(n);
        if sort.k == 0 && sort.i == sort.run && sort.j == 0 {
            sort.i = sort.run;
            sort.j = mid;
            sort.k = sort.run;
        }
        let take_left = sort.i < mid
            && (sort.j >= right || {
                let (left, right_item) = if sort.dest_is_scratch {
                    (&sort.boxes[sort.i], &sort.boxes[sort.j])
                } else {
                    (&sort.scratch[sort.i], &sort.scratch[sort.j])
                };
                Self::axis_min(left, sort.x_axis) <= Self::axis_min(right_item, sort.x_axis)
            });
        let src_idx = if take_left {
            let idx = sort.i;
            sort.i += 1;
            idx
        } else {
            let idx = sort.j;
            sort.j += 1;
            idx
        };
        let item = if sort.dest_is_scratch {
            sort.boxes[src_idx].clone()
        } else {
            sort.scratch[src_idx].clone()
        };
        if sort.dest_is_scratch {
            if sort.k == sort.scratch.len() {
                sort.scratch.push(item);
            } else {
                sort.scratch[sort.k] = item;
            }
        } else if sort.k == sort.boxes.len() {
            sort.boxes.push(item);
        } else {
            sort.boxes[sort.k] = item;
        }
        sort.k += 1;
        self.metrics.sort_steps += 1;
        if sort.k >= right {
            sort.run = sort.run.saturating_add(sort.width.saturating_mul(2));
            if sort.run >= n {
                sort.dest_is_scratch = !sort.dest_is_scratch;
                sort.width = sort.width.saturating_mul(2);
                if sort.width >= n {
                    let boxes = if sort.dest_is_scratch {
                        sort.boxes
                    } else {
                        sort.scratch
                    };
                    Self::finish_sort(scan, boxes, sort.x_axis);
                    return;
                }
                sort.run = 0;
            }
            let mid = (sort.run + sort.width).min(n);
            sort.i = sort.run;
            sort.j = mid;
            sort.k = sort.run;
        }
        scan.prep = Some(Prep::Sorting(Box::new(sort)));
    }
    fn step_sweep(
        &mut self,
        scan: &mut Scan,
        mut i: usize,
        mut active_j: usize,
        mut active: Vec<usize>,
        expire_read: Option<usize>,
        mut expire_write: usize,
        expired: bool,
    ) {
        if i >= scan.boxes.len() {
            Self::start_grouping(scan);
            return;
        }
        if let Some(read) = expire_read {
            self.metrics.expire_ops += 1;
            if read >= active.len() {
                active.truncate(expire_write);
                scan.prep = Some(Prep::Sweeping {
                    i,
                    active_j: 0,
                    active,
                    expire_read: None,
                    expire_write: 0,
                    expired: true,
                });
                return;
            }
            let keep = if scan.x_axis {
                scan.boxes[active[read]].max.x >= scan.boxes[i].min.x
            } else {
                scan.boxes[active[read]].max.y >= scan.boxes[i].min.y
            };
            if keep {
                active[expire_write] = active[read];
                expire_write += 1;
            }
            scan.prep = Some(Prep::Sweeping {
                i,
                active_j,
                active,
                expire_read: Some(read + 1),
                expire_write,
                expired,
            });
            return;
        }
        if !expired && active_j == 0 && !active.is_empty() {
            scan.prep = Some(Prep::Sweeping {
                i,
                active_j,
                active,
                expire_read: Some(0),
                expire_write: 0,
                expired: false,
            });
            return;
        }
        if active_j < active.len() {
            let a = &scan.boxes[active[active_j]];
            let b = &scan.boxes[i];
            self.metrics.aabb_compares += 1;
            self.metrics.broadphase_pairs += 1;
            if Self::aabb_overlap(a, b) {
                self.record_overlap(scan, a.item.key(), b.item.key());
            } else {
                self.metrics.certified_rejections += 1;
            }
            active_j += 1;
            scan.prep = Some(Prep::Sweeping {
                i,
                active_j,
                active,
                expire_read: None,
                expire_write: 0,
                expired: true,
            });
        } else {
            active.push(i);
            i += 1;
            scan.prep = Some(Prep::Sweeping {
                i,
                active_j: 0,
                active,
                expire_read: None,
                expire_write: 0,
                expired: false,
            });
        }
    }
    fn invalidate_or_repair(&mut self, dirty: &[u64]) {
        if !self.incremental_sap {
            self.pending = None;
            return;
        }
        let Some(mut scan) = self.pending.take() else {
            return;
        };
        if scan.prep.is_some()
            || scan.repair.is_some()
            || scan.commit.is_some()
            || scan.after.is_some()
            || scan.boxes.is_empty()
        {
            if scan.commit.is_some() || scan.after.is_some() {
                self.pending = Some(scan);
            }
            return;
        }
        self.begin_repair(&mut scan, dirty.to_vec());
        self.pending = Some(scan);
    }
    fn begin_repair(&mut self, scan: &mut Scan, dirty: Vec<u64>) {
        self.metrics.sap_repairs += 1;
        scan.jobs.clear();
        self.invalidate_dirty_certificates(scan, &dirty);
        let mut items = Vec::new();
        for id in dirty {
            if scan
                .boxes
                .iter()
                .any(|b| matches!(b.item, Item::Body(x) if x == id))
            {
                items.push(Item::Body(id));
                continue;
            }
            if let Some(pos) = scan.boxes.iter().position(|b| b.item.involves(id)) {
                let Item::Family { index, lo, hi } = scan.boxes[pos].item.clone() else {
                    items.push(Item::Body(id));
                    continue;
                };
                let old = scan.boxes[pos].item.key();
                scan.boxes.remove(pos);
                self.remove_item_overlaps(scan, old);
                if lo < id {
                    items.push(Item::Family {
                        index,
                        lo,
                        hi: id - 1,
                    });
                }
                items.push(Item::Body(id));
                if id < hi {
                    items.push(Item::Family {
                        index,
                        lo: id + 1,
                        hi,
                    });
                }
            } else {
                items.push(Item::Body(id));
            }
        }
        items.sort();
        items.dedup();
        scan.repair = Some(Repair::Update { items, next: 0 });
    }
    fn step_repair(&mut self, scan: &mut Scan) -> Result<(), EngineError> {
        let Some(repair) = scan.repair.take() else {
            return Ok(());
        };
        match repair {
            Repair::Update { items, next } => {
                if next >= items.len() {
                    let dirty = items.iter().map(Item::key).collect();
                    scan.repair = Some(Repair::Retest {
                        dirty,
                        di: 0,
                        j: 0,
                        a_at: None,
                    });
                } else {
                    let item = items[next].clone();
                    let key = item.key();
                    if let Some(pos) = scan.boxes.iter().position(|b| b.item.key() == key) {
                        scan.boxes.remove(pos);
                    }
                    self.remove_item_overlaps(scan, key);
                    let drift = self.scan_drift();
                    let built = self.build_box(item, scan.target, &drift)?;
                    Self::insert_sorted(&mut scan.boxes, built, scan.x_axis);
                    self.metrics.box_builds += 1;
                    self.metrics.broadphase_boxes += 1;
                    scan.repair = Some(Repair::Update {
                        items,
                        next: next + 1,
                    });
                }
            }
            Repair::Retest { dirty, mut di, mut j, a_at } => {
                if di >= dirty.len() {
                    scan.repair = Some(Repair::Enqueue);
                } else if j >= scan.boxes.len() {
                    di += 1;
                    scan.repair = Some(Repair::Retest { dirty, di, j: 0, a_at: None });
                } else {
                    let a_key = dirty[di];
                    // One lookup per dirty item (charged as this step), not one per compare.
                    let Some(a_at) = a_at.or_else(|| scan.boxes.iter().position(|b| b.item.key() == a_key)) else {
                        di += 1;
                        scan.repair = Some(Repair::Retest { dirty, di, j: 0, a_at: None });
                        return Ok(());
                    };
                    let b_key = scan.boxes[j].item.key();
                    if a_key != b_key {
                        self.metrics.aabb_compares += 1;
                        self.metrics.broadphase_pairs += 1;
                        if Self::aabb_overlap(&scan.boxes[a_at], &scan.boxes[j]) {
                            self.record_overlap(scan, a_key, b_key);
                        } else {
                            self.metrics.certified_rejections += 1;
                        }
                    }
                    j += 1;
                    scan.repair = Some(Repair::Retest { dirty, di, j, a_at: Some(a_at) });
                }
            }
            Repair::Enqueue => {
                Self::start_grouping(scan);
            }
        }
        Ok(())
    }
    fn scan_drift(&self) -> Vec2 {
        let mut shared: Option<Vec2> = None;
        for f in &self.state.families {
            if !f.shares_member_velocity() {
                return Vec2::zero();
            }
            match &shared {
                None => shared = Some(f.trajectory.velocity.clone()),
                Some(v) if *v == f.trajectory.velocity => {}
                Some(_) => return Vec2::zero(),
            }
        }
        shared.unwrap_or_else(Vec2::zero)
    }
    fn member_id(&self, item: &Item) -> Option<u64> {
        match item {
            Item::Body(id) => Some(*id),
            Item::Family { lo, hi, .. } if lo == hi => Some(*lo),
            _ => None,
        }
    }
    fn family_exception(&self, item: &Item) -> bool {
        matches!(item,Item::Family{lo,hi,..}if lo==hi && self.state.bodies.contains_key(lo))
    }
    fn split_item(item: Item) -> Option<(Item, Item)> {
        if let Item::Family { index, lo, hi } = item {
            if lo < hi {
                let m = lo + (hi - lo) / 2;
                return Some((
                    Item::Family { index, lo, hi: m },
                    Item::Family {
                        index,
                        lo: m + 1,
                        hi,
                    },
                ));
            }
        }
        None
    }
    fn item_count(item: &Item) -> u64 {
        match item {
            Item::Body(_) => 1,
            Item::Family { lo, hi, .. } => hi - lo + 1,
        }
    }
    fn disjoint(&self, a: &Item, b: &Item, from: i128, to: i128) -> Result<bool, EngineError> {
        if let (Item::Body(ia), Item::Body(ib)) = (a, b) {
            let aa = self.decode(*ia)?;
            let bb = self.decode(*ib)?;
            if aa.segments.len() == 1 && bb.segments.len() == 1 {
                return Ok(Self::inertial_pair_disjoint(
                    aa.flow(),
                    bb.flow(),
                    &aa.radius,
                    &bb.radius,
                    from,
                    to,
                ));
            }
        }
        let (sa, ra) = self.item_samples(a, from, to)?;
        let (sb, rb) = self.item_samples(b, from, to)?;
        let mut times = BTreeSet::new();
        times.insert(from);
        times.insert(to);
        for (t, _) in sa.iter().chain(sb.iter()) {
            times.insert(*t);
        }
        let mut minx = None;
        let mut maxx = None;
        let mut miny = None;
        let mut maxy = None;
        for t in times {
            let (pa, _) = self.item_positions(a, t)?;
            let (pb, _) = self.item_positions(b, t)?;
            for x in &pa {
                for y in &pb {
                    let d = x.clone() - y.clone();
                    minx = Some(minx.map_or(d.x.clone(), |v: Rational| v.min(d.x.clone())));
                    maxx = Some(maxx.map_or(d.x.clone(), |v: Rational| v.max(d.x)));
                    miny = Some(miny.map_or(d.y.clone(), |v: Rational| v.min(d.y.clone())));
                    maxy = Some(maxy.map_or(d.y.clone(), |v: Rational| v.max(d.y)));
                }
            }
        }
        let dx = Self::nearest_axis(minx.unwrap(), maxx.unwrap());
        let dy = Self::nearest_axis(miny.unwrap(), maxy.unwrap());
        let rr = ra + rb;
        Ok(dx.clone() * dx + dy.clone() * dy > rr.clone() * rr)
    }
    fn nearest_axis(lo: Rational, hi: Rational) -> Rational {
        if lo > r(0) {
            lo
        } else if hi < r(0) {
            -hi
        } else {
            r(0)
        }
    }
    fn inertial_pair_disjoint(
        a: &Inertial,
        b: &Inertial,
        ra: &Rational,
        rb: &Rational,
        from: i128,
        to: i128,
    ) -> bool {
        let mut minx = None;
        let mut maxx = None;
        let mut miny = None;
        let mut maxy = None;
        for t in [from, to] {
            let d = a.state_at(t) - b.state_at(t);
            minx = Some(minx.map_or(d.x.clone(), |v: Rational| v.min(d.x.clone())));
            maxx = Some(maxx.map_or(d.x.clone(), |v: Rational| v.max(d.x)));
            miny = Some(miny.map_or(d.y.clone(), |v: Rational| v.min(d.y.clone())));
            maxy = Some(maxy.map_or(d.y.clone(), |v: Rational| v.max(d.y)));
        }
        let dx = Self::nearest_axis(minx.unwrap(), maxx.unwrap());
        let dy = Self::nearest_axis(miny.unwrap(), maxy.unwrap());
        let rr = ra.clone() + rb.clone();
        dx.clone() * dx + dy.clone() * dy > rr.clone() * rr
    }
    fn process_job(&mut self, job: Job, scan: &mut Scan) -> Result<(), EngineError> {
        let start = self
            .state
            .clock
            .checked_add(1)
            .ok_or_else(|| EngineError::Invalid("time exhausted".into()))?;
        // Compile each overlapping pair through the remaining scan horizon and
        // persist the certificate so quiet commits do not re-run certified pairs.
        let end = scan.target;
        match job {
            Job::Scheduled(id) => {
                if let Some(s) = self.state.scheduled_courses.get(&id) {
                    if s.tick >= start && s.tick <= end {
                        let key = format!("course:{id}");
                        scan.heap.push(Reverse((s.tick, key.clone())));
                        scan.candidates.insert(
                            key.clone(),
                            Candidate {
                                tick: s.tick,
                                key,
                                action: Action::Course(id.clone()),
                            },
                        );
                        let observer = s.observer;
                        let tick = s.tick;
                        let keys: Vec<_> = scan
                            .traces
                            .keys()
                            .copied()
                            .filter(|k| k.involves(observer))
                            .collect();
                        for item in keys {
                            Self::tighten_trace(scan, item, tick, TraceGuard::SetCourse);
                        }
                    }
                    scan.scheduled_certs.insert(id, end);
                }
            }
            Job::ScheduledRange(id) => {
                if let Some(s) = self.state.scheduled_range_courses.get(&id) {
                    if s.tick >= start && s.tick <= end {
                        let key = format!("rcourse:{id}");
                        scan.heap.push(Reverse((s.tick, key.clone())));
                        scan.candidates.insert(
                            key.clone(),
                            Candidate {
                                tick: s.tick,
                                key,
                                action: Action::RangeCourse(id.clone()),
                            },
                        );
                        let lo = s.lo;
                        let hi = s.hi;
                        let tick = s.tick;
                        let keys: Vec<_> = scan
                            .traces
                            .keys()
                            .copied()
                            .filter(|k| k.intersects_range(lo, hi))
                            .collect();
                        for item in keys {
                            Self::tighten_trace(scan, item, tick, TraceGuard::SetCourseRange);
                        }
                    }
                    scan.scheduled_certs.insert(id, end);
                }
            }
            Job::Signal(id) => {
                let s = &self.state.signals[&id];
                let b = self.decode(s.target)?;
                let lower = start.max(s.tick.saturating_add(1));
                if lower <= end {
                    self.metrics.exact_leaf_queries += 1;
                    if let Some(tick) = geometry::first_signal_arrival_piecewise(
                        s.tick,
                        &s.position,
                        &b.segments,
                        TickInterval { start: lower, end },
                    ) {
                        let key = format!("signal:{id}");
                        scan.heap.push(Reverse((tick, key.clone())));
                        scan.candidates.insert(
                            key.clone(),
                            Candidate {
                                tick,
                                key,
                                action: Action::Arrival(id.clone()),
                            },
                        );
                        let target = s.target;
                        let keys: Vec<_> = scan
                            .traces
                            .keys()
                            .copied()
                            .filter(|k| k.involves(target))
                            .collect();
                        for item in keys {
                            Self::tighten_trace(scan, item, tick, TraceGuard::InboundSignal);
                        }
                    }
                }
                scan.signal_certs.insert(id, end);
            }
            Job::Wall(id) => {
                if let Some(c) = self.state.elastic.as_ref().and_then(|el| el.container.clone()) {
                    let b = self.decode(id)?;
                    if let Some(tick) = Self::first_wall_tick(&b, &c, self.state.clock, start, end) {
                        let key = format!("wall:{id:020}");
                        scan.heap.push(Reverse((tick, key.clone())));
                        scan.candidates.insert(
                            key.clone(),
                            Candidate { tick, key, action: Action::Wall(id) },
                        );
                        Self::tighten_trace(scan, ItemKey::Body(id), tick, TraceGuard::Wall);
                    }
                }
                scan.wall_certs.insert(id, end);
            }
            Job::Pair(a, b) => {
                let pair = Self::pair_key(a.key(), b.key());
                if self.family_exception(&a) || self.family_exception(&b) {
                    scan.overlap_certs.insert(pair, end);
                    return Ok(());
                }
                if self.member_id(&a).is_some() && self.member_id(&a) == self.member_id(&b) {
                    scan.overlap_certs.insert(pair, end);
                    return Ok(());
                }
                if self.disjoint(&a, &b, self.state.clock, end)? {
                    self.metrics.certified_rejections += 1;
                    scan.overlap_certs.insert(pair, end);
                    return Ok(());
                }
                if let (Some(ia), Some(ib)) = (self.member_id(&a), self.member_id(&b)) {
                    let (ia, ib) = if ia < ib { (ia, ib) } else { (ib, ia) };
                    let aa = self.decode(ia)?;
                    let bb = self.decode(ib)?;
                    if self
                        .state
                        .contacts
                        .contains(&(ia, ib, aa.revision, bb.revision))
                    {
                        scan.overlap_certs.insert(pair, end);
                        return Ok(());
                    }
                    if aa.bounce && bb.bounce {
                        // Overlapping bouncers that already separate never touch again on these
                        // trajectories (linear motion): no contact until one of them changes.
                        let d = bb.at(self.state.clock) - aa.at(self.state.clock);
                        let w = bb.velocity_at(self.state.clock) - aa.velocity_at(self.state.clock);
                        let reach = &aa.radius + &bb.radius;
                        if d.norm_squared() <= &reach * &reach && d.dot(&w) >= r(0) {
                            scan.overlap_certs.insert(pair, end);
                            return Ok(());
                        }
                    }
                    self.metrics.exact_leaf_queries += 1;
                    if let Some(tick) = geometry::first_contact_piecewise(
                        &aa.segments,
                        &bb.segments,
                        &(&aa.radius + &bb.radius),
                        TickInterval { start, end },
                    ) {
                        let key = format!("contact:{ia:020}:{ib:020}");
                        scan.heap.push(Reverse((tick, key.clone())));
                        scan.candidates.insert(
                            key.clone(),
                            Candidate {
                                tick,
                                key,
                                action: Action::Contact(ia, ib),
                            },
                        );
                        let stop = aa.stop_on_contact || bb.stop_on_contact;
                        let guard = if stop {
                            TraceGuard::ContactStop
                        } else {
                            TraceGuard::EnclosureOverlap
                        };
                        Self::tighten_trace(scan, a.key(), tick, guard);
                        Self::tighten_trace(scan, b.key(), tick, guard);
                    }
                    scan.overlap_certs.insert(pair, end);
                } else {
                    if scan.jobs.len() + 2 > self.max_pending_jobs {
                        return Err(EngineError::ResourceLimit(
                            "family refinement exceeds job capacity".into(),
                        ));
                    }
                    if Self::item_count(&a) >= Self::item_count(&b) {
                        let (l, h) = Self::split_item(a).unwrap();
                        scan.jobs.push_back(Job::Pair(l, b.clone()));
                        scan.jobs.push_back(Job::Pair(h, b));
                    } else {
                        let (l, h) = Self::split_item(b).unwrap();
                        scan.jobs.push_back(Job::Pair(a.clone(), l));
                        scan.jobs.push_back(Job::Pair(a, h));
                    }
                    scan.overlap_certs.insert(pair, end);
                }
            }
        }
        Ok(())
    }
    fn empty_effects() -> BatchEffects {
        BatchEffects {
            deltas: BTreeMap::new(),
            courses: BTreeMap::new(),
            stops: BTreeSet::new(),
            records: Vec::new(),
            contacts: Vec::new(),
            received: Vec::new(),
            fired_courses: Vec::new(),
            fired_ranges: Vec::new(),
            notifications: Vec::new(),
            bounces: Vec::new(),
            walls: BTreeSet::new(),
            elastic_only: BTreeSet::new(),
            residuals: BTreeMap::new(),
            wall_momentum: Vec2::zero(),
        }
    }
    /// Elastic responses for this batch's bounce contacts (H0159), resolved one pair at a time
    /// in canonical pair order, each from the velocities the earlier pairs left (sequential
    /// impulses; summing pairs from pre-batch states heated a dense gas by 3.2%). With a response quantum Q, each pair's
    /// momentum exchange is rounded per component to multiples of lcm(m_a, m_b)/Q, so both
    /// velocity changes stay on the 1/Q lattice and momentum stays exact. Among the floor/ceil
    /// candidates (never zero when the exact exchange is not), the one bringing the pair's owed
    /// energy closest to zero wins; ties keep enumeration order. Each pair's energy error is
    /// added to its lower-id body's residual; the batch's multi-contact remainder goes to the
    /// lowest-id body. Total kinetic energy minus total residual is therefore conserved.
    fn resolve_bounces(&mut self, tick: i128, acc: &mut BatchEffects) -> Result<(), EngineError> {
        let external: BTreeSet<u64> = acc
            .deltas
            .keys()
            .copied()
            .chain(acc.courses.keys().copied())
            .chain(acc.stops.iter().copied())
            .collect();
        for &id in &acc.walls {
            if !external.contains(&id) {
                acc.elastic_only.insert(id);
            }
        }
        if acc.bounces.is_empty() {
            return Ok(());
        }
        let mut pairs = acc.bounces.clone();
        pairs.sort_unstable();
        pairs.dedup();
        let quantum = self.state.elastic.as_ref().and_then(|el| el.response_quantum);
        let mut bodies: BTreeMap<u64, Body> = BTreeMap::new();
        for &(a, b) in &pairs {
            for id in [a, b] {
                if !bodies.contains_key(&id) {
                    bodies.insert(id, self.decode(id)?);
                }
            }
        }
        let mut residual: BTreeMap<u64, Rational> =
            bodies.iter().map(|(id, b)| (*id, b.energy_residual.clone())).collect();
        let original = residual.clone();
        let ke = |m: &Rational, v: &Vec2| m * v.norm_squared() / r(2);
        let mut delta: BTreeMap<u64, Vec2> = BTreeMap::new();
        let mut pair_errors = r(0);
        for &(a, b) in &pairs {
            let (ba, bb) = (&bodies[&a], &bodies[&b]);
            // Sequential impulses: each pair starts from the velocities the earlier pairs of
            // this batch left, so a multi-contact batch stays exactly elastic before rounding.
            let va = ba.velocity_at(tick) + delta.get(&a).cloned().unwrap_or_else(Vec2::zero);
            let vb = bb.velocity_at(tick) + delta.get(&b).cloned().unwrap_or_else(Vec2::zero);
            let d = bb.at(tick) - ba.at(tick);
            let w = vb.clone() - va.clone();
            let dot = d.dot(&w);
            let dd = d.norm_squared();
            if dot >= r(0) || dd == r(0) {
                continue;
            }
            let (ma, mb) = (ba.mass.clone(), bb.mass.clone());
            // Exact elastic momentum given to `a` along the line of centres.
            let exact = d.clone() * (r(2) * &ma * &mb / (&ma + &mb) * &dot / &dd);
            let chosen = match quantum {
                None => exact.clone(),
                Some(q) => {
                    if !ma.is_integer() || !mb.is_integer() {
                        return Err(EngineError::Unsupported(
                            "lattice bounces need integer masses".into(),
                        ));
                    }
                    let lcm = num_integer::Integer::lcm(&ma.to_integer(), &mb.to_integer());
                    let step = Rational::from_integer(lcm) / r(q);
                    let down = |x: &Rational| (x / &step).floor() * &step;
                    let up = |x: &Rational| (x / &step).ceil() * &step;
                    let mut cands: Vec<Vec2> = Vec::new();
                    for x in [down(&exact.x), up(&exact.x)] {
                        for y in [down(&exact.y), up(&exact.y)] {
                            let c = Vec2 { x: x.clone(), y };
                            if !cands.contains(&c) && !(c == Vec2::zero() && exact != Vec2::zero()) {
                                cands.push(c);
                            }
                        }
                    }
                    let owed = &residual[&a] + &residual[&b];
                    let mut best: Option<(Rational, Vec2)> = None;
                    for c in cands {
                        let na = va.clone() + c.clone() * (r(1) / &ma);
                        let nb = vb.clone() - c.clone() * (r(1) / &mb);
                        let e = ke(&ma, &na) + ke(&mb, &nb) - ke(&ma, &va) - ke(&mb, &vb);
                        let score = num_traits::Signed::abs(&(&owed + &e));
                        if best.as_ref().is_none_or(|(s, _)| score < *s) {
                            best = Some((score, c));
                        }
                    }
                    best.map_or(exact.clone(), |(_, c)| c)
                }
            };
            let da = chosen.clone() * (r(1) / &ma);
            let db = chosen * (-(r(1) / &mb));
            let e = ke(&ma, &(va.clone() + da.clone())) + ke(&mb, &(vb.clone() + db.clone()))
                - ke(&ma, &va)
                - ke(&mb, &vb);
            *residual.get_mut(&a).expect("pair body") += &e;
            pair_errors += &e;
            let ea = delta.entry(a).or_insert_with(Vec2::zero);
            *ea = ea.clone() + da;
            let eb = delta.entry(b).or_insert_with(Vec2::zero);
            *eb = eb.clone() + db;
        }
        // Multi-contact remainder: the true batch energy change minus the pairwise estimates.
        let mut batch_error = r(0);
        for (id, dv) in &delta {
            let b = &bodies[id];
            let v = b.velocity_at(tick);
            batch_error += ke(&b.mass, &(v.clone() + dv.clone())) - ke(&b.mass, &v);
        }
        if let Some(first) = bodies.keys().next().copied() {
            *residual.get_mut(&first).expect("first body") += batch_error - pair_errors;
        }
        for (id, value) in residual {
            if original.get(&id) != Some(&value) {
                acc.residuals.insert(id, value);
            }
        }
        for id in bodies.keys() {
            if !external.contains(id) {
                acc.elastic_only.insert(*id);
            }
        }
        for (id, dv) in delta {
            let e = acc.deltas.entry(id).or_insert_with(Vec2::zero);
            *e = e.clone() + dv;
        }
        Ok(())
    }
    fn accumulate_one(
        &self,
        tick: i128,
        candidate: &Candidate,
        acc: &mut BatchEffects,
    ) -> Result<(), EngineError> {
        match &candidate.action {
            Action::Course(id) => {
                let s = &self.state.scheduled_courses[id];
                acc.courses.insert(s.observer, s.velocity.clone());
                acc.records.push(event(
                    tick,
                    "burn",
                    vec![s.observer],
                    vec![id.clone()],
                    digest(&("scheduled", &s.velocity)),
                ));
                acc.fired_courses.push(id.clone());
            }
            Action::RangeCourse(id) => {
                let s = self.state.scheduled_range_courses[id].clone();
                acc.records.push(event(
                    tick,
                    "range_burn",
                    vec![s.lo, s.hi],
                    vec![id.clone()],
                    digest(&("scheduled-range", s.lo, s.hi, &s.velocity)),
                ));
                acc.fired_ranges.push(s);
            }
            Action::Arrival(id) => {
                let s = &self.state.signals[id];
                match &s.payload {
                    Payload::Impulse { delta } => {
                        let v = acc.deltas.entry(s.target).or_insert_with(Vec2::zero);
                        *v = v.clone() + delta.clone();
                    }
                    Payload::SetCourse { velocity } => {
                        acc.courses.insert(s.target, velocity.clone());
                    }
                    Payload::Momentum { impulse } => {
                        let mass = self.decode(s.target)?.mass;
                        if mass <= r(0) {
                            return Err(EngineError::Invalid("momentum needs positive mass".into()));
                        }
                        let v = acc.deltas.entry(s.target).or_insert_with(Vec2::zero);
                        *v = v.clone() + impulse.clone() * (r(1) / mass);
                    }
                    Payload::Ping => {}
                }
                acc.records.push(event(
                    tick,
                    "signal_arrived",
                    vec![s.source, s.target],
                    vec![id.clone()],
                    "causal reception".into(),
                ));
                acc.received.push(id.clone());
            }
            Action::Wall(id) => {
                acc.walls.insert(*id);
                acc.records.push(event(tick, "wall", vec![*id], vec![], "container wall".into()));
            }
            Action::Contact(a, b) => {
                let (a, b) = if a < b { (*a, *b) } else { (*b, *a) };
                let aa = self.decode(a)?;
                let bb = self.decode(b)?;
                acc.contacts.push((a, b, aa.revision, bb.revision));
                if aa.bounce && bb.bounce {
                    acc.bounces.push((a, b));
                }
                for body in [&aa, &bb] {
                    if body.stop_on_contact {
                        acc.stops.insert(body.id);
                    }
                    if let Some(target) = body.notify_on_contact {
                        acc.notifications.push((body.id, target));
                    }
                }
                acc.records.push(event(
                    tick,
                    "contact",
                    vec![a, b],
                    vec![],
                    format!("segments {}:{}", aa.revision, bb.revision),
                ));
            }
        }
        Ok(())
    }
    fn step_commit(
        &mut self,
        scan: &mut Scan,
    ) -> Result<Option<(i128, usize, Vec<u64>, bool)>, EngineError> {
        self.metrics.commit_prep_ops += 1;
        let Some(prep) = scan.commit.take() else {
            return Ok(None);
        };
        match prep {
            CommitPrep::Collect { tick, next, mut batch } => {
                let following = match next {
                    None => scan
                        .candidates
                        .iter()
                        .find(|(_, c)| c.tick == tick)
                        .map(|(k, _)| k.clone()),
                    Some(key) => scan
                        .candidates
                        .range((Excluded(key), Unbounded))
                        .find(|(_, c)| c.tick == tick)
                        .map(|(k, _)| k.clone()),
                };
                if let Some(key) = following {
                    if let Some(c) = scan.candidates.get(&key) {
                        batch.push(c.clone());
                    }
                    scan.commit = Some(CommitPrep::Collect {
                        tick,
                        next: Some(key),
                        batch,
                    });
                } else {
                    batch.sort_by(|a, b| a.key.cmp(&b.key));
                    scan.commit = Some(CommitPrep::Accumulate {
                        tick,
                        batch,
                        index: 0,
                        acc: Self::empty_effects(),
                    });
                }
                Ok(None)
            }
            CommitPrep::Accumulate {
                tick,
                batch,
                index,
                mut acc,
            } => {
                if index >= batch.len() {
                    acc.notifications.sort_unstable();
                    acc.notifications.dedup();
                    self.resolve_bounces(tick, &mut acc)?;
                    let affected: Vec<u64> = acc
                        .deltas
                        .keys()
                        .copied()
                        .chain(acc.courses.keys().copied())
                        .chain(acc.stops.iter().copied())
                        .chain(acc.walls.iter().copied())
                        .collect::<BTreeSet<_>>()
                        .into_iter()
                        .collect();
                    let new_count = affected
                        .iter()
                        .filter(|id| !self.state.bodies.contains_key(id))
                        .count();
                    if self.state.bodies.len() + new_count > self.max_resident_bodies {
                        return Err(EngineError::ResourceLimit(
                            "event requires too many independent ships".into(),
                        ));
                    }
                    scan.commit = Some(CommitPrep::ValidateAffected {
                        tick,
                        acc,
                        affected,
                        next: 0,
                        velocities: Vec::new(),
                    });
                } else {
                    self.accumulate_one(tick, &batch[index], &mut acc)?;
                    scan.commit = Some(CommitPrep::Accumulate {
                        tick,
                        batch,
                        index: index + 1,
                        acc,
                    });
                }
                Ok(None)
            }
            CommitPrep::ValidateAffected {
                tick,
                mut acc,
                affected,
                next,
                mut velocities,
            } => {
                if next >= affected.len() {
                    if self.state.signals.len() - acc.received.len() + acc.notifications.len()
                        > self.max_pending_jobs
                    {
                        return Err(EngineError::ResourceLimit(
                            "contact notifications exceed signal capacity".into(),
                        ));
                    }
                    scan.commit = Some(CommitPrep::ValidateNotes {
                        tick,
                        acc,
                        velocities,
                        note_i: 0,
                        notification_counts: BTreeMap::new(),
                    });
                } else {
                    let id = affected[next];
                    let b = self.decode(id)?;
                    // Stopping a body already at rest changes nothing physically. It must
                    // not open a new trajectory revision: that would re-arm contacts with
                    // every overlapping resting neighbour and make them re-collide each tick.
                    if acc.stops.contains(&id) && b.velocity_at(tick) == Vec2::zero() {
                        scan.commit = Some(CommitPrep::ValidateAffected {
                            tick,
                            acc,
                            affected,
                            next: next + 1,
                            velocities,
                        });
                        return Ok(None);
                    }
                    b.revision.checked_add(1).ok_or_else(|| {
                        EngineError::ResourceLimit("trajectory revision exhausted".into())
                    })?;
                    let mut v = if acc.stops.contains(&id) {
                        Vec2::zero()
                    } else if let Some(course) = acc.courses.remove(&id) {
                        course
                    } else {
                        b.flow().velocity.clone() + acc.deltas.remove(&id).unwrap_or_else(Vec2::zero)
                    };
                    if acc.walls.contains(&id) {
                        if let Some(c) = self.state.elastic.as_ref().and_then(|el| el.container.clone()) {
                            // Reflect each component still moving outward at a wall it touches.
                            let p = b.at(tick);
                            let before = v.clone();
                            if (p.x <= &c.min.x + &b.radius && v.x < r(0))
                                || (p.x >= &c.max.x - &b.radius && v.x > r(0))
                            {
                                v.x = -v.x.clone();
                            }
                            if (p.y <= &c.min.y + &b.radius && v.y < r(0))
                                || (p.y >= &c.max.y - &b.radius && v.y > r(0))
                            {
                                v.y = -v.y.clone();
                            }
                            acc.wall_momentum = acc.wall_momentum.clone() + (before - v.clone()) * b.mass.clone();
                        }
                    }
                    if acc.elastic_only.contains(&id) && v == b.velocity_at(tick) {
                        // A bounce or wall that leaves the velocity unchanged opens no revision.
                        scan.commit = Some(CommitPrep::ValidateAffected {
                            tick,
                            acc,
                            affected,
                            next: next + 1,
                            velocities,
                        });
                        return Ok(None);
                    }
                    Inertial::new(tick, b.at(tick), v.clone())?;
                    velocities.push((id, v));
                    scan.commit = Some(CommitPrep::ValidateAffected {
                        tick,
                        acc,
                        affected,
                        next: next + 1,
                        velocities,
                    });
                }
                Ok(None)
            }
            CommitPrep::ValidateNotes {
                tick,
                acc,
                velocities,
                note_i,
                mut notification_counts,
            } => {
                if note_i >= acc.notifications.len() {
                    for (source, count) in &notification_counts {
                        self.state
                            .emitter_sequence
                            .get(source)
                            .copied()
                            .unwrap_or(0)
                            .checked_add(*count)
                            .ok_or_else(|| {
                                EngineError::ResourceLimit("emitter sequence exhausted".into())
                            })?;
                    }
                    scan.commit = Some(CommitPrep::Publish {
                        tick,
                        acc,
                        velocities,
                    });
                } else {
                    let (source, target) = acc.notifications[note_i];
                    self.decode(source)?;
                    self.decode(target)?;
                    *notification_counts.entry(source).or_default() += 1;
                    scan.commit = Some(CommitPrep::ValidateNotes {
                        tick,
                        acc,
                        velocities,
                        note_i: note_i + 1,
                        notification_counts,
                    });
                }
                Ok(None)
            }
            CommitPrep::Publish {
                tick,
                acc,
                velocities,
            } => {
                let published = self.publish_prepared_batch(tick, acc, velocities)?;
                Ok(Some((tick, published.0, published.1, published.2)))
            }
        }
    }
    fn publish_prepared_batch(
        &mut self,
        tick: i128,
        acc: BatchEffects,
        velocities: Vec<(u64, Vec2)>,
    ) -> Result<(usize, Vec<u64>, bool), EngineError> {
        let dirty: Vec<u64> = velocities.iter().map(|(id, _)| *id).collect();
        for (id, v) in velocities {
            self.apply_course_change(id, tick, v)?;
        }
        for (id, value) in &acc.residuals {
            if let Some(b) = self.state.bodies.get_mut(id) {
                b.energy_residual = value.clone();
            }
        }
        if let Some(el) = self.state.elastic.as_mut() {
            el.wall_momentum = el.wall_momentum.clone() + acc.wall_momentum.clone();
        }
        for (a, b, _, _) in &acc.contacts {
            let aa = self.decode(*a)?;
            let bb = self.decode(*b)?;
            self.state
                .contacts
                .insert((*a, *b, aa.revision, bb.revision));
        }
        for id in acc.received {
            self.state.signals.remove(&id);
        }
        for id in acc.fired_courses {
            self.state.scheduled_courses.remove(&id);
        }
        let range_rebased = !acc.fired_ranges.is_empty();
        for s in acc.fired_ranges {
            self.apply_range_course(s.lo, s.hi, tick, s.velocity)?;
            self.state.scheduled_range_courses.remove(&s.id);
        }
        let n = acc.records.len();
        for e in acc.records {
            self.note_signal_arrival(&e);
            self.state.events.insert(e.id.clone(), e);
        }
        self.state.clock = tick;
        self.metrics.committed_events += n as u64;
        let _ = self.apply_received_policy()?;
        self.index_broadcast_receptions()?;
        for (source, target) in acc.notifications {
            self.apply_command(
                source,
                Command::SendSignal {
                    target,
                    payload: Payload::Ping,
                },
            )?;
        }
        Ok((n, dirty, range_rebased))
    }
    fn step_after_commit(&mut self, scan: &mut Scan) -> Result<bool, EngineError> {
        let Some(after) = scan.after.take() else {
            return Ok(false);
        };
        match after {
            AfterCommit::Reduce {
                tick,
                dirty,
                range_rebased,
            } => {
                if let Some(key) = scan
                    .candidates
                    .iter()
                    .find(|(_, c)| c.tick == tick)
                    .map(|(k, _)| k.clone())
                {
                    scan.candidates.remove(&key);
                    scan.after = Some(AfterCommit::Reduce {
                        tick,
                        dirty,
                        range_rebased,
                    });
                } else {
                    scan.heap.clear();
                    scan.after = Some(AfterCommit::RebuildHeap {
                        dirty,
                        range_rebased,
                        next: scan.candidates.keys().next().cloned(),
                    });
                }
                Ok(false)
            }
            AfterCommit::RebuildHeap {
                dirty,
                range_rebased,
                next,
            } => {
                if let Some(key) = next {
                    if let Some(c) = scan.candidates.get(&key) {
                        scan.heap.push(Reverse((c.tick, key.clone())));
                    }
                    let following = scan
                        .candidates
                        .range((Excluded(key), Unbounded))
                        .next()
                        .map(|(k, _)| k.clone());
                    scan.after = Some(AfterCommit::RebuildHeap {
                        dirty,
                        range_rebased,
                        next: following,
                    });
                } else {
                    scan.after = Some(AfterCommit::Apply {
                        dirty,
                        range_rebased,
                    });
                }
                Ok(false)
            }
            AfterCommit::Apply {
                dirty,
                range_rebased,
            } => {
                if range_rebased {
                    scan.after = Some(AfterCommit::Discard);
                } else if dirty.is_empty() {
                    self.metrics.quiet_commits += 1;
                    if self.frontier_needs_resume(scan) {
                        scan.repair = Some(Repair::Enqueue);
                    }
                } else {
                    self.begin_repair(scan, dirty);
                }
                Ok(false)
            }
            AfterCommit::Discard => Ok(true),
        }
    }
    pub fn advance(
        &mut self,
        target: i128,
        budget: WorkBudget,
    ) -> Result<AdvanceResult, EngineError> {
        if target < self.state.clock {
            return Err(EngineError::Invalid(
                "cannot advance committed history backwards".into(),
            ));
        }
        let mut coupled_ops = 0;
        if self.coupled.as_ref().is_some_and(|d| !d.is_ready()) {
            let mut rest = WorkBudget {
                operations: budget.operations,
                max_events: budget.max_events,
            };
            let before = rest.operations;
            self.poll_coupled(&mut rest)?;
            coupled_ops = before.saturating_sub(rest.operations);
            if self.coupled.as_ref().is_some_and(|d| !d.is_ready()) {
                return Ok(AdvanceResult {
                    committed_through: self.state.clock,
                    target,
                    complete: false,
                    operations: coupled_ops.max(1),
                    events: 0,
                    pending_jobs: self.coupled_pending_jobs()
                        + self.pending.as_ref().map_or(0, |s| s.pending_work()),
                });
            }
        }
        let budget = WorkBudget {
            operations: budget.operations.saturating_sub(coupled_ops),
            max_events: budget.max_events,
        };
        if budget.operations == 0 && self.state.clock < target {
            return Ok(AdvanceResult {
                committed_through: self.state.clock,
                target,
                complete: false,
                operations: coupled_ops.max(1),
                events: 0,
                pending_jobs: self.coupled_pending_jobs()
                    + self.pending.as_ref().map_or(0, |s| s.pending_work()),
            });
        }
        let mut used = 0;
        let mut events = 0;
        while self.state.clock < target && used < budget.operations && events < budget.max_events {
            if self.pending.as_ref().is_some_and(|s| s.target != target) {
                self.pending = None;
            }
            if self.pending.is_none() {
                self.begin_scan(target)?;
            }
            let mut scan = self.pending.take().unwrap();
            while used < budget.operations {
                if scan.prep.is_none() && scan.repair.is_none() {
                    break;
                }
                if let Err(err) = self.step_construction(&mut scan) {
                    self.pending = Some(scan);
                    return Err(err);
                }
                used += 1;
                self.metrics.search_operations += 1;
            }
            if scan.prep.is_some() || scan.repair.is_some() {
                self.pending = Some(scan);
                break;
            }
            while used < budget.operations {
                if let Some(job) = scan.jobs.pop_front() {
                    if let Err(err) = self.process_job(job.clone(), &mut scan) {
                        scan.jobs.push_front(job);
                        self.pending = Some(scan);
                        return Err(err);
                    }
                    used += 1;
                    self.metrics.search_operations += 1;
                } else {
                    break;
                }
            }
            if !scan.jobs.is_empty() {
                self.pending = Some(scan);
                break;
            }
            let mut discarded = false;
            while used < budget.operations && scan.after.is_some() {
                match self.step_after_commit(&mut scan) {
                    Ok(discard) => {
                        used += 1;
                        self.metrics.search_operations += 1;
                        if discard {
                            discarded = true;
                            break;
                        }
                    }
                    Err(e) => {
                        self.pending = Some(scan);
                        return Err(e);
                    }
                }
            }
            if discarded {
                used = used.max(1);
                continue;
            }
            if scan.after.is_some() {
                self.pending = Some(scan);
                break;
            }
            // The finished after-commit step may have scheduled a repair of the bodies the
            // last batch changed. Their new pairs must be searched before anything else
            // commits; otherwise a later commit overtakes (or overwrites) that repair and
            // contacts with freshly stopped or redirected bodies are missed or late.
            if scan.commit.is_none()
                && (scan.prep.is_some() || scan.repair.is_some() || !scan.jobs.is_empty())
            {
                self.pending = Some(scan);
                continue;
            }
            if scan.commit.is_none() {
                if let Some(Reverse((tick, _))) = scan.heap.peek() {
                    let tick = *tick;
                    scan.commit = Some(CommitPrep::Collect {
                        tick,
                        next: None,
                        batch: Vec::new(),
                    });
                }
            }
            while used < budget.operations && scan.commit.is_some() {
                match self.step_commit(&mut scan) {
                    Ok(None) => {
                        used += 1;
                        self.metrics.search_operations += 1;
                    }
                    Ok(Some((tick, n, dirty, range_rebased))) => {
                        used += 1;
                        self.metrics.search_operations += 1;
                        events += n;
                        if self.incremental_sap {
                            scan.after = Some(AfterCommit::Reduce {
                                tick,
                                dirty,
                                range_rebased,
                            });
                        } else {
                            scan.after = Some(AfterCommit::Discard);
                        }
                    }
                    Err(e) => {
                        self.pending = Some(scan);
                        return Err(e);
                    }
                }
            }
            if scan.commit.is_some() || scan.after.is_some() {
                self.pending = Some(scan);
                if used >= budget.operations {
                    break;
                }
                continue;
            }
            if self.force_rescan {
                self.force_rescan = false;
                self.pending = None;
                used = used.max(1);
                continue;
            }
            if scan.heap.peek().is_none()
                && scan.commit.is_none()
                && scan.after.is_none()
                && scan.prep.is_none()
                && scan.repair.is_none()
                && scan.jobs.is_empty()
            {
                self.state.clock = target;
            } else {
                self.pending = Some(scan);
            }
            // A scan with no jobs still makes progress without spending a timestep.
            used = used.max(1);
        }
        self.index_broadcast_receptions()?;
        self.sync_moving_compact();
        Ok(AdvanceResult {
            committed_through: self.state.clock,
            target,
            complete: self.state.clock == target,
            operations: used.saturating_add(coupled_ops),
            events,
            pending_jobs: self.coupled_pending_jobs()
                + self.pending.as_ref().map_or(0, |s| s.pending_work()),
        })
    }
    pub fn advance_fully(&mut self, target: i128) -> Result<AdvanceResult, EngineError> {
        let mut total = 0;
        let mut event_count = 0;
        loop {
            let mut result = self.advance(target, WorkBudget::new(100_000))?;
            total += result.operations;
            event_count += result.events;
            if result.complete {
                result.operations = total;
                result.events = event_count;
                return Ok(result);
            }
        }
    }
    /// Hash a declared completed cut; search/materialization coverage is excluded.
    pub fn history_digest(&self, through: i128) -> Result<String, EngineError> {
        if through < 0 || through > self.state.clock {
            return Err(EngineError::Invalid("digest cut is not committed".into()));
        }
        let facts: Vec<_> = self
            .state
            .events
            .values()
            .filter(|e| e.tick <= through)
            .collect();
        Ok(digest(&(
            LAW_ID,
            self.state.seed,
            &self.state.branch,
            &self.state.genesis_digest,
            through,
            facts,
        )))
    }
    pub fn sorted_events(&self) -> Vec<&EventRecord> {
        let mut e: Vec<_> = self.state.events.values().collect();
        e.sort_by(|a, b| (a.tick, &a.id).cmp(&(b.tick, &b.id)));
        e
    }

    pub(crate) fn note_signal_arrival(&mut self, e: &EventRecord) {
        if e.kind != "signal_arrived" || e.subjects.len() < 2 {
            return;
        }
        let observer = e.subjects[1];
        self.signal_arrivals
            .entry(observer)
            .or_default()
            .push((e.tick, e.predecessors.clone()));
    }

    pub(crate) fn rebuild_signal_arrivals(&mut self) {
        self.signal_arrivals.clear();
        let arrivals: Vec<(u64, i128, Vec<String>)> = self
            .state
            .events
            .values()
            .filter(|e| e.kind == "signal_arrived" && e.subjects.len() >= 2)
            .map(|e| (e.subjects[1], e.tick, e.predecessors.clone()))
            .collect();
        for (observer, tick, preds) in arrivals {
            self.signal_arrivals
                .entry(observer)
                .or_default()
                .push((tick, preds));
        }
    }

    /// Events examined to answer received-knowledge for one observer.
    /// Full-history scan is `state.events.len()`; the index is this observer's arrivals.
    pub fn knowledge_scan_width(&self, observer: u64) -> (usize, usize) {
        let full = self.state.events.len();
        let indexed = self
            .signal_arrivals
            .get(&observer)
            .map(|v| v.len())
            .unwrap_or(0);
        (full, indexed)
    }
    pub fn clear_derived(&mut self) {
        self.pending = None;
        self.sensor = None;
        if let Some(diag) = self.coupled.as_mut() {
            diag.clear_consumer_cache();
        }
    }
    pub fn sensor_pending(&self) -> bool {
        self.sensor.as_ref().is_some_and(|s| !s.complete)
    }
    pub fn cancel_sensor(&mut self) {
        self.sensor = None;
    }
    pub fn from_state(state: CanonicalState) -> Result<Self, EngineError> {
        let mut state = state;
        if state.genesis_families.is_empty() {
            state.genesis_families = state.families.clone();
        }
        let mut e = Self {
            state,
            metrics: Metrics::default(),
            pending: None,
            sensor: None,
            max_resident_bodies: resident_body_capacity(DEFAULT_MEMORY_BUDGET_BYTES),
            max_pending_jobs: 1_000_000,
            incremental_sap: true,
            causal_components: Vec::new(),
            coupled: None,
            moving_compact: None,
            policy: None,
            force_rescan: false,
            scheduler: CompositionScheduler::default(),
            archive: None,
            scan_filter: None,
            signal_arrivals: BTreeMap::new(),
        };
        e.rebuild_signal_arrivals();
        e.validate()?;
        Ok(e)
    }
    /// Re-evaluate from the initial generators and ordered external commands.
    /// Contacts, received signals, notifications and derived search are rebuilt.
    pub fn replay(&self) -> Result<Self, EngineError> {
        let families = if self.state.genesis_families.is_empty() {
            self.state.families.clone()
        } else {
            self.state.genesis_families.clone()
        };
        let mut e = Self::new(
            self.state.seed,
            self.state.genesis_bodies.values().cloned().collect(),
            families,
        )?;
        e.state.branch = self.state.branch.clone();
        e.policy = self.policy.clone();
        if let Some(el) = &self.state.elastic {
            e.state.elastic = Some(ElasticState {
                container: el.container.clone(),
                response_quantum: el.response_quantum,
                wall_momentum: Vec2::zero(),
            });
        }
        if e.state.genesis_digest != self.state.genesis_digest {
            return Err(EngineError::Checkpoint(
                "genesis commitment mismatch".into(),
            ));
        }
        for recorded in &self.state.interventions {
            e.advance_fully(recorded.tick)?;
            if e.intervene(recorded.observer, recorded.command.clone())? != recorded.event_id {
                return Err(EngineError::Checkpoint(
                    "intervention replay mismatch".into(),
                ));
            }
        }
        e.advance_fully(self.state.clock)?;
        if serde_json::to_vec(&e.state).map_err(|x| EngineError::Checkpoint(x.to_string()))?
            != serde_json::to_vec(&self.state)
                .map_err(|x| EngineError::Checkpoint(x.to_string()))?
        {
            return Err(EngineError::Checkpoint("canonical replay mismatch".into()));
        }
        Ok(e)
    }
    /// Return the most recent received emission from each target at this observation cut.
    /// A signal's origin is observed; inferred present positions are not silently substituted.
    /// Convenience wrapper: runs to completion or a hard resource cap. Does not store a continuation.
    pub fn observe(
        &self,
        observer: u64,
        now: i128,
        targets: &[u64],
    ) -> Result<Vec<Observation>, EngineError> {
        let mut job = self.begin_sensor(observer, now, targets)?;
        self.drive_sensor(&mut job, usize::MAX)?;
        if job.complete {
            Ok(job.observations)
        } else {
            Err(EngineError::ResourceLimit(
                "sensor family refinement budget exhausted".into(),
            ))
        }
    }
    /// Resumable sensor query. Small `WorkBudget` yields; resume with the same
    /// observer/cut/targets. Cancel via `clear_derived`. Incomplete results are
    /// pending, never a silent empty sky. Does not mutate canonical history.
    pub fn observe_with_budget(
        &mut self,
        observer: u64,
        now: i128,
        targets: &[u64],
        budget: WorkBudget,
    ) -> Result<ObserveResult, EngineError> {
        let mut job = match self.sensor.take() {
            Some(existing) if existing.matches(observer, now, targets) => existing,
            _ => self.begin_sensor(observer, now, targets)?,
        };
        let before_refinements = job.refinement_steps;
        let ops = match self.drive_sensor(&mut job, budget.operations) {
            Ok(n) => n,
            Err(err) => {
                self.sensor = None;
                return Err(err);
            }
        };
        job.charged = job.charged.saturating_add(ops);
        self.metrics.sensor_ops = self.metrics.sensor_ops.saturating_add(ops as u64);
        self.metrics.sensor_refinements = self
            .metrics
            .sensor_refinements
            .saturating_add((job.refinement_steps - before_refinements) as u64);
        let result = ObserveResult {
            observations: job.observations.clone(),
            complete: job.complete,
            operations: ops,
            pending_jobs: job.pending_work(self.state.families.len()),
            charged_sensor_ops: job.charged,
            refinement_steps: job.refinement_steps,
        };
        if job.complete {
            self.sensor = None;
        } else {
            self.sensor = Some(job);
        }
        Ok(result)
    }
    fn begin_sensor(
        &self,
        observer: u64,
        now: i128,
        targets: &[u64],
    ) -> Result<SensorJob, EngineError> {
        if now < 0 || now > self.state.clock {
            return Err(EngineError::Invalid("uncommitted observation".into()));
        }
        let receiver = self.decode(observer)?.at(now);
        Ok(SensorJob {
            observer,
            now,
            targets: targets.to_vec(),
            receiver,
            index: 0,
            inner: SensorInner::SelectTarget,
            observations: Vec::new(),
            complete: targets.is_empty(),
            refinement_steps: 0,
            charged: 0,
        })
    }
    fn drive_sensor(&self, job: &mut SensorJob, max_ops: usize) -> Result<usize, EngineError> {
        let mut ops = 0;
        while ops < max_ops && !job.complete {
            self.sensor_step(job)?;
            ops += 1;
        }
        Ok(ops)
    }
    fn finish_sensor_target(job: &mut SensorJob) {
        job.index += 1;
        job.inner = SensorInner::SelectTarget;
        if job.index >= job.targets.len() {
            job.complete = true;
        }
    }
    fn emit_sensor_target(job: &mut SensorJob, entity: u64, emission_tick: i128, emission: Vec2) {
        job.observations.push(Observation {
            entity,
            emission_tick,
            reception_tick: job.now,
            position: emission,
        });
        Self::finish_sensor_target(job);
    }
    fn sensor_step(&self, job: &mut SensorJob) -> Result<(), EngineError> {
        if job.complete {
            return Ok(());
        }
        if matches!(job.inner, SensorInner::OccludeFamilies(_)) {
            return self.sensor_refine_family(job);
        }
        if job.index >= job.targets.len() {
            job.complete = true;
            return Ok(());
        }
        let id = job.targets[job.index];
        if id == job.observer {
            Self::finish_sensor_target(job);
            return Ok(());
        }
        let b = self.decode(id)?;
        if !geometry::causal_reachable(0, &b.at(0), job.now, &job.receiver) {
            Self::finish_sensor_target(job);
            return Ok(());
        }
        let (mut lo, mut hi) = (0, job.now);
        while lo < hi {
            let mid = lo + (hi - lo) / 2 + 1;
            if geometry::causal_reachable(mid, &b.at(mid), job.now, &job.receiver) {
                lo = mid;
            } else {
                hi = mid - 1;
            }
        }
        let emission = b.at(lo);
        let blocked = self.state.bodies.values().any(|o| {
            o.id != job.observer
                && o.id != id
                && self.occludes(o, &emission, lo, &job.receiver, job.now)
        });
        if blocked {
            Self::finish_sensor_target(job);
            return Ok(());
        }
        if lo >= job.now || self.state.families.is_empty() {
            Self::emit_sensor_target(job, id, lo, emission);
            return Ok(());
        }
        let ray = Inertial {
            epoch: lo,
            origin: emission.clone(),
            velocity: (job.receiver.clone() - emission.clone()) * (r(1) / r(job.now - lo)),
        };
        let domain = TickInterval {
            start: lo + 1,
            end: job.now,
        };
        let first = &self.state.families[0];
        job.inner = SensorInner::OccludeFamilies(Box::new(FamilyOcclusion {
            target: id,
            emission_tick: lo,
            emission,
            ray,
            domain,
            family_index: 0,
            ranges: vec![(first.first_id, first.first_id + (first.count - 1))],
        }));
        Ok(())
    }
    fn sensor_refine_family(&self, job: &mut SensorJob) -> Result<(), EngineError> {
        let SensorInner::OccludeFamilies(work) = &job.inner else {
            return Ok(());
        };
        let mut work = work.as_ref().clone();
        if work.ranges.is_empty() {
            work.family_index += 1;
            if work.family_index >= self.state.families.len() {
                Self::emit_sensor_target(job, work.target, work.emission_tick, work.emission);
                return Ok(());
            }
            let family = &self.state.families[work.family_index];
            work.ranges
                .push((family.first_id, family.first_id + (family.count - 1)));
        }
        if job.refinement_steps >= self.max_pending_jobs {
            return Err(EngineError::ResourceLimit(
                "sensor family refinement budget exhausted".into(),
            ));
        }
        let (lo, hi) = work.ranges.pop().ok_or_else(|| {
            EngineError::Invalid("sensor family range stack underflow".into())
        })?;
        job.refinement_steps += 1;
        let family = &self.state.families[work.family_index];
        let mut occluded = false;
        let mut families_done = false;
        if self.family_range_away(family, lo, hi, &work.ray, work.domain) {
            families_done =
                work.ranges.is_empty() && work.family_index + 1 >= self.state.families.len();
        } else if lo == hi {
            let excluded = [job.observer, work.target];
            if !excluded.contains(&lo)
                && !self.state.bodies.contains_key(&lo)
                && geometry::first_contact_piecewise(
                    std::slice::from_ref(&work.ray),
                    &family.member_segments(lo).unwrap(),
                    &family.radius,
                    work.domain,
                )
                .is_some()
            {
                occluded = true;
            } else {
                families_done =
                    work.ranges.is_empty() && work.family_index + 1 >= self.state.families.len();
            }
        } else {
            let mid = lo + (hi - lo) / 2;
            work.ranges.push((mid + 1, hi));
            work.ranges.push((lo, mid));
        }
        if occluded {
            Self::finish_sensor_target(job);
            return Ok(());
        }
        if families_done {
            Self::emit_sensor_target(job, work.target, work.emission_tick, work.emission);
            return Ok(());
        }
        job.inner = SensorInner::OccludeFamilies(Box::new(work));
        Ok(())
    }
    fn family_range_away(
        &self,
        family: &Family,
        lo: u64,
        hi: u64,
        ray: &Inertial,
        domain: TickInterval,
    ) -> bool {
        let t0 = domain.start.saturating_sub(1);
        let t1 = domain.end;
        let Some(samples) = family.range_samples(lo, hi, t0, t1) else {
            return false;
        };
        let rel: Vec<Vec2> = samples
            .into_iter()
            .map(|(t, p)| p - ray.state_at(t))
            .collect();
        if rel.is_empty() {
            return false;
        }
        rel.iter().all(|p| p.x > family.radius)
            || rel.iter().all(|p| p.x < -&family.radius)
            || rel.iter().all(|p| p.y > family.radius)
            || rel.iter().all(|p| p.y < -&family.radius)
    }
    fn occludes(&self, b: &Body, start: &Vec2, from: i128, end: &Vec2, to: i128) -> bool {
        // Finite light segments are tested against every physical trajectory segment.
        if from == to {
            return false;
        }
        let velocity = (end.clone() - start.clone()) * (r(1) / r(to - from));
        // Lightlike motion is admissible to geometric predicates, not the massive constructor.
        let ray = Inertial {
            epoch: from,
            origin: start.clone(),
            velocity,
        };
        for (i, s) in b.segments.iter().enumerate() {
            let lower = from.max(s.epoch);
            let upper = to.min(b.segments.get(i + 1).map_or(to, |n| n.epoch));
            if lower < upper
                && geometry::first_contact(
                    &ray,
                    s,
                    &b.radius,
                    TickInterval {
                        start: lower.saturating_add(1),
                        end: upper,
                    },
                )
                .is_some()
            {
                return true;
            }
        }
        false
    }
}
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Observation {
    pub entity: u64,
    pub emission_tick: i128,
    pub reception_tick: i128,
    pub position: Vec2,
}
