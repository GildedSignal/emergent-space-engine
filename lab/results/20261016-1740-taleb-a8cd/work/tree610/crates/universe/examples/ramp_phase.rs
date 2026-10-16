// Jacobi error against the phase inside a body's step (anchor .. anchor + interval): `ramp_phase STEP_LOG2 PERIODS SHIP`.
// For the ships of `jacobi`, binned by the fraction of the step the sample falls at, raw tube and ramped readout.
use emergent_universe::observe::{root_state, root_state_raw};
use emergent_universe::scenario::restricted_with;
use emergent_universe::Config;
fn main() {
    let step_log2: i32 = std::env::args().nth(1).map(|s| s.parse().unwrap()).unwrap_or(7);
    let periods: i64 = std::env::args().nth(2).map(|s| s.parse().unwrap()).unwrap_or(20);
    let which: usize = std::env::args().nth(3).map(|s| s.parse().unwrap()).unwrap_or(1);
    let sep = 527_000_000i64;
    let hill = sep as f64 * (2f64.powi(-10) / 3.0).cbrt();
    let mut ships = Vec::new();
    let mut seed = 0x9E3779B97F4A7C15u64;
    let mut rnd = || { seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407); (seed >> 11) as f64 / (1u64 << 53) as f64 };
    for i in 0..12 {
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
    let jac = |w: &emergent_universe::scenario::Restricted, sh: usize, t: i64, raw: bool| {
        let ctx = w.u.ctx();
        let f = if raw { root_state_raw } else { root_state };
        let (xs, vs) = f(&ctx, sh, t).unwrap();
        let (xp, _) = f(&ctx, w.planet, t).unwrap();
        let r = (xs[0]*xs[0]+xs[1]*xs[1]).sqrt();
        let d = ((xs[0]-xp[0]).powi(2)+(xs[1]-xp[1]).powi(2)).sqrt();
        let rp3 = (xp[0]*xp[0]+xp[1]*xp[1]).powf(1.5);
        let e = 0.5*(vs[0]*vs[0]+vs[1]*vs[1]) - 1.0/r - mu/d + mu*(xs[0]*xp[0]+xs[1]*xp[1])/rp3;
        let l = xs[0]*vs[1]-xs[1]*vs[0];
        e - omega*l
    };
    let sh = w.ships[which];
    let c0 = jac(&w, sh, 0, true);
    const BINS: usize = 10;
    let mut worst = [[0.0f64; BINS]; 2];
    let fine = 37i64;
    for k in 1..=(periods * 8 * fine) {
        let t = (k as f64 * period / (8.0 * fine as f64)) as i64;
        w.u.settle(t);
        let rec = w.u.rec(sh);
        if !rec.alive || rec.interval == 0 { continue; }
        let ph = ((t - rec.anchor) as f64 / rec.interval as f64).clamp(0.0, 0.9999);
        let b = (ph * BINS as f64) as usize;
        for (m, raw) in [true, false].into_iter().enumerate() {
            let err = ((jac(&w, sh, t, raw) - c0) * ships[which].0 as f64).abs();
            worst[m][b] = worst[m][b].max(err);
            if !raw && err > 1.0e-4 * 0.0 + std::env::var("SHOW").ok().and_then(|v| v.parse::<f64>().ok()).unwrap_or(f64::INFINITY) {
                let ctx = w.u.ctx();
                let (xs, _) = root_state(&ctx, sh, t).unwrap();
                let (xp, _) = root_state(&ctx, w.planet, t).unwrap();
                let d = ((xs[0]-xp[0]).powi(2)+(xs[1]-xp[1]).powi(2)).sqrt() / hill;
                println!("t {t} phase {ph:.3} err {err:.2e} doll {} dist/hill {d:.3} interval {} step {} kick level {} len {} M-t {}", rec.b.doll, rec.interval, rec.step, rec.b.kick.level, rec.b.kick.len, t - rec.b.event_time);
            }
        }
    }
    println!("ship {which}, step 2^-{step_log2}, worst Jacobi error by phase of the step (deciles):");
    for (m, name) in ["raw tube   ", "ramped     "].iter().enumerate() {
        println!("{name} {:?}", worst[m].iter().map(|x| format!("{x:.1e}")).collect::<Vec<_>>());
    }
}
