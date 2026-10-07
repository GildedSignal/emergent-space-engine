//! The kick's rebind path: shipped compile cost vs the law's jet (law.md "the jet
//! (exact offset plus stored derivatives), re-anchored"). Bench on the integer law.
//!
//! Modes: cost | scan | stream | negctl
use emergent_space::binding::{self, Rebinding};
use emergent_space::orbit::{Orbit, OrbitKey, Scalar, ShapeMemo};
use std::time::Instant;

fn s_f64(s: Scalar) -> f64 {
    s.significand() as f64 * 2f64.powi(s.exponent() as i32)
}
fn f64_s(x: f64) -> Scalar {
    Scalar::raw((x * 2f64.powi(62)) as i128, -62).expect("scalar")
}
fn key_of(p: f64, e: f64) -> OrbitKey {
    OrbitKey::bound(f64_s(p), (e * 2f64.powi(48)) as u64).expect("bound key")
}
#[derive(Clone, Copy)]
struct Inc {
    advance: f64,
    period: f64,
    proper: f64,
}
fn incs(o: &Orbit) -> Inc {
    Inc {
        advance: s_f64(o.advance().unwrap()),
        period: s_f64(o.period().unwrap()),
        proper: s_f64(o.proper_period().unwrap()),
    }
}
fn compile(p: f64, e: f64) -> Inc {
    incs(&Orbit::compile(key_of(p, e)).unwrap())
}

/// First-order jet anchored at (p0, e0); derivatives by central differences
/// (in production they are stored with the cycle per law.md; the bench pays compiles).
struct Jet {
    p0: f64,
    e0: f64,
    i0: Inc,
    d_dp: Inc,
    d_de: Inc,
    c_est: f64,
    compiles: u32,
}
fn arm(p: f64, e: f64, h: f64) -> Jet {
    let i0 = compile(p, e);
    let ip = compile(p * (1.0 + h), e);
    let im = compile(p * (1.0 - h), e);
    let ie = compile(p, e * (1.0 + h));
    let iem = compile(p, e * (1.0 - h));
    let sc = 1.0 / (2.0 * h);
    let d = |a: f64, b: f64| (a - b) * sc; // wrt ln of the axis
    let curv = |a: f64, b: f64, c: f64, base: f64| ((a - 2.0 * b + c) / base / (h * h)).abs() * 0.5;
    let c_est = curv(ip.advance, i0.advance, im.advance, i0.advance)
        .max(curv(ie.advance, i0.advance, iem.advance, i0.advance))
        .max(curv(ip.period, i0.period, im.period, i0.period))
        .max(curv(ie.period, i0.period, iem.period, i0.period))
        .max(curv(ip.proper, i0.proper, im.proper, i0.proper))
        .max(curv(ie.proper, i0.proper, iem.proper, i0.proper))
        .max(0.25);
    Jet {
        p0: p,
        e0: e,
        c_est,
        d_dp: Inc {
            advance: d(ip.advance, im.advance),
            period: d(ip.period, im.period),
            proper: d(ip.proper, im.proper),
        },
        d_de: Inc {
            advance: d(ie.advance, iem.advance),
            period: d(ie.period, iem.period),
            proper: d(ie.proper, iem.proper),
        },
        i0,
        compiles: 5,
    }
}
impl Jet {
    fn predict(&self, p: f64, e: f64) -> Inc {
        let dp = (p / self.p0).ln();
        let de = (e / self.e0).ln();
        Inc {
            advance: self.i0.advance + self.d_dp.advance * dp + self.d_de.advance * de,
            period: self.i0.period + self.d_dp.period * dp + self.d_de.period * de,
            proper: self.i0.proper + self.d_dp.proper * dp + self.d_de.proper * de,
        }
    }
    fn drift(&self, p: f64, e: f64) -> f64 {
        (p / self.p0).ln().abs().max((e / self.e0).ln().abs())
    }
}

fn rel(a: f64, b: f64) -> f64 {
    ((a - b) / b).abs()
}

// ---------------- mode: cost ----------------
fn mode_cost() {
    let p = 5.27e8; // B17's scaled weak-field scene
    let e = 0.1f64;
    let n = 400;
    // fresh-key compile (each kick moves e by a real kick size)
    let t0 = Instant::now();
    let mut acc = 0.0f64;
    for i in 0..n {
        let ei = e * (1.0 + 2.5e-6 * (i + 1) as f64);
        acc += compile(p, ei).advance;
    }
    let compile_ns = t0.elapsed().as_nanos() as f64 / n as f64;
    // memo hit (weak field: p-only kick keeps the (k, q=0) shape key)
    let mut memo = ShapeMemo::default();
    memo.get(key_of(p, e)).unwrap();
    let t0 = Instant::now();
    for i in 0..n {
        memo.get(key_of(p * (1.0 + 1e-6 * (i + 1) as f64), e)).unwrap();
    }
    let hit_ns = t0.elapsed().as_nanos() as f64 / n as f64;
    // memo miss = e kick
    let mut memo2 = ShapeMemo::default();
    memo2.get(key_of(p, e)).unwrap();
    let t0 = Instant::now();
    for i in 0..n {
        memo2.get(key_of(p, e * (1.0 + 1e-6 * (i + 1) as f64))).unwrap();
    }
    let miss_ns = t0.elapsed().as_nanos() as f64 / n as f64;
    // state readout (a derived position)
    let o = Orbit::compile(key_of(p, e)).unwrap();
    let tt = Scalar::raw(37, -40).unwrap();
    let t0 = Instant::now();
    for _ in 0..n {
        acc += o.state(tt).unwrap().psi as f64;
    }
    let state_ns = t0.elapsed().as_nanos() as f64 / n as f64;
    // Rebinding::from_state: the shipped rebind tail per kick (fit + compile + residual)
    let st = o.state(tt).unwrap();
    let units = (0i16, -24i16);
    let cart = binding::cartesian(st, 0, false, units).unwrap();
    let t0 = Instant::now();
    for i in 0..n {
        let t2 = Scalar::raw(37 + i as i128, -40).unwrap();
        let r = Rebinding::from_state(cart, t2, None).unwrap();
        acc += r.decoded_event().unwrap().position[0] as f64;
    }
    let rebind_ns = t0.elapsed().as_nanos() as f64 / n as f64;
    println!(
        "cost p={p:.3e} e={e} compile_ns={compile_ns:.0} memo_hit_ns={hit_ns:.0} memo_miss_ns={miss_ns:.0} state_ns={state_ns:.0} rebind_ns={rebind_ns:.0} acc={acc:.3e}"
    );
}

// ---------------- mode: scan ----------------
fn mode_scan() {
    let h = 1e-3;
    for (p, e) in [(5.27e8, 0.1), (5.27e8, 0.5), (5.27e8, 0.9), (50.0, 0.5), (20.0, 0.3)] {
        let j = arm(p, e, h);
        println!("scan p={p:.3e} e={e}");
        for &d in &[
            1e-9, 3e-9, 1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3,
        ] {
            let truth = compile(p, e * (1.0 + d));
            let pred = j.predict(p, e * (1.0 + d));
            let ea = rel(pred.advance, truth.advance);
            let et = rel(pred.period, truth.period);
            let eu = rel(pred.proper, truth.proper);
            let truthp = compile(p * (1.0 + d), e);
            let predp = j.predict(p * (1.0 + d), e);
            println!(
                "  drift={d:.0e} e-axis adv={ea:.3e} per={et:.3e} prop={eu:.3e} | p-axis adv={:.3e} per={:.3e} prop={:.3e}",
                rel(predp.advance, truthp.advance),
                rel(predp.period, truthp.period),
                rel(predp.proper, truthp.proper)
            );
        }
    }
}

// ---------------- mode: stream / negctl ----------------
#[derive(Clone, Copy, PartialEq, Debug)]
enum Kick {
    Corr,   // +eps on e each kick (coherent tide)
    Rand,   // +-eps random sign (oscillatory tide)
    Peters, // p shrinks, eps growing (inspiral row)
    Plane,  // both axes, coherent, eps-sized like a plane kick
}
fn mode_stream(kind: Kick, eps: f64, p0: f64, e0: f64, n: u32, seed: u64, floor: f64, use_jet: bool) {
    let mut state = 12345u64
        .wrapping_mul(seed)
        .wrapping_add(1442695040888963407);
    let mut rng = move || {
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        ((state >> 33) & 1) as i64 * 2 - 1
    };
    let mut p = p0;
    let mut e = e0;
    let mut jet = arm(p, e, 1e-3);
    let mut dstar = (floor / (1.5 * jet.c_est)).sqrt();
    let mut c_max_seen = jet.c_est;
    let mut compiles = jet.compiles as u64;
    let mut anchors = 1u64;
    let mut max_err = 0.0f64;
    let mut max_err_at = 0u64;
    let mut err_hist = Vec::new();
    for i in 1..=n {
        let (dp, de) = match kind {
            Kick::Corr => (0.0, eps),
            Kick::Rand => (0.0, eps * rng() as f64),
            Kick::Peters => {
                let grow = 1.0 + 6.0 * i as f64 / n as f64;
                (-(eps * grow), 0.0)
            }
            Kick::Plane => (eps * 0.6, eps),
        };
        p *= 1.0 + dp;
        e *= 1.0 + de;
        let truth = compile(p, e);
        let drift = jet.drift(p, e);
        let pred = if use_jet { jet.predict(p, e) } else { jet.i0 };
        let err = rel(pred.period, truth.period)
            .max(rel(pred.advance, truth.advance))
            .max(rel(pred.proper, truth.proper));
        err_hist.push(err);
        if err > max_err {
            max_err = err;
            max_err_at = i as u64;
        }
        if drift >= dstar {
            jet = arm(p, e, 1e-3);
            dstar = (floor / (1.5 * jet.c_est)).sqrt();
            c_max_seen = c_max_seen.max(jet.c_est);
            compiles += jet.compiles as u64;
            anchors += 1;
        }
    }
    println!(
        "stream kind={kind:?} eps={eps:.0e} p={p0:.3e} e={e0} n={n} jet={use_jet} floor={floor:.0e} dstar={dstar:.1e} compiles={compiles} anchors={anchors} compiles_per_kick={:.4} max_err={max_err:.3e} at={max_err_at}",
        compiles as f64 / n as f64
    );
    let mut q = err_hist.clone();
    q.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let at = |f: f64| q[(f * (n - 1) as f64) as usize];
    println!(
        "  err p50={:.3e} p90={:.3e} p99={:.3e} max={:.3e}",
        at(0.5),
        at(0.9),
        at(0.99),
        q[n as usize - 1]
    );
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    match a[1].as_str() {
        "cost" => mode_cost(),
        "scan" => mode_scan(),
        "stream" | "negctl" => {
            let kind = match a[2].as_str() {
                "corr" => Kick::Corr,
                "rand" => Kick::Rand,
                "peters" => Kick::Peters,
                "plane" => Kick::Plane,
                _ => panic!("kind"),
            };
            let eps: f64 = a[3].parse().unwrap();
            let p: f64 = a[4].parse().unwrap();
            let e: f64 = a[5].parse().unwrap();
            let n: u32 = a[6].parse().unwrap();
            let seed: u64 = a[7].parse().unwrap();
            let floor: f64 = a.get(8).map(|s| s.parse().unwrap()).unwrap_or(1e-6);
            let jet = a[1] == "stream";
            mode_stream(kind, eps, p, e, n, seed, floor, jet);
        }
        _ => panic!("mode"),
    }
}
