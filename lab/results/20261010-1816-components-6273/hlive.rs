//! Lab run 20261010-1816 (components lens): H_live — distinctions created per orbit in a
//! stirred belt, measured on the law's integer grid (period/periapsis in ticks of 2^-32
//! time units; e and angle at 2^24 fractional bits, sensitivity checked at 2^16).
//!
//! Pass 1 (`scan`): every encounter of the genesis belt through the verified cone
//!   candidate set + exact per-pair checks (r8 v3's machinery, untouched).
//! Pass 2 (`sweep`): for each belt-body mass mu_b, apply mutual impulse-approximation
//!   kicks at each encounter in time order (per-body sequential refit), and measure the
//!   scar store: quantized element increments, their empirical order-0 entropy, the
//!   first-distinction address cost, and the min(scar, fresh-slot) rebind total.
//! Pass 3 (`feedback`): windowed run with kicks fed back into the candidate set, to check
//!   the frozen-geometry approximation of pass 2 on the event rate.
//!
//! Std only. One JSON line per phase.

use emergent_encounters::belt::{make_belt, Spec};
use emergent_encounters::kepler::Body;
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::cone_pairs;
use std::collections::HashMap;
use std::f64::consts::TAU;

const THREADS: usize = 4;
const SAFETY: f64 = 1.1;
/// A fresh quantized element set: period 35b + periapsis 35b + e 24b + angle 24b (+ slot).
const FRESH_SLOT_BITS: f64 = 130.0;

fn entropy<T: Eq + std::hash::Hash>(counts: &HashMap<T, u64>) -> f64 {
    let total: u64 = counts.values().sum();
    if total == 0 {
        return 0.0;
    }
    let t = total as f64;
    counts.values().map(|&c| { let p = c as f64 / t; -p * p.log2() }).sum()
}

/// Kepler elements (mu = 1) from a cartesian state, back onto the law's integer grid.
fn refit(x: f64, y: f64, vx: f64, vy: f64, t: f64) -> Body {
    let r = (x * x + y * y).sqrt();
    let v2 = vx * vx + vy * vy;
    let a = 1.0 / (2.0 / r - v2);
    let rv = x * vx + y * vy;
    let k = v2 - 1.0 / r;
    let ex = k * x - rv * vx;
    let ey = k * y - rv * vy;
    let e = (ex * ex + ey * ey).sqrt();
    let pom = ey.atan2(ex);
    let ea = (rv / a.sqrt()).atan2(1.0 - r / a);
    let m = ea - e * ea.sin();
    let n = a.powf(-1.5);
    Body::new(a, e, pom, pom + m - n * t)
}

/// One mutual encounter kick: impulse approximation, b ~ d (closest-approach distance),
/// equal belt-body masses, momentum conserved. Returns nothing; refits both bodies.
fn kick_pair(bi: &mut Body, bj: &mut Body, t: f64, d: f64, mu_b: f64) {
    let si = bi.state(t);
    let sj = bj.state(t);
    let rvx = sj[2] - si[2];
    let rvy = sj[3] - si[3];
    let u = (rvx * rvx + rvy * rvy).sqrt();
    if !(u > 0.0) {
        return;
    }
    let px = -rvy / u;
    let py = rvx / u;
    let mut s = (sj[0] - si[0]) * px + (sj[1] - si[1]) * py;
    if s == 0.0 {
        s = 1.0;
    }
    let dv = 2.0 * mu_b / (u * d);
    let (dvx, dvy) = (dv * px * s.signum(), dv * py * s.signum());
    *bi = refit(si[0], si[1], si[2] + dvx, si[3] + dvy, t);
    *bj = refit(sj[0], sj[1], sj[2] - dvx, sj[3] - dvy, t);
}

/// Quantized increments of the law's stored integers, new minus old (circular fields).
fn delta(new: &Body, old: &Body, ebits: i32) -> [i64; 4] {
    let dp = new.period as i64 - old.period as i64;
    let p = old.period as f64;
    let dtp = ((new.tp as f64 - old.tp as f64) + p / 2.0).rem_euclid(p) - p / 2.0;
    let q = (1u64 << ebits) as f64;
    let de = ((new.e - old.e) * q).round() as i64;
    let dw = ((((new.pom - old.pom) + TAU / 2.0).rem_euclid(TAU) - TAU / 2.0) / TAU * q).round() as i64;
    [dp, dtp.round() as i64, de, dw]
}

struct Acc {
    hist: [HashMap<i64, u64>; 4],
    mask: HashMap<u8, u64>,
    joint_dp_d: Vec<HashMap<i64, u64>>, // d-bin -> dp histogram
    updates: u64,
    nonzero_updates: u64,
    distinct: Vec<u32>,
    scar_bits: Vec<f64>,
    genesis_bits_per_body: f64,
    genesis_distinct: usize,
    /// Per body: every nonzero (field, value) it ever produced (true self-information).
    vals: Vec<Vec<(u8, i64)>>,
    max_rel_dp: f64,
}

impl Acc {
    fn new(n: usize) -> Self {
        Acc {
            hist: Default::default(),
            mask: Default::default(),
            joint_dp_d: (0..4).map(|_| Default::default()).collect(),
            updates: 0,
            nonzero_updates: 0,
            distinct: Vec::new(),
            scar_bits: vec![0.0; n],
            genesis_bits_per_body: 0.0,
            genesis_distinct: 0,
            vals: vec![Vec::new(); n],
            max_rel_dp: 0.0,
        }
    }

    fn record(&mut self, id: u32, d_rho: f64, dv: &[i64; 4]) {
        self.updates += 1;
        let mut mask = 0u8;
        let mut bits = 0.0f64;
        for (f, &v) in dv.iter().enumerate() {
            if v != 0 {
                mask |= 1 << f;
                *self.hist[f].entry(v).or_default() += 1;
                self.vals[id as usize].push((f as u8, v));
                bits += 1.0; // first-distinction detector only; bits recomputed at the end
            }
        }
        if mask == 0 {
            return;
        }
        if dv[0] != 0 {
            let bin = ((d_rho * 4.0) as usize).min(3);
            *self.joint_dp_d[bin].entry(dv[0]).or_default() += 1;
        }
        self.nonzero_updates += 1;
        *self.mask.entry(mask).or_default() += 1;
        self.scar_bits[id as usize] += bits;
        if self.scar_bits[id as usize] == bits {
            self.distinct.push(id); // first distinction
        }
    }

    /// Final bits from the measured histograms (order-0, self-coded).
    fn summarize(&self, n: usize, orbits: f64) -> serde_json_ish::Val {
        let fields = ["dP", "dtp", "de", "dpom"];
        let mut fh = Vec::new();
        let mut bits_per_update = entropy(&self.mask);
        let mut per_field = Vec::new();
        for f in 0..4 {
            let tot: u64 = self.hist[f].values().sum();
            let h = entropy(&self.hist[f]);
            let frac = if self.updates > 0 { tot as f64 / self.updates as f64 } else { 0.0 };
            bits_per_update += frac * h;
            per_field.push(format!("{}={:.2}b@{:.3}", fields[f], h, frac));
            fh.push(tot);
        }
        let h_dp = entropy(&self.hist[0]);
        let h_dp_cond = {
            // H(dp | d-bin) = H(dp, bin) - H(bin)
            let mut joint: HashMap<(u64, i64), u64> = HashMap::new();
            let mut bins: HashMap<u64, u64> = HashMap::new();
            for (b, h) in self.joint_dp_d.iter().enumerate() {
                for (v, &c) in h {
                    *joint.entry((b as u64, *v)).or_default() += c;
                    *bins.entry(b as u64).or_default() += c;
                }
            }
            entropy(&joint) - entropy(&bins)
        };
        // first-distinction address: entropy of sorted id gaps
        let mut ids = self.distinct.clone();
        ids.sort_unstable();
        let gaps: Vec<i64> = ids.windows(2).map(|w| (w[1] - w[0]) as i64).collect();
        let mut gh: HashMap<i64, u64> = HashMap::new();
        for g in gaps {
            *gh.entry(g).or_default() += 1;
        }
        let addr_bits = entropy(&gh) + 1.0;
        // store total: min(scar bits + address once, fresh slot)
        let tot: Vec<u64> = self.hist.iter().map(|h| h.values().sum::<u64>()).collect();
        let self_info = |f: u8, v: i64| -> f64 {
            let c = *self.hist[f as usize].get(&v).unwrap_or(&1) as f64;
            let t = tot[f as usize].max(1) as f64;
            -(c / t).log2()
        };
        let mut total = 0.0f64;
        let mut rebound = 0usize;
        for id in &ids {
            let scar: f64 = self.vals[*id as usize].iter().map(|&(f, v)| self_info(f, v)).sum();
            let b = (scar + addr_bits).min(FRESH_SLOT_BITS);
            if scar + addr_bits >= FRESH_SLOT_BITS {
                rebound += 1;
            }
            total += b;
        }
        serde_json_ish::obj(&[
            ("n", n.to_string()),
            ("orbits", format!("{orbits}")),
            ("updates", self.updates.to_string()),
            ("nonzero_updates", self.nonzero_updates.to_string()),
            ("distinct", ids.len().to_string()),
            ("events_per_body_per_orbit", format!("{:.5}", self.updates as f64 / 2.0 / n as f64 / orbits)),
            ("bits_per_update_order0", format!("{bits_per_update:.2}")),
            ("max_rel_dP", format!("{:e}", self.max_rel_dp)),
            ("fields", format!("\"{{{}}}\"", per_field.join(", "))),
            ("addr_bits_first", format!("{addr_bits:.2}")),
            ("h_dp", format!("{h_dp:.2}")),
            ("h_dp_given_dbin", format!("{h_dp_cond:.2}")),
            ("genesis_bits_per_body", format!("{:.3}", self.genesis_bits_per_body)),
            ("genesis_distinct", self.genesis_distinct.to_string()),
            ("store_bits_total", format!("{total:.0}")),
            ("store_bits_per_body", format!("{:.3}", total / n as f64)),
            ("store_MB_per_1e9", format!("{:.0}", total / n as f64 * 1e9 / 8.0 / 1e6)),
            ("rebound", rebound.to_string()),
        ])
    }
}

/// Pass 1: every encounter of the belt, as (i, j, t, d), time-sorted.
fn scan(belt: &[Body], rho: f64, orbits: f64) -> (Vec<(u32, u32, f64, f64)>, Stats, u64) {
    let cs = cone_pairs(belt, rho);
    let pairs = cs.pairs;
    let scanned = cs.scanned;
    let mut st = Stats::default();
    let parts = emergent_encounters::par_chunks(pairs.len(), 256, THREADS, |r| {
        let mut local = Vec::new();
        let mut st = Stats::default();
        for &p in &pairs[r] {
            let (i, j) = (p.0 as usize, p.1 as usize);
            let mut ev = Vec::new();
            pair_events(&belt[i], &belt[j], rho, SAFETY, 0.0, orbits, &mut st, &mut ev);
            for &(t, d) in &ev {
                local.push((p.0, p.1, t, d));
            }
        }
        (local, st)
    });
    let mut events = Vec::new();
    for (mut p, mut s) in parts {
        events.append(&mut p);
        st.add(&s);
    }
    events.sort_by(|a, b| a.2.total_cmp(&b.2));
    (events, st, scanned)
}

/// Pass 2: apply kicks in time order at this mu_b, measure the scar store at two grids.
fn sweep(belt: &[Body], events: &[(u32, u32, f64, f64)], rho: f64, mu_b: f64, ebits: i32) -> Acc {
    let mut bodies = belt.to_vec();
    let n = bodies.len();
    let mut acc = Acc::new(n);
    for &(i, j, t, d) in events {
        let (oi, oj) = (bodies[i as usize], bodies[j as usize]);
        let (lo, hi) = if i < j { bodies.split_at_mut(j as usize) } else { bodies.split_at_mut(i as usize) };
        let (a, b) = if i < j { (&mut lo[i as usize], &mut hi[0]) } else { (&mut hi[0], &mut lo[j as usize]) };
        kick_pair(a, b, t, d, mu_b);
        acc.record(i, d / rho, &delta(&bodies[i as usize], &oi, ebits));
        acc.record(j, d / rho, &delta(&bodies[j as usize], &oj, ebits));
    }
    // Genesis-anchored (reabsorption) accounting: each body's FINAL quantized offset from
    // its genesis elements, entropy over the population (nonzero offsets only).
    let mut gh: [HashMap<i64, u64>; 4] = Default::default();
    let mut nd = 0usize;
    for (b, g) in bodies.iter().zip(belt.iter()) {
        let d = delta(b, g, 24);
        if d.iter().any(|&v| v != 0) {
            nd += 1;
            for (f, &v) in d.iter().enumerate() {
                if v != 0 {
                    *gh[f].entry(v).or_default() += 1;
                }
            }
        }
    }
    let hb: f64 = gh.iter().map(|h| entropy(h)).sum();
    let addr = if nd > 0 { (n as f64 / nd as f64).log2().max(0.0) } else { 0.0 };
    acc.genesis_bits_per_body = if nd > 0 { hb + addr } else { 0.0 };
    acc.genesis_distinct = nd;
    acc.max_rel_dp = bodies
        .iter()
        .zip(belt.iter())
        .map(|(b, g)| (b.period as f64 - g.period as f64).abs() / g.period as f64)
        .fold(0.0f64, f64::max);
    acc
}

/// Pass 3: windowed run with kicks fed back into the candidates (geometry no longer frozen).
fn feedback(spec: &Spec, rho: f64, mu_b: f64, window: f64, ebits: i32) -> (u64, usize) {
    let mut bodies = make_belt(spec);
    let mut acc = Acc::new(bodies.len());
    let mut t0 = 0.0;
    while t0 < spec.orbits {
        let t1 = (t0 + window).min(spec.orbits);
        let (ev, _, _) = scan(&bodies, rho, t1);
        let ev: Vec<_> = ev.into_iter().filter(|e| e.2 >= t0 && e.2 < t1).collect();
        for &(i, j, t, d) in &ev {
            let (oi, oj) = (bodies[i as usize], bodies[j as usize]);
            let (lo, hi) = if i < j { bodies.split_at_mut(j as usize) } else { bodies.split_at_mut(i as usize) };
            let (a, b) = if i < j { (&mut lo[i as usize], &mut hi[0]) } else { (&mut hi[0], &mut lo[j as usize]) };
            kick_pair(a, b, t, d, mu_b);
            acc.record(i, d / rho, &delta(&bodies[i as usize], &oi, ebits));
            acc.record(j, d / rho, &delta(&bodies[j as usize], &oj, ebits));
        }
        t0 = t1;
    }
    (acc.updates / 2, acc.distinct.len())
}

/// Tiny hand-rolled JSON emission (std only, no serde in this crate).
mod serde_json_ish {
    pub type Val = String;
    pub fn obj(pairs: &[(&str, String)]) -> String {
        let body: Vec<String> = pairs.iter().map(|(k, v)| format!("\"{k}\":{v}")).collect();
        format!("{{{}}}", body.join(","))
    }
}

fn spec(n: usize, sigma_e: f64, rho: f64, a_lo: f64, a_hi: f64, orbits: f64, seed: u64) -> Spec {
    Spec { name: "hlive".into(), n, sigma_e, rho, a_lo, a_hi, keys: 0, seed, orbits }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).map(String::as_str).unwrap_or("all");
    // Shared "main" belt (tuned on): wide, r8-like.
    let n: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(2000);
    let sigma_e: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(1e-2);
    let rho: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(1e-3);
    let a_lo: f64 = args.get(5).and_then(|s| s.parse().ok()).unwrap_or(1.0);
    let a_hi: f64 = args.get(6).and_then(|s| s.parse().ok()).unwrap_or(1.5);
    let orbits: f64 = args.get(7).and_then(|s| s.parse().ok()).unwrap_or(100.0);
    let seed: u64 = args.get(8).and_then(|s| s.parse().ok()).unwrap_or(20261010);
    let sp = spec(n, sigma_e, rho, a_lo, a_hi, orbits, seed);
    let belt = make_belt(&sp);

    if mode == "scan" || mode == "all" {
        let t0 = std::time::Instant::now();
        let (events, st, scanned) = scan(&belt, rho, orbits);
        println!(
            "{{\"phase\":\"scan\",\"belt\":\"n={n} sig={sigma_e} rho={rho} a=[{a_lo},{a_hi}] orbits={orbits} seed={seed}\",\"candidates\":{},\"scanned\":{scanned},\"events\":{},\"checks\":{},\"pairs\":{},\"sec\":{:.2}}}",
            scanned, events.len(), st.checks_total(), st.pairs, t0.elapsed().as_secs_f32()
        );
        // Pass 2 over the mass sweep, both grids.
        for &mu_b in &[
            0.0f64, 1e-26, 1e-24, 1e-22, 1e-21, 3e-21, 1e-20, 3e-20, 1e-19, 1e-18, 1e-16, 1e-14, 1e-12,
        ] {
            let a24 = sweep(&belt, &events, rho, mu_b, 24);
            let v24 = a24.summarize(n, orbits);
            let a16 = sweep(&belt, &events, rho, mu_b, 16);
            let v16 = a16.summarize(n, orbits);
            let (d24, d16) = (a24.nonzero_updates, a16.nonzero_updates);
            let frac = if a24.updates > 0 { d24 as f64 / a24.updates as f64 } else { 0.0 };
            println!(
                "{{\"phase\":\"sweep\",\"mu_b\":{mu_b:e},\"distinct_frac_of_updates\":{frac:.4},\"grid24\":{v24},\"grid16\":{v16}}}"
            );
        }
    }

    if mode == "feedback" {
        for &mu_b in &[1e-18f64, 1e-12] {
            let t0 = std::time::Instant::now();
            let (ev, distinct) = feedback(&sp, rho, mu_b, 10.0, 24);
            println!(
                "{{\"phase\":\"feedback\",\"mu_b\":{mu_b:e},\"events\":{ev},\"distinct\":{distinct},\"sec\":{:.2}}}",
                t0.elapsed().as_secs_f32()
            );
        }
    }
}
