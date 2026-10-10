// Lens: components. The kick event's decomposition against its floor.
// Runs the plane's own pure resolve (like cost_split) and counts rebinds; then times
// the state readout's two extremes: signed_state (cold t→ψ solve, what every readout pays)
// against crossing_state (the direct crossing-table read: no quadrature, no root solve).
use emergent_space::binding::Trajectory;
use emergent_space::orbit::Scalar;
use emergent_universe::body::What;
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::step::{self, Resolved};
use emergent_universe::Config;
use std::time::Instant;

fn main() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
    let ship = p.ships[14];
    let ctx = p.u.ctx();
    let rec0 = p.u.rec(ship);
    let n = 3000;

    // 1) Pure resolve: kicks and rebinds (a rebind is new_entry set on a Kick).
    let t0 = Instant::now();
    let (mut kicks, mut rebinds, mut not_kick) = (0u32, 0u32, 0u32);
    for _ in 0..n {
        let mut r = rec0.clone();
        while !matches!(r.plan.first().map(|i| i.what), Some(What::Kick(0))) {
            if r.plan.remove(0).what == What::Boundary && r.plan.is_empty() {
                break;
            }
        }
        if !matches!(r.plan.first().map(|i| i.what), Some(What::Kick(0))) {
            not_kick += 1;
            continue;
        }
        let u = step::process(&ctx, ship, r);
        kicks += matches!(u.kind, Resolved::Kick) as u32;
        rebinds += (u.kind == Resolved::Kick && u.new_entry.is_some()) as u32;
        std::hint::black_box(&u);
    }
    let per = t0.elapsed().as_secs_f64() * 1e6 / n as f64;
    println!(
        "pure resolve {per:.1} us: {kicks} kicks, {rebinds} rebinds ({:.0}%), {not_kick} non-kick records",
        100.0 * rebinds as f64 / kicks.max(1) as f64
    );

    // 2) The readout's two extremes on this ship's own compiled orbit.
    let entry = rec0.b.entry.clone();
    let orbit = match &entry.trajectory {
        Trajectory::Cycle(o) => o,
        _ => panic!("not a cycle"),
    };
    let t = rec0.b.event_time + rec0.interval.max(1);
    let h = rec0.interval.max(1) as i64 * 1009;
    let t0 = Instant::now();
    for i in 0..n {
        let tt = Scalar::integer(t + i as i64 * h);
        std::hint::black_box(orbit.signed_state(tt).unwrap());
    }
    let signed = t0.elapsed().as_secs_f64() * 1e6 / n as f64;
    println!("signed_state (cold solve, sequential H steps) {signed:.2} us");

    // How many knots does one compiled cycle carry (the table a kick's state sits inside)?
    let mut knots = 0usize;
    loop {
        match orbit.crossing_state(knots, 0, true) {
            Ok(_) => knots += 1,
            Err(_) => break,
        }
    }
    // Direct table reads: the floor of a state read if the kick's phase were the parameter.
    let t0 = Instant::now();
    for i in 0..n {
        let k = knots.saturating_sub(1).min(1 + i % knots.max(2));
        std::hint::black_box(orbit.crossing_state(k, (i / 8) as u64, i % 2 == 0).unwrap());
    }
    let cross = t0.elapsed().as_secs_f64() * 1e6 / n as f64;
    println!("crossing_state (direct table read) {cross:.3} us  ({:.0}x below signed_state)", signed / cross);

    // The binding-level readout the kick actually calls, sequential kick times.
    let t0 = Instant::now();
    for i in 0..n {
        let tt = rec0.b.event_time + rec0.interval.max(1) as i64 * (i as i64 + 1);
        std::hint::black_box(rec0.b.readout(tt).unwrap());
    }
    let ro = t0.elapsed().as_secs_f64() * 1e6 / n as f64;
    println!("binding readout at kick times {ro:.2} us");

    drop(ctx);
    let _ = &mut p;
}
