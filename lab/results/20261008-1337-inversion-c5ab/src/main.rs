//! Inversion lens, run 20261008-1337: does the phase-neighbour certificate (gold 20261006-0346,
//! "every real encounter lies within partner rank 4 along the orbit") survive element dispersion?
//!
//! Scenes: co-orbital formations (one exact integer period for all bodies, a = 1 — maximal
//! concentration, the gold's trigger must fire), Rayleigh e / apsidal spread / one-body kicks.
//! Truth: the crate's own `truth_pair` (conservative advancement, dense in time, independent of
//! any conjunction or phase logic) over every radially overlapping pair, one full period (equal
//! periods => the relative configuration of every pair repeats exactly each period).
//!
//! Debug run correction (debug_kick.py): for equal-period pairs the offset at an orbit crossing
//! is v*tau ~ |gap| (full orbital speed; the relative velocity ~ sigma_e*v never closes it), so
//! each pair's two crossings give windows |DeltaM0 - DeltaM*| < rho each, independent of e.
//!
//! Metrics: per scene, the circular phase rank of every truly encountering pair under three
//! sort keys (mean anomaly M0 — time-invariant; mean longitude; true longitude at t=0),
//! miss fraction at k = 4, the 99%-quantile and max rank, and the churn of the true-longitude
//! order over one period relative to a co-rotating reference (rank exchanges per orbit).

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::pairs::radial_pairs;
use emergent_encounters::par_chunks;
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::f64::consts::TAU;
use std::time::Instant;

const THREADS: usize = 7;

#[derive(Clone, Copy)]
enum Pom {
    Aligned,
    Random,
}

fn formation(n: usize, sigma_e: f64, fixed_e: Option<f64>, pom: Pom, seed: u64) -> Vec<Body> {
    let mut rng = Rng(seed);
    let period = (TAU * TICKS).round() as u64; // a ~ 1 exactly, identical for all bodies
    (0..n)
        .map(|_| {
            let e = match fixed_e {
                Some(e) => e,
                None => {
                    if sigma_e > 0.0 {
                        let u = rng.f64();
                        (sigma_e * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.5)
                    } else {
                        0.0
                    }
                }
            };
            let p = match pom {
                Pom::Aligned => 0.0,
                Pom::Random => TAU * rng.f64(),
            };
            let lam = TAU * rng.f64();
            Body::with_period(period, e, p, lam)
        })
        .collect()
}

/// The three sort keys at t = 0.
fn keys(b: &[Body]) -> [Vec<f64>; 3] {
    let mut m0 = Vec::with_capacity(b.len());
    let mut ml = Vec::with_capacity(b.len());
    let mut tl = Vec::with_capacity(b.len());
    for bod in b {
        let m = bod.mean_anomaly(0.0);
        m0.push(m);
        ml.push((bod.pom + m).rem_euclid(TAU));
        let s = bod.state(0.0);
        tl.push(s[1].atan2(s[0]).rem_euclid(TAU));
    }
    [m0, ml, tl]
}

fn ranks(key: &[f64]) -> Vec<usize> {
    let n = key.len();
    let mut idx: Vec<usize> = (0..n).collect();
    idx.sort_by(|&a, &c| key[a].partial_cmp(&key[c]).unwrap());
    let mut r = vec![0usize; n];
    for (rr, &i) in idx.iter().enumerate() {
        r[i] = rr;
    }
    r
}

fn circrank(r: &[usize], i: usize, j: usize, n: usize) -> usize {
    let d = r[i].abs_diff(r[j]);
    d.min(n - d)
}

/// Pairs (i, j) with at least one truth minimum below rho over one period, plus stats.
fn truth_pairs(b: &[Body], pairs: &[(u32, u32)], rho: f64) -> (Vec<(u32, u32)>, u64, TruthStats) {
    let parts = par_chunks(pairs.len(), 2048, THREADS, |range| {
        let mut enc = Vec::new();
        let mut minima = 0u64;
        let mut st = TruthStats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &pairs[range] {
            tmp.clear();
            truth_pair(
                &b[i as usize],
                &b[j as usize],
                rho,
                TAU * 1.0005,
                &mut tmp,
                &mut st,
            );
            if tmp.iter().any(|&(_, d)| d < rho) {
                enc.push((i, j));
                minima += tmp.len() as u64;
            }
        }
        (enc, minima, st)
    });
    let mut enc = Vec::new();
    let mut minima = 0u64;
    let mut st = TruthStats::default();
    for (e, m, s) in parts {
        enc.extend(e);
        minima += m;
        st.add(&s);
    }
    (enc, minima, st)
}

/// Rank exchanges of the true-longitude order over one period, relative to a co-rotating
/// reference (body 0): rigid rotation gives 0, dispersion-driven passing counts.
fn churn(b: &[Body], samples: usize) -> usize {
    let n = b.len();
    let mut prev: Vec<usize> = Vec::new();
    let mut total = 0usize;
    for s in 0..samples {
        let t = (s as f64 + 0.5) * TAU / samples as f64;
        let mut key: Vec<(f64, usize)> = b
            .iter()
            .enumerate()
            .map(|(i, bod)| {
                let st = bod.state(t);
                (st[1].atan2(st[0]).rem_euclid(TAU), i)
            })
            .collect();
        key.sort_by(|a, c| a.0.partial_cmp(&c.0).unwrap());
        let mut rank = vec![0usize; n];
        for (rr, &(_, i)) in key.iter().enumerate() {
            rank[i] = rr;
        }
        if !prev.is_empty() {
            // ranks relative to body 0 kill the rigid rotation
            let rot = |r: &Vec<usize>| -> Vec<usize> {
                (0..n).map(|i| (n + r[i] - r[0]) % n).collect()
            };
            let (a, c) = (rot(&rank), rot(&prev));
            total += a.iter().zip(&c).map(|(&x, &y)| x.abs_diff(y)).sum::<usize>() / 2;
        }
        prev = rank;
    }
    total
}

fn quantile(mut v: Vec<usize>, q: f64) -> usize {
    if v.is_empty() {
        return 0;
    }
    v.sort_unstable();
    v[((v.len() as f64 - 1.0) * q).round() as usize]
}

fn analyse(
    name: &str,
    b: &[Body],
    npairs: usize,
    enc: &[(u32, u32)],
    minima: u64,
    exchanges: usize,
    st: &TruthStats,
) {
    let n = b.len();
    let ks = keys(b);
    let keynames = ["mean-anomaly", "mean-longitude", "true-longitude"];
    println!("scene {}", name);
    println!(
        "  n={} pairs_scanned={} enc_pairs={} enc_minima={} truth_steps={} truth_evals={}",
        n,
        npairs,
        enc.len(),
        minima,
        st.steps,
        st.evals
    );
    println!(
        "  exchanges_per_orbit={} exchanges_per_encounter={:.1}",
        exchanges,
        exchanges as f64 / enc.len().max(1) as f64
    );
    for (ki, kname) in keynames.iter().enumerate() {
        let r = ranks(&ks[ki]);
        let rs: Vec<usize> = enc
            .iter()
            .map(|&(i, j)| circrank(&r, i as usize, j as usize, n))
            .collect();
        let miss4 = rs.iter().filter(|&&x| x > 4).count();
        let k99 = quantile(rs.clone(), 0.99);
        let kmax = rs.iter().copied().max().unwrap_or(0);
        println!(
            "  key={:<15} miss_at_k4={:>6}/{} ({:.3}) k99={:>6} kmax={:>6}",
            kname,
            miss4,
            rs.len(),
            miss4 as f64 / rs.len().max(1) as f64,
            k99,
            kmax
        );
    }
}

fn main() {
    let t0 = Instant::now();
    let sel: Vec<String> = std::env::args().skip(1).collect();
    let chosen = |name: &str| sel.is_empty() || sel.iter().any(|s| name.starts_with(s.as_str()));
    let rho = 1e-4;
    let scenes: Vec<(&str, usize, f64, Option<f64>, Pom, u64)> = vec![
        ("A-control", 1600, 0.0, None, Pom::Aligned, 101),
        ("B-aligned-1e-3", 1600, 1e-3, None, Pom::Aligned, 102),
        ("C-aligned-1e-2", 1600, 1e-2, None, Pom::Aligned, 103),
        ("D-aligned-3e-2", 1600, 3e-2, None, Pom::Aligned, 104),
        ("E-fixe-1e-2-randpom", 1600, 0.0, Some(1e-2), Pom::Random, 105),
        ("F-sige-1e-2-randpom", 1600, 1e-2, None, Pom::Random, 106),
        ("G1-aligned-1e-2-n400", 400, 1e-2, None, Pom::Aligned, 107),
        ("G2-aligned-1e-2-n800", 800, 1e-2, None, Pom::Aligned, 108),
    ];
    for (name, n, sigma_e, fixed_e, pom, seed) in scenes {
        if !chosen(name) {
            continue;
        }
        let t1 = Instant::now();
        let b = formation(n, sigma_e, fixed_e, pom, seed);
        let pairs = radial_pairs(&b, rho);
        let (enc, minima, st) = truth_pairs(&b, &pairs, rho);
        let exchanges = churn(&b, 256);
        analyse(name, &b, pairs.len(), &enc, minima, exchanges, &st);
        println!("  wall={:.1}s", t1.elapsed().as_secs_f64());
    }

    // Kick scenes: the control formation, one body's e raised by de (mean longitude preserved).
    // rho = 1e-3 (r8's belt range) and n = 3200 so the two crossing windows (~2*rho/pi per pair)
    // give a measurable encounter count.
    let period = (TAU * TICKS).round() as u64;
    for (name, de) in [
        ("H1-kick-de1e-3", 1e-3),
        ("H2-kick-de1e-2", 1e-2),
        ("H3-kick-de3e-2", 3e-2),
    ] {
        for seed in [301u64, 302, 303] {
            let sname = format!("{}-s{}", name, seed - 300);
            if !chosen(&sname) {
                continue;
            }
            let t1 = Instant::now();
            let rho_k = 1e-3;
            let mut b = formation(3200, 0.0, None, Pom::Aligned, seed);
            let lam0 = (b[0].pom + b[0].mean_anomaly(0.0)).rem_euclid(TAU);
            b[0] = Body::with_period(period, de, 0.0, lam0);
            let pairs: Vec<(u32, u32)> = (1..b.len()).map(|j| (0, j as u32)).collect();
            let (enc, minima, st) = truth_pairs(&b, &pairs, rho_k);
            analyse(&sname, &b, pairs.len(), &enc, minima, 0, &st);
            println!("  wall={:.1}s", t1.elapsed().as_secs_f64());
        }
    }
    println!("total wall={:.1}s", t0.elapsed().as_secs_f64());
}
