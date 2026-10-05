// Jacobi error against the step: ships on circles at 1.5 to 3 Hill radii of a Jupiter, run for N planet periods at
// 2^step_log2 kicks per period. `jacobi STEP_LOG2 PERIODS SHIPS`; SYNC=1 samples the split's output (the ship's last boundary).
// States are read as every reader reads them, completed by the ramp between kicks (docs/law.md, "A body's state between
// kicks"); RAW=1 reads the tubes alone (the pending half kick, first order in the step).
use emergent_universe::observe::{root_state, root_state_raw};
use emergent_universe::scenario::restricted_with;
use emergent_universe::Config;
fn main() {
    let step_log2: i32 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(6);
    let periods: i64 = std::env::args().nth(2).map(|s| s.parse().unwrap()).unwrap_or(100);
    let sep = 527_000_000i64;
    let hill = sep as f64 * (2f64.powi(-10) / 3.0).cbrt();
    let n: usize = std::env::args().nth(3).map(|s| s.parse().unwrap()).unwrap_or(6);
    let mut ships = Vec::new();
    let mut seed = 0x9E3779B97F4A7C15u64;
    let mut rnd = || { seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407); (seed >> 11) as f64 / (1u64 << 53) as f64 };
    for i in 0..n {
        let k = 1.5 + 1.5 * rnd();
        let side = if i % 2 == 0 { 1.0 } else { -1.0 };
        let r = sep as f64 + side * hill * k;
        ships.push((r as i64, ((rnd() * (1u64 << 32) as f64) as u64 % (1 << 32)) as u32));
    }
    let cfg = Config { step_log2, ..Config::default() };
    let mut w = restricted_with(-10, sep, 49_000, &ships, 1, cfg).unwrap();
    let mu = 2f64.powi(-10);
    let omega = (1.0 + mu).sqrt() / (sep as f64).powf(1.5);
    let period = 2.0 * std::f64::consts::PI / omega;
    let jac = |w: &emergent_universe::scenario::Restricted, sh: usize, t: i64| {
        let ctx = w.u.ctx();
        let read = if std::env::var("RAW").is_ok() { root_state_raw } else { root_state };
        let (xs, vs) = read(&ctx, sh, t).unwrap();
        let (xp, _) = read(&ctx, w.planet, t).unwrap();
        let r = (xs[0]*xs[0]+xs[1]*xs[1]).sqrt();
        let d = ((xs[0]-xp[0]).powi(2)+(xs[1]-xp[1]).powi(2)).sqrt();
        let rp3 = (xp[0]*xp[0]+xp[1]*xp[1]).powf(1.5);
        let e = 0.5*(vs[0]*vs[0]+vs[1]*vs[1]) - 1.0/r - mu/d + if std::env::var("NOIND").is_ok() {0.0} else { mu*(xs[0]*xp[0]+xs[1]*xp[1])/rp3 };
        let l = xs[0]*vs[1]-xs[1]*vs[0];
        e - omega*l
    };
    let c0: Vec<f64> = w.ships.iter().map(|&s| jac(&w, s, 0)).collect();
    let mut worst = vec![0.0f64; ships.len()];
    let mut series: Vec<Vec<f64>> = vec![Vec::new(); ships.len()];
    let mut last_doll = vec![0u16; ships.len()];
    let mut passes = vec![0u32; ships.len()];
    let t0 = std::time::Instant::now();
    let fine: i64 = std::env::var("FINE").ok().map(|v| v.parse().unwrap()).unwrap_or(1);
    for k in 1..=(periods * 8 * fine) {
        let t = (k as f64 * period / (8.0 * fine as f64)) as i64;
        w.u.settle(t);
        for (i, &sh) in w.ships.iter().enumerate() {
            if !w.u.rec(sh).alive && std::env::var("ALIVE").is_ok() {
                continue;
            }
            let ts = if std::env::var("SYNC").is_ok() { w.u.rec(sh).anchor } else { t };
            let err = ((jac(&w, sh, ts) - c0[i]) * ships[i].0 as f64).abs();
            worst[i] = worst[i].max(err);
            series[i].push(err);
            if let Ok(wi) = std::env::var("WATCH") { if wi.parse::<usize>().unwrap() == i { let ctx = w.u.ctx(); let (xs, _) = root_state(&ctx, sh, t).unwrap(); let (xp, _) = root_state(&ctx, w.planet, t).unwrap(); println!("k {k} t {t} err {err:.2e} doll {} dist/hill {:.2}", w.u.rec(sh).b.doll, ((xs[0]-xp[0]).powi(2)+(xs[1]-xp[1]).powi(2)).sqrt()/hill); } }
            let d = w.u.rec(sh).b.doll;
            if d != last_doll[i] { if d == 1 { passes[i] += 1; } last_doll[i] = d; }
        }
    }
    println!("captures per ship: {passes:?}");
    for (i, &sh) in w.ships.iter().enumerate() {
        let r = w.u.rec(sh);
        if !r.alive {
            println!("ship {i} is gone: fault {:?}, doll {}, last binding at {}, refusals {}", r.fault, r.b.doll, r.b.event_time, r.refusals);
        }
    }
    let s = w.u.stats;
    println!("step 2^-{step_log2}: worst per ship {:?} | {:.1}s kicks {} handoffs {} lost {}", worst.iter().map(|x| format!("{x:.1e}")).collect::<Vec<_>>(), t0.elapsed().as_secs_f64(), s.kicks, s.handoffs, s.lost);
}
