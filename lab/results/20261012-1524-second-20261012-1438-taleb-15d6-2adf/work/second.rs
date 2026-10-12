//! Second-author probes for run 20261012-1524-second-...-taleb-15d6-2adf.
//! The named experiment, extended where the checker was terse:
//!   decomp  — decompose the built cert's reach into angular / equation-of-centre / shear,
//!             and test k_pred = reach * n / TAU against the measured window-k p50.
//!   surgery — does ONE body's eccentricity set the whole fleet's window cost?
//!             (centre is a max over bodies in phase.rs)

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::phase::Neighbours;
use std::collections::HashMap;
use std::f64::consts::TAU;

const RHO: f64 = 1e-4;

fn rayleigh(rng: &mut Rng, s: f64, cap: f64) -> f64 {
    let u = rng.f64();
    (s * (-2.0 * (1.0 - u).ln()).sqrt()).min(cap)
}

/// The checker's fleet() verbatim (spacing_rho <= 0 → uniform λ on the ring).
fn fleet(nc: usize, a_hw: f64, e_sig: f64, e_cap: f64, spacing_rho: f64, seed: u64) -> Vec<Body> {
    let mut rng = Rng(seed);
    let pom0 = TAU * rng.f64();
    let lam0 = TAU * rng.f64();
    let sig_lam = spacing_rho * RHO * nc as f64 / (2.0 * std::f64::consts::PI).sqrt();
    (0..nc)
        .map(|_| {
            let a = 1.0 + (2.0 * rng.f64() - 1.0) * a_hw;
            let e = rayleigh(&mut rng, e_sig, e_cap);
            let pom = pom0 + (2.0 * rng.f64() - 1.0) * 0.1;
            let lam = if spacing_rho <= 0.0 {
                TAU * rng.f64()
            } else {
                let (u1, u2) = (rng.f64(), rng.f64());
                let z = (-2.0 * (1e-12 + u1).ln()).sqrt() * (TAU * u2).cos();
                lam0 + sig_lam * z
            };
            Body::new(a, e, pom, lam)
        })
        .collect()
}

fn pos_of(b: &Body, t: f64) -> [f64; 2] {
    let m = b.mean_anomaly(t);
    let st = b.state_at_mean(m);
    [st[0], st[1]]
}

fn lam_mean0(b: &Body) -> f64 {
    (b.mean_anomaly(0.0) + b.pom).rem_euclid(TAU)
}

fn ang_gap(a: f64, b: f64) -> f64 {
    let d = (a - b).abs().rem_euclid(TAU);
    d.min(TAU - d)
}

/// phase.rs's reach terms, recomputed independently (same formulas, no code sharing).
struct Decomp {
    angular: f64,
    eoc: f64,
    shear: f64,
    eps: f64,
    e_max: f64,
    e_med: f64,
    shared_shape: bool,
}

fn decomp(b: &[Body], rho: f64, t0: f64, t1: f64) -> Decomp {
    let mut nlo = f64::INFINITY;
    let mut nhi = 0.0_f64;
    let mut rmin = f64::INFINITY;
    let mut centre = 0.0_f64;
    let mut es: Vec<f64> = b.iter().map(|x| x.e).collect();
    for x in b {
        nlo = nlo.min(x.n);
        nhi = nhi.max(x.n);
        rmin = rmin.min(x.rmin());
        centre = centre.max(x.e + 2.0 * (x.e / (1.0 + x.sq)).asin());
    }
    es.sort_by(|a, c| a.total_cmp(c));
    let e_med = es[es.len() / 2];
    let e_max = es[es.len() - 1];
    let mut angular = 2.0 * (rho / (2.0 * rmin)).min(1.0).asin();
    let shared_shape = b
        .first()
        .map(|f| b.iter().all(|x| x.e == f.e && x.pom == f.pom))
        .unwrap_or(false);
    if shared_shape {
        let e0 = b[0].e;
        angular *= (1.0 + e0).powf(1.5) / (1.0 - e0).sqrt();
    }
    let c2 = if shared_shape { 0.0 } else { 2.0 * centre };
    Decomp {
        angular,
        eoc: c2,
        shear: (nhi - nlo) * (t1 - t0) * 0.5,
        eps: 64.0 * f64::EPSILON * (1.0 + nhi * t0.abs().max(t1.abs())),
        e_max,
        e_med,
        shared_shape,
    }
}

fn kdists(f: &[Body], reach: f64) -> (u64, u64, u64, u64, u64) {
    let nc = f.len();
    let mut lam: Vec<(f64, usize)> = (0..nc).map(|i| (lam_mean0(&f[i]), i)).collect();
    lam.sort_unstable_by(|a, b| a.0.total_cmp(&b.0));
    let mut ks: Vec<u64> = Vec::with_capacity(nc);
    let mut end = 1usize;
    for start in 0..nc {
        end = end.max(start + 1);
        while end < start + nc
            && lam[end % nc].0 + if end >= nc { TAU } else { 0.0 } - lam[start].0 <= reach
        {
            end += 1;
        }
        ks.push((end - start - 1) as u64);
    }
    ks.sort_unstable();
    let q = |fr: f64| ks.get((fr * (ks.len() as f64 - 1.0)) as usize).copied().unwrap_or(0);
    (q(0.5), q(0.9), q(0.99), q(1.0), ks.iter().map(|x| x + 1).sum::<u64>())
}

/// t=0 contacts by position grid; miss if mean-lambda gap > reach (cert's own guarantee).
fn contacts_t0(f: &[Body], reach: f64) -> (u64, u64) {
    let nc = f.len();
    let mut pos = vec![[0.0f64; 2]; nc];
    let mut head: HashMap<(i64, i64), i64> = HashMap::with_capacity(nc);
    let mut nxt = vec![-1i64; nc];
    for i in 0..nc {
        pos[i] = pos_of(&f[i], 0.0);
        let key = ((pos[i][0] / RHO).floor() as i64, (pos[i][1] / RHO).floor() as i64);
        let e = head.entry(key).or_insert(-1);
        nxt[i] = *e;
        *e = i as i64;
    }
    let keys: Vec<(i64, i64)> = head.keys().copied().collect();
    let (mut pairs, mut miss) = (0u64, 0u64);
    for key in &keys {
        for (dx, dy) in [(0, 0), (1, 0), (0, 1), (1, 1), (-1, 1)] {
            let h2 = match head.get(&(key.0 + dx, key.1 + dy)) {
                Some(&h) => h,
                None => continue,
            };
            let mut p = head[key];
            while p >= 0 {
                let mut q = if (dx, dy) == (0, 0) { nxt[p as usize] } else { h2 };
                while q >= 0 {
                    let d = (pos[p as usize][0] - pos[q as usize][0])
                        .hypot(pos[p as usize][1] - pos[q as usize][1]);
                    if d < RHO {
                        pairs += 1;
                        if ang_gap(lam_mean0(&f[p as usize]), lam_mean0(&f[q as usize])) > reach {
                            miss += 1;
                        }
                    }
                    q = nxt[q as usize];
                }
                p = nxt[p as usize];
            }
        }
    }
    (pairs, miss)
}

fn one(name: &str, f: &[Body], t0: f64, t1: f64) {
    let nb = Neighbours::new(f, RHO, t0, t1).expect("phase gate refused");
    let d = decomp(f, RHO, t0, t1);
    let (p50, p90, p99, _max, tot) = kdists(f, nb.reach);
    let kpred = nb.reach * f.len() as f64 / TAU;
    let eoc_share = d.eoc / nb.reach;
    println!(
        "{{\"decomp\":\"{name}\",\"n\":{},\"reach\":{:.4e},\"terms\":{{\"angular\":{:.4e},\"eoc\":{:.4e},\"shear\":{:.4e},\"eps\":{:.3e}}},\"eoc_share\":{:.3},\"e_max\":{:.4e},\"e_med\":{:.4e},\"e_ratio\":{:.1},\"shared_shape\":{},\"k\":{{\"pred\":{:.0},\"p50\":{},\"p90\":{},\"p99\":{}}},\"visits_total\":{},\"pred_over_p50\":{:.3}}}",
        f.len(), nb.reach, d.angular, d.eoc, d.shear, d.eps, eoc_share,
        d.e_max, d.e_med, d.e_max / d.e_med.max(1e-12), d.shared_shape,
        kpred, p50, p90, p99, tot, kpred / p50.max(1) as f64,
    );
}

fn main() {
    let which = std::env::args().nth(1).unwrap_or_default();
    match which.as_str() {
        "decomp" => {
            one("tight-1e6", &fleet(1_000_000, 1e-5, 1e-5, 1e-4, 0.0, 62), 0.0, 0.0);
            one("gold-e-1e6", &fleet(1_000_000, 1e-5, 1e-3, 1e-2, 0.0, 63), 0.0, 0.0);
            // the gold's own adj scene and the espread scene, at snap
            one("adj-200-h1", &fleet(200, 1e-5, 1e-3, 1e-2, 1.25, 27), 0.0, 2.0 * TAU);
            one("espread-200-h2", &fleet(200, 1e-5, 1e-2, 5e-2, 1.25, 51), 0.0, 2.0 * TAU);
            // the builder's gate fleet: shared shape, uniform ring (cancellation fires)
            one("builder-gate-ring-1e6", &(0..1_000_000).map(|i| Body::new(1.0, 0.02, 0.0, TAU * i as f64 / 1e6)).collect::<Vec<_>>(), 0.0, TAU);
        }
        "surgery" => {
            let mut f = fleet(1_000_000, 1e-5, 1e-3, 1e-2, 0.0, 63);
            let (p50a, _, _, _, visa) = {
                let nb = Neighbours::new(&f, RHO, 0.0, 0.0).unwrap();
                kdists(&f, nb.reach)
            };
            let (cta, _) = contacts_t0(&f, Neighbours::new(&f, RHO, 0.0, 0.0).unwrap().reach);
            // surgery 1: the single worst-e body → fleet median e
            let mut es: Vec<f64> = f.iter().map(|x| x.e).collect();
            let worst = f
                .iter()
                .enumerate()
                .max_by(|a, b| a.1.e.total_cmp(&b.1.e))
                .unwrap()
                .0;
            es.sort_by(|a, b| a.total_cmp(b));
            let med = es[es.len() / 2];
            let keep = f[worst];
            let lam0 = lam_mean0(&keep);
            f[worst] = Body::new(keep.a, med, keep.pom, lam0);
            let nb1 = Neighbours::new(&f, RHO, 0.0, 0.0).unwrap();
            let (p50b, _, _, _, visb) = kdists(&f, nb1.reach);
            let (ctb, missb) = contacts_t0(&f, nb1.reach);
            println!(
                "{{\"surgery\":\"worst-to-median\",\"e_was\":{:.4e},\"e_now\":{:.4e},\"reach_now\":{:.4e},\"k_p50\":{{\"before\":{},\"after\":{}}},\"visits\":{{\"before\":{},\"after\":{}}},\"contacts_t0\":{{\"before\":{},\"after\":{},\"pct\":{:.2}}},\"window_miss_after\":{}}}",
                keep.e, med, nb1.reach, p50a, p50b, visa, visb, cta, ctb,
                100.0 * ctb as f64 / cta.max(1) as f64, missb,
            );
            // surgery 2: worst 10 bodies → 99.9th percentile e
            let mut idx: Vec<usize> = (0..f.len()).collect();
            idx.sort_by(|&a, &b| f[a].e.total_cmp(&f[b].e));
            let p999 = es[(es.len() as f64 * 0.999) as usize];
            let hot: Vec<usize> = idx[f.len() - 10..].to_vec();
            for &i in &hot {
                let lam0 = lam_mean0(&f[i]);
                let keep = f[i];
                f[i] = Body::new(keep.a, p999.min(keep.e), keep.pom, lam0);
            }
            let nb2 = Neighbours::new(&f, RHO, 0.0, 0.0).unwrap();
            let (p50c, _, _, _, visc) = kdists(&f, nb2.reach);
            let (ctc, missc) = contacts_t0(&f, nb2.reach);
            println!(
                "{{\"surgery\":\"top10-to-p99.9\",\"e_p999\":{:.4e},\"reach_now\":{:.4e},\"k_p50\":{}}},\"visits\":{},\"contacts_t0\":{},\"pct\":{:.2},\"window_miss\":{}}}",
                p999, nb2.reach, p50c, visc, ctc, 100.0 * ctc as f64 / cta.max(1) as f64, missc,
            );
        }
        "scaling" => {
            // k at fixed e-spread as n grows: the quadratic-in-n test (uniform lambda).
            for n in [100_000usize, 316_228, 1_000_000] {
                one(&format!("gold-e-scaling-{n}"), &fleet(n, 1e-5, 1e-3, 1e-2, 0.0, 63), 0.0, 0.0);
            }
        }
        "treefall" => {
            // what the fallback (tree tier) costs on the same fleets as the phase tier.
            use emergent_encounters::tier::{traverse, Tree, TreeStats};
            for n in [100_000usize, 1_000_000] {
                let f = fleet(n, 1e-5, 1e-3, 1e-2, 0.0, 63);
                let t0 = std::time::Instant::now();
                let tree = Tree::new(&f, 32);
                let mut st = TreeStats::default();
                let mut pairs = 0u64;
                traverse(&tree, &f, RHO, true, &mut |_, _| pairs += 1, &mut st);
                println!(
                    "{{\"treefall\":\"gold-e-{n}\",\"n\":{n},\"candidate_pairs\":{pairs},\"node_tests\":{},\"leafpair_tests\":{},\"build_traverse_ms\":{}}}",
                    st.node_tests, st.leafpair_tests, t0.elapsed().as_millis()
                );
                drop(tree);
            }
        }
        _ => eprintln!("usage: second decomp|surgery|scaling|treefall"),
    }
}
