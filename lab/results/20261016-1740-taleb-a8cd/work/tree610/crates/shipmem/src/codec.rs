//! One block: up to `MAXB` members, one column per state field. Each column is encoded by the
//! cheapest of five transforms, chosen by exact size, then bit-packed at the width its
//! residuals need, with rare outliers patched as exceptions ("the width follows the
//! information"). Every reference is a real member of the block or of the group, never a mean.
//!
//! - FOR: v − min.
//! - DFOR: v_i − v_{i−1} − (smallest step): sorted runs and arithmetic progressions.
//! - CHORD: v − the line through the block's first and last member, in column 0 (a field
//!   that follows the clock, like a port's angle along a traffic stream).
//! - DICT: an index into the block's distinct values (a few departure keys, a few kinds).
//! - TIED(c): a function of column c's dictionary index (L follows E): zero bits per member.
//! - REF: every member equals the group reference: one byte for the whole column.
//! - FORZ, DFORZ: FOR and DFOR around the block's median value or step (a real member's), in
//!   zigzag, so one outlier on either side is an exception instead of widening every member.
//!
//! Field layout: tag (codec | 8 if exceptions), width, codec parameters (varints relative to
//! the group reference), [exception count, (position, high bits)…], packed residuals.
use crate::bits::*;

pub const MAXB: usize = 256;
pub const MAXC: usize = 8;
pub const MAXD: usize = 64;

pub const FOR: u8 = 0;
pub const DFOR: u8 = 1;
pub const CHORD: u8 = 2;
pub const DICT: u8 = 3;
pub const TIED: u8 = 4;
pub const FORZ: u8 = 5;
pub const DFORZ: u8 = 6;
pub const REF: u8 = 7;
pub const NCODEC: usize = 8;
const EXC: u8 = 8;

/// A decoded block, column-major.
pub struct Buf {
    pub n: usize,
    pub col: Vec<[u64; MAXB]>,
    pub idx: Vec<[u8; MAXB]>,
    pub m: [usize; MAXC],
    tmp: Box<[u64; MAXB]>,
}
impl Default for Buf {
    fn default() -> Self {
        Self {
            n: 0,
            col: vec![[0; MAXB]; MAXC],
            idx: vec![[0; MAXB]; MAXC],
            m: [0; MAXC],
            tmp: Box::new([0; MAXB]),
        }
    }
}

#[derive(Default, Clone)]
pub struct Stats {
    pub bytes: [u64; MAXC],
    pub codec: [[u64; NCODEC]; MAXC],
    pub exceptions: u64,
}

#[derive(Default)]
pub struct Enc {
    pub stats: Stats,
    pub chord: bool,
    best: Vec<u8>,
    cand: Vec<u8>,
    e: Vec<u64>,
    d: Vec<u64>,
    idx: Vec<[u8; MAXB]>,
    m: [usize; MAXC],
}

/// The width minimizing packed bits plus patched exceptions (at most n/8 of them).
fn choose(e: &[u64]) -> (u32, usize) {
    let mut cnt = [0usize; 65];
    for &x in e {
        cnt[bitlen(x) as usize] += 1;
    }
    let maxb = (0..=64).rev().find(|&b| cnt[b] > 0).unwrap_or(0);
    let n = e.len();
    let (mut best_w, mut best_k, mut best_cost) = (maxb, 0usize, n * maxb);
    let (mut w, mut gt) = (maxb, 0usize);
    while w > 0 {
        gt += cnt[w];
        w -= 1;
        if gt > n / 8 {
            break;
        }
        let mut cost = n * w + 8 * uv_len(gt as u128);
        for (b, &c) in cnt.iter().enumerate().take(maxb + 1).skip(w + 1) {
            cost += c * (8 + 8 * (b - w).div_ceil(7));
        }
        if cost < best_cost {
            (best_w, best_k, best_cost) = (w, gt, cost);
        }
    }
    (best_w as u32, best_k)
}
fn uv_len(x: u128) -> usize {
    (bitlen128(x) as usize).div_ceil(7).max(1)
}
fn residuals(e: &[u64], w: u32, k: usize, out: &mut Vec<u8>) {
    if k > 0 {
        put_uv(out, k as u128);
        for (j, &x) in e.iter().enumerate() {
            if bitlen(x) > w {
                out.push(j as u8);
                put_uv(out, (x >> w) as u128);
            }
        }
    }
    pack(e, w, out);
}
fn tag(codec: u8, k: usize) -> u8 {
    codec | if k > 0 { EXC } else { 0 }
}

fn c_for(v: &[u64], r: u64, e: &mut Vec<u64>, out: &mut Vec<u8>) -> usize {
    let base = *v.iter().min().unwrap();
    e.clear();
    e.extend(v.iter().map(|&x| x - base));
    let (w, k) = choose(e);
    out.push(tag(FOR, k));
    out.push(w as u8);
    put_uv(out, zz(base as i128 - r as i128));
    residuals(e, w, k, out);
    k
}
fn c_dfor(v: &[u64], r: u64, e: &mut Vec<u64>, out: &mut Vec<u8>) -> usize {
    let dmin = v
        .windows(2)
        .map(|p| p[1].wrapping_sub(p[0]) as i64)
        .min()
        .unwrap();
    e.clear();
    e.extend(
        v.windows(2)
            .map(|p| p[1].wrapping_sub(p[0]).wrapping_sub(dmin as u64)),
    );
    let (w, k) = choose(e);
    out.push(tag(DFOR, k));
    out.push(w as u8);
    put_uv(out, zz(v[0] as i128 - r as i128));
    put_uv(out, zz(dmin as i128));
    residuals(e, w, k, out);
    k
}
#[inline(always)]
fn chord_pred(v0: i128, dv: i128, ds: i128, d: i128) -> i128 {
    let num = d * dv;
    if num.unsigned_abs() < (1u128 << 62) && ds < (1i128 << 62) {
        v0 + (num as i64).div_euclid(ds as i64) as i128
    } else {
        v0 + num.div_euclid(ds)
    }
}
fn median(v: impl Iterator<Item = u64>, d: &mut Vec<u64>) -> u64 {
    d.clear();
    d.extend(v);
    let k = d.len() / 2;
    *d.select_nth_unstable(k).1
}
fn c_forz(v: &[u64], r: u64, d: &mut Vec<u64>, e: &mut Vec<u64>, out: &mut Vec<u8>) -> usize {
    let med = median(v.iter().copied(), d);
    e.clear();
    e.extend(v.iter().map(|&x| zz64(x.wrapping_sub(med) as i64)));
    let (w, k) = choose(e);
    out.push(tag(FORZ, k));
    out.push(w as u8);
    put_uv(out, zz(med as i128 - r as i128));
    residuals(e, w, k, out);
    k
}
fn c_dforz(v: &[u64], r: u64, d: &mut Vec<u64>, e: &mut Vec<u64>, out: &mut Vec<u8>) -> usize {
    let dmed = median(v.windows(2).map(|p| p[1].wrapping_sub(p[0])), d);
    e.clear();
    e.extend(
        v.windows(2)
            .map(|p| zz64(p[1].wrapping_sub(p[0]).wrapping_sub(dmed) as i64)),
    );
    let (w, k) = choose(e);
    out.push(tag(DFORZ, k));
    out.push(w as u8);
    put_uv(out, zz(v[0] as i128 - r as i128));
    put_uv(out, zz(dmed as i64 as i128));
    residuals(e, w, k, out);
    k
}
fn c_chord(v: &[u64], s: &[u64], r: u64, e: &mut Vec<u64>, out: &mut Vec<u8>) -> Option<usize> {
    let n = v.len();
    if n < 3 || s[n - 1] <= s[0] {
        return None;
    }
    let (s0, ds) = (s[0] as i128, (s[n - 1] - s[0]) as i128);
    let (v0, dv) = (v[0] as i128, v[n - 1] as i128 - v[0] as i128);
    let maxs = s
        .iter()
        .map(|&x| (x as i128 - s0).unsigned_abs())
        .max()
        .unwrap();
    if bitlen128(maxs) + bitlen128(dv.unsigned_abs()) > 125 {
        return None;
    }
    let res: Vec<i128> = (0..n)
        .map(|i| v[i] as i128 - chord_pred(v0, dv, ds, s[i] as i128 - s0))
        .collect();
    let rmin = *res.iter().min().unwrap();
    e.clear();
    for &x in &res {
        e.push(u64::try_from(x - rmin).ok()?);
    }
    let (w, k) = choose(e);
    out.push(tag(CHORD, k));
    out.push(w as u8);
    put_uv(out, zz(v0 - r as i128));
    put_uv(out, zz(dv));
    put_uv(out, ds as u128);
    put_uv(out, zz(rmin));
    residuals(e, w, k, out);
    Some(k)
}
fn c_dict(
    v: &[u64],
    r: u64,
    d: &mut Vec<u64>,
    idx: &mut [u8; MAXB],
    out: &mut Vec<u8>,
) -> Option<usize> {
    d.clear();
    d.extend_from_slice(v);
    d.sort_unstable();
    d.dedup();
    let m = d.len();
    if !(2..=MAXD).contains(&m) {
        return None;
    }
    let w = bitlen(m as u64 - 1);
    out.push(DICT);
    out.push(w as u8);
    put_uv(out, m as u128);
    put_uv(out, zz(d[0] as i128 - r as i128));
    for j in 1..m {
        put_uv(out, (d[j] - d[j - 1]) as u128);
    }
    let mut e = [0u64; MAXB];
    for (i, &x) in v.iter().enumerate() {
        let k = d.binary_search(&x).unwrap();
        idx[i] = k as u8;
        e[i] = k as u64;
    }
    pack(&e[..v.len()], w, out);
    Some(m)
}
fn c_tied(v: &[u64], c: usize, m: usize, idx: &[u8; MAXB], r: u64, out: &mut Vec<u8>) -> bool {
    let mut map = [None::<u64>; MAXD];
    for (i, &x) in v.iter().enumerate() {
        let k = idx[i] as usize;
        match map[k] {
            None => map[k] = Some(x),
            Some(y) if y != x => return false,
            _ => {}
        }
    }
    out.push(TIED);
    out.push(0);
    out.push(c as u8);
    let mut prev = r as i128;
    for x in map.iter().take(m) {
        let x = x.unwrap() as i128;
        put_uv(out, zz(x - prev));
        prev = x;
    }
    true
}

impl Enc {
    pub fn new(chord: bool) -> Self {
        Self {
            chord,
            idx: vec![[0; MAXB]; MAXC],
            ..Default::default()
        }
    }
    /// Append one block (columns `buf.col[..cols][..buf.n]`) to `out`.
    pub fn block(&mut self, cols: usize, buf: &Buf, refs: &[u64], out: &mut Vec<u8>) {
        let n = buf.n;
        assert!((1..=MAXB).contains(&n));
        for f in 0..cols {
            let v = &buf.col[f][..n];
            let r = refs[f];
            if v.iter().all(|&x| x == r) {
                out.push(REF);
                self.m[f] = 0;
                self.stats.bytes[f] += 1;
                self.stats.codec[f][REF as usize] += 1;
                continue;
            }
            self.best.clear();
            let mut best_k = c_for(v, r, &mut self.e, &mut self.best);
            let mut codec = FOR;
            let mut dict_m = 0;
            if n >= 2 {
                self.cand.clear();
                let k = c_dfor(v, r, &mut self.e, &mut self.cand);
                if self.cand.len() < self.best.len() {
                    std::mem::swap(&mut self.best, &mut self.cand);
                    (codec, best_k) = (DFOR, k);
                }
            }
            self.cand.clear();
            let k = c_forz(v, r, &mut self.d, &mut self.e, &mut self.cand);
            if self.cand.len() < self.best.len() {
                std::mem::swap(&mut self.best, &mut self.cand);
                (codec, best_k) = (FORZ, k);
            }
            if n >= 2 {
                self.cand.clear();
                let k = c_dforz(v, r, &mut self.d, &mut self.e, &mut self.cand);
                if self.cand.len() < self.best.len() {
                    std::mem::swap(&mut self.best, &mut self.cand);
                    (codec, best_k) = (DFORZ, k);
                }
            }
            if self.chord && f > 0 {
                self.cand.clear();
                if let Some(k) = c_chord(v, &buf.col[0][..n], r, &mut self.e, &mut self.cand) {
                    if self.cand.len() < self.best.len() {
                        std::mem::swap(&mut self.best, &mut self.cand);
                        (codec, best_k) = (CHORD, k);
                    }
                }
            }
            if n >= 4 {
                self.cand.clear();
                if let Some(m) = c_dict(v, r, &mut self.d, &mut self.idx[f], &mut self.cand) {
                    if self.cand.len() < self.best.len() {
                        std::mem::swap(&mut self.best, &mut self.cand);
                        (codec, best_k, dict_m) = (DICT, 0, m);
                    }
                }
            }
            for c in 0..f {
                if self.m[c] > 0 {
                    self.cand.clear();
                    if c_tied(v, c, self.m[c], &self.idx[c], r, &mut self.cand)
                        && self.cand.len() < self.best.len()
                    {
                        std::mem::swap(&mut self.best, &mut self.cand);
                        (codec, best_k) = (TIED, 0);
                    }
                }
            }
            self.m[f] = if codec == DICT { dict_m } else { 0 };
            out.extend_from_slice(&self.best);
            self.stats.bytes[f] += self.best.len() as u64;
            self.stats.codec[f][codec as usize] += 1;
            self.stats.exceptions += best_k as u64;
        }
    }
}

struct Exc {
    k: usize,
    pos: [u8; MAXB / 8 + 1],
    high: [u64; MAXB / 8 + 1],
}
#[inline]
fn read_exc(b: &[u8], p: &mut usize, tag: u8) -> Exc {
    let mut x = Exc {
        k: 0,
        pos: [0; MAXB / 8 + 1],
        high: [0; MAXB / 8 + 1],
    };
    if tag & EXC != 0 {
        x.k = get_uv(b, p) as usize;
        for j in 0..x.k {
            x.pos[j] = b[*p];
            *p += 1;
            x.high[j] = get_uv(b, p) as u64;
        }
    }
    x
}

/// Decode a whole block into `buf`; returns the bytes read. `b` must extend `PAD` bytes past
/// the block.
pub fn decode_block(b: &[u8], n: usize, cols: usize, refs: &[u64], buf: &mut Buf) -> usize {
    buf.n = n;
    let mut p = 0;
    for (f, &r) in refs.iter().enumerate().take(cols) {
        let tag = b[p];
        buf.m[f] = 0;
        if tag == REF {
            buf.col[f][..n].fill(r);
            p += 1;
            continue;
        }
        let w = b[p + 1] as u32;
        p += 2;
        let (head, rest) = buf.col.split_at_mut(f);
        let out = &mut rest[0];
        let tmp = &mut buf.tmp;
        match tag & 7 {
            FOR => {
                let base = (r as i128 + get_zz(b, &mut p)) as u64;
                let x = read_exc(b, &mut p, tag);
                unsafe { unpack(b.as_ptr().add(p), n, w, &mut tmp[..]) };
                for j in 0..x.k {
                    tmp[x.pos[j] as usize] |= x.high[j] << w;
                }
                for i in 0..n {
                    out[i] = base.wrapping_add(tmp[i]);
                }
                p += packed_bytes(n, w);
            }
            DFOR => {
                let v0 = (r as i128 + get_zz(b, &mut p)) as u64;
                let dmin = get_zz(b, &mut p) as i64 as u64;
                let x = read_exc(b, &mut p, tag);
                unsafe { unpack(b.as_ptr().add(p), n - 1, w, &mut tmp[..]) };
                for j in 0..x.k {
                    tmp[x.pos[j] as usize] |= x.high[j] << w;
                }
                let mut acc = v0;
                out[0] = v0;
                for i in 1..n {
                    acc = acc.wrapping_add(tmp[i - 1]).wrapping_add(dmin);
                    out[i] = acc;
                }
                p += packed_bytes(n - 1, w);
            }
            FORZ => {
                let med = (r as i128 + get_zz(b, &mut p)) as u64;
                let x = read_exc(b, &mut p, tag);
                unsafe { unpack(b.as_ptr().add(p), n, w, &mut tmp[..]) };
                for j in 0..x.k {
                    tmp[x.pos[j] as usize] |= x.high[j] << w;
                }
                for i in 0..n {
                    out[i] = med.wrapping_add(unzz64(tmp[i]) as u64);
                }
                p += packed_bytes(n, w);
            }
            DFORZ => {
                let v0 = (r as i128 + get_zz(b, &mut p)) as u64;
                let dmed = get_zz(b, &mut p) as i64 as u64;
                let x = read_exc(b, &mut p, tag);
                unsafe { unpack(b.as_ptr().add(p), n - 1, w, &mut tmp[..]) };
                for j in 0..x.k {
                    tmp[x.pos[j] as usize] |= x.high[j] << w;
                }
                let mut acc = v0;
                out[0] = v0;
                for i in 1..n {
                    acc = acc
                        .wrapping_add(dmed)
                        .wrapping_add(unzz64(tmp[i - 1]) as u64);
                    out[i] = acc;
                }
                p += packed_bytes(n - 1, w);
            }
            CHORD => {
                let v0 = r as i128 + get_zz(b, &mut p);
                let dv = get_zz(b, &mut p);
                let ds = get_uv(b, &mut p) as i128;
                let rmin = get_zz(b, &mut p);
                let x = read_exc(b, &mut p, tag);
                unsafe { unpack(b.as_ptr().add(p), n, w, &mut tmp[..]) };
                for j in 0..x.k {
                    tmp[x.pos[j] as usize] |= x.high[j] << w;
                }
                let s = &head[0];
                let s0 = s[0] as i128;
                for i in 0..n {
                    out[i] =
                        (chord_pred(v0, dv, ds, s[i] as i128 - s0) + rmin + tmp[i] as i128) as u64;
                }
                p += packed_bytes(n, w);
            }
            DICT => {
                let m = get_uv(b, &mut p) as usize;
                let mut d = [0u64; MAXD];
                d[0] = (r as i128 + get_zz(b, &mut p)) as u64;
                for j in 1..m {
                    d[j] = d[j - 1] + get_uv(b, &mut p) as u64;
                }
                unsafe { unpack(b.as_ptr().add(p), n, w, &mut tmp[..]) };
                let ix = &mut buf.idx[f];
                for i in 0..n {
                    ix[i] = tmp[i] as u8;
                    out[i] = d[tmp[i] as usize];
                }
                buf.m[f] = m;
                p += packed_bytes(n, w);
            }
            TIED => {
                let c = b[p] as usize;
                p += 1;
                let m = buf.m[c];
                let mut map = [0u64; MAXD];
                let mut prev = r as i128;
                for e in map.iter_mut().take(m) {
                    prev += get_zz(b, &mut p);
                    *e = prev as u64;
                }
                let ix = &buf.idx[c];
                for i in 0..n {
                    out[i] = map[ix[i] as usize];
                }
            }
            _ => unreachable!(),
        }
    }
    p
}

/// Member `i` of a block, without decoding the block. O(1) per column except DFOR (a prefix
/// sum over at most `i` residuals).
pub fn access(b: &[u8], n: usize, cols: usize, refs: &[u64], i: usize, out: &mut [u64; MAXC]) {
    let mut p = 0;
    let mut idx = [0usize; MAXC];
    let mut ms = [0usize; MAXC];
    let mut s0 = 0u64;
    let base_ptr = b.as_ptr();
    for f in 0..cols {
        let r = refs[f];
        let tag = b[p];
        if tag == REF {
            out[f] = r;
            if f == 0 {
                s0 = r;
            }
            p += 1;
            continue;
        }
        let w = b[p + 1] as u32;
        p += 2;
        let exc_at = |x: &Exc, j: usize| -> u64 {
            for q in 0..x.k {
                if x.pos[q] as usize == j {
                    return x.high[q] << w;
                }
            }
            0
        };
        match tag & 7 {
            FOR => {
                let base = (r as i128 + get_zz(b, &mut p)) as u64;
                let x = read_exc(b, &mut p, tag);
                let pl = unsafe { base_ptr.add(p) };
                out[f] = base.wrapping_add(unsafe { rd(pl, i, w) } | exc_at(&x, i));
                if f == 0 {
                    s0 = base.wrapping_add(unsafe { rd(pl, 0, w) } | exc_at(&x, 0));
                }
                p += packed_bytes(n, w);
            }
            DFOR => {
                let v0 = (r as i128 + get_zz(b, &mut p)) as u64;
                let dmin = get_zz(b, &mut p) as i64 as u64;
                let x = read_exc(b, &mut p, tag);
                let pl = unsafe { base_ptr.add(p) };
                let mut acc = v0.wrapping_add((i as u64).wrapping_mul(dmin));
                for j in 0..i {
                    acc = acc.wrapping_add(unsafe { rd(pl, j, w) });
                }
                for q in 0..x.k {
                    if (x.pos[q] as usize) < i {
                        acc = acc.wrapping_add(x.high[q] << w);
                    }
                }
                out[f] = acc;
                if f == 0 {
                    s0 = v0;
                }
                p += packed_bytes(n - 1, w);
            }
            FORZ => {
                let med = (r as i128 + get_zz(b, &mut p)) as u64;
                let x = read_exc(b, &mut p, tag);
                let pl = unsafe { base_ptr.add(p) };
                out[f] = med.wrapping_add(unzz64(unsafe { rd(pl, i, w) } | exc_at(&x, i)) as u64);
                if f == 0 {
                    s0 = med.wrapping_add(unzz64(unsafe { rd(pl, 0, w) } | exc_at(&x, 0)) as u64);
                }
                p += packed_bytes(n, w);
            }
            DFORZ => {
                let v0 = (r as i128 + get_zz(b, &mut p)) as u64;
                let dmed = get_zz(b, &mut p) as i64 as u64;
                let x = read_exc(b, &mut p, tag);
                let pl = unsafe { base_ptr.add(p) };
                let mut acc = v0.wrapping_add((i as u64).wrapping_mul(dmed));
                let mut q = 0;
                for j in 0..i {
                    let mut e = unsafe { rd(pl, j, w) };
                    if q < x.k && x.pos[q] as usize == j {
                        e |= x.high[q] << w;
                        q += 1;
                    }
                    acc = acc.wrapping_add(unzz64(e) as u64);
                }
                out[f] = acc;
                if f == 0 {
                    s0 = v0;
                }
                p += packed_bytes(n - 1, w);
            }
            CHORD => {
                let v0 = r as i128 + get_zz(b, &mut p);
                let dv = get_zz(b, &mut p);
                let ds = get_uv(b, &mut p) as i128;
                let rmin = get_zz(b, &mut p);
                let x = read_exc(b, &mut p, tag);
                let pl = unsafe { base_ptr.add(p) };
                let e = unsafe { rd(pl, i, w) } | exc_at(&x, i);
                out[f] =
                    (chord_pred(v0, dv, ds, out[0] as i128 - s0 as i128) + rmin + e as i128) as u64;
                p += packed_bytes(n, w);
            }
            DICT => {
                let m = get_uv(b, &mut p) as usize;
                let mut d = [0u64; MAXD];
                d[0] = (r as i128 + get_zz(b, &mut p)) as u64;
                for j in 1..m {
                    d[j] = d[j - 1] + get_uv(b, &mut p) as u64;
                }
                let pl = unsafe { base_ptr.add(p) };
                let k = unsafe { rd(pl, i, w) } as usize;
                out[f] = d[k];
                idx[f] = k;
                ms[f] = m;
                if f == 0 {
                    s0 = d[unsafe { rd(pl, 0, w) } as usize];
                }
                p += packed_bytes(n, w);
            }
            TIED => {
                let c = b[p] as usize;
                p += 1;
                let mut prev = r as i128;
                let mut v = 0u64;
                for k in 0..ms[c] {
                    prev += get_zz(b, &mut p);
                    if k == idx[c] {
                        v = prev as u64;
                    }
                }
                out[f] = v;
            }
            _ => unreachable!(),
        }
    }
}
