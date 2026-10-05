// What the view's gather costs (docs/plane.md: the measured bottleneck of a light frame). Settles the plane
// to a tick, then gathers the view at successive frames the way a player's loop does, and reports ns per
// emitter for: the old search (a fixed point from the present, three to six readouts per body, a separate
// walk up the chain for the clock rate), the new search from scratch, and the new search from the last
// frame's crossing (the memo). The three alternate within every frame, so heat and load hit them alike;
// best of several rounds. `members` sets the fleet (48 emitters that need no readout).
use emergent_universe::fleet::Order;
use emergent_universe::observe::{clock_rate, root_state};
use emergent_universe::scenario::plane;
use emergent_universe::view::{gather, gather_cached, ViewCache};
use emergent_universe::Config;
use std::time::Instant;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let rtf: f64 = args.first().map(|s| s.parse().unwrap()).unwrap_or(100.0);
    let members: u64 = args.get(1).map(|s| s.parse().unwrap()).unwrap_or(48);
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, members).unwrap();
    let frame = (rtf / 60.0 / 4.925_490_947e-6) as i64; // ticks per 60 Hz frame
    let start = 3_000_000_000i64;
    p.u.settle(start);
    let n = 300;
    let (mut best, mut emitters, mut bodies, mut reads) = ([f64::MAX; 3], 0usize, 0usize, 0u64);
    let mut legacy_reads = 0u64;
    for round in 0..7 {
        let mut cache = ViewCache::default();
        let mut t = start + round as i64 * 10 * frame;
        let mut sum = [0.0f64; 3];
        for _ in 0..n {
            t += frame;
            p.u.settle(t);
            p.u.now = t;
            // the old search, bodies only: the retarded fixed point t = T − |x(t) − X|, then the clock's walk
            let ctx = p.u.ctx();
            let t0 = Instant::now();
            let (xo, _) = root_state(&ctx, p.player, t).unwrap();
            let mut lr = 0u64;
            for i in 0..p.u.n_bodies() {
                if i == p.player || !p.u.bodies().alive(i) {
                    continue;
                }
                let mut tt = t as f64;
                for _ in 0..6 {
                    lr += 1;
                    let Ok((x, _)) = root_state(&ctx, i, tt as i64) else { break };
                    let next = (t as f64 - ((x[0] - xo[0]).powi(2) + (x[1] - xo[1]).powi(2)).sqrt()).max(0.0);
                    let done = (next - tt).abs() < 1.0;
                    tt = next;
                    if done {
                        break;
                    }
                }
                std::hint::black_box(clock_rate(&ctx, i, tt as i64).unwrap());
            }
            sum[0] += t0.elapsed().as_secs_f64();
            legacy_reads = lr;
            drop(ctx);
            let t0 = Instant::now();
            let v = gather(&p.u, &p.names).unwrap();
            sum[1] += t0.elapsed().as_secs_f64();
            let t0 = Instant::now();
            let w = gather_cached(&p.u, &p.names, &mut cache).unwrap();
            sum[2] += t0.elapsed().as_secs_f64();
            assert_eq!(v, w, "a cache changes how a crossing is found, never what it is");
            reads += cache.readouts;
            emitters = v.seen.len();
            bodies = v.seen.iter().filter(|s| s.kind != 4).count();
            std::hint::black_box((&v, &w));
        }
        for k in 0..3 {
            best[k] = best[k].min(sum[k] / n as f64);
        }
    }
    let per = |s: f64, k: usize| s * 1e9 / k as f64;
    println!("rtf {rtf}, {members} members: {emitters} emitters, {bodies} of them bodies read out");
    println!("  old search, bodies only:      {:7.1} us per frame = {:6.0} ns per body ({:.2} readouts per body, each followed by a chain walk for the rate)", best[0] * 1e6, per(best[0], bodies), legacy_reads as f64 / bodies as f64);
    println!("  new gather, from scratch:     {:7.1} us per frame = {:6.0} ns per emitter (all {} emitters, fleet and Seen included)", best[1] * 1e6, per(best[1], emitters), emitters);
    println!("  new gather, from the memo:    {:7.1} us per frame = {:6.0} ns per emitter ({:.2} readouts per body)", best[2] * 1e6, per(best[2], emitters), reads as f64 / (7 * n) as f64 / bodies as f64);
}
