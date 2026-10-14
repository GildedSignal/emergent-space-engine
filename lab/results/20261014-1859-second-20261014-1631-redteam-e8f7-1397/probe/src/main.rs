// Positive control for the doll-chain simultaneity key (run 1397, second author on e8f7).
//
// The falsified design (ae29): key = doll tick + SUM of per-link simultaneity shears.
// The proposed fix: compose the chain's boosts as products of the crate's integer shears
// and read the key off the composed event map. This probe runs that fix on the design's
// own path: the shipped `lorentz::Frame` (nine shears per link, coefficients at 2^-100
// from an integer algorithm) applied to EVENTS (t, x, y) held as words at 2^-64 tick,
// ae29's accumulation level, chained over the doll tree.
//
// Nothing here edits the crates; it calls them. Output: one JSON object per line.
use emergent_space::orbit::Scalar;
use emergent_universe::lorentz::Frame;
use emergent_universe::num::{norm2, to_f64, V2};

const F: i64 = 40; // velocity words exponent: w = round(beta * 2^40)

fn words(beta: f64, theta: f64) -> V2 {
    let snap = |v: f64| Scalar::raw((v * (1u64 << F) as f64).round() as i128, -(F as i32)).unwrap();
    [snap(beta * theta.cos()), snap(beta * theta.sin())]
}

fn read_back(w: &V2) -> (f64, f64) {
    let b = to_f64(norm2(*w).unwrap());
    let (wx, wy) = (to_f64(w[0]), to_f64(w[1]));
    (b, wy.atan2(wx))
}

/// Exact 2+1 Lorentz map, doll frame -> parent frame, doll moving at +beta along theta (f64 oracle).
fn boost(beta: f64, theta: f64) -> [[f64; 3]; 3] {
    let g = 1.0 / (1.0 - beta * beta).sqrt();
    let n = [theta.cos(), theta.sin()];
    let mut m = [[0.0f64; 3]; 3];
    m[0][0] = g;
    m[0][1] = g * beta * n[0];
    m[0][2] = g * beta * n[1];
    m[1][0] = m[0][1];
    m[2][0] = m[0][2];
    for i in 0..2 {
        for j in 0..2 {
            m[1 + i][1 + j] = (if i == j { 1.0 } else { 0.0 }) + (g - 1.0) * n[i] * n[j];
        }
    }
    m
}

fn mat_mul(a: [[f64; 3]; 3], b: [[f64; 3]; 3]) -> [[f64; 3]; 3] {
    let mut m = [[0.0f64; 3]; 3];
    for i in 0..3 {
        for j in 0..3 {
            m[i][j] = a[i][0] * b[0][j] + a[i][1] * b[1][j] + a[i][2] * b[2][j];
        }
    }
    m
}

#[derive(Clone)]
struct Link {
    frame: Option<Frame>,
    beta: f64,
    theta: f64,
}

impl Link {
    fn new(beta: f64, theta: f64) -> Link {
        let w = words(beta, theta);
        let (b, t) = read_back(&w);
        Link { frame: Frame::of(w).unwrap(), beta: b, theta: t }
    }

    fn gamma(&self) -> f64 {
        1.0 / (1.0 - self.beta * self.beta).sqrt()
    }

    fn sinh_eta(&self) -> f64 {
        self.beta * self.gamma()
    }

    fn dir(&self) -> [f64; 2] {
        [self.theta.cos(), self.theta.sin()]
    }

    /// The event's coordinates in this link's parent: the shipped nine-shear Frame::inverse.
    fn up(&self, e: [i128; 3]) -> [i128; 3] {
        match &self.frame {
            Some(f) => f.inverse(e).unwrap(),
            None => e,
        }
    }
}

/// Composed integer key: walk the chain rootwards with the shipped integer shears.
fn composed_key(links: &[Link], e: [i128; 3]) -> [i128; 3] {
    let mut e = e;
    for l in links.iter().rev() {
        e = l.up(e);
    }
    e
}

/// Float oracle + additive variants for the same chain, at the engine's read-back parameters.
fn oracle_and_additive(links: &[Link], e: [i128; 3]) -> (f64, f64, f64) {
    // M = B_1 . B_2 . ... (links are listed root-first; apply innermost first)
    let mut m = [[1.0f64, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]];
    for l in links.iter() {
        m = mat_mul(m, boost(l.beta, l.theta));
    }
    let ef = [e[0] as f64, e[1] as f64, e[2] as f64].map(|v| v * 2.0f64.powi(-64));
    let t_exact = m[0][0] * ef[0] + m[0][1] * ef[1] + m[0][2] * ef[2];
    // Additive V1 (chain-tracking): walk positions up the chain, each link shears its own local offset.
    let xb = [ef[1], ef[2]];
    let tb = ef[0];
    let mut x = xb;
    let mut key1 = 0.0f64;
    for l in links.iter().rev() {
        let v = l.dir();
        key1 += l.sinh_eta() * (v[0] * x[0] + v[1] * x[1]);
        let g = l.gamma();
        let vd = v[0] * x[0] + v[1] * x[1];
        x = [
            x[0] + (g - 1.0) * vd * v[0] + g * l.beta * v[0] * tb,
            x[1] + (g - 1.0) * vd * v[1] + g * l.beta * v[1] * tb,
        ];
    }
    // Additive V2 (frozen per entity): every link's shear at the terminal offset.
    let mut key2 = 0.0f64;
    for l in links.iter() {
        let v = l.dir();
        key2 += l.sinh_eta() * (v[0] * xb[0] + v[1] * xb[1]);
    }
    (t_exact, key1, key2)
}

fn case(tag: &str, links: &[Link], d: f64, phi: f64, tb: f64) -> String {
    let theta_term = links.last().unwrap().theta + phi;
    let two64 = 2.0f64.powi(64);
    let e = [
        (tb * two64).round() as i128,
        (d * theta_term.cos() * two64).round() as i128,
        (d * theta_term.sin() * two64).round() as i128,
    ];
    let er = composed_key(links, e);
    let (t_exact, key1, key2) = oracle_and_additive(links, e);
    let t_comp = er[0] as f64 * 2.0f64.powi(-64);
    format!(
        "{{\"tag\":\"{}\",\"n\":{},\"d\":{:.1},\"phi_deg\":{:.1},\"tb\":{:.1},\"t_exact\":{:.17e},\"key1\":{:.17e},\"key2\":{:.17e},\"key_comp\":{:.17e},\"err1\":{:.6e},\"err2\":{:.6e},\"err_comp\":{:.6e}}}",
        tag, links.len(), d, phi.to_degrees(), tb, t_exact, key1, key2, t_comp,
        t_exact - key1, t_exact - key2, t_exact - t_comp
    )
}

fn tb_channel() -> String {
    // (0.5, 0) <- (0.5, 0) collinear and (0.5, 0) <- (0.5, 90deg) perpendicular; t_B = 1e4, no offset.
    let mut out = String::new();
    for (tag, th2) in [("collinear", 0.0f64), ("perpendicular", std::f64::consts::FRAC_PI_2)] {
        let l1 = Link::new(0.5, 0.0);
        let l2 = Link::new(0.5, th2);
        let tb = 1e4f64;
        let e = [(tb * 2.0f64.powi(64)).round() as i128, 0, 0];
        let er = composed_key(&[l1.clone(), l2.clone()], e);
        let t_comp = er[0] as f64 * 2.0f64.powi(-64);
        let g1 = l1.gamma();
        let g2 = 1.0f64 / (1.0f64 - 0.25f64).sqrt();
        // Exact carrier: the composed map's [0,0] entry.
        let m = mat_mul(boost(l1.beta, 0.0), boost(l2.beta, th2));
        let t_exact = m[0][0] * tb;
        out.push_str(&format!(
            "{{\"tag\":\"tb_{}\",\"tB\":{:.1},\"t_exact\":{:.17e},\"gamma12\":{:.17e},\"gamma12_1pb1b2\":{:.17e},\"t_comp\":{:.17e},\"err_unscaled\":{:.6e},\"err_gamma12\":{:.6e},\"err_comp\":{:.6e}}}\n",
            tag, tb, t_exact, g1 * g2, g1 * g2 * (1.0 + l1.beta * l2.beta), t_comp,
            t_exact - tb, t_exact - g1 * g2 * tb, t_exact - t_comp
        ));
    }
    out
}

fn main() {
    let mut lines: Vec<String> = Vec::new();

    // Instrument self-check: one link (depth 1 must be exact for the additive key too).
    {
        let l = Link::new(0.5, 0.35);
        let two64 = 2.0f64.powi(64);
        let e = [0i128, (3000.0 * two64).round() as i128, (4000.0 * two64).round() as i128];
        let er = composed_key(&[l.clone()], e);
        let (t_exact, k1, k2) = oracle_and_additive(&[l], e);
        let t_comp = er[0] as f64 * 2.0f64.powi(-64);
        lines.push(format!(
            "{{\"tag\":\"selfcheck_one_link\",\"t_exact\":{:.17e},\"key1\":{:.17e},\"key2\":{:.17e},\"key_comp\":{:.17e},\"err1\":{:.6e},\"err2\":{:.6e},\"err_comp\":{:.6e}}}",
            t_exact, k1, k2, t_comp, t_exact - k1, t_exact - k2, t_exact - t_comp
        ));
    }

    // SELFTEST=1: instrument validation only (single link); the decisive grid is not run.
    if std::env::var_os("SELFTEST").is_some() {
        for l in lines {
            println!("{}", l);
        }
        return;
    }

    // G1: the original 108-cell kill grid (theta1 = 0).
    for b1 in [0.1f64, 0.3, 0.5, 0.9] {
        let l1 = Link::new(b1, 0.0);
        for b2 in [0.01f64, 0.1, 0.3] {
            for th2 in [0.0f64, std::f64::consts::FRAC_PI_2, std::f64::consts::PI] {
                let l2 = Link::new(b2, th2);
                for d in [100.0f64, 1000.0, 10000.0] {
                    lines.push(case(
                        &format!("g1_b{}_b{}_th{}_d{}", b1, b2, th2.to_degrees() as i64, d as i64),
                        &[l1.clone(), l2.clone()], d, 0.0, 0.0,
                    ));
                }
            }
        }
    }

    // G2: extended adversarial cells (checker's ranges: beta2 0.5-0.9, theta 45-60 deg) + 0.99.
    for (b1, b2) in [(0.5f64, 0.5f64), (0.5, 0.9), (0.9, 0.5), (0.9, 0.9), (0.99, 0.5)] {
        let l1 = Link::new(b1, 0.0);
        for th2 in [45.0f64.to_radians(), 60.0f64.to_radians()] {
            let l2 = Link::new(b2, th2);
            for d in [1000.0f64, 10000.0] {
                lines.push(case(
                    &format!("g2_b{}_b{}_th{}_d{}", b1, b2, th2.to_degrees() as i64, d as i64),
                    &[l1.clone(), l2.clone()], d, 0.0, 0.0,
                ));
            }
        }
    }

    // G3: planar nine-shear arms with theta1 != 0.
    for (b1, t1) in [(0.5f64, 30.0f64), (0.9, 20.0)] {
        let l1 = Link::new(b1, t1.to_radians());
        for (b2, t2) in [(0.3f64, 75.0f64), (0.5, 110.0)] {
            let l2 = Link::new(b2, t2.to_radians());
            for d in [1000.0f64, 10000.0] {
                for phi in [0.0f64, std::f64::consts::FRAC_PI_2] {
                    lines.push(case(
                        &format!("g3_b{}t{}_b{}t{}_d{}_p{}", b1, t1 as i64, b2, t2 as i64, d as i64, phi.to_degrees() as i64),
                        &[l1.clone(), l2.clone()], d, phi, 0.0,
                    ));
                }
            }
        }
    }

    // Named held-out rows (the run's own), plus the understated worst cell, now measured.
    let named: Vec<(&str, Vec<Link>, f64, f64)> = vec![
        ("player_group", vec![Link::new(0.3, 0.0), Link::new(0.3, std::f64::consts::FRAC_PI_2)], 1000.0, 0.0),
        ("inspiral", vec![Link::new(0.5, 0.0), Link::new(0.5, 0.0)], 2000.0, 0.0),
        ("high_gamma", vec![Link::new(0.9, 0.0), Link::new(0.1, 0.0)], 1000.0, 0.0),
        ("perp_offset", vec![Link::new(0.5, 0.0), Link::new(0.5, std::f64::consts::FRAC_PI_2)], 2000.0, std::f64::consts::FRAC_PI_2),
        ("worst_cell", vec![Link::new(0.9, 0.0), Link::new(0.9, 45.0f64.to_radians())], 10000.0, 0.0),
    ];
    for (tag, links, d, phi) in named {
        lines.push(case(tag, &links, d, phi, 0.0));
    }

    // Scaling signature on the worst cell: oracle-noise-limited error scales with d; real error does not.
    {
        let links = vec![Link::new(0.9, 0.0), Link::new(0.9, 45.0f64.to_radians())];
        for d in [10000.0f64, 80000.0] {
            lines.push(case(&format!("scale_d{}", d as i64), &links, d, 0.0, 0.0));
        }
    }

    // Depth scaling: beta 0.3 per link, collinear, terminal offset 1000; and planar chains.
    for n in [2usize, 3, 4, 5, 6, 8] {
        let links: Vec<Link> = (0..n).map(|_| Link::new(0.3, 0.0)).collect();
        lines.push(case(&format!("depth{}_collinear", n), &links, 1000.0, 0.0, 0.0));
    }
    for n in [3usize, 4] {
        let links: Vec<Link> = (0..n)
            .map(|i| Link::new(0.3, if i % 2 == 0 { 0.0 } else { 15.0f64.to_radians() }))
            .collect();
        lines.push(case(&format!("depth{}_planar", n), &links, 1000.0, 0.0, 0.0));
    }

    // The t_B channel.
    lines.push(tb_channel().trim_end().to_string());

    for l in lines {
        println!("{}", l);
    }
}
