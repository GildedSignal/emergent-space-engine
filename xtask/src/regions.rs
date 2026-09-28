//! Regions mode (docs/engine.md): the allocator (crates/allocator) over
//! hybrid regions on the M1's 4 performance and 4 efficiency cores. Independent islands (a
//! galaxy's fleets) run as separate regions in parallel, each in event or Metal mode by
//! measured cost; results are bit-identical to one stepper over the scene. One ladder advance
//! is one certified batch to the target, so the ladder's unit timings do not apply: the row
//! reports the allocator's own worker units instead (the frame thread never waits on them).
use crate::hybrid::Hybrid;
use emergent_allocator::{Allocator, Config, Report};
use emergent_lattice::{Log, Metrics, Stepper, Tick, World};
use std::sync::Arc;

pub struct Regions {
    a: Allocator<Hybrid>,
    tick: Tick,
    log: Log,
    metrics: Metrics,
    pub report: Option<Report>,
}

impl Regions {
    pub fn new(w: World, keep: bool) -> Result<Self, String> {
        let tick = w.tick;
        let cfg = Config { p_workers: 4, e_workers: 4, ..Config::default() };
        let a = Allocator::new(vec![w], Arc::new(move |w| Hybrid::new(w, keep).expect("a valid region world")), cfg)?;
        Ok(Regions { a, tick, log: Log::new(keep), metrics: Metrics::default(), report: None })
    }
}

impl Stepper for Regions {
    fn tick(&self) -> Tick {
        self.tick
    }

    fn advance(&mut self, target: Tick, _budget: u64) -> Tick {
        let r = self.a.run_to(target);
        self.tick = target;
        self.log = self.a.log();
        self.report = Some(r);
        target
    }

    fn world(&self) -> World {
        self.a.world()
    }

    fn log(&self) -> &Log {
        &self.log
    }

    fn metrics(&self) -> &Metrics {
        &self.metrics
    }
}
