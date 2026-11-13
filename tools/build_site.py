"""Build the website (web/) from the Markdown pages and programs in this repo.

Run from the repo root after editing any page or program:

    pip install markdown        # once
    python3 tools/build_site.py
    node tools/make_pdfs.mjs     # optional: refresh the printable PDFs (needs Playwright)

The Markdown files stay the source of truth. web/ is generated: don't edit it by hand.

What it makes:
- web/index.html                the calendar, with a progress bar that remembers finished weeks
- web/<phase>/<week>/index.html one page per week, with the programs inline and a Copy button
- web/<page>.html               Start here, Parent guide, Materials, Safety, Glossary, ...
- web/print/*.html              printables: activity book, journal page, fridge poster,
                                certificate and grown-ups handbook (make_pdfs.mjs turns them into PDFs)
"""
import html
import pathlib
import re
import shutil
import sys

try:
    import markdown
except ImportError:
    sys.exit("Missing the 'markdown' package. Install it with:  pip install markdown")

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "web"
ASSETS_SRC = ROOT / "tools" / "site"

REPO = "pandagardenio/robokids"
GITHUB_BLOB = f"https://github.com/{REPO}/blob/main/"
PAGES_ROOT = "https://pandagardenio.github.io/robokids/"
SITE_URL = PAGES_ROOT + "web/"
BRIDGE_URL = PAGES_ROOT + "ai/bridge.html"

SITE_NAME = "A Year of Robots"

# Section headings → icon and whether it's a grown-up job.
SECTION_ICONS = {
    "You need": ("🧰", None),
    "Build together": ("🔧", "Together"),
    "Build: Cutebot mouse": ("🔧", "Together"),
    "Build: DIY mouse": ("🔧", "Together"),
    "Play": ("🎮", "Kid time"),
    "Talk about it": ("💬", "Together"),
    "Level up": ("⭐", "Kid time"),
    "Load the program": ("💻", "Grown-up job"),
    "Load the programs": ("💻", "Grown-up job"),
    "Words this week": ("📖", "For grown-ups"),
    "Robot Journal": ("✏️", "Kid time"),
    "Pick your version": ("🔀", None),
    "Tuning knobs": ("🎛️", "Together"),
    "Cheese": ("🧀", None),
}

# Extra pages, in menu order: (source, output, short name).
PAGES = [
    ("START-HERE.md", "start-here.html", "Start here"),
    ("PARENT-GUIDE.md", "parent-guide.html", "Parent guide"),
    ("MATERIALS.md", "materials.html", "Materials"),
    ("SAFETY.md", "safety.html", "Safety"),
    ("GLOSSARY.md", "glossary.html", "Glossary"),
    ("ai/README.md", "ai/index.html", "AI bridge guide"),
    ("TECHNICAL.md", "technical.html", "Technical notes"),
]

# Text that only makes sense on GitHub, rewritten for the website.
WEB_REPLACEMENTS = [
    (
        "Click the program link, then the **Copy raw file** button (two small squares, top right of the program).",
        "Click the green **📋 Copy** button on the program (below these steps).",
    ),
    (
        "**Copy the program.** On the week's page, click the program link (for example `main.ts`). GitHub shows the program. "
        "Click the **Copy raw file** button: two small overlapping squares at the top right of the program.\n"
        "   *Can't find it?* Click **Raw** instead, then select all (**Ctrl+A** / **Cmd+A**) and copy (**Ctrl+C** / **Cmd+C**).",
        "**Copy the program.** On the week's page, scroll to **Load the program** and click the green **📋 Copy** button on the program.",
    ),
    (
        "Open [`bridge.html`](bridge.html) on GitHub and click the **Download raw file** button",
        f"Open [`bridge.html` on GitHub]({GITHUB_BLOB}ai/bridge.html) and click the **Download raw file** button",
    ),
]

PHASE_SHORT = {1: "Circuits and Motors", 2: "micro:bit First Steps", 3: "The Robot Car", 4: "Smarter Robots", 5: "Robots That Learn"}
PHASE_EMOJI = {1: "💡", 2: "📟", 3: "🚗", 4: "🦾", 5: "🧠"}


# --------------------------------------------------------------------------- helpers

def esc(s):
    return html.escape(s, quote=True)


def slugify(text, sep="-"):
    """GitHub-style heading anchors, so links like START-HERE.md#load-a-program keep working."""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", sep).strip(sep) if text.strip() else "section"


def md_to_html(text):
    text = text.replace("<details>", '<details markdown="1">')
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "md_in_html", "sane_lists", "toc"],
        extension_configs={"toc": {"slugify": lambda value, separator: slugify(value, separator)}},
    )


def inline_md(text):
    """Render a single line of Markdown without the surrounding <p>."""
    out = md_to_html(text).strip()
    return re.sub(r"^<p>(.*)</p>$", r"\1", out, flags=re.S)


def rel(from_out: pathlib.Path, to_out: pathlib.Path) -> str:
    """Relative URL from one output file to another (both relative to OUT)."""
    import os
    return os.path.relpath(to_out, from_out.parent).replace(os.sep, "/")


def out_path_for_md(src: pathlib.Path) -> pathlib.Path:
    """Repo-relative .md path → output path relative to OUT."""
    for s, o, _ in PAGES:
        if src.as_posix() == s:
            return pathlib.Path(o)
    if src.as_posix() == "README.md":
        return pathlib.Path("index.html")
    if src.as_posix() == "PROGRESS.md":
        return pathlib.Path("progress.html")
    if src.name == "README.md":
        return src.parent / "index.html"
    return src.with_suffix(".html")


def rewrite_links(body: str, src: pathlib.Path, out: pathlib.Path) -> str:
    """Point .md links at the generated pages, .ts links at the inline programs, other files at GitHub."""
    import posixpath

    def fix(m):
        attr, url = m.group(1), html.unescape(m.group(2))
        if re.match(r"^(https?:|mailto:|#)", url):
            if url.startswith("http"):
                return f'{attr}="{esc(url)}" target="_blank" rel="noopener"'
            return f'{attr}="{esc(url)}"'
        path, _, frag = url.partition("#")
        target = pathlib.Path(posixpath.normpath(posixpath.join(src.parent.as_posix(), path)))
        if target.suffix == ".md":
            new = rel(out, out_path_for_md(target)) + (f"#{frag}" if frag else "")
        elif target.suffix == ".ts":
            anchor = "program-" + slugify(target.name.replace(".", "-"))
            if target.parent == src.parent:
                new = f"#{anchor}"
            else:
                new = rel(out, target.parent / "index.html") + f"#{anchor}"
        else:
            return f'{attr}="{esc(GITHUB_BLOB + target.as_posix())}" target="_blank" rel="noopener"'
        return f'{attr}="{esc(new)}"'

    return re.sub(r'(href)="([^"]*)"', fix, body)


def apply_web_replacements(text):
    for old, new in WEB_REPLACEMENTS:
        text = text.replace(old, new)
    return text


# --------------------------------------------------------------------------- content model

class Week:
    def __init__(self, path: pathlib.Path):
        self.dir = path.parent.relative_to(ROOT)
        self.src = path.relative_to(ROOT)
        self.out = self.dir / "index.html"
        raw = path.read_text(encoding="utf-8")
        lines = raw.splitlines()
        h1 = lines[0].lstrip("# ").strip()
        self.is_bonus = self.dir.parts[0] == "bonus"
        if self.is_bonus:
            self.number = None
            self.key = "bonus-" + self.dir.name
            self.title = h1.split("·", 1)[1].strip()
            self.label = "Bonus"
        else:
            m = re.match(r"Week (\d+) · (.*)", h1)
            self.number = int(m.group(1))
            self.key = f"w{self.number}"
            self.title = m.group(2).strip()
            self.label = f"Week {self.number}"
        self.phase = int(self.dir.parts[0].split("-")[1]) if not self.is_bonus else 0
        # The bold meta line under the title.
        meta_line = next(l for l in lines[1:] if l.strip())
        self.meta_md = meta_line
        parts = [p.strip() for p in meta_line.split(" · ")]
        self.time = ""
        self.skill = ""
        for p in parts:
            if p.startswith("**Skill") :
                self.skill = re.sub(r"^\*\*Skills?:\*\*\s*", "", p)
            elif "min" in p or "session" in p:
                self.time = p
        if self.is_bonus:
            self.fits = re.sub(r"\*\*", "", parts[0])
        body = "\n".join(lines[1:]).split(meta_line, 1)[1]
        # Drop the GitHub prev/next footer: the site has its own.
        body = re.split(r"\n---\n(?=\[)", body)[0]
        self.body_md = body.strip() + "\n"
        self.programs = sorted(self.dir_abs.glob("*.ts"), key=lambda p: (p.name != "main.ts", p.name))
        self.showcase = "Showcase" in self.title or "Grand Finale" in self.title

    @property
    def dir_abs(self):
        return ROOT / self.dir

    def sections(self):
        """Split the body into (heading, markdown) pairs."""
        out = []
        cur = None
        buf = []
        for line in self.body_md.splitlines():
            if line.startswith("## "):
                if cur is not None or buf:
                    out.append((cur, "\n".join(buf)))
                cur, buf = line[3:].strip(), []
            else:
                buf.append(line)
        out.append((cur, "\n".join(buf)))
        return [(h, b) for h, b in out if h or b.strip()]


class Phase:
    def __init__(self, path: pathlib.Path):
        self.dir = path.relative_to(ROOT)
        self.src = (path / "README.md").relative_to(ROOT)
        self.out = self.dir / "index.html"
        self.number = int(path.name.split("-")[1])
        raw = (path / "README.md").read_text(encoding="utf-8")
        self.h1 = raw.splitlines()[0].lstrip("# ").strip()
        self.title = PHASE_SHORT[self.number]
        paras = [p.strip() for p in raw.split("\n\n")[1:] if p.strip()]
        self.intro = paras[0]
        self.weeks = []

    @property
    def range(self):
        return f"Weeks {self.weeks[0].number}–{self.weeks[-1].number}"


def load():
    phases = []
    for p in sorted(ROOT.glob("phase-*")):
        if p.is_dir():
            ph = Phase(p)
            ph.weeks = [Week(w / "README.md") for w in sorted(p.glob("week-*")) if (w / "README.md").exists()]
            phases.append(ph)
    bonus = [Week(b / "README.md") for b in sorted((ROOT / "bonus").glob("*")) if (b / "README.md").exists()]
    weeks = [w for ph in phases for w in ph.weeks]
    return phases, weeks, bonus


# --------------------------------------------------------------------------- code highlighting

TS_TOKEN = re.compile(
    r"(?P<comment>//[^\n]*|/\*.*?\*/)"
    r"|(?P<string>\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)"
    r"|(?P<number>\b\d+(?:\.\d+)?\b)"
    r"|(?P<keyword>\b(?:let|const|function|if|else|for|while|return|true|false|of|in)\b)",
    re.S,
)


def highlight_ts(code):
    out, pos = [], 0
    for m in TS_TOKEN.finditer(code):
        out.append(esc(code[pos:m.start()]))
        kind = m.lastgroup
        out.append(f'<span class="tok-{kind}">{esc(m.group())}</span>')
        pos = m.end()
    out.append(esc(code[pos:]))
    return "".join(out)


def program_box(ts: pathlib.Path):
    code = ts.read_text(encoding="utf-8").rstrip() + "\n"
    anchor = "program-" + slugify(ts.name.replace(".", "-"))
    lines = code.count("\n")
    return f"""
<figure class="program" id="{anchor}">
  <figcaption>
    <span class="program-name">📄 {esc(ts.name)}</span>
    <span class="program-lines">{lines} lines</span>
    <button type="button" class="btn btn-copy" data-copy="{anchor}-code">📋 Copy</button>
  </figcaption>
  <pre><code id="{anchor}-code">{highlight_ts(code)}</code></pre>
  <p class="program-tip">Numbers in <span class="tok-number">orange</span> near the top are your kid's <b>knobs</b>: change them in MakeCode's Blocks view.</p>
</figure>"""


# --------------------------------------------------------------------------- templates

MASCOT = """<svg class="mascot" viewBox="0 0 120 140" role="img" aria-label="A friendly robot waving">
  <line x1="60" y1="8" x2="60" y2="26" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
  <circle cx="60" cy="8" r="7" fill="var(--p5)"/>
  <rect x="22" y="24" width="76" height="56" rx="18" fill="var(--p3)"/>
  <rect x="32" y="34" width="56" height="36" rx="12" fill="#fff"/>
  <circle cx="47" cy="50" r="6" fill="#2b2340"/><circle cx="73" cy="50" r="6" fill="#2b2340"/>
  <circle cx="49" cy="48" r="2" fill="#fff"/><circle cx="75" cy="48" r="2" fill="#fff"/>
  <path d="M50 61 q10 8 20 0" stroke="#2b2340" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <circle cx="16" cy="52" r="6" fill="var(--p1)"/><circle cx="104" cy="52" r="6" fill="var(--p1)"/>
  <rect x="32" y="84" width="56" height="40" rx="12" fill="var(--p2)"/>
  <path d="M60 112 l-9 -9 a5.5 5.5 0 0 1 9 -6 a5.5 5.5 0 0 1 9 6 z" fill="var(--p5)"/>
  <path d="M32 94 q-14 -4 -18 -20" stroke="var(--p2)" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M88 94 q12 6 14 20" stroke="var(--p2)" stroke-width="8" fill="none" stroke-linecap="round"/>
  <rect x="40" y="124" width="12" height="12" rx="4" fill="var(--p4)"/><rect x="68" y="124" width="12" height="12" rx="4" fill="var(--p4)"/>
</svg>"""


def page(out: pathlib.Path, title: str, body: str, *, theme="", description="", body_class="", extra_head=""):
    root = rel(out, pathlib.Path("index.html")).rsplit("index.html", 1)[0]
    asset = lambda p: root + "assets/" + p  # noqa: E731
    link = lambda p: root + p  # noqa: E731
    full_title = title if title == SITE_NAME else f"{title} · {SITE_NAME}"
    nav = [
        ("index.html#calendar", "🗓️", "Weeks"),
        ("start-here.html", "👋", "Start here"),
        ("print/index.html", "🖨️", "Printables"),
        ("parent-guide.html", "🧑‍🧒", "Grown-ups"),
    ]
    nav_html = "".join(
        f'<a href="{link(h)}"><span aria-hidden="true">{i}</span> {t}</a>' for h, i, t in nav
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description or 'A 50-week electronics and robotics calendar for a parent and a curious 6-year-old.')}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🤖%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{asset('style.css')}">
{extra_head}
</head>
<body class="{esc((theme + ' ' + body_class).strip())}">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="{link('index.html')}"><span class="brand-bot" aria-hidden="true">🤖</span> {SITE_NAME}</a>
  <nav aria-label="Main">{nav_html}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="footer">
  <p>{SITE_NAME} · Code: MIT · Activity text: CC BY 4.0 · <a href="https://github.com/{REPO}" target="_blank" rel="noopener">Source on GitHub</a></p>
  <p class="footer-note">Your ticks and drawings are saved only in this browser.</p>
</footer>
<script src="{asset('site.js')}"></script>
</body>
</html>
"""


def render_section(heading, md, ctx):
    """One ## section of a week page as a card."""
    icon, tag = SECTION_ICONS.get(heading, ("📌", None))
    sid = slugify(heading)
    inner = md_to_html(md)
    extra = ""
    if heading in ("Load the program", "Load the programs"):
        extra = "".join(program_box(p) for p in ctx.programs)
    if heading == "Robot Journal":
        inner += f'<div class="journal-pad" data-key="{ctx.key}"></div><div class="print-draw-box" aria-hidden="true"></div>'
    tag_html = f'<span class="sec-tag">{tag}</span>' if tag else ""
    return f"""<section class="sec sec-{sid}" aria-labelledby="{sid}">
  <h2 id="{sid}"><span class="sec-icon" aria-hidden="true">{icon}</span> {esc(heading)} {tag_html}</h2>
  {inner}{extra}
</section>"""


def week_page(w: Week, prev_w, next_w, phase: Phase | None):
    sections = []
    intro = ""
    for heading, md in w.sections():
        md = apply_web_replacements(md)
        if heading is None:
            intro = md_to_html(md)
            continue
        sections.append(render_section(heading, md, w))
    body = rewrite_links("\n".join(sections), w.src, w.out)
    intro = rewrite_links(intro, w.src, w.out)
    root = rel(w.out, pathlib.Path("index.html")).rsplit("index.html", 1)[0]

    if w.is_bonus:
        badge = '<div class="week-badge week-badge-bonus" aria-hidden="true">★</div>'
        chip = f'<a class="chip" href="{root}index.html#bonus">Bonus project</a> <span class="chip chip-soft">{esc(w.fits)}</span>'
    else:
        badge = f'<div class="week-badge" aria-hidden="true">{w.number}</div>'
        chip = f'<a class="chip" href="{rel(w.out, phase.out)}">{PHASE_EMOJI[w.phase]} Phase {w.phase} · {esc(phase.title)}</a>'
        if w.showcase:
            chip += ' <span class="chip chip-soft">🎉 Showcase week</span>'
    meta = []
    if w.time:
        meta.append(f"<span>⏱️ {inline_md(w.time)}</span>")
    if w.skill:
        meta.append(f"<span>🎯 <b>Skill:</b> {esc(w.skill)}</span>")

    def navlink(x, cls, arrow_first):
        if not x:
            return "<span></span>"
        label = f"{x.label}: {esc(x.title)}"
        inner = f"<small>{'← Previous' if arrow_first else 'Next →'}</small><span>{label}</span>"
        return f'<a class="pager-link {cls}" href="{rel(w.out, x.out)}">{inner}</a>'

    pager = f'<nav class="pager" aria-label="Weeks">{navlink(prev_w, "prev", True)}{navlink(next_w, "next", False)}</nav>'
    html_body = f"""
<article class="week" data-week="{w.key}">
  <header class="week-head">
    {badge}
    <div>
      <p class="week-chips">{chip}</p>
      <h1><span class="week-label">{esc(w.label)}</span> {esc(w.title)}</h1>
      <p class="week-meta">{' '.join(meta)}</p>
      <div class="week-actions">
        <button type="button" class="btn btn-done" data-done="{w.key}" aria-pressed="false"><span class="done-off">☐ Mark as done</span><span class="done-on">✅ Done! Great job</span></button>
        <button type="button" class="btn btn-ghost" data-print>🖨️ Print this week</button>
      </div>
    </div>
  </header>
  {intro}
  {body}
  <p class="print-only print-url">Programs and more: {SITE_URL}{w.out.as_posix().replace('index.html', '')}</p>
  {pager}
</article>"""
    theme = "bonus" if w.is_bonus else f"phase-{w.phase}"
    return page(w.out, f"{w.label}: {w.title}", html_body, theme=theme,
                description=f"{w.label} of {SITE_NAME}: {w.title}. Skill: {w.skill}.")


def week_card(w: Week, from_out: pathlib.Path):
    num = "★" if w.is_bonus else str(w.number)
    extra = '<span class="card-flag">🎉 Showcase</span>' if w.showcase else ""
    return f"""<li><a class="week-card" href="{rel(from_out, w.out)}" data-week="{w.key}">
  <span class="card-num">{num}</span>
  <span class="card-text"><b>{esc(w.title)}</b><small>{esc(w.skill)}</small>{extra}</span>
  <span class="card-done" aria-label="done">✓</span>
</a></li>"""


def home_page(phases, weeks, bonus):
    out = pathlib.Path("index.html")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    how = re.search(r"## How it works\n(.*?)\n## ", readme, re.S).group(1)
    how_html = rewrite_links(md_to_html(how), pathlib.Path("README.md"), out)
    phase_blocks = []
    for ph in phases:
        cards = "".join(week_card(w, out) for w in ph.weeks)
        phase_blocks.append(f"""<section class="phase phase-{ph.number}" id="phase-{ph.number}">
  <header class="phase-head">
    <span class="phase-emoji" aria-hidden="true">{PHASE_EMOJI[ph.number]}</span>
    <div>
      <p class="phase-kicker">Phase {ph.number} · {ph.range}</p>
      <h3><a href="{rel(out, ph.out)}">{esc(ph.title)}</a></h3>
      <p>{inline_md(ph.intro)}</p>
    </div>
    <span class="phase-count" data-phase-count="{','.join(w.key for w in ph.weeks)}"></span>
  </header>
  <ol class="week-grid">{cards}</ol>
</section>""")
    bonus_cards = "".join(week_card(b, out) for b in bonus)
    first = weeks[0]
    body = f"""
<section class="hero">
  <div class="hero-text">
    <p class="hero-kicker">50 weeks · 1 robot project a week · ages 6+</p>
    <h1>{SITE_NAME}</h1>
    <p class="hero-lead">Build, play and tinker together. You get things ready; your kid builds, names, tests and makes it their own. <b>No coding experience needed.</b></p>
    <div class="hero-actions">
      <a class="btn btn-big" href="{rel(out, first.out)}" data-continue>🚀 Start week 1</a>
      <a class="btn btn-big btn-ghost" href="start-here.html">👋 Grown-ups: start here</a>
      <a class="btn btn-big btn-ghost" href="print/index.html">🖨️ Printables</a>
    </div>
    <div class="progress" aria-live="polite">
      <div class="progress-bar"><span style="width:0%"></span></div>
      <p class="progress-text">Tick off a week when it's done and watch your robot year fill up!</p>
    </div>
  </div>
  {MASCOT}
</section>

<section class="how card">
  <h2>🧭 How it works</h2>
  {how_html}
  <p class="how-note">Weeks 1–10 need no laptop at all: just LEDs, batteries and motors.</p>
</section>

<h2 class="calendar-title" id="calendar">🗓️ The calendar</h2>
{''.join(phase_blocks)}

<section class="phase bonus" id="bonus">
  <header class="phase-head">
    <span class="phase-emoji" aria-hidden="true">🐭</span>
    <div><p class="phase-kicker">Any time after week 37</p><h3>Bonus projects</h3><p>Extra builds for robot fans who want more.</p></div>
  </header>
  <ol class="week-grid">{bonus_cards}</ol>
</section>

<section class="grownups card" id="grown-ups">
  <h2>🧑‍🧒 For grown-ups</h2>
  <ul class="link-grid">
    <li><a href="start-here.html"><b>👋 Start here</b><small>Set up the laptop in 15 minutes. No coding.</small></a></li>
    <li><a href="parent-guide.html"><b>🧑‍🧒 Parent guide</b><small>How much to hand over, MakeCode tips, AI helpers.</small></a></li>
    <li><a href="materials.html"><b>🛒 Materials</b><small>Shopping list per phase, with prices.</small></a></li>
    <li><a href="safety.html"><b>🦺 Safety</b><small>Coin cells, hot glue, screen time.</small></a></li>
    <li><a href="glossary.html"><b>📖 Glossary</b><small>Every technical word, in plain language.</small></a></li>
    <li><a href="progress.html"><b>✅ Progress checklist</b><small>All 50 weeks on one page.</small></a></li>
    <li><a href="ai/index.html"><b>🧠 AI bridge guide</b><small>Connect your kid's AI to the robot.</small></a></li>
    <li><a href="print/index.html"><b>🖨️ Printables</b><small>Activity book, journal, poster, certificate.</small></a></li>
  </ul>
</section>
"""
    return page(out, SITE_NAME, body, body_class="home")


def phase_page(ph: Phase, prev_ph, next_ph):
    cards = "".join(week_card(w, ph.out) for w in ph.weeks)
    pager_items = []
    pager_items.append(
        f'<a class="pager-link prev" href="{rel(ph.out, prev_ph.out)}"><small>← Previous phase</small><span>{esc(prev_ph.title)}</span></a>'
        if prev_ph else f'<a class="pager-link prev" href="{rel(ph.out, pathlib.Path("index.html"))}"><small>← Back</small><span>The calendar</span></a>')
    pager_items.append(
        f'<a class="pager-link next" href="{rel(ph.out, next_ph.out)}"><small>Next phase →</small><span>{esc(next_ph.title)}</span></a>'
        if next_ph else "<span></span>")
    body = f"""
<section class="phase phase-{ph.number} phase-page">
  <header class="phase-head">
    <span class="phase-emoji" aria-hidden="true">{PHASE_EMOJI[ph.number]}</span>
    <div>
      <p class="phase-kicker">Phase {ph.number} · {ph.range}</p>
      <h1>{esc(ph.title)}</h1>
      <p>{inline_md(ph.intro)}</p>
    </div>
    <span class="phase-count" data-phase-count="{','.join(w.key for w in ph.weeks)}"></span>
  </header>
  <ol class="week-grid">{cards}</ol>
</section>
<nav class="pager" aria-label="Phases">{''.join(pager_items)}</nav>"""
    return page(ph.out, f"Phase {ph.number}: {ph.title}", body, theme=f"phase-{ph.number}")


def doc_page(src_rel: str, out: pathlib.Path, title: str):
    src = pathlib.Path(src_rel)
    text = (ROOT / src).read_text(encoding="utf-8")
    text = apply_web_replacements(text)
    # Drop the trailing "Back to the calendar" link: the top bar has it.
    text = re.sub(r"\n---\s*\n+\[← Back to the calendar\]\([^)]*\)\s*$", "\n", text)
    text = re.sub(r"\n\[← Back to the calendar\]\([^)]*\)\s*$", "\n", text)
    body = rewrite_links(md_to_html(text), src, out)
    body = re.sub(r"<table>", '<div class="table-wrap"><table>', body)
    body = body.replace("</table>", "</table></div>")
    actions = '<p class="doc-actions"><button type="button" class="btn btn-ghost" data-print>🖨️ Print this page</button></p>'
    return page(out, title, f'<article class="doc card">{actions}{body}</article>')


def progress_page(phases, bonus):
    out = pathlib.Path("progress.html")
    groups = []
    for ph in phases + [None]:
        items = ph.weeks if ph else bonus
        name = f"{PHASE_EMOJI[ph.number]} Phase {ph.number} · {esc(ph.title)}" if ph else "🐭 Bonus"
        lis = "".join(
            f'<li><label><input type="checkbox" data-done-box="{w.key}"> <a href="{rel(out, w.out)}">{esc(w.label)}: {esc(w.title)}</a></label></li>'
            for w in items)
        cls = f"phase-{ph.number}" if ph else "bonus"
        groups.append(f'<section class="check-group {cls}"><h2>{name}</h2><ul class="checklist">{lis}</ul></section>')
    body = f"""<article class="doc card">
<p class="doc-actions"><button type="button" class="btn btn-ghost" data-print>🖨️ Print this page</button> <a class="btn btn-ghost" href="print/index.html#poster">🖍️ Fridge poster</a></p>
<h1>✅ Progress</h1>
<p>Tick each week when it's done. Ticks are saved in this browser and show on the calendar. Prefer paper? Print the <a href="print/index.html#poster">fridge poster</a> and let your kid color a circle each week.</p>
{''.join(groups)}
</article>"""
    return page(out, "Progress", body)


# --------------------------------------------------------------------------- printables

def print_page(out, title, body, *, landscape=False, description=""):
    root = rel(out, pathlib.Path("index.html")).rsplit("index.html", 1)[0]
    orient = ' data-orientation="landscape"' if landscape else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {SITE_NAME}</title>
<meta name="description" content="{esc(description)}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🤖%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{root}assets/printables.css">
</head>
<body{orient}>
<div class="screen-bar">
  <a href="index.html">← Printables</a>
  <span>{esc(title)}</span>
  <button type="button" onclick="window.print()">🖨️ Print</button>
</div>
{body}
</body>
</html>
"""


def journal_sheet(w: Week | None):
    if w:
        head = f'<p class="j-kicker">{esc(w.label)} · {esc(w.title)}</p>'
    else:
        head = '<p class="j-kicker">Week ______ · ______________________________</p>'
    return f"""<section class="sheet journal">
  {head}
  <h2>✏️ My Robot Journal</h2>
  <div class="j-draw"><span>Draw your robot here!</span></div>
  <p class="j-line">My robot is called <span class="blank"></span></p>
  <p class="j-line">It can <span class="blank"></span></p>
  <p class="j-line"><span class="blank full"></span></p>
  <div class="j-row">
    <p>How much fun? <span class="stars">☆ ☆ ☆ ☆ ☆</span></p>
    <p>Date <span class="blank short"></span></p>
  </div>
</section>"""


def book_week(w: Week, phase: Phase | None):
    parts = []
    for heading, md in w.sections():
        if heading is None or heading == "Robot Journal":
            continue
        icon, tag = SECTION_ICONS.get(heading, ("📌", None))
        if heading in ("Load the program", "Load the programs"):
            if w.programs:
                names = ", ".join(p.name for p in w.programs)
                inner = (f"<p>A grown-up loads the program ({esc(names)}) from the website: "
                         f"<b>{SITE_URL}{w.dir.as_posix()}/</b>. Each week's page has a big Copy button and the steps.</p>")
            else:
                inner = md_to_html(md)
                inner = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", inner)
        else:
            md = re.sub(r"All words: \[glossary\]\([^)]*\)\.?", "", md)
            md = re.sub(r"Loading words like .*?\n", "", md)
            inner = md_to_html(md)
            inner = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", inner)
        if heading == "You need":
            inner = inner.replace("<li>", '<li class="tick">')
        tag_html = f'<span class="tag">{tag}</span>' if tag else ""
        parts.append(f'<div class="blk blk-{slugify(heading)}"><h3>{icon} {esc(heading)} {tag_html}</h3>{inner}</div>')
    if w.is_bonus:
        kicker = f"Bonus project · {esc(w.fits)}"
        num = "★"
        theme = "bonus"
    else:
        kicker = f"Phase {w.phase} · {esc(phase.title)}"
        num = str(w.number)
        theme = f"phase-{w.phase}"
    meta = " · ".join(x for x in [esc(re.sub(r'\*', '', w.time)), f"Skill: {esc(w.skill)}" if w.skill else ""] if x)
    return f"""<section class="sheet activity {theme}">
  <header class="a-head">
    <div class="a-num">{num}</div>
    <div><p class="a-kicker">{kicker}</p><h2>{esc(w.title)}</h2><p class="a-meta">{meta}</p></div>
    <div class="a-check">Done! <span class="box"></span></div>
  </header>
  {''.join(parts)}
</section>
{journal_sheet(w)}"""


def printables(phases, weeks, bonus):
    d = pathlib.Path("print")
    files = {}
    phase_of = {w.key: ph for ph in phases for w in ph.weeks}

    # ---- Activity book
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    how = re.search(r"## How it works\n(.*?)\n## ", readme, re.S).group(1)
    how = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", how)
    contents = "".join(
        f'<li class="phase-{ph.number}"><b>{PHASE_EMOJI[ph.number]} Phase {ph.number} · {esc(ph.title)}</b> <span>{ph.range}</span></li>'
        for ph in phases) + '<li class="bonus"><b>🐭 Bonus · Robot Mouse</b> <span>after week 37</span></li>'
    sections = [f"""<section class="sheet cover">
  {MASCOT}
  <h1>{SITE_NAME}</h1>
  <p class="cover-sub">My robot activity book</p>
  <p class="cover-name">This book belongs to <span class="blank"></span></p>
  <p class="cover-foot">50 weeks · build, play, talk, level up · {SITE_URL}</p>
</section>
<section class="sheet intro">
  <h2>🧭 How this book works</h2>
  {md_to_html(how)}
  <ul>
    <li><b>Every week has two pages:</b> the activity (for doing it together) and a Robot Journal page (for your kid to draw and write).</li>
    <li><b>Programs</b> (from week 11) are loaded on a laptop from the website. A grown-up does that part; the week's page says where.</li>
    <li><b>Tick the box</b> at the top of each week when it's done, and color a circle on the fridge poster.</li>
  </ul>
  <div class="safety"><b>🦺 Safety first.</b> Coin cells (CR2032) are dangerous if swallowed: grown-ups hold them, tape them in and store them out of reach. Adults handle craft knives, hot glue and wire stripping.</div>
  <h2>🗓️ The year</h2>
  <ol class="toc">{contents}</ol>
</section>"""]
    for ph in phases:
        sections.append(f"""<section class="sheet divider phase-{ph.number}">
  <p class="d-emoji">{PHASE_EMOJI[ph.number]}</p>
  <p class="d-kicker">Phase {ph.number} · {ph.range}</p>
  <h2>{esc(ph.title)}</h2>
  <p>{esc(re.sub(r'[*_`]', '', ph.intro))}</p>
</section>""")
        for w in ph.weeks:
            sections.append(book_week(w, ph))
    for b in bonus:
        sections.append(book_week(b, None))
    files["book.html"] = print_page(d / "book.html", "Activity book", "\n".join(sections),
                                    description="Every week as a printable activity page plus a Robot Journal page.")

    # ---- Blank journal page
    files["journal.html"] = print_page(d / "journal.html", "Robot Journal page", journal_sheet(None),
                                       description="A blank Robot Journal page. Print as many as you like.")

    # ---- Fridge poster
    rows = []
    for ph in phases:
        dots = "".join(
            f'<li><span class="dot">{w.number}</span><small>{esc(w.title)}</small></li>' for w in ph.weeks)
        rows.append(f'<div class="p-row phase-{ph.number}"><h3>{PHASE_EMOJI[ph.number]} {esc(ph.title)}</h3><ol>{dots}</ol></div>')
    files["poster.html"] = print_page(d / "poster.html", "Fridge poster", f"""<section class="sheet poster">
  <header class="p-head">{MASCOT}<div><h1>My Year of Robots</h1><p>Color a circle every time you finish a week!</p></div></header>
  {''.join(rows)}
  <p class="p-name">Robot builder: <span class="blank"></span></p>
</section>""", description="A progress chart for the fridge: 50 circles to color in.")

    # ---- Certificate
    files["certificate.html"] = print_page(d / "certificate.html", "Certificate", f"""<section class="sheet certificate">
  <div class="c-frame">
    <p class="c-medal">🏅</p>
    <h1>Certificate of Robotics</h1>
    <p class="c-small">This certifies that</p>
    <p class="c-name"><span class="blank"></span></p>
    <p class="c-text">built, coded and trained robots for 50 weeks, including LED robots, a scribble bot,
    a micro:bit pet, a line-following car, a guard robot and an AI that learned from examples.</p>
    <div class="c-sign"><p><span class="blank"></span><small>Signed</small></p>{MASCOT}<p><span class="blank"></span><small>Date</small></p></div>
  </div>
</section>""", landscape=True, description="The week 50 certificate, ready to sign.")

    # ---- Grown-ups handbook
    docs = []
    for src_rel, title in [("START-HERE.md", "Start here"), ("PARENT-GUIDE.md", "Parent guide"), ("MATERIALS.md", "Materials"),
                           ("SAFETY.md", "Safety"), ("ai/README.md", "AI bridge guide"), ("GLOSSARY.md", "Glossary")]:
        text = (ROOT / src_rel).read_text(encoding="utf-8")
        text = apply_web_replacements(text)
        text = re.sub(r"\n---\s*\n+\[← Back to the calendar\]\([^)]*\)\s*$", "\n", text)
        text = text.replace("<details>", "<div>").replace("</details>", "</div>")
        text = re.sub(r"<summary>(.*?)</summary>", r"**\1**", text)
        h = rewrite_links(md_to_html(text), pathlib.Path(src_rel), d / "grown-ups.html")
        # In print, show where links go only for real web addresses.
        h = re.sub(r'<a href="(?!https?:)[^"]*"[^>]*>(.*?)</a>', r"\1", h)
        if src_rel == "GLOSSARY.md":
            h = re.sub(r"(<tr>(?:\s*<t[dh]>.*?</t[dh]>){3})\s*<t[dh]>.*?</t[dh]>", r"\1", h, flags=re.S)
        docs.append(f'<section class="sheet doc-sheet">{h}</section>')
    files["grown-ups.html"] = print_page(d / "grown-ups.html", "Grown-ups handbook", f"""<section class="sheet cover small-cover">
  {MASCOT}
  <h1>{SITE_NAME}</h1>
  <p class="cover-sub">Grown-ups handbook</p>
  <p class="cover-foot">Setup, materials, safety and every word explained · {SITE_URL}</p>
</section>""" + "\n".join(docs), description="Start here, parent guide, materials, safety, AI bridge and glossary.")

    # ---- Hub page (uses the normal site layout)
    out = d / "index.html"
    items = [
        ("book", "📚", "Activity book", "Every week on its own page, each followed by a Robot Journal page to draw in. About 110 pages: print it all for a binder, or one week at a time.", "book"),
        ("poster", "🖍️", "Fridge poster", "All 50 weeks as circles. Your kid colors one in after each week.", "poster"),
        ("journal", "✏️", "Robot Journal page", "A blank journal page. Print a stack and keep them in a folder.", "journal"),
        ("certificate", "🏅", "Certificate", "For the Grand Finale in week 50. Landscape, ready to sign.", "certificate"),
        ("grown-ups", "🧑‍🧒", "Grown-ups handbook", "Start here, parent guide, materials, safety, AI bridge and the full glossary.", "grown-ups"),
    ]
    cards = "".join(f"""<li class="print-card" id="{i}">
  <span class="print-icon" aria-hidden="true">{icon}</span>
  <div>
    <h2>{t}</h2><p>{desc}</p>
    <p class="print-links">
      <a class="btn" href="robokids-{f}-a4.pdf" download>⬇️ PDF (A4)</a>
      <a class="btn btn-ghost" href="robokids-{f}-letter.pdf" download>⬇️ PDF (US Letter)</a>
      <a class="btn btn-ghost" href="{f}.html">👀 Open and print</a>
    </p>
  </div>
</li>""" for i, icon, t, desc, f in items)
    hub = f"""<article class="doc">
<header class="print-hero card">
  <h1>🖨️ Printables</h1>
  <p>Paper versions for the kitchen table, the fridge and the car trip. Download a PDF, or open the page and print it from your browser (<b>Ctrl+P</b>, Mac: <b>Cmd+P</b>).</p>
  <p class="small">Any week page also prints nicely on its own: open it and press <b>🖨️ Print this week</b>.</p>
</header>
<ul class="print-grid">{cards}</ul>
<section class="card tips">
  <h2>🖍️ Printing tips</h2>
  <ul>
    <li><b>Black and white is fine.</b> Colors help, but every page works without them.</li>
    <li><b>Print the activity book in parts:</b> in the print dialog, choose <i>Pages</i>. Each week is two pages.</li>
    <li><b>Journal pages</b> look great hole-punched in a binder: by week 50 your kid has a whole robot book.</li>
    <li>Turn on <b>Background graphics</b> in the print dialog for the colored headers.</li>
  </ul>
</section>
</article>"""
    files["index.html"] = page(out, "Printables", hub, body_class="printables-hub")
    return {d / k: v for k, v in files.items()}


# --------------------------------------------------------------------------- main

def main():
    phases, weeks, bonus = load()
    # Start clean, but keep the PDFs (make_pdfs.mjs makes them; they're slow to rebuild).
    if OUT.exists():
        for p in sorted(OUT.rglob("*"), reverse=True):
            if p.is_file() and p.suffix != ".pdf":
                p.unlink()
            elif p.is_dir() and not any(p.iterdir()):
                p.rmdir()
    (OUT / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
    for f in ("style.css", "printables.css", "site.js"):
        shutil.copy(ASSETS_SRC / f, OUT / "assets" / f)
    for f in (ASSETS_SRC / "fonts").glob("*"):
        shutil.copy(f, OUT / "assets" / "fonts" / f.name)

    files = {}
    files[pathlib.Path("index.html")] = home_page(phases, weeks, bonus)
    for i, ph in enumerate(phases):
        files[ph.out] = phase_page(ph, phases[i - 1] if i else None, phases[i + 1] if i + 1 < len(phases) else None)
    phase_of = {w.key: ph for ph in phases for w in ph.weeks}
    for i, w in enumerate(weeks):
        files[w.out] = week_page(w, weeks[i - 1] if i else None, weeks[i + 1] if i + 1 < len(weeks) else None, phase_of[w.key])
    for b in bonus:
        files[b.out] = week_page(b, None, None, None)
    for src_rel, out, title in PAGES:
        files[pathlib.Path(out)] = doc_page(src_rel, pathlib.Path(out), title)
    files[pathlib.Path("progress.html")] = progress_page(phases, bonus)
    cert = pathlib.Path("phase-5-robots-that-learn/week-50-grand-finale-expo/certificate.md")
    if (ROOT / cert).exists():
        files[out_path_for_md(cert)] = doc_page(cert.as_posix(), out_path_for_md(cert), "Certificate")
    files.update(printables(phases, weeks, bonus))

    for path, content in files.items():
        target = OUT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    # Sanity check: every local link points at a file that exists.
    broken = []
    for path in files:
        for href in re.findall(r'href="([^"#:]+)(?:#[^"]*)?"', files[path]):
            if href.endswith(".pdf"):
                continue
            if not (OUT / path).parent.joinpath(href).resolve().exists():
                broken.append(f"{path}: {href}")
    print(f"Built {len(files)} pages into {OUT.relative_to(ROOT)}/")
    if broken:
        print("Broken links:\n  " + "\n  ".join(sorted(set(broken))))
        sys.exit(1)


if __name__ == "__main__":
    main()
