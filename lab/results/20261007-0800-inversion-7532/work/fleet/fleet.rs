//! Inversion of gold 20261006-0346-taleb-09b5: does "every real encounter lies within partner
//! rank 4 along the orbit" survive element spread, shear and a neighbouring population?
//! Truth = the encounters crate's own `truth_pair` (every local distance minimum < rho, rigorous
//! conservative advancement). Ranks are measured in mean longitude lambda = M + varpi:
//!   dynamic rank at t_m, static rank at t=0, lagged ranks at t_m - 2pi and t_m - 20pi.

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::pairs::radial_pairs;
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::f64::consts::TAU;

const THREADS: usize = 4;

struct Pop {
    n: usize,
    da: f64,       // a uniform in [1-da, 1+da]; da=0 -> a=1 exactly (identical periods)
    sigma_e: f64,  // Rayleigh eccentricity spread
    pom_half: f64, // varpi uniform in [-pom_half, pom_half]; >= pi -> uniform on the circle
    seed: u64,
}

fn make_pop(p: &Pop) -> Vec<Body> {
    let mut rng = Rng(p.seed);
    (0..p.n)
        .map(|_| {
            let a = if p.da == 0.0 {
                1.0
            } else {
                1.0 + (2.0 * rng.f64() - 1.0) * p.da
            };
            let u = rng.f64();
            let e = (p.sigma_e * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.5);
            let pom = if p.pom_half >= std::f64::consts::FRAC_PI_2 {
                TAU * rng.f64()
            } else {
                (2.0 * rng.f64() - 1.0) * p.pom_half
            };
            let lam = TAU * rng.f64();
            Body::new(a, e, pom, lam)
        })
        .collect()
}

#[inline]
fn circdist(x: f64) -> f64 {
    let m = x.rem_euclid(TAU);
    m.min(TAU - m)
}

fn lam_at(b: &[Body], t: f64) -> Vec<f64> {
    b.iter().map(|x| x.mean_anomaly(t) + x.pom).collect()
}

/// Rank of j among i's neighbours sorted by circular |lambda - lambda_i| distance.
fn rank_of(lams: &[f64], i: usize, j: usize) -> usize {
    let dij = circdist(lams[j] - lams[i]);
    lams.iter()
        .enumerate()
        .filter(|&(k, l)| k != i && circdist(l - lams[i]) < dij)
        .count()
}

struct Stats {
    n_events: u64,
    median: f64,
    p90: f64,
    frac_gt4: f64,
    frac_gt10: f64,
}

fn stats(v: &mut Vec<usize>) -> Stats {
    v.sort_unstable();
    let n = v.len() as u64;
    let q = |p: f64| -> f64 {
        if n == 0 {
            return f64::NAN;
        }
        v[((n as f64 - 1.0) * p).round() as usize] as f64
    };
    let gt = |k: usize| -> f64 {
        if n == 0 {
            return f64::NAN;
        }
        v.iter().filter(|&&x| x > k).count() as f64 / n as f64
    };
    Stats { n_events: n, median: q(0.5), p90: q(0.9), frac_gt4: gt(4), frac_gt10: gt(10) }
}

fn run_scene(name: &str, pops: &[Pop], rho: f64, orbits: f64, dump: &mut String) {
    let t0 = std::time::Instant::now();
    let mut bodies: Vec<Body> = Vec::new();
    let mut pop_of: Vec<u8> = Vec::new();
    for (pi, p) in pops.iter().enumerate() {
        bodies.extend(make_pop(p));
        pop_of.extend(std::iter::repeat(pi as u8).take(p.n));
    }
    let t_end = orbits * TAU;
    let pairs = radial_pairs(&bodies, rho);
    let npairs = pairs.len();
    let parts = emergent_encounters::par_chunks(pairs.len(), 128, THREADS, |r| {
        let mut mine: Vec<(u32, u32, f64, f64)> = Vec::new();
        let mut st = TruthStats::default();
        for &(i, j) in &pairs[r] {
            let mut out: Vec<(f64, f64)> = Vec::new();
            truth_pair(&bodies[i as usize], &bodies[j as usize], rho, t_end, &mut out, &mut st);
            mine.extend(out.into_iter().map(|(t, d)| (i, j, t, d)));
        }
        (mine, st)
    });
    let mut enc: Vec<(u32, u32, f64, f64)> = Vec::new();
    let mut tstat = TruthStats::default();
    for (o, s) in parts {
        enc.extend(o);
        tstat.add(&s);
    }
    enc.sort_by(|a, b| a.2.partial_cmp(&b.2).unwrap());

    let lam0 = lam_at(&bodies, 0.0);
    let mut rd = Vec::new(); // dynamic rank at t_m
    let mut rs = Vec::new(); // static rank (t=0)
    let mut r1 = Vec::new(); // lag one orbit
    let mut r10 = Vec::new(); // lag ten orbits
    let mut cross = [0u64; 4]; // [0-0, 0-1, 1-0, 1-1]
    let mut pair_set = std::collections::HashSet::new();
    let mut rows = 0u64;
    for &(i, j, t, d) in &enc {
        let (i, j) = (i as usize, j as usize);
        let lamd = lam_at(&bodies, t);
        let dyn_r = rank_of(&lamd, i, j).max(rank_of(&lamd, j, i));
        rd.push(dyn_r);
        let stat_r = rank_of(&lam0, i, j).max(rank_of(&lam0, j, i));
        rs.push(stat_r);
        let l1 = lam_at(&bodies, t - TAU);
        let lag1 = rank_of(&l1, i, j).max(rank_of(&l1, j, i));
        r1.push(lag1);
        let l10 = lam_at(&bodies, t - 20.0 * TAU);
        let lag10 = rank_of(&l10, i, j).max(rank_of(&l10, j, i));
        r10.push(lag10);
        cross[pop_of[i] as usize * 2 + pop_of[j] as usize] += 1;
        pair_set.insert((i.min(j) as u32, i.max(j) as u32));
        if rows < 4000 {
            dump.push_str(&format!(
                "{name},{i},{j},{:.4},{:.3e},{dyn_r},{stat_r},{lag1},{lag10},{},{}\n",
                t, d, pop_of[i], pop_of[j]
            ));
            rows += 1;
        }
    }
    let sd = stats(&mut rd);
    let ss = stats(&mut rs);
    let s1 = stats(&mut r1);
    let s10 = stats(&mut r10);
    println!(
        "{{\"scene\":\"{name}\",\"n\":{},\"rho\":{rho:e},\"orbits\":{orbits},\"pairs\":{npairs},\"events\":{},\"pairs_with_enc\":{},\"truth_steps\":{},\"secs\":{:.1},\
         \"rank_dyn\":{{\"med\":{},\"p90\":{},\"gt4\":{:.4},\"gt10\":{:.4}}},\
         \"rank_stat\":{{\"med\":{},\"p90\":{},\"gt4\":{:.4},\"gt10\":{:.4}}},\
         \"rank_lag1\":{{\"med\":{},\"p90\":{},\"gt4\":{:.4},\"gt10\":{:.4}}},\
         \"rank_lag10\":{{\"med\":{},\"p90\":{},\"gt4\":{:.4},\"gt10\":{:.4}}},\
         \"cross_00\":{},\"cross_01\":{},\"cross_11\":{}}}",
        bodies.len(), sd.n_events, pair_set.len(), tstat.steps, t0.elapsed().as_secs_f32(),
        sd.median, sd.p90, sd.frac_gt4, sd.frac_gt10,
        ss.median, ss.p90, ss.frac_gt4, ss.frac_gt10,
        s1.median, s1.p90, s1.frac_gt4, s1.frac_gt10,
        s10.median, s10.p90, s10.frac_gt4, s10.frac_gt10,
        cross[0], cross[1] + cross[2], cross[3]
    );
}

fn main() {
    let mut dump = String::from("scene,i,j,t,d,rank_dyn,rank_stat,rank_lag1,rank_lag10,pop_i,pop_j\n");
    // A: control, the gold's regime: tight circular formation, shear-only
    run_scene("A-control", &[Pop { n: 600, da: 1.2e-3, sigma_e: 1e-4, pom_half: 0.0, seed: 11 }], 1e-3, 120.0, &mut dump);
    // B: identical periods, eccentricity-vector spread (a formation after a burn)
    for (s, seed) in [(0.005f64, 21u64), (0.02, 22), (0.05, 23)] {
        run_scene(&format!("B-s{s:.3}"), &[Pop { n: 600, da: 0.0, sigma_e: s, pom_half: 0.2, seed }], 1e-3, 60.0, &mut dump);
    }
    // C: shearing formation (a-spread drives differential precession)
    run_scene("C-shear", &[Pop { n: 600, da: 5e-3, sigma_e: 1e-2, pom_half: 0.2, seed: 31 }], 1e-4, 100.0, &mut dump);
    // D: fleet embedded in a belt (composition)
    run_scene(
        "D-mixed",
        &[
            Pop { n: 200, da: 5e-4, sigma_e: 2e-3, pom_half: 1e-3, seed: 41 },
            Pop { n: 800, da: 1e-2, sigma_e: 1e-2, pom_half: TAU / 2.0, seed: 42 },
        ],
        1e-3, 100.0, &mut dump,
    );
    std::fs::write("events.csv", dump).unwrap();
}
