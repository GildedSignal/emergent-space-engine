//! The one-branch fix in the shipped law's own shape: `resolve_law` copied verbatim from
//! crates/lattice/src/relativity.rs (v1 path), with the receding gate's `continue`
//! replaced by the root test. When the fix is off, or the τ-window does not fire, the
//! code path is byte-identical to shipped (the digest control proves it). The stepper is
//! `Chronon::step` copied verbatim with `law::respond` swapped for ours.
use crate::root::{exact_candidates, Root};
use emergent_lattice::law::{dot, sub, Body, Container, Law, Response, World};
use emergent_lattice::relativity::{candidates, momentum, targets};
use emergent_lattice::{Event, Kind, Log, Metrics};
use std::collections::HashMap;

fn add3(a: [i128; 3], b: [i128; 3]) -> [i128; 3] {
    [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
}

/// The τ-window + root firing decision for one receding pair, from the bin-END integers
/// the resolver already holds (d_end = d0 + w). Pure integer arithmetic.
pub fn fires_root(d_end: [i128; 2], w: [i128; 2], reach: i128) -> bool {
    let d0 = [d_end[0] - w[0], d_end[1] - w[1]];
    Root::new(d0, w, reach).fires()
}

thread_local! {
    pub static ROOT_FIRED: std::cell::Cell<usize> = const { std::cell::Cell::new(0) };
}

/// resolve_law with the root branch. `fix` off ⇒ identical bits to shipped.
#[allow(clippy::too_many_arguments)]
pub fn resolve_fixed(
    law: Law,
    q: i64,
    bodies: &mut [Body],
    pairs: &[(usize, usize)],
    walls: &[bool],
    container: Option<&Container>,
    wall_momentum: &mut [i64; 2],
    fix: bool,
) {
    debug_assert!(law.subluminal());
    let four_momentum = |m: i64, k: [i64; 2], q: i64| momentum(law, m, k, q);
    let mut fired = 0usize;
    let before: Vec<[i64; 2]> = bodies.iter().map(|b| b.k).collect();
    let mut k = before.clone();
    let mut owe: Vec<[i128; 3]> = bodies.iter().map(|b| [b.residual as i128, b.carry[0] as i128, b.carry[1] as i128]).collect();
    let mut touched = vec![false; bodies.len()];
    for &(a, b) in pairs {
        if bodies[a].response != Response::Bounce || bodies[b].response != Response::Bounce {
            continue;
        }
        let d = sub(bodies[b].x, bodies[a].x);
        let w = sub(k[b], k[a]);
        let receding = dot(d, w) >= 0;
        let mut root: Option<Root> = None;
        if receding {
            if !fix || dot(d, d) == 0 {
                continue;
            }
            let reach = (bodies[a].radius + bodies[b].radius) as i128;
            let d0 = [d[0] - w[0], d[1] - w[1]];
            let rt = Root::new(d0, w, reach);
            if !rt.fires() {
                continue; // miss / consumed past root / future root / already-inside: shipped skip
            }
            fired += 1;
            root = Some(rt);
        }
        let (ma, mb) = (bodies[a].mass, bodies[b].mass);
        let (pa, pb) = (four_momentum(ma, k[a], q), four_momentum(mb, k[b], q));
        // Normal contacts: the shipped targets verbatim. Root contacts: exact Q(√D).
        let cands: Option<(Vec<[i64; 2]>, Vec<[i64; 2]>)> = match &root {
            None => targets(pa, pb, d, q).map(|(ta, tb)| (candidates(ta, q), candidates(tb, q))),
            Some(rt) => rt.exact_targets(pa, pb, q).map(|(ta, tb)| (exact_candidates(&ta, q), exact_candidates(&tb, q))),
        };
        let Some((fa_c, fb_c)) = cands else { continue };
        touched[a] = true;
        let fa: Vec<([i64; 2], [i128; 3])> = fa_c.into_iter().map(|c| (c, four_momentum(ma, c, q))).collect();
        let fb: Vec<([i64; 2], [i128; 3])> = fb_c.into_iter().map(|c| (c, four_momentum(mb, c, q))).collect();
        let old = add3(pa, pb);
        let owed = add3(owe[a], owe[b]);
        let unchanged_allowed = fa.len() * fb.len() == 1;
        let mut best: Option<(i128, [i64; 2], [i64; 2], [i128; 3])> = None;
        for (ca, ea) in &fa {
            for (cb, eb) in &fb {
                if !unchanged_allowed && *ca == k[a] && *cb == k[b] {
                    continue;
                }
                let e = [ea[0] + eb[0] - old[0], ea[1] + eb[1] - old[1], ea[2] + eb[2] - old[2]];
                let r = add3(owed, e);
                let score = r[0] * r[0] + r[1] * r[1] + r[2] * r[2];
                if best.as_ref().is_none_or(|(s, ..)| score < *s) {
                    best = Some((score, *ca, *cb, e));
                }
            }
        }
        let Some((_, ca, cb, e)) = best else { continue };
        owe[a] = add3(owe[a], e);
        k[a] = ca;
        k[b] = cb;
    }
    for &(a, b) in pairs {
        for i in [a, b] {
            if bodies[i].response == Response::Stop {
                k[i] = [0, 0];
            }
        }
    }
    if let Some(c) = container {
        for (i, body) in bodies.iter().enumerate() {
            if !walls[i] {
                continue;
            }
            let (lo, hi) = c.inset(body.radius);
            for ax in 0..2 {
                if (body.x[ax] <= lo[ax] && k[i][ax] < 0) || (body.x[ax] >= hi[ax] && k[i][ax] > 0) {
                    let dp = i64::try_from(2 * four_momentum(body.mass, k[i], q)[1 + ax]).expect("wall exchange fits i64");
                    wall_momentum[ax] = wall_momentum[ax].checked_add(dp).expect("wall ledger fits i64");
                    k[i][ax] = -k[i][ax];
                }
            }
        }
    }
    for (i, body) in bodies.iter_mut().enumerate() {
        if touched[i] {
            body.residual = i64::try_from(owe[i][0]).expect("energy carry fits i64");
            body.carry = [i64::try_from(owe[i][1]).expect("momentum carry fits i64"), i64::try_from(owe[i][2]).expect("momentum carry fits i64")];
        }
        if k[i] != before[i] {
            body.k = k[i];
            body.rev += 1;
        }
    }
    ROOT_FIRED.with(|c| c.set(c.get() + fired));
}

/// Chronon::step copied verbatim (detection, advance, walls, respond, consumed
/// bookkeeping, event log), with `law::respond` swapped for `resolve_fixed`.
pub struct FixedStepper {
    pub w: World,
    consumed: HashMap<(u32, u32), (u32, u32)>,
    log: Log,
    metrics: Metrics,
    reach_max: i64,
    pub fix: bool,
}

impl FixedStepper {
    pub fn new(world: World, keep_events: bool, fix: bool) -> Result<Self, emergent_lattice::law::LawError> {
        world.validate()?;
        let mut consumed = HashMap::new();
        for c in &world.consumed {
            let (Some(i), Some(j)) = (world.index_of(c.a), world.index_of(c.b)) else {
                return Err(emergent_lattice::law::LawError(format!("consumed pair ({}, {}) names a missing body", c.a, c.b)));
            };
            consumed.insert((i as u32, j as u32), (c.rev_a, c.rev_b));
        }
        let reach_max = 2 * world.max_radius();
        Ok(FixedStepper { w: world, consumed, log: Log::new(keep_events), metrics: Metrics::default(), reach_max, fix })
    }

    pub fn step(&mut self) {
        let t = self.w.tick + 1;
        let bodies = &self.w.bodies;
        let n = bodies.len();
        let mut ops = n as u64;

        // 1. Detect with positions at t-1 (shipped predicate, shipped code).
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
                            if emergent_lattice::law::hit(sub(b.x, a.x), sub(b.k, a.k), (a.radius + b.radius) as i128) {
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
                    if emergent_lattice::law::at_wall(b.x, b.k, lo, hi) {
                        walls.push(i);
                    }
                }
            }
        }
        ops += n as u64 + predicates;
        self.metrics.predicates += predicates;

        // 4. Respond (ours; identical bits to shipped when the fix never fires).
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
            resolve_fixed(self.w.law, self.w.q, &mut batch, &lp, &lw, self.w.container.as_ref(), &mut self.w.wall_momentum, self.fix);
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

        if t % 64 == 0 && !self.consumed.is_empty() {
            let bodies = &self.w.bodies;
            self.consumed.retain(|&(i, j), &mut (ra, rb)| {
                let (a, b) = (&bodies[i as usize], &bodies[j as usize]);
                a.rev == ra && b.rev == rb && dot(sub(b.x, a.x), sub(b.k, a.k)) < 0
            });
        }
    }

    pub fn log(&self) -> &Log {
        &self.log
    }
}
