//! Form P: a population as a program over its ordinals plus sparse scars.
//!
//! Ship i is `prog(i)` exactly, unless history scarred it: then its exact difference from its
//! program is stored at once. The program is an exact description of real individuals (a
//! convoy launched every Δt), never a statistic; every member stays individual and takes part
//! in every interaction. Identity is provenance: the ordinal. Scar ordinals are an Elias–Fano
//! set (about 2 + log2(n/k) bits each); scar values are rows of deltas from the program, packed
//! by the block codec. Events land in a small hot map; `seal` folds them in (a ship whose
//! state returns to its program is reabsorbed and costs nothing again).
use crate::bits::*;
use crate::codec::*;
use crate::shelf::{FxMap, Ship};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Prog {
    Belt(crate::belt::BeltColumn),
    Const(u64),
    /// a + b·i (wrapping).
    Affine {
        a: u64,
        b: i64,
    },
}
impl Prog {
    #[inline]
    pub fn at(self, i: u64) -> u64 {
        match self {
            Prog::Belt(b) => b.at(i),
            Prog::Const(v) => v,
            Prog::Affine { a, b } => a.wrapping_add((i as i64).wrapping_mul(b) as u64),
        }
    }
    fn shifted(self, s: u64) -> Self {
        match self {
            Prog::Belt(b) => Prog::Belt(b.shifted(s)),
            Prog::Const(v) => Prog::Const(v),
            Prog::Affine { a, b } => Prog::Affine {
                a: Prog::Affine { a, b }.at(s),
                b,
            },
        }
    }
}

/// Boyer–Moore majority, verified.
fn majority(it: impl Iterator<Item = u64> + Clone, n: usize) -> Option<u64> {
    let (mut cand, mut c) = (0u64, 0usize);
    for x in it.clone() {
        if c == 0 {
            cand = x;
            c = 1;
        } else if x == cand {
            c += 1;
        } else {
            c -= 1;
        }
    }
    (it.filter(|&x| x == cand).count() * 2 > n).then_some(cand)
}

/// Each column's program: the step shared by most consecutive real members, anchored at the
/// offset shared by most members. None if some column has no majority program.
pub fn infer(m: &[Ship], cols: usize) -> Option<[Prog; MAXC]> {
    let n = m.len();
    let mut prog = [Prog::Const(0); MAXC];
    for (f, p) in prog.iter_mut().enumerate().take(cols) {
        let b = if n < 2 {
            0
        } else {
            majority(m.windows(2).map(|w| w[1][f].wrapping_sub(w[0][f])), n - 1)? as i64
        };
        let a = majority(
            m.iter()
                .enumerate()
                .map(|(i, s)| s[f].wrapping_sub((i as i64).wrapping_mul(b) as u64)),
            n,
        )?;
        *p = if b == 0 {
            Prog::Const(a)
        } else {
            Prog::Affine { a, b }
        };
    }
    Some(prog)
}

/// Elias–Fano set of sorted values below `u`, with a sampled select0 for find and rank.
pub struct Ef {
    pub k: usize,
    pub u: u64,
    l: u32,
    low: Vec<u8>,
    high: Vec<u64>,
    samples: Vec<u32>,
}
impl Ef {
    pub fn new(v: &[u64], u: u64) -> Self {
        let k = v.len();
        let l = if k == 0 || u <= k as u64 {
            0
        } else {
            63 - (u / k as u64).leading_zeros()
        };
        let nhigh = if k == 0 { 1 } else { (u >> l) as usize + k + 1 };
        let mut high = vec![0u64; nhigh.div_ceil(64) + 1];
        let mut lows = Vec::with_capacity(k);
        for (j, &x) in v.iter().enumerate() {
            let p = (x >> l) as usize + j;
            high[p >> 6] |= 1 << (p & 63);
            lows.push(x & mask(l));
        }
        let mut low = Vec::new();
        pack(&lows, l, &mut low);
        low.extend_from_slice(&[0; PAD]);
        let mut samples = Vec::new();
        let mut zeros = 0usize;
        for p in 0..nhigh {
            if high[p >> 6] >> (p & 63) & 1 == 0 {
                if zeros % 64 == 0 {
                    samples.push(p as u32);
                }
                zeros += 1;
            }
        }
        Self {
            k,
            u,
            l,
            low,
            high,
            samples,
        }
    }
    pub fn bytes(&self) -> usize {
        self.low.capacity() + self.high.capacity() * 8 + self.samples.capacity() * 4
    }
    #[inline]
    fn low(&self, j: usize) -> u64 {
        unsafe { rd(self.low.as_ptr(), j, self.l) }
    }
    #[inline]
    fn bit(&self, p: usize) -> bool {
        self.high[p >> 6] >> (p & 63) & 1 == 1
    }
    fn select0(&self, h: usize) -> usize {
        let pos = self.samples[h >> 6] as usize;
        let mut r = h & 63;
        let mut w = pos >> 6;
        let mut word = !self.high[w] & (u64::MAX << (pos & 63));
        loop {
            let c = word.count_ones() as usize;
            if r < c {
                for _ in 0..r {
                    word &= word - 1;
                }
                return (w << 6) + word.trailing_zeros() as usize;
            }
            r -= c;
            w += 1;
            word = !self.high[w];
        }
    }
    #[inline]
    fn bucket(&self, h: usize) -> usize {
        if h == 0 {
            0
        } else {
            self.select0(h - 1) + 1
        }
    }
    /// The rank of x if x is in the set.
    pub fn find(&self, x: u64) -> Option<usize> {
        if self.k == 0 {
            return None;
        }
        let h = (x >> self.l) as usize;
        let xl = x & mask(self.l);
        let mut p = self.bucket(h);
        while self.bit(p) {
            let lo = self.low(p - h);
            if lo == xl {
                return Some(p - h);
            }
            if lo > xl {
                return None;
            }
            p += 1;
        }
        None
    }
    /// How many values are below x.
    pub fn rank(&self, x: u64) -> usize {
        if self.k == 0 {
            return 0;
        }
        if x >= self.u {
            return self.k;
        }
        let h = (x >> self.l) as usize;
        let xl = x & mask(self.l);
        let mut p = self.bucket(h);
        while self.bit(p) && self.low(p - h) < xl {
            p += 1;
        }
        p - h
    }
    /// (rank, value) for values from rank `j0` on, in order.
    pub fn cursor(&self, j0: usize) -> EfCursor<'_> {
        let mut c = EfCursor {
            ef: self,
            w: 0,
            word: self.high[0],
            j: 0,
        };
        if j0 >= self.k {
            c.j = self.k;
        } else if j0 > 0 {
            // Skip to the j0-th one: count ones word by word.
            let mut left = j0;
            loop {
                let ones = c.word.count_ones() as usize;
                if left < ones {
                    for _ in 0..left {
                        c.word &= c.word - 1;
                    }
                    break;
                }
                left -= ones;
                c.w += 1;
                c.word = self.high[c.w];
            }
            c.j = j0;
        }
        c
    }
}
pub struct EfCursor<'a> {
    ef: &'a Ef,
    w: usize,
    word: u64,
    j: usize,
}
impl Iterator for EfCursor<'_> {
    type Item = (usize, u64);
    #[inline]
    fn next(&mut self) -> Option<(usize, u64)> {
        if self.j >= self.ef.k {
            return None;
        }
        while self.word == 0 {
            self.w += 1;
            self.word = self.ef.high[self.w];
        }
        let p = self.w * 64 + self.word.trailing_zeros() as usize;
        self.word &= self.word - 1;
        let j = self.j;
        let v = (((p - j) as u64) << self.ef.l) | self.ef.low(j);
        self.j += 1;
        Some((j, v))
    }
}

/// Sparse exact differences from a base (a program, or packed blocks): Elias–Fano ranks plus
/// rows of zigzag deltas packed by the block codec.
pub struct Scars {
    pub ef: Ef,
    rows: Vec<u8>,
    rblocks: Vec<(u32, u16)>,
    pub maxdev: [u64; MAXC],
}
impl Scars {
    /// `entries`: (rank, full state, base state), sorted by rank; rows equal to their base are
    /// reabsorbed (not stored).
    pub fn new(n: u64, cols: usize, entries: &[(u64, Ship, Ship)], enc: &mut Enc) -> Self {
        let d: Vec<(u64, Ship)> = entries
            .iter()
            .map(|e| {
                let mut d = [0u64; MAXC];
                for f in 0..cols {
                    d[f] = zz64(e.1[f].wrapping_sub(e.2[f]) as i64);
                }
                (e.0, d)
            })
            .collect();
        Self::from_deltas(n, cols, &d, enc)
    }
    /// `entries`: (rank, zigzag deltas), sorted by rank; all-zero rows are reabsorbed.
    pub fn from_deltas(n: u64, cols: usize, entries: &[(u64, Ship)], enc: &mut Enc) -> Self {
        let kept: Vec<&(u64, Ship)> = entries
            .iter()
            .filter(|e| (0..cols).any(|f| e.1[f] != 0))
            .collect();
        let ords: Vec<u64> = kept.iter().map(|e| e.0).collect();
        let ef = Ef::new(&ords, n.max(1));
        let mut rows = Vec::new();
        let mut rblocks = Vec::new();
        let mut maxdev = [0u64; MAXC];
        let mut buf = Buf::default();
        for chunk in kept.chunks(RB) {
            buf.n = chunk.len();
            for (i, e) in chunk.iter().enumerate() {
                for f in 0..cols {
                    maxdev[f] = maxdev[f].max(unzz64(e.1[f]).unsigned_abs());
                    buf.col[f][i] = e.1[f];
                }
            }
            let off = rows.len() as u32;
            enc.block(cols, &buf, &[0; MAXC], &mut rows);
            rblocks.push((off, chunk.len() as u16));
        }
        rows.extend_from_slice(&[0; PAD]);
        rows.shrink_to_fit();
        rblocks.shrink_to_fit();
        Self {
            ef,
            rows,
            rblocks,
            maxdev,
        }
    }
    pub fn k(&self) -> usize {
        self.ef.k
    }
    pub fn bytes(&self) -> usize {
        std::mem::size_of::<Self>()
            + self.ef.bytes()
            + self.rows.capacity()
            + self.rblocks.capacity() * 8
    }
    /// Zigzag deltas of scar `j` (columns 0..cols).
    #[inline]
    pub fn row(&self, j: usize, out: &mut Ship, cols: usize) {
        let (off, n) = self.rblocks[j / RB];
        access(
            &self.rows[off as usize..],
            n as usize,
            cols,
            &[0; MAXC],
            j % RB,
            out,
        );
    }
    pub fn row_block(&self, rb: usize, cols: usize, buf: &mut Buf) {
        let (off, n) = self.rblocks[rb];
        decode_block(
            &self.rows[off as usize..],
            n as usize,
            cols,
            &[0; MAXC],
            buf,
        );
    }
    #[inline]
    pub fn apply(base: &mut Ship, d: &Ship, cols: usize) {
        for f in 0..cols {
            base[f] = base[f].wrapping_add(unzz64(d[f]) as u64);
        }
    }
}

pub struct Program {
    pub n: u64,
    pub cols: usize,
    pub prog: [Prog; MAXC],
    pub ef: Ef,
    rows: Vec<u8>,
    rblocks: Vec<(u32, u16)>,
    pub maxdev: [u64; MAXC],
    pub hot: FxMap<u32, Ship>,
}

pub const RB: usize = 128;

impl Program {
    /// Seal a program with its scars (ordinal, full state), sorted by ordinal.
    pub fn seal_from(
        n: u64,
        cols: usize,
        prog: [Prog; MAXC],
        scars: &[(u64, Ship)],
        enc: &mut Enc,
    ) -> Self {
        let ords: Vec<u64> = scars.iter().map(|s| s.0).collect();
        let ef = Ef::new(&ords, n.max(1));
        let mut rows = Vec::new();
        let mut rblocks = Vec::new();
        let mut maxdev = [0u64; MAXC];
        let mut buf = Buf::default();
        let zero = [0u64; MAXC];
        for chunk in scars.chunks(RB) {
            buf.n = chunk.len();
            for (i, (o, s)) in chunk.iter().enumerate() {
                for f in 0..cols {
                    let d = s[f].wrapping_sub(prog[f].at(*o)) as i64;
                    maxdev[f] = maxdev[f].max(d.unsigned_abs());
                    buf.col[f][i] = zz64(d);
                }
            }
            let off = rows.len() as u32;
            enc.block(cols, &buf, &zero, &mut rows);
            rblocks.push((off, chunk.len() as u16));
        }
        rows.extend_from_slice(&[0; PAD]);
        rows.shrink_to_fit();
        rblocks.shrink_to_fit();
        Self {
            n,
            cols,
            prog,
            ef,
            rows,
            rblocks,
            maxdev,
            hot: FxMap::default(),
        }
    }
    /// Infer the program from real members and seal every deviation as a scar.
    pub fn build(m: &[Ship], cols: usize, enc: &mut Enc) -> Option<Self> {
        Some(Self::with_prog(m, cols, infer(m, cols)?, enc))
    }
    /// Seal against a known program (the creating event's own description).
    pub fn with_prog(m: &[Ship], cols: usize, prog: [Prog; MAXC], enc: &mut Enc) -> Self {
        let scars: Vec<(u64, Ship)> = m
            .iter()
            .enumerate()
            .filter(|(i, s)| (0..cols).any(|f| s[f] != prog[f].at(*i as u64)))
            .map(|(i, s)| (i as u64, *s))
            .collect();
        Self::seal_from(m.len() as u64, cols, prog, &scars, enc)
    }
    pub fn bytes(&self) -> usize {
        std::mem::size_of::<Self>()
            + self.ef.bytes()
            + self.rows.capacity()
            + self.rblocks.capacity() * 8
            + self.hot.capacity() * 72
            + self.table_bytes()
    }
    pub fn scars(&self) -> usize {
        self.ef.k
    }
    /// The table is shared by all belt columns; count its payload once per population.
    pub fn table_bytes(&self) -> usize {
        if self.prog[..self.cols].iter().any(|p| matches!(p, Prog::Belt(_))) {
            crate::belt::Belt::table_bytes()
        } else { 0 }
    }
    #[inline]
    fn row(&self, j: usize, out: &mut Ship, cols: usize) {
        let (off, n) = self.rblocks[j / RB];
        access(
            &self.rows[off as usize..],
            n as usize,
            cols,
            &[0; MAXC],
            j % RB,
            out,
        );
    }
    /// Ship i, exactly.
    pub fn eval(&self, i: u64, out: &mut Ship) {
        if !self.hot.is_empty() {
            if let Some(s) = self.hot.get(&(i as u32)) {
                *out = *s;
                return;
            }
        }
        if let Some(mut s) = crate::belt::base(&self.prog, self.cols, i) {
            if let Some(j) = self.ef.find(i) {
                let mut d = [0; MAXC];
                self.row(j, &mut d, self.cols);
                Scars::apply(&mut s, &d, self.cols);
            }
            *out = s;
            return;
        }
        match self.ef.find(i) {
            Some(j) => {
                let mut d = [0u64; MAXC];
                self.row(j, &mut d, self.cols);
                for f in 0..self.cols {
                    out[f] = self.prog[f].at(i).wrapping_add(unzz64(d[f]) as u64);
                }
            }
            None => {
                for f in 0..self.cols {
                    out[f] = self.prog[f].at(i);
                }
            }
        }
    }
    /// An event changed ship i (O(1); sealed later, in idle time).
    pub fn update(&mut self, i: u64, s: Ship) {
        self.hot.insert(i as u32, s);
    }
    /// Fold the hot map into the scars.
    pub fn seal(&mut self, enc: &mut Enc) {
        if self.hot.is_empty() {
            return;
        }
        let mut hot: Vec<(u64, Ship)> = self.hot.drain().map(|(i, s)| (i as u64, s)).collect();
        hot.sort_unstable_by_key(|h| h.0);
        let mut scars = Vec::with_capacity(self.ef.k + hot.len());
        let mut q = 0;
        let mut buf = Buf::default();
        let mut cur_block = usize::MAX;
        for (j, o) in self.ef.cursor(0) {
            while q < hot.len() && hot[q].0 < o {
                scars.push(hot[q]);
                q += 1;
            }
            if q < hot.len() && hot[q].0 == o {
                scars.push(hot[q]);
                q += 1;
                continue;
            }
            if j / RB != cur_block {
                cur_block = j / RB;
                let (off, n) = self.rblocks[cur_block];
                decode_block(
                    &self.rows[off as usize..],
                    n as usize,
                    self.cols,
                    &[0; MAXC],
                    &mut buf,
                );
            }
            let mut s = [0u64; MAXC];
            for f in 0..self.cols {
                s[f] = self.prog[f]
                    .at(o)
                    .wrapping_add(unzz64(buf.col[f][j % RB]) as u64);
            }
            scars.push((o, s));
        }
        scars.extend_from_slice(&hot[q..]);
        let cols = self.cols;
        let prog = self.prog;
        scars.retain(|(o, s)| (0..cols).any(|f| s[f] != prog[f].at(*o)));
        *self = Self::seal_from(self.n, cols, prog, &scars, enc);
    }
    /// Stream every ship in ordinal order, `RB` at a time.
    pub fn for_each(&self, buf: &mut Buf, rbuf: &mut Buf, mut f: impl FnMut(u64, &Buf)) {
        let mut cur = self.ef.cursor(0);
        let mut next = cur.next();
        let mut cur_block = usize::MAX;
        let mut s = 0u64;
        while s < self.n {
            let n = (self.n - s).min(RB as u64) as usize;
            buf.n = n;
            for c in 0..self.cols {
                match self.prog[c] {
                    Prog::Belt(b) => {
                        for (i, x) in buf.col[c][..n].iter_mut().enumerate() {
                            *x = b.at(s + i as u64);
                        }
                    }
                    Prog::Const(v) => buf.col[c][..n].fill(v),
                    Prog::Affine { a, b } => {
                        let mut v = Prog::Affine { a, b }.at(s);
                        for x in buf.col[c][..n].iter_mut() {
                            *x = v;
                            v = v.wrapping_add(b as u64);
                        }
                    }
                }
            }
            while let Some((j, o)) = next {
                if o >= s + n as u64 {
                    break;
                }
                if j / RB != cur_block {
                    cur_block = j / RB;
                    let (off, rn) = self.rblocks[cur_block];
                    decode_block(
                        &self.rows[off as usize..],
                        rn as usize,
                        self.cols,
                        &[0; MAXC],
                        rbuf,
                    );
                }
                let i = (o - s) as usize;
                for c in 0..self.cols {
                    buf.col[c][i] = buf.col[c][i].wrapping_add(unzz64(rbuf.col[c][j % RB]) as u64);
                }
                next = cur.next();
            }
            f(s, buf);
            s += n as u64;
        }
    }
    /// How many ships have column 0 (the periapsis time: the arc they occupy) in [lo, hi].
    /// Needs column 0 to be an increasing program. O(log k + scars in the window).
    pub fn count_arc(&self, lo: u64, hi: u64) -> Option<u64> {
        let (a, b) = match self.prog[0] {
            Prog::Affine { a, b } if b > 0 => (a as i128, b as i128),
            _ => return None,
        };
        let n = self.n as i128;
        let clip = |lo: i128, hi: i128| -> (i128, i128) {
            let i0 = (lo - a + b - 1).div_euclid(b).max(0);
            let i1 = (hi - a).div_euclid(b).min(n - 1);
            (i0, i1)
        };
        let (i0, i1) = clip(lo as i128, hi as i128);
        let mut count = (i1 - i0 + 1).max(0);
        let dev = self.maxdev[0] as i128;
        let (j0, j1) = clip(lo as i128 - dev, hi as i128 + dev);
        if j1 >= j0 {
            let r0 = self.ef.rank(j0 as u64);
            let mut d = [0u64; MAXC];
            for (j, o) in self.ef.cursor(r0) {
                if o as i128 > j1 {
                    break;
                }
                self.row(j, &mut d, 1);
                let t = self.prog[0].at(o).wrapping_add(unzz64(d[0]) as u64);
                let in_prog = (o as i128) >= i0 && (o as i128) <= i1;
                let in_act = t >= lo && t <= hi;
                count += in_act as i128 - in_prog as i128;
            }
        }
        Some(count as u64)
    }
    /// A conservative bound on each column over ordinals [i0, i1]: the certificate a
    /// first-possible-contact test starts from, without expanding the population.
    pub fn bounds(&self, i0: u64, i1: u64) -> [(i128, i128); MAXC] {
        let mut out = [(0i128, 0i128); MAXC];
        for f in 0..self.cols {
            if let Prog::Belt(b) = self.prog[f] {
                let (lo, hi) = b.bounds();
                let d = self.maxdev[f] as i128;
                out[f] = (lo - d, hi + d);
                continue;
            }
            let (x, y) = (self.prog[f].at(i0) as i128, self.prog[f].at(i1) as i128);
            let d = self.maxdev[f] as i128;
            out[f] = (x.min(y) - d, x.max(y) + d);
        }
        out
    }
    /// Split at ordinal s into [0, s) and [s, n): the right half's program is shifted, its
    /// scars keep their rows (deltas from the program do not change).
    pub fn split(&self, s: u64, enc: &mut Enc) -> (Program, Program) {
        let mut left = Vec::new();
        let mut right = Vec::new();
        let mut buf = Buf::default();
        let mut cur_block = usize::MAX;
        for (j, o) in self.ef.cursor(0) {
            if j / RB != cur_block {
                cur_block = j / RB;
                let (off, n) = self.rblocks[cur_block];
                decode_block(
                    &self.rows[off as usize..],
                    n as usize,
                    self.cols,
                    &[0; MAXC],
                    &mut buf,
                );
            }
            let mut sh = [0u64; MAXC];
            for f in 0..self.cols {
                sh[f] = self.prog[f]
                    .at(o)
                    .wrapping_add(unzz64(buf.col[f][j % RB]) as u64);
            }
            if o < s {
                left.push((o, sh));
            } else {
                right.push((o - s, sh));
            }
        }
        let mut rp = self.prog;
        for p in rp.iter_mut().take(self.cols) {
            *p = p.shifted(s);
        }
        (
            Self::seal_from(s, self.cols, self.prog, &left, enc),
            Self::seal_from(self.n - s, self.cols, rp, &right, enc),
        )
    }
}
