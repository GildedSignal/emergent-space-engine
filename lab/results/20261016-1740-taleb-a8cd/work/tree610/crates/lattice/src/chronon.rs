//! CPU chronon mode: every chronon, bin bodies into a grid, test neighbour pairs with the
//! exact bin predicate, advance, find walls, resolve the batch. O(n) per chronon. It is the
//! reference every other mode must reproduce bit for bit, and itself checked against the
//! independent integer reference in `xtask/src/gas.rs`.
use crate::law::{self, Body, Consumed, Response, Tick, World};
use crate::{Event, Kickable, Kind, Log, Metrics, Motion, Stepper};
use std::collections::HashMap;

pub struct Chronon {
    w: World,
    /// (index a, index b), a < b → revisions at which the contact was consumed.
    consumed: HashMap<(u32, u32), (u32, u32)>,
    log: Log,
    metrics: Metrics,
    reach_max: i64,
}

impl Chronon {
    pub fn new(world: World, keep_events: bool) -> Result<Self, law::LawError> {
        world.validate()?;
        let mut consumed = HashMap::new();
        for c in &world.consumed {
            let (Some(i), Some(j)) = (world.index_of(c.a), world.index_of(c.b)) else {
                return Err(law::LawError(format!("consumed pair ({}, {}) names a missing body", c.a, c.b)));
            };
            consumed.insert((i as u32, j as u32), (c.rev_a, c.rev_b));
        }
        let reach_max = 2 * world.max_radius();
        Ok(Chronon { w: world, consumed, log: Log::new(keep_events), metrics: Metrics::default(), reach_max })
    }

    /// One chronon: (tick, tick + 1].
    pub fn step(&mut self) {
        let t = self.w.tick + 1;
        let bodies = &self.w.bodies;
        let n = bodies.len();
        let mut ops = n as u64;

        // 1. Detect with positions at t-1.
        let kmax = bodies.iter().map(|b| b.k[0].abs().max(b.k[1].abs())).max().unwrap_or(0);
        let cell = (self.reach_max + 2 * kmax).max(1);
        let key = |b: &Body| (b.x[0].div_euclid(cell), b.x[1].div_euclid(cell));
        let mut order: Vec<((i64, i64), u32)> = bodies.iter().enumerate().map(|(i, b)| (key(b), i as u32)).collect();
        order.sort_unstable();
        let mut ranges: HashMap<(i64, i64), (usize, usize)> = HashMap::with_capacity(n);
        let mut s = 0;
        while s < order.len() {
            let mut e = s + 1;
            while e < order.len() && order[e].0 == order[s].0 {
                e += 1;
            }
            ranges.insert(order[s].0, (s, e));
            s = e;
        }
        let mut pairs: Vec<(usize, usize)> = Vec::new();
        let mut predicates = 0u64;
        for (&(cx, cy), &(s0, e0)) in &ranges {
            for dx in -1..=1 {
                for dy in -1..=1 {
                    let Some(&(s1, e1)) = ranges.get(&(cx + dx, cy + dy)) else { continue };
                    for &(_, i) in &order[s0..e0] {
                        for &(_, j) in &order[s1..e1] {
                            if i >= j {
                                continue;
                            }
                            let (a, b) = (&bodies[i as usize], &bodies[j as usize]);
                            if self.consumed.get(&(i, j)) == Some(&(a.rev, b.rev)) {
                                continue;
                            }
                            predicates += 1;
                            if law::hit(law::sub(b.x, a.x), law::sub(b.k, a.k), (a.radius + b.radius) as i128) {
                                pairs.push((i as usize, j as usize));
                            }
                        }
                    }
                }
            }
        }
        pairs.sort_unstable();

        // 2. Advance.
        for b in self.w.bodies.iter_mut() {
            b.x = [b.x[0] + b.k[0], b.x[1] + b.k[1]];
        }

        // 3. Walls.
        let mut walls: Vec<usize> = Vec::new();
        if let Some(c) = &self.w.container {
            for (i, b) in self.w.bodies.iter().enumerate() {
                if b.response == Response::Bounce {
                    predicates += 1;
                    let (lo, hi) = c.inset(b.radius);
                    if law::at_wall(b.x, b.k, lo, hi) {
                        walls.push(i);
                    }
                }
            }
        }
        ops += n as u64 + predicates;
        self.metrics.predicates += predicates;

        // 4. Respond.
        if !pairs.is_empty() || !walls.is_empty() {
            let mut involved: Vec<usize> = pairs.iter().flat_map(|&(a, b)| [a, b]).chain(walls.iter().copied()).collect();
            involved.sort_unstable();
            involved.dedup();
            let local: HashMap<usize, usize> = involved.iter().enumerate().map(|(l, &g)| (g, l)).collect();
            let mut batch: Vec<Body> = involved.iter().map(|&g| self.w.bodies[g].clone()).collect();
            let lp: Vec<(usize, usize)> = pairs.iter().map(|&(a, b)| (local[&a], local[&b])).collect();
            let mut lw = vec![false; batch.len()];
            for &g in &walls {
                lw[local[&g]] = true;
            }
            law::respond(self.w.law, self.w.q, &mut batch, &lp, &lw, self.w.container.as_ref(), &mut self.w.wall_momentum);
            for (l, &g) in involved.iter().enumerate() {
                self.w.bodies[g] = batch[l].clone();
            }
            for &(a, b) in &pairs {
                let (ba, bb) = (&self.w.bodies[a], &self.w.bodies[b]);
                self.consumed.insert((a as u32, b as u32), (ba.rev, bb.rev));
                self.log.record(Event { tick: t, kind: Kind::Contact, a: ba.id, b: bb.id });
            }
            for &i in &walls {
                self.log.record(Event { tick: t, kind: Kind::Wall, a: self.w.bodies[i].id, b: 0 });
            }
            let size = (pairs.len() + walls.len()) as u64;
            self.metrics.batches += 1;
            self.metrics.max_batch = self.metrics.max_batch.max(size);
            self.metrics.fired += size;
            ops += involved.len() as u64 + pairs.len() as u64;
        }
        self.w.tick = t;
        self.metrics.ops += ops;

        // Keep the consumed map small: drop entries that can never matter again.
        if t % 64 == 0 && !self.consumed.is_empty() {
            let bodies = &self.w.bodies;
            self.consumed.retain(|&(i, j), &mut (ra, rb)| {
                let (a, b) = (&bodies[i as usize], &bodies[j as usize]);
                a.rev == ra && b.rev == rb && law::dot(law::sub(b.x, a.x), law::sub(b.k, a.k)) < 0
            });
        }
    }
}

impl Stepper for Chronon {
    fn tick(&self) -> Tick {
        self.w.tick
    }

    /// Whole chronons only: the overshoot bound is one chronon (about 2n + pairs ops).
    fn advance(&mut self, target: Tick, budget: u64) -> Tick {
        let start = self.metrics.ops;
        let mut did = false;
        while self.w.tick < target && (!did || self.metrics.ops - start < budget) {
            self.step();
            did = true;
        }
        if did {
            let spent = self.metrics.ops - start;
            self.metrics.units += 1;
            self.metrics.max_unit_ops = self.metrics.max_unit_ops.max(spent);
        }
        self.w.tick
    }

    fn world(&self) -> World {
        let mut w = self.w.clone();
        w.consumed = self
            .consumed
            .iter()
            .map(|(&(i, j), &(ra, rb))| Consumed { a: w.bodies[i as usize].id, b: w.bodies[j as usize].id, rev_a: ra, rev_b: rb })
            .collect();
        w.canonical()
    }

    fn log(&self) -> &Log {
        &self.log
    }

    fn metrics(&self) -> &Metrics {
        &self.metrics
    }
}

impl Kickable for Chronon {
    fn motions(&self, out: &mut Vec<Motion>) {
        out.clear();
        out.extend(self.w.bodies.iter().map(|b| Motion { x: b.x, k: b.k }));
    }

    /// Between chronons, so the next one sees the new velocities. Revised bodies invalidate
    /// their consumed contacts through `rev`; nothing else is indexed.
    fn kick(&mut self, dk: &[[i64; 2]]) -> Result<(), law::LawError> {
        if dk.len() != self.w.bodies.len() {
            return Err(law::LawError(format!("{} kicks for {} bodies", dk.len(), self.w.bodies.len())));
        }
        let mut next = Vec::with_capacity(dk.len());
        for (b, d) in self.w.bodies.iter().zip(dk) {
            next.push(crate::kicked(self.w.law, self.w.q, b.k, *d)?);
        }
        for ((b, d), k) in self.w.bodies.iter_mut().zip(dk).zip(next) {
            if *d != [0, 0] {
                b.k = k;
                b.rev += 1;
            }
        }
        Ok(())
    }

    fn masses(&self, out: &mut Vec<i64>) {
        out.clear();
        out.extend(self.w.bodies.iter().map(|b| b.mass));
    }

    /// Between chronons, like a kick; consumed contacts are keyed by revision, so a body whose
    /// velocity changed is live again.
    fn rebase(&mut self, dx: &[[i64; 2]], dk: &[[i64; 2]]) -> Result<(), law::LawError> {
        if dk.len() != self.w.bodies.len() || dx.len() != dk.len() {
            return Err(law::LawError(format!("{} shifts and {} kicks for {} bodies", dx.len(), dk.len(), self.w.bodies.len())));
        }
        crate::rebased_ok(self.w.law, self.w.q, self.w.container.is_some(), self.w.bodies.iter().map(|b| Motion { x: b.x, k: b.k }), dx, dk)?;
        let uniform = crate::uniform_shift(dx);
        for ((b, s), d) in self.w.bodies.iter_mut().zip(dx).zip(dk) {
            b.x = [b.x[0] + s[0], b.x[1] + s[1]];
            if *d != [0, 0] {
                b.k = [b.k[0] + d[0], b.k[1] + d[1]];
            }
            if crate::rebase_revises(uniform, *s, *d) {
                b.rev += 1;
            }
        }
        Ok(())
    }
}
