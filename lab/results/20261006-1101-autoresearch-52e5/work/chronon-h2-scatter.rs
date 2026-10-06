//! CPU chronon mode: every chronon, bin bodies into a grid, test neighbour pairs with the
//! exact bin predicate, advance, find walls, resolve the batch. O(n) per chronon. It is the
//! reference every other mode must reproduce bit for bit, and itself checked against the
//! independent integer reference in `xtask/src/gas.rs`.
use crate::law::{self, Body, Consumed, Response, Tick, World};
use crate::{Event, Kickable, Kind, Log, Metrics, Motion, Stepper};
use std::collections::HashMap;
use std::hash::BuildHasherDefault;

/// Multiply-xor hasher for the chronon's small integer keys. Hash iteration order never
/// reaches an output: `pairs` is re-sorted canonically before use, and `consumed` is only
/// probed and filtered, so any exact hasher preserves digests.
#[derive(Default)]
struct FastKey(u64);

impl FastKey {
    #[inline] fn mix(&mut self, v: u64) { self.0 = (self.0 ^ v).wrapping_mul(0x9E37_79B9_7F4A_7C15).rotate_left(17); }
}

impl std::hash::Hasher for FastKey {
    #[inline] fn finish(&self) -> u64 {
        let mut z = self.0;
        z ^= z >> 33; z = z.wrapping_mul(0xff51_afd7_ed55_8ccd);
        z ^= z >> 33; z = z.wrapping_mul(0xc4ce_b9fe_1a85_ec53);
        z ^ (z >> 33)
    }
    fn write(&mut self, bytes: &[u8]) { for &b in bytes { self.mix(b as u64) } }
    #[inline] fn write_u8(&mut self, v: u8) { self.mix(v as u64) }
    #[inline] fn write_u16(&mut self, v: u16) { self.mix(v as u64) }
    #[inline] fn write_u32(&mut self, v: u32) { self.mix(v as u64) }
    #[inline] fn write_u64(&mut self, v: u64) { self.mix(v) }
    #[inline] fn write_usize(&mut self, v: usize) { self.mix(v as u64) }
    #[inline] fn write_u128(&mut self, v: u128) { self.mix(v as u64); self.mix((v >> 64) as u64) }
    #[inline] fn write_i8(&mut self, v: i8) { self.mix(v as u8 as u64) }
    #[inline] fn write_i16(&mut self, v: i16) { self.mix(v as u16 as u64) }
    #[inline] fn write_i32(&mut self, v: i32) { self.mix(v as u32 as u64) }
    #[inline] fn write_i64(&mut self, v: i64) { self.mix(v as u64) }
    #[inline] fn write_isize(&mut self, v: isize) { self.mix(v as usize as u64) }
    #[inline] fn write_i128(&mut self, v: i128) { self.write_u128(v as u128) }
}

type FastMap<K, V> = HashMap<K, V, BuildHasherDefault<FastKey>>;

pub struct Chronon {
    w: World,
    /// (index a, index b), a < b → revisions at which the contact was consumed.
    consumed: FastMap<(u32, u32), (u32, u32)>,
    log: Log,
    metrics: Metrics,
    reach_max: i64,
    /// Open-addressed cell table, reused across chronons and epoch-invalidated (never
    /// cleared slot by slot). `slot_keys[slot]` is the cell, `slot_a[slot]` ends as the
    /// exclusive end of the cell's range in `order` (it is the fill cursor during the
    /// scatter), `slot_cnt[slot]` the body count, `slot_gen[slot]` the owning epoch.
    slot_key: Vec<(i64, i64)>,
    slot_a: Vec<u32>,
    slot_cnt: Vec<u32>,
    slot_gen: Vec<u32>,
    /// Per-body slot (computed once per chronon, reused by the scatter).
    bslot: Vec<u32>,
    /// Body indices grouped by cell.
    order: Vec<u32>,
    gen: u32,
    mask: usize,
}

impl Chronon {
    pub fn new(world: World, keep_events: bool) -> Result<Self, law::LawError> {
        world.validate()?;
        let mut consumed = FastMap::default();
        for c in &world.consumed {
            let (Some(i), Some(j)) = (world.index_of(c.a), world.index_of(c.b)) else {
                return Err(law::LawError(format!("consumed pair ({}, {}) names a missing body", c.a, c.b)));
            };
            consumed.insert((i as u32, j as u32), (c.rev_a, c.rev_b));
        }
        let n = world.bodies.len();
        let tsize = (2 * n).next_power_of_two().max(8).min(1 << 31);
        let reach_max = 2 * world.max_radius();
        Ok(Chronon {
            w: world,
            consumed,
            log: Log::new(keep_events),
            metrics: Metrics::default(),
            reach_max,
            slot_key: vec![(0, 0); tsize],
            slot_a: vec![0; tsize],
            slot_cnt: vec![0; tsize],
            slot_gen: vec![0; tsize],
            bslot: vec![0; n],
            order: Vec::with_capacity(n),
            gen: 0,
            mask: tsize - 1,
        })
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

        // 1. Detect with positions at t-1: bin bodies into the cell table (open addressing,
        //    epoch-invalidated), then test neighbour pairs with the exact bin predicate.
        //    The tested pair set, the i < j filter and `hit` are exactly the sorted-grid
        //    rule's; only the machinery that finds cells changed (pairs are re-sorted
        //    canonically below, so the digest cannot see the visit order).
        self.gen += 1;
        if self.gen == 0 {
            self.slot_gen.fill(0);
            self.gen = 1;
        }
        let gen = self.gen;
        let mask = self.mask;
        let (slot_key, slot_a, slot_cnt, slot_gen, bslot) =
            (&mut self.slot_key, &mut self.slot_a, &mut self.slot_cnt, &mut self.slot_gen, &mut self.bslot);
        #[inline]
        fn find_slot(gen: u32, mask: usize, slot_key: &[(i64, i64)], slot_gen: &[u32], key: (i64, i64)) -> usize {
            let mut h = (key.0 as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)
                ^ (key.1 as u64).wrapping_mul(0xC2B2_AE3D_27D4_EB4F);
            h ^= h >> 29;
            h = h.wrapping_mul(0x16566_7919_E377_9F9);
            h ^= h >> 32;
            let mut s = h as usize & mask;
            loop {
                if slot_gen[s] != gen || slot_key[s] == key {
                    return s;
                }
                s = (s + 1) & mask;
            }
        }
        for (i, b) in bodies.iter().enumerate() {
            let key = (b.x[0].div_euclid(cell), b.x[1].div_euclid(cell));
            let s = find_slot(gen, mask, slot_key, slot_gen, key);
            if slot_gen[s] != gen {
                slot_gen[s] = gen;
                slot_key[s] = key;
                slot_cnt[s] = 0;
            }
            slot_cnt[s] += 1;
            bslot[i] = s as u32;
        }
        let mut running = 0u32;
        for s in 0..=mask {
            if slot_gen[s] == gen {
                slot_a[s] = running;
                running += slot_cnt[s];
            }
        }
        self.order.clear();
        self.order.resize(n, 0);
        for (i, &s) in bslot.iter().enumerate() {
            let s = s as usize;
            let p = slot_a[s] as usize;
            self.order[p] = i as u32;
            slot_a[s] += 1;
        }
        let mut pairs: Vec<(usize, usize)> = Vec::new();
        let mut predicates = 0u64;
        for s in 0..=mask {
            if slot_gen[s] != gen {
                continue;
            }
            let (cx, cy) = slot_key[s];
            let e0 = slot_a[s] as usize;
            let s0 = (e0 - slot_cnt[s] as usize) as usize;
            for dx in -1i64..=1 {
                for dy in -1i64..=1 {
                    let nk = (cx + dx, cy + dy);
                    let ns = find_slot(gen, mask, slot_key, slot_gen, nk);
                    if slot_gen[ns] != gen {
                        continue;
                    }
                    let e1 = slot_a[ns] as usize;
                    let s1 = (e1 - slot_cnt[ns] as usize) as usize;
                    for &i in &self.order[s0..e0] {
                        for &j in &self.order[s1..e1] {
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
            let local: FastMap<usize, usize> = involved.iter().enumerate().map(|(l, &g)| (g, l)).collect();
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
