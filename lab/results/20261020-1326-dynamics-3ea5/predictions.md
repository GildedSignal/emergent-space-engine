# Predictions — 20261020-1326-dynamics-3ea5 (written before the decisive flights)

Question: the collapsed core's attractor on the shipped wiring (c644's named leftover #3;
19b9 took only N(t): 308→273 at 49→98k, rate ~4700/ch). The sub-quantum droplet
(~108 bodies below r = 0.5q at 49k, c644) was never itself measured.

Fermi first: bodies have radius 1q; any two bodies within r<0.5q of the center overlap
always, so the droplet bills ~C(n_sub,2) contacts/chronon. At n_sub≈105 that is ~5.5k
pairs — the measured ~4.7k/ch total rate is already ≈ the droplet's pair count. If the
droplet holds while N falls, the bill stays ~flat (n² law); if the droplet drains, the
bill falls quadratically. Hazard: 7.4e-6/ch/body (32-49k, c644) fell to 2.5e-6 (49-98k,
19b9) — evaporation slows as the bound binding deepens; from N≈273, λ·T·N with
λ≈2e-6, T=49k predicts ~25 more deaths by 147k (N≈250).

Arms (deterministic lineage: genesis/tide = e3b7/c644 verbatim; digest checkpoints at
t=49152 and 98304 must reproduce c644/19b9's counters):
- MAIN cold s1, H=147456 (B lineage extended 1.5× past 19b9).
- CTRL Pass s1, H=147456 (same genesis, Response::Pass).
- SEED thermal s2, H=98304 (C lineage doubled).

P1 (the droplet is the bill): per-stride total contacts ≈ f·C(n_sub,2) per chronon with
f ∈ [0.4, 1.3], and the zone-members' share (r<2.1q) of member-contact-increments ≥ 60%
through the tail. KILL/INVERT: f drifts >3× across 49k→147k, or the sub-2.1q share
< 50% (the bill lives outside the core).

P2 (quench, no grinder): windowed per-body death hazard over 98-147k λ ∈ [0.3, 3.0]e-6/ch
— no re-acceleration past 19b9's 2.5e-6. Point prediction N(147456) ∈ [230, 270].
KILL (the interesting inversion): λ(98-147k) > 5e-6 — the core re-arms the clamp pump
and grinds.

P3 (the droplet holds): n_sub(t) stays in [60, 175] over 98-147k with |trend| < 25 per
49k (no total absorption, no dissolution). Sub-case: if n_sub decays < 60 by 147k the
endgame is evaporation-dominant; if it grows > 175 the droplet is absorbing the skirt.

P4 (death channel unchanged): among deaths at t ≥ 98304, ≥ 70% never clamped
(relaxation-born), and ≤ 30% were sub-resident (r<0.5q) within 512 ch of death
(droplet ejections stay a minority channel).

P5 (control): Pass arm flat: n_sub = 0 at every stride, deaths 0, contacts/ch < 150 at
every stride past t=4096.

Instrument smoke: one H=2048 MAIN-format run before the flights (format check only,
disclosed here); its numbers are used for nothing else.
