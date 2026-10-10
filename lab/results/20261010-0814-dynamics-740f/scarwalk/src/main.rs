// scarwalk: does the population scar layer (H_live) walk to ruin or reach an attractor?
// Physics (float, exploration): exact Kepler element transforms + textbook impulse kicks
// sampled in the shearing sheet. Store (the measurement): the shipped `emergent-shipmem`
// Program/scars codec on the law's integer grid; only integers decide the reported bytes.
use emergent_shipmem::codec::{Enc, MAXC};
use emergent_shipmem::program::{Prog, Program};
use emergent_shipmem::shelf::Ship;

// ---------- rng ----------
struct Rng(u64);
impl Rng {
    fn u64(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
    fn f(&mut self) -> f64 {
        (self.u64() >> 11) as f64 / 9_007_199_254_740_992.0
    }
    fn norm(&mut self) -> f64 {
        let u1 = self.f().max(1e-300);
        (-2.0 * u1.ln()).sqrt() * (std::f64::consts::TAU * self.f()).cos()
    }
    fn cauchy(&mut self, c: f64) -> f64 {
        c * (std::f64::consts::PI * (self.f() - 0.5)).tan()
    }
    fn poisson(&mut self, lam: f64) -> u32 {
        let l = (-lam).exp();
        let (mut k, mut p) = (0u32, 1.0f64);
        loop {
            p *= self.f();
            if p <= l {
                return k;
            }
            k += 1;
        }
    }
}

// ---------- Kepler (GM = 1, a = 1 units) ----------
fn posvel(a: f64, ex: f64, ey: f64, lam: f64) -> ([f64; 2], [f64; 2]) {
    let e = (ex * ex + ey * ey).sqrt();
    let w = ey.atan2(ex);
    let m = lam - w;
    let mut ea = m;
    for _ in 0..24 {
        let f = ea - e * ea.sin() - m;
        let fp = 1.0 - e * ea.cos();
        let d = f / fp;
        ea -= d;
        if d.abs() < 1e-14 {
            break;
        }
    }
    let p = a * (1.0 - e * e);
    let fac = (1.0 / p).sqrt();
    let den = 1.0 - e * ea.cos();
    let nu = ((1.0 - e * e).sqrt() * ea.sin() / den).atan2((ea.cos() - e) / den);
    let th = w + nu;
    let (st, ct) = (th.sin(), th.cos());
    let vr = fac * e * nu.sin();
    let vt = fac * (1.0 + e * nu.cos());
    let r = a * den;
    (
        [r * ct, r * st],
        [vr * ct - vt * st, vr * st + vt * ct],
    )
}
fn elements(r: [f64; 2], v: [f64; 2]) -> (f64, f64, f64) {
    let rn = (r[0] * r[0] + r[1] * r[1]).sqrt();
    let vn2 = v[0] * v[0] + v[1] * v[1];
    let a = 1.0 / (2.0 / rn - vn2);
    let rv = r[0] * v[0] + r[1] * v[1];
    let c = vn2 - 1.0 / rn;
    (a, c * r[0] - rv * v[0], c * r[1] - rv * v[1])
}

// ---------- encounter law (shearing-sheet MC, impulse approximation) ----------
struct Belt {
    w: f64,
    sig_e: f64,
    m: f64,
    n_s: f64,
}

fn encounter_law(belt: &Belt, n: usize, rng: &mut Rng) -> (Vec<[f64; 3]>, f64) {
    let b_max = belt.w;
    let sig_v = belt.sig_e;
    let pdf = |b: f64| b * ((1.5 * b) * (1.5 * b) + sig_v * sig_v).sqrt();
    let mut out = Vec::with_capacity(n);
    for _ in 0..n {
        let b = loop {
            let cand = b_max * rng.f();
            if rng.f() * pdf(b_max) <= pdf(cand) {
                break cand;
            }
        };
        let vt = 1.5 * b + rng.norm() * sig_v * SQRT2;
        let vr = rng.norm() * sig_v * SQRT2;
        let vrel = (vr * vr + vt * vt).sqrt();
        let b90 = belt.m / (vrel * vrel);
        let dv = 2.0 * vrel / (1.0 + (b / b90) * (b / b90)).sqrt();
        let side = if rng.f() < 0.5 { 1.0 } else { -1.0 };
        let ur = vr / vrel;
        let ut = vt / vrel;
        let (dx, dy) = (-ut * side, ur * side);
        let half = dv * 0.5;
        let phi = rng.f() * std::f64::consts::TAU;
        let (sp, cp) = (phi.sin(), phi.cos());
        let dvx = (dx * cp - dy * sp) * half;
        let dvy = (dx * sp + dy * cp) * half;
        let a = 1.0 + (rng.f() - 0.5) * belt.w;
        let er = belt.sig_e * (-2.0 * (1.0 - rng.f()).ln()).sqrt();
        let ew = rng.f() * std::f64::consts::TAU;
        let (ex, ey) = (er * ew.cos(), er * ew.sin());
        let lam = rng.f() * std::f64::consts::TAU;
        let (r, v) = posvel(a, ex, ey, lam);
        let (a2, ex2, ey2) = elements(r, [v[0] + dvx, v[1] + dvy]);
        out.push([a2 - a, ex2 - ex, ey2 - ey]);
    }
    let nb = 400;
    let db = b_max / nb as f64;
    let mut s = 0.0;
    for i in 0..nb {
        let b = (i as f64 + 0.5) * db;
        s += belt.n_s * ((1.5 * b) * (1.5 * b) + sig_v * sig_v).sqrt() * 2.0 * std::f64::consts::PI * b * db;
    }
    (out, s / std::f64::consts::TAU)
}

// ---------- replay ----------
const HALF: i64 = 1 << 62;

struct Body {
    da: f64,
    dex: f64,
    dey: f64,
    dphi: f64,
}

fn seal_bytes(bodies: &[Body], anchor: bool, qa: f64, qe: f64, qphi: f64) -> (f64, f64, [f64; 4]) {
    let mut mean = [0.0f64; 4];
    if anchor {
        for b in bodies {
            mean[0] += b.da;
            mean[1] += b.dex;
            mean[2] += b.dey;
            mean[3] += b.dphi;
        }
        for m in mean.iter_mut() {
            *m /= bodies.len() as f64;
        }
    }
    let mut prog = [Prog::Const(0); MAXC];
    let mut sig = [0.0f64; 4];
    let mut scars: Vec<(u64, Ship)> = Vec::new();
    let mut states: Vec<Ship> = Vec::with_capacity(bodies.len());
    for (i, b) in bodies.iter().enumerate() {
        let mut s = [0u64; MAXC];
        let d = [
            b.da / qa,
            b.dex / qe,
            b.dey / qe,
            b.dphi / qphi,
        ];
        for (j, dj) in d.iter().enumerate() {
            sig[j] += (dj - mean[j]) * (dj - mean[j]);
            s[j] = (HALF + dj.round() as i64) as u64;
        }
        states.push(s);
        scars.push((i as u64, s));
    }
    for j in 0..4 {
        sig[j] = (sig[j] / bodies.len() as f64).sqrt();
    }
    for j in 0..3 {
        prog[j] = Prog::Const((HALF + mean[j].round() as i64) as u64);
    }
    prog[3] = Prog::Const((HALF + mean[3].round() as i64) as u64);
    scars.retain(|(o, s)| (0..4).any(|f| s[f] != prog[f].at(*o)));
    let mut enc = Enc::new(true);
    let n = bodies.len();
    let pr = Program::seal_from(n as u64, 4, prog, &scars, &mut enc);
    let mut sh = [0u64; MAXC];
    for (i, st) in states.iter().enumerate().step_by(97) {
        pr.eval(i as u64, &mut sh);
        assert_eq!(&sh, st, "store roundtrip failed at {}", i);
    }
    (pr.bytes() as f64 / n as f64, pr.scars() as f64 / n as f64, sig)
}

#[allow(clippy::too_many_arguments)]
fn replay(
    name: &str,
    nn: usize,
    law: &[[f64; 3]],
    per_epoch: f64,
    ind: [f64; 3],
    col: [f64; 3],
    cauchy_tail: bool,
    epochs: u32,
    qa: f64,
    qe: f64,
    qphi: f64,
    rng: &mut Rng,
) {
    let mut bodies: Vec<Body> = (0..nn).map(|_| Body { da: 0.0, dex: 0.0, dey: 0.0, dphi: 0.0 }).collect();
    let mut kicks = 0usize;
    println!("gen,k_eff,bytesP0,bytesP1,scars,sigA,sigEX,sigEY,sigPHI");
    for epoch in 1..=epochs {
        let shared: [f64; 3] = [
            if col[0] > 0.0 { if cauchy_tail { rng.cauchy(col[0]) } else { rng.norm() * col[0] } } else { 0.0 },
            if col[1] > 0.0 { if cauchy_tail { rng.cauchy(col[1]) } else { rng.norm() * col[1] } } else { 0.0 },
            if col[2] > 0.0 { if cauchy_tail { rng.cauchy(col[2]) } else { rng.norm() * col[2] } } else { 0.0 },
        ];
        let nk = if per_epoch > 0.0 { rng.poisson(per_epoch) } else { 0 };
        for b in bodies.iter_mut() {
            if per_epoch > 0.0 {
                for _ in 0..nk {
                    let k = &law[rng.u64() as usize % law.len()];
                    b.da += k[0];
                    b.dex += k[1];
                    b.dey += k[2];
                }
                kicks += nk as usize;
            } else {
                let draw = |rng: &mut Rng, s: f64| {
                    if s > 0.0 {
                        if cauchy_tail { rng.cauchy(s) } else { rng.norm() * s }
                    } else { 0.0 }
                };
                b.da += shared[0] + draw(rng, ind[0]);
                b.dex += shared[1] + draw(rng, ind[1]);
                b.dey += shared[2] + draw(rng, ind[2]);
                kicks += 1;
            }
            b.dphi += 1.5 * b.da * std::f64::consts::TAU;
        }
        if epoch == epochs {
            // per-column attribution: seal each column alone (cols=1); EF (~2-3 bits) counted per run
            let qs = [qa, qe, qe, qphi];
            let mut cols1 = String::new();
            for f in 0..4usize {
                let mut scars: Vec<(u64, Ship)> = Vec::new();
                let mut ok = true;
                for (i, b) in bodies.iter().enumerate() {
                    let d = [b.da / qa, b.dex / qe, b.dey / qe, b.dphi / qphi][f];
                    let mut s = [0u64; MAXC];
                    s[0] = (HALF + d.round() as i64) as u64;
                    if s[0] != (HALF) as u64 { ok = true; }
                    scars.push((i as u64, s));
                }
                let mut prog = [Prog::Const(0); MAXC];
                prog[0] = Prog::Const(HALF as u64);
                scars.retain(|(o, s)| s[0] != prog[0].at(*o));
                let mut enc = Enc::new(true);
                let pr = Program::seal_from(nn as u64, 1, prog, &scars, &mut enc);
                cols1.push_str(&format!("{:.3},", pr.bytes() as f64 / nn as f64));
                let _ = ok;
            }
            println!("#percol {},{:.4},,,,,{}", name, kicks as f64 / nn as f64, cols1);
        }
        if epoch.count_ones() == 1 || epoch == epochs {
            let (b0, s0, sig) = seal_bytes(&bodies, false, qa, qe, qphi);
            let (b1, _, _) = seal_bytes(&bodies, true, qa, qe, qphi);
            let keff = kicks as f64 / nn as f64;
            println!(
                "{},{:.4},{:.4},{:.4},{:.4},{:.3e},{:.3e},{:.3e},{:.3e}",
                name, keff, b0, b1, s0, sig[0], sig[1], sig[2], sig[3]
            );
        }
    }
}

const SQRT2: f64 = 1.4142135623730951;

fn main() {
    let mut rng = Rng(0x9E3779B97F4A7C15);
    // control: tangential impulse on a circular orbit gives da = 2 dv_t / n (n = 1 here)
    {
        let (r, v) = posvel(1.0, 0.0, 0.0, 0.4);
        let dvt = 1e-4;
        let th = r[1].atan2(r[0]);
        let v2 = [v[0] - dvt * th.sin(), v[1] + dvt * th.cos()];
        let (a2, _, _) = elements(r, v2);
        println!("# control da: analytic {:.3e} measured {:.3e}", 2.0 * dvt, a2 - 1.0);
    }
    let qa = 2f64.powi(-24);
    let qe = 2f64.powi(-24);
    let qphi = std::f64::consts::TAU / 2f64.powi(32);

    for (name, mu, w, sig_e) in [("physical", 1e-4f64, 0.06f64, 0.02f64), ("hot", 3e-2f64, 0.06f64, 0.05f64)] {
        let area = std::f64::consts::TAU * w;
        let n_s = 1_048_576.0 / area;
        let m = mu / (n_s * area);
        let belt = Belt { w, sig_e, m, n_s };
        let (law, rate) = encounter_law(&belt, 300_000, &mut rng);
        let sda = law.iter().map(|k| k[0] * k[0]).sum::<f64>() / law.len() as f64;
        let sde = law.iter().map(|k| k[1] * k[1] + k[2] * k[2]).sum::<f64>() / law.len() as f64;
        println!(
            "# belt {} mu={:e} m={:e} rate/orbit/body={:.5} rms/enc da={:.3e} rms/enc e={:.3e} ({} samples)",
            name, mu, m, rate, sda.sqrt(), sde.sqrt(), law.len()
        );
        if name == "physical" {
            // per-orbit action diffusion from the law, for the game-scale extrapolation
            let sa = (sda * rate).sqrt();
            let se = (sde * rate).sqrt();
            println!("# physical per-orbit rms: da={:.3e} de={:.3e}", sa, se);
            continue;
        }
        replay("G2gauss", 16384, &law, 0.0, [3e-3, 3e-3, 3e-3], [0.0; 3], false, 4096, qa, qe, qphi, &mut rng);
        replay("G3encounter", 16384, &law, 1.0, [0.0; 3], [0.0; 3], false, 4096, qa, qe, qphi, &mut rng);
        replay("G4cauchy", 16384, &law, 0.0, [3e-3, 3e-3, 3e-3], [0.0; 3], true, 4096, qa, qe, qphi, &mut rng);
        replay("G1collect", 16384, &law, 0.0, [0.0; 3], [3e-3, 3e-3, 3e-3], false, 4096, qa, qe, qphi, &mut rng);
        replay("Gmix99", 16384, &law, 0.0, [3e-5; 3], [3e-3, 3e-3, 3e-3], false, 4096, qa, qe, qphi, &mut rng);
        replay("G2gaussN4k", 4096, &law, 0.0, [3e-3, 3e-3, 3e-3], [0.0; 3], false, 4096, qa, qe, qphi, &mut rng);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn roundtrip_elements() {
        let mut rng = Rng(12345);
        let mut worst = 0.0f64;
        for _ in 0..20000 {
            let a = 1.0 + (rng.f() - 0.5) * 0.06;
            let er = 0.05 * (-2.0 * (1.0 - rng.f()).ln()).sqrt();
            let ew = rng.f() * std::f64::consts::TAU;
            let (ex, ey) = (er * ew.cos(), er * ew.sin());
            let lam = rng.f() * std::f64::consts::TAU;
            let (r, v) = posvel(a, ex, ey, lam);
            let (a2, ex2, ey2) = elements(r, v);
            worst = worst.max((a2 - a).abs()).max((ex2 - ex).abs()).max((ey2 - ey).abs());
        }
        eprintln!("worst roundtrip err {worst:.3e}");
        assert!(worst < 1e-12);
    }
}
