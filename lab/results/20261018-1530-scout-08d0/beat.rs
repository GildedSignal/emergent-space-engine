// Beat-slack toy: can a stored (k, d) beat record carry sound slack across kicks?
// Exact integer arithmetic: all phases in units of 2^-SH ticks (u128), zero float error.
// Constants from lab/wiki/encounters.md (1a29): w = 23 ticks, d ~ 3e5 ticks, k ~ 1e6,
// C chosen so mean first-hit = C/w ~ 1e6 conjunctions.
use std::env;

const SH: u32 = 25;
const ONE: u128 = 1u128 << SH; // one tick in units
const C_TICKS: u128 = 23_000_000;
const HALF_W: u128 = 23 * ONE / 2; // half window = 11.5 ticks
const K_CAP: u64 = 3_000_000;

struct Xo(u64);
impl Xo {
    fn next(&mut self) -> u64 {
        let mut x = self.0;
        x ^= x << 13; x ^= x >> 7; x ^= x << 17;
        self.0 = x; x
    }
    fn below(&mut self, m: u64) -> u64 { self.next() % m }
}

// Walk the rotation; return (first-hit k or None if censored, best (slack, j):
// slack/j = min_{j<k} (m_j - w/2)/j, tracked by cross-multiplication, all integer).
fn walk(phi0: u128, d: u128, c: u128) -> (Option<u64>, (u128, u128)) {
    let mut phi = phi0 % c;
    let mut best = (u128::MAX, 1u128); // (slack, j)
    for j in 1..=K_CAP {
        phi = (phi + d) % c;
        let x = phi.min(c - phi);
        if x <= HALF_W {
            return (Some(j), best);
        }
        let slack = x - HALF_W;
        if slack * best.1 < best.0 * j as u128 {
            best = (slack, j as u128);
        }
    }
    (None, best)
}

// hits within the next `h` conjunctions (walk only h steps)
fn hit_within(phi0: u128, d: u128, c: u128, h: u64) -> bool {
    let mut phi = phi0 % c;
    for _ in 0..h {
        phi = (phi + d) % c;
        let x = phi.min(c - phi);
        if x <= HALF_W {
            return true;
        }
    }
    false
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let seed: u64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(1);
    let n: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(2500);
    let c = C_TICKS * ONE;
    let mut rng = Xo(seed | 1);

    // Silent pairs: d log-uniform in [1.5e5, 6e5] ticks, phi0 uniform.
    let mut pairs = Vec::with_capacity(n);
    for _ in 0..n {
        let u = (rng.below(1_000_000) as f64) / 1e6;
        let d_t = (150_000.0 * 4f64.powf(u)) as u128;
        let phi0 = (rng.next() as u128) % c; // coarse-uniform phase, exact integer
        pairs.push((phi0, d_t * ONE));
    }

    // Initial exact book + slack S.
    let mut ks: Vec<Option<u64>> = Vec::with_capacity(n);
    let mut ss: Vec<(u128, u128)> = Vec::with_capacity(n);
    for &(phi0, d) in &pairs {
        let (k, s) = walk(phi0, d, c);
        ks.push(k);
        ss.push(s);
    }
    let uncensored: Vec<usize> = (0..n).filter(|&i| ks[i].is_some()).collect();
    let ku: Vec<u64> = uncensored.iter().map(|&i| ks[i].unwrap()).collect();
    let mut ksort = ku.clone();
    ksort.sort_unstable();
    let median_k = ksort[ksort.len() / 2];
    let mean_k = ku.iter().sum::<u64>() as f64 / ku.len() as f64;
    println!("pairs {} uncensored {} censored {}", n, uncensored.len(), n - uncensored.len());
    println!("k: mean {:.3e} median {} (model C/w = {:.3e}) p05 {} p95 {}",
        mean_k, median_k, 23_000_000.0 / 23.0, ksort[ksort.len() / 20], ksort[ksort.len() * 19 / 20]);

    // P1: S scaling. ratio = S / (3C/k^2) etc (report-only float stats).
    let mut r3 = Vec::new();
    let mut r1 = Vec::new();
    let mut jstar_frac_small = 0usize;
    for &i in &uncensored {
        let (s, j) = ss[i];
        let k = ks[i].unwrap() as f64;
        let s_f = s as f64 / ONE as f64 / j as f64; // in ticks
        let c_f = C_TICKS as f64;
        r3.push(s_f / (3.0 * c_f / (k * k)));
        r1.push(s_f / (c_f / k));
        if (j as f64) < 0.2 * k {
            jstar_frac_small += 1;
        }
    }
    r3.sort_by(|a, b| a.partial_cmp(b).unwrap());
    r1.sort_by(|a, b| a.partial_cmp(b).unwrap());
    println!("S scaling: median S/(3C/k^2) = {:.4}  median S/(C/k) = {:.4e}  P(j* < 0.2k) = {:.3}",
        r3[r3.len() / 2], r1[r1.len() / 2], jstar_frac_small as f64 / r3.len() as f64);

    // Kick arms: relative kick kappa = 2^-kap on d (1a29's 2^-23 belt quantum).
    for kap in [26u32, 23, 20, 17, 14] {
        let mut kept = 0usize;
        let mut viol = 0usize;
        let mut early = 0usize;
        let mut flip = [0usize; 3];
        let hs = [8u64, 128, 4096];
        for &i in &uncensored {
            let (phi0, d) = pairs[i];
            let k = ks[i].unwrap();
            let ddv = d >> kap; // delta-d in units, exact power-of-two
            let sign = if rng.next() & 1 == 0 { 1i128 } else { -1i128 };
            let d2 = (d as i128 + sign * ddv as i128) as u128;
            let (k2, _) = walk(phi0, d2, c);
            let k2u = k2.unwrap_or(K_CAP + 1);
            // slack rule: keep the stored due iff dd < S  (dd < s/j)
            let (s, j) = ss[i];
            let keep = ddv * j < s;
            if keep {
                kept += 1;
                if k2u < k {
                    viol += 1; // must stay 0: instrument validity (P5)
                }
            }
            if k2u < k {
                early += 1;
            }
            for (hi, &h) in hs.iter().enumerate() {
                if k >= h && k2u < h {
                    flip[hi] += 1;
                }
            }
        }
        let nref = uncensored.len() as f64;
        println!("kap 2^-{:>2}: keep(slack<S) {:.4}  recompute {:.4}  violations {} (must be 0)  P(k'<k) {:.3e}  flips-on H=8/128/4096: {:.3e}/{:.3e}/{:.3e}",
            kap, kept as f64 / nref, 1.0 - kept as f64 / nref, viol,
            early as f64 / nref,
            flip[0] as f64 / nref, flip[1] as f64 / nref, flip[2] as f64 / nref);
    }
    // P4: the epoch frontier. 256 kicks at the 2^-23 quantum; an exact re-arm every E
    // kicks covers its own next-E window; misses = in-window conjunctions inside the
    // next E steps arising at blind kicks (between re-arms).
    let tt = 256u64;
    let np = uncensored.len().min(800);
    for e in [1u64, 4, 16, 64, 256, 1024, 4096] {
        let mut missed_total = 0u64;
        let mut pairs_with_miss = 0u64;
        let mut rearm = 0u64;
        for &i in &uncensored[..np] {
            let (phi0, d) = pairs[i];
            let mut dcur = d as i128;
            let mut hit_any = false;
            for t in 0..tt {
                let ddv = (dcur.unsigned_abs() >> 23) as i128;
                let sign = if rng.next() & 1 == 0 { 1i128 } else { -1i128 };
                dcur += sign * ddv;
                if t % e == 0 {
                    rearm += 1;
                } else if hit_within(phi0, dcur as u128, c, e) {
                    missed_total += 1;
                    hit_any = true;
                }
            }
            if hit_any { pairs_with_miss += 1 }
        }
        println!("epoch E={:>4}: re-arms/pair/256k {:.2}  missed-conj/pair/256k {:.5}  pairs-with-miss {}/{}  missed per re-arm {:.3e}",
            e, rearm as f64 / np as f64, missed_total as f64 / np as f64,
            pairs_with_miss, np, missed_total as f64 / rearm as f64);
    }
    println!("DONE seed {} n {}", seed, n);
}
