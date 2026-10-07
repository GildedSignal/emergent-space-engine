//! Scar bits per kick on the shipped `Shelf`, with the plane's own kick deltas.
//!
//! Belt: the ladder's perfect convoy program structure (`pop::ladder` rung
//! Rate(0): every column shared, t_p affine in 2^12) rebuilt at the plane's own
//! scale — Home's band, 1 AU = 99.3e6 root units — in the tube's native columns
//! [t_p, kind, p Q16, k Q48, w u32]. The shipped `Key`/darwin column space
//! cannot hold plane orbits (p <= 8192 M there vs ~1e8 M here; capture
//! measures 100% exclusion), so the belt is generated here, in this folder,
//! with the same structure and the same Shelf machinery (blocks, deltas,
//! scars, compact, repack) as `crates/shipmem/examples/ladder.rs`.
//!
//! Each round kicks `rate·m` members chosen uniformly, applies one captured
//! plane delta per kick (or, in `synthetic` mode, `Pop::Convoy.kick`'s uniform
//! deltas at the ladder's magnitudes), then `compact()`s.
use emergent_shipmem::codec::{Enc, MAXC};
use emergent_shipmem::pop::{Pop, Rng};
use emergent_shipmem::program::{infer, Prog, Program};
use emergent_shipmem::shelf::{Kind, Shelf, Ship};
use serde_json::{json, Value};
use std::time::Instant;

const COLS: usize = 5;

/// The perfect convoy program at the plane's scale (root units: the star's
/// GM/c^2; Home, the fleet's planet, is at 99.3e6). Columns [t, kind, p Q16,
/// k Q48, w u32]. Returns members in birth order, the entropy drawn, and the
/// launch program.
fn belt(m: usize, g: u64, belt_p0: Option<u64>) -> (Vec<Ship>, f64, [Prog; MAXC]) {
    let mut r = Rng::new(g ^ 0xBE17);
    let kind = r.below(64);
    let p0: u64 = belt_p0.unwrap_or_else(|| ((89_370_000i64 + r.below(19_860_000) as i64) << 16) as u64);
    // e in [0, 0.6): k = 2^96 / (2^48 + e_q48), the OrbitKey::bound relation.
    let e_q48 = r.below(((0.6f64) * (1u64 << 48) as f64) as u64);
    let k0: u64 = (((1u128 << 96) / ((1u128 << 48) + e_q48 as u128)) as u64);
    let w0 = r.bitsn(32);
    let t0 = r.bitsn(40);
    let mut prog = [Prog::Const(0); MAXC];
    prog[0] = Prog::Affine { a: t0, b: 1 << 12 };
    prog[1] = Prog::Const(kind);
    prog[2] = Prog::Const(p0);
    prog[3] = Prog::Const(k0);
    prog[4] = Prog::Const(w0);
    let mut out = Vec::with_capacity(m);
    for i in 0..m as u64 {
        let mut s = [0u64; MAXC];
        for f in 0..COLS {
            s[f] = prog[f].at(i);
        }
        out.push(s);
    }
    (out, r.bits, prog)
}

fn med(mut v: Vec<f64>) -> f64 {
    if v.is_empty() {
        return f64::NAN;
    }
    v.sort_by(f64::total_cmp);
    v[v.len() / 2]
}

fn log2abs(x: i64) -> Option<f64> {
    (x != 0).then(|| (x.unsigned_abs() as f64).log2())
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let kicks_path = a[1].clone();
    let m: usize = a[2].parse().unwrap();
    let rounds: usize = a[3].parse().unwrap();
    let rate: f64 = a[4].parse().unwrap();
    let mode = a.get(5).cloned().unwrap_or_else(|| "plane".into());
    let belt_seed: u64 = a.get(6).and_then(|s| s.parse().ok()).unwrap_or(0x5EED);
    let doll_filter: i64 = a.get(7).and_then(|s| s.parse().ok()).unwrap_or(0);
    let belt_p0: Option<u64> = a.get(8).and_then(|s| s.parse().ok());

    let kicks: Vec<Value> =
        serde_json::from_str(&std::fs::read_to_string(&kicks_path).unwrap()).expect("kicks json");
    let get = |k: &Value, f: &str| k[f].as_i64().unwrap_or(0);
    let doll0: Vec<&Value> = kicks.iter().filter(|k| get(k, "doll") == doll_filter).collect();
    let frac = |f: &str| kicks.iter().filter(|k| get(k, f) == 0).count() as f64 / kicks.len() as f64;
    let medl = |f: &str| med(kicks.iter().filter_map(|k| log2abs(get(k, f))).collect());
    eprintln!(
        "{}",
        serde_json::to_string_pretty(&json!({
            "kicks_file": kicks_path, "kicks_total": kicks.len(), "kicks_doll0": doll0.len(),
            "delta_stats": {
                "dp_log2_median": medl("dp"), "dk_log2_median": medl("dk"),
                "dtp_log2_median": medl("dtp"), "dw_log2_median": medl("dw"),
                "dp_zero_frac": frac("dp"), "dk_zero_frac": frac("dk"),
                "dtp_zero_frac": frac("dtp"), "dw_zero_frac": frac("dw"),
            },
        }))
        .unwrap()
    );

    let wall = Instant::now();
    let (mut mem, bits, prog) = belt(m, belt_seed, belt_p0);
    let inferred_ok = infer(&mem, COLS)
        .map(|q| q[..COLS] == prog[..COLS])
        .unwrap_or(false);
    let mut enc = Enc::new(true);
    let prog_form = Program::with_prog(&mem, COLS, prog, &mut enc);
    let mut shelf = Shelf::new(COLS, 128, Pop::Convoy.orders(), true);
    let t0 = Instant::now();
    let gr = shelf.add_group(&mut mem, Kind::Slot { grid: 0 });
    let build_ns = t0.elapsed().as_nanos();
    let mut handles: Vec<u32> = Vec::with_capacity(m);
    for g in gr.clone() {
        let gref = shelf.groups[g as usize];
        for bi in gref.first as usize..(gref.first + gref.nb) as usize {
            let br = shelf.blocks[bi];
            for s in 0..br.n {
                handles.push(((bi as u32) << 8) | s as u32);
            }
        }
    }
    assert_eq!(handles.len(), m, "handle map covers the belt");
    drop(mem);
    shelf.shrink();
    let bytes_birth = shelf.bytes();

    let mut rng = Rng::new(belt_seed);
    let mut synth = Rng::new(belt_seed ^ 0x9E37);
    let picks = ((rate * m as f64).ceil() as usize).clamp(1, m);
    let mut applied = 0usize;
    let mut rows = Vec::new();
    let mut expect: Vec<(u32, Ship)> = Vec::new();
    let mut ship: Ship = [0u64; MAXC];
    for r in 0..rounds {
        let b_before = shelf.bytes();
        for j in 0..picks {
            let i = rng.below(m as u64) as usize;
            shelf.get(handles[i], &mut ship);
            if mode == "plane" {
                let k = doll0[(r * picks + j) % doll0.len()];
                ship[0] = ship[0].wrapping_add(get(k, "dtp") as u64);
                ship[2] = ship[2].wrapping_add(get(k, "dp") as u64);
                ship[3] = ship[3].wrapping_add(get(k, "dk") as u64);
                ship[4] = ship[4].wrapping_add(get(k, "dw") as u64) & 0xFFFF_FFFF;
            } else {
                ship = Pop::Convoy.kick(&ship, &mut synth);
            }
            shelf.update(handles[i], ship);
            if r + 1 == rounds {
                if let Some(e) = expect.iter_mut().find(|e| e.0 == handles[i]) {
                    e.1 = ship;
                } else {
                    expect.push((handles[i], ship));
                }
            }
            applied += 1;
        }
        let st = shelf.compact();
        let b_after = shelf.bytes();
        rows.push(json!({
            "round": r, "bytes": b_after, "d_bytes": b_after as i64 - b_before as i64,
            "repacks": st.repacks, "blocks_rewritten": st.blocks_rewritten,
            "max_compact_ns": st.max_step_ns, "arena_compactions": st.arena_compactions,
        }));
    }
    let half = rounds / 2;
    let b_half: i64 = rows[half]["bytes"].as_i64().unwrap();
    let b_last: i64 = rows.last().and_then(|v| v["bytes"].as_i64()).unwrap_or(b_half);
    let kicks_half = (rounds - half - 1) * picks;
    let bits_per_kick = if kicks_half > 0 {
        (b_last - b_half) as f64 * 8.0 / kicks_half as f64
    } else {
        f64::NAN
    };
    let mut bad = 0u64;
    for (h, exp) in &expect {
        shelf.get(*h, &mut ship);
        bad += u64::from(ship[..COLS] != exp[..COLS]);
    }
    println!(
        "{}",
        serde_json::to_string_pretty(&json!({
            "mode": mode, "m": m, "rounds": rounds, "rate": rate, "picks_per_round": picks,
            "applied_kicks": applied, "readback_bad": bad, "readback_checked": expect.len(),
            "belt_program": {
                "entropy_bits_floor": bits, "inferred_ok": inferred_ok,
                "program_bytes": prog_form.bytes(),
                "program_bits_per_body": prog_form.bytes() as f64 * 8.0 / m as f64,
                "scars_in_program_form": prog_form.scars(),
            },
            "shelf_birth_bytes": bytes_birth,
            "shelf_birth_bits_per_body": bytes_birth as f64 * 8.0 / m as f64,
            "build_ns": build_ns,
            "bytes_final": b_last,
            "bits_per_kick_steady": bits_per_kick,
            "bytes_first_round_delta": rows[0]["d_bytes"],
            "bytes_last_round_delta": rows.last().and_then(|v| v["d_bytes"].as_i64()),
            "rounds_log": rows,
            "wall_seconds": wall.elapsed().as_secs_f64(),
            "machine": {
                "load": std::fs::read_to_string("/proc/loadavg").unwrap_or_default().trim().to_string(),
                "meminfo": std::fs::read_to_string("/proc/meminfo").unwrap_or_default()
                    .lines().take(3).collect::<Vec<_>>().join(" "),
            },
        }))
        .unwrap()
    );
}
