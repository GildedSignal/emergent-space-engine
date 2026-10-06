# Probe C: Mitchell log2 + 16-entry correction table, for the view's colour path.
# Predictions 8 and 9 of predictions.md. Run: python3 probe_c.py
import math, random
random.seed(42)

TABLE = [math.log2(1.0 + i / 16.0) for i in range(17)]
ET = [2.0 ** (i / 16.0) for i in range(17)]

def mitchell(m):  # m in [1,2)
    return m - 1.0

def log2_mitchell(x):
    e = math.frexp(x)[1] - 1
    return e + mitchell(x / (2.0 ** e))

def log2_corr(x):
    e = math.frexp(x)[1] - 1
    t = (x / (2.0 ** e) - 1.0) * 16.0
    i = min(int(t), 15)
    return e + TABLE[i] + (t - i) * (TABLE[i + 1] - TABLE[i])

def antilog2(L):
    e = math.floor(L)
    t = (L - e) * 16.0
    i = min(int(t), 15)
    return (ET[i] + (t - i) * (ET[i + 1] - ET[i])) * (2.0 ** e)

maxerr_plain = maxerr_corr = 0.0
for _ in range(200000):
    x = random.uniform(1e-6, 1e6)
    maxerr_plain = max(maxerr_plain, abs(log2_mitchell(x) - math.log2(x)))
    maxerr_corr = max(maxerr_corr, abs(log2_corr(x) - math.log2(x)))
print(f"Mitchell plain:      max |err| on log2 = {maxerr_plain:.6f}  (prediction: 0.03-0.09)")
print(f"16-entry corrected:  max |err| on log2 = {maxerr_corr:.3e}  (prediction: <= 2^-11 = 4.9e-4)")

maxrel = 0.0
for _ in range(200000):
    x = random.uniform(0.5, 2.0); y = random.uniform(0.5, 2.0)
    maxrel = max(maxrel, abs(antilog2(log2_corr(x) + log2_corr(y)) / (x * y) - 1.0))
print(f"product via log-add + 16-entry antilog table: max rel err = {maxrel:.3e}  (prediction: <= 0.5%)")

mc = 0.0
for _ in range(200000):
    ks = [random.uniform(0.8, 1.25) for _ in range(4)]
    ex = 1.0
    for k in ks: ex *= k
    mc = max(mc, abs(antilog2(sum(log2_corr(k) for k in ks)) / ex - 1.0))
print(f"4-factor chain (beaming k^4 scale):           max rel err = {mc:.3e}")
