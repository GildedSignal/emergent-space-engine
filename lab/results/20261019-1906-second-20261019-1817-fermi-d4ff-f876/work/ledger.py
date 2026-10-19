#!/usr/bin/env python3
"""Fold the measured conjunction law into the 1e9 ledger rows.

Adopted constant: Gamma_flat, the exact-propagation (brute) pair-event rate per
root of reach, measured FLAT at d = 1e4..1e5 (four independent configs, 1182
events). Kinetic theory: the flux regime is flat in d, and no physics scale
exists between 68 root and 1e4 root (ship size 0.033 root is far below), so
the flat law is evaluated at the encounter (68 root) and contact (0.0664 root)
reaches. The MC full/safe values at those reaches are reported as upper
bookends only (their straight-line slow tail grows spurious as d falls).
"""
import json
import math
import numpy as np
import beltlib as bl

def main():
    brute = json.load(open("brute_ladder.json"))
    mc = json.load(open("mc_prod.json"))
    gvals = [b["gamma_per_root_per_game_s_at_1e9"] for b in brute]
    G = float(np.mean(gvals))
    Gspread = float(np.std(gvals, ddof=1)) if len(gvals) > 1 else 0.0
    Gsyst = 0.10 * G                      # sampling cap bias + flatness extrapolation
    mcrow = {r["d_root"]: r for r in mc["ladder"]}

    d_enc, d_con = bl.D_ENC, bl.D_CONTACT
    tp_bar = G * d_enc
    contacts = G * d_con
    per_body_contact = 2 * contacts / bl.N9
    per_body_enc = 2 * tp_bar / bl.N9
    item_m1 = bl.ITEM_US_X86 * bl.X86_TO_M1
    cores_today = contacts * bl.RTF * 2 * item_m1 * 1e-6
    cores_floor = contacts * bl.RTF * 2 * 6e-6
    wake_N = bl.N9 * math.sqrt(1.0 / 3600.0 / contacts)
    C_contact = bl.LAMBDA / per_body_contact
    C_belttemp = bl.LAMBDA / per_body_enc
    # belt density from the occupied annulus (author's def, sanity 29,000 km spacing)
    ro = json.load(open("kinetic.json"))
    A = math.pi * ((ro["occupied_r_AU"][1] * bl.AU) ** 2 - (ro["occupied_r_AU"][0] * bl.AU) ** 2)
    n_belt = bl.N9 / A
    F = 1e6
    side_km = math.sqrt(F / (C_contact * n_belt)) * bl.ROOT_KM
    out = {
        "adopted_gamma_per_root_per_game_s": G,
        "gamma_brute_values": gvals,
        "gamma_stat_sys_band": [G - Gspread - Gsyst, G + Gspread + Gsyst],
        "mc_bookends_at_68": {"full": mcrow[d_enc]["gamma_per_root_per_game_s"],
                              "shearsafe_gt10": mcrow[d_enc]["gamma_shearsafe_gt10"]},
        "mc_contacts_count_at_contact_reach": mcrow[d_con]["pair_events_per_game_s"],
        "tp_bar_events_per_game_s_100km": tp_bar,
        "contacts_per_game_s_1e9": contacts,
        "stream_row_addition_cores_today": cores_today,
        "stream_row_addition_cores_6us_floor": cores_floor,
        "contact_wakeup_N_per_game_hour": wake_N,
        "C_contact_equals_own_clock": C_contact,
        "C_belttemp_encounter_critical": C_belttemp,
        "fleet1e6_side_km_at_C_contact": side_km,
        "mean_spacing_km": math.sqrt(1 / n_belt) * bl.ROOT_KM,
        "filling_factor": n_belt * math.pi * (bl.R_S ** 2),
        "comparison": {
            "author_d4ff": {"gamma": 84.09, "tp": 5.7e3, "contacts": 5.58,
                            "cores": 0.054, "wake": 7.05e6, "C_contact": 3179, "C_temp": 3.1},
            "checker_correction": {"gamma": 4.9, "tp": 3.3e2, "contacts": 0.33,
                                   "cores": 0.006, "wake": 3e7, "C_contact": 5e4, "C_temp": 50},
            "this_run": {"gamma": G, "tp": tp_bar, "contacts": contacts,
                         "cores": cores_today, "wake": wake_N,
                         "C_contact": C_contact, "C_temp": C_belttemp}},
        "selectivity_note": {
            "pairs_at_1e9": bl.N9 * (bl.N9 - 1) / 2,
            "tp_selectivity": tp_bar / (bl.N9 * (bl.N9 - 1) / 2)},
    }
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
