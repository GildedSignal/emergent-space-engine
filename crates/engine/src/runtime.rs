//! Cooperative event execution for the versioned inertial causal laboratory law.
//! Search and caches are derived. Only completed causal cuts and event facts commit.
use crate::{
    geometry::{self, TickInterval},
    math::{r, Rational, Vec2},
    population::Family,
    propagator::Inertial,
    LAW_ID,
};
use serde::{Deserialize, Serialize};
use std::{
    cmp::Reverse,
    collections::{BTreeMap, BTreeSet, BinaryHeap, VecDeque},
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
    Impulse { delta: Vec2 },
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
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq)]
pub struct Metrics {
    pub search_operations: u64,
    pub certified_rejections: u64,
    pub exact_leaf_queries: u64,
    pub committed_events: u64,
    pub scans: u64,
    pub broadphase_boxes: u64,
    pub broadphase_pairs: u64,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CanonicalState {
    pub law: String,
    pub seed: u64,
    pub branch: String,
    pub genesis_digest: String,
    pub genesis_bodies: BTreeMap<u64, Body>,
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
}

#[derive(Clone, Debug)]
enum Item {
    Body(u64),
    Family { index: usize, lo: u64, hi: u64 },
}
#[derive(Clone, Debug)]
enum Job {
    Pair(Item, Item),
    Signal(String),
}
#[derive(Clone, Debug)]
enum Action {
    Contact(u64, u64),
    Arrival(String),
}
#[derive(Clone, Debug)]
struct Candidate {
    tick: i128,
    key: String,
    action: Action,
}
#[derive(Clone, Debug)]
struct Scan {
    target: i128,
    jobs: VecDeque<Job>,
    heap: BinaryHeap<Reverse<(i128, String)>>,
    candidates: BTreeMap<String, Candidate>,
}

#[derive(Clone, Debug)]
pub struct Engine {
    pub state: CanonicalState,
    pub metrics: Metrics,
    pending: Option<Scan>,
    pub max_resident_bodies: usize,
    pub max_pending_jobs: usize,
}

fn digest<T: Serialize>(value: &T) -> String {
    blake3::hash(&serde_json::to_vec(value).expect("serializable canonical facts"))
        .to_hex()
        .to_string()
}
fn event(
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
                    && a.name == f.name
                    && a.trajectory == f.trajectory
                    && a.stride == f.stride
                    && a.radius == f.radius
                    && a.mass == f.mass
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
                interventions: Vec::new(),
                clock: 0,
                bodies: map,
                families,
                signals: BTreeMap::new(),
                events: BTreeMap::new(),
                emitter_sequence: BTreeMap::new(),
                contacts: BTreeSet::new(),
                actuator_momentum: Vec2::zero(),
            },
            metrics: Metrics::default(),
            pending: None,
            max_resident_bodies: 100_000,
            max_pending_jobs: 1_000_000,
        };
        engine.validate()?;
        Ok(engine)
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
            let flow = f.member(id).unwrap();
            return Ok(Body::new(
                id,
                format!("{} · {}", f.name, id),
                flow,
                f.radius.clone(),
                f.mass.clone(),
            ));
        }
        Err(EngineError::UnknownIdentity(id))
    }
    fn family_for(&self, id: u64) -> Option<&Family> {
        let n = self.state.families.partition_point(|f| f.first_id <= id);
        n.checked_sub(1)
            .and_then(|i| self.state.families.get(i))
            .filter(|f| f.contains(id))
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
                self.materialize(observer)?;
                let before = self.state.bodies[&observer].flow().velocity.clone();
                self.set_velocity(observer, t, velocity.clone())?;
                let e = event(
                    t,
                    "burn",
                    vec![observer],
                    vec![],
                    digest(&(before, velocity, self.state.interventions.len())),
                );
                let id = e.id.clone();
                self.state.events.insert(id.clone(), e);
                self.pending = None;
                Ok(id)
            }
            Command::SendSignal { target, payload } => {
                self.decode(target)?;
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
                self.pending = None;
                Ok(id)
            }
        }
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
    fn start_scan(&mut self, target: i128) -> Result<(), EngineError> {
        let mut jobs = VecDeque::new();
        // Sweep conservative swept boxes in a shared co-moving frame. Shared drift
        // cancels before bounding, so an ancient convoy does not fill its whole path.
        struct Entry {
            item: Item,
            min: Vec2,
            max: Vec2,
        }
        let mut items: Vec<_> = self.state.bodies.keys().copied().map(Item::Body).collect();
        for (index, f) in self.state.families.iter().enumerate() {
            let end = f.first_id + (f.count - 1);
            let mut cursor = Some(f.first_id);
            // Exceptions are not members of the original generated trajectory.
            // Subtract their identities once, before spatial refinement, rather
            // than rediscovering each exclusion at the bottom of a binary tree.
            for (&id, _) in self.state.bodies.range(f.first_id..=end) {
                if let Some(lo) = cursor {
                    if lo < id {
                        items.push(Item::Family {
                            index,
                            lo,
                            hi: id - 1,
                        });
                    }
                }
                cursor = if id == end { None } else { Some(id + 1) };
            }
            if let Some(lo) = cursor {
                items.push(Item::Family { index, lo, hi: end });
            }
        }
        if items.len() > self.max_pending_jobs {
            return Err(EngineError::ResourceLimit(
                "broad-phase object budget exceeded".into(),
            ));
        }
        let drift = self
            .state
            .families
            .first()
            .map(|f| f.trajectory.velocity.clone())
            .unwrap_or_else(Vec2::zero);
        let mut boxes = Vec::with_capacity(items.len());
        for item in items {
            let (a, rad) = self.endpoint(&item, false)?;
            let (b, _) = self.endpoint(&item, true)?;
            let mut points = Vec::with_capacity(4);
            for flow in [&a, &b] {
                for t in [self.state.clock, target] {
                    points.push(flow.state_at(t) - drift.clone() * r(t));
                }
            }
            let min = Vec2 {
                x: points.iter().map(|p| p.x.clone()).min().unwrap() - &rad,
                y: points.iter().map(|p| p.y.clone()).min().unwrap() - &rad,
            };
            let max = Vec2 {
                x: points.iter().map(|p| p.x.clone()).max().unwrap() + &rad,
                y: points.iter().map(|p| p.y.clone()).max().unwrap() + &rad,
            };
            boxes.push(Entry { item, min, max });
        }
        self.metrics.broadphase_boxes += boxes.len() as u64;
        let spread = |axis: bool| -> Rational {
            let centers: Vec<_> = boxes
                .iter()
                .map(|b| {
                    if axis {
                        &b.min.x + &b.max.x
                    } else {
                        &b.min.y + &b.max.y
                    }
                })
                .collect();
            centers.iter().max().cloned().unwrap_or_else(|| r(0))
                - centers.iter().min().cloned().unwrap_or_else(|| r(0))
        };
        let x_axis = spread(true) >= spread(false);
        boxes.sort_by(|a, b| {
            if x_axis {
                a.min.x.cmp(&b.min.x)
            } else {
                a.min.y.cmp(&b.min.y)
            }
        });
        let mut active: Vec<usize> = Vec::new();
        for (i, b) in boxes.iter().enumerate() {
            active.retain(|j| {
                if x_axis {
                    boxes[*j].max.x >= b.min.x
                } else {
                    boxes[*j].max.y >= b.min.y
                }
            });
            for j in &active {
                let a = &boxes[*j];
                self.metrics.broadphase_pairs += 1;
                if a.min.x <= b.max.x
                    && b.min.x <= a.max.x
                    && a.min.y <= b.max.y
                    && b.min.y <= a.max.y
                {
                    if jobs.len() >= self.max_pending_jobs {
                        return Err(EngineError::ResourceLimit(
                            "dense interaction frontier exceeds job capacity".into(),
                        ));
                    }
                    jobs.push_back(Job::Pair(a.item.clone(), b.item.clone()));
                } else {
                    self.metrics.certified_rejections += 1;
                }
            }
            active.push(i);
        }
        for id in self.state.signals.keys() {
            if jobs.len() >= self.max_pending_jobs {
                return Err(EngineError::ResourceLimit(
                    "combined frontier exceeds job capacity".into(),
                ));
            }
            jobs.push_back(Job::Signal(id.clone()));
        }
        self.pending = Some(Scan {
            target,
            jobs,
            heap: BinaryHeap::new(),
            candidates: BTreeMap::new(),
        });
        self.metrics.scans += 1;
        Ok(())
    }
    fn endpoint(&self, item: &Item, last: bool) -> Result<(Inertial, Rational), EngineError> {
        match item {
            Item::Body(id) => {
                let b = self.decode(*id)?;
                Ok((b.flow().clone(), b.radius))
            }
            Item::Family { index, lo, hi } => {
                let f = &self.state.families[*index];
                Ok((
                    f.member(if last { *hi } else { *lo }).unwrap(),
                    f.radius.clone(),
                ))
            }
        }
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
        let (a0, ra) = self.endpoint(a, false)?;
        let (a1, _) = self.endpoint(a, true)?;
        let (b0, rb) = self.endpoint(b, false)?;
        let (b1, _) = self.endpoint(b, true)?;
        let mut minx = None;
        let mut maxx = None;
        let mut miny = None;
        let mut maxy = None;
        for x in [&a0, &a1] {
            for y in [&b0, &b1] {
                for t in [from, to] {
                    let d = x.state_at(t) - y.state_at(t);
                    minx = Some(minx.map_or(d.x.clone(), |v: Rational| v.min(d.x.clone())));
                    maxx = Some(maxx.map_or(d.x.clone(), |v: Rational| v.max(d.x)));
                    miny = Some(miny.map_or(d.y.clone(), |v: Rational| v.min(d.y.clone())));
                    maxy = Some(maxy.map_or(d.y.clone(), |v: Rational| v.max(d.y)));
                }
            }
        }
        fn nearest(lo: Rational, hi: Rational) -> Rational {
            if lo > r(0) {
                lo
            } else if hi < r(0) {
                -hi
            } else {
                r(0)
            }
        }
        let dx = nearest(minx.unwrap(), maxx.unwrap());
        let dy = nearest(miny.unwrap(), maxy.unwrap());
        let rr = ra + rb;
        Ok(dx.clone() * dx + dy.clone() * dy > rr.clone() * rr)
    }
    fn process_job(&mut self, job: Job, scan: &mut Scan) -> Result<(), EngineError> {
        let start = self
            .state
            .clock
            .checked_add(1)
            .ok_or_else(|| EngineError::Invalid("time exhausted".into()))?;
        // Once an earlier event is known, later candidates need not be discovered.
        let end = scan
            .heap
            .peek()
            .map_or(scan.target, |x| scan.target.min(x.0 .0));
        match job {
            Job::Signal(id) => {
                let s = &self.state.signals[&id];
                let b = self.decode(s.target)?;
                let lower = start.max(s.tick.saturating_add(1));
                if lower <= end {
                    self.metrics.exact_leaf_queries += 1;
                    if let Some(tick) = geometry::first_signal_arrival(
                        s.tick,
                        &s.position,
                        b.flow(),
                        TickInterval { start: lower, end },
                    ) {
                        let key = format!("signal:{id}");
                        scan.heap.push(Reverse((tick, key.clone())));
                        scan.candidates.insert(
                            key.clone(),
                            Candidate {
                                tick,
                                key,
                                action: Action::Arrival(id),
                            },
                        );
                    }
                }
            }
            Job::Pair(a, b) => {
                if self.family_exception(&a) || self.family_exception(&b) {
                    return Ok(());
                }
                if self.member_id(&a).is_some() && self.member_id(&a) == self.member_id(&b) {
                    return Ok(());
                }
                if self.disjoint(&a, &b, self.state.clock, end)? {
                    self.metrics.certified_rejections += 1;
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
                        return Ok(());
                    }
                    self.metrics.exact_leaf_queries += 1;
                    if let Some(tick) = geometry::first_contact(
                        aa.flow(),
                        bb.flow(),
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
                    }
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
                }
            }
        }
        Ok(())
    }
    fn commit_batch(
        &mut self,
        tick: i128,
        mut batch: Vec<Candidate>,
    ) -> Result<usize, EngineError> {
        batch.sort_by(|a, b| a.key.cmp(&b.key));
        let mut deltas: BTreeMap<u64, Vec2> = BTreeMap::new();
        let mut stops = BTreeSet::new();
        let mut records = Vec::new();
        let mut contacts = Vec::new();
        let mut received = Vec::new();
        let mut notifications = Vec::new();
        for c in &batch {
            match &c.action {
                Action::Arrival(id) => {
                    let s = &self.state.signals[id];
                    if let Payload::Impulse { delta } = &s.payload {
                        let v = deltas.entry(s.target).or_insert_with(Vec2::zero);
                        *v = v.clone() + delta.clone();
                    }
                    records.push(event(
                        tick,
                        "signal_arrived",
                        vec![s.source, s.target],
                        vec![id.clone()],
                        "causal reception".into(),
                    ));
                    received.push(id.clone());
                }
                Action::Contact(a, b) => {
                    let aa = self.decode(*a)?;
                    let bb = self.decode(*b)?;
                    contacts.push((*a, *b, aa.revision, bb.revision));
                    for body in [&aa, &bb] {
                        if body.stop_on_contact {
                            stops.insert(body.id);
                        }
                        if let Some(target) = body.notify_on_contact {
                            notifications.push((body.id, target));
                        }
                    }
                    records.push(event(
                        tick,
                        "contact",
                        vec![*a, *b],
                        vec![],
                        format!("segments {}:{}", aa.revision, bb.revision),
                    ));
                }
            }
        }
        // Validate the entire simultaneous transaction before mutating canonical state.
        let affected: BTreeSet<_> = deltas
            .keys()
            .copied()
            .chain(stops.iter().copied())
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
        let mut velocities = Vec::new();
        for id in affected {
            let b = self.decode(id)?;
            b.revision.checked_add(1).ok_or_else(|| {
                EngineError::ResourceLimit("trajectory revision exhausted".into())
            })?;
            let v = if stops.contains(&id) {
                Vec2::zero()
            } else {
                b.flow().velocity.clone() + deltas.remove(&id).unwrap_or_else(Vec2::zero)
            };
            Inertial::new(tick, b.at(tick), v.clone())?;
            velocities.push((id, v));
        }
        notifications.sort_unstable();
        notifications.dedup();
        if self.state.signals.len() - received.len() + notifications.len() > self.max_pending_jobs {
            return Err(EngineError::ResourceLimit(
                "contact notifications exceed signal capacity".into(),
            ));
        }
        let mut notification_counts = BTreeMap::<u64, u64>::new();
        for (source, target) in &notifications {
            self.decode(*source)?;
            self.decode(*target)?;
            *notification_counts.entry(*source).or_default() += 1;
        }
        for (source, count) in notification_counts {
            self.state
                .emitter_sequence
                .get(&source)
                .copied()
                .unwrap_or(0)
                .checked_add(count)
                .ok_or_else(|| EngineError::ResourceLimit("emitter sequence exhausted".into()))?;
        }
        for (id, v) in velocities {
            self.set_velocity(id, tick, v)?;
        }
        for (a, b, _, _) in &contacts {
            let aa = self.decode(*a)?;
            let bb = self.decode(*b)?;
            self.state
                .contacts
                .insert((*a, *b, aa.revision, bb.revision));
        }
        for id in received {
            self.state.signals.remove(&id);
        }
        let n = records.len();
        for e in records {
            self.state.events.insert(e.id.clone(), e);
        }
        self.state.clock = tick;
        self.metrics.committed_events += n as u64;
        for (source, target) in notifications {
            self.apply_command(
                source,
                Command::SendSignal {
                    target,
                    payload: Payload::Ping,
                },
            )?;
        }
        Ok(n)
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
        let mut used = 0;
        let mut events = 0;
        while self.state.clock < target && used < budget.operations && events < budget.max_events {
            if self.pending.as_ref().is_some_and(|s| s.target != target) {
                self.pending = None;
            }
            if self.pending.is_none() {
                self.start_scan(target)?;
            }
            let mut scan = self.pending.take().unwrap();
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
            if let Some(Reverse((tick, _))) = scan.heap.peek() {
                let tick = *tick;
                let batch: Vec<_> = scan
                    .candidates
                    .values()
                    .filter(|c| c.tick == tick)
                    .cloned()
                    .collect();
                match self.commit_batch(tick, batch) {
                    Ok(n) => events += n,
                    Err(e) => {
                        self.pending = Some(scan);
                        return Err(e);
                    }
                }
            } else {
                self.state.clock = target;
            }
            // A scan with no jobs still makes progress without spending a timestep.
            used = used.max(1);
        }
        Ok(AdvanceResult {
            committed_through: self.state.clock,
            target,
            complete: self.state.clock == target,
            operations: used,
            events,
            pending_jobs: self.pending.as_ref().map_or(0, |s| s.jobs.len()),
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
    pub fn clear_derived(&mut self) {
        self.pending = None;
    }
    pub fn from_state(state: CanonicalState) -> Result<Self, EngineError> {
        let e = Self {
            state,
            metrics: Metrics::default(),
            pending: None,
            max_resident_bodies: 100_000,
            max_pending_jobs: 1_000_000,
        };
        e.validate()?;
        Ok(e)
    }
    /// Re-evaluate from the initial generators and ordered external commands.
    /// Contacts, received signals, notifications and derived search are rebuilt.
    pub fn replay(&self) -> Result<Self, EngineError> {
        let mut e = Self::new(
            self.state.seed,
            self.state.genesis_bodies.values().cloned().collect(),
            self.state.families.clone(),
        )?;
        e.state.branch = self.state.branch.clone();
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
    pub fn observe(
        &self,
        observer: u64,
        now: i128,
        targets: &[u64],
    ) -> Result<Vec<Observation>, EngineError> {
        if now < 0 || now > self.state.clock {
            return Err(EngineError::Invalid("uncommitted observation".into()));
        }
        let receiver = self.decode(observer)?.at(now);
        let mut result = Vec::new();
        for id in targets {
            if *id == observer {
                continue;
            }
            let b = self.decode(*id)?;
            if !geometry::causal_reachable(0, &b.at(0), now, &receiver) {
                continue;
            }
            let (mut lo, mut hi) = (0, now);
            while lo < hi {
                let mid = lo + (hi - lo) / 2 + 1;
                if geometry::causal_reachable(mid, &b.at(mid), now, &receiver) {
                    lo = mid
                } else {
                    hi = mid - 1
                }
            }
            let emission = b.at(lo);
            let mut blocked = self.state.bodies.values().any(|o| {
                o.id != observer && o.id != *id && self.occludes(o, &emission, lo, &receiver, now)
            });
            if !blocked && lo < now {
                let ray = Inertial {
                    epoch: lo,
                    origin: emission.clone(),
                    velocity: (receiver.clone() - emission.clone()) * (r(1) / r(now - lo)),
                };
                blocked = self.family_occludes(
                    &ray,
                    TickInterval {
                        start: lo + 1,
                        end: now,
                    },
                    [observer, *id],
                )?;
            }
            if !blocked {
                result.push(Observation {
                    entity: *id,
                    emission_tick: lo,
                    reception_tick: now,
                    position: emission,
                });
            }
        }
        Ok(result)
    }
    fn family_occludes(
        &self,
        ray: &Inertial,
        domain: TickInterval,
        excluded: [u64; 2],
    ) -> Result<bool, EngineError> {
        let mut used = 0;
        for f in &self.state.families {
            let mut ranges = vec![(f.first_id, f.first_id + (f.count - 1))];
            while let Some((lo, hi)) = ranges.pop() {
                if used >= self.max_pending_jobs {
                    return Err(EngineError::ResourceLimit(
                        "sensor family refinement budget exhausted".into(),
                    ));
                }
                used += 1;
                let mut points = Vec::with_capacity(4);
                for id in [lo, hi] {
                    let member = f.member(id).unwrap();
                    for t in [domain.start - 1, domain.end] {
                        points.push(member.state_at(t) - ray.state_at(t));
                    }
                }
                if points.iter().all(|p| p.x > f.radius)
                    || points.iter().all(|p| p.x < -&f.radius)
                    || points.iter().all(|p| p.y > f.radius)
                    || points.iter().all(|p| p.y < -&f.radius)
                {
                    continue;
                }
                if lo == hi {
                    if !excluded.contains(&lo)
                        && !self.state.bodies.contains_key(&lo)
                        && geometry::first_contact(ray, &f.member(lo).unwrap(), &f.radius, domain)
                            .is_some()
                    {
                        return Ok(true);
                    }
                } else {
                    let mid = lo + (hi - lo) / 2;
                    ranges.push((mid + 1, hi));
                    ranges.push((lo, mid));
                }
            }
        }
        Ok(false)
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
