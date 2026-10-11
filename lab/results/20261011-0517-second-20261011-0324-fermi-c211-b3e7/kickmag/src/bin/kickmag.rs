//! The kick-magnitude rung (the checker's named experiment for 20261011-0324-fermi-c211).
//!
//! The shipped `Pop::kick` uses one hardcoded delta magnitude (t ±2^16, E/L/ω ±2^10 on the
//! 48/48/32/32-bit fields). This sweep applies the ladder's own store (form P: program +
//! scars; form B: packed blocks; the store keeps the smaller) to convoys kicked at magnitudes
//! from the shipped one up to family-jumping element changes (a fresh uniform orbit draw),
//! and measures the scar constant, the admission curve and the packed-form ceiling at each.
//!
//! Usage:
//!   kickmag curve <bt>,<be>,<bl>,<bw>|k0|k1|k2|k3|k4|k5|uniform <m> <npop> <f> [out.jsonl]
//!   kickmag events <mode> <m> <updates> [out.jsonl]
//! Mode is the per-field delta exponent (bt on t, be on E, bl on L, bw on ω); `uniform`
//! (be = -1) redraws E, L as a fresh law orbit and ω uniform, keeping t's delta at bt.
//! Every population round-trips bit for bit (asserted).
use emergent_shipmem::codec::{Buf, Enc, MAXC};
use emergent_shipmem::pop::{ladder, Pop, Rng, Rung};
use emergent_shipmem::program::{infer, Program};
use emergent_shipmem::shelf::{Kind, Shelf, Ship};
use std::io::Write;
use std::time::Instant;

const COLS: usize = 5;

#[derive(Clone, Copy)]
struct Mode {
    bt: i32,
    be: i32,
    bl: i32,
    bw: i32,
}
impl Mode {
    fn parse(s: &str) -> Self {
        match s {
            "k0" => Mode { bt: 16, be: 10, bl: 10, bw: 10 }, // shipped Pop::kick
            "k1" => Mode { bt: 22, be: 16, bl: 16, bw: 16 },
            "k2" => Mode { bt: 28, be: 22, bl: 22, bw: 22 },
            "k3" => Mode { bt: 34, be: 28, bl: 28, bw: 28 },
            "k4" => Mode { bt: 40, be: 34, bl: 34, bw: 34 },
            "k5" => Mode { bt: 46, be: 40, bl: 40, bw: 40 },
            "uniform" => Mode { bt: 46, be: -1, bl: -1, bw: -1 },
            x => {
                let v: Vec<i32> = x.split(',').map(|t| t.parse().unwrap()).collect();
                Mode { bt: v[0], be: v[1], bl: v[2], bw: v[3] }
            }
        }
    }
    fn name(&self) -> String {
        if self.be < 0 {
            "uniform".into()
        } else {
            format!("{},{},{},{}", self.bt, self.be, self.bl, self.bw)
        }
    }
}

/// A fresh law orbit (mirrors the private pop::orbit, same draw order).
fn orbit(r: &mut Rng) -> (u64, u64) {
    let p = r.range(100 << 16, 8000 << 16) as u32;
    let e = r.below((0.6 * (1u64 << 30) as f64) as u64) as u32;
    let k = emergent_space::Key::darwin(p, e).expect("bound orbit");
    (k.energy.get(), k.angular.get())
}

/// Pop::Convoy's kick, with the delta exponent per field (and the family-jump redraw).
fn kick_mag(s: &Ship, r: &mut Rng, m: Mode) -> Ship {
    let mut s = *s;
    let d = |r: &mut Rng, b: i32| r.below(2u64 << b).wrapping_sub(1u64 << b);
    s[0] = s[0].wrapping_add(d(r, m.bt));
    if m.be < 0 {
        let (e, l) = orbit(r);
        s[2] = e;
        s[3] = l;
        s[4] = r.bitsn(32);
    } else {
        s[2] = s[2].wrapping_add(d(r, m.be));
        s[3] = s[3].wrapping_add(d(r, m.bl));
        s[4] = s[4].wrapping_add(d(r, m.bw)) & 0xFFFF_FFFF;
    }
    s
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let mode = Mode::parse(&a[2]);
    let m: usize = a[3].parse().unwrap();
    let out_path = a.last().cloned().filter(|p| p.ends_with(".jsonl"));
    let enc = &mut Enc::new(true);
    let mut bad = 0u64;
    let line = if a[1] == "curve" {
        // ---- The admission curve: kick exactly f of the members once, both forms. ----
        let npop: usize = a[4].parse().unwrap();
        let f: f64 = a[5].parse().unwrap();
        let k = (f * m as f64).round() as usize;
        let mut enc2 = Enc::new(true);
        let mut shelves: Vec<Shelf> = Vec::new();
        let mut progs: Vec<Program> = Vec::new();
        let mut pmap: Vec<(usize, std::ops::Range<u32>)> = Vec::new();
        let (mut floor, mut n) = (0f64, 0u64);
        let mut inferred_ok = true;
        let mut members_all: Vec<Vec<Ship>> = Vec::new();
        let mut kr = Rng::new(0xFACE + mode.bt as u64 * 1000 + (mode.be.max(0) + 1) as u64);
        let mut sel = Rng::new(0x5EED);
        for g in 0..npop {
            let (mem, bits, prog) = ladder(Rung::Rate(0.0), m, g as u64);
            let prog = prog.unwrap();
            let mut mem = mem;
            floor += bits;
            // distinct kicked members: shuffle ordinals (sel, unaccounted), kick the first k
            let mut idx: Vec<u32> = (0..m as u32).collect();
            for i in (1..idx.len()).rev() {
                let j = sel.below((i + 1) as u64) as usize;
                idx.swap(i, j);
            }
            let fb = kr.bits;
            for &i in &idx[..k] {
                mem[i as usize] = kick_mag(&mem[i as usize], &mut kr, mode);
            }
            floor += kr.bits - fb;
            n += mem.len() as u64;
            inferred_ok &= infer(&mem, COLS).is_some();
            progs.push(Program::with_prog(&mem, COLS, prog, &mut enc2));
            if shelves.last().is_none_or(|s| s.n >= 1 << 20) {
                shelves.push(Shelf::new(COLS, 128, Pop::Convoy.orders(), true));
            }
            let r = shelves
                .last_mut()
                .unwrap()
                .add_group(&mut mem, Kind::Slot { grid: 0 });
            pmap.push((shelves.len() - 1, r));
            members_all.push(mem);
        }
        for s in &mut shelves {
            s.shrink();
        }
        let nf = n as f64;
        let b_bytes: usize = shelves.iter().map(|s| s.bytes()).sum();
        let p_bytes: usize = progs.iter().map(|p| p.bytes()).sum();
        let scars: usize = progs.iter().map(|p| p.scars()).sum();
        let b_per = b_bytes as f64 / nf;
        let chosen: f64 = progs
            .iter()
            .zip(&members_all)
            .map(|(p, mem)| (p.bytes() as f64).min(b_per * mem.len() as f64))
            .sum();
        // round trips
        let (mut buf, mut rbuf) = (Buf::default(), Buf::default());
        for (gi, (si, gs)) in pmap.iter().enumerate() {
            let mem = &members_all[gi];
            let s = &shelves[*si];
            let mut c = 0;
            for g in gs.clone() {
                let gr = s.groups[g as usize];
                for bi in gr.first as usize..(gr.first + gr.nb) as usize {
                    s.decode_into(bi, &mut buf);
                    for i in 0..buf.n {
                        bad += (0..COLS).any(|x| buf.col[x][i] != mem[c][x]) as u64;
                        c += 1;
                    }
                }
            }
            bad += (c != mem.len()) as u64;
            progs[gi].for_each(&mut buf, &mut rbuf, |s0, b| {
                for i in 0..b.n {
                    bad += (0..COLS).any(|x| b.col[x][i] != mem[s0 as usize + i][x]) as u64;
                }
            });
        }
        format!(
            "{{\"kind\":\"curve\",\"mode\":\"{}\",\"m\":{},\"npop\":{},\"f\":{},\"kicked\":{},\"scars\":{},\"p_bits\":{:.4},\"b_bits\":{:.4},\"chosen_bits\":{:.4},\"floor_bits\":{:.4},\"inferred\":{},\"mismatches\":{}}}",
            mode.name(), m, npop, f, k * npop, scars,
            p_bytes as f64 * 8.0 / nf, b_bytes as f64 * 8.0 / nf, chosen * 8.0 / nf,
            floor / nf, inferred_ok, bad
        )
    } else {
        // ---- Events on a perfect convoy: U random-ordinal kicks, hot map, seal, reabsorb. ----
        let updates: usize = a[4].parse().unwrap();
        let (mem, _, prog) = ladder(Rung::Rate(0.0), m, 0);
        let prog = prog.unwrap();
        let mut mem = mem;
        let mut p = Program::with_prog(&mem, COLS, prog, enc);
        let mut kr = Rng::new(0xE7E47);
        let targets: Vec<usize> = (0..updates).map(|_| kr.below(m as u64) as usize).collect();
        let (b0, k0) = (p.bytes(), p.scars());
        let t = Instant::now();
        for &i in &targets {
            let s = kick_mag(&mem[i], &mut kr, mode);
            mem[i] = s;
            p.update(i as u64, s);
        }
        let hot = t.elapsed().as_nanos() as f64 / updates as f64;
        let t = Instant::now();
        p.seal(enc);
        let seal = t.elapsed().as_nanos() as f64 / updates as f64;
        let (b1, k1) = (p.bytes(), p.scars());
        // reabsorption: half the kicked members return exactly to their program
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
            p.update(i as u64, s);
        }
        p.seal(enc);
        let (b2, k2) = (p.bytes(), p.scars());
        let (mut buf, mut rbuf) = (Buf::default(), Buf::default());
        p.for_each(&mut buf, &mut rbuf, |s0, b| {
            for i in 0..b.n {
                bad += (0..COLS).any(|x| b.col[x][i] != mem[s0 as usize + i][x]) as u64;
            }
        });
        // form B: same kicks on the packed shelf, then compact
        let (mem2, _, _) = ladder(Rung::Rate(0.0), m, 0);
        let mut mem2 = mem2;
        let mut s = Shelf::new(COLS, 128, Pop::Convoy.orders(), true);
        s.add_group(&mut mem2, Kind::Slot { grid: 0 });
        let mut kr2 = Rng::new(0xE7E47);
        let bb0 = s.bytes();
        let t = Instant::now();
        for _ in 0..updates {
            let i = kr2.below(m as u64) as usize;
            let sh = kick_mag(&mem2[i], &mut kr2, mode);
            mem2[i] = sh;
            s.update(((i / 128) as u32) << 8 | (i % 128) as u32, sh);
        }
        let b_hot = t.elapsed().as_nanos() as f64 / updates as f64;
        let t = Instant::now();
        s.compact();
        let b_comp = t.elapsed().as_nanos() as f64 / updates as f64;
        s.tidy();
        let bb1 = s.bytes();
        let mut c = 0;
        for g in 0..s.groups.len() {
            let gr = s.groups[g];
            for bi in gr.first as usize..(gr.first + gr.nb) as usize {
                s.decode_into(bi, &mut buf);
                for i in 0..buf.n {
                    bad += (0..COLS).any(|x| buf.col[x][i] != mem2[c][x]) as u64;
                    c += 1;
                }
            }
        }
        bad += (c != mem2.len()) as u64;
        format!(
            "{{\"kind\":\"events\",\"mode\":\"{}\",\"m\":{},\"updates\":{},\"p_update_ns\":{:.0},\"p_seal_ns_per_update\":{:.0},\"p_new_scars\":{},\"dH_bits_per_kick\":{:.1},\"dH_bits_per_new_scar\":{:.1},\"reabsorbed\":{},\"dH_bits_per_reabsorb\":{:.1},\"b_update_ns\":{:.0},\"b_compact_ns_per_update\":{:.0},\"b_dH_bits_per_kick\":{:.1},\"mismatches\":{}}}",
            mode.name(), m, updates, hot, seal,
            k1 as i64 - k0 as i64,
            (b1 as f64 - b0 as f64) * 8.0 / updates as f64,
            (b1 as f64 - b0 as f64) * 8.0 / (k1 as f64 - k0 as f64).max(1.0),
            k1 as i64 - k2 as i64,
            (b2 as f64 - b1 as f64) * 8.0 / (k1 as f64 - k2 as f64).max(1.0),
            b_hot, b_comp, (bb1 as f64 - bb0 as f64) * 8.0 / updates as f64, bad
        )
    };
    println!("{line}");
    if let Some(p) = out_path {
        let mut f = std::fs::OpenOptions::new().create(true).append(true).open(p).unwrap();
        writeln!(f, "{line}").unwrap();
    }
    assert_eq!(bad, 0, "round trip failed");
}

