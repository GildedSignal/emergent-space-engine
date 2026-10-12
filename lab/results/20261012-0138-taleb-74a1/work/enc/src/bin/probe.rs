//! Taleb probe: fragility of the phase-neighbour certificate (wt/cx-b-coorbital-cert).
//! Scenes:
//!   D<m>,<k>  dispersed formation: k shells spaced da=2e-3, m bodies/shell, arc A=0.1, e=0.
//!             Zero contacts by construction (cross-shell chord >= 2e-3 > rho; same-shell
//!             chord = const >= 1e-3 > rho). Phase cert should fire (reach < pi) and visit all pairs.
//!   T<n>      tight formation: one shell, spacing 0.6*rho -> permanent/near contacts (control).
//!   U<n>,<s>  scene T with e=0.05 shared; s=0 exact shapes, s=1 one body's e += 1e-16 (1 ULP).
//!   P         one hyperbolic body (e=1.5) in a co-orbital group: panic?
//!   B<n>      brute-force truth by sampling (instrument check for D and T).
use emergent_encounters::kepler::Body;
use emergent_encounters::phase::{group_events, Neighbours};
use emergent_encounters::tier;
use std::f64::consts::TAU;
use std::time::Instant;

const RHO: f64 = 1e-4;

fn dispersed(m: usize, shells: usize) -> Vec<Body> {
    dispersed_da(m, shells, 2e-3)
}

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

fn tight(n: usize, e: f64, ulp: bool) -> Vec<Body> {
    let mut b = Vec::new();
    for i in 0..n {
        let mut ei = e;
        if ulp && i == n / 2 {
            ei = f64::from_bits(ei.to_bits() + 1); // one representable step
        }
        let lam = TAU * 0.25 + 0.6 * RHO * i as f64;
        b.push(Body::new(1.0, ei, 0.0, lam));
    }
    b
}

fn min_dist_grid(b: &[Body], samples: usize, t0: f64, t1: f64) -> Vec<(u32, u32, f64)> {
    let mut out = Vec::new();
    for i in 0..b.len() {
        for j in i + 1..b.len() {
            let mut dm = f64::INFINITY;
            for k in 0..samples {
                let t = t0 + (t1 - t0) * k as f64 / samples as f64;
                let (x, y) = (b[i].state(t), b[j].state(t));
                let d = (x[0] - y[0]).hypot(x[1] - y[1]);
                dm = dm.min(d);
            }
            if dm < RHO {
                out.push((i as u32, j as u32, dm));
            }
        }
    }
    out
}

fn run_phase(b: &[Body], h: f64, label: &str) {
    let t = Instant::now();
    let mut ev = Vec::new();
    let st = group_events(b, RHO, 0.0, h, |i, j, tt, d| ev.push((i, j, tt, d)));
    println!(
        "{label}: n={} phase={} conc={:.4} reach_k={} neigh={} bcheck={} | exact pairs={} evals={} checks={} hits={} | events={} t={:.3}s",
        b.len(), st.phase, st.concentration, st.max_k, st.neighbours, st.boundary_checks,
        st.exact.pairs, st.exact.evals, st.exact.checks_total(), st.exact.hits_total(),
        ev.len(), t.elapsed().as_secs_f64()
    );
}

/// Same scene through the general tier only (what the phase cert displaced), same callback work.
fn run_tier(b: &[Body], h: f64, label: &str) {
    use emergent_encounters::method::{pair_events, Stats};
    let t = Instant::now();
    let tree = tier::Tree::new(b, 32);
    let mut ts = tier::TreeStats::default();
    let mut arm = tier::ArmStats::default();
    let mut ex = Stats::default();
    let mut pairs = 0u64;
    let mut bcheck = 0u64;
    let mut out = Vec::new();
    let mut ev = Vec::new();
    tier::traverse(&tree, b, RHO, true, &mut |i: u32, j: u32| {
        pairs += 1;
        let (bi, bj) = (&b[i as usize], &b[j as usize]);
        for tt in [0.0, h] {
            let (x, y) = (bi.state(tt), bj.state(tt));
            bcheck += 1;
            let d = (x[0] - y[0]).hypot(x[1] - y[1]);
            if d < RHO {
                ev.push((i, j, tt, d));
            }
        }
        if tier::arm_pair(bi, bj, RHO, 1.1, 0.0, h, &mut arm).0 {
            out.clear();
            pair_events(bi, bj, RHO, 1.1, 0.0, h, &mut ex, &mut out);
            for &(tt, d) in out.iter() {
                if tt > 0.0 && tt < h {
                    ev.push((i, j, tt, d));
                }
            }
        }
    }, &mut ts);
    println!(
        "{label}: n={} tier_pairs={} bcheck={} | exact pairs={} evals={} hits={} | events={} t={:.3}s",
        b.len(), pairs, bcheck, ex.pairs, ex.evals, ex.hits_total(), ev.len(),
        t.elapsed().as_secs_f64()
    );
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let which = args.get(1).map(|s| s.as_str()).unwrap_or("all");
    let h = 5.0_f64;
    if which == "all" || which == "truth" {
        let b = dispersed(100, 2);
        let truth = min_dist_grid(&b, 500, 0.0, h);
        println!("TRUTH D200 dispersed: brute contacts={} (expect 0)", truth.len());
        let bt = tight(200, 0.01, false);
        let truth = min_dist_grid(&bt, 500, 0.0, h);
        println!("TRUTH T200 tight: brute contacts={} (expect ~199 permanent neighbours)", truth.len());
        let mut ev = Vec::new();
        let st = group_events(&bt, RHO, 0.0, h, |i, j, t, d| ev.push((i, j, t, d)));
        let mut got: std::collections::BTreeSet<(u32, u32)> = ev.iter().map(|x| (x.0, x.1)).collect();
        let want: std::collections::BTreeSet<(u32, u32)> = truth.iter().map(|x| (x.0, x.1)).collect();
        let missed: Vec<_> = want.difference(&got).collect();
        println!("TRUTH T200 cert: phase={} events_pairs={} missed={:?} (expect none)", st.phase, got.len(), missed);
    }
    if which == "all" || which == "disp" {
        for &da in &[5e-4_f64, 2e-3, 8e-3] {
            let b = dispersed_da(100, 20, da);
            run_phase(&b, h, &format!("DISP n=2000 da={da}"));
        }
    }
    if which == "all" || which == "cone" {
        use emergent_encounters::pairs::is_candidate;
        let b = dispersed(100, 80);
        let t = Instant::now();
        if let Some(nb) = Neighbours::new(&b, RHO, 0.0, h) {
            let (all, _) = nb.visit(|_, _| {});
            let mut cand = 0u64;
            nb.visit(|i, j| {
                if is_candidate(&b[i as usize], &b[j as usize], RHO) {
                    cand += 1;
                }
            });
            println!(
                "CONE n=8000: window_pairs={} cone_survivors={} (tier found 396000) t={:.3}s",
                all, cand, t.elapsed().as_secs_f64()
            );
        }
    }
    if which == "all" || which == "n8k" {
        let b = dispersed(100, 80);
        run_phase(&b, h, "SCALE-D m=100 k=80");
        run_tier(&b, h, "SCALE-D-tier m=100 k=80");
    }
    if which == "all" || which == "scale" {
        for &(m, k) in &[(100usize, 10usize), (100, 20), (100, 40)] {
            let b = dispersed(m, k);
            run_phase(&b, h, &format!("SCALE-D m={m} k={k}"));
            run_tier(&b, h, &format!("SCALE-D-tier m={m} k={k}"));
        }
    }
    if which == "all" || which == "ulp" {
        for n in [500usize, 2000] {
            let b0 = tight(n, 0.05, false);
            if let Some(nb) = Neighbours::new(&b0, RHO, 0.0, h) {
                let (c0, k0) = nb.visit(|_, _| {});
                println!("ULP n={n} shared: reach_k={} neighbours={}", k0, c0);
            } else {
                println!("ULP n={n} shared: fallback");
            }
            let b1 = tight(n, 0.05, true);
            if let Some(nb) = Neighbours::new(&b1, RHO, 0.0, h) {
                let (c1, k1) = nb.visit(|_, _| {});
                println!("ULP n={n} broken(+1ulp on one body): reach_k={} neighbours={}", k1, c1);
            } else {
                println!("ULP n={n} broken: fallback");
            }
        }
    }
    if which == "all" || which == "panic" {
        let mut b: Vec<Body> = (0..8).map(|i| Body::new(1.0, 0.0, 0.0, TAU * i as f64 / 8.0)).collect();
        b.push(Body::new(1.0, 1.5, 0.3, 0.0)); // one hyperbolic flyby in the group
        let r = std::panic::catch_unwind(|| {
            group_events(&b, RHO, 0.0, 1.0, |_, _, _, _| {});
        });
        match r {
            Ok(_) => println!("PANIC: no panic (handled)"),
            Err(_) => println!("PANIC: group_events PANICS with one e=1.5 body in the group"),
        }
    }
}
