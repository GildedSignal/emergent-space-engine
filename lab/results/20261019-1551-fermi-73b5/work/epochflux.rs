//! Epoch-flux falsifier (lab run 20261019-1316-scout-e828).
//!
//! Encounters od 1 (the wiki's named decisive experiment): measure leak(E, kappa) on
//! the SHIPPED tier's real Diophantine due structure — e87d's integer replica
//! (`arm_sections` + `arm_pair`'s integer setup + `dioph::first_hit`) plus an epoch
//! dial E (kicks between re-certifications), a horizon dial P (passages: "event due
//! within P"), and a kick-quantum dial kappa. Discriminator between 08d0's protected
//! knee (leak ~0 then ~linear in E, knee ~ 1/kappa^2) and 9fd1's boundary flux
//! (per-interval leak flat in width, coefficient ~ kappa^1): the E-shape at fixed P
//! and the kappa-scaling.
//!
//! Exact in the section integers; floats only build sections (as shipped), exactly
//! like e87d's beatstore (kicks rebuild the Body from its own state).

use emergent_encounters::belt::{make_belt, Rng, Spec};
use emergent_encounters::dioph::first_hit;
use emergent_encounters::kepler::Body;
use emergent_encounters::pairs::cone_pairs;
use emergent_encounters::tier::arm_sections;
use std::f64::consts::TAU;

/// One section's integer rotation, replicating `arm_pair`'s setup at t0 = 0 (e87d's Rot).
struct Rot {
    c0: u64,
    d: u64,
    pi: u64,
    w: u64,
}

fn rots(bi: &Body, bj: &Body, rho: f64, safety: f64) -> Vec<Rot> {
    let mut out = Vec::new();
    for sec in arm_sections(bi, bj, rho, safety) {
        let ti = sec.ti as i128;
        let tj = sec.tj as i128;
        let pi = bi.period as i128;
        let pj = bj.period as i128;
        let ext = pi + 2 * pj;
        let base = tj + (0i128 - ext - tj).div_euclid(pj) * pj;
        let w1 = sec.w1 as i128;
        let w = (w1 + sec.w2 as i128).clamp(0, pi - 1);
        let c0 = (ti - base + w1).rem_euclid(pi);
        let d = (pi - pj.rem_euclid(pi)).rem_euclid(pi);
        out.push(Rot { c0: c0 as u64, d: d as u64, pi: pi as u64, w: w as u64 });
    }
    out
}

/// Pair due: min over its sections of first_hit; sentinel cap+1 when none.
fn pair_due(rs: &[Rot], cap: u128) -> u128 {
    let mut best = cap + 1;
    for r in rs {
        if let Some(k) = first_hit(r.c0 as u128, r.d as u128, r.pi as u128, 0, r.w as u128, &mut 0) {
            if (k as u128) < best {
                best = k as u128;
            }
        }
    }
    best
}

/// Exact kick (e87d's): state at t, add dv along (cos th, sin th), rebuild the Body.
fn kick(b: &Body, t: f64, dv: f64, th: f64) -> Body {
    let s = b.state(t);
    let vx = s[2] + dv * th.cos();
    let vy = s[3] + dv * th.sin();
    let (x, y) = (s[0], s[1]);
    let r = (x * x + y * y).sqrt();
    let v2 = vx * vx + vy * vy;
    let a = 1.0 / (2.0 / r - v2);
    let rv = x * vx + y * vy;
    let ex = (v2 - 1.0 / r) * x - rv * vx;
    let ey = (v2 - 1.0 / r) * y - rv * vy;
    let e = (ex * ex + ey * ey).sqrt();
    let pom = ey.atan2(ex).rem_euclid(TAU);
    let n = a.powf(-1.5);
    let mut ea = if e > 1e-14 { ((1.0 - r / a) / e).clamp(-1.0, 1.0).acos() } else { 0.0 };
    if rv < 0.0 {
        ea = TAU - ea;
    }
    let m = (ea - e * ea.sin()).rem_euclid(TAU);
    let lam0 = (pom + m - n * t).rem_euclid(TAU);
    Body::new(a, e, pom, lam0)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).map(|s| s.as_str()).unwrap_or("book");
    let rho: f64 = 3.34e-6; // design reach B = 5e5 m
    let safety = 1.1; // shipped Phase-A arm
    let seed: u64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(20261018);
    let width: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(1e-4);

    let spec = Spec {
        name: "cell".into(),
        n: 2000,
        sigma_e: 0.07,
        rho,
        a_lo: 2.0,
        a_hi: 2.0 + width,
        keys: 0,
        seed,
        orbits: 1.0,
    };
    let belt = make_belt(&spec);
    let cp = cone_pairs(&belt, rho);
    println!(
        "# bodies {} candidate pairs {} (scan {}) seed {} width {}",
        belt.len(),
        cp.pairs.len(),
        cp.scanned,
        seed,
        width
    );
    let stride = (cp.pairs.len() / 40_000).max(1);
    let sample: Vec<(u32, u32)> = cp.pairs.iter().step_by(stride).copied().collect();
    println!("# sample {} pairs (stride {})", sample.len(), stride);

    if mode == "book" {
        // The real due structure: full-range dues + armed fractions at the horizons.
        let mut dues: Vec<u128> = Vec::new();
        let mut wv: Vec<f64> = Vec::new();
        let mut dv: Vec<f64> = Vec::new();
        let mut piv: Vec<f64> = Vec::new();
        for &(i, j) in sample.iter().take(20_000) {
            let rs = rots(&belt[i as usize], &belt[j as usize], rho, safety);
            for r in &rs {
                wv.push(r.w as f64);
                dv.push(r.d as f64);
                piv.push(r.pi as f64);
            }
            dues.push(pair_due(&rs, 4_000_000));
        }
        let mut ws = wv.clone();
        let mut ds = dv.clone();
        let mut ps = piv.clone();
        let med = |v: &mut Vec<f64>| {
            v.sort_by(|a, b| a.total_cmp(b));
            v[v.len() / 2]
        };
        let w50 = med(&mut ws);
        let d50 = med(&mut ds);
        let pi50 = med(&mut ps);
        dues.sort();
        let n = dues.len() as f64;
        let q = |f: f64| -> f64 { dues[(f * (n - 1.0)) as usize] as f64 };
        let frac = |h: u128| -> f64 { dues.iter().filter(|&&k| k <= h).count() as f64 / n };
        println!(
            "BOOK dues q10 {:.3e} q50 {:.3e} q90 {:.3e} max {:.3e}",
            q(0.10),
            q(0.50),
            q(0.90),
            *dues.last().unwrap() as f64
        );
        println!(
            "BOOK armed(H): H=1 {:.3e} H=16 {:.3e} H=128 {:.3e} H=1000 {:.3e} H=1024 {:.3e} H=1e6 {:.3e}",
            frac(1),
            frac(16),
            frac(128),
            frac(1000),
            frac(1024),
            frac(1_000_000)
        );
        println!(
            "BOOK w p50 {:.1} d p50 {:.3e} pi p50 {:.3e} (ticks) pi/d p50 {:.1}",
            w50, d50, pi50, pi50 / d50
        );
        // due density near 0 (the boundary-flux coefficient's source) vs uniform-phase
        println!(
            "BOOK near-density P(k<=1) {:.3e} P(k<=16)/16 {:.3e} P(k<=128)/128 {:.3e} uniform-1/(pi/d) {:.3e}",
            frac(1),
            frac(16) / 16.0,
            frac(128) / 128.0,
            1.0 / (pi50 / d50)
        );
        return;
    }

    if mode == "smallh" {
        // Per-kick silent->armed flips at small horizons (08d0's protection claim:
        // toy said ~0 at H <= 128; e87d measured no protection at H >= 10^3).
        for (name, qe) in [("dv0", 0i32), ("q26", 26), ("q23", 23), ("q20", 20)] {
            let mut rng = Rng(7);
            let mut armed0 = [0u64; 4];
            let mut flips = [0u64; 4];
            let mut pairs = 0u64;
            for &(i, j) in sample.iter().take(60_000) {
                let bi = &belt[i as usize];
                let bj = &belt[j as usize];
                let rs0 = rots(bi, bj, rho, safety);
                let bk = if qe == 0 {
                    *bi
                } else {
                    kick(bi, 0.0, 2f64.powi(-qe) * bi.vmax(), TAU * rng.f64())
                };
                let rs1 = rots(&bk, bj, rho, safety);
                if rs1.len() != rs0.len() || rs0.is_empty() {
                    continue;
                }
                pairs += 1;
                for (h, &H) in [16u128, 128, 1000, 1_000_000].iter().enumerate() {
                    let a0 = pair_due(&rs0, H) <= H;
                    let a1 = pair_due(&rs1, H) <= H;
                    if a0 {
                        armed0[h] += 1;
                    }
                    if !a0 && a1 {
                        flips[h] += 1;
                    }
                }
            }
            println!(
                "SMALLH {} pairs {}: H=16 flips {:.3e} armed {:.3e} | H=128 flips {:.3e} armed {:.3e} | H=10^3 flips {:.3e} armed {:.3e} | H=10^6 flips {:.3e} armed {:.3e}",
                name,
                pairs,
                flips[0] as f64 / pairs as f64,
                armed0[0] as f64 / pairs as f64,
                flips[1] as f64 / pairs as f64,
                armed0[1] as f64 / pairs as f64,
                flips[2] as f64 / pairs as f64,
                armed0[2] as f64 / pairs as f64,
                flips[3] as f64 / pairs as f64,
                armed0[3] as f64 / pairs as f64
            );
        }
        return;
    }

    if mode == "stream" {
        // Sustained kicked stream; the leak surface leak(E, P) + per-kick base rates.
        let qe: i32 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(23);
        let t_kicks: usize = args.get(5).and_then(|s| s.parse().ok()).unwrap_or(2048);
        let n_pairs: usize = args.get(6).and_then(|s| s.parse().ok()).unwrap_or(1500);
        let rng0: u64 = args.get(7).and_then(|s| s.parse().ok()).unwrap_or(4242);
        let mut rng = Rng(rng0);

        const NP: usize = 4;
        const PS: [u128; NP] = [1, 16, 256, 1024];
        const NE: usize = 6;
        const ES: [usize; NE] = [1, 2, 8, 64, 256, 1024];
        let mut intervals = [[0u64; NP]; NE];
        let mut leaks = [[0u64; NP]; NE];
        let mut armed_per_kick = [0u64; NP];
        let mut flips_on = [0u64; NP];
        let mut kick_events = 0u64;
        let mut shape0 = 0u64;

        for &(i, j) in sample.iter().take(n_pairs) {
            let mut bi = belt[i as usize];
            let mut bj = belt[j as usize];
            let mut prev_armed = [0u16; NP];
            let mut k_grid: Vec<[u16; NP]> = Vec::with_capacity(t_kicks + 1);
            for t in 0..=t_kicks {
                if t > 0 {
                    if qe != 0 {
                        bi = kick(&bi, 0.0, 2f64.powi(-qe) * bi.vmax(), TAU * rng.f64());
                        bj = kick(&bj, 0.0, 2f64.powi(-qe) * bj.vmax(), TAU * rng.f64());
                    }
                    kick_events += 1;
                }
                let rs = rots(&bi, &bj, rho, safety);
                if rs.is_empty() {
                    shape0 += 1;
                }
                let due = pair_due(&rs, PS[NP - 1]);
                let mut row = [0u16; NP];
                for (p, &P) in PS.iter().enumerate() {
                    row[p] = (due <= P) as u16;
                    if t > 0 {
                        armed_per_kick[p] += row[p] as u64;
                        if row[p] == 1 && prev_armed[p] == 0 {
                            flips_on[p] += 1;
                        }
                    }
                    prev_armed[p] = row[p];
                }
                k_grid.push(row);
            }
            // Leak surface: blind interval [t_r, t_r + E): silent at t_r (due > P),
            // true due <= P at some interior t. E=1 has no interior: 0 by construction.
            for (e, &E) in ES.iter().enumerate() {
                let mut t_r = 0usize;
                while t_r < t_kicks {
                    let end = (t_r + E).min(t_kicks);
                    for p in 0..NP {
                        if k_grid[t_r][p] == 0 {
                            intervals[e][p] += 1;
                            let mut hit = false;
                            for t in (t_r + 1)..end {
                                if k_grid[t][p] == 1 {
                                    hit = true;
                                    break;
                                }
                            }
                            if hit {
                                leaks[e][p] += 1;
                            }
                        }
                    }
                    t_r += E;
                }
            }
        }
        println!(
            "STREAM seed {} kappa 2^-{} T {} pairs {} kicks {} shape0 {} rng {}",
            seed, qe, t_kicks, n_pairs.min(sample.len()), kick_events, shape0, rng0
        );
        for (e, &E) in ES.iter().enumerate() {
            let mut s = format!("LEAK E={:>4}", E);
            for p in 0..NP {
                s += &format!(
                    " P={:>4}: {:.3e} ({} / {})",
                    PS[p],
                    leaks[e][p] as f64 / intervals[e][p].max(1) as f64,
                    leaks[e][p],
                    intervals[e][p]
                );
            }
            println!("{}", s);
        }
        for p in 0..NP {
            println!(
                "BASE P={:>4}: armed/kick {:.3e} flips_on/kick {:.3e}",
                PS[p],
                armed_per_kick[p] as f64 / kick_events as f64,
                flips_on[p] as f64 / kick_events as f64
            );
        }
        return;
    }
}
