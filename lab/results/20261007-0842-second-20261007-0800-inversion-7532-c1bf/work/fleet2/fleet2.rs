//! Second author on run 20261007-0800-inversion-7532 (the checker's named experiment).
//! Implements the gold's ACTUAL watch — k = 4 nearest by current distance, min of both
//! directions — rebuilt on set-change, and measures misses + rebuilds on the inversion's
//! own scenes (same seeds, same `truth_pair`, same rho). The inversion's `events.csv`
//! regenerates bit-identically (make_pop, rank code and dump copied verbatim); the new
//! measurements go to watch-out.jsonl and lead.csv.
//!
//! Watch semantics (see ../predictions.md):
//!   exact policy    : watch = k nearest by distance at the last sample (256/orbit),
//!                     i.e. churn-following rebuild; caught iff j in watch(i) or i in watch(j).
//!   refresh policy  : the same watch frozen at epochs 1 orbit apart.
//!   rebuilds        : watch-entry events (k-set membership changes) per body per orbit.
//!   lead            : t_m - last entry of the partner into either watch before t_m.

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::pairs::radial_pairs;
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::f64::consts::{PI, TAU};

const THREADS: usize = 4;
const K: usize = 4; // the gold's k
const SPO: usize = 256; // watch samples per orbit
const REFRESH_EVERY: usize = SPO; // 1-orbit lazy refresh policy

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

/// Distance rank of j in i's neighbourhood (min of both directions), early exit above 5.
fn dist_rank_at(pos: &[[f64; 2]], i: usize, j: usize) -> usize {
    let (xi, yi) = (pos[i][0], pos[i][1]);
    let (xj, yj) = (pos[j][0], pos[j][1]);
    let dx = xi - xj;
    let dy = yi - yj;
    let dij2 = dx * dx + dy * dy;
    let (mut ci, mut cj) = (0usize, 0usize);
    for (k2, p) in pos.iter().enumerate() {
        if k2 == i || k2 == j {
            continue;
        }
        let dxk = xi - p[0];
        let dyk = yi - p[1];
        if dxk * dxk + dyk * dyk < dij2 {
            ci += 1;
            if ci > 5 && cj > 5 {
                return 6;
            }
        }
        let dxk = p[0] - xj;
        let dyk = p[1] - yj;
        if dxk * dxk + dyk * dyk < dij2 {
            cj += 1;
            if ci > 5 && cj > 5 {
                return 6;
            }
        }
    }
    ci.min(cj)
}

#[inline]
fn insert_k(kd: &mut [f64; K], kid: &mut [u32; K], d2: f64, id: u32) {
    if d2 >= kd[K - 1] {
        return;
    }
    let mut m = K - 1;
    while m > 0 && kd[m - 1] > d2 {
        kd[m] = kd[m - 1];
        kid[m] = kid[m - 1];
        m -= 1;
    }
    kd[m] = d2;
    kid[m] = id;
}

/// k nearest by Euclidean distance for every body: theta-ordered outward scan with the
/// chord lower bound dist >= 2*rmin*sin(dtheta/2) (valid for every pair, rmin = min r).
fn k_nearest(pos: &[[f64; 2]], theta: &[f64], ord: &[u32], rmin: f64, out: &mut Vec<[u32; K]>) {
    let n = pos.len();
    let mut trank = vec![0u32; n];
    for (p2, &b) in ord.iter().enumerate() {
        trank[b as usize] = p2 as u32;
    }
    for i in 0..n {
        let p = trank[i] as usize;
        let ti = theta[i];
        let (xi, yi) = (pos[i][0], pos[i][1]);
        let mut kd = [f64::MAX; K];
        let mut kid = [u32::MAX; K];
        let mut filled = 0usize;
        let mut stop_l = false;
        let mut stop_r = false;
        let mut s = 1usize;
        while s < n && !(stop_l && stop_r) {
            if !stop_r {
                let q = ord[(p + s) % n] as usize;
                let mut dth = (theta[q] - ti).rem_euclid(TAU);
                if dth > PI {
                    dth = TAU - dth;
                }
                let lb = 2.0 * rmin * (0.5 * dth).sin();
                if filled == K && lb * lb >= kd[K - 1] {
                    stop_r = true;
                } else {
                    let dx = xi - pos[q][0];
                    let dy = yi - pos[q][1];
                    let d2 = dx * dx + dy * dy;
                    if filled < K {
                        let mut m = filled;
                        while m > 0 && kd[m - 1] > d2 {
                            kd[m] = kd[m - 1];
                            kid[m] = kid[m - 1];
                            m -= 1;
                        }
                        kd[m] = d2;
                        kid[m] = id_q(q);
                        filled += 1;
                    } else {
                        insert_k(&mut kd, &mut kid, d2, id_q(q));
                    }
                }
            }
            if !stop_l {
                let q = ord[(p + n - s) % n] as usize;
                let mut dth = (ti - theta[q]).rem_euclid(TAU);
                if dth > PI {
                    dth = TAU - dth;
                }
                let lb = 2.0 * rmin * (0.5 * dth).sin();
                if filled == K && lb * lb >= kd[K - 1] {
                    stop_l = true;
                } else {
                    let dx = xi - pos[q][0];
                    let dy = yi - pos[q][1];
                    let d2 = dx * dx + dy * dy;
                    if filled < K {
                        let mut m = filled;
                        while m > 0 && kd[m - 1] > d2 {
                            kd[m] = kd[m - 1];
                            kid[m] = kid[m - 1];
                            m -= 1;
                        }
                        kd[m] = d2;
                        kid[m] = id_q(q);
                        filled += 1;
                    } else {
                        insert_k(&mut kd, &mut kid, d2, id_q(q));
                    }
                }
            }
            s += 1;
        }
        out[i] = kid;
    }
}

#[inline]
fn id_q(q: usize) -> u32 {
    q as u32
}

fn positions_at(bodies: &[Body], t: f64, pos: &mut Vec<[f64; 2]>) {
    for (b, p) in bodies.iter().zip(pos.iter_mut()) {
        let s = b.state(t);
        p[0] = s[0];
        p[1] = s[1];
    }
}

struct WatchResult {
    misses_exact: u64,
    misses_ref: u64,
    no_entry: u64,
    lead_med: f64,
    lead_p10: f64,
    entries_per_body_med: f64,
    entries_per_body_mean: f64,
    entries_total: u64,
    pop_med: Vec<f64>,
    fleet_cross_frac: Option<f64>,
    entries_split: [u64; 4], // [00, 01, 10, 11] by pop of (watcher, entering)

}

fn watch_pass(
    name: &str,
    bodies: &[Body],
    pop_of: &[u8],
    enc: &[(u32, u32, f64, f64)],
    orbits: f64,
    npops: usize,
    lead_dump: &mut String,
) -> WatchResult {
    let n = bodies.len();
    let samples = (orbits as usize) * SPO + 1;
    let dt = TAU / SPO as f64;
    let mut pos: Vec<[f64; 2]> = vec![[0.0; 2]; n];
    let mut theta: Vec<f64> = vec![0.0; n];
    let mut ord: Vec<u32> = (0..n as u32).collect();
    let mut set_cur: Vec<[u32; K]> = vec![[u32::MAX; K]; n];
    let mut set_prev: Vec<[u32; K]> = vec![[u32::MAX; K]; n];
    let mut stale: Vec<[u32; K]> = vec![[u32::MAX; K]; n];
    let mut entries_per_body = vec![0u64; n];
    let mut cross_entries = [0u64; 4]; // [00, 01, 10, 11] by pop of (watcher, entering)
    let mut last_entry: std::collections::HashMap<(u32, u32), f64> =
        std::collections::HashMap::new();
    let mut misses_exact = 0u64;
    let mut misses_ref = 0u64;
    let mut no_entry = 0u64;
    let mut leads: Vec<f64> = Vec::new();
    let mut pos_tm: Vec<[f64; 2]> = vec![[0.0; 2]; n];
    let mut rows = 0u64;
    let mut enc_ptr = 0usize;

    let mut consume_one = |
        enc_ptr: &mut usize,
        set_prev: &Vec<[u32; K]>,
        stale: &Vec<[u32; K]>,
        last_entry: &std::collections::HashMap<(u32, u32), f64>,
    | {
        let (ei, ej, tm, d) = enc[*enc_ptr];
        let (ei, ej) = (ei as usize, ej as usize);
        let caught_exact =
            set_prev[ei].contains(&(ej as u32)) || set_prev[ej].contains(&(ei as u32));
        if !caught_exact {
            misses_exact += 1;
        }
        let caught_ref =
            stale[ei].contains(&(ej as u32)) || stale[ej].contains(&(ei as u32));
        if !caught_ref {
            misses_ref += 1;
        }
        let key = (ei.min(ej) as u32, ei.max(ej) as u32);
        let te = last_entry.get(&key).copied().unwrap_or(-f64::INFINITY);
        let lead;
        if te == -f64::INFINITY {
            no_entry += 1;
            lead = f64::INFINITY;
        } else {
            lead = (tm - te) / TAU;
        }
        leads.push(lead);
        if rows < 100000 {
            positions_at(bodies, tm, &mut pos_tm);
            let dr = dist_rank_at(&pos_tm, ei, ej);
            lead_dump.push_str(&format!(
                "{name},{ei},{ej},{:.4},{:.3e},{dr},{lead:.4},{},{},{}\n",
                tm, d, caught_exact as u8, caught_ref as u8, pop_of[ei]
            ));
            rows += 1;
        }
        *enc_ptr += 1;
    };

    for s in 0..samples {
        let t = s as f64 * dt;
        while enc_ptr < enc.len() && enc[enc_ptr].2 <= t {
            consume_one(&mut enc_ptr, &set_prev, &stale, &last_entry);
        }
        positions_at(bodies, t, &mut pos);
        let mut rmin = f64::MAX;
        for (p, th) in pos.iter().zip(theta.iter_mut()) {
            *th = p[1].atan2(p[0]).rem_euclid(TAU);
            let r2 = p[0] * p[0] + p[1] * p[1];
            if r2 < rmin {
                rmin = r2;
            }
        }
        let rmin = rmin.sqrt();
        ord.sort_unstable_by(|&a, &b| theta[a as usize].partial_cmp(&theta[b as usize]).unwrap());
        k_nearest(&pos, &theta, &ord, rmin, &mut set_cur);
        if s > 0 {
            for i in 0..n {
                for &j in &set_cur[i] {
                    if j != u32::MAX && !set_prev[i].contains(&j) {
                        entries_per_body[i] += 1;
                        cross_entries[pop_of[i] as usize * 2 + pop_of[j as usize] as usize] += 1;
                        let key = (i.min(j as usize) as u32, i.max(j as usize) as u32);
                        last_entry.insert(key, t);
                    }
                }
            }
        }
        if s % REFRESH_EVERY == 0 {
            stale.copy_from_slice(&set_cur);
        }
        set_prev.copy_from_slice(&set_cur);
    }
    while enc_ptr < enc.len() {
        consume_one(&mut enc_ptr, &set_prev, &stale, &last_entry);
    }

    leads.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
    let q = |v: &[f64], p: f64| -> f64 {
        if v.is_empty() {
            return f64::NAN;
        }
        v[((v.len() as f64 - 1.0) * p).round() as usize]
    };
    let mut per_body: Vec<f64> =
        (0..n).map(|i| entries_per_body[i] as f64 / orbits).collect();
    per_body.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
    let bmed = per_body[n / 2];
    let bmean = per_body.iter().sum::<f64>() / n as f64;
    let mut pop_med = Vec::new();
    for p in 0..npops {
        let mut v: Vec<f64> = (0..n)
            .filter(|&i| pop_of[i] as usize == p)
            .map(|i| entries_per_body[i] as f64 / orbits)
            .collect();
        v.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
        pop_med.push(q(&v, 0.5));
    }
    let fleet_cross_frac = if npops == 2 {
        let tot = cross_entries.iter().sum::<u64>();
        Some((cross_entries[1] + cross_entries[2]) as f64 / tot as f64)
    } else {
        None
    };

    let entries_split = cross_entries;

    WatchResult {
        misses_exact,
        misses_ref,
        no_entry,
        lead_med: q(&leads, 0.5),
        lead_p10: q(&leads, 0.1),
        entries_per_body_med: bmed,
        entries_per_body_mean: bmean,
        entries_total: entries_per_body.iter().sum(),
        pop_med,
        fleet_cross_frac,
        entries_split,
    }
}

fn run_scene(
    name: &str,
    pops: &[Pop],
    rho: f64,
    orbits: f64,
    dump: &mut String,
    watch_dump: &mut String,
    lead_dump: &mut String,
) {

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

    // --- the inversion's original per-event analysis (copied verbatim; keeps events.csv
    // --- bit-identical), plus the distance rank at t_m on the same events.
    let lam0 = lam_at(&bodies, 0.0);
    let mut rd = Vec::new();
    let mut rs = Vec::new();
    let mut r1 = Vec::new();
    let mut r10 = Vec::new();
    let mut dr_vec = Vec::new();
    let mut cross = [0u64; 4];
    let mut pair_set = std::collections::HashSet::new();
    let mut rows = 0u64;
    let mut pos_tm: Vec<[f64; 2]> = vec![[0.0; 2]; bodies.len()];
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
        positions_at(&bodies, t, &mut pos_tm);
        let dr = dist_rank_at(&pos_tm, i, j);
        dr_vec.push(dr);
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
    let sdd = stats(&mut dr_vec);
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

    // --- the named experiment: the gold's watch, k = 4 nearest by distance
    let wr = watch_pass(name, &bodies, &pop_of, &enc, orbits, pops.len(), lead_dump);
    let events = enc.len() as u64;
    watch_dump.push_str(&format!(
        "{{\"scene\":\"{name}\",\"events\":{events},\
         \"dist_rank_tm\":{{\"med\":{},\"gt4\":{:.4},\"max\":{}}},\
         \"miss_exact\":{},\"miss_exact_frac\":{:.6},\
         \"miss_ref1\":{},\"miss_ref1_frac\":{:.4},\
         \"no_entry\":{},\"lead_med_orbits\":{:.3},\"lead_p10_orbits\":{:.3},\
         \"entries_total\":{},\"entries_per_body_per_orbit\":{{\"med\":{:.3},\"mean\":{:.3}}},\
         \"pop_med\":[{}],\"fleet_cross_frac\":{},\"entries_split\":[{},{},{},{}]}}\n",
        sdd.median, sdd.frac_gt4, dr_vec.iter().max().copied().unwrap_or(0),
        wr.misses_exact, wr.misses_exact as f64 / events as f64,
        wr.misses_ref, wr.misses_ref as f64 / events as f64,
        wr.no_entry, wr.lead_med, wr.lead_p10,
        wr.entries_total, wr.entries_per_body_med, wr.entries_per_body_mean,
        wr.pop_med.iter().map(|x| format!("{x:.3}")).collect::<Vec<_>>().join(","),
        match wr.fleet_cross_frac {
            Some(f) => format!("{f:.4}"),
            None => "null".into(),
        },
        wr.entries_split[0], wr.entries_split[1], wr.entries_split[2], wr.entries_split[3]
    ));
}

fn main() {
    let mode = std::env::args().nth(1).unwrap_or_else(|| "full".into());
    let mut dump =
        String::from("scene,i,j,t,d,rank_dyn,rank_stat,rank_lag1,rank_lag10,pop_i,pop_j\n");
    let mut watch_dump = String::new();
    let mut lead_dump = String::from(
        "scene,i,j,t_m,d,dist_rank_tm,lead_orbits,caught_exact,caught_ref1,pop_i\n",
    );
    if mode == "smoke" {
        run_scene(
            "B-smoke",
            &[Pop { n: 600, da: 0.0, sigma_e: 0.02, pom_half: 0.2, seed: 22 }],
            1e-3, 4.0, &mut dump, &mut watch_dump, &mut lead_dump,
        );
        println!("{watch_dump}");
        println!("{lead_dump}");
        return;
    }
    // A: control, the gold's regime: tight circular formation, shear-only
    run_scene("A-control", &[Pop { n: 600, da: 1.2e-3, sigma_e: 1e-4, pom_half: 0.0, seed: 11 }], 1e-3, 120.0, &mut dump, &mut watch_dump, &mut lead_dump);
    // B: identical periods, eccentricity-vector spread (a formation after a burn)
    for (s, seed) in [(0.005f64, 21u64), (0.02, 22), (0.05, 23)] {
        run_scene(&format!("B-s{s:.3}"), &[Pop { n: 600, da: 0.0, sigma_e: s, pom_half: 0.2, seed }], 1e-3, 60.0, &mut dump, &mut watch_dump, &mut lead_dump);
    }
    // C: shearing formation (a-spread drives differential precession)
    run_scene("C-shear", &[Pop { n: 600, da: 5e-3, sigma_e: 1e-2, pom_half: 0.2, seed: 31 }], 1e-4, 100.0, &mut dump, &mut watch_dump, &mut lead_dump);
    // D: fleet embedded in a belt (composition)
    run_scene(
        "D-mixed",
        &[
            Pop { n: 200, da: 5e-4, sigma_e: 2e-3, pom_half: 1e-3, seed: 41 },
            Pop { n: 800, da: 1e-2, sigma_e: 1e-2, pom_half: TAU / 2.0, seed: 42 },
        ],
        1e-3, 100.0, &mut dump, &mut watch_dump, &mut lead_dump,
    );
    std::fs::write("events.csv", dump).unwrap();
    std::fs::write("watch-out.jsonl", watch_dump).unwrap();
    std::fs::write("lead.csv", lead_dump).unwrap();
}
