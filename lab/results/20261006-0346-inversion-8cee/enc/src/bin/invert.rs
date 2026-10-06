//! Inversion probe (run 20261006-0346): the r8 verification lineage never ran e > 0.5 (the belt
//! generator caps it) and never ran a fleet formation. Scenes here sit outside that space; the
//! crate's own truth (radial pairs, conservative advancement) judges completeness, and a dense
//! fixed-grid scan (minima by comparison + golden refine, Halley states — no sign-change brackets,
//! no Newton-on-g) is a third opinion that shares no decision rule with method or truth.

use emergent_encounters::belt::{make_belt, Rng, Spec};
use emergent_encounters::kepler::{rel, Body, TICKS};
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{cone_pairs, is_candidate, norm, radial_pairs, sections};
use emergent_encounters::truth::{truth_pair, TruthStats};

use emergent_encounters::par_chunks;
use std::f64::consts::TAU;
use std::time::Instant;

const THREADS: usize = 4;
const SAFETY: f64 = 1.1;
type Enc = (u32, u32, f64, f64);

fn scene(name: &str) -> (Vec<Body>, f64, f64) {
    let mut r = Rng(0xABCD98765432u64 ^ name.bytes().fold(0u64, |a, b| a.wrapping_add(b as u64)));
    let un = |r: &mut Rng| r.f64();
    match name {
        // Instrument control: inside the frozen verification space (e <= 0.5).
        "ctrl-coorbital" => {
            let sp = Spec {
                name: "c".into(),
                n: 300,
                sigma_e: 3e-4,
                rho: 1e-3,
                a_lo: 1.0,
                a_hi: 1.0001,
                keys: 0,
                seed: 20261001 + 9,
                orbits: 50.0,
            };
            (make_belt(&sp), sp.rho, sp.orbits * TAU)
        }
        "ctrl-narrow" => {
            let sp = Spec {
                name: "c".into(),
                n: 400,
                sigma_e: 0.025,
                rho: 3e-3,
                a_lo: 1.0,
                a_hi: 1.0025,
                keys: 0,
                seed: 20261001 + 8,
                orbits: 20.0,
            };
            (make_belt(&sp), sp.rho, sp.orbits * TAU)
        }
        // Outside the space: high eccentricity, apsides aligned (crossings near common periapsis,
        // maximum curvature) vs random.
        "highe-align" | "highe-rand" => {
            let n = 240;
            let b: Vec<Body> = (0..n)
                .map(|_| {
                    let a = 1.0 + 0.2 * un(&mut r);
                    let e = 0.60 + 0.35 * un(&mut r);
                    let pom = if name == "highe-align" { 0.0 } else { TAU * un(&mut r) };
                    let lam = TAU * un(&mut r);
                    Body::new(a, e, pom, lam)
                })
                .collect();
            (b, 1e-3, 10.0 * TAU)
        }
        // The fleet: nearly identical orbits, aligned apsides (a formation), spread or clustered.
        "formation" | "wall" => {
            let n = 240;
            let b: Vec<Body> = (0..n)
                .map(|_| {
                    let a = 1.0 + (un(&mut r) - 0.5) * 8e-4;
                    let e = 0.02 * un(&mut r);
                    let pom = 0.0;
                    let lam = if name == "formation" { TAU * un(&mut r) } else { (un(&mut r) - 0.5) * 0.6 };
                    Body::new(a, e, pom, lam)
                })
                .collect();
            (b, 1e-3, 20.0 * TAU)
        }
        _ => panic!("unknown scene"),
    }
}

fn dist(bi: &Body, bj: &Body, t: f64) -> f64 {
    let (rr, _, _) = rel(bi, bj, t, true);
    norm(rr)
}

/// Golden-section minimum of the distance on [a, b] (comparison only).
fn golden(bi: &Body, bj: &Body, a: f64, b: f64, evals: &mut u64) -> (f64, f64) {
    let (mut lo, mut hi) = (a, b);
    let gr = 0.6180339887498949;
    let mut c = hi - gr * (hi - lo);
    let mut d = lo + gr * (hi - lo);
    let mut fc = dist(bi, bj, c);
    let mut fd = dist(bi, bj, d);
    *evals += 2;
    for _ in 0..100 {
        if fc < fd {
            hi = d;
            d = c;
            fd = fc;
            c = hi - gr * (hi - lo);
            fc = dist(bi, bj, c);
        } else {
            lo = c;
            c = d;
            fc = fd;
            d = lo + gr * (hi - lo);
            fd = dist(bi, bj, d);
        }
        *evals += 1;
        if hi - lo < 1e-13 * (1.0 + lo.abs()) {
            break;
        }
    }
    let t = 0.5 * (lo + hi);
    (t, dist(bi, bj, t))
}

/// Dense fixed-grid scan: every grid point inside a sub-rho dip; minima by comparison, golden refine.
fn dense_minima(bi: &Body, bj: &Body, rho: f64, t_end: f64, out: &mut Vec<(f64, f64)>, evals: &mut u64) {
    let vpi = ((1.0 + bi.e) / (bi.a * (1.0 - bi.e))).sqrt();
    let vpj = ((1.0 + bj.e) / (bj.a * (1.0 - bj.e))).sqrt();
    let h = rho / (2.0 * (vpi + vpj));
    let mut tm1 = 0.0;
    let mut dm1 = dist(bi, bj, 0.0);
    let mut t0 = h;
    let mut d0 = dist(bi, bj, h);
    *evals += 2;
    let mut q = 2u64;
    while t0 < t_end {
        let t = h * q as f64;
        let dnow = if t < t_end { dist(bi, bj, t) } else { f64::INFINITY };
        *evals += 1;
        if d0 <= dm1 && d0 < dnow && d0 < 2.0 * rho {
            let (tmin, dmin) = golden(bi, bj, tm1, (h * (q + 1) as f64).min(t_end), evals);
            if dmin < rho && tmin > 0.0 && tmin < t_end {
                out.push((tmin, dmin));
            }
        }
        tm1 = t0;
        dm1 = d0;
        t0 = t;
        d0 = dnow;
        q += 1;
    }
}

/// (missed, false) of `a` against `b`, both within margins, tolerance tol on t.
fn diff(a: &[Enc], b: &[Enc], t_end: f64, tol: f64) -> (Vec<Enc>, Vec<Enc>) {
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;
    let mut missed = Vec::new();
    for e in a.iter().filter(|e| inside(e.2)) {
        if !b.iter().any(|f| f.0 == e.0 && f.1 == e.1 && (f.2 - e.2).abs() < tol) {
            missed.push(*e);
        }
    }
    let mut false_ = Vec::new();
    for e in b.iter().filter(|e| inside(e.2)) {
        if !a.iter().any(|f| f.0 == e.0 && f.1 == e.1 && (f.2 - e.2).abs() < tol) {
            false_.push(*e);
        }
    }
    (missed, false_)
}

fn run(name: &str, dense_stride: usize, dense_orbits: f64) {
    let t_wall = Instant::now();
    let (b, rho, t_end) = scene(name);
    let n = b.len();

    let rp = radial_pairs(&b, rho);
    let t0 = Instant::now();
    let cs = cone_pairs(&b, rho);
    let cone_s = t0.elapsed().as_secs_f64();
    // Radial candidates the cone rejects: a candidate-level miss source.
    let radial_not_cone: Vec<_> = rp.iter().filter(|&&(i, j)| !is_candidate(&b[i as usize], &b[j as usize], rho)).cloned().collect();

    let t1 = Instant::now();
    let truth_parts = par_chunks(rp.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = TruthStats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &rp[r] {
            tmp.clear();
            truth_pair(&b[i as usize], &b[j as usize], rho, t_end, &mut tmp, &mut st);
            out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, st)
    });
    let mut truth = Vec::new();
    let mut tst = TruthStats::default();
    for (o, s) in truth_parts {
        truth.extend(o);
        tst.add(&s);
    }
    let truth_s = t1.elapsed().as_secs_f64();

    let t2 = Instant::now();
    let meth_parts = par_chunks(cs.pairs.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = Stats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &cs.pairs[r] {
            tmp.clear();
            pair_events(&b[i as usize], &b[j as usize], rho, SAFETY, 0.0, t_end, &mut st, &mut tmp);
            out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, st)
    });
    let mut meth = Vec::new();
    let mut mst = Stats::default();
    for (o, s) in meth_parts {
        meth.extend(o);
        mst.add(&s);
    }
    let meth_s = t2.elapsed().as_secs_f64();

    let inside_dn = |t: f64| t > 0.05 && t < (dense_orbits * TAU) - 0.05;
    let (missed, false_, matched) = {
        let (m, f) = diff(&truth, &meth, t_end, 1e-3);
        let inside = |t: f64| t > 0.05 && t < t_end - 0.05;
        let matched = truth.iter().filter(|e| inside(e.2)).count() - m.len();
        (m, f, matched)
    };
    let outside_cone = truth.iter().filter(|e| !is_candidate(&b[e.0 as usize], &b[e.1 as usize], rho)).count();
    if !radial_not_cone.is_empty() {
        for &(i, j) in radial_not_cone.iter().take(12) {
            let (bi, bj) = (&b[i as usize], &b[j as usize]);
            let mut best = (0.0f64, f64::INFINITY);
            let mut q = 0u64;
            while q as f64 * 0.01 < t_end {
                let t = q as f64 * 0.01;
                let d = dist(bi, bj, t);
                if d < best.1 { best = (t, d); }
                q += 1;
            }
            let (t, _) = golden(bi, bj, (best.0 - 0.02).max(0.0), best.0 + 0.02, &mut 0u64);
            println!("{{\"exp\":\"cone_rejected\",\"scene\":\"{}\",\"pair\":[{},{}],\"dmin\":{:.4e},\"in_rho_units\":{:.2},\"t\":{:.3}}}", name, i, j, dist(bi, bj, t), dist(bi, bj, t) / rho, t);
        }
    }

    // Third opinion: dense grid on a strided pair sample, short horizon.
    let t3 = Instant::now();
    let dt_end = dense_orbits * TAU;
    let sample: Vec<(u32, u32)> = rp.iter().step_by(dense_stride).cloned().collect();
    let dense_parts = par_chunks(sample.len(), 16, THREADS, |r| {
        let mut out = Vec::new();
        let mut evals = 0u64;
        let mut tmp = Vec::new();
        for &(i, j) in &sample[r] {
            tmp.clear();
            dense_minima(&b[i as usize], &b[j as usize], rho, dt_end, &mut tmp, &mut evals);
            out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, evals)
    });
    let mut dense = Vec::new();
    let mut dense_evals = 0u64;
    for (o, ev) in dense_parts {
        dense.extend(o);
        dense_evals += ev;
    }
    let dense_s = t3.elapsed().as_secs_f64();
    // Compare only on the sampled pairs: method/truth events restricted to the sample frame.
    let in_sample = |e: &Enc| sample.iter().any(|&(i, j)| i == e.0 && j == e.1);
    let meth_sm: Vec<Enc> = meth.iter().filter(|e| inside_dn(e.2) && in_sample(e)).cloned().collect();
    let truth_sm: Vec<Enc> = truth.iter().filter(|e| inside_dn(e.2) && in_sample(e)).cloned().collect();
    let (m_meth, f_meth) = diff(&dense, &meth_sm, dt_end, 1e-3);
    let (m_truth, _f_truth) = diff(&dense, &truth_sm, dt_end, 1e-3);

    println!(
        "{{\"exp\":\"invert\",\"scene\":\"{}\",\"n\":{},\"rho\":{},\"orbits\":{:.1},\"radial_pairs\":{},\"radial_not_cone\":{},\"cone_pairs\":{},\"cone_scanned\":{},\"cone_s\":{:.3},\
\"truth_enc\":{},\"truth_steps\":{},\"truth_fine\":{},\"truth_s\":{:.2},\"outside_cone\":{},\"method_enc\":{},\"matched\":{},\"missed\":{},\"false\":{},\"max_util_cross\":{:.4},\
\"sections\":{:?},\"checks\":{:?},\"hits\":{:?},\"queries\":{},\"qsteps\":{},\"evals\":{},\"method_s\":{:.2},\"evals_per_enc\":{:.0},\"checks_per_enc\":{:.2},\
\"dense_pairs\":{},\"dense_orbits\":{:.1},\"dense_enc\":{},\"dense_evals\":{},\"dense_s\":{:.2},\"dense_missed_by_method\":{},\"dense_false_by_method\":{},\"dense_missed_by_truth\":{},\
\"wall_s\":{:.2},\"missed_list\":\"{:?}\",\"false_list\":\"{:?}\",\"dm_list\":\"{:?}\",\"fm_list\":\"{:?}\"}}",
        name, n, rho, t_end / TAU, rp.len(), radial_not_cone.len(), cs.pairs.len(), cs.scanned, cone_s,
        truth.len(), tst.steps, tst.fine, truth_s, outside_cone, meth.len(), matched, missed.len(), false_.len(), mst.max_util_cross,
        mst.sections, mst.checks, mst.hits, mst.queries, mst.qsteps, mst.evals, meth_s,
        if meth.is_empty() { 0.0 } else { mst.evals as f64 / meth.len() as f64 },
        if meth.is_empty() { 0.0 } else { mst.checks_total() as f64 / meth.len() as f64 },
        sample.len(), dense_orbits, dense.len(), dense_evals, dense_s, m_meth.len(), f_meth.len(), m_truth.len(),
        t_wall.elapsed().as_secs_f64(),
        &missed[..missed.len().min(6)], &false_[..false_.len().min(6)],
        &m_meth[..m_meth.len().min(6)], &f_meth[..f_meth.len().min(6)]
    );
    let _ = TICKS;
}

/// Forensics on one pair: sections vs a dense full-horizon scan.
fn validate(name: &str, i: u32, j: u32, orbits: f64) {
    let (b, rho, _) = scene(name);
    let (bi, bj) = (&b[i as usize], &b[j as usize]);
    let t_end = orbits * TAU;
    let mut evals = 0u64;
    println!("{{\"exp\":\"validate\",\"scene\":\"{}\",\"pair\":[{},{}],\"i\":{{\"a\":{:.6},\"e\":{:.4},\"pom\":{:.4}}},\"j\":{{\"a\":{:.6},\"e\":{:.4},\"pom\":{:.4}}},\"rho\":{},\"t_end\":{:.2}}}",
        name, i, j, bi.a, bi.e, bi.pom, bj.a, bj.e, bj.pom, rho, t_end);
    for sec in sections(bi, bj, rho, SAFETY, &mut evals) {
        println!("{{\"exp\":\"section\",\"kind\":{},\"theta\":{:.6},\"w1\":{},\"w2\":{},\"di\":[{:.5},{:.5}],\"dj\":[{:.5},{:.5}],\"ti\":{},\"tj\":{}}}",
            sec.kind as u8, sec.theta, sec.w1, sec.w2, sec.di.0, sec.di.1, sec.dj.0, sec.dj.1, sec.ti, sec.tj);
    }
    let mut ev = Vec::new();
    let mut st = Stats::default();
    pair_events(bi, bj, rho, SAFETY, 0.0, t_end, &mut st, &mut ev);
    for &(t, d) in &ev {
        println!("{{\"exp\":\"method_event\",\"t\":{:.6},\"d\":{:.3e}}}", t, d);
    }
    let mut tv = Vec::new();
    let mut ts = TruthStats::default();
    truth_pair(bi, bj, rho, t_end, &mut tv, &mut ts);
    for &(t, d) in &tv {
        println!("{{\"exp\":\"truth_event\",\"t\":{:.6},\"d\":{:.3e}}}", t, d);
    }
    let mut dv = Vec::new();
    let mut de = 0u64;
    dense_minima(bi, bj, rho, t_end, &mut dv, &mut de);
    for &(t, d) in &dv {
        println!("{{\"exp\":\"dense_event\",\"t\":{:.6},\"d\":{:.3e}}}", t, d);
    }
    let dv4: Vec<Enc> = dv.iter().map(|&(t, d)| (i, j, t, d)).collect();
    let ev4: Vec<Enc> = ev.iter().map(|&(t, d)| (i, j, t, d)).collect();
    let tv4: Vec<Enc> = tv.iter().map(|&(t, d)| (i, j, t, d)).collect();
    let (m_meth, f_meth) = diff(&dv4, &ev4, t_end, 1e-3);
    println!("{{\"exp\":\"validate_sum\",\"dense\":{},\"method\":{},\"truth\":{},\"missed_by_method\":{},\"false_by_method\":{},\"missed_by_truth\":{},\"dense_evals\":{}}}",
        dv.len(), ev.len(), tv.len(), m_meth.len(), f_meth.len(), diff(&dv4, &tv4, t_end, 1e-3).0.len(), de);
    for e in &m_meth {
        // Distance at the missed event, one window-width around it, to place the miss.
        let (t, d) = (e.2, e.3);
        let mut prof = Vec::new();
        for q in -6..=6 {
            let tt = t + q as f64 * 0.02;
            if tt > 0.0 {
                prof.push(format!("({:.4},{:.3e})", tt, dist(bi, bj, tt)));
            }
        }
        println!("{{\"exp\":\"missed_profile\",\"t\":{:.6},\"d\":{:.3e},\"d_pm0.12\":[{}]}}", t, d, prof.join(","));
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    match args[1].as_str() {
        "run" => run(&args[2], args.get(3).and_then(|x| x.parse().ok()).unwrap_or(16), args.get(4).and_then(|x| x.parse().ok()).unwrap_or(4.0)),
        "validate" => validate(&args[2], args[3].parse().unwrap(), args[4].parse().unwrap(), args.get(5).and_then(|x| x.parse().ok()).unwrap_or(4.0)),
        _ => panic!("usage: invert run <scene> [stride] [dense_orbits] | invert validate <scene> <i> <j> [orbits]"),
    }
}
