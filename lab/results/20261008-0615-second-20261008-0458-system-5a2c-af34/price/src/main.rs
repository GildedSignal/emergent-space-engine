//! Prices a reband scar layer and the literal Form-P inference with the SHIPPED
//! `emergent-shipmem` codec. Nothing here re-implements shipmem accounting.
//!
//! Modes (stdin or file arg):
//!   price <n>            rows "ordinal d0 d1" -> shipped Program::seal_from bytes for the
//!                        scar layer (prog = Const(0), the record-predicted base; deltas are
//!                        the body's departure from its record, zigzag-packed by the block
//!                        codec, ordinals Elias–Fano).
//!   infer <n> <cols>     rows "c0 c1 ..." (one member per line, birth order) -> the shipped
//!                        `program::infer` verdict on the members.
use emergent_shipmem::codec::MAXC;
use emergent_shipmem::program::{infer, Program, Prog};
use std::io::Read;

fn read_rows(path: &str) -> Vec<Vec<i64>> {
    let mut s = String::new();
    if path == "-" {
        std::io::stdin().read_to_string(&mut s).unwrap();
    } else {
        s = std::fs::read_to_string(path).unwrap();
    }
    s.lines()
        .filter(|l| !l.trim().is_empty() && !l.starts_with('#'))
        .map(|l| l.split_whitespace().map(|x| x.parse::<i64>().unwrap()).collect())
        .collect()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args[1].clone();
    let n: u64 = args[2].parse().unwrap();
    let rows = read_rows(args.get(3).map(|s| s.as_str()).unwrap_or("-"));
    match mode.as_str() {
        "price" => {
            let mut enc = emergent_shipmem::codec::Enc::new(true);
            let scars: Vec<(u64, [u64; MAXC])> = rows
                .iter()
                .map(|r| {
                    let mut s = [0u64; MAXC];
                    s[0] = r[1] as u64; // signed departure, wrapping-cast as seal_from expects
                    s[1] = r[2] as u64;
                    (r[0] as u64, s)
                })
                .collect();
            let prog = [Prog::Const(0), Prog::Const(0), Prog::Const(0), Prog::Const(0),
                        Prog::Const(0), Prog::Const(0), Prog::Const(0), Prog::Const(0)];
            let p = Program::seal_from(n, 2, prog, &scars, &mut enc);
            println!(
                "scars {} bytes {} bits_per_body {:.4} bits_per_scar {:.3}",
                p.scars(),
                p.bytes(),
                p.bytes() as f64 * 8.0 / n as f64,
                p.bytes() as f64 * 8.0 / p.scars().max(1) as f64
            );
        }
        "infer" => {
            let m: Vec<[u64; MAXC]> = rows
                .iter()
                .map(|r| {
                    let mut s = [0u64; MAXC];
                    for (f, v) in r.iter().enumerate() {
                        s[f] = *v as u64;
                    }
                    s
                })
                .collect();
            match infer(&m, 2) {
                Some(prog) => println!("infer: Some({:?})", &prog[..2]),
                None => println!("infer: None (Form P rejects the members: no majority program)"),
            }
        }
        _ => panic!("unknown mode"),
    }
}
