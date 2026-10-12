//! Independent r8 truth construction, with the gold fleet sampler copied verbatim.
//! Run `cargo test --release -p emergent-encounters --test phase_truth -- --nocapture`.
//! ENCOUNTER_BASELINE=1 selects main's pairwise path for the before measurement.
#[path = "support/r8_truth.rs"]
#[allow(dead_code)]
mod oracle;

use emergent_encounters::{
    belt::Rng,
    kepler::Body,
    method::{pair_events, Stats},
};
use std::f64::consts::TAU;
use std::time::Instant;

fn fleet(n: usize, width: f64, sigma: f64, seed: u64) -> Vec<Body> {
    let mut rng = Rng(seed);
    let pom0 = TAU * rng.f64();
    let lam0 = TAU * rng.f64();
    (0..n)
        .map(|_| {
            let a = 1.0 + (2.0 * rng.f64() - 1.0) * width;
            let e = (0.001 * (-2.0 * (1.0 - rng.f64()).ln()).sqrt()).min(0.01);
            let pom = pom0 + (2.0 * rng.f64() - 1.0) * 0.1;
            let lam = if sigma <= 0.0 {
                TAU * rng.f64()
            } else {
                let (u1, u2) = (rng.f64(), rng.f64());
                lam0 + sigma * (-2.0 * (1e-12 + u1).ln()).sqrt() * (TAU * u2).cos()
            };
            Body::new(a, e, pom, lam)
        })
        .collect()
}

fn independent(x: &Body) -> oracle::Body {
    // Give both algorithms the same integer-clock input, rather than independently
    // rounding a nominal phase; the position/minimum solvers are entirely separate.
    oracle::Body::new(x.a, x.e, x.pom, x.pom - TAU * x.tp as f64 / x.period as f64)
}

fn measure(name: &str, b: Vec<Body>, horizon: f64, rho: f64) {
    let now = Instant::now();
    let obs: Vec<_> = b.iter().map(independent).collect();
    let mut expected = Vec::new();
    let mut evals = 0;
    for i in 0..b.len() {
        for j in i + 1..b.len() {
            let mut hits = Vec::new();
            oracle::truth_pair(&obs[i], &obs[j], rho, horizon, &mut hits, &mut evals);
            expected.extend(hits.into_iter().map(|(t, _)| (i as u32, j as u32, t)));
            // Gold's checker counts existing contacts at query edges. r8's local
            // minima remain separately identifiable by their interior timestamps.
            for t in [0.0, horizon] {
                let (x, y) = (obs[i].state(t), obs[j].state(t));
                if (x[0] - y[0]).hypot(x[1] - y[1]) < rho {
                    expected.push((i as u32, j as u32, t));
                }
            }
        }
    }
    let mut stats = Stats::default();
    let mut actual = Vec::new();
    let mut candidate_work = 0;
    let mut max_k = 0;
    if std::env::var_os("ENCOUNTER_BASELINE").is_some() {
        for i in 0..b.len() {
            for j in i + 1..b.len() {
                let mut out = Vec::new();
                pair_events(&b[i], &b[j], rho, 1.1, 0.0, horizon, &mut stats, &mut out);
                actual.extend(out.into_iter().map(|(t, _)| (i as u32, j as u32, t)));
            }
        }
        candidate_work = stats.pairs;
    } else {
        let group =
            emergent_encounters::phase::group_events(&b, rho, 0.0, horizon, |i, j, t, _| {
                actual.push((i, j, t))
            });
        stats = group.exact;
        candidate_work += group.neighbours + group.tree.node_tests + group.tree.cand;
        max_k = group.max_k;
    }
    let matches = |x: &(u32, u32, f64), ys: &[(u32, u32, f64)]| {
        ys.iter()
            .any(|y| x.0 == y.0 && x.1 == y.1 && (x.2 - y.2).abs() < 1e-5)
    };
    let misses = expected.iter().filter(|x| !matches(x, &actual)).count();
    let false_ = actual.iter().filter(|x| !matches(x, &expected)).count();
    println!("GATE {name} truth={} misses={misses} false={false_} setups={} checks={} candidate_work={candidate_work} max_k={max_k} oracle_evals={evals} seconds={:.3}", expected.len(), stats.pairs, stats.checks_total(), now.elapsed().as_secs_f64());
    assert_eq!(misses, 0, "{name}: truth contacts lost");
    assert_eq!(false_, 0, "{name}: reports absent from independent truth");
}

#[test]
fn gold_adj() {
    measure("gold-adj", fleet(200, 1e-5, 0.01, 27), TAU, 1e-4);
}

#[test]
fn gold_uniform() {
    measure("gold-uniform", fleet(200, 1e-3, 0.0, 21), TAU, 1e-4);
}

#[test]
fn gold_800() {
    measure("gold-800", fleet(800, 1e-3, 0.0, 22), TAU * 0.5, 1e-4);
}

#[test]
fn gold_wide() {
    measure("gold-wide", fleet(200, 3e-3, 0.0, 23), TAU, 1e-4);
}

#[test]
fn gold_bunch24() {
    measure("gold-bunch24", fleet(200, 1e-5, 0.05, 24), TAU, 1e-4);
}

#[test]
fn gold_bunch25() {
    measure("gold-bunch25", fleet(200, 1e-3, 0.05, 25), TAU, 1e-4);
}

#[test]
fn gold_bunch26() {
    measure("gold-bunch26", fleet(200, 1e-5, 0.02, 26), TAU, 1e-4);
}

#[test]
fn gold_bunch28() {
    measure("gold-bunch28", fleet(200, 1e-3, 0.02, 28), TAU, 1e-4);
}

#[test]
fn checker_jam() {
    measure("checker-jam", fleet(200, 1e-5, 0.005, 27), TAU, 1e-4);
}

#[test]
fn dense_ring() {
    let b = (0..256)
        .map(|i| Body::new(1.0, 0.02, 0.3, TAU * i as f64 / 256.0))
        .collect();
    measure("dense-ring", b, TAU, 0.03);
}

#[test]
fn work_per_real_contact_stays_bounded_under_ring_dilution() {
    for n in [32, 64, 128] {
        let rho = 1.5 * TAU / n as f64;
        let b: Vec<_> = (0..n)
            .map(|i| Body::new(1.0, 0.02, 0.3, TAU * i as f64 / n as f64))
            .collect();
        let obs: Vec<_> = b.iter().map(independent).collect();
        let mut real = 0;
        for i in 0..n {
            for j in i + 1..n {
                let mut hits = Vec::new();
                oracle::truth_pair(&obs[i], &obs[j], rho, TAU, &mut hits, &mut 0);
                real += hits.len();
            }
        }
        let work = if std::env::var_os("ENCOUNTER_BASELINE").is_some() {
            let mut stats = Stats::default();
            for i in 0..n {
                for j in i + 1..n {
                    pair_events(
                        &b[i],
                        &b[j],
                        rho,
                        1.1,
                        0.0,
                        TAU,
                        &mut stats,
                        &mut Vec::new(),
                    );
                }
            }
            stats.pairs + stats.checks_total()
        } else {
            let stats =
                emergent_encounters::phase::group_events(&b, rho, 0.0, TAU, |_, _, _, _| {});
            stats.neighbours
                + stats.exact.pairs
                + stats.exact.checks_total()
                + stats.boundary_checks
        };
        // This shape has one contact per neighbour per cycle. Charge traversal,
        // setup, proposed passage checks (including padding), and both edges.
        // Sixteen operations/contact allows two full sets of those charges;
        // the limit is constant under dilution, independent of n.
        println!(
            "GATE ring-work n={n} truth={real} work={work} bound={}",
            16 * real
        );
        assert!(real > 0 && work <= 16 * real as u64);
    }
}
