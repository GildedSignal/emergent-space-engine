// checker: 2-point mini-ladder for the scales metric (casec has produced nothing in 15+ min).
// Same intensive rates as casec (checks per body per orbit; truth encounter rate), smaller
// sample (48 bodies, 300-orbit horizon) so it fits the checker window.
fn main() {
    use std::f64::consts::TAU;
    let mut res: Vec<(usize, f64, f64)> = Vec::new();
    for name in ["c-n1000", "c-n10000"] {
        let b = rung::load_belt(&format!("data/{name}.bin"));
        let (n, rho, h) = (b.len(), if name == "c-n1000" { 1e-3 } else { 1e-4 }, 300.0f64);
        let specs: Vec<&str> = vec![];
        let _ = specs;
        // rho from belts.tsv semantics: 1e-4 * 1e4 / n
        let rho = 1e-4 * 1e4 / n as f64;
        let _ = rho;
        let sorted = emergent_encounters::pairs::Sorted::new(&b, rho);
        let ns = 48usize;
        let sample: Vec<u32> = (0..ns).map(|k| (k * n / ns) as u32).collect();
        let mut in_sample = vec![false; n];
        for &i in &sample { in_sample[i as usize] = true; }
        let t0 = std::time::Instant::now();
        let mut st = emergent_encounters::method::Stats::default();
        let mut tmp = Vec::new();
        for &i in &sample {
            let bi = &b[i as usize];
            let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
            for &(_, j) in &sorted.order[lo..hi] {
                let bj = &b[j as usize];
                if j == i || (in_sample[j as usize] && j < i) || !emergent_encounters::pairs::is_candidate(bi, bj, rho) {
                    continue;
                }
                tmp.clear();
                emergent_encounters::method::pair_events(bi, bj, rho, 1.1, 0.0, h * TAU, &mut st, &mut tmp);
            }
        }
        let dioph_rate = st.checks_total() as f64 / (ns as f64 * h);
        let ds = t0.elapsed().as_secs_f64();
        // truth rate from 24 rejection-sampled radial pairs over the same horizon
        let mut xr = emergent_encounters::belt::Rng(24681357);
        let mut picked: Vec<(u32, u32)> = Vec::new();
        let mut tries = 0u64;
        while picked.len() < 24 && tries < (1 << 24) {
            tries += 1;
            let i = (xr.next_u64() as usize) % n;
            let j = (xr.next_u64() as usize) % n;
            if i == j { continue; }
            let (i, j) = (i.min(j), i.max(j));
            let (bi, bj) = (&b[i], &b[j]);
            let (x, y) = if bi.rmin() <= bj.rmin() { (bi, bj) } else { (bj, bi) };
            if y.rmin() <= x.rmax() + 2.0 * rho && !picked.contains(&(i as u32, j as u32)) {
                picked.push((i as u32, j as u32));
            }
        }
        let t1 = std::time::Instant::now();
        let mut enc = 0usize;
        for &(i, j) in &picked {
            let mut out = Vec::new();
            let mut ts = rung::TStats::default();
            rung::truth_pair(&b[i as usize], &b[j as usize], rho, h * TAU, &mut out, &mut ts);
            enc += out.len();
        }
        let ts = t1.elapsed().as_secs_f64();
        // total radial pairs by sweep
        let mut idx: Vec<u32> = (0..n as u32).collect();
        idx.sort_by_key(|&i| b[i as usize].rmin().to_bits());
        let rmins: Vec<f64> = idx.iter().map(|&i| b[i as usize].rmin()).collect();
        let mut nradial = 0u64;
        for (k, &i) in idx.iter().enumerate() {
            let hi = b[i as usize].rmax() + 2.0 * rho;
            nradial += rmins[k + 1..].partition_point(|&x| x <= hi) as u64;
        }
        let truth_rate = enc as f64 / picked.len() as f64 * nradial as f64 / (n as f64 * h);
        println!("{{\"belt\":\"{name}\",\"n\":{n},\"rho\":{rho:.1e},\"bodies\":{ns},\"horizon\":{h:.0},\"checks\":{},\"setups\":{},\"hits\":{},\"dioph_checks_per_body_orbit\":{:.5e},\"truth_rate\":{:.5e},\"truth_enc\":{enc},\"radial\":{nradial},\"dioph_s\":{ds:.1},\"truth_s\":{ts:.1}}}",
            st.checks_total(), st.pairs, st.hits_total(), dioph_rate, truth_rate);
        res.push((n, dioph_rate, truth_rate));
    }
    if res.len() == 2 {
        let fit = |sel: &dyn Fn(&(usize, f64, f64)) -> f64| {
            let (x0, x1) = ((res[0].0 as f64).ln(), (res[1].0 as f64).ln());
            let (y0, y1) = ((sel(&res[0]) * res[0].0 as f64).ln(), (sel(&res[1]) * res[1].0 as f64).ln());
            (y1 - y0) / (x1 - x0)
        };
        println!("mini scale exponents: dioph {:.4} truth/oracle {:.4}", fit(&|r| r.1), fit(&|r| r.2));
    }
}
