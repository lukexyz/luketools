# Why the Harness Matters More Than the Model

> **Source status — read this first.**
> Video `n9xKblqyQ28` could not be retrieved. `yt-dlp` was installed and run; the session's
> egress proxy returns `403 Forbidden` on `CONNECT youtube.com:443`, and every mirror/transcript
> proxy probed was unreachable. **No transcript exists in this document.** The model below is
> synthesised from the published thesis and its benchmarks, not from the video's audio.
> To get the real transcript, run locally:
>
> ```bash
> yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" --sub-format vtt \
>        "https://www.youtube.com/watch?v=n9xKblqyQ28"
> ```

---

## The Claim

<pre>
  <b><span style="color:#a855f7">The model is the engine. The harness is the vehicle.</span></b>
  You do not win a race by swapping engines while the chassis is made of cardboard.
</pre>

---

## Flow: What Actually Determines the Outcome

<pre>
                          ┌───────────────────────────┐
                          │      TASK  /  INTENT      │
                          └─────────────┬─────────────┘
                                        │
    ╔═══════════════════════════════════▼═══════════════════════════════════╗
    ║                                                                       ║
    ║      <b><span style="color:#a855f7">T  H  E     H  A  R  N  E  S  S</span></b>        <span style="color:#a855f7">◄── the leverage</span>          ║
    ║                                                                       ║
    ║   ┌────────────┬────────────┬────────────┬────────────┬───────────┐   ║
    ║   │  CONTEXT   │   TOOLS    │  SANDBOX   │   MEMORY   │ SUBAGENTS │   ║
    ║   │ prompts,   │  scoped,   │ perms,     │ state that │ decompose │   ║
    ║   │ CLAUDE.md  │  typed     │ blast rad. │ outlives   │ + delegate│   ║
    ║   └─────┬──────┴─────┬──────┴─────┬──────┴─────┬──────┴─────┬─────┘   ║
    ║         └────────────┴──────┬─────┴────────────┴────────────┘         ║
    ║                             │                                         ║
    ║                     ┌───────▼────────┐                                ║
    ║                     │   <b>AGENT LOOP</b>   │◄────────────────┐              ║
    ║                     └───────┬────────┘                 │              ║
    ╚═════════════════════════════│═════════════════════════│═══════════════╝
                                  │                         │
                                  ▼                         │
                        ┌───────────────────┐               │
                        │       MODEL       │               │  <span style="color:#a855f7">feedback</span>
                        │  <i>commodity tier</i>  │               │   <span style="color:#a855f7">is the</span>
                        │  <i>swappable, churns</i>│               │  <span style="color:#a855f7">whole game</span>
                        └─────────┬─────────┘               │
                                  ▼                         │
                        ┌───────────────────┐   fail        │
                        │     VALIDATOR     ├───────────────┘
                        │ tests·lint·types  │
                        └─────────┬─────────┘
                                  │ pass
                                  ▼
                        ┌───────────────────┐
                        │      OUTCOME      │
                        └───────────────────┘
</pre>

---

## Leverage Ranking

<pre>
  RANK   LEVER                        MARGINAL RETURN
  ────   ──────────────────────────   ────────────────────────────────────────────
   <b><span style="color:#a855f7">01</span></b>    <b><span style="color:#a855f7">Feedback loop quality</span></b>        <span style="color:#a855f7">████████████████████</span>  a model that cannot
                                                        see its own failure cannot fix it
   <b><span style="color:#a855f7">02</span></b>    <b><span style="color:#a855f7">Context curation</span></b>             <span style="color:#a855f7">██████████████████</span>    signal density > token count
   <b><span style="color:#a855f7">03</span></b>    <b><span style="color:#a855f7">Tool design &amp; scoping</span></b>        <span style="color:#a855f7">████████████████</span>      narrow typed tools beat
                                                        one omnipotent shell
   04    Sandbox / permissions        ████████████        bounds the blast radius,
                                                        unlocks autonomy
   05    Sub-agent decomposition      ██████████          context isolation, parallelism
   06    <i>Model version</i>                ██████              <i>real, but the smallest knob</i>
</pre>

---

## The Two Load-Bearing Numbers

<pre>
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  HarnessBench — 106 coding tasks, <b>weights held constant</b>                  │
  │  harness swap alone  ──►  <b><span style="color:#a855f7">&gt; 20 percentage-point spread</span></b>                   │
  ├──────────────────────────────────────────────────────────────────────────┤
  │  ARC-AGI — identical model weights                                       │
  │  weak harness  30%   ──────────────────────►   <b><span style="color:#a855f7">95%</span></b>  strong harness       │
  └──────────────────────────────────────────────────────────────────────────┘
</pre>

---

## Why It Compounds: Asymmetric Half-Lives

<pre>
   MODEL     ├──┤├──┤├──┤├──┤├──┤├──┤├──┤├──┤     obsolete every few months
             <i>you rent it</i>

   <b><span style="color:#a855f7">HARNESS</span></b>   <b><span style="color:#a855f7">├──────────────────────────────────────┤</span></b>     <b><span style="color:#a855f7">carries forward intact</span></b>
             <b><span style="color:#a855f7">you own it — and it compounds</span></b>
                                                  <span style="color:#a855f7">▲</span>
                    a stronger model ships ───────<span style="color:#a855f7">┘</span> your context files,
                                                    tool list and guardrails
                                                    <b><span style="color:#a855f7">transfer unchanged</span></b>
</pre>

---

## Corollaries

<pre>
  →  <b><span style="color:#a855f7">Harness investment is the only durable investment.</span></b> Model spend depreciates on a
     one-quarter schedule; harness spend does not.

  →  <b><span style="color:#a855f7">A strong harness lifts a weak model past a weak harness on a strong model.</span></b>
     This is the democratisation argument: local open-weights become viable.

  →  <b>Benchmark the harness, not the model.</b> A leaderboard score without a stated harness
     is an unfalsifiable number.

  →  <b>"Just use the better model" is the expensive way to avoid engineering.</b>
</pre>

---

## Legend

<pre>
  <b><span style="color:#a855f7">purple</span></b>  = load-bearing claim / critical path
  ╔═══╗   = the layer under your control
  ┌───┐   = commodity or derived
</pre>

<sub>Rendering note: purple emphasis uses inline HTML, which renders in VS Code preview, Obsidian
and most local viewers. GitHub sanitises inline styles — the ASCII structure degrades gracefully
to plain monospace there. The companion <code>harness-vs-model.html</code> is the full-fidelity version.</sub>
