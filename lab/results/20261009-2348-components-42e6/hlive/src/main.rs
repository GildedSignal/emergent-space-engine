//! H_live probe: the bits of live distinguishing information the plane creates per game-second.
//!
//! Census pattern copied from xtask's kick_bench: at deterministic 60 Hz snapshots, every distinct
//! pending ship kick is resolved once against the snapshot by the pure resolver (`step::process`,
//! deterministic, the same resolution the run applies), and its state-delta fields are dumped.
//! No digests are consumed by this; nothing is applied; the universe itself keeps running by
//! `frame` + `settle`, so the census follows the real plan stream.
use emergent_space::{binding::Trajectory, orbit::{MemoCode, ShapeKey}};
use emergent_universe::{body::What, step, Budget, Kind};
use std::collections::HashSet;
use std::io::Write;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let seconds: f64 = args.iter().position(|a| a == "--seconds").and_then(|i| args.get(i + 1)).and_then(|v| v.parse().ok()).unwrap_or(10.0);
    let rtf: f64 = args.iter().position(|a| a == "--rtf").and_then(|i| args.get(i + 1)).and_then(|v| v.parse().ok()).unwrap_or(1.0);
    let seed: u64 = args.iter().position(|a| a == "--seed").and_then(|i| args.get(i + 1)).and_then(|v| v.parse().ok()).unwrap_or(1);
    let members: u64 = args.iter().position(|a| a == "--members").and_then(|i| args.get(i + 1)).and_then(|v| v.parse().ok()).unwrap_or(48);

    let p = emergent_universe::scenario::plane(
        emergent_universe::Config::default(),
        seed,
        emergent_universe::fleet::Order::Sparse,
        1,
        members,
    )
    .expect("plane");
    let mut u = p.u;
    let (t0, t1) = (u.now, 0i64);

    let mut out = std::io::BufWriter::new(std::fs::File::create("kicks.jsonl").expect("kicks.jsonl"));
    let mut seen: Vec<Option<i64>> = Vec::new();
    let (mut kicks, mut handoffs, mut other, mut new_entry) = (0u64, 0u64, 0u64, 0u64);
    let (mut cycle_rebinds, mut passages) = (0u64, 0u64);
    let mut exact: HashSet<u64> = HashSet::new();
    let mut quantized: HashSet<u64> = HashSet::new();
    let mut kind_counts: [u64; 4] = [0; 4];
    let mut retired: u64 = 0;

    let frames = (seconds * 60.0) as usize;
    let wall = std::time::Instant::now();
    for n in 1..=frames {
        if wall.elapsed().as_secs_f64() >= 52.0 {
            eprintln!("wall guard at frame {n}");
            break;
        }
        let _ = n;
        seen.resize(u.n_bodies(), None);
        for (i, s) in seen.iter_mut().enumerate() {
            let rec = u.rec(i);
            if !rec.alive {
                continue;
            }
            let k = match rec.kind {
                Kind::Ship => 0,
                Kind::Player => 1,
                Kind::Planet => 2,
                Kind::Moon => 3,
            };
            let Some(item) = rec.plan.first().copied() else { continue };
            if !matches!(item.what, What::Kick(_)) || *s == Some(item.t) {
                continue;
            }
            *s = Some(item.t);
            let upd = step::process(&u.ctx(), i, rec);
            kind_counts[k] += 1;
            retired += upd.retired.len() as u64;
            match upd.kind {
                step::Resolved::Kick => kicks += 1,
                step::Resolved::Handoff => handoffs += 1,
                _ => other += 1,
            }
            let b = &upd.rec.b;
            // shape accounting (kick_bench's Shapes, exact + quantized memo)
            if let Some(e) = &upd.new_entry {
                new_entry += 1;
                match &e.trajectory {
                    Trajectory::Cycle(c) => {
                        cycle_rebinds += 1;
                        let key = c.key();
                        if let Ok(sk) = ShapeKey::for_orbit(key) {
                            let mut h = std::collections::hash_map::DefaultHasher::new();
                            std::hash::Hash::hash(&format!("{sk:?}"), &mut h);
                            exact.insert(std::hash::Hasher::finish(&h));
                        }
                        if let Ok(mc) = MemoCode::encode(key) {
                            quantized.insert(mc.bits());
                        }
                    }
                    Trajectory::Passage(_) => passages += 1,
                }
            }
            let kind_str = match upd.kind {
                step::Resolved::Kick => "K",
                step::Resolved::Handoff => "H",
                step::Resolved::Lost => "L",
                step::Resolved::Refused => "R",
                step::Resolved::Open | step::Resolved::Boundary => "O",
            };
            let r = &b.residual;
            writeln!(
                out,
                "{i}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                item.t, kind_str, k, b.doll, b.tube.key, b.tube.periapsis_angle,
                b.tube.periapsis_time.get() as i64,
                b.kick.dv[0], b.kick.dv[1], b.kick.len, b.kick.level,
                b.kick.clock as u8, b.kick.boundary, b.kick.lead,
                r.position[0], r.position[1], r.velocity[0], r.velocity[1],
                b.turn.a, b.turn.b, b.event_time,
                upd.rec.carry[0], upd.rec.carry[1],
                upd.new_entry.is_some() as u8,
            )
            .expect("write");
        }
        u.frame(1.0 / 60.0, rtf, Budget::unlimited());
        u.settle(u.now);
    }
    out.flush().expect("flush");
    let game_seconds = (u.now - t0) as f64 * emergent_universe::view::TICK_SECONDS;
    let sz = |n: &str, s: usize| println!("size {n} = {s}");
    sz("Binding", std::mem::size_of::<emergent_universe::bind::Binding>());
    sz("Segment", std::mem::size_of::<emergent_universe::body::Segment>());
    sz("BodyRec", std::mem::size_of::<emergent_universe::body::BodyRec>());
    sz("Trajectory", std::mem::size_of::<Trajectory>());
    sz("Entry", std::mem::size_of::<emergent_universe::bind::Entry>());
    sz("Tube", std::mem::size_of::<emergent_space::Tube>());
    sz("Residual", std::mem::size_of::<emergent_space::binding::Residual>());
    println!(
        "frames_done game_seconds ticks t0 t1 bodies kicks handoffs other kind_ship kind_player kind_planet kind_moon retired_segments new_entries cycle_rebinds passages exact_shapes quantized_shapes catalogue_live stats_kicks stats_events rtf seed members",
    );
    println!(
        "{} {:.6} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {:?} {} {} {} {}",
        frames, game_seconds, u.now - t0, t0, u.now, u.n_bodies(),
        kicks, handoffs, other,
        kind_counts[0], kind_counts[1], kind_counts[2], kind_counts[3],
        retired, new_entry, cycle_rebinds, passages,
        exact.len(), quantized.len(),
        0, // catalogue_live placeholder (probe never applies entries)
        format!("{:?}", u.stats.kicks),
        u.stats.events(),
        rtf, seed, members,
    );
}
