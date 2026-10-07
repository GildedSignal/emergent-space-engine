//! Taleb lens, 20261007: two swarms on crossing orbits (the fleet engagement). Every prior
//! concentration test (taleb-09b5 + its two checkers) worked intra-clump: one orbit family. Here
//! each swarm is internally tight (the train trigger fires per clump) but the CROSS pairs are the
//! question: does the pairwise tier go quadratic there, does the window tier miss encounters, and
//! does a node-interchange guard (two trains meeting at the <=2 crossing longitudes of the mean
//! orbits, a merge scan in node-passage time) hold with bounded rank?

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{is_candidate, sections};
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::f64::consts::TAU;

/// A tight swarm: a-hw in a, Rayleigh e_spr around e0 plus a hard e_hw spread, pom within +-pom_hw.
fn swarm(n: usize, seed: u64, a0: f64, e0: f64, pom0: f64, a_hw: f64, e_spr: f64, e_hw: f64, pom_hw: f64) -> Vec<Body> {
    let mut rng = Rng(seed);
    (0..n)
        .map(|_| {
            let a = a0 + a_hw * (2.0 * rng.f64() - 1.0);
            let u = rng.f64();
            let e = e0 + e_spr * (-2.0 * (1.0 - u).ln()).sqrt();
            let e = (e + e_hw * (2.0 * rng.f64() - 1.0)).clamp(0.0, 0.9);
            let pom = pom0 + pom_hw * (2.0 * rng.f64() - 1.0);
            let lam = TAU * rng.f64();
            Body::new(a, e, pom, lam)
        })
        .collect()
}

/// Crossing longitudes of two orbits (Binet cone solution), if they cross.
fn node_thetas(bi: &Body, bj: &Body) -> Option<(f64, f64)> {
    let ui = bi.binet();
    let uj = bj.binet();
    let du = ui[0] - uj[0];
    let dv = ui[1] - uj[1];
    let dw = ui[2] - uj[2];
    let r = (dv * dv + dw * dw).sqrt();
    let c = -du / r;
    if !(-1.0..=1.0).contains(&c) {
        return None;
    }
    let base = dw.atan2(dv);
    let w = c.acos();
    Some((base + w, base - w))
}

/// Times in [0, tend) when body b crosses longitude th (prograde: one per revolution).
fn passages(b: &Body, th: f64, tend: f64) -> Vec<f64> {
    let per = b.period as f64 / TICKS;
    let d = |t: f64| -> f64 { (b.state(t)[1].atan2(b.state(t)[0]) - th + std::f64::consts::PI).rem_euclid(TAU) - std::f64::consts::PI };
    let mut out = Vec::new();
    let steps = 96usize;
    let dt = per / steps as f64;
    let mut t = 0.0f64;
    let mut prev = d(0.0);
    while t < tend {
        let tn = (t + dt).min(tend);
        let cur = d(tn);
        if prev < 0.0 && cur >= 0.0 && cur - prev < std::f64::consts::PI {
            let (mut lo, mut hi) = (t, tn);
            for _ in 0..50 {
                let mid = 0.5 * (lo + hi);
                if d(mid) < 0.0 {
                    lo = mid;
                } else {
                    hi = mid;
                }
            }
            out.push(0.5 * (lo + hi));
        }
        prev = cur;
        t = tn;
    }
    out
}

/// Rank of body j (in swarm B, whose node-th passages are pb) among all B bodies by nearest
/// node-passage to the encounter time tt. 0 = the closest B body at that node.
fn node_rank(pb: &[Vec<f64>], j: usize, tt: f64) -> usize {
    let jbest = pb[j].iter().map(|t| (t - tt).abs()).fold(f64::INFINITY, f64::min);
    let mut rank = 0usize;
    for other in pb.iter() {
        let o = other.iter().map(|t| (t - tt).abs()).fold(f64::INFINITY, f64::min);
        if o < jbest - 1e-12 {
            rank += 1;
        }
    }
    rank
}

fn rank_stats(mut ranks: Vec<usize>) -> (usize, usize, usize, usize) {
    if ranks.is_empty() {
        return (0, 0, 0, 0);
    }
    let n = ranks.len();
    ranks.sort_unstable();
    let p99i = ((n as f64 * 0.99) as usize).min(n - 1);
    (n, ranks[n / 2], ranks[p99i], ranks[n - 1])
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let cmd = args.get(1).map(|s| s.as_str()).unwrap_or("help");
    let rho = 1e-4;
    let safety = 1.5;
    let so: u64 = std::env::var("CROSS_SEED").ok().and_then(|s| s.parse().ok()).unwrap_or(0);
    match cmd {
        // ---- control: the gold's regime, one co-orbital formation (replication) ----
        "fleet" => {
            let n_c = 200usize;
            let mut rng = Rng(27);
            let fleet: Vec<Body> = (0..n_c)
                .map(|_| {
                    let a = 1.0 + 1e-5 * (2.0 * rng.f64() - 1.0);
                    let u = rng.f64();
                    let e = 0.001 * (-2.0 * (1.0 - u).ln()).sqrt();
                    Body::new(a, e, TAU * rng.f64(), TAU * rng.f64())
                })
                .collect();
            let mut ff = 0u64;
            for i in 0..n_c {
                for j in (i + 1)..n_c {
                    if is_candidate(&fleet[i], &fleet[j], rho) {
                        ff += 1;
                    }
                }
            }
            println!("fleet control: n_c={n_c} fleet-fleet candidates={ff} of {} (= n_c(n_c-1)/2)", n_c * (n_c - 1) / 2);
        }
        // ---- the engagement: cross-tier economics (no truth) ----
        "econ" => {
            let n_a: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(200);
            let n_b: usize = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(200);
            let h: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(20.0);
            let t_end = h * TAU;
            let sa = swarm(n_a, 101 + so, 1.0, 0.0, 0.0, 1e-5, 0.001, 0.0, 0.1);
            let sb = swarm(n_b, 202 + so, 1.2, 0.3, 0.0, 1e-5, 0.001, 0.0, 0.1);
            // trigger blindness, measured: intra-swarm Binet diameter vs eps_u (the gold's
            let dia = |s: &Vec<Body>| -> (f64, f64) {
                let mut dmax = 0.0f64;
                let mut emax = 0.0f64;
                for i in 0..s.len() {
                    for j in (i + 1)..s.len() {
                        let (ui, uj) = (s[i].binet(), s[j].binet());
                        let d2 = (ui[0] - uj[0]).powi(2) + (ui[1] - uj[1]).powi(2) + (ui[2] - uj[2]).powi(2);
                        dmax = dmax.max(d2.sqrt());
                        emax = emax.max(emergent_encounters::pairs::eps_u(&s[i], &s[j], rho));
                    }
                }
                (dmax, emax)
            };
            let (da, ea) = dia(&sa);
            let (db, eb) = dia(&sb);
            let (mut cross_sep_min, mut cross_sep_max) = (f64::INFINITY, 0.0f64);
            for bi in &sa {
                for bj in &sb {
                    let (ui, uj) = (bi.binet(), bj.binet());
                    let d2 = (ui[0] - uj[0]).powi(2) + (ui[1] - uj[1]).powi(2) + (ui[2] - uj[2]).powi(2);
                    cross_sep_min = cross_sep_min.min(d2.sqrt());
                    cross_sep_max = cross_sep_max.max(d2.sqrt());
                }
            }
            let mut ncand = 0u64;
            for bi in &sa {
                for bj in &sb {
                    if is_candidate(bi, bj, rho) {
                        ncand += 1;
                    }
                }
            }
            let tot = (n_a * n_b) as u64;
            let mut evals = 0u64;
            let mut kinds = [0u64; 3];
            let mut per_pair: Vec<u64> = Vec::with_capacity(4096);
            let mut nsec = 0u64;
            for bi in &sa {
                for bj in &sb {
                    let mut e0 = 0u64;
                    let ss = sections(bi, bj, rho, safety, &mut e0);
                    evals += e0;
                    nsec += ss.len() as u64;
                    for s in &ss {
                        kinds[s.kind as usize] += 1;
                    }
                    if per_pair.len() < 4096 {
                        per_pair.push(e0);
                    }
                }
            }
            per_pair.sort_unstable();
            let mut st = Stats::default();
            let mut hits = 0u64;
            let mut ev: Vec<(f64, f64)> = Vec::new();
            for bi in &sa {
                for bj in &sb {
                    let l = ev.len();
                    pair_events(bi, bj, rho, safety, 0.0, t_end, &mut st, &mut ev);
                    hits += (ev.len() - l) as u64;
                }
            }
            println!(
                "econ n_a={n_a} n_b={n_b} H={h:.0}orbits: intra-diameter A={da:.2e} (max eps_u {ea:.2e}) B={db:.2e} (eps_u {eb:.2e}) | cross Binet sep [{cross_sep_min:.3e},{cross_sep_max:.3e}] | cross-candidates {ncand}/{tot} ({:.1}%) sections={nsec} kinds C/W/F={}/{}/{} setup_evals_total={evals} per-pair p50={} p90={} p100={} | method pairs={} checks={} hits={} evals={} | work_per_hit={:.0}",
                100.0 * ncand as f64 / tot as f64,
                kinds[0], kinds[1], kinds[2],
                per_pair[per_pair.len() / 2],
                per_pair[(per_pair.len() as f64 * 0.9) as usize],
                per_pair[per_pair.len() - 1],
                st.pairs, st.checks_total(), hits, st.evals,
                (evals + st.evals) as f64 / hits.max(1) as f64
            );
        }
        // ---- truth vs method + node-rank guard on the full cross set (small n) ----
        "guard" => {
            let n_a: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(60);
            let n_b: usize = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(60);
            let h: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(6.0);
            let t_end = h * TAU;
            let sa = swarm(n_a, 101 + so, 1.0, 0.0, 0.0, 1e-5, 0.001, 0.0, 0.1);
            let sb = swarm(n_b, 202 + so, 1.2, 0.3, 0.0, 1e-5, 0.001, 0.0, 0.1);
            let (th1, th2) = node_thetas(&sa[n_a / 2], &sb[n_b / 2]).expect("mean orbits cross");
            let pa1: Vec<Vec<f64>> = sa.iter().map(|b| passages(b, th1, t_end)).collect();
            let pa2: Vec<Vec<f64>> = sa.iter().map(|b| passages(b, th2, t_end)).collect();
            let pb1: Vec<Vec<f64>> = sb.iter().map(|b| passages(b, th1, t_end)).collect();
            let pb2: Vec<Vec<f64>> = sb.iter().map(|b| passages(b, th2, t_end)).collect();
            let mut miss = 0u64;
            let mut extra = 0u64;
            let mut true_hits = 0u64;
            let mut meth_hits = 0u64;
            let mut ranks: Vec<usize> = Vec::new();
            let mut jbests: Vec<f64> = Vec::new();
            let mut ibests: Vec<f64> = Vec::new();
            let mut node_off: Vec<f64> = Vec::new();
            let mut tst = TruthStats::default();
            let mut mst = Stats::default();
            for i in 0..n_a {
                for j in 0..n_b {
                    let mut tv = Vec::new();
                    truth_pair(&sa[i], &sb[j], rho, t_end, &mut tv, &mut tst);
                    let mut mv = Vec::new();
                    pair_events(&sa[i], &sb[j], rho, safety, 0.0, t_end, &mut mst, &mut mv);
                    true_hits += tv.len() as u64;
                    let (mut k, mut l) = (0, 0);
                    while k < tv.len() && l < mv.len() {
                        let dt = tv[k].0 - mv[l].0;
                        if dt.abs() < 1e-6 {
                            k += 1;
                            l += 1;
                        } else if dt < 0.0 {
                            miss += 1;
                            k += 1;
                        } else {
                            extra += 1;
                            l += 1;
                        }
                    }
                    miss += (tv.len() - k) as u64;
                    extra += (mv.len() - l) as u64;
                    for (tt, _d) in &tv {
                        // which node does this encounter live at?
                        let mut best = (usize::MAX, f64::INFINITY);
                        for (idx, (pai, pbi)) in [(&pa1[i], &pb1[j]), (&pa2[i], &pb2[j])].iter().enumerate() {
                            let ni = pai.iter().map(|t| (t - tt).abs()).fold(f64::INFINITY, f64::min);
                            let nj = pbi.iter().map(|t| (t - tt).abs()).fold(f64::INFINITY, f64::min);
                            let s = ni + nj;
                            if s < best.1 {
                                best = (idx, s);
                            }
                        }
                        let pb = if best.0 == 0 { &pb1 } else { &pb2 };
                        ranks.push(node_rank(pb, j, *tt));
                        // diagnostics: how far is the encounter from the station passages?
                        let (mut bi_n, mut bj_n, mut lo) = (f64::INFINITY, f64::INFINITY, f64::INFINITY);
                        for th in [th1, th2] {
                            for t in pa1[i].iter().chain(pa2[i].iter()) {
                                bi_n = bi_n.min((t - tt).abs());
                            }
                            for t in pb1[j].iter().chain(pb2[j].iter()) {
                                bj_n = bj_n.min((t - tt).abs());
                            }
                            let s1 = sa[i].state(*tt);
                            let s2 = sb[j].state(*tt);
                            let l1 = s1[1].atan2(s1[0]);
                            let l2 = s2[1].atan2(s2[0]);
                            lo = lo.min((l1 - th).abs().min((l2 - th).abs()));
                        }
                        ibests.push(bi_n);
                        jbests.push(bj_n);
                        node_off.push(lo);
                    }
                }
            }
            let (nr, p50, p99, mx) = rank_stats(ranks);
            let q = |mut v: Vec<f64>| -> String {
                if v.is_empty() {
                    return "none".into();
                }
                v.sort_by(|a, b| a.partial_cmp(b).unwrap());
                format!("p50={:.2e} max={:.2e}", v[v.len() / 2], v[v.len() - 1])
            };
            println!(
                "guard n={n_a}x{n_b} H={h:.0}: true={true_hits} method={meth_hits} missed={miss} extra={extra} | node-time ranks over {nr} encounters: p50={p50} p99={p99} max={mx} | station diag: partner passage dist {} A passage dist {} node long offset {} | truth_evals={} method_evals={}",
                q(jbests), q(ibests), q(node_off),
                tst.evals, mst.evals
            );
        }
        // ---- scale probe of the guard (method-anchored), n growing ----
        "rankscale" => {
            let n: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(120);
            let h: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(4.0);
            let t_end = h * TAU;
            let sa = swarm(n, 101 + so, 1.0, 0.0, 0.0, 1e-5, 0.001, 0.0, 0.1);
            let sb = swarm(n, 202 + so, 1.2, 0.3, 0.0, 1e-5, 0.001, 0.0, 0.1);
            let (th1, th2) = node_thetas(&sa[0], &sb[0]).expect("cross");
            let pa1: Vec<Vec<f64>> = sa.iter().map(|b| passages(b, th1, t_end)).collect();
            let pa2: Vec<Vec<f64>> = sa.iter().map(|b| passages(b, th2, t_end)).collect();
            let pb1: Vec<Vec<f64>> = sb.iter().map(|b| passages(b, th1, t_end)).collect();
            let pb2: Vec<Vec<f64>> = sb.iter().map(|b| passages(b, th2, t_end)).collect();
            let mut ranks: Vec<usize> = Vec::new();
            let mut mst = Stats::default();
            let mut hits = 0u64;
            for i in 0..n {
                for j in 0..n {
                    let mut mv = Vec::new();
                    pair_events(&sa[i], &sb[j], rho, safety, 0.0, t_end, &mut mst, &mut mv);
                    hits += mv.len() as u64;
                    for (tt, _d) in &mv {
                        let mut best = (usize::MAX, f64::INFINITY);
                        for (idx, (pai, pbi)) in [(&pa1[i], &pb1[j]), (&pa2[i], &pb2[j])].iter().enumerate() {
                            let ni = pai.iter().map(|t| (t - tt).abs()).fold(f64::INFINITY, f64::min);
                            let nj = pbi.iter().map(|t| (t - tt).abs()).fold(f64::INFINITY, f64::min);
                            let s = ni + nj;
                            if s < best.1 {
                                best = (idx, s);
                            }
                        }
                        let pb = if best.0 == 0 { &pb1 } else { &pb2 };
                        ranks.push(node_rank(pb, j, *tt));
                    }
                }
            }
            let (nr, p50, p99, mx) = rank_stats(ranks);
            println!("rankscale n={n} H={h:.0}: encounters={hits} | ranks over {nr}: p50={p50} p99={p99} max={mx}");
        }
        _ => println!("commands: fleet | econ [n_a n_b H] | guard [n_a n_b H] | rankscale [n H]"),
    }
}
