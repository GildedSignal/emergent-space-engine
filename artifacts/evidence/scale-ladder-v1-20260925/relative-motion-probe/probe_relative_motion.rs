//! TEMPORARY probe (delete after use): cost of proving "no contact" when groups move relative
//! to each other. Parallel lanes never touch, so every row must finish with 0 events.
use emergent_engine::{
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    scenario::JULIAN_YEAR_TICKS,
    Engine, WorkBudget,
};
use std::time::Instant;

fn world(count: u64, groups: u64, delta_den: i128, vertical: bool) -> Engine {
    let mut families = Vec::new();
    let mut first = 10_000;
    for lane in 0..groups {
        let len = count / groups;
        // speed along the lane = 1/4 + lane * 2^-k (0 when delta_den == 0)
        let along = if delta_den == 0 {
            r(1) / r(4)
        } else {
            r(1) / r(4) + r(lane as i128) / r(delta_den)
        };
        let offset = 100_000 + lane as i128 * 1000;
        let (pos, vel, stride) = if vertical {
            (Vec2::new(offset, 0), Vec2 { x: r(0), y: along }, Vec2::new(0, 64))
        } else {
            (Vec2::new(0, offset), Vec2 { x: along, y: r(0) }, Vec2::new(64, 0))
        };
        families.push(Family::affine(
            format!("L{lane}"),
            first,
            len,
            0,
            Inertial::new(0, pos, vel).unwrap(),
            stride,
            r(1),
            r(1),
        ));
        first += len;
    }
    Engine::new(0x0E5C_A051, vec![], families).unwrap()
}

fn main() {
    let cap_s = 20.0;
    let mut cases = Vec::new();
    for &g in &[16u64, 256] {
        for &k in &[0i128, 1 << 30, 1 << 20, 1 << 10] {
            for &v in &[false, true] {
                cases.push((g, k, v, 10_000_000_000i128));
            }
        }
    }
    for &years in &[1i128, 1_000, 1_000_000, 1_000_000_000] {
        cases.push((16, 1 << 10, false, years));
    }
    println!("groups,delta,axis,years,complete,events,ops,aabb_compares,rejections,family_range_ops,ms");
    for (g, k, vertical, years) in cases {
        let mut e = world(1_000_000_000, g, k, vertical);
        let target = years * JULIAN_YEAR_TICKS;
        let t = Instant::now();
        let (mut ops, mut events, mut complete) = (0usize, 0usize, false);
        while t.elapsed().as_secs_f64() < cap_s {
            let res = e.advance(target, WorkBudget::new(100_000)).unwrap();
            ops += res.operations;
            events += res.events;
            if res.complete {
                complete = true;
                break;
            }
        }
        let m = serde_json::to_value(&e.metrics).unwrap();
        let get = |f: &str| m.get(f).and_then(|x| x.as_u64()).unwrap_or(0);
        println!(
            "{g},{},{},{years},{complete},{events},{ops},{},{},{},{:.2}",
            if k == 0 { "0".into() } else { format!("2^-{}", k.trailing_zeros()) },
            if vertical { "y" } else { "x" },
            get("aabb_compares"),
            get("certified_rejections"),
            get("family_range_ops"),
            t.elapsed().as_secs_f64() * 1e3
        );
    }
}
