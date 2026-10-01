// A ship on a bound planetocentric orbit whose apoapsis is just past the edge: it crosses the edge,
// leaves the planet's doll and falls back, again and again. Jacobi error against passes.
use emergent_universe::num::s;
use emergent_universe::observe::root_state;
use emergent_universe::scenario::restricted;
use emergent_universe::{Kind, OrbitSpec};
fn main() {
    let peri: f64 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(0.1);
    let apo: f64 = std::env::args().nth(2).map(|s| s.parse().unwrap()).unwrap_or(1.05);
    let periods: i64 = std::env::args().nth(3).map(|s| s.parse().unwrap()).unwrap_or(40);
    let sep = 527_000_000i64;
    let mut w = restricted(-10, sep, 49_000, &[], 1).unwrap();
    let edge = emergent_universe::num::to_f64(w.u.dolls[1].edge);
    let e = (apo - peri) / (apo + peri);
    let p = (edge * peri) as i64;
    let sh = w.u.add_body(Kind::Ship, OrbitSpec { doll: 1, periapsis: s(p), e_q48: (e * (1u64 << 48) as f64) as u64, clockwise: false, angle: 1 << 29, phase: 1 << 31 }, emergent_space::orbit::Scalar::ZERO).unwrap();
    w.u.start().unwrap();
    let mu = 2f64.powi(-10);
    let omega = 1.0 / (sep as f64).powf(1.5);
    let period = 2.0 * std::f64::consts::PI * (sep as f64).powf(1.5);
    let jac = |w: &emergent_universe::scenario::Restricted, t: i64| {
        let ctx = w.u.ctx();
        let (xs, vs) = root_state(&ctx, sh, t).unwrap();
        let (xp, _) = root_state(&ctx, w.planet, t).unwrap();
        let r = (xs[0]*xs[0]+xs[1]*xs[1]).sqrt();
        let d = ((xs[0]-xp[0]).powi(2)+(xs[1]-xp[1]).powi(2)).sqrt();
        let e = 0.5*(vs[0]*vs[0]+vs[1]*vs[1]) - 1.0/r - mu/d;
        let l = xs[0]*vs[1]-xs[1]*vs[0];
        e - omega*l
    };
    let c0 = jac(&w, 0);
    let scale = sep as f64;
    let mut worst = 0.0f64; let mut series = Vec::new();
    let t0 = std::time::Instant::now();
    for k in 1..=(periods * 16) {
        let t = (k as f64 * period / 16.0) as i64;
        w.u.settle(t);
        let r = w.u.rec(sh);
        if !r.alive { println!("lost at t/P={:.2} {:?}", t as f64 / period, r.fault); break; }
        if k == 1 { let st = r.b.entry.trajectory.key(); println!("peri {} k {} edge {} step {} interval {} plan {:?}", emergent_universe::num::to_f64(st.periapsis), st.k as f64/(1u64<<48) as f64, edge, r.step, r.interval, &r.plan[..r.plan.len().min(4)]); }
        let err = ((jac(&w, r.anchor) - c0) * scale).abs();
        worst = worst.max(err); series.push(err);
        if k % (16 * 5) == 0 { println!("P={:>3} worst {:.2e} doll {} handoffs {} kicks {}", k / 16, worst, r.b.doll, w.u.stats.handoffs, w.u.stats.kicks); }
    }
    println!("{:.1}s handoffs {}", t0.elapsed().as_secs_f64(), w.u.stats.handoffs);
}
