//! I2 composition scheduler: unequal certified cuts and arriving influence.
//! Conservative finite-horizon dependency frontier. Not gravitational authority.

use crate::{
    geometry::{Aabb, TickInterval},
    runtime::{Engine, EngineError},
};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct IncomingInfluence {
    pub id: String,
    pub source_region: String,
    pub emission_tick: i128,
    pub earliest_arrival: i128,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Region {
    pub name: String,
    pub lo: u64,
    pub hi: u64,
    pub certified_through: i128,
    pub incoming: Vec<IncomingInfluence>,
    /// Spatial overlap with another live region forbids permanent independence.
    pub independent: bool,
}

#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq)]
pub struct CompositionScheduler {
    pub regions: Vec<Region>,
    pub lost_lookahead: Vec<String>,
    pub cyclic_wait: bool,
    pub starved: Vec<String>,
}

impl CompositionScheduler {
    pub fn region_mut(&mut self, name: &str) -> Option<&mut Region> {
        self.regions.iter_mut().find(|r| r.name == name)
    }

    pub fn region(&self, name: &str) -> Option<&Region> {
        self.regions.iter().find(|r| r.name == name)
    }

    pub fn global_cut(&self) -> Option<i128> {
        if self.regions.is_empty()
            || self.regions.iter().any(|r| !r.incoming.is_empty())
            || self.cyclic_wait
            || !self.lost_lookahead.is_empty()
        {
            return None;
        }
        let first = self.regions[0].certified_through;
        if self.regions.iter().all(|r| r.certified_through == first) {
            Some(first)
        } else {
            None
        }
    }

    fn detect_cycles_and_starvation(&mut self) {
        self.cyclic_wait = false;
        self.starved.clear();
        let mut waiting: BTreeMap<String, String> = BTreeMap::new();
        for r in &self.regions {
            if let Some(inf) = r.incoming.first() {
                waiting.insert(r.name.clone(), inf.source_region.clone());
            }
        }
        for (a, b) in &waiting {
            if waiting.get(b).is_some_and(|c| c == a) {
                self.cyclic_wait = true;
            }
        }
        let max = self
            .regions
            .iter()
            .map(|r| r.certified_through)
            .max()
            .unwrap_or(0);
        for r in &self.regions {
            if r.certified_through < max && !r.incoming.is_empty() {
                self.starved.push(r.name.clone());
            }
        }
    }
}

impl Engine {
    pub fn register_region(&mut self, name: &str, lo: u64, hi: u64) -> Result<(), EngineError> {
        if lo > hi {
            return Err(EngineError::Invalid("region range".into()));
        }
        self.scheduler.regions.retain(|r| r.name != name);
        self.scheduler.regions.push(Region {
            name: name.into(),
            lo,
            hi,
            certified_through: 0,
            incoming: Vec::new(),
            independent: true,
        });
        self.refresh_region_overlap()?;
        Ok(())
    }

    pub fn refresh_region_overlap(&mut self) -> Result<(), EngineError> {
        let clock = self.state.clock;
        let horizon = clock.max(1);
        let domain = TickInterval::new(0, horizon)?;
        let boxes: Vec<(String, Aabb)> = self
            .scheduler
            .regions
            .iter()
            .map(|r| {
                let mut pts = Vec::new();
                for id in [r.lo, r.hi] {
                    if let Ok(b) = self.decode(id) {
                        pts.push(b.at(domain.start));
                        pts.push(b.at(domain.end));
                    }
                }
                let aabb = if pts.len() >= 2 {
                    Aabb::from_points(&pts[0], &pts[1])
                } else {
                    Aabb::from_points(&crate::math::Vec2::zero(), &crate::math::Vec2::zero())
                };
                (r.name.clone(), aabb)
            })
            .collect();
        for i in 0..self.scheduler.regions.len() {
            let mut independent = true;
            for j in 0..boxes.len() {
                if i == j {
                    continue;
                }
                if boxes[i].1.intersects(&boxes[j].1) {
                    independent = false;
                }
            }
            self.scheduler.regions[i].independent = independent;
        }
        Ok(())
    }

    /// Certify a region through `through` if dependencies are already resolved.
    pub fn certify_region(&mut self, name: &str, through: i128) -> Result<i128, EngineError> {
        if through < 0 || through > self.state.clock {
            return Err(EngineError::Invalid("region cut is not committed".into()));
        }
        self.refresh_region_overlap()?;
        let Some(idx) = self.scheduler.regions.iter().position(|r| r.name == name) else {
            return Err(EngineError::Invalid("unknown region".into()));
        };
        let incoming = self.scheduler.regions[idx].incoming.clone();
        for inf in &incoming {
            if inf.earliest_arrival <= through {
                let source_cut = self
                    .scheduler
                    .region(&inf.source_region)
                    .map(|s| s.certified_through)
                    .unwrap_or(0);
                if inf.emission_tick > source_cut {
                    self.scheduler
                        .lost_lookahead
                        .push(format!("{}:{through}", inf.id));
                    return Err(EngineError::Invalid(
                        "lost lookahead: source region is behind the emission".into(),
                    ));
                }
                return Err(EngineError::Invalid(
                    "arriving influence requires reconcile before this cut".into(),
                ));
            }
        }
        self.scheduler.regions[idx].certified_through = through;
        self.scheduler.detect_cycles_and_starvation();
        Ok(through)
    }

    pub fn note_arriving_influence(
        &mut self,
        dest: &str,
        influence: IncomingInfluence,
    ) -> Result<(), EngineError> {
        let Some(region) = self.scheduler.region_mut(dest) else {
            return Err(EngineError::Invalid("unknown region".into()));
        };
        region.incoming.push(influence);
        self.scheduler.detect_cycles_and_starvation();
        Ok(())
    }

    /// Apply a recorded reception and raise the destination cut.
    pub fn reconcile_region(
        &mut self,
        dest: &str,
        influence_id: &str,
        through: i128,
    ) -> Result<i128, EngineError> {
        {
            let Some(region) = self.scheduler.region_mut(dest) else {
                return Err(EngineError::Invalid("unknown region".into()));
            };
            region
                .incoming
                .retain(|i| i.id != influence_id);
        }
        self.scheduler
            .lost_lookahead
            .retain(|s| !s.starts_with(influence_id));
        self.certify_region(dest, through)
    }

    /// Advance only this region's identities from its certified cut to `target`.
    /// Spatial overlap with a lagging region, or an influence whose source is
    /// uncertified, refuses independent advance (joint solve / lost lookahead).
    pub fn advance_region(
        &mut self,
        name: &str,
        target: i128,
        budget: crate::runtime::WorkBudget,
    ) -> Result<crate::runtime::AdvanceResult, EngineError> {
        let Some(idx) = self.scheduler.regions.iter().position(|r| r.name == name) else {
            return Err(EngineError::Invalid("unknown region".into()));
        };
        let lo = self.scheduler.regions[idx].lo;
        let hi = self.scheduler.regions[idx].hi;
        let from = self.scheduler.regions[idx].certified_through;
        if target < from {
            return Err(EngineError::Invalid(
                "cannot advance a region behind its certified cut".into(),
            ));
        }
        let incoming = self.scheduler.regions[idx].incoming.clone();
        for inf in &incoming {
            if inf.earliest_arrival <= target {
                let source_cut = self
                    .scheduler
                    .region(&inf.source_region)
                    .map(|s| s.certified_through)
                    .unwrap_or(0);
                if inf.emission_tick > source_cut {
                    self.scheduler
                        .lost_lookahead
                        .push(format!("{}:{target}", inf.id));
                    return Err(EngineError::Invalid(
                        "lost lookahead: source region is behind the emission".into(),
                    ));
                }
            }
        }
        if self.region_advance_overlaps_lagging(idx, from, target)? {
            return Err(EngineError::Invalid(
                "spatial overlap with a lagging region requires a joint solve".into(),
            ));
        }
        let saved_clock = self.state.clock;
        self.clear_pending_scan();
        self.scan_filter = Some((lo, hi));
        self.state.clock = from;
        let ops = budget.operations.max(1);
        let result = loop {
            let step = self.advance(target, crate::runtime::WorkBudget::new(ops))?;
            if step.complete {
                break step;
            }
        };
        self.scan_filter = None;
        self.clear_pending_scan();
        self.scheduler.regions[idx].certified_through = target;
        self.state.clock = saved_clock.max(target);
        self.scheduler.detect_cycles_and_starvation();
        Ok(result)
    }

    pub fn advance_joint(
        &mut self,
        a: &str,
        b: &str,
        target: i128,
        budget: crate::runtime::WorkBudget,
    ) -> Result<crate::runtime::AdvanceResult, EngineError> {
        let from = {
            let ra = self
                .scheduler
                .region(a)
                .ok_or_else(|| EngineError::Invalid("unknown region".into()))?;
            let rb = self
                .scheduler
                .region(b)
                .ok_or_else(|| EngineError::Invalid("unknown region".into()))?;
            ra.certified_through.min(rb.certified_through)
        };
        if target < from {
            return Err(EngineError::Invalid(
                "cannot jointly advance behind the lagging certified cut".into(),
            ));
        }
        let saved_clock = self.state.clock;
        self.clear_pending_scan();
        self.scan_filter = None;
        self.state.clock = from;
        let ops = budget.operations.max(1);
        let result = loop {
            let step = self.advance(target, crate::runtime::WorkBudget::new(ops))?;
            if step.complete {
                break step;
            }
        };
        for name in [a, b] {
            if let Some(r) = self.scheduler.region_mut(name) {
                r.certified_through = r.certified_through.max(target);
            }
        }
        self.state.clock = saved_clock.max(target);
        self.scheduler.detect_cycles_and_starvation();
        Ok(result)
    }

    fn region_advance_overlaps_lagging(
        &self,
        idx: usize,
        from: i128,
        target: i128,
    ) -> Result<bool, EngineError> {
        let lo = self.scheduler.regions[idx].lo;
        let hi = self.scheduler.regions[idx].hi;
        let mine = self.region_window_aabb(lo, hi, from, target)?;
        for (j, other) in self.scheduler.regions.iter().enumerate() {
            if j == idx {
                continue;
            }
            if other.certified_through >= target {
                continue;
            }
            let theirs = self.region_window_aabb(
                other.lo,
                other.hi,
                other.certified_through,
                target,
            )?;
            if mine.intersects(&theirs) {
                return Ok(true);
            }
        }
        Ok(false)
    }

    fn region_window_aabb(
        &self,
        lo: u64,
        hi: u64,
        t0: i128,
        t1: i128,
    ) -> Result<Aabb, EngineError> {
        let mut pts = Vec::new();
        let mut rad = crate::math::r(0);
        for id in [lo, hi] {
            let body = self.decode(id)?;
            pts.push(body.at(t0));
            pts.push(body.at(t1));
            if body.radius > rad {
                rad = body.radius.clone();
            }
        }
        for (_, body) in self.state.bodies.range(lo..=hi) {
            pts.push(body.at(t0));
            pts.push(body.at(t1));
            if body.radius > rad {
                rad = body.radius.clone();
            }
        }
        let mut aabb = Aabb::from_points(&pts[0], pts.get(1).unwrap_or(&pts[0]));
        for p in &pts[1..] {
            aabb.min.x = aabb.min.x.clone().min(p.x.clone());
            aabb.min.y = aabb.min.y.clone().min(p.y.clone());
            aabb.max.x = aabb.max.x.clone().max(p.x.clone());
            aabb.max.y = aabb.max.y.clone().max(p.y.clone());
        }
        aabb.min.x -= rad.clone();
        aabb.min.y -= rad.clone();
        aabb.max.x += rad.clone();
        aabb.max.y += rad;
        Ok(aabb)
    }

    pub fn joint_solve_required(&self, a: &str, b: &str) -> bool {
        let Some(ra) = self.scheduler.region(a) else {
            return false;
        };
        let Some(rb) = self.scheduler.region(b) else {
            return false;
        };
        !ra.independent || !rb.independent || self.scheduler.cyclic_wait
    }
}
