//! The degradation benchmark: `ladder <rung> <m> <npop> <updates> [out.jsonl]`, rung one of
//! 0, 1e-4, 1e-3, 1e-2, 1e-1, 0.3, 1 (the fraction of members kicked), poisson, random.
//! Every population is stored twice, as a program plus scars (form P) and as packed blocks in
//! birth order (form B); the store keeps the smaller. Every round trip is checked bit for bit.
use emergent_shipmem::codec::{Buf, Enc, MAXC};
use emergent_shipmem::pop::{ladder, Pop, Rng, Rung};
use emergent_shipmem::program::{infer, Program};
use emergent_shipmem::shelf::{Kind, Shelf, Ship};
use std::io::Write;
use std::process::Command;
use std::time::Instant;

const COLS: usize = 5;

fn sh(cmd: &str, args: &[&str]) -> String {
    Command::new(cmd)
        .args(args)
        .output()
        .map(|o| {
            String::from_utf8_lossy(&o.stdout)
                .trim()
                .replace('\n', " / ")
                .replace('"', "'")
        })
        .unwrap_or_default()
}
fn machine() -> String {
    format!(
        "load {} ; swap {} ; therm {} ; power {}",
        sh("sysctl", &["-n", "vm.loadavg"]),
        sh("sysctl", &["-n", "vm.swapusage"]),
        sh("pmset", &["-g", "therm"]),
        sh("pmset", &["-g", "batt"]).split(';').next().unwrap_or("")
    )
}
fn med(mut v: Vec<f64>) -> f64 {
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    v[v.len() / 2]
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let rung = match a[1].as_str() {
        "poisson" => Rung::Poisson,
        "random" => Rung::Random,
        x => Rung::Rate(x.parse().unwrap()),
    };
    let m: usize = a[2].parse().unwrap();
    let npop: usize = a[3].parse().unwrap();
    let updates: usize = a[4].parse().unwrap();
    let out_path = a.get(5).cloned();
    let before = machine();
    let wall = Instant::now();
    let mut enc = Enc::new(true);
    let mut shelves: Vec<Shelf> = Vec::new();
    let mut progs: Vec<Option<Program>> = Vec::new();
    let (mut floor, mut n) = (0f64, 0u64);
    let (mut p_ns, mut b_ns) = (0u128, 0u128);
    let mut inferred_ok = true;
    let mut pmap: Vec<(usize, std::ops::Range<u32>)> = Vec::new();
    for g in 0..npop {
        let (mut mem, bits, prog) = ladder(rung, m, g as u64);
        floor += bits;
        n += mem.len() as u64;
        if let Some(p) = prog {
            let inf = infer(&mem, COLS);
            inferred_ok &= inf.map(|q| q[..COLS] == p[..COLS]).unwrap_or(false);
            let t = Instant::now();
            progs.push(Some(Program::with_prog(&mem, COLS, p, &mut enc)));
            p_ns += t.elapsed().as_nanos();
        } else {
            progs.push(None);
        }
        if shelves.last().is_none_or(|s| s.n >= 1 << 20) {
            shelves.push(Shelf::new(COLS, 128, Pop::Convoy.orders(), true));
        }
        let t = Instant::now();
        let r = shelves
            .last_mut()
            .unwrap()
            .add_group(&mut mem, Kind::Slot { grid: 0 });
        pmap.push((shelves.len() - 1, r));
        b_ns += t.elapsed().as_nanos();
    }
    for s in &mut shelves {
        s.shrink();
    }
    let nf = n as f64;
    let b_bytes: usize = shelves.iter().map(|s| s.bytes()).sum();
    let p_bytes: Option<usize> = progs.iter().map(|p| p.as_ref().map(|p| p.bytes())).sum();
    let scars: usize = progs.iter().flatten().map(|p| p.scars()).sum();
    // The chosen form: per population, the smaller (form B's share by its member count).
    let b_per = b_bytes as f64 / nf;
    let chosen: f64 = progs
        .iter()
        .map(|p| match p {
            Some(p) => (p.bytes() as f64).min(b_per * p.n as f64),
            None => b_per * m as f64,
        })
        .sum();

    // Round trips.
    let mut buf = Buf::default();
    let mut rbuf = Buf::default();
    let mut bad = 0u64;
    for (gi, (si, gs)) in pmap.iter().enumerate() {
        let (mem, _, _) = ladder(rung, m, gi as u64);
        let s = &shelves[*si];
        let mut k = 0;
        for g in gs.clone() {
            let gr = s.groups[g as usize];
            for bi in gr.first as usize..(gr.first + gr.nb) as usize {
                s.decode_into(bi, &mut buf);
                for i in 0..buf.n {
                    bad += (0..COLS).any(|c| buf.col[c][i] != mem[k][c]) as u64;
                    k += 1;
                }
            }
        }
        bad += (k != mem.len()) as u64;
        if let Some(p) = &progs[gi] {
            p.for_each(&mut buf, &mut rbuf, |s0, b| {
                for i in 0..b.n {
                    bad += (0..COLS).any(|c| b.col[c][i] != mem[s0 as usize + i][c]) as u64;
                }
            });
        }
    }

    // Streaming, three passes each.
    let mut ck = 0u64;
    let (mut ps, mut bs) = (Vec::new(), Vec::new());
    for _ in 0..3 {
        if progs[0].is_some() {
            let t = Instant::now();
            for p in progs.iter().flatten() {
                p.for_each(&mut buf, &mut rbuf, |_, b| {
                    for c in 0..COLS {
                        ck = ck.wrapping_add(
                            b.col[c][..b.n].iter().fold(0u64, |x, &y| x.wrapping_add(y)),
                        );
                    }
                });
            }
            ps.push(t.elapsed().as_nanos() as f64 / nf);
        }
        let t = Instant::now();
        for s in &shelves {
            s.for_each(&mut buf, |b, _| {
                for c in 0..COLS {
                    ck = ck
                        .wrapping_add(b.col[c][..b.n].iter().fold(0u64, |x, &y| x.wrapping_add(y)));
                }
            });
        }
        bs.push(t.elapsed().as_nanos() as f64 / nf);
    }

    // Random access.
    let mut rng = Rng::new(0xACCE55);
    let mut out = [0u64; MAXC];
    let mut p_eval = f64::NAN;
    if progs[0].is_some() {
        let q: Vec<(usize, u64)> = (0..1_000_000)
            .map(|_| (rng.below(npop as u64) as usize, rng.below(m as u64)))
            .collect();
        let t = Instant::now();
        for &(g, i) in &q {
            progs[g].as_ref().unwrap().eval(i, &mut out);
            ck = ck.wrapping_add(out[0] ^ out[4]);
        }
        p_eval = t.elapsed().as_nanos() as f64 / q.len() as f64;
        let (mem, _, _) = ladder(rung, m, 0);
        for &(g, i) in q.iter().filter(|q| q.0 == 0).take(20_000) {
            progs[g].as_ref().unwrap().eval(i, &mut out);
            bad += (0..COLS).any(|c| out[c] != mem[i as usize][c]) as u64;
        }
    }
    let hq: Vec<(usize, u32)> = (0..1_000_000)
        .map(|_| {
            let si = rng.below(shelves.len() as u64) as usize;
            let bi = rng.below(shelves[si].blocks.len() as u64) as u32;
            let slot = rng.below(shelves[si].blocks[bi as usize].n as u64) as u32;
            (si, bi << 8 | slot)
        })
        .collect();
    let t = Instant::now();
    for &(si, h) in &hq {
        shelves[si].get(h, &mut out);
        ck = ck.wrapping_add(out[0] ^ out[4]);
    }
    let b_get = t.elapsed().as_nanos() as f64 / hq.len() as f64;

    // Queries on form P: arcs (which ships occupy a phase window), certificates, split.
    let mut extra = String::new();
    if let Some(p0) = &progs[0] {
        let (mem, _, prog) = ladder(rung, m, 0);
        let t_of = |i: u64| prog.unwrap()[0].at(i);
        let width = 1000u64 << 12;
        let arcs: Vec<(u64, u64)> = (0..100_000)
            .map(|_| {
                let lo = t_of(0).wrapping_add(rng.below((m as u64) << 12));
                (lo, lo + width)
            })
            .collect();
        let t = Instant::now();
        let mut total = 0u64;
        for &(lo, hi) in &arcs {
            total += p0.count_arc(lo, hi).unwrap();
        }
        let arc_ns = t.elapsed().as_nanos() as f64 / arcs.len() as f64;
        for &(lo, hi) in arcs.iter().take(50) {
            let brute = mem.iter().filter(|s| s[0] >= lo && s[0] <= hi).count() as u64;
            bad += (brute != p0.count_arc(lo, hi).unwrap()) as u64;
        }
        let t = Instant::now();
        let mut acc = 0i128;
        for k in 0..1_000_000u64 {
            let i0 = k * 7919 % m as u64;
            acc += p0.bounds(i0, (i0 + 1000).min(m as u64 - 1))[2].1;
        }
        let bounds_ns = t.elapsed().as_nanos() as f64 / 1e6;
        let mut split_ns = Vec::new();
        for k in 0..5 {
            let s = (k as u64 * 2 + 1) * m as u64 / 11;
            let t = Instant::now();
            let (l, r) = p0.split(s, &mut enc);
            split_ns.push(t.elapsed().as_nanos() as f64);
            for i in (0..m as u64).step_by(97) {
                if i < s {
                    l.eval(i, &mut out);
                } else {
                    r.eval(i - s, &mut out);
                }
                bad += (0..COLS).any(|c| out[c] != mem[i as usize][c]) as u64;
            }
        }
        extra = format!(
            ",\"arc_ns\":{:.0},\"arc_ships_mean\":{:.0},\"bounds_ns\":{:.1},\"split_ns\":{:.0},\"bounds_ck\":{}",
            arc_ns,
            total as f64 / arcs.len() as f64,
            bounds_ns,
            med(split_ns),
            acc % 7
        );
    }

    // Events on population 0: kicks at random ordinals, both forms, then recompression.
    let mut upd = String::new();
    if updates > 0 {
        let (mut mem, _, _) = ladder(rung, m, 0);
        let mut krng = Rng::new(0xE7E47);
        let mut restores: Vec<(usize, Ship)> = Vec::new();
        let targets: Vec<usize> = (0..updates)
            .map(|_| krng.below(m as u64) as usize)
            .collect();
        let news: Vec<Ship> = targets
            .iter()
            .map(|&i| {
                let s = Pop::Convoy.kick(&mem[i], &mut krng);
                mem[i] = s;
                s
            })
            .collect();
        if let Some(p0) = progs[0].as_mut() {
            let (b0, k0) = (p0.bytes(), p0.scars());
            let t = Instant::now();
            for (&i, s) in targets.iter().zip(&news) {
                p0.update(i as u64, *s);
            }
            let hot = t.elapsed().as_nanos() as f64 / updates as f64;
            let t = Instant::now();
            p0.seal(&mut enc);
            let seal = t.elapsed().as_nanos() as f64 / updates as f64;
            let (b1, k1) = (p0.bytes(), p0.scars());
            // Reabsorption: half of the kicked ships return exactly to their program.
            let prog = ladder(rung, 1, 0).2.unwrap();
            let mut back: Vec<usize> = targets.clone();
            back.sort_unstable();
            back.dedup();
            back.truncate(back.len() / 2);
            for &i in &back {
                let mut s = [0u64; MAXC];
                for f in 0..COLS {
                    s[f] = prog[f].at(i as u64);
                }
                mem[i] = s;
                p0.update(i as u64, s);
            }
            p0.seal(&mut enc);
            let (b2, k2) = (p0.bytes(), p0.scars());
            p0.for_each(&mut buf, &mut rbuf, |s0, b| {
                for i in 0..b.n {
                    bad += (0..COLS).any(|c| b.col[c][i] != mem[s0 as usize + i][c]) as u64;
                }
            });
            upd += &format!(
                ",\"p_update_ns\":{:.0},\"p_seal_ns_per_update\":{:.0},\"p_new_scars\":{},\"dH_bits_per_kick\":{:.1},\"dH_bits_per_new_scar\":{:.1},\"reabsorbed\":{},\"dH_bits_per_reabsorb\":{:.1}",
                hot,
                seal,
                k1 as i64 - k0 as i64,
                (b1 as f64 - b0 as f64) * 8.0 / updates as f64,
                (b1 as f64 - b0 as f64) * 8.0 / (k1 as f64 - k0 as f64).max(1.0),
                k1 as i64 - k2 as i64,
                (b2 as f64 - b1 as f64) * 8.0 / (k1 as f64 - k2 as f64).max(1.0)
            );
        }
        if let Some(prog) = ladder(rung, 1, 0).2 {
            if progs[0].is_none() {
                // no program: the restore step above did not run
            } else {
                let mut back: Vec<usize> = targets.clone();
                back.sort_unstable();
                back.dedup();
                back.truncate(back.len() / 2);
                restores = back
                    .iter()
                    .map(|&i| {
                        let mut s = [0u64; MAXC];
                        for f in 0..COLS {
                            s[f] = prog[f].at(i as u64);
                        }
                        (i, s)
                    })
                    .collect();
            }
        }
        let s = &mut shelves[0];
        let phase = |ops: &[(usize, Ship)], s: &mut Shelf| -> (f64, f64, f64) {
            let b0 = s.bytes();
            let t = Instant::now();
            for (i, x) in ops {
                s.update(((i / 128) as u32) << 8 | (i % 128) as u32, *x);
            }
            let hot = t.elapsed().as_nanos() as f64 / ops.len().max(1) as f64;
            let t = Instant::now();
            s.compact();
            let comp = t.elapsed().as_nanos() as f64 / ops.len().max(1) as f64;
            s.tidy();
            (
                hot,
                comp,
                (s.bytes() as f64 - b0 as f64) * 8.0 / ops.len().max(1) as f64,
            )
        };
        let kicks: Vec<(usize, Ship)> = targets.iter().copied().zip(news.iter().copied()).collect();
        let (hot, comp, dk) = phase(&kicks, s);
        let (_, _, dr) = phase(&restores, s);
        let mut k = 0;
        for g in pmap[0].1.clone() {
            let gr = s.groups[g as usize];
            for bi in gr.first as usize..(gr.first + gr.nb) as usize {
                s.decode_into(bi, &mut buf);
                for i in 0..buf.n {
                    bad += (0..COLS).any(|c| buf.col[c][i] != mem[k][c]) as u64;
                    k += 1;
                }
            }
        }
        upd += &format!(
            ",\"b_update_ns\":{:.0},\"b_compact_ns_per_update\":{:.0},\"b_dH_bits_per_kick\":{:.1},\"b_dH_bits_per_restore\":{:.1}",
            hot, comp, dk, dr
        );
    }

    let line = format!(
        "{{\"rung\":\"{}\",\"m\":{},\"npop\":{},\"n\":{},\"floor_bits\":{:.4},\"p_bits\":{},\"b_bits\":{:.4},\"chosen_bits\":{:.4},\"bytes_per_million\":{:.0},\"scars\":{},\"inferred\":{},\"p_build_ns\":{:.1},\"b_build_ns\":{:.1},\"p_stream_ns\":{:.2},\"b_stream_ns\":{:.2},\"p_eval_ns\":{:.1},\"b_get_ns\":{:.1}{}{},\"mismatches\":{},\"wall_s\":{:.1},\"ck\":{},\"before\":\"{}\",\"after\":\"{}\"}}",
        a[1],
        m,
        npop,
        n,
        floor / nf,
        p_bytes.map(|b| format!("{:.4}", b as f64 * 8.0 / nf)).unwrap_or("null".into()),
        b_bytes as f64 * 8.0 / nf,
        chosen * 8.0 / nf,
        chosen / nf * 1e6,
        scars,
        inferred_ok,
        p_ns as f64 / nf,
        b_ns as f64 / nf,
        if ps.is_empty() { f64::NAN } else { med(ps) },
        med(bs),
        p_eval,
        b_get,
        extra,
        upd,
        bad,
        wall.elapsed().as_secs_f64(),
        ck,
        before,
        machine()
    );
    let line = line.replace("NaN", "null");
    println!("{line}");
    if let Some(p) = out_path {
        let mut f = std::fs::OpenOptions::new()
            .create(true)
            .append(true)
            .open(p)
            .unwrap();
        writeln!(f, "{line}").unwrap();
    }
    assert_eq!(bad, 0, "round trip failed");
}
