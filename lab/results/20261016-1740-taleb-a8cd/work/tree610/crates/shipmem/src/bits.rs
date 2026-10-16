//! Varints, zigzag and LSB-first bit packing. Readers load unaligned words, so every buffer
//! that is decoded keeps `PAD` zero bytes after its last payload.
pub const PAD: usize = 16;

#[inline]
pub fn zz(x: i128) -> u128 {
    ((x << 1) ^ (x >> 127)) as u128
}
#[inline]
pub fn unzz(u: u128) -> i128 {
    ((u >> 1) as i128) ^ -((u & 1) as i128)
}
#[inline]
pub fn zz64(x: i64) -> u64 {
    ((x << 1) ^ (x >> 63)) as u64
}
#[inline]
pub fn unzz64(u: u64) -> i64 {
    ((u >> 1) as i64) ^ -((u & 1) as i64)
}

pub fn put_uv(out: &mut Vec<u8>, mut x: u128) {
    loop {
        let b = (x & 0x7f) as u8;
        x >>= 7;
        if x == 0 {
            out.push(b);
            return;
        }
        out.push(b | 0x80);
    }
}
#[inline]
pub fn get_uv(b: &[u8], p: &mut usize) -> u128 {
    let mut x = 0u128;
    let mut s = 0;
    loop {
        let c = b[*p];
        *p += 1;
        x |= ((c & 0x7f) as u128) << s;
        if c < 0x80 {
            return x;
        }
        s += 7;
    }
}
#[inline]
pub fn get_zz(b: &[u8], p: &mut usize) -> i128 {
    unzz(get_uv(b, p))
}
#[inline]
pub fn bitlen(x: u64) -> u32 {
    64 - x.leading_zeros()
}
#[inline]
pub fn bitlen128(x: u128) -> u32 {
    128 - x.leading_zeros()
}
#[inline]
pub fn mask(w: u32) -> u64 {
    if w >= 64 {
        u64::MAX
    } else {
        (1u64 << w) - 1
    }
}
#[inline]
pub fn packed_bytes(n: usize, w: u32) -> usize {
    (n * w as usize).div_ceil(8)
}

/// Low `w` bits of each value, LSB first, `packed_bytes(n, w)` bytes.
pub fn pack(e: &[u64], w: u32, out: &mut Vec<u8>) {
    if w == 0 {
        return;
    }
    let m = mask(w);
    let mut acc: u128 = 0;
    let mut nb = 0u32;
    for &x in e {
        acc |= ((x & m) as u128) << nb;
        nb += w;
        while nb >= 8 {
            out.push(acc as u8);
            acc >>= 8;
            nb -= 8;
        }
    }
    if nb > 0 {
        out.push(acc as u8);
    }
}

/// Value `j` of a packed array of width `w` at `p`. Safety: `p` plus the payload plus `PAD`
/// bytes must be readable.
#[inline(always)]
pub unsafe fn rd(p: *const u8, j: usize, w: u32) -> u64 {
    let bit = j * w as usize;
    let q = p.add(bit >> 3);
    let s = (bit & 7) as u32;
    if w <= 56 {
        (u64::from_le((q as *const u64).read_unaligned()) >> s) & mask(w)
    } else {
        ((u128::from_le((q as *const u128).read_unaligned()) >> s) as u64) & mask(w)
    }
}

/// Unpack `n` values. Safety as for [`rd`].
#[inline]
pub unsafe fn unpack(p: *const u8, n: usize, w: u32, out: &mut [u64]) {
    let out = &mut out[..n];
    if w == 0 {
        out.fill(0);
    } else if w <= 56 {
        let m = mask(w);
        let wz = w as usize;
        for (j, o) in out.iter_mut().enumerate() {
            let bit = j * wz;
            *o = (u64::from_le((p.add(bit >> 3) as *const u64).read_unaligned()) >> (bit & 7)) & m;
        }
    } else {
        for (j, o) in out.iter_mut().enumerate() {
            *o = rd(p, j, w);
        }
    }
}
