//! Small adversarial round trips (well under a second): the Elias–Fano set against brute force,
//! and the block codecs on extreme words, outliers and every width.
use emergent_shipmem::bits::PAD;
use emergent_shipmem::codec::{access, decode_block, Buf, Enc, MAXC};
use emergent_shipmem::pop::Rng;
use emergent_shipmem::program::Ef;

#[test]
fn elias_fano_matches_brute_force() {
    let mut r = Rng::new(7);
    for &(u, k) in &[
        (1u64, 0usize),
        (1, 1),
        (1000, 0),
        (1000, 1),
        (1000, 999),
        (1 << 20, 100),
        (1 << 20, 50_000),
        (5, 5),
    ] {
        let mut v: Vec<u64> = (0..k).map(|_| r.below(u)).collect();
        v.sort_unstable();
        v.dedup();
        let ef = Ef::new(&v, u);
        let got: Vec<u64> = ef.cursor(0).map(|x| x.1).collect();
        assert_eq!(got, v);
        for _ in 0..2000 {
            let x = r.below(u);
            assert_eq!(
                ef.find(x),
                v.binary_search(&x).ok(),
                "find {x} in u={u} k={k}"
            );
            assert_eq!(ef.rank(x), v.partition_point(|&y| y < x), "rank {x}");
        }
        for j0 in [0, v.len() / 2, v.len()] {
            assert_eq!(ef.cursor(j0).count(), v.len() - j0.min(v.len()));
        }
    }
}

#[test]
fn block_codecs_round_trip_extremes() {
    let mut r = Rng::new(11);
    let mut enc = Enc::new(true);
    let mut buf = Buf::default();
    let mut out = Buf::default();
    for case in 0..400 {
        let n = 1 + (case * 7) % 256;
        let cols = 1 + case % MAXC;
        buf.n = n;
        for c in 0..cols {
            let w = (case * 13 + c * 5) % 65;
            let base = if case % 3 == 0 {
                u64::MAX - 5
            } else {
                r.next()
            };
            for i in 0..n {
                let x = match (case + c) % 6 {
                    0 => base,
                    1 => base.wrapping_add(i as u64 * 4096),
                    2 => base.wrapping_add(if w == 0 { 0 } else { r.next() >> (64 - w) }),
                    3 => [1u64, 2, 3, 5][(r.next() % 4) as usize],
                    4 => {
                        if r.next() % 16 == 0 {
                            r.next()
                        } else {
                            base.wrapping_sub(i as u64)
                        }
                    }
                    _ => buf.col[0][i].wrapping_mul(3),
                };
                buf.col[c][i] = x;
            }
        }
        let refs: [u64; MAXC] = std::array::from_fn(|_| r.next());
        let mut bytes = Vec::new();
        enc.block(cols, &buf, &refs, &mut bytes);
        bytes.extend_from_slice(&[0; PAD]);
        decode_block(&bytes, n, cols, &refs, &mut out);
        for c in 0..cols {
            assert_eq!(&out.col[c][..n], &buf.col[c][..n], "case {case} col {c}");
        }
        let mut s = [0u64; MAXC];
        for i in (0..n).step_by(7) {
            access(&bytes, n, cols, &refs, i, &mut s);
            for c in 0..cols {
                assert_eq!(s[c], buf.col[c][i], "access case {case} col {c} member {i}");
            }
        }
    }
}
