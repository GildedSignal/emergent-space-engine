//! Probe 20261010-1407-inversion-5c2a: does the adopted phase-neighbour certificate
//! (lab gold 20261006-0346-taleb-09b5; build spec lab/lenses/b-coorbital-cert.md) survive
//! multi-population concentration? Scenes: two fleets, each narrow in period (any concentration
//! trigger that fires on the gold's co-orbital belt fires on each fleet), whose orbits cross
//! only through eccentricity spread; RETRO mirrors one fleet (counter-orbiting).
//!
//! Truth for CTRL/FLEET2 is the crate's own `truth_pair`, untouched. RETRO uses a copied
//! march with a y-mirrored relative state (mirror preserves rmin, so the same Lipschitz bounds
//! hold) and a bisection refine. Output: one JSON object per line.

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::f64::consts::TAU;

const THREADS: usize = 4;

struct Fleet {
    n: usize,
    a_lo: f64,
    a_hi: f64,
    sigma_e: f64,
    mirror: bool,
}

fn sample(f: &Fleet, rng: &mut Rng, out: &mut Vec<Body>, groups: &mut Vec<u32>, mirrors: &mut Vec<bool>, g: u32) {
    for _ in 0..f.n {
        let a = f.a_lo + (f.a_hi - f.a_lo) * rng.f64();
        let u = rng.f64();
        let e = (f.sigma_e * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.5);
        let pom = TAU * rng.f64();
        let lam = TAU * rng.f64();
        out.push(Body::new(a, e, pom, lam));
        groups.push(g);
        mirrors.push(f.mirror);
    }
}

/// Mirrored relative state: exactly one Kepler solution's y-image per mirrored body.
fn rel2(bi: &Body, bj: &Body, mi: bool, mj: bool, t: f64, evals: &mut u64) -> ([f64; 2], [f64; 2]) {
    *evals += 1;
    let s = |b: &Body, m: bool| -> [f64; 4] {
        let s = b.state(t);
        if m { [s[0], -s[1], s[2], -s[3]] } else { s }
    };
    let (si, sj) = (s(bi, mi), s(bj, mj));
    ([si[0] - sj[0], si[1] - sj[1]], [si[2] - sj[2], si[3] - sj[3]])
}

fn dot2(a: [f64; 2], b: [f64; 2]) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}

fn norm2(a: [f64; 2]) -> f64 {
    dot2(a, a).sqrt()
}

/// truth_pair's march, mirrored; refine by bisection on the sign of d(r·v).
#[allow(clippy::too_many_arguments)]
fn truth_pair2(bi: &Body, bj: &Body, mi: bool, mj: bool, rho: f64, t_end: f64, out: &mut Vec<(f64, f64)>, st: &mut TruthStats) {
    let rmin = bi.rmin().min(bj.rmin());
    let a_glob = 1.0 / (bi.rmin() * bi.rmin()) + 1.0 / (bj.rmin() * bj.rmin());
    let dcap = 0.5f64.min(rmin);
    let rseg = (rmin * rmin - 0.25 * dcap * dcap).sqrt();
    let om = (2.0 / (rseg * rseg * rseg)).sqrt();
    let mut t = 0.0;
    let (mut r, mut v) = rel2(bi, bj, mi, mj, t, &mut st.evals);
    let mut g = dot2(r, v);
    while t < t_end {
        let d = norm2(r);
        let tn = if d > 2.0 * rho {
            st.steps += 1;
            // safe_step inlined (same bounds; mirror preserves rmin)
            let d0 = d;
            let v0 = norm2(v);
            let rv = g;
            let vv = dot2(v, v);
            let lb = |h: f64| -> f64 {
                let tau = if vv > 0.0 { (-rv / vv).clamp(0.0, h) } else { 0.0 };
                let ml = norm2([r[0] + v[0] * tau, r[1] + v[1] * tau]);
                let lb1 = ml - 0.5 * a_glob * h * h;
                let x = om * h;
                let u = d0 * x.cosh() + (v0 / om) * x.sinh();
                let lb2 = if u <= dcap { ml - (u - d0 - v0 * h) } else { f64::NEG_INFINITY };
                lb1.max(lb2)
            };
            let mut h = 1.0f64;
            while lb(h) < 1.5 * rho && h > 1e-13 {
                h *= 0.5;
            }
            t + h
        } else {
            st.steps += 1;
            st.fine += 1;
            t + (0.25 * rho / norm2(v).max(1e-12)).min(0.05)
        };
        let (rn, vn) = rel2(bi, bj, mi, mj, tn, &mut st.evals);
        let gn = dot2(rn, vn);
        if d <= 2.0 * rho && g < 0.0 && gn >= 0.0 {
            let (mut lo, mut hi) = (t, tn);
            for _ in 0..80 {
                let mid = 0.5 * (lo + hi);
                let (rm, vm) = rel2(bi, bj, mi, mj, mid, &mut st.evals);
                if dot2(rm, vm) < 0.0 { lo = mid } else { hi = mid }
            }
            let tm = 0.5 * (lo + hi);
            let (rm, _) = rel2(bi, bj, mi, mj, tm, &mut st.evals);
            let dm = norm2(rm);
            if dm < rho && tm > 0.0 && tm < t_end {
                out.push((tm, dm));
            }
        }
        t = tn;
        r = rn;
        v = vn;
        g = gn;
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let scene = args.get(1).map(|s| s.as_str()).unwrap_or("ctrl").to_string();
    let rho = 1e-3;
    let orbits = 50.0f64;
    let t_end = orbits * TAU;
    let (bodies, groups, mirrors, seed) = match scene.as_str() {
        "ctrl" => {
            let (mut b, mut g, mut m) = (Vec::new(), Vec::new(), Vec::new());
            sample(&Fleet { n: 300, a_lo: 1.0, a_hi: 1.0001, sigma_e: 3e-4, mirror: false }, &mut Rng(20261010), &mut b, &mut g, &mut m, 0);
            (b, g, m, 20261010u64)
        }
        "fleet2" => {
            let (mut b, mut g, mut m) = (Vec::new(), Vec::new(), Vec::new());
            let mut rng = Rng(20261011);
            sample(&Fleet { n: 300, a_lo: 1.0000, a_hi: 1.0002, sigma_e: 0.04, mirror: false }, &mut rng, &mut b, &mut g, &mut m, 0);
            sample(&Fleet { n: 300, a_lo: 1.0600, a_hi: 1.0602, sigma_e: 0.04, mirror: false }, &mut rng, &mut b, &mut g, &mut m, 1);
            (b, g, m, 20261011)
        }
        "retro" => {
            let (mut b, mut g, mut m) = (Vec::new(), Vec::new(), Vec::new());
            let mut rng = Rng(20261012);
            sample(&Fleet { n: 300, a_lo: 1.0000, a_hi: 1.0002, sigma_e: 0.04, mirror: false }, &mut rng, &mut b, &mut g, &mut m, 0);
            sample(&Fleet { n: 300, a_lo: 1.0600, a_hi: 1.0602, sigma_e: 0.04, mirror: true }, &mut rng, &mut b, &mut g, &mut m, 1);
            (b, g, m, 20261012)
        }
        _ => panic!("unknown scene"),
    };
    let n = bodies.len();
    // Radial overlap with 2ρ margin (the crate's count_radial rule): a pair whose [rmin, rmax]
    // intervals are disjoint by more than 2ρ cannot produce a minimum below ρ.
    let mut pairs = Vec::new();
    for i in 0..n {
        for j in (i + 1)..n {
            let (lo_i, hi_i) = (bodies[i].rmin(), bodies[i].rmax());
            let (lo_j, hi_j) = (bodies[j].rmin(), bodies[j].rmax());
            if lo_i <= hi_j + 2.0 * rho && lo_j <= hi_i + 2.0 * rho {
                pairs.push((i as u32, j as u32));
            }
        }
    }
    let t0 = std::time::Instant::now();
    let chunks: Vec<std::ops::Range<usize>> = (0..THREADS).map(|k| (k * pairs.len() / THREADS)..((k + 1) * pairs.len() / THREADS)).collect();
    let parts = std::thread::scope(|s| {
        let handles: Vec<_> = chunks.into_iter().map(|r| {
            let bodies = &bodies;
            let mirrors = &mirrors;
            let pairs = &pairs;
            s.spawn(move || {
                let mut out: Vec<(u32, u32, f64, f64)> = Vec::new();
                let mut st = TruthStats::default();
                let mut tmp = Vec::new();
                for &(i, j) in &pairs[r] {
                    tmp.clear();
                    let (mi, mj) = (mirrors[i as usize], mirrors[j as usize]);
                    if mi || mj {
                        truth_pair2(&bodies[i as usize], &bodies[j as usize], mi, mj, rho, t_end, &mut tmp, &mut st);
                    } else {
                        truth_pair(&bodies[i as usize], &bodies[j as usize], rho, t_end, &mut tmp, &mut st);
                    }
                    out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
                }
                (out, st)
            })
        }).collect();
        handles.into_iter().map(|h| h.join().unwrap()).collect::<Vec<_>>()
    });
    let mut enc = Vec::new();
    let mut st = TruthStats::default();
    for (o, s) in parts {
        enc.extend(o);
        st.add(&s);
    }
    enc.sort_by(|a, b| a.0.cmp(&b.0).then(a.1.cmp(&b.1)).then(a.2.total_cmp(&b.2)));
    println!("{{\"ev\":\"meta\",\"scene\":\"{}\",\"seed\":{},\"n\":{},\"rho\":{:e},\"orbits\":{},\"t_end\":{:.17e},\"pairs\":{},\"enc\":{},\"steps\":{},\"fine\":{},\"evals\":{},\"wall_s\":{:.3}}}",
        scene, seed, n, rho, orbits, t_end, pairs.len(), enc.len(), st.steps, st.fine, st.evals, t0.elapsed().as_secs_f64());
    for (i, b) in bodies.iter().enumerate() {
        println!("{{\"ev\":\"body\",\"i\":{},\"g\":{},\"a\":{:.17e},\"e\":{:.17e},\"pom\":{:.17e},\"period\":{},\"tp\":{},\"mirror\":{}}}",
            i, groups[i], b.a, b.e, b.pom, b.period, b.tp, mirrors[i]);
    }
    for &(i, j, t, d) in &enc {
        println!("{{\"ev\":\"enc\",\"i\":{},\"j\":{},\"t\":{:.17e},\"d\":{:.17e}}}", i, j, t, d);
    }
    println!("{{\"ev\":\"done\"}}");
}
