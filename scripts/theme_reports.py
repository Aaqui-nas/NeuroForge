"""Inject the NeuroForge theme into generated HTML reports (htmlcov, graphify)."""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

INJECT = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap');

/* ── NeuroForge theme injection (hue 225) ── */
:root {
  --nf-bg:        hsla(225, 15%, 14%, 1);
  --nf-surface:   hsla(225, 15%, 17%, 1);
  --nf-surface-2: hsla(225, 15%, 21%, 1);
  --nf-surface-3: hsla(225, 15%, 26%, 1);
  --nf-text:        hsla(225, 15%, 95%, 1);
  --nf-text-muted:  hsla(225, 15%, 90%, 0.54);
  --nf-border:      hsla(225, 15%, 90%, 0.12);
  --nf-border-2:    hsla(225, 15%, 90%, 0.32);
  --nf-primary:     #7e56c2;
  --nf-link:        #7e56c2;
  --nf-success:     #4caf50;
  --nf-error:       #ef5350;
  --nf-warning:     #ff9800;
  --nf-font:        'Roboto', -apple-system, sans-serif;
  --nf-font-mono:   'Roboto Mono', 'Courier New', monospace;
}

html, body {
  background: var(--nf-bg) !important;
  color: var(--nf-text) !important;
  font-family: var(--nf-font) !important;
}

h1, h2, h3, h4 { color: var(--nf-text) !important; }
a { color: var(--nf-link) !important; text-decoration: none !important; }
a:hover { opacity: 0.8 !important; }

/* ── coverage.py: <header> element (not #header) ── */
header {
  background: var(--nf-primary) !important;
  color: #fff !important;
  border-bottom: none !important;
}

header h1 { color: #fff !important; font-size: 1rem !important; font-weight: 500 !important; }
header h1 .pc_cov { color: rgba(255,255,255,0.95) !important; }

/* Tabs: Files / Functions / Classes */
header h2 { margin-top: 0.5rem !important; }
header a.button {
  background: rgba(255,255,255,0.15) !important;
  color: rgba(255,255,255,0.87) !important;
  border: none !important;
  border-radius: 4px !important;
  padding: 4px 12px !important;
  text-decoration: none !important;
}
header a.button.current {
  background: rgba(255,255,255,0.3) !important;
  color: #fff !important;
}
header a.button:hover {
  background: rgba(255,255,255,0.22) !important;
  opacity: 1 !important;
}

/* "coverage.py v7.x.x" link in header */
header p.text { color: rgba(255,255,255,0.65) !important; margin: 0.25rem 0 0 !important; }
header a.nav  { color: rgba(255,255,255,0.87) !important; }

/* Filter form (inside header) */
#filter {
  background: rgba(255,255,255,0.15) !important;
  color: #fff !important;
  border: 1px solid rgba(255,255,255,0.3) !important;
  border-radius: 4px !important;
  padding: 4px 8px !important;
}
#filter::placeholder { color: rgba(255,255,255,0.45) !important; }
label[for="hide100"]  { color: rgba(255,255,255,0.75) !important; }
#hide100 { accent-color: #fff !important; }

/* Keyboard help panel */
#help_panel_wrapper img { filter: invert(1) brightness(1.5) !important; }
#help_panel {
  background: var(--nf-surface) !important;
  border: 1px solid var(--nf-border-2) !important;
  color: var(--nf-text) !important;
}
#help_panel p { color: var(--nf-text-muted) !important; }
#help_panel kbd {
  background: var(--nf-surface-2) !important;
  border: 1px solid var(--nf-border-2) !important;
  color: var(--nf-text) !important;
  border-radius: 3px !important;
  padding: 2px 5px !important;
}

/* ── Main index table ── */
#index { background: var(--nf-bg) !important; }

table {
  border-collapse: collapse !important;
  background: var(--nf-surface) !important;
  border: 1px solid var(--nf-border) !important;
}

td, th {
  background: transparent !important;
  color: var(--nf-text) !important;
  border-color: var(--nf-border) !important;
}

tr.tablehead th {
  background: var(--nf-surface-2) !important;
  border-bottom: 2px solid var(--nf-primary) !important;
  color: var(--nf-text-muted) !important;
  font-size: 0.72rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  font-weight: 500 !important;
}

tr.region:hover td { background: hsla(225, 15%, 90%, 0.06) !important; }

tr.total {
  background: var(--nf-surface-2) !important;
  font-weight: 500 !important;
}
tr.total td { color: var(--nf-text) !important; }

/* Coverage % colour per class (coverage.py adds pct-N) */
.pct-96, .pct-97, .pct-98, .pct-99, .pct-100 { color: var(--nf-success) !important;
font-weight: 500 !important; }
.pct-75,  .pct-80,  .pct-85,  .pct-90, .pct-95  { color: var(--nf-warning) !important; }
.pct-0,   .pct-10,  .pct-20,  .pct-30, .pct-40,
.pct-50,  .pct-60,  .pct-70               { color: var(--nf-error)   !important; }

/* Sort arrows */
span.arrows { color: var(--nf-primary) !important; }

/* ── Run info panel (top of source file pages) ── */
.run-info {
  background: var(--nf-surface) !important;
  border: 1px solid var(--nf-border) !important;
  color: var(--nf-text-muted) !important;
}
.run-info th { background: var(--nf-surface-2) !important; }

/* ── Source file view ── */
#source { background: var(--nf-surface) !important; border: 1px solid var(--nf-border) !important; }
.text .n { color: var(--nf-text-muted) !important; font-family: var(--nf-font-mono) !important; }
.text .t { color: var(--nf-text) !important; font-family: var(--nf-font-mono) !important; }

.mis { background: rgba(239, 83, 80, 0.15) !important; }
.run { background: rgba(76, 175, 80, 0.10) !important; }
.par { background: rgba(255, 152,  0, 0.15) !important; }

/* ── Footer ── */
footer > .content {
  border-top: 1px solid var(--nf-border) !important;
  color: var(--nf-text-muted) !important;
  font-size: 0.82rem !important;
}
footer > .content a.nav { color: var(--nf-link) !important; }

/* ── graphify overrides ── */
.node-label { fill: var(--nf-text) !important; }
.link { stroke: var(--nf-border) !important; }
.node circle { stroke: var(--nf-primary) !important; }
svg { background: var(--nf-bg) !important; }
</style>
"""


THEME_MARKER = "NeuroForge theme injection (hue 225)"


def inject(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    if THEME_MARKER in content:
        return
    patched = content.replace("</head>", f"{INJECT}</head>", 1)
    if patched == content:
        patched = INJECT + content
    path.write_text(patched, encoding="utf-8")
    print(f"  themed: {path.relative_to(ROOT)}")


def theme_directory(directory: Path, pattern: str = "*.html") -> None:
    if not directory.exists():
        print(f"  skip (not found): {directory}")
        return
    files = list(directory.rglob(pattern))
    for f in files:
        inject(f)
    print(f"  {len(files)} file(s) in {directory.relative_to(ROOT)}")


if __name__ == "__main__":
    targets = sys.argv[1:] or ["htmlcov", "graphify-out"]
    for target in targets:
        path = ROOT / target
        print(f"Theming {target}…")
        if path.is_file():
            inject(path)
        else:
            theme_directory(path)
