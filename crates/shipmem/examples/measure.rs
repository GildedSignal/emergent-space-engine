//! `cargo run --release -p emergent-shipmem --example measure -- <pop> <n> [updates] [bsize] [out.jsonl]`
//! Builds a population of about n ships, measures bits per ship against the entropy floor,
//! streaming decode, random access and event updates, and checks every round trip bit for bit.
use emergent_shipmem::codec::{Buf, MAXC, NCODEC};
use emergent_shipmem::pop::{log2_factorial, Group, Pop, Rng};
use emergent_shipmem::shelf::{cmp, Kind, Shelf, Ship};
use std::io::Write;
use std::process::Command;
use std::time::Instant;

const SHELF: u64 = 1 << 20;

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
        sh("pmset", &["-g", "batt"])
    )
}
fn canon(pop: Pop, grp: &mut Group) {
    if let Kind::Sorted { order } = grp.kind {
        let o = pop.orders()[order as usize];
        grp.members
            .sort_unstable_by(|a, b| cmp(a, b, &o, pop.cols()));
    }
}
fn decode_group(s: &Shelf, g: usize, buf: &mut Buf, out: &mut Vec<Ship>) {
    out.clear();
    let gr = s.groups[g];
    for bi in gr.first as usize..(gr.first + gr.nb) as usize {
        if s.blocks[bi].n == 0 {
            continue;
        }
        s.decode_into(bi, buf);
        for i in 0..buf.n {
            let mut x = [0u64; MAXC];
            for (c, v) in x.iter_mut().enumerate().take(s.cols) {
                *v = buf.col[c][i];
            }
            out.push(x);
        }
    }
}
fn pct(v: &mut [u64], q: f64) -> u64 {
    v.sort_unstable();
    v[((v.len() - 1) as f64 * q) as usize]
}
fn parse_n(s: &str) -> u64 {
    if let Some((a, b)) = s.split_once('e') {
        (a.parse::<f64>().unwrap() * 10f64.powi(b.parse().unwrap())) as u64
    } else {
        s.parse().unwrap()
    }
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let pop = Pop::parse(&a[1]).expect("pop: formation convoy stream battle traders random");
    let n = parse_n(&a[2]);
    let updates: usize = a.get(3).map(|s| parse_n(s) as usize).unwrap_or(0);
    let bsize: usize = a.get(4).map(|s| s.parse().unwrap()).unwrap_or(128);
    let out_path = a.get(5).cloned();
    let chord = std::env::var("SHIPMEM_NOCHORD").is_err();
    // Identity from provenance for exchangeable populations: keep birth order, do not sort.
    let birth = std::env::var("SHIPMEM_BIRTH").is_ok();
    let cols = pop.cols();
    let before = machine();
    let wall = Instant::now();

    // Build, one group at a time (the source is dropped after encoding).
    let mut shelves: Vec<Shelf> = Vec::new();
    let mut map: Vec<(usize, std::ops::Range<u32>)> = Vec::new();
    let (mut total, mut floor_bits, mut g) = (0u64, 0f64, 0u64);
    let mut floor_ordered = 0f64;
    let (mut gen_ns, mut enc_ns) = (0u128, 0u128);
    while total < n {
        let t = Instant::now();
        let mut grp = pop.group(g);
        if birth {
            grp.kind = Kind::Slot { grid: 0 };
        }
        gen_ns += t.elapsed().as_nanos();
        let m = grp.members.len() as u64;
        floor_bits += grp.bits
            - if grp.exchangeable {
                log2_factorial(m)
            } else {
                0.0
            };
        floor_ordered += grp.bits;
        if shelves
            .last()
            .is_none_or(|s| s.n >= SHELF || (grp.exchangeable && s.n > 0))
        {
            shelves.push(Shelf::new(cols, bsize, pop.orders(), chord));
        }
        let t = Instant::now();
        let s = shelves.last_mut().unwrap();
        let gi = s.add_group(&mut grp.members, grp.kind);
        enc_ns += t.elapsed().as_nanos();
        map.push((shelves.len() - 1, gi));
        total += m;
        g += 1;
    }
    for s in &mut shelves {
        s.shrink();
    }
    let bytes: usize = shelves.iter().map(|s| s.bytes()).sum();
    let bits = bytes as f64 * 8.0 / total as f64;
    let floor = floor_bits / total as f64;
    let mut field_bits = vec![0f64; cols];
    let mut codecs = vec![[0u64; NCODEC]; cols];
    let mut exceptions = 0u64;
    for s in &shelves {
        for c in 0..cols {
            field_bits[c] += s.enc.stats.bytes[c] as f64 * 8.0 / total as f64;
            for k in 0..NCODEC {
                codecs[c][k] += s.enc.stats.codec[c][k];
            }
        }
        exceptions += s.enc.stats.exceptions;
    }
    let blocks: usize = shelves.iter().map(|s| s.blocks.len()).sum();
    let groups: usize = shelves.iter().map(|s| s.groups.len()).sum();

    // Streaming decode: every live member, every column (median of three passes).
    let mut buf = Buf::default();
    let mut passes = Vec::new();
    let mut ck = 0u64;
    for _ in 0..3 {
        let t = Instant::now();
        for s in &shelves {
            s.for_each(&mut buf, |b, _| {
                for c in 0..cols {
                    let mut acc = 0u64;
                    for &v in &b.col[c][..b.n] {
                        acc = acc.wrapping_add(v);
                    }
                    ck = ck.wrapping_add(acc).rotate_left(7);
                }
            });
        }
        passes.push(t.elapsed().as_nanos() as u64);
    }
    let stream_ns = pct(&mut passes, 0.5) as f64 / total as f64;

    // Round trip: regenerate every group and compare with its decode.
    let t = Instant::now();
    let mut mismatches = 0u64;
    let mut dec = Vec::new();
    for (gi, (si, sgs)) in map.iter().enumerate() {
        let si = *si;
        let mut grp = pop.group(gi as u64);
        if birth {
            grp.kind = Kind::Slot { grid: 0 };
        }
        canon(pop, &mut grp);
        dec.clear();
        let mut part = Vec::new();
        for sg in sgs.clone() {
            decode_group(&shelves[si], sg as usize, &mut buf, &mut part);
            dec.extend_from_slice(&part);
        }
        if dec.len() != grp.members.len() {
            mismatches += 1;
            continue;
        }
        mismatches += dec.iter().zip(&grp.members).filter(|(x, y)| x != y).count() as u64;
    }
    let verify_s = t.elapsed().as_secs_f64();

    // Random access over the whole store, then a check against block decodes.
    let mut rng = Rng::new(0xACCE55);
    let nb_cum: Vec<usize> = shelves
        .iter()
        .scan(0, |acc, s| {
            *acc += s.blocks.len();
            Some(*acc)
        })
        .collect();
    let pick = |rng: &mut Rng, shelves: &[Shelf]| -> (usize, u32) {
        let x = rng.below(blocks as u64) as usize;
        let si = nb_cum.partition_point(|&c| c <= x);
        let bi = x - if si == 0 { 0 } else { nb_cum[si - 1] };
        let slot = rng.below(shelves[si].blocks[bi].n as u64) as u32;
        (si, (bi as u32) << 8 | slot)
    };
    let handles: Vec<(usize, u32)> = (0..1_000_000).map(|_| pick(&mut rng, &shelves)).collect();
    let mut out = [0u64; MAXC];
    let t = Instant::now();
    for &(si, h) in &handles {
        shelves[si].get(h, &mut out);
        ck = ck.wrapping_add(out[0] ^ out[cols - 1]);
    }
    let rand_ns = t.elapsed().as_nanos() as f64 / handles.len() as f64;
    let mut rand_bad = 0u64;
    for &(si, h) in handles.iter().take(20_000) {
        shelves[si].get(h, &mut out);
        shelves[si].decode_into((h >> 8) as usize, &mut buf);
        let slot = (h & 255) as usize;
        rand_bad += (0..cols).any(|c| buf.col[c][slot] != out[c]) as u64;
    }

    // Events on the first shelf: hot path, then compaction (twice), each checked against an
    // oracle that applies the same meaning (a formation member returns to its slot; any other
    // kicked ship joins the doll's loose group).
    let mut upd = String::new();
    if updates > 0 {
        let s = &mut shelves[0];
        let mut oracle: Vec<Vec<Ship>> = Vec::new();
        for (gi, (si, _)) in map.iter().enumerate() {
            if *si == 0 {
                let mut grp = pop.group(gi as u64);
                if birth {
                    grp.kind = Kind::Slot { grid: 0 };
                }
                canon(pop, &mut grp);
                for chunk in grp.members.chunks(emergent_shipmem::shelf::MAXG) {
                    oracle.push(chunk.to_vec());
                }
            }
        }
        let bits0 = s.bytes() as f64 * 8.0 / s.n as f64;
        let mut hot_ns = Vec::with_capacity(updates);
        let (mut compact_total, mut max_step, mut arena_ns, mut repacks) =
            (0u128, 0u64, 0u64, 0u64);
        let mut ok = true;
        let mut krng = Rng::new(0xE7E47);
        for _round in 0..2 {
            // The hot tier is sized ahead, in idle time (a rehash inside an event is a spike).
            s.hot.reserve(updates / 2);
            s.forward.reserve(updates / 2);
            let mut pending: std::collections::HashMap<(usize, usize), Ship> = Default::default();
            for _ in 0..updates / 2 {
                let bi = krng.below(s.blocks.len() as u64) as usize;
                if s.blocks[bi].n == 0 {
                    continue;
                }
                let slot = krng.below(s.blocks[bi].n as u64) as usize;
                let h = (bi as u32) << 8 | slot as u32;
                s.get(h, &mut out);
                let new = pop.kick(&out, &mut krng);
                let t = Instant::now();
                s.update(h, new);
                hot_ns.push(t.elapsed().as_nanos() as u64);
                let br = s.blocks[bi];
                pending.insert((br.group as usize, br.start as usize + slot), new);
            }
            let t = Instant::now();
            let st = s.compact();
            s.tidy();
            compact_total += t.elapsed().as_nanos();
            max_step = max_step.max(st.max_step_ns);
            arena_ns = arena_ns.max(st.arena_ns);
            repacks += st.repacks;
            // Oracle: every ship keeps its slot.
            for (&(g, rank), &new) in &pending {
                oracle[g][rank] = new;
            }
            for (g, want) in oracle.iter().enumerate() {
                decode_group(s, g, &mut buf, &mut dec);
                if &dec != want {
                    ok = false;
                }
            }
            ok &= oracle.len() == s.groups.len();
        }
        let bits1 = s.bytes() as f64 * 8.0 / s.n as f64;
        let mean = hot_ns.iter().sum::<u64>() as f64 / hot_ns.len() as f64;
        let n_upd = hot_ns.len();
        upd = format!(
            ",\"updates\":{},\"hot_ns_mean\":{:.0},\"hot_ns_p50\":{},\"hot_ns_p99\":{},\"hot_ns_max\":{},\"compact_ns_per_update\":{:.0},\"compact_max_step_ns\":{},\"arena_compaction_ns\":{},\"repacks\":{},\"bits_before\":{:.2},\"bits_after\":{:.2},\"updates_roundtrip\":{}",
            n_upd,
            mean,
            pct(&mut hot_ns, 0.5),
            pct(&mut hot_ns, 0.99),
            pct(&mut hot_ns, 1.0),
            compact_total as f64 / n_upd as f64,
            max_step,
            arena_ns,
            repacks,
            bits0,
            bits1,
            ok
        );
    }

    let fb: Vec<String> = field_bits.iter().map(|x| format!("{x:.2}")).collect();
    let cd: Vec<String> = codecs.iter().map(|c| format!("{c:?}")).collect();
    let line = format!(
        "{{\"pop\":\"{}\",\"birth_order\":{},\"n\":{},\"bsize\":{},\"chord\":{},\"groups\":{},\"blocks\":{},\"floor_bits\":{:.2},\"floor_ordered_bits\":{:.2},\"bits\":{:.2},\"bytes\":{},\"field_bits\":[{}],\"codecs_for_dfor_chord_dict_tied_forz_dforz\":[{}],\"exceptions\":{},\"gen_ns\":{:.1},\"build_ns\":{:.1},\"stream_ns\":{:.2},\"rand_ns\":{:.1},\"roundtrip_mismatches\":{},\"rand_mismatches\":{},\"verify_s\":{:.1}{},\"wall_s\":{:.1},\"checksum\":{},\"before\":\"{}\",\"after\":\"{}\"}}",
        pop.name(),
        birth,
        total,
        bsize,
        chord,
        groups,
        blocks,
        floor,
        floor_ordered / total as f64,
        bits,
        bytes,
        fb.join(","),
        cd.join(","),
        exceptions,
        gen_ns as f64 / total as f64,
        enc_ns as f64 / total as f64,
        stream_ns,
        rand_ns,
        mismatches,
        rand_bad,
        verify_s,
        upd,
        wall.elapsed().as_secs_f64(),
        ck,
        before,
        machine()
    );
    println!("{line}");
    if let Some(p) = out_path {
        let mut f = std::fs::OpenOptions::new()
            .create(true)
            .append(true)
            .open(p)
            .unwrap();
        writeln!(f, "{line}").unwrap();
    }
    assert_eq!(mismatches, 0, "round trip failed");
    assert_eq!(rand_bad, 0, "random access failed");
}
