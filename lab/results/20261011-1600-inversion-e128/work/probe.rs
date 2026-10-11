//! Inversion probe (run 20261011-1600-inversion-e128): what the merged energy register and
//! held-burn cap actually carry between the merge's green point (β 0.999, no physics checked
//! there) and the first stop — held out: the leave, a register refusal, or a law failure.
//!
//! Measures, at log-spaced checkpoints of a held level-`L` forward burn from the plane's start:
//! the local γ and rapidity against the exact closed form γ(τ) = γ₀·cosh(ατ) + (u₀·n)·sinh(ατ);
//! the relativistic work integral ΔE_∞ = ∫√f·(u·n)·α·dτ; the throttle gate's own Newtonian
//! criterion ΔE_N = ∫α·v_x·dt; the register (pt, pt_exp, carries) and its constraint violation
//! p_t − (U_P − H_D); the binding's words; refusals, loss and the event lag.
use emergent_space::orbit::Scalar;
use emergent_universe::force;
use emergent_universe::num::{to_f64, Tick};
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::Universe;

/// The local (static-frame) speed and γ at a doll state, with f = 1 − 2μ/r.
fn local(x: [f64; 2], v: [f64; 2], mu: f64) -> (f64, f64, f64) {
    let r = (x[0] * x[0] + x[1] * x[1]).sqrt();
    let f = 1.0 - 2.0 * mu / r;
    let rh = [x[0] / r, x[1] / r];
    let th = [-rh[1], rh[0]];
    let vr = v[0] * rh[0] + v[1] * rh[1];
    let vt = v[0] * th[0] + v[1] * th[1];
    let sf = f.max(1e-18).sqrt();
    let w = [vr / f.max(1e-18), vt / sf];
    let w2 = w[0] * w[0] + w[1] * w[1];
    (w2.sqrt(), 1.0 / (1.0 - w2.min(1.0 - 1e-18)).sqrt(), f)
}

struct Row {
    t: i64,
    tau: f64,        // proper ticks since 0
    beta: f64,       // |v| doll units (c = 1)
    gamma: f64,      // local γ
    gamma_pred: f64, // γ₀cosh(ατ) + (u₀n)sinh(ατ)
    gamma_exact_t: f64, // √(1+(αt)²): the SR-exact γ at coordinate time t
    r: f64,
    e_inf: f64,      // γ√f
    work_gate: f64,  // ∫ α v_x dt  (the frozen gate's work)
    work_rel: f64,   // ∫ √f (u·n) α dτ (the exact relativistic work)
    e_newton: f64,   // v²/2 − μ/r
    pt: i128,
    pt_exp: i16,
    pt_carry: i64,
    viol: f64,       // p_t − (U_P − H_D), doll units
    ve: i16,
    le: i16,
    lag: i64,
    refusals: u64,
    alive: bool,
    step: i64,
}

fn main() {
    let level: u8 = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(15);
    let tmax: f64 = std::env::args().nth(2).and_then(|s| s.parse().ok()).unwrap_or(41.7);
    let cfg = emergent_universe::Config::default();
    let alpha = 2f64.powi(cfg.thrust_log2 + level as i32); // rapidity per proper tick
    let mut p = plane(cfg, 1, emergent_universe::fleet::Order::Sparse, 1, 48).unwrap();
    let me = p.player;
    p.u.input(0, word(1, level)).unwrap();

    let ctx = p.u.ctx();
    let mu = to_f64(ctx.tube_unit(me, 0).unwrap().mu);
    let shift = ctx.dolls[0].shift as i32;
    let f64v = |v: [Scalar; 2]| [to_f64(v[0]), to_f64(v[1])];

    // The start state at t = 0: γ₀ and u₀·n (n = (1,0), the heading is 0 and no turn key is held).
    let (x0, v0) = {
        let r = p.u.rec(me);
        let (x, v) = r.b.cartesian(0).unwrap();
        (f64v(x), f64v(v))
    };
    let (w0, g0, _) = local(x0, v0, mu);
    let u0n = g0 * w0 * v0[0] / (v0[0] * v0[0] + v0[1] * v0[1]).sqrt(); // γ·w·(v̂·n)
    let eta0 = ((1.0 + w0) / (1.0 - w0)).sqrt().ln();
    eprintln!("start: r0={} v0=({},{}) mu={} w0={} gamma0={} u0n={} eta0={}", (x0[0] * x0[0] + x0[1] * x0[1]).sqrt(), v0[0], v0[1], mu, w0, g0, u0n, eta0);

    let proper_at = |u: &Universe, t: Tick| -> f64 {
        let rec = u.rec(me);
        let d = rec.b.doll as usize;
        let now = rec.b.orbit_state(t).unwrap().proper_time;
        let ev = rec.b.orbit_state(rec.b.event_time).unwrap().proper_time;
        to_f64(rec.proper) + to_f64(now.sub(ev).unwrap()) * 2f64.powi(-(u.ctx().dolls[d].shift as i32))
    };

    let mut rows: Vec<Row> = Vec::new();
    let mut work_gate = 0.0f64;
    let mut work_rel = 0.0f64;
    let mut prev: Option<(f64, f64, f64, f64, f64)> = None; // (t, tau, vx, e_inf, un)
    let mut t_prev = 0i64;
    let n = 140;
    for j in 0..=n {
        let t = if j == 0 { 0 } else { (2f64.powf(24.0 + (tmax - 24.0) * j as f64 / n as f64)) as i64 };
        if t <= t_prev {
            continue;
        }
        p.u.settle(t);
        let rec = p.u.rec(me);
        if !rec.alive && j > 0 {
            eprintln!("lost at t={} (refusals {}): {:?}", t, rec.refusals, rec.fault);
            break;
        }
        let (x, v) = match rec.b.cartesian(t) {
            Ok((x, v)) => (f64v(x), f64v(v)),
            Err(e) => {
                eprintln!("readout refused at t={}: {:?}", t, e);
                break;
            }
        };
        let tau = proper_at(&p.u, t);
        let doll = p.u.rec(me).b.doll;
        let ctx = p.u.ctx();
        let mu_d = to_f64(ctx.tube_unit(me, doll).unwrap().mu);
        let (w, g, f) = local(x, v, mu_d);
        let un = g * w * v[0] / (v[0] * v[0] + v[1] * v[1]).sqrt();
        let r = (x[0] * x[0] + x[1] * x[1]).sqrt();
        let e_newton = 0.5 * (v[0] * v[0] + v[1] * v[1]) - mu_d / r;
        let e_inf = g * f.sqrt();
        if let Some((_pt, ptau, pvx, pf, pun)) = prev {
            let dt = (t - t_prev) as f64;
            let dtau = tau - ptau;
            work_gate += alpha * 0.5 * (pvx + v[0]) * dt;
            work_rel += 0.5 * (pf.sqrt() * pun + f.sqrt() * un) * alpha * dtau;
        }
        prev = Some((t as f64, tau, v[0], f, un));
        t_prev = t;
        // The register and its constraint.
        let (xsc, vsc) = {
            let rec = p.u.rec(me);
            let (x, v) = rec.b.cartesian(t).unwrap();
            (x, v)
        };
        let secs = ctx.secondaries(doll, t, me).unwrap();
        let u_p = force::field(&secs, xsc).unwrap().potential;
        let hd = force::kepler(xsc, vsc, ctx.tube_unit(me, doll).unwrap().mu).unwrap();
        let viol = match p.u.rec(me).ext {
            Some(e) => to_f64(e.pt_value().unwrap().sub(u_p.sub(hd).unwrap()).unwrap()),
            None => f64::NAN,
        };
        let rec = p.u.rec(me);
        let (pt, pt_exp, pt_carry) = rec.ext.map_or((0, 0, 0), |e| (e.pt, e.pt_exp, e.pt_carry));
        let gamma_pred = g0 * (alpha * tau).cosh() + u0n * (alpha * tau).sinh();
        rows.push(Row {
            t,
            tau,
            beta: (v[0] * v[0] + v[1] * v[1]).sqrt(),
            gamma: g,
            gamma_pred,
            gamma_exact_t: (1.0 + (alpha * t as f64) * (alpha * t as f64)).sqrt(),
            r,
            e_inf,
            work_gate,
            work_rel,
            e_newton,
            pt,
            pt_exp,
            pt_carry,
            viol,
            ve: rec.b.units.1,
            le: rec.b.units.0,
            lag: t - rec.b.event_time,
            refusals: rec.refusals,
            alive: rec.alive,
            step: rec.b.kick.len,
        });
        let last = rows.last().unwrap();
        eprintln!(
            "t={:>12} tau={:>11.0} beta={:.9} gamma={:>9.1} pred={:>9.1} gext={:>9.2} r={:>11.0} wg={:>10.3} wr={:>10.1} dEN={:>10.3} pt_exp={} pt={:>6} carry={:>6} viol={:>9.2e} ve={} lag={} ref={} step={}",
            last.t, last.tau, last.beta, last.gamma, last.gamma_pred, last.gamma_exact_t, last.r, last.work_gate, last.work_rel, last.e_newton, last.pt_exp, last.pt, last.pt_carry, last.viol, last.ve, last.lag, last.refusals, last.step
        );
    }
    println!("level,{}", level);
    println!("alpha_per_tick,{}", alpha);
    println!("mu,{}", mu);
    println!("gamma0,{}", g0);
    println!("u0n,{}", u0n);
    println!("t,tau,beta,gamma,gamma_pred,gamma_exact_t,r,e_inf,work_gate,work_rel,e_newton,pt,pt_exp,pt_carry,viol,ve,le,lag,refusals,alive,step");
    for r in &rows {
        println!(
            "{},{:.3},{:.12},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{},{},{},{:.3e},{},{},{},{},{},{}",
            r.t, r.tau, r.beta, r.gamma, r.gamma_pred, r.gamma_exact_t, r.r, r.e_inf, r.work_gate, r.work_rel, r.e_newton, r.pt, r.pt_exp, r.pt_carry, r.viol, r.ve, r.le, r.lag, r.refusals, r.alive as u8, r.step
        );
    }
}
