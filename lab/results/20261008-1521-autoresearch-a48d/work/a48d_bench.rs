use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::force;
use emergent_universe::{bind, Config};
use std::time::Instant;
fn bench<T>(name: &str, n: usize, mut f: impl FnMut() -> T) {
    for _ in 0..(n / 10).max(1) {
        std::hint::black_box(f());
    }
    let t0 = Instant::now();
    let mut last = None;
    for _ in 0..n {
        last = Some(f());
    }
    let per = t0.elapsed().as_secs_f64() * 1e6 / n as f64;
    if let Some(l) = &last {
        println!("{name:<34} {per:7.2} us   ptr {l:p}");
    }
}

fn main() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
    let ship = p.ships[14];
    let n = 3000;
    let ctx = p.u.ctx();
    let rec = p.u.rec(ship);
    bench("process (full kick)", n, || {
        let mut r = rec.clone();
        while !matches!(r.plan.first().map(|i| i.what), Some(emergent_universe::body::What::Kick(0))) {
            r.plan.remove(0);
        }
        emergent_universe::step::process(&ctx, ship, r)
    });
    let t = rec.b.event_time + 1000;
    bench("readout", n, || rec.b.readout(t).unwrap());
    let st = rec.b.readout(t).unwrap();
    let (x, v) = bind::scalars(&st).unwrap();
    bench("secondaries", n, || ctx.secondaries(rec.b.doll, t, ship).unwrap());
    let secs = ctx.secondaries(rec.b.doll, t, ship).unwrap();
    bench("tide", n, || ctx.tide(rec.b.doll, t).unwrap());
    let tide = ctx.tide(rec.b.doll, t).unwrap();
    bench("force::acceleration", n, || force::acceleration(0, x, &secs, tide).unwrap());
    // the rebind, exactly as kick() does it (root doll ships: no passage edge; else 2*edge)
    let clock_exp = ctx.dolls[rec.b.doll as usize].clock_exp();
    let edge = if rec.b.doll != 0 { ctx.dolls[rec.b.doll as usize].edge.scale(2).ok() } else { None };
    let unit = ctx.tube_unit(ship, rec.b.doll).unwrap();
    // inside the readout: the solve vs the read
    if let emergent_space::binding::Trajectory::Cycle(o) = &rec.b.entry.trajectory {
        let elapsed = emergent_space::orbit::Scalar::integer(1_000_003);
        bench("Trajectory state (solve+read)", n, || o.signed_state(elapsed).unwrap());
        let st8 = o.signed_state(elapsed).unwrap();
        let probe = emergent_space::orbit::Scalar::raw(1, -40).unwrap();
        bench("at_phase (solve+read)", n, || o.at_phase(st8.cycles, probe).unwrap());

        bench("crossing_state (read only)", n, || o.crossing_state(o.shape().knots().len() / 2, st8.cycles, true).unwrap());
        bench("Orbit::compile", n, || emergent_space::orbit::Orbit::compile(o.key()).unwrap());
    }
    bench("bind (the rebind)", n, || bind::bind(st.clone(), t, clock_exp, edge, unit).unwrap());
    // and inside bind: from_state on the same state, in tube units
    bench("bind+rebind via from_state", n, || {
        emergent_space::binding::Rebinding::from_state(st.clone(), emergent_space::orbit::Scalar::integer(0), None)
    });
    drop(ctx);
    drop(p);
}
