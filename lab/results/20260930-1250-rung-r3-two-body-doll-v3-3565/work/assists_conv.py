"""Half-step rerun agreement for the assist references (reference_converged)."""
import json
import math

from common import R_PLANET_AU, sample_cases
from assists import run_ref_flyby
from nbary import helio_state


def main():
    _, b_rplanet = sample_cases()
    worst = 0.0
    for br in b_rplanet:
        b = br * R_PLANET_AU
        _, _, y1 = run_ref_flyby(b, h_bg=2e-3, c_enc=250.0)
        _, _, y2 = run_ref_flyby(b, h_bg=1e-3, c_enc=354.0)
        (r1x, r1y), _ = helio_state(y1)
        (r2x, r2y), _ = helio_state(y2)
        worst = max(worst, math.hypot(r1x - r2x, r1y - r2y) / math.hypot(r1x, r1y))
    print(f"worst rel = {worst:.3e}")
    json.dump({"worst_rel": worst}, open("assists_conv.json", "w"))


if __name__ == "__main__":
    main()
