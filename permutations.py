# /// script
# requires-python = ">=3.10"
# dependencies = ["marimo", "anywidget", "traitlets"]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="medium",
    layout_file="layouts/permutations.slides.json",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import random
    from collections import Counter
    from functools import reduce
    from math import cos, factorial, lcm, log10, pi, sin

    import anywidget
    import traitlets

    return (
        Counter,
        anywidget,
        cos,
        factorial,
        lcm,
        log10,
        mo,
        pi,
        random,
        reduce,
        sin,
        traitlets,
    )


@app.cell(hide_code=True)
def _(mo):
    _SERIES = {
        "light": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"],
        "dark": ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"],
    }
    # sequential blue, steps 100..700
    _BLUE = [
        "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
        "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
    ]
    _RAMP_LIGHT = _BLUE[3:]  # 250..700: lightest step still clears 2:1 on light
    _RAMP_DARK = _BLUE[10::-1]  # 600..100: anchor flips on dark

    def _rgb(h):
        return [int(h[i : i + 2], 16) for i in (1, 3, 5)]

    def _lerp(stops, t):
        x = t * (len(stops) - 1)
        i = min(int(x), len(stops) - 2)
        a, b = _rgb(stops[i]), _rgb(stops[i + 1])
        return "#" + "".join(f"{round(p + (q - p) * (x - i)):02x}" for p, q in zip(a, b))

    def _ink(h):
        def lin(v):
            v /= 255
            return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

        r, g, b = map(lin, _rgb(h))
        return "#ffffff" if 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.3 else "#0b0b0b"

    def _vars(mode):
        return ";".join(f"--s{i}:{c}" for i, c in enumerate(_SERIES[mode]))

    _DARK_VARS = f"--t1:#f0efec;--t2:#c3c2b7;--grid:#383835;--track:#2a2a28;--surface:#1a1a19;{_vars('dark')}"
    _DARK = '.dark .viz,[data-theme="dark"] .viz'
    _CSS = f"""
    .viz{{--t1:#0b0b0b;--t2:#52514e;--grid:#e4e3df;--track:#efeeea;--surface:#fcfcfb;{_vars('light')};
      color:var(--t1);font:13px/1.45 ui-sans-serif,system-ui,sans-serif}}
    {_DARK}{{{_DARK_VARS}}}
    .viz svg text{{fill:var(--t1)}}
    .viz svg .t2{{fill:var(--t2)}}
    .viz .muted{{color:var(--t2)}}
    .viz .tile{{width:16px;height:16px;border-radius:3px;font:600 10px/16px ui-monospace,monospace;
      text-align:center;background:var(--bl);color:var(--il)}}
    .dark .viz .tile,[data-theme="dark"] .viz .tile{{background:var(--bd);color:var(--id)}}
    .viz .now{{box-shadow:0 0 0 2px var(--t1)}}
    .viz .tile.lg{{width:30px;height:30px;font-size:15px;line-height:30px;border-radius:5px}}
    .viz .grid{{display:grid;gap:2px;align-items:center;width:max-content}}
    .viz .lbl{{font-size:10px;color:var(--t2);white-space:nowrap;padding-right:6px;text-align:right}}
    .viz .hd{{font-size:9px;color:var(--t2);text-align:center}}
    .viz .cell{{width:16px;height:12px;border-radius:2px;background:var(--track);display:flex;align-items:center;justify-content:center}}
    .viz .dot{{width:10px;height:10px;border-radius:50%}}
    .viz .scroll{{overflow:auto;padding:4px 2px 8px}}
    .viz .stats{{display:flex;flex-wrap:wrap;gap:12px}}
    .viz .stat{{border:1px solid var(--grid);border-radius:8px;padding:10px 16px;min-width:110px}}
    .viz .stat b{{display:block;font-size:28px;line-height:1.1;font-variant-numeric:tabular-nums}}
    .viz .stat.big b{{font-size:40px}}
    .viz .legend{{display:flex;gap:16px;flex-wrap:wrap;margin:4px 0 8px}}
    .viz .sw{{display:inline-block;width:12px;height:3px;border-radius:2px;vertical-align:middle;margin-right:6px}}
    .viz .chip{{border:2px solid var(--grid);border-radius:6px;width:34px;text-align:center;padding:2px 0}}
    .viz .chip.on{{border-color:var(--s0);background:color-mix(in srgb,var(--s0) 14%,transparent)}}
    .viz .chip b{{font:600 16px ui-monospace,monospace;display:block}}
    .viz .panel{{border:1px solid var(--grid);border-radius:10px;padding:12px;flex:1;min-width:280px}}
    .viz .panels{{display:flex;gap:14px;flex-wrap:wrap;align-items:stretch}}
    .viz .bar{{display:flex;gap:2px;margin:6px 0}}
    .viz .seg{{height:22px;border-radius:4px;color:#fff;font:600 11px/22px ui-sans-serif,system-ui;text-align:center}}
    """

    def viz(body):
        return mo.Html(f'<div class="viz"><style>{_CSS}</style>{body}</div>')

    def series(i):
        return f"var(--s{i})" if i < 8 else "var(--t2)"

    def letter_colors(letter, n):
        t = letter / max(n - 1, 1)
        bl, bd = _lerp(_RAMP_LIGHT, t), _lerp(_RAMP_DARK, t)
        return bl, _ink(bl), bd, _ink(bd)

    def tile(letter, n, cls="", title=""):
        bl, il, bd, idk = letter_colors(letter, n)
        return (
            f'<div class="tile {cls}" title="{title}" style="--bl:{bl};--il:{il};--bd:{bd};--id:{idk}">'
            f"{chr(97 + letter)}</div>"
        )

    def tiles(s, n):
        return f'<div style="display:flex;gap:2px">{"".join(tile(ord(ch) - 97, n) for ch in s)}</div>'

    def track(hit, color, title=""):
        dot = f'<div class="dot" style="background:{color}"></div>' if hit else ""
        return f'<div class="cell" title="{title}">{dot}</div>'

    return letter_colors, series, tile, tiles, track, viz


@app.cell(hide_code=True)
def _(anywidget, traitlets):
    class DancePlayer(anywidget.AnyWidget):
        """Animated line of dancers; each tile slides to its new slot after every dance."""

        _esm = r"""
        function render({ model, el }) {
          const frames = model.get("frames");
          const pal = model.get("palette");
          const dark = document.body.classList.contains("dark")
            || document.documentElement.getAttribute("data-theme") === "dark";
          const colors = dark ? pal.dark : pal.light;
          const W = 30, n = frames[0].length, last = frames.length - 1;
          el.innerHTML = `<div class="dp">
            <div class="dp-stage" style="width:${n * W}px"></div>
            <div class="dp-bar">
              <button class="dp-play">▶ play</button><button class="dp-step">step ›</button>
              <input class="dp-range" type="range" min="0" max="${last}" value="0">
            </div>
            <div class="dp-k"></div></div>`;
          const stage = el.querySelector(".dp-stage");
          const tiles = {};
          for (const ch of frames[0]) {
            const t = document.createElement("div");
            t.className = "dp-tile";
            t.textContent = ch;
            [t.style.background, t.style.color] = colors[ch];
            stage.appendChild(t);
            tiles[ch] = t;
          }
          const range = el.querySelector(".dp-range");
          const label = el.querySelector(".dp-k");
          const play = el.querySelector(".dp-play");
          let k = 0, timer = null;
          function show(next) {
            k = next;
            range.value = k;
            [...frames[k]].forEach((ch, i) => { tiles[ch].style.transform = `translateX(${i * W}px)`; });
            const home = [...frames[k]].filter((ch, i) => ch === frames[0][i]).length;
            const back = k > 0 && frames[k] === frames[0];
            label.textContent = `after ${k} dance${k === 1 ? "" : "s"} · ${home} of ${n} in their starting position`
              + (back ? "  ↺ back to the start!" : "");
            stage.classList.toggle("dp-home", back);
          }
          function stop() { clearInterval(timer); timer = null; play.textContent = "▶ play"; }
          play.onclick = () => {
            if (timer) return stop();
            if (k === last) show(0);
            play.textContent = "❚❚ pause";
            timer = setInterval(() => (k >= last ? stop() : show(k + 1)), model.get("interval"));
          };
          el.querySelector(".dp-step").onclick = () => { stop(); show(k === last ? 0 : k + 1); };
          range.oninput = () => { stop(); show(+range.value); };
          show(0);
          return () => clearInterval(timer);
        }
        export default { render };
        """
        _css = r"""
        .dp { font: 13px ui-sans-serif, system-ui, sans-serif; }
        .dp-stage { position: relative; height: 42px; margin: 6px 0 10px; border-radius: 8px;
          transition: box-shadow .3s; }
        .dp-home { box-shadow: 0 0 0 3px #0ca30c; }
        .dp-tile { position: absolute; top: 6px; left: 2px; width: 26px; height: 30px; border-radius: 5px;
          font: 600 15px/30px ui-monospace, monospace; text-align: center;
          transition: transform .45s cubic-bezier(.4, 0, .2, 1); }
        .dp-bar { display: flex; gap: 8px; align-items: center; }
        .dp-bar button { font: inherit; padding: 3px 12px; border-radius: 6px; border: 1px solid #8888;
          background: transparent; color: inherit; cursor: pointer; }
        .dp-range { flex: 1; max-width: 420px; }
        .dp-k { margin-top: 6px; font-variant-numeric: tabular-nums; }
        """
        frames = traitlets.List().tag(sync=True)
        palette = traitlets.Dict().tag(sync=True)
        interval = traitlets.Int(550).tag(sync=True)

    return (DancePlayer,)


@app.cell(hide_code=True)
def _(mo):
    # only offered when running next to a local input.txt; the browser export has none
    try:
        my_input = (mo.notebook_dir() / "input.txt").read_text()
    except (OSError, TypeError):
        my_input = None
    _choices = {"my puzzle input": "input"} if my_input else {}
    _choices |= {
        "a random 10,000-move dance": "random",
        "paste a puzzle input": "paste",
        "puzzle example (5 dancers)": "example",
        "custom": "custom",
    }
    source = mo.ui.dropdown(_choices, value=next(iter(_choices)), label="Dance")
    pasted_input = mo.ui.text_area(placeholder="paste a day 16 puzzle input here", full_width=True, rows=3)
    custom_moves = mo.ui.text(value="x0/1,pa/b", label="Custom moves", full_width=True)
    custom_n = mo.ui.number(start=2, stop=26, value=5, label="Dancers")
    return custom_moves, custom_n, my_input, pasted_input, source


@app.cell(hide_code=True)
def _(custom_moves, custom_n, my_input, pasted_input, random, source):
    def random_dance(n=16, count=10_000, seed=2020):
        rng = random.Random(seed)
        out = []
        for _ in range(count):
            match rng.choice("sxp"):
                case "s":
                    out.append(f"s{rng.randrange(1, n)}")
                case "x":
                    i, j = rng.sample(range(n), 2)
                    out.append(f"x{i}/{j}")
                case "p":
                    a, b = rng.sample(range(n), 2)
                    out.append(f"p{chr(97 + a)}/{chr(97 + b)}")
        return ",".join(out)

    def valid(move, n):
        match move[:1], move[1:].split("/"):
            case "s", [k]:
                return k.isdigit()
            case "x", [i, j]:
                return i.isdigit() and j.isdigit() and int(i) < n and int(j) < n
            case "p", [a, b]:
                return len(a) == len(b) == 1 and 0 <= ord(a) - 97 < n and 0 <= ord(b) - 97 < n
        return False

    n = 16
    match source.value:
        case "input":
            moves_text = my_input
        case "paste":
            moves_text = pasted_input.value
        case "example":
            moves_text, n = "s1,x3/4,pe/b", 5
        case "custom":
            moves_text, n = custom_moves.value, custom_n.value
        case _:
            moves_text = random_dance()
    moves = [m.strip() for m in moves_text.strip().split(",") if valid(m.strip(), n)]
    dance_note = ""
    if not moves:
        moves, n = random_dance().split(","), 16
        dance_note = "No valid moves yet, so this is showing a random 10,000-move dance."
    return dance_note, moves, n


@app.cell(hide_code=True)
def _(moves, n):
    def split_dance(moves, n):
        """Return (P, L): slot k ends up holding dancer P[k], and name x becomes L[x]."""
        P, L = list(range(n)), list(range(n))
        for move in moves:
            match move[0], *move[1:].split("/"):
                case "s", k:
                    k = int(k) % n
                    P = P[-k:] + P[:-k] if k else P
                case "x", i, j:
                    i, j = int(i), int(j)
                    P[i], P[j] = P[j], P[i]
                case "p", a, b:
                    i, j = L.index(ord(a) - 97), L.index(ord(b) - 97)
                    L[i], L[j] = L[j], L[i]
        return P, L

    def compose(f, g):
        """f after g."""
        return [f[x] for x in g]

    def power(p, k):
        result = list(range(len(p)))
        while k:
            if k & 1:
                result = compose(p, result)
            p = compose(p, p)
            k >>= 1
        return result

    def line(Pk, Lk):
        return "".join(chr(97 + Lk[d]) for d in Pk)

    P, L = split_dance(moves, n)
    identity = list(range(n))
    return L, P, compose, identity, line, power


@app.cell(hide_code=True)
def _(lcm, reduce):
    def cycles(p):
        seen, out = set(), []
        for start in range(len(p)):
            if start in seen:
                continue
            cyc, x = [], start
            while x not in seen:
                seen.add(x)
                cyc.append(x)
                x = p[x]
            out.append(cyc)
        return sorted(out, key=len, reverse=True)

    def order(p):
        return reduce(lcm, (len(c) for c in cycles(p)), 1)

    return cycles, order


@app.cell(hide_code=True)
def _(L, P, compose, identity, lcm, line, order):
    ord_P, ord_L = order(P), order(L)
    bound = lcm(ord_P, ord_L)
    start_line = line(identity, identity)

    # walk until the line comes back; bijections on a finite set have no tail
    period = [start_line]
    _Pk, _Lk = identity, identity
    while True:
        _Pk, _Lk = compose(P, _Pk), compose(L, _Lk)
        period.append(line(_Pk, _Lk))
        if period[-1] == start_line:
            break
    c = len(period) - 1
    one_dance = period[1]
    return bound, c, ord_L, ord_P, period, start_line


@app.cell(hide_code=True)
def _(factorial, lcm, reduce):
    def _partitions(n, most=None):
        most = most or n
        if n == 0:
            yield ()
            return
        for first in range(min(n, most), 0, -1):
            for rest in _partitions(n - first, first):
                yield (first,) + rest

    landau = {}
    for _m in range(1, 41):
        _best = {}
        for _part in _partitions(_m):
            _o = reduce(lcm, _part, 1)
            if _o not in _best or len(_part) < len(_best[_o]):
                _best[_o] = _part
        _g = max(_best)
        _pl, _a, _b = max((lcm(a, b), a, b) for a in _best for b in _best)
        landau[_m] = {
            "g": _g,
            "cycle type": " + ".join(str(x) for x in _best[_g] if x > 1) or "1",
            "pair": _pl,
            "pair from": f"lcm({_a}, {_b})",
            "distinct orders": len(_best),
            "fact": factorial(_m),
        }
    return (landau,)


@app.cell(hide_code=True)
def _(
    c,
    custom_moves,
    custom_n,
    dance_note,
    factorial,
    landau,
    mo,
    n,
    pasted_input,
    source,
    viz,
):
    _controls = [source]
    if source.value == "custom":
        _controls.append(mo.hstack([custom_moves, custom_n]))
    elif source.value == "paste":
        _controls.append(pasted_input)
    if dance_note:
        _controls.append(mo.md(f"*{dance_note}*"))
    mo.vstack(
        [
            mo.md(
                r"""
                # Why does the dance repeat so fast?

                *Advent of Code 2017, day 16: Permutation Promenade, part two*

                Finding the cycle and using `%` works. But **why** is there a short cycle at all?
                """
            ),
            viz(
                f"""<div class="stats" style="margin:18px 0">
                <div class="stat big"><span class="muted">possible lines of {n} dancers</span><b>{factorial(n):,}</b></div>
                <div class="stat big" style="border-color:var(--t1)"><span class="muted">dances until this one repeats</span><b>{c}</b></div>
                <div class="stat big"><span class="muted">longest possible, for any dance of {n}</span><b>{landau[min(n, 40)]["pair"]:,}</b></div>
                </div>"""
            ),
            *_controls,
        ]
    )
    return


@app.cell(hide_code=True)
def _(DancePlayer, letter_colors, mo, n, period):
    _pal = {"light": {}, "dark": {}}
    for _i in range(n):
        _bl, _il, _bd, _id = letter_colors(_i, n)
        _pal["light"][chr(97 + _i)] = [_bl, _il]
        _pal["dark"][chr(97 + _i)] = [_bd, _id]
    player = mo.ui.anywidget(DancePlayer(frames=period, palette=_pal))
    return (player,)


@app.cell(hide_code=True)
def _(c, mo, player):
    mo.vstack(
        [
            mo.md(
                rf"""
                ## The usual approach

                ```python
                seen = {{0: start}}
                for i in count(1):
                    state = dance(state)
                    if state == start: break   # ← this happens at i = {c}. Why so soon?
                    seen[i] = state
                answer = seen[10**9 % i]
                ```

                Press play and watch the line. Each tile slides to its new position after every dance.
                """
            ),
            player,
            mo.md(
                r"""
                There are **20,922,789,888,000** ways to arrange 16 dancers. If each dance sent the
                line somewhere unpredictable, a repeat would take trillions of dances. But a dance
                isn't unpredictable: it applies **the same moves every time**, and that turns out
                to be very restrictive.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(bound, mo):
    k_slider = mo.ui.slider(0, 2 * bound, value=1, label="dances k", show_value=True, full_width=True)
    return (k_slider,)


@app.cell(hide_code=True)
def _(cos, cycles, pi, series, sin):
    def rings(p, k, inner, outer, noun):
        """Each cycle of p as a ring; labels have rotated k steps along the arrows."""
        NODE, PAD, STEP, GAP = 12, 14, 36, 18
        laid, x, h = [], GAP / 2, 0
        for cyc in cycles(p):
            r = 0 if len(cyc) == 1 else max(STEP * len(cyc) / (2 * pi), STEP / 2)
            laid.append((cyc, r, x + r + NODE + PAD))
            x += 2 * (r + NODE + PAD) + GAP
            h = max(h, 2 * (r + NODE + PAD))
        cy, H = h / 2 + 4, h + 40
        out = []
        for ci, (cyc, r, cx) in enumerate(laid):
            m = len(cyc)
            home = k % m == 0
            color = series(ci) if m > 1 else "var(--t2)"
            width, alpha = (3, 1) if home else (1.75, 0.55)
            theta = [-pi / 2 + 2 * pi * j / m for j in range(m + 1)]
            pos = [(cx + r * cos(t), cy + r * sin(t)) for t in theta]
            if m > 1:
                d = (NODE + 4) / r
                for j in range(m):
                    a1, a2 = theta[j + 1] - d, theta[j] + d
                    x1, y1 = cx + r * cos(a1), cy + r * sin(a1)
                    x2, y2 = cx + r * cos(a2), cy + r * sin(a2)
                    out.append(
                        f'<path d="M{x1:.1f},{y1:.1f} A{r:.1f},{r:.1f} 0 0 0 {x2:.1f},{y2:.1f}" '
                        f'fill="none" stroke="{color}" stroke-width="{width}" opacity="{alpha}"/>'
                    )
                    tx, ty = sin(a2), -cos(a2)  # direction of travel at the arrow tip
                    nx, ny = cos(a2), sin(a2)
                    pts = [(x2, y2), (x2 - 7 * tx + 4 * nx, y2 - 7 * ty + 4 * ny), (x2 - 7 * tx - 4 * nx, y2 - 7 * ty - 4 * ny)]
                    out.append(
                        f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{color}" opacity="{alpha}"/>'
                    )
            for j in range(m):
                px, py = pos[j]
                here = cyc[(j + k) % m]
                ox, oy = (px, py - NODE - 6) if m == 1 else (cx + (r + NODE + 8) * cos(theta[j]), cy + (r + NODE + 8) * sin(theta[j]) + 3)
                out.append(
                    f"<g><title>{noun(cyc[j])} → {inner(here)} after {k} dance{'s' * (k != 1)}</title>"
                    f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{NODE}" fill="var(--surface)" stroke="{color}" stroke-width="{width}"/>'
                    f'<text x="{px:.1f}" y="{py + 4:.1f}" text-anchor="middle" font-size="12" font-weight="600">{inner(here)}</text>'
                    f'<text class="t2" x="{ox:.1f}" y="{oy:.1f}" text-anchor="middle" font-size="9">{outer(cyc[j])}</text></g>'
                )
            status = "✓ home" if home else f"{k % m} / {m}"
            out.append(
                f'<text x="{cx:.1f}" y="{H - 20}" text-anchor="middle" font-size="11" font-weight="600">{m}-cycle</text>'
                f'<text class="t2" x="{cx:.1f}" y="{H - 6}" text-anchor="middle" font-size="10">{status}</text>'
            )
        return f'<svg viewBox="0 0 {x:.0f} {H:.0f}" style="width:100%;max-width:{x:.0f}px">{"".join(out)}</svg>'

    return (rings,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The moves, and one fixed rearrangement

    A quick recap of the three moves:

    - **spin** `sX`: move the last X dancers to the front
    - **exchange** `xA/B`: swap the dancers at positions A and B
    - **partner** `pA/B`: swap the dancers *named* A and B

    Partner moves are the tricky kind, so set them aside until later.

    Spins and exchanges only ever talk about *positions*: "whoever is at position 3 goes to
    position 7". They never care who that dancer is. So the combined effect of one dance's
    spins and exchanges is **the same rearrangement of positions every time**.

    Call that rearrangement **P**.
    """)
    return


@app.cell(hide_code=True)
def _(P, k_slider, mo, n, ord_P, power, rings, tiles, viz):
    _k = k_slider.value
    _Pk = power(P, _k)
    _letter = lambda x: chr(97 + x)
    mo.vstack(
        [
            mo.md(
                r"""
                ## Why: one fixed shuffle sends every dancer around a fixed loop

                Repeating P moves the dancer at position 3 to position 7, then on to wherever 7 leads,
                and so on until it's back at 3. Every position is on a **loop** like this, and the loops
                are the same every dance. Drag $k$ to watch:
                """
            ),
            k_slider,
            viz(
                f"""<div style="display:flex;gap:10px;align-items:center;margin:6px 0">
                <b>Line after {_k} dance{"s" * (_k != 1)}, counting only spins and exchanges:</b>{tiles("".join(_letter(d) for d in _Pk), n)}</div>
                <div class="muted" style="margin-bottom:2px">Each ring is one loop of positions. Big letter = dancer at that position now,
                small number = the position.</div>
                {rings(P, _k, _letter, str, lambda s: f"position {s}")}"""
            ),
            mo.md(
                rf"""
                A loop of length $m$ is back where it started after $m, 2m, 3m, \dots$ dances. The whole
                line is back only when **every** loop is back at once, which first happens at the
                **lcm** of the loop lengths. That number is called the **order** of P. For this input's
                spins and exchanges it's **{ord_P}**.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    lcm_source = mo.ui.radio(
        ["P: this input's spins and exchanges", "L: this input's partner moves", "a random shuffle of 16", "custom lengths"],
        value="P: this input's spins and exchanges",
        inline=True,
    )
    lengths_input = mo.ui.text(value="4, 5, 7", label="loop lengths")
    lcm_reroll = mo.ui.button(label="🔀 shuffle again", value=0, on_click=lambda v: v + 1)
    return lcm_reroll, lcm_source, lengths_input


@app.cell(hide_code=True)
def _(
    L,
    P,
    cycles,
    lcm,
    lcm_reroll,
    lcm_source,
    lengths_input,
    mo,
    random,
    reduce,
    series,
    track,
    viz,
):
    if lcm_source.value == "P: this input's spins and exchanges":
        _ls = [len(cy) for cy in cycles(P)]
    elif lcm_source.value == "L: this input's partner moves":
        _ls = [len(cy) for cy in cycles(L)]
    elif lcm_source.value == "a random shuffle of 16":
        _q = list(range(16))
        random.Random(lcm_reroll.value).shuffle(_q)
        _ls = [len(cy) for cy in cycles(_q)]
    else:
        _ls = [int(x) for x in lengths_input.value.replace(",", " ").split() if x.isdigit() and int(x) > 0] or [1]
    _ord = reduce(lcm, _ls, 1)
    _cols = min(max(_ord, 12), 150)

    _segs = "".join(
        f'<div class="seg" style="flex:{m};background:{series(i) if m > 1 else "var(--t2)"}" title="loop of {m}">{m}</div>'
        for i, m in enumerate(_ls)
    )
    _cells = ["<div></div>"] + [
        f'<div class="hd" style="font-weight:{700 if j == _ord else 400}">{j if j % 10 == 0 or j == _ord else ""}</div>'
        for j in range(1, _cols + 1)
    ]
    for _i, _m in enumerate(_ls):
        _cells.append(f'<div class="lbl">loop of {_m}</div>')
        _cells += [track(j % _m == 0, series(_i) if _m > 1 else "var(--t2)", f"k={j}: {j % _m} / {_m}") for j in range(1, _cols + 1)]
    _cells.append('<div class="lbl"><b>all home</b></div>')
    _cells += [track(j % _ord == 0, "var(--t1)", f"k={j}") for j in range(1, _cols + 1)]

    _extra = {"a random shuffle of 16": lcm_reroll, "custom lengths": lengths_input}.get(lcm_source.value)
    mo.vstack(
        [
            mo.md(
                r"""
                ## Loops line up at the lcm

                Each row is one loop. A dot means that loop is home after $k$ dances. The line is back
                to the start only in a column where **every** row has a dot.
                """
            ),
            mo.hstack([lcm_source, _extra] if _extra else [lcm_source], justify="start", gap=1),
            viz(
                f"""<div class="bar" style="max-width:520px">{_segs}</div>
                <div style="margin:4px 0 6px">{sum(_ls)} positions in loops of {", ".join(map(str, _ls))} ·
                order = lcm = <b style="font-size:16px">{_ord}</b>
                <span class="muted">{"(first 150 shown)" if _ord > 150 else ""}</span></div>
                <div class="scroll"><div class="grid" style="grid-template-columns:auto repeat({_cols},16px)">
                {"".join(_cells)}</div></div>"""
            ),
            mo.md(
                r"""
                Some lengths to try with **custom lengths**:

                - `5, 5` and then `5`: the same order. A repeated length adds nothing.
                - `4, 6`: order 12, not 24, because 4 and 6 share a factor of 2.
                - `4, 5, 7`: order 140, the largest possible with 16 positions.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, moves, start_line, viz):
    def simulate(state, moves):
        """Run one dance on an actual line of letters, moves interleaved."""
        d = list(state)
        for move in moves:
            match move[0], *move[1:].split("/"):
                case "s", k:
                    k = int(k) % len(d)
                    d = d[-k:] + d[:-k] if k else d
                case "x", i, j:
                    i, j = int(i), int(j)
                    d[i], d[j] = d[j], d[i]
                case "p", a, b:
                    i, j = d.index(a), d.index(b)
                    d[i], d[j] = d[j], d[i]
        return "".join(d)

    def _shuffle(before, after):
        return [before.index(ch) for ch in after]

    _d1 = simulate(start_line, moves)
    _d2 = simulate(_d1, moves)
    _q1, _q2 = _shuffle(start_line, _d1), _shuffle(_d1, _d2)
    mo.vstack(
        [
            mo.md(
                r"""
                ## The wrinkle: partner moves

                `pa/b` swaps *dancers a and b*, wherever they're standing. Which positions that touches
                depends on where the names are, so the full dance is **not** the same rearrangement of positions each time:
                """
            ),
            viz(
                f"""<pre style="font-size:12px;margin:0 0 10px">where each position's dancer came from
    dance 1: {_q1}
    dance 2: {_q2}   {"same" if _q1 == _q2 else "← different!"}</pre>"""
            ),
            mo.md(
                r"""
                The way out is to treat it as **two** fixed shuffles. **P** rearranges
                *positions* (spins and exchanges, as before), and a second one, **L**, relabels *names*
                (partner moves). Each is a fixed shuffle of just 16 things,
                with its own loops and its own order. The next slide shows why they can be pulled apart.
                """
            ),
        ]
    )
    return (simulate,)


@app.cell(hide_code=True)
def _(mo):
    _options = ["s1", "s2", "x0/2", "x1/3", "x3/4", "pa/c", "pb/d", "pc/e", "pa/b"]
    move_a = mo.ui.dropdown(_options, value="x0/2", label="move A")
    move_b = mo.ui.dropdown(_options, value="pb/d", label="move B")
    return move_a, move_b


@app.cell(hide_code=True)
def _(mo, move_a, move_b, simulate, tile, viz):
    _start = "abcde"

    def _kind(m):
        return "name move" if m[0] == "p" else "position move"

    def _line(s, prev):
        return '<div style="display:flex;gap:3px">' + "".join(
            tile(ord(ch) - 97, 5, "lg now" if prev and ch != prev[i] else "lg") for i, ch in enumerate(s)
        ) + "</div>"

    def _row(label, first, second):
        one = simulate(_start, [first])
        two = simulate(one, [second])
        step = lambda m: f'<div class="muted" style="text-align:center;font-size:12px">→ <code>{m}</code> →</div>'
        return f'<div class="lbl" style="font-size:12px">{label}</div>{_line(_start, None)}{step(first)}{_line(one, _start)}{step(second)}{_line(two, one)}', two

    _a, _b = move_a.value, move_b.value
    _r1, _end1 = _row("A then B", _a, _b)
    _r2, _end2 = _row("B then A", _b, _a)
    _same = _end1 == _end2
    mo.vstack(
        [
            mo.md(
                r"""
                ## Why the two kinds of moves can be separated

                Picture every dancer wearing a name tag.

                - A **position move** (spin, exchange) is an instruction about places: "swap whoever
                  is at positions 0 and 2". It can be carried out without reading a single name tag.
                - A **name move** (partner) is an instruction about tags: "swap the dancers tagged a and c".
                  That gives the same line as just swapping those two tags, which doesn't depend on
                  where anyone is standing.

                Neither kind depends on anything the other kind changes. So a position move followed
                by a name move gives the same line as the other way round. Pick two moves and compare:
                """
            ),
            mo.hstack([move_a, move_b], justify="start", gap=2),
            viz(
                f"""<div style="margin:6px 0 4px" class="muted">A is a {_kind(_a)}, B is a {_kind(_b)}.
                Outlined dancers changed in that step.</div>
                <div class="grid" style="grid-template-columns:auto auto auto auto auto auto;gap:10px 10px">{_r1}{_r2}</div>
                <div style="margin-top:10px;font-size:15px"><b>{"✓ same line either way" if _same else "✗ the order matters here"}</b></div>"""
            ),
            mo.md(
                r"""
                A position move and a name move always give the same line. Try two position moves,
                or two partner moves that share a dancer: there, the order usually matters.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo, moves, n, series, simulate, start_line, tiles, viz):
    _shown = moves[:48]
    _position_moves = [m for m in moves if m[0] != "p"]
    _name_moves = [m for m in moves if m[0] == "p"]

    def _chips(ms):
        return "".join(
            f'<span style="display:inline-block;border:2px solid {series(1) if m[0] == "p" else series(0)};'
            f'border-radius:4px;padding:0 4px;margin:2px;font:11px ui-monospace,monospace">{m}</span>'
            for m in ms
        )

    _regrouped = [m for m in _shown if m[0] != "p"] + [m for m in _shown if m[0] == "p"]
    _real = simulate(start_line, moves)
    _split = simulate(start_line, _position_moves + _name_moves)
    mo.vstack(
        [
            mo.md(
                r"""
                ## So every dance is "all position moves, then all name moves"

                Since a position move can always trade places with a name move next to it, keep
                trading until every position move is at the front, still in its original order.
                Here are the first 48 of this input's moves:
                """
            ),
            viz(
                f"""<div class="legend"><span><span class="sw" style="background:var(--s0);height:10px"></span>position move (spin, exchange)</span>
                <span><span class="sw" style="background:var(--s1);height:10px"></span>name move (partner)</span></div>
                <div class="lbl" style="text-align:left;margin-top:4px">as written</div><div style="max-width:720px">{_chips(_shown)}</div>
                <div class="lbl" style="text-align:left;margin-top:8px">position moves first</div><div style="max-width:720px">{_chips(_regrouped)}</div>
                <div class="grid" style="grid-template-columns:auto auto auto;gap:6px 12px;margin-top:12px">
                <div class="lbl">whole dance, as written</div>{tiles(_real, n)}<div></div>
                <div class="lbl">whole dance, position moves first</div>{tiles(_split, n)}<div>{"✓ same" if _real == _split else "✗ different"}</div>
                </div>"""
            ),
            mo.md(
                r"""
                All the position moves together are **P**, and all the name moves together are **L**,
                so one dance is "P, then L". Two dances are P, L, P, L, and the middle L and P can trade
                places too, giving P, P, L, L. In general, **$k$ dances = P applied $k$ times, then L
                applied $k$ times**. That's why P and L can each be raised to a power on their own and
                the results applied at the end.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The same idea, in symbols

    Write the current line as a function $\sigma$: give it a position, and it returns the
    name standing there.

    - A **position move** rearranges which position each spot reads from. If it sends
      position $i$ to read old position $\pi(i)$, the new line is $\sigma \circ \pi$.
      It attaches on the **right**, the input side, where positions go in.
    - A **name move** relabels whatever name comes out. If it renames $x$ to $\lambda(x)$,
      the new line is $\lambda \circ \sigma$. It attaches on the **left**, the output side,
      where names come out.

    So with both, a position goes through $\pi$, then $\sigma$, then $\lambda$. That's written
    $\lambda \circ \sigma \circ \pi$, because composition reads right to left.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    sym_pos = mo.ui.dropdown(["x0/2", "x1/4", "s1", "s2"], value="x0/2", label="position move π")
    sym_name = mo.ui.dropdown(["pb/d", "pa/e", "pc/e"], value="pb/d", label="name move λ")
    return sym_name, sym_pos


@app.cell(hide_code=True)
def _(L, P, compose, mo, series, simulate, sym_name, sym_pos, tiles, viz):
    _sigma = "baecd"
    _m, _l = sym_pos.value, sym_name.value
    if _m[0] == "s":
        _pi = [(i - int(_m[1:])) % 5 for i in range(5)]
    else:
        _a, _b = map(int, _m[1:].split("/"))
        _pi = list(range(5))
        _pi[_a], _pi[_b] = _b, _a
    _lam = lambda ch: _l[3] if ch == _l[1] else _l[1] if ch == _l[3] else ch

    _X, _Y = [60, 230, 400, 570], lambda j: 60 + 40 * j
    _svg = [
        f'<text class="t2" x="{x}" y="18" text-anchor="middle" font-size="11">{t}</text>'
        for x, t in zip(_X, ["position i", "reads position π(i)", "name there, σ(π(i))", "relabeled, λ(σ(π(i)))"])
    ]
    for _x0, _x1, _t, _c in [(_X[0], _X[1], "π", series(0)), (_X[1], _X[2], "σ", "var(--t2)"), (_X[2], _X[3], "λ", series(1))]:
        _svg.append(f'<text x="{(_x0 + _x1) / 2}" y="40" text-anchor="middle" font-size="14" font-weight="700" fill="{_c}">{_t}</text>')
    for _i in range(5):
        _svg.append(f'<line x1="{_X[0] + 14}" y1="{_Y(_i)}" x2="{_X[1] - 14}" y2="{_Y(_pi[_i])}" stroke="var(--s0)" stroke-width="2"/>')
        _svg.append(f'<line x1="{_X[1] + 14}" y1="{_Y(_i)}" x2="{_X[2] - 14}" y2="{_Y(_i)}" stroke="var(--t2)" stroke-width="1.5" stroke-dasharray="3 3"/>')
        _changed = _lam(_sigma[_i]) != _sigma[_i]
        _svg.append(
            f'<line x1="{_X[2] + 14}" y1="{_Y(_i)}" x2="{_X[3] - 14}" y2="{_Y(_i)}" stroke="var(--s1)" stroke-width="{2.5 if _changed else 1}" opacity="{1 if _changed else 0.4}"/>'
        )
    for _col, _labels in enumerate([range(5), range(5), list(_sigma), [_lam(ch) for ch in _sigma]]):
        for _j, _lab in enumerate(_labels):
            _svg.append(
                f'<circle cx="{_X[_col]}" cy="{_Y(_j)}" r="13" fill="var(--surface)" stroke="var(--t2)"/>'
                f'<text x="{_X[_col]}" y="{_Y(_j) + 4}" text-anchor="middle" font-size="12" font-weight="600">{_lab}</text>'
            )

    _result = "".join(_lam(_sigma[_pi[_i]]) for _i in range(5))
    _pos_first = simulate(simulate(_sigma, [_m]), [_l])
    _name_first = simulate(simulate(_sigma, [_l]), [_m])
    _PL, _LP = compose(P, L), compose(L, P)
    mo.vstack(
        [
            mo.md(
                r"""
                ## Positions on the right, names on the left

                Pick a position move and a name move, and follow each position from left to right.
                """
            ),
            mo.hstack([sym_pos, sym_name], justify="start", gap=2),
            viz(
                f"""<svg viewBox="0 0 640 {_Y(4) + 24}" style="width:100%;max-width:640px">{"".join(_svg)}</svg>
                <div class="grid" style="grid-template-columns:auto auto auto;gap:6px 12px;margin-top:4px">
                <div class="lbl">read off the diagram</div>{tiles(_result, 5)}<div></div>
                <div class="lbl">position move, then name move</div>{tiles(_pos_first, 5)}<div>{"✓" if _pos_first == _result else "✗"}</div>
                <div class="lbl">name move, then position move</div>{tiles(_name_first, 5)}<div>{"✓" if _name_first == _result else "✗"}</div>
                </div>"""
            ),
            mo.md(
                rf"""
                $\pi$ only touches the start of each path and $\lambda$ only the end, so it doesn't matter
                which is added first: $\lambda \circ (\sigma \circ \pi) = (\lambda \circ \sigma) \circ \pi$.
                Every dance adds P on the right and L on the left, so after $k$ dances the line is
                $L^k \circ \sigma \circ P^k$.

                What commutes is *acting on the right* with *acting on the left*. P and L composed
                directly with each other generally don't commute: for this dance,
                $P \circ L {"=" if _PL == _LP else r"\neq"} L \circ P$.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(
    L,
    P,
    bound,
    c,
    compose,
    identity,
    k_slider,
    mo,
    n,
    ord_L,
    ord_P,
    rings,
    series,
    tile,
    track,
    viz,
):
    _k = k_slider.value
    _cols = min(max(bound, 12), 120)
    _snap, _Pk, _Lk = [], identity, identity
    for _ in range(_cols + 1):
        _snap.append((_Pk, _Lk))
        _Pk, _Lk = compose(P, _Pk), compose(L, _Lk)

    _cells = ["<div></div>"] + [
        f'<div class="hd" style="font-weight:{700 if j in (c, _k) else 400}">{j if j % 5 == 0 or j in (c, _k) else ""}</div>'
        for j in range(_cols + 1)
    ]
    for _s in range(n):
        _cells.append(f'<div class="lbl">pos {_s}</div>')
        _cells += [tile(lk[pk[_s]], n, "now" if j == _k else "", f"k={j}, position {_s}") for j, (pk, lk) in enumerate(_snap)]
    _cells += ['<div style="height:6px"></div>'] * (_cols + 2)
    for _label, _color, _hit in [
        (f"position loops home (every {ord_P})", series(0), lambda pk, lk: pk == identity),
        (f"name loops home (every {ord_L})", series(1), lambda pk, lk: lk == identity),
        ("line = start", "var(--t1)", lambda pk, lk: [lk[d] for d in pk] == identity),
    ]:
        _cells.append(f'<div class="lbl">{_label}</div>')
        _cells += [track(_hit(pk, lk), _color, f"k={j}") for j, (pk, lk) in enumerate(_snap)]

    _letter = lambda x: chr(97 + x)
    mo.vstack(
        [
            mo.md(
                rf"""
                ## Putting it together

                Position loops come home every **{ord_P}** dances and name loops every **{ord_L}**. Both are
                home at lcm({ord_P}, {ord_L}) = **{bound}**, and the line is back at **{c}**. Each column
                below is the line after $k$ dances. Color follows the letter, so the start is a smooth gradient.
                """
            ),
            k_slider,
            viz(
                f"""<div class="scroll"><div class="grid" style="grid-template-columns:auto repeat({_cols + 1},16px)">
                {"".join(_cells)}</div></div>
                <details style="margin-top:6px"><summary class="muted">name loops (L) after {_k}</summary>
                {rings(L, _k, _letter, _letter, lambda x: f"dancer {_letter(x)}")}</details>"""
            ),
            mo.md(
                r"""
                It *can* come back before the lcm: with the custom dance `x0/1,pa/b`, the rename
                undoes the swap, so it repeats after 1 even though both orders are 2. The lcm is only
                an upper bound.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    hist_reroll = mo.ui.button(label="🔀 draw 20,000 new shuffles", value=0, on_click=lambda v: v + 1)
    return (hist_reroll,)


@app.cell(hide_code=True)
def _(
    Counter,
    cycles,
    hist_reroll,
    lcm,
    mo,
    ord_L,
    ord_P,
    random,
    reduce,
    viz,
):
    _rng = random.Random(hist_reroll.value)
    _counts = Counter()
    _q = list(range(16))
    for _ in range(20_000):
        _rng.shuffle(_q)
        _counts[reduce(lcm, (len(cy) for cy in cycles(_q)), 1)] += 1
    _orders = sorted(_counts)
    _W, _H, _l, _b, _t = 680, 240, 40, 34, 22
    _bw = (_W - _l - 8) / len(_orders)
    _top = max(_counts.values())
    _svg = []
    for _f in (0.25, 0.5, 0.75, 1):
        _y = _H - _b - _f * (_H - _b - _t)
        _svg.append(
            f'<line x1="{_l}" x2="{_W}" y1="{_y:.1f}" y2="{_y:.1f}" stroke="var(--grid)"/>'
            f'<text class="t2" x="{_l - 4}" y="{_y + 3:.1f}" font-size="9" text-anchor="end">{_f * _top / 200:.0f}%</text>'
        )
    _mark = {ord_P: "this P", ord_L: "this L", 140: "max 140"}
    for _i, _o in enumerate(_orders):
        _h = _counts[_o] / _top * (_H - _b - _t)
        _x = _l + _i * _bw
        _svg.append(
            f'<rect x="{_x + 1:.1f}" y="{_H - _b - _h:.1f}" width="{max(_bw - 2, 1):.1f}" height="{_h:.1f}" rx="2" '
            f'fill="var(--s0)"><title>order {_o}: {_counts[_o] / 200:.2f}% of shuffles</title></rect>'
        )
        if _o in _mark or _i % 4 == 0:
            _svg.append(f'<text class="t2" x="{_x + _bw / 2:.1f}" y="{_H - _b + 12}" font-size="9" text-anchor="middle">{_o}</text>')
        if _o in _mark:
            _svg.append(
                f'<text x="{_x + _bw / 2:.1f}" y="{_H - _b - _h - 6:.1f}" font-size="10" font-weight="600" text-anchor="{"end" if _i > len(_orders) - 4 else "middle"}">{_mark[_o]}</text>'
            )
    _svg.append(f'<text class="t2" x="{(_W + _l) / 2}" y="{_H - 4}" font-size="10" text-anchor="middle">order of the shuffle (one bar per possible value)</text>')
    _over100 = sum(v for o, v in _counts.items() if o > 100) / 200
    mo.vstack(
        [
            mo.md(
                r"""
                ## How long could a loop-up take?

                Shuffle 16 positions at random 20,000 times and see how many repeats each shuffle needs
                before it's back to the start (its order):
                """
            ),
            hist_reroll,
            viz(
                f"""<svg viewBox="0 0 {_W} {_H}" style="width:100%;max-width:{_W}px">{"".join(_svg)}</svg>
                <div class="stats" style="margin-top:6px">
                <div class="stat"><span class="muted">most common</span><b>{max(_counts, key=_counts.get)}</b></div>
                <div class="stat"><span class="muted">largest seen</span><b>{max(_orders)}</b></div>
                <div class="stat"><span class="muted">order &gt; 100</span><b>{_over100:.1f}%</b></div>
                </div>"""
            ),
            mo.md(
                r"""
                There are only a few dozen possible orders, and **none above 140**. The maximum comes
                from loops of $4 + 5 + 7$. That's the next slide.
                """
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    landau_n = mo.ui.slider(1, 40, value=16, label="dancers n", show_value=True, full_width=True)
    return (landau_n,)


@app.cell(hide_code=True)
def _(landau, landau_n, log10, mo, series, viz):
    _W, _H, _l, _r, _t, _b = 680, 280, 44, 96, 12, 30
    _N, _ymax = 40, 48
    _sel = landau_n.value
    _X = lambda m: _l + (m - 1) / (_N - 1) * (_W - _l - _r)
    _Y = lambda v: _t + (1 - log10(v) / _ymax) * (_H - _t - _b)
    _lines = [("n!", "fact", series(2)), ("worst dance", "pair", series(1)), ("g(n)", "g", series(0))]

    _svg = []
    for _e in range(0, _ymax + 1, 8):
        _svg.append(
            f'<line x1="{_l}" x2="{_W - _r}" y1="{_Y(10**_e):.1f}" y2="{_Y(10**_e):.1f}" stroke="var(--grid)"/>'
            f'<text class="t2" x="{_l - 6}" y="{_Y(10**_e) + 3:.1f}" text-anchor="end" font-size="10">10<tspan dy="-4" font-size="8">{_e}</tspan></text>'
        )
    for _m in (1, 5, 10, 15, 20, 25, 30, 35, 40):
        _svg.append(f'<text class="t2" x="{_X(_m):.1f}" y="{_H - 12}" text-anchor="middle" font-size="10">{_m}</text>')
    _svg.append(f'<text class="t2" x="{(_W - _r + _l) / 2}" y="{_H}" text-anchor="middle" font-size="10">dancers n</text>')
    _svg.append(f'<line x1="{_X(_sel):.1f}" x2="{_X(_sel):.1f}" y1="{_t}" y2="{_H - _b}" stroke="var(--t2)" stroke-dasharray="3 3"/>')
    for _name, _key, _color in _lines:
        _pts = " ".join(f"{_X(m):.1f},{_Y(landau[m][_key]):.1f}" for m in range(1, _N + 1))
        _svg.append(f'<polyline points="{_pts}" fill="none" stroke="{_color}" stroke-width="2" stroke-linejoin="round"/>')
        _svg.append(f'<text x="{_X(_N) + 8:.1f}" y="{_Y(landau[_N][_key]) + 4:.1f}" font-size="11">{_name}</text>')
        _svg.append(
            f'<circle cx="{_X(_sel):.1f}" cy="{_Y(landau[_sel][_key]):.1f}" r="5" fill="{_color}" stroke="var(--surface)" stroke-width="2"/>'
        )
    _step = (_W - _l - _r) / (_N - 1)
    for _m in range(1, _N + 1):
        _d = landau[_m]
        _svg.append(
            f'<rect x="{_X(_m) - _step / 2:.1f}" y="{_t}" width="{_step:.1f}" height="{_H - _t - _b}" fill="transparent">'
            f'<title>n = {_m}\ng(n) = {_d["g"]:,} ({_d["cycle type"]})\nworst dance ≤ {_d["pair"]:,} = {_d["pair from"]}\nn! = {_d["fact"]:,}</title></rect>'
        )

    _d = landau[_sel]
    mo.vstack(
        [
            mo.md(
                r"""
                ## The ceiling: Landau's function

                $g(n)$ is the largest lcm obtainable by splitting $n$ positions into loops. The best
                splits use loop lengths with no common factors. A dance has two shuffles, so its
                worst case is the largest lcm of two possible orders. Note the log scale.
                """
            ),
            landau_n,
            viz(
                f"""<div class="legend">{"".join(f'<span><span class="sw" style="background:{c}"></span>{nm}</span>' for nm, _, c in reversed(_lines))}</div>
                <svg viewBox="0 0 {_W} {_H}" style="width:100%;max-width:{_W}px">{"".join(_svg)}</svg>
                <div class="stats" style="margin-top:8px">
                <div class="stat"><span class="muted">g({_sel})</span><b>{_d["g"]:,}</b><span class="muted">loops {_d["cycle type"]}</span></div>
                <div class="stat"><span class="muted">worst dance of {_sel}</span><b>{_d["pair"]:,}</b><span class="muted">{_d["pair from"]}</span></div>
                <div class="stat"><span class="muted">{_sel}! possible lines</span><b>{_d["fact"]:.2e}</b></div>
                </div>"""
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(c, mo, ord_L, ord_P):
    mo.md(rf"""
    ## Takeaways

    1. **16! is the wrong number.** A dance doesn't wander among 16! lines. It applies the
       *same* shuffle every time, and that's a much more rigid thing.
    2. **Fixed shuffle → fixed loops.** Every position (and every name) goes around a loop that
       never changes. Everything is home at the **lcm of the loop lengths**: the shuffle's *order*.
    3. **Partner moves are a second shuffle, of names.** Rearranging positions and relabeling names
       commute, so $k$ dances is P applied $k$ times, then L applied $k$ times. The line repeats within
       lcm(ord P, ord L): lcm({ord_P}, {ord_L}) for this input, and the actual cycle is {c}.
    4. **The ceiling is tiny.** Loops of 16 positions give at most order 140 (4 + 5 + 7), and a dance of
       16 can't take more than 5,460 rounds. Cycle detection is *guaranteed* to finish quickly.
    5. **No tail, either.** A shuffle can be undone, so the first repeated line is always the start.
       Checking `state == start` is enough.
    6. **The same fact allows exponentiating.** Raise P and L to the $K$-th power separately, then apply both.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    big_k = mo.ui.text(value="1000000000", label="dances K")
    return (big_k,)


@app.cell(hide_code=True)
def _(
    L,
    P,
    big_k,
    c,
    identity,
    line,
    mo,
    n,
    ord_L,
    ord_P,
    period,
    power,
    start_line,
    tiles,
    viz,
):
    _K = int(big_k.value) if big_k.value.strip().isdigit() else 0
    _a, _b = _K % ord_P, _K % ord_L
    _slots = line(power(P, _a), identity)
    _final = line(power(P, _a), power(L, _b))
    _check = period[_K % c]
    mo.vstack(
        [
            mo.md(
                rf"""
                ## Exponentiating, briefly

                Because $K$ dances is P applied $K$ times and then L applied $K$ times, part two only needs $P^K$ and $L^K$.
                And because $P^{{{ord_P}}} = \mathrm{{id}}$ and $L^{{{ord_L}}} = \mathrm{{id}}$, only $K$ modulo
                each order matters:
                """
            ),
            big_k,
            viz(
                f"""<div style="margin:8px 0 12px;font-variant-numeric:tabular-nums">
                P<sup>K</sup> = P<sup>{_K:,} mod {ord_P}</sup> = <b>P<sup>{_a}</sup></b> &nbsp;·&nbsp;
                L<sup>K</sup> = L<sup>{_K:,} mod {ord_L}</sup> = <b>L<sup>{_b}</sup></b></div>
                <div class="grid" style="grid-template-columns:auto auto;gap:6px 14px">
                <div class="lbl">start</div>{tiles(start_line, n)}
                <div class="lbl">apply P<sup>{_a}</sup> (move positions)</div>{tiles(_slots, n)}
                <div class="lbl">apply L<sup>{_b}</sup> (rename)</div>{tiles(_final, n)}
                <div class="lbl">cycle detection: dance {_K % c}</div>{tiles(_check, n)}
                </div><div style="margin-top:6px">{"✓ same answer" if _final == _check else "✗ mismatch"}</div>"""
            ),
            mo.md(
                r"""
                Without knowing the orders, repeated squaring does the same job in about $\log_2 K$ steps:
                compute $P, P^2, P^4, P^8, \dots$ and multiply the ones matching $K$'s binary digits
                (for example $10 = 8 + 2$, so $P^{10} = P^8 \circ P^2$).
                """
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
