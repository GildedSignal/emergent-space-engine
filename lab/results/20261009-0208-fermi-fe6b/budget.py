#!/usr/bin/env python3
"""The 10^9 steady-state budget on one 8 GB M1, generator-native.

Every constant carries its source. Fresh measurements (this Linux runner, orders of
magnitude only; the integrator re-measures on the M1):
  [F1] emergent-universe example `cost` (shipped code, release): compile 3.4 us,
       state 2.8 us, cartesian 0.3 us, from_state 11.1 us.
  [F2] reabsorb.py: re-band 5.7e6-7.0e6 bodies/s/core (numpy stable argsort lower
       bound; a Rust radix sort is ~10x this).
Stored evidence (M1):
  [S1] artifacts/evidence/opus-encounters-20260930/kick.jsonl: n=1e4, rho=1e-4:
       pairs_per_kick 812.8, us_per_kick 4345.4 => 5.35 us/pair; slack_skippable
       0.9458 (eps 1e-9).
  [S2] same, steady.jsonl: n=3000, rho=1e-4: hits_per_body_orbit 0.00586;
       scale.jsonl (n*rho=1 sweep): enc_per_body_orbit ~0.04 at all n.
  [S3] docs/representation.md:68 / board H0190: kicks 32/orbit, 0.28 orbit-averaged.
  [S4] gold components-98bc: smooth belt program 0.126 bit/body.
  [S5] representation.md:90: floor 12-16 B per individual in a doll; Body today 88 B.
  [S6] representation.md:114: design's own kick row "~50 ns each, <1% of a core";
       re-anchor memo 0.05 compiles/kick (docs/law.md:35).
Spec (public, M1 MacBook Air): 4P+4E cores ~1e10 simple ops/s CPU, ~60-68 GB/s
unified memory [X1]. Board claim checked: "10^9 orbiting bodies at today's rates
would need about 190 cores" [B1].
"""
import json

N = 1e9          # bodies
P = 1.26e8       # s per orbit (4 yr, AU-scale belt) [game-seconds]
RTF = 100        # the plane's flying speed [B1/HANDOFF]
SKIN = 12.6      # slack-skin factor, board-adopted [B1 taste log 6 Oct]
K_AVG = 0.28     # orbit-averaged kicks per body per orbit [S3]
K_FULL = 32.0    # unaveraged [S3]
PAIRS_PER_KICK = 812.8   # at fixed belt density, n=1e4 [S1]
US_PER_PAIR = 5.35       # [S1]
COMPILE_US = 3.4         # [F1]
KICK_ARITH_S = 50e-9 + 0.05 * COMPILE_US * 1e-6  # 50 ns + 0.05 compiles [S6]
ENC_PER_BODY_ORBIT = 0.00586  # close-conjunction "hits" [S2]
ENC_US = 1.0              # one exact per-pair conjunction evaluation, order [S1 qsteps]
REABSORB_PER_S_CORE = 5.7e6   # [F2] lower bound
SCAR_BYTES = 24           # 16 B individual floor + id/metadata, order [S5]
KEY_BYTES = 12            # 8 B far-time + 4 B id [law.md:12 tube view]


def cores_per_term(kicks_per_s, cost_per_kick):
    return kicks_per_s * cost_per_kick  # s of work per real second == cores


rows = []
r = rows.append

# --- event rates (per real second at RTF) -----------------------------------
kicks_s = N * K_AVG / P * RTF       # 222/s
kicks_s_full = N * K_FULL / P * RTF
enc_s = N * ENC_PER_BODY_ORBIT / P * RTF

# --- the cascade term, three certificate regimes ----------------------------
casc_pair_cert = PAIRS_PER_KICK * US_PER_PAIR * 1e-6            # fixed-density tier, no skin
casc_skin = casc_pair_cert / SKIN                                # + slack skin
casc_phase = 4 * US_PER_PAIR * 1e-6                              # phase-neighbour rank-4 (taleb-09b5)

r(("kick arithmetic (incremental + 0.05 compiles/kick)", kicks_s, KICK_ARITH_S,
   f"{cores_per_term(kicks_s, KICK_ARITH_S):.2e}"))
r(("certificate cascade: two-tier, no skin", kicks_s, casc_pair_cert,
   f"{cores_per_term(kicks_s, casc_pair_cert):.2e}"))
r(("certificate cascade: two-tier + slack skin", kicks_s, casc_skin,
   f"{cores_per_term(kicks_s, casc_skin):.2e}"))
r(("certificate cascade: phase-neighbour rank-4", kicks_s, casc_phase,
   f"{cores_per_term(kicks_s, casc_phase):.2e}"))
r(("certificate cascade: fixed-extent belt, two-tier (pairs ∝ N, no cert fix)", kicks_s,
   PAIRS_PER_KICK * (N / 1e4) * US_PER_PAIR * 1e-6,
   f"{cores_per_term(kicks_s, PAIRS_PER_KICK * (N / 1e4) * US_PER_PAIR * 1e-6):.1e}"))
r(("certificate cascade: two-tier + skin, UNAVERAGED k=32", kicks_s_full, casc_skin,
   f"{cores_per_term(kicks_s_full, casc_skin):.2e}"))
r(("certificate cascade: two-tier, no skin, UNAVERAGED k=32", kicks_s_full, casc_pair_cert,
   f"{cores_per_term(kicks_s_full, casc_pair_cert):.2e}"))
r(("encounter handling (0.00586/body/orbit)", enc_s, ENC_US * 1e-6,
   f"{cores_per_term(enc_s, ENC_US * 1e-6):.2e}"))

# --- memory ------------------------------------------------------------------
prog_mb = N * 0.126 / 8 / 1e6
for f in (0.01, 0.1, 0.33):
    r((f"scars at live fraction {f:.0%} (24 B each)", None, None,
       f"{f * N * SCAR_BYTES / 1e9:.2f} GB"))
r(("per-body event keys (12 B x 1e9)", None, None, f"{N * KEY_BYTES / 1e9:.1f} GB  (> 8 GB)"))
r(("program-level keys (1 per 128-body block)", None, None,
   f"{N / 128 * KEY_BYTES / 1e6:.0f} MB"))

# --- H_live steady state ------------------------------------------------------
creation_s = kicks_s            # worst case: every averaged kick touches a scar
steady_live = creation_s * 1e5   # 1e5 s residence (a full session) -> live bodies
r(("scar creation (=kick rate) vs reabsorption", creation_s, None,
   f"{creation_s:.0f}/s vs {REABSORB_PER_S_CORE:.1e}/s per core ({REABSORB_PER_S_CORE/creation_s:.0e}x slack)"))
r(("live bodies at 1e5 s residence", steady_live, None,
   f"{steady_live:.1e} = {steady_live*SCAR_BYTES/1e9:.2f} GB"))

# --- rtf ceilings (4 P-cores as 4 s/s of compute) -----------------------------
for name, k, cost in (("averaged + skin", K_AVG, casc_skin),
                      ("averaged, no skin", K_AVG, casc_pair_cert),
                      ("unaveraged + skin", K_FULL, casc_skin),
                      ("unaveraged, no skin", K_FULL, casc_pair_cert),
                      ("averaged + phase-neighbour", K_AVG, casc_phase)):
    per_rtf = N * k / P * cost
    r((f"max rtf on 4 cores: {name}", None, None, f"{4/per_rtf:,.0f}"))

# --- claim checks --------------------------------------------------------------
board_190 = N * K_FULL / P * RTF * casc_pair_cert
r(("re-derivation of board's '190 cores' (k=32, no skin, rtf 100, fixed density)",
   None, None, f"{board_190:.0f} cores"))
board_190_p1yr = N * K_FULL / 3.15e7 * RTF * casc_pair_cert
r(("same at P=1 yr", None, None, f"{board_190_p1yr:.0f} cores"))

print("| Term | s/s (cores) or size |")
print("|---|---|")
for name, rate, cost, val in rows:
    print(f"| {name} | {val} |")
json.dump({"rows": [dict(name=n, val=v) for n, _, _, v in rows],
           "constants": dict(N=N, P=P, RTF=RTF, SKIN=SKIN, K_AVG=K_AVG, K_FULL=K_FULL,
                             PAIRS_PER_KICK=PAIRS_PER_KICK, US_PER_PAIR=US_PER_PAIR,
                             COMPILE_US=COMPILE_US, ENC_PER_BODY_ORBIT=ENC_PER_BODY_ORBIT,
                             SCAR_BYTES=SCAR_BYTES, KEY_BYTES=KEY_BYTES)},
          open("budget.json", "w"), indent=1)
