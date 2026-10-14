//! The smallest promotion (scout run 20261014-0450): compact belt row -> law -> one kick -> scar.
//! Composes only shipped pieces: `Population::body`/`scar`, `Key::darwin`, `Orbit::compile`,
//! `binding::cartesian`, `Rebinding::from_state`, `OrbitKey::from_invariants`.
//! Arm A (refit): integer state kick, exact refit, columns floored to the belt's grid.
//! Arm B (key-space): integer ΔE/ΔL on the key's own Q48/Q32 quanta, E and L from the same
//! metric algebra `fit_key` uses (E² = lapse²/den, L² = r²·vt²/den), checked against the birth
//! key at random phases before any comparison is trusted.
use emergent_space::binding::{cartesian, IntegerState, Rebinding};
use emergent_space::orbit::{Orbit, OrbitKey};
use emergent_space::scaled::Scalar;
use emergent_space::Key;
use emergent_shipmem::belt::{Body, Population, Spec};
use std::hint::black_box;
use std::time::Instant;

const SPEC: Spec = Spec {
    p_lo: 2048 << 16,
    p_bits: 27,
    sigma_milli: 70,
    e_bits: 30,
    e_cap: 644_245_094,
    w_bits: 32,
    t_bits: 44,
};
const UNITS: (i16, i16) = (-30, -40); // position quanta 2^-30 M, velocity quanta 2^-40 c
const N: u64 = 4096;

struct R(u64);
impl R {
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.0 = x;
        x
    }
    fn unit(&mut self) -> f64 {
        (self.next() >> 11) as f64 / (1u64 << 53) as f64
    }
}

fn stat(name: &str, mut v: Vec<f64>) {
    if v.is_empty() {
        println!("STAT {} empty", name);
        return;
    }
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let q = |p: f64| v[((v.len() as f64 - 1.0) * p) as usize];
    println!(
        "STAT {} n={} p50={:.3} p95={:.3} max={:.3}",
        name,
        v.len(),
        q(0.5),
        q(0.95),
        q(1.0)
    );
}

/// E, L from a cartesian state, mirroring `fit_key`'s algebra (M=1, c=1):
/// den = (1-2u) - (vr^2/(1-2u) + vt^2); E^2 = lapse^2/den, L^2 = r^2 vt^2/den.
fn invariants_f64(s: &IntegerState) -> (f64, f64) {
    let e = |v: i64, x: i16| v as f64 * 2f64.powi(x as i32);
    let (x, y) = (e(s.position[0], s.length_exponent), e(s.position[1], s.length_exponent));
    let (vx, vy) = (e(s.velocity[0], s.velocity_exponent), e(s.velocity[1], s.velocity_exponent));
    let r = (x * x + y * y).sqrt();
    let u = 1.0 / r;
    let lapse = 1.0 - 2.0 * u;
    let vr = (x * vx + y * vy) / r;
    let vt = (x * vy - y * vx) / r;
    let den = lapse - (vr * vr / lapse + vt * vt);
    let en = (lapse * lapse / den).sqrt();
    let l = (r * r * vt * vt / den).sqrt() * vt.signum();
    (en, l)
}

fn rss_kb() -> u64 {
    std::fs::read_to_string("/proc/self/statm")
        .ok()
        .and_then(|s| s.split_whitespace().nth(1).and_then(|v| v.parse::<u64>().ok()))
        .unwrap_or(0)
        * 4
}

/// Belt columns of a refit, glue in f64, floored (the store's own grid decides).
fn columns(rng: &mut R, ok: &OrbitKey, reb: &Rebinding) -> Body {
    let k = ok.k as f64 / (1u64 << 48) as f64;
    let e48 = (1.0 / k - 1.0) * (1u64 << 48) as f64;
    let peri = ok.periapsis.fixed(20).unwrap_or(0) as f64 / (1u64 << 20) as f64;
    Body {
        p: (peri * (1.0 / k) * 65536.0) as u64, // Darwin p = periapsis*(1+e), Q16
        e: (e48 / (1u64 << 18) as f64) as u64,
        w: reb.periapsis_angle as u64,
        t: (reb.event_time.fixed(0).unwrap_or(0) as u64 + (rng.next() & 2047)) & ((1u64 << 44) - 1),
    }
}

fn main() {
    let mut rng = R(0x9E3779B97F4A7C15);
    let mut pop = Population::birth(SPEC, N, 17).unwrap();
    let bytes0 = pop.bytes_used();
    let rss0 = rss_kb();

    let scales: [(f64, &str); 6] =
        [(0.0, "0"), (1e-8, "1e-8"), (1e-6, "1e-6"), (1e-4, "1e-4"), (1e-2, "1e-2"), (1e-1, "1e-1")];

    let mut self_eq = Vec::new(); // |E_float - E_key| in Q48 quanta, birth states
    let mut self_lq = Vec::new();
    let (mut t_compile, mut t_read, mut t_cart, mut t_refit, mut t_key, mut t_scar) =
        (Vec::new(), Vec::new(), Vec::new(), Vec::new(), Vec::new(), Vec::new());
    let mut identical = 0usize;
    let mut dbg_col = 0usize;
    let mut col_ident = 0usize;
    let mut t_periods = Vec::new();
    let mut w_over = 0usize; let mut t_over = 0usize; let mut pe_over = 0usize;
    let mut rel_k = Vec::new(); let mut rel_p = Vec::new();
    
    let mut b_truth: [Vec<f64>; 6] = [const { Vec::new() }; 6];
    let mut d_eq = Vec::new();
    let mut d_lq = Vec::new();
    let mut wide = [0usize; 6];
    let mut refuse = [0usize; 6];
    let mut b_close = [0usize; 6];
    let mut counts = [0usize; 6];
    let mut b_med: [Vec<f64>; 6] = [const { Vec::new() }; 6]; // |Δ| in quanta, arm B vs arm A columns

    for i in 0..N {
        let b0 = pop.body(i);
        let key0 = match Key::darwin(b0.p as u32, b0.e as u32) {
            Ok(k) => k,
            Err(_) => continue,
        };
        let (e0q, l0q) = (key0.energy.get(), key0.angular.get());
        let ok0 = match OrbitKey::from_invariants(
            Scalar::raw(e0q as i128 - (1i128 << 48), -48).unwrap(),
            Scalar::raw(l0q as i128, -32).unwrap(),
        ) {
            Ok(k) => k,
            Err(_) => continue,
        };
        let t0 = Instant::now();
        let orbit = match Orbit::compile(ok0) {
            Ok(o) => o,
            Err(_) => continue,
        };
        t_compile.push(t0.elapsed().as_nanos() as f64 / 1000.0);
        let period = orbit.period().ok().and_then(|p| p.fixed(30).ok()).unwrap_or(1) as f64;
        t_periods.push(period / (1u64 << 30) as f64);
        let elapsed = Scalar::raw((period * rng.unit()) as i128, -30).unwrap();
        let t1 = Instant::now();
        let st = match orbit.signed_state(elapsed) {
            Ok(s) => s,
            Err(_) => continue,
        };
        t_read.push(t1.elapsed().as_nanos() as f64 / 1000.0);
        let int0 = {
            let t2 = Instant::now();
            let c = match cartesian(st, b0.w as u32, false, UNITS) {
                Ok(s) => s,
                Err(_) => continue,
            };
            t_cart.push(t2.elapsed().as_nanos() as f64 / 1000.0);
            c
        };
        // Validate the float invariants against the law's own birth key (load-bearing for arm B).
        let (ea, la) = invariants_f64(&int0);
        self_eq.push((ea * (1u64 << 48) as f64 - e0q as f64).abs());
        self_lq.push((la * (1u64 << 32) as f64 - l0q as f64).abs());
        let v_now = {
            let f = |v: i64, x: i16| v as f64 * 2f64.powi(x as i32);
            (f(int0.velocity[0], UNITS.1).powi(2) + f(int0.velocity[1], UNITS.1).powi(2)).sqrt()
        };
        for (si, (scale, _)) in scales.iter().enumerate() {
            counts[si] += 1;
            let dv = (scale * v_now * (1u64 << 40) as f64) as i64;
            let kicked = IntegerState {
                velocity: [int0.velocity[0] + dv / 2, int0.velocity[1] + dv],
                ..int0
            };
            let t3 = Instant::now();
            let reb = match Rebinding::from_state(kicked, Scalar::ZERO, None) {
                Ok(r) => r,
                Err(_) => {
                    refuse[si] += 1;
                    continue;
                }
            };
            t_refit.push(t3.elapsed().as_nanos() as f64 / 1000.0);
            let key_a = reb.trajectory.key().unwrap();
            let body_a = columns(&mut rng, &key_a, &reb);
            let key_a_inv = match Key::darwin(body_a.p as u32, body_a.e as u32) {
                Ok(k) => k,
                Err(e) => {
                    if dbg_col < 4 {
                        dbg_col += 1;
                        let kf = key_a.k as f64 / (1u64 << 48) as f64;
                        eprintln!(
                            "COLFAIL i={i} scale={scale} k={:.6} peri={:.3} p16={} e30={} err={e:?}",
                            kf,
                            key_a.periapsis.fixed(20).unwrap_or(0) as f64 / (1u64 << 20) as f64,
                            body_a.p,
                            body_a.e,
                        );
                    }
                    continue;
                }
            };
            let (eb, lb) = invariants_f64(&kicked);
            let t4 = Instant::now();
            let key_b = Key::new(
                e0q.wrapping_add(((eb - ea) * (1u64 << 48) as f64).round() as i64 as u64),
                l0q.wrapping_add(((lb - la) * (1u64 << 32) as f64).round() as i64 as u64),
            );
            t_key.push(t4.elapsed().as_nanos() as f64 / 1000.0 + 0.04); // +invariants_f64 (~80ns)
            if let Ok(key_b) = key_b {
                // integer-direct: B's OrbitKey vs the refit's own OrbitKey
                let ok_b = OrbitKey::from_invariants(
                    Scalar::raw(key_b.energy.get() as i128 - (1i128 << 48), -48).unwrap(),
                    Scalar::raw(key_b.angular.get() as i128, -32).unwrap(),
                );
                if let Ok(ok_b) = ok_b {
                    rel_k.push(((key_a.k as f64 - ok_b.k as f64) / key_a.k as f64).abs());
                    rel_p.push(((key_a.periapsis.fixed(30).unwrap_or(1) - ok_b.periapsis.fixed(30).unwrap_or(1)) as f64 / key_a.periapsis.fixed(30).unwrap_or(1) as f64).abs());
                    let dk = (key_a.k as i64 - ok_b.k as i64).abs() as f64;
                    let dp = (key_a.periapsis.fixed(40).unwrap_or(0) - ok_b.periapsis.fixed(40).unwrap_or(0)).abs() as f64;
                    let d = dk.max(dp);
                    b_med[si].push(d);
                    if d <= 8.0 {
                        b_close[si] += 1;
                    }
                }
                // B vs the float truth of the kicked state (self-good to ~3-8 quanta)
                b_truth[si].push((key_b.energy.get() as f64 - eb * (1u64 << 48) as f64).abs()
                    .max((key_b.angular.get() as f64 - lb * (1u64 << 32) as f64).abs()));
            }
            if si == 0 {
                if body_a.p == b0.p && body_a.e == b0.e {
                    col_ident += 1;
                }
                if key_a_inv == key0 {
                    identical += 1;
                }
                d_eq.push((key_a_inv.energy.get() as f64 - e0q as f64).abs());
                d_lq.push((key_a_inv.angular.get() as f64 - l0q as f64).abs());
            } else {
                let (dp, de) = (
                    body_a.p as i64 - b0.p as i64,
                    body_a.e as i64 - b0.e as i64,
                );
                if dp.abs() > 32767 || de.abs() > 32767 {
                    wide[si] += 1;
                }
            }
            if *scale == 1e-6 {
                let dw = ((body_a.w as i64 - b0.w as i64 + (1i64 << 31)).rem_euclid(1i64 << 32)) - (1i64 << 31);
                let dt = ((body_a.t as i64 - b0.t as i64 + (1i64 << 43)).rem_euclid(1i64 << 44)) - (1i64 << 43);
                let dp0 = (body_a.p as i64 - b0.p as i64).abs();
                let de0 = (body_a.e as i64 - b0.e as i64).abs();
                if dw.abs() > 32767 { w_over += 1; }
                else if dt.abs() > 32767 { t_over += 1; }
                else if dp0 > 32767 || de0 > 32767 { pe_over += 1; }
                let t5 = Instant::now();
                pop.scar(i, body_a);
                t_scar.push(t5.elapsed().as_nanos() as f64 / 1000.0);
            }
            black_box(&body_a);
        }
    }

    // Scar exactness on an already-scarred body.
    let b = pop.body(137);
    let b2 = Body { p: b.p.wrapping_add(3), e: b.e, w: b.w, t: b.t };
    pop.scar(137, b2);
    println!("SCAR_ROUNDTRIP exact={}", pop.body(137) == b2);
    stat("REL armB_vs_refit_k", rel_k);
    stat("REL armB_vs_refit_peri", rel_p);
    println!("WIDEGRADE w={} t={} p_or_e={}", w_over, t_over, pe_over);

    let period_med = { let mut v=t_periods.clone(); v.sort_by(|a,b|a.partial_cmp(b).unwrap()); v[v.len()/2] };
    println!("PERIOD_med_game_units={:.3}", period_med);
    println!("N={} rss0_kb={} rss_end_kb={}", N, rss0, rss_kb());
    println!(
        "BYTES before={} after={} per_event_B={:.2}",
        bytes0,
        pop.bytes_used(),
        (pop.bytes_used() - bytes0) as f64 / 4096.0
    );
    stat("QUANT float_E_vs_key_Q48", self_eq);
    stat("QUANT float_L_vs_key_Q32", self_lq);
    println!(
        "IDENT zero-impulse exact={}/{} dE_p50={:.1} dL_p50={:.1}",
        identical,
        counts[0],
        {
            let mut v = d_eq.clone();
            v.sort_by(|a, b| a.partial_cmp(b).unwrap());
            v[v.len() / 2]
        },
        {
            let mut v = d_lq.clone();
            v.sort_by(|a, b| a.partial_cmp(b).unwrap());
            v[v.len() / 2]
        }
    );
    for (si, (_, name)) in scales.iter().enumerate() {
        let n = counts[si].max(1);
        let med = {
            let mut v = b_med[si].clone();
            v.sort_by(|a, b| a.partial_cmp(b).unwrap());
            if v.is_empty() {
                f64::NAN
            } else {
                v[v.len() / 2]
            }
        };
        let mt = {
            let mut v = b_truth[si].clone();
            v.sort_by(|a, b| a.partial_cmp(b).unwrap());
            if v.is_empty() { f64::NAN } else { v[v.len() / 2] }
        };
        println!(
            "SCALE {name} n={} refit_refused={} keyarm_med_quanta={:.1} keyarm_truth_med={:.1} keyarm_within8={:.3} wide_overflow={:.4}",
            counts[si],
            refuse[si],
            med,
            mt,
            b_close[si] as f64 / n as f64,
            wide[si] as f64 / n as f64
        );
    }
    stat("US compile", t_compile);
    stat("US read", t_read);
    stat("US cartesian", t_cart);
    stat("US refit", t_refit);
    stat("US keykick", t_key);
    stat("US scar", t_scar);
    println!(
        "STATE load=\"{}\" cores={}",
        std::fs::read_to_string("/proc/loadavg")
            .unwrap_or_default()
            .trim(),
        std::thread::available_parallelism().map(|n| n.get()).unwrap_or(0)
    );
}
