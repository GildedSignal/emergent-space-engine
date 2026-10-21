//! Fixed, changed-velocity rebind census drawn from the N1 population, not repeated identical keys.
use emergent_universe::{bind::bind_surface, fleet::Order, scenario::plane_extra, Config};
use std::{hint::black_box, time::Instant};
fn main() {
    let n: usize = std::env::args()
        .nth(1)
        .unwrap_or("0".into())
        .parse()
        .unwrap();
    let p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let mut inputs = Vec::new();
    let count = p.u.n_bodies();
    for j in 0..1024 {
        let i = j * count / 1024;
        let r = p.u.rec(i);
        if !r.alive {
            continue;
        }
        let mut st = r.b.readout(r.b.event_time).unwrap();
        // A distinct, small physical kick (~2^-30 c), retained in the body's exact word.
        let kick = (1i64 << (-30 - st.velocity_exponent as i32).clamp(0, 40)) + j as i64;
        st.velocity[j % 2] = st.velocity[j % 2].checked_add(kick).unwrap();
        let d = &p.u.dolls[r.b.doll as usize];
        inputs.push((st, r.b.event_time, d.clock_exp(), d.edge, d.unit, d.surface));
    }
    let mut ns = Vec::new();
    let mut refused = 0;
    let _ = emergent_space::binding::take_fit_profile();
    let begin = Instant::now();
    for (st, t, clock, edge, unit, surface) in inputs {
        let start = Instant::now();
        let fit = bind_surface(black_box(st), t, clock, Some(edge), unit, Some(surface));
        ns.push(start.elapsed().as_nanos());
        if fit.is_err() {
            refused += 1;
        }
        let _ = black_box(fit);
    }
    let profile = emergent_space::binding::take_fit_profile();
    if profile.iter().sum::<u128>() > 0 {
        println!("fit_profile_us: inverse={:.3} shape={:.3} locate={:.3} reconstruct={:.3}", profile[0] as f64 / 1000. / ns.len() as f64, profile[1] as f64 / 1000. / ns.len() as f64, profile[2] as f64 / 1000. / ns.len() as f64, profile[3] as f64 / 1000. / ns.len() as f64);
    }
    ns.sort_unstable();
    println!("rebind: n={n} samples={} mean_us={:.3} p50_us={:.3} p99_us={:.3} refused={refused} wall_s={:.3}", ns.len(), ns.iter().sum::<u128>() as f64 / ns.len() as f64 / 1000., ns[ns.len()/2] as f64 / 1000., ns[ns.len()*99/100] as f64 / 1000., begin.elapsed().as_secs_f64());
    println!("cache: {:?}", emergent_space::orbit::shape_cache_stats());
}
