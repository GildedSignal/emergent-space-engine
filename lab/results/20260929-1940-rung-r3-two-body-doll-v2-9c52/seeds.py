import random, math
rng = random.Random(20261002)
with open("seeds.txt", "w") as f:
    for i in range(1024):
        p = math.exp(rng.uniform(math.log(20.0), math.log(1000.0)))
        e = rng.uniform(0.0, 0.6)
        nu = rng.uniform(0.01, 0.25)
        f.write("%.17g %.17g %.17g\n" % (p, e, nu))
with open("flybys.txt", "w") as f:
    for i in range(64):
        b = math.exp(rng.uniform(math.log(1.5), math.log(50.0)))
        f.write("%.17g\n" % b)
