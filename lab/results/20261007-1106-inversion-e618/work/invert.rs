//! Inversion-lens probe: does the adopted "train" certificate (sort by longitude, watch k~4
//! neighbours) hold at the fleet scale it was adopted for? Measures, at each brute-forced
//! sub-rho closest approach: partner DISTANCE-rank (the gold's metric) and partner
//! LONGITUDE-rank (the order the certificate actually watches), plus the rho-window angular
//! occupancy (the watch width k* the train would need). Scenarios print one JSON line each.

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use std::collections::HashMap;
use std::f64::consts::TAU;
use std::time::Instant;

const RHO: f64 = 1e-4;

fn rayleigh(rng: &mut Rng, s: f64, cap: f64) -> f64 {
    let u = rng.f64();
    (s * (-2.0 * (1.0 - u).ln()).sqrt()).min(cap)
}

fn pct(v: &mut Vec<f64>, q: f64) -> f64 {
    if v.is_empty() {
        return 0.0;
    }
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    v[((q * (v.len() - 1) as f64).round() as usize).min(v.len() - 1)]
}

/// Co-orbital fleet: tight a, Rayleigh e with swept sigma, apsides within +-pom_half of a
/// common direction, mean longitude bunched at sig_lam (Gaussian). Same shape as the gold's
/// fleet(), with sigma_e and the apsidal spread as parameters.
fn fleet(nc: usize, a_hw: f64, sig_e: f64, pom_half: f64, sig_lam: f64, seed: u64) -> Vec<Body> {
    let mut rng = Rng(seed);
    let pom0 = TAU * rng.f64();
    let lam0 = TAU * rng.f64();
    (0..nc)
        .map(|_| {
            let a = 1.0 + (2.0 * rng.f64() - 1.0) * a_hw;
            let e = rayleigh(&mut rng, sig_e, 6.0 * sig_e);
            let pom = pom0 + (2.0 * rng.f64() - 1.0) * pom_half;
            let (u1, u2) = (rng.f64(), rng.f64());
            let z = (-2.0 * (1e-12 + u1).ln()).sqrt() * (TAU * u2).cos();
            Body::new(a, e, pom, lam0 + sig_lam * z)
        })
        .collect()
}

fn wrap(x: f64) -> f64 {
    let a = x.abs().rem_euclid(TAU);
    a.min(TAU - a)
}

struct Probe {
    best: HashMap<(u32, u32), (f64, f64)>, // pair -> (best d, t)
    occ_sum: f64,
    occ_n: u64,
    occ_max: f64,
    occ_bins: usize,
}

/// One step: bin by TRUE longitude (position angle), check same and +-1 bins.
fn step(b: &[Body], pos: &mut Vec<[f64; 2]>, th: &mut Vec<f64>, t: f64, nb: usize, p: &mut Probe) {
    let binsz = TAU / nb as f64;
    let mut head = vec![-1i64; nb];
    let mut nxt = vec![-1i64; b.len()];
    let mut occupied: Vec<usize> = Vec::new();
    for i in 0..b.len() {
        let st = b[i].state(t);
        pos[i] = [st[0], st[1]];
        th[i] = st[1].atan2(st[0]).rem_euclid(TAU);
        let bin = ((th[i] / binsz) as usize).min(nb - 1);
        if head[bin] < 0 {
            occupied.push(bin);
        }
        nxt[i] = head[bin];
        head[bin] = i as i64;
    }
    for &bin in &occupied {
        let mut check = |i: usize, j: usize, p: &mut Probe| {
            let dx = pos[i][0] - pos[j][0];
            let dy = pos[i][1] - pos[j][1];
            let d = dx.hypot(dy);
            if d < 1.3 * RHO {
                let key = if i < j { (i as u32, j as u32) } else { (j as u32, i as u32) };
                let e = p.best.entry(key).or_insert((f64::INFINITY, t));
                if d < e.0 {
                    *e = (d, t);
                }
            }
        };
        let mut a = head[bin];
        while a >= 0 {
            let mut c = nxt[a as usize];
            while c >= 0 {
                check(a as usize, c as usize, p);
                c = nxt[c as usize];
            }
            a = nxt[a as usize];
        }
        for db in 1..=1usize {
            let bin2 = (bin + nb + db) % nb;
            let mut a = head[bin];
            while a >= 0 {
                let mut c = head[bin2];
                while c >= 0 {
                    check(a as usize, c as usize, p);
                    c = nxt[c as usize];
                }
                a = nxt[a as usize];
            }
        }
    }
    // occupancy: bodies within ~rho arc, all bodies, every Kth step (exact, cheap)
    let ths = {
        let mut v = th.clone();
        v.sort_by(|a, b| a.partial_cmp(b).unwrap());
        v
    };
    let w = 1.1 * RHO;
    let n = ths.len();
    for &x in ths.iter() {
        let lo = x - w;
        let hi = x + w;
        let cnt = |a: f64, bnd: f64| ths.partition_point(|&y| y < bnd) - ths.partition_point(|&y| y < a);
        let c = if lo >= 0.0 && hi < TAU {
            cnt(lo, hi)
        } else {
            cnt(lo.rem_euclid(TAU), TAU) + cnt(0.0, hi.rem_euclid(TAU))
        };
        p.occ_sum += c as f64;
        p.occ_n += 1;
        if c as f64 > p.occ_max {
            p.occ_max = c as f64;
        }
    }
    let _ = n;
}

/// Refine d_min by dense resampling +-2dt around the sampled minimum.
fn refine(b: &[Body], i: usize, j: usize, t: f64, dt: f64) -> (f64, f64) {
    let ns = 321;
    let mut best = (f64::INFINITY, t);
    for s in 0..ns {
        let tt = t - 2.0 * dt + 4.0 * dt * s as f64 / (ns - 1) as f64;
        let si = b[i].state(tt);
        let sj = b[j].state(tt);
        let d = (si[0] - sj[0]).hypot(si[1] - sj[1]);
        if d < best.0 {
            best = (d, tt);
        }
    }
    best
}

fn run(
    nc: usize,
    sig_e: f64,
    pom_half: f64,
    sig_lam: f64,
    orbits: f64,
    seed: u64,
    validate: bool,
) {
    let t_start = Instant::now();
    let b = fleet(nc, 1e-5, sig_e, pom_half, sig_lam, seed);
    // conservative relative-velocity bound at conjunction: direction spread ~ 2 * e_cap,
    // plus Kepler shear of the a-spread.
    let e_cap = 6.0 * sig_e;
    let vrel = 2.5 * e_cap + 3.0 * 1e-5 + 1e-6;
    let dt = RHO / (4.0 * vrel);
    let steps = (orbits * TAU / dt) as usize;
    let nb = 6284usize; // bin ~ 1e-3 rad; +-1 bin covers ~ 2e-3 rad >> 1.3 rho arc
    let mut p = Probe { best: HashMap::new(), occ_sum: 0.0, occ_n: 0, occ_max: 0.0, occ_bins: nb };
    let mut pos = vec![[0.0f64; 2]; nc];
    let mut th = vec![0.0f64; nc];
    let t0 = Instant::now();
    for s in 0..steps {
        step(&b, &mut pos, &mut th, s as f64 * dt, nb, &mut p);
    }
    let scan_us = t0.elapsed().as_micros();
    // refine and rank
    let mut keys: Vec<_> = p.best.keys().copied().collect();
    keys.sort_unstable();
    let mut d_rank = Vec::new();
    let mut l_rank = Vec::new();
    let mut il_rad = Vec::new();
    let mut contacts: Vec<(u32, u32, f64)> = Vec::new();
    let mut n_enc = 0usize;
    let t0 = Instant::now();
    for &(i, j) in &keys {
        let (d0, t0_) = p.best[&(i, j)];
        if d0 > 1.2 * RHO {
            continue; // cannot refine into contact
        }
        let (d, t) = refine(&b, i as usize, j as usize, t0_, dt);
        if d <= RHO {
            n_enc += 1;
            contacts.push((i, j, t));
        }
    }
    let refine_us = t0.elapsed().as_micros();
    // rank pass on a stride sample (bounded cost); occupancy below bounds the true max rank
    let stride = contacts.len().div_ceil(4000).max(1);
    let t0 = Instant::now();
    for &(i, j, t) in contacts.iter().step_by(stride) {
        let mut all: Vec<([f64; 2], f64)> = Vec::new();
        for k in 0..nc {
            let st = b[k].state_halley(t); // truth-side solver for the rank pass
            all.push(([st[0], st[1]], st[1].atan2(st[0]).rem_euclid(TAU)));
        }
        let (mut di, mut dj) = (Vec::new(), Vec::new());
        let (mut li, mut lj) = (Vec::new(), Vec::new());
        let (ci, cj) = (all[i as usize], all[j as usize]);
        for k in 0..nc {
            let q = all[k];
            if k != i as usize {
                di.push((((q.0[0] - ci.0[0]).hypot(q.0[1] - ci.0[1])), k));
                li.push((wrap(q.1 - ci.1), k, (q.0[0] * q.0[0] + q.0[1] * q.0[1]).sqrt()));
            }
            if k != j as usize {
                dj.push((((q.0[0] - cj.0[0]).hypot(q.0[1] - cj.0[1])), k));
                lj.push((wrap(q.1 - cj.1), k, (q.0[0] * q.0[0] + q.0[1] * q.0[1]).sqrt()));
            }
        }
        let rank2 = |v: &[(f64, usize)], other: f64| {
            v.iter().filter(|x| x.0 < other - 1e-15).count() as u64
        };
        let rank3 = |v: &[(f64, usize, f64)], other: f64| {
            v.iter().filter(|x| x.0 < other - 1e-15).count() as u64
        };
        let dji = di.iter().find(|x| x.1 == j as usize).unwrap().0;
        let dij = dj.iter().find(|x| x.1 == i as usize).unwrap().0;
        let rdi = rank2(&di, dji);
        let rdj = rank2(&dj, dij);
        let lji = li.iter().find(|x| x.1 == j as usize).unwrap().0;
        let lij = lj.iter().find(|x| x.1 == i as usize).unwrap().0;
        let rli = rank3(&li, lji);
        let rlj = rank3(&lj, lij);
        let dr = rdi.min(rdj) as f64;
        let lr = rli.min(rlj) as f64;
        // radial offsets of the angular interleavers (bodies closer in angle than the partner)
        let ri = (ci.0[0] * ci.0[0] + ci.0[1] * ci.0[1]).sqrt();
        let mut rr: Vec<f64> = li
            .iter()
            .filter(|x| x.0 < lji)
            .map(|x| (x.2 - ri).abs())
            .collect();
        rr.sort_by(|a, b| a.partial_cmp(b).unwrap());
        if !rr.is_empty() {
            il_rad.push(rr[rr.len() / 2]);
        }
        d_rank.push(dr);
        l_rank.push(lr);
    }
    let rank_us = t0.elapsed().as_micros();
    let _ = refine_us;
    let frac_gt = |v: &[f64], k: f64| v.iter().filter(|&&x| x > k).count() as f64 / v.len().max(1) as f64;
    // validation: full pair scan, same dt, tiny config, compare pair sets
    let val = if validate {
        let mut seen: Vec<(u32, u32)> = Vec::new();
        let vs = (0.5 * TAU / dt) as usize;
        for s in 0..vs {
            let t = s as f64 * dt;
            let all: Vec<[f64; 2]> = (0..nc).map(|k| b[k].state(t)).map(|x| [x[0], x[1]]).collect();
            for i in 0..nc {
                for j in (i + 1)..nc {
                    let d = (all[i][0] - all[j][0]).hypot(all[i][1] - all[j][1]);
                    if d < 1.3 * RHO {
                        seen.push((i as u32, j as u32));
                    }
                }
            }
        }
        seen.sort_unstable();
        seen.dedup();
        let grid_pairs = p.best.len();
        let miss: Vec<(u32, u32)> = seen.iter().filter(|p2| !p.best.contains_key(p2)).copied().collect();
        format!(
            "{{\"val_pairs_seen\":{},\"val_grid\":{},\"val_miss\":{}}}",
            seen.len(),
            grid_pairs,
            miss.len()
        )
    } else {
        String::new()
    };
    println!(
        "{{\"nc\":{},\"sig_e\":{},\"pom_half\":{},\"sig_lam\":{},\"seed\":{},\"orbits\":{},\"dt\":{:.2e},\"steps\":{},\"enc\":{},\"enc_sampled\":{},\"scan_us\":{},\"rank_us\":{},\"dist_rank\":{{\"p50\":{:.0},\"p99\":{:.0},\"max\":{:.0},\"gt4\":{:.3}}},\"lon_rank\":{{\"p50\":{:.0},\"p99\":{:.0},\"max\":{:.0},\"gt4\":{:.3},\"gt8\":{:.3},\"gt32\":{:.3}}},\"occ_mean\":{:.1},\"occ_max\":{:.0},\"il_rad_med\":{:.2e}}}",
        nc, sig_e, pom_half, sig_lam, seed, orbits, dt, steps, n_enc, d_rank.len(), scan_us, rank_us,
        pct(&mut d_rank, 0.5), pct(&mut d_rank, 0.99), pct(&mut d_rank, 1.0), frac_gt(&d_rank, 4.0),
        pct(&mut l_rank, 0.5), pct(&mut l_rank, 0.99), pct(&mut l_rank, 1.0), frac_gt(&l_rank, 4.0), frac_gt(&l_rank, 8.0), frac_gt(&l_rank, 32.0),
        p.occ_sum / p.occ_n.max(1) as f64,
        p.occ_max,
        pct(&mut il_rad, 0.5),
    );
    if !val.is_empty() {
        println!("{}", val);
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).map(|s| s.as_str()).unwrap_or("smoke");
    match mode {
        "smoke" => {
            run(200, 0.001, 0.1, 0.01, 1.0, 7, true);
        }
        "sweep" => {
            // nc scaling at the gold's own fleet parameters (sig_e = 0.001, pom +-0.1)
            for &nc in &[200usize, 800, 3200, 12800] {
                run(nc, 0.001, 0.1, 0.01, if nc > 800 { 1.0 } else { 2.0 }, 7, false);
            }
            // e-spread: dispersed fleets (radial breathing 6x and 60x rho)
            for &se in &[0.003, 0.01] {
                for &nc in &[800usize, 3200] {
                    run(nc, se, 0.1, 0.01, if nc > 800 { 1.0 } else { 2.0 }, 7, false);
                }
            }
            // bunch-width scaling at fixed nc
            for &sl in &[0.02, 0.005] {
                run(3200, 0.01, 0.1, sl, 1.0, 7, false);
            }
            // isotropic apsides control
            run(3200, 0.01, std::f64::consts::PI, 0.01, 1.0, 7, false);
            // seed variation on the headline config
            for &sd in &[8u64, 9] {
                run(3200, 0.01, 0.1, 0.01, 1.0, sd, false);
            }
        }
        _ => eprintln!("modes: smoke | sweep"),
    }
}
