//! Pin probe (clock job, 12 October): at log-spaced checkpoints of a held burn from the plane start, the exact E of the readout state (E = f·u^t) next to the E the compiled key implies (tn/d from k and the periapsis) and the tube's own dt/dtau (orbit_state proper time). Usage: clock_pin <level> [log2 tmax]; outputs in artifacts/runs/clock/.
use emergent_space::orbit::Scalar;
use emergent_universe::num::{to_f64, Tick};
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;

fn main() {
    let level: u8 = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(15);
    let tmax: f64 = std::env::args().nth(2).and_then(|s| s.parse().ok()).unwrap_or(41.7);
    let cfg = emergent_universe::Config::default();
    let mut p = plane(cfg, 1, emergent_universe::fleet::Order::Sparse, 1, 48).unwrap();
    let me = p.player;
    p.u.input(0, word(1, level)).unwrap();
    let f64v = |v: [Scalar; 2]| [to_f64(v[0]), to_f64(v[1])];
    let n = 100;
    let mut t_prev = 0i64;
    for j in 0..=n {
        let t: i64 = if j == 0 { 0 } else { (2f64.powf(24.0 + (tmax - 24.0) * j as f64 / n as f64)) as i64 };
        if t <= t_prev { continue; }
        p.u.settle(t);
        let rec = p.u.rec(me);
        if !rec.alive { eprintln!("lost at {t}: {:?}", rec.fault); break; }
        let ctx = p.u.ctx();
        let (x, v) = match rec.b.cartesian(t) { Ok((x, v)) => (f64v(x), f64v(v)), Err(e) => { eprintln!("refused {e:?}"); break; } };
        let mu = to_f64(ctx.tube_unit(me, rec.b.doll).unwrap().mu);
        let r = (x[0] * x[0] + x[1] * x[1]).sqrt();
        let f = 1.0 - 2.0 * mu / r;
        let rh = [x[0] / r, x[1] / r];
        let vr = v[0] * rh[0] + v[1] * rh[1];
        let vt = -v[0] * rh[1] + v[1] * rh[0];
        let den = f - vr * vr / f - vt * vt;
        let ut = 1.0 / den.sqrt();
        let e_ex = f * ut;
        let l_ex = r * vt * ut;
        // key
        let key = rec.b.entry.trajectory.key();
        let peri = to_f64(key.periapsis);
        let kq = key.k as f64 / 2f64.powi(48);
        let q = 1.0 / peri;
        let eta = 1.0 - kq;
        let d = kq - q * (3.0 * kq * kq + eta * eta);
        let tn = kq * (1.0 - 2.0 * q) * (1.0 + 2.0 * q * (1.0 - 2.0 * kq));
        let e_key = (tn / d).sqrt();
        // tube's dt/dtau
        let shift = ctx.dolls[rec.b.doll as usize].shift as i32;
        let dtk: Tick = 1 << 16;
        let a = rec.b.orbit_state(t).unwrap().proper_time;
        let b = rec.b.orbit_state(t + dtk).unwrap().proper_time;
        let dtau = to_f64(b.sub(a).unwrap()) * 2f64.powi(-shift);
        let dtdtau = dtk as f64 / dtau;
        let kind = match &rec.b.entry.trajectory { emergent_space::binding::Trajectory::Cycle(_) => "cycle", _ => "passage" };
        let b2 = (l_ex / e_ex).abs();
        eprintln!("t={:>12} r={:>11.4e} gamma={:>11.4} E_exact={:>12.6} E_key={:>12.6} dt/dtau_tube={:>11.6} u^t={:>12.6} L/E={:.4e} peri={:.4e} k={:.6e} q={:.3e} kind={kind} refusals={} ev_lag={}", t, r, 1.0/(1.0-(vr*vr+vt*vt)).sqrt(), e_ex, e_key, dtdtau, ut, b2, peri, kq, q, rec.refusals, t-rec.b.event_time);
        t_prev = t;
    }
}
