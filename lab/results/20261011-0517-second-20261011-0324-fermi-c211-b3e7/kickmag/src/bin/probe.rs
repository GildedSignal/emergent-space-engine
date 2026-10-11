//! Probe: the law's orbit key ranges (pop::orbit draws), to size "family-jumping" kicks.
//! Usage: probe [draws]
use emergent_shipmem::pop::Rng;

fn orbit_raw(r: &mut Rng) -> (u64, u64) {
    // Mirrors pop::orbit (private); same draw order so the ranges match the law's.
    let p = r.range(100 << 16, 8000 << 16) as u32;
    let e = r.below((0.6 * (1u64 << 30) as f64) as u64) as u32;
    let k = emergent_space::Key::darwin(p, e).expect("bound orbit");
    (k.energy.get(), k.angular.get())
}
fn main() {
    let n: usize = std::env::args()
        .nth(1)
        .and_then(|s| s.parse().ok())
        .unwrap_or(200_000);
    let mut r = Rng::new(0xBEED);
    let mut es = Vec::with_capacity(n);
    let mut ls = Vec::with_capacity(n);
    for _ in 0..n {
        let (e, l) = orbit_raw(&mut r);
        es.push(e);
        ls.push(l);
    }
    es.sort_unstable();
    ls.sort_unstable();
    let q = |v: &[u64], f: f64| v[(f * (v.len() - 1) as f64) as usize];
    let bl = |x: u64| 64 - x.leading_zeros();
    println!("draws {n}");
    println!(
        "E: min {:>17} (2^{}) p1 {:>17} med {:>17} p99 {:>17} max {:>17} (2^{}) spread {:>17} (2^{})",
        es[0], bl(es[0]), q(&es, 0.01), q(&es, 0.5), q(&es, 0.99), *es.last().unwrap(),
        bl(*es.last().unwrap()), es[n - 1] - es[0], bl(es[n - 1] - es[0])
    );
    println!(
        "L: min {:>17} (2^{}) p1 {:>17} med {:>17} p99 {:>17} max {:>17} (2^{}) spread {:>17} (2^{})",
        ls[0], bl(ls[0]), q(&ls, 0.01), q(&ls, 0.5), q(&ls, 0.99), *ls.last().unwrap(),
        bl(*ls.last().unwrap()), ls[n - 1] - ls[0], bl(ls[n - 1] - ls[0])
    );
    // Family-jump delta scale: |E_i - E_j|, |L_i - L_j| for random distinct pairs.
    let mut de = Vec::with_capacity(100_000);
    let mut dl = Vec::with_capacity(100_000);
    for _ in 0..100_000 {
        let (i, j) = (r.below(n as u64) as usize, r.below(n as u64) as usize);
        de.push(es[i].abs_diff(es[j]));
        dl.push(ls[i].abs_diff(ls[j]));
    }
    de.sort_unstable();
    dl.sort_unstable();
    println!(
        "pairwise |dE|: med 2^{} p99 2^{} max 2^{}",
        bl(q(&de, 0.5)), bl(q(&de, 0.99)), bl(*de.last().unwrap())
    );
    println!(
        "pairwise |dL|: med 2^{} p99 2^{} max 2^{}",
        bl(q(&dl, 0.5)), bl(q(&dl, 0.99)), bl(*dl.last().unwrap())
    );
}
