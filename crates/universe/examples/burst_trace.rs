use emergent_universe::num::to_f64;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{fleet::Order, scenario::plane, thrust::word, Config};
fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.get(1).is_some_and(|s| s == "warning") {
        warning();
        return;
    }
    let level: u8 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(8);
    let mut p = plane(Config::default(), 5, Order::Sparse, 1, 8).unwrap();
    let start = 2_000_000;
    let end = start + (2000.0 / TICK_SECONDS) as i64;
    p.u.settle(start);
    p.u.input(start, word(1, level)).unwrap();
    println!("seconds,kicks,interval_seconds,nominal_seconds,ahead_seconds,doll,speed_c");
    loop {
        let r = p.u.rec(p.player);
        let th = r.thrust.unwrap();
        let t = r.plan[0].t;
        if t > end {
            break;
        }
        let before = th.since;
        p.u.settle(t);
        let r = p.u.rec(p.player);
        let th = r.thrust.unwrap();
        if th.since != before {
            let (_, v) = r.b.cartesian(t).unwrap();
            let speed = (to_f64(v[0]).powi(2) + to_f64(v[1]).powi(2)).sqrt();
            println!(
                "{:.6},{},{:.6},{:.6},{:.6},{},{:.9}",
                (t - start) as f64 * TICK_SECONDS,
                th.kicks,
                r.interval as f64 * TICK_SECONDS,
                r.step as f64 * TICK_SECONDS,
                to_f64(th.ahead) * TICK_SECONDS,
                r.b.doll,
                speed
            );
        }
        if !r.alive {
            break;
        }
    }
    p.u.settle(end);
    p.u.input(end, word(0, level)).unwrap();
    let r = p.u.rec(p.player);
    eprintln!(
        "cut: alive={} refusals={} ahead={} proper={}",
        r.alive,
        r.refusals,
        to_f64(r.thrust.unwrap().ahead),
        to_f64(r.proper)
    );
}

fn warning() {
    use emergent_universe::{Budget, view::gather, observe::held_thrust};
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 8).unwrap();
    p.u.input(0, word(2, 4)).unwrap();
    for f in 0..10 {
        p.u.frame(1.0/60.0, 100.0, Budget::unlimited());
        let v = gather(&p.u, &p.names).unwrap();
        if v.impact.is_some() {
            let r = p.u.rec(p.player);
            let th = r.thrust.unwrap();
            let peri = r.b.to_doll(r.b.entry.trajectory.key().unwrap().periapsis).unwrap();
            let surface = p.u.dolls[r.b.doll as usize].surface;
            let (_, dv) = held_thrust(&p.u.ctx(), &r, p.u.now).unwrap().unwrap();
            println!("before cut: frame={f} t={} ahead_s={:.9} correction_c={dv:?} peri_over_surface={:.9} warning={:?}", p.u.now, to_f64(th.ahead)*TICK_SECONDS, to_f64(peri)/to_f64(surface),v.impact);
            p.u.input(p.u.now,word(0,4)).unwrap();
            let r = p.u.rec(p.player);
            let peri = r.b.to_doll(r.b.entry.trajectory.key().unwrap().periapsis).unwrap();
            println!("after cut: ahead={} peri_over_surface={:.9} warning={:?} refusals={}",to_f64(r.thrust.unwrap().ahead),to_f64(peri)/to_f64(surface),gather(&p.u,&p.names).unwrap().impact,r.refusals);
            return;
        }
    }
    panic!("no warning in ten frames");
}
