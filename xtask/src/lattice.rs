//! The lattice contract (crates/lattice) against the independent integer gas reference
//! (gas.rs, which shares no code with it): events, final states and the wall ledger must
//! be identical.
use crate::gas;
use emergent_lattice::{chronon::Chronon, worlds, Kind, Stepper};
use serde_json::{json, Value};

pub fn check_gas(n: u64, horizon: i64, seed: u64) -> Value {
    let g = gas::world(n, 0.1, 1024, 256, seed);
    let w = worlds::gas(n, 0.1, 1024, 256, seed);
    let same_genesis = g.bodies.len() == w.bodies.len()
        && g.bodies.iter().zip(&w.bodies).all(|((p, v), b)| {
            [p[0] as i64 * 1024, p[1] as i64 * 1024] == b.x && [v[0] as i64, v[1] as i64] == b.k
        });
    let t = std::time::Instant::now();
    let reference = gas::reference(&g, horizon as i128);
    let reference_ms = t.elapsed().as_secs_f64() * 1e3;
    let t = std::time::Instant::now();
    let mut c = Chronon::new(w, true).expect("gas world");
    c.run_to(horizon);
    let chronon_ms = t.elapsed().as_secs_f64() * 1e3;
    let events: Vec<(i128, String, Vec<u64>)> = c
        .log()
        .sorted()
        .into_iter()
        .map(|e| match e.kind {
            Kind::Contact => (e.tick as i128, "contact".to_string(), vec![e.a, e.b]),
            Kind::Wall => (e.tick as i128, "wall".to_string(), vec![e.a]),
        })
        .collect();
    let world = c.world();
    let finals: Vec<([i128; 2], [i128; 2], i128, u64)> = world
        .bodies
        .iter()
        .map(|b| ([b.x[0] as i128, b.x[1] as i128], [b.k[0] as i128, b.k[1] as i128], b.residual as i128, b.rev as u64))
        .collect();
    let wm = [world.wall_momentum[0] as i128, world.wall_momentum[1] as i128];
    let first_event_diff = events.iter().zip(&reference.events).position(|(a, b)| a != b);
    json!({
        "bodies": n, "horizon": horizon, "same_genesis": same_genesis,
        "events_equal": events == reference.events, "finals_equal": finals == reference.finals,
        "wall_momentum_equal": wm == reference.wall_momentum,
        "contacts": c.log().contacts, "walls": c.log().walls,
        "first_event_difference": first_event_diff.map(|i| format!("{:?} vs {:?}", events.get(i), reference.events.get(i))),
        "reference_ms": reference_ms, "chronon_ms": chronon_ms,
        "metrics": serde_json::to_value(c.metrics()).unwrap_or(Value::Null),
    })
}

/// All pairs every chronon, no grid: the plainest reading of the law (the C1 audit).
pub fn all_pairs(mut w: emergent_lattice::World, horizon: i64) -> (emergent_lattice::World, emergent_lattice::Log) {
    use emergent_lattice::{law, Event, Log, Response};
    use std::collections::HashMap;
    let mut consumed: HashMap<(usize, usize), (u32, u32)> = HashMap::new();
    let mut log = Log::new(true);
    for t in w.tick + 1..=horizon {
        let n = w.bodies.len();
        let mut pairs = vec![];
        for i in 0..n {
            for j in i + 1..n {
                let (a, b) = (&w.bodies[i], &w.bodies[j]);
                if consumed.get(&(i, j)) == Some(&(a.rev, b.rev)) {
                    continue;
                }
                if law::hit(law::sub(b.x, a.x), law::sub(b.k, a.k), (a.radius + b.radius) as i128) {
                    pairs.push((i, j));
                }
            }
        }
        for b in w.bodies.iter_mut() {
            b.x = [b.x[0] + b.k[0], b.x[1] + b.k[1]];
        }
        let walls: Vec<bool> = w
            .bodies
            .iter()
            .map(|b| {
                b.response == Response::Bounce
                    && w.container.is_some_and(|c| {
                        let (lo, hi) = c.inset(b.radius);
                        law::at_wall(b.x, b.k, lo, hi)
                    })
            })
            .collect();
        let (container, lw, q) = (w.container, w.law, w.q);
        law::respond(lw, q, &mut w.bodies, &pairs, &walls, container.as_ref(), &mut w.wall_momentum);
        for &(i, j) in &pairs {
            consumed.insert((i, j), (w.bodies[i].rev, w.bodies[j].rev));
            log.record(Event { tick: t, kind: Kind::Contact, a: w.bodies[i].id, b: w.bodies[j].id });
        }
        for (i, &on) in walls.iter().enumerate() {
            if on {
                log.record(Event { tick: t, kind: Kind::Wall, a: w.bodies[i].id, b: 0 });
            }
        }
        w.tick = t;
    }
    w.consumed = consumed
        .iter()
        .map(|(&(i, j), &(ra, rb))| law::Consumed { a: w.bodies[i].id, b: w.bodies[j].id, rev_a: ra, rev_b: rb })
        .collect();
    (w.canonical(), log)
}

/// Compare a lattice run of the gas with the independent reference.
pub fn gas_reference_equal(g: &gas::Gas, horizon: i64, world: &emergent_lattice::World, log: &emergent_lattice::Log) -> (bool, Value) {
    let reference = gas::reference(g, horizon as i128);
    let events: Vec<(i128, String, Vec<u64>)> = log
        .sorted()
        .into_iter()
        .map(|e| match e.kind {
            Kind::Contact => (e.tick as i128, "contact".to_string(), vec![e.a, e.b]),
            Kind::Wall => (e.tick as i128, "wall".to_string(), vec![e.a]),
        })
        .collect();
    let finals: Vec<([i128; 2], [i128; 2], i128, u64)> = world
        .bodies
        .iter()
        .map(|b| ([b.x[0] as i128, b.x[1] as i128], [b.k[0] as i128, b.k[1] as i128], b.residual as i128, b.rev as u64))
        .collect();
    let wm = [world.wall_momentum[0] as i128, world.wall_momentum[1] as i128];
    let (ev, fin, w) = (events == reference.events, finals == reference.finals, wm == reference.wall_momentum);
    let first = events.iter().zip(&reference.events).position(|(a, b)| a != b);
    (ev && fin && w, json!({"events_equal": ev, "finals_equal": fin, "wall_momentum_equal": w, "reference_events": reference.events.len(),
        "first_event_difference": first.map(|i| format!("{:?} vs {:?}", events.get(i), reference.events.get(i)))}))
}

/// The relativistic law in the chronon reference against the independent relativistic
/// gas reference (gas_rel.rs, no shared code).
pub fn check_gas_relativistic(n: u64, horizon: i64, vmax: i64, seed: u64) -> Value {
    let g = gas::world(n, 0.1, 1024, vmax as i128, seed);
    let w = worlds::gas(n, 0.1, 1024, vmax, seed).with_law(emergent_lattice::Law::Relativistic).expect("subluminal gas");
    let t = std::time::Instant::now();
    let reference = crate::gas_rel::reference(&g, horizon as i128);
    let reference_ms = t.elapsed().as_secs_f64() * 1e3;
    let mut c = Chronon::new(w, true).expect("gas world");
    c.run_to(horizon);
    let events: Vec<(i128, String, Vec<u64>)> = c
        .log()
        .sorted()
        .into_iter()
        .map(|e| match e.kind {
            Kind::Contact => (e.tick as i128, "contact".to_string(), vec![e.a, e.b]),
            Kind::Wall => (e.tick as i128, "wall".to_string(), vec![e.a]),
        })
        .collect();
    let world = c.world();
    let finals: Vec<([i128; 2], [i128; 2], i128, [i128; 2], u64)> = world
        .bodies
        .iter()
        .map(|b| ([b.x[0] as i128, b.x[1] as i128], [b.k[0] as i128, b.k[1] as i128], b.residual as i128, [b.carry[0] as i128, b.carry[1] as i128], b.rev as u64))
        .collect();
    let wm = [world.wall_momentum[0] as i128, world.wall_momentum[1] as i128];
    let first = events.iter().zip(&reference.events).position(|(a, b)| a != b);
    let first_body = finals.iter().zip(&reference.finals).position(|(a, b)| a != b);
    json!({
        "bodies": n, "horizon": horizon, "vmax_units": vmax,
        "events_equal": events == reference.events, "finals_equal": finals == reference.finals,
        "wall_momentum_equal": wm == reference.wall_momentum,
        "contacts": c.log().contacts, "walls": c.log().walls, "reference_ms": reference_ms,
        "first_event_difference": first.map(|i| format!("{:?} vs {:?}", events.get(i), reference.events.get(i))),
        "first_body_difference": first_body.map(|i| format!("{:?} vs {:?}", finals.get(i), reference.finals.get(i))),
    })
}

/// Compare a relativistic lattice run of the gas with the independent relativistic reference.
pub fn gas_rel_equal(g: &gas::Gas, horizon: i64, world: &emergent_lattice::World, log: &emergent_lattice::Log) -> (bool, Value) {
    let reference = crate::gas_rel::reference(g, horizon as i128);
    let events: Vec<(i128, String, Vec<u64>)> = log
        .sorted()
        .into_iter()
        .map(|e| match e.kind {
            Kind::Contact => (e.tick as i128, "contact".to_string(), vec![e.a, e.b]),
            Kind::Wall => (e.tick as i128, "wall".to_string(), vec![e.a]),
        })
        .collect();
    let finals: Vec<([i128; 2], [i128; 2], i128, [i128; 2], u64)> = world
        .bodies
        .iter()
        .map(|b| ([b.x[0] as i128, b.x[1] as i128], [b.k[0] as i128, b.k[1] as i128], b.residual as i128, [b.carry[0] as i128, b.carry[1] as i128], b.rev as u64))
        .collect();
    let wm = [world.wall_momentum[0] as i128, world.wall_momentum[1] as i128];
    let (ev, fin, w) = (events == reference.events, finals == reference.finals, wm == reference.wall_momentum);
    (ev && fin && w, json!({"events_equal": ev, "finals_equal": fin, "wall_momentum_equal": w, "reference_events": reference.events.len()}))
}
