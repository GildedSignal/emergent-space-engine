# predictions — 20261017-2142-taleb-8fb9 (written before any engine flight)

Question: does a period/phase-quantized belt — the compact store's own form (shared (anchor, full)
= shared fire ticks; calendar topic, open direction 4) — re-create a standing comb on the shipped
chained clock, or does the per-fire step drift shear it apart (the unmeasured "train lifetime vs
step spread" rule this page's checker named the next run)?

Instrument: `belt_comb` (new example), flying `scenario::plane_extra` with the belt draw quantized
by ES_BELT_A_SHIFT (period classes) / ES_BELT_PHASE_SHIFT (phase classes), advanced one rtf-100
frame at a time with Budget::unlimited (true dues, never deferred), events per frame recorded.
Windows of 6e9 ticks ≈ one belt fire each. N = 50,000 (belt 49,700). Arms (seed 1 unless said):

- CTRL   s=0  p=0  (shipped draw bit for bit; negative control)
- PER    s=27 p=0  (~193 period classes, continuous phases)
- PHASE  s=0  p=8  (256 phase classes, continuous periods)
- BOTH   s=28 p=3  (~48 period x 8 phase = ~384 combos, battalion ~129)
- BOTH6  s=29 p=1  (~24 x 2 = ~48 combos, battalion ~1,036; positive control)
- seed 7 held-out: CTRL and BOTH

Predictions (none of these arms has been run):

P1 CTRL reproduces the quant run's census shape: window 0 (genesis train) ev_max >= 5x the
   steady mean; windows 2-4 settle to ev_mean ~ 6-9/frame (2 events/body/fire over ~17.7k frames)
   with ev_max <= 120.
P2 PER: no battalions are possible (phases continuous within a class). Every window within ~1.5x
   of CTRL's same window. Genesis concentration may fall below CTRL (the a-phase product
   correlation weakens); never above 2x.
P3 PHASE: window 0 shows rails (ev_max >= 2x CTRL's w0), decaying toward CTRL's steady state by
   window 3-4 (periods continuous shear the shared anchors at the shipped ~2.6e-4/fire).
P4 BOTH: the decisive arm. If within-combo step drift <= ~1e-5 relative/fire, windows 1-4 keep
   ev_max >= 65 (half the ~129 battalion; a STANDING comb >= 5x CTRL steady). If the shipped
   ~2.6e-4/fire drift decorrelates combos within ~3 fires, windows 2-4 fall to <= 3x CTRL steady.
P5 BOTH6: window 0 ev_max >= 300 (positive control; else the instrument is VOID). If the comb
   stands, steady ev_max ~ 700-1,100 (~100x CTRL) and its worst frame's wall ms >= 15 ms at
   ~25 us/event — the 12 ms letter broken by 6 schedule bits at N=5e4.
P6 seed 7 (CTRL, BOTH): same structure, ev_max within x0.5-2 of seed 1 (multinomial noise).
P7 total events per window are ~equal across all arms (~2/belt body/window): quantization moves
   WHERE dues land, not HOW MANY (no law change in count; any arm deviating > 20% in total events
   flags a law interaction, not a schedule effect).

Kill criterion (pre-written): BOTH arms' windows 2-4 ev_max <= 3x CTRL's => the standing-comb
premise is dead; the compact store is innocent on the schedule axis (self-shearing), and calendar
od 4 closes. BOTH steady ev_max >= 5x CTRL and within ~2x of N/combos => the comb stands and the
fence is schedule bits >= log2(N x us-per-event / 12 ms).
