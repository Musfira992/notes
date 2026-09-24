#!/usr/bin/env bash
# Build a single-page Pandoc handbook into docs/ for GitHub Pages.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

mkdir -p docs
BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT

python3 - "$ROOT" "$BUILD_DIR" <<'PY'
import re
import sys
from datetime import date
from pathlib import Path

root = Path(sys.argv[1])
build_dir = Path(sys.argv[2])
summary = (root / "SUMMARY.md").read_text(encoding="utf-8")

def demote_headings(text: str, by: int = 1) -> str:
    """Shift ATX headings down by `by` levels, skipping fenced code blocks."""
    out = []
    in_fence = False
    fence_marker = None
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif stripped.startswith(fence_marker):
                in_fence = False
                fence_marker = None
            out.append(line)
            continue
        if not in_fence:
            m = re.match(r"^(#{1,6})(\s+)", line)
            if m:
                hashes = m.group(1)
                new_level = min(6, len(hashes) + by)
                line = "#" * new_level + m.group(2) + line[m.end() :]
        out.append(line)
    return "".join(out)

def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            rest = text[end + 4 :]
            if rest.startswith("\n"):
                rest = rest[1:]
            return rest
    return text

parts = []
parts.append(
    "---\n"
    "title: \"Technical Notes\"\n"
    "subtitle: \"Genomics, Databricks, software engineering, statistics, and lab techniques\"\n"
    "author: \"Musfira Jamil\"\n"
    f"date: \"{date.today().isoformat()}\"\n"
    "---\n\n"
)
parts.append(
    "Welcome. This handbook collects practical notes and primers across "
    "genomics, Databricks and lakehouse patterns, software engineering for "
    "scientific work, statistics and visualisation, and laboratory data "
    "generation techniques. Use the table of contents to jump by category.\n\n"
    "Content originated as primers on "
    "[musfirajamil.com](https://www.musfirajamil.com/primers) and is maintained "
    "here as Markdown for browsing, study, and republishing.\n\n"
)

# Parse SUMMARY.md: ## Category then * [Title](path)
category_re = re.compile(r"^##\s+(.+)\s*$")
link_re = re.compile(r"^\*\s+\[([^\]]+)\]\(([^)]+)\)\s*$")

current_category = None
note_count = 0
missing = []

for line in summary.splitlines():
    cm = category_re.match(line)
    if cm:
        current_category = cm.group(1).strip()
        parts.append(f"# {current_category}\n\n")
        continue
    lm = link_re.match(line)
    if lm:
        title, rel = lm.group(1), lm.group(2)
        path = root / rel
        if not path.is_file():
            missing.append(rel)
            continue
        body = strip_frontmatter(path.read_text(encoding="utf-8"))
        body = demote_headings(body, by=1)
        # Ensure a blank line before the note body
        if not body.startswith("\n"):
            body = "\n" + body
        if not body.endswith("\n"):
            body += "\n"
        parts.append(body)
        parts.append("\n")
        note_count += 1

if missing:
    raise SystemExit("Missing notes referenced in SUMMARY.md:\n  " + "\n  ".join(missing))
if note_count == 0:
    raise SystemExit("No notes found from SUMMARY.md")

manuscript = build_dir / "manuscript.md"
manuscript.write_text("".join(parts), encoding="utf-8")
print(f"Assembled {note_count} notes into {manuscript}")
PY

# Handbook styles (paper-like, TOC sidebar). Kept next to index.html for Pages.
cat > docs/styles.css << 'CSSEOF'
:root {
  --paper: #faf7f2;
  --ink: #2a2b2f;
  --soft-ink: #3f444a;
  --muted: #6e7680;
  --muted-light: #8f969e;
  --line: #e4dfd6;
  --accent: #0f7a6c;
  --accent-soft: #e6f4f1;
  --code-bg: #f1eee7;
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Times New Roman", serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, Helvetica, Arial, sans-serif;
  --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
}

* { box-sizing: border-box; }

html { background: var(--paper); }

body {
  margin: 0 auto;
  padding: 40px 40px 72px;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--serif);
  font-size: 18.5px;
  line-height: 1.7;
  display: grid;
  grid-template-columns: minmax(220px, 300px) minmax(0, 760px);
  column-gap: 56px;
  align-items: start;
  justify-content: center;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

body > nav#TOC {
  grid-column: 1;
  grid-row: 1 / span 999;
  width: 100%;
  max-height: calc(100vh - 64px);
  overflow: auto;
  position: sticky;
  top: 28px;
  padding: 4px 20px 24px 0;
  margin: 0;
  border-right: 1px solid var(--line);
  font-family: var(--sans);
  font-size: 14.5px;
  line-height: 1.35;
  scrollbar-width: thin;
  scrollbar-color: #cfc9bd transparent;
}

body > nav#TOC::before {
  content: "CONTENTS";
  display: block;
  margin: 0 0 12px 0;
  color: #56606b;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.18em;
}

nav#TOC ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

nav#TOC ul ul {
  padding-left: 14px;
}

nav#TOC a {
  color: var(--muted);
  display: block;
  padding: 3px 0 4px 12px;
  border-left: 3px solid transparent;
  text-decoration: none;
}

nav#TOC a:hover {
  color: var(--accent);
  border-left-color: var(--accent);
}

nav#TOC > ul > li > a {
  color: var(--soft-ink);
  font-weight: 650;
  margin-top: 8px;
}

body > :not(nav#TOC) {
  grid-column: 2;
  width: 100%;
  max-width: 760px;
  min-width: 0;
}

#title-block-header {
  margin: 0 0 40px;
}

h1, h2, h3, h4 {
  line-height: 1.15;
  font-family: var(--serif);
  color: #24252a;
}

h1.title {
  font-size: clamp(2.8rem, 6vw, 4.4rem);
  margin: 0 0 14px;
  font-weight: 800;
}

.subtitle {
  margin: 0 0 28px;
  color: #666c73;
  font-style: italic;
  font-size: 1.25rem;
  line-height: 1.35;
}

.author,
.date {
  display: inline-block;
  width: min(48%, 280px);
  margin: 0 0 4px;
  color: var(--muted);
  font-family: var(--sans);
  font-size: 0.92rem;
  line-height: 1.4;
}

.author::before,
.date::before {
  display: block;
  margin-bottom: 4px;
  color: var(--muted-light);
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.12em;
}

.author::before { content: "AUTHOR"; }
.date::before { content: "UPDATED"; }

/* Category chapters (top-level after title) */
body > h1:not(.title) {
  font-size: 2.15rem;
  margin: 3.2rem 0 1rem;
  padding-top: 1.2rem;
  border-top: 1px solid var(--line);
}

h2 {
  font-size: 1.55rem;
  margin: 2.2rem 0 0.85rem;
  color: #303238;
}

h3 {
  font-size: 1.2rem;
  margin-top: 1.6rem;
  color: #3a3d43;
}

p { margin: 0 0 1.2rem; }

a {
  color: var(--accent);
  text-decoration-thickness: 0.08em;
  text-underline-offset: 0.12em;
}

ul, ol {
  margin: 0 0 1.2rem;
  padding-left: 1.4rem;
}

li { margin: 0.25rem 0; }

blockquote {
  margin: 1.2rem 0;
  padding: 0.2rem 0 0.2rem 1rem;
  border-left: 4px solid var(--line);
  color: var(--soft-ink);
}

code {
  font-family: var(--mono);
  background: var(--code-bg);
  border-radius: 4px;
  padding: 0.05rem 0.28rem;
  font-size: 0.88em;
}

pre {
  background: var(--code-bg);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 0.95rem 1.05rem;
  overflow-x: auto;
  margin: 0 0 1.35rem;
  font-size: 0.86rem;
  line-height: 1.45;
}

pre code {
  background: transparent;
  padding: 0;
  font-size: inherit;
}

hr {
  border: 0;
  border-top: 1px solid var(--line);
  margin: 2rem 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 1.35rem;
  font-size: 0.95rem;
}

th, td {
  border: 1px solid var(--line);
  padding: 0.45rem 0.65rem;
  text-align: left;
}

th {
  background: #f3efe7;
  font-family: var(--sans);
  font-size: 0.85rem;
}

img {
  max-width: 100%;
  height: auto;
}

@media (max-width: 960px) {
  body {
    padding: 22px 16px 48px;
    font-size: 17.5px;
    display: block;
    max-width: 760px;
  }

  body > nav#TOC {
    position: static;
    width: auto;
    max-height: none;
    border-right: none;
    border-bottom: 1px solid var(--line);
    margin: 0 0 22px;
    padding: 0 0 16px;
  }

  h1.title { font-size: 2.6rem; }
  body > h1:not(.title) { font-size: 1.85rem; }
}
CSSEOF

pandoc "$BUILD_DIR/manuscript.md" \
  --from markdown+yaml_metadata_block+fenced_code_blocks+pipe_tables+strikeout \
  --standalone \
  --toc \
  --toc-depth=3 \
  -c styles.css \
  --metadata lang=en-AU \
  -o docs/index.html

# Ensure Pages does not run Jekyll over the static build
: > docs/.nojekyll

echo "Wrote docs/index.html ($(wc -c < docs/index.html) bytes)"
echo "Wrote docs/styles.css and docs/.nojekyll"
