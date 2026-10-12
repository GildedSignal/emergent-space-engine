//! SpaceX probe: does the fixed phase certificate's work track real encounters?
//! Scenes: D dispersed shells, T tight formation, U shared-shape + ULP outliers,
//! M mixed-e group, R random belt, X seam+overtake, P hyperbolic intruders.
//! Modes: truth | scale | ulp | mixed | panic | crossover | all
use emergent_encounters::kepler::Body;
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::radial_pairs;
use emergent_encounters::phase::{group_events, Neighbours};
use emergent_encounters::phase_orig;
use emergent_encounters::tier;
use std::collections::BTreeSet;
use std::f64::consts::TAU;
use std::time::Instant;

const RHO: f64 = 1e-4;
const H: f64 = 5.0;

fn dispersed_da(m: usize, shells: usize, da: f64) -> Vec<Body> {
    let mut b = Vec::new();
    for s in 0..shells {
        let a = 1.0 + da * s as f64;
        for i in 0..m {
            let lam = TAU * 0.25 + 0.1 * i as f64 / m as f64;
            b.push(Body::new(a, 0.0, 0.0, lam));
        }
    }
    b
}

fn tight(n: usize, e: f64, outliers: usize) -> Vec<Body> {
    // outliers: bodies whose e is one representable step above the shared e.
    let e_ulp = f64::from_bits(e.to_bits() + 1);
    (0..n)
        .map(|i| {
            let ei = if outliers > 0 && i % (n / outliers.max(1)).max(1) == 0 && outliers <= n {
                e_ulp
            } else {
                e
            };
            let lam = TAU * 0.25 + 0.6 * RHO * i as f64;
            Body::new(1.0, ei, 0.0, lam)
        })
        .collect()
}

fn mixed(n: usize) -> Vec<Body> {
    // Half circles, half e=0.3 ellipses, same a, one arc: real cross conjunctions.
    (0..n)
        .map(|i| {
            let e = if i % 2 == 0 { 0.0 } else { 0.3 };
            let lam = TAU * 0.25 + 0.1 * i as f64 / n as f64;
            Body::new(1.0, e, 0.0, lam)
        })
        .collect()
}

fn seam(n: usize) -> Vec<Body> {
    // Two arcs across the seam plus an a-spread for overtakes within the horizon.
    (0..n)
        .map(|i| {
            let half = if i % 2 == 0 { -0.05 } else { 0.05 };
            let lam = (half + 0.1 * ((i / 2) as f64) / (n as f64 / 2.0)).rem_euclid(TAU);
            let a = 1.0 + 0.001 * ((i % 7) as f64);
            Body::new(a, 0.0, 0.0, lam)
        })
        .collect()
}

fn belt(n: usize, seed: u64) -> Vec<Body> {
    // Deterministic LCG belt: spread a, e, pom, lambda.
    let mut s = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
    let mut r = || {
        s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (s >> 11) as f64 / (1u64 << 53) as f64
    };
    (0..n)
        .map(|_| {
            let a = 0.98 + 0.04 * r();
            let e = 0.15 * r();
            let pom = TAU * r();
            let lam = TAU * r();
            Body::new(a, e, pom, lam)
        })
        .collect()
}

fn hyper(n: usize) -> Vec<Body> {
    let mut b: Vec<Body> = (0..n - 4)
        .map(|i| Body::new(1.0, 0.01, 0.0, TAU * 0.25 + 0.6 * RHO * i as f64))
        .collect();
    for k in 0..4 {
        b.push(Body::new(1.0, 1.5, 0.3 * k as f64, TAU * 0.25 + 0.01));
    }
    b
}

/// Exact truth: radial-overlap superset, ungated exact per-pair machinery.
fn exact_truth(b: &[Body]) -> (BTreeSet<(u32, u32)>, u64) {
    let cand = radial_pairs(b, RHO);
    let mut set = BTreeSet::new();
    let mut evals = 0u64;
    let mut out = Vec::new();
    let mut st = Stats::default();
    for &(i, j) in &cand {
        let (bi, bj) = (&b[i as usize], &b[j as usize]);
        for t in [0.0, H] {
            let (x, y) = (bi.state(t), bj.state(t));
            if (x[0] - y[0]).hypot(x[1] - y[1]) < RHO {
                set.insert((i, j));
            }
        }
        out.clear();
        pair_events(bi, bj, RHO, 1.1, 0.0, H, &mut st, &mut out);
        evals += 1;
        if out.iter().any(|&(t, _)| t > 0.0 && t < H) {
            set.insert((i, j));
        }
    }
    (set, evals)
}

fn cert_pairs(b: &[Body]) -> (BTreeSet<(u32, u32)>, emergent_encounters::phase::GroupStats, f64) {
    let t = Instant::now();
    let mut ev = Vec::new();
    let st = group_events(b, RHO, 0.0, H, |i, j, _tt, _d| ev.push((i, j)));
    let set: BTreeSet<_> = ev.into_iter().collect();
    (set, st, t.elapsed().as_secs_f64())
}

fn check_scene(name: &str, b: &[Body], truth_on_core: bool) {
    let (want, truth_evals) = if truth_on_core {
        exact_truth(b)
    } else {
        // Hyperbolic scene: truth over the Kepler core only (indices n-4.. are hyper);
        // the crate's exact machinery is out of domain for them.
        let core: Vec<Body> = b[..b.len() - 4].to_vec();
        let (s, e) = exact_truth(&core);
        (s, e)
    };
    let (got, st, dt) = cert_pairs(b);
    let missing: Vec<_> = want.difference(&got).collect();
    let hyper_pairs: Vec<_> = got
        .iter()
        .filter(|&&(i, j)| (i as usize) >= b.len() - 4 || (j as usize) >= b.len() - 4)
        .collect();
    println!(
        "{name}: n={} truth_pairs={} truth_evals={} | cert: phase={} budget_fb={} walk={} w_rej={} cone_rej={} armed={} bcheck={} evals={} events_pairs={} | t={:.3}s",
        b.len(), want.len(), truth_evals,
        st.phase, st.budget_fallback, st.walk, st.window_reject, st.cone_reject,
        st.neighbours, st.boundary_checks, st.exact.evals, got.len(), dt
    );
    if truth_on_core || b.len() == 0 {
        assert!(missing.is_empty(), "{name}: MISSED {:?}", missing);
    } else {
        assert!(missing.is_empty(), "{name}: MISSED {:?}", missing);
        assert!(hyper_pairs.is_empty(), "{name}: hyper pairs emitted {:?}", hyper_pairs);
    }
    println!("{name}: OK zero-miss (cert evals/truth evals = {:.2})", st.exact.evals as f64 / truth_evals.max(1) as f64);
}

fn run_orig(b: &[Body], label: &str) {
    let t = Instant::now();
    let mut ev = 0u64;
    let st = phase_orig::group_events(b, RHO, 0.0, H, |_i, _j, _t, _d| ev += 1);
    println!(
        "{label}: ORIG n={} phase={} conc={:.4} neigh={} bcheck={} evals={} events={} t={:.3}s",
        b.len(), st.phase, st.concentration, st.neighbours, st.boundary_checks,
        st.exact.evals, ev, t.elapsed().as_secs_f64()
    );
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let which = args.get(1).map(|s| s.as_str()).unwrap_or("all");
    if which == "all" || which == "truth" {
        check_scene("TRUTH T200   tight", &tight(200, 0.01, 0), true);
        check_scene("TRUTH D200   dispersed", &dispersed_da(100, 2, 2e-3), true);
        check_scene("TRUTH U400/0 shared-e.05", &tight(400, 0.05, 0), true);
        check_scene("TRUTH U400/1 +1ulp", &tight(400, 0.05, 1), true);
        check_scene("TRUTH U400/8 +8ulp", &tight(400, 0.05, 8), true);
        check_scene("TRUTH M400   mixed-e", &mixed(400), true);
        check_scene("TRUTH X400   seam+overtake", &seam(400), true);
        check_scene("TRUTH R400   belt s1", &belt(400, 1), true);
        check_scene("TRUTH R400   belt s2", &belt(400, 2), true);
        check_scene("TRUTH P400   hyper4", &hyper(400), false);
        // Regression: the original certificate on the same in-domain scenes.
        run_orig(&tight(400, 0.05, 0), "ORIG U400/0");
        run_orig(&tight(400, 0.05, 1), "ORIG U400/1");
        run_orig(&mixed(400), "ORIG M400");
        run_orig(&belt(400, 1), "ORIG R400 s1");
    }
    if which == "all" || which == "scale" {
        // Dispersed at fixed per-shell count: the board's scaling demand.
        for &(m, k) in &[(100usize, 10usize), (100, 20), (100, 40), (100, 80), (400, 80)] {
            let b = dispersed_da(m, k, 2e-3);
            let (got, st, dt) = cert_pairs(&b);
            println!(
                "SCALE-D n={:6} phase={} fb={} walk={} w_rej={} cone_rej={} armed={} evals={} events={} t={:.3}s",
                b.len(), st.phase, st.budget_fallback, st.walk, st.window_reject,
                st.cone_reject, st.neighbours, st.exact.evals, got.len(), dt
            );
        }
        // Tight concentration with outliers: exact work must stay linear.
        for &n in &[1000usize, 4000, 16000] {
            for &o in &[0usize, 1, 8] {
                let b = tight(n, 0.05, o);
                let (got, st, dt) = cert_pairs(&b);
                println!(
                    "SCALE-T n={:6} out={} phase={} walk={} w_rej={} cone_rej={} armed={} evals={} events={} t={:.3}s",
                    n, o, st.phase, st.walk, st.window_reject, st.cone_reject,
                    st.neighbours, st.exact.evals, got.len(), dt
                );
            }
        }
        // Mixed-e concentration: work per real encounter at growing n.
        for &n in &[200usize, 800, 3200] {
            let b = mixed(n);
            let (got, st, dt) = cert_pairs(&b);
            println!(
                "SCALE-M n={:6} phase={} fb={} walk={} cone_rej={} armed={} evals={} events={} per_enc={:.1} t={:.3}s",
                n, st.phase, st.budget_fallback, st.walk, st.cone_reject,
                st.neighbours, st.exact.evals, got.len(),
                st.exact.evals as f64 / got.len().max(1) as f64, dt
            );
        }
    }
    if which == "all" || which == "ulp" {
        for &n in &[500usize, 2000, 8000] {
            for &o in &[0usize, 1, 8] {
                let b = tight(n, 0.05, o);
                if let Some(nb) = Neighbours::new(&b, RHO, 0.0, H) {
                    let st = nb.visit(&b, RHO, u64::MAX, |_i, _j| {});
                    println!(
                        "ULP n={:5} out={} walk={} w_rej={} cone_rej={} ARMED={} max_k={}",
                        n, o, st.walk, st.window_reject, st.cone_reject, st.pairs, st.max_k
                    );
                } else {
                    println!("ULP n={n} out={o}: no phase cert (tree)");
                }
            }
        }
    }
    if which == "all" || which == "panic" {
        for &n in &[10usize, 400] {
            let b = hyper(n);
            let r = std::panic::catch_unwind(|| {
                let mut ev = 0u64;
                let st = group_events(&b, RHO, 0.0, 1.0, |_i, _j, _t, _d| ev += 1);
                (st.domain_refusals, st.phase, ev)
            });
            match r {
                Ok((dr, ph, ev)) => println!(
                    "PANIC n={n}: no panic; domain_refusals={} phase={} events={} (expect 4 / true-ish / core contacts only)",
                    dr, ph, ev
                ),
                Err(_) => println!("PANIC n={n}: STILL PANICS"),
            }
        }
    }
    if which == "all" || which == "crossover" {
        // D n=8000: phase-sweep-to-completion vs tree, to place the budget.
        let b = dispersed_da(100, 80, 2e-3);
        if let Some(nb) = Neighbours::new(&b, RHO, 0.0, H) {
            let t = Instant::now();
            let st = nb.visit(&b, RHO, u64::MAX, |_i, _j| {});
            println!(
                "CROSS D8000 sweep-only: walk={} armed={} t={:.3}s (filters only, no exact work)",
                st.walk, st.pairs, t.elapsed().as_secs_f64()
            );
        }
        let (_got, st, dt) = cert_pairs(&b);
        println!(
            "CROSS D8000 default group_events: fb={} evals={} t={:.3}s",
            st.budget_fallback, st.exact.evals, dt
        );
        // Tree path alone, same measurement as the red-team's run_tier.
        let t = Instant::now();
        let tree = tier::Tree::new(&b, 32);
        let mut ts = tier::TreeStats::default();
        let mut arm = tier::ArmStats::default();
        let mut ex = Stats::default();
        let mut out = Vec::new();
        let mut pairs = 0u64;
        tier::traverse(&tree, &b, RHO, true, &mut |i: u32, j: u32| {
            pairs += 1;
            if tier::arm_pair(&b[i as usize], &b[j as usize], RHO, 1.1, 0.0, H, &mut arm).0 {
                out.clear();
                pair_events(&b[i as usize], &b[j as usize], RHO, 1.1, 0.0, H, &mut ex, &mut out);
            }
        }, &mut ts);
        println!(
            "CROSS D8000 tree-only: pairs={} evals={} t={:.3}s",
            pairs, ex.evals, t.elapsed().as_secs_f64()
        );
    }
}
