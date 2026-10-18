Working...
Check complete. `check.md` written to `lab/results/20261018-0932-fermi-cd3b/check.md` — **Grade: silver**.

**What I did:**
- **Reproduced** `regen.sh` in a clean tree (empty patch, no source edits): exit 0, `ledger-out.json` identical field-for-field. Anchor 14,071 to the digit.
- **Verified the model's base**: all geometry constants match `scenario.rs` (AU, belt a∈[2,3), Rayleigh 0.07/redraw 0.4, ship radius 34·2⁻¹⁰ ru, Moon 1,176 ru); all 18 cited lever constants located in the wiki at their stated grades (29.3 µs/1051, split 8/7f97-de7b, 274/712/1a46, 16ec-49e9 fast path 4.4–5.6→0.21–0.27 µs, 16.4 µs mint, 277d 0.6 µs, efd4 intern gold, ec74, 09a1, 1b1f, 2b89, 3294, 4e2d, 8ffc, e7ef, fe6b).
- **Pre-registration confirmed** by mtime: predictions 09:40:53 < outputs 09:44:30. P1/P2/P4/P6 held, P3's mint term failed exactly as disclosed, P5 never fired.
- **Attacked**: N=10⁵ (p50 14,072, +0.007%), seed 2 via temporary example edit, restored (tree clean), N=3×10⁵ — 30× beyond the author's anchor (14,072, 692 MB) — and an adversarial-constant envelope (geometric annulus, epicyclic-only v_rel): contacts stay 0.16–0.47/game-s, mint worst case 1.4–4.0 cores, so the churn-not-flow decomposition survives its own ±.
- **Corrected the author's page in place** on two overstatements: ec74 is silver (not gold), and "10¹-scale occupancy" → "10⁹-scale (cells of 10²–10⁴)". One intermediate edit of mine mangled the cross-check sentence; re-read and rebuilt it correctly.

**Why silver, not gold:** the flow Fermi, the subtraction decomposition, and the composition update (S* 20.7 → 2.1 via the 16ec/49e9 fast path) are new and solid, but no new measurement flew beyond an anchor already known to the digit (8ffc/3294, re-flown by 4e2d) — and the decisive constant, churn per kick at 10⁹-scale occupancy, is precisely what the run leaves unmeasured. The one experiment to gold is the run's own open direction: a mint-counter flight plus fe6b's pairs/kick measured at cell occupancies 10²–10⁴ on the live anchor.
