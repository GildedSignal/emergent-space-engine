//! Fermi probe A: true encounter rate per body at FIXED distribution (sigma_e = 1e-2,
//! rho = 1e-4, a in [1, 1.5]) as N grows. Truth = the crate's exact conservative-advancement
//! reference (r8 v2's), over the radial-overlap candidate set. One JSON line per belt.

use emergent_encounters::belt::{make_belt, Spec};
use emergent_encounters::pairs::radial_pairs;
use emergent_encounters::par_chunks;
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::time::Instant;

const THREADS: usize = 4;

fn main() {
    let orbits: f64 = 20.0;
    let t_end = orbits * std::f64::consts::TAU;
    for (i, &n) in [1000usize, 2000, 4000].iter().enumerate() {
        let sp = Spec {
            name: format!("fixed-n{n}"),
            n,
            sigma_e: 1e-2,
            rho: 1e-4,
            a_lo: 1.0,
            a_hi: 1.5,
            keys: 0,
            seed: 20261008 + i as u64,
            orbits,
        };
        let b = make_belt(&sp);
        let t0 = Instant::now();
        let pairs = radial_pairs(&b, sp.rho);
        let t_cone = t0.elapsed().as_secs_f64();
        let t1 = Instant::now();
        let parts = par_chunks(pairs.len(), 256, THREADS, |r| {
            let mut out: Vec<(u32, u32)> = Vec::new();
            let mut st = TruthStats::default();
            let mut tmp = Vec::new();
            for &(i, j) in &pairs[r] {
                tmp.clear();
                truth_pair(&b[i as usize], &b[j as usize], sp.rho, t_end, &mut tmp, &mut st);
                for &(t, _d) in &tmp {
                    if t > 0.05 * std::f64::consts::TAU && t < t_end - 0.05 * std::f64::consts::TAU {
                        out.push((i, j));
                    }
                }
            }
            (out, st)
        });
        let mut enc = 0u64;
        let mut st = TruthStats::default();
        for (o, s) in &parts {
            enc += o.len() as u64;
            st.add(s);
        }
        let truth_s = t1.elapsed().as_secs_f64();
        // distinct encounter events per body per orbit
        let per_body_orbit = enc as f64 / (n as f64 * orbits);
        println!(
            "{{\"n\":{},\"pairs\":{},\"enc\":{},\"per_body_orbit\":{:.3e},\"enc_per_body_orbit\":{:.3e},\"truth_steps\":{},\"truth_s\":{:.2},\"cone_s\":{:.3}}}",
            n, pairs.len(), enc, per_body_orbit, per_body_orbit, st.steps, truth_s, t_cone
        );
    }
}
